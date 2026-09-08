<a id="lesson-start"></a>
# CSS moderno, layout e responsive design

<a id="lesson-objectives"></a>
## In questa unità impareremo

<table align="center"><tr><td>
<details>
<summary>&#129517; <strong>Orientamento della sezione</strong></summary>

<p align="justify"><strong><span style="font-size: 1.15em;">&#128506;</span> Contesto:</strong>
la lezione precedente ha dato struttura e significato alla pagina. Ora dobbiamo controllarne presentazione e layout senza compromettere semantica, leggibilità e adattamento allo spazio disponibile.</p>

<p align="justify"><strong><span style="font-size: 1.15em;">&#10067;</span> Domande guida:</strong>
come decide il browser quale dichiarazione CSS applicare? Quando conviene Flexbox e quando Grid? Come si costruisce un layout che reagisce al contenuto invece che a un elenco di dispositivi?</p>

<p align="justify"><strong><span style="font-size: 1.15em;">&#127919;</span> Obiettivi:</strong>
Al termine lo studente dovrà saper:</p>
<ul>
  <li>spiegare il ruolo di CSS nella Web Platform senza confonderlo con HTML;</li>
  <li>leggere e scrivere regole CSS composte da selettore, proprietà e valore;</li>
  <li>prevedere il risultato di conflitti semplici usando cascade, specificità e ordine;</li>
  <li>usare il box model e <code>box-sizing: border-box</code> in modo consapevole;</li>
  <li>distinguere normal flow, <code>block</code>, <code>inline</code> e contenitori di layout;</li>
  <li>scegliere Flexbox per problemi prevalentemente monodimensionali;</li>
  <li>scegliere Grid per layout bidimensionali;</li>
  <li>costruire layout che si adattano al viewport invece di fissare larghezze rigide;</li>
  <li>usare media query solo quando il layout fluido da solo non basta;</li>
  <li>definire e riusare custom properties CSS;</li>
  <li>diagnosticare overflow, specificità e breakpoint errati con DevTools;</li>
  <li>realizzare la milestone responsive iniziale di Feisbuc.</li>
</ul>

<p align="justify"><strong><span style="font-size: 1.15em;">&#129504;</span> Prerequisiti:</strong></p>
<ul>
  <li>aver completato la lezione <a href="01_WEB_PLATFORM_HTML_MODERNO.md">Web Platform e HTML moderno</a>;</li>
  <li>saper riconoscere una struttura semantica con <code>header</code>, <code>nav</code>, <code>main</code>, <code>section</code>, <code>article</code> e <code>footer</code>;</li>
  <li>saper usare le funzioni essenziali dei browser DevTools;</li>
  <li>non è richiesta alcuna conoscenza di Bootstrap.</li>
</ul>

<p align="justify"><strong><span style="font-size: 1.15em;">&#10145;</span> Prossimo passo:</strong>
nella lezione 03 confronteremo il CSS scritto direttamente con le convenzioni e i componenti di Bootstrap.</p>

</details>
</td></tr></table>

<a id="lesson-mdn-maps"></a>
## Orientamento nella documentazione MDN

<p align="justify">La dispensa costruisce un percorso guidato in italiano, mentre MDN rimane la documentazione tecnica da imparare a consultare. Se è la prima volta che la usi, apri prima la <a href="GUIDA_USO_MDN.md">guida trasversale a MDN</a>. La mappa e l'indice seguenti mostrano quali argomenti studiare ora e quali riconoscere per un approfondimento successivo.</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128506;</span> Come leggere i colori:</strong>
<strong>coperto</strong> indica i contenuti spiegati dalla dispensa e richiesti in questa lezione; <strong>introdotto</strong> segnala una prima presentazione da riconoscere o sperimentare; <strong>più avanti</strong> identifica gli argomenti esclusi dallo studio attuale. Ogni stato è scritto anche accanto al colore, che non è quindi l'unico segnale.</p>
</td></tr></table>

<a id="lesson-mdn-map-css"></a>
<table align="center"><tr><td>
<details>
<summary>&#128506;&#65039; <strong>Mappa — CSS moderno, layout e responsive design</strong></summary>

<p align="justify">La mappa collega i nuclei della dispensa alle pagine e alle sezioni MDN corrispondenti. Le frecce verdi indicano ciò che viene spiegato in italiano, la freccia ambra una prima introduzione e quella grigia gli argomenti esclusi dallo studio attuale.</p>

<p align="center">
  <img src="../../assets/tpsi5/02-mdn-css-coverage.svg" alt="Mappa tra i paragrafi della dispensa su CSS moderno, layout e responsive design e le pagine MDN corrispondenti. La legenda distingue contenuti coperti, introdotti e rimandati">
</p>

</details>
</td></tr></table>

<a id="lesson-mdn-cross-index"></a>
<table align="center" width="100%"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato navigabile — Dispensa ↔ MDN</strong></summary>

