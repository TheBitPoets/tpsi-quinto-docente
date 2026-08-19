# TPSI quinto 2026/27 — matrice di copertura iniziale

Stato: **draft**. Questa matrice descrive il perimetro del corso prima della decomposizione definitiva in lezioni e Activity.

| Area | Core 2026/27 | Progetto Feisbuc | Note |
| --- | --- | --- | --- |
| Web Platform e browser | sì | struttura iniziale | **iniziato**: documenti, metadata, DevTools e distinzione sorgente/DOM in `01_WEB_PLATFORM_HTML_MODERNO.md` |
| HTML moderno e semantica | sì | **milestone 0 disponibile** | Activity A anatomia documento + Activity B Feisbuc semantico; form e immagini verranno approfonditi nello stesso blocco |
| CSS moderno | sì | **milestone 1 disponibile** | `02_CSS_MODERNO_RESPONSIVE.md`: cascade, specificità, inheritance, box model, normal flow, Flexbox, Grid, custom properties |
| Responsive design | sì | shell mobile-first | Activity C costruzione autonoma + Activity D debug/diagnosi; media query solo quando il layout fluido non basta |
| Bootstrap | sì, dopo CSS nativo | revisione UI | framework CSS, non sostituto dei fondamenti; non ancora iniziato |
| JavaScript moderno | sì | comportamento client | scope, funzioni, array/object, moduli, errori |
| DOM e Browser APIs | sì | feed dinamico | eventi, delegation, storage, form |
| Asincronia | sì | caricamento dati | Promise, async/await, fetch |
| HTTP | sì, approfondito | contratto client/server | request/response, metodi, status, header, cookie, cache, CORS, HTTPS concettuale |
| REST/API design | sì | API Feisbuc | resource modelling, error model, validation |
| Node.js | sì | backend principale | runtime, moduli, npm, env, server HTTP minimo |
| Express | sì | API/SSR | routing, Router, middleware, error handling, static, CORS, auth |
| SQL | integrazione col corso SQL | persistenza | SQL raw prima dell'ORM |
| ORM Node | sì, tecnologia TBD | persistenza evoluta | confronto Drizzle / Prisma / Sequelize |
| Auth e sicurezza web | sì | login/sessione | password hashing, authn/authz, XSS/CSRF/SQLi, secret, cookie |
| Template/SSR | sì, compatto | confronto architetturale | mantenere Nunjucks o equivalente come passaggio concettuale |
| Framework frontend | sì, tecnologia TBD | SPA Feisbuc | candidato Vue 3; confronto con React da decidere |
| SPA e routing | sì | client completo | componenti, stato, form, REST |
| WebSocket/realtime | sì | live feed/chat/notifiche | WebSocket concettuale + Socket.IO applicativo |
| FastAPI mirror track | sì, mirato | API alternativa | stesso contratto HTTP, non doppio corso |
| OpenAPI | sì | documentazione API | particolarmente naturale nel mirror FastAPI |
| SQLAlchemy | sì nel mirror Python | persistenza Python | mapping SQL ↔ ORM |
| Testing/debugging | sì | test Feisbuc | CSS debugging avviato con Activity D; più avanti unit/API/integration |
| Deployment | sì | release finale | env, build, log, HTTPS/reverse proxy concettuali |
| Capstone | sì | Feisbuc | milestone progressive e prodotto finale |
| TypeScript | da decidere | eventuale fase avanzata | breve core o track advanced |
| Senior track | no, previsto | prosecuzione futura | architecture, perf, cache/queue, observability, CI/CD, scaling |

## Stato Activity rappresentative Content Pack v1

- [x] A — osservazione/modifica controllata: `tpsi5-activity-a-html-anatomy-001`;
- [x] B — modifica controllata + milestone Feisbuc: `tpsi5-activity-b-feisbuc-semantic-001`;
- [x] C — implementazione autonoma: `tpsi5-activity-c-feisbuc-responsive-layout-001`;
- [x] D — debug/diagnosi: `tpsi5-activity-d-debug-responsive-css-001`;
- [ ] E/F — mini-progetto/prodotto integrato.

## Gate prima del freeze del curriculum

1. audit completo di `html_css_summary`, `labs_summary` e `feisbuc`;
2. scelta framework frontend;
3. scelta ORM Node;
4. scelta profondità TypeScript;
5. definizione del confine col corso SQL separato;
6. calendario/UDA definitivo dopo verifica delle ore reali disponibili;
7. completare almeno una Activity E/F; A-D sono ora rappresentate nel corso.
