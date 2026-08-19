# CSS moderno, layout e responsive design

Stato: **draft didattico**. Questa lezione prosegue UDA 21 dopo `01_WEB_PLATFORM_HTML_MODERNO.md` e trasforma lo scheletro semantico di Feisbuc in una interfaccia responsive senza introdurre ancora Bootstrap o framework frontend.

## Obiettivi

Al termine della lezione lo studente deve saper:

- spiegare il ruolo di CSS nella Web Platform senza confonderlo con HTML;
- leggere e scrivere regole CSS composte da selettore, proprietà e valore;
- prevedere il risultato di conflitti semplici usando cascade, specificità e ordine;
- usare il box model e `box-sizing: border-box` in modo consapevole;
- distinguere normal flow, `block`, `inline` e contenitori di layout;
- scegliere Flexbox per problemi prevalentemente monodimensionali;
- scegliere Grid per layout bidimensionali;
- costruire layout che si adattano al viewport invece di fissare larghezze rigide;
- usare media query solo quando il layout fluido da solo non basta;
- definire e riusare custom properties CSS;
- diagnosticare overflow, specificità e breakpoint errati con DevTools;
- realizzare la milestone responsive iniziale di Feisbuc.

## Prerequisiti

- completamento di `01_WEB_PLATFORM_HTML_MODERNO.md`;
- struttura semantica con `header`, `nav`, `main`, `section`, `article`, `footer`;
- uso essenziale di browser DevTools;
- nessuna conoscenza di Bootstrap richiesta.

## Problema iniziale

Il nostro HTML semantico sa gia dire che cosa sono header, navigazione, feed e post. Ma il browser, senza istruzioni di presentazione, li mostra quasi tutti nel normale flusso del documento.

Vogliamo ottenere una pagina che:

- resti leggibile su uno smartphone;
- sfrutti piu spazio su un desktop;
- non abbia larghezze fissate per un solo monitor;
- non dipenda da `float` per costruire le colonne;
- non richieda una cascata di `!important` per funzionare.

Questo e il problema che affrontiamo con CSS.

## HTML e CSS hanno responsabilita diverse

HTML descrive soprattutto **struttura e significato**. CSS descrive **presentazione e layout**.

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

Cambiare il bordo non trasforma `article` in un altro tipo di contenuto: cambia il modo in cui viene presentato.

## Anatomia di una regola CSS

```css
.post {
  padding: 1rem;
  border: 1px solid #bbb;
}
```

- `.post` e il **selettore**;
- `padding` e `border` sono **proprieta**;
- `1rem` e `1px solid #bbb` sono **valori**;
- `padding: 1rem` e una **dichiarazione**;
- l'insieme fra `{` e `}` e il blocco delle dichiarazioni.

### Selettori da padroneggiare nel core

```css
article { }
.post { }
#feed { }
nav a { }
.post > h2 { }
button:hover { }
```

Nel corso preferiremo normalmente classi e selettori semplici per lo styling. Gli ID rimangono utili per identificazione, fragment link, accessibilita e casi mirati, ma non vogliamo costruire fogli di stile impossibili da sovrascrivere.

## Cascade: perche una regola vince su un'altra?

CSS significa *Cascading Style Sheets*: piu dichiarazioni possono riguardare lo stesso elemento e il browser deve decidere quale applicare.

Per i casi iniziali ragioniamo in questo ordine mentale:

1. le dichiarazioni sono entrambe applicabili all'elemento?
2. c'e un'importanza/origine diversa?
3. quale selettore e piu specifico?
4. se la priorita e equivalente, quale dichiarazione arriva dopo?

Esempio:

```css
.post {
  color: #222;
}

#feed .post {
  color: #333;
}
```

Il secondo selettore ha specificita maggiore.

### Specificita senza formule magiche

Per il livello core basta ricordare una gerarchia pratica:

- selettori di tipo (`article`) hanno peso basso;
- classi, attributi e pseudo-classi (`.post`, `[hidden]`, `:hover`) hanno peso maggiore;
- ID (`#feed`) hanno peso ancora maggiore;
- gli stili inline sono ancora piu difficili da sovrascrivere nel normale author CSS.

