#!/usr/bin/env python3

import argparse
import numpy
import os
import subprocess as sub
import shutil

def find_sim_in_log( sim_log, fitness ):
  """
  @input: sim log location, fitness of experiment
  @output if found, output which sim_run is matched
  """
  
  sim_cnt = -1

  with open( sim_log, 'r' ) as sim_f:
    for line in sim_f:
      if line.count('Running simulation') > 0:
        sim_cnt += 1
      #fitness may be too long, we need to cut it
      elif line.count( fitness[0:12] ) > 0: 
        return sim_cnt

  return -1

def match_simulations( archive_name, exp_folder ):
  """
  @input: archive name, experiment folder location (absolute or relative)
  @output: list of sim run ids that match archive
  """
  #this is how sim folders/logs are usually defined  
  MEdata = exp_folder + "/MEdata/" + archive_name
  sim_log = exp_folder + "/simulation.log"
  
  matches = []

  with open( MEdata, 'r' ) as me_f:
    for line in me_f:
      info = line.strip().split(' ')
      fit = info[0]
      sim = find_sim_in_log( sim_log, fit )

      matches.append( sim if sim != -1 else "Not found" )

  return matches

def rerun_simulation( exp_folder, matches ):
  """
  @input: archive name, voxcraft-sim and vx3_node_worker location,
          number of material properties used
  Create new folder with reran experiments.
  """

  new_folder = "./rerun"

  if not os.path.exists( new_folder ):
    os.mkdir( new_folder )
  else:
    print("Folder exists, some files may be overriden.")
  
  for m in matches:
    shutil.copy( "{}/simdata/sim_run{}.vxa".format( exp_folder, m ), 
                 "{}/base.vxa".format( exp_folder ) )
    sub.call( "./voxcraft-sim -i {0} -o {1}/sim_run{2}.xml -f > {1}/sim_run{2}.history"\
              .format( exp_folder, new_folder, m ), shell=True )
    print( "Reran {}!".format( m ) )

  
  if os.path.exists( "{}/base.vxa".format( exp_folder ) ):
    os.remove( "{}/base.vxa".format( exp_folder ) )

  print("Done!")
      
if __name__ == "__main__":
  parser = argparse.ArgumentParser( description='Visualize archive data in simulator' )
  parser.add_argument( '-a', '--archive', help="Name of the archive, e.g. -a archive_500.dat", required=True )
  parser.add_argument( '-e', '--experiment', help="Experiment folder location, e.g. -e experiment_data/####", required=True )
  parser.add_argument( '-r', '--rerun', help="Rerun given archive, this may be needed if for example the history files\
                                              are incomplete.", type=bool, default=False ) #type bool?

  args = parser.parse_args()
  archive = args.archive
  exp_folder = args.experiment
  rerun = args.rerun

  m = match_simulations( archive, exp_folder )
  print( "{} matches:\n{}".format( archive, m ) ) 
  if rerun:
    print( "Rerunning archive simulations." )
    rerun_simulation( exp_folder, m )
