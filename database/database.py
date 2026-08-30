"""
Andishkadeh Management & Market
SQLite Database Layer
"""

import os
import sqlite3
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from config import (
    DATABASE_PATH,
    DEFAULT_POINTS,
    DEFAULT_LEVEL,
)


class Database:
    """Central database manager for the bot."""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path

        directory = os.path.dirname(self.db_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        self.initialize()

    # ==========================================================
    # Connection
    # ==========================================================

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.db_path,
            timeout=30,
        )

        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    # ==========================================================
    # Initialization
    # ==========================================================

    def initialize(self) -> None:
        """Create required database tables."""

        with self._connect() as conn:

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TEXT NOT NULL,
                    last_seen TEXT NOT NULL,
                    points INTEGER NOT NULL DEFAULT 0,
                    level INTEGER NOT NULL DEFAULT 1,
                    current_course TEXT,
                    current_chapter TEXT
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    course TEXT NOT NULL,
                    chapter TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL,

                    UNIQUE(user_id, course, chapter),

                    FOREIGN KEY(user_id)
                        REFERENCES users(user_id)
                        ON DELETE CASCADE
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    course TEXT NOT NULL,
                    chapter TEXT,
                    score INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    created_at TEXT NOT NULL,

                    FOREIGN KEY(user_id)
                        REFERENCES users(user_id)
                        ON DELETE CASCADE
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_date TEXT NOT NULL UNIQUE,
                    course TEXT NOT NULL,
                    question TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    option_c TEXT NOT NULL,
                    option_d TEXT NOT NULL,
                    correct_option TEXT NOT NULL,
                    explanation TEXT
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    selected_option TEXT NOT NULL,
                    is_correct INTEGER NOT NULL,
                    answered_at TEXT NOT NULL,

                    UNIQUE(user_id, question_id),

                    FOREIGN KEY(user_id)
                        REFERENCES users(user_id)
                        ON DELETE CASCADE,

                    FOREIGN KEY(question_id)
                        REFERENCES daily_questions(id)
                        ON DELETE CASCADE
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    activity_type TEXT NOT NULL,
                    activity_data TEXT,
                    created_at TEXT NOT NULL,

                    FOREIGN KEY(user_id)
                        REFERENCES users(user_id)
                        ON DELETE CASCADE
                )
                """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_progress_user
                ON progress(user_id)
                """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_quiz_user
                ON quiz_results(user_id)
                """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_activity_user
                ON activity_log(user_id)
                """
            )

            conn.commit()

    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def _now() -> str:
        """Return current UTC timestamp."""

        return datetime.now(
            timezone.utc
        ).isoformat()

    # ==========================================================
    # Users
    # ==========================================================

    def create_or_update_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> None:
        """Create or update a Telegram user."""

        now = self._now()

        with self._connect() as conn:

            existing = conn.execute(
                """
                SELECT user_id
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

            if existing:

                conn.execute(
                    """
                    UPDATE users
                    SET
                        username = ?,
                        first_name = ?,
                        last_name = ?,
                        last_seen = ?
                    WHERE user_id = ?
                    """,
                    (
                        username,
                        first_name,
                        last_name,
                        now,
                        user_id,
                    ),
                )

            else:

                conn.execute(
                    """
                    INSERT INTO users (
                        user_id,
                        username,
                        first_name,
                        last_name,
                        created_at,
                        last_seen,
                        points,
                        level
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        username,
                        first_name,
                        last_name,
                        now,
                        now,
                        DEFAULT_POINTS,
                        DEFAULT_LEVEL,
                    ),
                )

            conn.commit()

    def get_user(
        self,
        user_id: int,
    ) -> Optional[Dict[str, Any]]:
        """Return user information."""

        with self._connect() as conn:

            row = conn.execute(
                """
                SELECT *
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

            if not row:
                return None

            return dict(row)

    # ==========================================================
    # Points
    # ==========================================================

    def add_points(
        self,
        user_id: int,
        points: int,
    ) -> Optional[Dict[str, Any]]:
        """Add points and calculate user level."""

        if points == 0:
            return self.get_user(user_id)

        with self._connect() as conn:

            row = conn.execute(
                """
                SELECT points
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

            if not row:
                return None

            new_points = max(
                0,
                row["points"] + points,
            )

            new_level = max(
                1,
                (new_points // 100) + 1,
            )

            conn.execute(
                """
                UPDATE users
                SET
                    points = ?,
                    level = ?
                WHERE user_id = ?
                """,
                (
                    new_points,
                    new_level,
                    user_id,
                ),
            )

            conn.commit()

        return self.get_user(user_id)

    # ==========================================================
    # Learning Progress
    # ==========================================================

    def save_progress(
        self,
        user_id: int,
        course: str,
        chapter: str,
        completed: bool = False,
    ) -> None:
        """Save or update learning progress."""

        now = self._now()

        with self._connect() as conn:

            conn.execute(
                """
                INSERT INTO progress (
                    user_id,
                    course,
                    chapter,
                    completed,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?)

                ON CONFLICT(user_id, course, chapter)
                DO UPDATE SET
                    completed = excluded.completed,
                    updated_at = excluded.updated_at
                """,
                (
                    user_id,
                    course,
                    chapter,
                    1 if completed else 0,
                    now,
                ),
            )

            conn.execute(
                """
                UPDATE users
                SET
                    current_course = ?,
                    current_chapter = ?,
                    last_seen = ?
                WHERE user_id = ?
                """,
                (
                    course,
                    chapter,
                    now,
                    user_id,
                ),
            )

            conn.commit()

    def get_progress(
        self,
        user_id: int,
        course: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Return learning progress."""

        with self._connect() as conn:

            if course:

                rows = conn.execute(
                    """
                    SELECT *
                    FROM progress
                    WHERE user_id = ?
                      AND course = ?
                    ORDER BY id
                    """,
                    (
                        user_id,
                        course,
                    ),
                ).fetchall()

            else:

                rows = conn.execute(
                    """
                    SELECT *
                    FROM progress
                    WHERE user_id = ?
                    ORDER BY id
                    """,
                    (user_id,),
                ).fetchall()

            return [
                dict(row)
                for row in rows
            ]

    # ==========================================================
    # Quiz Results
    # ==========================================================

    def save_quiz_result(
        self,
        user_id: int,
        course: str,
        score: int,
        total: int,
        chapter: Optional[str] = None,
    ) -> int:
        """Save a quiz result."""

        percentage = (
            round((score / total) * 100, 2)
            if total > 0
            else 0.0
        )

        now = self._now()

        with self._connect() as conn:

            cursor = conn.execute(
                """
                INSERT INTO quiz_results (
                    user_id,
                    course,
                    chapter,
                    score,
                    total,
                    percentage,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    course,
                    chapter,
                    score,
                    total,
                    percentage,
                    now,
                ),
            )

            conn.commit()

            return cursor.lastrowid

    def get_quiz_results(
        self,
        user_id: int,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Return latest quiz results."""

        with self._connect() as conn:

            rows = conn.execute(
                """
                SELECT *
                FROM quiz_results
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (
                    user_id,
                    limit,
                ),
            ).fetchall()

            return [
                dict(row)
                for row in rows
            ]

    # ==========================================================
    # Daily Questions
    # ==========================================================

    def add_daily_question(
        self,
        question_date: str,
        course: str,
        question: str,
        option_a: str,
        option_b: str,
        option_c: str,
        option_d: str,
        correct_option: str,
        explanation: Optional[str] = None,
    ) -> Optional[int]:
        """Add a daily question."""

        with self._connect() as conn:

            try:

                cursor = conn.execute(
                    """
                    INSERT INTO daily_questions (
                        question_date,
                        course,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_option,
                        explanation
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        question_date,
                        course,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_option,
                        explanation,
                    ),
                )

                conn.commit()

                return cursor.lastrowid

            except sqlite3.IntegrityError:

                return None

    def get_daily_question(
        self,
        question_date: str,
    ) -> Optional[Dict[str, Any]]:
        """Return daily question."""

        with self._connect() as conn:

            row = conn.execute(
                """
                SELECT *
                FROM daily_questions
                WHERE question_date = ?
                """,
                (question_date,),
            ).fetchone()

            if not row:
                return None

            return dict(row)

    # ==========================================================
    # Daily Answers
    # ==========================================================

    def save_daily_answer(
        self,
        user_id: int,
        question_id: int,
        selected_option: str,
        is_correct: bool,
    ) -> bool:
        """Save daily question answer."""

        now = self._now()

        with self._connect() as conn:

            try:

                conn.execute(
                    """
                    INSERT INTO daily_answers (
                        user_id,
                        question_id,
                        selected_option,
                        is_correct,
                        answered_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        question_id,
                        selected_option,
                        1 if is_correct else 0,
                        now,
                    ),
                )

                conn.commit()

                return True

            except sqlite3.IntegrityError:

                return False

    def has_answered_daily_question(
        self,
        user_id: int,
        question_id: int,
    ) -> bool:
        """Check whether user already answered."""

        with self._connect() as conn:

            row = conn.execute(
                """
                SELECT id
                FROM daily_answers
                WHERE user_id = ?
                  AND question_id = ?
                """,
                (
                    user_id,
                    question_id,
                ),
            ).fetchone()

            return row is not None

    # ==========================================================
    # Activity Log
    # ==========================================================

    def log_activity(
        self,
        user_id: int,
        activity_type: str,
        activity_data: Optional[str] = None,
    ) -> None:
        """Store user activity."""

        with self._connect() as conn:

            conn.execute(
                """
                INSERT INTO activity_log (
                    user_id,
                    activity_type,
                    activity_data,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    activity_type,
                    activity_data,
                    self._now(),
                ),
            )

            conn.commit()

    def get_recent_activity(
        self,
        user_id: int,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Return recent user activity."""

        with self._connect() as conn:

            rows = conn.execute(
                """
                SELECT *
                FROM activity_log
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (
                    user_id,
                    limit,
                ),
            ).fetchall()

            return [
                dict(row)
                for row in rows
            ]

    # ==========================================================
    # Statistics
    # ==========================================================

    def get_user_statistics(
        self,
        user_id: int,
    ) -> Dict[str, Any]:
        """Return user statistics."""

        with self._connect() as conn:

            quiz_count = conn.execute(
                """
                SELECT COUNT(*)
                FROM quiz_results
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()[0]

            completed_lessons = conn.execute(
                """
                SELECT COUNT(*)
                FROM progress
                WHERE user_id = ?
                  AND completed = 1
                """,
                (user_id,),
            ).fetchone()[0]

            total_lessons = conn.execute(
                """
                SELECT COUNT(*)
                FROM progress
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()[0]

            activity_count = conn.execute(
                """
                SELECT COUNT(*)
                FROM activity_log
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()[0]

            user = conn.execute(
                """
                SELECT points, level
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

            return {
                "points": user["points"] if user else 0,
                "level": user["level"] if user else 1,
                "quiz_count": quiz_count,
                "completed_lessons": completed_lessons,
                "total_lessons": total_lessons,
                "activity_count": activity_count,
            }
