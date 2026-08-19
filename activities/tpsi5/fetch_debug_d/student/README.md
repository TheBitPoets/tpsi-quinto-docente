# Debug fetch/HTTP

## Regola del lab

**Prima diagnosi, poi fix.**

1. avvia `node server.mjs`;
2. apri l'URL stampato;
3. apri DevTools → Network e Console;
4. esegui i tre casi;
5. compila `DIAGNOSI.md`;
6. soltanto dopo modifica `client.js`.

## I tre casi

- **GET missing**: la risorsa non esiste;
- **POST broken**: il client vuole inviare JSON;
- **204 no content**: il server conferma successo senza body.

## Obiettivo

Arrivare a un helper che distingua:

```text
fetch reject / runtime problem
          !=
HTTP response con status 4xx/5xx
          !=
response 2xx con parsing body scorretto
```

## Definition of done

- [ ] DIAGNOSI compilata prima del fix;
- [ ] 404 non appare piu come successo;
- [ ] POST usa representation JSON coerente e riceve 201;
- [ ] 204 non viene parsato con `response.json()`;
- [ ] UI distingue `http` da `network-or-runtime`;
- [ ] usi `response.ok`;
- [ ] verifichi le correzioni dal pannello Network.
