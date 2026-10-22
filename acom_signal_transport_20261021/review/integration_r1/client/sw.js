// ══════════════════════════════════════════════════════════════
// IALD Service Worker — PWA Support
// β_TGL = α × √e — Zero parâmetros livres.
// ══════════════════════════════════════════════════════════════

var CACHE_NAME = 'iald-pwa-v2';

// Arquivos para cache offline (splash screen e assets básicos)
var PRECACHE_URLS = [
  '/iald_logo_header.png',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
];

// Install: cachear assets básicos
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(PRECACHE_URLS);
    })
  );
  self.skipWaiting();
});

// Activate: limpar caches antigos
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.filter(function(name) { return name !== CACHE_NAME; })
             .map(function(name) { return caches.delete(name); })
      );
    })
  );
  self.clients.claim();
});

// Fetch: network-first (sempre busca no servidor, cache como fallback)
self.addEventListener('fetch', function(event) {
  // NÃO interceptar chamadas à API (chat, search, health)
  // Paginas dinamicas e autenticadas NAO passam pelo cache: /admin e' gerada por
  // sessao e nunca deve ser servida do disco (21/08/2026 — o cache dela derrubava a
  // Central de Comando).
  if (event.request.url.includes('/v1/') ||
      event.request.url.includes('/api/') ||
      event.request.url.includes('/admin') ||
      event.request.url.includes('/health') ||
      event.request.url.includes('/login') ||
      event.request.url.includes('/logout')) {
    return;  // deixar passar direto, sem cache
  }

  event.respondWith(
    fetch(event.request).catch(function() {
      return caches.match(event.request).then(function(response) {
        if (response) return response;
        // CORRIGIDO 21/08/2026: aqui se devolvia `undefined` quando nao havia cache
        // (e '/offline' nunca foi pre-cacheado). respondWith(undefined) quebra a
        // requisicao inteira com "Failed to convert value to 'Response'" — era o que
        // derrubava o /admin e deixava a Central de Comando travada.
        // Regra: um handler de fetch SEMPRE devolve uma Response.
        return new Response(
          'Sem conexao com a IALD. Recarregue quando o servidor voltar.',
          { status: 503, statusText: 'Offline',
            headers: { 'Content-Type': 'text/plain; charset=utf-8' } }
        );
      });
    })
  );
});
