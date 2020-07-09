#!/usr/bin/env python3

from Utils.VXD import VXD
from datetime import datetime
from lxml import etree
import numpy as np
import os

def create_folders( exp_folder ):
  #get current time in year/month/day/hour/min/sec format
  curr_time = datetime.now().strftime("%y%m%d%H%M%S")
  
  if not os.path.exists( exp_folder ):
    os.mkdir( exp_folder )

  dirs = { "mapelites" : exp_folder + "/exp" + curr_time + "/MEdata",
           "simulator" : exp_folder + "/exp" + curr_time + "/simdata",
           "experiment" : exp_folder + "/exp" + curr_time }
  
  #we want these to throw if anything goes wrong
  os.makedirs( dirs["mapelites"] )
  os.makedirs( dirs["simulator"] )

  return dirs

def minimize_structure( structure ):
  """
  @input: etree element with structure data from vxa file
  @output: minimized numpy array
  Take current structure and get rid of unwanted zeros.
  Also minimize the number of materials.
  """

  x = int( structure.find( "X_Voxels" ).text )
  y = int( structure.find( "Y_Voxels" ).text )
  z = int( structure.find( "Z_Voxels" ).text )

  data = structure.find( "Data" )

  #extract layers from data
  assert z == len( data ), "z dimension of the file is incorrect"
  z_list = []
  for layer in data:
    assert len( layer.text ) == x * y, "x & y dimensions are incorrect"
    x_list = []
    for i in range( x ):
      y_list = []
      for j in range( y ):
        y_list.append( int( layer.text[i*x + j] ) )
      x_list.append( y_list )
    z_list.append( x_list )

  arr = np.array( z_list )
  ind = np.nonzero( arr )

  #created minimized array using
  min_arr =  arr[ind[0][0]:ind[0][-1] + 1, ind[1][0]:ind[1][-1] + 1, ind[2][0]:ind[2][-1] + 1]
  #minimize the number of used materials
  unq = np.unique( min_arr )
  for i,u in zip( range( 1, len( unq ) + 1 ), unq ):
    if i != u:
      min_arr[np.where( min_arr == u )] -= u - i
 
  return min_arr.reshape( min_arr.shape[::-1] )

def vxa_structure_to_vxd( filename, output_f="converted.vxd",
                          minimize=False ):

  try:
    root = etree.parse( filename )
  except OSError:
    print("An error occured! Perhaps filename is wrong?")
    return None
  except:
    print("An unknown error occured! Please try again.")
    return None

  strut = root.find( "*/Structure" )
  strut.set( "replace", "VXA.VXC.Structure" )
 
  if not minimize: 
    with open( output_f, "w" ) as f:
      f.write( etree.tostring( root, pretty_print=True ).decode( "utf-8" ) ) 
  else:
    min_arr = minimize_structure( strut )
    vxd = VXD( min_arr )
    vxd.write_to_xml( output_f )

if __name__ == "__main__":
  x = create_folders( "test" )
  print( x["mapelites"], x["simulator"], x["experiment"] )

  vxa_structure_to_vxd( "snake.vxa" )
