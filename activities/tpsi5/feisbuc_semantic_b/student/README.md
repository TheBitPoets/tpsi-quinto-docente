# Activity B — Feisbuc milestone 0

Tempo indicativo: 45 minuti.

## Obiettivo

Trasformare una pagina che usa contenitori generici in un documento che esprime meglio il significato delle sue parti.

Non devi renderla bella: **nessun CSS**. Non devi renderla interattiva: **nessun JavaScript**.

## Strategia

Per ogni `div` chiediti:

> questo blocco ha un ruolo riconoscibile nella pagina?

Se la risposta è sì, valuta un elemento semantico. Se la risposta è no, `div` può rimanere la scelta corretta.

## Trasformazioni richieste

- intestazione principale → `header`;
- menu → `nav` con `aria-label="Navigazione principale"`;
- contenuto principale → `main`;
- feed → `section id="feed" aria-labelledby="feed-title"`;
- titolo Feed → `h2 id="feed-title"`;
- ogni post → `article`;
- autore del post → `h3`;
- blocco finale → `footer`.

Il profilo può essere una seconda `section` oppure un contenitore semanticamente motivato: spiega la tua scelta.

## Regola importante

Non fare una sostituzione meccanica:

```text
div -> sempre section
```

sarebbe sbagliato quanto usare sempre `div`.

## Confronto con la documentazione

Prima di consegnare verifica almeno:

- [Document and website structure](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents)
- [Elemento `main`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/main)
- [Elemento `article`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/article)

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

## Perché è una milestone Feisbuc

Questo file non verrà buttato via. Le prossime milestone aggiungeranno progressivamente layout CSS, responsive design, JavaScript, API REST, database, autenticazione e realtime.
