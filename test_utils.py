from core.utils import (
    TELEGRAM_MESSAGE_LIMIT,
    split_long_text,
)


def test_short_text():
    text = "سلام اندیشکده"

    chunks = split_long_text(text)

    assert chunks == [text]


def test_long_text():
    text = "الف" * (TELEGRAM_MESSAGE_LIMIT + 100)

    chunks = split_long_text(text)

    assert len(chunks) >= 2
    assert all(
        len(chunk) <= TELEGRAM_MESSAGE_LIMIT
        for chunk in chunks
    )

    assert "".join(chunks) == text


def test_paragraph_split():
    text = (
        "بخش اول\n\n"
        + ("الف" * 2000)
        + "\n\n"
        + ("ب" * 2000)
    )

    chunks = split_long_text(text)

    assert len(chunks) >= 2

    assert all(
        len(chunk) <= TELEGRAM_MESSAGE_LIMIT
        for chunk in chunks
    )


def test_empty_text():
    assert split_long_text("") == []


print("UTILS TEST PASSED")
