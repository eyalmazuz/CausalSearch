from typing import List
import logging

import networkx as nx
from networkx.classes.digraph import DiGraph

from src.search_algorithms.abstract_search import Search
from src.utils.utils import get_graph_node_pairs, generate_fake_data, graph_to_str

logger = logging.getLogger(__name__)


class UCS(Search):

    def __init__(self,
                 network,
                 criterion,
                 goal_test,
                 scoring_function,
                 edge_function,
                 number_of_samples=1000,
                 data=None,
                 **kwargs):
        super(UCS, self).__init__(network, criterion, goal_test)

        self.number_of_samples = number_of_samples if data is None else data.shape[0]
        self.data = generate_fake_data(network, number_of_samples) if data is None else data
        self.scorer = scoring_function(self.data)
        self.edge_function = edge_function

    def find(self, run=None, debug=False) -> DiGraph:

        graph = nx.DiGraph()
        graph.add_nodes_from(self.network['model'])

        open_list = []
        start_bic = 0.0
        for node in graph:
            start_bic -= self.scorer.local_score(node, graph.predecessors(node))  # Positive bic score
        open_list.append((start_bic, graph))
        closed_list: List[DiGraph] = []
        if debug:
            logging.debug(f'Initial BIC: {start_bic=}')

        # UCS version of the algorithm to find longest path
        # A longest path between two given vertices s and t in a weighted graph G is the same thing as a shortest path in a graph −G
        # We will work with negative weights for that reason
        # heaviest path is the path with the most improvement in the BIC score
        # since bic decreases the proposed graph is better
        iteration = 0
        while open_list:
            iteration += 1
            if debug:
                logging.debug(f'{len(open_list)=}, {len(closed_list)=}')

            # Finds the minimum node graph from the queue
            best, graph = float('inf'), None
            if debug:
                logging.debug(f'{best=}, {None=}')
            for (cost, cur_graph) in open_list:
                if cost < best:
                    if debug:
                        logging.debug(f'Found better graph in open list {cost=} {graph_to_str(cur_graph)=}')
                    best = cost
                    graph = cur_graph

            # "pops" the minimum node from the queue
            if graph is not None:
                open_list.remove((best, graph))

            cost, cur_graph = best, graph
            if debug:
                logging.debug(f'Best Graph at iteration {iteration=} {cost=}, {graph_to_str(cur_graph)=}')

            # checks if the node is our goal and return it if so
            if self.goal_test(cur_graph):
                return cur_graph

            # Generates all the neighbors for that given node
            neighbors = self.expand(cur_graph, closed_list, debug)
            if debug:
                logging.debug(f'Iteration {iteration=} has {len(neighbors)=} new neighbors')

            # Iterates over the neighbors and inserts them into the open list if necessary
            for neighbor_graph in neighbors:
                neighbor_bic = 0.0
                for node in neighbor_graph:
                    neighbor_bic -= self.scorer.local_score(node, neighbor_graph.predecessors(node))

                if debug:
                    logging.debug(f'Old neighbor BIC {neighbor_bic=} {cost=} Edge Weight={(neighbor_bic - cost)=}')
                # Transform the edge weight if needed (i.e. if we use negative weights then make sure no weight is > 0)
                neighbor_bic = self.edge_function(neighbor_bic, cost) + cost
                if debug:
                    logging.debug(f'New neighbor BIC {neighbor_bic=}')

                # Checks for duplicates in the open list
                # if the graph already exists in the open list
                # we will insert it only if the weight we found is better
                found = False
                visited, score = None, 0
                for i, (score, visited) in enumerate(open_list):
                    if nx.utils.graphs_equal(neighbor_graph, visited):
                        found = True
                        break

                # enter here if we found the node in our open list
                if found:
                    if debug:
                        logging.debug(f'Found existing graph {graph_to_str(visited)=} in open list with score {score=}')

                    # checks that the new edge weight is better than the existing one.
                    if neighbor_bic < score:
                        if debug:
                            logging.debug(f'Removing best graph with cost {score=} with graph with cost {neighbor_bic=}')
                        # if it better, we remove the node entry from the open list and append the better one
                        open_list.remove((score, visited))
                        logging.debug(open_list)

                        open_list.append((neighbor_bic, neighbor_graph))

                # there is no existing node in the open list
                # we will just add the node as a new one
                else:
                    if debug:
                        logging.debug(f'No existing graph found adding graph to open list {(neighbor_bic, graph_to_str(neighbor_graph))=}')

                    open_list.append((neighbor_bic, neighbor_graph))

            if debug:
                logging.debug([(c, graph_to_str(g)) for (c, g) in open_list])
            closed_list.append(cur_graph)

    def expand(self, graph: DiGraph, closed_list: List[DiGraph], debug=False) -> List[DiGraph]:
        neighbors = []
        for u, v in get_graph_node_pairs(graph):
            if debug:
                logging.debug(f'Expanding {u}->{v}')
            neighbor = graph.copy()
            neighbor.add_edge(u, v)

            if (self.criterion and self.criterion(neighbor)
                and neighbor not in neighbors):
                # and not any(nx.utils.graphs_equal(neighbor, exists) for exists in closed_list)):
                neighbors.append(neighbor)

        return neighbors

    def check_duplicates(self, new_nodes: List[DiGraph], already_expanded: List[DiGraph]) -> List[DiGraph]:
        if len(already_expanded) == 0:
            return new_nodes

        already_expanded_set = set(already_expanded)
        kept = [(cost, new_graph) for (cost, new_graph) in new_nodes
                if not any(nx.is_isomorphic(new_graph, exists) for (_, exists) in already_expanded_set)]
        return kept
