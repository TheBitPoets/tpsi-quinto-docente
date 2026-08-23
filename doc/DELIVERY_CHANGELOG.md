# TPSI quinto — Delivery Change Log 2026/27

Curriculum release: **Content Pack 1.0.0 / approved**  
Curriculum freeze: `doc/CURRICULUM_FREEZE_2026_2027.md`.

Questo changelog registra modifiche al materiale di delivery durante l'anno scolastico senza confonderle con modifiche del curriculum.

| Data | Modulo/materiale | Tipo | Modifica | Motivo | Materiale già distribuito superato? |
|---|---|---|---|---|---|
| 2026-08-21 | delivery layer | `setup` | Aggiunte guide docente/studente e policy di manutenzione in-year. | Preparare il corso all'uso reale in aula mantenendo il curriculum 1.0.0 congelato. | no |
| 2026-08-23 | modulo 00 + slide 00 | `errata` / `clarification` | Rimossi i riferimenti bootstrap a decisioni ancora aperte; esplicitate D1–D5 già congelate e il fatto che il modulo 00 non ha Activity dedicata. | Il dry-run docente/studente mostrava una contraddizione tra lesson iniziale e Content Pack 1.0.0 / freeze. | no |
| 2026-08-23 | modulo 01 + slide 01 + indice Activity | `clarification` | Allineato lo stato della lesson a `Content Pack 1.0.0 / approved`; aggiunti link diretti alle prime Activity, allo starter e un indice navigabile UDA21–23. | Rendere il primo handoff al laboratorio raggiungibile senza ricerca manuale nel repository. | no |
| 2026-08-23 | guide docente/studente + `teacher/THEBITLAB_HANDOFF.md` | `setup` | Documentato il percorso TPSI5 → validazione Activity → assegnazione/scaffold → canale studente sul pin TheBitLab; chiariti i boundary di grading manuale/automatico. | Chiudere l'ultimo miglio operativo emerso dal delivery dry-run senza simulare capability non disponibili. | no |
| 2026-08-23 | Activity packaging + TheBitLab handoff | `lab-fix` / `setup` | Aggiunto adapter TPSI5 che preserva gli Activity JSON canonici, rimappa la guida studente `README.md` in `GUIDA.md` solo nel bundle effimero, classifica TypeScript/asset-directory come fallback espliciti e aggiunge uno smoke cross-repo Linux/Windows sul pin reale. Allineati inoltre i soli `tipo` delle Activity evidence E e capstone F ai valori ammessi dallo schema, lasciando invariati difficoltà, consegna, rubrica e grading. | Il rehearsal post-merge ha mostrato che la validazione schema da sola non garantiva la scaffoldability: `README.md` è riservato dalla piattaforma e alcune capability non sono presenti nel pin. | no |
| 2026-08-23 | `teacher/PILOT_REHEARSAL_TPSI5.md` + teacher guide | `setup` | Aggiunto un playbook TPSI5 per la prova generale prima della prima classe: congela release/pin, usa il primo lab HTML come content smoke, verifica adapter/scaffold e separa i controlli CI dai gate sul deployment reale necessari per `GO pilot`. | Rendere ripetibile la decisione `GO tecnico demo` / `GO pilot` / `NO-GO` senza confondere una CI verde con readiness operativa di autenticazione, Docker, tentativi, backup, revoca e governance. | no |

## Tipi

- `errata` — errore corretto;
- `clarification` — spiegazione resa più chiara senza cambiare obiettivi;
- `slides` — modifica al materiale di presentazione;
- `lab-fix` — correzione di laboratorio a parità di contratto/obiettivo;
- `setup` — installazione, avvio, ambiente o troubleshooting;
- `curriculum-change` — modifica significativa che richiede review/versioning del curriculum.

## Regola operativa

Aggiornare prima la fonte canonica, poi slide/guide/artifact derivati. Se gli studenti hanno già ricevuto una versione precedente, indicare esplicitamente se può ancora essere usata oppure è stata superata.
