const details_voyage = {
    id: 125,
    gare_depart: { libelle_gare: "Kinshasa (Gare Centrale)" },
    gare_arrive: { libelle_gare: "Lubumbashi (Gare du Sud)" },
    distance: 1800,
    slug: "kinshasa-lubumbashi-125"
};

const tarifs = {
    "Premiere Classe": 45000,
    "Premium": 85000,
    "Luxe / VIP": 150000
};


function formatCDF(number) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'CDF',
        minimumFractionDigits: 0
    }).format(number).replace('FC', 'CDF'); 
}
document.addEventListener('DOMContentLoaded', () => {
    const trajetDetails = document.getElementById('trajet-details');
    const tarifsList = document.getElementById('tarifs-list');
    const slugText = document.getElementById('slug-text');
    const backButton = document.getElementById('back-button');
    const editButton = document.getElementById('edit-button');
    // Remplissage des détails du Trajet
    if (trajetDetails) {
        trajetDetails.innerHTML = `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <strong>ID du Trajet:</strong>
                <span class="badge info-badge rounded-pill">${details_voyage.id}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <strong>Gare de Départ:</strong>
                <span>${details_voyage.gare_depart.libelle_gare}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <strong>Gare d'Arrivée:</strong>
                <span>${details_voyage.gare_arrive.libelle_gare}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <strong>Distance:</strong>
                <span class="text-danger fw-bold">${details_voyage.distance} Km</span>
            </li>
        `;
    }
    
    
    if (slugText) {
        slugText.textContent = details_voyage.slug;
    }
    
    if (tarifsList) {
        let htmlTarifs = '';
        for (const [classe, prix] of Object.entries(tarifs)) {
            htmlTarifs += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <strong>Prix ${classe}:</strong>
                    <span class="price-value">${formatCDF(prix)}</span>
                </li>
            `;
        }
        if (htmlTarifs) {
            tarifsList.innerHTML = htmlTarifs;
        } else {
            tarifsList.innerHTML = '<li class="list-group-item text-center text-muted">Aucune tarification n\'est définie pour ce trajet.</li>';
        }
    }
    
    backButton.onclick = () => alert("Redirection vers la liste des tarifications...");
    editButton.onclick = () => alert(`Redirection vers la modification du trajet ID ${details_voyage.id}...`);
});
