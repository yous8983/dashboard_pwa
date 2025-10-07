const CACHE_NAME = "zarsa-matchs-cache-v1";

// Liste des fichiers essentiels à mettre en cache
const urlsToCache = [
  "/",
  "/index.html",
  "/assets/css/style.css",
  "/assets/js/app.js",
  "/data/matches.json", // NOUVEAU : Assurez-vous que ce chemin est correct
  "/manifest.json",
  // Ajoutez ici d'autres ressources comme les icônes si vous en utilisez
];

// Installation: Mise en cache des ressources statiques
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Cache ouvert: ressources mises en cache.");
      return cache.addAll(urlsToCache);
    })
  );
});

// Activation: Nettoyage des anciens caches
self.addEventListener("activate", (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log("Suppression de l'ancien cache:", cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch: Stratégie "Cache, puis Network fallback"
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // Retourne la ressource mise en cache si elle existe
      if (response) {
        return response;
      }
      // Sinon, essaie de la récupérer depuis le réseau
      return fetch(event.request);
    })
  );
});
