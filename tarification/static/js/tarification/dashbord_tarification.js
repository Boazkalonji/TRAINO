// script.js

let sortDirection = {}; // Objet pour garder trace de la direction de tri pour chaque colonne

/**
 * Trie le tableau en fonction de l'index de la colonne cliquée.
 * @param {number} n - L'index de la colonne (0 pour la première).
 */
function sortTable(n) {
    const table = document.getElementById("tarifTable");
    let rows, switching, i, x, y, shouldSwitch;
    switching = true;
    
    // Initialise ou inverse la direction de tri
    if (sortDirection[n] === undefined) {
        sortDirection[n] = "asc";
    } else {
        sortDirection[n] = (sortDirection[n] === "asc") ? "desc" : "asc";
    }

    /* Boucle jusqu'à ce qu'aucun changement n'ait été effectué */
    while (switching) {
        switching = false;
        rows = table.rows;

        /* Commence à la deuxième ligne (index 1) pour ignorer l'en-tête */
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            /* Obtient les deux éléments à comparer, un pour la ligne actuelle et un pour la suivante */
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            // Détermine si la comparaison doit être numérique ou textuelle
            let xContent = x.innerHTML;
            let yContent = y.innerHTML;

            // Pour les colonnes 1 à 4 (Distance et Tarifs), on convertit en nombre.
            if (n >= 1 && n <= 4) {
                xContent = parseFloat(xContent.replace(',', '.')); // Utilise replace pour les décimaux si le formatage venait à changer
                yContent = parseFloat(yContent.replace(',', '.'));
            }

            // Vérifie si les lignes doivent changer de place
            if (sortDirection[n] === "asc") {
                if (xContent > yContent) {
                    shouldSwitch = true;
                    break;
                }
            } else if (sortDirection[n] === "desc") {
                if (xContent < yContent) {
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            /* Si un changement est nécessaire, effectue le changement et marque 'switching' comme vrai pour une autre itération */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
    updateSortIcons(n); // Met à jour les icônes de tri
}

/**
 * Met à jour les icônes de tri dans l'en-tête du tableau.
 * @param {number} n - L'index de la colonne triée.
 */
function updateSortIcons(n) {
    const headers = document.getElementById("tarifTable").getElementsByTagName("TH");
    for (let i = 0; i < headers.length; i++) {
        const icon = headers[i].querySelector('i');
        if (icon) {
            icon.className = 'fas fa-sort'; // Réinitialise toutes les icônes

            if (i === n) {
                // Met à jour l'icône de la colonne triée
                if (sortDirection[n] === "asc") {
                    icon.className = 'fas fa-sort-up';
                } else {
                    icon.className = 'fas fa-sort-down';
                }
            }
        }
    }
}