import sqlite3


DATABASE = "data/bot.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def initialize():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS Votes (
                server_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                target_user_id INTEGER NOT NULL,
                voter_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                PRIMARY KEY (server_id, message_id, voter_id, score)
            )
        """)
                           
        connection.execute("""
            CREATE TABLE IF NOT EXISTS Servers (
                server_id INTEGER PRIMARY KEY,
                leaderboard_channel_id INTEGER,
                highlights_channel_id INTEGER,
                vote_positive_emote TEXT NOT NULL,
                vote_negative_emote TEXT NOT NULL,
                highlights_threshold INTEGER NOT NULL DEFAULT 1
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS HighlightedMessages (
                server_id INTEGER NOT NULL,
                message_id INTEGER PRIMARY KEY,
                webhook_message_id INTEGER
            )
        """)


def add_vote(server_id, message_id, target_user_id, voter_id, score):
    with get_connection() as connection:
        connection.execute("""
            INSERT OR REPLACE INTO Votes (
                server_id,
                message_id,
                target_user_id,
                voter_id,
                score
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            server_id,
            message_id,
            target_user_id,
            voter_id,
            score
        ))


def remove_vote(message_id, voter_id, score):
    with get_connection() as connection:
        connection.execute("""
            DELETE FROM Votes
            WHERE message_id = ?
            AND voter_id = ?
            AND score = ?
        """, (message_id, voter_id, score))


def get_leaderboard(server_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT
                target_user_id,
                SUM(score) AS total_score
            FROM Votes
            WHERE server_id = ?
            GROUP BY target_user_id
            ORDER BY total_score DESC
        """, (server_id,))

        return cursor.fetchall()

def add_server(server_id):
    with get_connection() as connection:
        connection.execute("""
            INSERT OR IGNORE INTO Servers (
                server_id,
                leaderboard_channel_id,
                highlights_channel_id,
                vote_positive_emote,
                vote_negative_emote,
                highlights_threshold
            )
            VALUES (?, NULL, NULL, ?, ?, ?)
        """, (
            server_id,
            "🟩",
            "🟥",
            1
        ))

def get_server(server_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT
                server_id,
                leaderboard_channel_id,
                highlights_channel_id,
                vote_positive_emote,
                vote_negative_emote,
                highlights_threshold
            FROM Servers
            WHERE server_id = ?
        """, (server_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "server_id": row[0],
            "leaderboard_channel_id": row[1],
            "highlights_channel_id": row[2],
            "vote_positive_emote": row[3],
            "vote_negative_emote": row[4],
            "highlights_threshold": row[5],
        }

def set_leaderboard_channel(server_id, channel_id):
    with get_connection() as connection:
        connection.execute("""
            UPDATE Servers
            SET leaderboard_channel_id = ?
            WHERE server_id = ?
        """, (channel_id, server_id))


def set_highlights_channel(server_id, channel_id):
    with get_connection() as connection:
        connection.execute("""
            UPDATE Servers
            SET highlights_channel_id = ?
            WHERE server_id = ?
        """, (channel_id, server_id))


def set_vote_emotes(server_id, positive_emote, negative_emote):
    with get_connection() as connection:
        connection.execute("""
            UPDATE Servers
            SET vote_positive_emote = ?,
                vote_negative_emote = ?
            WHERE server_id = ?
        """, (positive_emote, negative_emote, server_id))


def set_highlights_threshold(server_id, threshold):
    with get_connection() as connection:
        connection.execute("""
            UPDATE Servers
            SET highlights_threshold = ?
            WHERE server_id = ?
        """, (threshold, server_id))

def get_votes_for_message(message_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT score
            FROM Votes
            WHERE message_id = ?
        """, (message_id,))

        return cursor.fetchall()

def add_vote(server_id, message_id, target_user_id, voter_id, score):
    with get_connection() as connection:
        connection.execute("""
            INSERT OR REPLACE INTO Votes (
                server_id,
                message_id,
                target_user_id,
                voter_id,
                score
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            server_id,
            message_id,
            target_user_id,
            voter_id,
            score
        ))

def remove_vote(message_id, voter_id, score):
    with get_connection() as connection:
        connection.execute("""
            DELETE FROM Votes
            WHERE message_id = ?
              AND voter_id = ?
              AND score = ?
        """, (
            message_id,
            voter_id,
            score
        ))

def add_highlighted_message(message_id):
    with get_connection() as connection:
        connection.execute("""
            INSERT OR IGNORE INTO HighlightedMessages (
                message_id
            )
            VALUES (?)
        """, (message_id,))


def is_message_highlighted(message_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT 1
            FROM HighlightedMessages
            WHERE message_id = ?
        """, (message_id,))

        return cursor.fetchone() is not None