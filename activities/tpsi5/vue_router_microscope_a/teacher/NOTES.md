# Note docente — Vue Router microscope

Evidenze attese:

- `RouterLink` aggiorna la location senza document reload completo;
- `RouterView` cambia la view mantenendo il layout `App.vue`;
- back/forward percorrono le entry della session history;
- `/inesistente` e intercettata dal catch-all client e mostra `NotFoundView`;
- con HTML5 history un deep link in produzione arriva prima al server HTTP;
- Express deve servire `index.html` per le location della SPA non corrispondenti ad asset reali;
- il fallback server non sostituisce il catch-all Vue Router.

Non valutare la memorizzazione di API. Valutare la capacita di distinguere browser history, router client e HTTP server.
