#!/usr/bin/env python3

from evosorocore2.Simulator import default_sim
from evosorocore2.Environment import default_env
from Utils.fitness import Distance
from Utils.VXA import VXA
from Utils.tools import create_folders,file_stream_handler,use_checkpoint
from Simulation_Manager import SimulationManager as SM
import map_elites.cvt as cvt_map_elites
import map_elites.common as cm_map_elites
import numpy as np
import random
import time
import logging
import argparse

if __name__ == "__main__":

  parser = argparse.ArgumentParser( description='Run mapelites experiment with voxcraft-sim' )
  parser.add_argument( '-m', '--message', help="Print message to logfile" )
  #parse checkpoint as an integer, then convert it to string
  parser.add_argument( '-c', '--checkpoint', help='Use checkpoint, eg. "200717134521"', type=int )

  args = parser.parse_args()

  checkpoint = str( args.checkpoint ) if args.checkpoint else None 
  logmessage = args.message

  seed = int( time.time() )
  
  random.seed( seed )
  np.random.seed( seed )

  number_of_materials = 3
  mult_arr = np.array( [ 1e6, 5, 1, 1e6, 0.1,
                         1e7, 5, 1, 1e6, 0,
                         1e6, 5, 1, 1e6, -0.1 ] )
  exp_folder = "./experiment_data"
  robot_folder = "./demo"
  logfile = "simulation.log"

  #create experiment folders
  dirs = create_folders( exp_folder, checkpoint )

  #create logger
  logger = logging.getLogger( __name__ )
  f,s = file_stream_handler( dirs["experiment"] + "/" + logfile )
  logger.addHandler( f )
  logger.addHandler( s )
  logger.setLevel( logging.DEBUG )
  logger.info( ''.join( ['-'] * 30 ) )
  if logmessage is not None:
    logger.info( "User: " + logmessage )

  #save seed and inform about using checkpoint
  logger.info( "Using seed: {0}".format( seed ) )
  if checkpoint:
    logger.info( "Using {} as a checkpoint, using seed above for next runs may not matter."\
                  .format( checkpoint ) )

  #simulator and environment parameters
  sim = default_sim.copy()
  sim["DtFrac"] = 0.5
  sim["RecordStepSize"] = 100
  sim["StopConditionFormula"] = 3
  env = default_env.copy()
  env["TempEnabled"] = True
  env["VaryTempEnabled"] = True
  env["TempAmplitude"] = 5 #14.4714
  env["TempPeriod"] = 0.2
  vxa = VXA( sim, env )

  dist_fit = Distance( dirs["simulator"], dirs["experiment"] + "/" + logfile ) #fitness function based on distance
  simulation = SM( number_of_materials, dist_fit, robot_folder, dirs["experiment"],\
                   mult_arr, vxa, log=dirs["experiment"] + "/" + logfile )

  #map elites parameters
  px = cm_map_elites.default_params.copy()
  px["parallel"] = False #voxcraft-sim may allocate quite a bit of memory for one simulation
  px["batch_size"] = 20
  px["random_init_batch"] = 20
  px["dump_period"] = 10 #if batch size is bigger, it will be used as a dump_period instead
  px["random_init"] = 0.7

  #create map elites instance (or use cached one)
  if checkpoint:
    logger.info("Loading cached Map Elites instance")
    ME, last_run = use_checkpoint( exp_folder, checkpoint )
    logger.info("Using cached Map Elites instance")
  else:
    logger.info("Creating new Map Elites instance")
    ME = cvt_map_elites.mapelites( simulation, n_niches=25,
                                   max_evals=500, params=px,
                                   exp_folder=dirs["mapelites"] + "/" )

  #run map elites
  logger.info("Running Map Elites now")
  ME.compute( log_file=open(dirs["mapelites"] + "/cvt.dat", 'a' ),
              sim_log_f=dirs["experiment"] + "/" + logfile )
