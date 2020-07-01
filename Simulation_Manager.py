#!/usr/bin/env python3

from Utils.VXA import VXA
from Utils.VXD import VXD
from evosorocore.Material import Material
from lxml import etree
import numpy as np
import subprocess as sub
import os


class SimulationManager( object ):

  def __init__( self, material_cnt, fit, folder_bot, folder_exp_data="experiment_data",
                verbose=False ):
    self.material_cnt = material_cnt
    self.materials = [] #materials need to be created during simulation process 
    #TODO check whether folders exist
    self.folder_bot = folder_bot #folder where .vxa/.vxd files are stored
    self.folder_exp_data = folder_exp_data #folder where experiment data should be stored
    self.fit = fit #fitness function defined by user needs
    self.vxa = VXA()
    self.vxd = VXD()
    self.verbose = verbose
    self.sim_run = 0
    self.par_cnt = 5 #number of parameters for materials
    self.mult_arr = np.array( [ 10e7, 5, 1, 1.5e3, 1e-4 ] ) #multiplicative constants for mat properties

  def create_materials( self, mat_list ):
    """
    @input: list of numpy arrays
    Create material list using evosorocore Material.
    Expected material properties are following: elastic_mod, uStatic, uDynamic, density, CTE.
    This format is used by VXA class.
    """
    assert self.material_cnt == len( mat_list ), "Number of materials differs from the number of materials expected"
    self.materials = []

    for m,i in zip( mat_list, range( len( mat_list ) ) ):
      self.materials.append( Material( i, str( i ), m[0], m[1], m[2], m[3], m[4] ) )

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
    
    return [ mat_arr[ i*c : c + i*c ] * self.mult_arr for i in range( self.material_cnt ) ]
  
  def create_base_vxa( self ):
    self.vxa.write_to_xml( self.folder_bot + "/base.vxa", self.materials )

  def run_simulator( self ):
    """
    @output: data from simulation
    Run voxcraft simulation and get data out of it.  
    """

    #TODO move assert to init? we don't need to do this everytime
    assert os.path.exists("./voxcraft-sim") and os.path.exists("./vx3_node_worker"), "voxcraft-sim or vx3_node_worker do not exist in the current folder_bot"

    if self.verbose:
      print("running simulation")
    #TODO get rid of the output? /give an option to control the output?

    while True: #taken from voxcraft-evo
      try:
        #TODO for vx3_node_worker when file exists (too quick simulation runs)
        #TODO formatting?
        sub.call( "./voxcraft-sim -i {0} -o {1}/sim_run{2}.xml -f"\
                  .format( self.folder_bot, self.folder_exp_data, self.sim_run ), shell=True ) #shell=True shouldn't be normally used
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