Non useremo la specificita come una gara a costruire il selettore piu lungo. Il buon obiettivo e il contrario: **regole semplici e prevedibili**.

### Perche evitare `!important` come soluzione abituale

`!important` cambia la priorita nella cascata. Esistono casi reali in cui e utile, ma non deve diventare il cerotto con cui nascondiamo una architettura CSS confusa.

Quando senti il bisogno di scrivere:

```css
#feed .post.card.special {
  padding: 2rem !important;
}
```

prima chiediti:

- sto usando selettori troppo specifici?
- sto duplicando regole?
- l'ordine del foglio e comprensibile?
- posso modellare meglio i componenti con classi?

## Inheritance

Alcune proprieta possono essere ereditate dai discendenti, altre no.

```css
body {
  color: #222;
  font-family: system-ui, sans-serif;
}
```

Molto testo dentro `body` usera naturalmente questi valori. Un `margin` assegnato a `body`, invece, non viene semplicemente ereditato da tutti i figli.

Quando non ricordi se una proprieta eredita, consulta la sezione **Formal definition** della pagina MDN della proprieta.

## Box model: ogni elemento genera scatole

Per capire dimensioni e spazi dobbiamo visualizzare:

```text
margin
└─ border
   └─ padding
      └─ content
```

Un elemento puo avere:

- area del contenuto;
- padding attorno al contenuto;
- bordo;
- margine esterno.

Esempio:

```css
.post {
  width: 20rem;
  padding: 1rem;
  border: 0.25rem solid #777;
}
```

Con il box model standard la `width` indica la larghezza del **content box**, quindi padding e border si sommano alla dimensione finale.

### `box-sizing: border-box`

Per interfacce applicative e spesso piu facile ragionare cosi:

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

Con `border-box`, quando impostiamo una larghezza, padding e border rientrano nella dimensione dichiarata.

Questo non e un reset magico di tutto il CSS: risolve un problema preciso di calcolo delle dimensioni.

## Normal flow prima del layout speciale

Prima di Flexbox e Grid, il browser ha gia un algoritmo di layout: il **normal flow**.

Gli elementi block tendono a disporsi uno dopo l'altro lungo la direzione di blocco. Il contenuto inline scorre invece dentro le righe.

Capire il normal flow serve perche Flexbox e Grid non sostituiscono CSS: cambiano il modo in cui vengono disposti i figli di uno specifico contenitore.

## Flexbox: una dimensione alla volta

Flexbox e adatto quando il problema principale e distribuire elementi in una **riga oppure colonna**.

Esempio: il menu di Feisbuc.

```css
.nav-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
}
```

Concetti essenziali:

- flex container;
- flex item;
- main axis;
- cross axis;
- `flex-direction`;
- `justify-content`;
- `align-items`;
- `gap`;
- `flex-wrap`;
- `flex` / crescita e restringimento quando serve.

### Errore comune: memorizzare `justify` = orizzontale

Non e corretto. `justify-content` lavora sull'**asse principale**. Se cambi `flex-direction`, cambia anche l'orientamento dell'asse principale.

## Grid: righe e colonne coordinate

Grid e adatto quando il layout deve ragionare contemporaneamente su **due dimensioni**.

Per Feisbuc, su uno schermo ampio potremmo voler coordinare:

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

Concetti core:

- grid container;
- grid item;
- righe e colonne;
- track;
- `fr`;
- `gap`;
- `grid-template-columns`;
- `minmax()`;
- auto-placement;
- grid areas solo dopo avere capito le colonne di base.

### Perche `minmax(0, 1fr)` nel feed?

Il valore `1fr` distribuisce spazio flessibile. In certi layout, un contenuto lungo puo pero impedire alla colonna di restringersi come immaginiamo. Rendere esplicito il minimo `0` e una tecnica utile per permettere alla colonna centrale di contrarsi e gestire correttamente l'overflow.

## Flexbox o Grid?

Usa questa domanda, non una regola religiosa:

> Sto organizzando soprattutto una fila/colonna, oppure devo coordinare righe e colonne?

