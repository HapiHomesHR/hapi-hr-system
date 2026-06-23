self.addEventListener("install", event => {
  console.log("Hapi HR Service Worker installed");
});

self.addEventListener("fetch", event => {
  event.respondWith(fetch(event.request));
});