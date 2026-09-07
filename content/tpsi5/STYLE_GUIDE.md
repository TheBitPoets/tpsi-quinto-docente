# Standard di formattazione delle dispense TPSI5

Questo documento definisce il formato editoriale canonico delle pagine del corso TPSI5. Il modello deriva dalla grammatica HTML/Markdown usata nel corso [2cornot2c](https://github.com/TheBitPoets/2cornot2c), adattata alle dispense di sviluppo full stack.

Lo standard si applica a tutte le lezioni in `content/tpsi5/`. Le pagine esistenti vengono adeguate progressivamente quando sono revisionate; ogni contenuto nuovo deve nascere già conforme.

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
python3 scripts/build_course_diagrams.py --check
python3 scripts/build_slides.py --check-only
```

## Rapporto con le slide

Questo standard riguarda le dispense in `content/tpsi5/`. Le presentazioni in `slides/tpsi5/` seguono la sintassi e i vincoli Marp: non devono essere convertite automaticamente in HTML. Dispensa e slide condividono però lessico, ordine didattico, icone e diagrammi.
