# Web Platform e HTML moderno

## In questa unità impareremo

<table align="center">
<tr><td>
<details>
<summary>&#129517; <strong>Orientamento della sezione</strong></summary>

<p align="justify"><strong><span style="font-size: 1.15em;">&#128506;</span> Contesto:</strong>
Nella lezione precedente abbiamo osservato l'intera applicazione full stack: browser, protocolli, backend e database. Ora rimaniamo nel frontend e studiamo il primo documento che il server può inviare al browser: il documento HTML.</p>

<p align="justify"><strong><span style="font-size: 1.15em;">&#10067;</span> Domande guida:</strong>
Che cosa riceve il browser prima di mostrare una pagina? Come riconosce un titolo, una navigazione o il contenuto principale? Qual è la differenza tra il file HTML, il DOM e ciò che vediamo sullo schermo?</p>

<p align="justify"><strong><span style="font-size: 1.15em;">&#127919;</span> Obiettivi:</strong>
Al termine lo studente dovrà saper:</p>
<ul>
  <li>spiegare il ruolo di HTML nella Web Platform;</li>
  <li>distinguere struttura, significato, presentazione e comportamento;</li>
  <li>riconoscere elemento, tag, contenuto e attributi;</li>
  <li>scrivere lo scheletro di un documento HTML moderno;</li>
  <li>usare consapevolmente <code>lang</code>, <code>meta charset</code>, viewport e <code>title</code>;</li>
  <li>scegliere elementi semantici invece di usare <code>div</code> come contenitore universale;</li>
  <li>distinguere file sorgente, DOM e pagina visualizzata;</li>
  <li>ispezionare il DOM con gli strumenti di sviluppo del browser;</li>
  <li>costruire il primo scheletro semantico del progetto Feisbuc.</li>
</ul>

<p align="justify"><strong><span style="font-size: 1.15em;">&#10145;</span> Prossimo passo:</strong>
Dopo aver dato struttura e significato ai contenuti, useremo CSS per controllarne presentazione, layout e adattamento alle diverse dimensioni dello schermo.</p>

</details>
</td></tr>
</table>

## Dal server alla pagina visualizzata

<p align="justify">Nella lezione 00 abbiamo visto che il browser svolge il ruolo di client. Quando richiede una pagina, il server può rispondere tramite HTTP inviando un documento HTML. All'inizio quel documento non è ancora la pagina grafica che vediamo sullo schermo: è una sequenza di caratteri che descrive i contenuti e le relazioni tra essi.</p>

<p align="justify">Il browser interpreta il markup HTML, costruisce una rappresentazione ad albero chiamata <strong>DOM</strong> e usa questa struttura per produrre la pagina visualizzata. Più avanti CSS contribuirà alla presentazione e JavaScript potrà leggere o modificare il DOM.</p>

<p align="center">
  <img src="../../assets/tpsi5/01-http-html-dom.svg" alt="Il server invia HTML in una risposta HTTP; il browser interpreta il documento, costruisce il DOM e visualizza la pagina">
</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128161;</span> Idea chiave:</strong>
il file HTML, il DOM costruito dal browser e la pagina visualizzata sono tre rappresentazioni collegate, ma non sono la stessa cosa.</p>
</td></tr></table>

## Che cos'è la Web Platform

<p align="justify">La <strong>Web Platform</strong> è l'insieme delle tecnologie standard che i browser comprendono e mettono a disposizione per costruire applicazioni web. Nel frontend incontreremo soprattutto HTML, CSS, JavaScript e le API fornite dal browser.</p>

<p align="justify">Queste tecnologie collaborano, ma hanno responsabilità differenti:</p>
<ul>
  <li><strong>HTML</strong> descrive la struttura e il significato del contenuto;</li>
  <li><strong>CSS</strong> descrive la presentazione e il layout;</li>
  <li><strong>JavaScript</strong> aggiunge comportamento e interazione;</li>
  <li>le <strong>API del browser</strong> offrono al codice funzionalità come DOM, eventi, rete, storage e multimedia.</li>
