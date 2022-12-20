from time import time
from typing import Any, Callable, List, Optional

import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes.digraph import DiGraph
import pandas as pd
from pgmpy.models.BayesianNetwork import BayesianNetwork # type: ignore

from src.search_algorithms.abstract_search import Search

def run_experiment(network: BayesianNetwork, search_method: Search,
                   criterion: Optional[Callable[[DiGraph], bool]]=None,
                   goal_test: Optional[Callable[[DiGraph], bool]]=None,
                   scoring_function: Optional[Callable[[Any], float]]=None,
                   ):
    
    start = time()
    sm = search_method(network, criterion, goal_test, scoring_function)

    best_graph = sm.find()
    
    end = time()
    print(f'Run took {end - start} seconds')

    log_results(best_graph, network, scoring_function)

    

def log_results(best_graph: DiGraph, network: BayesianNetwork, scoring_function: Optional[Callable[[Any], float]]):

    nx.draw_networkx(best_graph)
    plt.savefig('./best.png')

def main():
    pass

if __name__ == "__main__":
    main()
