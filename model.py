import pydot

class Node:
    def __init__(self, node):
        self.name = node.get_name()
        self.edges = {self: 1}

    def __hash__(self):
        return hash(self.name)

def load(file):
    dot = pydot.graph_from_dot_file(file)

    nodes = {}
    for n in dot.get_nodes():
        nodes[n.get_name()] = Node(n)

    edges = dot.get_edges()
    for e in edges:
        nodes[e.get_source()].edges[nodes[e.get_destination()]] = 1

    return nodes.values()
