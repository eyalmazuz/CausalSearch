import bnlearn as bn
import networkx as nx
from networkx.classes.digraph import DiGraph
from pgmpy.estimators import HillClimbSearch

from src.search_algorithms.abstract_search import Search
from src.utils.utils import generate_fake_data


class HillClimb(Search):
    def __init__(self,
                 network,
                 scoring_function,
                 epsilon=1e-4,
                 number_of_samples=1000,
                 **kwargs):
        
        super(HillClimb, self).__init__(network, scoring_function=scoring_function)
        
        self.epsilon = epsilon
        self.number_of_samples = number_of_samples
        self.data = generate_fake_data(network, number_of_samples)

        self.estimator = HillClimbSearch(self.data)

    def find(self, debug) -> DiGraph:
        best_model = self.estimator.estimate(scoring_method=self.scoring_function(self.data),
                                             epsilon=self.epsilon)
        
        graph = nx.DiGraph()

        graph.add_nodes_from(best_model.nodes)
        graph.add_edges_from(best_model.edges)

        return graph
