from typing import List
from django.db import models
import uuid

from core.filters.filter_chain import FilterChain
from core.filters.base_filter import Filter
from api.models.graph import Graph

class TreeViewNode:
    def __init__(
        self, name: str, expanded: bool, children: list, data: dict, children_ids
    ) -> None:
        self.name = name
        self.expanded = expanded
        self.children = children if expanded else []
        self.data = data
        self.children_ids = children_ids


class Workspace:
    def __init__(
        self, name: str, selected_datasource: str, datasource_config: dict, app_config
    ) -> None:
        self.id = uuid.uuid4().hex
        self.name = name
        self.selected_datasource = selected_datasource
        self.datasource_config = datasource_config
        self.filter_chain = FilterChain()
        self.graph = app_config.data_source_plugins_dict[selected_datasource].provide(
            **datasource_config
        )
    
    def add_filter(self, filter: Filter):
        self.filter_chain.add_filter(filter)

    def get_filtered_graph(self) -> Graph:
        return self.filter_chain.filter(self.graph)

    def get_filters(self) -> List[Filter]:
        return self.filter_chain.get_filters()

    def get_filter_chain(self) -> FilterChain:
        return self.filter_chain