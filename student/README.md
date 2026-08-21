# TPSI quinto — Student Guide

Corso: **Full Stack Web Developer 2026/27**.

Questa guida spiega **come lavorare** durante il corso. I contenuti teorici sono nei moduli `content/tpsi5/`; gli esercizi e i progetti sono in `activities/tpsi5/` e, quando previsto, in TheBitLab.

## Il ciclo di lavoro

Usa sempre questo processo:

```text
leggi -> esegui -> osserva -> modifica -> testa -> fai debug -> consegna -> correggi
```

Non saltare direttamente alla soluzione finale: il corso serve a capire **perché** il sistema funziona e quale componente è responsabile di ogni comportamento.

## Prima di iniziare

Per ogni modulo:

1. apri la lezione dal README del repository;
2. controlla prerequisiti e obiettivi;
3. segui le slide durante la spiegazione;
4. prova gli esempi in locale;
5. apri l'Activity indicata;
6. esegui test/check disponibili;
7. conserva l'evidenza richiesta.

## Strumenti base

Durante l'anno useremo progressivamente:

- browser e DevTools;
- editor/IDE;
- terminale;
- Node.js/npm;
- SQLite;
- Vue/Vite;
- TypeScript nei boundary previsti;
- Socket.IO;
- Python + ambiente virtuale nella parte FastAPI;
- pytest;
- TheBitLab quando l'Activity è supportata dalla piattaforma.

Le versioni e i comandi esatti sono quelli dichiarati dai moduli/reference del repository.

## Regola importante: prima capire il confine

Quando qualcosa non funziona, chiediti nell'ordine:

1. il browser ha caricato la risorsa?
2. il JavaScript sta ricevendo i dati giusti?
3. la request HTTP è corretta?
4. il backend ha ricevuto/validato la request?
5. il database contiene i dati attesi?
6. auth/sessione permettono l'operazione?
7. il frontend sta renderizzando lo stato corretto?
8. nel realtime serve un nuovo evento o un resync REST?
9. il problema è di configurazione/runtime invece che di codice?

Questa checklist vale più del “provare modifiche a caso”.

## Node.js / npm

Quando entri in una directory Node:

```bash
npm install
```

Poi usa gli script dichiarati nel relativo `package.json`, ad esempio:

```bash
npm run dev
npm test
npm run build
```

Non assumere che tutti i progetti abbiano gli stessi script: controlla sempre `package.json`.

## Python / virtual environment

Nella parte FastAPI/SQLAlchemy/testing usa un ambiente virtuale dedicato quando lavori fuori dall'ambiente già preparato dal laboratorio.

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installa poi le dipendenze indicate dal progetto/reference. Per uscire:

```bash
deactivate
```

## Debug minimo

Prima di chiedere “non funziona”, raccogli almeno:

- comando eseguito;
- messaggio di errore completo;
- file/linea coinvolti;
- request/response HTTP se il problema è di rete;
- stato del database se il problema è di persistenza;
- test fallito e relativo output se esiste.

## TheBitLab

Alcune attività hanno runner automatici, altre restano rubric/manuali. Se l'Activity non ha un grader automatico, segui la procedura di evidenza/consegna indicata dal docente: non significa che l'attività sia meno importante.

## Feisbuc

Feisbuc cresce durante tutto il corso. Non è un progetto nuovo a ogni UDA: è lo stesso sistema che cambia quando impariamo un nuovo confine.

Quando completi una milestone dovresti saper dire:

- cosa hai aggiunto;
- quale responsabilità vive nel browser;
- quale vive nel backend;
- quale dato è persistente;
- quale contratto HTTP/evento collega i componenti;
- come hai verificato che funzioni.

## Se resti bloccato

Procedi in questo ordine:

1. rileggi l'errore;
2. riproducilo con il caso più piccolo possibile;
3. controlla la lesson e la slide del boundary interessato;
4. usa DevTools/log/test;
5. confronta input e output attesi;
6. solo dopo confronta con un esempio/reference fornito dal docente.

## Consegna

Una consegna valida non è soltanto “il codice”. Quando richiesto deve includere l'evidenza prevista dall'Activity: test, output, screenshot non sensibili, risposta HTTP, file generato o altra prova definita dal laboratorio.

## Aggiornamenti durante l'anno

Le spiegazioni, slide e procedure possono essere corrette/migliorate durante l'anno senza cambiare gli obiettivi del curriculum. Se una procedura cambia, usa sempre la versione più recente nel repository e controlla eventuali note del docente.