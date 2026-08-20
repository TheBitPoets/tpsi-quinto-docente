# Feisbuc milestone 12 — realtime

Parti dalla milestone 11 TypeScript. Applica gli asset overlay di questa Activity.

## Obiettivo osservabile

Apri due sessioni browser distinte, Alice e Bob.

1. entrambi fanno login;
2. entrambi aprono `/vue/feed`;
3. Alice crea un post con la normale API REST;
4. Bob vede il post senza refresh;
5. Bob cambia like: Alice vede l'update;
6. Alice elimina un proprio post: Bob lo vede scomparire;
7. simula offline di Bob, modifica il feed con Alice, poi riporta Bob online;
8. al reconnect Bob deve rifare `GET /api/posts` e convergere allo snapshot server.

## Boundary obbligatorio

```text
POST/PATCH/DELETE -> REST -> auth/validation/store
                                  ↓
                            domain event
                                  ↓
                             Socket.IO
                                  ↓
                            altri client
```

Non aggiungere handler socket `post:create`, `post:like` o `post:delete`.

## Checklist

- [ ] `socket.io` e `socket.io-client` pinned 4.8.3;
- [ ] stesso cookie HttpOnly della sessione;
- [ ] socket anonimo rifiutato;
- [ ] `post:created`, `post:updated`, `post:deleted`;
- [ ] reducer idempotente;
- [ ] listener registrati una sola volta e rimossi allo stop;
- [ ] reconnect -> snapshot REST;
- [ ] nessun Pinia;
- [ ] nessun `authorId` scelto dal client;
- [ ] `npm run type-check` verde;
- [ ] evidence con due utenti.

## Evidence da consegnare

In `EVIDENCE.md` annota per almeno una create/update/delete:

- request HTTP che ha eseguito il comando;
- response HTTP;
- evento realtime ricevuto dall'altro client;
- stato finale dei due feed.

Aggiungi una prova di disconnect/reconnect e spiega perche il nuovo snapshot e necessario.
