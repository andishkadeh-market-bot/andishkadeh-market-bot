"""
Andishkadeh Management & Market
Universal Content Initializer

مسئولیت‌ها:
- کشف خودکار ماژول‌ها
- ثبت Module / Chapter / Lesson در Registry
- انتقال محتوای کامل درس‌ها
- انتقال Quiz هر درس
- پشتیبانی از ساختارهای قدیمی و جدید
- پشتیبانی از CHAPTER_01 / CHAPTERS / LESSONS
- پشتیبانی از lessons تو در تو
- پشتیبانی از Management
- پشتیبانی از Banking
- پشتیبانی از International Trade
- پشتیبانی از Psychology & Social Work
- پشتیبانی از Finance
- پشتیبانی از Accounting
- پشتیبانی از Marketing
- Health Check
- Statistics

این فایل فقط مسئول Initialization است.
منطق Telegram و UI در handlers.py قرار دارد.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from typing import Any

from core.database import init_database
from core.registry import registry


# ==========================================================
# Content Packages
# ==========================================================

CONTENT_PACKAGES: dict[str, str] = {
    "management": "modules.management.data",
    "banking": "modules.banking.data",
    "international_trade": "modules.international_trade.data",
    "psychology_socialwork": "modules.psychology.data",
    "finance": "modules.finance.data",
    "accounting": "modules.accounting.data",
    "marketing": "modules.marketing.data",
}


CONTENT_MODULE_IDS: tuple[str, ...] = (
    "management",
    "banking",
    "international_trade",
    "psychology_socialwork",
    "finance",
    "accounting",
    "marketing",
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


def _safe_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value

    return []


def _safe_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

    return {}


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
# Quiz Normalization
# ==========================================================

def _normalize_quiz_questions(
    questions: Any,
) -> list[dict[str, Any]]:

    if not isinstance(
        questions,
        list,
    ):
        return []

    normalized: list[dict[str, Any]] = []

    for question in questions:

        if not isinstance(
            question,
            dict,
        ):
            continue

        item = dict(question)

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
                "correct_index"
            )

        if answer is None:
            answer = item.get(
                "answer_index"
            )

        if answer is None:
            answer = item.get(
                "correct_answer_index"
            )

        if answer is None:
            answer = item.get(
                "correct_option"
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
                0
                <= answer
                < len(options)
            ):
                normalized_answer = answer

            elif (
                1
                <= answer
                <= len(options)
            ):
                normalized_answer = (
                    answer - 1
                )

        # --------------------------------------------------
        # String answer
        # --------------------------------------------------

        elif answer is not None:

            answer_text = _safe_str(
                answer
            )

            upper_answer = (
                answer_text.upper()
            )

            letter_map = {
                "A": 0,
                "B": 1,
                "C": 2,
                "D": 3,
            }

            persian_map = {
                "الف": 0,
                "ب": 1,
                "ج": 2,
                "د": 3,
            }

            if (
                upper_answer
                in letter_map
            ):

                index = letter_map[
                    upper_answer
                ]

                if index < len(options):
                    normalized_answer = index

            elif (
                answer_text
                in persian_map
            ):

                index = persian_map[
                    answer_text
                ]

                if index < len(options):
                    normalized_answer = index

            # Numeric string
            if (
                normalized_answer
                is None
            ):

                try:

                    numeric = int(
                        answer_text
                    )

                    if (
                        0
                        <= numeric
                        < len(options)
                    ):
                        normalized_answer = numeric

                    elif (
                        1
                        <= numeric
                        <= len(options)
                    ):
                        normalized_answer = (
                            numeric - 1
                        )

                except (
                    TypeError,
                    ValueError,
                ):
                    pass

            # Full option text
            if (
                normalized_answer
                is None
            ):

                for index, option in enumerate(
                    options
                ):

                    if (
                        _safe_str(option)
                        == answer_text
                    ):

                        normalized_answer = index
                        break

        if (
            normalized_answer
            is not None
        ):
            item["answer"] = normalized_answer

        if "explanation" not in item:

            item["explanation"] = (
                item.get(
                    "explain",
                    "",
                )
                or ""
            )

        normalized.append(
            item
        )

    return normalized


# ==========================================================
# Management Quiz
# ==========================================================

def _get_management_quiz(
    data_module: Any,
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:

    quiz_map = getattr(
        data_module,
        "MANAGEMENT_QUIZ_QUESTIONS",
        None,
    )

    if isinstance(
        quiz_map,
        dict,
    ):

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

    return []


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

    if "quiz" in metadata:

        metadata["quiz"] = (
            _normalize_quiz_questions(
                metadata.get("quiz")
            )
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

    if isinstance(
        raw_lessons,
        dict,
    ):
        raw_lessons = list(
            raw_lessons.values()
        )

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
            lesson_item,
            module_id,
            chapter_id,
        )

        if lesson is not None:
            lessons.append(
                lesson
            )

    return lessons


# ==========================================================
# Generic Chapter Collection
# ==========================================================

def _discover_numbered_chapters(
    data_module: Any,
) -> list[dict[str, Any]]:

    chapters: list[
        dict[str, Any]
    ] = []

    for name in dir(
        data_module
    ):

        if not name.startswith(
            "CHAPTER_"
        ):
            continue

        value = getattr(
            data_module,
            name,
            None,
        )

        if not isinstance(
            value,
            dict,
        ):
            continue

        if not (
            value.get("id")
            or value.get("chapter_id")
        ):
            continue

        chapters.append(
            value
        )

    return chapters


def _get_chapters_source(
    data_module: Any,
) -> list[dict[str, Any]]:

    candidates = (
        "CHAPTERS",
        "CURRICULUM",
        "MANAGEMENT_CURRICULUM",
        "MANAGEMENT_CHAPTERS",
        "MARKETING_CURRICULUM",
        "ACCOUNTING_CURRICULUM",
        "PSYCHOLOGY_CURRICULUM",
        "PSYCHOLOGY_CHAPTERS",
        "INTERNATIONAL_TRADE_CURRICULUM",
    )

    for name in candidates:

        value = getattr(
            data_module,
            name,
            None,
        )

        if isinstance(
            value,
            list,
        ):
            return value

    numbered = (
        _discover_numbered_chapters(
            data_module
        )
    )

    if numbered:
        return numbered

    return []


# ==========================================================
# Generic Lesson Source
# ==========================================================

def _get_lessons_source(
    data_module: Any,
) -> Any:

    candidates = (
        "LESSONS",
        "MANAGEMENT_LESSONS",
        "MARKETING_LESSONS",
        "ACCOUNTING_LESSONS",
        "PSYCHOLOGY_LESSONS",
        "INTERNATIONAL_TRADE_LESSONS",
    )

    for name in candidates:

        value = getattr(
            data_module,
            name,
            None,
        )

        if isinstance(
            value,
            (list, dict),
        ):
            return value

    return []


def _build_lessons_by_chapter(
    lessons_source: Any,
) -> dict[
    str,
    list[dict[str, Any]],
]:

    result: dict[
        str,
        list[dict[str, Any]],
    ] = {}

    if isinstance(
        lessons_source,
        dict,
    ):

        # ----------------------------------------------
        # Dictionary may be:
        # chapter_id -> [lessons]
        # OR lesson_id -> lesson
        # ----------------------------------------------

        for key, value in lessons_source.items():

            if isinstance(
                value,
                list,
            ):

                result[
                    _safe_str(key)
                ] = [
                    item
                    for item in value
                    if isinstance(
                        item,
                        dict,
                    )
                ]

            elif isinstance(
                value,
                dict,
            ):

                lesson = dict(
                    value
                )

                chapter_id = _first_non_empty(
                    lesson,
                    (
                        "chapter_id",
                        "original_chapter_id",
                    ),
                )

                if chapter_id:

                    result.setdefault(
                        chapter_id,
                        [],
                    ).append(
                        lesson
                    )

        return result

    if not isinstance(
        lessons_source,
        list,
    ):
        return result

    for lesson in lessons_source:

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

        result.setdefault(
            chapter_id,
            [],
        ).append(
            lesson
        )

    return result


# ==========================================================
# Generic Curriculum Extraction
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

    chapters_data = (
        _get_chapters_source(
            data_module
        )
    )

    if not chapters_data:
        return None

    lessons_source = (
        _get_lessons_source(
            data_module
        )
    )

    lessons_by_chapter = (
        _build_lessons_by_chapter(
            lessons_source
        )
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
                "slug",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
                "chapter_title",
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

        nested_lessons = (
            chapter_item.get(
                "lessons"
            )
        )

        if isinstance(
            nested_lessons,
            (list, dict),
        ):

            raw_lessons = nested_lessons

        else:

            raw_lessons = (
                lessons_by_chapter.get(
                    chapter_id,
                    [],
                )
            )

        lessons = (
            _extract_chapter_lessons(
                raw_lessons,
                module_id,
                chapter_id,
            )
        )

        # --------------------------------------------------
        # Management compatibility:
        # quiz stored separately in MANAGEMENT_QUIZ_QUESTIONS
        # --------------------------------------------------

        if module_id == "management":

            for lesson in lessons:

                quiz = _get_management_quiz(
                    data_module,
                    chapter_id,
                    lesson.lesson_id,
                )

                if quiz:
                    lesson.metadata[
                        "quiz"
                    ] = quiz

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
# Specialized International Trade
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
            chapter_id,
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

        lessons = (
            _extract_chapter_lessons(
                raw_lessons,
                module_id,
                chapter_id,
            )
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

    module_id = _safe_str(
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
            "[ContentInitializer] "
            f"Failed to import {package_path}: {exc}"
        )

        return None

    if module_id == "international_trade":

        result = (
            _extract_international_trade_curriculum(
                data_module
            )
        )

        if result is not None:
            return result

    result = _extract_generic_curriculum(
        data_module,
        module_id,
    )

    return result


# ==========================================================
# Registry Registration
# ==========================================================

def _register_module(
    module: DiscoveredModule,
) -> int:

    try:

        registry.register_module(
            module_id=module.module_id,
            title=module.title,
            description=module.description,
        )

    except TypeError:

        try:

            registry.register_module(
                module.module_id,
                module.title,
                module.description,
            )

        except TypeError:

            registry.register_module(
                module.module_id,
                module.title,
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

            try:

                registry.register_chapter(
                    chapter.module_id,
                    chapter.chapter_id,
                    chapter.title,
                    chapter.description,
                )

            except TypeError:

                registry.register_chapter(
                    chapter.module_id,
                    chapter.chapter_id,
                    chapter.title,
                )

        for lesson in chapter.lessons:

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

            if lesson.content:

                lesson_data[
                    "content"
                ] = lesson.content

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

            if "quiz" in lesson_data:

                lesson_data[
                    "quiz"
                ] = _normalize_quiz_questions(
                    lesson_data.get(
                        "quiz"
                    )
                )

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
# Module Initialization
# ==========================================================

def initialize_module(
    module_id: str,
) -> dict[str, Any]:

    module_id = _safe_str(
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

    try:

        lesson_count = _register_module(
            module
        )

    except Exception as exc:

        print(
            "[ContentInitializer] "
            f"Registration failed for {module_id}: {exc}"
        )

        return {
            "module_id": module_id,
            "status": "error",
            "modules": 0,
            "chapters": 0,
            "lessons": 0,
            "error": str(exc),
        }

    return {
        "module_id": module.module_id,
        "status": "ok",
        "modules": 1,
        "chapters": len(
            module.chapters
        ),
        "lessons": lesson_count,
    }


# ==========================================================
# Initialize Everything
# ==========================================================

def initialize_all_content() -> dict[str, Any]:

    try:
        init_database()
    except Exception as exc:
        print(
            "[ContentInitializer] "
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

            total_modules += int(
                result.get(
                    "modules",
                    0,
                )
            )

            total_chapters += int(
                result.get(
                    "chapters",
                    0,
                )
            )

            total_lessons += int(
                result.get(
                    "lessons",
                    0,
                )
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
                module.module_id
            ):

                lesson_count = len(
                    getattr(
                        chapter,
                        "lessons",
                        {},
                    )
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
# Compatibility
# ==========================================================

def auto_initialize_content() -> dict[str, Any]:
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
