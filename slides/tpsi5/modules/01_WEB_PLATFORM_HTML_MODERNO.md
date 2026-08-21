---
marp: true
paginate: true
size: 16:9
title: 01 — Web Platform e HTML moderno
---

# 01 — Web Platform e HTML moderno
## Struttura, semantica e documento

UDA 21 — Frontend foundations

---

# Richiamo

Nel modulo 00 abbiamo separato:

```text
browser ↔ HTTP ↔ backend ↔ database
```

Oggi restiamo nel browser e rispondiamo a una domanda:

> Che cosa riceve davvero il browser prima che esista una pagina “visiva”?

---

# Obiettivi

Alla fine dovrai saper:

- riconoscere la struttura minima di un documento HTML;
- distinguere struttura da presentazione;
- usare elementi semantici;
- spiegare il ruolo di metadata e landmark;
- leggere il DOM con DevTools;
- migliorare la prima pagina Feisbuc.

---

# HTML non è “grafica”

HTML descrive **che cosa è** un contenuto.

```html
<h1>Feisbuc</h1>
<p>Il tuo feed didattico</p>
```

CSS descriverà come appare.
JavaScript descriverà come reagisce.

Separare i ruoli ci rende più bravi a fare debug.

---

# Documento minimo moderno

```html
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Feisbuc</title>
</head>
<body>
  <h1>Feisbuc</h1>
</body>
</html>
```

Quali righe servono al browser? Quali servono agli utenti?

---

# Semantica: dire che cosa significa

Confronta:

```html
<div class="top">...</div>
<div class="menu">...</div>
<div class="main">...</div>
```

con:

```html
<header>...</header>
<nav>...</nav>
<main>...</main>
```

Il secondo documento comunica meglio struttura e responsabilità.

---

# Un post Feisbuc

```html
<article>
  <header>
    <h2>Mario Rossi</h2>
    <time datetime="2026-09-12T10:15">10:15</time>
  </header>
  <p>Primo post del corso.</p>
</article>
```

Perché `article` è più informativo di un `div`?

---

# Form: struttura di un'interazione

```html
<form>
  <label for="post-text">Nuovo post</label>
  <textarea id="post-text" name="text"></textarea>
  <button type="submit">Pubblica</button>
</form>
```

Nota:

- label collegata;
- `name` utile al dato;
- button con tipo esplicito.

---

# Metadata e viewport

```html
<meta charset="utf-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1">
```

Senza viewport, un layout mobile può essere interpretato come una pagina desktop rimpicciolita.

HTML prepara già il terreno al responsive design.

---

# DevTools: leggere il documento vero

Il file sorgente e il DOM non sono sempre identici.

Con DevTools puoi:

- ispezionare elementi;
- vedere la struttura DOM;
- modificare attributi temporaneamente;
- controllare accessibilità di base;
- capire quale nodo è coinvolto in un problema.

---

# Errore tipico: div soup

```html
<div>
  <div>
    <div>Mario</div>
    <div>Testo del post</div>
  </div>
</div>
```

Problema: il browser lo renderizza, ma il significato è quasi tutto perso.

Correzione: usare elementi semantici quando descrivono davvero il contenuto.

---

# Checkpoint

Scegli l'elemento più adatto:

1. contenuto principale della pagina;
2. blocco indipendente di un post;
3. collegamenti di navigazione;
4. data/ora di pubblicazione;
5. campo con etichetta per scrivere il post.

Motiva ogni scelta.

---

# Feisbuc milestone

Obiettivo pratico:

- costruire uno skeleton semantico;
- header/nav/main riconoscibili;
- feed fatto di `article`;
- form accessibile;
- struttura pronta a ricevere CSS.

Non serve ancora “farlo bello”.

---

# Handoff al laboratorio

Durante l'Activity:

1. osserva un documento;
2. identifica semantica debole;
3. rifattorizza senza cambiare il significato funzionale;
4. verifica con DevTools;
5. spiega perché la nuova struttura è migliore.

---

# Recap

HTML moderno significa:

- documento valido;
- semantica esplicita;
- metadata corretti;
- form comprensibili;
- struttura leggibile da persone e strumenti.

Prossimo modulo: **CSS moderno e responsive design**.