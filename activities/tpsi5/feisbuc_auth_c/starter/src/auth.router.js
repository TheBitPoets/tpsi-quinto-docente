import { Router } from "express";
import { HttpError } from "./http-errors.js";
import { requireJson } from "./middleware.js";
import { hashPassword, verifyPassword } from "./passwords.js";
import { requireAuth } from "./session.js";
import { validateLogin, validateRegistration } from "./auth-validation.js";

export function createAuthRouter({ authStore, config }) {
  const router = Router();

  router.post("/register", requireJson, async (req, res) => {
    const checked = validateRegistration(req.body);
    if (!checked.ok) throw new HttpError(400, "registration-invalid", "Registrazione non valida.");
    // TODO: duplicate check -> hashPassword -> createUser -> nuova sessione -> cookie.
    throw new Error("TODO register");
  });

  router.post("/login", requireJson, async (req, res) => {
    const checked = validateLogin(req.body);
    // TODO: generic invalid-credentials, verifyPassword e nuova sessione.
    void checked;
    void verifyPassword;
    throw new Error("TODO login");
  });

  router.get("/me", requireAuth, (req, res) => {
    res.status(200).json({ user: req.auth.user });
  });

  router.post("/logout", (req, res) => {
    // TODO: invalida DB session e cancella cookie con lo stesso scope.
    res.status(501).json({ error: { code: "TODO", message: "Completa logout." } });
  });

  void authStore;
  void config;
  void hashPassword;
  return router;
}
