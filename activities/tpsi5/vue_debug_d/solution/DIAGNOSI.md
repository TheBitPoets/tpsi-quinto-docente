# Diagnosi attesa

1. `const { title } = state` copia la primitive e perde il collegamento reattivo; usare `state.title` o `toRef(state,'title')`.
2. `postCount` e inizializzato una volta; e stato derivato e va espresso con `computed(() => posts.value.length)`.
3. Il child muta una prop: viola one-way data flow. Deve emettere un'intenzione e lasciare al parent l'update.
4. Il child dichiara/emette `toggle`, il parent ascolta `toggle-like`: rendere coerente il contratto.
5. `:key="index"` lega identita alla posizione; usare `post.id` stabile.
