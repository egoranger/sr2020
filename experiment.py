#!/usr/bin/env python3

from evosorocore2.Simulator import default_sim
from evosorocore2.Environment import default_env
from Utils.fitness import Distance
from Utils.VXA import VXA
from Utils.tools import create_folders
from Simulation_Manager import SimulationManager as SM
import map_elites.cvt as cvt_map_elites
import map_elites.common as cm_map_elites

if __name__ == "__main__":

  #TODO seeds

  number_of_materials = 4
  exp_folder = "./experiment_data"
  robot_folder = "./demo"

  #create experiment folders
  dirs = create_folders( exp_folder )

  #simulator and environment parameters
  sim = default_sim.copy()
  env = default_env.copy()
  vxa = VXA( sim, env )

  dist_fit = Distance( dirs["simulator"] ) #fitness function based on distance
  simulation = SM( number_of_materials, dist_fit.fitness, robot_folder, dirs["experiment"],\
                   vxa, verbose=True )

  #map elites parameters
  px = cm_map_elites.default_params.copy()
  px["parallel"] = False #voxcraft-sim may allocate quite a bit of memory for one simulation

  #TODO dim_x depends on # of material properties
  cvt_map_elites.compute( 2, 5*number_of_materials, simulation.fitness,
                          n_niches=10, max_evals=2, 
                          log_file=open(dirs["mapelites"] + '/cvt.dat', 'w'), 
                          params=px, exp_folder=dirs["mapelites"] + "/" )  
