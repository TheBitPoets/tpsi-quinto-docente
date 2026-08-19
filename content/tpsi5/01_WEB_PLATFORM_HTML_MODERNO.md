# Web Platform e HTML moderno

Stato: **draft didattico**. Questa lezione inaugura UDA 21 e sostituisce la parte introduttiva di `html_css_summary` con una versione moderna, semantica e orientata alla documentazione professionale.

## Obiettivi

Al termine della lezione lo studente deve saper:

- spiegare il ruolo di HTML nella Web Platform;
- distinguere struttura, semantica e presentazione;
- riconoscere elemento, tag, contenuto e attributi;
- scrivere lo scheletro di un documento HTML moderno;
- usare `lang`, `meta charset`, `viewport` e `title` in modo consapevole;
- scegliere elementi semantici invece di usare `div` per ogni contenitore;
- leggere una pagina MDN individuando sintassi, esempi e riferimenti;
- usare DevTools per ispezionare il DOM prodotto dal browser;
- costruire il primo scheletro semantico del progetto Feisbuc.

## Prerequisiti

- saper creare e salvare file di testo;
- saper usare un browser e un editor;
- conoscenza intuitiva di pagina web, client e server;
- nessuna conoscenza HTML formale richiesta.

## Problema iniziale

Un browser riceve un documento come testo. Come fa a capire che una parte e un titolo, una parte e un menu di navigazione e un'altra e il contenuto principale?

HTML risolve proprio questo problema: **descrive la struttura e il significato del contenuto**. CSS descrivera soprattutto la presentazione; JavaScript aggiungera comportamento e interazione.

Una prima regola del corso e quindi:

> prima costruiamo una struttura con un significato, poi decidiamo come appare e come si comporta.

## HTML5 o HTML Living Standard?

Nel linguaggio comune continueremo a dire spesso "HTML5" per indicare l'HTML moderno. La specifica tecnica di riferimento e pero mantenuta come **HTML Living Standard** dal WHATWG. Questo ci permette di insegnare agli studenti una distinzione utile anche nel lavoro reale: il nome storico di una generazione tecnologica non coincide necessariamente con il modo in cui lo standard viene mantenuto oggi.

Riferimento: <https://html.spec.whatwg.org/>

## Anatomia di un elemento

```html
<p class="intro">Ciao Web!</p>
```

Possiamo leggerlo come una piccola frase strutturata:

- `p` indica il tipo di elemento;
- `<p>` e il tag di apertura;
- `</p>` e il tag di chiusura;
- `Ciao Web!` e il contenuto;
- `class="intro"` e un attributo.

Gli attributi aggiungono informazioni all'elemento. Non tutti gli elementi hanno un tag di chiusura: alcuni elementi sono *void*, per esempio `meta` e `img`.

### Annidamento

Gli elementi possono stare dentro altri elementi, ma devono essere annidati in modo coerente.

```html
<p>Sto studiando <strong>HTML</strong>.</p>
```

Pensali come scatole: se apri una scatola dentro un'altra, devi chiudere prima quella interna.

## Lo scheletro moderno di una pagina

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

### `<!doctype html>`

Non e un normale elemento HTML. Serve a far interpretare il documento al browser nella modalita standard prevista per l'HTML moderno.

### `<html lang="it">`

`html` e l'elemento radice. `lang="it"` comunica che il contenuto principale e in italiano. L'informazione e utile anche alle tecnologie assistive e ad altri strumenti che devono interpretare correttamente il testo.

### `<head>`

Contiene metadati e collegamenti a risorse del documento, non il contenuto principale mostrato nella pagina.

### `<meta charset="utf-8">`

Dichiara UTF-8 come codifica dei caratteri. Nel corso lo inseriremo sempre nei documenti HTML.

### viewport

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Dice ai browser mobili di usare come base la larghezza reale del dispositivo. Diventera importante quando studieremo responsive design.

### `<title>`

Descrive il titolo del documento, usato per esempio nella scheda del browser. Non sostituisce il titolo visibile della pagina, che puo essere espresso con un heading come `h1`.

### `<body>`

Contiene il contenuto del documento destinato alla pagina: testo, immagini, collegamenti, moduli e strutture dell'interfaccia.

Riferimenti MDN:

- Basic HTML syntax: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax>
- Web page metadata: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata>