</ul>

<p align="center">
  <img src="../../assets/tpsi5/01-web-platform-roles.svg" alt="Nel browser HTML si occupa di struttura e significato, CSS di presentazione e layout, JavaScript di comportamento e interazione">
</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128214;</span> Definizione — HTML:</strong>
HTML significa <em>HyperText Markup Language</em>. È un <strong>linguaggio di markup</strong>: usa marcatori per descrivere la struttura e il significato dei contenuti. Non è un linguaggio di programmazione, perché non descrive algoritmi o procedure da eseguire.</p>
</td></tr></table>

<p align="justify">La prima regola di questa parte del corso sarà quindi: prima costruiamo una struttura con un significato, poi decidiamo come appare e come si comporta.</p>

### HTML5 o HTML Living Standard?

<p align="justify">Nel linguaggio comune si usa ancora spesso il nome “HTML5” per indicare l'HTML moderno. La specifica viene però mantenuta e aggiornata dal WHATWG come <strong>HTML Living Standard</strong>. Per scrivere le nostre pagine non cambia la sintassi di base: questa distinzione ci ricorda semplicemente che lo standard continua a evolvere.</p>

<p align="justify">Riferimento ufficiale: <a href="https://html.spec.whatwg.org/">WHATWG — HTML Living Standard</a>.</p>

## Anatomia di un elemento HTML

```html
<p class="intro">Ciao Web!</p>
```

<p align="justify">Possiamo leggere questo frammento come una piccola frase strutturata:</p>
<ul>
  <li><code>p</code> è il nome del tipo di elemento;</li>
  <li><code>&lt;p class="intro"&gt;</code> è il tag di apertura;</li>
  <li><code>class="intro"</code> è un attributo formato da nome e valore;</li>
  <li><code>Ciao Web!</code> è il contenuto;</li>
  <li><code>&lt;/p&gt;</code> è il tag di chiusura;</li>
  <li>l'intera espressione è un elemento HTML.</li>
</ul>

<p align="center">
  <img src="../../assets/tpsi5/01-html-element-anatomy.svg" alt="Anatomia dell'elemento HTML p con tag di apertura, attributo class, contenuto e tag di chiusura">
</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#9888;</span> Attenzione — tag ed elemento:</strong>
un tag è una parte della sintassi, per esempio <code>&lt;p&gt;</code>. L'elemento comprende invece il tag di apertura, gli eventuali attributi, il contenuto e il tag di chiusura.</p>
</td></tr></table>

### Elementi vuoti

<p align="justify">Non tutti gli elementi racchiudono un contenuto. Alcuni sono detti <em>void elements</em>, cioè elementi vuoti, e non hanno un tag di chiusura. Due esempi che useremo presto sono <code>meta</code> e <code>img</code>.</p>

```html
<meta charset="utf-8">
<img src="ada.jpg" alt="Ada sorride davanti al suo computer">
```

### Annidamento

<p align="justify">Gli elementi possono contenere altri elementi. Questa relazione si chiama <strong>annidamento</strong>. Le aperture e le chiusure devono essere coerenti: se apriamo un elemento dentro un altro, chiudiamo prima quello più interno.</p>

```html
<p>Sto studiando <strong>HTML</strong>.</p>
```

<p align="justify">Possiamo pensarli come scatole: <code>strong</code> è contenuto dentro <code>p</code>, quindi viene chiuso prima di <code>p</code>.</p>

### Convenzioni di scrittura del corso

<p align="justify">Il browser tollera diverse varianti sintattiche, ma un progetto condiviso ha bisogno di uno stile leggibile e prevedibile. Negli esempi del corso:</p>
<ul>
  <li>scriveremo in minuscolo i nomi degli elementi e degli attributi;</li>
  <li>racchiuderemo tra virgolette i valori degli attributi;</li>
  <li>chiuderemo tutti gli elementi che prevedono un tag di chiusura;</li>
  <li>useremo l'indentazione per rendere visibile l'annidamento;</li>
  <li>sceglieremo nomi e struttura in base al significato, non all'aspetto desiderato.</li>
