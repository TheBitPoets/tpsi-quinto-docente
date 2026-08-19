# Note docente — auth security review

Valutare il **ragionamento**, non la quantità di parole.

Finding minimi attesi:

1. password plaintext;
2. enumerazione email;
3. session ID = user id;
4. cookie privo di attributi;
5. password/sessionId restituiti al JS;
6. autore scelto dal client;
7. delete autorizzata con dati scelti dal client;
8. nessuna expiry/revoca server-side.

Chiedere sempre evidence: query DB, header `Set-Cookie`, due utenti distinti, vecchio cookie dopo logout, request cross-site simulata.

Non accettare `usa JWT` come risposta sufficiente: JWT non corregge automaticamente password storage, cookie scope, CSRF o authorization.
