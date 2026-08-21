---
marp: true
paginate: true
size: 16:9
title: 09 — SSR e template server-side
---

# 09 — SSR e template server-side
## Stesso dominio, altra responsabilità di rendering

UDA 24 — Backend

---

# Richiamo

Feisbuc oggi ha:

```text
browser client
→ API JSON
→ Express
→ auth/session
→ SQLite
```

Ma chi deve produrre l'HTML?

Finora: il browser.
Oggi proviamo: il server.

---

# Obiettivi

Alla fine dovrai saper:

- distinguere client rendering e server-side rendering;
- costruire un view model;
- spiegare template e autoescape;
- usare il pattern POST/Redirect/GET;
- capire come API e SSR possano convivere;
- confrontare trade-off senza trasformare SSR in “stack nuovo”.

---

# Due strategie

## Client rendering

```text
GET /posts -> JSON -> JS -> DOM
```

## Server rendering

```text
GET /feed -> HTML già renderizzato
```

Stesso dominio, diversa responsabilità.

---

# Nunjucks

Template:

```html
{% for post in posts %}
  <article>
    <h2>{{ post.author }}</h2>
    <p>{{ post.text }}</p>
  </article>
{% endfor %}
```

Il server combina dati + template e produce HTML.

---

# View model

Non passare “tutto il database” alla view.

Meglio costruire il dato che serve davvero:

```js
const viewModel = {
  currentUser,
  posts,
  canCreate: Boolean(currentUser)
};
```

La view riceve un contratto pensato per il rendering.

---

# Autoescape

Se un utente scrive:

```html
<script>alert('xss')</script>
```

un template con autoescape deve mostrarlo come testo, non eseguirlo.

L'escaping è parte del boundary dati → HTML.

---

# Form SSR

```html
<form method="post" action="/posts">
  <textarea name="text"></textarea>
  <button>Pubblica</button>
</form>
```

Il browser può inviare form standard senza JavaScript personalizzato.

---

# POST / Redirect / GET

Dopo il POST:

```text
POST /posts
→ 303 See Other
→ GET /feed
```

Vantaggio: refresh della pagina non ripete facilmente la stessa mutazione.

---

# API e SSR possono convivere

```text
/posts        -> API JSON
/feed         -> HTML SSR
```

Entrambi possono usare:

- stesso dominio;
- stesso PostStore;
- stessa sessione;
- stesse regole authz.

Non duplicare logica di business nel template.

---

# Errore tipico: logica nella view

Da evitare:

```text
if utente X e post Y e ruolo Z allora...
```

La view dovrebbe soprattutto **presentare** decisioni già preparate dal backend/view model.

---

# Confronto

Client rendering:

- più interattività locale;
- API esplicita;
- più JS browser.

SSR:

- HTML pronto dal server;
- form/navigation semplici;
- meno dipendenza da JS per il primo rendering.

Non esiste una risposta sempre migliore.

---

# Checkpoint

Per ogni responsabilità, scegli API/client o SSR/server:

1. generare markup iniziale;
2. decidere ownership;
3. leggere post dal DB;
4. escape di testo nel template;
5. aggiornare dinamicamente senza reload;
6. redirect dopo form POST.

---

# Feisbuc milestone

Feisbuc dimostra due vie sopra lo stesso backend:

```text
API JSON + client render
        oppure
SSR Nunjucks
```

Auth, store e dominio restano stabili.

Prossimo salto: frontend framework / SPA.

---

# Handoff al laboratorio

Durante le Activity:

1. costruisci un view model;
2. prova autoescape;
3. implementa/formula un flusso PRG;
4. confronta API e SSR;
5. diagnostica una responsabilità finita nel layer sbagliato.

---

# Recap

SSR insegna che:

- rendering è una responsabilità spostabile;
- il dominio non deve dipendere dal template;
- autoescape protegge il boundary HTML;
- PRG rende i form più robusti;
- API e SSR possono condividere backend e sessione.

Prossimo modulo: **Vue 3 e prima SPA Feisbuc**.