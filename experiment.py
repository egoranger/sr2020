#!/usr/bin/env python3

from Simulation_Manager import SimulationManager as SM
from Utils.fitness import Distance
import map_elites.cvt as cvt_map_elites
import map_elites.common as cm_map_elites

if __name__ == "__main__":

  number_of_materials = 1
  exp_folder = "./experiment_data"
  robot_folder = "./demo"

  dist_fit = Distance( exp_folder )
  simulation = SM( number_of_materials, dist_fit.fitness, robot_folder, exp_folder, True )

  px = cm_map_elites.default_params.copy()
  px["parallel"] = False #voxcraft-sim may allocate quite a bit of memory for one simulation

  #TODO dim_x depends on # of material properties
  cvt_map_elites.compute( 2, 5*number_of_materials, simulation.fitness,
                          n_niches=10, max_evals=2, log_file=open('cvt.dat', 'w'), params=px )  
