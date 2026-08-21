---
marp: true
paginate: true
size: 16:9
title: 03 — Bootstrap: dal CSS nativo a un framework
---

# 03 — Bootstrap
## Dal CSS nativo a un framework frontend

UDA 21 — Frontend foundations

---

# Richiamo

Abbiamo già costruito un layout responsive con CSS nativo.

Ora possiamo capire Bootstrap come:

> una API di classi e componenti costruita sopra concetti CSS che conosciamo già.

---

# Obiettivi

Alla fine dovrai saper:

- spiegare cosa astrae Bootstrap;
- usare container, grid e utility;
- leggere una classe Bootstrap come una scelta CSS;
- usare componenti senza perdere semantica;
- decidere quando il framework accelera davvero il lavoro.

---

# Framework ≠ magia

```html
<div class="d-flex gap-3 align-items-center">
```

Dietro quelle classi ci sono concetti già noti:

```css
display: flex;
gap: ...;
align-items: center;
```

Se capisci CSS, Bootstrap diventa leggibile.

---

# Container e breakpoint

```html
<div class="container">
  ...
</div>
```

Bootstrap applica larghezze massime e padding coerenti a breakpoint definiti.

Domanda: quale problema risolve rispetto a scrivere ogni volta il proprio wrapper?

---

# Grid Bootstrap

```html
<div class="row g-3">
  <aside class="col-12 col-lg-3">...</aside>
  <main class="col-12 col-lg-9">...</main>
</div>
```

Lettura:

- mobile: una colonna;
- large: 3/12 + 9/12;
- gutter controllato.

---

# Utility class

```html
<div class="p-3 mb-3 border rounded shadow-sm">
```

Vantaggi:

- velocità;
- coerenza;
- meno CSS locale.

Rischio:

- markup rumoroso;
- uso meccanico senza capire l'effetto.

---

# Componenti

Un componente Bootstrap porta con sé:

- struttura attesa;
- classi;
- spesso comportamento/accessibilità prevista.

Esempio: navbar, alert, modal.

Prima domanda: **serve davvero un componente o basta HTML/CSS semplice?**

---

# Feisbuc: prima e dopo

Prima:

```html
<article class="post">...</article>
```

Dopo:

```html
<article class="card mb-3">
  <div class="card-body">...</div>
</article>
```

La semantica `article` resta: Bootstrap non deve cancellare il significato HTML.

---

# Errore tipico: framework come scorciatoia mentale

Se un elemento è storto e aggiungi classi casuali finché “sembra giusto”, non stai usando il framework bene.

Procedura:

1. identifica il layout desiderato;
2. traducilo in concetti CSS;
3. trova le utility/componenti equivalenti;
4. verifica nel browser.

---

# Checkpoint

Traduci mentalmente:

- `d-flex`;
- `justify-content-between`;
- `col-md-6`;
- `mt-3`;
- `w-100`.

Quale proprietà/idea CSS rappresentano?

---

# Feisbuc milestone

Rifattorizziamo la UI:

- shell responsive;
- card dei post;
- form;
- navbar;
- spaziature coerenti.

Obiettivo: ottenere velocità **senza perdere comprensione**.

---

# Handoff al laboratorio

Confronta due implementazioni:

1. CSS nativo;
2. Bootstrap.

Per ogni scelta annota:

- cosa è stato sostituito;
- quale classe Bootstrap lo rappresenta;
- quale CSS equivalente avresti scritto.

---

# Recap

Bootstrap è utile quando:

- conosci il problema CSS sottostante;
- vuoi convenzioni coerenti;
- accetti la sua API di classi/componenti.

Non sostituisce la comprensione di HTML e CSS.

Prossimo modulo: **JavaScript, DOM e Browser APIs**.