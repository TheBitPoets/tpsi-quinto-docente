const STORAGE_KEY = "feisbuc.posts";

export function savePosts(posts) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(posts));
    return true;
  } catch (error) {
    console.error("Impossibile salvare i post", error);
    return false;
  }
}

export function loadPosts() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return [];
    }

    const value = JSON.parse(raw);
    return Array.isArray(value) ? value : [];
  } catch (error) {
    console.error("Storage Feisbuc non leggibile", error);
    return [];
  }
}
