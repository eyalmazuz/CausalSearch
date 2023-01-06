from typing import Callable, List, Optional

import networkx as nx
from networkx.classes.digraph import DiGraph

from src.search_algorithms.abstract_search import Search
from src.utils.utils import get_graph_node_pairs


class BFS(Search):

    def __init__(self,
                 network,
                 criterion,
                 goal_test,
                 **kwargs):
        super(BFS, self).__init__(network, criterion, goal_test)

    def find(self) -> DiGraph:

        graph = nx.DiGraph()
        graph.add_nodes_from(self.network['model'])

        open_list = [graph]
        closed_list: List[DiGraph] = []

        while True:
            if not open_list:
                return None

            node = open_list.pop(0)

            if self.goal_test(node):
                return node

            neighbors = self.expand(node)

            for neighbor in neighbors:
                if self.goal_test(neighbor):
                    return neighbor

            neighbors = self.check_duplicates(neighbors, open_list)
            neighbors = self.check_duplicates(neighbors, closed_list)
            open_list += neighbors
            closed_list.append(node)

    def expand(self, graph: DiGraph) -> List[DiGraph]:
        neighbors = []
        for u, v in get_graph_node_pairs(graph):
            neighbor = graph.copy()
            neighbor.add_edge(u, v)

            if self.criterion and self.criterion(neighbor) and neighbor not in neighbors:
                neighbors.append(neighbor)

        return neighbors

    def check_duplicates(self, new_nodes: List[DiGraph], already_expanded: List[DiGraph]) -> List[DiGraph]:
        if len(already_expanded) == 0:
            return new_nodes

        already_expanded_set = set(already_expanded)
        kept = [new_graph for new_graph in new_nodes
                if not any(nx.is_isomorphic(new_graph, exists) for exists in already_expanded_set)]
        return kept
