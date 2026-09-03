/* =========================================================
   ANDISHKADEH
   MODULES PAGE
========================================================= */
/* =========================================================
   MODULE ICONS
========================================================= */
const MODULE_ICONS = {
    banking:
        "🏦",
    management:
        "📚",
    international_trade:
        "🌍",
    marketing_sales:
        "📈",
    economics_market:
        "💰",
    employment_exam:
        "📝",
    psychology_social_work:
        "🧠",
    finance:
        "💳",
    accounting:
        "🧮",
    general:
        "📘",
    default:
        "📘"
};
/* =========================================================
   DOM ELEMENTS
========================================================= */
const modulesContainer =
    document.getElementById(
        "modulesContainer"
    );
const loadingElement =
    document.getElementById(
        "loading"
    );
const errorElement =
    document.getElementById(
        "error"
    );
const errorDetailsElement =
    document.getElementById(
        "errorDetails"
    );
const emptyElement =
    document.getElementById(
        "empty"
    );
const retryButton =
    document.getElementById(
        "retryButton"
    );
const moduleCountElement =
    document.getElementById(
        "moduleCount"
    );
const chapterCountElement =
    document.getElementById(
        "chapterCount"
    );
const lessonCountElement =
    document.getElementById(
        "lessonCount"
    );
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
   GET MODULE ICON
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
    const title =
        String(
            module?.title || ""
        )
        .trim();
    if (
        MODULE_ICONS[id]
    ) {
        return MODULE_ICONS[id];
    }
    /*
     * fallback بر اساس عنوان
     */
    const titleLower =
        title.toLowerCase();
    if (
        title.includes("بانک") ||
        titleLower.includes("bank")
    ) {
        return "🏦";
    }
    if (
        title.includes("مدیریت") ||
        titleLower.includes("management")
    ) {
        return "📚";
    }
    if (
        title.includes("تجارت") ||
        titleLower.includes("trade")
    ) {
        return "🌍";
    }
    if (
        title.includes("بازاریابی") ||
        title.includes("فروش") ||
        titleLower.includes("marketing")
    ) {
        return "📈";
    }
    if (
        title.includes("اقتصاد") ||
        titleLower.includes("econom")
    ) {
        return "💰";
    }
    if (
        title.includes("آزمون") ||
        title.includes("استخدام")
    ) {
        return "📝";
    }
    if (
        title.includes("روانشناسی") ||
        title.includes("مددکاری")
    ) {
        return "🧠";
    }
    return MODULE_ICONS.default;
}
/* =========================================================
   NORMALIZE MODULE DATA
========================================================= */
function normalizeModulesResponse(
    data
) {
    /*
     * حالت معمول:
     *
     * {
     *     "modules": [...]
     * }
     */
    if (
        data &&
        Array.isArray(data.modules)
    ) {
        return data.modules;
    }
    /*
     * بعضی APIها مستقیماً آرایه برمی‌گردانند.
     */
    if (
        Array.isArray(data)
    ) {
        return data;
    }
    /*
     * حالت احتمالی:
     *
     * {
     *     "data": {
     *         "modules": [...]
     *     }
     * }
     */
    if (
        data &&
        data.data &&
        Array.isArray(data.data.modules)
    ) {
        return data.data.modules;
    }
    return [];
}
/* =========================================================
   GET NUMBER
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
   CALCULATE STATISTICS
========================================================= */
function calculateStats(
    modules,
    apiData
) {
    let chapters = 0;
    let lessons = 0;
    modules.forEach(
        module => {
            chapters +=
                getNumber(
                    module.chapter_count
                );
            lessons +=
                getNumber(
                    module.lesson_count
                );
        }
    );
    /*
     * اگر API آمار کلی را خودش داده باشد،
     * در صورت وجود از آن استفاده می‌کنیم.
     */
    if (
        apiData &&
        apiData.chapter_count !== undefined
    ) {
        chapters =
            getNumber(
                apiData.chapter_count
            );
    }
    if (
        apiData &&
        apiData.lesson_count !== undefined
    ) {
        lessons =
            getNumber(
                apiData.lesson_count
            );
    }
    return {
        modules:
            modules.length,
        chapters,
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
        moduleCountElement
    ) {
        moduleCountElement.textContent =
            stats.modules;
    }
    if (
        chapterCountElement
    ) {
        chapterCountElement.textContent =
            stats.chapters;
    }
    if (
        lessonCountElement
    ) {
        lessonCountElement.textContent =
            stats.lessons;
    }
}
/* =========================================================
   SHOW LOADING
========================================================= */
function showLoading() {
    if (
        loadingElement
    ) {
        loadingElement.style.display =
            "block";
    }
    if (
        errorElement
    ) {
        errorElement.style.display =
            "none";
    }
    if (
        emptyElement
    ) {
        emptyElement.style.display =
            "none";
    }
    if (
        modulesContainer
    ) {
        modulesContainer.style.display =
            "none";
    }
}
/* =========================================================
   SHOW ERROR
========================================================= */
function showModulesError(
    error
) {
    if (
        loadingElement
    ) {
        loadingElement.style.display =
            "none";
    }
    if (
        emptyElement
    ) {
        emptyElement.style.display =
            "none";
    }
    if (
        modulesContainer
    ) {
        modulesContainer.style.display =
            "none";
    }
    if (
        errorElement
    ) {
        errorElement.style.display =
            "block";
    }
    if (
        errorDetailsElement
    ) {
        errorDetailsElement.textContent =
            error?.message ||
            "Unknown error";
    }
}
/* =========================================================
   SHOW EMPTY
========================================================= */
function showEmpty() {
    if (
        loadingElement
    ) {
        loadingElement.style.display =
            "none";
    }
    if (
        errorElement
    ) {
        errorElement.style.display =
            "none";
    }
    if (
        modulesContainer
    ) {
        modulesContainer.style.display =
            "none";
    }
    if (
        emptyElement
    ) {
        emptyElement.style.display =
            "block";
    }
}
/* =========================================================
   CREATE MODULE CARD
========================================================= */
function createModuleCard(
    module
) {
    if (
        !module
    ) {
        return "";
    }
    const moduleId =
        String(
            module.id || ""
        ).trim();
    if (
        !moduleId
    ) {
        return "";
    }
    const title =
        escapeHtml(
            module.title ||
            "ماژول آموزشی"
        );
    const description =
        escapeHtml(
            module.description ||
            "مشاهده فصل‌ها و درس‌های آموزشی اندیشکده"
        );
    const chapterCount =
        getNumber(
            module.chapter_count
        );
    const lessonCount =
        getNumber(
            module.lesson_count
        );
    const icon =
        getModuleIcon(
            module
        );
    const chapterURL =
        `chapter.html?module=${encodeURIComponent(
            moduleId
        )}`;
    return `
        <a
            href="${chapterURL}"
            class="module-card"
            data-module="${escapeHtml(
                moduleId
            )}"
        >
            <div class="module-icon">
                ${icon}
            </div>
            <h2>
                ${title}
            </h2>
            <p>
                ${description}
            </p>
            <div class="module-meta">
                <span>
                    📖
                    ${chapterCount}
                    فصل
                </span>
                <span>
                    📝
                    ${lessonCount}
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
        !Array.isArray(modules)
    ) {
        throw new Error(
            "ساختار اطلاعات ماژول‌ها نامعتبر است."
        );
    }
    if (
        modules.length === 0
    ) {
        showEmpty();
        return;
    }
    const cards =
        modules
            .map(
                createModuleCard
            )
            .filter(
                Boolean
            )
            .join("");
    if (
        !cards
    ) {
        showEmpty();
        return;
    }
    modulesContainer.innerHTML =
        cards;
    modulesContainer.style.display =
        "grid";
    loadingElement.style.display =
        "none";
    errorElement.style.display =
        "none";
    emptyElement.style.display =
        "none";
}
/* =========================================================
   LOAD MODULES
========================================================= */
async function loadModules() {
    showLoading();
    try {
        const data =
            await getModules();
        console.log(
            "[Andishkadeh] API response:",
            data
        );
        const modules =
            normalizeModulesResponse(
                data
            );
        const stats =
            calculateStats(
                modules,
                data
            );
        renderStats(
            stats
        );
        renderModules(
            modules
        );
    } catch (error) {
        console.error(
            "[Andishkadeh] Failed to load modules:",
            error
        );
        showModulesError(
            error
        );
    }
}
/* =========================================================
   RETRY
========================================================= */
if (
    retryButton
) {
    retryButton.addEventListener(
        "click",
        () => {
            loadModules();
        }
    );
}
/* =========================================================
   PAGE LOAD
========================================================= */
document.addEventListener(
    "DOMContentLoaded",
    () => {
        loadModules();
    }
);
