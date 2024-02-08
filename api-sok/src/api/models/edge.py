from .node import Node


class Edge:
    def __init__(self, data: dict, src: Node, dest: Node):
        self.data = data
        self.src = src
        self.dest = dest

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Edge):
            for key, value in __value.data.items():
                if key not in self.data or self.data[key] != value:
                    return False

            return self.src == __value.src and self.dest == __value.dest

        return False

    def __hash__(self) -> int:
        return hash((frozenset(self.data), self.src, self.dest))
