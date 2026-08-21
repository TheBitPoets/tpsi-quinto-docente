# Diagnosi FastAPI

Per ogni difetto indica:

- sintomo HTTP/OpenAPI;
- causa;
- boundary violato;
- fix minimo;
- test che impedirebbe la regressione.

Casi da coprire:
1. status create;
2. body/schema;
3. authorId/trust;
4. id mancante;
5. campo interno in output.
