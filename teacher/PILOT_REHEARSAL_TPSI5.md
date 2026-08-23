# TPSI5 — rehearsal TheBitLab prima della prima classe

Questo playbook riduce il runbook generale del pilot TheBitLab al primo percorso reale del corso **TPSI quinto 2026/27**. Serve a decidere se la delivery è pronta con dati demo prima di coinvolgere studenti reali.

Non modifica il curriculum: la baseline resta **Content Pack 1.0.0 / approved**. Non aggiunge grader o capability alla piattaforma.

## Baseline da congelare nella prova

Registrare prima di iniziare:

- SHA di `TheBitPoets/tpsi-quinto-docente` candidato alla lezione;
- esito `Quality` e `Slides` dello stesso SHA;
- Content Pack `1.0.0 / approved`;
- checkout `TheBitPoets/2cornot2c` esattamente a `5472eef86568a4e7ce59ad34ba937220df27efd7`;
- Python 3.11–3.13;
- Docker disponibile se si vuole arrivare a `GO pilot`;
- topologia dichiarata: **una sola data root autorevole** per server, TUI, runner, tentativi e dashboard;
- account e dati esclusivamente demo.

Se lo SHA, il pin o la topologia cambiano, il rehearsal non descrive più la release che verrà usata in classe.

## Esiti ammessi

- **GO tecnico demo** — repository, contenuto, packaging e flusso demo funzionano; non autorizza dati reali.
- **GO pilot** — tutti i gate obbligatori del runbook TheBitLab sono superati sul deployment reale, compresi auth/authz, Docker, backup/restore, revoca, governance e decisione finale.
- **NO-GO** — almeno un gate obbligatorio è fallito, bloccato o privo di evidenza.

La CI del repository può supportare il primo esito, ma **non può da sola produrre `GO pilot`**.

## Contenuto scelto per il primo smoke

Il modulo 00 è orientamento. Il primo laboratorio operativo è:

```text
modulo 01 — Web Platform e HTML moderno
Activity: tpsi5-activity-a-html-anatomy-001
bundle: activities/tpsi5/html_anatomy_a/
```

Percorso studente previsto:

```text
README corso
→ student/README.md
→ content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md
→ activities/tpsi5/html_anatomy_a/student/README.md
→ starter/index.html
```

Per questa Activity la fonte di verità dichiara:

```text
compila=false
test=false
sandbox=false
ai_feedback=false
```

Quindi il laboratorio si valuta con browser, editor, DevTools, checklist e rubrica docente. **Non simulare autograding HTML/DOM.**

## Evidenze

Conservare le evidenze sensibili fuori dal repository, in una directory protetta. Nell'issue o nella PR pubblicare solo esiti sanitizzati.

Struttura consigliata:

```text
tpsi5-first-class-YYYYMMDD-NN/
  00-run-record.md
  01-release-and-ci.txt
  02-content-and-activity.txt
  03-adapter-capability.json
  04-assignment-dry-run.json
  05-scaffold-check.txt
  06-demo-root-check.json
  07-student-flow.md
  08-teacher-flow.md
  09-authz-revocation.md
  10-docker-attempt.md
  11-backup-restore.md
  12-go-no-go.md
```

Non salvare o condividere cookie, bearer, token dashboard, proof di pairing, codici OAuth, state/nonce, client secret, private key, HAR o dump del database.

## Gate 1 — release e repository

Dai due checkout puliti verificare:

```bash
git -C tpsi-quinto-docente rev-parse HEAD
git -C tpsi-quinto-docente status --porcelain=v1
git -C 2cornot2c rev-parse HEAD
```

PASS se:

- TPSI5 è sullo SHA candidato e il worktree è pulito;
- Quality e Slides dello stesso SHA sono verdi;
- 2cornot2c è esattamente sul pin `5472eef...`.

Un checkout diverso dal pin non può essere usato per dichiarare superata questa prova.

