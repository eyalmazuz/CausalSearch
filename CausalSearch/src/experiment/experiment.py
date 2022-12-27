from time import time
from typing import Any, Callable, List, Optional

import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes.digraph import DiGraph
import pandas as pd
from pgmpy.models.BayesianNetwork import BayesianNetwork # type: ignore

from src.search_algorithms.abstract_search import Search

def run_experiment(search_method: Search):
    
    start = time()

    best_graph = search_method.find()
    
    end = time()
    print(f'Run took {end - start} seconds')

    log_results(best_graph)

    

def log_results(best_graph: DiGraph):

    nx.draw_networkx(best_graph)
    plt.savefig('./result/best.png')

def main():
    pass

if __name__ == "__main__":
    main()
