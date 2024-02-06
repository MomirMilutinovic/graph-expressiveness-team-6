import unittest
from .search_filter import SearchFilter
from api.models.graph import Graph
from api.models.node import Node
from api.models.edge import Edge

class SearchFilterTests(unittest.TestCase):
    def test_filter_removes_edges(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = SearchFilter("node2")
        filtered_graph = search_filter.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node2])
        self.assertEqual(filtered_graph.get_edges(), [])
        self.assertNotEqual(filtered_graph, graph)

    def test_filter_all_nodes_pass_attribute_value(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = SearchFilter("n")
        filtered_graph = search_filter.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node1, node2, node3])
        self.assertEqual(filtered_graph.get_edges(), [edge1, edge2])
        self.assertNotEqual(filtered_graph, graph)

    def test_filter_all_nodes_pass_attribute_key(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = SearchFilter("me")
        filtered_graph = search_filter.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node1, node2, node3])
        self.assertEqual(filtered_graph.get_edges(), [edge1, edge2])
        self.assertNotEqual(filtered_graph, graph)

    def test_filter_id(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = SearchFilter("2")
        filtered_graph = search_filter.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node2])
        self.assertEqual(filtered_graph.get_edges(), [])
        self.assertNotEqual(filtered_graph, graph)

    def test_filter_preserves_edge(self):
        node1 = Node("1", {"name": "node1pass"})
        node2 = Node("2", {"name": "node2pass"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = SearchFilter("pass")
        filtered_graph = search_filter.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node1, node2])
        self.assertEqual(filtered_graph.get_edges(), [edge1])
        self.assertNotEqual(filtered_graph, graph)


if __name__ == '__main__':
    unittest.main()