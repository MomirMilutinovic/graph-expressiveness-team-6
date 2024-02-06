from django.apps import AppConfig
from core.infrastructure import DataSource, Visualizer, get_plugins
from .models import Workspace


class GraphVisualizerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "graph_visualizer"

    data_source_plugins: list[DataSource] = []
    data_source_plugins_dict: dict[DataSource] = {}
    visualizer_plugins: list[Visualizer] = []
    workspaces: list[Workspace] = []

    def ready(self):
        self.data_source_plugins, self.visualizer_plugins = get_plugins()

        self.data_source_plugins_dict = {
            ds.get_name(): ds for ds in self.data_source_plugins
        }

    def add_workspace(self, workspace: Workspace):
        self.workspaces.append(workspace)
