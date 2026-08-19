# Osservazioni Vue Router

Non modificare il codice finche non hai raccolto le evidenze.

## 1. RouterLink

- URL prima del click:
- URL dopo il click:
- La pagina ha fatto un reload completo? Quale evidenza usi?

## 2. RouterView

- Quale componente viene mostrato su `/`?
- Quale componente viene mostrato su `/feed`?
- Cosa resta invariato nel layout?

## 3. History

Naviga `Home -> Feed -> Home`, poi usa Back e Forward.

- Sequenza osservata:
- Perche questo comportamento e coerente con la History API?

## 4. 404 client-side

Apri `/inesistente` usando il link fornito.

- Quale route record intercetta la location?
- Il risultato e un 404 HTTP oppure una view 404 della SPA?

## 5. Deep link

Con `npm run dev`, prova ad aprire direttamente `/feed` nella barra degli indirizzi. Poi spiega cosa dovra fare **Express in produzione** quando la build e montata sotto `/vue/`.

- comportamento dev:
- requisito server production:
- differenza tra server fallback e catch-all client:
