import networkx as nx
import pytest

from src import utils

class TestPairs():
    def test_generate_pairs(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(['a', 'b', 'c'])

        actual = []
        expected = [('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]
        for pair in utils.get_graph_node_pairs(graph):
            actual.append(pair)

        assert len(actual) == len(expected)
        assert all([a == b for a, b in zip(actual, expected)])
