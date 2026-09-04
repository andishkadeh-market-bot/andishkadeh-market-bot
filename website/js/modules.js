/* =========================================================
   ANDISHKADEH MANAGEMENT & MARKET
   MODULES PAGE
   ========================================================= */
"use strict";
/* =========================================================
   MODULE ICONS
========================================================= */
const MODULE_ICONS = {
    management:
        "📚",
    banking:
        "🏦",
    international_trade:
        "🌍",
    psychology_socialwork:
        "🧠",
    finance:
        "💰",
    general_exam:
        "📝"
};
/* =========================================================
   DOM ELEMENTS
========================================================= */
let modulesContainer;
let loadingBox;
let errorBox;
let errorDetails;
let emptyBox;
let retryButton;
let moduleCount;
let chapterCount;
let lessonCount;
/* =========================================================
   INITIALIZE DOM
========================================================= */
function initializeElements() {
    modulesContainer =
        document.getElementById(
            "modulesContainer"
        );
    loadingBox =
        document.getElementById(
            "loading"
        );
    errorBox =
        document.getElementById(
            "error"
        );
    errorDetails =
        document.getElementById(
            "errorDetails"
        );
    emptyBox =
        document.getElementById(
            "empty"
        );
    retryButton =
        document.getElementById(
            "retryButton"
        );
    moduleCount =
        document.getElementById(
            "moduleCount"
        );
    chapterCount =
        document.getElementById(
            "chapterCount"
        );
    lessonCount =
        document.getElementById(
            "lessonCount"
        );
}
/* =========================================================
   ESCAPE HTML
========================================================= */
function escapeHtml(value) {
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
/* =========================================================
   MODULE ICON
========================================================= */
function getModuleIcon(
    module
) {
    const id =
        String(
            module?.id || ""
        )
            .trim()
            .toLowerCase();
    if (
        MODULE_ICONS[id]
    ) {
        return MODULE_ICONS[id];
    }
    const title =
        String(
            module?.title || ""
        );
    if (
        title.includes("مدیریت")
    ) {
        return "📚";
    }
    if (
        title.includes("بانک")
    ) {
        return "🏦";
    }
    if (
        title.includes("تجارت")
    ) {
        return "🌍";
    }
    if (
        title.includes("روان") ||
        title.includes("مددکار")
    ) {
        return "🧠";
    }
    if (
        title.includes("مالی")
    ) {
        return "💰";
    }
    if (
        title.includes("آزمون")
    ) {
        return "📝";
    }
    return "📘";
}
/* =========================================================
   NUMBER NORMALIZER
========================================================= */
function getNumber(
    value
) {
    if (
        typeof value === "number" &&
        Number.isFinite(value)
    ) {
        return value;
    }
    if (
        typeof value === "string"
    ) {
        const normalized =
            value
                .replace(
                    /[۰-۹]/g,
                    digit =>
                        String(
                            "۰۱۲۳۴۵۶۷۸۹"
                                .indexOf(digit)
                        )
                )
                .replace(
                    /,/g,
                    ""
                )
                .trim();
        const number =
            Number(
                normalized
            );
        if (
            Number.isFinite(number)
        ) {
            return number;
        }
    }
    const number =
        Number(value);
    if (
        Number.isFinite(number)
    ) {
        return number;
    }
    return 0;
}
/* =========================================================
   NORMALIZE MODULE RESPONSE
========================================================= */
function normalizeModulesResponse(
    data
) {
    /*
       Supported formats:
       1)
       {
           count: 6,
           modules: [...]
       }
       2)
       [...]
       3)
       {
           data: {
               modules: [...]
           }
       }
       4)
       {
           data: [...]
       }
    */
    if (
        Array.isArray(data)
    ) {
        return data;
    }
    if (
        data &&
        Array.isArray(
            data.modules
        )
    ) {
        return data.modules;
    }
    if (
        data &&
        data.data &&
        Array.isArray(
            data.data.modules
        )
    ) {
        return data.data.modules;
    }
    if (
        data &&
        Array.isArray(
            data.data
        )
    ) {
        return data.data;
    }
    return [];
}
/* =========================================================
   NORMALIZE CHAPTER RESPONSE
========================================================= */
function normalizeChaptersResponse(
    data
) {
    if (
        Array.isArray(data)
    ) {
        return data;
    }
    if (
        data &&
        Array.isArray(
            data.chapters
        )
    ) {
        return data.chapters;
    }
    if (
        data &&
        data.data &&
        Array.isArray(
            data.data.chapters
        )
    ) {
        return data.data.chapters;
    }
    if (
        data &&
        Array.isArray(
            data.data
        )
    ) {
        return data.data;
    }
    return [];
}
/* =========================================================
   NORMALIZE LESSON RESPONSE
========================================================= */
function normalizeLessonsResponse(
    data
) {
    if (
        Array.isArray(data)
    ) {
        return data;
    }
    if (
        data &&
        Array.isArray(
            data.lessons
        )
    ) {
        return data.lessons;
    }
    if (
        data &&
        data.data &&
        Array.isArray(
            data.data.lessons
        )
    ) {
        return data.data.lessons;
    }
    if (
        data &&
        Array.isArray(
            data.data
        )
    ) {
        return data.data;
    }
    return [];
}
/* =========================================================
   GET MODULE ID
========================================================= */
function getModuleId(
    module
) {
    return String(
        module?.id ||
        module?.module_id ||
        ""
    ).trim();
}
/* =========================================================
   GET MODULE CHAPTER COUNT
========================================================= */
function getModuleChapterCount(
    module
) {
    return getNumber(
        module?.chapter_count ??
        module?.chapters_count ??
        (
            Array.isArray(
                module?.chapters
            )
                ? module.chapters.length
                : null
        )
    );
}
/* =========================================================
   GET MODULE LESSON COUNT
========================================================= */
function getModuleLessonCount(
    module
) {
    return getNumber(
        module?.lesson_count ??
        module?.lessons_count ??
        (
            Array.isArray(
                module?.lessons
            )
                ? module.lessons.length
                : null
        )
    );
}
/* =========================================================
   LOAD MODULE DETAILS
========================================================= */
async function enrichModule(
    module
) {
    const moduleId =
        getModuleId(
            module
        );
    if (
        !moduleId
    ) {
        return {
            ...module,
            _chapterCount: 0,
            _lessonCount: 0
        };
    }
    let chapters =
        [];
    let chapterCountFromModule =
        getModuleChapterCount(
            module
        );
    let lessonCountFromModule =
        getModuleLessonCount(
            module
        );
    /*
       If chapter count and lesson count already exist,
       keep the API metadata and avoid unnecessary requests.
    */
    const needsChapters =
        chapterCountFromModule === 0;
    const needsLessons =
        lessonCountFromModule === 0;
    if (
        needsChapters ||
        needsLessons
    ) {
        try {
            if (
                typeof getModuleChapters ===
                "function"
            ) {
                const chapterData =
                    await getModuleChapters(
                        moduleId
                    );
                chapters =
                    normalizeChaptersResponse(
                        chapterData
                    );
            }
        } catch (
            chapterError
        ) {
            console.warn(
                `[Modules] Failed to load chapters for ${moduleId}:`,
                chapterError
            );
        }
    }
    if (
        chapterCountFromModule === 0 &&
        chapters.length > 0
    ) {
        chapterCountFromModule =
            chapters.length;
    }
    /*
       Calculate lessons only when the module itself
       does not already provide the total.
    */
    if (
        needsLessons &&
        chapters.length > 0 &&
        typeof getChapterLessons ===
        "function"
    ) {
        let totalLessons =
            0;
        /*
           Load lesson lists sequentially.
           This is slightly slower but kinder to a free
           Render instance and avoids a burst of requests.
        */
        for (
            const chapter of chapters
        ) {
            const chapterId =
                String(
                    chapter?.id ||
                    chapter?.chapter_id ||
                    ""
                ).trim();
            if (
                !chapterId
            ) {
                continue;
            }
            try {
                const lessonData =
                    await getChapterLessons(
                        moduleId,
                        chapterId
                    );
                const lessons =
                    normalizeLessonsResponse(
                        lessonData
                    );
                totalLessons +=
                    lessons.length;
            } catch (
                lessonError
            ) {
                console.warn(
                    `[Modules] Failed to load lessons for ${moduleId}/${chapterId}:`,
                    lessonError
                );
            }
        }
        if (
            totalLessons > 0
        ) {
            lessonCountFromModule =
                totalLessons;
        }
    }
    return {
        ...module,
        _chapterCount:
            chapterCountFromModule,
        _lessonCount:
            lessonCountFromModule
    };
}
/* =========================================================
   CALCULATE STATISTICS
========================================================= */
function calculateStats(
    modules
) {
    let chapters =
        0;
    let lessons =
        0;
    for (
        const module of modules
    ) {
        chapters +=
            getNumber(
                module?._chapterCount
            );
        lessons +=
            getNumber(
                module?._lessonCount
            );
    }
    return {
        modules:
            modules.length,
        chapters:
            chapters,
        lessons:
            lessons
    };
}
/* =========================================================
   RENDER STATISTICS
========================================================= */
function renderStats(
    stats
) {
    if (
        moduleCount
    ) {
        moduleCount.textContent =
            stats.modules.toLocaleString(
                "fa-IR"
            );
    }
    if (
        chapterCount
    ) {
        chapterCount.textContent =
            stats.chapters.toLocaleString(
                "fa-IR"
            );
    }
    if (
        lessonCount
    ) {
        lessonCount.textContent =
            stats.lessons.toLocaleString(
                "fa-IR"
            );
    }
}
/* =========================================================
   SHOW LOADING
========================================================= */
function showLoading() {
    if (
        loadingBox
    ) {
        loadingBox.hidden =
            false;
    }
    if (
        errorBox
    ) {
        errorBox.hidden =
            true;
    }
    if (
        emptyBox
    ) {
        emptyBox.hidden =
            true;
    }
    if (
        modulesContainer
    ) {
        modulesContainer.innerHTML =
            "";
    }
}
/* =========================================================
   SHOW ERROR
========================================================= */
function showModulesError(
    error
) {
    if (
        loadingBox
    ) {
        loadingBox.hidden =
            true;
    }
    if (
        emptyBox
    ) {
        emptyBox.hidden =
            true;
    }
    if (
        modulesContainer
    ) {
        modulesContainer.innerHTML =
            "";
    }
    if (
        errorBox
    ) {
        errorBox.hidden =
            false;
    }
    if (
        errorDetails
    ) {
        errorDetails.textContent =
            error?.message ||
            "خطای نامشخص در دریافت اطلاعات.";
    }
}
/* =========================================================
   SHOW EMPTY
========================================================= */
function showEmpty() {
    if (
        loadingBox
    ) {
        loadingBox.hidden =
            true;
    }
    if (
        errorBox
    ) {
        errorBox.hidden =
            true;
    }
    if (
        emptyBox
    ) {
        emptyBox.hidden =
            false;
    }
    if (
        modulesContainer
    ) {
        modulesContainer.innerHTML =
            "";
    }
}
/* =========================================================
   CREATE MODULE CARD
========================================================= */
function createModuleCard(
    module
) {
    const moduleId =
        escapeHtml(
            getModuleId(
                module
            )
        );
    const title =
        escapeHtml(
            module?.title ||
            module?.name ||
            "ماژول آموزشی"
        );
    const description =
        escapeHtml(
            module?.description ||
            module?.summary ||
            "محتوای تخصصی و کاربردی اندیشکده مدیریت و بازار."
        );
    const chapters =
        getNumber(
            module?._chapterCount
        );
    const lessons =
        getNumber(
            module?._lessonCount
        );
    const icon =
        getModuleIcon(
            module
        );
    return `
        <a
            class="module-card"
            href="chapter.html?module=${encodeURIComponent(
                moduleId
            )}"
            aria-label="${title}"
        >
            <div class="module-icon">
                ${icon}
            </div>
            <h3>
                ${title}
            </h3>
            <p>
                ${description}
            </p>
            <div class="module-meta">
                <span class="meta-badge">
                    ${chapters.toLocaleString("fa-IR")}
                    فصل
                </span>
                <span class="meta-badge">
                    ${lessons.toLocaleString("fa-IR")}
                    درس
                </span>
            </div>
        </a>
    `;
}
/* =========================================================
   RENDER MODULES
========================================================= */
function renderModules(
    modules
) {
    if (
        !modulesContainer
    ) {
        throw new Error(
            "عنصر modulesContainer در صفحه پیدا نشد."
        );
    }
    modulesContainer.innerHTML =
        modules
            .map(
                createModuleCard
            )
            .join("");
    if (
        loadingBox
    ) {
        loadingBox.hidden =
            true;
    }
    if (
        errorBox
    ) {
        errorBox.hidden =
            true;
    }
    if (
        emptyBox
    ) {
        emptyBox.hidden =
            true;
    }
}
/* =========================================================
   LOAD MODULES
========================================================= */
async function loadModules() {
    console.log(
        "[Modules] Loading modules..."
    );
    showLoading();
    try {
        if (
            typeof getModules !==
            "function"
        ) {
            throw new Error(
                "تابع getModules در api.js پیدا نشد."
            );
        }
        const data =
            await getModules();
        console.log(
            "[Modules] API data:",
            data
        );
        const rawModules =
            normalizeModulesResponse(
                data
            );
        console.log(
            "[Modules] Raw modules:",
            rawModules
        );
        if (
            !rawModules.length
        ) {
            renderStats({
                modules:
                    0,
                chapters:
                    0,
                lessons:
                    0
            });
            showEmpty();
            return;
        }
        /*
           Enrich every module with real chapter/lesson
           counts when the /api/modules response does not
           already contain them.
        */
        const modules =
            await Promise.all(
                rawModules.map(
                    enrichModule
                )
            );
        console.log(
            "[Modules] Enriched modules:",
            modules
        );
        const stats =
            calculateStats(
                modules
            );
        renderStats(
            stats
        );
        renderModules(
            modules
        );
        console.log(
            `[Modules] ${modules.length} modules rendered successfully.`
        );
        console.log(
            `[Modules] Statistics: ${stats.modules} modules, ${stats.chapters} chapters, ${stats.lessons} lessons.`
        );
    } catch (
        error
    ) {
        console.error(
            "[Modules] Loading failed:",
            error
        );
        showModulesError(
            error
        );
    }
}
/* =========================================================
   RETRY BUTTON
========================================================= */
function initializeRetry() {
    if (
        !retryButton
    ) {
        return;
    }
    retryButton.addEventListener(
        "click",
        () => {
            loadModules();
        }
    );
}
/* =========================================================
   DOM READY
========================================================= */
document.addEventListener(
    "DOMContentLoaded",
    () => {
        initializeElements();
        initializeRetry();
        loadModules();
    }
);
