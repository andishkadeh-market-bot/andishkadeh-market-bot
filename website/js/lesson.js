“use strict”;

/* =========================================================
LOAD LESSON
========================================================= */

document.addEventListener(
“DOMContentLoaded”,
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
    showError(
        document.getElementById(
            "lessonContent"
        ),
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
 * ساختار API فعلی:
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
 *      example,
 *      quiz
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
   QUIZ
===================================================== */
/*
 * ساختار واقعی درس‌ها:
 *
 * quiz: [
 *   {
 *      question: "...",
 *      options: [...],
 *      answer: 2,
 *      explanation: "..."
 *   }
 * ]
 */
const quiz =
    Array.isArray(data.quiz)
        ? data.quiz
        : (
            Array.isArray(data.questions)
                ? data.questions
                : []
        );
renderQuiz(
    quiz
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
            note => {
                let text =
                    note;
                /*
                 * اگر نکته به صورت object باشد
                 * عنوان و توضیح آن را نیز پشتیبانی می‌کنیم.
                 */
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
                        ${escapeHtml(text)}
                    </li>
                `;
            }
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
    container.innerHTML =
        "";
    return;
}
section.style.display =
    "";
container.innerHTML =
    `
        <div class="quiz-intro">
            <p>
                به سوالات زیر پاسخ دهید و دانش خود را محک بزنید.
            </p>
        </div>
        <div class="quiz-list">
            ${questions
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
                .join("")}
        </div>
        <div
            id="quizFinalResult"
            class="quiz-final-result"
            style="display:none"
        ></div>
    `;
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
/*
 * در فایل‌های فعلی management:
 *
 * answer = 0 / 1 / 2 / ...
 *
 * بنابراین مقدار صحیح را به شکل رشته نگه می‌داریم.
 */
const correctAnswer =
    normalizeAnswer(
        question.answer !== undefined
            ? question.answer
            : question.correct_answer
    );
const explanation =
    question.explanation ||
    question.explain ||
    "";
return `
    <div
        class="quiz-question"
        data-question="${index}"
        data-answer="${escapeHtml(correctAnswer)}"
        data-explanation="${escapeHtml(explanation)}"
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
                    (
                        option,
                        optionIndex
                    ) => {
                        const normalized =
                            normalizeOption(
                                option,
                                optionIndex
                            );
                        return `
                            <button
                                type="button"
                                class="quiz-option"
                                data-option="${escapeHtml(
                                    normalized.value
                                )}"
                            >
                                <strong>
                                    ${escapeHtml(
                                        normalized.label
                                    )}.
                                </strong>
                                <span>
                                    ${escapeHtml(
                                        normalized.text
                                    )}
                                </span>
                            </button>
                        `;
                    }
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
NORMALIZE ANSWER
========================================================= */

function normalizeAnswer(
answer
) {

if (
    answer === null ||
    answer === undefined
) {
    return "";
}
/*
 * اگر answer عددی باشد:
 *
 * 0 = A
 * 1 = B
 * 2 = C
 * 3 = D
 */
if (
    typeof answer ===
    "number"
) {
    return String(answer);
}
const text =
    String(answer).trim();
/*
 * اگر پاسخ A/B/C/D باشد
 * به index عددی تبدیل می‌شود.
 */
const upper =
    text.toUpperCase();
const letters = {
    A: "0",
    B: "1",
    C: "2",
    D: "3"
};
if (
    Object.prototype.hasOwnProperty.call(
        letters,
        upper
    )
) {
    return letters[upper];
}
return text;

}

/* =========================================================
NORMALIZE OPTION
========================================================= */

function normalizeOption(
option,
index
) {

/*
 * حالت ساده:
 *
 * "گزینه اول"
 */
if (
    typeof option ===
    "string"
) {
    return {
        value:
            String(index),
        label:
            getOptionLabel(index),
        text:
            option
    };
}
/*
 * حالت object
 */
if (
    option &&
    typeof option ===
    "object"
) {
    const rawId =
        option.id ??
        option.value ??
        option.key;
    let value;
    if (
        rawId === null ||
        rawId === undefined
    ) {
        value =
            String(index);
    } else {
        value =
            normalizeAnswer(
                rawId
            );
    }
    return {
        value,
        label:
            getOptionLabel(index),
        text:
            String(
                option.text ??
                option.label ??
                option.title ??
                ""
            )
    };
}
return {
    value:
        String(index),
    label:
        getOptionLabel(index),
    text:
        ""
};

}

/* =========================================================
OPTION LABEL
========================================================= */

function getOptionLabel(
index
) {

const labels = [
    "A",
    "B",
    "C",
    "D"
];
return (
    labels[index] ||
    String(index + 1)
);

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
/*
 * جلوگیری از پاسخ دوباره
 */
if (
    question.dataset.answered ===
    "true"
) {
    return;
}
question.dataset.answered =
    "true";
options.forEach(
    option => {
        option.disabled =
            true;
    }
);
const correctButton =
    Array.from(
        options
    ).find(
        option =>
            option.dataset.option ===
            correctAnswer
    );
const explanation =
    question.dataset.explanation ||
    "";
if (
    selected ===
    correctAnswer
) {
    button.classList.add(
        "correct"
    );
    result.innerHTML =
        `
            <div class="quiz-success">
                <strong>✅ پاسخ صحیح است.</strong>
                ${
                    explanation
                        ? `<p>${escapeHtml(explanation)}</p>`
                        : ""
                }
            </div>
        `;
} else {
    button.classList.add(
        "wrong"
    );
    if (correctButton) {
        correctButton.classList.add(
            "correct"
        );
    }
    const correctLabel =
        correctButton
            ? correctButton.querySelector(
                "strong"
            )?.textContent || ""
            : "";
    result.innerHTML =
        `
            <div class="quiz-error">
                <strong>
                    ❌ پاسخ شما صحیح نیست.
                </strong>
                <p>
                    پاسخ صحیح:
                    ${escapeHtml(correctLabel)}
                </p>
                ${
                    explanation
                        ? `<p>${escapeHtml(explanation)}</p>`
                        : ""
                }
            </div>
        `;
}
result.style.display =
    "block";
updateQuizScore();

}

/* =========================================================
QUIZ SCORE
========================================================= */

function updateQuizScore() {

const questions =
    document.querySelectorAll(
        ".quiz-question"
    );
if (!questions.length) {
    return;
}
let answered =
    0;
let correct =
    0;
questions.forEach(
    question => {
        if (
            question.dataset.answered !==
            "true"
        ) {
            return;
        }
        answered++;
        const selectedButton =
            question.querySelector(
                ".quiz-option.correct"
            );
        const selectedWrong =
            question.querySelector(
                ".quiz-option.wrong"
            );
        /*
         * اگر گزینه صحیح توسط کاربر انتخاب شده باشد
         * دکمه correct همان دکمه انتخاب‌شده است.
         */
        if (
            selectedButton &&
            !selectedWrong
        ) {
            correct++;
        }
    }
);
if (
    answered !==
    questions.length
) {
    return;
}
const finalResult =
    document.getElementById(
        "quizFinalResult"
    );
if (!finalResult) {
    return;
}
const percentage =
    Math.round(
        (
            correct /
            questions.length
        ) *
        100
    );
finalResult.innerHTML =
    `
        <div class="quiz-score">
            <h3>
                🎯 نتیجه آزمون
            </h3>
            <p>
                ${correct}
                پاسخ صحیح از
                ${questions.length}
                سؤال
            </p>
            <strong>
                امتیاز:
                ${percentage}٪
            </strong>
        </div>
    `;
finalResult.style.display =
    "block";

}
