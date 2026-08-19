# Activity C — Feisbuc milestone 3

## Obiettivo

Portare Feisbuc da pagina responsive statica a piccola applicazione client-side senza server.

## Architettura richiesta

```text
posts.js
  createPost / toggleLike
       |
       v
app.js <---- storage.js
  |             |
  |             +-- localStorage + JSON
  |
  +-- form submit
  +-- renderPosts
  +-- event delegation
       |
       v
      DOM
```

## Ordine consigliato

1. completa `posts.js` e verifica manualmente le funzioni dalla console/module;
2. completa `storage.js`;
3. implementa `createPostElement()` usando `createElement` e `textContent`;
4. implementa `renderPosts()`;
5. gestisci `submit` della form;
6. aggiungi un solo listener `click` a `#post-list`;
7. verifica reload e storage corrotto.

## Definition of done

- [ ] nessun post e scritto staticamente nel feed;
- [ ] la form pubblica con mouse e tastiera tramite `submit`;
- [ ] testo vuoto/spazi non crea post;
- [ ] ogni post e un `article[data-post-id]`;
- [ ] testo utente passa da `textContent`;
- [ ] ogni like button ha `data-action="like"` e `aria-pressed`;
- [ ] un post creato dopo il caricamento puo ricevere like;
- [ ] esiste un solo listener click sul contenitore del feed;
- [ ] post e like sopravvivono al reload;
- [ ] JSON storage non valido non blocca la pagina;
- [ ] non uso `fetch`, Promise o async/await;
- [ ] `app.js`, `posts.js`, `storage.js` sono ES modules.

## Test manuale minimo

1. cancella `feisbuc.posts` dal pannello Application/Storage;
2. ricarica: deve comparire empty state;
3. pubblica `Ciao <strong>mondo</strong>`: deve comparire letteralmente il testo, non markup interpretato;
4. premi Mi piace sul nuovo post;
5. ricarica: post e like devono restare;
6. modifica manualmente `feisbuc.posts` con JSON invalido e ricarica: la pagina deve tornare a uno stato utilizzabile.

## Domande finali

- dov'e la fonte di verita del numero di like?
- perche il listener sul feed funziona anche con post creati dopo?
- perche usiamo `data-post-id` invece di un id globale per ogni pulsante?
- che cosa cambiera in UDA 23 quando i post arriveranno da un server?
