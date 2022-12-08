import networkx as nx
import pytest

from src import bfs, utils


class TestExpand():

    def test_expand_2_nodes_root(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(['treatment', 'condition'])
            
        graph1 = graph.copy()
        graph1.add_edge('treatment', 'condition')
        graph2 = graph.copy()
        graph2.add_edge('condition', 'treatment')

        expected = [graph1, graph2]

        actual = bfs.expand(graph, utils.check_is_dag)
                
        assert len(actual) == len(expected)
        assert all([nx.utils.graphs_equal(a, b) for a, b in zip(actual, expected)])

    def test_expand_3_nodes_root(self):
        node_pairs = [('treatment', 'condition'), ('treatment', 'outcome'),
                      ('condition', 'treatment'), ('condition', 'outcome'),
                      ('outcome', 'treatment'), ('outcome', 'condition')]
        
        graph = nx.DiGraph()
        graph.add_nodes_from(['treatment', 'condition', 'outcome'])

        expected = []
        for u, v in node_pairs:
            copy_graph = graph.copy()
            copy_graph.add_edge(u, v)
            expected.append(copy_graph)

        actual = bfs.expand(graph, utils.check_is_dag)
                
        assert len(actual) == len(expected)
        assert all([nx.utils.graphs_equal(a, b) for a, b in zip(actual, expected)])

    def test_expand_2_nodes_mid_no_graphs(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(['treatment', 'condition'])
        graph.add_edge('treatment', 'condition')
            
        expected = []

        actual = bfs.expand(graph, utils.check_is_dag)
                
        assert len(actual) == 0

    def test_expand_3_nodes_mid_4_results(self):
        node_pairs = [('treatment', 'outcome'), ('condition', 'outcome'),
                      ('outcome', 'treatment'), ('outcome', 'condition')]
        
        graph = nx.DiGraph()
        graph.add_nodes_from(['treatment', 'condition', 'outcome'])
        graph.add_edge('treatment', 'condition')

        expected = []
        for u, v in node_pairs:
            copy_graph = graph.copy()
            copy_graph.add_edge(u, v)
            expected.append(copy_graph)

        actual = bfs.expand(graph, utils.check_is_dag)
                
        assert len(actual) == len(expected)
        assert all([nx.utils.graphs_equal(a, b) for a, b in zip(actual, expected)])


class TestBFS():
    def test_bfs_specific_node(self):

        def goal_test(graph):
            goal_graph = nx.DiGraph()
            goal_graph.add_nodes_from(['treatment', 'condition', 'outcome'])
            goal_graph.add_edges_from([('treatment', 'outcome'), ('condition', 'treatment'),
                                       ('condition', 'outcome')])

            return nx.utils.graphs_equal(graph, goal_graph)

        graph = nx.DiGraph()
        graph.add_nodes_from(['treatment', 'condition', 'outcome'])
        
        actual = bfs.bfs(graph, goal_test, utils.check_is_dag)

        expected = nx.DiGraph()
        expected.add_nodes_from(['treatment', 'condition', 'outcome'])
        expected.add_edges_from([('treatment', 'outcome'), ('condition', 'treatment'),
                                   ('condition', 'outcome')])

        assert nx.utils.graphs_equal(actual, expected)
