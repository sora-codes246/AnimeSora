import sqlite3

from database import get_connection, initialize_database


SQLITE_DATABASE = "animesora.db"


def get_sqlite_anime():

    connection = sqlite3.connect(
        SQLITE_DATABASE
    )

    connection.row_factory = sqlite3.Row

    try:

        anime = connection.execute("""
            SELECT
                id,
                title,
                status,
                current_episode,
                total_episodes,
                score,
                poster,
                release_day
            FROM anime
            ORDER BY id
        """).fetchall()

        return anime

    finally:

        connection.close()


def migrate():

    print("Reading local SQLite database...")

    anime_list = get_sqlite_anime()

    print(
        f"Found {len(anime_list)} anime "
        "in the local database."
    )

    print("Connecting to Supabase...")

    initialize_database()

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            for anime in anime_list:

                cursor.execute("""
                    INSERT INTO anime (
                        id,
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
                        %s,
                        %s
                    )
                    ON CONFLICT (id)
                    DO UPDATE SET
                        title = EXCLUDED.title,
                        status = EXCLUDED.status,
                        current_episode = EXCLUDED.current_episode,
                        total_episodes = EXCLUDED.total_episodes,
                        score = EXCLUDED.score,
                        poster = EXCLUDED.poster,
                        release_day = EXCLUDED.release_day
                """, (
                    anime["id"],
                    anime["title"],
                    anime["status"],
                    anime["current_episode"],
                    anime["total_episodes"],
                    anime["score"],
                    anime["poster"],
                    anime["release_day"]
                ))

            cursor.execute("""
                SELECT setval(
                    pg_get_serial_sequence(
                        'anime',
                        'id'
                    ),
                    COALESCE(
                        (SELECT MAX(id) FROM anime),
                        1
                    ),
                    true
                )
            """)

        connection.commit()

    finally:

        connection.close()

    print()
    print("========================================")
    print("Migration completed successfully.")
    print("========================================")


if __name__ == "__main__":
    migrate()