from api.components.data_source import DataSource
from api.components.visualizer import Visualizer
from api.models.graph import Graph
from .filters.operator_filter import OperatorFilter


class ContentModule:
    INVALID_WORKSPACE_ID = -1

    def __init__(
        self,
        data_source_plugins: list[DataSource],
        visualizer_plugins: list[Visualizer],
    ):
        self.data_source_plugins = data_source_plugins
        self.visualizer_plugins = visualizer_plugins
        self.data_source_plugins_dict = {
            ds.get_name(): ds for ds in self.data_source_plugins
        }
        self.current_data_source: DataSource | None = None
        self.current_visualizer: Visualizer | None = (
            self.visualizer_plugins[0] if self.visualizer_plugins else None
        )
        self.graph: Graph = (
            self.current_data_source.provide() if self.current_data_source else Graph()
        )
        self.workspaces = []
        self.workspace_id = ContentModule.INVALID_WORKSPACE_ID

    def select_data_source(self, data_source_name):
        self.current_data_source = next(
            (
                ds
                for ds in self.data_source_plugins
                if ds.get_name() == data_source_name
            ),
            None,
        )

    def set_graph(self, graph: Graph):
        self.graph = graph

    def select_visualizer(self, visualizer_name):
        self.current_visualizer = next(
            (v for v in self.visualizer_plugins if v.get_name() == visualizer_name),
            None,
        )

    def get_data_source_params(self):
        return (
            self.current_data_source.get_configuration_parameters()
            if self.current_data_source
            else {}
        )

    def get_context(self):
        content = {
            "visualizers": [
                {"name": v.get_name(), "id": i}
                for i, v in enumerate(self.visualizer_plugins)
            ],
            "data_sources": [
                {"name": ds.get_name(), "id": i}
                for i, ds in enumerate(self.data_source_plugins)
            ],
            "current_visualizer": (
                self.current_visualizer.get_name() if self.current_visualizer else None
            ),
            "current_data_source": (
                self.current_data_source.get_name()
                if self.current_data_source
                else None
            ),
            "data_source_params": self.get_data_source_params(),
            "content": (
                self.current_visualizer.display(self.get_filtered_graph())
                if self.current_visualizer
                else None
            ),
            "workspaces": [vars(ws) for ws in self.workspaces],
            "active_ws_id": self.workspace_id,
            "filters": (
                list(
                    map(
                        lambda filter: filter.to_json(),
                        self.get_current_workspace().get_filters(),
                    )
                )
                if self.workspace_id != ContentModule.INVALID_WORKSPACE_ID
                else []
            ),
            "operators": list(OperatorFilter.operators.keys()),
        }
        return content

    def get_filtered_graph(self):
        return (
            self.get_current_workspace().get_filtered_graph()
            if self.workspace_id != -1
            else self.graph
        )

    def get_current_workspace(self):
        return next((ws for ws in self.workspaces if ws.id == self.workspace_id), None)

    def add_workspace(self, workspace):
        self.workspaces.append(workspace)

    def get_workspace(self, id_):
        return next((ws for ws in self.workspaces if ws.id == id_), None)

    def delete_workspace(self, id_):
        self.workspaces = [ws for ws in self.workspaces if ws.id != id_]

    def get_number_of_workspaces(self):
        return len(self.workspaces)

    def get_datasource_configuration(self, datasource_name: str) -> dict:
        return self.data_source_plugins_dict[
            datasource_name
        ].get_configuration_parameters()
