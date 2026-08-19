# Bootstrap: dal CSS nativo a un framework frontend

Stato: **draft didattico**. Questa lezione conclude il blocco CSS di UDA 21 introducendo Bootstrap **dopo** cascade, box model, Flexbox, Grid e responsive design.

## Obiettivi

Al termine della lezione lo studente deve saper:

- spiegare che cosa offre un framework CSS e quale problema risolve;
- distinguere concetti CSS nativi da convenzioni/classi Bootstrap;
- usare container, grid, breakpoint e utility senza perdere la semantica HTML;
- usare componenti come navbar, card e button sapendo quali comportamenti richiedono JavaScript;
- leggere la documentazione ufficiale Bootstrap e risalire al concetto CSS sottostante;
- evitare l'uso di Bootstrap come sostituto della conoscenza di CSS;
- rifattorizzare la shell Feisbuc mantenendo accessibilità e responsive design;
- motivare quando usare una utility, un componente o CSS personalizzato.

## Prerequisiti

- HTML semantico;
- cascade, specificità e inheritance;
- box model e `box-sizing`;
- Flexbox e Grid;
- responsive design mobile-first e media query;
- Activity A-D di UDA 21.

## Problema iniziale

Nel modulo precedente abbiamo scritto direttamente regole come:

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

Funziona, ma molte applicazioni ripetono schemi simili: container centrati, colonne responsive, spaziature, pulsanti, navbar, card, form.

Un framework CSS fornisce **convenzioni e componenti riutilizzabili** per questi problemi ricorrenti.

La domanda importante non è quindi:

> Quale classe Bootstrap devo ricordare?

ma:

> Quale concetto CSS sto delegando al framework?

## Bootstrap nel corso

La linea usata in questo modulo è **Bootstrap 5.3**. Al momento della redazione la documentazione ufficiale indica la release 5.3.8.

La versione va sempre verificata nella documentazione ufficiale prima di aggiornare gli esempi del corso.

Riferimento: <https://getbootstrap.com/docs/5.3/>

## Un framework non sostituisce la Web Platform

Bootstrap continua a produrre pagine basate su:

```text
HTML
 +
CSS
 +
JavaScript quando un componente ne ha bisogno
```

Per esempio:

```html
<div class="d-flex gap-3">
```

non introduce un nuovo layout engine. La classe `d-flex` porta a un comportamento equivalente al concetto:

```css
display: flex;
```

La utility `gap-3` applica invece una spaziatura secondo la scala definita dal framework.

Questa relazione va sempre resa esplicita durante il corso.

## Metodo di lavoro con la documentazione

Quando incontri una classe nuova:

1. identifica il problema che vuoi risolvere;
2. cerca nella documentazione Bootstrap;
3. prova l'esempio minimo;
4. individua il concetto CSS sottostante;
5. usa la classe solo se rende il codice più chiaro/manutenibile;
6. evita di sommare utility senza capire quale regola stai ottenendo.

MDN resta il riferimento per capire **CSS e Web Platform**; la documentazione Bootstrap descrive invece l'API del framework.

## Caricare Bootstrap

Per gli esempi iniziali possiamo usare i link CDN documentati ufficialmente.

```html
<link
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
  rel="stylesheet"
  integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
  crossorigin="anonymous"
>
```

Per i componenti interattivi che richiedono JavaScript:

```html
<script
  src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
  integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
  crossorigin="anonymous"
></script>
```

Il bundle include ciò che serve ai componenti interattivi più comuni.

### Uso offline

Il concetto didattico **non dipende dal CDN**. In un laboratorio senza accesso Internet il docente può distribuire i file compilati ufficiali di Bootstrap e sostituire gli URL con path locali.

Più avanti, quando avremo introdotto npm, vedremo anche l'installazione come dipendenza del progetto.

## Container

Un container gestisce larghezza massima, centratura e padding orizzontale.

```html
<main class="container py-4">
  ...
</main>
```

Prima di usare `container`, chiediti come avresti ottenuto un risultato simile con CSS nativo:

```css
main {
  width: min(100% - 2rem, 75rem);
  margin-inline: auto;
}
```

Non sono implementazioni identiche, ma risolvono una famiglia di problemi simile.

## Grid Bootstrap

Bootstrap usa una griglia a 12 colonne.

```html
<div class="row g-3">
  <aside class="col-12 col-lg-3">Profilo</aside>
  <section class="col-12 col-lg-6">Feed</section>
  <aside class="col-12 col-lg-3">Tendenze</aside>
</div>
```

