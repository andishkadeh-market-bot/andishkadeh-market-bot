const API_BASE =
    "https://andishkadeh-market-bot-2tdu.onrender.com/api";


/* =========================================================
   API FETCH
========================================================= */

async function apiFetch(endpoint = "") {

    const response = await fetch(
        API_BASE + endpoint,
        {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        }
    );


    if (!response.ok) {

        throw new Error(
            `API Error: ${response.status}`
        );

    }


    return await response.json();

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
        `/modules/${encodeURIComponent(moduleId)}`
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
        `/modules/${encodeURIComponent(moduleId)}/chapters`
    );

}


/* =========================================================
   GET ONE CHAPTER
========================================================= */

async function getChapter(
    moduleId,
    chapterId
) {

    if (!moduleId || !chapterId) {

        throw new Error(
            "Module ID and Chapter ID are required."
        );

    }


    return await apiFetch(
        `/modules/${encodeURIComponent(moduleId)}/chapters/${encodeURIComponent(chapterId)}`
    );

}


/* =========================================================
   GET CHAPTER LESSONS
========================================================= */

async function getChapterLessons(
    moduleId,
    chapterId
) {

    if (!moduleId || !chapterId) {

        throw new Error(
            "Module ID and Chapter ID are required."
        );

    }


    return await apiFetch(
        `/modules/${encodeURIComponent(moduleId)}/chapters/${encodeURIComponent(chapterId)}/lessons`
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
        `/modules/${encodeURIComponent(moduleId)}/chapters/${encodeURIComponent(chapterId)}/lessons/${encodeURIComponent(lessonId)}`
    );

}


/* =========================================================
   SEARCH
========================================================= */

async function searchContent(query) {

    if (!query || !query.trim()) {

        return {
            results: []
        };

    }


    return await apiFetch(
        `/search?q=${encodeURIComponent(query.trim())}`
    );

}
