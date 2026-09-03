document.addEventListener(

    "DOMContentLoaded",

    async () => {

        await loadHomeStats();

        await loadFeaturedModules();

    }

);

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

        document.getElementById(

            "statModules"

        ).textContent = modules;

        document.getElementById(

            "statChapters"

        ).textContent = chapters;

        document.getElementById(

            "statLessons"

        ).textContent = lessons;

        document.getElementById(

            "heroModuleCount"

        ).textContent = modules;

        document.getElementById(

            "heroChapterCount"

        ).textContent = chapters;

        document.getElementById(

            "heroLessonCount"

        ).textContent = lessons;

    } catch (error) {

        console.error(error);

    }

}

async function loadFeaturedModules() {

    const container =

        document.getElementById(

            "featuredModules"

        );

    try {

        const data =

            await getModules();

        const modules =

            data.modules || [];

        const featured =

            modules.slice(0, 6);

        if (!featured.length) {

            showError(

                container,

                "ماژول آموزشی پیدا نشد."

            );

            return;

        }

        container.innerHTML =

            featured

                .map(createModuleCard)

                .join("");

    } catch (error) {

        console.error(error);

        showError(

            container,

            "ارتباط با API برقرار نشد."

        );

    }

}

function createModuleCard(module) {

    const id =

        encodeURIComponent(

            module.id

        );

    return `

        <a

            class="module-card"

            href="chapter.html?module=${id}&overview=true"

        >

            <div class="module-icon">

                ${getModuleIcon(module.title)}

            </div>

            <h3>

                ${escapeHtml(module.title)}

            </h3>

            <p>

                ${escapeHtml(

                    module.description ||

                    "محتوای تخصصی آموزشی"

                )}

            </p>

            <div class="module-meta">

                <span class="meta-badge">

                    ${module.chapter_count ?? 0}

                    فصل

                </span>

                <span class="meta-badge">

                    ${module.lesson_count ?? 0}

                    درس

                </span>

            </div>

        </a>

    `;

}
