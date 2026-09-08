# Bootstrap: dal CSS nativo a un framework frontend

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> conosciamo già cascade, box model, Flexbox, Grid e responsive design. Bootstrap viene quindi letto come un'API di classi e componenti costruita sopra la Web Platform, non come una scorciatoia incomprensibile.</p>
<p align="justify"><strong>Domande guida:</strong> quale concetto CSS applica una utility? Quando una convenzione condivisa migliora il progetto? Quali responsabilità restano comunque dell'autore?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> tradurre classi Bootstrap in comportamenti CSS, costruire layout e form accessibili, distinguere componenti statici e interattivi e riconoscere il class soup.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 04 aggiungerà comportamento alla UI con JavaScript, DOM ed eventi.</p>

</details>
</td></tr></table>

<p align="justify">Stato: <strong>draft didattico</strong>. Questa lezione conclude il blocco CSS di UDA 21 introducendo Bootstrap <strong>dopo</strong> cascade, box model, Flexbox, Grid e responsive design.</p>

## Obiettivi

<p align="justify">Al termine della lezione lo studente deve saper:</p>

<ul>
  <li>spiegare che cosa offre un framework CSS e quale problema risolve;</li>
  <li>distinguere concetti CSS nativi da convenzioni/classi Bootstrap;</li>
  <li>usare container, grid, breakpoint e utility senza perdere la semantica HTML;</li>
  <li>usare componenti come navbar, card e button sapendo quali comportamenti richiedono JavaScript;</li>
  <li>leggere la documentazione ufficiale Bootstrap e risalire al concetto CSS sottostante;</li>
  <li>evitare l'uso di Bootstrap come sostituto della conoscenza di CSS;</li>
  <li>rifattorizzare la shell Feisbuc mantenendo accessibilità e responsive design;</li>
  <li>motivare quando usare una utility, un componente o CSS personalizzato.</li>
</ul>

## Prerequisiti

<ul>
  <li>HTML semantico;</li>
  <li>cascade, specificità e inheritance;</li>
  <li>box model e <code>box-sizing</code>;</li>
  <li>Flexbox e Grid;</li>
  <li>responsive design mobile-first e media query;</li>
  <li>Activity A-D di UDA 21.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — Dispensa ↔ Bootstrap e MDN</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-bootstrap-platform">Framework e Web Platform</a></td><td><a href="https://getbootstrap.com/docs/5.3/getting-started/introduction/">Bootstrap — Introduction</a><br><a href="GUIDA_USO_MDN.md#mdn-guide-source-choice">Scegliere la fonte giusta</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-bootstrap-layout">Container, Grid e breakpoint</a></td><td><a href="https://getbootstrap.com/docs/5.3/layout/grid/">Bootstrap — Grid system</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-bootstrap-utilities">Utilities</a></td><td><a href="https://getbootstrap.com/docs/5.3/utilities/api/">Bootstrap — Utility API</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-bootstrap-components">Componenti e JavaScript</a></td><td><a href="https://getbootstrap.com/docs/5.3/components/card/">Bootstrap — Card</a><br><a href="https://getbootstrap.com/docs/5.3/getting-started/javascript/">Bootstrap — JavaScript</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-bootstrap-forms">Form e accessibilità</a></td><td><a href="https://getbootstrap.com/docs/5.3/forms/overview/">Bootstrap — Forms</a><br><a href="https://getbootstrap.com/docs/5.3/getting-started/accessibility/">Bootstrap — Accessibility</a></td><td>&#128994; studiare ora</td></tr>
<tr><td>Sass, theming avanzato e plugin esterni</td><td><a href="https://getbootstrap.com/docs/5.3/customize/overview/">Bootstrap — Customize</a></td><td>&#128993; riconoscere, fuori dal core</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">Nel modulo precedente abbiamo scritto direttamente regole come:</p>

```css
.page-shell {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 56rem) {
  .page-shell {
    grid-template-columns: minmax(0, 1fr) minmax(0, 2fr) minmax(0, 1fr);
  }
}
```

