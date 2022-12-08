import networkx as nx

from networkx.classes.digraph import DiGraph

def all_nodes_degree_one_or_more(graph: DiGraph) -> bool:
    for node in graph:
        if graph.degree(node) == 0:
            return False

    return True
