# OSSERVAZIONI — realtime microscope

Compila con frasi brevi ma causali.

## 1. Polling

- Chi avvia ogni richiesta?
- Che cosa succede se non ci sono novita?
- Quale latenza massima introduce un polling ogni 5 secondi?

## 2. WebSocket

- Quale richiesta iniziale permette di aprire il canale?
- Dopo l'handshake, chi puo inviare dati?
- Che cosa **non** definisce da solo WebSocket a livello applicativo?

## 3. Socket.IO

- Perche non e corretto scrivere `Socket.IO = WebSocket`?
- Che ruolo hanno eventi come `post:created`?
- Che cosa fa automaticamente quando perde temporaneamente la connessione?

## 4. Reconnect e recovery

Scenario: Bob e offline mentre Alice crea un post.

- Bob riceve quell'evento mentre e offline?
- Che cosa deve fare al reconnect per tornare coerente?
- Nel nostro corso, quale endpoint fornisce lo snapshot autorevole?

## 5. Command vs event

Completa:

```text
creare un post: ____________
notificare gli altri client: ____________
source of truth persistente: ____________
recovery dopo reconnect: ____________
```
