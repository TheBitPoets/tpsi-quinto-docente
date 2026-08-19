# Activity B — Validation pura

## Input

Un JSON su stdin:

```json
{"text":"  Ciao  "}
```

## Output valido

```json
{"ok":true,"value":{"text":"Ciao"}}
```

## Error code ammessi

```text
body-invalid
text-required
text-too-long
```

## Regola architetturale

La funzione non deve conoscere:

- `req`;
- `res`;
- Express;
- status HTTP.

Prima definiamo **se i dati sono validi**.

La route decidera poi come tradurre il risultato nel contratto HTTP.
