const staticCacheName = 'site-static';
const dynamicCacheName = 'site-dynamic';
const precachedResources = [
'/ijalagam/static/css/styles.css',
'/ijalagam/static/css/bootstrap.min.css',
'/ijalagam/static/js/bootstrap.min.js',
'/ijalagam/static/js/popper.min.js',
'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css',
'/ijalagam/static/manifest.json',
'/ijalagam/static/assets/icon_512.png',
'/ijalagam/static/assets/icon_256.png',
'/ijalagam/static/assets/icon_128.png',
'/ijalagam/static/assets/icon_64.png',
'/ijalagam/static/assets/icon_32.png'
];
async function precache() {
  const cache = await caches.open(staticCacheName);
  return cache.addAll(precachedResources);
}


self.addEventListener('install', evt => {
  console.log('service worker installed');
  evt.waitUntil(
    precache()
  );
});

// //   // activate event
self.addEventListener('activate', evt => {
  console.log('service worker activated');
});

function isCacheable(request) {
  const url = new URL(request.url);
  return !url.pathname.endsWith(".json");
}

async function cacheFirstWithRefresh(request) {
  try {
    const fetchResponsePromise = fetch(request)
      .then(async (networkResponse) => {
        if (networkResponse.ok) {
          const cache = await caches.open(dynamicCacheName);
          cache.put(request, networkResponse.clone());
        }
        return networkResponse;
      });
  } catch (error) {
    console.log(error);
  }

  return (await caches.match(request)) || (await fetchResponsePromise);
}

self.addEventListener("fetch", (event) => {
  console.log('service worker installed');
  if (isCacheable(event.request)) {
    event.respondWith(cacheFirstWithRefresh(event.request));
  }
});

  self.addEventListener('fetch', function (event) {
    event.respondWith(
        fetch(event.request).catch(function() {
            return caches.match(event.request)
        })
    )
})