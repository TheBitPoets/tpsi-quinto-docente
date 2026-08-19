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
7. passare a un frontend componentizzato con il framework che verrà scelto;
8. introdurre realtime con WebSocket/Socket.IO;
9. riscrivere una parte mirata del backend con FastAPI per dimostrare che il contratto HTTP separa client e server;
10. testare e distribuire il prodotto finale.

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

## Decisioni ancora aperte

Sono deliberatamente lasciate aperte nel bootstrap:

- framework frontend principale;
- ORM Node;
- profondità TypeScript nel core;
- ampiezza esatta del mirror FastAPI;
- confine temporale col corso SQL separato.

Queste decisioni saranno congelate prima della release del curriculum, non nascoste in scelte tecniche accidentali.
