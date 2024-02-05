from jinja2 import Environment, FileSystemLoader
import os
from api.components.visualizer import Visualizer
from api.models.graph import Graph


class MockGraph(Graph):
    def get_nodes(self):
        return [{"id": str(i)} for i in range(20)]

    def get_edges(self):
        edges = []
        for i in range(10):
            for j in range(10):
                if i == j:
                    continue
                edges.append({
                    "src": {"id": str(i)},
                    "dest": {"id": str(j)}
                })
        edges.append({
            "src": {"id": "10"},
            "dest": {"id": "11"}
        })
        edges.append({
            "src": {"id": "11"},
            "dest": {"id": "12"}
        })
        return edges


class SimpleVisualizer(Visualizer):
    def __init__(self):
        path=os.path.join(os.path.dirname(__file__))
        self.environment = Environment(loader=FileSystemLoader(path + "/templates"))
        self.template = self.environment.get_template("simple_visualizer_template.html")

    def get_name(self):
        return "simple_visualizer"

    def display(self, graph: Graph) -> str:
        return self.template.render(nodes=graph.get_nodes(), edges=graph.get_edges(), name=self.get_name())


if __name__ == "__main__":
    sv = SimpleVisualizer()
    graph = MockGraph()
    print(sv.display(graph))