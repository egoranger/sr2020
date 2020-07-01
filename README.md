# Summer Research 2020

## Setup

Clone this repo.

If you have evosorocore already installed, we will need to get rid of it.
`sudo pip uninstall evosorocore`

For now, some folders need to be manually create. These folders are specified in `experiment.py` (exp\_folder and robot\_folder).
`mkdir experiment_data`

Create some .vxd file(s) in the demo (robot\_folder) folder. You can take a look at the `bot.vxd` to see what .vxd file should look like.

Also, this directory needs to contain `voxcraft-sim` and `vx3_node_worker`. Copy them here from the voxcraft-sim build.

You should be able to run the experiment.

`python experiment.py`

## Changing properties

You can change some values in `experiment.py`. 
TBD
