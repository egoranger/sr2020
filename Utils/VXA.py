#!/usr/bin/env python3

#NOTE: we are expected to work with our updated version of evosorocore
from evosorocore.Material import Material as Mat
from evosorocore.Simulator import Sim
from evosorocore.Environment import Env,VXC_Wrapper
from lxml import etree

class VXA( object ):
  """
  Class to create vxa file with necessary parameters for voxcraft-sim.
  In the specified folder "$path" will be created.
  VXA object does not contain Material details.
  """

  def __init__( self ):
    self.root = None
    self.sim = None
    self.vxc = None

  def write_to_xml( self, path="./base.vxa", materials=[] ):
    """
    Write data to the file specified by the path.
    """
    self.create_header() #override old data
    self.create_sim()
    self.create_vxc()

    self.sim.write_to_xml( self.root )
    self.vxc.write_to_xml( self.root, materials )

    with open( path, "w" ) as f:
      f.write( etree.tostring( self.root, pretty_print=True ).decode( "utf-8" ) ) #TODO is pretty and decoding necessary?

  def create_header( self ):
    self.root = etree.Element( "VXA", Version="1.1" )

  #TODO extend parameters
  def create_sim( self ):
    self.sim = Sim() 

  def create_vxc( self ):
    self.vxc = VXC_Wrapper()

#run some tests
if __name__ == "__main__":
  vxa = VXA()
  vxa.write_to_xml()

