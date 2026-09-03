document.addEventListener(
    "DOMContentLoaded",
    async () => {

        const moduleId =
            getQueryParam("module");

        const chapterId =
            getQueryParam("chapter");

        const lessonId =
            getQueryParam("lesson");


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

    }
);


/* =========================================================
   LOAD LESSON
========================================================= */

async function loadLesson(
    moduleId,
    chapterId,
    lessonId
) {

    try {

        const response =
            await getLesson(
                moduleId,
                chapterId,
                lessonId
            );


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
            "Lesson loading error:",
            error
        );


        showError(
            document.getElementById(
                "lessonContent"
            ),
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


    const data =
        lesson.data ||
        lesson;


    const title =
        data.title ||
        lesson.title ||
        "درس آموزشی";


    const content =
        data.content ||
        "محتوای آموزشی برای این درس ثبت نشده است.";


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


    const moduleMeta =
        document.getElementById(
            "lessonModuleMeta"
        );

    if (moduleMeta) {

        moduleMeta.textContent =
            getModuleTitle(moduleId);

    }


    const chapterMeta =
        document.getElementById(
            "lessonChapterMeta"
        );

    if (chapterMeta) {

        chapterMeta.textContent =
            getChapterTitle(chapterId);

    }


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


    const contentElement =
        document.getElementById(
            "lessonContent"
        );


    if (contentElement) {

        contentElement.textContent =
            content;

    }


    renderExample(
        data
    );


    renderNotes(
        "specializedNotes",
        "specializedSection",
        data.specialized_notes
    );


    renderNotes(
        "examNotes",
        "examSection",
        data.exam_notes
    );


    renderQuiz(
        data.questions || []
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
            "💰 مالی و اقتصاد",

        general_exam:
            "📝 آزمون استخدامی"

    };


    return (
        titles[moduleId] ||
        moduleId
    );

}


/* =========================================================
   CHAPTER TITLE
========================================================= */

function getChapterTitle(
    chapterId
) {

    const titles = {

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
        chapterId
    );

}


/* =========================================================
   EXAMPLE
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


    if (
        !data.example ||
        !String(
            data.example
        ).trim()
    ) {

        section.style.display =
            "none";

        return;

    }


    section.style.display =
        "";


    box.textContent =
        data.example;

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
   QUIZ
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

        return;

    }


    section.style.display =
        "";


    container.innerHTML =
        questions
            .map(
                (question, index) =>
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
        Array.isArray(
            question.options
        )
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


        result.innerHTML =
            "✅ پاسخ شما صحیح است.";


    } else {

        button.classList.add(
            "wrong"
        );


        let correctButton = null;


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


        result.innerHTML =
            `❌ پاسخ صحیح: ${escapeHtml(
                correctAnswer
            )}`;

    }


    result.style.display =
        "block";

}
