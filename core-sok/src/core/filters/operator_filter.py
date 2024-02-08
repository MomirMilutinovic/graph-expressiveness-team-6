from api.models.graph import Graph
from .base_filter import Filter
from api.models.node import Node
from typing import Callable
from typing import Any
from re import search


class OperatorFilter(Filter):
    """
    OperatorFilter filters the graph so only nodes that contain a specific
    attribute for which the given comparison returns true remain in the graph.
    The filtering is done in-place.
    """
    operators = {
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
        "contains": lambda a, b: b in a,
        "matches": lambda a, regex: search(regex, a) is not None,
        "divisible by": lambda a, b: a % b == 0,
    }

    def __init__(self, attribute: str, operator_name: str, value: Any, operator: Callable[[Any, Any], bool]=None):
        """
        Initializes the operator filter.
        The value will be converted to the type of the attribute once filter is called.

        :param attribute: The attribute to filter by.
        :type attribute: str
        :param operator_name: The name of the operator.
        :type operator_name: str
        :param value: The value to compare to.
        :type value: str
        :param operator: The operator to use.
        :type operator: Callable[[Any, Any], bool]
        """
        self.attribute = attribute
        self.operator_name = operator_name
        self.value = value
        if operator_name not in OperatorFilter.operators and operator is None:
            raise ValueError("Invalid operator")
        self.operator = OperatorFilter.operators[operator_name] if operator is None else operator
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OperatorFilter):
            return False
        return self.attribute == __value.attribute and self.operator_name == __value.operator_name and self.value == __value.value

    def satisfiesQuery(self, node: Node) -> bool:
        """
        Checks if the node satisfies the query.
        :param node: The node to check.
        :type node: Node
        :return: True if the node satisfies the query, False otherwise. 
        """
        if self.attribute not in node.data and self.attribute != "id":
            return False

        if self.attribute == "id":
            return self.operator(node.id, self.value)
        return self.operator(node.data[self.attribute], self.value)

    def filter(self, graph: Graph) -> Graph:
        """
        Filters the graph.

        :param graph: The graph to filter.
        :type graph: Graph
        :return: The filtered graph.
        :rtype: Graph
        """
        for node in list(graph.nodes):
            if not self.satisfiesQuery(node):
                graph.remove_node(node)

        return graph

    def to_json(self) -> dict:
        return {
            "type": "OperatorFilter",
            "attribute": self.attribute,
            "operator": self.operator_name,
            "value": self.value
        }