<p align="justify">Funziona, ma molte applicazioni ripetono schemi simili: container centrati, colonne responsive, spaziature, pulsanti, navbar, card, form.</p>

<p align="justify">Un framework CSS fornisce <strong>convenzioni e componenti riutilizzabili</strong> per questi problemi ricorrenti.</p>

<p align="justify">La domanda importante non è quindi:</p>

<blockquote>
<p align="justify">Quale classe Bootstrap devo ricordare?</p>
</blockquote>

<p align="justify">ma:</p>

<blockquote>
<p align="justify">Quale concetto CSS sto delegando al framework?</p>
</blockquote>

## Bootstrap nel corso

<p align="justify">La linea usata in questo modulo è <strong>Bootstrap 5.3</strong>. Al momento della redazione la documentazione ufficiale indica la release 5.3.8.</p>

<p align="justify">La versione va sempre verificata nella documentazione ufficiale prima di aggiornare gli esempi del corso.</p>

<p align="justify">Riferimento: <a href="https://getbootstrap.com/docs/5.3/">https://getbootstrap.com/docs/5.3/</a></p>

<a id="lesson-bootstrap-platform"></a>
## Un framework non sostituisce la Web Platform

<p align="justify">Bootstrap continua a produrre pagine basate su:</p>

```text
HTML
 +
CSS
 +
JavaScript quando un componente ne ha bisogno
```

<p align="justify">Per esempio:</p>

```html
<div class="d-flex gap-3">
```

<p align="justify">non introduce un nuovo layout engine. La classe <code>d-flex</code> porta a un comportamento equivalente al concetto:</p>

```css
display: flex;
```

<p align="justify">La utility <code>gap-3</code> applica invece una spaziatura secondo la scala definita dal framework.</p>

<p align="justify">Questa relazione va sempre resa esplicita durante il corso.</p>

## Metodo di lavoro con la documentazione

<p align="justify">Quando incontri una classe nuova:</p>

<ol>
  <li>identifica il problema che vuoi risolvere;</li>
  <li>cerca nella documentazione Bootstrap;</li>
  <li>prova l'esempio minimo;</li>
  <li>individua il concetto CSS sottostante;</li>
  <li>usa la classe solo se rende il codice più chiaro/manutenibile;</li>
  <li>evita di sommare utility senza capire quale regola stai ottenendo.</li>
</ol>

<p align="justify">MDN resta il riferimento per capire <strong>CSS e Web Platform</strong>; la documentazione Bootstrap descrive invece l'API del framework.</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> Due documentazioni, due responsabilità:</strong> consulta <a href="GUIDA_USO_MDN.md#mdn-guide-source-choice">come scegliere la fonte nel corso full stack</a>. Per una classe Bootstrap parti dalla documentazione Bootstrap; per comprendere la regola <code>display</code>, il layout Flex/Grid, il box model o il comportamento HTML sottostante usa MDN.</p>
<p align="justify"><strong>Prodotto atteso:</strong> per ogni utility nuova indica sia la classe del framework sia il concetto Web Platform che sta applicando.</p>
</td></tr></table>

## Caricare Bootstrap

<p align="justify">Per gli esempi iniziali possiamo usare i link CDN documentati ufficialmente.</p>

```html
<link
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
  rel="stylesheet"
  integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
  crossorigin="anonymous"
>
```

<p align="justify">Per i componenti interattivi che richiedono JavaScript:</p>

```html
<script
  src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
  integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
  crossorigin="anonymous"
></script>
```

<p align="justify">Il bundle include ciò che serve ai componenti interattivi più comuni.</p>

### Uso offline

<p align="justify">Il concetto didattico <strong>non dipende dal CDN</strong>. In un laboratorio senza accesso Internet il docente può distribuire i file compilati ufficiali di Bootstrap e sostituire gli URL con path locali.</p>

<p align="justify">Più avanti, quando avremo introdotto npm, vedremo anche l'installazione come dipendenza del progetto.</p>

<a id="lesson-bootstrap-layout"></a>
## Container

