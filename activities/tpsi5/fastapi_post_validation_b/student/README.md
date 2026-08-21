# Post policy Python

Input:

```json
{"text":"  ciao  "}
```

Output valido:

```json
{"ok":true,"text":"ciao"}
```

Errori ammessi:

```text
post-text-required
post-text-too-long
```

La funzione e volutamente indipendente da FastAPI/Pydantic: il dominio non deve esistere solo dentro il framework.
