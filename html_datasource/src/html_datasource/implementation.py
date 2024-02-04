from api.components.data_source import DataSource
from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node

import requests
from bs4 import BeautifulSoup


def make_node(tag):
    id_ = tag.attrs.get("id", "")
    if id_ == "":
        id_ = str(hash(tag))
    data = {"tag": tag.name}
    if tag.name in ["a", "img"]:
        data["href"] = tag.attrs.get("href", "")
    if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "title"]:
        data["text"] = tag.text
    if tag.name == "input":
        data["type"] = tag.attrs.get("type", "")

    node = Node(id_, data)
    return node


def add_edges(nodes: list[Node], node: Node, graph: Graph):
    if node.edges is None:
        node.edges = []
    for n in nodes:
        e = Edge({}, node, n)
        node.edges.append(e)
        graph.add_edge(e)


class HtmlDataSource(DataSource):
    def get_configuration_parameters(self) -> dict[str, str]:
        return {"url": "str"}

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
        add_edges(nodes, node_from_element, graph)
        graph.add_node(node_from_element)
        return node_from_element

    def provide(self, **kwargs) -> Graph:
        url = kwargs.get("url", "https://www.google.com")
        g = Graph([], set())
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        root = soup.html

        self.recursive_html_traversal(g, root)
        return g


if __name__ == '__main__':
    # Create an instance of the HTML data source
    src = "https://www.google.com"
    html_data_source = HtmlDataSource()

    # Get the data from the HTML page
    gg = html_data_source.provide(url=src)
    found_element = next(filter(lambda x: x.data["tag"] == "html", gg.nodes), None)
