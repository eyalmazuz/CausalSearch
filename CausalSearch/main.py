from argparse import ArgumentParser

import bnlearn as bn

from src.experiment.experiment import run_experiment
from src.search_algorithms.get_model import get_model

def parse_args():
    parser = ArgumentParser()

    parser.add_argument('-sm', '--search-method', type=str, required=True,
                        choices=['BFS', 'DFS', 'A*', 'HC'],
                        help='Search algorithm to find the optimal graph')
    
    parser.add_argument('-sf', '--scoring-function', type=str, choices=['BIC'],
                        help='Scoring function for a given graph')

    parser.add_argument('-c', '--criterion', type=str, choices=['DAG'],
                        help='expansion criteria for search methods')

    parser.add_argument('-gt', '--goal-test', type=str, choices=['Degree One'],
                        help='goal test criteria for search methods')

    parser.add_argument('-d', '--data', type=str, required=True, help='path to the bif graph file')

    parser.add_argument('--epsilon', type=float, help='epsilon threshold for hill climb')
    
    return parser.parse_args()

def main():
    
    args = parse_args()
    
    network = bn.import_DAG(args.data)

    model_params = vars(args)

    search_algorithm = get_model(network, **model_params)

    run_experiment(search_algorithm)

if __name__ == "__main__":
    main()
