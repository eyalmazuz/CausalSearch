import networkx as nx
import pytest

from src.utils import goals

class TestGoals():
    def test_two_nodes_no_edges(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(['a', 'b'])

        assert not goals.all_nodes_degree_one_or_more(graph)

    def test_two_nodes_no_one_edge(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(['a', 'b'])
        graph.add_edge('b', 'a') 

        assert goals.all_nodes_degree_one_or_more(graph)
