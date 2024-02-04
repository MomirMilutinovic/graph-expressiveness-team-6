from .node import Node


class Edge:
    def __init__(self, data: dict, src: Node, dest: Node):
        self.data = data
        self.src = src
        self.dest = dest
