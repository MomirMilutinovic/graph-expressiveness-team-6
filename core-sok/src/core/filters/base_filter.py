from abc import ABC, abstractmethod
from api.models.graph import Graph

class Filter(ABC):
    """
    Base class for graph filters.
    """

    @abstractmethod
    def filter(self, graph: Graph) -> Graph:
        """
        Filters the graph.

        :param graph: The graph to filter.
        :type graph: Graph
        :return: The filtered graph.
        :rtype: Graph
        """
        pass