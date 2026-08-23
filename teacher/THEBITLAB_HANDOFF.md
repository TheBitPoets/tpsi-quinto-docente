# TPSI5 → TheBitLab — handoff operativo docente

Questa guida collega le Activity del corso TPSI quinto al pilot TheBitLab **senza modificare il curriculum canonico** e senza attribuire alla piattaforma capability che non esistono ancora.

## Baseline supportata

- TPSI5: **Content Pack 1.0.0 / approved**;
- schema Activity: `1.0`;
- contratto/pilot TheBitLab pinned dal Content Pack: `5472eef86568a4e7ce59ad34ba937220df27efd7` di `TheBitPoets/2cornot2c`;
- adapter di delivery TPSI5: [`../scripts/tpsi5_thebitlab_assign.py`](../scripts/tpsi5_thebitlab_assign.py).

Quando si prepara la classe, usare il pin dichiarato dal Content Pack come riferimento riproducibile. Aggiornare TheBitLab a una revisione diversa è una decisione di compatibilità/delivery separata, non un cambiamento silenzioso del corso.

## Modello mentale

```text
lesson TPSI5
   ↓
Activity TPSI5 / activity.json                 ← fonte canonica, immutata
   ↓
validation Activity 1.0
   ↓
adapter TPSI5 di delivery
   ├── capability supportata → bundle effimero compatibile → scaffold TheBitLab
   └── capability non presente → fallback repo/manuale/reference CI
   ↓
studente: repository di consegna e/o CLI/TUI del pilot
```

Lo studente **non deve eseguire direttamente `activity.json`**.

## Perché esiste l'adapter

Il dry-run reale ha verificato un confine che la sola validazione schema non vede:

- TheBitLab genera e possiede `README.md` nello scaffold studente;
- le Activity TPSI5 usano spesso `student/README.md` come guida didattica;
- il pin non supporta ancora lo scaffold TypeScript;
- gli asset dichiarati come intere directory non sono copiabili dal generatore pinned.

L'adapter risolve **solo il packaging di delivery**: quando una guida studente avrebbe come target `README.md`, crea un bundle temporaneo che la espone come `GUIDA.md`. Il file `activity.json` canonico nel corso non viene riscritto.

TypeScript e asset-directory non vengono invece mascherati: l'adapter li segnala come capability non disponibile e richiede il fallback documentato.

## 1. Individuare l'Activity

Usare l'[indice Activity](../activities/tpsi5/README.md) oppure il collegamento presente nel modulo.

Primo esempio del corso:

```text
activities/tpsi5/html_anatomy_a/activity.json
```

I file destinati allo studente sono dichiarati nell'array `assets` dell'Activity. `teacher_only`, solution e materiale di grading non devono comparire nello scaffold studente.

## 2. Preparare il checkout TheBitLab pinned

Usare una copia locale di `TheBitPoets/2cornot2c` esattamente alla revisione:

```text
5472eef86568a4e7ce59ad34ba937220df27efd7
```

Negli esempi seguenti si assume questa disposizione:

```text
workspace/
├── 2cornot2c/
└── tpsi-quinto-docente/
```

## 3. Validare il contratto Activity

Dalla root di `2cornot2c`:

```bash
python scripts/validate_activity.py ../tpsi-quinto-docente/activities/tpsi5/html_anatomy_a/activity.json
```

Output atteso:

```text
Activity validation passed.
```

La validazione del JSON e la scaffoldability sono due controlli diversi: una Activity può rispettare lo schema ma richiedere una capability di delivery non presente nel pin.

## 4. Verificare la capability di delivery

Dalla root di `tpsi-quinto-docente`:

```bash
python scripts/tpsi5_thebitlab_assign.py --activity activities/tpsi5/html_anatomy_a/activity.json --platform ../2cornot2c --capability-only
```

Per una Activity scaffoldabile restituisce `supported: true`.

Se restituisce exit code `2` e una motivazione come:

```text
typescript-runner/scaffold-not-supported-by-pinned-thebitlab
```

oppure:

```text
directory-asset-not-supported-by-pinned-thebitlab
```

