// Données pour le graphique de tendance (Revenus)
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    new Chart(revenueCtx, {
        type: 'line',
        data: {
            labels: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
            datasets: [{
                label: 'Revenus journaliers ($US)',
                data: [35000, 38000, 42000, 39000, 45780, 48000, 41000],
                backgroundColor: 'rgba(220, 53, 69, 0.1)', // Rouge léger
                borderColor: '#dc3545', // Rouge ONATRA
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: false }
            }
        }
    });

    // Données pour le graphique à secteurs (Répartition par Classe)
    const classPieCtx = document.getElementById('classPieChart').getContext('2d');
    new Chart(classPieCtx, {
        type: 'doughnut',
        data: {
            labels: ['Classe de Luxe', 'Premium', '1ère Classe'],
            datasets: [{
                data: [20000, 15000, 10780],
                backgroundColor: [
                    '#dc3545', // Rouge (Luxe)
                    '#ffc107', // Jaune (Premium)
                    '#0dcaf0'  // Cyan (1ère Classe)
                ],
                hoverOffset: 4
            }]
        },
        options: {
             responsive: true,
             plugins: {
                legend: { display: false } // Masque la légende pour garder le graphique petit
             }
        }
    });