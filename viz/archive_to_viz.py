#!/usr/bin/env python3

import argparse

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
      
if __name__ == "__main__":
  parser = argparse.ArgumentParser( description='Visualize archive data in simulator' )
  parser.add_argument( '-a', '--archive', help="Name of the archive, e.g. -a archive_500.dat", required=True )
  parser.add_argument( '-e', '--experiment', help="Experiment folder location, e.g. -e experiment_data/####", required=True )

  args = parser.parse_args()
  archive = args.archive
  exp_folder = args.experiment
 
  m = match_simulations( archive, exp_folder )
  print( "{} matches:\n{}".format( archive, m ) ) 
