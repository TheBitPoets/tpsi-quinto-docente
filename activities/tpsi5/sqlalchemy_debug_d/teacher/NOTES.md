# Note docente

Far classificare i difetti prima di correggerli:

- infrastructure lifetime -> Engine;
- unit-of-work lifetime -> Session;
- API generation -> Query legacy vs `select`;
- transaction durability -> flush/commit;
- failure recovery -> rollback;
- representation boundary -> `row.__dict__`.

Insistere su due distinzioni:

1. `flush` non e commit;
2. Session SQLAlchemy non e sessione HTTP.

La reference usa un mapping esplicito di output e Session corte. Non introdurre dependency injection framework-specifica nel repository: il punto e mantenere il data layer indipendente da FastAPI.
