# Feisbuc milestone 1 — shell responsive

## Obiettivo

Trasformare lo scheletro semantico di Feisbuc in un layout responsive senza framework CSS.

## File da modificare

- `style.css`;
- `index.html` solo se devi aggiungere una classe strettamente necessaria al layout: non riscrivere la semantica.

## Contratto minimo

### Base mobile

Con viewport stretto:

- una sola colonna;
- nessuna larghezza principale fissa;
- nessun overflow orizzontale;
- menu capace di andare a capo;
- post leggibili senza zoom orizzontale.

### Viewport ampio

Da `56rem`:

```text
profilo | feed | tendenze
```

La colonna centrale deve essere flessibile e restringibile.

## Tecniche richieste

- `box-sizing: border-box`;
- almeno 4 custom properties in `:root`;
- CSS Grid per `.page-shell`;
- Flexbox per `.nav-list`;
- Flexbox per `.post-actions`;
- `gap`;
- una media query `min-width: 56rem`;
- immagini responsive.

## Tecniche vietate

- `float` per le colonne;
- `!important`;
- `overflow-x: hidden` per nascondere errori;
- `width: 1200px` o equivalenti per il layout principale.

## Procedura consigliata

1. Apri la pagina senza modifiche.
2. Imposta custom properties e box sizing.
3. Sistema le card senza ancora creare colonne.
4. Rendi menu e azioni Flexbox.
5. Costruisci `.page-shell` a una colonna.
6. Prova 360px, 768px e un viewport desktop usando Responsive Design Mode.
7. Solo dopo aggiungi la media query wide.
8. Attiva il Grid overlay dei DevTools e controlla le tre track.
9. Cerca overflow orizzontale prima della consegna.

## Domande da saper spiegare

- Perche il menu e Flexbox e la pagina principale Grid?
- Perche la regola di base e a una colonna?
- Perche `minmax(0, 1fr)` e utile per il feed?
- Che cosa cambia con `box-sizing: border-box`?
- Quale problema risolvono le custom properties?

## Definition of done

La pagina funziona con viewport stretto e ampio, usa gli strumenti richiesti e sai motivare le scelte senza dire soltanto “perche cosi funziona”.
