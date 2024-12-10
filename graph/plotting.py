import gravis as gv

from . import BaseNode


def plot_graph(nodes: list[BaseNode], directed: bool = True):
    """
    Plot a graph using the gravis library.

    Args:
        nodes (list[BaseNode]): The nodes to plot.
    """
    graph_data = {
        "graph": {
            "directed": directed,
            "metadata": {},
            "nodes": {n.id: {} for n in nodes},
            "edges": [{"source": n.id, "target": c.id, "metadata": {}} for n in nodes for c in n.children],
        },
    }

    return gv.d3(graph_data)
