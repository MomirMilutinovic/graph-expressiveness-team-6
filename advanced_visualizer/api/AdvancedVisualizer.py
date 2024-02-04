import os

from jinja2 import Environment, FileSystemLoader

from api.components.visualizer import Visualizer
from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node


class AdvancedVisualizer(Visualizer):
    def get_name(self) -> str:
        return "advanced_visualizer_plugin"

    def display(self, graph: Graph):
        try:
            nodes_data = [{'id': node.id, 'data': node.data} for node in graph.get_nodes()]
            if not nodes_data:
                raise ValueError("No nodes found in the graph.")

            edges_data = [{'src': edge.src.id, 'dest': edge.dest.id, 'data': edge.data} for edge in graph.get_edges()]

        except Exception as e:
            return f"<html><body><h2>Error: Invalid graph data.</h2><p>Details: {e}</p></body></html>"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, '..', 'templates')
        env = Environment(loader=FileSystemLoader(templates_dir))

        template = env.get_template("advanced_visualizer.html")

        content = {
            "nodes": nodes_data,
            "edges": edges_data
        }

        return template.render(nodes=content['nodes'], edges=content['edges'])


if __name__ == "__main__":
    # Test the AdvancedVisualizer class
    node1 = Node(id="1", data={"label": "Node 1"})
    node2 = Node(id="2", data={"label": "Node 2"})
    node3 = Node(id="3", data={"label": "Node 3"})
    node4 = Node(id="4", data={"label": "Node 4"})
    node5 = Node(id="5", data={"label": "Node 5"})
    node6 = Node(id="6", data={"label": "Node 6"})
    node7 = Node(id="7", data={"label": "Node 7"})
    node8 = Node(id="8", data={"label": "Node 8"})
    node9 = Node(id="9", data={"label": "Node 9"})
    node10 = Node(id="10", data={"label": "Node 10"})

    test_nodes = {node1, node2, node3, node4, node5, node6, node7, node8, node9, node10}

    edge1 = Edge(data={"weight": 5}, src=node1, dest=node2)
    edge2 = Edge(data={"weight": 3}, src=node1, dest=node3)
    edge3 = Edge(data={"weight": 7}, src=node1, dest=node4)
    edge4 = Edge(data={"weight": 2}, src=node2, dest=node5)
    edge5 = Edge(data={"weight": 1}, src=node2, dest=node6)
    edge6 = Edge(data={"weight": 4}, src=node3, dest=node7)
    edge7 = Edge(data={"weight": 6}, src=node3, dest=node8)
    edge8 = Edge(data={"weight": 8}, src=node4, dest=node9)
    edge9 = Edge(data={"weight": 9}, src=node4, dest=node10)

    test_edges = [edge1, edge2, edge3, edge4, edge5, edge6, edge7, edge8, edge9]

    test_graph = Graph(edges=test_edges, nodes=test_nodes)

    visualizer = AdvancedVisualizer()
    html_output = visualizer.display(test_graph)
    print(html_output)