Esempi Feisbuc:

- menu orizzontale con wrapping → Flexbox;
- pulsanti di una card → Flexbox;
- layout profilo/feed/tendenze → Grid;
- griglia di card con colonne → Grid;
- una singola riga di avatar → Flexbox.

Le due tecnologie si combinano normalmente nella stessa pagina.

## Responsive design: non significa scegliere tre telefoni

Responsive design significa progettare affinche il contenuto rimanga utilizzabile in una gamma di spazi disponibili.

Partiamo da un layout semplice per viewport piccoli:

```css
.page-shell {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
```

Poi aggiungiamo un breakpoint quando **il contenuto** ha spazio sufficiente per una struttura piu ricca:

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

Questo e un approccio mobile-first: la base funziona con poco spazio; una media query aggiunge il layout ampio.

### Media query solo quando serve

Flexbox e Grid sono gia flessibili. Non dobbiamo creare un breakpoint per ogni modello di telefono.

Prima prova:

- dimensioni relative;
- wrapping;
- `minmax()`;
- `max-width`;
- Grid/Flex flessibili.

Aggiungi `@media` quando la struttura ha davvero bisogno di cambiare.

## Unita utili

Non esiste una singola unita corretta per tutto.

- `px`: utile per dettagli come alcuni border;
- `%`: relativo a un riferimento contestuale;
- `rem`: utile per spazi e dimensioni scalabili rispetto alla root;
- `fr`: quota dello spazio disponibile in Grid;
- `vw`/`vh`: viewport-relative, da usare con consapevolezza;
- `min()`, `max()`, `clamp()` possono esprimere dimensioni fluide, ma sono un passo successivo.

Evitiamo layout come:

```css
.page-shell {
  width: 1200px;
}
```

se quella larghezza rigida e l'unico modo in cui la pagina funziona.

## Immagini responsive

Una regola semplice evita molte sorprese:

```css
img {
  max-width: 100%;
  height: auto;
}
```

Non risolve da sola art direction, formati o performance delle immagini, ma impedisce spesso che una immagine superi il contenitore.

## Custom properties: valori con un nome

Possiamo dichiarare valori riusabili:

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

Il vantaggio didattico non e solo evitare copia-incolla: i nomi permettono di esprimere intenzioni.

## Feisbuc milestone 1: shell responsive

Partiamo dallo scheletro semantico della milestone 0.

```html
<main class="page-shell">
  <section class="profile" aria-labelledby="profile-title">...</section>
  <section id="feed" aria-labelledby="feed-title">...</section>
  <aside class="trends" aria-labelledby="trends-title">...</aside>
</main>
```

La base mobile:

```css
.page-shell {
  width: min(100% - 2rem, 75rem);
  margin-inline: auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
```

La versione ampia:

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

Il menu e le azioni di un post possono invece essere Flexbox.

Questa separazione e intenzionale:

```text
Grid    → macro layout della pagina
Flexbox → gruppi monodimensionali dentro le regioni
```

## Debug CSS: osserva prima di cambiare

Quando un layout si rompe:

1. riproduci il problema a una larghezza precisa;
2. individua l'elemento che provoca l'overflow o il conflitto;
3. usa DevTools per vedere regole applicate e barrate;
4. controlla box model e dimensioni calcolate;
5. controlla quale regola vince nella cascade;
6. modifica una ipotesi alla volta;
7. verifica di nuovo mobile e desktop.

Non partire aggiungendo `overflow-x: hidden`: potrebbe nascondere il sintomo senza correggere la causa.

## Errori frequenti

### 1. Layout a larghezza fissa

```css
main {
  width: 1200px;
}
```

Su un viewport piu piccolo puo produrre overflow.

### 2. Usare `float` come sistema principale di colonne

`float` resta una funzionalita CSS reale, ma non e il nostro strumento principale per costruire il layout applicativo moderno di Feisbuc.

### 3. `!important` ovunque

Nasconde conflitti invece di farli comprendere.

### 4. Breakpoint invertiti

