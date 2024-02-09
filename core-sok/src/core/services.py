from typing import Any
from api.models.graph import Graph


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
