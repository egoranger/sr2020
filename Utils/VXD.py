#!/usr/bin/env python3

#NOTE: we are expected to work with our updated version of evosorocore
from evosorocore.Robot import Robot
from lxml import etree

class VXD( object ):
  """
  Class to create vxd file that contains robot structure (morphology).
  In the specified folder "$path" will be created.
  """
  def __init__( self, morphology=None ):
    self.root = None
    self.robot = Robot( morphology ) 

  def write_to_xml( self, path="./bot.vxd" ):
    self.create_header()
    self.robot.write_to_xml( self.root ) 

    with open( path, "w" ) as f:
      f.write( etree.tostring( self.root, pretty_print=True ).decode( "utf-8" ) ) #TODO is pretty print and decoding necessary?

  def create_header( self ):
    self.root = etree.Element( "VXD" )

  #TODO overwrite robot if needed?
  #TODO import info from VXA file?

#run some tests
if __name__ == "__main__":
  vxd = VXD()
  vxd.write_to_xml()
