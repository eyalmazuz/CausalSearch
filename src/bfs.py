from typing import Callable, List, Optional

import networkx as nx
from networkx.classes.digraph import DiGraph

from .utils import get_graph_node_pairs, check_duplicates

def expand(graph: DiGraph, criterion: Optional[Callable[[DiGraph], bool]]=None) -> List[DiGraph]:
    neighbors = []
    for (u, v) in get_graph_node_pairs(graph):
        neighbor = graph.copy()
        print(u, v)
        neighbor.add_edge(u, v)

        if criterion and criterion(neighbor) and not nx.utils.graphs_equal(graph, neighbor):
            neighbors.append(neighbor)

    return neighbors


def bfs(graph: DiGraph,
        goal_test: Callable[[DiGraph], bool],
        criterion: Callable[[DiGraph], bool]) -> DiGraph:

    open_list = [graph]
    closed_list: List[DiGraph] = []

    while True:
        if not open_list:
            return None

        node = open_list.pop(0)

        if goal_test(node):
            return node

        neighbors = expand(node, criterion)

        check_duplicates(neighbors, open_list)
        check_duplicates(neighbors, closed_list)

        open_list += neighbors