<p align="justify">L’indice è organizzato in gruppi espandibili e in schede abbinate. In ogni scheda, il titolo della dispensa conduce al punto esatto della lezione e il titolo MDN apre la documentazione corrispondente. Le descrizioni sono brevi punti elenco e non sono cliccabili.</p>

<p><strong>Legenda:</strong> &#128309; contenuto della dispensa · &#128994; contenuto MDN · una voce in corsivo segnala che non esiste una corrispondenza diretta.</p>

<details>
<summary><strong>Orientamento e fondamenti</strong> · 4 voci</summary>

<blockquote>
<p><strong>01 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-objectives">In questa unità impareremo</a></strong></p>
<ul><li>Contesto, domande guida, obiettivi e prerequisiti.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<em>Nessun riferimento MDN diretto per questa voce.</em></p>
</blockquote>

<blockquote>
<p><strong>02 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-mdn-map-css">Mappa — CSS moderno, layout e responsive design</a></strong></p>
<ul><li>Raccordo visuale fra i nuclei della dispensa e le fonti MDN.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics">CSS styling basics</a></strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout">CSS layout</a></strong></p>
<ul><li>I due moduli MDN attraversati dalla lezione.</li></ul>
</blockquote>

<blockquote>
<p><strong>03 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-foundations">HTML e CSS hanno responsabilità diverse</a></strong></p>
<ul><li>Ruolo di CSS, stili predefiniti e collegamento del foglio esterno.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/What_is_CSS">What is CSS?</a></strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Getting_started#applying_css_to_html">Applying CSS to HTML</a></strong></p>
<ul><li>Scopo di CSS, stili del browser e modalità di applicazione.</li></ul>
</blockquote>

<blockquote>
<p><strong>04 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-rule">Anatomia di una regola CSS</a></strong></p>
<ul><li>Selettore, dichiarazioni, proprietà, valori e selettori core.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/What_is_CSS#css_syntax_basics">CSS syntax basics</a></strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Basic_selectors">Basic CSS selectors</a></strong></p>
<ul><li>Sintassi di una regola e selettori fondamentali.</li></ul>
</blockquote>

</details>

<details>
<summary><strong>Cascade e dimensioni</strong> · 3 voci</summary>

<blockquote>
<p><strong>05 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-cascade">Cascade, specificità ed ereditarietà</a></strong></p>
<ul><li>Scelta della dichiarazione vincente e uso prudente di <code>!important</code>.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts">Handling conflicts</a></strong></p>
<ul><li>Inheritance, cascade, specificity e ordine delle regole.</li></ul>
</blockquote>

<blockquote>
<p><strong>06 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-box-model">Box model: ogni elemento genera scatole</a></strong></p>
<ul><li>Content, padding, border, margin e <code>border-box</code>.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model">The box model</a></strong></p>
<ul><li>Parti della scatola e modelli alternativi di calcolo.</li></ul>
</blockquote>

<blockquote>
<p><strong>07 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-normal-flow">Normal flow prima del layout speciale</a></strong></p>
<ul><li>Disposizione iniziale di contenuti block e inline.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Introduction">Introduction to CSS layout</a></strong></p>
<ul><li>Flusso normale e panoramica dei metodi di layout.</li></ul>
</blockquote>

</details>

<details>
<summary><strong>Sistemi di layout</strong> · 3 voci</summary>

<blockquote>
<p><strong>08 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-layout">Flexbox: una dimensione alla volta</a></strong></p>
<ul><li>Container, item, assi, allineamento, gap e wrapping.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox">Flexbox</a></strong></p>
<ul><li>Modello monodimensionale e proprietà fondamentali.</li></ul>
</blockquote>

<blockquote>
<p><strong>09 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-grid">Grid: righe e colonne coordinate</a></strong></p>
<ul><li>Track, frazioni, gap, auto-placement e <code>minmax()</code>.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids">CSS grid layout</a></strong></p>
<ul><li>Griglie bidimensionali, righe, colonne e posizionamento.</li></ul>
</blockquote>

<blockquote>
<p><strong>10 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-layout-choice">Flexbox o Grid?</a></strong></p>
<ul><li>Criterio pratico per scegliere il sistema di layout.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<em>Nessun paragrafo MDN unico: la scelta nasce dal confronto fra i due modelli.</em></p>
</blockquote>

</details>

<details>
<summary><strong>Responsive design e riuso</strong> · 3 voci</summary>

<blockquote>
<p><strong>11 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-responsive">Responsive design e media query</a></strong></p>
<ul><li>Layout mobile-first, breakpoint guidati dal contenuto e fluidità.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design">Responsive web design</a></strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Media_queries">Media query fundamentals</a></strong></p>
<ul><li>Strategia responsive e condizioni applicate tramite media query.</li></ul>
</blockquote>

<blockquote>
<p><strong>12 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-units">Unità, testo e immagini responsive</a></strong></p>
<ul><li>Misure relative, leggibilità e contenuti che non superano il contenitore.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Values_and_units">Values and units</a></strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Text_styling/Fundamentals">Fundamental text and font styling</a></strong></p>
<ul><li>Unità CSS e proprietà tipografiche fondamentali.</li></ul>
</blockquote>

