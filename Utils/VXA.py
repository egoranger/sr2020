#!/usr/bin/env python3

from evosorocore2.Material import Material as Mat
from evosorocore2.Simulator import Sim,default_sim
from evosorocore2.Environment import Env,default_env,VXC_Wrapper
from lxml import etree

class VXA( object ):
  """
  Class to create vxa file with necessary parameters for voxcraft-sim.
  In the specified folder "$path" will be created.
  VXA object does not contain Material details.
  """

  def __init__( self, sim_params=default_sim.copy(), env_params=default_env.copy() ):
    self.sim = Sim( sim_params )
    self.env = Env( env_params )
    self.vxc = VXC_Wrapper()

  def write_to_xml( self, path="./base.vxa", materials=[] ):
    """
    Write data to the file specified by the path.
    """
    root = etree.Element( "VXA", Version="1.1" )

    self.sim.write_to_xml( root )
    self.env.write_to_xml( root )
    self.vxc.write_to_xml( root, materials )

    with open( path, "w" ) as f:
      f.write( etree.tostring( root, pretty_print=True ).decode( "utf-8" ) ) #TODO is pretty and decoding necessary?

#run some tests
if __name__ == "__main__":
  vxa = VXA()
  vxa.write_to_xml()

