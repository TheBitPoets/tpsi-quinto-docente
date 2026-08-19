# Note docente — Feisbuc milestone 5

## Focus

Questa Activity non valuta SQL o autenticazione. Valuta se lo studente sa trasformare una fixture HTTP in una applicazione Express **senza perdere il contratto**.

## Domande di revisione

1. Se sostituissimo `MemoryPostStore` con SQL, quali file dovrebbero cambiare?
2. Perché `express.json()` deve stare prima del Router?
3. Perché il 404 middleware deve stare dopo le route/static?
4. Perché `validation.js` non importa Express?
5. Che differenza c'è fra `req.params.id` e `req.query.id`?
6. Perché il client non deve inventare l'id del post?
7. Perché `X-Request-Id` è utile anche prima dell'observability avanzata?
8. Perché non abbiamo aggiunto `cors()`?

## Red flags

- tutto in `server.js`;
- route che manipola direttamente `postStore.posts`;
- status sempre 200;
- `GET` che modifica lo stato;
- response error plain text casuali;
- password/auth aggiunte prematuramente;
- `try/catch` duplicato in ogni route per errori che la pipeline può centralizzare.

## Passaggio alla prossima fase

Quando il memory store è isolato bene, la PR SQL dovrà poter sostituire il repository senza riscrivere il client e senza cambiare il Router oltre al wiring necessario.