<blockquote>
<p><strong>13 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-custom-properties">Custom properties: valori con un nome</a></strong></p>
<ul><li>Dichiarazione di valori riusabili e prima applicazione di <code>var()</code>.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties">Using CSS custom properties</a></strong></p>
<ul><li>Guida completa alle proprietà personalizzate e ai valori di fallback.</li></ul>
</blockquote>

</details>

<details>
<summary><strong>Applicazione, debug e confini</strong> · 3 voci</summary>

<blockquote>
<p><strong>14 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-css-debug">Debug CSS ed errori frequenti</a></strong></p>
<ul><li>Procedura con DevTools per overflow, cascade e breakpoint errati.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<em>Nessun riferimento MDN diretto selezionato per questa voce.</em></p>
</blockquote>

<blockquote>
<p><strong>15 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<strong><a href="#lesson-lab">Laboratorio</a></strong></p>
<ul><li>Osservazione, shell responsive Feisbuc e diagnosi guidata.</li></ul>
<p><strong>&#128994; MDN</strong><br>
<em>Le Activity applicano i concetti senza riprodurre un esercizio MDN.</em></p>
</blockquote>

<blockquote>
<p><strong>16 · CORRISPONDENZA</strong></p>
<p><strong>&#128309; DISPENSA</strong><br>
<em>Nessun paragrafo operativo: contenuti esclusi dalla lezione.</em></p>
<p><strong>&#128994; MDN</strong><br>
<strong><a href="https://developer.mozilla.org/en-US/docs/Web/CSS">CSS reference</a></strong></p>
<ul><li>Writing modes, animazioni e moduli avanzati da studiare più avanti.</li></ul>
</blockquote>

</details>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">Il nostro HTML semantico sa già dire che cosa sono header, navigazione, feed e post. Ma il browser, senza istruzioni di presentazione, li mostra quasi tutti nel normale flusso del documento.</p>

<p align="justify">Vogliamo ottenere una pagina che:</p>

<ul>
  <li>resti leggibile su uno smartphone;</li>
  <li>sfrutti più spazio su un desktop;</li>
  <li>non abbia larghezze fissate per un solo monitor;</li>
  <li>non dipenda da <code>float</code> per costruire le colonne;</li>
  <li>non richieda una cascata di <code>!important</code> per funzionare.</li>
</ul>

<p align="justify">Questo è il problema che affrontiamo con CSS.</p>

<a id="lesson-css-foundations"></a>
## HTML e CSS hanno responsabilità diverse

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128161;</span> Idea chiave — responsabilità distinte:</strong>
HTML descrive soprattutto <strong>struttura e significato</strong>. CSS descrive <strong>presentazione e layout</strong>.</p>
</td></tr></table>

```html
<article class="post">
  <h2>Primo post</h2>
  <p>Ciao Feisbuc!</p>
</article>
```

```css
.post {
  border: 1px solid #bbb;
  border-radius: 0.75rem;
  padding: 1rem;
}
```

<p align="justify">Cambiare il bordo non trasforma <code>article</code> in un altro tipo di contenuto: cambia il modo in cui viene presentato.</p>

### Da dove arriva lo stile

<p align="justify">Prima ancora del nostro CSS, il browser applica un proprio foglio di stile: è il motivo per cui, per esempio, un <code>h1</code> appare grande e in grassetto anche in una pagina senza CSS. Questi <strong>stili predefiniti</strong> sono una base utile, non un errore da eliminare alla cieca.</p>

<p align="justify">Possiamo aggiungere CSS in tre modi:</p>

<ol>
  <li>con un foglio esterno collegato da <code>&lt;link&gt;</code>: è la scelta normale del corso, perché separa struttura e presentazione e permette il riuso;</li>
  <li>con un elemento <code>&lt;style&gt;</code> nel documento: utile per una demo isolata o una pagina autosufficiente;</li>
  <li>con l'attributo <code>style</code> sul singolo elemento: da riconoscere e saper ispezionare, ma da non usare come strategia abituale.</li>
</ol>

```html
<head>
  <link rel="stylesheet" href="styles.css">
</head>
```

<p align="justify">Il riferimento guidato è <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Getting_started#applying_css_to_html">Applying CSS to HTML</a>: studia il collegamento esterno e riconosci le altre due possibilità.</p>

<a id="lesson-css-rule"></a>
## Anatomia di una regola CSS

```css
.post {
  padding: 1rem;
  border: 1px solid #bbb;
}
```

<ul>
  <li><code>.post</code> è il <strong>selettore</strong>;</li>
  <li><code>padding</code> e <code>border</code> sono <strong>proprietà</strong>;</li>
  <li><code>1rem</code> e <code>1px solid #bbb</code> sono <strong>valori</strong>;</li>
  <li><code>padding: 1rem</code> è una <strong>dichiarazione</strong>;</li>
  <li>l'insieme fra <code>{</code> e <code>}</code> è il blocco delle dichiarazioni.</li>
