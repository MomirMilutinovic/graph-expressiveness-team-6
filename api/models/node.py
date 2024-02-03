from edge import Edge


class Node:

    def __init__(self, id_: str, data: dict, edges: list[Edge]):
        self.id = id_
        self.data = data
        self.edges = edges

    def get_neighbours(self):
        pass
