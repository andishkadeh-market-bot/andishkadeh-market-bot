const API_BASE =
    "https://andishkadeh-market-bot-2tdu.onrender.com/api";

let currentModuleId = null;
let currentChapterId = null;
let currentLessons = [];


/* =========================
   API
========================= */

async function apiFetch(endpoint) {

    const response = await fetch(API_BASE + endpoint, {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    });

    if (!response.ok) {
        throw new Error(
            `API Error: ${response.status}`
        );
    }

    return await response.json();
}


/* =========================
   INITIALIZATION
========================= */

document.addEventListener("DOMContentLoaded", () => {

    loadStatistics();
    loadModules();

});


/* =========================
   STATISTICS
========================= */

async function loadStatistics() {

    try {

        const data = await apiFetch("");

        const statistics = data.statistics || {};

        const modules =
            statistics.modules ?? 0;

        const chapters =
            statistics.chapters ?? 0;

        const lessons =
            statistics.lessons ?? 0;


        setText("statModules", modules);
        setText("statChapters", chapters);
        setText("statLessons", lessons);

        setText("heroModuleCount", modules);
        setText("heroChapterCount", chapters);
        setText("heroLessonCount", lessons);

    } catch (error) {

        console.error("Statistics error:", error);

        setText("statModules", "-");
        setText("statChapters", "-");
        setText("statLessons", "-");

        setText("heroModuleCount", "-");
        setText("heroChapterCount", "-");
        setText("heroLessonCount", "-");
    }
}


/* =========================
   MODULES
========================= */

async function loadModules() {

    const container =
        document.getElementById("modulesContainer");

    try {

        const data =
            await apiFetch("/modules");

        const modules =
            data.modules || [];

        if (!modules.length) {

            container.innerHTML = `
                <div class="error-box">
                    هنوز محتوای آموزشی در سیستم مرکزی ثبت نشده است.
                </div>
            `;

            return;
        }


        container.innerHTML = modules
            .map((module, index) =>
                createModuleCard(module, index)
            )
            .join("");


    } catch (error) {

        console.error("Modules error:", error);

        container.innerHTML = `
            <div class="error-box">
                اتصال به سیستم آموزشی برقرار نشد.
                <br>
                لطفاً API را بررسی کنید.
            </div>
        `;
    }
}


function createModuleCard(module, index) {

    const icons = [
        "📚",
        "🏦",
        "🌍",
        "💰",
        "📝",
        "📈",
        "🧠",
        "📊"
    ];

    const icon =
        icons[index % icons.length];

    const title =
        escapeHTML(module.title || "ماژول آموزشی");

    const description =
        escapeHTML(
            module.description ||
            "مجموعه‌ای از آموزش‌ها و درس‌های تخصصی اندیشکده."
        );

    const chapterCount =
        module.chapter_count ?? 0;

    const lessonCount =
        module.lesson_count ?? 0;


    return `
        <article
            class="module-card"
            onclick="openModule('${escapeAttribute(module.id)}')"
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

                <span>
                    📖 ${chapterCount} فصل
                </span>

                <span>
                    🎓 ${lessonCount} درس
                </span>

            </div>

            <span class="module-button">
                مشاهده آموزش‌ها ←
            </span>

        </article>
    `;
}


/* =========================
   MODULE
========================= */

