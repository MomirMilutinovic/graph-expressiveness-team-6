from pkg_resources import iter_entry_points

from api.components.data_source import DataSource
from api.components.visualizer import Visualizer


def load_plugins(entry_point_name):
    return [x.load()() for x in iter_entry_points(entry_point_name)]


def get_plugins() -> tuple[list[DataSource], list[Visualizer]]:
    data_source_plugins = load_plugins("datasources")
    visualizer_plugins = load_plugins("visualizers")
    return data_source_plugins, visualizer_plugins
