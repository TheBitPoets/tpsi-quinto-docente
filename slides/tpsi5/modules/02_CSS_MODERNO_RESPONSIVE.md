---
marp: true
paginate: true
size: 16:9
title: 02 — CSS moderno e responsive design
---

# 02 — CSS moderno e responsive design
## Dal documento al layout adattivo

UDA 21 — Frontend foundations

---

# Richiamo

HTML ha descritto **che cosa è** il contenuto.

Oggi CSS risponde a:

> Come viene presentato lo stesso documento su schermi e spazi diversi?

---

# Obiettivi

Alla fine dovrai saper:

- spiegare cascade, inheritance e specificity;
- ragionare sul box model;
- scegliere Flexbox o Grid;
- costruire layout mobile-first;
- usare media query con criterio;
- diagnosticare un layout rotto con DevTools.

---

# La cascade

Più regole possono influenzare lo stesso elemento.

```css
p { color: black; }
.post p { color: #333; }
```

Il browser deve decidere quale dichiarazione vince.

La cascade combina:

- origine;
- importanza;
- specificity;
- ordine.

---

# Specificity: non combatterla

```css
#feed .post p { ... }
```

funziona, ma crea CSS difficile da sovrascrivere.

Preferisci selettori comprensibili e stabili:

```css
.post__text { ... }
```

Il problema non è “vincere” la specificity, ma evitare guerre di selettori.

---

# Box model

Ogni elemento occupa spazio come:

```text
margin
  border
    padding
      content
```

Con:

```css
* { box-sizing: border-box; }
```

larghezze e altezze diventano più intuitive da gestire.

---

# Flexbox: una dimensione principale

```css
.toolbar {
  display: flex;
  gap: 1rem;
  align-items: center;
}
```

Ottimo per:

- righe/colonne;
- distribuzione di elementi;
- allineamento.

---

# Grid: struttura bidimensionale

```css
.layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 1.5rem;
}
```

Ottimo quando righe e colonne fanno parte della struttura del layout.

---

# Mobile-first

Parti dalla versione più stretta:

```css
.feed {
  padding: 1rem;
}
```

Poi aggiungi complessità:

```css
@media (min-width: 768px) {
  .feed {
    max-width: 720px;
    margin: 0 auto;
  }
}
```

---

# Responsive ≠ solo media query

Un layout è responsive anche grazie a:

- `max-width`;
- unità relative;
- Flexbox/Grid fluidi;
- wrapping;
- immagini adattive;
- contenuto che non dipende da dimensioni fisse.

---

# Errore tipico: pixel ovunque

```css
.card {
  width: 640px;
}
```

Su uno schermo da 390 px crea overflow.

Meglio:

```css
.card {
  width: min(100%, 640px);
}
```

---

# Debug con DevTools

Quando un layout è rotto controlla:

- box model;
- regola sovrascritta;
- overflow;
- dimensioni calcolate;
- flex/grid overlay;
- breakpoint attivo.

Non correggere “a tentativi” senza osservare lo stile calcolato.

---

# Checkpoint

Scegli lo strumento migliore:

1. toolbar orizzontale;
2. dashboard a due colonne;
3. card che non deve superare il viewport;
4. layout che cambia a 768 px;
5. spazio costante tra elementi.

---

# Feisbuc milestone

Portiamo lo skeleton HTML a un layout:

- leggibile su mobile;
- centrato e contenuto su desktop;
- feed coerente;
- form usabile;
- senza framework CSS.

Prima capiamo CSS, poi useremo Bootstrap.

---

# Handoff al laboratorio

Durante l'Activity:

1. parti da HTML semantico;
2. costruisci il layout nativo;
3. prova viewport diversi;
4. introduci un errore responsive;
5. diagnosticalo con DevTools;
6. documenta la causa, non solo la correzione.

---

# Recap

CSS moderno richiede di capire:

- cascade;
- box model;
- layout primitives;
- fluidità;
- breakpoint come eccezioni controllate.

Prossimo modulo: **Bootstrap come framework sopra CSS**.