const STORAGE_KEY = "feisbuc.posts";

export function savePosts(posts) {
  // TODO: localStorage conserva stringhe.
  // Serializza posts con JSON.
}

export function loadPosts() {
  // TODO:
  // - se la chiave manca, restituisci [];
  // - prova a fare JSON.parse;
  // - se il valore non e un array o il JSON e corrotto, restituisci [];
  return [];
}
