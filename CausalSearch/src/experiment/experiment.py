from datetime import datetime
import os
from time import time
from typing import Any, Callable, List, Optional
import logging
logger = logging.getLogger(__name__)

import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes.digraph import DiGraph
import pandas as pd
from pgmpy.models.BayesianNetwork import BayesianNetwork  # type: ignore
from pgmpy.estimators import BicScore

from src.search_algorithms.abstract_search import Search
from src.utils.utils import generate_fake_data


def run_experiment(search_method: Search, save_path: str, debug):

    start = time()
    if debug:
        logging.info(f'Start time: {datetime.now()}')

    best_graph = search_method.find(debug)

    end = time()
    if debug:
        logging.info(f'End time: {datetime.now()}')
    logging.info(f'Run took {end - start} seconds')

    if hasattr(search_method, 'data'):
        data = search_method.data
    else:
        data = generate_fake_data(search_method.network)

    if debug:
        logging.info('Logging results')
    log_results(best_graph, search_method.network, data, save_path, debug)


def log_results(best_graph: DiGraph, network: BayesianNetwork, data, save_path: str, debug):

    save_path = os.path.join(save_path, str(datetime.now()))
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)

    if debug:
        logging.info(f'Creating save folder at: {save_path}')

    if debug:
        logging.info('Saving graph')
    # saves an image of the graph
    nx.draw_networkx(best_graph)
    plt.savefig(os.path.join(save_path, 'best_graph.png'))

    if debug:
        logging.info('Calculating metrics')
    # convert the model to networkx DiGraph
    model = network['model']
    goal = nx.DiGraph()

    goal.add_nodes_from(model.nodes)
    goal.add_edges_from(model.edges)

    # calc precision and recall
    shared_edges = set(best_graph.edges) & set(goal.edges)

    if debug:
        logging.info('Calculating Precision')
    precision = len(shared_edges) / len(best_graph.edges)

    if debug:
        logging.info('Calculating Recall')
    recall = len(shared_edges) / len(goal.edges)

    if debug:
        logging.info('Calculating BIC score')
    # calculate BIC score
    scorer = BicScore(data)

    bic_score = 0.0
    for node in best_graph:
        bic_score += scorer.local_score(node, best_graph.predecessors(node))

    print(f'Precision: {round(precision, 4)}, Recall: {round(recall, 4)} BIC: {round(bic_score, 4)}')
    if debug:
        logging.info(f'Precision: {round(precision, 4)}, Recall: {round(recall, 4)} BIC: {round(bic_score, 4)}')


def main():
    pass


if __name__ == "__main__":
    main()
