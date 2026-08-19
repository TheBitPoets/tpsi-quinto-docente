# Activity A — `node:http` vs Express

## Setup

```bash
npm install
```

Avvia prima il server nativo:

```bash
PORT=3001 npm run native
```

Poi, dopo averlo fermato, avvia Express sulla stessa porta:

```bash
PORT=3001 npm run express
```

Su PowerShell:

```powershell
$env:PORT=3001; npm run native
$env:PORT=3001; npm run express
```

## Request da ripetere su entrambi

```bash
curl -i http://127.0.0.1:3001/api/health
```

```bash
curl -i \
  -H "Content-Type: application/json" \
  -d '{"message":"ciao"}' \
  http://127.0.0.1:3001/api/echo
```

```bash
curl -i http://127.0.0.1:3001/non-esiste
```

## Obiettivo

Non dire soltanto "Express ha meno righe".

Individua **quali responsabilita** vengono astratte:

- routing;
- parsing;
- response helper;
- middleware/error pipeline.

E quali restano HTTP:

- metodo;
- path;
- status;
- header;
- representation.

Completa `MAPPING.md`.
