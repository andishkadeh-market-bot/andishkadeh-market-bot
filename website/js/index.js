document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await loadHomeStats();

        await loadFeaturedModules();

    }
);


/* =========================================================
   HOME STATISTICS
========================================================= */

async function loadHomeStats() {

    try {

        const data =
            await getApiInfo();


        const stats =
            data.statistics || {};


        const modules =
            stats.modules ?? 0;

        const chapters =
            stats.chapters ?? 0;

        const lessons =
            stats.lessons ?? 0;


        setElementText(
            "statModules",
            modules
        );

        setElementText(
            "statChapters",
            chapters
        );

        setElementText(
            "statLessons",
            lessons
        );


        setElementText(
            "heroModuleCount",
            modules
        );

        setElementText(
            "heroChapterCount",
            chapters
        );

        setElementText(
            "heroLessonCount",
            lessons
        );


    } catch (error) {

        console.error(
            "Home statistics error:",
            error
        );

    }

}


/* =========================================================
   FEATURED MODULES
========================================================= */

async function loadFeaturedModules() {

    const container =
        document.getElementById(
            "featuredModules"
        );


    if (!container) {

        return;

    }


    try {

        const data =
            await getModules();


        const modules =
            Array.isArray(data.modules)
                ? data.modules
                : [];


        const featured =
            modules.slice(
                0,
                6
            );


        if (!featured.length) {

            showError(
                container,
                "ماژول آموزشی پیدا نشد."
            );

            return;

        }


        container.innerHTML =
            featured
                .map(
                    createModuleCard
                )
                .join("");


    } catch (error) {

        console.error(
            "Featured modules error:",
            error
        );


        showError(
            container,
            "ارتباط با API برقرار نشد."
        );

    }

}


/* =========================================================
   CREATE MODULE CARD
========================================================= */

function createModuleCard(
    module
) {

    const id =
        encodeURIComponent(
            module.id || ""
        );


    const title =
        module.title ||
        "ماژول آموزشی";


    const description =
        module.description ||
        "محتوای تخصصی آموزشی";


    const chapterCount =
        module.chapter_count ??
        0;


    const lessonCount =
        module.lesson_count ??
        0;


    return `

        <a
            class="module-card"
            href="chapter.html?module=${id}"
        >

            <div class="module-icon">

                ${getModuleIcon(title)}

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

                <span class="meta-badge">

                    ${chapterCount}

                    فصل

                </span>


                <span class="meta-badge">

                    ${lessonCount}

                    درس

                </span>

            </div>

        </a>

    `;

}


/* =========================================================
   SAFE TEXT SETTER
========================================================= */

function setElementText(
    elementId,
    value
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {

        return;

    }


    element.textContent =
        value;

}
