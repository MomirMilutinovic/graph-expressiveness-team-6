from api.components.data_source import DataSource
from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node

import requests
from bs4 import BeautifulSoup


def make_node(tag):
    guid = str(hash(tag))
    data = {"tag": tag.name, "text": tag.text}
    node = Node(guid, data)
    return node


def add_edges(nodes: list[Node], node: Node):
    if node.edges is None:
        node.edges = []
    for n in nodes:
        e = Edge({}, node, n)
        node.edges.append(e)


class HtmlDataSource(DataSource):
    def get_name(self):
        return "HTML Data Source"

    def recursive_html_traversal(self, graph: Graph, element):
        nodes = []
        # Recursively traverse all children of the current element
        for child in element.children:
            if child.name is None:
                continue
            if child.name in ["script", "style", "meta", "link"]:
                continue

            node_from_child = self.recursive_html_traversal(graph, child)
            nodes.append(node_from_child)

        node_from_element = make_node(element)
        add_edges(nodes, node_from_element)
        graph.add_node(node_from_element)
        return node_from_element

    def provide(self) -> Graph:
        g = Graph([], set())
        # response = requests.get(self.url)
        # soup = BeautifulSoup(response.content, 'html.parser')
        with open(self.url, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        root = soup.html

        self.recursive_html_traversal(g, root)
        return g

    def __init__(self, url):
        self.url = url


if __name__ == '__main__':
    # Create an instance of the HTML data source
    src = "E:/balsa/faks/treca godina/softverski obrasci i komponente/index.html"
    html_data_source = HtmlDataSource(src)

    # Get the data from the HTML page
    gg = html_data_source.provide()
    found_element = next(filter(lambda x: x.data["tag"] == "html", gg.nodes), None)

    pass
