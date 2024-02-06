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

    @abstractmethod
    def to_json(self) -> dict:
        """
        Converts the filter to a JSON object.
        The JSON object should contain a "type" field with the filter type.

        :return: The JSON object.
        :rtype: dict
        """
        pass