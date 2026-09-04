"""
Andishkadeh Management & Market
Content Initializer

مسئول:
- کشف محتوای ماژول‌ها
- ثبت Module / Chapter / Lesson در Registry
- انتقال محتوای کامل درس‌ها به Registry
- انتقال آزمون درس‌ها به Registry
- همگام‌سازی محتوا با SQLite
- پشتیبانی از ساختارهای قدیمی و جدید ماژول‌ها
- پشتیبانی از ساختار Banking با lessons تو در تو
- Health Check
- Statistics

نکته:
این فایل فقط مسئول Initialization و Registration محتواست.
منطق Telegram و UI در handlers.py قرار دارد.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from typing import Any

from core.database import (
    init_database,
    upsert_module,
    upsert_chapter,
    upsert_lesson,
)

from core.registry import registry


# ==========================================================
# Module Configuration
# ==========================================================

CONTENT_PACKAGES: dict[str, str] = {
    "management": "modules.management.data",
    "banking": "modules.banking.data",
    "international_trade": "modules.international_trade.data",
    "psychology_socialwork": "modules.psychology.data",
    "finance": "modules.finance.data",
}


CONTENT_MODULE_IDS: tuple[str, ...] = (
    "management",
    "banking",
    "international_trade",
    "psychology_socialwork",
    "finance",
)


# ==========================================================
# Data Models
# ==========================================================

@dataclass
class DiscoveredLesson:
    lesson_id: str
    title: str
    module_id: str
    chapter_id: str
    content: str = ""
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class DiscoveredChapter:
    chapter_id: str
    title: str
    module_id: str
    description: str = ""
    lessons: list[DiscoveredLesson] = field(
        default_factory=list
    )


@dataclass
class DiscoveredModule:
    module_id: str
    title: str
    description: str = ""
    chapters: list[DiscoveredChapter] = field(
        default_factory=list
    )


# ==========================================================
# Generic Helpers
# ==========================================================

def _safe_str(value: Any) -> str:

    if value is None:
        return ""

    try:
        return str(value).strip()

    except Exception:
        return ""


def _first_non_empty(
    data: dict[str, Any],
    keys: tuple[str, ...],
    default: str = "",
) -> str:

    for key in keys:

        value = data.get(key)

        if value is None:
            continue

        text = _safe_str(value)

        if text:
            return text

    return default


def _normalize_id(
    value: Any,
) -> str:

    return _safe_str(value)


def _get_module_id(
    data_module: Any,
    fallback: str = "",
) -> str:

    value = getattr(
        data_module,
        "MODULE_ID",
        None,
    )

    if value:
        return _safe_str(value)

    return fallback


def _get_module_title(
    data_module: Any,
    fallback: str = "",
) -> str:

    value = getattr(
        data_module,
        "MODULE_TITLE",
        None,
    )

    if value:
        return _safe_str(value)

    return fallback


def _get_module_description(
    data_module: Any,
) -> str:

    value = getattr(
        data_module,
        "MODULE_DESCRIPTION",
        "",
    )

    return _safe_str(value)


# ==========================================================
# Quiz Helpers
# ==========================================================

def _normalize_quiz_questions(
    questions: Any,
) -> list[dict[str, Any]]:
    """
    Normalize quiz questions into a format that the
    website JavaScript can consume.

    Supported source formats:

    1. answer = numeric index
    2. correct_answer = option text
    3. correct_answer = numeric index
    4. correct_answer = A / B / C / D

    Output always keeps:
        question
        options
        answer
        explanation

    The original fields are preserved when possible.
    """

    if not isinstance(
        questions,
        list,
    ):
        return []

    normalized: list[
        dict[str, Any]
    ] = []

    for question in questions:

        if not isinstance(
            question,
            dict,
        ):
            continue

        item = dict(
            question
        )

        options = item.get(
            "options",
            [],
        )

        if not isinstance(
            options,
            list,
        ):
            options = []

        item["options"] = options

        answer = item.get(
            "answer"
        )

        if answer is None:

            answer = item.get(
                "correct_answer"
            )

        normalized_answer = None

        # --------------------------------------------------
        # Numeric answer
        # --------------------------------------------------

        if isinstance(
            answer,
            int,
        ):

            if (
                0 <= answer < len(options)
            ):
                normalized_answer = answer

        # --------------------------------------------------
        # String answer
        # --------------------------------------------------

        elif answer is not None:

            answer_text = str(
                answer
            ).strip()

            # A / B / C / D
            letter_map = {
                "A": 0,
                "B": 1,
                "C": 2,
                "D": 3,
            }

            upper_answer = (
                answer_text.upper()
            )

            if (
                upper_answer
                in letter_map
            ):

                index = (
                    letter_map[
                        upper_answer
                    ]
                )

                if (
                    index < len(options)
                ):
                    normalized_answer = (
                        index
                    )

            # Numeric string
            if (
                normalized_answer
                is None
            ):

                try:

                    numeric_answer = int(
                        answer_text
                    )

                    if (
                        0
                        <= numeric_answer
                        < len(options)
                    ):
                        normalized_answer = (
                            numeric_answer
                        )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

            # Answer as option text
            if (
                normalized_answer
                is None
            ):

                for index, option in enumerate(
                    options
                ):

                    if (
                        str(option).strip()
                        == answer_text
                    ):

                        normalized_answer = (
                            index
                        )

                        break

        # --------------------------------------------------
        # Preserve question only if valid
        # --------------------------------------------------

        if (
            normalized_answer
            is not None
        ):

            item["answer"] = (
                normalized_answer
            )

        # --------------------------------------------------
        # Explanation compatibility
        # --------------------------------------------------

        if (
            "explanation"
            not in item
        ):

            if (
                "explain"
                in item
            ):

                item["explanation"] = (
                    item.get("explain")
                    or ""
                )

            else:

                item["explanation"] = ""

        normalized.append(
            item
        )

    return normalized


def _get_management_quiz(
    data_module: Any,
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """
    Retrieve Management quiz questions.

    Current Management data.py stores questions in:

        MANAGEMENT_QUIZ_QUESTIONS

    with the key:

        (chapter_id, lesson_id)
    """

    quiz_map = getattr(
        data_module,
        "MANAGEMENT_QUIZ_QUESTIONS",
        None,
    )

    if not isinstance(
        quiz_map,
        dict,
    ):
        return []

    questions = quiz_map.get(
        (
            chapter_id,
            lesson_id,
        ),
        [],
    )

    return _normalize_quiz_questions(
        questions
    )


# ==========================================================
# Lesson Extraction
# ==========================================================

def _extract_lesson(
    lesson_item: dict[str, Any],
    module_id: str,
    chapter_id: str,
) -> DiscoveredLesson | None:

    lesson_id = _first_non_empty(
        lesson_item,
        (
            "id",
            "lesson_id",
            "key",
            "slug",
        ),
    )

    if not lesson_id:
        return None

    lesson_title = _first_non_empty(
        lesson_item,
        (
            "title",
            "name",
            "lesson_title",
        ),
        f"درس {lesson_id}",
    )

    lesson_content = _first_non_empty(
        lesson_item,
        (
            "content",
            "lesson_text",
            "text",
            "body",
            "description",
            "lesson",
        ),
    )

    metadata = dict(
        lesson_item
    )

    metadata.setdefault(
        "id",
        lesson_id,
    )

    metadata.setdefault(
        "lesson_id",
        lesson_id,
    )

    metadata.setdefault(
        "title",
        lesson_title,
    )

    metadata.setdefault(
        "module_id",
        module_id,
    )

    metadata.setdefault(
        "chapter_id",
        chapter_id,
    )

    if lesson_content:

        metadata.setdefault(
            "content",
            lesson_content,
        )

    return DiscoveredLesson(
        lesson_id=lesson_id,
        title=lesson_title,
        module_id=module_id,
        chapter_id=chapter_id,
        content=lesson_content,
        metadata=metadata,
    )


def _extract_chapter_lessons(
    raw_lessons: Any,
    module_id: str,
    chapter_id: str,
) -> list[DiscoveredLesson]:

    if not isinstance(
        raw_lessons,
        list,
    ):
        return []

    lessons: list[
        DiscoveredLesson
    ] = []

    for lesson_item in raw_lessons:

        if not isinstance(
            lesson_item,
            dict,
        ):
            continue

        lesson = _extract_lesson(
            lesson_item=lesson_item,
            module_id=module_id,
            chapter_id=chapter_id,
        )

        if lesson is not None:

            lessons.append(
                lesson
            )

    return lessons


# ==========================================================
# International Trade Extraction
# ==========================================================

def _extract_international_trade_curriculum(
    data_module: Any,
) -> DiscoveredModule | None:

    module_id = _get_module_id(
        data_module,
        "international_trade",
    )

    module_title = _get_module_title(
        data_module,
        "🌍 تجارت بین‌الملل",
    )

    module_description = (
        _get_module_description(
            data_module
        )
    )

    curriculum = getattr(
        data_module,
        "INTERNATIONAL_TRADE_CURRICULUM",
        None,
    )

    lessons_map = getattr(
        data_module,
        "INTERNATIONAL_TRADE_LESSONS",
        None,
    )

    if not isinstance(
        curriculum,
        list,
    ):
        return None

    if not isinstance(
        lessons_map,
        dict,
    ):
        lessons_map = {}

    chapters: list[
        DiscoveredChapter
    ] = []

    for chapter_item in curriculum:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
                "original_chapter_id",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        chapter_description = _first_non_empty(
            chapter_item,
            (
                "description",
                "desc",
            ),
        )

        raw_lessons = lessons_map.get(
            chapter_id,
            [],
        )

        lessons = _extract_chapter_lessons(
            raw_lessons=raw_lessons,
            module_id=module_id,
            chapter_id=chapter_id,
        )

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=chapter_description,
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Finance Extraction
# ==========================================================

def _extract_finance_curriculum(
    data_module: Any,
) -> DiscoveredModule | None:

    module_id = _get_module_id(
        data_module,
        "finance",
    )

    module_title = _get_module_title(
        data_module,
        "💰 مدیریت مالی حرفه‌ای",
    )

    module_description = (
        _get_module_description(
            data_module
        )
    )

    chapters_data = getattr(
        data_module,
        "CHAPTERS",
        None,
    )

    lessons_data = getattr(
        data_module,
        "LESSONS",
        None,
    )

    if not isinstance(
        chapters_data,
        list,
    ):
        return None

    if not isinstance(
        lessons_data,
        list,
    ):
        lessons_data = []

    lessons_by_chapter: dict[
        str,
        list[dict[str, Any]],
    ] = {}

    for lesson in lessons_data:

        if not isinstance(
            lesson,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            lesson,
            (
                "chapter_id",
                "original_chapter_id",
            ),
        )

        if not chapter_id:
            continue

        lessons_by_chapter.setdefault(
            chapter_id,
            [],
        ).append(
            lesson
        )

    chapters: list[
        DiscoveredChapter
    ] = []

    for chapter_item in chapters_data:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        chapter_description = _first_non_empty(
            chapter_item,
            (
                "description",
                "desc",
            ),
        )

        raw_lessons = lessons_by_chapter.get(
            chapter_id,
            [],
        )

        lessons = _extract_chapter_lessons(
            raw_lessons=raw_lessons,
            module_id=module_id,
            chapter_id=chapter_id,
        )

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=chapter_description,
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Management Extraction
# ==========================================================

def _extract_management_curriculum(
    data_module: Any,
) -> DiscoveredModule | None:

    module_id = _get_module_id(
        data_module,
        "management",
    )

    module_title = _get_module_title(
        data_module,
        "📚 آموزش مدیریت",
    )

    module_description = (
        _get_module_description(
            data_module
        )
    )

    curriculum = getattr(
        data_module,
        "MANAGEMENT_CURRICULUM",
        None,
    )

    if not isinstance(
        curriculum,
        list,
    ):

        curriculum = getattr(
            data_module,
            "MANAGEMENT_CHAPTERS",
            None,
        )

    lessons_map = getattr(
        data_module,
        "MANAGEMENT_LESSONS",
        None,
    )

    if not isinstance(
        curriculum,
        list,
    ):
        return None

    if not isinstance(
        lessons_map,
        dict,
    ):
        lessons_map = {}

    chapters: list[
        DiscoveredChapter
    ] = []

    for chapter_item in curriculum:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
                "original_chapter_id",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        chapter_description = _first_non_empty(
            chapter_item,
            (
                "description",
                "desc",
            ),
        )

        raw_lessons = lessons_map.get(
            chapter_id,
            [],
        )

        lessons = _extract_chapter_lessons(
            raw_lessons=raw_lessons,
            module_id=module_id,
            chapter_id=chapter_id,
        )

        # --------------------------------------------------
        # IMPORTANT:
        # Add quiz questions to every Management lesson.
        # --------------------------------------------------

        for lesson in lessons:

            quiz_questions = (
                _get_management_quiz(
                    data_module=data_module,
                    chapter_id=chapter_id,
                    lesson_id=lesson.lesson_id,
                )
            )

            if quiz_questions:

                lesson.metadata[
                    "quiz"
                ] = quiz_questions

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=chapter_description,
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Banking Extraction
# ==========================================================

def _extract_banking_curriculum(
    data_module: Any,
) -> DiscoveredModule | None:

    module_id = _get_module_id(
        data_module,
        "banking",
    )

    module_title = _get_module_title(
        data_module,
        "🏦 بانکداری تخصصی",
    )

    module_description = (
        _get_module_description(
            data_module
        )
    )

    chapters_data = getattr(
        data_module,
        "CHAPTERS",
        None,
    )

    if not isinstance(
        chapters_data,
        list,
    ):
        return None

    chapters: list[
        DiscoveredChapter
    ] = []

    for chapter_item in chapters_data:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
                "key",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        chapter_description = _first_non_empty(
            chapter_item,
            (
                "description",
                "desc",
            ),
        )

        raw_lessons = chapter_item.get(
            "lessons",
            [],
        )

        lessons = _extract_chapter_lessons(
            raw_lessons=raw_lessons,
            module_id=module_id,
            chapter_id=chapter_id,
        )

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=chapter_description,
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Generic Extraction
# ==========================================================

def _extract_generic_curriculum(
    data_module: Any,
    module_id: str,
) -> DiscoveredModule | None:

    module_title = _get_module_title(
        data_module,
        module_id,
    )

    module_description = (
        _get_module_description(
            data_module
        )
    )

    chapters_data = getattr(
        data_module,
        "CHAPTERS",
        None,
    )

    lessons_data = getattr(
        data_module,
        "LESSONS",
        None,
    )

    if not isinstance(
        chapters_data,
        list,
    ):
        return None

    if not isinstance(
        lessons_data,
        list,
    ):
        lessons_data = []

    lessons_by_chapter: dict[
        str,
        list[dict[str, Any]],
    ] = {}

    for lesson_item in lessons_data:

        if not isinstance(
            lesson_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            lesson_item,
            (
                "chapter_id",
                "original_chapter_id",
            ),
        )

        if not chapter_id:
            continue

        lessons_by_chapter.setdefault(
            chapter_id,
            [],
        ).append(
            lesson_item
        )

    chapters: list[
        DiscoveredChapter
    ] = []

    for chapter_item in chapters_data:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
                "key",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        chapter_description = _first_non_empty(
            chapter_item,
            (
                "description",
                "desc",
            ),
        )

        nested_lessons = chapter_item.get(
            "lessons",
        )

        if isinstance(
            nested_lessons,
            list,
        ):

            raw_lessons = nested_lessons

        else:

            raw_lessons = lessons_by_chapter.get(
                chapter_id,
                [],
            )

        lessons = _extract_chapter_lessons(
            raw_lessons=raw_lessons,
            module_id=module_id,
            chapter_id=chapter_id,
        )

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=chapter_description,
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Psychology / Social Work Extraction
# ==========================================================

def _extract_psychology_curriculum(
    data_module: Any,
) -> DiscoveredModule | None:

    module_id = _get_module_id(
        data_module,
        "psychology_socialwork",
    )

    module_title = _get_module_title(
        data_module,
        "🧠 روانشناسی و مددکاری اجتماعی",
    )

    module_description = (
        _get_module_description(
            data_module
        )
    )

    candidates = (
        "PSYCHOLOGY_CURRICULUM",
        "PSYCHOLOGY_CHAPTERS",
        "CURRICULUM",
        "CHAPTERS",
    )

    curriculum = None

    for attribute_name in candidates:

        value = getattr(
            data_module,
            attribute_name,
            None,
        )

        if isinstance(
            value,
            list,
        ):

            curriculum = value

            break

    if not isinstance(
        curriculum,
        list,
    ):
        return None

    lessons_candidates = (
        "PSYCHOLOGY_LESSONS",
        "LESSONS",
    )

    lessons_data = None

    for attribute_name in lessons_candidates:

        value = getattr(
            data_module,
            attribute_name,
            None,
        )

        if isinstance(
            value,
            (list, dict),
        ):

            lessons_data = value

            break

    chapters: list[
        DiscoveredChapter
    ] = []

    lessons_by_chapter: dict[
        str,
        list[dict[str, Any]],
    ] = {}

    if isinstance(
        lessons_data,
        list,
    ):

        for lesson_item in lessons_data:

            if not isinstance(
                lesson_item,
                dict,
            ):
                continue

            chapter_id = _first_non_empty(
                lesson_item,
                (
                    "chapter_id",
                    "original_chapter_id",
                ),
            )

            if chapter_id:

                lessons_by_chapter.setdefault(
                    chapter_id,
                    [],
                ).append(
                    lesson_item
                )

    for chapter_item in curriculum:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
                "key",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        chapter_description = _first_non_empty(
            chapter_item,
            (
                "description",
                "desc",
            ),
        )

        nested_lessons = chapter_item.get(
            "lessons",
        )

        if isinstance(
            nested_lessons,
            list,
        ):

            raw_lessons = nested_lessons

        elif isinstance(
            lessons_data,
            dict,
        ):

            raw_lessons = lessons_data.get(
                chapter_id,
                [],
            )

        else:

            raw_lessons = lessons_by_chapter.get(
                chapter_id,
                [],
            )

        lessons = _extract_chapter_lessons(
            raw_lessons=raw_lessons,
            module_id=module_id,
            chapter_id=chapter_id,
        )

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=chapter_description,
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Module Discovery
# ==========================================================

def discover_module(
    module_id: str,
) -> DiscoveredModule | None:

    module_id = _normalize_id(
        module_id
    )

    if not module_id:
        return None

    package_path = CONTENT_PACKAGES.get(
        module_id
    )

    if not package_path:
        return None

    try:

        data_module = import_module(
            package_path
        )

    except Exception as exc:

        print(
            f"[ContentInitializer] "
            f"Failed to import {package_path}: {exc}"
        )

        return None

    # ------------------------------------------------------
    # Specialized extractors
    # ------------------------------------------------------

    if module_id == "banking":

        result = (
            _extract_banking_curriculum(
                data_module
            )
        )

        if result is not None:
            return result

    if module_id == "international_trade":

        result = (
            _extract_international_trade_curriculum(
                data_module
            )
        )

        if result is not None:
            return result

    if module_id == "finance":

        result = (
            _extract_finance_curriculum(
                data_module
            )
        )

        if result is not None:
            return result

    if module_id == "management":

        result = (
            _extract_management_curriculum(
                data_module
            )
        )

        if result is not None:
            return result

    if module_id == "psychology_socialwork":

        result = (
            _extract_psychology_curriculum(
                data_module
            )
        )

        if result is not None:
            return result

    # ------------------------------------------------------
    # Generic fallback
    # ------------------------------------------------------

    return _extract_generic_curriculum(
        data_module=data_module,
        module_id=module_id,
    )


# ==========================================================
# Registration
# ==========================================================

def _register_module(
    module: DiscoveredModule,
) -> int:
    """
    Register a complete module in Registry.

    مهم:
    تمام محتوای درس در data ذخیره می‌شود.
    آزمون نیز در data["quiz"] ذخیره می‌شود.

    بنابراین API می‌تواند اطلاعات کامل درس را
    در اختیار frontend قرار دهد.
    """

    try:

        registry.register_module(
            module_id=module.module_id,
            title=module.title,
            description=module.description,
        )

    except TypeError:

        registry.register_module(
            module.module_id,
            module.title,
            module.description,
        )

    lesson_count = 0

    for chapter in module.chapters:

        try:

            registry.register_chapter(
                module_id=chapter.module_id,
                chapter_id=chapter.chapter_id,
                title=chapter.title,
                description=chapter.description,
            )

        except TypeError:

            registry.register_chapter(
                chapter.module_id,
                chapter.chapter_id,
                chapter.title,
                chapter.description,
            )

        for lesson in chapter.lessons:

            # --------------------------------------------------
            # Build complete lesson data
            # --------------------------------------------------

            lesson_data: dict[
                str,
                Any,
            ] = {}

            if isinstance(
                lesson.metadata,
                dict,
            ):

                lesson_data.update(
                    lesson.metadata
                )

            # --------------------------------------------------
            # Content is explicitly preserved.
            # --------------------------------------------------

            if lesson.content:

                lesson_data[
                    "content"
                ] = lesson.content

            # --------------------------------------------------
            # Standard identifiers
            # --------------------------------------------------

            lesson_data.setdefault(
                "id",
                lesson.lesson_id,
            )

            lesson_data.setdefault(
                "lesson_id",
                lesson.lesson_id,
            )

            lesson_data.setdefault(
                "title",
                lesson.title,
            )

            lesson_data.setdefault(
                "module_id",
                lesson.module_id,
            )

            lesson_data.setdefault(
                "chapter_id",
                lesson.chapter_id,
            )

            # --------------------------------------------------
            # Quiz normalization
            #
            # If quiz exists in metadata, normalize it again
            # to guarantee a frontend-compatible structure.
            # --------------------------------------------------

            if "quiz" in lesson_data:

                normalized_quiz = (
                    _normalize_quiz_questions(
                        lesson_data.get(
                            "quiz"
                        )
                    )
                )

                if normalized_quiz:

                    lesson_data[
                        "quiz"
                    ] = normalized_quiz

                else:

                    lesson_data.pop(
                        "quiz",
                        None,
                    )

            # --------------------------------------------------
            # Register lesson with full data
            # --------------------------------------------------

            try:

                registry.register_lesson(
                    module_id=lesson.module_id,
                    chapter_id=lesson.chapter_id,
                    lesson_id=lesson.lesson_id,
                    title=lesson.title,
                    data=lesson_data,
                )

            except TypeError:

                registry.register_lesson(
                    lesson.module_id,
                    lesson.chapter_id,
                    lesson.lesson_id,
                    lesson.title,
                    lesson_data,
                )

            lesson_count += 1

    return lesson_count


# ==========================================================
# Initialization
# ==========================================================

def initialize_module(
    module_id: str,
) -> dict[str, Any]:

    module_id = _normalize_id(
        module_id
    )

    if not module_id:

        return {
            "module_id": "",
            "status": "error",
            "modules": 0,
            "chapters": 0,
            "lessons": 0,
        }

    try:

        init_database()

    except Exception as exc:

        print(
            f"[ContentInitializer] "
            f"Database initialization warning: {exc}"
        )

    module = discover_module(
        module_id
    )

    if module is None:

        return {
            "module_id": module_id,
            "status": "not_found",
            "modules": 0,
            "chapters": 0,
            "lessons": 0,
        }

    lesson_count = _register_module(
        module
    )

    return {
        "module_id": module.module_id,
        "status": "ok",
        "modules": 1,
        "chapters": len(
            module.chapters
        ),
        "lessons": lesson_count,
    }


def initialize_all_content() -> dict[str, Any]:
    """
    Initialize every configured content module.

    Returns a complete initialization report.
    """

    try:

        init_database()

    except Exception as exc:

        print(
            f"[ContentInitializer] "
            f"Database initialization warning: {exc}"
        )

    results: dict[
        str,
        Any,
    ] = {}

    total_modules = 0
    total_chapters = 0
    total_lessons = 0

    for module_id in CONTENT_MODULE_IDS:

        result = initialize_module(
            module_id
        )

        results[
            module_id
        ] = result

        if (
            result.get("status")
            == "ok"
        ):

            total_modules += result.get(
                "modules",
                0,
            )

            total_chapters += result.get(
                "chapters",
                0,
            )

            total_lessons += result.get(
                "lessons",
                0,
            )

    return {
        "status": "ok",
        "modules": total_modules,
        "chapters": total_chapters,
        "lessons": total_lessons,
        "details": results,
    }


# ==========================================================
# Health Check
# ==========================================================

def content_health() -> dict[str, Any]:
    """
    Return current Registry health.
    """

    try:

        statistics = registry.statistics()

        return {
            "status": "ok",
            "registry": statistics,
            "configured_modules": len(
                CONTENT_MODULE_IDS
            ),
        }

    except Exception as exc:

        return {
            "status": "error",
            "error": str(exc),
        }


# ==========================================================
# Statistics
# ==========================================================

def get_content_statistics() -> dict[str, Any]:
    """
    Return detailed content statistics.
    """

    try:

        statistics = registry.statistics()

        modules: list[
            dict[str, Any]
        ] = []

        for module in registry.list_modules():

            module_lessons = 0

            chapters: list[
                dict[str, Any]
            ] = []

            for chapter in registry.list_chapters(
                module.module_id,
            ):

                lesson_count = len(
                    chapter.lessons
                )

                module_lessons += (
                    lesson_count
                )

                chapters.append(
                    {
                        "id": chapter.chapter_id,
                        "title": chapter.title,
                        "lesson_count": lesson_count,
                    }
                )

            modules.append(
                {
                    "id": module.module_id,
                    "title": module.title,
                    "chapter_count": len(
                        chapters
                    ),
                    "lesson_count": module_lessons,
                    "chapters": chapters,
                }
            )

        return {
            "status": "ok",
            "statistics": statistics,
            "modules": modules,
        }

    except Exception as exc:

        return {
            "status": "error",
            "error": str(exc),
        }


# ==========================================================
# Auto Initialization
# ==========================================================

def auto_initialize_content() -> dict[str, Any]:
    """
    Compatibility alias.

    Allows bot.py or other modules to call:

        auto_initialize_content()

    without needing to know the internal initializer name.
    """

    return initialize_all_content()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "CONTENT_PACKAGES",
    "CONTENT_MODULE_IDS",
    "DiscoveredLesson",
    "DiscoveredChapter",
    "DiscoveredModule",
    "discover_module",
    "initialize_module",
    "initialize_all_content",
    "auto_initialize_content",
    "content_health",
    "get_content_statistics",
]
