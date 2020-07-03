# Summer Research 2020

## Setup

Clone this repo.

If you have evosorocore already installed, we will need to get rid of it.
```console
sr2020@union:~$ sudo pip uninstall evosorocore
```

For now, some folders need to be manually create. These folders are specified in `experiment.py` (exp\_folder and robot\_folder).
```console
sr2020@union:~$ mkdir experiment_data
```

Create some .vxd file(s) in the demo (robot\_folder) folder. You can take a look at the `bot.vxd` to see what .vxd file should look like.

Also, this directory needs to contain `voxcraft-sim` and `vx3_node_worker`. Copy them here from the voxcraft-sim build.

You should be able to run the experiment.

```console
sr2020@union:~$ python experiment.py
```

## Changing properties

You may change some of the properties for simulations. Example usage:
```python
from evosorocore.Environment import default_env

env = default_env.copy()
env["TempPeriod"] = 0.2
```

### `Environment.py`:
```python
default_env = \
    {
        #True or False, use Simulator Force Field as an alternative
        "GravEnabled" : True,
        #a real number in m/s^2, negative means downwards
        "GravAcc" : -9.81,
        #True or False (False will let things fall for ever)
        "FloorEnabled" : True,
        #True or False (this way we can move the voxels)
        "VaryTempEnabled" : True,
        #a real number in degree Celsius (amplitude of temp oscillation)
        "TempAmplitude" : 0,
        #a real number in second (period of temp oscillation)
        "TempPeriod" : 0.1
    }
```
### `Simulator.py`
```python
default_sim = \
    {
        #"FitnessFunction" : "UNDEFINED",
        #0.0 ~ 1.0, how safe do we want to have the time step 
        #1.0 if everything is fine, 0.5 if we want a safer run
        "DtFrac" : 0.9,
        #0.0 ~ 1.0, if we want voxels to jiggle a lot, we use 0.0, if we want to calm down, 1.0
        "BondDampingZ" : 0.1,
        #0.0 ~ 1.0, if we want voxels bouncing on the floor, we use 0.0, otherwise 1.0    
        "ColDampingZ" : 1.0,
        #0.0 ~ 1.0, if we want to dump everything in simulation, we use 1.0, otherwise 0.0
        "SlowDampingZ" : 1.0, 
        #number of seconds to run the experiment
        "StopConditionFormula" : 1,
        #number of steps per which we want to record voxels (e.g. 100 means every 100 steps)
        "RecordStepSize" : 100,
        #True or False, True if want to record voxels, else False
        "RecordVoxel" : True,
        #True or False, True if we want to record voxel links, else False
        "RecordLink" : False,
        #True or False, True if we want voxel collisions, else False
        "EnableCollision" : True,
        #"EnableAttach" : False,
        #"AttachCondition" : "UNDEFINED",
        #integer, number of steps in which there will be a special damping
        "SafetyGuard" : 500,
        #"ForceField" : "UNDEFINED",
        #True or False, True if we want to enable signals, else False
        "EnableSignals" : False,
        #True or False, True if we want to enable Cilia, else False
        "EnableCilia" : False,
        #True or False, True if we want to save position of all voxels
        "SavePositionOfAllVoxels" : False,
        #real number, sometimes we need to count how many pairs of Target voxels are close to each other
        "MaxDistInVoxelLengthsToCountAsPair" : 0
    }
```
### mapelites
```python
default_params = \
    {
        # more of this -> higher-quality CVT
        "cvt_samples": 25000,
        # we evaluate in batches to paralleliez
        "batch_size": 100,
        # proportion of niches to be filled before starting
        "random_init": 0.1,
        # batch for random initialization
        "random_init_batch": 100,
        # when to write results (one generation = one batch)
        "dump_period": 10000,
        # do we use several cores?
        "parallel": True,
        # do we cache the result of CVT and reuse?
        "cvt_use_cache": True,
        # min/max of parameters
        "min": 0,
        "max": 1,
    }
```
