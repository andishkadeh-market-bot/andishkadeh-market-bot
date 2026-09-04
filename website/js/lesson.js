"use strict";
/* =========================================================
   TELEGRAM BOT CONFIG
========================================================= */
const TELEGRAM_BOT_USERNAME = "YOUR_BOT_USERNAME";
/* =========================================================
   LOAD LESSON
========================================================= */
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const moduleId = getQueryParam("module");
        const chapterId = getQueryParam("chapter");
        const lessonId = getQueryParam("lesson");
        console.log("[Lesson] Parameters:", {
            moduleId,
            chapterId,
            lessonId
        });
        if (!moduleId || !chapterId || !lessonId) {
            showError(
                document.getElementById("lessonContent"),
                "اطلاعات درس کامل نیست."
            );
            return;
        }
        await loadLesson(
            moduleId,
            chapterId,
            lessonId
        );
    } catch (error) {
        console.error(
            "[Lesson] Initialization error:",
            error
        );
        showError(
            document.getElementById("lessonContent"),
            "خطایی هنگام آماده‌سازی صفحه درس رخ داد."
        );
    }
});
/* =========================================================
   LOAD LESSON FROM API
========================================================= */
async function loadLesson(
    moduleId,
    chapterId,
    lessonId
) {
    try {
        console.log(
            "[Lesson] Loading:",
            moduleId,
            chapterId,
            lessonId
        );
        const response = await getLesson(
            moduleId,
            chapterId,
            lessonId
        );
        console.log(
            "[Lesson] API response:",
            response
        );
        if (!response) {
            throw new Error(
                "پاسخ خالی از API دریافت شد."
            );
        }
        const lesson =
            response.lesson ||
            response;
        renderLesson(
            lesson,
            moduleId,
            chapterId,
            lessonId
        );
    } catch (error) {
        console.error(
            "[Lesson] Loading error:",
            error
        );
        showError(
            document.getElementById("lessonContent"),
            error.message ||
            "امکان دریافت این درس وجود ندارد."
        );
    }
}
/* =========================================================
   RENDER LESSON
========================================================= */
function renderLesson(
    lesson,
    moduleId,
    chapterId,
    lessonId
) {
    if (!lesson) {
        showError(
            document.getElementById("lessonContent"),
            "اطلاعات این درس یافت نشد."
        );
        return;
    }
    /*
     * ساختار فعلی API:
     *
     * {
     *   id,
     *   title,
     *   module_id,
     *   chapter_id,
     *   data: {
     *      title,
     *      content,
     *      special_points,
     *      exam_points,
     *      example
     *   }
     * }
     */
    const data =
        lesson.data ||
        lesson;
    /* =====================================================
       TITLE
    ===================================================== */
    const title =
        data.title ||
        lesson.title ||
        "درس آموزشی";
    document.title =
        `${title} | اندیشکده مدیریت و بازار`;
    const titleElement =
        document.getElementById(
            "lessonTitle"
        );
    if (titleElement) {
        titleElement.textContent =
            title;
    }
    /* =====================================================
       MODULE
    ===================================================== */
    const moduleMeta =
        document.getElementById(
            "lessonModuleMeta"
        );
    if (moduleMeta) {
        moduleMeta.textContent =
            getModuleTitle(moduleId);
    }
    /* =====================================================
       CHAPTER
    ===================================================== */
    const chapterMeta =
        document.getElementById(
            "lessonChapterMeta"
        );
    if (chapterMeta) {
        chapterMeta.textContent =
            getChapterTitle(chapterId);
    }
    /* =====================================================
       CHAPTER LINK
    ===================================================== */
    const chapterLink =
        document.getElementById(
            "lessonChapterLink"
        );
    if (chapterLink) {
        chapterLink.href =
            `chapter.html?module=${encodeURIComponent(moduleId)}&chapter=${encodeURIComponent(chapterId)}`;
        chapterLink.textContent =
            getChapterTitle(chapterId);
    }
    /* =====================================================
       MAIN CONTENT
    ===================================================== */
    const contentElement =
        document.getElementById(
            "lessonContent"
        );
    const content =
        data.content ||
        data.lesson ||
        "محتوای آموزشی برای این درس ثبت نشده است.";
    if (contentElement) {
        contentElement.textContent =
            String(content);
    }
    /* =====================================================
       EXAMPLE
    ===================================================== */
    renderExample(data);
    /* =====================================================
       SPECIAL POINTS
    ===================================================== */
    const specialPoints =
        Array.isArray(data.special_points)
            ? data.special_points
            : (
                Array.isArray(data.specialized_points)
                    ? data.specialized_points
                    : (
                        Array.isArray(data.specialized_notes)
                            ? data.specialized_notes
                            : []
                    )
            );
    renderNotes(
        "specializedNotes",
        "specializedSection",
        specialPoints
    );
    /* =====================================================
       EXAM POINTS
    ===================================================== */
    const examPoints =
        Array.isArray(data.exam_points)
            ? data.exam_points
            : (
                Array.isArray(data.exam_notes)
                    ? data.exam_notes
                    : []
            );
    renderNotes(
        "examNotes",
        "examSection",
        examPoints
    );
    /* =====================================================
       TELEGRAM QUIZ CTA
    ===================================================== */
    renderTelegramQuizButton(
        moduleId,
        chapterId,
        lessonId
    );
    console.log(
        "[Lesson] Render completed successfully."
    );
}
/* =========================================================
   MODULE TITLE
========================================================= */
function getModuleTitle(moduleId) {
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
            "💰 مدیریت مالی",
        general_exam:
            "📝 آزمون استخدامی"
    };
    return (
        titles[moduleId] ||
        moduleId ||
        "آموزش"
    );
}
/* =========================================================
   CHAPTER TITLE
========================================================= */
function getChapterTitle(chapterId) {
    const titles = {
        /* مدیریت */
        chapter_01:
            "مبانی مدیریت",
        chapter_02:
            "برنامه‌ریزی",
        chapter_03:
            "سازماندهی",
        chapter_04:
            "هدایت",
        chapter_05:
            "کنترل",
        chapter_06:
            "تصمیم‌گیری",
        chapter_07:
            "مدیریت منابع انسانی",
        chapter_08:
            "رفتار سازمانی",
        chapter_09:
            "رهبری",
        chapter_10:
            "مدیریت استراتژیک",
        chapter_11:
            "مدیریت مالی",
        chapter_12:
            "مدیریت بازاریابی",
        /* بانکداری */
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
/* =========================================================
   EXAMPLE
========================================================= */
function renderExample(data) {
    const section =
        document.getElementById(
            "exampleSection"
        );
    const box =
        document.getElementById(
            "lessonExample"
        );
    if (!section || !box) {
        return;
    }
    const example =
        data.example ||
        data.practical_example;
    if (
        !example ||
        !String(example).trim()
    ) {
        section.style.display =
            "none";
        box.textContent =
            "";
        return;
    }
    section.style.display =
        "";
    box.textContent =
        String(example);
}
/* =========================================================
   NOTES
========================================================= */
function renderNotes(
    listId,
    sectionId,
    notes
) {
    const section =
        document.getElementById(
            sectionId
        );
    const list =
        document.getElementById(
            listId
        );
    if (!section || !list) {
        return;
    }
    if (
        !Array.isArray(notes) ||
        !notes.length
    ) {
        section.style.display =
            "none";
        list.innerHTML =
            "";
        return;
    }
    section.style.display =
        "";
    list.innerHTML =
        notes
            .map(note => {
                let text =
                    note;
                if (
                    typeof note ===
                    "object"
                ) {
                    text =
                        note.title
                            ? `${note.title}: ${note.description || ""}`
                            : (
                                note.description ||
                                ""
                            );
                }
                return `
                    <li>
                        ${escapeHtml(String(text))}
                    </li>
                `;
            })
            .join("");
}
/* =========================================================
   TELEGRAM QUIZ BUTTON
========================================================= */
function renderTelegramQuizButton(
    moduleId,
    chapterId,
    lessonId
) {
    const section =
        document.getElementById(
            "quizSection"
        );
    const container =
        document.getElementById(
            "quizContainer"
        );
    if (!section || !container) {
        console.warn(
            "[Lesson] Quiz CTA elements not found in HTML."
        );
        return;
    }
    const telegramLink =
        buildTelegramQuizLink(
            moduleId,
            chapterId,
            lessonId
        );
    /*
     * اگر نام کاربری ربات هنوز تنظیم نشده باشد،
     * بخش آزمون نمایش داده نمی‌شود تا لینک خراب
     * در سایت منتشر نشود.
     */
    if (!telegramLink) {
        section.style.display =
            "none";
        container.innerHTML =
            "";
        console.warn(
            "[Lesson] Telegram bot username is not configured."
        );
        return;
    }
    section.style.display =
        "";
    container.innerHTML = `
        <div class="telegram-quiz-box">
            <div class="telegram-quiz-icon">
                📝
            </div>
            <div class="telegram-quiz-content">
                <h3>
                    آزمون و ارزیابی این درس
                </h3>
                <p>
                    برای شرکت در آزمون چهارگزینه‌ای،
                    مشاهده نتیجه و ثبت پیشرفت خود،
                    آزمون این درس را در ربات تلگرام انجام دهید.
                </p>
                <a
                    href="${escapeHtml(telegramLink)}"
                    class="telegram-quiz-button"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    🚀 شرکت در آزمون در ربات تلگرام
                </a>
            </div>
        </div>
    `;
}
/* =========================================================
   BUILD TELEGRAM DEEP LINK
========================================================= */
function buildTelegramQuizLink(
    moduleId,
    chapterId,
    lessonId
) {
    const username =
        String(
            TELEGRAM_BOT_USERNAME || ""
        )
            .trim()
            .replace(/^@/, "");
    if (
        !username ||
        username ===
        "YOUR_BOT_USERNAME"
    ) {
        return "";
    }
    /*
     * Telegram deep-link payload
     *
     * مثال:
     *
     * quiz_international_trade_chapter_01_lesson_01_01
     */
    const payload =
        `quiz_${moduleId}_${chapterId}_${lessonId}`;
    return (
        `https://t.me/${encodeURIComponent(username)}?start=${encodeURIComponent(payload)}`
    );
}