</ul>

### Selettori da padroneggiare nel core

```css
article { }
.post { }
#feed { }
nav a { }
.post > h2 { }
button:hover { }
input[type="email"] { }
.post + .post { }
.post::first-line { }
```

<p align="justify">Un selettore dice <strong>quali elementi devono ricevere una regola</strong>. Non descrive un percorso imperativo nel DOM: il browser confronta gli elementi con il pattern dichiarato.</p>

<ul>
  <li><code>article</code>, <code>.post</code>, <code>#feed</code> sono selettori di tipo, classe e ID;</li>
  <li><code>[type="email"]</code> seleziona in base a un attributo;</li>
  <li><code>:hover</code> descrive uno stato, quindi è una pseudo-classe;</li>
  <li><code>::first-line</code> seleziona una parte generata dell'elemento, quindi è uno pseudo-elemento;</li>
  <li>lo spazio, <code>&gt;</code> e <code>+</code> mettono in relazione elementi discendenti, figli o fratelli adiacenti;</li>
  <li>una virgola raggruppa selettori che condividono le stesse dichiarazioni.</li>
</ul>

<p align="justify">Nel corso preferiremo normalmente classi e selettori semplici per lo styling. Gli ID rimangono utili per identificazione, collegamenti a frammenti, accessibilità e casi mirati, ma non vogliamo costruire fogli di stile impossibili da sovrascrivere. Nella <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Basic_selectors">guida MDN ai selettori</a> studia i selettori di base; combinatori, pseudo-classi e pseudo-elementi vanno saputi leggere e cercare nella documentazione.</p>

<a id="lesson-css-cascade"></a>
## Cascade: perché una regola vince su un'altra?

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128214;</span> Definizione — cascade:</strong>
CSS significa <em>Cascading Style Sheets</em>: più dichiarazioni possono riguardare lo stesso elemento e il browser deve decidere quale applicare.</p>
</td></tr></table>

<p align="justify">Per i casi iniziali ragioniamo in questo ordine mentale:</p>

<ol>
  <li>le dichiarazioni sono entrambe applicabili all'elemento?</li>
  <li>c'è un'importanza/origine diversa?</li>
  <li>quale selettore è più specifico?</li>
  <li>se la priorità è equivalente, quale dichiarazione arriva dopo?</li>
</ol>

<p align="justify">Esempio:</p>

```css
.post {
  color: #222;
}

#feed .post {
  color: #333;
}
```

<p align="justify">Il secondo selettore ha specificità maggiore.</p>

### Specificità senza formule magiche

<p align="justify">Per il livello core basta ricordare una gerarchia pratica:</p>

