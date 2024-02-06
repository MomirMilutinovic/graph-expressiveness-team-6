from api.models.graph import Graph
from .base_filter import Filter
from api.models.node import Node


class OperatorFilter(Filter):
    """
    OperatorFilter filters the graph so only nodes that contain a specific
    attribute for which the given comparison returns true remain in the graph.
    """

    def __init__(self, attribute: str, operator: str, value: str):
        """
        Initializes the attribute filter.

        :param attribute: The attribute to filter by.
        :type attribute: str
        :param operator: The operator to use.
        :type operator: str
        :param value: The value to compare to.
        :type value: str
        """
        self.attribute = attribute
        self.operator = operator
        self.value = value
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OperatorFilter):
            return False
        return self.attribute == __value.attribute and self.operator == __value.operator and self.value == __value.value

    def satisfiesQuery(self, node: Node) -> bool:
        """
        Chcecks if the node satisfies the query.
        :param node: The node to check.
        :type node: Node
        :return: True if the node satisfies the query, False otherwise. 
        """
        if self.attribute not in node.data:
            return False

        try:
            self.value = type(node.data[self.attribute])(self.value)
        except ValueError:
            return False

        if self.operator == "==":
            return node.data[self.attribute] == self.value
        if self.operator == "!=":
            return node.data[self.attribute] != self.value
        if self.operator == ">":
            return node.data[self.attribute] > self.value
        if self.operator == "<":
            return node.data[self.attribute] < self.value
        if self.operator == ">=":
            return node.data[self.attribute] >= self.value
        if self.operator == "<=":
            return node.data[self.attribute] <= self.value

        return False

    def filter(self, graph: Graph) -> Graph:
        """
        Filters the graph.

        :param graph: The graph to filter.
        :type graph: Graph
        :return: The filtered graph.
        :rtype: Graph
        """
        nodes = list(filter(lambda node: self.satisfiesQuery(node), graph.nodes))
        edges = list(filter(lambda edge: edge.src in nodes and edge.dest in nodes, graph.edges))
        return Graph(edges, nodes)

    def to_json(self) -> dict:
        return {
            "type": "AttributeFilter",
            "attribute": self.attribute,
            "operator": self.operator,
            "value": self.value
        }

