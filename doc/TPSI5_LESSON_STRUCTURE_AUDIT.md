# Audit strutturale e di profondità delle lezioni TPSI5

Data dell'audit: **2026-09-08**.

## Scopo

Questo audit confronta le lezioni `00–18` con il modello editoriale della lezione 01 e con le fonti tecniche ufficiali pertinenti. Il confronto non usa la lunghezza come metrica: verifica se gli obiettivi dichiarati hanno spiegazioni, esempi, confini, attività osservabili e riferimenti sufficienti.

## Criteri

Per ogni lezione sono stati controllati:

- orientamento iniziale e continuità con il percorso;
- gerarchia dei titoli;
- presenza di un problema iniziale;
- progressione definizione → esempio → applicazione → limite;
- rapporto tra dispensa e documentazione ufficiale;
- errori frequenti e metodo di debug;
- laboratorio, verifica, sintesi e prossimo passo;
- profondità rispetto agli obiettivi del Content Pack congelato.

## Esito per modulo

| Modulo | Esito dell'audit | Criticità rilevata | Intervento applicato |
|---:|---|---|---|
| 00 | adeguata | già conforme al visual system | solo controllo di coerenza |
| 01 | riferimento | nessuna criticità bloccante | mantenuto come modello |
| 02 | adeguata dopo integrazione | selettori, applicazione CSS e stile del testo troppo compressi | ampliati i fondamenti e creato l'orientamento documentale |
| 03 | adeguata dopo integrazione | form Bootstrap quasi assenti | aggiunti form, validazione e confine con HTML nativo |
| 04 | adeguata dopo integrazione | controllo di flusso implicito negli esempi | reso esplicito e raccordato a collezioni, render ed eventi |
| 05 | adeguata | struttura dei titoli e orientamento | normalizzate gerarchia e mappa delle fonti |
| 06 | adeguata | documentazione Node/Express non guidata | aggiunti indice documentale e gerarchia uniforme |
| 07 | adeguata dopo integrazione | `NULL`, relazioni e lettura del piano poco visibili | aggiunti fondamenti mirati senza anticipare il corso SQL |
| 08 | approfondita | densità elevata e gerarchia irregolare | aggiunti orientamento, titoli e percorsi di lettura |
| 09 | approfondita | fonti distribuite ma non mappate | aggiunti indice documentale e formato canonico |
| 10 | adeguata dopo integrazione | lifecycle e side effect Vue troppo impliciti | aggiunto lifecycle minimo e confine `computed`/`watch` |
| 11 | approfondita | orientamento documentale frammentato | aggiunta mappa Vue Router/History/Express |
| 12 | approfondita e mirata | fonti non classificate per responsabilità | aggiunta mappa TypeScript/Vue/runtime validation |
| 13 | adeguata | fonti WebSocket e Socket.IO da separare meglio | aggiunto indice documentale per i due livelli |
| 14 | adeguata come translation lab | brevità intenzionale non dichiarata graficamente | resi visibili orientamento e confini |
| 15 | approfondita | fonti FastAPI/OpenAPI non trasformate in percorso | aggiunto indice documentale |
| 16 | approfondita | alta densità concettuale | aggiunti orientamento e percorso SQLAlchemy ufficiale |
| 17 | approfondita | mancava una guida iniziale fra livelli di test e fonti | aggiunto indice documentale pytest/FastAPI/SQLAlchemy |
| 18 | adeguata dopo integrazione | handoff operativo, shutdown e osservabilità troppo sintetici | ampliato il ciclo di esercizio senza introdurre cloud avanzato |

## Decisione editoriale

Tutte le lezioni adotteranno lo stesso telaio riconoscibile, ma conserveranno lunghezza e profondità coerenti con la loro funzione. Le fonti generali della Web Platform saranno collegate tramite MDN; framework, runtime e librerie useranno prima la propria documentazione ufficiale. Le specifiche normative saranno indicate quando chiariscono un contratto, non come lettura obbligatoria integrale.

## Esito editoriale

Le lezioni 02–18 ora hanno un pannello iniziale uniforme, una mappa incrociata verso le fonti ufficiali, anchor stabili e il formato ibrido HTML/Markdown della lezione 01. La gerarchia irregolare dei moduli 05, 06 e 08 è stata corretta. Gli approfondimenti aggiunti risolvono i sei gap di contenuto senza espandere il curriculum con argomenti avanzati non necessari.
