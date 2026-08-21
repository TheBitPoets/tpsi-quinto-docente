# Osservazioni FastAPI/OpenAPI

1. In `/openapi.json`, dove trovi GET e POST di `/api/posts`?
2. Quale schema descrive il body della POST?
3. Quale schema descrive la response pubblica?
4. Che status restituisce una POST valida? Che header aggiunge?
5. Che cosa succede con `{ "text": "" }`? La funzione `create_post` viene eseguita?
6. Perche `422` e una decisione osservabile dal client e non solo un dettaglio interno?
7. Mappa `@app.get(...)` con la responsabilita equivalente gia vista in Express.
8. Spiega in una frase la differenza tra type hint Python e validation runtime.
