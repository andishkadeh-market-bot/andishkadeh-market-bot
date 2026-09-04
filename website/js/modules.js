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
        title.includes(
            "مدیریت"
        )
    ) {

        return "📚";

    }

    if (
        title.includes(
            "بانک"
        )
    ) {

        return "🏦";

    }

    if (
        title.includes(
            "تجارت"
        )
    ) {

        return "🌍";

    }

    if (
        title.includes(
            "روان"
        ) ||
        title.includes(
            "مددکار"
        )
    ) {

        return "🧠";

    }

    if (
        title.includes(
            "مالی"
        )
    ) {

        return "💰";

    }

    if (
        title.includes(
            "آزمون"
        )
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

    return [];

}

/* =========================================================
   CALCULATE STATISTICS
   ========================================================= */

function calculateStats(
    modules
) {

    let chapters = 0;
    let lessons = 0;

    for (
        const module of modules
    ) {

        chapters +=
            getNumber(
                module?.chapter_count ??
                module?.chapters_count ??
                module?.chapters ??
                0
            );

        lessons +=
            getNumber(
                module?.lesson_count ??
                module?.lessons_count ??
                module?.lessons ??
                0
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
        String(
            module?.id || ""
        );

    const title =
        escapeHtml(
            module?.title ||
            "ماژول آموزشی"
        );

    const description =
        escapeHtml(
            module?.description ||
            "محتوای تخصصی و کاربردی اندیشکده مدیریت و بازار."
        );

    const chapters =
        getNumber(
            module?.chapter_count ??
            module?.chapters_count ??
            module?.chapters ??
            0
        );

    const lessons =
        getNumber(
            module?.lesson_count ??
            module?.lessons_count ??
            module?.lessons ??
            0
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

        const data =
            await getModules();

        console.log(
            "[Modules] API data:",
            data
        );

        const modules =
            normalizeModulesResponse(
                data
            );

        console.log(
            "[Modules] Modules:",
            modules
        );

        const stats =
            calculateStats(
                modules
            );

        renderStats(
            stats
        );

        if (
            !modules.length
        ) {

            showEmpty();

            return;

        }

        renderModules(
            modules
        );

        console.log(
            `[Modules] ${modules.length} modules rendered successfully.`
        );

    } catch (error) {

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
