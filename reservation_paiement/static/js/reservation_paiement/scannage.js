// scannage.js - Avec html5-qrcode (ZXing-JS)

const statusElement = document.getElementById('status');
const resultElement = document.getElementById('scanned-code');

// L'ID 'preview' n'est plus une balise <video>, mais la DIV qui la contient.
// NOTE: La librairie va créer sa propre balise vidéo à l'intérieur de cet ID.
const scannerId = "preview"; 

// --- 1. INITIALISATION DU SCANNER ---
// Créer une instance du scanner, en pointant vers l'ID de la DIV ou VIDEO
const html5QrcodeScanner = new Html5QrcodeScanner(
    scannerId, 
    { 
        fps: 10,                 // Frames par seconde
        qrbox: { width: 250, height: 250 }, // Zone de détection
        disableFlip: false       // Permet de lire les QR codes inversés
    },
    /* verbose= */ false
);

// Démarrer le scanner avec la fonction de succès et d'erreur
html5QrcodeScanner.render(onScanSuccess, onScanFailure);


// --- FONCTION DE SUCCÈS (Le QR Code est lu) ---
function onScanSuccess(decodedText, decodedResult) {
    // Le code décodé est dans 'decodedText'
    statusElement.innerHTML = "✅ **Code QR détecté !** Envoi à Django...";
    resultElement.textContent = decodedText;
    
    // Arrêter le scanner pour éviter de le scanner en boucle
    html5QrcodeScanner.clear(); 
    
    // Envoyer l'information à Django
    sendCodeToDjango(decodedText);
}

// --- FONCTION D'ERREUR ---
function onScanFailure(error) {
    // Si la caméra n'est pas encore prête, ça va s'afficher ici, mais c'est normal
    console.warn(`Scan failure = ${error}`); 
}


// --- 2. FONCTION D'ENVOI À DJANGO ---
function sendCodeToDjango(code) {
    statusElement.textContent = `Code scanné : ${code}. Vérification en cours...`;
    
    // ⚠️ IMPORTANT : L'URL de votre vue Django
    fetch('scannage_verifiaction_paiement', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify({ 'ticket_code': code })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            statusElement.innerHTML = `✅ **Vérification Réussie** : Billet valide pour ${data.passenger_name}`;
        } else {
            statusElement.innerHTML = `❌ **Vérification Échouée** : ${data.message}`;
        }
    })
    .catch(error => {
        console.error('Erreur réseau ou Django:', error);
        statusElement.innerHTML = '❌ Erreur : Problème de communication avec le serveur.';
    });
}

// ⚠️ FONCTION getCookie (Nécessaire pour les requêtes POST avec Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}