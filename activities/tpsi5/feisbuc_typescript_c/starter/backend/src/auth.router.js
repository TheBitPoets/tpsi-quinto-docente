import { Router } from "express";
import { HttpError } from "./http-errors.js";
import { requireJson } from "./middleware.js";
import { hashPassword, verifyPassword } from "./passwords.js";
import {
  clearSessionCookie,
  createSessionToken,
  hashSessionToken,
  requireAuth,
  setSessionCookie,
} from "./session.js";
import { validateLogin, validateRegistration } from "./auth-validation.js";

const DUMMY_HASH = "scrypt$16384$8$5$AAAAAAAAAAAAAAAAAAAAAA$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";

const registrationMessage = (errors) => ({
  code: "registration-invalid",
  message: `Registrazione non valida: ${errors.join(", ")}`,
});

export function createAuthRouter({ authStore, config }) {
  const router = Router();

  const issueSession = (res, user) => {
    const token = createSessionToken();
    const idHash = hashSessionToken(token);
    const now = Date.now();
    authStore.createSession({
      idHash,
      userId: user.id,
      createdAt: now,
      expiresAt: now + config.sessionTtlMs,
    });
    setSessionCookie(res, token, config);
  };

  router.post("/register", requireJson, async (req, res) => {
    const checked = validateRegistration(req.body);
    if (!checked.ok) {
      const error = registrationMessage(checked.errors);
      throw new HttpError(400, error.code, error.message);
    }

    const { email, displayName, password } = checked.value;
    if (authStore.findCredentialByEmail(email)) {
      throw new HttpError(409, "email-already-registered", "Email gia registrata.");
    }

    const passwordHash = await hashPassword(password);
    const user = authStore.createUser({ email, displayName, passwordHash });
    issueSession(res, user);
    res.status(201).json({ user });
  });

  router.post("/login", requireJson, async (req, res) => {
    const checked = validateLogin(req.body);
    const credentials = checked.ok
      ? authStore.findCredentialByEmail(checked.value.email)
      : null;
    const candidateHash = credentials?.passwordHash ?? DUMMY_HASH;
    const password = checked.ok ? checked.value.password : "invalid-login-attempt";
    const matches = await verifyPassword(password, candidateHash);

    if (!checked.ok || !credentials || !matches) {
      throw new HttpError(401, "invalid-credentials", "Credenziali non valide.");
    }

    issueSession(res, credentials.user);
    res.status(200).json({ user: credentials.user });
  });

  router.get("/me", requireAuth, (req, res) => {
    res.status(200).json({ user: req.auth.user });
  });

  router.post("/logout", (req, res) => {
    if (req.auth?.sessionHash) authStore.deleteSession(req.auth.sessionHash);
    clearSessionCookie(res, config);
    res.status(204).end();
  });

  return router;
}
