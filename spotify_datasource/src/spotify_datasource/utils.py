import requests
from .models import Artist


def get_artist_by_name(auth_token: str, artist_name: str) -> Artist:
    try:
        response = requests.get(
            f"https://api.spotify.com/v1/search?q={artist_name}&type=artist",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
    except Exception:
        raise Exception("Error happened while fetching Spotify data")

    body = response.json()
    try:
        artist_results = body["artists"]["items"]
    except Exception:
        raise Exception("Auth token expired!")

    if len(artist_results) > 0:
        return Artist(artist_results[0])
    else:
        raise Exception("Error while fetching artists, check the search query")


def get_related_artists(
    auth_token: str, artist_id: str, max_neighbours: int = 20
) -> list[Artist]:
    try:
        response = requests.get(
            f"https://api.spotify.com/v1/artists/{artist_id}/related-artists",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
    except Exception:
        raise Exception("Error happened while fetching Spotify data")

    body = response.json()
    artist_results = body["artists"]
    related_artists = []

    for i, artist in enumerate(artist_results):
        if i > max_neighbours:
            break

        related_artists.append(Artist(artist))

    return related_artists
