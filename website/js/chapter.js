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
         * یعنی کاربر هنوز فصل خاصی را انتخاب نکرده
         * و باید لیست فصل‌های ماژول نمایش داده شود.
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
         * یعنی یک فصل انتخاب شده و باید درس‌های آن
         * فصل نمایش داده شوند.
         */

        if (!moduleId || !chapterId) {

            showError(
                document.getElementById("lessonsList"),
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


/*
 * =========================================================
 * نمایش فصل‌های یک ماژول
 * =========================================================
 */

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

    try {

        /*
         * دریافت اطلاعات ماژول
         */

        const moduleData =
            await getModule(moduleId);


        /*
         * بعضی APIها اطلاعات فصل‌ها را مستقیماً
         * داخل data.chapters می‌دهند.
         */

        let chapters =
            Array.isArray(moduleData?.chapters)
                ? moduleData.chapters
                : [];


        /*
         * اگر getModule فصل‌ها را برنگرداند،
         * مستقیماً endpoint فصل‌ها را صدا می‌زنیم.
         *
         * این قسمت برای سازگاری بیشتر با API فعلی اضافه شده.
         */

        if (!chapters.length) {

            try {

                const response =
                    await fetch(
                        `/api/modules/${encodeURIComponent(moduleId)}/chapters`,
                        {
                            method: "GET",
                            headers: {
                                "Accept": "application/json"
                            }
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        `HTTP ${response.status}`
                    );
                }


                const chaptersData =
                    await response.json();


                /*
                 * پشتیبانی از چند ساختار احتمالی API
                 */

                if (
                    Array.isArray(
                        chaptersData
                    )
                ) {

                    chapters =
                        chaptersData;

                } else if (
                    Array.isArray(
                        chaptersData.chapters
                    )
                ) {

                    chapters =
                        chaptersData.chapters;

                } else if (
                    Array.isArray(
                        chaptersData.data
                    )
                ) {

                    chapters =
                        chaptersData.data;

                }

            } catch (apiError) {

                console.error(
                    "Direct chapters API error:",
                    apiError
                );

            }

        }


        /*
         * عنوان ماژول
         */

        const moduleName =
            moduleData?.title ||
            moduleId;


        moduleTitle.textContent =
            moduleName;


        title.textContent =
            moduleName;


        description.textContent =
            moduleData?.description ||
            "فصل‌های آموزشی این ماژول";


        /*
         * تغییر عنوان بخش
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

        const countElement =
            document.getElementById(
                "lessonCount"
            );


        if (countElement) {

            countElement.textContent =
                `${chapters.length} فصل`;

        }


        /*
         * اگر فصلی وجود نداشت
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


        showError(
            list,
            "امکان دریافت فصل‌ها وجود ندارد."
        );

    }

}


/*
 * =========================================================
 * ساخت کارت فصل
 * =========================================================
 */

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


/*
 * =========================================================
 * نمایش درس‌های یک فصل
 * =========================================================
 */

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


        const lessons =
            Array.isArray(
                lessonsResponse?.lessons
            )
                ? lessonsResponse.lessons
                : (
                    Array.isArray(
                        lessonsResponse
                    )
                        ? lessonsResponse
                        : []
                );


        /*
         * عنوان فصل
         */

        title.textContent =
            chapter?.title ||
            chapterId;


        /*
         * توضیحات فصل
         */

        description.textContent =
            chapter?.description ||
            "درس‌های این فصل";


        /*
         * عنوان ماژول
         *
         * ابتدا تلاش می‌کنیم نام واقعی ماژول را
         * دریافت کنیم.
         */

        try {

            const moduleData =
                await getModule(moduleId);


            document.getElementById(
                "chapterModuleTitle"
            ).textContent =
                moduleData?.title ||
                moduleId;

        } catch {

            document.getElementById(
                "chapterModuleTitle"
            ).textContent =
                moduleId;

        }


        /*
         * تعداد درس‌ها
         */

        document.getElementById(
            "lessonCount"
        ).textContent =
            `${lessons.length} درس`;


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


        showError(
            list,
            "امکان دریافت درس‌ها وجود ندارد."
        );

    }

}


/*
 * =========================================================
 * ساخت کارت درس
 * =========================================================
 */

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
