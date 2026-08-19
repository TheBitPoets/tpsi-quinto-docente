# Activity B — Nunjucks e autoescape

Installa:

```bash
npm install
```

Completa `render.mjs` e `templates/post.njk`.

Verifica due casi:

```bash
node render.mjs
node render.mjs no-delete
```

Nel primo output il testo `<script>...</script>` deve apparire escapato, non come elemento `<script>` eseguibile.

Non usare `|safe` per ottenere il risultato.