</ul>

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

<p align="justify">Non è un normale elemento HTML. Comunica al browser che deve interpretare il documento nella modalità standard prevista per l'HTML moderno.</p>

### `<html lang="it">`

<p align="justify"><code>html</code> è l'elemento radice: contiene l'intero documento. L'attributo <code>lang="it"</code> indica che la lingua principale è l'italiano. Questa informazione aiuta browser, motori di ricerca e tecnologie assistive a interpretare correttamente il testo.</p>

### `<head>`

<p align="justify">Contiene informazioni sul documento e collegamenti alle sue risorse. Queste informazioni sono chiamate <strong>metadati</strong> e non costituiscono il contenuto principale mostrato nella pagina.</p>

### `<meta charset="utf-8">`

<p align="justify">Dichiara UTF-8 come codifica dei caratteri. Permette di interpretare correttamente lettere accentate, simboli e caratteri appartenenti a molte lingue. Nel corso lo inseriremo sempre all'inizio di <code>head</code>.</p>

### Viewport

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

<p align="justify">Chiede al browser mobile di impostare la larghezza iniziale dell'area di visualizzazione in base alla larghezza del dispositivo, espressa in pixel CSS. Diventerà importante quando studieremo il responsive design.</p>

### `<title>`

<p align="justify">Descrive il titolo del documento e viene usato, per esempio, nella scheda del browser e nei preferiti. Non sostituisce il titolo visibile della pagina, normalmente espresso con un heading come <code>h1</code>.</p>

### `<body>`

<p align="justify">Contiene ciò che appartiene alla pagina: testo, immagini, collegamenti, moduli e strutture dell'interfaccia.</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Riferimenti MDN per lo scheletro del documento</strong></summary>

<p align="justify">Nel tutorial <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax">Basic HTML syntax</a> concentrati su anatomia degli elementi, attributi, annidamento, elementi vuoti e anatomia del documento.</p>

<p align="justify">Nel tutorial <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata">What's in the head? Web page metadata</a> studia <code>title</code>, metadati, codifica dei caratteri e lingua principale del documento.</p>

</details>
</td></tr></table>

## Testo, liste, collegamenti e immagini

<p align="justify">HTML non indica soltanto dove inizia e finisce un contenuto: ne descrive anche il ruolo. Un titolo, un paragrafo, una lista e un collegamento hanno significati differenti.</p>

```html
<h1>Profilo di Ada</h1>
<p>Sviluppatrice web.</p>

<h2>Interessi</h2>
<ul>
  <li>Web Platform</li>
  <li>Accessibilità</li>
  <li>JavaScript</li>
</ul>

<p>
  Consulta la
  <a href="https://developer.mozilla.org/">documentazione MDN</a>.
</p>

<img src="ada.jpg" alt="Ada lavora al portatile nella biblioteca della scuola">
```

<p align="justify">Un heading non si sceglie per ottenere un testo più grande: descrive la gerarchia del contenuto. La dimensione e lo stile arriveranno con CSS.</p>

<p align="justify">L'attributo <code>alt</code> descrive il contenuto o la funzione di un'immagine quando questa informazione è necessaria. Se un'immagine è puramente decorativa, useremo un testo alternativo vuoto: <code>alt=""</code>. Approfondiremo i casi possibili quando studieremo le immagini in modo sistematico.</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128161;</span> Link o pulsante?</strong>
Un link porta l'utente verso una destinazione, come un'altra pagina o una sezione. Un pulsante esegue un'azione, come pubblicare un post o aprire un menu. L'aspetto grafico non deve determinare la scelta dell'elemento.</p>
</td></tr></table>

