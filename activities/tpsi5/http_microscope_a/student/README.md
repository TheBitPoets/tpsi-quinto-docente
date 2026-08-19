# HTTP al microscopio

## Avvio

```bash
node server.mjs
```

Il server stampa l'URL di ascolto, normalmente `http://127.0.0.1:3000`.

## Esperimenti obbligatori

### 1. GET collezione

```bash
curl -i http://127.0.0.1:3000/api/posts
```

### 2. GET risorsa mancante

```bash
curl -i http://127.0.0.1:3000/api/posts/missing
```

### 3. POST JSON valido

```bash
curl -i \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"text":"Post da curl"}' \
  http://127.0.0.1:3000/api/posts
```

### 4. Media type errato

Invia lo stesso body senza `Content-Type: application/json` e confronta la risposta.

### 5. Metodo non ammesso

```bash
curl -i -X DELETE http://127.0.0.1:3000/api/posts
```

## Tabella da compilare

| Caso | Method | Target | Request Content-Type | Request body | Status | Response Content-Type | Response body | Nota semantica |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GET posts | | | | | | | | |
| GET missing | | | | | | | | |
| POST JSON | | | | | | | | |
| POST media type errato | | | | | | | | |
| DELETE | | | | | | | | |

## DevTools

Ripeti almeno una richiesta dal browser o da una pagina locale che usa `fetch`, quindi apri **Network** e individua:

- Request URL;
- Request Method;
- Status Code;
- Request Headers;
- Request Payload;
- Response Headers;
- Response/Preview.

## Domande

1. Che differenza c'e fra status code e body JSON?
2. Perche `201 Created` comunica qualcosa che il solo JSON non comunica?
3. Che cosa significa `Content-Type: application/json`?
4. In quale caso hai ricevuto una risposta HTTP valida ma con esito negativo?
5. Che differenza c'e fra `404` e "server non raggiungibile"?
6. Che informazione aggiunge l'header `Allow` nella risposta `405`?
7. Perche la fixture non richiede Express per parlare HTTP?

## Definition of done

- [ ] cinque casi osservati;
- [ ] tabella completa;
- [ ] almeno un uso di `curl -i`;
- [ ] almeno una request letta da DevTools Network;
- [ ] sai spiegare request, response, status, header e content senza nominare Express.
