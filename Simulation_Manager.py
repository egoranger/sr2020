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

  #expect list with np arrays in following format: elastic_mod, friction_static, friction_dynamic, density, CTE (we'll start small)
  def convert_materials( self, mat_list ):
    assert self.material_cnt == len( mat_list ), "Number of materials differs from the number of materials expected"
    self.materials = []

    for m,i in zip( mat_list, range( len( mat_list ) ) ):
      self.materials.append( Material( i, str( i ), m[0], m[1], m[2], m[3], m[4] ) )
  
  def create_base_vxa( self ):
    self.vxa.write_to_xml( self.folder + "/base.vxa", self.materials )

  #TODO run voxcraft-sim
  def run_simulator( self ):
    #TODO check if voxcraft-sim and worker exist in current folder
    #TODO check exceptions
    print("running simulation")
    sub.call( "./voxcraft-sim -i {0} -o test.xml -f".format( self.folder ), shell=True ) #shell=True shouldn't be normally used 
    root = etree.parse( "test.xml" ).getroot()
    fitness = float(root.findall("detail/bot/")[0].text)
    return fitness #TODO change!!

  #TODO fitness to pass to mapelites
  #needs to accept data from mapelites as well as to return fitness and descriptor
  def fitness( self, x ):
   
    print("Printing...")
    print( x )
 
    self.convert_materials( [x] )
    self.create_base_vxa()
    fit = self.run_simulator()
    
    return fit, "3.14"

  #write to file
  #parse materials into Material format

#TODO do some testing
if __name__ == "__main__":
  mgr = SimulationManager( 1, "." )
  mgr.convert_materials( [np.array( [0,1,2,3,4] )] )
  mgr.create_base_vxa()
