#!/usr/bin/env python3

from Utils.VXD import VXD
from datetime import datetime
from lxml import etree
import numpy as np
import os
import sys
import logging

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

if __name__ == "__main__":
  x = create_folders( "test" )
  print( x["mapelites"], x["simulator"], x["experiment"] )
