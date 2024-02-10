from django.apps import AppConfig

from api.components.data_source import DataSource
from api.components.visualizer import Visualizer
from core.infrastructure import get_plugins
from core.models import Workspace
from core.content import ContentModule


class GraphVisualizerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "graph_visualizer"

    data_source_plugins: list[DataSource] = []
    visualizer_plugins: list[Visualizer] = []
    workspaces: list[Workspace] = []

    def ready(self):
        self.data_source_plugins, self.visualizer_plugins = get_plugins()

    def get_content_module(self) -> ContentModule:
        return ContentModule(self.data_source_plugins, self.visualizer_plugins)
