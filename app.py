from flask import Flask, render_template, request, redirect, url_for

from database import (
    initialize_database,
    get_all_anime,
    get_anime,
    add_anime,
    update_anime,
    delete_anime
)

from anime_api import search_anime
from anime_data import search_local_anime


app = Flask(__name__)


initialize_database()


# ========================================
# HOME
# ========================================

@app.route("/")
def home():

    anime = get_all_anime()

    return render_template(
        "index.html",
        anime=anime
    )


# ========================================
# SCHEDULE
# ========================================

@app.route("/schedule")
def schedule():

    return render_template(
        "schedule.html"
    )


# ========================================
# MY ANIME
# ========================================

@app.route("/my-anime")
def my_anime():

    anime = get_all_anime()

    return render_template(
        "my_anime.html",
        anime=anime,
        search_results=[],
        search_query="",
        search_performed=False
    )


# ========================================
# SEARCH ANIME
# ========================================

@app.route("/search-anime")
def search_anime_route():

    search_query = request.args.get(
        "q",
        ""
    ).strip()


    if not search_query:

        return redirect(
            url_for("my_anime")
        )


    # Try the live Kitsu API first
    search_results = search_anime(
        search_query
    )


    # Use local fallback if API is unavailable
    if not search_results:

        search_results = search_local_anime(
            search_query
        )


    anime = get_all_anime()


    return render_template(
        "my_anime.html",
        anime=anime,
        search_results=search_results,
        search_query=search_query,
        search_performed=True
    )


# ========================================
# ADD ANIME
# ========================================

@app.route("/add-anime", methods=["POST"])
def add_anime_route():

    title = request.form.get(
        "title",
        ""
    ).strip()


    if not title:

        return redirect(
            url_for("my_anime")
        )


    # User's tracking status
    status = request.form.get(
        "status",
        "Plan to Watch"
    )


    # Current episode
    current_episode = request.form.get(
        "current_episode",
        "0"
    )


    # Total episodes
    total_episodes = request.form.get(
        "total_episodes",
        ""
    )


    # User score
    score = request.form.get(
        "score",
        ""
    )


    # Anime information from API
    title_english = request.form.get(
        "title_english",
        ""
    )


    title_romaji = request.form.get(
        "title_romaji",
        ""
    )


    title_native = request.form.get(
        "title_native",
        ""
    )


    poster = request.form.get(
        "poster",
        ""
    )


    anime_status = request.form.get(
        "anime_status",
        ""
    )


    anime_type = request.form.get(
        "anime_type",
        ""
    )


    start_date = request.form.get(
        "start_date",
        ""
    )


    end_date = request.form.get(
        "end_date",
        ""
    )


    synopsis = request.form.get(
        "synopsis",
        ""
    )


    release_day = request.form.get(
        "release_day",
        ""
    )


    # ----------------------------------------
    # Convert numeric values safely
    # ----------------------------------------

    try:

        current_episode = int(
            current_episode
        )

    except ValueError:

        current_episode = 0


    try:

        total_episodes = (
            int(total_episodes)
            if total_episodes
            else None
        )

    except ValueError:

        total_episodes = None


    try:

        score = (
            float(score)
            if score
            else None
        )

    except ValueError:

        score = None


    # Prevent negative episode numbers
    if current_episode < 0:

        current_episode = 0


    # Prevent going beyond total episodes
    if (
        total_episodes is not None
        and current_episode > total_episodes
    ):

        current_episode = total_episodes


    # ----------------------------------------
    # Save everything
    # ----------------------------------------

    add_anime(
        title=title,

        title_english=title_english or None,

        title_romaji=title_romaji or None,

        title_native=title_native or None,

        status=status,

        current_episode=current_episode,

        total_episodes=total_episodes,

        score=score,

        poster=poster or None,

        anime_status=anime_status or None,

        anime_type=anime_type or None,

        start_date=start_date or None,

        end_date=end_date or None,

        synopsis=synopsis or None,

        release_day=release_day or None
    )


    return redirect(
        url_for("my_anime")
    )


# ========================================
# EDIT ANIME
# ========================================

@app.route("/edit-anime/<int:anime_id>", methods=["POST"])
def edit_anime(anime_id):

    anime = get_anime(
        anime_id
    )


    if not anime:

        return redirect(
            url_for("my_anime")
        )


    status = request.form.get(
        "status",
        "Plan to Watch"
    )


    current_episode = request.form.get(
        "current_episode",
        "0"
    )


    score = request.form.get(
        "score",
        ""
    )


    try:

        current_episode = int(
            current_episode
        )

    except ValueError:

        current_episode = 0


    try:

        score = (
            float(score)
            if score
            else None
        )

    except ValueError:

        score = None


    if current_episode < 0:

        current_episode = 0


    if (
        anime["total_episodes"] is not None
        and current_episode > anime["total_episodes"]
    ):

        current_episode = anime[
            "total_episodes"
        ]


    update_anime(
        anime_id=anime_id,

        status=status,

        current_episode=current_episode,

        score=score
    )


    return redirect(
        url_for("my_anime")
    )


# ========================================
# DELETE ANIME
# ========================================

@app.route("/delete-anime/<int:anime_id>", methods=["POST"])
def delete_anime_route(anime_id):

    delete_anime(
        anime_id
    )


    return redirect(
        url_for("my_anime")
    )


# ========================================
# RUN APPLICATION
# ========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )