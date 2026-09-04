"use strict";

/* =========================================================
   LOAD LESSON
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        try {

            const moduleId =
                getQueryParam("module");

            const chapterId =
                getQueryParam("chapter");

            const lessonId =
                getQueryParam("lesson");


            console.log(
                "[Lesson] Parameters:",
                {
                    moduleId,
                    chapterId,
                    lessonId
                }
            );


            if (
                !moduleId ||
                !chapterId ||
                !lessonId
            ) {

                showError(
                    document.getElementById(
                        "lessonContent"
                    ),
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
                document.getElementById(
                    "lessonContent"
                ),
                "خطایی هنگام آماده‌سازی صفحه درس رخ داد."
            );

        }

    }
);


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


        const response =
            await getLesson(
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


        /*
         * API فعلی به این شکل است:
         *
         * {
         *   id: "...",
         *   title: "...",
         *   module_id: "...",
         *   chapter_id: "...",
         *   data: {
         *      title: "...",
         *      content: "...",
         *      special_points: [],
         *      exam_points: [],
         *      example: "..."
         *   }
         * }
         */


        const lesson =
            response.lesson ||
            response;


        renderLesson(
            lesson,
            moduleId,
            chapterId
        );

    } catch (error) {

        console.error(
            "[Lesson] Loading error:",
            error
        );


        const content =
            document.getElementById(
                "lessonContent"
            );


        showError(
            content,
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
    chapterId
) {

    if (!lesson) {

        showError(
            document.getElementById(
                "lessonContent"
            ),
            "اطلاعات این درس یافت نشد."
        );

        return;

    }


    /*
     * اطلاعات محتوایی داخل data قرار دارد.
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
       MODULE META
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
       CHAPTER META
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
        "محتوای آموزشی برای این درس ثبت نشده است.";


    if (contentElement) {

        /*
         * textContent استفاده شده تا محتوای API
         * به عنوان HTML اجرا نشود.
         */

        contentElement.textContent =
            content;

    }


    /* =====================================================
       EXAMPLE
    ===================================================== */

    renderExample(data);


    /* =====================================================
       SPECIAL POINTS
    ===================================================== */

    /*
     * ساختار واقعی API:
     * special_points
     *
     * برای سازگاری با نسخه‌های قدیمی:
     * specialized_notes
     * نیز پشتیبانی می‌شود.
     */

    const specialPoints =
        Array.isArray(data.special_points)
            ? data.special_points
            : data.specialized_notes;


    renderNotes(
        "specializedNotes",
        "specializedSection",
        specialPoints
    );


    /* =====================================================
       EXAM POINTS
    ===================================================== */

    /*
     * ساختار واقعی API:
     * exam_points
     *
     * برای سازگاری با نسخه‌های قدیمی:
     * exam_notes
     * نیز پشتیبانی می‌شود.
     */

    const examPoints =
        Array.isArray(data.exam_points)
            ? data.exam_points
            : data.exam_notes;


    renderNotes(
        "examNotes",
        "examSection",
        examPoints
    );


    /* =====================================================
       QUIZ
    ===================================================== */

    const questions =
        Array.isArray(data.questions)
            ? data.questions
            : [];


    renderQuiz(
        questions
    );


    console.log(
        "[Lesson] Render completed successfully."
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

function getChapterTitle(
    chapterId
) {

    const titles = {

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
   RENDER EXAMPLE
========================================================= */

function renderExample(
    data
) {

    const section =
        document.getElementById(
            "exampleSection"
        );


    const box =
        document.getElementById(
            "lessonExample"
        );


    if (
        !section ||
        !box
    ) {

        return;

    }


    const example =
        data.example;


    if (
        !example ||
        !String(example).trim()
    ) {

        section.style.display =
            "none";

        return;

    }


    section.style.display =
        "";


    box.textContent =
        String(example);

}


/* =========================================================
   RENDER NOTES
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


    if (
        !section ||
        !list
    ) {

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
            .map(
                note =>
                    `<li>${escapeHtml(note)}</li>`
            )
            .join("");

}


/* =========================================================
   RENDER QUIZ
========================================================= */

function renderQuiz(
    questions
) {

    const section =
        document.getElementById(
            "quizSection"
        );


    const container =
        document.getElementById(
            "quizContainer"
        );


    if (
        !section ||
        !container
    ) {

        return;

    }


    if (
        !Array.isArray(questions) ||
        !questions.length
    ) {

        section.style.display =
            "none";

        container.innerHTML =
            "";

        return;

    }


    section.style.display =
        "";


    container.innerHTML =
        questions
            .map(
                (
                    question,
                    index
                ) =>
                    createQuestion(
                        question,
                        index
                    )
            )
            .join("");


    document
        .querySelectorAll(
            ".quiz-option"
        )
        .forEach(
            button => {

                button.addEventListener(
                    "click",
                    () => {

                        handleQuizAnswer(
                            button
                        );

                    }
                );

            }
        );

}


/* =========================================================
   CREATE QUESTION
========================================================= */

function createQuestion(
    question,
    index
) {

    const options =
        Array.isArray(question.options)
            ? question.options
            : [];


    const correctAnswer =
        question.correct_answer ||
        question.answer ||
        "";


    return `

        <div
            class="quiz-question"
            data-question="${index}"
            data-answer="${escapeHtml(correctAnswer)}"
        >

            <h3>
                ${index + 1}.
                ${escapeHtml(
                    question.question ||
                    "سؤال بدون متن"
                )}
            </h3>


            <div class="quiz-options">

                ${options
                    .map(
                        option => `

                            <button
                                type="button"
                                class="quiz-option"
                                data-option="${escapeHtml(
                                    option.id || ""
                                )}"
                            >

                                <strong>
                                    ${escapeHtml(
                                        option.id || ""
                                    )}.
                                </strong>

                                ${escapeHtml(
                                    option.text || ""
                                )}

                            </button>

                        `
                    )
                    .join("")}

            </div>


            <div
                class="quiz-result"
                style="display:none"
            ></div>

        </div>

    `;

}


/* =========================================================
   HANDLE QUIZ ANSWER
========================================================= */

function handleQuizAnswer(
    button
) {

    const question =
        button.closest(
            ".quiz-question"
        );


    if (!question) {

        return;

    }


    const correctAnswer =
        question.dataset.answer;


    const selected =
        button.dataset.option;


    const result =
        question.querySelector(
            ".quiz-result"
        );


    if (!result) {

        return;

    }


    const options =
        question.querySelectorAll(
            ".quiz-option"
        );


    options.forEach(
        option => {

            option.disabled =
                true;

        }
    );


    if (
        selected ===
        correctAnswer
    ) {

        button.classList.add(
            "correct"
        );


        result.textContent =
            "✅ پاسخ شما صحیح است.";

    } else {

        button.classList.add(
            "wrong"
        );


        let correctButton =
            null;


        options.forEach(
            option => {

                if (
                    option.dataset.option ===
                    correctAnswer
                ) {

                    correctButton =
                        option;

                }

            }
        );


        if (correctButton) {

            correctButton.classList.add(
                "correct"
            );

        }


        result.textContent =
            `❌ پاسخ صحیح: ${correctAnswer}`;

    }


    result.style.display =
        "block";

}
