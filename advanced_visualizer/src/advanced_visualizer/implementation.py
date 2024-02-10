import os

from jinja2 import Environment, FileSystemLoader

from api.components.visualizer import Visualizer
from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node


class AdvancedVisualizer(Visualizer):

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, "../templates")
        self.environment = Environment(loader=FileSystemLoader(templates_dir))
        self.template = self.environment.get_template("advanced_visualizer.html")

    def get_name(self) -> str:
        return "Advanced Visualizer"

    def display(self, graph: Graph):
        try:
            nodes = graph.get_nodes()
            if not nodes:
                raise ValueError("No nodes found in the graph.")
        except Exception as e:
            return f"<html><body><h2>Error: Invalid graph data.</h2><p>Details: {e}</p></body></html>"

        return self.template.render(nodes=graph.get_nodes(), edges=graph.get_edges(), name=self.get_name(),
                                    directed=graph.directed)


class MockGraph(Graph):
    def get_nodes(self):
        # Create mock nodes with IDs and labels
        return [Node(id=str(i), data={"label": f"Node {i}", "extraInfo": f"Info {i}", "info2": f"Info {i}"}) for i in
                range(1, 21)]

    def get_edges(self):
        # Create mock edges between nodes with some data
        edges = []
        for i in range(1, 10):  # Creating edges from each node to the next
            edges.append(Edge(src=Node(id=str(i), data={"label": f"Node {i}"}),
                              dest=Node(id=str(i + 1), data={"label": f"Node {i + 1}"}),
                              data={"weight": i}))

        edges.append(Edge(src=Node(id=str(1), data={"label": "Node 1"}),
                          dest=Node(id=str(20), data={"label": "Node 20"}),
                          data={"weight": 10}))
        edges.append(Edge(src=Node(id=str(20), data={"label": "Node 20"}),
                          dest=Node(id=str(1), data={"label": "Node 1"}),
                          data={"weight": 10}))
        edges.append(Edge(src=Node(id=str(1), data={"label": "Node 1"}),
                          dest=Node(id=str(10), data={"label": "Node 10"}),
                          data={"weight": 5}))
        edges.append(Edge(src=Node(id=str(10), data={"label": "Node 10"}),
                          dest=Node(id=str(1), data={"label": "Node 1"}),
                          data={"weight": 2}))
        return edges


if __name__ == "__main__":
    visualizer = AdvancedVisualizer()
    mock_graph = MockGraph()
    html_output = visualizer.display(mock_graph)
    print(html_output)
