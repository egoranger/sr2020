#!/usr/bin/env python3

from Utils.VXA import VXA
from Utils.VXD import VXD
from evosorocore.Material import Material
import numpy as np

class SimulationManager( object ):

  def __init__( self, material_cnt, folder ):
    self.material_cnt = material_cnt
    self.materials = [None] * self.material_cnt #TODO this has to be vxa materials
    self.folder = folder
    self.vxa = VXA()
    self.vxd = VXD()

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
    pass

  #TODO fitness to pass to mapelites
  def fitness( self ):
    pass

  #write to file
  #parse materials into Material format

#TODO do some testing
if __name__ == "__main__":
  mgr = SimulationManager( 1, "." )
  mgr.convert_materials( [np.array( [0,1,2,3,4] )] )
  mgr.create_base_vxa()
