from django.apps import apps
from api.components.data_source import DataSource
from api.models.node import Node
from api.models.graph import Graph
import random
from .models import TreeViewNode


def get_tree_view_data(graph: Graph) -> TreeViewNode:
    graph_root = random.choice(list(graph.get_nodes()))

    tree_view_root = process_node(graph_root)

    return tree_view_root


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
