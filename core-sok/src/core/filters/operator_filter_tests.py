
import unittest
from .operator_filter import OperatorFilter
from api.models.graph import Graph
from api.models.node import Node
from api.models.edge import Edge

class OperatorFilterTests(unittest.TestCase):
    def test_all_nodes_pass(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = OperatorFilter("name", "!=", 1)
        filtered_graph = search_filter.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node1, node2, node3])
        self.assertEqual(filtered_graph.get_edges(), [edge1, edge2])
        self.assertNotEqual(filtered_graph, graph)

    def test_no_node_passes(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = OperatorFilter("name", "==", 1)
        filtered_graph = search_filter.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [])
        self.assertEqual(filtered_graph.get_edges(), [])
        self.assertNotEqual(filtered_graph, graph)

    def test_string_comparison(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = OperatorFilter("name", "<=", "node2")
        filtered_graph = search_filter.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node1, node2])
        self.assertEqual(filtered_graph.get_edges(), [edge1])
        self.assertNotEqual(filtered_graph, graph)
    
    def test_no_attribute(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = OperatorFilter("age", "==", "node1")
        filtered_graph = search_filter.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [])
        self.assertEqual(filtered_graph.get_edges(), [])
        self.assertNotEqual(filtered_graph, graph)

if __name__ == '__main__':
    unittest.main()