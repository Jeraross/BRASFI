document.addEventListener("DOMContentLoaded", () => {
    let check = [false, false, false, false]; // [username, password, confirm password, email]

    const updateSubmitState = () => {
        const isFormValid = check.every(Boolean);
        document.querySelector('input[type="submit"]').disabled = !isFormValid;
    };

    document.querySelectorAll(".inp").forEach(input => {
        input.addEventListener('input', () => {
            if (input.classList.contains('usrname')) {
                check[0] = input.value.trim().length !== 0;
            }

            if (input.classList.contains('pswd')) {
                document.querySelector('.cpswd').value = "";
                document.querySelector('.cpswd').parentElement.querySelector('span').innerText = "";
                check[2] = false;
                check[1] = input.value.trim().length !== 0;
            }

            if (input.classList.contains('cpswd')) {
                const password = document.querySelector('.pswd').value;
                if (input.value.trim().length !== 0) {
                    if (input.value !== password) {
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

            if (input.classList.contains('email')) {
                check[3] = input.value.trim().length !== 0;
            }

            updateSubmitState();
        });

        // Se for SELECT, força o evento input
        if (input.tagName === "SELECT") {
            input.addEventListener('change', () => input.dispatchEvent(new Event('input')));
        }
    });

    // Atualiza label do input de arquivo
    document.querySelectorAll('.custom-file-input').forEach(element => {
        element.addEventListener("change", event => {
            const label = event.target.parentElement.querySelector('.custom-file-label');
            if (event.target.files[0]) {
                label.innerText = event.target.files[0].name;
            } else {
                label.innerHTML = '<span style="color: #f8f8f8;">Escolha a foto do perfil</span>';
            }
        });
    });
});
