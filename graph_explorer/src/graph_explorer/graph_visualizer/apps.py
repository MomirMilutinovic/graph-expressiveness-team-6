from django.apps import AppConfig
from pkg_resources import iter_entry_points

from api.components.data_source import DataSource
from api.components.visualizer import Visualizer


def load_plugins(entry_point_name):
    return [x.load()() for x in iter_entry_points(entry_point_name)]


class GraphVisualizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graph_visualizer'

    data_source_plugins: list[DataSource] = []
    visualizer_plugins: list[Visualizer] = []

    def ready(self):
        self.data_source_plugins = load_plugins("datasources")
        self.visualizer_plugins = load_plugins("visualizers")
