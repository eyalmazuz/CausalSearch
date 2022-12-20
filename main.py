from argparse import ArgumentParser

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
    
    return parser

def main():
    
    parser = parse_args()


if __name__ == "__main__":
    main()
