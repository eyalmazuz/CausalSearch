import os
import sys
from typing import Dict, Generator, List, Tuple, Union

import bnlearn # type: ignore
import pandas as pd

import networkx as nx
from networkx.classes.digraph import DiGraph

from pgmpy.estimators import BicScore
from pgmpy.models.BayesianNetwork import BayesianNetwork # type: ignore

def generate_fake_data(network: BayesianNetwork, n: int=100) -> pd.DataFrame:
    return bnlearn.sampling(network, n=n)

def read_graph(graph_path: str, CPD: bool=True) -> Dict[str, Union[BayesianNetwork, pd.DataFrame]]:
    causal_graph = bnlearn.import_DAG(graph_path, CPD)

    return causal_graph

def check_is_dag(graph: DiGraph) -> bool:
    x = nx.is_directed_acyclic_graph(graph) # type: ignore
    return x

def get_scoring_function(fn_name):
    if fn_name == 'BIC':
        return BicScore

def check_duplicates(new_nodes: List[DiGraph], already_expanded: List[DiGraph]) -> List[DiGraph]:
    kept = []
    for to_be_added_graph in new_nodes:
        for graph in already_expanded:
            if not nx.utils.graphs_equal(to_be_added_graph, graph):
                kept.append(to_be_added_graph)

    return kept

def get_graph_node_pairs(graph: DiGraph) -> Generator[Tuple[str, str], None, None]:
    for u in graph:
        for v in graph:
            if u != v and v not in graph[u]:
                yield (u, v)

def main(graph_path):
    causal_graph = read_graph(graph_path)

    print(causal_graph)
    print(type(causal_graph))
    print(type(causal_graph['adjmat']))
    edges = causal_graph['model'].edges()

    print(edges)

if __name__ == "__main__":
    main(sys.argv[1])