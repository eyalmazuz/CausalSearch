from argparse import ArgumentParser

import bnlearn as bn

from src.experiment.experiment import run_experiment
from src.search_algorithms.get_model import get_model


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('-sm', '--search-method', type=str, required=True,
                        choices=['BFS', 'DFS', 'UCS', 'A*', 'HC'],
                        help='Search algorithm to find the optimal graph')

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

    network = bn.import_DAG(args.data)

    model_params = {k: v for k, v in vars(args).items() if v}

    save_path = model_params.pop('save_path')

    search_algorithm = get_model(network, **model_params)

    run_experiment(search_algorithm, save_path)


if __name__ == "__main__":
    main()
