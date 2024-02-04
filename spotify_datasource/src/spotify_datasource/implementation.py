from api.components.data_source import DataSource
from api.models.graph import Graph
from .services import get_graph


class SpotifyDataSource(DataSource):
    def get_name(self):
        return "Spotify DataSource"

    def provide(self, **kwargs) -> Graph:
        auth_token = kwargs["auth_token"]

        return get_graph(auth_token)