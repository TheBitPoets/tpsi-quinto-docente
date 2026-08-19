# Activity D — Debug Feisbuc JavaScript

## Regola principale

**Prima diagnosi, poi fix.**

Lo starter contiene piu problemi indipendenti. Se cambi codice a caso potresti nascondere un sintomo senza capire la causa.

## Procedura

1. apri la pagina e la Console;
2. prova a pubblicare un post;
3. registra in `DIAGNOSI.md` la prima eccezione e lo stack;
4. usa breakpoint nel listener `submit`;
5. ispeziona il pannello Application/Storage;
6. verifica quando vengono registrati i listener dei like;
7. crea un post dopo il caricamento e prova il suo bottone;
8. prova testo che contiene markup, per esempio `<strong>ciao</strong>`;
9. soltanto dopo almeno cinque diagnosi, correggi il codice.

## Definition of done

- [ ] submit non produce eccezioni;
- [ ] `preventDefault()` usa il parametro corretto del listener;
- [ ] un nuovo post puo ricevere like;
- [ ] esiste un solo listener click sul contenitore del feed;
- [ ] l'identita del dato usa `data-post-id` e l'azione usa `data-action`;
- [ ] likes/liked vivono in un array di stato;
- [ ] il DOM viene renderizzato dallo stato;
- [ ] localStorage contiene JSON valido;
- [ ] storage assente/corrotto non blocca l'app;
- [ ] testo utente viene trattato come testo (`textContent`);
- [ ] nessun `fetch`/backend/async e stato introdotto.

## Debrief

Preparati a spiegare per ogni fix:

```text
sintomo -> causa -> evidenza -> modifica -> verifica
```

Un'app che "funziona" ma di cui non sai spiegare la causa del bug non completa l'obiettivo dell'Activity D.
