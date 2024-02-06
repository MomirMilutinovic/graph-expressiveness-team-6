import uuid

from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def make_node(tag) -> Node:
    id_ = _generate_id(tag)
    data = {"tag": tag.name}
    if tag.name in ["a", "img"]:
        data["href"] = tag.attrs.get("href", "")
    if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "title"]:
        data["text"] = tag.text
    if tag.name == "input":
        data["type"] = tag.attrs.get("type", "")

    node = Node(id_, data)
    return node


def _generate_id(tag) -> str:
    id_ = tag.attrs.get("id", "")
    if id_ == "":
        id_ = uuid.uuid4().hex
    id_ = f'{tag.name}#{id_}'
    return id_


def add_edges(nodes: list[Node], node: Node, graph: Graph):
    if node.edges is None:
        node.edges = []
    for n in nodes:
        e = Edge({}, node, n)
        graph.add_edge(e)


def driver_setup(url) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(5)
    return driver
