#! /usr/bin/env python
#| This file is a part of the pymap_elites framework.
#| Copyright 2019, INRIA
#| Main contributor(s):
#| Jean-Baptiste Mouret, jean-baptiste.mouret@inria.fr
#| Eloise Dalin , eloise.dalin@inria.fr
#| Pierre Desreumaux , pierre.desreumaux@inria.fr
#|
#|
#| **Main paper**: Mouret JB, Clune J. Illuminating search spaces by
#| mapping elites. arXiv preprint arXiv:1504.04909. 2015 Apr 20.
#|
#| This software is governed by the CeCILL license under French law
#| and abiding by the rules of distribution of free software.  You
#| can use, modify and/ or redistribute the software under the terms
#| of the CeCILL license as circulated by CEA, CNRS and INRIA at the
#| following URL "http://www.cecill.info".
#|
#| As a counterpart to the access to the source code and rights to
#| copy, modify and redistribute granted by the license, users are
#| provided only with a limited warranty and the software's author,
#| the holder of the economic rights, and the successive licensors
#| have only limited liability.
#|
#| In this respect, the user's attention is drawn to the risks
#| associated with loading, using, modifying and/or developing or
#| reproducing the software by the user in light of its specific
#| status of free software, that may mean that it is complicated to
#| manipulate, and that also therefore means that it is reserved for
#| developers and experienced professionals having in-depth computer
#| knowledge. Users are therefore encouraged to load and test the
#| software's suitability as regards their requirements in conditions
#| enabling the security of their systems and/or data to be ensured
#| and, more generally, to use and operate it in the same conditions
#| as regards security.
#|
#| The fact that you are presently reading this means that you have
#| had knowledge of the CeCILL license and that you accept its terms.

import math
import numpy as np
import multiprocessing
import logging
import pickle
from Utils.tools import file_stream_handler as fsh

# from scipy.spatial import cKDTree : TODO -- faster?
from sklearn.neighbors import KDTree

from map_elites import common as cm



def add_to_archive(s, centroid, archive, kdt):
    niche_index = kdt.query([centroid], k=1)[1][0][0]
    niche = kdt.data[niche_index]
    n = cm.make_hashable(niche)
    s.centroid = n
    if n in archive:
        if s.fitness > archive[n].fitness:
            archive[n] = s
            return 1
        return 0
    else:
        archive[n] = s
        return 1


# evaluate a single vector (x) with a function f and return a species
# t = vector, function
def evaluate(t):
    z, f = t  # evaluate z with function f
    fit, desc = f(z)
    return cm.Species(z, desc, fit)

#mapelites class so we can create checkpoints while using it
class mapelites( object ):

    def __init__( self, sim_mngr, n_niches=1000, max_evals=1e5,
                  params=cm.default_params, ME_log_file=None,
                  variation_operator=cm.variation, exp_folder="",
                  sim_log_name=None ):
        self.sim_mngr = sim_mngr
        self.n_niches = n_niches
        self.max_evals = max_evals
        self.params = params
        self.variation_operator = variation_operator
        self.exp_folder = exp_folder
        self.sim_log_name = sim_log_name
  
        self.dim_map = self.sim_mngr.get_desc_size()
        self.dim_x = self.sim_mngr.get_feature_space_size()

        self.archive = {} # init archive (empty)
        self.n_evals = 0 # number of evaluations since the beginning
        self.b_evals = 0 # number evaluation since the last dump

    def init_loggers( self ):
        """
        Init loggers as they get ignored when using pickling
        """        

        self.sim_mngr.init_logger()
        
        #setup logging
        sim_log = logging.getLogger( __name__ ) if self.sim_log_name else None
    
        if sim_log:
            f,s = fsh( self.sim_log_name )
            sim_log.addHandler( f )
            sim_log.addHandler( s )
            sim_log.setLevel( logging.DEBUG )   

        return sim_log
 
    # map-elites algorithm (CVT variant)
    def compute( self, log_file=None ):
        """CVT MAP-Elites
           Vassiliades V, Chatzilygeroudis K, Mouret JB. Using centroidal voronoi tessellations to scale up the multidimensional archive of phenotypic elites algorithm. IEEE Transactions on Evolutionary Computation. 2017 Aug 3;22(4):623-30.
    
           Format of the logfile: evals archive_size max mean median 5%_percentile, 95%_percentile
    
        """
        # setup the parallel processing pool
        num_cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool( num_cores )
  
        # create the CVT
        c = cm.cvt( self.n_niches, self.dim_map,
                  self.params['cvt_samples'], self.params['cvt_use_cache'], self.exp_folder )
        kdt = KDTree( c, leaf_size=30, metric='euclidean' )
        cm.write_centroids( c, self.exp_folder )

        sim_log = self.init_loggers()

        # main loop
        while self.n_evals < self.max_evals:
            to_evaluate = []
            # random initialization
            if len( self.archive ) <= self.params['random_init'] * self.n_niches:
  
                if sim_log:
                    sim_log.info("Not enough niches filled, running random")
  
                for i in range( 0, self.params['random_init_batch'] ):
                    x = np.random.uniform( low=self.params['min'], high=self.params['max'],
                                           size=self.dim_x )
                    to_evaluate += [(x, self.sim_mngr.fitness)]
            else:  # variation/selection loop
  
                if sim_log:
                    sim_log.info("Running variation/selection loop")
  
                keys = list( self.archive.keys() )
                # we select all the parents at the same time because randint is slow
                rand1 = np.random.randint( len(keys), size=self.params['batch_size'] )
                rand2 = np.random.randint( len(keys), size=self.params['batch_size'] )
                for n in range(0, self.params['batch_size'] ):
                    # parent selection
                    x = self.archive[keys[rand1[n]]]
                    y = self.archive[keys[rand2[n]]]
                    # copy & add variation
                    z = self.variation_operator(x.x, y.x, self.params)
                    to_evaluate += [(z, self.sim_mngr.fitness)]
            # evaluation of the fitness for to_evaluate
            s_list = cm.parallel_eval(evaluate, to_evaluate, pool, self.params)
            # natural selection
            for s in s_list:
                add_to_archive(s, s.desc, self.archive, kdt)
            # count evals
            self.n_evals += len(to_evaluate)
            self.b_evals += len(to_evaluate)
    
            # write archive and save checkpoint
            if self.b_evals >= self.params['dump_period'] and self.params['dump_period'] != -1:

                if sim_log:
                    sim_log.info("Saving archive_{}.dat".format(self.n_evals))
                    sim_log.info( "[{}/{}]".format( self.n_evals, int( self.max_evals ) ) )

                cm.save_archive( self.archive, self.n_evals, self.exp_folder )
                self.b_evals = 0

                #save checkpoint
                if sim_log:
                    sim_log.info("Creating checkpoint pickled_{:08d}.p".format( self.n_evals ) )
                with open( self.exp_folder + "pickled_{:08d}.p".format( self.n_evals ), "wb" ) as filelog:
                  pickle.dump( self, filelog ) 

            # write log
            if log_file != None:
                fit_list = np.array([x.fitness for x in self.archive.values()])
                log_file.write("{} {} {} {} {} {}\n".format( self.n_evals, len(self.archive.keys()),
                        fit_list.max(), np.mean(fit_list), np.median(fit_list),
                        np.percentile(fit_list, 5), np.percentile(fit_list, 95)))
                log_file.flush()
        cm.save_archive(self.archive, self.n_evals, self.exp_folder)
        return self.archive
