from jinja2 import Environment, FileSystemLoader
import os
from api.components.visualizer import Visualizer
from api.models.graph import Graph



class SimpleVisualizer(Visualizer):
    def __init__(self):
        path=os.path.join(os.path.dirname(__file__))
        self.environment = Environment(loader=FileSystemLoader(path + "/templates"))
        self.template = self.environment.get_template("simple_visualizer_template.html")

    def get_name(self):
        return "simple_visualizer"

    def display(self, graph: Graph) -> str:
        return self.template.render(nodes=graph.get_nodes(), edges=graph.get_edges(), name=self.get_name())
