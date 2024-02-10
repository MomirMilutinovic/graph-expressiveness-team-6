from .base_filter import Filter
from api.models.graph import Graph
from api.models.node import Node

class SearchFilter(Filter):
    """
    SearchFilter filters the graph so only nodes where the search query occurs
    remain in the graph.
    The filtering is done in-place.
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

    def filter(self, graph: Graph) -> Graph:
        """
        Filters the graph.

        :param graph: The graph to filter.
        :type graph: Graph
        :return: The filtered graph.
        :rtype: Graph
        """
        for node in list(graph.nodes):
            if self.search_term not in node:
                graph.remove_node(node)
            
        return graph

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