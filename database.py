import os

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Make sure your .env file contains DATABASE_URL."
        )

    connection = psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anime (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Plan to Watch',
                    current_episode INTEGER NOT NULL DEFAULT 0,
                    total_episodes INTEGER,
                    score REAL,
                    poster TEXT,
                    release_day TEXT
                )
            """)

        connection.commit()

    finally:

        connection.close()


# =========================================================
# GET ALL ANIME
# =========================================================

def get_all_anime():

    connection = get_connection()

    try:

        with connection.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
                SELECT *
                FROM anime
                ORDER BY title
            """)

            anime = cursor.fetchall()

            return anime

    finally:

        connection.close()


# =========================================================
# GET SINGLE ANIME
# =========================================================

def get_anime(anime_id):

    connection = get_connection()

    try:

        with connection.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
                SELECT *
                FROM anime
                WHERE id = %s
            """, (anime_id,))

            anime = cursor.fetchone()

            return anime

    finally:

        connection.close()


# =========================================================
# ADD ANIME
# =========================================================

def add_anime(
    title,
    status="Plan to Watch",
    current_episode=0,
    total_episodes=None,
    score=None,
    poster=None,
    release_day=None
):

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                INSERT INTO anime (
                    title,
                    status,
                    current_episode,
                    total_episodes,
                    score,
                    poster,
                    release_day
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                title,
                status,
                current_episode,
                total_episodes,
                score,
                poster,
                release_day
            ))

        connection.commit()

    finally:

        connection.close()


# =========================================================
# UPDATE ANIME
# =========================================================

def update_anime(
    anime_id,
    status,
    current_episode,
    score
):

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                UPDATE anime
                SET
                    status = %s,
                    current_episode = %s,
                    score = %s
                WHERE id = %s
            """, (
                status,
                current_episode,
                score,
                anime_id
            ))

        connection.commit()

    finally:

        connection.close()


# =========================================================
# DELETE ANIME
# =========================================================

def delete_anime(anime_id):

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                DELETE FROM anime
                WHERE id = %s
            """, (anime_id,))

        connection.commit()

    finally:

        connection.close()