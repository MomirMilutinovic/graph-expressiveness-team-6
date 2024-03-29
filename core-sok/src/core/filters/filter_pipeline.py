from api.models.graph import Graph
from .base_filter import Filter
from typing import List
import copy


class FilterPipeline(Filter):
    """
    FilterPipeline is a filter that chains multiple filters together.
    The output of this filters is the result of applying all the filters in the pipeline.
    The filters are applied in the order they were added.
    The filter makes a deep copy of the graph before applying the filters.
    """

    def __init__(self) -> None:
        super().__init__()
        self.filters: List[Filter] = []

    def add_filter(self, filter: Filter) -> None:
        """
        Adds a filter to the pipeline.
        :param filter: The filter to add.
        :type filter: Filter
        """
        self.filters.append(filter)

    def remove_filter(self, filter: Filter) -> None:
        """
        Removes a filter from the pipeline.
        :param filter: The filter to remove.
        :type filter: Filter
        """
        self.filters.remove(filter)

    def filter(self, graph: Graph) -> Graph:
        """
        Applies all the filters in the pipeline to the graph.
        :param graph: The graph to filter.
        :type graph: Graph
        :return: The filtered graph.
        :rtype: Graph
        """
        graph = copy.deepcopy(graph)
        for filter in self.filters:
            graph = filter.filter(graph)
        return graph

    def to_json(self) -> dict:
        """
        Returns a JSON representation of the filter pipeline.
        :return: The JSON representation of the filter pipeline.
        :rtype: dict
        """
        return {
            "type": "FilterPipeline",
            "filters": [filter.to_json() for filter in self.filters]
        }

    def get_filters(self) -> List[Filter]:
        """
        Returns the filters in the pipeline as a list.
        :return: The filters in the pipeline.
        :rtype: List[Filter]
        """
        return self.filters
