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

        console.error(error);


        showError(
            document.getElementById(
                "lessonContent"
            ),
            "امکان دریافت این درس وجود ندارد."
        );

    }

}


function renderLesson(
    lesson,
    moduleId,
    chapterId
) {

    const data =
        lesson.data ||
        lesson;


    const title =
        data.title ||
        lesson.title ||
        "درس آموزشی";


    document.title =
        `${title} | اندیشکده مدیریت و بازار`;


    document.getElementById(
        "lessonTitle"
    ).textContent =
        title;


    document.getElementById(
        "lessonModuleMeta"
    ).textContent =
        moduleId;


    document.getElementById(
        "lessonChapterMeta"
    ).textContent =
        chapterId;


    const chapterLink =
        document.getElementById(
            "lessonChapterLink"
        );


    chapterLink.href =
        `chapter.html?module=${encodeURIComponent(moduleId)}&chapter=${encodeURIComponent(chapterId)}`;


    chapterLink.textContent =
        chapterId;


    document.getElementById(
        "lessonContent"
    ).textContent =
        data.content ||
        "محتوای آموزشی برای این درس ثبت نشده است.";


    renderExample(data);

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


function renderExample(data) {

    const section =
        document.getElementById(
            "exampleSection"
        );


    const box =
        document.getElementById(
            "lessonExample"
        );


    if (
        !data.example ||
        !String(data.example).trim()
    ) {

        section.style.display =
            "none";

        return;

    }


    box.textContent =
        data.example;

}


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
        !Array.isArray(notes) ||
        !notes.length
    ) {

        section.style.display =
            "none";

        return;

    }


    list.innerHTML =
        notes
            .map(
                note =>
                    `<li>${escapeHtml(note)}</li>`
            )
            .join("");

}


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
        !Array.isArray(questions) ||
        !questions.length
    ) {

        section.style.display =
            "none";

        return;

    }


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
        .querySelectorAll(".quiz-option")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    handleQuizAnswer(
                        button
                    );

                }
            );

        });

}


function createQuestion(
    question,
    index
) {

    const options =
        Array.isArray(question.options)
            ? question.options
            : [];


    return `
        <div
            class="quiz-question"
            data-question="${index}"
            data-answer="${escapeHtml(
                question.correct_answer ||
                question.answer ||
                ""
            )}"
        >

            <h3>
                ${index + 1}.
                ${escapeHtml(
                    question.question
                )}
            </h3>


            <div>

                ${options
                    .map(
                        option => `
                            <button
                                type="button"
                                class="quiz-option"
                                data-option="${escapeHtml(option.id)}"
                            >
                                <strong>
                                    ${escapeHtml(option.id)}.
                                </strong>

                                ${escapeHtml(option.text)}
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


function handleQuizAnswer(
    button
) {

    const question =
        button.closest(
            ".quiz-question"
        );


    const correctAnswer =
        question.dataset.answer;


    const selected =
        button.dataset.option;


    const result =
        question.querySelector(
            ".quiz-result"
        );


    question
        .querySelectorAll(
            ".quiz-option"
        )
        .forEach(option => {

            option.disabled = true;

        });


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


        const correctButton =
            question.querySelector(
                `[data-option="${CSS.escape(correctAnswer)}"]`
            );


        if (correctButton) {

            correctButton.classList.add(
                "correct"
            );

        }


        result.innerHTML =
            `❌ پاسخ صحیح: ${escapeHtml(correctAnswer)}`;

    }


    result.style.display =
        "block";

}
