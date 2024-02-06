from django.db import models
import uuid


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
        self.filter_props = []
        self.graph = app_config.data_source_plugins_dict[selected_datasource].provide(
            **datasource_config
        )
