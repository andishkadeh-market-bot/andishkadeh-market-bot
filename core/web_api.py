"""
Andishkadeh Management & Market
Website API
Shared content API powered by the central Registry.
"""

from __future__ import annotations

from aiohttp import web

from core.registry import registry


def _lesson_payload(lesson):
    return {
        "id": lesson.lesson_id,
        "title": lesson.title,
        "content": lesson.content,
        "order": lesson.order,
    }


def _chapter_payload(chapter):
    return {
        "id": chapter.chapter_id,
        "title": chapter.title,
        "order": chapter.order,
        "lesson_count": len(chapter.lessons),
    }


def _module_payload(module):
    return {
        "id": module.module_id,
        "title": module.title,
        "description": getattr(module, "description", ""),
        "order": module.order,
        "chapter_count": len(module.chapters),
    }


def _json(data, status=200):
    response = web.json_response(data, status=status)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    return response


async def api_options(request):
    return _json({"ok": True})


async def api_info(request):
    return _json({
        "name": "Andishkadeh Management & Market API",
        "version": "1.0.0",
        "status": "online",
        "source": "central_registry",
    })


async def api_modules(request):
    modules = registry.list_modules()

    return _json({
        "count": len(modules),
        "modules": [
            _module_payload(module)
            for module in modules
        ],
    })


async def api_module(request):
    module_id = request.match_info["module_id"]

    module = registry.get_module(module_id)

    if module is None:
        return _json({
            "error": "Module not found"
        }, 404)

    return _json(_module_payload(module))


async def api_chapters(request):
    module_id = request.match_info["module_id"]

    module = registry.get_module(module_id)

    if module is None:
        return _json({
            "error": "Module not found"
        }, 404)

    chapters = module.chapters

    return _json({
        "module_id": module_id,
        "count": len(chapters),
        "chapters": [
            _chapter_payload(chapter)
            for chapter in chapters
        ],
    })


async def api_chapter(request):
    module_id = request.match_info["module_id"]
    chapter_id = request.match_info["chapter_id"]

    module = registry.get_module(module_id)

    if module is None:
        return _json({
            "error": "Module not found"
        }, 404)

    chapter = next(
        (
            chapter
            for chapter in module.chapters
            if chapter.chapter_id == chapter_id
        ),
        None,
    )

    if chapter is None:
        return _json({
            "error": "Chapter not found"
        }, 404)

    return _json({
        "module_id": module_id,
        **_chapter_payload(chapter),
    })


async def api_lessons(request):
    module_id = request.match_info["module_id"]
    chapter_id = request.match_info["chapter_id"]

    module = registry.get_module(module_id)

    if module is None:
        return _json({
            "error": "Module not found"
        }, 404)

    chapter = next(
        (
            chapter
            for chapter in module.chapters
            if chapter.chapter_id == chapter_id
        ),
        None,
    )

    if chapter is None:
        return _json({
            "error": "Chapter not found"
        }, 404)

    return _json({
        "module_id": module_id,
        "chapter_id": chapter_id,
        "count": len(chapter.lessons),
        "lessons": [
            _lesson_payload(lesson)
            for lesson in chapter.lessons
        ],
    })


async def api_lesson(request):
    module_id = request.match_info["module_id"]
    chapter_id = request.match_info["chapter_id"]
    lesson_id = request.match_info["lesson_id"]

    module = registry.get_module(module_id)

    if module is None:
        return _json({
            "error": "Module not found"
        }, 404)

    chapter = next(
        (
            chapter
            for chapter in module.chapters
            if chapter.chapter_id == chapter_id
        ),
        None,
    )

    if chapter is None:
        return _json({
            "error": "Chapter not found"
        }, 404)

    lesson = next(
        (
            lesson
            for lesson in chapter.lessons
            if lesson.lesson_id == lesson_id
        ),
        None,
    )

    if lesson is None:
        return _json({
            "error": "Lesson not found"
        }, 404)

    return _json({
        "module_id": module_id,
        "chapter_id": chapter_id,
        **_lesson_payload(lesson),
    })


async def api_search(request):
    query = request.query.get("q", "").strip().lower()

    if not query:
        return _json({
            "query": "",
            "count": 0,
            "results": [],
        })

    results = []

    for module in registry.list_modules():

        module_title = str(module.title or "")

        if query in module_title.lower():
            results.append({
                "type": "module",
                "module_id": module.module_id,
                "title": module.title,
            })

        for chapter in module.chapters:

            chapter_title = str(chapter.title or "")

            if query in chapter_title.lower():
                results.append({
                    "type": "chapter",
                    "module_id": module.module_id,
                    "chapter_id": chapter.chapter_id,
                    "title": chapter.title,
                })

            for lesson in chapter.lessons:

                title = str(lesson.title or "")
                content = str(lesson.content or "")

                if (
                    query in title.lower()
                    or query in content.lower()
                ):
                    results.append({
                        "type": "lesson",
                        "module_id": module.module_id,
                        "chapter_id": chapter.chapter_id,
                        "lesson_id": lesson.lesson_id,
                        "title": lesson.title,
                    })

    return _json({
        "query": query,
        "count": len(results),
        "results": results,
    })


def register_web_api(app):
    """
    Register all website API routes on the existing aiohttp application.
    """

    app.router.add_get("/api", api_info)
    app.router.add_options("/api", api_options)

    app.router.add_get("/api/modules", api_modules)
    app.router.add_options("/api/modules", api_options)

    app.router.add_get(
        "/api/modules/{module_id}",
        api_module,
    )

    app.router.add_get(
        "/api/modules/{module_id}/chapters",
        api_chapters,
    )

    app.router.add_get(
        "/api/modules/{module_id}/chapters/{chapter_id}",
        api_chapter,
    )

    app.router.add_get(
        "/api/modules/{module_id}/chapters/{chapter_id}/lessons",
        api_lessons,
    )

    app.router.add_get(
        "/api/modules/{module_id}/chapters/{chapter_id}/lessons/{lesson_id}",
        api_lesson,
    )

    app.router.add_get(
        "/api/search",
        api_search,
    )

    app.router.add_options(
        "/api/search",
        api_options,
    )