Leggila così:

- `row`: riga della griglia;
- `g-3`: gutter/spaziatura;
- `col-12`: su viewport piccoli occupa 12 colonne su 12;
- `col-lg-3`: da `lg` occupa 3/12;
- `col-lg-6`: da `lg` occupa 6/12.

Il risultato concettuale richiama la milestone Grid precedente:

```text
mobile  -> una colonna
wide    -> 3 / 6 / 3
```

La differenza è che adesso il breakpoint e le proporzioni sono espresse attraverso l'API del framework.

## Breakpoint: non sono dispositivi

Non pensare:

```text
lg = laptop
md = tablet
sm = telefono
```

Pensa invece:

> il layout cambia quando il contenuto ha abbastanza spazio.

I nomi Bootstrap sono convenzioni di breakpoint; non descrivono un dispositivo reale.

## Utilities

Le utility permettono di esprimere regole frequenti:

```html
<div class="d-flex flex-wrap gap-2 align-items-center">
```

Mappa concettuale:

| Bootstrap | concetto CSS |
| --- | --- |
| `d-flex` | `display: flex` |
| `flex-wrap` | `flex-wrap: wrap` |
| `gap-2` | `gap` |
| `align-items-center` | `align-items: center` |
| `p-3` | padding dalla scala Bootstrap |
| `mb-3` | margin-bottom dalla scala Bootstrap |

Le utility sono utili finché rendono evidente l'intento. Se un elemento accumula troppe classi o una regola rappresenta il design specifico del prodotto, CSS personalizzato può essere più leggibile.

## Componenti

### Card

Un post Feisbuc può diventare una card mantenendo `article` come elemento semantico:

```html
<article class="card mb-3">
  <div class="card-body">
    <h3 class="card-title h5">Titolo del post</h3>
    <p class="card-text">Contenuto del post.</p>
    <button class="btn btn-outline-primary" type="button">Mi piace</button>
  </div>
</article>
```

Bootstrap aggiunge presentazione; `article` continua a comunicare il significato del contenuto.

### Navbar

Una navbar responsiva può usare il componente Bootstrap e il plugin Collapse.

Il fatto che Bootstrap fornisca il comportamento non elimina le responsabilità HTML:

- usare un landmark di navigazione;
- mantenere label comprensibili;
- collegare correttamente bottone e pannello collassabile;
- conservare `aria-*` richiesti dal componente.

## Componenti JavaScript

Non tutti i componenti Bootstrap richiedono JavaScript.

Una grid o una card funzionano con CSS. Una navbar con collapse richiede invece il bundle JavaScript.

Questa distinzione prepara un concetto importante per il seguito:

```text
presentazione statica
        !=
comportamento interattivo
```

## Bootstrap e accessibilità

Un framework può fornire pattern utili, ma **non rende automaticamente accessibile un'applicazione**.

Rimangono responsabilità dello sviluppatore:

- gerarchia degli heading;
- landmark semantici;
- testo dei link;
- label dei form;
- contrasto delle personalizzazioni;
- focus e uso da tastiera;
- attributi ARIA solo quando necessari e corretti.

## Bootstrap e CSS personalizzato

Nel progetto finale di questo modulo useremo Bootstrap per:

- macro-layout;
- spaziature standard;
- navbar;
- card;
- pulsanti;
- utility responsive.

Il CSS personalizzato resta per ciò che appartiene davvero al prodotto, per esempio:

```css
:root {
  --feisbuc-brand: #243b53;
}

.feisbuc-brand {
  color: var(--feisbuc-brand);
}
```

Non vogliamo riscrivere in `custom.css` il sistema di grid che abbiamo appena scelto di delegare a Bootstrap.

## Confronto: CSS nativo e Bootstrap

| Problema | CSS nativo | Bootstrap |
| --- | --- | --- |
| pagina centrata | `width` + `margin-inline` | `container` |
| layout responsive | Grid + media query | `row` + `col-*` |
| gruppo orizzontale | Flexbox | `d-flex` + utility |
| spaziatura | `margin` / `padding` / `gap` | `m-*`, `p-*`, `gap-*` |
| post visuale | regole custom | `card` |
| azione | regole custom | `btn` |
| nav collassabile | CSS + JS custom | `navbar` + Collapse |

L'obiettivo non è stabilire quale soluzione sia sempre migliore, ma saperne riconoscere il **trade-off**.

