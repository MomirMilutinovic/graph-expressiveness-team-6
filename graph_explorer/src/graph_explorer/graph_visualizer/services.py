from django.apps import apps
from api.components.data_source import DataSource
from api.models.node import Node
from api.models.graph import Graph
import random
from typing import Any
from .models import TreeViewNode


def get_tree_view_data(graph: Graph) -> dict:

    if len(graph.get_nodes()) == 0:
        return {}

    graph_root = random.choice(list(graph.get_nodes()))

    tree_view_root = process_node(graph_root)

    return vars(tree_view_root)


def get_node_dict(graph: Graph) -> dict:
    nodes = graph.get_nodes()
    node_dict = {
        node.id: vars(
            TreeViewNode(
                node.id,
                False,
                [],
                node.data,
                list(map(lambda node: node.id, node.get_neighbours())),
            )
        )
        for node in nodes
    }

    return node_dict


def process_node(node: Node, level: int = 0) -> TreeViewNode:
    children = []
    neighbours = node.get_neighbours()

    for neighbour in neighbours:
        child = vars(
            TreeViewNode(
                neighbour.id,
                False,
                [],
                neighbour.data,
                list(map(lambda node: node.id, neighbour.get_neighbours())),
            )
        )
        children.append(child)

    return TreeViewNode(
        node.id,
        True if level in [0, 1] else False,
        children,
        node.data,
        list(map(lambda node: node.id, node.get_neighbours())),
    )


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


def coerce_filter_value(value: str, attribute: str, graph: Graph, operator: str) -> Any:
    node_iterator = iter(graph.get_nodes())
    first_node = next(node_iterator)
    if attribute not in first_node.data:
        return value
    representative_value = first_node.data[attribute]
    if operator != "contains":
        return type(representative_value)(value)
    else:
        return coerce_value_for_contains_operator(value, attribute, graph)


def coerce_value_for_contains_operator(value: str, attribute: str, graph: Graph) -> Any:
    nodes = list(graph.get_nodes())
    representative_value = nodes[0].data[attribute]

    if type(representative_value) == str:
        return value
    elif type(representative_value) == list:
        for node in nodes:
            representative_value = node.data[attribute]
            if len(representative_value) > 0:
                return type(representative_value[0])(value)

    return value