## Semantica: scegliere l'elemento per cio che significa

Considera questa struttura:

```html
<div class="header">
  <div class="menu">...</div>
</div>
<div class="content">...</div>
<div class="footer">...</div>
```

Il browser vede contenitori generici. Possiamo esprimere meglio l'intenzione:

```html
<header>
  <nav>...</nav>
</header>
<main>...</main>
<footer>...</footer>
```

Gli elementi semantici rendono piu esplicito il ruolo delle parti del documento.

### Elementi strutturali che useremo spesso

- `header`: introduzione/intestazione di una pagina o sezione;
- `nav`: area con collegamenti di navigazione;
- `main`: contenuto principale del documento;
- `section`: sezione tematica;
- `article`: contenuto autonomo o riutilizzabile, per esempio un post;
- `aside`: contenuto complementare;
- `footer`: informazioni di chiusura.

`div` non e sbagliato: e un contenitore generico e rimane utile quando non esiste un significato semantico piu preciso.

Riferimento MDN: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents>

## Testo, liste e collegamenti

I primi elementi del vecchio `html_css_summary` rimangono validi come concetti, ma vengono riposizionati dentro una logica semantica:

```html
<h1>Profilo di Ada</h1>
<p>Sviluppatrice web.</p>

<h2>Interessi</h2>
<ul>
  <li>Web Platform</li>
  <li>Accessibilita</li>
  <li>JavaScript</li>
</ul>

<p>
  Consulta la
  <a href="https://developer.mozilla.org/">documentazione MDN</a>.
</p>
```

Un heading non va scelto per avere testo piu grande: descrive la gerarchia del contenuto. Lo stile arrivera con CSS.

## Accessibilita: iniziamo subito

Non faremo un modulo di accessibilita separato "alla fine": alcune abitudini devono nascere insieme all'HTML.

Da subito:

- impostare correttamente `lang`;
- usare heading con una gerarchia comprensibile;
- usare elementi semantici;
- fornire testo alternativo significativo alle immagini quando necessario;
- usare veri link e veri pulsanti quando servono link e pulsanti;
- in seguito associare correttamente `label` e controlli dei form.

## Imparare a leggere MDN

MDN non deve essere una pagina da copiare. Nel corso la useremo come **strumento di lavoro**.

Quando incontri un elemento o una API:

1. cerca il concetto;
2. leggi prima la descrizione breve;
3. individua sintassi e struttura;
4. prova l'esempio;
5. modifica una sola cosa e osserva l'effetto;
6. controlla le note di accessibilita o compatibilita quando sono rilevanti;
7. torna al nostro problema e riscrivilo senza copiare l'esempio.

Per il primo modulo useremo spesso il percorso MDN `Structuring content with HTML`:
<https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content>

## DevTools: il browser non vede il file come lo vedi tu

Apri una pagina HTML, premi `F12` e osserva il pannello Elements/Inspector.

Il browser ha analizzato il testo HTML e costruito una rappresentazione ad albero che piu avanti chiameremo DOM. In questa fase basta notare due cose:

- file sorgente e albero interpretato non sono concetti identici;
- il browser puo correggere automaticamente alcuni errori di markup, quindi "si vede bene" non significa necessariamente "HTML corretto".

Quando faremo debugging useremo anche un validator e gli strumenti del browser.

## Esempio minimo

```html
<!doctype html>
<html lang="it">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Prima pagina</title>
  </head>
  <body>
    <header>
      <h1>Prima pagina</h1>
    </header>
    <main>
      <p>Sto imparando a descrivere il contenuto, non a decorarlo.</p>
    </main>
  </body>
</html>
```

## Esempio realistico: Feisbuc milestone 0

La prima versione di Feisbuc non deve ancora essere bella e non deve ancora avere JavaScript. Deve essere **strutturata bene**.

```html
<body>
  <header>
    <h1>Feisbuc</h1>
    <nav aria-label="Navigazione principale">
      <a href="#feed">Feed</a>
      <a href="#profilo">Profilo</a>
    </nav>
  </header>

  <main>
    <section id="feed" aria-labelledby="feed-title">
      <h2 id="feed-title">Feed</h2>

      <article>
        <h3>Ada</h3>
        <p>Il mio primo post semantico.</p>
      </article>
    </section>
  </main>

  <footer>
    <p>Progetto didattico TPSI</p>
  </footer>
</body>
```

