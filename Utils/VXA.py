#!/usr/bin/env python3

from Utils.tools import write_to_xml
from evosorocore2.Material import Material as Mat
from evosorocore2.Environment import VXC_Wrapper
from sim_config import simconfig,envconfig
from lxml import etree

class VXA( object ):
  """
  Class to create vxa file with necessary parameters for voxcraft-sim.
  In the specified folder "$path" will be created.
  VXA object does not contain Material details.
  """

  #def __init__( self, sim_params=default_sim.copy(), env_params=default_env.copy() ):
  def __init__( self, sim_params=simconfig.copy(), env_params=envconfig.copy() ):
    self.sim = sim_params
    self.env = env_params
    self.vxc = VXC_Wrapper()

  def write_to_xml( self, path="./base.vxa", materials=[] ):
    """
    Write data to the file specified by the path.
    """

    root = etree.Element( "VXA", Version="1.1" )

    write_to_xml( root, self.sim )
    write_to_xml( root, self.env )
    self.vxc.write_to_xml( root, materials )

    with open( path, "w" ) as f:
      f.write( etree.tostring( root, pretty_print=True ).decode( "utf-8" ) ) #TODO is pretty and decoding necessary?

#run some tests
if __name__ == "__main__":
  vxa = VXA()
  vxa.write_to_xml()

