document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('multiStepForm');
    const steps = form.querySelectorAll('.form-step');
    const progressBar = document.getElementById('progressIndicator');
    let currentStepIndex = 0; // Index du tableau steps (0 pour Étape 1, 1 pour Étape 2)

    // Initialise l'affichage
    function updateSteps() {
        steps.forEach((step, index) => {
            step.style.display = index === currentStepIndex ? 'block' : 'none';
        });

        // Mise à jour de la barre de progression
        const progressValue = ((currentStepIndex + 1) / steps.length) * 100;
        progressBar.style.width = progressValue + '%';
        progressBar.setAttribute('aria-valuenow', progressValue);
    }
    
    // Fonction de validation (simple : vérifie que tous les champs requis de l'étape sont remplis)
    function validateCurrentStep() {
        const currentStep = steps[currentStepIndex];
        let isValid = true;
        const requiredInputs = currentStep.querySelectorAll('[required]');

        requiredInputs.forEach(input => {
            if (input.value.trim() === '') {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        return isValid;
    }

    // Gestion des boutons 'Continuer'
    form.querySelectorAll('.next-step').forEach(button => {
        button.addEventListener('click', () => {
            if (validateCurrentStep()) {
                if (currentStepIndex < steps.length - 1) {
                    currentStepIndex++;
                    updateSteps();
                }
            } else {
                alert('Veuillez remplir tous les champs requis pour continuer.');
            }
        });
    });

    // Gestion des boutons 'Retour'
    form.querySelectorAll('.prev-step').forEach(button => {
        button.addEventListener('click', () => {
            if (currentStepIndex > 0) {
                currentStepIndex--;
                updateSteps();
            }
        });
    });
    
    // Assurer que les styles sont appliqués au chargement (seulement l'étape 1 visible)
    updateSteps();
});