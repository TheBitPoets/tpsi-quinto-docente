# Activity B — Navigation policy TypeScript

La logica deve restare equivalente alla milestone 10.

| Route | requiresAuth | authStatus | Decision |
| --- | --- | --- | --- |
| about | false | unknown | allow |
| login | false | unknown | resolve-auth |
| feed | true | unknown | resolve-auth |
| feed | true | anonymous | redirect login + fullPath |
| feed | true | authenticated | allow |
| login | false | authenticated | redirect feed |

## Domande

1. Perche `NavigationDecision` e una discriminated union invece di un oggetto con campi opzionali generici?
2. Cosa impedisce `RouteName`?
3. Cosa impedisce `AuthStatus`?
4. Perche la funzione non importa Vue Router?
5. Quale errore diventerebbe possibile usando `string` al posto di `RouteName`?

## Definition of done

- `npm run type-check` verde;
- nessun `any`;
- la semantica della matrice e rispettata;
- la policy resta pura e riutilizzabile.
