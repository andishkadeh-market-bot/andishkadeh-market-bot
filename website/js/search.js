document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "searchForm"
            );


        if (!form) {

            return;

        }


        form.addEventListener(
            "submit",
            event => {

                event.preventDefault();

                runSearch();

            }
        );


        const query =
            getQueryParam("q");


        if (query) {

            const input =
                document.getElementById(
                    "searchInput"
                );

            if (input) {

                input.value =
                    query;

            }


            runSearch();

        }

    }
);


/* =========================================================
   RUN SEARCH
========================================================= */

async function runSearch() {

    const input =
        document.getElementById(
            "searchInput"
        );

    const summary =
        document.getElementById(
            "searchSummary"
        );

    const results =
        document.getElementById(
            "searchResults"
        );


    if (
        !input ||
        !summary ||
        !results
    ) {

        return;

    }


    const query =
        input.value
            .trim();


    if (query.length < 2) {

        summary.textContent =
            "حداقل دو حرف برای جست‌وجو وارد کنید.";

        results.innerHTML =
            "";

        return;

    }


    summary.textContent =
        "در حال جست‌وجو در محتوای اندیشکده...";


    results.innerHTML = `
        <div class="loading-card">
            🔎 در حال جست‌وجو...
        </div>
    `;


    try {

        const response =
            await searchContent(
                query
            );


        const matches =
            extractResults(
                response
            );


        summary.textContent =
            `${matches.length} نتیجه برای «${query}» پیدا شد.`;


        if (!matches.length) {

            results.innerHTML = `
                <div class="loading-card">
                    نتیجه‌ای برای جست‌وجوی شما پیدا نشد.
                </div>
            `;

            return;

        }


        results.innerHTML =
            matches
                .map(
                    createSearchResult
                )
                .join("");


    } catch (error) {

        console.error(
            "Search error:",
            error
        );


        summary.textContent =
            "خطا در جست‌وجو.";


        showError(
            results,
            "ارتباط با API برقرار نشد."
        );

    }

}


/* =========================================================
   EXTRACT SEARCH RESULTS
========================================================= */

function extractResults(
    response
) {

    if (
        !response
    ) {

        return [];

    }


    if (
        Array.isArray(
            response.results
        )
    ) {

        return response.results;

    }


    if (
        Array.isArray(
            response.lessons
        )
    ) {

        return response.lessons;

    }


    if (
        Array.isArray(
            response
        )
    ) {

        return response;

    }


    return [];

}


/* =========================================================
   CREATE SEARCH RESULT
========================================================= */

function createSearchResult(
    lesson
) {

    const moduleId =
        lesson.module_id ||
        lesson.moduleId ||
        "";


    const chapterId =
        lesson.chapter_id ||
        lesson.chapterId ||
        "";


    const lessonId =
        lesson.id ||
        lesson.lesson_id ||
        "";


    const title =
        lesson.title ||
        "درس آموزشی";


    const moduleTitle =
        lesson.moduleTitle ||
        lesson.module_title ||
        getModuleTitle(
            moduleId
        );


    const chapterTitle =
        lesson.chapterTitle ||
        lesson.chapter_title ||
        getChapterTitle(
            chapterId
        );


    const data =
        lesson.data ||
        {};


    const content =
        data.content ||
        lesson.content ||
        "";


    const preview =
        createPreview(
            content
        );


    return `
        <a
            class="lesson-item"
            href="lesson.html?module=${encodeURIComponent(moduleId)}&chapter=${encodeURIComponent(chapterId)}&lesson=${encodeURIComponent(lessonId)}"
        >

            <div class="lesson-item-info">

                <div class="lesson-number">
                    🔎
                </div>

                <div>

                    <h3>
                        ${escapeHtml(title)}
                    </h3>

                    <span class="meta-badge">
                        ${escapeHtml(moduleTitle)}
                    </span>

                    <span class="meta-badge">
                        ${escapeHtml(chapterTitle)}
                    </span>

                    ${
                        preview
                            ? `
                                <p class="search-preview">
                                    ${escapeHtml(preview)}
                                </p>
                            `
                            : ""
                    }

                </div>

            </div>

            <div class="lesson-arrow">
                ←
            </div>

        </a>
    `;

}


/* =========================================================
   CREATE CONTENT PREVIEW
========================================================= */

function createPreview(
    content
) {

    if (!content) {

        return "";

    }


    const text =
        String(content)
            .replace(/\s+/g, " ")
            .trim();


    if (
        text.length <= 180
    ) {

        return text;

    }


    return (
        text.substring(
            0,
            180
        ) +
        "..."
    );

}


/* =========================================================
   MODULE TITLE
========================================================= */

function getModuleTitle(
    moduleId
) {

    const titles = {

        management:
            "📚 آموزش مدیریت",

        banking:
            "🏦 بانکداری تخصصی",

        international_trade:
            "🌍 تجارت بین‌الملل",

        psychology_socialwork:
            "🧠 روانشناسی و مددکاری",

        finance:
            "💰 مالی و اقتصاد",

        general_exam:
            "📝 آزمون استخدامی"

    };


    return (
        titles[moduleId] ||
        moduleId ||
        "اندیشکده مدیریت و بازار"
    );

}


/* =========================================================
   CHAPTER TITLE
========================================================= */

function getChapterTitle(
    chapterId
) {

    const titles = {

        banking_fundamentals:
            "مبانی و مفاهیم بانکداری",

        banking_deposits:
            "سپرده‌های بانکی",

        banking_islamic_contracts:
            "عقود و قراردادهای بانکی",

        banking_facilities:
            "تسهیلات بانکی",

        banking_risk:
            "ریسک در بانکداری",

        central_bank_monetary_policy:
            "بانک مرکزی و سیاست پولی",

        aml_cft:
            "مبارزه با پولشویی و تأمین مالی تروریسم",

        international_banking:
            "بانکداری بین‌الملل",

        digital_banking:
            "بانکداری دیجیتال",

        bank_financial_statements:
            "صورت‌های مالی بانک",

        bank_management:
            "مدیریت بانک",

        banking_employment_exam:
            "آزمون استخدامی بانکداری"

    };


    return (
        titles[chapterId] ||
        chapterId ||
        "فصل آموزشی"
    );

}
