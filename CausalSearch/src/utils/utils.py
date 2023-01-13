import os
import sys
from typing import Dict, Generator, List, Tuple, Union
import logging
logger = logging.getLogger(__name__)

import bnlearn # type: ignore
import pandas as pd

import networkx as nx
from networkx.classes.digraph import DiGraph

from pgmpy.models.BayesianNetwork import BayesianNetwork  # type: ignore


def generate_fake_data(network: BayesianNetwork, n: int=1000) -> pd.DataFrame:
    return bnlearn.sampling(network, n=n)


def read_graph(graph_path: str, CPD: bool=True) -> Dict[str, Union[BayesianNetwork, pd.DataFrame]]:
    causal_graph = bnlearn.import_DAG(graph_path, CPD)

    return causal_graph


def check_is_dag(graph: DiGraph) -> bool:
    x = nx.is_directed_acyclic_graph(graph)  # type: ignore
    return x


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