<a id="semantica-scegliere-lelemento-per-cio-che-significa"></a>

## Semantica: scegliere l'elemento per ciò che significa

<p align="justify">Consideriamo una pagina costruita soltanto con contenitori generici:</p>

```html
<div class="header">
  <div class="menu">...</div>
</div>
<div class="content">...</div>
<div class="footer">...</div>
```

<p align="justify">Il browser riconosce tre contenitori, ma i nomi delle classi non assegnano automaticamente un significato strutturale. Possiamo esprimere meglio l'intenzione usando elementi semantici:</p>

```html
<header>
  <nav>...</nav>
</header>
<main>...</main>
<footer>...</footer>
```

<p align="justify">Gli elementi semantici rendono più esplicito il ruolo delle parti del documento per chi legge il codice, per il browser e per le tecnologie assistive.</p>

### Elementi strutturali che useremo spesso

<ul>
  <li><code>header</code>: contenuto introduttivo o intestazione di una pagina o di una sezione;</li>
  <li><code>nav</code>: una sezione che contiene collegamenti di navigazione importanti;</li>
  <li><code>main</code>: il contenuto principale e specifico del documento;</li>
  <li><code>section</code>: una sezione tematica del documento, normalmente identificata da un titolo;</li>
  <li><code>article</code>: un contenuto autonomo, per esempio un post;</li>
  <li><code>aside</code>: un contenuto collegato, ma complementare rispetto a quello principale;</li>
  <li><code>footer</code>: informazioni conclusive sulla pagina o sulla sezione a cui appartiene.</li>
</ul>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#9888;</span> Attenzione — <code>div</code> non è sbagliato:</strong>
<code>div</code> è un contenitore generico e rimane utile quando non esiste un elemento con un significato più preciso. L'errore consiste nell'usarlo automaticamente per qualsiasi blocco.</p>
</td></tr></table>

## Accessibilità: iniziamo subito

<p align="justify">L'accessibilità non sarà un'aggiunta da applicare alla fine. Alcune abitudini devono nascere insieme alla struttura HTML.</p>

<p align="justify">Da subito:</p>
<ul>
  <li>impostiamo correttamente la lingua con <code>lang</code>;</li>
  <li>costruiamo una gerarchia di heading comprensibile;</li>
  <li>usiamo elementi semantici adatti al loro scopo;</li>
  <li>forniamo alle immagini il testo alternativo appropriato;</li>
  <li>usiamo link per le destinazioni e pulsanti per le azioni;</li>
  <li>quando introdurremo i form, assoceremo ogni controllo alla sua etichetta.</li>
</ul>

## Il DOM e gli strumenti di sviluppo

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128214;</span> Definizione — DOM:</strong>
DOM significa <em>Document Object Model</em>. È la rappresentazione ad albero del documento che il browser costruisce dopo aver interpretato l'HTML. Ogni elemento, attributo e contenuto diventa parte di questa struttura.</p>
</td></tr></table>

<p align="center">
  <img src="../../assets/tpsi5/01-html-dom-tree.svg" alt="Un frammento di codice HTML di Feisbuc viene trasformato dal browser in un albero DOM con body, header, main, h1, article e p">
</p>

<p align="justify">Apri una pagina HTML e usa il pannello <strong>Elements</strong> o <strong>Inspector</strong> degli strumenti di sviluppo. Nella maggior parte dei browser puoi aprirlo con <code>F12</code>, con il menu degli strumenti per sviluppatori oppure scegliendo “Ispeziona” dal menu contestuale.</p>

<p align="justify">Con DevTools puoi:</p>
<ul>
  <li>osservare la struttura DOM prodotta dal browser;</li>
  <li>espandere e richiudere i nodi dell'albero;</li>
  <li>leggere e modificare temporaneamente contenuti e attributi;</li>
  <li>confrontare il file sorgente con la struttura interpretata;</li>
  <li>individuare il nodo coinvolto in un problema.</li>
