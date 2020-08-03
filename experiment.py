#!/usr/bin/env python3

from Utils.fitness import Distance
from Utils.VXA import VXA
from Utils.tools import create_folders,file_stream_handler,use_checkpoint
from Simulation_Manager import SimulationManager as SM
import map_elites.cvt as cvt_map_elites
import numpy as np
import random
import time
import logging
import argparse
import shutil
from glob import glob
from config import * #import all variables from config

if __name__ == "__main__":

  parser = argparse.ArgumentParser( description='Run mapelites experiment with voxcraft-sim' )
  parser.add_argument( '-m', '--message', help="Print message to logfile" )
  #parse checkpoint as an integer, then convert it to string
  parser.add_argument( '-c', '--checkpoint', help='Use checkpoint, eg. "200717134521"', type=int )

  args = parser.parse_args()

  checkpoint = str( args.checkpoint ) if args.checkpoint else None 
  logmessage = args.message

  #create new seed and set it to randoms
  seed = int( time.time() )
  random.seed( seed )
  np.random.seed( seed )

  #create experiment folders
  dirs = create_folders( exp_folder, checkpoint )

  #copy bot and config file to expfolder
  shutil.copy( "./config.py", dirs["experiment"] )
  vxdfiles = glob( robot_folder + "/*.vxd" )
  for f in vxdfiles:
    shutil.copy( f, dirs["experiment"] )

  #create logger
  logger = logging.getLogger( __name__ ) if logfile else None
  if logger:
    f,s = file_stream_handler( dirs["experiment"] + "/" + logfile )
    logger.addHandler( f )
    logger.addHandler( s )
    logger.setLevel( logging.DEBUG )
    logger.info( ''.join( ['-'] * 30 ) )
    if logmessage is not None:
      logger.info( "User: " + logmessage )

  #save seed and inform about using checkpoint
  if logger:
    logger.info( "Using seed: {0}".format( seed ) )
    logger.info( "mult_arr: {}".format( mult_arr ) )
    logger.info( "shift_arr: {}".format( shift_arr ) )
    logger.info( "ME_arr: {}".format( ME_arr ) )
  if checkpoint and logger:
    logger.info( "Using {} as a checkpoint, using seed above for next runs may not matter."\
                  .format( checkpoint ) )

  #create map elites instance (or use cached one)
  if checkpoint is None:

    vxa = VXA( simconfig, envconfig )

    dist_fit = Distance( dirs["simulator"], dirs["experiment"] + "/" + logfile ) #fitness function based on distance
    simulation = SM( number_of_materials, dist_fit, robot_folder, dirs["experiment"],\
                     mult_arr, shift_arr, ME_arr, vxa,
                     log=dirs["experiment"] + "/" + logfile )
    simulation.calibrate( calibration_runs )

    if logger:
      logger.info("Creating new Map Elites instance")
    ME = cvt_map_elites.mapelites( simulation, n_niches=n_niches,
                                   max_evals=max_evals, params=px,
                                   exp_folder=dirs["mapelites"] + "/",
                                   sim_log_name=dirs["experiment"] + "/" + logfile )

  else:
    if logger:
      logger.info("Loading cached Map Elites instance")
    ME, last_run = use_checkpoint( exp_folder, checkpoint )
    if logger:
      logger.info("Using cached Map Elites instance")

  #run map elites
  if logger:
    logger.info("Running Map Elites now")
  ME.compute( log_file=open(dirs["mapelites"] + "/cvt.dat", 'a' ) )
