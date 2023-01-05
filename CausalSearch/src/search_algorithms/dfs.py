from typing import Callable, List, Optional

import networkx as nx
from networkx.utils import graphs_equal
from networkx.classes.digraph import DiGraph

from src.search_algorithms.abstract_search import Search
from src.utils.utils import get_graph_node_pairs


class DFS(Search):

    def __init__(self,
                 network,
                 criterion,
                 goal_test,
                 **kwargs):
        super(DFS, self).__init__(network, criterion, goal_test)

    def find(self) -> DiGraph:

        graph = nx.DiGraph()
        graph.add_nodes_from(self.network['model'])

        nodes = [graph]

        while True:
            if not nodes:
                return None

            node = nodes.pop(0)

            if self.goal_test(node):
                return node

            neighbors = self.expand(node)

            for neighbor in neighbors:
                if self.goal_test(neighbor):
                    return neighbor

            nodes = neighbors + nodes

    def expand(self, graph: DiGraph) -> List[DiGraph]:
        neighbors = []
        for (u, v) in get_graph_node_pairs(graph):
            neighbor = graph.copy()
            neighbor.add_edge(u, v)

            if self.criterion and self.criterion(neighbor) and not graphs_equal(graph, neighbor):
                neighbors.append(neighbor)

        return neighbors
