# Architettura didattica del corso Full Stack

## In questa unità impareremo

Questa unità introduce il percorso e rende visibile il filo logico dell'anno: una applicazione web non è una collezione di tecnologie isolate, ma una catena di componenti che collaborano attraverso contratti espliciti.

Al termine lo studente dovrà saper:

- distinguere client e server sia come dispositivi sia come programmi;
- spiegare perché client e server hanno bisogno di un protocollo condiviso;
- distinguere il modello request/response di HTTP dal canale persistente e bidirezionale di WebSocket;
- riconoscere servizi, API, risorse e metodi HTTP in una semplice applicazione web;
- descrivere, a livello introduttivo, il percorso completo di una richiesta.

![Dal browser al servizio completo: la mappa del percorso full stack](../../assets/tpsi5/00-course-path.svg)

## Problema iniziale

Quando premiamo «Pubblica» in un social network, dove va il testo? Chi lo riceve? Dove viene salvato? Come arriva agli altri utenti? Perché il browser può mostrare nuovi dati senza ricaricare tutta la pagina?

Il corso risponderà progressivamente a queste domande costruendo e ricostruendo lo stesso progetto: **Feisbuc**.

## Client e server: due ruoli

Quando utilizziamo un'applicazione web, almeno due soggetti collaborano: un **client** e un **server**.

Queste parole non indicano soltanto due tipi di computer. Indicano soprattutto due **ruoli**:

- il client chiede un servizio o una risorsa;
- il server riceve la richiesta, la elabora e restituisce una risposta.

Possiamo osservare questi ruoli da due punti di vista.

| Punto di vista | Client | Server |
|---|---|---|
| **Hardware** | Il computer, tablet o smartphone dell'utente | Un computer fisico o virtuale, spesso ospitato in un data center o nel cloud |
| **Software** | Il programma che invia le richieste | Il programma che rimane in ascolto e risponde alle richieste |

![Client e server osservati come hardware e come software](../../assets/tpsi5/00-client-server-roles.svg)

Client e server non sono necessariamente due “scatole” diverse. Durante lo sviluppo possono anche trovarsi sullo stesso computer: quando apriamo un'applicazione su `localhost`, il browser svolge il ruolo di client e il programma Node.js svolge il ruolo di server.

## Il WWW come esempio

Nel World Wide Web il client software è normalmente il **browser**:

- Mozilla Firefox;
- Google Chrome;
- Apple Safari;
- Microsoft Edge.

Il browser richiede pagine e dati, interpreta HTML, CSS e JavaScript e mostra l'interfaccia all'utente.

Sul lato server troviamo invece un software capace di ricevere richieste web. Alcuni esempi sono:

- Apache HTTP Server;
- Nginx;
- Microsoft IIS;
- un'applicazione Node.js, spesso costruita con Express.

In questo corso il backend principale sarà realizzato con **Node.js ed Express**.

> **Attenzione:** Node.js è l'ambiente nel quale eseguiamo JavaScript sul server; Express è il framework che useremo per organizzare route, middleware e risposte HTTP.

## Il protocollo: le regole della comunicazione

Client e server devono accordarsi su come comunicare. Non è sufficiente che siano collegati alla stessa rete.

Un **protocollo** è un insieme di regole condivise che stabilisce, per esempio:

- come iniziare una comunicazione;
- come sono costruiti i messaggi;
- quale significato hanno i messaggi;
- in quale ordine possono essere inviati;
- come segnalare un risultato o un errore.

### Un protocollo nella vita quotidiana

Immaginiamo questa conversazione:

> **Marco:** «Ciao Giulia, posso chiederti una cosa?»<br>
> **Giulia:** «Sì, dimmi.»<br>
> **Marco:** «Mi passi il quaderno blu?»<br>
> **Giulia:** «Non ho capito quale quaderno. Puoi ripetere?»<br>
> **Marco:** «Quello blu sul banco vicino alla finestra.»<br>
> **Giulia:** «Ricevuto, eccolo.»<br>
> **Marco:** «Grazie, ciao.»

Anche questa semplice conversazione funziona perché Marco e Giulia seguono alcune regole condivise.

![Le cinque regole di un protocollo mappate su una conversazione tra Marco e Giulia](../../assets/tpsi5/00-conversation-protocol.svg)

| Regola del protocollo | Esempio nella conversazione |
|---|---|
| **1. Come iniziare la comunicazione** | Marco saluta e chiede se può parlare. Giulia risponde e accetta di iniziare la conversazione. |
| **2. Come sono costruiti i messaggi** | Entrambi usano frasi in italiano. La richiesta contiene un'azione, «passare», e l'oggetto interessato, «il quaderno blu». |
| **3. Quale significato hanno i messaggi** | Marco e Giulia attribuiscono lo stesso significato alle parole «quaderno», «blu» e «sul banco». |
| **4. In quale ordine vengono inviati** | Prima avviene il saluto, poi la richiesta, quindi la risposta e infine la chiusura. Giulia non consegna un quaderno prima di sapere quale deve prendere. |
| **5. Come indicare un risultato o un errore** | «Ricevuto, eccolo» indica che la richiesta è stata completata. «Non ho capito» segnala invece un errore e richiede un messaggio più preciso. |

