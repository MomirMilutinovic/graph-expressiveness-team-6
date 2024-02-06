from api.components.data_source import DataSource
from api.models.graph import Graph

from .services import get_graph


class HtmlDataSource(DataSource):
    def get_configuration_parameters(self) -> dict[str, str]:
        return {"url": "str"}

    def get_name(self):
        return "HTML Data Source"

    def provide(self, **kwargs) -> Graph:
        url = kwargs.get("url", "https://www.google.com")

        return get_graph(url)
