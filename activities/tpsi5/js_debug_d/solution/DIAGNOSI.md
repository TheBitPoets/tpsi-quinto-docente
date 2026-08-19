# Diagnosi di riferimento

Sono valide formulazioni diverse se collegano sintomo, causa ed evidenza.

1. **`event.preventDefault()` usa un nome non dichiarato nel listener**: il callback riceve `e`, ma usa `event`. In ambienti/browser dove non esiste un global implicito, il submit genera `ReferenceError`; anche dove esistesse sarebbe una dipendenza fragile. Fix: usare il parametro `event`/`e` ricevuto.
2. **Lo storage viene letto come array senza JSON.parse**: `localStorage.getItem()` restituisce una stringa o `null`; `saved.forEach` non e quindi valido. Fix: parse esplicito e controllo `Array.isArray`.
3. **Lo storage salva un object direttamente**: `setItem(..., { ... })` converte l'object in una stringa non JSON (`[object Object]`). Fix: conservare lo stato e usare `JSON.stringify(posts)`.
4. **I listener like vengono cercati troppo presto**: `querySelectorAll(".like-button")` gira prima di `renderSavedPosts()` e prima dei post creati dall'utente; la NodeList iniziale non si aggiorna da sola. Fix: event delegation su `#feed`.
5. **L'identita appartiene ai controlli tramite `counter`**: `post_0`/`like_button_0` legano il modello all'ordine DOM e allo stato globale. Fix: id del post (`crypto.randomUUID`) + `data-post-id`/`data-action`.
6. **Il numero di like vive soltanto nel testo del bottone**: il programma legge una cifra dal DOM e disabilita il controllo; dopo reload non esiste una fonte dati affidabile. Fix: `likes/liked` nello state, poi render.
7. **`innerHTML = text` interpreta input utente come markup**: il test `<strong>ciao</strong>` produce HTML invece di testo. Fix: `textContent` e creazione DOM esplicita.
8. **La persistenza non ha recovery**: JSON assente/corrotto puo interrompere il caricamento. Fix: `try/catch`, valore `[]` di fallback e controllo del tipo.

## Verifica finale

- submit non genera eccezioni;
- nuovi post ricevono like tramite il listener sul feed;
- il like modifica lo state e persiste al reload;
- Application/Storage mostra un array JSON;
- testo con markup viene visualizzato letteralmente;
- corrompendo il JSON la pagina torna utilizzabile con state vuoto.
