#!/usr/bin/env python3

from Utils.VXA import VXA
from Utils.VXD import VXD
from evosorocore.Material import Material
from lxml import etree
import numpy as np
import subprocess as sub


class SimulationManager( object ):

  def __init__( self, material_cnt, folder, verbose=False ):
    self.material_cnt = material_cnt
    self.materials = [] #materials need to be created during simulation process 
    self.folder = folder #folder where .vxa/.vxd files are stored
    self.vxa = VXA()
    self.vxd = VXD()
    self.verbose = verbose
    self.par_cnt = 5 #number of parameters for materials
    self.mult_arr = np.array( [ 10e7, 5, 1, 1.5e3, 1e-2 ] ) #multiplicative constants for mat properties

  #expect list with np arrays in following format:
  #elastic_mod, friction_static, friction_dynamic, density, CTE (we'll start small)
  def create_materials( self, mat_list ):
    assert self.material_cnt == len( mat_list ), "Number of materials differs from the number of materials expected"
    self.materials = []

    for m,i in zip( mat_list, range( len( mat_list ) ) ):
      self.materials.append( Material( i, str( i ), m[0], m[1], m[2], m[3], m[4] ) )

  def convert_materials( self, mat_arr ):
    c = self.par_cnt
    assert len( mat_arr.shape ) == 1, "Wrong shape of an array with materials"
    assert mat_arr.shape[0] % c == 0, "Wrong number of parameters, cannot construct list of materials"
    
    return [ mat_arr[ i*c : c + i*c ] * self.mult_arr for i in range( self.material_cnt ) ]
  
  def create_base_vxa( self ):
    self.vxa.write_to_xml( self.folder + "/base.vxa", self.materials )

  #TODO run voxcraft-sim
  def run_simulator( self ):
    #TODO check if voxcraft-sim and worker exist in current folder
    #TODO check exceptions
    if self.verbose:
      print("running simulation")
    #TODO get rid of output?
    sub.call( "./voxcraft-sim -i {0} -o test.xml -f".format( self.folder ), shell=True ) #shell=True shouldn't be normally used 
    root = etree.parse( "test.xml" ).getroot()
    fitness = float(root.findall("detail/bot/")[0].text)
    return fitness #TODO change!!

  #TODO fitness to pass to mapelites
  #needs to accept data from mapelites as well as to return fitness and descriptor
  def fitness( self, x ):
   
    self.create_materials( [x] )
    self.create_base_vxa()
    fit = self.run_simulator()
    
    return fit, np.array( [3.14] )

  #write to file
  #parse materials into Material format

#TODO do some testing
if __name__ == "__main__":
  mgr = SimulationManager( 2, "." )
  mats = mgr.convert_materials( np.array( [1,1,1,1,1,1,1,1,1,1] ) )
  mgr.create_materials( mats )
  #mgr.create_base_vxa()
