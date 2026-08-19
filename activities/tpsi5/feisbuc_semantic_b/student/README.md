# Activity B — Feisbuc milestone 0

## Obiettivo

Trasformare una pagina che usa contenitori generici in un documento che esprime meglio il significato delle sue parti.

Non devi renderla bella: **nessun CSS**. Non devi renderla interattiva: **nessun JavaScript**.

## Strategia

Per ogni `div` chiediti:

> questo blocco ha un ruolo riconoscibile nella pagina?

Se la risposta e si, valuta un elemento semantico. Se la risposta e no, `div` puo rimanere la scelta corretta.

## Trasformazioni richieste

- intestazione principale → `header`;
- menu → `nav` con `aria-label="Navigazione principale"`;
- contenuto principale → `main`;
- feed → `section id="feed" aria-labelledby="feed-title"`;
- titolo Feed → `h2 id="feed-title"`;
- ogni post → `article`;
- autore del post → `h3`;
- blocco finale → `footer`.

Il profilo puo essere una seconda `section` oppure un contenitore semanticamente motivato: spiega la tua scelta.

## Regola importante

Non fare una sostituzione meccanica:

```text
div -> sempre section
```

sarebbe sbagliato quanto usare sempre `div`.

## Confronto con la documentazione

Prima di consegnare verifica almeno:

- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/main
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/article

## Checklist

- [ ] un solo `h1`;
- [ ] un solo `main`;
- [ ] menu dentro `nav`;
- [ ] feed dentro `section`;
- [ ] feed collegato a `feed-title`;
- [ ] due post come `article`;
- [ ] heading h1 → h2 → h3 coerenti;
- [ ] `footer` usato per la chiusura;
- [ ] nessun CSS;
- [ ] nessun JavaScript;
- [ ] so indicare almeno un caso in cui `div` rimane corretto.

## Perche e una milestone Feisbuc

Questo file non verra buttato via. Le prossime milestone aggiungeranno progressivamente layout CSS, responsive design, JavaScript, API REST, database, autenticazione e realtime.
