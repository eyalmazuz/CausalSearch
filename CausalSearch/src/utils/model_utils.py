from functools import partial
from math import log

import numpy as np
from pgmpy.estimators import StructureScore

from src.utils.goals import connected_degree_one, target_graph
from src.utils.utils import check_is_dag


class BicScore(StructureScore):
    def __init__(self, data, **kwargs):
        super(BicScore, self).__init__(data, **kwargs)

    def local_score(self, variable, parents):
        'Computes a score that measures how much a \
        given variable is "influenced" by a given list of potential parents.'

        # var_states = self.state_names[variable]
        # var_cardinality = len(var_states)
        state_counts = self.state_counts(variable, parents)
        # sample_size = len(self.data)
        # num_parents_states = float(state_counts.shape[1])

        counts = np.asarray(state_counts)
        log_likelihoods = np.zeros_like(counts, dtype=float)

        # Compute the log-counts
        np.log(counts, out=log_likelihoods, where=counts > 0)

        # Compute the log-conditional sample size
        log_conditionals = np.sum(counts, axis=0, dtype=float)
        np.log(log_conditionals, out=log_conditionals, where=log_conditionals > 0)

        # Compute the log-likelihoods
        log_likelihoods -= log_conditionals
        log_likelihoods *= counts

        score = np.sum(log_likelihoods)
        # score -= 0.5 * log(sample_size) * num_parents_states * (var_cardinality - 1)

        return score


def get_scoring_function(fn_name: str, debug):
    if debug:
        print(f'Loading scoring function: {fn_name}')
    if fn_name == 'BIC':
        return BicScore


def get_criterion(criterion: str, debug):
    if debug:
        print(f'Loading criterion function: {criterion}')
    if criterion == 'DAG':
        crit = check_is_dag
    else:
        raise ValueError('Criterion does not exists')
    return crit


def get_goal(test: str, network, debug):
    if debug:
        print(f'Loading goal test function: {test}')
    if test == 'Degree One':
        fn = connected_degree_one
    elif test == 'Target':
        fn = partial(target_graph, network=network)
    else:
        raise ValueError('Goal test does not exists')

    return fn
