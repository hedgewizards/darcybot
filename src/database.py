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
                leaderboard_message_id INTEGER,
                vote_positive_emote TEXT NOT NULL,
                vote_negative_emote TEXT NOT NULL,
                highlights_threshold INTEGER NOT NULL DEFAULT 1,
                leaderboard_size INTEGER NOT NULL DEFAULT 10
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS HighlightedMessages (
                server_id INTEGER NOT NULL,
                message_id INTEGER PRIMARY KEY,
                webhook_message_id INTEGER
            )
        """)
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_votes_user_id
                ON Votes(target_user_id, server_id, score);
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
                leaderboard_message_id,
                highlights_channel_id,
                vote_positive_emote,
                vote_negative_emote,
                highlights_threshold,
                leaderboard_size
            FROM Servers
            WHERE server_id = ?
        """, (server_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "server_id": row[0],
            "leaderboard_channel_id": row[1],
            "leaderboard_message_id": row[2],
            "highlights_channel_id": row[3],
            "vote_positive_emote": row[4],
            "vote_negative_emote": row[5],
            "highlights_threshold": row[6],
            "leaderboard_size": row[7]
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

def add_highlighted_message(server_id, message_id, webhook_message_id):
    with get_connection() as connection:
        connection.execute("""
            INSERT OR IGNORE INTO HighlightedMessages (
                server_id, message_id, webhook_message_id
            )
            VALUES (?, ?, ?)
        """, (server_id, message_id, webhook_message_id,))

# returns the bot webhook message for an associated highlight
def get_message_highlight(message_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT webhook_message_id
            FROM HighlightedMessages
            WHERE message_id = ?
        """, (message_id,))

        row = cursor.fetchone()
        return row[0] if row else None

def is_message_highlighted(message_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT 1
            FROM HighlightedMessages
            WHERE message_id = ?
        """, (message_id,))

        return cursor.fetchone() is not None
    
def get_user_vote_count(
    server_id,
    target_user_id,
    score
):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT COUNT(*)
            FROM Votes
            WHERE server_id = ?
              AND target_user_id = ?
              AND score = ?
        """, (
            server_id,
            target_user_id,
            score
        ))

        return cursor.fetchone()[0]


def get_top_voted_users(
    server_id,
    score,
    limit
):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT
                target_user_id,
                COUNT(*) AS vote_count
            FROM Votes
            WHERE server_id = ?
              AND score = ?
            GROUP BY target_user_id
            ORDER BY vote_count DESC
            LIMIT ?
        """, (
            server_id,
            score,
            limit
        ))

        return cursor.fetchall()
    
def set_leaderboard_message_id(server_id, message_id):
    with get_connection() as connection:
        connection.execute("""
            UPDATE Servers
            SET leaderboard_message_id = ?
            WHERE server_id = ?
        """, (message_id, server_id))