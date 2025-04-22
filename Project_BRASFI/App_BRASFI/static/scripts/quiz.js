const parsedQuestions = JSON.parse(document.getElementById('questions-data').textContent);
const timeLimit = JSON.parse(document.getElementById('time-limit').textContent);
let current = 0;
let correctCount = 0;
let timer;


function renderQuestion() {
    const q = parsedQuestions[current];
    document.getElementById("question-number").innerText = `Pergunta ${current + 1} de ${parsedQuestions.length}`;
    document.getElementById("question-text").innerText = q.text;
    document.getElementById("feedback").innerText = "";
    document.getElementById("next-button").style.display = "none";

    const choicesDiv = document.getElementById("choices");
    choicesDiv.innerHTML = "";

    q.choices.forEach((choice, index) => {
        const btn = document.createElement("button");
        btn.innerText = choice.text;
        btn.className = "choice-button";
        btn.onclick = () => handleAnswer(index, choice.is_correct, btn);
        choicesDiv.appendChild(btn);
    });

    startTimer();
}


    function startTimer() {
    let timeLeft = timeLimit;
    const timerBar = document.getElementById('timer-bar');
    timerBar.style.width = '100%';
    timerBar.style.backgroundColor = '#4caf50'; // verde

    const interval = 1000;
    const decrement = 100 / timeLimit;

    timer = setInterval(() => {
        timeLeft--;
        document.getElementById("timer").innerText = `⏳ Tempo: ${timeLeft}s`;
        const percent = timeLeft * decrement;
        timerBar.style.width = `${percent}%`;

        if (percent < 50 && percent >= 20) timerBar.style.backgroundColor = '#ff9800'; // laranja
        else if (percent < 20) timerBar.style.backgroundColor = '#f44336'; // vermelho

        if (timeLeft <= 0) {
            clearInterval(timer);
            showCorrectAnswer(true);
        }
    }, interval);
}


function handleAnswer(index, isCorrect, btn) {
    clearInterval(timer);
    disableChoices();

    const allButtons = document.querySelectorAll("#choices button");
    const q = parsedQuestions[current];

    allButtons.forEach((b, idx) => {
        b.disabled = true;
        if (q.choices[idx].is_correct) {
            b.classList.add("correct");
        } else if (b === btn && !isCorrect) {
            b.classList.add("incorrect");
        }
    });

    if (isCorrect) correctCount++;

    document.getElementById("next-button").style.display = "inline-block";
}

function showCorrectAnswer(timeout = false) {
    const q = parsedQuestions[current];
    const allButtons = document.querySelectorAll("#choices button");

    allButtons.forEach((btn, idx) => {
        btn.disabled = true;
        if (q.choices[idx].is_correct) {
            btn.classList.add("correct");
            btn.innerHTML = "✅ " + q.choices[idx].text;
        }
    });

    if (timeout) {
        document.getElementById("feedback").innerText = "⏰ Tempo esgotado!";
        document.getElementById("next-button").style.display = "inline-block";
    }
}

function disableChoices() {
    document.querySelectorAll("#choices button").forEach(btn => btn.disabled = true);
}

function nextQuestion() {
    current++;
    if (current < parsedQuestions.length) {
        renderQuestion();
    } else {
        showResult();
    }
}

function showResult() {
    document.getElementById("quiz-container").style.display = "none";
    document.getElementById("result").style.display = "block";
    document.getElementById("correct-count").innerText = correctCount;

    fetch('/quizzes/submit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            quiz_id: Number("{{ quiz.id }}"),
            score: correctCount,
            total: parsedQuestions.length
        })
    });
}

window.onload = () => {
    renderQuestion();
};