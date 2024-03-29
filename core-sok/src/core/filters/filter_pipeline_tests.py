import unittest
from api.models.graph import Graph
from api.models.node import Node
from api.models.edge import Edge
from .search_filter import SearchFilter
from .filter_pipeline import FilterPipeline


class FilterPipelineTests(unittest.TestCase):
    def test_filter_pipeline_no_filters(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        filter_pipeline = FilterPipeline()
        filtered_graph = filter_pipeline.filter(graph)
        self.assertNotEqual(filtered_graph, graph)

    def test_filter_pipeline_only_one_filter(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = SearchFilter("node2")
        filter_pipeline = FilterPipeline()
        filter_pipeline.add_filter(search_filter)
        filtered_graph = filter_pipeline.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node2])
        self.assertEqual(filtered_graph.get_edges(), [])
        self.assertNotEqual(filtered_graph, graph)

    def test_filter_pipeline_only_two_filters_no_nodes_pass(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge(None, node1, node2)
        edge2 = Edge(None, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = SearchFilter("node2")
        another_search_filter = SearchFilter("node1")
        filter_pipeline = FilterPipeline()
        filter_pipeline.add_filter(search_filter)
        filter_pipeline.add_filter(another_search_filter)
        filtered_graph = filter_pipeline.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [])
        self.assertEqual(filtered_graph.get_edges(), [])
        self.assertNotEqual(filtered_graph, graph)

    def test_filter_pipeline_only_two_filters_all_nodes_pass(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"name": "node2"})
        node3 = Node("3", {"name": "node3"})
        edge1 = Edge({}, node1, node2)
        edge2 = Edge({}, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3])
        search_filter = SearchFilter("n")
        another_search_filter = SearchFilter("d")
        filter_pipeline = FilterPipeline()
        filter_pipeline.add_filter(search_filter)
        filter_pipeline.add_filter(another_search_filter)
        filtered_graph = filter_pipeline.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node1, node2, node3])
        self.assertEqual(filtered_graph.get_edges(), [edge1, edge2])
        self.assertNotEqual(filtered_graph, graph)
    
    def test_filter_pipeline_composition(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"word": "name"})
        node3 = Node("3", {"name": "node3"})
        node4 = Node("4", {"name": "armor"})
        edge1 = Edge({}, node1, node2)
        edge2 = Edge({}, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3, node4])
        search_filter = SearchFilter("or")
        another_search_filter = SearchFilter("me")
        filter_pipeline = FilterPipeline()
        filter_pipeline.add_filter(search_filter)
        filter_pipeline.add_filter(another_search_filter)
        composed_filter_pipeline = FilterPipeline()
        composed_filter_pipeline.add_filter(filter_pipeline)
        filtered_graph = composed_filter_pipeline.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node2, node4])
        self.assertEqual(filtered_graph.get_edges(), [])
        self.assertNotEqual(filtered_graph, graph)

    def test_filter_pipeline_remove_filter(self):
        node1 = Node("1", {"name": "node1"})
        node2 = Node("2", {"word": "name"})
        node3 = Node("3", {"name": "node3"})
        node4 = Node("4", {"name": "armor"})
        edge1 = Edge({}, node1, node2)
        edge2 = Edge({}, node2, node3)
        graph = Graph([edge1, edge2], [node1, node2, node3, node4])
        search_filter = SearchFilter("or")
        another_search_filter = SearchFilter("me")
        filter_pipeline = FilterPipeline()
        filter_pipeline.add_filter(search_filter)
        filter_pipeline.add_filter(another_search_filter)
        filter_pipeline.remove_filter(search_filter)
        filtered_graph = filter_pipeline.filter(graph)
        self.assertEqual(filtered_graph.get_nodes(), [node1, node2, node3, node4])
        self.assertEqual(filtered_graph.get_edges(), [edge1, edge2])
        self.assertNotEqual(filtered_graph, graph)

if __name__ == '__main__':
    unittest.main()