async function openModule(moduleId) {

    currentModuleId = moduleId;

    hideAllPages();

    document
        .getElementById("modulePage")
        .classList.remove("hidden");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });


    const header =
        document.getElementById("moduleHeader");

    const container =
        document.getElementById("chaptersContainer");


    header.innerHTML = `
        <h1>در حال بارگذاری...</h1>
        <p>لطفاً منتظر بمانید.</p>
    `;

    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>در حال دریافت فصل‌ها...</p>
        </div>
    `;


    try {

        const data =
            await apiFetch(
                `/modules/${encodeURIComponent(moduleId)}`
            );


        const module =
            data.module || data;


        header.innerHTML = `
            <h1>
                ${escapeHTML(module.title || moduleId)}
            </h1>

            <p>
                ${escapeHTML(
                    module.description ||
                    "مسیر آموزشی اندیشکده مدیریت و بازار"
                )}
            </p>
        `;


        const chapters =
            data.chapters || [];


        if (!chapters.length) {

            container.innerHTML = `
                <div class="error-box">
                    فصلی برای این ماژول پیدا نشد.
                </div>
            `;

            return;
        }


        container.innerHTML =
            chapters
                .map((chapter, index) =>
                    createChapterCard(chapter, index)
                )
                .join("");


    } catch (error) {

        console.error("Module error:", error);

        container.innerHTML = `
            <div class="error-box">
                دریافت فصل‌های این ماژول با خطا مواجه شد.
            </div>
        `;
    }
}


function createChapterCard(chapter, index) {

    return `
        <article
            class="chapter-card"
            onclick="
                openChapter(
                    '${escapeAttribute(chapter.module_id || currentModuleId)}',
                    '${escapeAttribute(chapter.id)}'
                )
            "
        >

            <div class="chapter-number">
                ${index + 1}
            </div>

            <div class="chapter-info">

                <h3>
                    ${escapeHTML(
                        chapter.title || "فصل آموزشی"
                    )}
                </h3>

                <span>
                    ${chapter.lesson_count ?? 0} درس آموزشی
                </span>

            </div>

            <div class="chapter-arrow">
                ←
            </div>

        </article>
    `;
}


/* =========================
   CHAPTER
========================= */

async function openChapter(moduleId, chapterId) {

    currentModuleId = moduleId;
    currentChapterId = chapterId;

    hideAllPages();

    document
        .getElementById("chapterPage")
        .classList.remove("hidden");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });


    const header =
        document.getElementById("chapterHeader");

    const container =
        document.getElementById("lessonsContainer");


    header.innerHTML = `
        <h1>در حال بارگذاری...</h1>
        <p>در حال دریافت اطلاعات فصل.</p>
    `;


    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>در حال دریافت درس‌ها...</p>
        </div>
    `;


    try {

        const chapterData =
            await apiFetch(
                `/modules/${encodeURIComponent(moduleId)}/chapters/${encodeURIComponent(chapterId)}`
            );


        const chapter =
            chapterData.chapter || chapterData;


        header.innerHTML = `
            <h1>
                ${escapeHTML(
                    chapter.title || "فصل آموزشی"
                )}
            </h1>

            <p>
                ${escapeHTML(
                    chapter.description ||
                    "درس‌های این فصل را انتخاب کنید."
                )}
            </p>
        `;


        const lessonsData =
            await apiFetch(
                `/modules/${encodeURIComponent(moduleId)}/chapters/${encodeURIComponent(chapterId)}/lessons`
            );


        const lessons =
            lessonsData.lessons || [];


        currentLessons = lessons;


        if (!lessons.length) {

            container.innerHTML = `
                <div class="error-box">
                    هنوز درسی برای این فصل ثبت نشده است.
                </div>
            `;

            return;
        }


        container.innerHTML =
            lessons
                .map((lesson, index) =>
                    createLessonCard(lesson, index)
                )
                .join("");


    } catch (error) {

        console.error("Chapter error:", error);

        container.innerHTML = `
            <div class="error-box">
                دریافت درس‌های این فصل با خطا مواجه شد.
            </div>
        `;
    }
}


function createLessonCard(lesson, index) {

    return `
        <article
            class="lesson-card"
            onclick="
                openLesson(
                    '${escapeAttribute(
                        lesson.module_id || currentModuleId
                    )}',
                    '${escapeAttribute(
                        lesson.chapter_id || currentChapterId
                    )}',
                    '${escapeAttribute(lesson.id)}'
                )
            "
        >

            <h3>
                ${index + 1}. 
                ${escapeHTML(
                    lesson.title || "درس آموزشی"
                )}
            </h3>

            <span>
                مشاهده درس ←
            </span>

        </article>
    `;
}


/* =========================
   LESSON
========================= */

