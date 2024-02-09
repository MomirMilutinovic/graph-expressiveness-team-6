from .edge import Edge
from .node import Node


class Graph:

    def __init__(self, edges=None, nodes=None, directed=True, root_id=None):
        if nodes is None:
            nodes = set()
        if edges is None:
            edges = set()
        self.edges = edges
        self.nodes = nodes
        self.directed = directed
        self.root_id = root_id

    def remove_node(self, node: Node):
        self.nodes.remove(node)
        self.edges = [
            edge for edge in self.edges if edge.src != node and edge.dest != node
        ]
        for node in self.nodes:
            node.edges = list(
                filter(
                    lambda edge: edge.src in self.nodes and edge.dest in self.nodes,
                    node.edges,
                )
            )

    def add_node(self, node: Node):
        self.nodes.add(node)

    def add_edge(self, edge: Edge):
        self.add_node(edge.src)
        self.add_node(edge.dest)

        if edge not in self.edges:
            self.edges.add(edge)

            if not self.directed:
                inverted_edge = Edge(edge.data, edge.dest, edge.src)
                self.edges.add(inverted_edge)

            for node in self.nodes:
                if node == edge.src:
                    node.edges.append(edge)
                if not self.directed and node == edge.dest:
                    node.edges.append(inverted_edge)

    def get_nodes(self) -> set[Node]:
        return self.nodes

    def get_edges(self) -> list[Edge]:
        return list(self.edges)
