import json
import urllib.parse
import urllib.request
import urllib.error


KITSU_URL = "https://kitsu.io/api/edge"


def search_anime(search):
    """
    Search Kitsu for anime.
    """

    encoded_search = urllib.parse.quote(search)

    url = (
        f"{KITSU_URL}/anime"
        f"?filter[text]={encoded_search}"
        f"&page[limit]=10"
    )

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.api+json",
            "User-Agent": "AnimeSora/1.0"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        anime_results = []

        for anime in result.get("data", []):

            attributes = anime.get(
                "attributes",
                {}
            )

            titles = attributes.get(
                "titles",
                {}
            )

            poster = attributes.get(
                "posterImage",
                {}
            )

            anime_results.append({

                "id": anime.get("id"),

                "title": (
                    titles.get("en")
                    or titles.get("en_jp")
                    or titles.get("ja_jp")
                    or attributes.get("canonicalTitle")
                ),

                "title_english": titles.get(
                    "en"
                ),

                "title_romaji": titles.get(
                    "en_jp"
                ),

                "title_native": titles.get(
                    "ja_jp"
                ),

                "image": (
                    poster.get("large")
                    or poster.get("medium")
                    or poster.get("small")
                ),

                "episodes": attributes.get(
                    "episodeCount"
                ),

                # Kitsu ratings are out of 100.
                # AnimeSora uses a 10-point scale.
                "score": (
                    round(
                        float(attributes["averageRating"]) / 10,
                        2
                    )
                    if attributes.get("averageRating")
                    else None
                ),

                "status": attributes.get(
                    "status"
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

                "next_episode": None

            })

        return anime_results


    except urllib.error.HTTPError as error:

        print(
            f"Kitsu HTTP error: "
            f"{error.code} {error.reason}"
        )

        return []


    except urllib.error.URLError as error:

        print(
            "Could not connect to Kitsu:"
        )

        print(error)

        return []


    except TimeoutError:

        print(
            "Kitsu request timed out."
        )

        return []


    except Exception as error:

        print(
            "Unexpected Kitsu error:"
        )

        print(error)

        return []