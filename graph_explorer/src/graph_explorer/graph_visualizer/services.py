from django.apps import apps
from api.components.data_source import DataSource
from api.models.node import Node
import random
from .models import TreeViewNode


def get_tree_view_data(datasource_name: str) -> TreeViewNode:
    data_sources: list[DataSource] = apps.get_app_config(
        "graph_visualizer"
    ).data_source_plugins
    graph = data_sources[1].provide(
        auth_token="BQAP22lDj_nBchesUAyO79AAd15V8QRH5yDHrG0qh0QhG9lJSE2xZzMVPINL20v45nnuFZsBlQjv_Od17GIjyLsMjl4hxCz1Qbnwbvw7NzZaoA1zdMs"
    )

    graph_root = random.choice(list(graph.get_nodes()))

    tree_view_root = process_node(graph_root)

    return tree_view_root


def process_node(node: Node, level: int = 0) -> TreeViewNode:
    children = []
    neighbours = node.get_neighbours()

    for neighbour in neighbours:
        child = vars(TreeViewNode(neighbour.id, False, []))
        children.append(child)

    return TreeViewNode(node.id, True if level in [0, 1] else False, children)


def get_datasource_configuration(datasource_name) -> dict:
    data_sources: list[DataSource] = apps.get_app_config(
        "graph_visualizer"
    ).data_source_plugins_dict

    return data_sources[datasource_name].get_configuration_parameters()


def get_datasource_names() -> list:
    data_sources: list[DataSource] = apps.get_app_config(
        "graph_visualizer"
    ).data_source_plugins

    return list(map(lambda ds: ds.get_name(), data_sources))
