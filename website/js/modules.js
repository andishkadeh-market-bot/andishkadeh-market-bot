document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await loadModules();

    }
);


async function loadModules() {

    const grid =
        document.getElementById(
            "modulesGrid"
        );


    const status =
        document.getElementById(
            "modulesStatus"
        );


    try {

        const data =
            await getModules();


        const modules =
            data.modules || [];


        status.textContent =
            `${modules.length} مسیر آموزشی در اندیشکده فعال است.`;


        if (!modules.length) {

            showError(
                grid,
                "هیچ ماژول آموزشی پیدا نشد."
            );

            return;

        }


        grid.innerHTML =
            modules
                .map(createModuleCard)
                .join("");


    } catch (error) {

        console.error(error);


        status.textContent =
            "خطا در ارتباط با API";


        showError(
            grid,
            "امکان دریافت ماژول‌ها وجود ندارد."
        );

    }

}


function createModuleCard(module) {

    return `
        <a
            class="module-card"
            href="chapter.html?module=${encodeURIComponent(module.id)}"
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
                    "محتوای تخصصی آموزشی اندیشکده"
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
