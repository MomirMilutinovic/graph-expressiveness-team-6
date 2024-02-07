from .utils import *
from api.models.edge import Edge
from api.models.node import Node
from api.models.graph import Graph


def get_graph(
    auth_token: str,
    artist_name: str = "Gunna",
    max_neighbours: int = 10,
    recursion_depth: int = 2,
) -> Graph:
    artist = get_artist_by_name(auth_token, artist_name)
    graph = Graph(directed=False)
    processed_artist_ids = set()

    process_artists_recursively(
        auth_token, artist, max_neighbours, recursion_depth, graph, processed_artist_ids
    )

    return graph


def process_artists_recursively(
    auth_token: str,
    artist: Artist,
    max_neighbours: int,
    recursion_depth: int,
    graph: Graph,
    processed_artist_ids: set[str],
):
    if recursion_depth == 0:
        return

    if artist.id in processed_artist_ids:
        return

    rel_artists = get_related_artists(auth_token, artist.id, max_neighbours)
    processed_artist_ids.add(artist.id)

    for i, rel_artist in enumerate(rel_artists):
        if i > max_neighbours - 1:
            break

        process_artists_recursively(
            auth_token,
            rel_artist,
            max_neighbours,
            recursion_depth - 1,
            graph,
            processed_artist_ids,
        )

        src = Node(artist.id, vars(artist))
        dest = Node(rel_artist.id, vars(rel_artist))
        edge = Edge({}, src, dest)

        graph.add_edge(edge)
