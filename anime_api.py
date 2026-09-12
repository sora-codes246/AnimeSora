import json
import urllib.parse
import urllib.request
import urllib.error


JIKAN_URL = "https://api.jikan.moe/v4"
KITSU_URL = "https://kitsu.io/api/edge"


# =========================================================
# GENERIC HTTP REQUEST
# =========================================================

def make_request(url, headers=None):

    request_headers = {
        "Accept": "application/json",
        "User-Agent": "AnimeSora/1.0"
    }

    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(
        url,
        headers=request_headers
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            return json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as error:

        print(
            f"HTTP error: {error.code} {error.reason}"
        )

        return None

    except urllib.error.URLError as error:

        print(
            "Could not connect to API:"
        )

        print(error)

        return None

    except TimeoutError:

        print(
            "API request timed out."
        )

        return None

    except Exception as error:

        print(
            "Unexpected API error:"
        )

        print(error)

        return None


# =========================================================
# JIKAN
# =========================================================

def format_jikan_anime(anime):

    images = anime.get(
        "images",
        {}
    )

    jpg = images.get(
        "jpg",
        {}
    )

    aired = anime.get(
        "aired",
        {}
    )

    return {

        "id": anime.get(
            "mal_id"
        ),

        "title": anime.get(
            "title"
        ),

        "title_english": anime.get(
            "title_english"
        ),

        "title_romaji": anime.get(
            "title"
        ),

        "title_native": anime.get(
            "title_japanese"
        ),

        "image": (
            jpg.get(
                "large_image_url"
            )
            or jpg.get(
                "image_url"
            )
        ),

        "episodes": anime.get(
            "episodes"
        ),

        "score": anime.get(
            "score"
        ),

        "status": anime.get(
            "status"
        ),

        "type": anime.get(
            "type"
        ),

        "start_date": aired.get(
            "from"
        ),

        "end_date": aired.get(
            "to"
        ),

        "synopsis": anime.get(
            "synopsis"
        ),

        "broadcast": anime.get(
            "broadcast",
            {}
        )
    }


def search_jikan(search):

    encoded_search = urllib.parse.quote(
        search
    )

    url = (
        f"{JIKAN_URL}/anime"
        f"?q={encoded_search}"
        f"&limit=10"
        f"&sfw=true"
    )

    result = make_request(
        url
    )

    if not result:
        return None

    return [
        format_jikan_anime(anime)
        for anime in result.get(
            "data",
            []
        )
    ]


# =========================================================
# KITSU FALLBACK
# =========================================================

def format_kitsu_anime(anime):

    attributes = anime.get(
        "attributes",
        {}
    )

    poster = attributes.get(
        "posterImage",
        {}
    )

    image = (
        poster.get("large")
        or poster.get("medium")
        or poster.get("small")
    )

    score = attributes.get(
        "averageRating"
    )

    if score:

        try:

            score = round(
                float(score) / 10,
                1
            )

        except (ValueError, TypeError):

            score = None

    status = attributes.get(
        "status"
    )

    status_map = {

        "current": "Currently Airing",

        "finished": "Finished Airing",

        "upcoming": "Not Yet Aired",

        "tba": "To Be Announced"

    }

    return {

        "id": anime.get(
            "id"
        ),

        "title": attributes.get(
            "canonicalTitle"
        ),

        "title_english": (
            attributes.get(
                "titles",
                {}
            ).get(
                "en"
            )
        ),

        "title_romaji": (
            attributes.get(
                "titles",
                {}
            ).get(
                "en_jp"
            )
        ),

        "title_native": (
            attributes.get(
                "titles",
                {}
            ).get(
                "ja_jp"
            )
        ),

        "image": image,

        "episodes": attributes.get(
            "episodeCount"
        ),

        "score": score,

        "status": status_map.get(
            status,
            status
        ),

        "type": attributes.get(
            "subtype"
        ),

        "start_date": attributes.get(
            "startDate"
        ),

        "end_date": attributes.get(
            "endDate"
        ),

        "synopsis": attributes.get(
            "synopsis"
        ),

        "broadcast": {}

    }


def search_kitsu(search):

    encoded_search = urllib.parse.quote(
        search
    )

    url = (
        f"{KITSU_URL}/anime"
        f"?filter[text]={encoded_search}"
        f"&page[limit]=10"
    )

    result = make_request(
        url,
        {
            "Accept": "application/vnd.api+json"
        }
    )

    if not result:
        return []

    return [
        format_kitsu_anime(anime)
        for anime in result.get(
            "data",
            []
        )
    ]


# =========================================================
# MAIN SEARCH
# =========================================================

def search_anime(search):

    search = search.strip()

    if not search:

        return []

    print(
        f"Searching for anime: {search}"
    )

    # ---------------------------------------------
    # Try Jikan first
    # ---------------------------------------------

    jikan_results = search_jikan(
        search
    )

    if jikan_results:

        print(
            "Search source: Jikan"
        )

        return jikan_results

    # ---------------------------------------------
    # Jikan failed -> Kitsu fallback
    # ---------------------------------------------

    print(
        "Jikan search failed."
    )

    print(
        "Switching to Kitsu fallback..."
    )

    kitsu_results = search_kitsu(
        search
    )

    print(
        f"Kitsu returned {len(kitsu_results)} results."
    )

    return kitsu_results


# =========================================================
# CURRENTLY AIRING
# =========================================================

def get_currently_airing(limit=20):

    url = (
        f"{JIKAN_URL}/top/anime"
        f"?filter=airing"
        f"&limit={limit}"
        f"&sfw=true"
    )

    result = make_request(
        url
    )

    if not result:

        return []

    return [
        format_jikan_anime(anime)
        for anime in result.get(
            "data",
            []
        )
    ]


# =========================================================
# WEEKLY SCHEDULE
# =========================================================

def get_weekly_schedule():

    url = (
        f"{JIKAN_URL}/schedules"
        f"?sfw=true"
    )

    result = make_request(
        url
    )

    if not result:

        return {}

    return result.get(
        "data",
        {}
    )