## Gate 2 — Activity e capability di delivery

Dalla root di `2cornot2c`:

```bash
python scripts/validate_activity.py ../tpsi-quinto-docente/activities/tpsi5/html_anatomy_a/activity.json
```

Output atteso:

```text
Activity validation passed.
```

Dalla root di TPSI5:

```bash
python scripts/tpsi5_thebitlab_assign.py \
  --activity activities/tpsi5/html_anatomy_a/activity.json \
  --platform ../2cornot2c \
  --capability-only
```

PASS se restituisce `supported: true`.

Per Activity future, exit code `2` con una motivazione di capability è un **fallback esplicito**, non un invito a forzare lo scaffold. TypeScript e asset-directory non supportati dal pin restano su repository/reference CI/checklist/rubrica secondo il corso.

## Gate 3 — dry-run assegnazione

Preparare un repository studente demo vuoto e lanciare:

```bash
python scripts/tpsi5_thebitlab_assign.py \
  --activity activities/tpsi5/html_anatomy_a/activity.json \
  --platform ../2cornot2c \
  --target ../student-demo \
  --dry-run
```

PASS se il piano mostra almeno:

- starter `index.html` visibile allo studente;
- guida TPSI5 consegnata come `GUIDA.md`;
- `README.md` riservato allo scaffold TheBitLab;
- nessun asset `teacher_only`, solution o hidden grading nel piano studente;
- `canonical_activity_unchanged: true`;
- pin TheBitLab corretto.

Non usare `--force` come default.

## Gate 4 — scaffold reale demo

Ripetere senza `--dry-run` e controllare il repository demo.

Lo scaffold del primo lab deve contenere il materiale studente previsto, in particolare:

```text
README.md      # generato dalla piattaforma
GUIDA.md       # guida TPSI5
index.html     # starter
```

Deve essere assente qualunque soluzione o nota docente.

Aprire `GUIDA.md`, poi `index.html` nel browser e verificare che le istruzioni siano comprensibili senza consultare directory riservate.

## Gate 5 — prova didattica del primo laboratorio

Eseguire il lab come studente demo, senza guardare la solution:

1. aprire `index.html` nel browser;
2. aprire DevTools;
3. aggiungere doctype, `lang="it"`, charset e viewport;
4. sostituire il contenitore dell'intestazione con `header`;
5. verificare che resti un solo `h1`;
6. completare la checklist in `GUIDA.md`;
7. spiegare a voce la differenza tra `head` e `header` e tra sorgente e DOM.

Il docente applica i `manual_checks` e la rubrica dell'Activity canonica. PASS se il flusso è eseguibile senza ambiguità e senza capability inventate.

## Gate 6 — root demo autorevole

Per il pilot vero seguire il runbook `doc/PILOT_REHEARSAL.md` del pin e creare una **sola data root demo**. Server, TUI, runner, tentativi e dashboard devono leggere la stessa root.

Una topologia con esecuzione su host studente separati e report locali non sincronizzati è NO-GO per il pilot del pin.

PASS solo se il bootstrap/validation della root demo del runbook restituisce gli esiti attesi e non esistono istanze concorrenti sulla stessa root.

## Gate 7 — account demo, auth e TUI

Sul deployment reale:

- usare un account docente demo e uno studente demo;
- verificare ruolo, classe e membership;
- eseguire pairing/browser auth secondo il pin;
- aprire dalla CLI/TUI soltanto le consegne consentite allo studente demo;
- verificare logout/revoca;
- provare almeno un caso negativo cross-student/cross-class previsto dal runbook.

PASS se l'identità della TUI deriva dal bearer/pairing e non da parametri fidati forniti dal client.

Non consegnare agli studenti la dashboard locale docente/demo come interfaccia self-service.

## Gate 8 — runner Docker e tentativi

Il primo lab HTML non richiede runner automatico, ma `GO pilot` richiede comunque il gate Docker della piattaforma perché il pilot lo userà nelle Activity supportate.

