class Node:

    def __init__(self, id: str, data: dict, edges=None):
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

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Node):
            return self.id == __value.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
