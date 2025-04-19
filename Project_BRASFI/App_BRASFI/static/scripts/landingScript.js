function videoUrl(x) {
    document.getElementById("slider").src = x;
}

document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("header");

    // Adiciona a classe transparente no início
    header.classList.add("transparent");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            header.classList.remove("transparent");
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
            header.classList.add("transparent");
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("header");
    const logo = document.getElementById("logo");

    if (!header || !logo) return;

    const logoOriginal = logo.dataset.original;
    const logoScrolled = logo.dataset.scrolled;

    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            header.classList.add("scrolled");
            logo.src = logoScrolled;
        } else {
            header.classList.remove("scrolled");
            logo.src = logoOriginal;
        }
    });
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));

        let offset = 80; // Valor padrão

        if (this.getAttribute("href") === "#impac") {
            offset = -50;
        }

        const targetPosition = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: targetPosition, behavior: "smooth" });
    });
});
