# TPSI Visual System

Questo pack rende coerenti i diagrammi del corso TPSI5. Gli oggetti non vengono ridisegnati dentro ogni immagine: le scene sorgente usano simboli condivisi e lo script `scripts/build_course_diagrams.py` produce SVG autonomi compatibili con GitHub e Marp.

## Principi

1. stesso concetto, stesso componente;
2. stesso colore, stesso significato;
3. testo sempre presente: il colore non deve essere l'unico segnale;
4. grafica vettoriale, offline e leggibile in proiezione;
5. diagrammi finali autonomi, senza riferimenti a CDN o file esterni;
6. marchi tecnologici usati solo quando identificano davvero una tecnologia;
7. nei flussi ordinari si preferiscono browser, server e database generici.

## Colori semantici

| Colore | Significato |
|---|---|
| blu | client |
| azzurro | frontend e richieste HTTP |
| verde chiaro | risposte HTTP |
| viola | WebSocket e realtime |
| turchese | API e servizi |
| verde | server e backend |
| indaco | dati e persistenza |
| rosso | sicurezza, rifiuto o errore |
| viola scuro | testing |
| ambra | runtime, configurazione e attenzione |

I valori canonici sono in `tokens.json`.

## Grammatica dei connettori

- linea continua con una freccia: chiamata o flusso;
- azzurro verso destra: HTTP request;
- verde verso sinistra: HTTP response;
- linea viola con due punte: canale realtime bidirezionale;
- linea tratteggiata: dipendenza o relazione indiretta;
- freccia circolare: ciclo, retry o recovery;
- linea rossa interrotta: operazione rifiutata.

Ogni freccia importante deve avere un'etichetta. Non affidarsi alla sola direzione o al solo colore.

## Componenti disponibili

`components.svg` contiene simboli riutilizzabili per:

- laptop, browser, smartphone e utente;
- server, rete, cloud e database;
- API, servizio, repository e route;
- documento, terminale e componente UI;
- cookie, lock, test, health e artifact;
- badge HTML, CSS, JavaScript, Node.js, Express, SQLite, Vue, React, TypeScript e Python.

La tavola `catalog/component-catalog.svg` è il riferimento visivo rapido.

## Varianti e composizione

I simboli sono intenzionalmente privi di contesto. Una scena decide dimensione, etichette e relazioni. Per esempio il laptop contiene uno slot nel quale una scena può collocare un browser, un editor o un terminale.

```text
laptop
└── browser
    └── HTML + CSS + JavaScript
```

Le scene sorgente sono in `scenes/*.scene.svg`. Usano `<use href="#tpsi-...">` e dichiarano il file finale con `data-output`. Lo script incorpora tutte le definizioni nel risultato: gli SVG pubblicati non dipendono dal pack a runtime.

## Rigenerazione

Generare catalogo e diagrammi:

```bash
python3 scripts/build_course_diagrams.py
```

Controllare che gli SVG versionati siano aggiornati senza modificarli:

```bash
python3 scripts/build_course_diagrams.py --check
```

Dopo la rigenerazione eseguire anche:

```bash
python3 scripts/build_slides.py --check-only
```

## Come aggiungere un componente

1. aggiungere un `<symbol>` a `components.svg` con ID prefissato `tpsi-`;
2. usare il `viewBox` più piccolo e stabile possibile;
3. usare i colori semantici del pack;
4. evitare testo nel simbolo, salvo i badge tecnologici;
5. aggiungere il componente alla scena catalogo;
6. rigenerare e controllare il catalogo a dimensione slide.

## Marchi e icone tecnologiche

I badge inclusi sono rappresentazioni didattiche coerenti, non copie dei loghi ufficiali. Se in futuro vengono importati marchi ufficiali, devono essere salvati localmente e accompagnati da fonte, versione, licenza e note sul marchio. Non usare URL remoti nelle slide.

## Formato delle scene

- canvas standard: `1920 × 1080`, rapporto `16:9`;
- griglia: multipli di 8 px;
- margine sicuro minimo: 56 px;
- titolo consigliato: 46 px;
- testo minimo nei diagrammi proiettati: 17 px;
- output: SVG autonomo con titolo e descrizione accessibili.

Le scene devono privilegiare una relazione principale. Se un'immagine richiede molte legende o più di due letture indipendenti, va divisa in più slide.
