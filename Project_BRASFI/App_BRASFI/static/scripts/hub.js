function toggleUserDropdown(event) {
    const dropdown = document.getElementById('userDropdown');
    dropdown.style.display = (dropdown.style.display === 'block') ? 'none' : 'block';
    event.stopPropagation();
}

// Fecha o dropdown ao clicar fora
document.addEventListener('click', function () {
    const dropdown = document.getElementById('userDropdown');
    dropdown.style.display = 'none';
});

function editProfile() {
    const popup = document.querySelector(".popup");
    popup.style.display = 'block';
    const editPopup = popup.querySelector('.popup-edit');
    editPopup.style.display = 'block';

    document.querySelector('.body').setAttribute('aria-hidden', 'true');
    document.querySelector('body').style.overflow = "hidden";

    const nameInput = editPopup.querySelector("input[name='username']");
    const profilePicInput = editPopup.querySelector("input[name='profilePic']");
    const submitBtn = editPopup.querySelector("button[type='submit']");

    // Reset apenas do input de arquivo
    profilePicInput.value = '';
    
    // Habilita o botão só se houver alteração
    const originalName = nameInput.value;

    function validateEditForm() {
        const nameChanged = nameInput.value.trim() !== originalName.trim();
        const picUploaded = profilePicInput.files.length > 0;

        submitBtn.disabled = !(nameChanged || picUploaded);
    }

    nameInput.addEventListener('input', validateEditForm);
    profilePicInput.addEventListener('change', validateEditForm);

    // Executa uma validação inicial
    validateEditForm();
}

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

function createproject() {
    const popup = document.querySelector(".popup");
    popup.style.display = 'block';
    popup.querySelector('.popup-create-project').style.display = 'block';

    document.querySelector('.body').setAttribute('aria-hidden', 'true');
    document.querySelector('body').style.overflow = "hidden";

    const titleInput = popup.querySelector("input[name='title']");
    const descriptionInput = popup.querySelector("textarea[name='description']");
    const areaSelect = popup.querySelector("select[name='impact_area']");
    const objectiveInput = popup.querySelector("textarea[name='objective']");
    const submitBtn = popup.querySelector('.submit-btn');

    // Reset previous state
    titleInput.value = '';
    descriptionInput.value = '';
    areaSelect.value = '';
    objectiveInput.value = '';
    submitBtn.disabled = true;

    function validateForm() {
        const hasTitle = titleInput.value.trim().length > 0;
        const hasDesc = descriptionInput.value.trim().length > 0;
        const hasArea = areaSelect.value.trim().length > 0;
        const hasObjective = objectiveInput.value.trim().length > 0;

        submitBtn.disabled = !(hasTitle && hasDesc && hasArea && hasObjective);
    }

    titleInput.addEventListener('input', validateForm);
    descriptionInput.addEventListener('input', validateForm);
    areaSelect.addEventListener('change', validateForm);
    objectiveInput.addEventListener('input', validateForm);
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

    // Adiciona o campo de tempo se não existir ainda
    if (!quizPopup.querySelector("#quizTime")) {
        const timeInputDiv = document.createElement("div");
        timeInputDiv.classList.add("mb-3");
        timeInputDiv.innerHTML = `
            <label for="quizTime" class="form-label mt-3">Tempo por pergunta (em segundos)</label>
            <input type="number" class="form-control" id="quizTime" name="quizTime" min="5" value="20" required>
        `;
        descriptionInput.parentElement.insertBefore(timeInputDiv, questionsDiv);
    }

    // Reset do conteúdo
    titleInput.value = '';
    descriptionInput.value = '';
    questionsDiv.innerHTML = '';
    quizPopup.querySelector("#quizTime").value = 20;
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
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="mb-0">Pergunta ${numeroPergunta}</h5>
            <button type="button" class="btn btn-danger btn-sm" onclick="removeQuestion(this)" title="Remover pergunta">✕</button>
        </div>

        <input type="text" name="qtext" class="form-control modern-input mb-3" placeholder="Enunciado da pergunta" required>

        <div class="choices"></div>

        <button type="button" class="btn btn-sm btn-outline-primary mt-2" onclick="addChoice(this)">+ Adicionar Alternativa</button>
    `;

    questionsDiv.appendChild(qDiv);
    addChoice(qDiv.querySelector('.btn-outline-primary'));
}

function addChoice(button) {
    const questionCard = button.closest('.card');
    const questionIndex = Array.from(document.querySelectorAll('#questions .card')).indexOf(questionCard);
    const choicesContainer = button.previousElementSibling;

    const choiceDiv = document.createElement('div');
    choiceDiv.classList.add('input-group', 'mb-2');

    choiceDiv.innerHTML = `
        <div class="input-group-text">
            <input type="radio" name="correct-${questionIndex}" class="correct-choice" title="Resposta correta">
        </div>
        <input type="text" class="form-control" placeholder="Texto da alternativa" required>
        <button type="button" class="btn btn-outline-danger" onclick="this.parentElement.remove()" title="Remover alternativa">✕</button>
    `;

    choicesContainer.appendChild(choiceDiv);
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
    const time = parseInt(document.getElementById('quizTime').value) || 20;
    const questionBlocks = document.querySelectorAll('#questions > div');
    const csrfToken = document.querySelector('.popup-create-quiz input[name="csrfmiddlewaretoken"]').value;

    const questions = Array.from(questionBlocks).map((qBlock, qIndex) => {
        const text = qBlock.querySelector('input[name="qtext"]').value;
        const choices = [];

        const choiceDivs = qBlock.querySelectorAll('.input-group');
        choiceDivs.forEach(choiceDiv => {
            const inputText = choiceDiv.querySelector('input[type="text"]');
            const inputRadio = choiceDiv.querySelector(`input[type="radio"][name="correct-${qIndex}"]`);
            choices.push({
                text: inputText.value,
                is_correct: inputRadio.checked
            });
        });

        return { text, choices };
    });

    fetch('/quizzes/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ title, description, time, questions })
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
            window.location.reload(); // Recarregar a página para atualizar o conteúdo
        } else {
            window.location.reload();
        }
    });
}

function closeCreatePostPopup() {
    document.querySelector('.popup').style.display = 'none';
    window.location.reload(); // Recarregar a página para atualizar o conteúdo
}