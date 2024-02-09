from .node import Node


class Edge:
    """
    A class representing an edge between two nodes in a graph.

    Attributes:
        data (dict): A dictionary containing additional data associated with the edge.
        src (Node): The source node of the edge.
        dest (Node): The destination node of the edge.
    """

    def __init__(self, data: dict, src: Node, dest: Node):
        """
        Initializes an Edge object.

        Args:
            data (dict): A dictionary containing additional data associated with the edge.
            src (Node): The source node of the edge.
            dest (Node): The destination node of the edge.
        """
        self.data = data
        self.src = src
        self.dest = dest

    def __eq__(self, __value: object) -> bool:
        """
        Checks if the current edge is equal to another edge.

        Args:
            __value (object): The object to compare with.

        Returns:
            bool: True if the edges are equal, False otherwise.
        """
        if isinstance(__value, Edge):
            for key, value in __value.data.items():
                if key not in self.data or self.data[key] != value:
                    return False

            return self.src == __value.src and self.dest == __value.dest

        return False

    def __hash__(self) -> int:
        """
        Computes the hash value of the edge.

        Returns:
            int: The hash value of the edge.
        """
        return hash((frozenset(self.data), self.src, self.dest))
