from typing import List
import logging
logger = logging.getLogger(__name__)

import networkx as nx
import numpy as np
from networkx.classes.digraph import DiGraph

from src.search_algorithms.abstract_search import Search
from src.utils.utils import get_graph_node_pairs, generate_fake_data


class UCS(Search):

    def __init__(self,
                 network,
                 criterion,
                 goal_test,
                 scoring_function,
                 edge_function,
                 n=1000,
                 **kwargs):
        super(UCS, self).__init__(network, criterion, goal_test)

        self.n = n
        self.data = generate_fake_data(network, n)
        self.scorer = scoring_function(self.data)
        self.edge_function = edge_function

    def find(self, debug=False) -> DiGraph:

        graph = nx.DiGraph()
        graph.add_nodes_from(self.network['model'])

        open_list = []
        start_bic = 0.0
        for node in graph:
            start_bic -= self.scorer.local_score(node, graph.predecessors(node))
        open_list.append((start_bic, graph))
        closed_list: List[DiGraph] = []
        if debug:
            logging.debug(f'Initial BIC: {start_bic=}')

        i = 0
        while open_list:
            i += 1
            if debug:
                logging.debug(f'{len(open_list)=}, {len(closed_list)=}')
            best, graph = float('inf'), None
            for (cost, cur_graph) in open_list:
                if cost <= best:
                    best = cost
                    graph = cur_graph

            if graph is not None:
                open_list.remove((cost, cur_graph))

            cost, cur_graph = best, graph
            if debug:
                logging.debug(f'Best Graph at iteration {i=} {cost=}, {cur_graph=}')

            if self.goal_test(cur_graph):
                return cur_graph

            neighbors = self.expand(cur_graph, closed_list)
            if debug:
                logging.debug(f'Iteration {i=} has {len(neighbors)=} new neighbors')

            for neighbor_graph in neighbors:
                if self.goal_test(neighbor_graph):
                    return neighbor_graph

            for neighbor_graph in neighbors:
                neighbor_bic = 0.0
                for node in neighbor_graph:
                    neighbor_bic -= self.scorer.local_score(node, neighbor_graph.predecessors(node))

                # neighbor_cost = np.minimum(neighbor_bic - cost, 0)
                neighbor_cost = self.edge_function(neighbor_bic - cost)
                if debug:
                    logging.debug(f'New neighbor BIC Before: {(neighbor_bic - cost)=} After: {neighbor_cost=}')

                found = False
                visited, score = None, 0
                for i, (score, visited) in enumerate(open_list):
                    if nx.utils.graphs_equal(neighbor_graph, visited):
                        found = True
                        break

                if found:
                    if debug:
                        logging.debug(f'Found existing graph {visited=} in open list with score {score=}')
                    if neighbor_cost < score:
                        if debug:
                            logging.debug(f'Removing best graph with cost {score=} with graph with cost {neighbor_cost=}')
                        open_list.remove((score, visited))
                        logging.debug(open_list)

                        open_list.append((neighbor_cost, neighbor_graph))

                else:
                    logging.debug(open_list)
                    if debug:
                        logging.debug(f'No existing graph found adding graph to open list {(neighbor_cost, neighbor_graph)=}')

                    open_list.append((neighbor_cost, neighbor_graph))

            closed_list.append(cur_graph)

    def expand(self, graph: DiGraph, closed_list: List[DiGraph]) -> List[DiGraph]:
        neighbors = []
        for u, v in get_graph_node_pairs(graph):
            neighbor = graph.copy()
            neighbor.add_edge(u, v)

            if (self.criterion and self.criterion(neighbor) and
               neighbor not in neighbors and
               not any(nx.utils.graphs_equal(neighbor, exists) for exists in closed_list)):
                neighbors.append(neighbor)

        return neighbors

    def check_duplicates(self, new_nodes: List[DiGraph], already_expanded: List[DiGraph]) -> List[DiGraph]:
        if len(already_expanded) == 0:
            return new_nodes

        already_expanded_set = set(already_expanded)
        kept = [(cost, new_graph) for (cost, new_graph) in new_nodes
                if not any(nx.is_isomorphic(new_graph, exists) for (_, exists) in already_expanded_set)]
        return kept
