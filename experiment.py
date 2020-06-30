#!/usr/bin/env python3

from Simulation_Manager import SimulationManager as SM
import map_elites.cvt as cvt_map_elites
import map_elites.common as cm_map_elites

if __name__ == "__main__":
  simulation = SM( 1, "./demo" )

  px = cm_map_elites.default_params.copy()
  px["parallel"] = False

  cvt_map_elites.compute( 2, 5, simulation.fitness, n_niches=10, max_evals=2, log_file=open('cvt.dat', 'w'), params=px )  
