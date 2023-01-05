from datetime import datetime
import os
from time import time
from typing import Any, Callable, List, Optional

import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes.digraph import DiGraph
import pandas as pd
from pgmpy.models.BayesianNetwork import BayesianNetwork # type: ignore
from pgmpy.estimators import BicScore

from src.search_algorithms.abstract_search import Search
from src.utils.utils import generate_fake_data

def run_experiment(search_method: Search, save_path: str):
    
    start = time()

    best_graph = search_method.find()
    
    end = time()
    print(f'Run took {end - start} seconds')

    if hasattr(search_method, 'data'):
        data = search_method.data
    else:
        data = generate_fake_data(search_method.network)

    log_results(best_graph, search_method.network, data, save_path)

    

def log_results(best_graph: DiGraph, network:BayesianNetwork, data, save_path: str):
    
    save_path = os.path.join(save_path, str(datetime.now()))
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)

    # saves an image of the graph
    nx.draw_networkx(best_graph)
    plt.savefig(os.path.join(save_path, 'best_graph.png'))

    # convert the model to networkx DiGraph
    model = network['model']
    goal = nx.DiGraph()

    goal.add_nodes_from(model.nodes)
    goal.add_edges_from(model.edges)

    # calc precision and recall
    shared_edges = set(best_graph.edges) & set(goal.edges)

    precision = len(shared_edges) / len(best_graph.edges)
    recall = len(shared_edges) / len(goal.edges)

    # calculate BIC score
    scorer = BicScore(data)

    bic_score = 0.0
    for node in best_graph:
        bic_score += scorer.local_score(node, best_graph.predecessors(node))

    print(f'Precision: {round(precision, 4)}, Recall: {round(recall, 4)} BIC: {round(bic_score, 4)}')
    
def main():
    pass

if __name__ == "__main__":
    main()
