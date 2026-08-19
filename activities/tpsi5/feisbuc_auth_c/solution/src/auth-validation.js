const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function normalizeEmail(value) {
  return typeof value === "string" ? value.trim().toLowerCase() : "";
}

export function validateRegistration(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return { ok: false, errors: ["body-invalid"] };
  }

  const email = normalizeEmail(input.email);
  const displayName = typeof input.displayName === "string" ? input.displayName.trim() : "";
  const password = typeof input.password === "string" ? input.password : "";
  const errors = [];

  if (!EMAIL_RE.test(email)) errors.push("email-invalid");
  if (Array.from(displayName).length < 1 || Array.from(displayName).length > 80) {
    errors.push("display-name-invalid");
  }
  const length = Array.from(password).length;
  if (length < 15) errors.push("password-too-short");
  if (length > 128) errors.push("password-too-long");

  return errors.length
    ? { ok: false, errors }
    : { ok: true, value: { email, displayName, password } };
}

export function validateLogin(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return { ok: false };
  }
  const email = normalizeEmail(input.email);
  const password = typeof input.password === "string" ? input.password : "";
  if (!EMAIL_RE.test(email) || !password) return { ok: false };
  return { ok: true, value: { email, password } };
}
