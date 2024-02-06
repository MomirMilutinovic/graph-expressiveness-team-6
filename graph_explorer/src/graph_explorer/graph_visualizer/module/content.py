from api.components.data_source import DataSource
from api.components.visualizer import Visualizer
from api.models.graph import Graph


class ContentModule:
    def __init__(self, data_source_plugins: list[DataSource], visualizer_plugins: list[Visualizer]):
        self.data_source_plugins = data_source_plugins
        self.visualizer_plugins = visualizer_plugins
        self.current_data_source: DataSource | None = None
        self.current_visualizer: Visualizer | None = self.visualizer_plugins[0] if self.visualizer_plugins else None
        self.graph: Graph = self.current_data_source.provide() if self.current_data_source else Graph()
        self.workspaces = []
        self.workspace_id = -1

    def select_data_source(self, data_source_name):
        self.current_data_source = \
            next((ds for ds in self.data_source_plugins if ds.get_name() == data_source_name), None)

    def set_graph(self, graph: Graph):
        self.graph = graph

    def select_visualizer(self, visualizer_name):
        self.current_visualizer = \
            next((v for v in self.visualizer_plugins if v.get_name() == visualizer_name), None)

    def get_data_source_params(self):
        return self.current_data_source.get_configuration_parameters() if self.current_data_source else {}

    def get_context(self):
        content = {
            "visualizers": [{"name": v.get_name(), "id": i} for i, v in enumerate(self.visualizer_plugins)],
            "data_sources": [{"name": ds.get_name(), "id": i} for i, ds in enumerate(self.data_source_plugins)],
            "current_visualizer": self.current_visualizer.get_name() if self.current_visualizer else None,
            "current_data_source": self.current_data_source.get_name() if self.current_data_source else None,
            "data_source_params": self.get_data_source_params(),
            "content": self.current_visualizer.display(self.graph) if self.current_visualizer else None,
            "workspaces": self.workspaces,
            "active_ws_id": self.workspace_id,
        }
        return content

    def search(self, query):
        self.graph.nodes = [node for node in self.graph.nodes if query in node]

    def provide_data(self, kwargs: dict):
        if self.current_data_source is None:
            return
        self.graph = self.current_data_source.provide(**kwargs)
