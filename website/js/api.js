/* =========================================================
ANDISHKADEH MANAGEMENT & MARKET
API COMMUNICATION LAYER
========================================================= */

“use strict”;

/* =========================================================
API BASE URL
========================================================= */

const API_BASE =
“https://andishkadeh-market-bot-2tdu.onrender.com/api”;

/* =========================================================
GENERIC API FETCH
========================================================= */

async function apiFetch(endpoint = “”) {

const url =
    API_BASE + endpoint;
console.log(
    "[Andishkadeh API] Request:",
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
/* =====================================================
   HTTP ERROR
===================================================== */
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
        `خطای API: HTTP ${response.status}`
    );
}
/* =====================================================
   CONTENT TYPE
===================================================== */
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
        "[Andishkadeh API] Invalid response:",
        text
    );
    throw new Error(
        "پاسخ API به صورت JSON نیست."
    );
}
/* =====================================================
   JSON PARSE
===================================================== */
try {
    const data =
        await response.json();
    console.log(
        "[Andishkadeh API] Response:",
        data
    );
    return data;
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
API INFORMATION
========================================================= */

async function getApiInfo() {

return await apiFetch(
    ""
);

}

/* =========================================================
ALL MODULES
========================================================= */

async function getModules() {

return await apiFetch(
    "/modules"
);

}

/* =========================================================
SINGLE MODULE
========================================================= */

async function getModule(
moduleId
) {

if (!moduleId) {
    throw new Error(
        "شناسه ماژول مشخص نشده است."
    );
}
return await apiFetch(
    `/modules/${encodeURIComponent(
        moduleId
    )}`
);

}

/* =========================================================
MODULE CHAPTERS
========================================================= */

async function getModuleChapters(
moduleId
) {

if (!moduleId) {
    throw new Error(
        "شناسه ماژول مشخص نشده است."
    );
}
return await apiFetch(
    `/modules/${encodeURIComponent(
        moduleId
    )}/chapters`
);

}

/* =========================================================
SINGLE CHAPTER
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
        "شناسه ماژول یا فصل مشخص نشده است."
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
CHAPTER LESSONS
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
        "شناسه ماژول یا فصل مشخص نشده است."
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
SINGLE LESSON
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
        "شناسه ماژول، فصل یا درس مشخص نشده است."
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

async function searchContent(
query
) {

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
