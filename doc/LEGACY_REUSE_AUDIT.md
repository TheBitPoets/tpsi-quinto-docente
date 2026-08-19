# Audit delle risorse legacy TPSI quinto

Stato: **draft progressivo**. Gli SHA sono snapshot di provenance; nessun repository legacy viene copiato integralmente.

## Strategia generale

```text
legacy -> audit -> reuse/rewrite/replace/retire -> contenuto originale + Activity
```

La progressione storica `statico -> JS -> fetch/Express -> SQLite -> login -> template -> realtime` viene conservata come intuizione, ma il nuovo ordine rende espliciti i modelli prima delle librerie.

## UDA21–23

- `html_css_summary` snapshot `d71da420f1aa2ea39b61356e4f9900c6371e7a42`: concetti riusati, struttura/semantica/CSS modernizzati;
- `kinderp/lab3` snapshot `0deae0eb606bc9c2849ba271bdf03c128910f1ac`: JavaScript selective rewrite; `Promise/async-await` viene spostato a **UDA 23**, mentre DOM, state/render ed **event delegation** restano in UDA22;
- `TheBitPoets/feisbuc` snapshot `086995ece4260a3408740b94cfe2701ce24f8b57`: progetto longitudinale; l'output JavaScript locale e la **milestone 3** `feisbuc-03-dynamic-local-feed`;
- `lab5/6/7`: client/server, form POST, query/path/body ricollocati dopo HTTP esplicito.

## UDA24 — responsabilita una alla volta

```text
node:http fixture
 -> Express + MemoryPostStore
 -> SqlPostStore + SQLite
 -> users/session/authz
 -> SSR/template comparison
```

### `kinderp/lab8`

Snapshot `be9a3988aec8a99b1a0f6776ad8cbeba33d82353`.

Decisione: **MIGRATED SQL CONCEPTS; RETIRE MUTATING GET/TIGHT COUPLING**.

Output: `07_SQL_RAW_PERSISTENCE.md`, SQL Activity A/B/D, `SqlPostStore`, milestone 6.

### `kinderp/lab9`

Snapshot `97ee815691e0c985e5216e6f9ed264fd809509ee`.

Decisione: **MIGRATED AUTH MOTIVATION; RETIRE CREDENTIAL/PORTABILITY/TRUST ANTI-PATTERNS**.

```text
legacy password plaintext -> scrypt + salt
absolute DB path           -> DB_PATH
client identity            -> req.auth.user
implicit authz             -> owner check server-side
no real revocation         -> opaque session + TTL/logout
```

Output: `08_AUTH_SESSIONI_SICUREZZA.md`, auth Activity A-D, milestone 7.

### `kinderp/lab10`

Snapshot `7319c0696c8a6f76237e1ef21b4c3c2b535c4958`.

Decisione: **MIGRATED SSR INTUITION; SPLIT PRESENTATION FROM SQL/AUTH**.

Valore conservato:

- Nunjucks come template engine;
- dati persistenti trasformati in HTML server-side;
- utilita del confronto con un client che riceve JSON.

Debiti ritirati:

| Legacy | Nuovo modello |
| --- | --- |
| Express + SQLite + query + template nello stesso `server.js` | store/auth gia esistenti + SSR Router separato |
| route `/api/...` che restituisce HTML | `/api/*` resta JSON; `/ssr` rende HTML |
| query SQL dentro le route di rendering | `SqlPostStore` dietro interface |
| template context costruito direttamente da row DB | view model minimo |
| nessun confronto con client rendering | stessa feature osservata in Network via API e SSR |

Il server legacy mostrava gia `nunjucks.configure(..., { autoescape: true, express: app })`; il nuovo corso conserva **autoescape**, ma usa un `Environment` esplicito e mantiene auth/SQL fuori dal template.

Output quarto blocco UDA24:

- `09_SSR_NUNJUCKS_CONFRONTO.md`;
- Activity A view model autograded;
- Activity B Nunjucks autoescape;
- Activity C Feisbuc `feisbuc-08-ssr-nunjucks`;
- Activity D SSR boundary review.

## UDA24 completata

```text
protocollo -> framework -> persistence -> identity/security -> presentation comparison
```

Il prossimo capitolo storico da auditare e `lab11`/Socket.IO quando entreremo in UDA25 realtime. ORM resta una decisione indipendente: non viene inserito solo perche UDA24 e terminata.
