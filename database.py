
import sqlite3

DB_NAME = "learning.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    """Create required tables if they do not already exist."""

    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                topic TEXT PRIMARY KEY,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                percentage REAL NOT NULL,
                attempted_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                is_correct INTEGER NOT NULL,
                FOREIGN KEY (attempt_id)
                    REFERENCES quiz_results(id)
                    ON DELETE CASCADE
            )
        """)


def save_progress(topic, completed):
    """Save or update completion status for a topic."""

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO progress (topic, completed)
            VALUES (?, ?)
            ON CONFLICT(topic)
            DO UPDATE SET completed = excluded.completed
        """, (topic, int(completed)))


def load_progress():
    """Return all completed topics as a set."""

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT topic
            FROM progress
            WHERE completed = 1
        """).fetchall()

    return {row[0] for row in rows}


def save_quiz_result(quiz_name, answers):
    """
    Save quiz score and individual answers.

    Each item in answers should contain:
    {
        "topic": "Functions",
        "is_correct": True
    }
    """

    score = sum(bool(item["is_correct"]) for item in answers)
    total = len(answers)
    percentage = (score / total * 100) if total else 0

    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO quiz_results
                (quiz_name, score, total, percentage)
            VALUES (?, ?, ?, ?)
        """, (quiz_name, score, total, percentage))

        attempt_id = cursor.lastrowid

        conn.executemany("""
            INSERT INTO quiz_answers
                (attempt_id, topic, is_correct)
            VALUES (?, ?, ?)
        """, [
            (
                attempt_id,
                item["topic"],
                int(bool(item["is_correct"]))
            )
            for item in answers
        ])

    return score, total, percentage


def load_quiz_results():
    """Return quiz attempts, newest first."""

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                id,
                quiz_name,
                score,
                total,
                percentage,
                attempted_at
            FROM quiz_results
            ORDER BY id DESC
        """).fetchall()

    return rows


def load_topic_performance():
    """Return topic-wise attempts, correct answers, and accuracy."""

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                topic,
                COUNT(*) AS attempts,
                SUM(is_correct) AS correct_answers,
                ROUND(
                    100.0 * SUM(is_correct) / COUNT(*),
                    1
                ) AS accuracy
            FROM quiz_answers
            GROUP BY topic
            ORDER BY accuracy ASC
        """).fetchall()

    return rows
