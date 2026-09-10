import sqlite3
from pathlib import Path


# ========================================
# DATABASE
# ========================================

DATABASE = Path("animesora.db")


# ========================================
# CONNECTION
# ========================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


# ========================================
# INITIALIZE DATABASE
# ========================================

def initialize_database():

    connection = get_connection()


    # ----------------------------------------
    # Create the table if it doesn't exist
    # ----------------------------------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS anime (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            title_english TEXT,

            title_romaji TEXT,

            title_native TEXT,

            status TEXT NOT NULL
                DEFAULT 'Plan to Watch',

            current_episode INTEGER NOT NULL
                DEFAULT 0,

            total_episodes INTEGER,

            score REAL,

            poster TEXT,

            anime_status TEXT,

            anime_type TEXT,

            start_date TEXT,

            end_date TEXT,

            synopsis TEXT,

            release_day TEXT
        )
    """)


    # ----------------------------------------
    # Automatically upgrade old databases
    # ----------------------------------------

    existing_columns = [

        row["name"]

        for row in connection.execute(
            "PRAGMA table_info(anime)"
        ).fetchall()

    ]


    new_columns = {

        "title_english": "TEXT",

        "title_romaji": "TEXT",

        "title_native": "TEXT",

        "anime_status": "TEXT",

        "anime_type": "TEXT",

        "start_date": "TEXT",

        "end_date": "TEXT",

        "synopsis": "TEXT"

    }


    for column_name, column_type in new_columns.items():

        if column_name not in existing_columns:

            connection.execute(
                f"""
                ALTER TABLE anime
                ADD COLUMN {column_name} {column_type}
                """
            )


    connection.commit()

    connection.close()


# ========================================
# GET ALL ANIME
# ========================================

def get_all_anime():

    connection = get_connection()


    anime = connection.execute("""
        SELECT *
        FROM anime
        ORDER BY title
    """).fetchall()


    connection.close()


    return anime


# ========================================
# GET ONE ANIME
# ========================================

def get_anime(anime_id):

    connection = get_connection()


    anime = connection.execute("""
        SELECT *
        FROM anime
        WHERE id = ?
    """, (
        anime_id,
    )).fetchone()


    connection.close()


    return anime


# ========================================
# ADD ANIME
# ========================================

def add_anime(

    title,

    title_english=None,

    title_romaji=None,

    title_native=None,

    status="Plan to Watch",

    current_episode=0,

    total_episodes=None,

    score=None,

    poster=None,

    anime_status=None,

    anime_type=None,

    start_date=None,

    end_date=None,

    synopsis=None,

    release_day=None

):

    connection = get_connection()


    connection.execute("""
        INSERT INTO anime (

            title,

            title_english,

            title_romaji,

            title_native,

            status,

            current_episode,

            total_episodes,

            score,

            poster,

            anime_status,

            anime_type,

            start_date,

            end_date,

            synopsis,

            release_day

        )

        VALUES (

            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?

        )
    """, (

        title,

        title_english,

        title_romaji,

        title_native,

        status,

        current_episode,

        total_episodes,

        score,

        poster,

        anime_status,

        anime_type,

        start_date,

        end_date,

        synopsis,

        release_day

    ))


    connection.commit()

    connection.close()


# ========================================
# UPDATE ANIME
# ========================================

def update_anime(

    anime_id,

    status,

    current_episode,

    score

):

    connection = get_connection()


    connection.execute("""
        UPDATE anime

        SET

            status = ?,

            current_episode = ?,

            score = ?

        WHERE id = ?
    """, (

        status,

        current_episode,

        score,

        anime_id

    ))


    connection.commit()

    connection.close()


# ========================================
# DELETE ANIME
# ========================================

def delete_anime(anime_id):

    connection = get_connection()


    connection.execute("""
        DELETE FROM anime
        WHERE id = ?
    """, (
        anime_id,
    ))


    connection.commit()

    connection.close()