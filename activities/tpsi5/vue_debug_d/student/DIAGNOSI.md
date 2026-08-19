# Diagnosi

Per ogni problema indica: **sintomo → causa → fix → evidence**.

1. Il titolo non segue eventuali modifiche di `state.title`.
2. Il contatore post resta vecchio dopo `addPost()`.
3. Il child modifica direttamente `post.liked`.
4. L'evento non raggiunge il listener atteso dal parent.
5. La lista usa una key non legata all'identita del post.
