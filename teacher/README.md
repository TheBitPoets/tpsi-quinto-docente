# TPSI quinto — Teacher Guide

Curriculum: **Content Pack 1.0.0 / approved**  
Delivery layer: evolving during a.s. 2026/27.

Questa guida raccoglie ciò che serve per **insegnare** il corso senza modificare il curriculum congelato. Le correzioni in-year vanno registrate in `doc/DELIVERY_CHANGELOG.md`.

## Workflow docente per ogni modulo

1. Apri il modulo dal README principale.
2. Ripassa prerequisiti, obiettivi e collegamento al progetto Feisbuc.
3. Usa le slide come narrazione della lezione, non come sostituto della dispensa.
4. Esegui la demo prevista o un esempio minimo equivalente.
5. Inserisci almeno un checkpoint orale/rapido prima del laboratorio.
6. Avvia le Activity collegate dall'[indice Activity](../activities/tpsi5/README.md).
7. Usa reference solution e Quality per verificare contratti e comportamento.
8. Registra eventuali chiarimenti/correzioni emersi in aula nel delivery changelog.

Il **modulo 00** è orientamento e non ha una Activity dedicata. Il primo handoff operativo è il modulo 01 → [`html_anatomy_a`](../activities/tpsi5/html_anatomy_a/student/README.md).

## Struttura consigliata di una lezione

- 5–10 min: richiamo e domanda di attivazione;
- 15–25 min: modello mentale / concetto nuovo;
- 15–25 min: esempio progressivo o live coding;
- 5 min: checkpoint;
- laboratorio guidato/autonomo;
- recap finale e anticipazione del passo successivo.

I tempi sono indicativi: il Course Design resta la fonte della distribuzione complessiva delle 33 settimane.

## Cosa può cambiare durante l'anno senza rompere il freeze

Sono normalmente patch-safe:

- correzioni di testo;
- spiegazioni più chiare;
- nuovi diagrammi;
- esempi equivalenti aggiuntivi;
- miglioramento delle slide;
- correzioni setup/comandi;
- troubleshooting;
- lab-fix che preservano gli stessi obiettivi e contratti.

Richiedono invece review curricolare esplicita: nuovi argomenti obbligatori, nuovi prerequisiti, cambio di framework/tool obbligatorio, modifica degli obiettivi o delle competenze valutate, rimozione/aggiunta sostanziale di milestone.

## Feisbuc come filo conduttore

Durante la spiegazione conviene rendere sempre esplicita la domanda: **“cosa cambia in Feisbuc e quale confine stiamo introducendo?”**

La progressione deve restare visibile:

`pagina -> UI dinamica -> client REST -> API Express -> SQLite -> identità/sessione -> SSR comparison -> SPA Vue -> routing -> typing boundary -> realtime -> mirror Python -> deploy/evidence`

## Demo e debugging

Ogni demo dovrebbe includere almeno uno di questi momenti:

- osservazione con DevTools;
- modifica controllata;
- errore intenzionale;
- diagnosi del boundary;
- verifica con test o output osservabile.

L'obiettivo non è mostrare solo codice corretto, ma insegnare **come capire dove si è rotto il sistema**.

## Soluzioni e reference

Le reference solution sono in `activities/tpsi5/` nelle directory previste dai singoli moduli. Non vanno presentate come unica soluzione possibile: servono come baseline verificata, regressione e supporto docente.

## TheBitLab

Il curriculum resta compatibile con il pilot TheBitLab pinned definito dal Content Pack. Dove il runner/grader non esiste ancora, usare il fallback manuale/rubric-based documentato dal modulo/Activity; non presentarlo agli studenti come grading automatico.

Per il percorso concreto **Activity TPSI5 → validazione → assegnazione/scaffold → canale studente**, usare la guida [TPSI5 → TheBitLab — handoff operativo docente](THEBITLAB_HANDOFF.md). La guida resta pinnata alla revisione TheBitLab dichiarata dal Content Pack e distingue esplicitamente runner automatici da checklist, reference CI ed evidence manuale.

## Checklist prima di una lezione

- slide del modulo aperte;
- lesson canonica aperta;
- demo verificata;
- Activity/starter verificati;
- eventuali credenziali/tool esterni pronti;
- output atteso chiaro;
- tipo di grading realmente disponibile verificato;
- piano B se TheBitLab o rete non sono disponibili.

## Prima della prima classe

Eseguire almeno una volta il rehearsal completo con dati demo:

```text
README → teacher guide → modulo 00 → modulo 01
→ prima Activity → starter → grading/rubrica
```

Se TheBitLab viene usato nel pilot, aggiungere validazione Activity, dry-run dell'assegnazione e prova del canale studente secondo `THEBITLAB_HANDOFF.md`.

## Durante l'anno

Quando emerge una spiegazione migliore, un errore o un problema operativo:

1. correggere la **fonte canonica**;
2. aggiornare slide/guide se necessario;
3. registrare la modifica in `doc/DELIVERY_CHANGELOG.md`;
4. rigenerare eventuali artifact derivati;
5. indicare se il materiale già distribuito agli studenti è superato.
