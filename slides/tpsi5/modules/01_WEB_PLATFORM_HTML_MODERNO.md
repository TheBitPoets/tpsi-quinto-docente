---
marp: true
paginate: true
size: 16:9
title: 01 — Web Platform e HTML moderno
---

# 01 — Web Platform e HTML moderno
## Dal documento ricevuto alla struttura della pagina

UDA 21 — Frontend foundations

---

# Richiamo dalla lezione 00

Abbiamo separato:

```text
browser ↔ HTTP ↔ server ↔ database
```

Oggi seguiamo un solo passaggio:

> Che cosa succede quando il server invia un documento HTML al browser?

---

# Obiettivi

Alla fine dovrai saper:

- collocare HTML nella Web Platform;
- riconoscere elementi, tag, attributi e annidamento;
- costruire un documento HTML moderno;
- usare elementi semantici;
- distinguere file sorgente, DOM e pagina visualizzata;
- ispezionare il DOM con DevTools;
- costruire la milestone 0 di Feisbuc.

---

![bg contain](../../../assets/tpsi5/01-http-html-dom.svg)

---

# Tre rappresentazioni collegate

## File HTML

Testo sorgente scritto dallo sviluppatore o inviato dal server.

## DOM

Albero di nodi costruito dal browser interpretando il markup.

## Pagina visualizzata

Risultato prodotto dal browser usando DOM, regole CSS e altre informazioni.

> Sono collegate, ma non sono la stessa cosa.

---

![bg contain](../../../assets/tpsi5/01-web-platform-roles.svg)

---

# HTML è un linguaggio di markup

**HTML** significa *HyperText Markup Language*.

Descrive:

- che cosa è un contenuto;
- come è strutturato;
- quali relazioni ha con gli altri contenuti.

Non descrive algoritmi o procedure: **non è un linguaggio di programmazione**.

---

![bg contain](../../../assets/tpsi5/01-html-element-anatomy.svg)

---

# Annidamento ed elementi vuoti

Un elemento può contenerne un altro:

```html
<p>Sto studiando <strong>HTML</strong>.</p>
```

Le chiusure devono rispettare l'ordine delle aperture.

Alcuni elementi non racchiudono contenuto e non hanno tag di chiusura:

```html
<meta charset="utf-8">
<img src="ada.jpg" alt="Ada sorride davanti al computer">
```

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

---

# Che cosa appartiene a `head`?

- `meta charset` → codifica dei caratteri;
- `meta viewport` → area iniziale sui dispositivi mobili;
- `title` → titolo del documento e della scheda;
- altri metadati e collegamenti a risorse.

`head` non è l'intestazione grafica della pagina.

```text
head   → informazioni sul documento
header → intestazione visibile di una pagina o sezione
```

---

# Il contenuto dentro `body`

```html
<h1>Profilo di Ada</h1>
<p>Sviluppatrice web.</p>

<h2>Interessi</h2>
<ul>
  <li>Web Platform</li>
  <li>Accessibilità</li>
</ul>

<a href="https://developer.mozilla.org/">Consulta MDN</a>
```

Gli heading descrivono la gerarchia, non la dimensione del testo.

---

# Semantica: dire che cosa significa

Confronta:

```html
<div class="header">...</div>
<div class="menu">...</div>
<div class="main">...</div>
```

con:

```html
<header>...</header>
<nav>...</nav>
<main>...</main>
```

Il secondo documento rende espliciti i ruoli delle parti.

---

# Elementi strutturali

- `header` → contenuto introduttivo;
- `nav` → navigazione importante;
- `main` → contenuto principale;
- `section` → sezione tematica, normalmente con un titolo;
- `article` → contenuto autonomo, come un post;
- `aside` → contenuto complementare;
- `footer` → informazioni conclusive.

> `div` rimane corretto quando serve davvero un contenitore generico.

---

# Accessibilità fin dall'inizio

- dichiarare la lingua con `lang`;
- costruire una gerarchia di heading coerente;
- usare elementi semantici;
- decidere consapevolmente il valore di `alt`;
- usare link per le destinazioni;
- usare pulsanti per le azioni.

```html
<img src="ada.jpg" alt="Ada lavora al portatile">
```

Un'immagine puramente decorativa usa `alt=""`.

---

![bg contain](../../../assets/tpsi5/01-html-dom-tree.svg)

---

# DevTools: osservare il DOM

Nel pannello **Elements/Inspector** puoi:

- espandere i nodi dell'albero;
- leggere elementi e attributi;
- modificare temporaneamente il DOM;
- confrontare sorgente e struttura interpretata;
- individuare il nodo coinvolto in un problema.

Il browser può correggere alcuni errori di markup.

> “Si vede” non significa automaticamente “è corretto”.

---

# Rendering e validazione

Sono due controlli differenti:

| Rendering nel browser | Nu Html Checker |
|---|---|
| mostra ciò che il browser rappresenta | controlla le regole del markup |
| può tollerare o correggere errori | segnala errori e avvertimenti |
| serve anche al debug visivo | serve alla verifica strutturale |

Validator: `https://validator.w3.org/nu/`

---

# Feisbuc milestone 0

```html
<header>
  <h1>Feisbuc</h1>
  <nav aria-label="Navigazione principale">
    <a href="#feed">Feed</a>
    <a href="#profilo">Profilo</a>
  </nav>
</header>
<main>
  <section id="feed">...</section>
  <section id="profilo">...</section>
</main>
<footer>...</footer>
```

Ogni collegamento interno deve avere una destinazione esistente.

---

# Handoff al laboratorio

## Activity A — Anatomia del documento

Osserva → modifica → ricarica → confronta sorgente e DOM → spiega.

## Activity B — Feisbuc semantico

Trasforma la “div soup” scegliendo ogni elemento in base al significato.

Vincoli comuni:

- nessun CSS;
- nessun JavaScript;
- le scelte devono essere motivate.

---

# Checkpoint

1. Qual è il percorso dalla risposta HTTP alla pagina?
2. Quali ruoli hanno HTML, CSS e JavaScript?
3. Qual è la differenza tra tag ed elemento?
4. Qual è la differenza tra `head` e `header`?
5. Quando `div` è ancora corretto?
6. Che differenza c'è tra sorgente e DOM?
7. Perché “si vede bene” non prova che l'HTML sia corretto?

---

# Recap

- HTML descrive struttura e significato;
- il browser interpreta il markup e costruisce il DOM;
- il documento moderno contiene metadati essenziali;
- gli elementi semantici comunicano il ruolo dei contenuti;
- accessibilità e validazione iniziano subito;
- Feisbuc parte da una struttura corretta, non dall'aspetto.

Prossimo modulo: **CSS moderno e responsive design**.
