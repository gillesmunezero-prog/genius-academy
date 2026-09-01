const CACHE_NAME = 'genius-academy-v5';
const CORE_ASSETS = [
'./',
'./index.html',
'./manifest.json',
'./icons/icon-192.png',
'./icons/icon-512.png',
'./icons/icon-maskable-512.png',
'./icons/apple-touch-icon.png',
'./curriculum/maths.json',
'./curriculum/francais.json',
'./curriculum/anglais.json',
'./curriculum/geographie.json',
'./curriculum/lecture.json',
'./curriculum/sciences.json',
'./curriculum/histoire.json',
'./curriculum/informatique.json',
'./curriculum/echecs.json',
'./curriculum/arts.json',
'./curriculum/viepratique.json',
'./curriculum/conversations_anglais.json',
'./curriculum/version.json'
];

self.addEventListener('install', function(event){
event.waitUntil(
caches.open(CACHE_NAME).then(function(cache){
return Promise.all(CORE_ASSETS.map(function(url){
return cache.add(url).catch(function(){ /* ignore missing assets */ });
}));
})
);
self.skipWaiting();
});

self.addEventListener('activate', function(event){
event.waitUntil(
caches.keys().then(function(keys){
return Promise.all(keys.filter(function(k){ return k !== CACHE_NAME; }).map(function(k){ return caches.delete(k); }));
})
);
self.clients.claim();
});

// Strategie : reseau d'abord (pour avoir les cours et l'appli a jour apres
// chaque deploiement), puis cache si hors-ligne. 'cache: reload' force le
// navigateur a revalider aupres du serveur plutot que de reutiliser une
// reponse HTTP deja en cache disque, pour eviter tout index.html/curriculum
// perime meme quand le SW lui-meme est a jour.
self.addEventListener('fetch', function(event){
if (event.request.method !== 'GET') return;
event.respondWith(
fetch(event.request, { cache: 'reload' }).then(function(response){
if (response && response.ok) {
var copy = response.clone();
caches.open(CACHE_NAME).then(function(cache){ cache.put(event.request, copy); });
}
return response;
}).catch(function(){
return caches.match(event.request).then(function(cached){
return cached || caches.match('./index.html');
});
})
);
});