<p align="justify">Un container gestisce larghezza massima, centratura e padding orizzontale.</p>

```html
<main class="container py-4">
  ...
</main>
```

<p align="justify">Prima di usare <code>container</code>, chiediti come avresti ottenuto un risultato simile con CSS nativo:</p>

```css
main {
  width: min(100% - 2rem, 75rem);
  margin-inline: auto;
}
```

<p align="justify">Non sono implementazioni identiche, ma risolvono una famiglia di problemi simile.</p>

## Grid Bootstrap

<p align="justify">Bootstrap usa una griglia a 12 colonne.</p>

```html
<div class="row g-3">
  <aside class="col-12 col-lg-3">Profilo</aside>
  <section class="col-12 col-lg-6">Feed</section>
  <aside class="col-12 col-lg-3">Tendenze</aside>
</div>
```

<p align="justify">Leggila così:</p>

<ul>
  <li><code>row</code>: riga della griglia;</li>
  <li><code>g-3</code>: gutter/spaziatura;</li>
  <li><code>col-12</code>: su viewport piccoli occupa 12 colonne su 12;</li>
  <li><code>col-lg-3</code>: da <code>lg</code> occupa 3/12;</li>
  <li><code>col-lg-6</code>: da <code>lg</code> occupa 6/12.</li>
</ul>

<p align="justify">Il risultato concettuale richiama la milestone Grid precedente:</p>

```text
mobile  -> una colonna
wide    -> 3 / 6 / 3
```

<p align="justify">La differenza è che adesso il breakpoint e le proporzioni sono espresse attraverso l'API del framework.</p>

## Breakpoint: non sono dispositivi

<p align="justify">Non pensare:</p>

```text
lg = laptop
md = tablet
sm = telefono
```

<p align="justify">Pensa invece:</p>

<blockquote>
<p align="justify">il layout cambia quando il contenuto ha abbastanza spazio.</p>
</blockquote>

<p align="justify">I nomi Bootstrap sono convenzioni di breakpoint; non descrivono un dispositivo reale.</p>

<a id="lesson-bootstrap-utilities"></a>
## Utilities

<p align="justify">Le utility permettono di esprimere regole frequenti:</p>

```html
<div class="d-flex flex-wrap gap-2 align-items-center">
```

<p align="justify">Mappa concettuale:</p>

<table align="center">
<thead>
<tr>
<th>Bootstrap</th>
<th>concetto CSS</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>d-flex</code></td>
<td><code>display: flex</code></td>
</tr>
<tr>
<td><code>flex-wrap</code></td>
<td><code>flex-wrap: wrap</code></td>
</tr>
<tr>
<td><code>gap-2</code></td>
<td><code>gap</code></td>
</tr>
<tr>
<td><code>align-items-center</code></td>
<td><code>align-items: center</code></td>
</tr>
<tr>
<td><code>p-3</code></td>
<td>padding dalla scala Bootstrap</td>
</tr>
<tr>
<td><code>mb-3</code></td>
<td>margin-bottom dalla scala Bootstrap</td>
</tr>
</tbody>
</table>

<p align="justify">Le utility sono utili finché rendono evidente l'intento. Se un elemento accumula troppe classi o una regola rappresenta il design specifico del prodotto, CSS personalizzato può essere più leggibile.</p>

<a id="lesson-bootstrap-components"></a>
## Componenti

### Card

<p align="justify">Un post Feisbuc può diventare una card mantenendo <code>article</code> come elemento semantico:</p>

```html
<article class="card mb-3">
  <div class="card-body">
    <h3 class="card-title h5">Titolo del post</h3>
    <p class="card-text">Contenuto del post.</p>
    <button class="btn btn-outline-primary" type="button">Mi piace</button>
  </div>
</article>
```

<p align="justify">Bootstrap aggiunge presentazione; <code>article</code> continua a comunicare il significato del contenuto.</p>

### Navbar

<p align="justify">Una navbar responsiva può usare il componente Bootstrap e il plugin Collapse.</p>

<p align="justify">Il fatto che Bootstrap fornisca il comportamento non elimina le responsabilità HTML:</p>

