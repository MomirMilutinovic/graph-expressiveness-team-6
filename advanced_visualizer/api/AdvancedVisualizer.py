from django.template.loader import render_to_string

from api.components.visualizer import Visualizer
from api.models.graph import Graph


class AdvancedVisualizer(Visualizer):
    def get_name(self) -> str:
        return "advanced_visualizer_plugin"

    def display(self, graph: Graph):
        try:
            nodes = graph.get_nodes()
            if not nodes:
                raise ValueError("No nodes found in the graph.")

            edges = []
            for node in nodes:
                for neighbour in node.get_neighbours():
                    edges.append({"src": node.id, "dest": neighbour.id})

        except Exception as e:
            return f"<html><body><h2>Error: Invalid graph data.</h2><p>Details: {e}</p></body></html>"

        content = {
            "nodes": nodes,
            "edges": edges
        }
        return render_to_string("advanced_visualizer/advanced_visualizer.html", context=content)

