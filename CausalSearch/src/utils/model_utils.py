from functools import partial

from pgmpy.estimators import BicScore

from src.utils.goals import connected_degree_one, target_graph
from src.utils.utils import check_is_dag

def get_scoring_function(fn_name: str):
    if fn_name == 'BIC':
        return BicScore

def get_criterion(criterion: str):
    if criterion == 'DAG':
        crit = check_is_dag 
    else:
        raise ValueError('Criterion does not exists')
    return crit

def get_goal(test: str, network):
    if test == 'Degree One':
        fn = connected_degree_one 
    elif test == 'Target':
        fn = partial(target_graph, network=network)
    else:
        raise ValueError('Goal test does not exists')

    return fn
