from .bfs import BFS
from .dfs import DFS
from .ucs import UCS
from .hc import HillClimb
import logging
logger = logging.getLogger(__name__)

from src.utils.model_utils import get_criterion, get_goal, get_scoring_function, get_edge_function


def get_model(network, debug, data=None, **kwargs):
    search_method = kwargs.pop('search_method')
    if debug:
        logging.info(f'Loading search method: {search_method}')
    if search_method == 'BFS':
        criterion = get_criterion(kwargs.pop('criterion'), debug)
        goal_test = get_goal(kwargs.pop('goal_test'), network, debug)
        model = BFS(network, criterion=criterion, goal_test=goal_test, **kwargs)

    elif search_method == 'DFS':
        criterion = get_criterion(kwargs.pop('criterion'), debug)
        goal_test = get_goal(kwargs.pop('goal_test'), network, debug)
        model = DFS(network, criterion=criterion, goal_test=goal_test, **kwargs)

    elif search_method == 'UCS':
        criterion = get_criterion(kwargs.pop('criterion'), debug)
        goal_test = get_goal(kwargs.pop('goal_test'), network, debug)
        scoring_function = get_scoring_function(kwargs.pop('scoring_function'), debug)
        edge_function = get_edge_function(kwargs.pop('edge_function'), debug)
        model = UCS(network, criterion=criterion, goal_test=goal_test, scoring_function=scoring_function,
                    edge_function=edge_function, data=data, **kwargs)

    elif search_method == 'HC':
        scoring_function = get_scoring_function(kwargs.pop('scoring_function'), debug)
        model = HillClimb(network, scoring_function=scoring_function, data=data, **kwargs)

    else:
        raise ValueError('Search method does not exists')

    return model
