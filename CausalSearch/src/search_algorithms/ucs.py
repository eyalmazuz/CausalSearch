import heapq
from typing import Callable, List, Optional

import networkx as nx
from networkx.utils import graphs_equal
from networkx.classes.digraph import DiGraph

from src.search_algorithms.abstract_search import Search
from src.utils.utils import get_graph_node_pairs, generate_fake_data


class UCS(Search):

    def __init__(self,
                 network,
                 criterion,
                 goal_test,
                 scoring_function,
                 n=1000,
                 **kwargs):
        super(UCS, self).__init__(network, criterion, goal_test)

        self.n = n
        self.data = generate_fake_data(network, n)
        self.scorer = scoring_function(self.data)

    def find(self) -> DiGraph:

        graph = nx.DiGraph()
        graph.add_nodes_from(self.network['model'])

        open_list = []
        heapq.heappush(open_list, (0, graph))
        closed_list: List[DiGraph] = []

        while True:
            if not open_list:
                return None

            cost, cur_graph = heapq.heappop(open_list)
            node_bic = 0.0
            for node in cur_graph:
                node_bic += self.scorer.local_score(node, cur_graph.predecessors(node))

            if self.goal_test(cur_graph):
                return node

            neighbors = self.expand(node)

            for neighbor in neighbors:
                if self.goal_test(neighbor):
                    return neighbor

            nn = []
            for neighbor in neighbors:
                neighbor_bic = 0.0
                for node in neighbor:
                    neighbor_bic += self.scorer.local_score(node, neighbor.predecessors(node))

                heapq.heappush(nn, (node_bic - neighbor_bic, neighbor))

            neighbors = self.check_duplicates(nn, open_list)
            neighbors = self.check_duplicates(nn, closed_list)

            open_list += neighbors

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

        kept = []
        for new_graph in new_nodes:
            for exists in already_expanded:
                if not nx.utils.graphs_equal(new_graph, exists):
                    kept.append(new_graph)

        return kept
