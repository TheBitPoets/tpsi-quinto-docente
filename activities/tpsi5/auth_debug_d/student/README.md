# Activity D — security review auth

Il codice `insecure.js` e intenzionalmente vulnerabile. Non va riutilizzato in progetti reali.

## Metodo

Per ogni finding compila:

```text
asset / trust boundary
        ↓
vulnerabilita
        ↓
attacco possibile
        ↓
fix
        ↓
evidence che dimostra il fix
```

Non fermarti a “manca HttpOnly”. Spiega **che cosa protegge**, che cosa non protegge e come lo verificheresti.

Finding minimi:

- password storage;
- user enumeration;
- session ID;
- cookie;
- secret nella response;
- identity spoofing su create;
- authorization/IDOR su delete;
- revoca e scadenza sessione.

Concludi disegnando il trust boundary corretto dal browser al DB.
