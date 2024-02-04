from jinja2 import Environment, PackageLoader


# TODO: Remove when real implementation of graph is available
class Graph:
    def get_nodes(self):
        pass

    def get_edges(self):
        pass


class MockGraph(Graph):
    def get_nodes(self):
        return [{"id": str(i)} for i in range(300)]

    def get_edges(self):
        edges = []
        for i in range(200):
            for j in range(200):
                edges.append({
                    "src": {"id": str(i)},
                    "dest": {"id": str(j)}
                })
        return edges


class SimpleVisualizer():
    def __init__(self):
        self.environment = Environment(loader=PackageLoader("simple_visualizer", package_path="templates/"))
        self.template = self.environment.get_template("simple_visualizer_template.html")

    def get_name(self):
        return "simple_visualizer"

    def display(self, graph: Graph) -> str:
        return self.template.render(nodes=graph.get_nodes(), edges=graph.get_edges())


if __name__ == "__main__":
    sv = SimpleVisualizer()
    graph = MockGraph()
    print(sv.display(graph))