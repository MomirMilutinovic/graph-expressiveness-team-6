from api.components.data_source import DataSource
from api.models.graph import Graph, Node

import requests
from bs4 import BeautifulSoup


class HtmlDataSource(DataSource):
    def get_name(self):
        return "HTML Data Source"

    def provide(self) -> Graph:
        g = Graph([], set())
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_elements = soup.find_all()
        for element in all_elements:
            guid = str(hash(element))
            n = Node(guid, element.name)
            g.add_node(n)
        return g

    def __init__(self, url):
        self.url = url


if __name__ == '__main__':
    # Create an instance of the HTML data source
    html_data_source = HtmlDataSource("https://www.google.com")

    # Get the data from the HTML page
    g = html_data_source.provide()
    pass
