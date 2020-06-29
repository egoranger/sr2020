#!/usr/bin/env python3

from evosorocore.Robot import Robot

class VXD( object ):

  def __init__( self ):
    self.root = None

  #TODO
  def write_to_xml( self, path="./bot.vxd" ):
    pass

  def create_header( self ):
    self.root = etree.Element( "VXD" )

#TODO run some tests
if __name__ == "__main__":
  pass
