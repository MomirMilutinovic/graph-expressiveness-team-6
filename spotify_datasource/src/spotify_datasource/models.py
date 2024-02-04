class Artist:
    def __init__(self, artist_body: dict) -> None:
        self.id = artist_body["id"]
        self.name = artist_body["name"]
        self.popularity = artist_body["popularity"]
        self.genres = artist_body["genres"]
        self.followers = artist_body["followers"]["total"]

    def __str__(self) -> str:
        return f"{self.id}, {self.name}, {self.popularity}, {self.genres}, {self.followers}"
