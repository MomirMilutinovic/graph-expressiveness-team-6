from api.models.graph import Graph
from .base_filter import Filter
from typing import List

class FilterChain(Filter):
    def __init__(self) -> None:
        super().__init__()
        self.filters: List[Filter] = []

    def add_filter(self, filter: Filter) -> None:
        self.filters.append(filter)

    def remove_filter(self, filter: Filter) -> None:
        self.filters.remove(filter)
    
    def filter(self, graph: Graph) -> Graph:
        for filter in self.filters:
            graph = filter.filter(graph)
        return graph

    def to_json(self) -> dict:
        return {
            "type": "FilterChain",
            "filters": [filter.to_json() for filter in self.filters]
        }
    
    def get_filters(self) -> List[Filter]:
        return self.filters
