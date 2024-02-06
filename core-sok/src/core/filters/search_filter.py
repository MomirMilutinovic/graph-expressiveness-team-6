from .base_filter import Filter
from api.models.graph import Graph
from api.models.node import Node

class SearchFilter(Filter):
    """
    SearchFilter filters the graph so only nodes where the search query occurs
    remain in the graph.
    """

    def __init__(self, search_term: str):
        """
        Initializes the search filter.

        :param search_term: The search term.
        :type search_term: str
        """
        self.search_term = search_term

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, SearchFilter):
            return False
        return self.search_term == __value.search_term

    def satisfiesQuery(self, node: Node) -> bool:
        """
        Chcecks if the node satisfies the query.
        :param node: The node to check.
        :type node: Node
        :return: True if the node satisfies the query, False otherwise. 
        """
        return self.search_term in node.id or any(self.search_term in str(value) for value in node.data.values()) or any(self.search_term in str(key) for key in node.data.keys())

    def filter(self, graph: Graph) -> Graph:
        """
        Filters the graph.

        :param graph: The graph to filter.
        :type graph: Graph
        :return: The filtered graph.
        :rtype: Graph
        """
        nodes = list(filter(lambda node: self.satisfiesQuery(node), graph.nodes))
        edges = list(filter(lambda edge: edge.src in nodes and edge.dest in nodes, graph.edges))
        return Graph(edges, nodes)

    def to_json(self) -> dict:
        """
        Returns a JSON representation of the filter.
        :return: The JSON representation of the filter.
        :rtype: dict
        """
        return {
            "type": "SearchFilter",
            "search_term": self.search_term
        }