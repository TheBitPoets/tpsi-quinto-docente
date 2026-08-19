# Activity A — policy credenziali

Obiettivo: separare **policy di input** e **password hashing**.

Il programma legge un JSON da stdin:

```json
{"email":"  STUDENTE@Example.Test ","password":"una passphrase lunga 2026"}
```

e stampa:

```json
{"ok":true,"email":"studente@example.test","errors":[]}
```

Regole:

- `input` deve essere un oggetto;
- `email`: trim + lowercase e controllo formato essenziale;
- password: **15–128 code point**;
- usa `Array.from(password).length`;
- non richiedere maiuscole, numeri o simboli;
- ordine errori: `body-invalid`, `email-invalid`, `password-too-short`, `password-too-long`.

Questa Activity **non** salva password e non implementa `scrypt`: serve a verificare prima il contratto di validazione che verra riusato dalla milestone auth.