non forzare `assign_activity.py`: usare il fallback repository/manuale/reference previsto dal modulo e dalla matrice di grading.

## 5. Preparare lo scaffold studente

Negli esempi `../student-repo` rappresenta un repository studente demo.

Prima eseguire sempre un dry-run:

```bash
python scripts/tpsi5_thebitlab_assign.py --activity activities/tpsi5/html_anatomy_a/activity.json --platform ../2cornot2c --target ../student-repo --dry-run
```

Per la prima Activity il piano deve mostrare che:

- `index.html` arriva dallo starter;
- `README.md` resta il README generato da TheBitLab;
- la guida didattica TPSI5 viene consegnata come `GUIDA.md`;
- solution e note docente non fanno parte degli asset studente;
- `canonical_activity_unchanged` è `true`.

Se il piano è corretto, ripetere senza `--dry-run`:

```bash
python scripts/tpsi5_thebitlab_assign.py --activity activities/tpsi5/html_anatomy_a/activity.json --platform ../2cornot2c --target ../student-repo
```

Per più repository si può ripetere `--target` oppure usare `--targets-file`.

### Regola fail-safe

Non usare `--force` come default. Se una consegna esiste già, fermarsi e capire se si tratta di un tentativo studente, di uno scaffold precedente o di una reale correzione di delivery.

## 6. Quando usare la CLI/TUI studente

Nel pilot 2026/27 la CLI/TUI autenticata è il canale self-service studente. Il docente deve prima avere predisposto classe, membership e assegnazioni nel runtime TheBitLab secondo la guida MVP del pin.

Il flusso lato studente è concettualmente:

1. autenticazione/pairing previsto dall'installazione;
2. elenco consegne;
3. apertura del dettaglio;
4. lettura della policy di aiuto;
5. esecuzione del runner quando disponibile;
6. consultazione di test/tentativi;
7. selezione del tentativo definitivo quando prevista.

Non consegnare agli studenti la dashboard web locale docente/demo come se fosse la loro interfaccia federata.

## 7. Scegliere il grading corretto

La fonte di verità è `correzione` nell'`activity.json` e la matrice di grading del corso.

### Primo lab HTML

`tpsi5-activity-a-html-anatomy-001` dichiara:

```text
compila=false
test=false
sandbox=false
ai_feedback=false
```

Quindi la procedura corretta è:

- browser + editor + DevTools;
- checklist studente;
- manual checks;
- rubrica docente;
- eventuale tracciamento/assegnazione TheBitLab;
- **nessun autograding HTML simulato**.

### Activity automatiche

Quando l'Activity dichiara un runner supportato dal pin, usare il runner deterministico e conservare il report previsto.

### TypeScript, browser/framework e asset-directory

Quando il pin non supporta il boundary di delivery richiesto, usare repository Git, reference CI, E2E, checklist o rubrica come documentato. La reference solution dimostra il contratto atteso ma non trasforma automaticamente la consegna dello studente in un runner che la piattaforma non possiede.

## 8. Primo rehearsal consigliato

Prima della prima classe eseguire l'intero percorso con dati demo:

```text
README corso
→ teacher/README.md
→ modulo 00
→ modulo 01
→ html_anatomy_a
→ validate_activity.py
→ adapter --capability-only
→ adapter --dry-run
→ scaffold demo
→ verifica README.md + GUIDA.md + index.html
→ checklist/rubrica
```

La CI del corso ripete inoltre questo contratto su Linux e Windows contro il **pin reale**, così una futura incompatibilità di packaging non resta nascosta dietro la sola validazione JSON.

Se si usa anche il runtime autenticato, aggiungere un account demo docente e uno studente e verificare il flusso CLI/TUI end-to-end prima di inserire dati reali.

## 9. Se qualcosa cambia durante l'anno

Una correzione di path, setup, istruzioni, slide o troubleshooting che preserva obiettivi e contratti è delivery-safe, ma va registrata in `doc/DELIVERY_CHANGELOG.md`.

Un cambiamento a obiettivi, stack core, UDA, milestone, prerequisiti o grading contract non va introdotto come semplice fix di questa guida: richiede la governance curricolare/versioning prevista dal freeze.
