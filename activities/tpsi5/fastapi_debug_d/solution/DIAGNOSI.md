# Diagnosi reference

## 1. Create status

Il decoratore senza `status_code` usa 200. Una creazione deve dichiarare 201 e, nel contratto del corso, `Location`.

## 2. Body `dict`

`dict` non descrive campi/constraint del command. `PostCreate` rende validation e OpenAPI leggibili; non e solo una questione di autocomplete.

## 3. `authorId` trusted

Il broken backend usa `payload["authorId"]`: identity spoofing. `authorId` non appartiene a `PostCreate`; nel mirror usa una fixture server-side, nel prodotto reale deriva dalla sessione.

## 4. Id mancante

`posts[post_id]` alza `KeyError` e puo diventare 500. L'assenza della risorsa e un caso HTTP governato: 404.

## 5. Campo interno

Restituire il dict interno pubblica `internalSecret`. `response_model=Post` definisce la representation pubblica e filtra il campo. Questo non sostituisce l'authorization: protegge la shape, non decide chi puo leggere.
