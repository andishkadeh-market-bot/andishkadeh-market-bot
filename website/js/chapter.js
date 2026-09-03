document.addEventListener(
    "DOMContentLoaded",
    async () => {

        const moduleId =
            getQueryParam("module");

        const chapterId =
            getQueryParam("chapter");


        /*
         * حالت اول:
         *
         * chapter.html?module=banking
         *
         * نمایش فصل‌های ماژول
         */

        if (moduleId && !chapterId) {

            await loadModuleChapters(moduleId);

            return;
        }


        /*
         * حالت دوم:
         *
         * chapter.html?module=banking&chapter=...
         *
         * نمایش درس‌های فصل
         */

        if (!moduleId || !chapterId) {

            const list =
                document.getElementById(
                    "lessonsList"
                );

            showError(
                list,
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


/* =========================================================
   نمایش فصل‌های یک ماژول
========================================================= */

async function loadModuleChapters(moduleId) {

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

    const countElement =
        document.getElementById(
            "lessonCount"
        );


    try {

        /*
         * دریافت اطلاعات ماژول
         */

        const moduleData =
            await getModule(moduleId);


        /*
         * دریافت فصل‌ها
         *
         * تمام درخواست‌ها از api.js عبور می‌کنند.
         */

        const chaptersResponse =
            await getModuleChapters(moduleId);


        let chapters = [];


        if (
            Array.isArray(
                chaptersResponse?.chapters
            )
        ) {

            chapters =
                chaptersResponse.chapters;

        } else if (
            Array.isArray(
                chaptersResponse
            )
        ) {

            chapters =
                chaptersResponse;

        } else if (
            Array.isArray(
                chaptersResponse?.data
            )
        ) {

            chapters =
                chaptersResponse.data;

        }


        /*
         * عنوان ماژول
         */

        const moduleName =
            moduleData?.title ||
            moduleId;


        if (moduleTitle) {

            moduleTitle.textContent =
                moduleName;

        }


        if (title) {

            title.textContent =
                moduleName;

        }


        if (description) {

            description.textContent =
                moduleData?.description ||
                "فصل‌های آموزشی این ماژول";

        }


        /*
         * تغییر عنوان لیست
         */

        const listHeader =
            document.querySelector(
                ".lesson-list-header h2"
            );


        if (listHeader) {

            listHeader.textContent =
                "فصل‌های آموزشی";

        }


        /*
         * تعداد فصل‌ها
         */

        if (countElement) {

            countElement.textContent =
                `${chapters.length} فصل`;

        }


        /*
         * اگر فصل وجود نداشت
         */

        if (!chapters.length) {

            showError(
                list,
                "فصلی برای این ماژول پیدا نشد."
            );

            return;
        }


        /*
         * نمایش فصل‌ها
         */

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

        console.error(
            "Load module chapters error:",
            error
        );


        if (countElement) {

            countElement.textContent =
                "خطا";

        }


        showError(
            list,
            "امکان دریافت فصل‌ها وجود ندارد."
        );

    }

}


/* =========================================================
   ساخت کارت فصل
========================================================= */

function createChapterItem(
    chapter,
    index,
    moduleId
) {

    const chapterId =
        chapter?.id || "";


    const chapterTitle =
        chapter?.title ||
        "فصل بدون عنوان";


    const lessonCount =
        chapter?.lesson_count ??
        chapter?.lessons_count ??
        0;


    return `
        <a
            class="lesson-item"
            href="chapter.html?module=${encodeURIComponent(moduleId)}&chapter=${encodeURIComponent(chapterId)}"
        >

            <div class="lesson-item-info">

                <div class="lesson-number">
                    ${index + 1}
                </div>

                <div>

                    <h3>
                        ${escapeHtml(chapterTitle)}
                    </h3>

                    <span class="meta-badge">
                        ${lessonCount}
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


/* =========================================================
   نمایش درس‌های یک فصل
========================================================= */

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

    const moduleTitle =
        document.getElementById(
            "chapterModuleTitle"
        );

    const countElement =
        document.getElementById(
            "lessonCount"
        );


    try {

        /*
         * دریافت اطلاعات فصل
         */

        const chapter =
            await getChapter(
                moduleId,
                chapterId
            );


        /*
         * دریافت درس‌های فصل
         */

        const lessonsResponse =
            await getChapterLessons(
                moduleId,
                chapterId
            );


        let lessons = [];


        if (
            Array.isArray(
                lessonsResponse?.lessons
            )
        ) {

            lessons =
                lessonsResponse.lessons;

        } else if (
            Array.isArray(
                lessonsResponse
            )
        ) {

            lessons =
                lessonsResponse;

        } else if (
            Array.isArray(
                lessonsResponse?.data
            )
        ) {

            lessons =
                lessonsResponse.data;

        }


        /*
         * عنوان فصل
         */

        if (title) {

            title.textContent =
                chapter?.title ||
                chapterId;

        }


        /*
         * توضیحات فصل
         */

        if (description) {

            description.textContent =
                chapter?.description ||
                "درس‌های این فصل";

        }


        /*
         * دریافت عنوان ماژول
         */

        try {

            const moduleData =
                await getModule(moduleId);


            if (moduleTitle) {

                moduleTitle.textContent =
                    moduleData?.title ||
                    moduleId;

            }

        } catch (moduleError) {

            console.error(
                "Load module title error:",
                moduleError
            );


            if (moduleTitle) {

                moduleTitle.textContent =
                    moduleId;

            }

        }


        /*
         * تعداد درس‌ها
         */

        if (countElement) {

            countElement.textContent =
                `${lessons.length} درس`;

        }


        /*
         * اگر درس وجود نداشت
         */

        if (!lessons.length) {

            showError(
                list,
                "درسی برای این فصل پیدا نشد."
            );

            return;
        }


        /*
         * نمایش درس‌ها
         */

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

        console.error(
            "Load chapter error:",
            error
        );


        if (countElement) {

            countElement.textContent =
                "خطا";

        }


        showError(
            list,
            "امکان دریافت درس‌ها وجود ندارد."
        );

    }

}


/* =========================================================
   ساخت کارت درس
========================================================= */

function createLessonItem(
    lesson,
    index,
    moduleId,
    chapterId
) {

    const lessonId =
        lesson?.id || "";


    const lessonTitle =
        lesson?.title ||
        "درس بدون عنوان";


    return `
        <a
            class="lesson-item"
            href="lesson.html?module=${encodeURIComponent(moduleId)}&chapter=${encodeURIComponent(chapterId)}&lesson=${encodeURIComponent(lessonId)}"
        >

            <div class="lesson-item-info">

                <div class="lesson-number">
                    ${index + 1}
                </div>

                <div>

                    <h3>
                        ${escapeHtml(lessonTitle)}
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
