#!/usr/bin/env python3


from evosorocore.Material import Material as Mat
from evosorocore.Simulator import Sim
from evosorocore.Environment import Env,VXC_Wrapper
from lxml import etree
import os

class VXA( object ):
  """
  Class to create vxa file with necessary parameters for voxcraft-sim.
  In the specified folder base.vxa will be created.
  """

  def __init__( self ):
    self.root = None
    self.sim = None
    self.vxc = None

  def write_to_xml( self, path="./base.vxa" ):
    """
    Write data to the file specified by the path.
    """
    self.create_header() #override old data
    self.create_sim()
    self.sim.write_to_xml( self.root )

    with open( path, "w" ) as f:
      f.write( etree.tostring( self.root, pretty_print=True ).decode( "utf-8" ) )

  def create_header( self ):
    self.root = etree.Element( "VXA", Version="1.1" )

  #TODO extend parameters
  def create_sim( self ):
    self.sim = Sim() 

  #TODO changing materials... how should this be done, how do we know what material had the biggest impact?

