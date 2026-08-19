# Activity D — Debug CSS responsive

Questa non e una gara a modificare proprieta finche la pagina “sembra giusta”. Devi produrre una **diagnosi ripetibile**.

## Ordine obbligatorio

1. Apri la pagina a viewport desktop e mobile.
2. Non modificare ancora il CSS.
3. Compila almeno cinque righe in `DIAGNOSI.md`.
4. Usa DevTools per ispezionare dimensioni e regole applicate.
5. Correggi `style.css` una causa alla volta.
6. Dopo ogni correzione verifica se il sintomo previsto cambia.
7. Completa la sezione finale del report.

## Obiettivo finale

- mobile: una colonna;
- wide da 56rem: tre colonne flessibili;
- nessun overflow orizzontale;
- feed restringibile;
- navigazione con wrapping;
- `box-sizing: border-box`;
- nessun `!important`;
- nessun `overflow-x: hidden`.

## Non modificare

`index.html` e corretto. Se senti il bisogno di cambiarlo per sistemare la larghezza, torna alla diagnosi CSS.

## Domande guida

- Il `body` ha una dimensione che puo superare il viewport?
- Le colonne Grid sono fisse o flessibili?
- Padding e border entrano o si sommano alla width?
- Quale dichiarazione di `padding` vince su `#feed`?
- Il breakpoint wide sta davvero creando il layout wide?
- La navigazione e libera di andare a capo?
- Un contenuto lungo puo costringere il feed a non restringersi?

## Definition of done

Sai mostrare il prima/dopo a due viewport e, per ogni modifica principale, sai spiegare quale causa hai eliminato.
