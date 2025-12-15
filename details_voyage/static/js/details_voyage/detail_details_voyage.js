// Exemple : Afficher une alerte de confirmation avant suppression
document.querySelector('.btn-outline-danger').addEventListener('click', function(e) {
    e.preventDefault();
    if (confirm("Êtes-vous sûr de vouloir supprimer cette catégorie ? Cette action est irréversible.")) {
        window.location.href = e.target.closest('a').href;
    }
});