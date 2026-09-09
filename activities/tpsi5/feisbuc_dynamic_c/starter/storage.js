const STORAGE_KEY = "feisbuc.posts";

export function savePosts(posts) {
  // TODO: localStorage conserva stringhe.
  // Serializza posts con JSON dentro try/catch.
  // Restituisci true se il salvataggio riesce, false in caso di errore.
  return false;
}

export function loadPosts() {
  // TODO:
  // - se la chiave manca, restituisci [];
  // - prova a fare JSON.parse;
  // - se il valore non è un array o il JSON è corrotto, restituisci [];
  return [];
}