</ul>

<p align="justify">Il browser può correggere automaticamente alcuni errori di markup. Per questo motivo “la pagina si vede” non significa necessariamente “l'HTML è corretto”. Le modifiche effettuate nel pannello Elements sono inoltre temporanee: ricaricando la pagina, il browser ricostruisce il DOM dal documento sorgente.</p>

<table align="center"><tr><td>
<details>
<summary>&#9989; <strong>Controllo aggiuntivo — validare il documento</strong></summary>

<p align="justify">Il <a href="https://validator.w3.org/nu/">Nu Html Checker</a> controlla il markup e segnala errori o avvertimenti. Il rendering nel browser e la validazione rispondono a domande diverse: il primo mostra che cosa il browser riesce a rappresentare; la seconda aiuta a verificare se il documento rispetta le regole del linguaggio.</p>

</details>
</td></tr></table>

## Esempio realistico: Feisbuc milestone 0

<p align="justify">La prima versione di Feisbuc non deve ancora essere bella e non deve avere JavaScript. Deve descrivere in modo chiaro l'intestazione, la navigazione, il contenuto principale, i post, il profilo e il piè di pagina.</p>

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
        <h3>Post di Ada</h3>
        <p>Il mio primo post semantico.</p>
      </article>
    </section>

    <section id="profilo" aria-labelledby="profilo-title">
      <h2 id="profilo-title">Profilo</h2>
      <p>Studente TPSI quinto anno.</p>
    </section>
  </main>

  <footer>
    <p>Progetto didattico TPSI</p>
  </footer>