<ul>
  <li>usare un landmark di navigazione;</li>
  <li>mantenere label comprensibili;</li>
  <li>collegare correttamente bottone e pannello collassabile;</li>
  <li>conservare <code>aria-*</code> richiesti dal componente.</li>
</ul>

## Componenti JavaScript

<p align="justify">Non tutti i componenti Bootstrap richiedono JavaScript.</p>

<p align="justify">Una grid o una card funzionano con CSS. Una navbar con collapse richiede invece il bundle JavaScript.</p>

<p align="justify">Questa distinzione prepara un concetto importante per il seguito:</p>

```text
presentazione statica
        !=
comportamento interattivo
```

<a id="lesson-bootstrap-forms"></a>
## Form Bootstrap: stile, significato e validazione

<p align="justify">Bootstrap puo rendere coerente l'aspetto di un form, ma il contratto del form resta HTML. Il <code>type</code> corretto comunica il tipo di dato atteso, la <code>label</code> assegna un nome al controllo e <code>aria-describedby</code> puo collegare un aiuto breve.</p>

```html
<form class="row g-3" novalidate>
  <div class="col-12">
    <label class="form-label" for="post-text">Testo del post</label>
    <textarea
      class="form-control"
      id="post-text"
      name="text"
      required
      maxlength="280"
      aria-describedby="post-help"
    ></textarea>
    <div id="post-help" class="form-text">Massimo 280 caratteri.</div>
    <div class="invalid-feedback">Inserisci il testo del post.</div>
  </div>
  <div class="col-12">
    <button class="btn btn-primary" type="submit">Pubblica</button>
  </div>
</form>
```

<p align="justify">La validazione ha confini diversi:</p>

<ul>
  <li>gli attributi HTML (<code>required</code>, <code>maxlength</code>, <code>type</code>) aiutano il browser e l'utente;</li>
  <li>classi come <code>.was-validated</code> e <code>.is-invalid</code> mostrano visivamente uno stato gia determinato;</li>
  <li>JavaScript coordina l'interazione quando serve;</li>
  <li>il server deve comunque validare ogni richiesta, perche il client non e un confine affidabile.</li>
</ul>

<p align="justify">Non usiamo il solo colore per indicare un errore: testo e associazioni semantiche devono renderlo comprensibile. Nella documentazione Bootstrap studia <a href="https://getbootstrap.com/docs/5.3/forms/form-control/">form controls</a> e <a href="https://getbootstrap.com/docs/5.3/forms/validation/">validation</a>; personalizzazioni complesse e validazione asincrona arriveranno quando esistera il backend.</p>

## Bootstrap e accessibilità

<p align="justify">Un framework può fornire pattern utili, ma <strong>non rende automaticamente accessibile un'applicazione</strong>.</p>

<p align="justify">Rimangono responsabilità dello sviluppatore:</p>

<ul>
  <li>gerarchia degli heading;</li>
  <li>landmark semantici;</li>
  <li>testo dei link;</li>
  <li>label dei form;</li>
  <li>contrasto delle personalizzazioni;</li>
  <li>focus e uso da tastiera;</li>
  <li>attributi ARIA solo quando necessari e corretti.</li>
</ul>

## Bootstrap e CSS personalizzato

<p align="justify">Nel progetto finale di questo modulo useremo Bootstrap per:</p>

<ul>
  <li>macro-layout;</li>
  <li>spaziature standard;</li>
  <li>navbar;</li>
  <li>card;</li>
  <li>pulsanti;</li>
  <li>utility responsive.</li>
</ul>

<p align="justify">Il CSS personalizzato resta per ciò che appartiene davvero al prodotto, per esempio:</p>

```css
:root {
  --feisbuc-brand: #243b53;
}

.feisbuc-brand {
  color: var(--feisbuc-brand);
}
```

<p align="justify">Non vogliamo riscrivere in <code>custom.css</code> il sistema di grid che abbiamo appena scelto di delegare a Bootstrap.</p>

