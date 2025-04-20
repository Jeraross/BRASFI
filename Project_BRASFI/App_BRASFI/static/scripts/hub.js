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

function closeCreatePostPopup() {
    document.querySelector('.popup').style.display = 'none';
    window.location.href = 'videos';
}