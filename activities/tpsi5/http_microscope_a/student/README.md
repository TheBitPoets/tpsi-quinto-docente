# HTTP al microscopio

## Avvio

```bash
node server.mjs
```

Il server stampa l'URL di ascolto, normalmente `http://127.0.0.1:3000`.

Apri quell'indirizzo: la pagina **HTTP observer** genera le stesse richieste dal browser, così puoi leggerle in DevTools → Network.

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

## Schede da compilare

Per ciascuno dei cinque casi copia questo modello. Le righe brevi restano leggibili anche su uno schermo piccolo.

### Caso: …

- Metodo e target:
- Request header significativi:
- Request body:
- Status:
- Response header significativi:
- Response body:
- Significato del risultato:
- Protocollo o rappresentazione? Perché?

## DevTools

Ripeti almeno una richiesta dal browser o da una pagina locale che usa `fetch`, quindi apri **Network** e individua:

- Request URL;
- Request Method;
- Status Code;
- Request Headers;
- Request Payload;
- Response Headers;
- Response/Preview.

## Esperimento same-origin e CORS

La pagina aperta da `http://127.0.0.1:3000` e la relativa API hanno la stessa origin. Ora servi gli stessi file da un'altra porta:

Da un secondo terminale, nella cartella che contiene i file dell'Activity:

```bash
python3 -m http.server 5173
```

Apri `http://127.0.0.1:5173/observer.html`, lascia come endpoint API `http://127.0.0.1:3000` e confronta:

- un GET, che normalmente non richiede preflight;
- un POST JSON, per il quale il browser invia normalmente prima `OPTIONS`;
- gli header `Origin`, `Access-Control-Request-*` e `Access-Control-Allow-*`;
- ciò che vede lo script e ciò che rimane comunque visibile in Network e Console.

La fixture consente soltanto le origin didattiche sulla porta 5173: CORS non equivale a “accetta chiunque”.

## Domande

1. Che differenza c'è fra status code e body JSON?
2. Perché `201 Created` comunica qualcosa che il solo JSON non comunica?
3. Che cosa significa `Content-Type: application/json`?
4. In quale caso hai ricevuto una risposta HTTP valida ma con esito negativo?
5. Che differenza c'è fra `404` e “server non raggiungibile”?
6. Che informazione aggiunge l'header `Allow` nella risposta `405`?
7. Perché la fixture non richiede Express per parlare HTTP?
8. Perché la richiesta POST cross-origin produce un preflight, mentre il GET può non produrlo?

## Definition of done

- [ ] cinque casi osservati;
- [ ] tabella completa;
- [ ] almeno un uso di `curl -i`;
- [ ] almeno una request letta da DevTools Network;
- [ ] confronto fra stessa origine e origine diversa completato;
- [ ] sai spiegare request, response, status, header e content senza nominare Express.
