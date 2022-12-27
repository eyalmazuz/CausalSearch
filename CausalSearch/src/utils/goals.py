import networkx as nx
from networkx.classes.digraph import DiGraph
from pgmpy.models.BayesianNetwork import BayesianNetwork # type: ignore

def connected_degree_one(graph: DiGraph):
    if not nx.is_weakly_connected(graph):
        return False

    for node in graph:
        if graph.degree(node) == 0:
            return False

    return True

def target_graph(graph: DiGraph, network: BayesianNetwork):
    model = network['model']
    goal = nx.DiGraph()

    goal.add_nodes_from(model.nodes)
    goal.add_edges_from(model.edges)

    return nx.utils.graphs_equal(graph, goal)

