document.addEventListener("DOMContentLoaded", () => {
    let check = [false, false, false, false, false]; // [username, password, confirm password, email, type]

    document.querySelectorAll(".inp").forEach(input => {
        input.addEventListener('input', () => {

            if(input.classList.contains('usrname')){
                check[0] = input.value.trim().length !== 0;
            }

            if(input.classList.contains('pswd')){
                document.querySelector('.cpswd').value = "";
                document.querySelector('.cpswd').parentElement.querySelector('span').innerText = "";
                check[2] = false;
                check[1] = input.value.trim().length !== 0;
            }

            if(input.classList.contains('cpswd')){
                if(input.value.trim().length !== 0) {
                    if(input.value !== document.querySelector('.pswd').value) {
                        input.parentElement.querySelector('span').innerText = "A senha deve corresponder";
                        check[2] = false;
                    } else {
                        input.parentElement.querySelector('span').innerText = "";
                        check[2] = true;
                    }
                } else {
                    check[2] = false;
                }
            }

            if(input.classList.contains('email')){
                check[3] = input.value.trim().length !== 0;
            }

            if (input.classList.contains('tipo')) {
                check[4] = input.value !== "";
            }

            let i;
            for (i = 0; i < 5; i++) {
                if (!check[i]) break;
            }

            document.querySelector('input[type="submit"]').disabled = i !== 5;
        });

        // Trigger change manually for select dropdown
        if (input.tagName === "SELECT") {
            input.addEventListener('change', () => input.dispatchEvent(new Event('input')));
        }
    });

    document.querySelectorAll('.custom-file-input').forEach(element => {
        element.addEventListener("change", event => {
            const label = event.target.parentElement.querySelector('.custom-file-label');
            if (event.target.files[0]) {
                label.innerText = event.target.files[0].name;
            } else {
                label.innerHTML = event.target.id === 'profile'
                    `<span style="color: #6c757d;">Escolha a foto do perfil</span>`;
            }
        });
    });
});
