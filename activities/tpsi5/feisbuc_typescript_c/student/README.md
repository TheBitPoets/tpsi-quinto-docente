# Activity C — Feisbuc milestone 11

Questa Activity e un **overlay della milestone 10**.

## Procedura

1. copia la solution/starter della milestone 10 in una nuova directory;
2. sovrapponi i file `starter/frontend` di questa Activity;
3. rimuovi i file JavaScript sostituiti dai nuovi moduli TypeScript:
   - `src/main.js`
   - `src/api.js`
   - `src/navigation-policy.js`
   - `src/session.js`
   - `src/router.js`
4. completa `api.ts` e `navigation-policy.ts`;
5. porta i componenti/view principali a `<script setup lang="ts">` seguendo la dispensa;
6. esegui:

```bash
npm install
npm run type-check
npm run build
```

## Contratti da preservare

- nessuna modifica alle route `/api/*`;
- cookie di sessione ancora HttpOnly;
- nessun token in storage o `document.cookie`;
- ownership ancora server-side;
- `/vue/feed` deve continuare a funzionare come deep link;
- `Post` e `User` non vanno duplicati nei componenti.

## Boundary HTTP

Non e ammesso sostituire il parser con:

```ts
const post = await response.json() as Post
```

Il JSON esterno deve essere trattato come `unknown` e ristretto prima di entrare nel dominio.

## Definition of done

- `strict` resta attivo;
- `npm run type-check` verde;
- `npm run build` verde;
- nessun `any` nei file core;
- `domain.ts` e l'unico punto che dichiara User/Post/AuthStatus;
- props/emits principali tipizzati;
- navigation decision discriminated union;
- `RouteMeta.requiresAuth` tipizzato;
- deep-link e API auth invariati.
