#!/usr/bin/env python3

from evosorocore2.Robot import Robot
from lxml import etree
import numpy as np

class VXD( object ):
  """
  Class to create vxd file that contains robot structure (morphology).
  In the specified folder "$path" will be created.
  """
  def __init__( self, morphology=None ):
    self.robot = Robot( morphology ) 

  def write_to_xml( self, path="./bot.vxd" ):
    root = etree.Element( "VXD" )
    self.robot.write_to_xml( root ) 

    with open( path, "w" ) as f:
      f.write( etree.tostring( root, pretty_print=True ).decode( "utf-8" ) ) #TODO is pretty print and decoding necessary?

  def convert_structure( self, structure ):
    """
    @input: etree element with structure data from vxa file
    @output: numpy array
    """
    #get dimensions
    x = int( structure.find( "X_Voxels" ).text )
    y = int( structure.find( "Y_Voxels" ).text )
    z = int( structure.find( "Z_Voxels" ).text )

    
    data = structure.find( "Data" )

    #extract layers from data
    assert z == len( data ), "z dimension of the file is incorrect"
    z_list = []
    for layer in data:
      assert len( layer.text ) == x * y, "x & y dimensions are incorrect"
      y_list = []
      for i in range( y ):
        x_list = []
        for j in range( x ):
          x_list.append( int( layer.text[i*x + j] ) )
        y_list.append( x_list )
      z_list.append( y_list )

    return np.array( z_list )

  def minimize_arr( self, arr, change_mats ):
    """
    @input: numpy array
    @output: minimized numpy array
    Minimize number of materials and get rid of unwanted zeros.
    """
    ind = np.nonzero( arr )

    #created minimized array using
    min_arr =  arr[ind[0][0]:ind[0][-1] + 1, ind[1][0]:ind[1][-1] + 1, ind[2][0]:ind[2][-1] + 1]
    #minimize the number of used materials
    if change_mats:
      unq = np.unique( min_arr )
      unq = unq[ unq != 0 ]
      for i,u in zip( range( 1, len( unq ) + 1 ), unq ):
        if i != u:
          min_arr[np.where( min_arr == u )] -= u - i
 
    return min_arr

  def create_bot_from_vxa( self, filename, minimize=False, change_mats=False ):
    try:
      root = etree.parse( filename )
    except OSError:
      print("An error occured! Perhaps filename is wrong?")
      return False
    except:
      print("An unknown error occured! Please try again.")
      return False

    strut = root.find( "*/Structure" ) if root.find( "*/Structure" ) is not None else root.find( "Structure" )
    if strut is None:
      raise Exception("Cannot find Structure in the vxd file")

    arr = self.convert_structure( strut )   
    if minimize:
      arr = self.minimize_arr( arr, change_mats )
    self.robot = Robot( arr )

    return True

  def create_bot_from_vxc( self, filename, minimize=False, change_mats=False ):
    return self.create_bot_from_vxa( filename, minimize, change_mats )
     
#run some tests
if __name__ == "__main__":
  vxd = VXD()
  vxd.write_to_xml()
