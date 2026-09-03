document.addEventListener(

    "DOMContentLoaded",

    async () => {

        const moduleId =

            getQueryParam("module");

        const chapterId =

            getQueryParam("chapter");

        /*

         * اگر فقط module آمده باشد،

         * فصل‌های ماژول را نمایش می‌دهیم.

         */

        if (

            moduleId &&

            !chapterId

        ) {

            await loadModuleChapters(

                moduleId

            );

            return;

        }

        if (

            !moduleId ||

            !chapterId

        ) {

            showError(

                document.getElementById(

                    "lessonsList"

                ),

                "شناسه ماژول یا فصل مشخص نشده است."

            );

            return;

        }

        await loadChapter(

            moduleId,

            chapterId

        );

    }

);

async function loadModuleChapters(

    moduleId

) {

    const title =

        document.getElementById(

            "chapterTitle"

        );

    const description =

        document.getElementById(

            "chapterDescription"

        );

    const list =

        document.getElementById(

            "lessonsList"

        );

    const moduleTitle =

        document.getElementById(

            "chapterModuleTitle"

        );

    try {

        const data =

            await getModule(

                moduleId

            );

        const chapters =

            data.chapters || [];

        moduleTitle.textContent =

            data.title || moduleId;

        title.textContent =

            data.title || "فصل‌های آموزشی";

        description.textContent =

            data.description ||

            "فصل‌های آموزشی این ماژول";

        document.querySelector(

            ".lesson-list-header h2"

        ).textContent =

            "فصل‌های آموزشی";

        document.getElementById(

            "lessonCount"

        ).textContent =

            `${chapters.length} فصل`;

        if (!chapters.length) {

            showError(

                list,

                "فصلی برای این ماژول پیدا نشد."

            );

            return;

        }

        list.innerHTML =

            chapters

                .map(

                    (chapter, index) =>

                        createChapterItem(

                            chapter,

                            index,

                            moduleId

                        )

                )

                .join("");

    } catch (error) {

        console.error(error);

        showError(

            list,

            "امکان دریافت فصل‌ها وجود ندارد."

        );

    }

}

function createChapterItem(

    chapter,

    index,

    moduleId

) {

    return `

        <a

            class="lesson-item"

            href="chapter.html?module=${encodeURIComponent(moduleId)}&chapter=${encodeURIComponent(chapter.id)}"

        >

            <div class="lesson-item-info">

                <div class="lesson-number">

                    ${index + 1}

                </div>

                <div>

                    <h3>

                        ${escapeHtml(chapter.title)}

                    </h3>

                    <span class="meta-badge">

                        ${chapter.lesson_count ?? 0}

                        درس

                    </span>

                </div>

            </div>

            <div class="lesson-arrow">

                ←

            </div>

        </a>

    `;

}

async function loadChapter(

    moduleId,

    chapterId

) {

    const title =

        document.getElementById(

            "chapterTitle"

        );

    const description =

        document.getElementById(

            "chapterDescription"

        );

    const list =

        document.getElementById(

            "lessonsList"

        );

    try {

        const chapter =

            await getChapter(

                moduleId,

                chapterId

            );

        const lessonsResponse =

            await getChapterLessons(

                moduleId,

                chapterId

            );

        const lessons =

            lessonsResponse.lessons || [];

        title.textContent =

            chapter.title ||

            chapterId;

        description.textContent =

            chapter.description ||

            "درس‌های این فصل";

        document.getElementById(

            "chapterModuleTitle"

        ).textContent =

            moduleId;

        document.getElementById(

            "lessonCount"

        ).textContent =

            `${lessons.length} درس`;

        if (!lessons.length) {

            showError(

                list,

                "درسی برای این فصل پیدا نشد."

            );

            return;

        }

        list.innerHTML =

            lessons

                .map(

                    (lesson, index) =>

                        createLessonItem(

                            lesson,

                            index,

                            moduleId,

                            chapterId

                        )

                )

                .join("");

    } catch (error) {

        console.error(error);

        showError(

            list,

            "امکان دریافت درس‌ها وجود ندارد."

        );

    }

}

function createLessonItem(

    lesson,

    index,

    moduleId,

    chapterId

) {

    return `

        <a

            class="lesson-item"

            href="lesson.html?module=${encodeURIComponent(moduleId)}&chapter=${encodeURIComponent(chapterId)}&lesson=${encodeURIComponent(lesson.id)}"

        >

            <div class="lesson-item-info">

                <div class="lesson-number">

                    ${index + 1}

                </div>

                <div>

                    <h3>

                        ${escapeHtml(lesson.title)}

                    </h3>

                    <span class="meta-badge">

                        درس آموزشی

                    </span>

                </div>

            </div>

            <div class="lesson-arrow">

                ←

            </div>

        </a>

    `;

}
