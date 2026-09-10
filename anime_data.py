ANIME_CATALOG = [

    {
        "id": 21,
        "title": "One Piece",
        "title_english": "One Piece",
        "image": "",
        "episodes": 0,
        "score": 8.7,
        "status": "Currently Airing",
        "type": "TV"
    },

    {
        "id": 20,
        "title": "Naruto",
        "title_english": "Naruto",
        "image": "",
        "episodes": 220,
        "score": 8.0,
        "status": "Finished Airing",
        "type": "TV"
    },

    {
        "id": 1735,
        "title": "Naruto: Shippuden",
        "title_english": "Naruto: Shippuden",
        "image": "",
        "episodes": 500,
        "score": 8.2,
        "status": "Finished Airing",
        "type": "TV"
    },

    {
        "id": 16498,
        "title": "Attack on Titan",
        "title_english": "Attack on Titan",
        "image": "",
        "episodes": 25,
        "score": 8.5,
        "status": "Finished Airing",
        "type": "TV"
    },

    {
        "id": 11061,
        "title": "Hunter x Hunter",
        "title_english": "Hunter x Hunter",
        "image": "",
        "episodes": 148,
        "score": 9.0,
        "status": "Finished Airing",
        "type": "TV"
    }

]


def search_local_anime(search):

    search = search.lower().strip()

    if not search:
        return []

    results = []

    for anime in ANIME_CATALOG:

        title = anime["title"].lower()

        english_title = (
            anime["title_english"] or ""
        ).lower()

        if (
            search in title
            or search in english_title
        ):

            results.append(anime)

    return results