# TPSI5 → TheBitLab — handoff operativo docente

Questa guida collega le Activity del corso TPSI quinto al pilot TheBitLab **senza modificare il curriculum** e senza attribuire alla piattaforma grader che non esistono ancora.

## Baseline supportata

- TPSI5: **Content Pack 1.0.0 / approved**;
- schema Activity: `1.0`;
- contratto/pilot TheBitLab pinned dal Content Pack: `5472eef86568a4e7ce59ad34ba937220df27efd7` di `TheBitPoets/2cornot2c`.

Quando si prepara la classe, usare il pin dichiarato dal Content Pack come riferimento riproducibile. Aggiornare TheBitLab a una revisione diversa è una decisione di compatibilità/delivery separata, non un cambiamento silenzioso del corso.

## Modello mentale

```text
lesson TPSI5
   ↓
Activity TPSI5 / activity.json
   ↓
validazione contratto TheBitLab
   ↓
assegnazione / scaffold predisposto dal docente
   ↓
studente: repository di consegna e/o CLI/TUI del pilot
   ↓
runner automatico, reference CI oppure rubrica/evidence
```

Lo studente **non deve eseguire direttamente `activity.json`**.

## 1. Individuare l'Activity

Usare l'[indice Activity](../activities/tpsi5/README.md) oppure il collegamento presente nel modulo.

Primo esempio del corso:

```text
activities/tpsi5/html_anatomy_a/activity.json
```

I file destinati allo studente sono dichiarati nell'array `assets` dell'Activity. `teacher_only`, solution e materiale di grading non devono essere copiati nello scaffold studente.

## 2. Validare l'Activity con il pin TheBitLab

Con una copia locale di `TheBitPoets/2cornot2c` alla revisione:

```text
5472eef86568a4e7ce59ad34ba937220df27efd7
```

eseguire dalla root di `2cornot2c`:

```bash
python scripts/validate_activity.py ../tpsi-quinto-docente/activities/tpsi5/html_anatomy_a/activity.json
```

Il comando usa `/` anche su Windows: Python lo accetta normalmente. Se la disposizione delle cartelle è diversa, sostituire i path con quelli reali senza usare placeholder fra `<` e `>`.

Output atteso:

```text
Activity validation passed.
```

## 3. Preparare uno scaffold repository studente

Il pin TheBitLab espone `scripts/assign_activity.py`, che accetta un path Activity esterno.

Negli esempi seguenti `../student-repo` rappresenta un repository studente demo. Sostituirlo con il path reale.

Prima fare sempre un dry-run:

```bash
python scripts/assign_activity.py --activity ../tpsi-quinto-docente/activities/tpsi5/html_anatomy_a/activity.json --target ../student-repo --thebitlab-ref 5472eef86568a4e7ce59ad34ba937220df27efd7 --dry-run
```

Se il piano è corretto, ripetere senza `--dry-run`:

```bash
python scripts/assign_activity.py --activity ../tpsi-quinto-docente/activities/tpsi5/html_anatomy_a/activity.json --target ../student-repo --thebitlab-ref 5472eef86568a4e7ce59ad34ba937220df27efd7
```

Le forme a riga singola sono copiabili in Bash, PowerShell e terminali equivalenti. Per più repository si può ripetere `--target` oppure usare `--targets-file` secondo la CLI del pin.

### Regola fail-safe

Non usare `--force` come default. Se una consegna esiste già, fermarsi e capire se si tratta di un tentativo studente, di uno scaffold precedente o di una reale correzione di delivery.

## 4. Quando usare la CLI/TUI studente

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

## 5. Scegliere il grading corretto

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

### Activity browser/framework/multi-file

Quando il runtime non supporta il boundary richiesto, usare reference CI, E2E, checklist o rubrica come documentato. La reference solution dimostra il contratto atteso ma non trasforma automaticamente la consegna dello studente in un test che la piattaforma non possiede.

## 6. Primo rehearsal consigliato

Prima della prima classe eseguire l'intero percorso con dati demo:

```text
README corso
→ teacher/README.md
→ modulo 00
→ modulo 01
→ html_anatomy_a
→ validate_activity.py
→ assign_activity.py --dry-run
→ scaffold demo
→ apertura starter come studente
→ checklist/rubrica
```

Se si usa anche il runtime autenticato, aggiungere un account demo docente e uno studente e verificare il flusso CLI/TUI end-to-end prima di inserire dati reali.

## 7. Se qualcosa cambia durante l'anno

Una correzione di path, setup, istruzioni, slide o troubleshooting che preserva obiettivi e contratti è delivery-safe, ma va registrata in `doc/DELIVERY_CHANGELOG.md`.

Un cambiamento a obiettivi, stack core, UDA, milestone, prerequisiti, grading contract o capability richiesta non va introdotto come semplice fix di questa guida: richiede la governance curricolare/versioning prevista dal freeze.
