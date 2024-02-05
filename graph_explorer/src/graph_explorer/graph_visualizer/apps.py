from django.apps import AppConfig
from core.infrastructure import DataSource, Visualizer, get_plugins


class GraphVisualizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graph_visualizer'

    data_source_plugins: list[DataSource] = []
    visualizer_plugins: list[Visualizer] = []

    def ready(self):
        self.data_source_plugins, self.visualizer_plugins = get_plugins()
