const API_BASE =
    "https://andishkadeh-market-bot-2tdu.onrender.com/api";


async function apiFetch(path = "") {

    const url =
        `${API_BASE}${path}`;

    const response =
        await fetch(url, {
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


/* API */

async function getApiInfo() {
    return await apiFetch("");
}


async function getModules() {
    return await apiFetch("/modules");
}


async function getModule(moduleId) {
    return await apiFetch(
        `/modules/${encodeURIComponent(moduleId)}`
    );
}


async function getChapter(
    moduleId,
    chapterId
) {

    return await apiFetch(
        `/modules/${encodeURIComponent(moduleId)}/chapters/${encodeURIComponent(chapterId)}`
    );

}


async function getChapterLessons(
    moduleId,
    chapterId
) {

    return await apiFetch(
        `/modules/${encodeURIComponent(moduleId)}/chapters/${encodeURIComponent(chapterId)}/lessons`
    );

}


async function getLesson(
    moduleId,
    chapterId,
    lessonId
) {

    return await apiFetch(
        `/modules/${encodeURIComponent(moduleId)}/chapters/${encodeURIComponent(chapterId)}/lessons/${encodeURIComponent(lessonId)}`
    );

}


/*
 * دریافت تمام درس‌ها
 * برای نسخه اول جست‌وجو
 */

async function getAllLessons() {

    const modulesResponse =
        await getModules();


    const modules =
        modulesResponse.modules || [];


    const results = [];


    for (const module of modules) {

        const moduleId =
            module.id;


        const moduleResponse =
            await getModule(moduleId);


        const chapters =
            moduleResponse.chapters || [];


        for (const chapter of chapters) {

            const chapterLessons =
                await getChapterLessons(
                    moduleId,
                    chapter.id
                );


            const lessons =
                chapterLessons.lessons || [];


            for (const lesson of lessons) {

                results.push({
                    ...lesson,

                    moduleTitle:
                        module.title,

                    chapterTitle:
                        chapter.title

                });

            }

        }

    }


    return results;

}
