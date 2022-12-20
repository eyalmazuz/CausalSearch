import bnlearn
import networkx as nx
import pytest

from src.search_algorithms import bfs
from src.utils import utils


class TestExpand():

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.search = bfs.BFSSearch(None, utils.check_is_dag, None, None)


    def test_expand_2_nodes_root(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(['treatment', 'condition'])
            
        graph1 = graph.copy()
        graph1.add_edge('treatment', 'condition')
        graph2 = graph.copy()
        graph2.add_edge('condition', 'treatment')

        expected = [graph1, graph2]

        actual = self.search.expand(graph)
                
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

        actual = self.search.expand(graph)
                
        assert len(actual) == len(expected)
        assert all([nx.utils.graphs_equal(a, b) for a, b in zip(actual, expected)])

    def test_expand_2_nodes_mid_no_graphs(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(['treatment', 'condition'])
        graph.add_edge('treatment', 'condition')
            
        expected = []

        actual = self.search.expand(graph)
                
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

        actual = self.search.expand(graph)
                
        assert len(actual) == len(expected)
        assert all([nx.utils.graphs_equal(a, b) for a, b in zip(actual, expected)])


class TestBFS():
    
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.network = bnlearn.import_DAG('./graphs/cancer.bif')
        self.search = bfs.BFSSearch(self.network, utils.check_is_dag, self.goal_test, None)
        self.target = nx.DiGraph()
        self.target.add_nodes_from(self.network['model'])
        self.target.add_edges_from([('Cancer', 'Dyspnoea'), ('Smoker', 'Cancer')])

    def goal_test(self, graph):
        return nx.utils.graphs_equal(graph, self.target)
    
    def test_bfs_specific_node(self):
        actual = self.search.find()

        assert nx.utils.graphs_equal(actual, self.target)
