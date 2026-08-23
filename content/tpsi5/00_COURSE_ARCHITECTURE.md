# Architettura didattica del corso Full Stack

## In questa unità impareremo

Questa unità introduce il percorso e rende visibile il filo logico dell'anno: una applicazione web non è una collezione di tecnologie isolate, ma una catena di componenti che collaborano attraverso contratti espliciti.

Al termine lo studente dovrà saper descrivere, a livello introduttivo, il percorso:

```text
browser
  ↓
HTML + CSS + JavaScript
  ↓
HTTP
  ↓
API / backend
  ↓
database
  ↓
autenticazione / realtime / deploy
```

## Problema iniziale

Quando premiamo «Pubblica» in un social network, dove va il testo? Chi lo riceve? Dove viene salvato? Come arriva agli altri utenti? Perché il browser può mostrare nuovi dati senza ricaricare tutta la pagina?

Il corso risponderà progressivamente a queste domande costruendo e ricostruendo lo stesso progetto: **Feisbuc**.

## Principio di progressione

1. capire la Web Platform senza framework;
2. capire JavaScript nel browser e il DOM;
3. capire HTTP prima di nasconderlo dietro librerie;
4. costruire il backend principale con Node.js + Express;
5. usare SQL direttamente prima dell'ORM;
6. introdurre autenticazione e sicurezza;
7. confrontare il rendering server-side prima della SPA;
8. passare a un frontend componentizzato con **Vue 3 + Vite**;
9. introdurre routing e TypeScript mirato ai boundary;
10. introdurre realtime con WebSocket/Socket.IO;
11. usare React in un laboratorio di traduzione/comparazione, non come secondo framework core;
12. riscrivere una parte mirata del backend con FastAPI/SQLAlchemy per rendere visibili gli stessi contratti da un altro stack;
13. testare e distribuire il prodotto finale raccogliendo evidence verificabili.

## Ambienti di laboratorio

- **MDN Playground** per micro-esempi Web Platform;
- **JSFiddle** per preservare e analizzare esempi legacy quando utile;
- **StackBlitz** opzionale per esperimenti zero-install;
- **TheBitLab** per Activity valutate e riproducibili;
- **repository Git** per Feisbuc e i progetti reali.

Nessun laboratorio valutato deve dipendere obbligatoriamente da un SaaS esterno.

## Tassonomia Activity

La tassonomia ufficiale resta quella TheBitLab:

- A — esegui/osserva;
- B — modifica controllata;
- C — implementazione autonoma;
- D — debug/diagnosi;
- E — mini-progetto;
- F — prodotto integrato.

## Decisioni congelate per il 2026/27

Il Content Pack **1.0.0 / approved** ha già chiuso le decisioni architetturali del core:

- **D1:** Vue 3 + Vite è il framework frontend principale; React resta un translation/comparison lab;
- **D2:** nessun ORM Node nel core: prima SQL raw + SQLite + repository;
- **D3:** TypeScript è usato in modo mirato ai boundary frontend, non come riscrittura totale dello stack;
- **D4:** il mirror FastAPI è mirato e serve a confrontare contratti e confini, non a duplicare Feisbuc;
- **D5:** il futuro corso SQL può integrarsi con TPSI5, ma non è un prerequisito bloccante.

Queste scelte sono parte del curriculum congelato e non vengono ridefinite durante la delivery ordinaria.

## Orientamento e primo laboratorio

Questo modulo 00 è una **lezione di orientamento** e non ha una Activity separata nel Content Pack. Il primo laboratorio operativo arriva nel modulo 01, **Web Platform e HTML moderno**, con l'Activity [Anatomia di un documento HTML moderno](../../activities/tpsi5/html_anatomy_a/student/README.md).
