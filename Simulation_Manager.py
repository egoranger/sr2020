#!/usr/bin/env python3

from Utils.VXA import VXA
from Utils.VXD import VXD
from evosorocore.Material import Material,default_mat
from lxml import etree
import numpy as np
import subprocess as sub
import os


class SimulationManager( object ):

  def __init__( self, material_cnt, fit, folder_bot, folder_exp_data,
                vxa=VXA(), vxd=VXD(), verbose=False ):
    self.material_cnt = material_cnt
    self.materials = [] #materials need to be created during simulation process 
    #TODO check whether folders exist
    self.folder_bot = folder_bot #folder where .vxa/.vxd files are stored
    self.folder_exp_data = folder_exp_data #folder where experiment data should be stored
    self.fit = fit #fitness function defined by user needs
    self.vxa = vxa
    self.vxd = vxd
    self.verbose = verbose
    self.sim_run = 0
    self.par_cnt = 5 #number of parameters for materials
    self.mult_arr = np.array( [ 1e5, 5, 1, 1.5e3, 1e-4 ] ) #multiplicative constants for mat properties

  def create_materials( self, mat_list ):
    """
    @input: list of numpy arrays
    Create material list using evosorocore Material.
    Expected material properties are following: elastic_mod, uStatic, uDynamic, density, CTE.
    This format is used by VXA class.
    """
    assert self.material_cnt == len( mat_list ), "Number of materials differs from the number of materials expected"
    self.materials = []

    for m in mat_list:
      self.materials.append( Material( m ) )

  def convert_materials( self, mat_arr ):
    """
    @input: mat_arr (np.array)
    @output: list of numpy arrays
    Convert numpy array received by fitness function to more material properties.
    Each array needs to be fixed by some constant. This is defined by self.mult_arr.
    """
    c = self.par_cnt
    assert len( mat_arr.shape ) == 1, "Wrong shape of an array with materials"
    assert mat_arr.shape[0] % c == 0, "Wrong number of parameters, cannot construct list of materials"
    
    mats = []

    for i in range( self.material_cnt ):
      extract = mat_arr[ i*c : c + i*c ] * self.mult_arr
      new_mat = default_mat.copy()
      new_mat["id"] = i
      new_mat["Name"] = "Material " + str( i )
      new_mat["color"] = tuple( np.random.random( 3 ) ) + ( 1, )
      new_mat["Elastic_Mod"] = extract[0]
      new_mat["uStatic"] = extract[1]
      new_mat["uDynamic"] = extract[2]
      new_mat["Density"] = extract[3]
      new_mat["CTE"] = extract[4]

      mats.append( new_mat )

    return mats
  
  def create_base_vxa( self ):
    self.vxa.write_to_xml( self.folder_bot + "/base.vxa", self.materials )
    #TODO create one file where all material data are going to be stored?
    self.vxa.write_to_xml( self.folder_exp_data + "/simdata/sim_run{0}.vxa".format( self.sim_run ),
                           self.materials ) #copy of the vxa file

  def run_simulator( self ):
    """
    @output: data from simulation
    Run voxcraft simulation and get data out of it.  
    """

    #TODO move assert to init? we don't need to do this everytime
    assert os.path.exists("./voxcraft-sim") and os.path.exists("./vx3_node_worker"), "voxcraft-sim or vx3_node_worker do not exist in the current folder_bot"

    if self.verbose:
      print( "running simulation #{0}".format( self.sim_run ) )
    #TODO get rid of the output? /give an option to control the output?

    while True: #taken from voxcraft-evo
      try:
        #TODO for vx3_node_worker when file exists (too quick simulation runs)
        #TODO formatting?
        sub.call( "./voxcraft-sim -i {0} -o {1}/sim_run{2}.xml -f > {1}/sim_run{2}.history"\
                  .format( self.folder_bot, self.folder_exp_data + "/simdata", self.sim_run ), shell=True ) #shell=True shouldn't be normally used
        break
      except IOError:
        if self.verbose:
          print("IOError, resimulating.")
        pass
      except IndexError:
        if self.verbose:
          print("IndexError, resimulating.")
        pass

  def fitness( self, materials ):
    """
    @input: numpy array with materials
    @output: fitness (float), np.array (descriptor)
    """
   
    self.create_materials( self.convert_materials( materials ) )
    self.create_base_vxa()
    self.run_simulator()
    fit, desc = self.fit( self.sim_run )

    if self.verbose:
      print("Fitness for current experiment was:", fit, "and descriptor was:", desc )

    self.sim_run += 1
   
    return fit, desc 

if __name__ == "__main__":
  mgr = SimulationManager( 2, "./demo" )
  mats = mgr.convert_materials( np.array( [0.01,1,1,1,1,0.01,1,1,1,1] ) )
  mgr.create_materials( mats )
  mgr.create_base_vxa()
  mgr.run_simulator()
