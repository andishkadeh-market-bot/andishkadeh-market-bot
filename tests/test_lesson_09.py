from modules.management.lessons.lesson_09 import LESSON_09


def test_lesson_09_exists():
    assert LESSON_09 is not None


def test_lesson_09_has_required_fields():
    required_fields = [
        "id",
        "title",
        "objectives",
        "lesson",
        "key_concepts",
        "specialized_points",
        "exam_points",
        "practical_example",
        "review",
        "quiz",
    ]

    for field in required_fields:
        assert field in LESSON_09


def test_lesson_09_id():
    assert LESSON_09["id"] == "management_02_02"


def test_lesson_09_has_content():
    assert LESSON_09["objectives"]
    assert LESSON_09["lesson"]
    assert LESSON_09["key_concepts"]
    assert LESSON_09["specialized_points"]
    assert LESSON_09["exam_points"]
    assert LESSON_09["practical_example"]
    assert LESSON_09["review"]


def test_lesson_09_quiz_exists():
    assert LESSON_09["quiz"]
    assert len(LESSON_09["quiz"]) >= 5


def test_lesson_09_quiz_structure():
    for question in LESSON_09["quiz"]:
        assert "question" in question
        assert "options" in question
        assert "answer" in question
        assert "explanation" in question

        assert question["question"]
        assert len(question["options"]) >= 2

        assert isinstance(
            question["answer"],
            int,
        )

        assert 0 <= question["answer"] < len(
            question["options"]
        )

        assert question["explanation"]


def test_lesson_09_quiz_answers_are_valid():
    for question in LESSON_09["quiz"]:
        answer = question["answer"]
        options = question["options"]

        assert 0 <= answer < len(options)


def test_lesson_09_covers_planning_types():
    lesson_text = LESSON_09["lesson"]

    assert "راهبردی" in lesson_text
    assert "تاکتیکی" in lesson_text
    assert "عملیاتی" in lesson_text
    assert "بلندمدت" in lesson_text
    assert "کوتاه‌مدت" in lesson_text
    assert "دائمی" in lesson_text
    assert "یک‌بارمصرف" in lesson_text
    assert "اقتضایی" in lesson_text
