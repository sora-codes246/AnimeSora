from datetime import date, timedelta
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from database import (
    initialize_database,
    get_all_anime,
    get_anime,
    add_anime,
    update_anime,
    delete_anime
)

from anime_api import (
    search_anime,
    get_currently_airing,
    get_weekly_schedule
)

from anime_data import search_local_anime


app = Flask(__name__)

# Secret key used to securely manage login sessions.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "animesora-local-development-key"
)

# Password is stored as an environment variable.
APP_PASSWORD = os.environ.get(
    "ANIMESORA_PASSWORD",
    ""
)


initialize_database()


@app.before_request
def require_login():

    # These pages are always accessible.
    allowed_routes = {
        "login",
        "static"
    }

    if request.endpoint in allowed_routes:
        return

    # If the user is not logged in,
    # send them to the lock screen.
    if not session.get("authenticated"):
        return redirect(
            url_for("login")
        )


@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        if password == APP_PASSWORD and APP_PASSWORD:

            session["authenticated"] = True

            return redirect(
                url_for("home")
            )

        error = "Incorrect password."

    return render_template(
        "login.html",
        error=error
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


@app.route("/")
def home():

    anime = get_all_anime()

    return render_template(
        "index.html",
        anime=anime
    )


@app.route("/schedule")
def schedule():

    airing_anime = get_currently_airing(
        limit=10
    )

    today = date.today()

    days_since_sunday = (
        today.weekday() + 1
    ) % 7

    sunday = (
        today
        - timedelta(
            days=days_since_sunday
        )
    )

    schedule_days = []

    for day_number in range(7):

        current_date = (
            sunday
            + timedelta(
                days=day_number
            )
        )

        schedule_days.append({
            "name": current_date.strftime(
                "%A"
            ),

            "date": current_date,

            "date_display": current_date.strftime(
                "%d"
            ),

            "episodes": []
        })


    for anime in airing_anime:

        episodes = get_weekly_schedule(
            anime["id"],
            limit=10
        )

        for episode in episodes:

            airdate = episode.get(
                "airdate"
            )

            if not airdate:
                continue

            try:

                episode_date = date.fromisoformat(
                    airdate[:10]
                )

            except ValueError:

                continue

            if (
                episode_date < sunday
                or episode_date > sunday + timedelta(days=6)
            ):

                continue

            day_index = (
                episode_date - sunday
            ).days

            schedule_days[
                day_index
            ]["episodes"].append({

                "anime": anime,

                "episode": episode

            })


    for day in schedule_days:

        day["episodes"].sort(
            key=lambda item: (
                item["episode"].get("airdate")
                or "",
                item["anime"].get("title")
                or ""
            )
        )


    return render_template(
        "schedule.html",
        schedule_days=schedule_days,
        today=today
    )


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


    search_results = search_anime(
        search_query
    )


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


@app.route("/add-anime", methods=["POST"])
def add_anime_route():

    title = request.form.get(
        "title",
        ""
    ).strip()

    status = request.form.get(
        "status",
        "Plan to Watch"
    )

    current_episode = request.form.get(
        "current_episode",
        "0"
    )

    total_episodes = request.form.get(
        "total_episodes",
        ""
    )

    score = request.form.get(
        "score",
        ""
    )

    poster = request.form.get(
        "poster",
        ""
    )


    if not title:

        return redirect(
            url_for("my_anime")
        )


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


    add_anime(
        title=title,
        status=status,
        current_episode=current_episode,
        total_episodes=total_episodes,
        score=score,
        poster=poster or None
    )


    return redirect(
        url_for("my_anime")
    )


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
        anime["total_episodes"]
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


@app.route("/delete-anime/<int:anime_id>", methods=["POST"])
def delete_anime_route(anime_id):

    delete_anime(
        anime_id
    )

    return redirect(
        url_for("my_anime")
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )