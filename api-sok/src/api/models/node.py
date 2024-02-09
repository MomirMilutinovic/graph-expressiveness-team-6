class Node:
    """
    A class representing a node in a graph.

    Attributes:
        id (str): The identifier of the node.
        data (dict): A dictionary containing additional data associated with the node.
        edges (list): A list of edges incident to the node.
    """

    def __init__(self, id: str, data: dict, edges=None):
        """
        Initializes a Node object.

        Args:
            id (str): The identifier of the node.
            data (dict): A dictionary containing additional data associated with the node.
            edges (list, optional): A list of edges incident to the node. Defaults to None.
        """
        if edges is None:
            edges = []
        self.id = id
        self.data = data
        self.edges = edges

    def get_neighbours(self) -> list["Node"]:
        """
        Retrieves the neighboring nodes of the current node.

        Returns:
            list[Node]: A list of neighboring nodes.
        """
        neighbours: list[Node] = []

        for edge in self.edges:
            if edge.src == self:
                neighbours.append(edge.dest)

        return neighbours

    def __eq__(self, __value: object) -> bool:
        """
        Checks if the current node is equal to another node.

        Args:
            __value (object): The object to compare with.

        Returns:
            bool: True if the nodes are equal, False otherwise.
        """
        if isinstance(__value, Node):
            return self.id == __value.id
        return False

    def __hash__(self) -> int:
        """
        Computes the hash value of the node.

        Returns:
            int: The hash value of the node.
        """
        return hash(self.id)

    def __contains__(self, item):
        """
        Checks if the node contains the specified item.

        Args:
            item: The item to check for containment.

        Returns:
            bool: True if the item is contained in the node's id or data, False otherwise.
        """
        return (
            item in self.id
            or any(item in str(value) for value in self.data.values())
            or any(item in str(key) for key in self.data.keys())
        )