Se la base e mobile-first, una regola `min-width` dovrebbe normalmente aggiungere complessita quando cresce lo spazio, non forzare la singola colonna proprio sui viewport piu larghi.

### 5. Confondere Grid e Flex

Usare Flexbox per simulare una tabella bidimensionale o Grid per una semplice riga di bottoni puo rendere il codice piu difficile del necessario.

### 6. Riordinare visivamente senza pensare alla semantica

CSS puo modificare la posizione visuale. L'ordine del DOM rimane pero importante per lettura, tastiera e tecnologie assistive. Non usiamo il layout per mascherare una struttura HTML sbagliata.

## Come studiare con MDN

Per ogni concetto non leggere MDN dall'inizio alla fine come un romanzo.

### Cascade e specificita

Cerca:

- “Introduction to the CSS cascade”;
- “Specificity”;
- “Handling conflicts”.

Domande:

1. quali regole sono candidate?
2. quale dichiarazione vince?
3. il problema si puo risolvere semplificando il selettore?

### Box model

Apri la guida “The box model” e usa DevTools per confrontare content, padding, border e margin.

### Flexbox

Apri “Flexbox” e identifica sempre:

- container;
- items;
- main axis;
- cross axis.

### Grid

Apri “CSS grid layout” e identifica:

- tracks;
- columns/rows;
- gap;
- posizione degli item.

### Responsive

Apri “Responsive web design” e “Media query fundamentals”. Prova prima a rendere flessibile il layout senza breakpoint, poi aggiungi una media query solo quando il contenuto lo richiede.

## Esempi da modificare

### A — osservazione

Modifica `padding`, `border` e `margin` di una card e osserva il box model nei DevTools.

### B — modifica controllata

Trasforma un menu verticale in un flex container con wrapping.

### C — implementazione autonoma

**Activity `tpsi5-activity-c-feisbuc-responsive-layout-001`**: costruisci la shell responsive di Feisbuc usando Grid per il macro-layout e Flexbox per i gruppi interni.

### D — debug e diagnosi

**Activity `tpsi5-activity-d-debug-responsive-css-001`**: ricevi una pagina che funziona apparentemente solo su desktop. Prima documenta le cause, poi correggi il CSS senza `!important` e senza nascondere l'overflow.

### E — mini-progetto futuro

Costruire una pagina profilo completa con layout responsive, form e componenti visuali riusabili.

### F — prodotto integrato futuro

Integrare layout, comportamento JavaScript, API e backend nel Feisbuc full stack.

## Verifica rapida

1. Che differenza c'e fra HTML e CSS?
2. Da quali parti e composto il box model?
3. Che cosa cambia con `box-sizing: border-box`?
4. Quando useresti Flexbox invece di Grid?
5. Perche `justify-content` non significa semplicemente “allinea orizzontalmente”?
6. Perche un layout `width: 1200px` puo essere fragile?
7. A cosa serve una media query?
8. Perche non serve una media query per ogni telefono?
9. Che cosa risolve la specificita?
10. Perche `!important` non deve essere la prima soluzione?
11. Che cosa rappresenta `1fr` in Grid?
12. Perche in un debug CSS e utile vedere le regole barrate nei DevTools?

## Sintesi inclusiva

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

## Fonti e provenance

Fonti tecniche professionali:

- MDN CSS: <https://developer.mozilla.org/en-US/docs/Web/CSS>
- MDN Handling conflicts: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts>
- MDN Box model: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model>
- MDN Flexbox: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox>
- MDN Grid: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids>
- MDN Responsive design: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design>
- MDN Media queries: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Media_queries>
- MDN Custom properties: <https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties>

Provenance interna:

- `TheBitPoets/html_css_summary` pinned: sintassi CSS, box model, block/inline, padding/margin/border;
- `TheBitPoets/feisbuc` pinned: layout legacy basato su colonne/float e progetto longitudinale da modernizzare.

Riferimento docente licensed, non riprodotto nel corso:

- Manning, *CSS in Depth, Second Edition*.

Il testo, gli esempi canonici, le Activity e le soluzioni di riferimento di questo modulo sono materiale originale del corso.