# Diagnosi di riferimento

Sono accettabili formulazioni diverse se collegano chiaramente causa ed effetto.

1. **`body { width: 1200px; }`**: obbliga il documento a una larghezza superiore a molti viewport e genera overflow.
2. **`.page-shell` con colonne `280px 700px 280px`, gap e width fissa**: il macro-layout non puo contrarsi.
3. **`box-sizing: content-box`**: padding e border si sommano alle larghezze dichiarate, aggravando il calcolo.
4. **`#feed { min-width: 700px; }`**: impedisce al feed di restringersi.
5. **`padding: 4rem !important` su `#feed`**: vince sulla regola successiva `.page-shell #feed`; il problema e di cascade/important, non di ordine soltanto.
6. **`.nav-list { flex-wrap: nowrap; width: 700px; }`**: la navigazione resta rigida su viewport stretti.
7. **Media query invertita**: da `min-width: 56rem` la Grid viene ridotta a una colonna proprio quando dovrebbe diventare wide.
8. **Stringa lunga**: rende visibile l'assenza di una strategia di wrapping/min-size, ma non e la causa primaria delle larghezze rigide.

## Fix di riferimento

- border-box globale;
- rimozione delle width rigide da body/nav/page-shell;
- Grid base a una colonna;
- tre colonne flessibili da 56rem;
- `min-width: 0` sulle regioni;
- wrapping nella nav;
- rimozione di `!important`;
- `overflow-wrap: anywhere` sul contenuto lungo come gestione del contenuto, non come occultamento del layout.