## Errore frequente: class soup

Questo markup è tecnicamente possibile:

```html
<div class="d-flex flex-column flex-md-row align-items-start align-items-md-center gap-1 gap-md-3 p-1 p-md-3 mt-2 mb-4 border rounded shadow-sm">
```

ma può diventare difficile da leggere.

Domanda da farsi:

> queste classi descrivono un pattern standard oppure sto nascondendo un componente di design che meriterebbe una classe nostra?

## Errore frequente: combattere Bootstrap

Se il progetto contiene decine di override ad alta specificità e `!important`, probabilmente stiamo usando il framework contro il suo modello.

Prima di aggiungere un override:

1. controlla la documentazione;
2. verifica se esiste una utility;
3. ispeziona la regola in DevTools;
4. valuta se il componente Bootstrap è davvero adatto al problema.

## Quando Bootstrap è una buona scelta

Può essere utile quando:

- serve prototipare rapidamente;
- il team vuole convenzioni condivise;
- il design è compatibile con i componenti disponibili;
- si vogliono usare utility responsive già coerenti.

Può essere meno adatto quando:

- il design è estremamente custom;
- il framework introduce più override che vantaggi;
- si vuole minimizzare al massimo il CSS/JS consegnato;
- il team non comprende i fondamenti e finisce per dipendere da classi memorizzate.

## Feisbuc milestone 2

La nuova milestone parte dalla shell responsive costruita con CSS nativo.

Lo studente deve trasformarla in una versione Bootstrap mantenendo:

- semantica HTML;
- layout mobile-first;
- tre regioni desktop 3/6/3;
- navbar responsive;
- post come `article` + card;
- azioni come button Bootstrap;
- CSS personalizzato minimo;
- una mappa esplicita fra soluzione nativa e astrazione Bootstrap.

La milestone è:

```text
feisbuc-02-bootstrap-ui
```

## Activity E — mini-progetto

`tpsi5-activity-e-feisbuc-bootstrap-ui-001`

Non basta ottenere una pagina visivamente corretta. La consegna richiede anche `MAPPING.md`, nel quale lo studente documenta almeno sei scelte del tipo:

```text
problema
-> soluzione CSS nativa precedente
-> classe/componente Bootstrap scelto
-> concetto CSS sottostante
```

In questo modo il framework non diventa magia.

## Esercizi A-F del modulo

- **A**: apri un esempio della grid ufficiale e individua container, row e col;
- **B**: sostituisci una regola Flexbox semplice con utility Bootstrap equivalenti;
- **C**: ricrea un layout 1-colonna / 3-colonne con il sistema a 12 colonne;
- **D**: diagnostica una navbar che non collassa perché manca il bundle o il target non coincide;
- **E**: completa la milestone Feisbuc Bootstrap;
- **F**: futuro prodotto integrato con frontend dinamico e backend.

## Verifica rapida

1. Bootstrap sostituisce HTML/CSS/JavaScript?
2. Che differenza c'è fra `container`, `row` e `col-*`?
3. Che concetto CSS esprime `d-flex`?
4. Perché `article.card` è preferibile a trasformare tutto in `div.card`?
5. Quali componenti possono richiedere il bundle JavaScript?
6. Quando è preferibile una classe CSS custom a dieci utility?
7. Perché dobbiamo saper leggere ancora MDN?

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

- Bootstrap 5.3 — Getting started: <https://getbootstrap.com/docs/5.3/getting-started/introduction/>
- Bootstrap layout/grid: <https://getbootstrap.com/docs/5.3/layout/grid/>
- Bootstrap utilities: <https://getbootstrap.com/docs/5.3/utilities/api/>
- Bootstrap navbar: <https://getbootstrap.com/docs/5.3/components/navbar/>
- Bootstrap card: <https://getbootstrap.com/docs/5.3/components/card/>
- MDN responsive design: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design>

### Docente

- Manning, *CSS in Depth, Second Edition* — teacher-reference licensed;
- documentazione ufficiale Bootstrap per esempi/versionamento;
- modulo precedente `02_CSS_MODERNO_RESPONSIVE.md` per mantenere il mapping framework -> CSS.

## Activity correlate

- `tpsi5-activity-c-feisbuc-responsive-layout-001` — baseline CSS nativa;
- `tpsi5-activity-d-debug-responsive-css-001` — debugging;
- `tpsi5-activity-e-feisbuc-bootstrap-ui-001` — mini-progetto Bootstrap.