Seguire lo scenario Docker del runbook pinned e verificare:

- immagine immutabile letta dal toolchain lock;
- container senza rete e senza segreti;
- un tentativo positivo e uno negativo osservabili;
- storico coerente;
- errore fail-closed se Docker non è disponibile.

Questo gate prova la piattaforma, non trasforma il primo lab HTML in un esercizio autograded.

## Gate 9 — tentativo definitivo e registro docente

Su una Activity runner-backed demo del runbook:

1. produrre almeno due tentativi;
2. selezionare esplicitamente il definitivo dalla TUI;
3. rileggere lo storico e verificare che il marker `final` persista;
4. rigenerare il registro docente;
5. verificare che `attempt_id`, esito e conteggio test coincidano tra TUI, report persistito, registro e dashboard.

Qualunque divergenza è NO-GO.

Per `html_anatomy_a` la valutazione rimane invece rubric/manuale; non creare un falso report automatico solo per uniformare il flusso.

## Gate 10 — backup, restore, incident e shutdown

Sul deployment candidato eseguire i gate del runbook generale:

- backup coerente della data root e dei dati necessari;
- restore in directory isolata;
- verifica che segreti esterni non finiscano nel backup applicativo non cifrato;
- prova revoca/incident minima;
- shutdown pulito e assenza di processi/lock residui.

PASS solo con evidenza ripetibile sullo stesso candidato che verrà usato nel pilot.

## Gate 11 — governance prima dei dati reali

`GO tecnico demo` non richiede dati reali. `GO pilot` sì.

Prima di inserire studenti reali devono essere approvati i punti di governance richiesti dal pin: base giuridica/informativa, ruoli, finalità, categorie di dati, retention, accessi, backup, incident response, provider e uso AI.

Se questa parte non è chiusa, l'esito massimo è **GO tecnico demo**.

## Matrice finale

| Gate | CI/repo può coprirlo? | Richiede host/deployment reale? | Obbligatorio per GO pilot |
|---|---|---|---|
| Release SHA + CI | sì | no | sì |
| Activity schema + adapter | sì | no | sì |
| Dry-run/scaffold first lab | sì | no | sì |
| Prova didattica HTML | parzialmente | sì, almeno prova manuale | sì per la prima lezione |
| Root autorevole | no | sì | sì |
| Auth/authz/pairing/TUI | no | sì | sì |
| Docker runner | CI solo parziale | sì | sì |
| Final attempt ↔ registro | no | sì | sì |
| Backup/restore | no | sì | sì |
| Revoca/incident/shutdown | no | sì | sì |
| Governance dati reali | no | organizzativa | sì |

## Record decisionale

Compilare `12-go-no-go.md` con:

```text
Rehearsal ID:
TPSI5 SHA:
TheBitLab SHA: 5472eef86568a4e7ce59ad34ba937220df27efd7
Topologia:
Activity first-class: tpsi5-activity-a-html-anatomy-001
Account usati: alias demo only
Gate PASS:
Gate FAIL/BLOCKED:
Finding aperti:
Rischi residui non bloccanti:
Decisione: GO tecnico demo | GO pilot | NO-GO
Decision owner:
Data/ora/timezone:
```

Non dichiarare `GO pilot` se un gate obbligatorio è `BLOCKED`, se l'evidenza appartiene a una release diversa o se la governance necessaria ai dati reali non è stata approvata.

## Dopo il rehearsal

- findings di setup/troubleshooting che preservano il curriculum → `doc/DELIVERY_CHANGELOG.md`;
- incompatibilità di packaging TPSI5/TheBitLab → fix nell'adapter con smoke cross-repo;
- nuove capability di piattaforma → issue/PR in `TheBitPoets/2cornot2c`, non workaround silenziosi nel corso;
- cambi a obiettivi, milestone, stack o grading contract → governance curricolare/versioning, non delivery patch.
