import { computed, readonly, ref } from "vue";
import { api, ApiError } from "./api.js";

const userState = ref(null);
const statusState = ref("unknown");
const loadingState = ref(false);

async function ensureKnown() {
  if (statusState.value !== "unknown") return statusState.value;
  loadingState.value = true;
  try {
    const payload = await api.me();
    userState.value = payload.user;
    statusState.value = "authenticated";
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      userState.value = null;
      statusState.value = "anonymous";
    } else {
      throw error;
    }
  } finally {
    loadingState.value = false;
  }
  return statusState.value;
}

async function login(credentials) {
  loadingState.value = true;
  try {
    userState.value = (await api.login(credentials)).user;
    statusState.value = "authenticated";
    return userState.value;
  } finally {
    loadingState.value = false;
  }
}

async function register(credentials) {
  loadingState.value = true;
  try {
    userState.value = (await api.register(credentials)).user;
    statusState.value = "authenticated";
    return userState.value;
  } finally {
    loadingState.value = false;
  }
}

async function logout() {
  loadingState.value = true;
  try {
    await api.logout();
    userState.value = null;
    statusState.value = "anonymous";
  } finally {
    loadingState.value = false;
  }
}

function markAnonymous() {
  userState.value = null;
  statusState.value = "anonymous";
}

export const session = {
  user: readonly(userState),
  status: readonly(statusState),
  loading: readonly(loadingState),
  loggedIn: computed(() => statusState.value === "authenticated"),
  ensureKnown,
  login,
  register,
  logout,
  markAnonymous,
};

export function useSession() {
  return session;
}
