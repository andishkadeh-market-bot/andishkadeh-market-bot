/* =========================================================
   ANDISHKADEH API
   Central API communication layer
========================================================= */
/*
 * آدرس اصلی API
 *
 * Backend فعلی روی Render قرار دارد.
 *
 * به /api ختم می‌شود.
 */
const API_BASE =
    "https://andishkadeh-market-bot-2tdu.onrender.com/api";
/* =========================================================
   API FETCH
========================================================= */
async function apiFetch(endpoint = "") {
    const url =
        API_BASE +
        endpoint;
    console.log(
        "[Andishkadeh API]",
        url
    );
    let response;
    try {
        response =
            await fetch(
                url,
                {
                    method: "GET",
                    headers: {
                        "Accept":
                            "application/json"
                    },
                    cache: "no-store"
                }
            );
    } catch (error) {
        console.error(
            "[Andishkadeh API] Network error:",
            error
        );
        throw new Error(
            "ارتباط با سرور API برقرار نشد."
        );
    }
    if (!response.ok) {
        let details = "";
        try {
            details =
                await response.text();
        } catch (_) {
            details = "";
        }
        console.error(
            "[Andishkadeh API] HTTP error:",
            response.status,
            details
        );
        throw new Error(
            `API Error: HTTP ${response.status}`
        );
    }
    const contentType =
        response.headers.get(
            "content-type"
        ) || "";
    if (
        !contentType
            .toLowerCase()
            .includes("application/json")
    ) {
        const text =
            await response.text();
        console.error(
            "[Andishkadeh API] Expected JSON but received:",
            text
        );
        throw new Error(
            "پاسخ API به صورت JSON نیست."
        );
    }
    try {
        return await response.json();
    } catch (error) {
        console.error(
            "[Andishkadeh API] JSON parse error:",
            error
        );
        throw new Error(
            "ساختار پاسخ API قابل خواندن نیست."
        );
    }
}
/* =========================================================
   GET API INFORMATION
========================================================= */
async function getApiInfo() {
    return await apiFetch("");
}
/* =========================================================
   GET ALL MODULES
========================================================= */
async function getModules() {
    return await apiFetch(
        "/modules"
    );
}
/* =========================================================
   GET ONE MODULE
========================================================= */
async function getModule(moduleId) {
    if (!moduleId) {
        throw new Error(
            "Module ID is required."
        );
    }
    return await apiFetch(
        `/modules/${encodeURIComponent(
            moduleId
        )}`
    );
}
/* =========================================================
   GET MODULE CHAPTERS
========================================================= */
async function getModuleChapters(moduleId) {
    if (!moduleId) {
        throw new Error(
            "Module ID is required."
        );
    }
    return await apiFetch(
        `/modules/${encodeURIComponent(
            moduleId
        )}/chapters`
    );
}
/* =========================================================
   GET ONE CHAPTER
========================================================= */
async function getChapter(
    moduleId,
    chapterId
) {
    if (
        !moduleId ||
        !chapterId
    ) {
        throw new Error(
            "Module ID and Chapter ID are required."
        );
    }
    return await apiFetch(
        `/modules/${encodeURIComponent(
            moduleId
        )}/chapters/${encodeURIComponent(
            chapterId
        )}`
    );
}
/* =========================================================
   GET CHAPTER LESSONS
========================================================= */
async function getChapterLessons(
    moduleId,
    chapterId
) {
    if (
        !moduleId ||
        !chapterId
    ) {
        throw new Error(
            "Module ID and Chapter ID are required."
        );
    }
    return await apiFetch(
        `/modules/${encodeURIComponent(
            moduleId
        )}/chapters/${encodeURIComponent(
            chapterId
        )}/lessons`
    );
}
/* =========================================================
   GET ONE LESSON
========================================================= */
async function getLesson(
    moduleId,
    chapterId,
    lessonId
) {
    if (
        !moduleId ||
        !chapterId ||
        !lessonId
    ) {
        throw new Error(
            "Module ID, Chapter ID and Lesson ID are required."
        );
    }
    return await apiFetch(
        `/modules/${encodeURIComponent(
            moduleId
        )}/chapters/${encodeURIComponent(
            chapterId
        )}/lessons/${encodeURIComponent(
            lessonId
        )}`
    );
}
/* =========================================================
   SEARCH
========================================================= */
async function searchContent(query) {
    if (
        !query ||
        !query.trim()
    ) {
        return {
            results: []
        };
    }
    return await apiFetch(
        `/search?q=${encodeURIComponent(
            query.trim()
        )}`
    );
}
