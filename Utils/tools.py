#!/usr/bin/env python3

from Utils.VXD import VXD
from datetime import datetime
from lxml import etree
import numpy as np
import os
import sys
import logging
from glob import glob
import pickle
import re

def create_folders( exp_folder, time_mark=None ):
  """
  @input: experiment folder, time mark (if we want to use cached data
  @output: dictionary of paths
  """
  #get current time in year/month/day/hour/min/sec format
  curr_time = datetime.now().strftime("%y%m%d%H%M%S") if time_mark is None else time_mark
  
  if not os.path.exists( exp_folder ):
    os.mkdir( exp_folder )

  dirs = { "mapelites" : exp_folder + "/" + curr_time + "/MEdata",
           "simulator" : exp_folder + "/" + curr_time + "/simdata",
           "experiment" : exp_folder + "/" + curr_time }

  if time_mark is not None:
    if not os.path.exists( dirs["mapelites"] ) or not os.path.exists( dirs["simulator"] ):
      raise Exception("Cannot use cached data, {} or {} do not exist!"\
                       .format( dirs["mapelites"], dirs["simulator"] ) )
    return dirs
  
  #we want these to throw if anything goes wrong
  os.makedirs( dirs["mapelites"] )
  os.makedirs( dirs["simulator"] )

  return dirs

def file_stream_handler( filename ):
  """
  @input: filename
  @output: file handler, stream handler
  create file and stream handlers for given filename with predifined formatting
  """
  file_handler = logging.FileHandler( filename )
  stream_handler = logging.StreamHandler( sys.stderr )
  formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
  file_handler.setFormatter(formatter)
  stream_handler.setFormatter(formatter)

  return file_handler, stream_handler

def use_checkpoint( exp_folder, time_mark ):
  """
  @input: experiment folder, time mark (of cached experiment data)
  @output:
  """
  dirs = create_folders( exp_folder, time_mark )

  pickled_data = glob( dirs["mapelites"] + "/*.p" )
  if pickled_data == []:
    raise Exception("No checkpoints found! Nothing to unpickle.")
  pickled_data = sorted( pickled_data, reverse=True )

  for p in pickled_data:
    try:
      with open( p, "rb" ) as f:
        unpickled_data = pickle.load( f )
      print("Successfully unpickled data.")
      last_run = int( re.findall( r'\d+', p.split("/")[-1] )[0] )
      break
    except pickle.UnpicklingError:
      print( "Unpickling error for {}!".format( p ) )
    except EOFError:
      print( "End of file error for {}!".format( p ) )
 
  return unpickled_data, last_run

def check_for_errors( filename ):
  """
  @input: filename
  @output: True if errorless, otherwise False; string - type of error
  """
  with open( filename, "r" ) as f:
    #TODO check for divergence error
    #TODO check whether the file is correct
    #TODO general error
    pass
  pass

def write_to_xml( root, d ):
  """
  @input: etree element, dictionary
  @output: etree element
  recursively create xml from dictionary
  """
  for x,y in d.items():

    sub = etree.SubElement( root, x )

    if isinstance( y, dict ):
      write_to_xml( sub, y )
    else:
      sub.text = str( y )

  return root

def parse_history_file( num ):
  """
  @input: id of sim_run (eg. sim_run3.history, where id is 3)
  @output: 3d numpy array, in 3rd dimension you'll find:
           posx, posy, posz, angledeg, orix, oriy, oriz, voxsize
  """
  brackets = re.compile( '<<<[^<>]*>>>' ) #we will need to get rid of brackets
  arr = []
  with open( "sim_run{}.history".format( num ), 'r' ) as f:
    #history_file = f.read()
    for line in f:
      if line.find( "<<<>>>" ) != -1:
        voxels = brackets.sub( '', line ).split(';') #divide by each voxel
        points = []
        for v in voxels:
          items = v.split(',') #seperate voxel info
          if len( items ) >= 15: #if enough data info is present
            items = [ float( i ) if i else None for i in items ]
            posx, posy, posz = items[0], items[1], items[2]
            angledeg, orix, oriy, oriz = items[3], items[4], items[5], items[6] 
            vox_size = ( items[10] - items[7], items[11] - items[8], items[12] - items[9] )
            points.append( [ posx, posy, posz, angledeg, orix, oriy, oriz ] + list( vox_size ) )
        arr.append( points )

  return np.array( arr )

def get_angle( num ):
  """
  @input: id of sim_run (eg. sim_run3.history, where id is 3)
  @output: angle of given simulation in radians
  """
  arr = parse_history_file( num )

  #suppose first and last element are most furthest
  v1 = np.array( arr[0][0][0:3] ) - np.array( arr[0][-1][0:3] )
  v2 = np.array( arr[-1][0][0:3] ) - np.array( arr[-1][-1][0:3] )
  unit_v1 = v1 / np.linalg.norm( v1 )
  unit_v2 = v2 / np.linalg.norm( v2 )
  dot_product = np.dot( unit_v1, unit_v2 )
  angle = np.arccos( dot_product )

  return angle

if __name__ == "__main__":
  x = create_folders( "test" )
  print( x["mapelites"], x["simulator"], x["experiment"] )
