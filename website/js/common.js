document.addEventListener(

    "DOMContentLoaded",

    () => {

        const year =

            document.getElementById(

                "currentYear"

            );

        if (year) {

            year.textContent =

                new Date().getFullYear();

        }

        const menuButton =

            document.getElementById(

                "mobileMenuBtn"

            );

        const mobileNav =

            document.getElementById(

                "mobileNav"

            );

        if (

            menuButton &&

            mobileNav

        ) {

            menuButton.addEventListener(

                "click",

                () => {

                    mobileNav.classList.toggle(

                        "open"

                    );

                }

            );

        }

    }

);

function escapeHtml(value) {

    if (

        value === null ||

        value === undefined

    ) {

        return "";

    }

    return String(value)

        .replaceAll("&", "&amp;")

        .replaceAll("<", "&lt;")

        .replaceAll(">", "&gt;")

        .replaceAll('"', "&quot;")

        .replaceAll("'", "&#039;");

}

function getQueryParam(name) {

    const params =

        new URLSearchParams(

            window.location.search

        );

    return params.get(name);

}

function showError(

    element,

    message = "خطا در دریافت اطلاعات."

) {

    if (!element) {

        return;

    }

    element.innerHTML = `

        <div class="loading-card">

            ❌ ${escapeHtml(message)}

        </div>

    `;

}

function showToast(message) {

    const toast =

        document.getElementById("toast");

    if (!toast) {

        return;

    }

    toast.textContent =

        message;

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    }, 3000);

}

function getModuleIcon(title = "") {

    const text =

        title.toLowerCase();

    if (

        text.includes("بانک")

    ) {

        return "🏦";

    }

    if (

        text.includes("تجارت")

    ) {

        return "🌍";

    }

    if (

        text.includes("مالی")

    ) {

        return "💰";

    }

    if (

        text.includes("مدیریت")

    ) {

        return "📚";

    }

    if (

        text.includes("بازاریابی")

    ) {

        return "📈";

    }

    if (

        text.includes("اقتصاد")

    ) {

        return "📊";

    }

    if (

        text.includes("آزمون")

    ) {

        return "📝";

    }

    return "🎓";
