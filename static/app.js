const taskElement = document.getElementById("task");
const levelElement = document.getElementById("level");
const levelLabel = document.getElementById("levelLabel");

const inputElement = document.getElementById("inputText");
const inputLabel = document.getElementById("inputLabel");

const submitButton = document.getElementById("submitButton");
const buttonText = document.getElementById("buttonText");
const spinner = document.getElementById("spinner");

const resultSection = document.getElementById("resultSection");
const resultTitle = document.getElementById("resultTitle");
const resultContent = document.getElementById("resultContent");

const errorBox = document.getElementById("errorBox");
const copyButton = document.getElementById("copyButton");


const TASK_CONFIG = {
    qa: {
        label: "Your question",
        placeholder:
            "Example: What is the largest ocean in the world?",
        button: "Ask EduGenie",
        title: "Answer"
    },

    explain: {
        label: "Concept to explain",
        placeholder:
            "Example: Explain the Pythagoras theorem in simple terms.",
        button: "Explain Concept",
        title: "Explanation"
    },

    quiz: {
        label: "Topic or study material",
        placeholder:
            "Paste a topic or educational passage here to generate a quiz.",
        button: "Generate Quiz",
        title: "Quiz"
    },

    summarize: {
        label: "Text to summarize",
        placeholder:
            "Paste the educational passage you want to summarize.",
        button: "Summarize",
        title: "Summary"
    },

    learn: {
        label: "Topic to learn",
        placeholder:
            "Example: SQL",
        button: "Create Learning Path",
        title: "Learning Path"
    }
};


function updateTaskUI() {
    const task = taskElement.value;

    const config = TASK_CONFIG[task];

    inputLabel.textContent = config.label;

    inputElement.placeholder = config.placeholder;

    buttonText.textContent = config.button;

    levelElement.classList.toggle(
        "hidden",
        task !== "learn"
    );

    levelLabel.classList.toggle(
        "hidden",
        task !== "learn"
    );
}


function showError(message) {
    errorBox.textContent = message;

    errorBox.classList.remove("hidden");
}


function hideError() {
    errorBox.textContent = "";

    errorBox.classList.add("hidden");
}


function setLoading(isLoading) {
    submitButton.disabled = isLoading;

    spinner.classList.toggle(
        "hidden",
        !isLoading
    );

    if (isLoading) {
        buttonText.textContent = "Thinking...";
    } else {
        buttonText.textContent =
            TASK_CONFIG[taskElement.value].button;
    }
}


function showResult(title) {
    resultTitle.textContent = title;

    resultSection.classList.remove("hidden");
}


function escapeHtml(value) {
    const div = document.createElement("div");

    div.textContent = String(value);

    return div.innerHTML;
}


function renderText(text) {
    resultContent.innerHTML = "";

    const body = document.createElement("div");

    body.className = "result-body";

    body.textContent = text;

    resultContent.appendChild(body);
}


function renderQuiz(data) {
    resultContent.innerHTML = "";

    const title = document.createElement("h3");

    title.textContent = data.title;

    resultContent.appendChild(title);


    data.questions.forEach((question, questionIndex) => {

        const questionBox =
            document.createElement("div");

        questionBox.className = "quiz-question";


        const heading =
            document.createElement("h3");

        heading.textContent =
            `${questionIndex + 1}. ${question.question}`;

        questionBox.appendChild(heading);


        const options =
            document.createElement("div");

        options.className = "quiz-options";


        question.options.forEach((option) => {

            const button =
                document.createElement("button");

            button.className = "quiz-option";

            button.type = "button";

            button.textContent = option;


            button.addEventListener("click", () => {

                const allOptions =
                    questionBox.querySelectorAll(
                        ".quiz-option"
                    );

                allOptions.forEach(
                    (item) => {
                        item.disabled = true;
                    }
                );


                if (
                    option ===
                    question.correct_answer
                ) {
                    button.classList.add("correct");

                    button.textContent =
                        `${option} ✓ Correct`;
                } else {
                    button.classList.add("incorrect");

                    button.textContent =
                        `${option} ✗ Incorrect`;

                    allOptions.forEach(
                        (item) => {

                            if (
                                item.textContent ===
                                question.correct_answer
                            ) {
                                item.classList.add(
                                    "correct"
                                );

                                item.textContent =
                                    `${question.correct_answer} ✓ Correct answer`;
                            }
                        }
                    );
                }


                const explanation =
                    document.createElement("div");

                explanation.className =
                    "quiz-explanation";

                explanation.textContent =
                    question.explanation;

                questionBox.appendChild(
                    explanation
                );
            });


            options.appendChild(button);
        });


        questionBox.appendChild(options);

        resultContent.appendChild(questionBox);
    });
}


