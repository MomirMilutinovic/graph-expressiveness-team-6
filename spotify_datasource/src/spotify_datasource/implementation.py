from api.components.data_source import DataSource
from api.models.graph import Graph
from .services import get_graph


class SpotifyDataSource(DataSource):
    def get_name(self):
        return "Spotify DataSource"

    def provide(self, **kwargs) -> Graph:
        auth_token = kwargs["auth_token"]
        artist_name = kwargs["artist_name"]
        max_neighbours = kwargs["max_neighbours"]
        recursion_depth = kwargs["recursion_depth"]

        return get_graph(auth_token, artist_name, max_neighbours, recursion_depth)

    def get_configuration_parameters(self) -> dict[str, str]:
        return {
            "auth_token": "str",
            "artist_name": "str",
            "max_neighbours": "int",
            "recursion_depth": "int",
        }
