#!/usr/bin/env python3

import numpy as np
from sim_config import simconfig,envconfig
import map_elites.common as cm_map_elites

number_of_materials = 3
mult_arr = np.array( [ 1e6, 5, 1, 1e6, 0.01,
                       1e7, 5, 1, 1e6, 0,
                       1e6, 5, 1, 1e6, -0.01 ] )

shift_arr = np.array( [0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0 ] )

ME_arr = np.array( [ False, False, False, False, False,
                     False, False, False, False, False,
                     False, False, False, False, False ] )

#folders/locations
exp_folder = "./experiment_data"
robot_folder = "./demo"
logfile = "simulation.log"

#number of calibration runs
calibration_runs = 15

#map elites parameters
px = cm_map_elites.default_params.copy()
px["parallel"] = False #voxcraft-sim may allocate quite a bit of memory for one simulation
px["batch_size"] = 20
px["random_init_batch"] = 20
px["dump_period"] = 10 #if batch size is bigger, it will be used as a dump_period instead
px["random_init"] = 0.2

#compute parameters
n_niches=36
max_evals=10000
