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
- usare attributi normali e booleani;
- costruire un documento HTML moderno;
- descrivere i metadati principali di `head`;
- usare elementi semantici;
- distinguere file sorgente, DOM e pagina visualizzata;
- ispezionare il DOM con DevTools;
- costruire la milestone 0 di Feisbuc.

---

![bg contain](../../../assets/tpsi5/01-mdn-basic-html-coverage.svg)

---

![bg contain](../../../assets/tpsi5/01-mdn-metadata-coverage.svg)

---

![bg contain](../../../assets/tpsi5/01-mdn-semantics-coverage.svg)

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

# Attributi

Gli attributi aggiungono informazioni all'elemento e si scrivono nel tag di apertura:

```html
<p class="introduzione" lang="it">Benvenuti.</p>
```

- spazio dopo il nome dell'elemento;
- nome dell'attributo;
- segno `=`;
- valore tra virgolette;
- spazi tra attributi diversi.

[MDN — Attributes](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#attributes)

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

[MDN — Nesting](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#nesting_elements) · [MDN — Void elements](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#void_elements)

---

# Attributi booleani e virgolette

La presenza di un attributo booleano rappresenta il valore vero:

```html
<input id="nome" name="nome" disabled>
```

`disabled="false"` non significa falso: l'attributo è presente.

Negli esempi del corso useremo sempre virgolette doppie:

```html
<a href="profilo.html" title="Profilo di Ada">Profilo</a>
```

[MDN — Boolean attributes](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#boolean_attributes)

---

# Spazi, caratteri speciali e commenti

- gli spazi consecutivi vengono normalmente ridotti a uno;
- l'indentazione rende visibile l'annidamento;
- i caratteri della sintassi si rappresentano con riferimenti come `&lt;` e `&amp;`;
- i commenti restano nel sorgente, ma non vengono visualizzati.

```html
<!-- Navigazione principale -->
<p>Un paragrafo si scrive con &lt;p&gt; e &lt;/p&gt;.</p>
```

[MDN — Whitespace](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#whitespace_in_html) · [Character references](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#character_references_including_special_characters_in_html) · [Comments](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#html_comments)

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

[MDN — What is the HTML head?](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata#what_is_the_html_head)

---

# Metadati descrittivi

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="Classe 5A Informatica">
<meta name="description" content="Progetto full stack Feisbuc">
```

- `charset` → codifica;
- `name` → tipo di metadato;
- `content` → valore del metadato;
- `keywords` → vecchio metadato ignorato dai motori di ricerca.

[MDN — The meta element](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata#metadata_the_meta_element)

---

# Favicon, CSS e JavaScript

```html
<head>
  <link rel="icon" href="/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="css/style.css">
  <script src="js/app.js" defer></script>
</head>
```

`link` è un elemento vuoto. `script` **non** lo è e richiede `</script>`.

[MDN — Custom icons](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata#adding_custom_icons_to_your_site) · [CSS and JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata#applying_css_and_javascript_to_html)

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

[MDN — Adding features](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#adding_some_features_to_an_html_document)

---

# Immagini: attributi da conoscere

```html
<img
  src="images/ada.jpg"
  alt="Ada collega un cavo di rete al computer"
  width="1200"
  height="800">
```

- `src` → risorsa da caricare;
- `alt` → sostituzione testuale;
- `width` e `height` → dimensioni intrinseche e spazio riservato;
- `loading="lazy"` → caricamento differito, quando appropriato.

[MDN — `<img>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img) · [Tutorial sugli attributi di `img`](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#adding_attributes_to_an_element)

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

[MDN — HTML layout elements](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents#html_layout_elements_in_more_detail)

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

[MDN — HTML accessibility](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML)

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

[MDN — DOM Inspector](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Tools_and_setup/What_are_browser_developer_tools#the_inspector_dom_explorer_and_css_editor)

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
4. Come riconosci un attributo booleano?
5. Qual è la differenza tra `head` e `header`?
6. Che cosa descrivono `name` e `content` in un elemento `meta`?
7. Quali attributi devi conoscere per `img`?
8. Quando `div` è ancora corretto?
9. Che differenza c'è tra sorgente e DOM?
10. Perché “si vede bene” non prova che l'HTML sia corretto?

---

# Recap

- HTML descrive struttura e significato;
- il browser interpreta il markup e costruisce il DOM;
- il documento moderno contiene metadati essenziali;
- attributi, spazi, riferimenti a caratteri e commenti hanno regole precise;
- `head` collega anche favicon, CSS e JavaScript;
- gli elementi semantici comunicano il ruolo dei contenuti;
- accessibilità e validazione iniziano subito;
- Feisbuc parte da una struttura corretta, non dall'aspetto.

Prossimo modulo: **CSS moderno e responsive design**.