Questo e il primo mattone del capstone. Nei moduli successivi lo stesso documento ricevera CSS, layout responsive, comportamento JavaScript, REST API, database, autenticazione e realtime.

## Confronto con il materiale legacy

| Elemento legacy | Decisione | Evoluzione nel corso |
| --- | --- | --- |
| scheletro `html/head/body` | reuse + rewrite | aggiungere doctype, `lang`, charset, viewport e spiegazione semantica |
| `p`, `ol`, `ul`, `a` | reuse | esempi nuovi e semanticamente corretti |
| uso di `div` | keep with context | usare `div` quando serve un contenitore generico, non come default universale |
| JSFiddle | keep as legacy tool | affiancare MDN Playground e file/repo locali |
| esempio `<ul>` con `<ol>` | retire/fix | sostituire con esempio corretto |
| HTML orientato all'aspetto | rewrite | separare struttura HTML e presentazione CSS |

Provenienza legacy: `TheBitPoets/html_css_summary` @ `d71da420f1aa2ea39b61356e4f9900c6371e7a42`.

## Errori frequenti

1. dimenticare `<!doctype html>`;
2. omettere `lang`;
3. pensare che `head` sia l'header grafico della pagina;
4. usare `h1/h2/...` solo per ottenere una dimensione del testo;
5. usare `div` per qualsiasi cosa;
6. annidare male gli elementi;
7. usare un'immagine senza considerare `alt`;
8. confondere `title` con `h1`;
9. copiare esempi dalla documentazione senza capire il problema che risolvono;
10. considerare il rendering visivo come prova che il markup sia corretto.

## Esercizi graduati A-F

### A — osserva e modifica

Apri lo starter dell'Activity `tpsi5-activity-a-html-anatomy-001`, aggiungi i metadati mancanti e osserva il DOM con DevTools.

### B — modifica controllata

Nell'Activity `tpsi5-activity-b-feisbuc-semantic-001`, trasforma uno scheletro Feisbuc composto quasi soltanto da `div` in una struttura semantica.

### C — scrittura autonoma

Progetta da zero la struttura HTML di una pagina profilo senza copiare gli starter. Sara formalizzata in una Activity successiva.

### D — debugging

Riceverai un documento con nesting scorretto, heading incoerenti e problemi di accessibilita da diagnosticare.

### E — mini-progetto

Costruisci due pagine semanticamente coerenti con navigazione reciproca.

### F — prodotto integrato

Feisbuc crescera fino a diventare l'applicazione full stack del corso.

## Laboratorio

Le prime due Activity sono pensate per lavorare in locale con browser + editor e per essere registrabili da TheBitLab. Il grader HTML/browser generico di 2cornot2c e ancora pianificato: in questa fase la valutazione e guidata da checklist e rubrica docente, senza simulare test automatici inesistenti.

## Verifica rapida

1. Perche HTML non dovrebbe descrivere principalmente l'aspetto grafico?
2. Qual e la differenza tra `head` e `header`?
3. A cosa serve `lang="it"`?
4. Perche `main`, `nav` e `article` possono essere migliori di tre `div` generici?
5. Quando `div` resta una scelta corretta?
6. Che differenza c'e tra il file HTML e cio che osservi nel pannello Elements?

## Sintesi inclusiva

```text
HTML = struttura + significato

Documento
├── doctype
└── html lang="it"
    ├── head
    │   ├── charset
    │   ├── viewport
    │   └── title
    └── body
        ├── header
        ├── nav
        ├── main
        │   ├── section
        │   └── article
        └── footer

CSS        -> aspetto/layout
JavaScript -> comportamento
HTTP       -> comunicazione client/server
```

## Fonti e collegamenti

- MDN — Structuring content with HTML: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content>
- MDN — Basic HTML syntax: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax>
- MDN — Web page metadata: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata>
- MDN — Structuring documents: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents>
- WHATWG — HTML Living Standard: <https://html.spec.whatwg.org/>
- Legacy snapshot: `TheBitPoets/html_css_summary@d71da420f1aa2ea39b61356e4f9900c6371e7a42`

## Activity correlate

- `tpsi5-activity-a-html-anatomy-001`
- `tpsi5-activity-b-feisbuc-semantic-001`
