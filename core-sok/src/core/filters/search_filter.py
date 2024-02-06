from .base_filter import Filter
from api.models.graph import Graph

class SearchFilter(Filter):
    """
    Filter for searching a graph.
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

    def satisfiesQuery(self, node):
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
        return {
            "type": "SearchFilter",
            "search_term": self.search_term
        }