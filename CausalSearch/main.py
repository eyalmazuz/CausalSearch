from argparse import ArgumentParser
from datetime import datetime
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

import bnlearn as bn
import pandas as pd

from src.experiment.experiment import run_experiment
from src.search_algorithms.get_model import get_model

FORMAT = '%(asctime)s %(message)s'


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('-sm', '--search-method', type=str, required=True,
                        choices=['BFS', 'DFS', 'UCS', 'A*', 'HC'],
                        help='Search algorithm to find the optimal graph')

    parser.add_argument('-ef', '--edge-function', type=str,
                        choices=['ReLU', 'Const', 'None'], default='None',
                        help='Transformation function for the weights of the edges in weighted search')

    parser.add_argument('-sf', '--scoring-function', type=str, choices=['BIC'],
                        default='BIC', help='Scoring function for a given graph')

    parser.add_argument('-c', '--criterion', type=str, choices=['DAG'],
                        help='expansion criteria for search methods')

    parser.add_argument('-gt', '--goal-test', type=str, choices=['Degree One'],
                        help='goal test criteria for search methods')

    parser.add_argument('-n', '--number-of-samples', type=int, default=1000,
                        help='number of data points to generate')

    parser.add_argument('-g', '--graph', type=str, required=True, help='path to the bif graph file')

    parser.add_argument('-d', '--data', type=str, help='path to the csv data file')

    parser.add_argument('--epsilon', type=float, help='epsilon threshold for hill climb')

    parser.add_argument('--save_path', type=str, help='Path to where to save the results')

    parser.add_argument('--debug', help='print helpful debug message', action='store_true')

    return parser.parse_args()


def main():
    args = parse_args()

    debug = args.debug
    del args.debug

    if debug:
        logging.basicConfig(filename=f"logs/{datetime.now()}.log", format=FORMAT, level=logging.DEBUG)
        logging.info(f'Loading graph from: {args.graph}')

    network = bn.import_DAG(args.graph)

    if args.data is not None:
        logging.info(f'Loading csv data from {args.data} for {args.graph}')
        data_path = args.data
        del args.data
        data = pd.read_csv(data_path)
    else:
        data = None

    model_params = {k: v for k, v in vars(args).items() if v}
    if debug:
        logging.info(f'{model_params=}')

    if debug:
        logging.info(f'Will save results to: {args.save_path}')

    if debug:
        logging.info('Creating search algorithm')

    search_algorithm = get_model(network, debug, data=data, **model_params)

    if debug:
        logging.info('Running experiment')
    run_experiment(search_algorithm, args, data=None, debug=debug)


if __name__ == "__main__":
    main()
