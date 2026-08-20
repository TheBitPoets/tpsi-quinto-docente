import { computed, readonly, ref } from "vue";
import { api, ApiError } from "./api";
import type {
  AuthStatus,
  LoginCredentials,
  RegistrationCredentials,
  User,
} from "./domain";

const userState = ref<User | null>(null);
const statusState = ref<AuthStatus>("unknown");
const loadingState = ref(false);

async function ensureKnown(): Promise<AuthStatus> {
  if (statusState.value !== "unknown") return statusState.value;
  loadingState.value = true;
  try {
    const payload = await api.me();
    userState.value = payload.user;
    statusState.value = "authenticated";
  } catch (error: unknown) {
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

async function login(credentials: LoginCredentials): Promise<User> {
  loadingState.value = true;
  try {
    const user = (await api.login(credentials)).user;
    userState.value = user;
    statusState.value = "authenticated";
    return user;
  } finally {
    loadingState.value = false;
  }
}

async function register(credentials: RegistrationCredentials): Promise<User> {
  loadingState.value = true;
  try {
    const user = (await api.register(credentials)).user;
    userState.value = user;
    statusState.value = "authenticated";
    return user;
  } finally {
    loadingState.value = false;
  }
}

async function logout(): Promise<void> {
  loadingState.value = true;
  try {
    await api.logout();
    userState.value = null;
    statusState.value = "anonymous";
  } finally {
    loadingState.value = false;
  }
}

function markAnonymous(): void {
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
