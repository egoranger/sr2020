#!/usr/bin/env python3

import numpy as np
from evosorocore2.Simulator import default_sim
from evosorocore2.Environment import default_env
import map_elites.common as cm_map_elites

number_of_materials = 3
mult_arr = np.array( [ 1e6, 5, 1, 1e6, 0.01,
                       1e7, 5, 1, 1e6, 0,
                       1e6, 5, 1, 1e6, -0.01 ] )

#folders/locations
exp_folder = "./experiment_data"
robot_folder = "./demo"
logfile = "simulation.log"

#sim config
sim = default_sim.copy()
sim["DtFrac"] = 0.5
sim["RecordStepSize"] = 100
sim["StopConditionFormula"] = 3

#env config
env = default_env.copy()
env["TempEnabled"] = True
env["VaryTempEnabled"] = True
env["TempAmplitude"] = 5 #14.4714
env["TempPeriod"] = 0.2

#map elites parameters
px = cm_map_elites.default_params.copy()
px["parallel"] = False #voxcraft-sim may allocate quite a bit of memory for one simulation
px["batch_size"] = 20
px["random_init_batch"] = 20
px["dump_period"] = 10 #if batch size is bigger, it will be used as a dump_period instead
px["random_init"] = 0.4

#compute parameters
n_niches=25
max_evals=500