async function openLesson(
    moduleId,
    chapterId,
    lessonId
) {

    currentModuleId = moduleId;
    currentChapterId = chapterId;

    hideAllPages();

    document
        .getElementById("lessonPage")
        .classList.remove("hidden");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });


    const container =
        document.getElementById("lessonContent");


    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>در حال دریافت محتوای درس...</p>
        </div>
    `;


    try {

        const data =
            await apiFetch(
                `/modules/${encodeURIComponent(moduleId)}/chapters/${encodeURIComponent(chapterId)}/lessons`
            );


        const lessons =
            data.lessons || [];


        const lesson =
            lessons.find(
                item => item.id === lessonId
            );


        if (!lesson) {

            throw new Error(
                "Lesson not found"
            );
        }


        renderLesson(lesson);


    } catch (error) {

        console.error("Lesson error:", error);

        container.innerHTML = `
            <div class="error-box">
                محتوای این درس دریافت نشد.
            </div>
        `;
    }
}


/* =========================
   RENDER LESSON
========================= */

function renderLesson(lesson) {

    const container =
        document.getElementById("lessonContent");


    const data =
        lesson.data || {};


    const content =
        data.content || "";


    const example =
        data.example || "";


    const specializedNotes =
        Array.isArray(data.specialized_notes)
            ? data.specialized_notes
            : [];


    const examNotes =
        Array.isArray(data.exam_notes)
            ? data.exam_notes
            : [];


    const questions =
        Array.isArray(data.questions)
            ? data.questions
            : [];


    let html = `

        <h1 class="lesson-title">
            ${escapeHTML(
                data.title ||
                lesson.title ||
                "درس آموزشی"
            )}
        </h1>


        <section class="lesson-section">

            <h3>
                📖 درسنامه
            </h3>

            <div class="lesson-text">
                ${formatText(content)}
            </div>

        </section>

    `;


    if (example) {

        html += `

            <section class="lesson-section">

                <h3>
                    💡 مثال کاربردی
                </h3>

                <div class="lesson-text">
                    ${formatText(example)}
                </div>

            </section>

        `;
    }


    if (specializedNotes.length) {

        html += `

            <section class="lesson-section">

                <h3>
                    🎯 نکات تخصصی
                </h3>

                <ul class="notes-list">

                    ${specializedNotes
                        .map(note => `
                            <li>
                                ${escapeHTML(note)}
                            </li>
                        `)
                        .join("")
                    }

                </ul>

            </section>

        `;
    }


    if (examNotes.length) {

        html += `

            <section class="lesson-section">

                <h3>
                    📝 نکات آزمونی
                </h3>

                <ul class="notes-list">

                    ${examNotes
                        .map(note => `
                            <li>
                                ${escapeHTML(note)}
                            </li>
                        `)
                        .join("")
                    }

                </ul>

            </section>

        `;
    }


    if (questions.length) {

        html += `

            <section class="lesson-section">

                <h3>
                    🧠 آزمون درس
                </h3>

        `;


        questions.forEach(
            (question, index) => {

                html += `
                    <div class="question-card">

                        <div class="question-title">

                            ${index + 1}.
                            ${escapeHTML(
                                question.question || ""
                            )}

                        </div>
                `;


                const options =
                    question.options || [];


                options.forEach(option => {

                    html += `
                        <div class="question-option">

                            ${escapeHTML(
                                option.id || ""
                            )})

                            ${escapeHTML(
                                option.text || ""
                            )}

                        </div>
                    `;

                });


                html += `
                    </div>
                `;

            }
        );


        html += `
            </section>
        `;
    }


    container.innerHTML = html;
}


/* =========================
   NAVIGATION
========================= */

function showHome() {

    hideAllPages();

    document
        .getElementById("homePage")
        .classList.remove("hidden");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    loadModules();
}


function goBackToModule() {

    if (currentModuleId) {
        openModule(currentModuleId);
    } else {
        showHome();
    }
}


function goBackToChapter() {

    if (
        currentModuleId &&
        currentChapterId
    ) {

        openChapter(
            currentModuleId,
            currentChapterId
        );

    } else {

        showHome();

    }
}


function hideAllPages() {

    [
        "homePage",
        "modulePage",
        "chapterPage",
        "lessonPage"
    ].forEach(id => {

        const element =
            document.getElementById(id);

        if (element) {
            element.classList.add("hidden");
        }

    });
}


/* =========================
   MOBILE MENU
========================= */

function toggleMobileMenu() {

    const menu =
        document.getElementById("mobileMenu");

    menu.classList.toggle("active");
}


function closeMobileMenu() {

    const menu =
        document.getElementById("mobileMenu");

    menu.classList.remove("active");
}


/* =========================
   HELPERS
========================= */

function setText(id, value) {

    const element =
        document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


function formatText(text) {

    return escapeHTML(text)
        .replace(/\n/g, "<br>");
}


function escapeHTML(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function escapeAttribute(value) {

    return escapeHTML(value)
        .replace(/`/g, "&#096;");
}