<ul>
  <li>selettori di tipo (<code>article</code>) hanno peso basso;</li>
  <li>classi, attributi e pseudo-classi (<code>.post</code>, <code>[hidden]</code>, <code>:hover</code>) hanno peso maggiore;</li>
  <li>ID (<code>#feed</code>) hanno peso ancora maggiore;</li>
  <li>gli stili inline sono ancora più difficili da sovrascrivere nel normale CSS dell'autore.</li>
</ul>

<p align="justify">Non useremo la specificità come una gara a costruire il selettore più lungo. Il buon obiettivo è il contrario: <strong>regole semplici e prevedibili</strong>.</p>

### Perché evitare `!important` come soluzione abituale

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#9888;</span> Attenzione — <code>!important</code>:</strong>
<code>!important</code> cambia la priorità nella cascata. Esistono casi reali in cui è utile, ma non deve diventare il cerotto con cui nascondiamo un'architettura CSS confusa.</p>
</td></tr></table>

<p align="justify">Quando senti il bisogno di scrivere:</p>

```css
#feed .post.card.special {
  padding: 2rem !important;
}
```

<p align="justify">prima chiediti:</p>

<ul>
  <li>sto usando selettori troppo specifici?</li>
  <li>sto duplicando regole?</li>
  <li>l'ordine del foglio è comprensibile?</li>
  <li>posso modellare meglio i componenti con classi?</li>
</ul>

## Ereditarietà

<p align="justify">Alcune proprietà possono essere ereditate dai discendenti, altre no.</p>

```css
body {
  color: #222;
  font-family: system-ui, sans-serif;
}
```

<p align="justify">Molto testo dentro <code>body</code> userà naturalmente questi valori. Un <code>margin</code> assegnato a <code>body</code>, invece, non viene semplicemente ereditato da tutti i figli.</p>

<p align="justify">Quando non ricordi se una proprietà eredita, consulta la sezione <strong>Formal definition</strong> della pagina MDN della proprietà.</p>

<a id="lesson-css-box-model"></a>
## Box model: ogni elemento genera scatole

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128214;</span> Definizione — box model:</strong>
ogni elemento genera una scatola composta dall'area del contenuto e, procedendo verso l'esterno, da padding, bordo e margine.</p>
</td></tr></table>

<p align="justify">Per capire dimensioni e spazi dobbiamo visualizzare:</p>

```text
margin
└─ border
   └─ padding
      └─ content
```

<p align="justify">Un elemento può avere:</p>

<ul>
  <li>area del contenuto;</li>
  <li>padding attorno al contenuto;</li>
  <li>bordo;</li>
  <li>margine esterno.</li>
</ul>

<p align="justify">Esempio:</p>

```css
.post {
  width: 20rem;
  padding: 1rem;
  border: 0.25rem solid #777;
}
```

<p align="justify">Con il box model standard la <code>width</code> indica la larghezza del <strong>content box</strong>, quindi padding e border si sommano alla dimensione finale.</p>

### `box-sizing: border-box`

<p align="justify">Per interfacce applicative è spesso più facile ragionare così:</p>

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

<p align="justify">Con <code>border-box</code>, quando impostiamo una larghezza, padding e border rientrano nella dimensione dichiarata.</p>

<p align="justify">Questo non è un reset magico di tutto il CSS: risolve un problema preciso di calcolo delle dimensioni.</p>

<a id="lesson-css-normal-flow"></a>
## Normal flow prima del layout speciale

<p align="justify">Prima di Flexbox e Grid, il browser ha già un algoritmo di layout: il <strong>normal flow</strong>.</p>

<p align="justify">Gli elementi block tendono a disporsi uno dopo l'altro lungo la direzione di blocco. Il contenuto inline scorre invece dentro le righe.</p>

<p align="justify">Capire il normal flow serve perché Flexbox e Grid non sostituiscono CSS: cambiano il modo in cui vengono disposti i figli di uno specifico contenitore.</p>

<a id="lesson-css-layout"></a>
## Flexbox: una dimensione alla volta

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128161;</span> Modello mentale — Flexbox:</strong>
Flexbox è adatto quando il problema principale è distribuire elementi in una <strong>riga oppure colonna</strong>.</p>
</td></tr></table>

<p align="justify">Esempio: il menu di Feisbuc.</p>

```css
.nav-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
}
```

<p align="justify">Concetti essenziali:</p>

<ul>
  <li>flex container;</li>
  <li>flex item;</li>
  <li>main axis;</li>
  <li>cross axis;</li>
  <li><code>flex-direction</code>;</li>
  <li><code>justify-content</code>;</li>
  <li><code>align-items</code>;</li>
  <li><code>gap</code>;</li>
  <li><code>flex-wrap</code>;</li>
  <li><code>flex</code> / crescita e restringimento quando serve.</li>
</ul>

### Errore comune: memorizzare `justify` = orizzontale

<p align="justify">Non è corretto. <code>justify-content</code> lavora sull'<strong>asse principale</strong>. Se cambi <code>flex-direction</code>, cambia anche l'orientamento dell'asse principale.</p>

<a id="lesson-css-grid"></a>
## Grid: righe e colonne coordinate

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128161;</span> Modello mentale — Grid:</strong>
Grid è adatto quando il layout deve ragionare contemporaneamente su <strong>due dimensioni</strong>.</p>
</td></tr></table>

<p align="justify">Per Feisbuc, su uno schermo ampio potremmo voler coordinare:</p>

```text
profilo | feed | tendenze
```

```css
.page-shell {
  display: grid;
  grid-template-columns:
    minmax(12rem, 16rem)
    minmax(0, 1fr)
    minmax(12rem, 16rem);
  gap: 1rem;
}
```

<p align="justify">Concetti core:</p>

<ul>
  <li>grid container;</li>
  <li>grid item;</li>
  <li>righe e colonne;</li>
  <li>track;</li>
  <li><code>fr</code>;</li>
  <li><code>gap</code>;</li>
  <li><code>grid-template-columns</code>;</li>
  <li><code>minmax()</code>;</li>
  <li>auto-placement;</li>
  <li>grid areas solo dopo avere capito le colonne di base.</li>
</ul>

### Perché `minmax(0, 1fr)` nel feed?

<p align="justify">Il valore <code>1fr</code> distribuisce spazio flessibile. In certi layout, un contenuto lungo può però impedire alla colonna di restringersi come immaginiamo. Rendere esplicito il minimo <code>0</code> è una tecnica utile per permettere alla colonna centrale di contrarsi e gestire correttamente l'overflow.</p>

<a id="lesson-css-layout-choice"></a>
## Flexbox o Grid?

<p align="justify">Usa questa domanda, non una regola religiosa:</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#10067;</span> Domanda guida:</strong>
sto organizzando soprattutto una fila o una colonna, oppure devo coordinare righe e colonne?</p>
</td></tr></table>

<p align="justify">Esempi Feisbuc:</p>

<ul>
  <li>menu orizzontale con wrapping → Flexbox;</li>
  <li>pulsanti di una card → Flexbox;</li>
  <li>layout profilo/feed/tendenze → Grid;</li>
  <li>griglia di card con colonne → Grid;</li>
  <li>una singola riga di avatar → Flexbox.</li>
</ul>

<p align="justify">Le due tecnologie si combinano normalmente nella stessa pagina.</p>

<a id="lesson-css-responsive"></a>
## Responsive design: non significa scegliere tre telefoni

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128214;</span> Definizione — responsive design:</strong>
responsive design significa progettare affinché il contenuto rimanga utilizzabile in una gamma di spazi disponibili.</p>
</td></tr></table>

<p align="justify">Partiamo da un layout semplice per viewport piccoli:</p>

```css
.page-shell {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
```

<p align="justify">Poi aggiungiamo un breakpoint quando <strong>il contenuto</strong> ha spazio sufficiente per una struttura più ricca:</p>

```css
@media (min-width: 56rem) {
  .page-shell {
    grid-template-columns:
      minmax(12rem, 16rem)
      minmax(0, 1fr)
      minmax(12rem, 16rem);
  }
}
```

<p align="justify">Questo è un approccio mobile-first: la base funziona con poco spazio; una media query aggiunge il layout ampio.</p>

### Media query solo quando serve

<p align="justify">Flexbox e Grid sono già flessibili. Non dobbiamo creare un breakpoint per ogni modello di telefono.</p>

<p align="justify">Prima prova:</p>

<ul>
  <li>dimensioni relative;</li>
  <li>wrapping;</li>
  <li><code>minmax()</code>;</li>
  <li><code>max-width</code>;</li>
  <li>Grid/Flex flessibili.</li>
</ul>

<p align="justify">Aggiungi <code>@media</code> quando la struttura ha davvero bisogno di cambiare.</p>

<a id="lesson-css-units"></a>
## Unità utili

<p align="justify">Non esiste una singola unità corretta per tutto.</p>

<ul>
  <li><code>px</code>: utile per dettagli come alcuni border;</li>
  <li><code>%</code>: relativo a un riferimento contestuale;</li>
  <li><code>rem</code>: utile per spazi e dimensioni scalabili rispetto alla root;</li>
  <li><code>fr</code>: quota dello spazio disponibile in Grid;</li>
  <li><code>vw</code>/<code>vh</code>: viewport-relative, da usare con consapevolezza;</li>
  <li><code>min()</code>, <code>max()</code>, <code>clamp()</code> possono esprimere dimensioni fluide, ma sono un passo successivo.</li>
</ul>

<p align="justify">Evitiamo layout come:</p>

```css
.page-shell {
  width: 1200px;
}
```

<p align="justify">se quella larghezza rigida è l'unico modo in cui la pagina funziona.</p>

### Testo leggibile: font, ritmo e colore

<p align="justify">Lo stile del testo non è decorazione separata dal layout: dimensione, interlinea e larghezza della riga decidono se il contenuto si legge bene.</p>

```css
body {
  color: #1f2937;
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  line-height: 1.5;
}

.post__text {
  max-width: 65ch;
}
```

<ul>
  <li>una <strong>font stack</strong> offre alternative se il primo font non è disponibile;</li>
  <li><code>rem</code> collega le dimensioni alla base del documento e rispetta meglio le preferenze utente;</li>
  <li><code>line-height</code> senza unità mantiene una proporzione utile anche nei discendenti;</li>
  <li><code>ch</code> può limitare righe di testo troppo lunghe;</li>
  <li>il colore deve avere contrasto sufficiente e non deve essere l'unico segnale di stato.</li>
</ul>

<p align="justify">Nella pagina MDN <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Text_styling/Fundamentals">Fundamental text and font styling</a> studia famiglie, dimensioni, peso, stile e interlinea; le proprietà tipografiche avanzate restano materiale di consultazione.</p>

## Immagini responsive

<p align="justify">Una regola semplice evita molte sorprese:</p>

```css
img {
  max-width: 100%;
  height: auto;
}
```

<p align="justify">Non risolve da sola art direction, formati o performance delle immagini, ma impedisce spesso che un'immagine superi il contenitore.</p>

<a id="lesson-css-custom-properties"></a>
## Custom properties: valori con un nome

<p align="justify">Possiamo dichiarare valori riusabili:</p>

```css
:root {
  --space-1: 0.5rem;
  --space-2: 1rem;
  --surface: #fff;
  --border: #d7d7d7;
}

.post {
  padding: var(--space-2);
  background: var(--surface);
  border: 1px solid var(--border);
}
```

<p align="justify">Il vantaggio didattico non è solo evitare copia-incolla: i nomi permettono di esprimere intenzioni.</p>

## Feisbuc milestone 1: shell responsive

<p align="justify">Partiamo dallo scheletro semantico della milestone 0.</p>

```html
<main class="page-shell">
  <section class="profile" aria-labelledby="profile-title">...</section>
  <section id="feed" aria-labelledby="feed-title">...</section>
  <aside class="trends" aria-labelledby="trends-title">...</aside>
</main>
```

<p align="justify">La base mobile:</p>

```css
.page-shell {
  width: min(100% - 2rem, 75rem);
  margin-inline: auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
```

<p align="justify">La versione ampia:</p>

```css
@media (min-width: 56rem) {
  .page-shell {
    grid-template-columns:
      minmax(12rem, 16rem)
      minmax(0, 1fr)
      minmax(12rem, 16rem);
    align-items: start;
  }
}
```

<p align="justify">Il menu e le azioni di un post possono invece essere Flexbox.</p>

<p align="justify">Questa separazione è intenzionale:</p>

```text
Grid    → macro layout della pagina
Flexbox → gruppi monodimensionali dentro le regioni
```

<a id="lesson-css-debug"></a>
## Debug CSS: osserva prima di cambiare

<p align="justify">Quando un layout si rompe:</p>

<ol>
  <li>riproduci il problema a una larghezza precisa;</li>
  <li>individua l'elemento che provoca l'overflow o il conflitto;</li>
  <li>usa DevTools per vedere regole applicate e barrate;</li>
  <li>controlla box model e dimensioni calcolate;</li>
  <li>controlla quale regola vince nella cascade;</li>
  <li>modifica un'ipotesi alla volta;</li>
  <li>verifica di nuovo mobile e desktop.</li>
</ol>

<p align="justify">Non partire aggiungendo <code>overflow-x: hidden</code>: potrebbe nascondere il sintomo senza correggere la causa.</p>

## Errori frequenti

### 1. Layout a larghezza fissa

```css
main {
  width: 1200px;
}
```

<p align="justify">Su un viewport più piccolo può produrre overflow.</p>

### 2. Usare `float` come sistema principale di colonne

<p align="justify"><code>float</code> resta una funzionalità CSS reale, ma non è il nostro strumento principale per costruire il layout applicativo moderno di Feisbuc.</p>

### 3. `!important` ovunque

<p align="justify">Nasconde conflitti invece di farli comprendere.</p>

### 4. Breakpoint invertiti

<p align="justify">Se la base è mobile-first, una regola <code>min-width</code> dovrebbe normalmente aggiungere complessità quando cresce lo spazio, non forzare la singola colonna proprio sui viewport più larghi.</p>

### 5. Confondere Grid e Flex

<p align="justify">Usare Flexbox per simulare una tabella bidimensionale o Grid per una semplice riga di bottoni può rendere il codice più difficile del necessario.</p>

### 6. Riordinare visivamente senza pensare alla semantica

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#9888;</span> Attenzione — ordine visivo e ordine del DOM:</strong>
CSS può modificare la posizione visuale. L'ordine del DOM rimane però importante per lettura, tastiera e tecnologie assistive. Non usiamo il layout per mascherare una struttura HTML sbagliata.</p>
</td></tr></table>

<a id="lesson-lab"></a>
## Laboratorio

<p align="justify">Il laboratorio procede dall'osservazione del box model alla costruzione e al debug della shell responsive di Feisbuc. Gli ultimi due punti anticipano prodotti che verranno completati nelle lezioni successive.</p>

<table align="center"><tr><td>
<details>
<summary>&#128187; <strong>Esercizi A e B — osservazione e modifica controllata</strong></summary>

<ul>
  <li><strong>A — osservazione:</strong> modifica <code>padding</code>, <code>border</code> e <code>margin</code> di una card e osserva il box model nei DevTools.</li>
  <li><strong>B — modifica controllata:</strong> trasforma un menu verticale in un flex container con wrapping.</li>
</ul>

</details>
</td></tr></table>

<table align="center"><tr><td>
<details>
<summary>&#128187; <strong>Activity C — Feisbuc responsive</strong></summary>

<p align="justify">Costruisci la shell responsive di Feisbuc usando Grid per il macro-layout e Flexbox per i gruppi interni.</p>

<p align="justify"><a href="../../activities/tpsi5/feisbuc_responsive_c/student/README.md">Apri la consegna dell'Activity C</a> e lavora sullo <a href="../../activities/tpsi5/feisbuc_responsive_c/starter/index.html">starter <code>index.html</code></a>.</p>

</details>
</td></tr></table>

<table align="center"><tr><td>
<details>
<summary>&#128187; <strong>Activity D — Debug responsive CSS</strong></summary>

<p align="justify">Ricevi una pagina che funziona apparentemente solo su desktop. Prima documenta le cause, poi correggi il CSS senza <code>!important</code> e senza nascondere l'overflow.</p>

<p align="justify"><a href="../../activities/tpsi5/css_debug_d/student/README.md">Apri la consegna dell'Activity D</a>, lavora sullo <a href="../../activities/tpsi5/css_debug_d/starter/index.html">starter <code>index.html</code></a> e documenta la diagnosi nel file <a href="../../activities/tpsi5/css_debug_d/starter/DIAGNOSI.md"><code>DIAGNOSI.md</code></a>.</p>

</details>
</td></tr></table>

<table align="center"><tr><td>
<details>
<summary>&#10145; <strong>Sviluppi successivi — punti E e F</strong></summary>

<ul>
  <li><strong>E — mini-progetto futuro:</strong> costruire una pagina profilo completa con layout responsive, form e componenti visuali riusabili.</li>
  <li><strong>F — prodotto integrato futuro:</strong> integrare layout, comportamento JavaScript, API e backend nel Feisbuc full stack.</li>
</ul>

</details>
</td></tr></table>

<a id="lesson-checkpoint"></a>
## Verifica rapida

<table align="center"><tr><td>
<details>
<summary>&#9989; <strong>Checkpoint — controlla ciò che hai compreso</strong></summary>

<ol>
  <li>Che differenza c'è fra HTML e CSS?</li>
  <li>Da quali parti è composto il box model?</li>
  <li>Che cosa cambia con <code>box-sizing: border-box</code>?</li>
  <li>Quando useresti Flexbox invece di Grid?</li>
  <li>Perché <code>justify-content</code> non significa semplicemente “allinea orizzontalmente”?</li>
  <li>Perché un layout <code>width: 1200px</code> può essere fragile?</li>
  <li>A cosa serve una media query?</li>
  <li>Perché non serve una media query per ogni telefono?</li>
  <li>Che cosa risolve la specificità?</li>
  <li>Perché <code>!important</code> non deve essere la prima soluzione?</li>
  <li>Che cosa rappresenta <code>1fr</code> in Grid?</li>
  <li>Perché in un debug CSS è utile vedere le regole barrate nei DevTools?</li>
</ol>

</details>
</td></tr></table>

<a id="lesson-summary"></a>
## Sintesi

```text
HTML → che cosa significa il contenuto
CSS  → come viene presentato e disposto

Cascade → quale dichiarazione vince
Box model → content + padding + border + margin

Flexbox → soprattutto una dimensione
Grid    → due dimensioni

Responsive → layout che si adatta allo spazio
Media query → cambia regole quando una condizione lo richiede

Feisbuc mobile → una colonna
Feisbuc wide   → profilo | feed | tendenze
```

<a id="lesson-reading-mdn"></a>
## MDN in questa lezione

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> Percorso MDN — CSS:</strong> usa il metodo generale della <a href="GUIDA_USO_MDN.md">guida trasversale a MDN</a> e, quando apri la scheda di una proprietà, segui l'ordine indicato in <a href="GUIDA_USO_MDN.md#mdn-guide-css">Come leggere una reference CSS</a>.</p>
<ul>
  <li><strong>Cascade e specificità:</strong> studia <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts">Handling conflicts</a>; ricostruisci quali dichiarazioni sono candidate e perché una vince;</li>
  <li><strong>box model:</strong> studia <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model">The box model</a>; confronta content, padding, border e margin nei DevTools;</li>
  <li><strong>Flexbox:</strong> studia <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox">Flexbox</a>; identifica container, item, main axis e cross axis;</li>
  <li><strong>Grid:</strong> studia <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids">CSS grid layout</a>; identifica track, righe, colonne, gap e posizione degli item;</li>
  <li><strong>responsive:</strong> studia <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design">Responsive web design</a> e <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Media_queries">Media query fundamentals</a>; aggiungi un breakpoint soltanto quando lo richiede il contenuto.</li>
</ul>
<p align="justify"><strong>Prodotto atteso:</strong> per ogni problema annota la regola CSS responsabile, la prova svolta nei DevTools e il cambiamento osservato.</p>
</td></tr></table>

<a id="lesson-sources"></a>
## Fonti e documentazione

<p align="justify">Fonti tecniche professionali:</p>

<ul>
  <li><a href="https://developer.mozilla.org/en-US/docs/Web/CSS">MDN — CSS reference</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts">MDN — Handling conflicts</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model">MDN — The box model</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox">MDN — Flexbox</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids">MDN — CSS grid layout</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design">MDN — Responsive web design</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Media_queries">MDN — Media query fundamentals</a>;</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties">MDN — Using CSS custom properties</a>.</li>
</ul>

<p align="justify">Provenienza interna:</p>

<ul>
  <li><code>TheBitPoets/html_css_summary</code>, versione fissata: sintassi CSS, box model, block/inline, padding/margin/border;</li>
  <li><code>TheBitPoets/feisbuc</code>, versione fissata: layout precedente basato su colonne/float e progetto longitudinale da modernizzare.</li>
</ul>

<p align="justify">Riferimento per il docente acquistato con licenza e non riprodotto nel corso:</p>

<ul>
  <li>Manning, <em>CSS in Depth, Second Edition</em>.</li>
</ul>

<p align="justify">Il testo, gli esempi canonici, le Activity e le soluzioni di riferimento di questo modulo sono materiale originale del corso.</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#10145;</span> Prossimo passo:</strong>
nella lezione <a href="03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md">Da CSS a Bootstrap</a> confronteremo queste scelte di layout con il sistema responsive e i componenti offerti da un framework frontend.</p>
</td></tr></table>
