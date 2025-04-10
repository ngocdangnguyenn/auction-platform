// Activer les tooltips
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Activer les popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function (popoverTriggerEl) {
        new bootstrap.Popover(popoverTriggerEl);
    });
});

// Faire disparaître les alertes après 5 secondes
document.addEventListener('DOMContentLoaded', function () {
    var alertList = document.querySelectorAll('.alert');
    alertList.forEach(function (alert) {
        setTimeout(function () {
            alert.classList.add('fade');
            alert.classList.remove('show');
        }, 5000); // 5000 ms = 5 secondes
    });
});

// Confirmation pour les actions sensibles
document.addEventListener('DOMContentLoaded', function () {
    var deleteLinks = document.querySelectorAll('.delete-link');
    deleteLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            if (!confirm('Êtes-vous sûr de vouloir effectuer cette action ?')) {
                event.preventDefault();
            }
        });
    });
});

// Défilement fluide pour les liens d'ancrage
document.addEventListener('DOMContentLoaded', function () {
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            var targetId = this.getAttribute('href').substring(1);
            var targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

// Afficher un message de chargement lors de la soumission d'un formulaire
document.addEventListener('DOMContentLoaded', function () {
    var forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        form.addEventListener('submit', function () {
            var submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const caroussel = document.querySelector("#caroussel > div");
    const prevBtn = document.querySelector("#prev-btn");
    const nextBtn = document.querySelector("#next-btn");

    const items = caroussel.children; // Les enchères dans le carrousel
    const itemWidth = items[0].offsetWidth + 20; // Largeur d'un élément + marge
    const totalItems = items.length;

    let currentIndex = totalItems / 2; // Commence au milieu (car duplication)

    // Fonction pour mettre à jour la position du carrousel
    const updateCaroussel = () => {
        caroussel.style.transition = "transform 0.5s ease-in-out";
        caroussel.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
    };

    // Réinitialise la position pour l'effet de boucle infinie
    const resetPosition = () => {
        caroussel.style.transition = "none"; // Désactive la transition
        if (currentIndex === 0) {
            currentIndex = totalItems / 2;
        } else if (currentIndex === totalItems - 1) {
            currentIndex = totalItems / 2 - 1;
        }
        caroussel.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
    };

    // Bouton "Précédent"
    prevBtn.addEventListener("click", () => {
        currentIndex--;
        updateCaroussel();
        setTimeout(resetPosition, 500); // Réinitialise après la transition
    });

    // Bouton "Suivant"
    nextBtn.addEventListener("click", () => {
        currentIndex++;
        updateCaroussel();
        setTimeout(resetPosition, 500); // Réinitialise après la transition
    });

    // Initialisation
    resetPosition();
});

    // Show the button when the user scrolls down
    const backToTopButton = document.getElementById('backToTop');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    // Scroll to the top when the button is clicked
    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });