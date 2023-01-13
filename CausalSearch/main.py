from argparse import ArgumentParser
from datetime import datetime
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

import bnlearn as bn

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

    parser.add_argument('-d', '--data', type=str, required=True, help='path to the bif graph file')

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
        logging.info(f'Loading graph from: {args.data}')

    network = bn.import_DAG(args.data)

    model_params = {k: v for k, v in vars(args).items() if v}
    if debug:
        logging.info(f'{model_params=}')

    save_path = model_params.pop('save_path')
    if debug:
        logging.info(f'Will save results to: {save_path}')

    if debug:
        logging.info('Creating search algorithm')
    search_algorithm = get_model(network, debug, **model_params)

    if debug:
        logging.info('Running experiment')
    run_experiment(search_algorithm, save_path, debug)


if __name__ == "__main__":
    main()