</body>
```

<p align="justify">Ora entrambi i collegamenti della navigazione hanno una destinazione nel documento: <code>#feed</code> identifica la sezione con <code>id="feed"</code>, mentre <code>#profilo</code> identifica quella con <code>id="profilo"</code>.</p>

<p align="justify">Questo è il primo mattone di Feisbuc. Nei moduli successivi lo stesso documento riceverà CSS, layout responsive, comportamento JavaScript, REST API, database, autenticazione e funzionalità realtime.</p>

## Errori frequenti

<ol>
  <li>dimenticare <code>&lt;!doctype html&gt;</code>;</li>
  <li>omettere l'attributo <code>lang</code>;</li>
  <li>confondere <code>head</code> con l'header visibile della pagina;</li>
  <li>confondere <code>title</code> con <code>h1</code>;</li>
  <li>scegliere <code>h1</code>, <code>h2</code> o <code>h3</code> soltanto per la loro dimensione;</li>
  <li>usare <code>div</code> per qualsiasi contenitore;</li>
  <li>annidare gli elementi in modo scorretto;</li>
  <li>usare un'immagine senza decidere consapevolmente il valore di <code>alt</code>;</li>
  <li>usare un link per eseguire un'azione o un pulsante per raggiungere una destinazione;</li>
  <li>considerare il rendering visivo come prova che il markup sia corretto.</li>
</ol>

## Laboratorio

<p align="justify">La lezione può essere distribuita in tre momenti: una prima parte guidata sui concetti e sui diagrammi, circa 30 minuti per l'Activity A e circa 45 minuti per l'Activity B. Le due Activity non devono necessariamente essere completate nella stessa ora.</p>

<table align="center"><tr><td>
<details>
<summary>&#128187; <strong>Activity A — Anatomia di un documento HTML moderno</strong></summary>

<p align="justify">Parti da una pagina che il browser riesce già a visualizzare, aggiungi i metadati mancanti e confronta il file sorgente con il DOM mostrato da DevTools.</p>

<p align="justify"><a href="../../activities/tpsi5/html_anatomy_a/student/README.md">Apri la consegna dell'Activity A</a> e lavora sullo <a href="../../activities/tpsi5/html_anatomy_a/starter/index.html">starter <code>index.html</code></a>.</p>

</details>
</td></tr></table>

<table align="center"><tr><td>
<details>
<summary>&#128187; <strong>Activity B — Feisbuc semantico</strong></summary>

<p align="justify">Trasforma uno scheletro Feisbuc composto quasi soltanto da <code>div</code> in una struttura semantica. Non sostituire meccanicamente ogni <code>div</code>: scegli gli elementi in base al significato del contenuto.</p>

<p align="justify"><a href="../../activities/tpsi5/feisbuc_semantic_b/student/README.md">Apri la consegna dell'Activity B</a> e lavora sullo <a href="../../activities/tpsi5/feisbuc_semantic_b/starter/index.html">starter <code>index.html</code></a>.</p>

</details>
</td></tr></table>

## Verifica rapida

<table align="center"><tr><td>
<details>
<summary>&#9989; <strong>Checkpoint — controlla ciò che hai compreso</strong></summary>

<ol>
  <li>Quale percorso trasforma una risposta HTTP in una pagina visualizzata?</li>
  <li>Quali responsabilità hanno HTML, CSS e JavaScript?</li>
  <li>Qual è la differenza tra un tag e un elemento?</li>
  <li>Qual è la differenza tra <code>head</code> e <code>header</code>?</li>
  <li>A che cosa servono <code>lang="it"</code>, <code>meta charset</code> e viewport?</li>
  <li>Perché <code>main</code>, <code>nav</code> e <code>article</code> possono comunicare più significato di tre <code>div</code>?</li>
  <li>Quando <code>div</code> rimane una scelta corretta?</li>
  <li>Qual è la differenza tra file HTML, DOM e pagina visualizzata?</li>
  <li>Perché il fatto che una pagina sia visibile non dimostra che il markup sia corretto?</li>
</ol>

</details>
</td></tr></table>

## Sintesi

<ul>
  <li>il server può inviare HTML nel corpo di una risposta HTTP;</li>
  <li>HTML descrive struttura e significato, non l'aspetto grafico;</li>
  <li>il browser interpreta il documento e costruisce il DOM;</li>
  <li>elementi, attributi e annidamento formano il markup;</li>
  <li><code>head</code> contiene metadati, mentre <code>body</code> contiene la pagina;</li>
  <li>gli elementi semantici comunicano il ruolo delle parti del documento;</li>
  <li>DevTools mostra il DOM; un validator controlla le regole del markup;</li>
  <li>CSS controllerà l'aspetto e JavaScript il comportamento.</li>
</ul>

## Imparare a leggere MDN

<p align="justify">La dispensa costruisce il percorso didattico in italiano; MDN viene usata come documentazione tecnica di riferimento. Quando incontriamo un elemento, non dobbiamo copiare l'intera pagina: dobbiamo saper trovare le informazioni necessarie per usarlo correttamente.</p>

<p align="justify">Per ogni elemento HTML controlleremo progressivamente:</p>
<ol>
  <li>quale problema risolve e quale significato esprime;</li>
  <li>la sintassi e un esempio minimo;</li>
  <li>gli attributi importanti per il nostro caso d'uso;</li>
  <li>quali elementi può contenere e dove può essere inserito;</li>
  <li>le note di accessibilità;</li>
  <li>gli errori più frequenti e gli eventuali vincoli.</li>
</ol>

<p align="justify">Nella prossima revisione estenderemo questa lezione con una selezione esplicita degli elementi da studiare e, per ciascuno, con il collegamento alla relativa pagina MDN e l'indicazione delle sezioni e degli attributi da conoscere.</p>

## Fonti e documentazione

<ul>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content">MDN — Structuring content with HTML</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax">MDN — Basic HTML syntax</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata">MDN — What's in the head? Web page metadata</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents">MDN — Document and website structure</a>;</li>
  <li><a href="https://html.spec.whatwg.org/">WHATWG — HTML Living Standard</a>;</li>
  <li><a href="https://validator.w3.org/nu/">Nu Html Checker</a>.</li>
</ul>