Se uno dei due ignorasse queste regole — parlasse una lingua sconosciuta, rispondesse prima della richiesta o non segnalasse di non aver capito — la comunicazione potrebbe fallire.

Allo stesso modo, client e server devono concordare come iniziare lo scambio, come rappresentare i messaggi, che cosa significa ogni messaggio, in quale ordine scambiarli e come comunicare risultati ed errori.

La differenza è che, tra programmi, queste regole devono essere definite con grande precisione: un computer non può affidarsi all'intuizione per interpretare un messaggio ambiguo.

Nel corso incontreremo soprattutto due protocolli: **HTTP** e **WebSocket**.

### HTTP e WebSocket

| HTTP | WebSocket |
|---|---|
| Ogni scambio viene iniziato dal client | Dopo il collegamento, client e server possono inviare messaggi |
| Il client invia una richiesta e il server restituisce una risposta | La connessione rimane aperta e la comunicazione è bidirezionale |
| È adatto a pagine, API e operazioni sui dati | È adatto agli aggiornamenti in tempo reale |
| Può essere pensato, in modo semplificato, come “pull” | Permette anche il “push” dal server |

Con HTTP il browser può chiedere: «Dammi gli ultimi post» oppure «Salva questo nuovo post».

Con WebSocket il server può comunicare: «È appena arrivato un nuovo post», senza aspettare che ogni browser ripeta continuamente la stessa richiesta.

La semplificazione **HTTP = pull** e **WebSocket = push** è utile come primo modello mentale, ma non è una definizione completa:

- HTTP usa un modello request/response iniziato dal client;
- WebSocket crea un canale persistente e bidirezionale.

Nel progetto Feisbuc useremo HTTP per i comandi e il recupero dei dati, e WebSocket/Socket.IO per distribuire gli aggiornamenti in tempo reale.

## Dal servizio all'interfaccia

Un server viene realizzato per offrire uno o più **servizi** ai client.

Per esempio, il server di Feisbuc può offrire servizi per:

- recuperare i post;
- pubblicare un nuovo post;
- modificare o cancellare un post;
- autenticare un utente.

Un client non deve conoscere il codice interno con cui il server realizza queste operazioni. Deve però sapere quali servizi può richiedere, a quale indirizzo inviare la richiesta, quali dati fornire e quale risultato aspettarsi.

Il server ha quindi bisogno di un punto d'ingresso ben definito: una **interfaccia pubblica** attraverso la quale i client possono utilizzare i servizi offerti.

“Pubblica” non significa necessariamente “accessibile a tutti”: l'interfaccia può richiedere autenticazione e autorizzazione. Significa che quella è la parte del server esposta ai client, mentre l'implementazione interna rimane nascosta.

### Che cos'è un'API?

API significa **Application Programming Interface**, cioè **interfaccia di programmazione di un'applicazione**.

Un'API è un insieme di regole che permette a un programma di utilizzare le funzionalità offerte da un altro programma.

```text
CLIENT
“Voglio recuperare i post”
        │
        ▼
API DEL SERVER
“Puoi farlo in questo modo”
        │
        ▼
SERVIZIO
recupera i dati e produce il risultato
```

Possiamo immaginare l'API come la reception di un albergo: il cliente esprime una richiesta alla reception, il lavoro viene svolto dalle parti interne dell'albergo e il cliente riceve il risultato senza dover conoscere l'organizzazione interna.

Allo stesso modo, il client comunica con l'API senza conoscere direttamente il codice del backend, le tabelle del database o le istruzioni SQL.

> L'API descrive **come entrare** nel sistema. Il servizio descrive **che cosa il sistema sa fare**.

### Che cos'è un web service?

Un **web service** è un servizio software accessibile attraverso una rete utilizzando tecnologie e protocolli del Web.

Per esempio, Feisbuc può offrire un servizio per pubblicare un post. Il servizio viene eseguito sul server e può essere utilizzato da client differenti:

- un'applicazione eseguita nel browser;
- un'applicazione per smartphone;
- un altro server;
- uno strumento di test.

```text
Browser ───────┐
App mobile ────┼──► Web API ──► servizio sul server
Altro server ──┘
```

I client possono essere diversi, ma utilizzano tutti la stessa interfaccia esposta dal server. In questo corso i web service saranno esposti principalmente tramite una **Web API basata su HTTP**.

### API e Web API

Non tutte le API utilizzano Internet. Anche una libreria JavaScript possiede una API: funzioni, classi e metodi che possiamo utilizzare nel nostro programma.

Quando l'API è esposta da un server attraverso il Web, parliamo di **Web API**.

