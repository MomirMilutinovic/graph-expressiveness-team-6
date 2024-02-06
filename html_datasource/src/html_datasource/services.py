from bs4 import BeautifulSoup
from .utils import driver_setup, make_node, add_edges

from api.models.graph import Graph


def get_graph(url):
    g = Graph([], set())
    driver = driver_setup(url)
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, 'html.parser')
    root = soup.html
    recursive_html_traversal(g, root)
    return g


def recursive_html_traversal(graph: Graph, element):
    nodes = []

    for child in element.children:
        if child.name is None:
            continue
        if child.name in ["script", "style", "meta", "link"]:
            continue

        node_from_child = recursive_html_traversal(graph, child)
        nodes.append(node_from_child)

    node_from_element = make_node(element)
    add_edges(nodes, node_from_element, graph)
    graph.add_node(node_from_element)
    return node_from_element
