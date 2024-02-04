from __future__ import annotations

if False:
    from api.models.edge import Edge


class Node:

    def __init__(self, id: str, data: dict, edges: 'Edge' = None):
        if edges is None:
            edges = []
        self.id = id
        self.data = data
        self.edges = edges

    def get_neighbours(self):
        neighbours: list[Node] = []

        for edge in self.edges:
            if edge.dest == self:
                neighbours.append(edge.src)
            else:
                neighbours.append(edge.dest)

        return neighbours

    def __str__(self):
        return f"Node: {self.id} with data: {self.data}"