function renderLearningPath(data) {
    resultContent.innerHTML = "";


    const overview =
        document.createElement("p");

    overview.className =
        "path-overview";

    overview.textContent =
        data.overview;

    resultContent.appendChild(overview);


    data.steps.forEach((step) => {

        const box =
            document.createElement("div");

        box.className =
            "learning-step";


        const heading =
            document.createElement("h3");

        heading.textContent =
            `${step.order}. ${step.topic}`;

        box.appendChild(heading);


        const meta =
            document.createElement("div");

        meta.className =
            "learning-meta";

        meta.textContent =
            `${step.difficulty} • ${step.estimated_time}`;

        box.appendChild(meta);


        const description =
            document.createElement("p");

        description.textContent =
            step.description;

        box.appendChild(description);


        if (
            Array.isArray(step.resources) &&
            step.resources.length > 0
        ) {

            const resourceTitle =
                document.createElement("strong");

            resourceTitle.textContent =
                "Suggested resources:";

            box.appendChild(resourceTitle);


            const list =
                document.createElement("ul");

            list.className =
                "learning-resources";


            step.resources.forEach((resource) => {

                const item =
                    document.createElement("li");

                item.textContent = resource;

                list.appendChild(item);
            });


            box.appendChild(list);
        }


        resultContent.appendChild(box);
    });
}


async function callApi(endpoint, body) {

    const response =
        await fetch(endpoint, {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(body)
        });


    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error(
            "The server returned an invalid response."
        );
    }


    if (!response.ok) {

        const detail =
            data.detail ||
            "The server could not complete the request.";

        throw new Error(detail);
    }


    return data;
}


async function handleSubmit() {

    hideError();

    const task = taskElement.value;

    const text =
        inputElement.value.trim();


    if (!text) {

        showError(
            "Please enter something before submitting."
        );

        inputElement.focus();

        return;
    }


    setLoading(true);


    try {

        let data;


        if (task === "qa") {

            data = await callApi(
                "/qa",
                {
                    question: text
                }
            );

            showResult("Answer");

            renderText(data.answer);

        }


        else if (task === "explain") {

            data = await callApi(
                "/explain",
                {
                    text: text
                }
            );

            showResult("Explanation");

            renderText(data.explanation);

        }


        else if (task === "quiz") {

            data = await callApi(
                "/quiz",
                {
                    text: text
                }
            );

            showResult("Generated Quiz");

            renderQuiz(data);

        }


        else if (task === "summarize") {

            data = await callApi(
                "/summarize",
                {
                    text: text
                }
            );

            showResult("Summary");

            renderText(data.summary);

        }


        else if (task === "learn") {

            data = await callApi(
                "/learn/recommendations",
                {
                    topic: text,
                    level: levelElement.value
                }
            );

            showResult("Personalized Learning Path");

            renderLearningPath(data);

        }

    } catch (error) {

        resultSection.classList.add("hidden");

        showError(
            error.message ||
            "Something went wrong."
        );

    } finally {

        setLoading(false);
    }
}


copyButton.addEventListener(
    "click",
    async () => {

        const text =
            resultContent.innerText.trim();

        if (!text) {
            return;
        }


        try {

            await navigator.clipboard.writeText(text);

            copyButton.textContent = "Copied!";

            setTimeout(() => {
                copyButton.textContent = "Copy";
            }, 1500);

        } catch {

            showError(
                "Could not copy the result."
            );
        }
    }
);


taskElement.addEventListener(
    "change",
    updateTaskUI
);


submitButton.addEventListener(
    "click",
    handleSubmit
);


inputElement.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            event.ctrlKey
        ) {
            handleSubmit();
        }
    }
);


updateTaskUI();