## Confronto: CSS nativo e Bootstrap

<table align="center">
<thead>
<tr>
<th>Problema</th>
<th>CSS nativo</th>
<th>Bootstrap</th>
</tr>
</thead>
<tbody>
<tr>
<td>pagina centrata</td>
<td><code>width</code> + <code>margin-inline</code></td>
<td><code>container</code></td>
</tr>
<tr>
<td>layout responsive</td>
<td>Grid + media query</td>
<td><code>row</code> + <code>col-*</code></td>
</tr>
<tr>
<td>gruppo orizzontale</td>
<td>Flexbox</td>
<td><code>d-flex</code> + utility</td>
</tr>
<tr>
<td>spaziatura</td>
<td><code>margin</code> / <code>padding</code> / <code>gap</code></td>
<td><code>m-*</code>, <code>p-*</code>, <code>gap-*</code></td>
</tr>
<tr>
<td>post visuale</td>
<td>regole custom</td>
<td><code>card</code></td>
</tr>
<tr>
<td>azione</td>
<td>regole custom</td>
<td><code>btn</code></td>
</tr>
<tr>
<td>nav collassabile</td>
<td>CSS + JS custom</td>
<td><code>navbar</code> + Collapse</td>
</tr>
</tbody>
</table>

<p align="justify">L'obiettivo non è stabilire quale soluzione sia sempre migliore, ma saperne riconoscere il <strong>trade-off</strong>.</p>

## Errore frequente: class soup

<p align="justify">Questo markup è tecnicamente possibile:</p>

```html
<div class="d-flex flex-column flex-md-row align-items-start align-items-md-center gap-1 gap-md-3 p-1 p-md-3 mt-2 mb-4 border rounded shadow-sm">
```

<p align="justify">ma può diventare difficile da leggere.</p>

<p align="justify">Domanda da farsi:</p>

<blockquote>
<p align="justify">queste classi descrivono un pattern standard oppure sto nascondendo un componente di design che meriterebbe una classe nostra?</p>
</blockquote>

## Errore frequente: combattere Bootstrap

<p align="justify">Se il progetto contiene decine di override ad alta specificità e <code>!important</code>, probabilmente stiamo usando il framework contro il suo modello.</p>

<p align="justify">Prima di aggiungere un override:</p>

<ol>
  <li>controlla la documentazione;</li>
  <li>verifica se esiste una utility;</li>
  <li>ispeziona la regola in DevTools;</li>
  <li>valuta se il componente Bootstrap è davvero adatto al problema.</li>
</ol>

## Quando Bootstrap è una buona scelta

<p align="justify">Può essere utile quando:</p>

<ul>
  <li>serve prototipare rapidamente;</li>
  <li>il team vuole convenzioni condivise;</li>
  <li>il design è compatibile con i componenti disponibili;</li>
  <li>si vogliono usare utility responsive già coerenti.</li>
</ul>

<p align="justify">Può essere meno adatto quando:</p>

<ul>
  <li>il design è estremamente custom;</li>
  <li>il framework introduce più override che vantaggi;</li>
  <li>si vuole minimizzare al massimo il CSS/JS consegnato;</li>
  <li>il team non comprende i fondamenti e finisce per dipendere da classi memorizzate.</li>
</ul>

## Feisbuc milestone 2

<p align="justify">La nuova milestone parte dalla shell responsive costruita con CSS nativo.</p>

<p align="justify">Lo studente deve trasformarla in una versione Bootstrap mantenendo:</p>

<ul>
  <li>semantica HTML;</li>
  <li>layout mobile-first;</li>
  <li>tre regioni desktop 3/6/3;</li>
  <li>navbar responsive;</li>
  <li>post come <code>article</code> + card;</li>
  <li>azioni come button Bootstrap;</li>
  <li>CSS personalizzato minimo;</li>
  <li>una mappa esplicita fra soluzione nativa e astrazione Bootstrap.</li>
</ul>

<p align="justify">La milestone è:</p>

```text
feisbuc-02-bootstrap-ui
```

## Activity E — mini-progetto

