from .bfs import BFS
from .dfs import DFS
from .hc import HillClimb

from src.utils.model_utils import get_criterion, get_goal, get_scoring_function


def get_model(network, **kwargs):
    search_method = kwargs.pop('search_method')
    if search_method == 'BFS':
        criterion = get_criterion(kwargs.pop('criterion'))
        goal_test = get_goal(kwargs.pop('goal_test'), network)
        model = BFS(network, criterion=criterion, goal_test=goal_test, **kwargs)

    elif search_method == 'DFS':
        criterion = get_criterion(kwargs.pop('criterion'))
        goal_test = get_goal(kwargs.pop('goal_test'), network)
        model = DFS(network, criterion=criterion, goal_test=goal_test, **kwargs)

    elif search_method == 'HC':
        scoring_function = get_scoring_function(kwargs.pop('scoring_function'))
        model = HillClimb(network, scoring_function=scoring_function, **kwargs)

    else:
        raise ValueError('Search method does not exists')

    return model
