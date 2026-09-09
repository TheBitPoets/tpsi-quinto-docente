# Activity C — Feisbuc milestone 11

Lo starter è già un progetto full stack completo. Contiene il backend funzionante, il frontend della milestone 10 e i file TypeScript con i TODO della milestone 11. Non devi copiare file, applicare overlay o eliminare manualmente i moduli JavaScript sostituiti.

## Procedura

1. esegui `npm install` dalla root dello starter;
2. completa `frontend/src/api.ts` e `frontend/src/navigation-policy.ts`;
3. porta i componenti e le view principali a `<script setup lang="ts">` seguendo la dispensa;
4. esegui dalla root:

```bash
npm run type-check
npm run build
```

`npm run build` ripete anche il type-check e integra automaticamente la build Vue nel backend. Per lavorare in modalità sviluppo puoi usare due terminali:

```bash
npm run dev:backend
npm run dev:frontend
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
