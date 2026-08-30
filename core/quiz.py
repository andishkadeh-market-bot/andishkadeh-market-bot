"""
Reusable quiz engine for Andishkadeh Management & Market.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class QuizQuestion:
    """Represents one multiple-choice question."""

    question: str
    options: list[str]
    answer: int
    explanation: str = ""


@dataclass
class QuizResult:
    """Represents the result of a completed quiz."""

    total: int
    correct: int
    wrong: int

    @property
    def percentage(self) -> float:
        """Return score percentage."""

        if self.total == 0:
            return 0.0

        return (self.correct / self.total) * 100


class QuizSession:
    """Manage the state of a quiz session."""

    def __init__(
        self,
        questions: list[QuizQuestion],
    ) -> None:
        self.questions = questions
        self.current_index = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.answers: list[Optional[int]] = []

    @property
    def current_question(
        self,
    ) -> Optional[QuizQuestion]:
        """Return the current question."""

        if self.is_finished:
            return None

        return self.questions[
            self.current_index
        ]

    @property
    def is_finished(self) -> bool:
        """Return whether the quiz is complete."""

        return (
            self.current_index
            >= len(self.questions)
        )

    @property
    def total_questions(self) -> int:
        """Return total number of questions."""

        return len(self.questions)

    def answer(
        self,
        selected_option: int,
    ) -> bool:
        """
        Submit an answer.

        Returns True when the selected option is correct.
        """

        if self.is_finished:
            raise ValueError(
                "Quiz has already finished."
            )

        question = self.current_question

        if question is None:
            raise ValueError(
                "No current question."
            )

        if (
            selected_option < 0
            or selected_option >= len(
                question.options
            )
        ):
            raise ValueError(
                "Invalid option index."
            )

        is_correct = (
            selected_option == question.answer
        )

        if is_correct:
            self.correct_answers += 1
        else:
            self.wrong_answers += 1

        self.answers.append(
            selected_option
        )

        self.current_index += 1

        return is_correct

    def result(self) -> QuizResult:
        """Return the current quiz result."""

        return QuizResult(
            total=self.total_questions,
            correct=self.correct_answers,
            wrong=self.wrong_answers,
        )


def build_questions(
    raw_questions: list[dict],
) -> list[QuizQuestion]:
    """Convert dictionary questions into quiz objects."""

    questions = []

    for item in raw_questions:
        questions.append(
            QuizQuestion(
                question=item["question"],
                options=item["options"],
                answer=item["answer"],
                explanation=item.get(
                    "explanation",
                    "",
                ),
            )
        )

    return questions


def format_quiz_result(
    result: QuizResult,
) -> str:
    """Create a readable quiz result message."""

    percentage = round(
        result.percentage,
        1,
    )

    if percentage >= 80:
        level = "🏆 عالی"
    elif percentage >= 60:
        level = "🟢 خوب"
    elif percentage >= 40:
        level = "🟡 نیاز به مرور"
    else:
        level = "🔴 نیاز به مطالعه بیشتر"

    return f"""
<b>📊 نتیجه آزمون</b>

تعداد سوالات: {result.total}

✅ پاسخ صحیح: {result.correct}

❌ پاسخ غلط: {result.wrong}

📈 درصد: {percentage}٪

<b>ارزیابی:</b>
{level}
"""
