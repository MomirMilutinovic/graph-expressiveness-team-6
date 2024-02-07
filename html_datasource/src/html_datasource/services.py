from bs4 import BeautifulSoup

from api.models.edge import Edge
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
    handle_self_pointing_hrefs(g)
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


def handle_self_pointing_hrefs(graph: Graph):
    for node in graph.nodes:
        if node.data.get("tag") == "a":
            href = node.data.get("href")
            if not href or not href.startswith("#"):
                continue
            if href == "#":
                dest_node = _find_node_by_id(graph, "html")
                if dest_node:
                    graph.add_edge(Edge({}, node, dest_node))
            else:
                dest_id = href[1:]
                dest_node = _find_node_by_id(graph, dest_id)
                if dest_node:
                    graph.add_edge(Edge({}, node, dest_node))
    return graph


def _find_node_by_id(graph: Graph, sub_id: str):
    return next((n for n in graph.nodes if sub_id in n.id), None)
