# Osservazioni attese

1. `paths -> /api/posts -> get/post` descrive le path operation.
2. Il body usa lo schema `PostCreate` generato da Pydantic/JSON Schema.
3. La response usa `Post` (lista di Post per GET, Post per POST).
4. La POST valida restituisce 201 e `Location: /api/posts/<id>`.
5. Il body vuoto viola `min_length`; la validation avviene prima della funzione e FastAPI restituisce 422.
6. Lo status e l'envelope della validation fanno parte della response HTTP osservata: un client puo dipenderne.
7. `@app.get` registra route/method come `router.get` in Express, pur con un modello di framework diverso.
8. Il type hint descrive un contratto per tooling/framework; Pydantic esegue la verifica runtime del dato remoto.
