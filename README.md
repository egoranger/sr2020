# Summer Research 2020

## Dependencies

[voxcraft-sim](https://github.com/voxcraft/voxcraft-sim)
python packages: numpy, sklearn, lxml
```console
sr2020@union:~$ pip3 install --user numpy sklearn lxml
```

You can use [voxcraft-viz](https://github.com/voxcraft/voxcraft-viz) to visualize the data.

## Setup

Clone this repo.

Create some .vxd file(s) in the demo (robot\_folder) folder. You can take a look at the `bot.vxd` to see what .vxd file should look like.

Also, this directory needs to contain `voxcraft-sim` and `vx3_node_worker`. Copy them here from the voxcraft-sim build.

You should be able to run the experiment.

```console
sr2020@union:~$ python experiment.py
```

## Changing properties

Checkout the [voxcraft docs](https://gpuvoxels.readthedocs.io/) if you're not sure what the settings are doing.

You may change some of the properties for simulations. Example usage:
```python
from evosorocore2.Environment import default_env

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
        #Is temperature enabled?
        "TempEnabled" : False,
        #True or False (this way we can move the voxels)
        "VaryTempEnabled" : False,
        #degrees of Celsius
        "TempBase" : 25,
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
### `Material.py`
```python
default_mat = \
    {
        #material id
        "id" : 0,
        #material name
        "Name" : "Default name",
        #material color, rgba
        "color" : (1,0,1,1),
        #True if we want voxels of this mat. to be target, else False
        "isTarget" : False,
        #True if we want to measure voxels made by this mat. in all MathTree fcs(), else False
        "isMeasured" : True,
        #True if we don't want this material to move at all, else False
        "Fixed" : False,
        #True if we want attachment happen to this mat., else False
        "Sticky" : False,
        #real number, 0 if we don't want cilia to happen
        "Cilia" : 0,
        #True if this mat. can generate periodic signals, else False
        "isPaceMaker" : False,
        #real number, period between two signal
        "PaceMakerPeriod" : 0,
        #0.0 ~ 1.0, decay ratio of signal propagation in other parts of the body
        "signalValueDecay" : 0.9,
        #real number/sec delay of signal at every stop
        "signalTimeDelay" : 0.03,
        #real number how long does voxel stay inactive after sending signal
        "inactivePeriod" : 0.03,
        #False simple elastic model, True for perfectly elastic mat.
        "MatModel" : False,
        #real number in Pascal, Young's Modulus
        "Elastic_Mod" : 0,
        #real number in Pascal, if stress > threshold -> mat. will fail by fracture
        "Fail_Stress" : 0,
        #real number in kg/m^3, e.g. rubber's density 1.5e+3 kg/m^3
        "Density" : 0,
        #0.0 ~ 0.5
        "Poissons_Ratio" : 0,
        #small real number in 1/degree Celsius
        "CTE" : 0,
        #0.0 ~ 5.0, static frictional coefficient
        "uStatic" : 0,
        #0.0 ~ 1.0, kinetic frictional coefficient
        "uDynamic" : 0,
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
