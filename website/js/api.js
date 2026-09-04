/* =========================================================
   ANDISHKADEH MANAGEMENT & MARKET
   WEBSITE APPLICATION
   API + UI + NAVIGATION + QUIZ
   ========================================================= */

"use strict";


/* =========================================================
   API BASE URL
   ========================================================= */

const API_BASE =
    "https://andishkadeh-market-bot-2tdu.onrender.com/api";


/* =========================================================
   GLOBAL STATE
   ========================================================= */

let currentModuleId = null;
let currentChapterId = null;
let currentLessonId = null;

let currentModuleData = null;
let currentChapterData = null;

let modulesCache = [];

let navigationState = {
    moduleId: null,
    chapterId: null,
    lessonId: null
};


/* =========================================================
   API COMMUNICATION
   ========================================================= */

async function apiFetch(endpoint = "") {

    const url = API_BASE + endpoint;

    console.log(
        "[Andishkadeh API] Request:",
        url
    );

    let response;

    try {

        response = await fetch(
            url,
            {
                method: "GET",
                headers: {
                    "Accept": "application/json"
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
            details = await response.text();
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

    return await apiFetch("");

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


/* =========================================================
   GENERIC DATA NORMALIZATION
   ========================================================= */

function normalizeList(
    data,
    possibleKeys = []
) {

    if (Array.isArray(data)) {
        return data;
    }

    if (
        data &&
        typeof data === "object"
    ) {

        for (
            const key of possibleKeys
        ) {

            if (
                Array.isArray(
                    data[key]
                )
            ) {

                return data[key];
            }
        }

        if (
            data.data &&
            Array.isArray(
                data.data
            )
        ) {

            return data.data;
        }

        if (
            data.result &&
            Array.isArray(
                data.result
            )
        ) {

            return data.result;
        }
    }

    return [];
}


function getObjectId(
    item
) {

    if (
        !item ||
        typeof item !== "object"
    ) {

        return "";
    }

    return String(
        item.id ||
        item.module_id ||
        item.chapter_id ||
        item.lesson_id ||
        ""
    );
}


function getTitle(
    item,
    fallback = "بدون عنوان"
) {

    if (
        !item ||
        typeof item !== "object"
    ) {

        return fallback;
    }

    return (
        item.title ||
        item.name ||
        item.label ||
        fallback
    );
}


function getDescription(
    item
) {

    if (
        !item ||
        typeof item !== "object"
    ) {

        return "";
    }

    return (
        item.description ||
        item.summary ||
        item.short_description ||
        ""
    );
}


/* =========================================================
   TEXT SAFETY
   ========================================================= */

function escapeHtml(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";
    }

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


function formatText(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";
    }

    return escapeHtml(
        value
    );
}


/* =========================================================
   DOM HELPERS
   ========================================================= */

function getElement(
    id
) {

    return document.getElementById(
        id
    );
}


function setHtml(
    id,
    html
) {

    const element =
        getElement(id);

    if (!element) {
        return;
    }

    element.innerHTML = html;
}


function showElement(
    id
) {

    const element =
        getElement(id);

    if (!element) {
        return;
    }

    element.classList.remove(
        "hidden"
    );
}


function hideElement(
    id
) {

    const element =
        getElement(id);

    if (!element) {
        return;
    }

    element.classList.add(
        "hidden"
    );
}


/* =========================================================
   LOADING / ERROR HTML
   ========================================================= */

function loadingHtml(
    message = "در حال دریافت اطلاعات..."
) {

    return `
        <div class="loading">
            <div class="spinner"></div>
            <p>${escapeHtml(message)}</p>
        </div>
    `;
}


function errorHtml(
    message
) {

    return `
        <div class="error-box">
            <strong>دریافت اطلاعات با مشکل مواجه شد.</strong>
            <p style="margin-top:8px;">
                ${escapeHtml(
                    message ||
                    "خطای نامشخص"
                )}
            </p>
        </div>
    `;
}


/* =========================================================
   TOAST
   ========================================================= */

function showToast(
    message
) {

    const toast =
        getElement("toast");

    if (!toast) {
        return;
    }

    toast.textContent =
        message || "";

    toast.classList.add(
        "show"
    );

    clearTimeout(
        showToast.timeout
    );

    showToast.timeout =
        setTimeout(
            () => {
                toast.classList.remove(
                    "show"
                );
            },
            3000
        );
}


/* =========================================================
   MOBILE MENU
   ========================================================= */

function toggleMobileMenu() {

    const menu =
        getElement("mobileMenu");

    if (!menu) {
        return;
    }

    menu.classList.toggle(
        "active"
    );
}


function closeMobileMenu() {

    const menu =
        getElement("mobileMenu");

    if (!menu) {
        return;
    }

    menu.classList.remove(
        "active"
    );
}


/* =========================================================
   URL STATE
   ========================================================= */

function updateUrl(
    params = {},
    replace = false
) {

    const url =
        new URL(
            window.location.href
        );

    url.search = "";

    Object.keys(params)
        .forEach(
            key => {

                const value =
                    params[key];

                if (
                    value !== null &&
                    value !== undefined &&
                    value !== ""
                ) {

                    url.searchParams.set(
                        key,
                        value
                    );
                }
            }
        );

    if (replace) {

        window.history.replaceState(
            {},
            "",
            url
        );

    } else {

        window.history.pushState(
            {},
            "",
            url
        );
    }
}


function readUrlState() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    return {
        moduleId:
            params.get("module"),
        chapterId:
            params.get("chapter"),
        lessonId:
            params.get("lesson")
    };
}


/* =========================================================
   PAGE VISIBILITY
   ========================================================= */

function hideAllPages() {

    hideElement(
        "homePage"
    );

    hideElement(
        "modulePage"
    );

    hideElement(
        "chapterPage"
    );

    hideElement(
        "lessonPage"
    );
}


function showHome(
    updateHistory = true
) {

    hideAllPages();

    showElement(
        "homePage"
    );

    currentModuleId = null;
    currentChapterId = null;
    currentLessonId = null;

    currentModuleData = null;
    currentChapterData = null;

    navigationState = {
        moduleId: null,
        chapterId: null,
        lessonId: null
    };

    if (updateHistory) {

        updateUrl(
            {},
            false
        );
    }

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    closeMobileMenu();
}


/* =========================================================
   MODULE PAGE
   ========================================================= */

async function showModule(
    moduleId,
    updateHistory = true
) {

    if (!moduleId) {
        return;
    }

    hideAllPages();

    showElement(
        "modulePage"
    );

    const header =
        getElement(
            "moduleHeader"
        );

    const container =
        getElement(
            "chaptersContainer"
        );

    if (header) {
        header.innerHTML =
            loadingHtml(
                "در حال دریافت اطلاعات ماژول..."
            );
    }

    if (container) {
        container.innerHTML =
            loadingHtml(
                "در حال دریافت فصل‌ها..."
            );
    }

    currentModuleId =
        String(moduleId);

    currentChapterId = null;
    currentLessonId = null;

    navigationState = {
        moduleId:
            currentModuleId,
        chapterId: null,
        lessonId: null
    };

    if (updateHistory) {

        updateUrl({
            module:
                currentModuleId
        });
    }

    closeMobileMenu();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    try {

        const [
            moduleResponse,
            chaptersResponse
        ] = await Promise.all([
            getModule(
                currentModuleId
            ),
            getModuleChapters(
                currentModuleId
            )
        ]);

        currentModuleData =
            moduleResponse;

        const chapters =
            normalizeList(
                chaptersResponse,
                [
                    "chapters",
                    "items",
                    "results"
                ]
            );

        renderModuleHeader(
            moduleResponse,
            chapters
        );

        renderChapters(
            chapters
        );

    } catch (error) {

        console.error(
            "[Andishkadeh] Module error:",
            error
        );

        if (header) {
            header.innerHTML =
                errorHtml(
                    error.message
                );
        }

        if (container) {
            container.innerHTML =
                "";
        }

        showToast(
            error.message
        );
    }
}


/* =========================================================
   MODULE HEADER
   ========================================================= */

function renderModuleHeader(
    data,
    chapters
) {

    const header =
        getElement(
            "moduleHeader"
        );

    if (!header) {
        return;
    }

    const module =
        data &&
        data.module
            ? data.module
            : data;

    const title =
        getTitle(
            module,
            "ماژول آموزشی"
        );

    const description =
        getDescription(
            module
        );

    header.innerHTML = `
        <div>
            <span
                style="
                    display:inline-block;
                    color:#16c7bd;
                    font-size:13px;
                    font-weight:700;
                    margin-bottom:8px;
                "
            >
                مسیر آموزشی
            </span>

            <h1>
                ${escapeHtml(title)}
            </h1>

            ${
                description
                    ? `
                        <p>
                            ${escapeHtml(
                                description
                            )}
                        </p>
                    `
                    : ""
            }

            <div
                style="
                    display:flex;
                    gap:18px;
                    flex-wrap:wrap;
                    margin-top:18px;
                    color:#b9c7d3;
                    font-size:13px;
                "
            >
                <span>
                    📚 ${chapters.length} فصل
                </span>
            </div>
        </div>
    `;
}


/* =========================================================
   RENDER MODULES
   ========================================================= */

async function loadModules() {

    const container =
        getElement(
            "modulesContainer"
        );

    if (!container) {
        return;
    }

    container.innerHTML =
        loadingHtml(
            "در حال دریافت محتوای آموزشی..."
        );

    try {

        const response =
            await getModules();

        const modules =
            normalizeList(
                response,
                [
                    "modules",
                    "items",
                    "results"
                ]
            );

        modulesCache =
            modules;

        renderModules(
            modules
        );

        await updateStatistics(
            modules
        );

    } catch (error) {

        console.error(
            "[Andishkadeh] Modules error:",
            error
        );

        container.innerHTML =
            errorHtml(
                error.message
            );

        showToast(
            error.message
        );
    }
}


/* =========================================================
   MODULE ICON
   ========================================================= */

function getModuleIcon(
    module
) {

    const id =
        getObjectId(
            module
        ).toLowerCase();

    const title =
        getTitle(
            module
        ).toLowerCase();

    if (
        id.includes("bank") ||
        title.includes("بانک")
    ) {
        return "🏦";
    }

    if (
        id.includes("trade") ||
        title.includes("تجارت")
    ) {
        return "🌍";
    }

    if (
        id.includes("psych") ||
        title.includes("روان")
    ) {
        return "🧠";
    }

    if (
        id.includes("management") ||
        title.includes("مدیریت")
    ) {
        return "📊";
    }

    if (
        id.includes("finance") ||
        title.includes("مال")
    ) {
        return "💰";
    }

    if (
        id.includes("exam") ||
        title.includes("آزمون")
    ) {
        return "🎯";
    }

    return "📚";
}


/* =========================================================
   RENDER MODULE CARDS
   ========================================================= */

function renderModules(
    modules
) {

    const container =
        getElement(
            "modulesContainer"
        );

    if (!container) {
        return;
    }

    if (!modules.length) {

        container.innerHTML = `
            <div class="error-box">
                هنوز ماژول آموزشی‌ای ثبت نشده است.
            </div>
        `;

        return;
    }

    container.innerHTML =
        modules
            .map(
                (
                    module,
                    index
                ) => {

                    const id =
                        getObjectId(
                            module
                        );

                    const title =
                        getTitle(
                            module,
                            `ماژول ${index + 1}`
                        );

                    const description =
                        getDescription(
                            module
                        ) ||
                        "مسیر آموزشی تخصصی اندیشکده مدیریت و بازار.";

                    const chapterCount =
                        Number(
                            module.chapter_count ||
                            module.chapters_count ||
                            0
                        );

                    const lessonCount =
                        Number(
                            module.lesson_count ||
                            module.lessons_count ||
                            0
                        );

                    return `
                        <article
                            class="module-card"
                            data-module-id="${escapeHtml(id)}"
                        >

                            <div class="module-icon">
                                ${getModuleIcon(module)}
                            </div>

                            <h3>
                                ${escapeHtml(title)}
                            </h3>

                            <p>
                                ${escapeHtml(
                                    description
                                )}
                            </p>

                            <div class="module-meta">

                                ${
                                    chapterCount
                                        ? `
                                            <span>
                                                📚 ${chapterCount} فصل
                                            </span>
                                        `
                                        : ""
                                }

                                ${
                                    lessonCount
                                        ? `
                                            <span>
                                                📖 ${lessonCount} درس
                                            </span>
                                        `
                                        : ""
                                }

                            </div>

                            <button
                                type="button"
                                class="module-button"
                                onclick="showModule('${escapeHtml(id)}')"
                            >
                                مشاهده مسیر آموزشی ←
                            </button>

                        </article>
                    `;
                }
            )
            .join("");
}


/* =========================================================
   STATISTICS
   ========================================================= */

async function updateStatistics(
    modules
) {

    let totalModules =
        modules.length;

    let totalChapters = 0;
    let totalLessons = 0;

    const chapterPromises =
        modules.map(
            async module => {

                const moduleId =
                    getObjectId(
                        module
                    );

                if (!moduleId) {
                    return [];
                }

                try {

                    const response =
                        await getModuleChapters(
                            moduleId
                        );

                    return normalizeList(
                        response,
                        [
                            "chapters",
                            "items",
                            "results"
                        ]
                    );

                } catch (error) {

                    console.warn(
                        "[Andishkadeh] Statistics chapter error:",
                        moduleId,
                        error
                    );

                    return [];
                }
            }
        );

    const chapterResults =
        await Promise.all(
            chapterPromises
        );

    chapterResults.forEach(
        chapters => {

            totalChapters +=
                chapters.length;

            chapters.forEach(
                chapter => {

                    const lessonCount =
                        Number(
                            chapter.lesson_count ||
                            chapter.lessons_count ||
                            0
                        );

                    totalLessons +=
                        lessonCount;
                }
            );
        }
    );

    /*
     * If chapter metadata does not contain
     * lesson counts, fetch lessons.
     */

    if (
        totalLessons === 0 &&
        totalChapters > 0
    ) {

        const lessonPromises = [];

        modules.forEach(
            (
                module,
                moduleIndex
            ) => {

                const moduleId =
                    getObjectId(
                        module
                    );

                const chapters =
                    chapterResults[
                        moduleIndex
                    ] || [];

                chapters.forEach(
                    chapter => {

                        const chapterId =
                            getObjectId(
                                chapter
                            );

                        if (
                            moduleId &&
                            chapterId
                        ) {

                            lessonPromises.push(
                                getChapterLessons(
                                    moduleId,
                                    chapterId
                                )
                            );
                        }
                    }
                );
            }
        );

        const lessonResults =
            await Promise.all(
                lessonPromises
                    .map(
                        promise =>
                            promise.catch(
                                () => []
                            )
                    )
            );

        lessonResults.forEach(
            response => {

                totalLessons +=
                    normalizeList(
                        response,
                        [
                            "lessons",
                            "items",
                            "results"
                        ]
                    ).length;
            }
        );
    }

    setText(
        "statModules",
        totalModules
    );

    setText(
        "statChapters",
        totalChapters
    );

    setText(
        "statLessons",
        totalLessons
    );

    setText(
        "heroModuleCount",
        totalModules
    );

    setText(
        "heroChapterCount",
        totalChapters
    );

    setText(
        "heroLessonCount",
        totalLessons
    );
}


function setText(
    id,
    value
) {

    const element =
        getElement(id);

    if (!element) {
        return;
    }

    element.textContent =
        value;
}


/* =========================================================
   CHAPTERS
   ========================================================= */

function renderChapters(
    chapters
) {

    const container =
        getElement(
            "chaptersContainer"
        );

    if (!container) {
        return;
    }

    if (!chapters.length) {

        container.innerHTML = `
            <div class="error-box">
                هنوز فصلی برای این ماژول ثبت نشده است.
            </div>
        `;

        return;
    }

    container.innerHTML =
        chapters
            .map(
                (
                    chapter,
                    index
                ) => {

                    const chapterId =
                        getObjectId(
                            chapter
                        );

                    const title =
                        getTitle(
                            chapter,
                            `فصل ${index + 1}`
                        );

                    const description =
                        getDescription(
                            chapter
                        );

                    const lessonCount =
                        Number(
                            chapter.lesson_count ||
                            chapter.lessons_count ||
                            0
                        );

                    return `
                        <article
                            class="chapter-card"
                            onclick="showChapter(
                                '${escapeHtml(
                                    chapterId
                                )}'
                            )"
                        >

                            <div
                                class="chapter-number"
                            >
                                ${index + 1}
                            </div>

                            <div
                                class="chapter-info"
                            >

                                <h3>
                                    ${escapeHtml(title)}
                                </h3>

                                ${
                                    description
                                        ? `
                                            <span>
                                                ${escapeHtml(
                                                    description
                                                )}
                                            </span>
                                        `
                                        : `
                                            <span>
                                                مسیر آموزشی فصل
                                            </span>
                                        `
                                }

                                ${
                                    lessonCount
                                        ? `
                                            <span
                                                style="
                                                    display:block;
                                                    margin-top:4px;
                                                "
                                            >
                                                📖 ${lessonCount} درس
                                            </span>
                                        `
                                        : ""
                                }

                            </div>

                            <div
                                class="chapter-arrow"
                            >
                                ←
                            </div>

                        </article>
                    `;
                }
            )
            .join("");
}


/* =========================================================
   SHOW CHAPTER
   ========================================================= */

async function showChapter(
    chapterId,
    updateHistory = true
) {

    if (
        !currentModuleId ||
        !chapterId
    ) {

        showToast(
            "اطلاعات ماژول یا فصل ناقص است."
        );

        return;
    }

    hideAllPages();

    showElement(
        "chapterPage"
    );

    currentChapterId =
        String(chapterId);

    currentLessonId = null;

    navigationState = {
        moduleId:
            currentModuleId,
        chapterId:
            currentChapterId,
        lessonId: null
    };

    if (updateHistory) {

        updateUrl({
            module:
                currentModuleId,
            chapter:
                currentChapterId
        });
    }

    const header =
        getElement(
            "chapterHeader"
        );

    const container =
        getElement(
            "lessonsContainer"
        );

    if (header) {

        header.innerHTML =
            loadingHtml(
                "در حال دریافت اطلاعات فصل..."
            );
    }

    if (container) {

        container.innerHTML =
            loadingHtml(
                "در حال دریافت درس‌ها..."
            );
    }

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    try {

        const [
            chapterResponse,
            lessonsResponse
        ] = await Promise.all([
            getChapter(
                currentModuleId,
                currentChapterId
            ),
            getChapterLessons(
                currentModuleId,
                currentChapterId
            )
        ]);

        currentChapterData =
            chapterResponse;

        const lessons =
            normalizeList(
                lessonsResponse,
                [
                    "lessons",
                    "items",
                    "results"
                ]
            );

        renderChapterHeader(
            chapterResponse,
            lessons
        );

        renderLessons(
            lessons
        );

    } catch (error) {

        console.error(
            "[Andishkadeh] Chapter error:",
            error
        );

        if (header) {

            header.innerHTML =
                errorHtml(
                    error.message
                );
        }

        if (container) {
            container.innerHTML = "";
        }

        showToast(
            error.message
        );
    }
}


/* =========================================================
   CHAPTER HEADER
   ========================================================= */

function renderChapterHeader(
    data,
    lessons
) {

    const header =
        getElement(
            "chapterHeader"
        );

    if (!header) {
        return;
    }

    const chapter =
        data &&
        data.chapter
            ? data.chapter
            : data;

    const title =
        getTitle(
            chapter,
            "فصل آموزشی"
        );

    const description =
        getDescription(
            chapter
        );

    header.innerHTML = `
        <span
            style="
                display:inline-block;
                color:#16c7bd;
                font-size:13px;
                font-weight:700;
                margin-bottom:8px;
            "
        >
            فصل آموزشی
        </span>

        <h1>
            ${escapeHtml(title)}
        </h1>

        ${
            description
                ? `
                    <p>
                        ${escapeHtml(
                            description
                        )}
                    </p>
                `
                : ""
        }

        <div
            style="
                margin-top:16px;
                color:#b9c7d3;
                font-size:13px;
            "
        >
            📖 ${lessons.length} درس
        </div>
    `;
}


/* =========================================================
   RENDER LESSONS
   ========================================================= */

function renderLessons(
    lessons
) {

    const container =
        getElement(
            "lessonsContainer"
        );

    if (!container) {
        return;
    }

    if (!lessons.length) {

        container.innerHTML = `
            <div class="error-box">
                هنوز درسی برای این فصل ثبت نشده است.
            </div>
        `;

        return;
    }

    container.innerHTML =
        lessons
            .map(
                (
                    lesson,
                    index
                ) => {

                    const lessonId =
                        getObjectId(
                            lesson
                        );

                    const title =
                        getTitle(
                            lesson,
                            `درس ${index + 1}`
                        );

                    const description =
                        getDescription(
                            lesson
                        );

                    return `
                        <article
                            class="lesson-card"
                            onclick="showLesson(
                                '${escapeHtml(
                                    lessonId
                                )}'
                            )"
                        >

                            <div
                                style="
                                    color:#16c7bd;
                                    font-size:12px;
                                    font-weight:700;
                                    margin-bottom:8px;
                                "
                            >
                                درس ${index + 1}
                            </div>

                            <h3>
                                ${escapeHtml(title)}
                            </h3>

                            ${
                                description
                                    ? `
                                        <span>
                                            ${escapeHtml(
                                                description
                                            )}
                                        </span>
                                    `
                                    : `
                                        <span>
                                            مشاهده محتوای درس ←
                                        </span>
                                    `
                            }

                        </article>
                    `;
                }
            )
            .join("");
}


/* =========================================================
   SHOW LESSON
   ========================================================= */

async function showLesson(
    lessonId,
    updateHistory = true
) {

    if (
        !currentModuleId ||
        !currentChapterId ||
        !lessonId
    ) {

        showToast(
            "اطلاعات مسیر درس ناقص است."
        );

        return;
    }

    hideAllPages();

    showElement(
        "lessonPage"
    );

    currentLessonId =
        String(lessonId);

    navigationState = {
        moduleId:
            currentModuleId,
        chapterId:
            currentChapterId,
        lessonId:
            currentLessonId
    };

    if (updateHistory) {

        updateUrl({
            module:
                currentModuleId,
            chapter:
                currentChapterId,
            lesson:
                currentLessonId
        });
    }

    const container =
        getElement(
            "lessonContent"
        );

    if (!container) {
        return;
    }

    container.innerHTML =
        loadingHtml(
            "در حال دریافت محتوای درس..."
        );

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    try {

        const response =
            await getLesson(
                currentModuleId,
                currentChapterId,
                currentLessonId
            );

        renderLesson(
            response
        );

    } catch (error) {

        console.error(
            "[Andishkadeh] Lesson error:",
            error
        );

        container.innerHTML =
            errorHtml(
                error.message
            );

        showToast(
            error.message
        );
    }
}


/* =========================================================
   LESSON DATA EXTRACTION
   ========================================================= */

function extractLesson(
    data
) {

    if (
        data &&
        typeof data === "object"
    ) {

        if (
            data.lesson &&
            typeof data.lesson === "object"
        ) {

            return data.lesson;
        }

        if (
            data.data &&
            data.data.lesson &&
            typeof data.data.lesson === "object"
        ) {

            return data.data.lesson;
        }
    }

    return data || {};
}


/* =========================================================
   LESSON CONTENT EXTRACTION
   ========================================================= */

function getLessonText(
    lesson
) {

    return (
        lesson.content ||
        lesson.text ||
        lesson.body ||
        lesson.description ||
        ""
    );
}


function getLessonExample(
    lesson
) {

    return (
        lesson.example ||
        lesson.practical_example ||
        lesson.application_example ||
        ""
    );
}


function getLessonSpecialNotes(
    lesson
) {

    return (
        lesson.specialized_notes ||
        lesson.special_notes ||
        lesson.expert_notes ||
        lesson.notes ||
        []
    );
}


function getLessonExamTips(
    lesson
) {

    return (
        lesson.exam_tips ||
        lesson.test_tips ||
        lesson.exam_notes ||
        []
    );
}


/* =========================================================
   NORMALIZE NOTES
   ========================================================= */

function normalizeNotes(
    notes
) {

    if (!notes) {
        return [];
    }

    if (Array.isArray(notes)) {

        return notes.map(
            item => {

                if (
                    typeof item === "string"
                ) {

                    return item;
                }

                if (
                    item &&
                    typeof item === "object"
                ) {

                    return (
                        item.text ||
                        item.title ||
                        item.content ||
                        JSON.stringify(item)
                    );
                }

                return String(item);
            }
        );
    }

    if (
        typeof notes === "string"
    ) {

        return notes
            .split(/\r?\n/)
            .map(
                item => item.trim()
            )
            .filter(Boolean);
    }

    return [];
}


/* =========================================================
   QUIZ EXTRACTION
   ========================================================= */

function extractQuestions(
    lesson
) {

    let questions =
        lesson.questions ||
        lesson.quiz ||
        lesson.quiz_questions ||
        [];

    if (
        questions &&
        !Array.isArray(questions) &&
        typeof questions === "object"
    ) {

        questions =
            questions.questions ||
            questions.items ||
            questions.results ||
            [];
    }

    return Array.isArray(
        questions
    )
        ? questions
        : [];
}


/* =========================================================
   NORMALIZE QUESTION OPTIONS
   ========================================================= */

function normalizeOptions(
    question
) {

    let options =
        question.options ||
        question.choices ||
        question.answers ||
        [];

    if (
        !Array.isArray(options) &&
        typeof options === "object"
    ) {

        options =
            Object.keys(options)
                .map(
                    key => ({
                        id: key,
                        text:
                            options[key]
                    })
                );
    }

    if (!Array.isArray(options)) {
        return [];
    }

    return options.map(
        (
            option,
            index
        ) => {

            if (
                typeof option === "string"
            ) {

                return {
                    id:
                        String.fromCharCode(
                            65 + index
                        ),
                    text:
                        option
                };
            }

            if (
                option &&
                typeof option === "object"
            ) {

                return {
                    id:
                        String(
                            option.id ||
                            option.key ||
                            String.fromCharCode(
                                65 + index
                            )
                        ),
                    text:
                        option.text ||
                        option.label ||
                        option.title ||
                        String(option)
                };
            }

            return {
                id:
                    String.fromCharCode(
                        65 + index
                    ),
                text:
                    String(option)
            };
        }
    );
}


/* =========================================================
   CORRECT ANSWER
   ========================================================= */

function getCorrectAnswer(
    question,
    options
) {

    let answer =
        question.correct_answer;

    if (
        answer === undefined ||
        answer === null ||
        answer === ""
    ) {

        answer =
            question.answer;
    }

    if (
        answer === undefined ||
        answer === null ||
        answer === ""
    ) {

        answer =
            question.correct;
    }

    if (
        typeof answer === "number"
    ) {

        if (
            options[answer]
        ) {

            return options[
                answer
            ].id;
        }

        if (
            options[answer - 1]
        ) {

            return options[
                answer - 1
            ].id;
        }
    }

    if (
        typeof answer === "string"
    ) {

        const normalized =
            answer.trim();

        const direct =
            options.find(
                option =>
                    String(
                        option.id
                    ).toLowerCase() ===
                    normalized.toLowerCase()
            );

        if (direct) {
            return direct.id;
        }

        const index =
            Number(normalized);

        if (
            !Number.isNaN(index)
        ) {

            if (
                options[index]
            ) {

                return options[
                    index
                ].id;
            }

            if (
                options[index - 1]
            ) {

                return options[
                    index - 1
                ].id;
            }
        }

        const byText =
            options.find(
                option =>
                    String(
                        option.text
                    ).trim() ===
                    normalized
            );

        if (byText) {
            return byText.id;
        }
    }

    return "";
}


/* =========================================================
   RENDER LESSON
   ========================================================= */

function renderLesson(
    data
) {

    const container =
        getElement(
            "lessonContent"
        );

    if (!container) {
        return;
    }

    const lesson =
        extractLesson(
            data
        );

    const title =
        getTitle(
            lesson,
            "درس آموزشی"
        );

    const content =
        getLessonText(
            lesson
        );

    const example =
        getLessonExample(
            lesson
        );

    const specialNotes =
        normalizeNotes(
            getLessonSpecialNotes(
                lesson
            )
        );

    const examTips =
        normalizeNotes(
            getLessonExamTips(
                lesson
            )
        );

    const questions =
        extractQuestions(
            lesson
        );

    let html = `
        <h1 class="lesson-title">
            ${escapeHtml(title)}
        </h1>
    `;


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    if (content) {

        html += `
            <section class="lesson-section">

                <h3>
                    📖 محتوای درس
                </h3>

                <div class="lesson-text">
                    ${formatText(content)}
                </div>

            </section>
        `;
    }


    /* =====================================================
       EXAMPLE
       ===================================================== */

    if (example) {

        html += `
            <section class="lesson-section">

                <h3>
                    💡 مثال کاربردی
                </h3>

                <div class="lesson-text">
                    ${formatText(example)}
                </div>

            </section>
        `;
    }


    /* =====================================================
       SPECIALIZED NOTES
       ===================================================== */

    if (specialNotes.length) {

        html += `
            <section class="lesson-section">

                <h3>
                    🎓 نکات تخصصی
                </h3>

                <ul class="notes-list">

                    ${specialNotes
                        .map(
                            note => `
                                <li>
                                    ${formatText(
                                        note
                                    )}
                                </li>
                            `
                        )
                        .join("")
                    }

                </ul>

            </section>
        `;
    }


    /* =====================================================
       EXAM TIPS
       ===================================================== */

    if (examTips.length) {

        html += `
            <section class="lesson-section">

                <h3>
                    🎯 نکات آزمونی
                </h3>

                <ul class="notes-list">

                    ${examTips
                        .map(
                            tip => `
                                <li>
                                    ${formatText(
                                        tip
                                    )}
                                </li>
                            `
                        )
                        .join("")
                    }

                </ul>

            </section>
        `;
    }


    /* =====================================================
       QUIZ
       ===================================================== */

    if (questions.length) {

        html += `
            <section
                class="lesson-section"
                id="quizSection"
            >

                <h3>
                    📝 آزمون درس
                </h3>

                <div id="quizContainer">

                    ${renderQuizQuestions(
                        questions
                    )}

                    <button
                        type="button"
                        class="btn btn-primary"
                        style="
                            margin-top:25px;
                            border:none;
                            cursor:pointer;
                        "
                        onclick="submitQuiz()"
                    >
                        بررسی پاسخ‌ها
                    </button>

                    <div
                        id="quizResult"
                        style="
                            margin-top:20px;
                        "
                    ></div>

                </div>

            </section>
        `;

    } else {

        html += `
            <section class="lesson-section">

                <div class="error-box">
                    آزمون این درس هنوز ثبت نشده است.
                </div>

            </section>
        `;
    }

    container.innerHTML =
        html;
}


/* =========================================================
   RENDER QUIZ QUESTIONS
   ========================================================= */

function renderQuizQuestions(
    questions
) {

    return questions
        .map(
            (
                question,
                questionIndex
            ) => {

                const options =
                    normalizeOptions(
                        question
                    );

                const correctAnswer =
                    getCorrectAnswer(
                        question,
                        options
                    );

                const explanation =
                    question.explanation ||
                    question.explain ||
                    "";

                return `
                    <div
                        class="question-card"
                        data-question-index="${questionIndex}"
                        data-correct-answer="${escapeHtml(
                            correctAnswer
                        )}"
                        data-explanation="${escapeHtml(
                            explanation
                        )}"
                    >

                        <div
                            class="question-title"
                        >
                            ${questionIndex + 1}.
                            ${escapeHtml(
                                question.question ||
                                question.text ||
                                question.title ||
                                "سؤال"
                            )}
                        </div>

                        ${options
                            .map(
                                (
                                    option,
                                    optionIndex
                                ) => {

                                    const optionId =
                                        String(
                                            option.id ||
                                            String.fromCharCode(
                                                65 +
                                                optionIndex
                                            )
                                        );

                                    return `
                                        <label
                                            class="question-option"
                                            style="
                                                display:block;
                                                cursor:pointer;
                                            "
                                        >

                                            <input
                                                type="radio"
                                                name="question_${questionIndex}"
                                                value="${escapeHtml(
                                                    optionId
                                                )}"
                                                style="
                                                    margin-left:8px;
                                                "
                                            >

                                            <strong>
                                                ${escapeHtml(
                                                    optionId
                                                )}
                                            </strong>

                                            ${escapeHtml(
                                                option.text
                                            )}

                                        </label>
                                    `;
                                }
                            )
                            .join("")
                        }

                        <div
                            class="question-feedback"
                            style="
                                margin-top:12px;
                                display:none;
                            "
                        ></div>

                    </div>
                `;
            }
        )
        .join("");
}


/* =========================================================
   SUBMIT QUIZ
   ========================================================= */

function submitQuiz() {

    const container =
        getElement(
            "quizContainer"
        );

    const result =
        getElement(
            "quizResult"
        );

    if (
        !container ||
        !result
    ) {
        return;
    }

    const cards =
        Array.from(
            container.querySelectorAll(
                ".question-card"
            )
        );

    if (!cards.length) {
        return;
    }

    let correct = 0;
    let answered = 0;

    cards.forEach(
        card => {

            const index =
                card.dataset.questionIndex;

            const correctAnswer =
                card.dataset.correctAnswer;

            const selected =
                card.querySelector(
                    `input[name="question_${index}"]:checked`
                );

            const feedback =
                card.querySelector(
                    ".question-feedback"
                );

            if (selected) {

                answered++;

                if (
                    String(
                        selected.value
                    ).toLowerCase() ===
                    String(
                        correctAnswer
                    ).toLowerCase()
                ) {

                    correct++;

                    if (feedback) {

                        feedback.style.display =
                            "block";

                        feedback.innerHTML =
                            `
                                <div
                                    style="
                                        color:#168b66;
                                        font-weight:600;
                                    "
                                >
                                    ✓ پاسخ صحیح
                                </div>
                            `;
                    }

                } else {

                    if (feedback) {

                        feedback.style.display =
                            "block";

                        const explanation =
                            card.dataset.explanation;

                        feedback.innerHTML =
                            `
                                <div
                                    style="
                                        color:#b33;
                                        font-weight:600;
                                    "
                                >
                                    ✕ پاسخ نادرست
                                </div>

                                ${
                                    explanation
                                        ? `
                                            <div
                                                style="
                                                    margin-top:6px;
                                                    color:#687583;
                                                "
                                            >
                                                ${escapeHtml(
                                                    explanation
                                                )}
                                            </div>
                                        `
                                        : ""
                                }
                            `;
                    }
                }

            } else {

                if (feedback) {

                    feedback.style.display =
                        "block";

                    feedback.innerHTML =
                        `
                            <div
                                style="
                                    color:#a66;
                                    font-weight:600;
                                "
                            >
                                پاسخ داده نشده
                            </div>
                        `;
                }
            }
        }
    );

    const total =
        cards.length;

    const percentage =
        Math.round(
            (
                correct /
                total
            ) * 100
        );

    let message =
        "";

    if (percentage >= 80) {

        message =
            "عملکرد بسیار خوب 👏";

    } else if (
        percentage >= 60
    ) {

        message =
            "عملکرد قابل قبول 👍";

    } else {

        message =
            "نیاز به مرور بیشتر دارید 📚";
    }

    result.innerHTML = `
        <div
            style="
                background:#071a2f;
                color:white;
                border-radius:16px;
                padding:22px;
            "
        >

            <div
                style="
                    color:#16c7bd;
                    font-size:13px;
                    font-weight:700;
                "
            >
                نتیجه آزمون
            </div>

            <div
                style="
                    font-size:34px;
                    font-weight:800;
                    margin-top:5px;
                "
            >
                ${correct} از ${total}
            </div>

            <div
                style="
                    color:#c4d0da;
                    margin-top:5px;
                "
            >
                درصد: ${percentage}٪
            </div>

            <div
                style="
                    margin-top:12px;
                "
            >
                ${message}
            </div>

            ${
                answered < total
                    ? `
                        <div
                            style="
                                margin-top:8px;
                                color:#d8c28a;
                                font-size:12px;
                            "
                        >
                            ${total - answered}
                            سؤال بدون پاسخ باقی مانده است.
                        </div>
                    `
                    : ""
            }

        </div>
    `;

    result.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


/* =========================================================
   BACK NAVIGATION
   ========================================================= */

function goBackToModule() {

    if (
        currentModuleId
    ) {

        showModule(
            currentModuleId
        );

    } else {

        showHome();
    }
}


function goBackToChapter() {

    if (
        currentModuleId &&
        currentChapterId
    ) {

        showChapter(
            currentChapterId
        );

    } else {

        showHome();
    }
}


/* =========================================================
   INITIAL ROUTING
   ========================================================= */

async function initializePage() {

    console.log(
        "[Andishkadeh] Initializing website..."
    );

    const state =
        readUrlState();

    if (
        state.moduleId &&
        state.chapterId &&
        state.lessonId
    ) {

        currentModuleId =
            state.moduleId;

        currentChapterId =
            state.chapterId;

        await showLesson(
            state.lessonId,
            false
        );

        return;
    }

    if (
        state.moduleId &&
        state.chapterId
    ) {

        currentModuleId =
            state.moduleId;

        await showChapter(
            state.chapterId,
            false
        );

        return;
    }

    if (
        state.moduleId
    ) {

        await showModule(
            state.moduleId,
            false
        );

        return;
    }

    showHome(
        false
    );

    await loadModules();
}


/* =========================================================
   BROWSER BACK / FORWARD
   ========================================================= */

window.addEventListener(
    "popstate",
    async () => {

        const state =
            readUrlState();

        if (
            state.moduleId &&
            state.chapterId &&
            state.lessonId
        ) {

            currentModuleId =
                state.moduleId;

            currentChapterId =
                state.chapterId;

            await showLesson(
                state.lessonId,
                false
            );

            return;
        }

        if (
            state.moduleId &&
            state.chapterId
        ) {

            currentModuleId =
                state.moduleId;

            await showChapter(
                state.chapterId,
                false
            );

            return;
        }

        if (
            state.moduleId
        ) {

            await showModule(
                state.moduleId,
                false
            );

            return;
        }

        showHome(
            false
        );

        await loadModules();
    }
);


/* =========================================================
   HEADER BRAND
   ========================================================= */

document.addEventListener(
    "click",
    event => {

        const brand =
            event.target.closest(
                ".brand"
            );

        if (!brand) {
            return;
        }

        event.preventDefault();

        showHome();
    }
);


/* =========================================================
   CLOSE MOBILE MENU ON OUTSIDE CLICK
   ========================================================= */

document.addEventListener(
    "click",
    event => {

        const menu =
            getElement(
                "mobileMenu"
            );

        const button =
            event.target.closest(
                ".mobile-menu-btn"
            );

        if (
            !menu ||
            button
        ) {
            return;
        }

        if (
            !menu.contains(
                event.target
            )
        ) {

            closeMobileMenu();
        }
    }
);


/* =========================================================
   ESC KEY
   ========================================================= */

document.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Escape"
        ) {

            closeMobileMenu();
        }
    }
);


/* =========================================================
   GLOBAL EXPORTS
   ========================================================= */

window.apiFetch =
    apiFetch;

window.getApiInfo =
    getApiInfo;

window.getModules =
    getModules;

window.getModule =
    getModule;

window.getModuleChapters =
    getModuleChapters;

window.getChapter =
    getChapter;

window.getChapterLessons =
    getChapterLessons;

window.getLesson =
    getLesson;

window.searchContent =
    searchContent;

window.showHome =
    showHome;

window.showModule =
    showModule;

window.showChapter =
    showChapter;

window.showLesson =
    showLesson;

window.goBackToModule =
    goBackToModule;

window.goBackToChapter =
    goBackToChapter;

window.toggleMobileMenu =
    toggleMobileMenu;

window.closeMobileMenu =
    closeMobileMenu;

window.submitQuiz =
    submitQuiz;


/* =========================================================
   START APPLICATION
   ========================================================= */

if (
    document.readyState === "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        initializePage
    );

} else {

    initializePage();
}
