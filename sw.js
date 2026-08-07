const CACHE_NAME = 'genius-academy-v4';
const CORE_ASSETS = [
'./',
'./index.html',
'./manifest.json',
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

// Strategie : reseau d'abord (pour avoir les cours a jour), puis cache si hors-ligne.
self.addEventListener('fetch', function(event){
if (event.request.method !== 'GET') return;
event.respondWith(
fetch(event.request).then(function(response){
var copy = response.clone();
caches.open(CACHE_NAME).then(function(cache){ cache.put(event.request, copy); });
return response;
}).catch(function(){
return caches.match(event.request).then(function(cached){
return cached || caches.match('./index.html');
});
})
);
});
