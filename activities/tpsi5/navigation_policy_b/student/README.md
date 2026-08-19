# Activity B — Navigation policy

Modella la decisione prima di collegarla a Vue Router.

| Route | requiresAuth | authStatus | Decisione |
| --- | --- | --- | --- |
| about | false | unknown | allow |
| feed | true | unknown | resolve-auth |
| login | false | unknown | resolve-auth |
| feed | true | anonymous | redirect login + fullPath |
| login | false | authenticated | redirect feed |
| feed | true | authenticated | allow |
| login | false | anonymous | allow |

Domanda chiave: **perche `unknown` non e uguale a `anonymous`?**

Il file deve leggere un JSON da stdin e stampare un solo JSON su stdout.
