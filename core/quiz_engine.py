"""
Central Quiz Engine for Andishkadeh Management & Market.

Responsibilities:
- Create quiz sessions
- Manage question order
- Validate answers
- Track correct / wrong answers
- Calculate score
- Complete quiz
- Cancel quiz
- Keep user sessions isolated
- Provide serializable quiz state
- Remain independent from Telegram handlers

Integration:
- Management handlers
- Exam handlers
- Statistics
- Progress

The engine does NOT depend on Telegram Update objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from typing import Any, Iterable, Mapping, Sequence
import random


# ==========================================================
# Constants
# ==========================================================

DEFAULT_SCORE_PRECISION = 2

STATUS_ACTIVE = "active"
STATUS_COMPLETED = "completed"
STATUS_CANCELLED = "cancelled"

RESULT_CORRECT = "correct"
RESULT_WRONG = "wrong"
RESULT_FINISHED = "finished"


# ==========================================================
# Helpers
# ==========================================================

def _utc_now() -> str:
    """Return the current UTC timestamp as ISO text."""
    return datetime.now(timezone.utc).isoformat()


def calculate_score(
    correct_answers: int,
    total_questions: int,
) -> float:
    """
    Calculate quiz score as percentage.
    """

    if total_questions <= 0:
        raise ValueError(
            "total_questions must be greater than zero."
        )

    if correct_answers < 0:
        raise ValueError(
            "correct_answers cannot be negative."
        )

    if correct_answers > total_questions:
        raise ValueError(
            "correct_answers cannot exceed total_questions."
        )

    return round(
        correct_answers
        / total_questions
        * 100,
        DEFAULT_SCORE_PRECISION,
    )


# ==========================================================
# Quiz Question
# ==========================================================

@dataclass(frozen=True)
class QuizQuestion:
    """
    Normalized quiz question.

    Supported input fields:
    - id
    - question
    - options
    - correct_answer
    - explanation
    """

    id: str
    question: str
    options: tuple[str, ...]
    correct_answer: str
    explanation: str = ""

    def __post_init__(self) -> None:

        if not self.id:
            raise ValueError(
                "Question id cannot be empty."
            )

        if not self.question:
            raise ValueError(
                "Question text cannot be empty."
            )

        if not self.options:
            raise ValueError(
                "Question must contain options."
            )

        if self.correct_answer not in self.options:
            raise ValueError(
                "correct_answer must exist "
                "inside options."
            )

    @classmethod
    def from_mapping(
        cls,
        data: Mapping[str, Any],
    ) -> "QuizQuestion":
        """
        Build a QuizQuestion from a dictionary.
        """

        question_id = (
            data.get("id")
            or data.get("question_id")
        )

        question_text = (
            data.get("question")
            or data.get("text")
            or data.get("title")
        )

        options = data.get("options")

        correct_answer = (
            data.get("correct_answer")
            or data.get("answer")
            or data.get("correct")
        )

        explanation = (
            data.get("explanation")
            or data.get("feedback")
            or ""
        )

        if question_id is None:
            raise ValueError(
                "Question is missing id."
            )

        if question_text is None:
            raise ValueError(
                "Question is missing text."
            )

        if options is None:
            raise ValueError(
                "Question is missing options."
            )

        if correct_answer is None:
            raise ValueError(
                "Question is missing correct_answer."
            )

        normalized_options = tuple(
            str(option)
            for option in options
        )

        return cls(
            id=str(question_id),
            question=str(question_text),
            options=normalized_options,
            correct_answer=str(correct_answer),
            explanation=str(explanation),
        )


# ==========================================================
# Answer Record
# ==========================================================

@dataclass
class QuizAnswer:
    """Store one submitted answer."""

    question_id: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    answered_at: str = field(
        default_factory=_utc_now
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "question_id": self.question_id,
            "selected_answer": self.selected_answer,
            "correct_answer": self.correct_answer,
            "is_correct": self.is_correct,
            "answered_at": self.answered_at,
        }


# ==========================================================
# Quiz Result
# ==========================================================

@dataclass
class QuizResult:
    """Final quiz result."""

    telegram_id: int
    module_id: str
    chapter_id: str
    lesson_id: str

    total_questions: int
    answered_questions: int
    correct_answers: int
    wrong_answers: int
    score: float

    status: str

    started_at: str
    completed_at: str | None = None

    answers: list[QuizAnswer] = field(
        default_factory=list
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "telegram_id": self.telegram_id,
            "module_id": self.module_id,
            "chapter_id": self.chapter_id,
            "lesson_id": self.lesson_id,
            "total_questions": self.total_questions,
            "answered_questions": self.answered_questions,
            "correct_answers": self.correct_answers,
            "wrong_answers": self.wrong_answers,
            "score": self.score,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "answers": [
                answer.to_dict()
                for answer in self.answers
            ],
        }


# ==========================================================
# Quiz Session
# ==========================================================

@dataclass
class QuizSession:
    """
    Runtime state of one quiz.
    """

    telegram_id: int

    module_id: str
    chapter_id: str
    lesson_id: str

    questions: list[QuizQuestion]

    current_index: int = 0

    answers: list[QuizAnswer] = field(
        default_factory=list
    )

    status: str = STATUS_ACTIVE

    started_at: str = field(
        default_factory=_utc_now
    )

    completed_at: str | None = None

    def total_questions(self) -> int:
        return len(self.questions)

    def answered_questions(self) -> int:
        return len(self.answers)

    def correct_answers(self) -> int:
        return sum(
            1
            for answer in self.answers
            if answer.is_correct
        )

    def wrong_answers(self) -> int:
        return (
            self.answered_questions()
            - self.correct_answers()
        )

    def score(self) -> float:
        return calculate_score(
            self.correct_answers(),
            self.total_questions(),
        )

    def is_finished(self) -> bool:
        return (
            self.current_index
            >= self.total_questions()
        )

    def current_question(
        self,
    ) -> QuizQuestion | None:

        if self.status != STATUS_ACTIVE:
            return None

        if self.is_finished():
            return None

        return self.questions[
            self.current_index
        ]

    def to_result(self) -> QuizResult:

        return QuizResult(
            telegram_id=self.telegram_id,
            module_id=self.module_id,
            chapter_id=self.chapter_id,
            lesson_id=self.lesson_id,
            total_questions=self.total_questions(),
            answered_questions=self.answered_questions(),
            correct_answers=self.correct_answers(),
            wrong_answers=self.wrong_answers(),
            score=self.score(),
            status=self.status,
            started_at=self.started_at,
            completed_at=self.completed_at,
            answers=list(self.answers),
        )


# ==========================================================
# Quiz Engine
# ==========================================================

class QuizEngine:
    """
    Central runtime engine for all quizzes.

    One active session is allowed per Telegram user.

    Sessions are isolated by telegram_id.
    """

    def __init__(
        self,
        *,
        shuffle_questions: bool = False,
        shuffle_options: bool = False,
        random_seed: int | None = None,
    ) -> None:

        self.shuffle_questions = (
            shuffle_questions
        )

        self.shuffle_options = (
            shuffle_options
        )

        self._random = random.Random(
            random_seed
        )

        self._sessions: dict[
            int,
            QuizSession,
        ] = {}

        self._lock = RLock()

    # ======================================================
    # Question normalization
    # ======================================================

    def normalize_questions(
        self,
        questions: Iterable[
            QuizQuestion
            | Mapping[str, Any]
        ],
    ) -> list[QuizQuestion]:
        """
        Convert all question inputs to QuizQuestion.
        """

        normalized: list[
            QuizQuestion
        ] = []

        for question in questions:

            if isinstance(
                question,
                QuizQuestion,
            ):
                normalized.append(
                    question
                )

            elif isinstance(
                question,
                Mapping,
            ):
                normalized.append(
                    QuizQuestion.from_mapping(
                        question
                    )
                )

            else:
                raise TypeError(
                    "Each question must be "
                    "QuizQuestion or Mapping."
                )

        if not normalized:
            raise ValueError(
                "Quiz must contain at least "
                "one question."
            )

        ids = [
            question.id
            for question in normalized
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "Question IDs must be unique."
            )

        return normalized

    # ======================================================
    # Start
    # ======================================================

    def start_quiz(
        self,
        *,
        telegram_id: int,
        module_id: str,
        chapter_id: str,
        lesson_id: str,
        questions: Sequence[
            QuizQuestion
            | Mapping[str, Any]
        ],
        replace_existing: bool = False,
    ) -> QuizSession:
        """
        Start a new quiz session.
        """

        if telegram_id <= 0:
            raise ValueError(
                "telegram_id must be positive."
            )

        if not module_id:
            raise ValueError(
                "module_id cannot be empty."
            )

        if not chapter_id:
            raise ValueError(
                "chapter_id cannot be empty."
            )

        if not lesson_id:
            raise ValueError(
                "lesson_id cannot be empty."
            )

        normalized = (
            self.normalize_questions(
                questions
            )
        )

        with self._lock:

            existing = self._sessions.get(
                telegram_id
            )

            if (
                existing is not None
                and existing.status
                == STATUS_ACTIVE
                and not replace_existing
            ):
                raise RuntimeError(
                    "User already has an active quiz."
                )

            quiz_questions = list(
                normalized
            )

            if self.shuffle_questions:
                self._random.shuffle(
                    quiz_questions
                )

            if self.shuffle_options:

                quiz_questions = [
                    QuizQuestion(
                        id=question.id,
                        question=question.question,
                        options=tuple(
                            self._shuffled_options(
                                question.options
                            )
                        ),
                        correct_answer=(
                            question.correct_answer
                        ),
                        explanation=(
                            question.explanation
                        ),
                    )
                    for question
                    in quiz_questions
                ]

            session = QuizSession(
                telegram_id=telegram_id,
                module_id=module_id,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                questions=quiz_questions,
            )

            self._sessions[
                telegram_id
            ] = session

            return session

    # ======================================================
    # Option shuffle
    # ======================================================

    def _shuffled_options(
        self,
        options: Sequence[str],
    ) -> list[str]:

        result = list(options)

        self._random.shuffle(
            result
        )

        return result

    # ======================================================
    # Active session
    # ======================================================

    def get_session(
        self,
        telegram_id: int,
    ) -> QuizSession | None:
        """Return active or completed session."""

        with self._lock:

            return self._sessions.get(
                telegram_id
            )

    def get_active_session(
        self,
        telegram_id: int,
    ) -> QuizSession | None:
        """Return active session only."""

        session = self.get_session(
            telegram_id
        )

        if (
            session is None
            or session.status
            != STATUS_ACTIVE
        ):
            return None

        return session

    def has_active_quiz(
        self,
        telegram_id: int,
    ) -> bool:
        """Return True when user has active quiz."""

        return (
            self.get_active_session(
                telegram_id
            )
            is not None
        )

    # ======================================================
    # Current question
    # ======================================================

    def get_current_question(
        self,
        telegram_id: int,
    ) -> QuizQuestion | None:
        """Return the current question."""

        session = (
            self.get_active_session(
                telegram_id
            )
        )

        if session is None:
            return None

        return session.current_question()

    # ======================================================
    # Answer
    # ======================================================

    def submit_answer(
        self,
        *,
        telegram_id: int,
        answer: str,
    ) -> dict[str, Any]:
        """
        Submit an answer for the current question.

        Returns:
            A structured answer result.
        """

        if answer is None:
            raise ValueError(
                "answer cannot be None."
            )

        session = (
            self.get_active_session(
                telegram_id
            )
        )

        if session is None:
            raise RuntimeError(
                "No active quiz for this user."
            )

        question = (
            session.current_question()
        )

        if question is None:
            raise RuntimeError(
                "No current question available."
            )

        selected_answer = str(
            answer
        )

        if (
            selected_answer
            not in question.options
        ):
            raise ValueError(
                "Selected answer is not "
                "one of the question options."
            )

        is_correct = (
            selected_answer
            == question.correct_answer
        )

        answer_record = QuizAnswer(
            question_id=question.id,
            selected_answer=selected_answer,
            correct_answer=(
                question.correct_answer
            ),
            is_correct=is_correct,
        )

        session.answers.append(
            answer_record
        )

        session.current_index += 1

        finished = (
            session.is_finished()
        )

        if finished:
            self.complete_quiz(
                telegram_id
            )

        return {
            "result": (
                RESULT_FINISHED
                if finished
                else (
                    RESULT_CORRECT
                    if is_correct
                    else RESULT_WRONG
                )
            ),
            "is_correct": is_correct,
            "question_id": question.id,
            "selected_answer": (
                selected_answer
            ),
            "correct_answer": (
                question.correct_answer
            ),
            "explanation": (
                question.explanation
            ),
            "current_index": (
                session.current_index
            ),
            "total_questions": (
                session.total_questions()
            ),
            "answered_questions": (
                session.answered_questions()
            ),
            "correct_answers": (
                session.correct_answers()
            ),
            "wrong_answers": (
                session.wrong_answers()
            ),
            "score": session.score(),
            "finished": finished,
        }

    # ======================================================
    # Complete
    # ======================================================

    def complete_quiz(
        self,
        telegram_id: int,
    ) -> QuizResult:
        """
        Complete an active quiz.
        """

        session = self.get_session(
            telegram_id
        )

        if session is None:
            raise RuntimeError(
                "Quiz session not found."
            )

        if session.status == STATUS_CANCELLED:
            raise RuntimeError(
                "Cancelled quiz cannot be completed."
            )

        if session.status == STATUS_COMPLETED:
            return session.to_result()

        if not session.is_finished():
            raise RuntimeError(
                "Quiz cannot be completed "
                "before all questions are answered."
            )

        session.status = (
            STATUS_COMPLETED
        )

        session.completed_at = (
            _utc_now()
        )

        return session.to_result()

    # ======================================================
    # Cancel
    # ======================================================

    def cancel_quiz(
        self,
        telegram_id: int,
    ) -> QuizResult:
        """
        Cancel an active quiz.
        """

        session = self.get_session(
            telegram_id
        )

        if session is None:
            raise RuntimeError(
                "Quiz session not found."
            )

        if session.status == STATUS_COMPLETED:
            raise RuntimeError(
                "Completed quiz cannot be cancelled."
            )

        if session.status == STATUS_CANCELLED:
            return session.to_result()

        session.status = (
            STATUS_CANCELLED
        )

        session.completed_at = (
            _utc_now()
        )

        return session.to_result()

    # ======================================================
    # Reset
    # ======================================================

    def remove_session(
        self,
        telegram_id: int,
    ) -> bool:
        """
        Completely remove a quiz session
        from runtime memory.
        """

        with self._lock:

            return (
                self._sessions.pop(
                    telegram_id,
                    None,
                )
                is not None
            )

    def clear_completed_session(
        self,
        telegram_id: int,
    ) -> bool:
        """
        Remove only completed/cancelled sessions.
        """

        session = self.get_session(
            telegram_id
        )

        if session is None:
            return False

        if session.status == STATUS_ACTIVE:
            return False

        return self.remove_session(
            telegram_id
        )

    # ======================================================
    # Result
    # ======================================================

    def get_result(
        self,
        telegram_id: int,
    ) -> QuizResult | None:
        """
        Return current session result.
        """

        session = self.get_session(
            telegram_id
        )

        if session is None:
            return None

        return session.to_result()

    # ======================================================
    # State
    # ======================================================

    def get_state(
        self,
        telegram_id: int,
    ) -> dict[str, Any] | None:
        """
        Return serializable quiz state.
        """

        session = self.get_session(
            telegram_id
        )

        if session is None:
            return None

        current_question = (
            session.current_question()
        )

        return {
            "telegram_id": session.telegram_id,
            "module_id": session.module_id,
            "chapter_id": session.chapter_id,
            "lesson_id": session.lesson_id,
            "status": session.status,
            "current_index": (
                session.current_index
            ),
            "total_questions": (
                session.total_questions()
            ),
            "answered_questions": (
                session.answered_questions()
            ),
            "correct_answers": (
                session.correct_answers()
            ),
            "wrong_answers": (
                session.wrong_answers()
            ),
            "score": session.score(),
            "started_at": session.started_at,
            "completed_at": session.completed_at,
            "current_question": (
                {
                    "id": current_question.id,
                    "question": (
                        current_question.question
                    ),
                    "options": list(
                        current_question.options
                    ),
                }
                if current_question is not None
                else None
            ),
        }

    # ======================================================
    # Statistics payload
    # ======================================================

    def build_statistics_payload(
        self,
        telegram_id: int,
    ) -> dict[str, Any] | None:
        """
        Build the payload required by the
        Statistics layer.
        """

        result = self.get_result(
            telegram_id
        )

        if result is None:
            return None

        return {
            "telegram_id": result.telegram_id,
            "module_id": result.module_id,
            "chapter_id": result.chapter_id,
            "lesson_id": result.lesson_id,
            "total_questions": (
                result.total_questions
            ),
            "correct_answers": (
                result.correct_answers
            ),
            "score": result.score,
            "status": result.status,
        }

    # ======================================================
    # Progress payload
    # ======================================================

    def build_progress_payload(
        self,
        telegram_id: int,
    ) -> dict[str, Any] | None:
        """
        Build the payload required by
        the Progress layer.
        """

        result = self.get_result(
            telegram_id
        )

        if result is None:
            return None

        return {
            "telegram_id": result.telegram_id,
            "module_id": result.module_id,
            "chapter_id": result.chapter_id,
            "lesson_id": result.lesson_id,
            "completed": (
                result.status
                == STATUS_COMPLETED
            ),
        }

    # ======================================================
    # Users
    # ======================================================

    def active_users(self) -> list[int]:
        """
        Return Telegram IDs with active quizzes.
        """

        with self._lock:

            return [
                telegram_id
                for telegram_id, session
                in self._sessions.items()
                if session.status
                == STATUS_ACTIVE
            ]

    def active_session_count(self) -> int:
        """Return number of active quiz sessions."""

        return len(
            self.active_users()
        )

    # ======================================================
    # Health check
    # ======================================================

    def health_check(self) -> bool:
        """
        Check engine availability.
        """

        try:

            test_questions = [
                QuizQuestion(
                    id="health",
                    question="Health?",
                    options=(
                        "yes",
                        "no",
                    ),
                    correct_answer="yes",
                )
            ]

            session = self.start_quiz(
                telegram_id=-1,
                module_id="health",
                chapter_id="health",
                lesson_id="health",
                questions=test_questions,
                replace_existing=True,
            )

            if session.total_questions() != 1:
                return False

            self.submit_answer(
                telegram_id=-1,
                answer="yes",
            )

            result = self.get_result(
                telegram_id=-1
            )

            self.remove_session(-1)

            return (
                result is not None
                and result.status
                == STATUS_COMPLETED
                and result.correct_answers
                == 1
                and result.score
                == 100.0
            )

        except Exception:
            return False


# ==========================================================
# Global Engine
# ==========================================================

quiz_engine = QuizEngine()


# ==========================================================
# Convenience functions
# ==========================================================

def start_quiz(
    *,
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    questions: Sequence[
        QuizQuestion
        | Mapping[str, Any]
    ],
    replace_existing: bool = False,
) -> QuizSession:
    """Start a quiz using the global engine."""

    return quiz_engine.start_quiz(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        questions=questions,
        replace_existing=replace_existing,
    )


def submit_answer(
    *,
    telegram_id: int,
    answer: str,
) -> dict[str, Any]:
    """Submit an answer using the global engine."""

    return quiz_engine.submit_answer(
        telegram_id=telegram_id,
        answer=answer,
    )


def complete_quiz(
    telegram_id: int,
) -> QuizResult:
    """Complete a quiz using the global engine."""

    return quiz_engine.complete_quiz(
        telegram_id
    )


def cancel_quiz(
    telegram_id: int,
) -> QuizResult:
    """Cancel a quiz using the global engine."""

    return quiz_engine.cancel_quiz(
        telegram_id
    )


def get_current_question(
    telegram_id: int,
) -> QuizQuestion | None:
    """Return current question."""

    return quiz_engine.get_current_question(
        telegram_id
    )


def get_quiz_state(
    telegram_id: int,
) -> dict[str, Any] | None:
    """Return serializable quiz state."""

    return quiz_engine.get_state(
        telegram_id
    )


def quiz_engine_health_check() -> bool:
    """Check global quiz engine."""

    return quiz_engine.health_check()


# ==========================================================
# Module-level health
# ==========================================================

if __name__ == "__main__":

    print(
        "Quiz Engine health:",
        quiz_engine_health_check(),
    )
