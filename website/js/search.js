let allLessons = [];


document.addEventListener(
    "DOMContentLoaded",
    async () => {

        const form =
            document.getElementById(
                "searchForm"
            );


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

            document.getElementById(
                "searchInput"
            ).value = query;

            await runSearch();

        }

    }
);


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


    const query =
        input.value
            .trim()
            .toLowerCase();


    if (query.length < 2) {

        summary.textContent =
            "حداقل دو حرف برای جست‌وجو وارد کنید.";

        results.innerHTML =
            "";

        return;

    }


    summary.textContent =
        "در حال جست‌وجو در محتوای اندیشکده...";


    results.innerHTML =
        `
            <div class="loading-card">
                در حال دریافت اطلاعات...
            </div>
        `;


    try {

        if (!allLessons.length) {

            allLessons =
                await getAllLessons();

        }


        const matches =
            allLessons.filter(
                lesson => {

                    const title =
                        String(
                            lesson.title || ""
                        ).toLowerCase();


                    const data =
                        lesson.data || {};


                    const content =
                        String(
                            data.content || ""
                        ).toLowerCase();


                    return (
                        title.includes(query) ||
                        content.includes(query)
                    );

                }
            );


        summary.textContent =
            `${matches.length} نتیجه برای «${query}» پیدا شد.`;


        if (!matches.length) {

            results.innerHTML =
                `
                    <div class="loading-card">
                        نتیجه‌ای پیدا نشد.
                    </div>
                `;

            return;

        }


        results.innerHTML =
            matches
                .map(createSearchResult)
                .join("");


    } catch (error) {

        console.error(error);


        summary.textContent =
            "خطا در جست‌وجو.";


        showError(
            results,
            "ارتباط با API برقرار نشد."
        );

    }

}


function createSearchResult(
    lesson
) {

    return `
        <a
            class="lesson-item"
            href="lesson.html?module=${encodeURIComponent(lesson.module_id)}&chapter=${encodeURIComponent(lesson.chapter_id)}&lesson=${encodeURIComponent(lesson.id)}"
        >

            <div class="lesson-item-info">

                <div class="lesson-number">
                    🔎
                </div>

                <div>

                    <h3>
                        ${escapeHtml(
                            lesson.title
                        )}
                    </h3>

                    <span class="meta-badge">
                        ${escapeHtml(
                            lesson.moduleTitle
                        )}
                    </span>

                    <span class="meta-badge">
                        ${escapeHtml(
                            lesson.chapterTitle
                        )}
                    </span>

                </div>

            </div>

            <div class="lesson-arrow">
                ←
            </div>

        </a>
    `;

}
