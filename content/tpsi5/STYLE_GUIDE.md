# Standard di formattazione delle dispense TPSI5

Questo documento definisce il formato editoriale canonico delle pagine del corso TPSI5. Il modello deriva dalla grammatica HTML/Markdown usata nel corso [2cornot2c](https://github.com/TheBitPoets/2cornot2c), adattata alle dispense di sviluppo full stack.

Lo standard si applica a tutte le lezioni in `content/tpsi5/`. Le lezioni revisionate manualmente costituiscono il riferimento qualitativo; la sola normalizzazione automatica dell'HTML non equivale a una revisione editoriale completa. Ogni contenuto nuovo deve nascere già conforme.

## Principio generale

Le dispense usano un formato ibrido compatibile con GitHub:

- titoli Markdown per conservare indice, anchor e link diretti alle sezioni;
- HTML per impaginazione, allineamento e componenti didattici;
- SVG locali costruiti con il Visual System TPSI5;
- blocchi di codice Markdown fuori dai contenitori HTML, oppure `<pre><code>` dentro i pannelli espandibili.

Non aggiungere CSS, JavaScript o dipendenze remote: la pagina deve rimanere leggibile direttamente su GitHub.

## Titoli

I titoli restano in Markdown:

```markdown
# Titolo della lezione

## Argomento

### Sottoargomento
```

Questo preserva gli anchor generati da GitHub. Non sostituire i titoli con `<h1>`, `<h2>` o `<h3>`.

Gerarchia obbligatoria:

- un solo titolo `#` per il documento;
- sezioni principali con `##`;
- sottosezioni con `###`;
- livelli più profondi soltanto quando servono davvero.

Per le destinazioni richiamate da mappe e indici usare un anchor esplicito e stabile prima del titolo:

```html
<a id="lesson-example"></a>
## Titolo della sezione
```

## Struttura canonica di una lezione

La lezione `01_WEB_PLATFORM_HTML_MODERNO.md` è il riferimento strutturale. Ogni nuova dispensa, e ogni dispensa sottoposta a revisione completa, segue questo ordine adattandolo all'argomento:

1. titolo della lezione;
2. pannello espandibile di orientamento con contesto, domande guida, obiettivi osservabili e prossimo passo;
3. obiettivi e prerequisiti dettagliati;
4. orientamento nella documentazione con fonti ufficiali, profondità richiesta e prodotto osservabile;
5. problema iniziale concreto;
6. spiegazione progressiva dei concetti;
7. applicazione al progetto Feisbuc o confronto fra implementazioni;
8. errori frequenti e metodo di debug;
9. esercizi o laboratorio;
10. verifica rapida;
11. sintesi inclusiva;
12. fonti, provenance e collegamento alla lezione successiva.

L'ordine non obbliga tutte le lezioni ad avere la stessa lunghezza. Un translation lab può essere più breve di una lezione fondativa, ma non può omettere il modello mentale, gli esempi verificabili o i confini dichiarati.

### Componenti editoriali obbligatori

Le lezioni sottoposte a revisione completa devono rendere riconoscibili, nello stesso ordine e con le stesse icone, almeno questi componenti:

1. un pannello espandibile <strong>Orientamento della sezione</strong>, che contiene contesto, domande guida, obiettivi, prerequisiti e prossimo passo;
2. quando si usa documentazione esterna, una sezione di orientamento con legenda, mappa di copertura specifica della lezione e indice incrociato navigabile;
3. una mappa espandibile delle schede tecniche operative — elementi, proprietà, classi, componenti o API — quando lo studente deve consultarle durante la lezione;
4. anchor espliciti e stabili per ogni sezione raggiunta dalle mappe o dagli indici;
5. callout canonici per definizioni, modelli mentali, attenzioni e decisioni;
6. laboratorio e Activity dentro pannelli espandibili con collegamenti cliccabili a consegna e starter;
7. checkpoint dentro un pannello espandibile con icona coerente;
8. sintesi visibile, fonti ufficiali, provenienza interna e rimando alla lezione successiva.

Il testo fondamentale della spiegazione <strong>non deve essere collassato</strong>. I pannelli espandibili organizzano orientamento, mappe, materiale operativo, approfondimenti e verifiche; non devono nascondere la definizione necessaria per comprendere il paragrafo seguente.

### Forma dell'indice incrociato

L'indice incrociato non usa una tabella larga con molte colonne. Per evitare lo scorrimento orizzontale, viene suddiviso in gruppi espandibili e schede verticali abbinate:

- il titolo della dispensa è cliccabile e conduce all'anchor locale;
- il titolo della fonte ufficiale è cliccabile e apre la pagina pertinente;
- le descrizioni sono elenchi brevi e non cliccabili;
- una voce senza corrispondenza viene dichiarata esplicitamente;
- stato e profondità non dipendono soltanto dal colore.

### Diagrammi richiesti dalla spiegazione

L'immagine generale sulla profondità della documentazione non sostituisce una mappa di copertura specifica. Quando una lezione introduce relazioni, flussi, gerarchie, anatomie o confronti con almeno tre elementi, deve usare un diagramma locale del Visual System. Gli schemi ASCII possono restare soltanto per micro-esempi testuali; non sostituiscono un'immagine quando lo schema svolge una funzione didattica centrale.

## Struttura di un argomento

Quando introduce un concetto nuovo, il paragrafo cerca di rendere visibili almeno questi passaggi:

1. problema o domanda a cui il concetto risponde;
2. definizione semplice e precisa;
3. modello mentale o rappresentazione osservabile;
4. esempio minimo;
5. applicazione nel progetto del corso;
6. errore frequente o limite;
7. riferimento ufficiale puntuale.

Non è necessario trasformare ogni punto in un sottotitolo. È invece necessario evitare sequenze di API o sintassi prive di una spiegazione del perché e di una prova concreta.

## Audit di profondità

La qualità non si misura contando righe o tentando di riprodurre integralmente MDN e le documentazioni dei framework. Per ogni lezione si confrontano gli obiettivi dichiarati con le fonti ufficiali e si classificano i contenuti:

- <strong>studiare ora:</strong> indispensabili per raggiungere gli obiettivi della lezione;
- <strong>riconoscere:</strong> presentati per orientarsi nella documentazione ma non ancora richiesti in autonomia;
- <strong>più avanti:</strong> pertinenti, ma assegnati esplicitamente a una lezione successiva;
- <strong>fuori confine:</strong> esclusi intenzionalmente dal curriculum corrente.

Una lezione è sufficientemente profonda quando spiega tutti i concetti necessari ai propri obiettivi, li rende osservabili e dichiara i confini. Non deve copiare l'intero indice della fonte esterna.

## Paragrafi

Il testo discorsivo usa paragrafi giustificati:

```html
<p align="justify">
Testo del paragrafo.
</p>
```

Usare `<strong>`, `<em>` e `<code>` al posto della sintassi Markdown quando il testo si trova dentro un blocco HTML.

## Immagini

Le immagini sono locali, centrate e dotate di testo alternativo:

```html
<p align="center">
  <img src="../../assets/tpsi5/nome-immagine.svg" alt="Descrizione chiara del contenuto dell'immagine">
</p>
```

Regole:

- non usare URL remoti;
- non omettere `alt`;
- usare gli SVG generati dal Visual System quando il diagramma è componibile;
- non affidare un significato esclusivamente al colore.

## Liste

Nei contenuti HTML usare liste HTML:

```html
<ul>
  <li>primo elemento;</li>
  <li>secondo elemento.</li>
</ul>
```

Per sequenze e procedure usare `<ol>`.

## Tabelle informative

Le tabelle di confronto usano HTML e vengono centrate:

```html
<table align="center">
<thead>
<tr><th>Concetto A</th><th>Concetto B</th></tr>
</thead>
<tbody>
<tr><td>Descrizione A</td><td>Descrizione B</td></tr>
</tbody>
</table>
```

## Callout semantici

Definizioni, attenzioni e idee chiave sono visualizzate dentro una tabella HTML centrata:

```html
<table align="center">
<tr>
<td>
<p align="justify">
<strong><span style="font-size: 1.15em;">&#128214;</span> Definizione — termine:</strong>
Testo breve, autonomo e preciso.
</p>
</td>
</tr>
</table>
```

Vocabolario delle icone:

| Entità | Icona | Codice HTML | Etichetta consigliata |
|---|---:|---:|---|
| orientamento o percorso | 🗺 | `&#128506;` | Contesto / Percorso concettuale |
| definizione | 📖 | `&#128214;` | Definizione — termine |
| attenzione | ⚠ | `&#9888;` | Attenzione |
| idea o modello introduttivo | 💡 | `&#128161;` | Idea chiave / Modello introduttivo |
| checkpoint | ✅ | `&#9989;` | Verifica rapida |
| laboratorio | 💻 | `&#128187;` | Laboratorio / Esercizi collegati |
| decisione congelata | 🔒 | `&#128274;` | Decisione architetturale |
| rimando | 🔗 | `&#128279;` | Rimando / Approfondimento |

La stessa funzione didattica deve usare sempre la stessa icona e la stessa etichetta.

## Pannelli espandibili

Contenuti accessori, riepiloghi, soluzioni, checkpoint e laboratori possono usare `<details>` e `<summary>`. Quando serve un bordo visivo coerente, il pannello viene inserito in una tabella centrata:

```html
<table align="center">
<tr>
<td>
<details>
<summary>&#128187; <strong>Laboratorio — titolo</strong></summary>

<p align="justify">
Descrizione del laboratorio.
</p>

<pre lang="bash"><code>comando da eseguire</code></pre>

</details>
</td>
</tr>
</table>
```

Il `<summary>` deve spiegare che cosa verrà aperto. Non nascondere dentro un pannello chiuso una definizione indispensabile per comprendere il paragrafo successivo.

## Orientamento della lezione

All'inizio di ogni lezione inserire un pannello `Orientamento della sezione` con almeno:

- contesto;
- domande guida o prerequisiti;
- obiettivi osservabili;
- prossimo passo.

Il pannello serve a collegare la lezione a quella precedente e a quella successiva, non a ripetere l'indice.

## Riferimenti MDN

Il metodo generale di consultazione vive in `GUIDA_USO_MDN.md` e non deve essere duplicato nelle singole dispense. Quando MDN è una fonte operativa per lo studente, la lezione inserisce un pannello visibile “MDN in questa lezione” che contiene:

- il collegamento alla sezione pertinente della guida trasversale;
- le pagine MDN selezionate per l'argomento;
- la profondità richiesta, distinguendo ciò che va studiato da ciò che basta riconoscere;
- un prodotto osservabile, per esempio una scheda di lettura, una prova nei DevTools o una scelta tecnica motivata.

La documentazione specifica di framework, runtime e librerie resta la fonte primaria per le rispettive API. MDN viene affiancata per rendere esplicito il comportamento della Web Platform sottostante.

## Codice

Fuori dai blocchi HTML sono ammessi i fenced code block Markdown:

````markdown
```http
GET /api/posts
```
````

Dentro `<details>` usare invece:

```html
<pre lang="http"><code>GET /api/posts</code></pre>
```

Nei blocchi `<pre><code>` devono essere convertiti in entità HTML almeno `&`, `<` e `>`.

## Criteri di qualità

Prima di consegnare una pagina verificare che:

1. tutti i tag HTML siano bilanciati;
2. ogni immagine abbia `alt` e un percorso locale valido;
3. i titoli Markdown producano anchor stabili;
4. definizioni e avvertenze usino le icone canoniche;
5. il testo principale resti visibile senza aprire pannelli accessori;
6. diagrammi e slide siano aggiornati;
7. la resa su GitHub sia leggibile da desktop e non dipenda da CSS personalizzato.

Controlli minimi del repository:

```bash
git diff --check
python3 scripts/format_tpsi5_lessons.py --check
python3 scripts/build_course_diagrams.py --check
python3 scripts/build_slides.py --check-only
```

Il normalizzatore controlla le lezioni 00–18; la conversione iniziale ha interessato soprattutto le lezioni 02–18, che usavano prevalentemente Markdown. Conserva titoli e blocchi di codice Markdown, non modifica i componenti HTML già presenti e converte prosa, liste, citazioni e tabelle semplici nel formato ibrido canonico. Per applicare intenzionalmente la normalizzazione:

```bash
python3 scripts/format_tpsi5_lessons.py --write
```

La lezione 01 resta il riferimento editoriale verificato a mano; la lezione 00 contiene componenti introduttivi costruiti direttamente nel visual system.

## Rapporto con le slide

Questo standard riguarda le dispense in `content/tpsi5/`. Le presentazioni in `slides/tpsi5/` seguono la sintassi e i vincoli Marp: non devono essere convertite automaticamente in HTML. Dispensa e slide condividono però lessico, ordine didattico, icone e diagrammi.
