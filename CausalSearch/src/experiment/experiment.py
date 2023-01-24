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


def run_experiment(search_method: Search, args, data=None, run=None, debug=False):

    start = time()
    if debug:
        logging.info(f'Start time: {datetime.now()}')

    best_graph = search_method.find(run, debug)

    run_time = time() - start
    if debug:
        logging.info(f'End time: {datetime.now()}')
        logging.info(f'Run took {run_time} seconds')
    print(f'Run took {run_time} seconds')

    if run:
        run.summary['run_time'] = run_time

    if hasattr(search_method, 'data'):
        data = search_method.data
    elif data is None:
        data = generate_fake_data(search_method.network, n=args.number_of_samples)


    if debug:
        logging.info('Logging results')
    log_results(best_graph, search_method.network, data, run, args.save_path, debug)


def log_results(best_graph: DiGraph, network: BayesianNetwork, data, run, save_path: str, debug):

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

    if run:
        run.summary['precision'] = precision
        run.summary['recall'] = recall
        run.summary['bic_score'] = bic_score

def main():
    pass


if __name__ == "__main__":
    main()
