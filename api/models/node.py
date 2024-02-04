from .edge import Edge


class Node:

    def __init__(self, id: str, data: dict, edges: list[Edge] = []):
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
