from database import Database


def main():
    db = Database()

    test_user_id = 999999999

    db.create_or_update_user(
        user_id=test_user_id,
        username="test_user",
        first_name="Test",
        last_name="User",
    )

    user = db.get_user(test_user_id)

    assert user is not None
    assert user["user_id"] == test_user_id

    db.add_points(
        user_id=test_user_id,
        points=150,
    )

    user = db.get_user(test_user_id)

    assert user["points"] == 150
    assert user["level"] == 2

    db.save_progress(
        user_id=test_user_id,
        course="management",
        chapter="chapter_1",
        completed=True,
    )

    progress = db.get_progress(
        user_id=test_user_id,
        course="management",
    )

    assert len(progress) == 1
    assert progress[0]["completed"] == 1

    result_id = db.save_quiz_result(
        user_id=test_user_id,
        course="management",
        chapter="chapter_1",
        score=8,
        total=10,
    )

    assert result_id is not None

    results = db.get_quiz_results(
        user_id=test_user_id,
    )

    assert len(results) >= 1
    assert results[0]["score"] == 8
    assert results[0]["total"] == 10

    stats = db.get_user_statistics(
        user_id=test_user_id,
    )

    assert stats["points"] == 150
    assert stats["level"] == 2
    assert stats["quiz_count"] >= 1
    assert stats["completed_lessons"] >= 1

    print("DATABASE TEST PASSED")


if __name__ == "__main__":
    main()
