from argparse import ArgumentParser

import bnlearn as bn

from src.experiment.experiment import run_experiment
from src.search_algorithms.bfs import BFSSearch
from src.utils.utils import check_is_dag
from src.utils.goals import same_graph_goal

def parse_args():
    parser = ArgumentParser()

    parser.add_argument('-sm', '--search-method', type=str, required=True,
                        choices=['BFS', 'DFS', 'A*', 'Hill Climbing'],
                        help='Search algorithm to find the optimal graph')
    
    parser.add_argument('-sf', '--scoring-function', type=str, choices=['BIC'],
                        help='Scoring function for a given graph')

    parser.add_argument('-c', '--criterion', type=str, choices=['DAG'],
                        help='expansion criteria for search methods')

    parser.add_argument('-d', '--data', type=str, required=True, help='path to the bif graph file')
    
    return parser.parse_args()

def main():
    
    parser = parse_args()
    
    network = bn.import_DAG(parser.data)
    goal_test = same_graph_goal(network)

    run_experiment(network, BFSSearch, check_is_dag, goal_test, None)

if __name__ == "__main__":
    main()
