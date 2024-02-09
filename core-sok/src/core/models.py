import uuid
from typing import List

from .filters.filter_pipeline import FilterPipeline
from .filters.base_filter import Filter
from .content import ContentModule
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
        self,
        name: str,
        selected_datasource: str,
        datasource_config: dict,
        content_module: ContentModule,
    ) -> None:
        self.id = uuid.uuid4().hex
        self.name = name
        self.selected_datasource = selected_datasource
        self.datasource_config = datasource_config
        self.filter_pipeline = FilterPipeline()
        self.graph = content_module.data_source_plugins_dict[
            selected_datasource
        ].provide(**datasource_config)
        self.filtered_graph = self.graph

    def add_filter(self, filter: Filter):
        self.filter_pipeline.add_filter(filter)
        try:
            self.filtered_graph = self.filter_pipeline.filter(self.graph)
        except Exception as e:
            self.filter_pipeline.remove_filter(filter)
            raise e

    def get_filtered_graph(self) -> Graph:
        return self.filtered_graph

    def get_filters(self) -> List[Filter]:
        return self.filter_pipeline.get_filters()

    def get_filter_pipeline(self) -> FilterPipeline:
        return self.filter_pipeline

    def get_unfiltered_graph(self) -> Graph:
        return self.graph

    def remove_filter(self, filter: Filter):
        self.filter_pipeline.remove_filter(filter)
        self.filtered_graph = self.filter_pipeline.filter(self.graph)

    def set_data_source(
        self,
        datasource_name: str,
        datasource_config: dict,
        content_module: ContentModule,
    ):
        self.graph = content_module.data_source_plugins_dict[datasource_name].provide(
            **datasource_config
        )
        self.selected_datasource = datasource_name
        self.datasource_config = datasource_config
        self.filtered_graph = self.filter_pipeline.filter(self.graph)
