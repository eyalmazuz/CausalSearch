import networkx as nx
from networkx.classes.digraph import DiGraph
from pgmpy.models.BayesianNetwork import BayesianNetwork # type: ignore

def all_nodes_degree_one_or_more(graph: DiGraph) -> bool:
    for node in graph:
        if graph.degree(node) == 0:
            return False

    return True

def same_graph_goal(network: BayesianNetwork):
    model = network['model']
    goal = nx.DiGraph()

    goal.add_nodes_from(model.nodes)
    goal.add_edges_from(model.edges)

    def check_goal(graph: DiGraph):
        return nx.utils.graphs_equal(graph, goal)

    return check_goal
