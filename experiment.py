#!/usr/bin/env python3

from evosorocore2.Simulator import default_sim
from evosorocore2.Environment import default_env
from Utils.fitness import Distance
from Utils.VXA import VXA
from Utils.tools import create_folders,file_stream_handler
from Simulation_Manager import SimulationManager as SM
import map_elites.cvt as cvt_map_elites
import map_elites.common as cm_map_elites
import numpy as np
import random
import time
import logging

if __name__ == "__main__":

  seed = int( time.time() )
  
  random.seed( seed )
  np.random.seed( seed )

  number_of_materials = 3
  mult_arr = np.array( [ 1e6, 5, 1, 1.5e3, 0.1,
                         1e7, 5, 1, 1.5e3, 0,
                         1e6, 5, 1, 1.5e3, -0.1 ] )
  exp_folder = "./experiment_data"
  robot_folder = "./demo"
  logfile = "simulation.log"

  #create experiment folders
  dirs = create_folders( exp_folder )

  #create logger
  logger = logging.getLogger( __name__ )
  f,s = file_stream_handler( dirs["experiment"] + "/" + logfile )
  logger.addHandler( f )
  logger.addHandler( s )
  logger.setLevel( logging.DEBUG )

  #save seed
  logger.info( "Using seed: {0}".format( seed ) )

  #simulator and environment parameters
  sim = default_sim.copy()
  sim["DtFrac"] = 0.5
  sim["RecordStepSize"] = 100
  sim["StopConditionFormula"] = 3
  env = default_env.copy()
  env["TempEnabled"] = True
  env["VaryTempEnabled"] = True
  env["TempAmplitude"] = 14.4714
  env["TempPeriod"] = 0.2
  vxa = VXA( sim, env )

  dist_fit = Distance( dirs["simulator"], dirs["experiment"] + "/" + logfile ) #fitness function based on distance
  simulation = SM( number_of_materials, dist_fit.fitness, robot_folder, dirs["experiment"],\
                   mult_arr, vxa, log=dirs["experiment"] + "/" + logfile )

  #map elites parameters
  px = cm_map_elites.default_params.copy()
  px["parallel"] = False #voxcraft-sim may allocate quite a bit of memory for one simulation
  px["batch_size"] = 10
  px["random_init_batch"] = 10
  px["dump_period"] = 1

  logger.info("Running Map Elites now")
  #TODO dim_x depends on # of material properties
  cvt_map_elites.compute( 2, 5*number_of_materials, simulation.fitness,
                          n_niches=100, max_evals=1000, 
                          log_file=open(dirs["mapelites"] + '/cvt.dat', 'w'), 
                          params=px, exp_folder=dirs["mapelites"] + "/" )  
