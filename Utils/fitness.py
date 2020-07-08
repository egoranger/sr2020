#!/usr/bin/env3 python3

from lxml import etree
import numpy as np

class Distance( object ):
  """
  Class to calculate fitness based on distance.
  """

  def __init__( self, exp_folder ):
    #TODO should this be passed to fitness fnc()?
    self.exp_folder = exp_folder

  def parser( self, sim_run ):
    """
    @input: sim_run (int)
    @output: initial center of mass, final center of mass (both np arrays)
    Extract data from xml file using lxml.etree.
    """
    #we are interested in initial and final position of the center of mass
    initial = []
    final = []
    #TODO exceptions?
    root = etree.parse( self.exp_folder + "/sim_run{0}.xml".format( sim_run ) )
    for i in root.findall( "detail/*/initialCenterOfMass" ):
      initial.append( np.array( [ float( j.text ) for j in i  ], dtype=np.longdouble ) )
    for i in root.findall( "detail/*/currentCenterOfMass" ):
      final.append( np.array( [ float( j.text ) for j in i  ], dtype=np.longdouble ) )

    return np.asarray( initial ), np.asarray( final )

  def fitness( self, sim_run ):
    """
    @input: sim_run (int)
    @output: fitness (float), descriptor (np array)
    Calculate fitness based on vector (final - initial) norms, return descriptor
    based on distance traveled in x,y coordinates.
    If there are multiple robot data present, take the average.
    """

    if sim_run is None:
      return self.fitness_fake()

    initial, final = self.parser( sim_run )

    vectors = np.absolute( final[:,:2] - initial[:,:2] )
    vec_sizes = np.linalg.norm( vectors, axis=1 )
    avg = np.average( vec_sizes )

    return avg, np.array( [ np.average( vectors[:,:1] ), np.average( vectors[:,1:2] ) ] )

  def fitness_fake( self ):
    """
    @output: zero fitness and desc
    Sometimes the simulation may fail, we may or we may not want to ignore this.
    """
    return -1, np.array( [0] * 2 )

if __name__ == "__main__":
  fit = Distance(".")
  print( fit.fitness( 0 ) )
