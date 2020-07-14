#!/usr/bin/env3 python3

from lxml import etree
import numpy as np
import logging
import math
from Utils.tools import file_stream_handler as fsh

class Distance( object ):
  """
  Class to calculate fitness based on distance.
  """

  def __init__( self, exp_folder, log=None ):
    self.exp_folder = exp_folder
    self.log = logging.getLogger( __name__ ) if log else None

    if self.log:
      f,s = fsh( log )
      self.log.addHandler( f )
      self.log.addHandler( s )
      self.log.setLevel( logging.DEBUG )

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
    try:
      root = etree.parse( self.exp_folder + "/sim_run{0}.xml".format( sim_run ) )
    except:
      if self.log:
        self.log.error("There was an error in parsing the xml file: sim_run{0}.xml".format( sim_run ) )
      return np.zeros( (1,3), dtype=np.int8 ), np.zeros( (1,3), dtype=np.int8 )

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

    if math.isnan( avg ):
      if self.log:
        self.log.error("Fitness is NaN! Returning 0 instead.")
      return self.fitness_fake()

    return avg, np.array( [ np.average( vectors[:,:1] ), np.average( vectors[:,1:2] ) ] )

  def fitness_fake( self ):
    """
    @output: zero fitness and desc
    Sometimes the simulation may fail, we may or we may not want to ignore this.
    """
    return 0.0, np.array( [0] * 2 )

if __name__ == "__main__":
  fit = Distance(".")
  print( fit.fitness( 0 ) )
