function createvideo() {
    const popup = document.querySelector(".popup");
    popup.style.display = 'block';
    popup.querySelector('.popup-create-post').style.display = 'block';

    document.querySelector('.body').setAttribute('aria-hidden', 'true');
    document.querySelector('body').style.overflow = "hidden";

    const videoInput = document.querySelector('#video-upload');
    const titleInput = popup.querySelector("input[name='title']");
    const descriptionInput = popup.querySelector("textarea[name='description']");
    const submitBtn = popup.querySelector('.submit-btn');
    const previewDiv = document.getElementById('video-preview-div');
    const videoTag = document.getElementById('video-preview');

    // Reset previous state
    titleInput.value = '';
    descriptionInput.value = '';
    videoInput.value = '';
    videoTag.src = '';
    previewDiv.style.display = 'none';
    submitBtn.disabled = true;

    function validateForm() {
        const hasTitle = titleInput.value.trim().length > 0;
        const hasDesc = descriptionInput.value.trim().length > 0;
        const hasVideo = videoInput.files.length > 0;

        submitBtn.disabled = !(hasTitle && hasDesc && hasVideo);
    }

    // Video preview
    videoInput.onchange = function () {
        const file = this.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            videoTag.src = url;
            previewDiv.style.display = 'block';
        }
        validateForm();
    };

    titleInput.addEventListener('input', validateForm);
    descriptionInput.addEventListener('input', validateForm);
}

function createquiz() {
    const popup = document.querySelector(".popup");
    popup.style.display = 'block';
    const quizPopup = popup.querySelector('.popup-create-quiz');

    quizPopup.style.display = 'block';

    // Bloquear fundo
    document.querySelector('.body').setAttribute('aria-hidden', 'true');
    document.querySelector('body').style.overflow = "hidden";

    // Elementos do formulário
    const titleInput = quizPopup.querySelector("#quizTitle");
    const descriptionInput = quizPopup.querySelector("#quizDescription");
    const questionsDiv = quizPopup.querySelector("#questions");
    const submitBtn = quizPopup.querySelector(".submit-quiz-btn");

    // Reset do conteúdo
    titleInput.value = '';
    descriptionInput.value = '';
    questionsDiv.innerHTML = '';
    submitBtn.disabled = true;

    // Função de validação
    function validateForm() {
        const hasTitle = titleInput.value.trim().length > 0;
        const hasDesc = descriptionInput.value.trim().length > 0;
        const hasQuestions = questionsDiv.querySelectorAll('.card').length > 0;
        submitBtn.disabled = !(hasTitle && hasDesc && hasQuestions);
    }

    // Observador de mudanças em perguntas
    const observer = new MutationObserver(validateForm);
    observer.observe(questionsDiv, { childList: true, subtree: true });

    // Eventos de input
    titleInput.addEventListener('input', validateForm);
    descriptionInput.addEventListener('input', validateForm);

    // Reset prévio do observer anterior (evita duplicidade)
    if (quizPopup.__observer__) {
        quizPopup.__observer__.disconnect();
    }
    quizPopup.__observer__ = observer;
}

function addQuestion() {
    const questionsDiv = document.getElementById('questions');
    const totalPerguntasAtuais = questionsDiv.querySelectorAll('.card').length;
    const numeroPergunta = totalPerguntasAtuais + 1;

    const qDiv = document.createElement('div');
    qDiv.classList.add('card', 'my-3', 'p-3');

    qDiv.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <h5>Pergunta ${numeroPergunta}</h5>
            <button type="button" class="btn btn-danger btn-sm" onclick="removeQuestion(this)">✕</button>
        </div>
        <input type="text" class="form-control mb-2" placeholder="Enunciado da pergunta" name="qtext">
        <div class="choices"></div>
        <button class="btn btn-sm btn-outline-primary my-1" onclick="addChoice(this)">+ Alternativa</button>
    `;

    questionsDiv.appendChild(qDiv);
    addChoice(qDiv.querySelector('.btn-outline-primary'));
}

function addChoice(button) {
    const choiceDiv = document.createElement('div');
    choiceDiv.classList.add('input-group', 'mb-1');
    choiceDiv.innerHTML = `
        <div class="input-group-text">
            <input type="radio" name="correct" class="correct-choice">
        </div>
        <input type="text" class="form-control" placeholder="Texto da alternativa">
        <button class="btn btn-outline-danger" onclick="this.parentElement.remove()">✕</button>
    `;

    button.previousElementSibling.appendChild(choiceDiv);
}

function removeQuestion(button) {
    button.closest('.card').remove();
    renumerarPerguntas();
}

function renumerarPerguntas() {
    const cards = document.querySelectorAll('#questions .card');
    cards.forEach((card, index) => {
        card.querySelector('h5').innerText = `Pergunta ${index + 1}`;
    });
}

function submitQuiz() {
    const title = document.getElementById('quizTitle').value;
    const description = document.getElementById('quizDescription').value;
    const questionBlocks = document.querySelectorAll('#questions > div');
    const csrfToken = document.querySelector('.popup-create-quiz input[name="csrfmiddlewaretoken"]').value;

    const questions = Array.from(questionBlocks).map(qBlock => {
        const text = qBlock.querySelector('input[name="qtext"]').value;
        const choices = Array.from(qBlock.querySelectorAll('.input-group')).map(choiceDiv => {
            return {
                text: choiceDiv.querySelector('input[type="text"]').value,
                is_correct: choiceDiv.querySelector('input[type="radio"]').checked
            };
        });
        return { text, choices };
    });

    fetch('/quizzes/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ title, description, questions })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'ok') {
            window.location.reload();
        } else {
            alert("Erro: " + data.message);
        }
    })
    .catch(err => {
        console.error("Erro ao criar quiz:", err);
        alert("Erro inesperado. Tente novamente.");
    });
}

function deleteQuiz(quizId) {
    if (!confirm("Tem certeza que deseja excluir este quiz?")) return;

    fetch(`/quizzes/delete/${quizId}/`, {
        method: "POST",
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(res => {
        if (res.ok) {
            document.querySelector(`li[data-id='${quizId}']`).remove();
        } else {
            alert("Erro ao tentar remover o quiz.");
        }
    });
}

function closeCreatePostPopup() {
    document.querySelector('.popup').style.display = 'none';
    window.location.reload(); // Recarregar a página para atualizar o conteúdo
}