```text
API
├── API di una libreria
├── API del browser
├── API del sistema operativo
└── Web API esposta da un server
```

Nel nostro progetto:

```text
frontend nel browser
        │ richiesta HTTP
        ▼
Web API di Feisbuc
        │
        ▼
servizi del backend
        │
        ▼
database
```

## Che cos'è una REST API?

Una **REST API** è una Web API organizzata seguendo lo stile architetturale REST. Il suo modello fondamentale è basato sulle **risorse**.

Una risorsa è qualcosa che il sistema gestisce e che possiamo identificare. In Feisbuc avremo, per esempio, post, utenti, commenti e sessioni.

Ogni risorsa accessibile attraverso l'API possiede un identificatore rappresentato da un URL.

```text
/api/posts       → collezione dei post
/api/posts/42    → post identificato dal numero 42
/api/users/7     → utente identificato dal numero 7
```

`/api/posts/42` è l'URL utilizzato dal client per identificare la risorsa. Nel backend potremmo definire una route parametrica:

```text
/api/posts/:id
```

La route dice al server: «Riconosci tutti gli URL con questa struttura e conserva il valore finale nel parametro `id`».

```text
URL richiesto:       /api/posts/42
Route del backend:   /api/posts/:id
Parametro ottenuto:  id = 42
```

Quindi:

- l'**URL** identifica la risorsa per il client;
- la **route** è la regola usata dal backend per riconoscere quell'URL;
- l'**ID** distingue una singola risorsa dalle altre.

### Risorse e metodi HTTP

L'URL indica **su quale risorsa** vogliamo operare. Il metodo HTTP indica **quale azione** vogliamo compiere.

| Metodo HTTP | Significato introduttivo | Esempio |
|---|---|---|
| `GET` | Recuperare una o più risorse | Leggere i post |
| `POST` | Creare una nuova risorsa | Pubblicare un post |
| `PUT` | Sostituire completamente una risorsa | Sostituire un post |
| `PATCH` | Modificare una parte della risorsa | Modificare il testo |
| `DELETE` | Cancellare una risorsa | Eliminare un post |

La combinazione tra metodo e URL esprime l'operazione richiesta:

```http
GET /api/posts
GET /api/posts/42
POST /api/posts
PATCH /api/posts/42
DELETE /api/posts/42
```

La risorsa può rimanere la stessa mentre cambia l'azione espressa dal metodo HTTP.

In questa prima lezione ci basta ricordare:

1. il server offre dei servizi;
2. l'API è l'interfaccia attraverso cui i client possono richiederli;
3. una Web API è raggiungibile attraverso tecnologie Web;
4. una REST API organizza il sistema intorno alle risorse;
5. l'URL identifica la risorsa;
6. il metodo HTTP indica l'azione richiesta.

Nel modulo dedicato a HTTP analizzeremo con maggiore precisione request, response, header, body, status code, semantica dei metodi e progettazione REST.

## Anatomia di un'applicazione web full stack

![Architettura completa di una applicazione web full stack](../../assets/tpsi5/00-full-stack-architecture.svg)

Una web application full stack comprende più parti con responsabilità diverse.

Il **frontend** viene eseguito nel browser e gestisce ciò che l'utente vede e con cui interagisce. Le sue tecnologie fondamentali sono:

- HTML per struttura e contenuto;
- CSS per presentazione e layout;
- JavaScript per comportamento e interazione.

Il **backend** viene eseguito sul server. Riceve le richieste, applica le regole dell'applicazione e decide quali dati leggere o modificare. Nel nostro stack useremo principalmente Node.js ed Express.

Il **database** conserva i dati anche dopo la chiusura del browser o il riavvio dell'applicazione. Lo interrogheremo usando SQL; il database principale del corso sarà SQLite.

Il browser non dovrebbe collegarsi direttamente al database. Comunica con il backend, che controlla e protegge l'accesso ai dati.

## Esempio completo: pubblicare un post

Quando un utente preme «Pubblica» in Feisbuc:

1. JavaScript intercetta l'azione nel browser;
2. il frontend prepara i dati del post;
3. il browser invia una richiesta HTTP `POST /api/posts`;
4. la REST API riceve il documento JSON;
5. Express controlla la richiesta e valida i dati;
6. il backend esegue un'istruzione SQL;
7. SQLite conserva il nuovo post;
8. il server restituisce una risposta HTTP in JSON;
9. il frontend aggiorna ciò che l'utente vede;
10. in modalità realtime, il server può notificare gli altri browser attraverso WebSocket/Socket.IO.

Questa catena è il filo conduttore dell'intero corso. Durante l'anno studieremo ogni passaggio separatamente, poi li collegheremo in un'unica applicazione.

### Checkpoint

Per cancellare il post numero 12:

1. qual è la risorsa?
2. qual è il suo URL?
3. quale metodo HTTP useresti?
4. quale parte rappresenta l'API e quale il servizio interno?

La richiesta attesa è:

```http
DELETE /api/posts/12
```

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