<p align="justify"><code>tpsi5-activity-e-feisbuc-bootstrap-ui-001</code></p>

<p align="justify">Non basta ottenere una pagina visivamente corretta. La consegna richiede anche <code>MAPPING.md</code>, nel quale lo studente documenta almeno sei scelte del tipo:</p>

```text
problema
-> soluzione CSS nativa precedente
-> classe/componente Bootstrap scelto
-> concetto CSS sottostante
```

<p align="justify">In questo modo il framework non diventa magia.</p>

## Esercizi A-F del modulo

<ul>
  <li><strong>A</strong>: apri un esempio della grid ufficiale e individua container, row e col;</li>
  <li><strong>B</strong>: sostituisci una regola Flexbox semplice con utility Bootstrap equivalenti;</li>
  <li><strong>C</strong>: ricrea un layout 1-colonna / 3-colonne con il sistema a 12 colonne;</li>
  <li><strong>D</strong>: diagnostica una navbar che non collassa perché manca il bundle o il target non coincide;</li>
  <li><strong>E</strong>: completa la milestone Feisbuc Bootstrap;</li>
  <li><strong>F</strong>: futuro prodotto integrato con frontend dinamico e backend.</li>
</ul>

## Verifica rapida

<ol>
  <li>Bootstrap sostituisce HTML/CSS/JavaScript?</li>
  <li>Che differenza c'è fra <code>container</code>, <code>row</code> e <code>col-*</code>?</li>
  <li>Che concetto CSS esprime <code>d-flex</code>?</li>
  <li>Perché <code>article.card</code> è preferibile a trasformare tutto in <code>div.card</code>?</li>
  <li>Quali componenti possono richiedere il bundle JavaScript?</li>
  <li>Quando è preferibile una classe CSS custom a dieci utility?</li>
  <li>Perché dobbiamo saper leggere ancora MDN?</li>
</ol>

## Sintesi inclusiva

```text
CSS nativo
   |
   +-- capisco layout, cascade, box model
   |
   v
Bootstrap
   |
   +-- convenzioni
   +-- grid
   +-- utilities
   +-- components
   |
   v
sviluppo piu rapido senza perdere il modello mentale CSS
```

## Fonti e collegamenti

### Studente

<ul>
  <li>Bootstrap 5.3 — Getting started: <a href="https://getbootstrap.com/docs/5.3/getting-started/introduction/">https://getbootstrap.com/docs/5.3/getting-started/introduction/</a></li>
  <li>Bootstrap layout/grid: <a href="https://getbootstrap.com/docs/5.3/layout/grid/">https://getbootstrap.com/docs/5.3/layout/grid/</a></li>
  <li>Bootstrap utilities: <a href="https://getbootstrap.com/docs/5.3/utilities/api/">https://getbootstrap.com/docs/5.3/utilities/api/</a></li>
  <li>Bootstrap navbar: <a href="https://getbootstrap.com/docs/5.3/components/navbar/">https://getbootstrap.com/docs/5.3/components/navbar/</a></li>
  <li>Bootstrap card: <a href="https://getbootstrap.com/docs/5.3/components/card/">https://getbootstrap.com/docs/5.3/components/card/</a></li>
  <li>MDN responsive design: <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design">https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design</a></li>
</ul>

### Docente

<ul>
  <li>Manning, <em>CSS in Depth, Second Edition</em> — teacher-reference licensed;</li>
  <li>documentazione ufficiale Bootstrap per esempi/versionamento;</li>
  <li>modulo precedente <code>02_CSS_MODERNO_RESPONSIVE.md</code> per mantenere il mapping framework -> CSS.</li>
</ul>

## Activity correlate

<ul>
  <li><code>tpsi5-activity-c-feisbuc-responsive-layout-001</code> — baseline CSS nativa;</li>
  <li><code>tpsi5-activity-d-debug-responsive-css-001</code> — debugging;</li>
  <li><code>tpsi5-activity-e-feisbuc-bootstrap-ui-001</code> — mini-progetto Bootstrap.</li>
</ul>
