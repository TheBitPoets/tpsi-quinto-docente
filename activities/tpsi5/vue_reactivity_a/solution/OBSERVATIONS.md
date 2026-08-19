# Osservazioni attese

1. Nello script `count`, `step` e gli altri ref usano `.value`; nel template Vue effettua l'unwrapping.
2. `doubled` viene ricalcolato quando cambia la dipendenza reattiva `count`.
3. Un secondo state manuale introdurrebbe due fonti da sincronizzare; `computed` esprime una relazione derivata.
4. `v-model.number` collega valore dell'input, evento di input e conversione numerica; il modello sottostante resta quello gia studiato nel DOM.
5. DOM manuale: leggi state -> aggiorna textContent/input -> listener modifica state -> richiama render.
