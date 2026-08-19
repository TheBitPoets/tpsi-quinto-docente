# Diagnosi di riferimento SSR

| Finding | Sintomo/rischio | Trust boundary | Fix | Evidence |
| --- | --- | --- | --- | --- |
| `post.text | safe` | markup utente diventa HTML eseguibile/XSS | input utente -> template | rimuovere `safe`, mantenere autoescape | stringa `<script>` appare come testo escapato |
| delete soltanto nascosta ai non-owner | un client puo chiamare direttamente la route | UI non e authorization | `deleteOwned(id, req.auth.user.id)` | secondo utente riceve 403 |
| delete via GET | link/crawler/prefetch puo mutare stato | semantica HTTP | form POST dedicato o REST DELETE | GET non modifica il DB |
| create -> 200 HTML | refresh puo proporre/resubmit della POST | navigation after mutation | `res.redirect(303, "/ssr")` | Network mostra POST 303 + GET 200 |
| cookie/secret nel template context | secret puo finire nel markup/log/debug | server secret -> presentation | view model minimo | HTML non contiene token/cookie |
| authorId dal body | impersonation | client input -> identity | usare `req.auth.user.id` | body spoofed non cambia autore |
