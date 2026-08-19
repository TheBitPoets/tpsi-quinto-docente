export function validateNewPost(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return { ok: false, error: "body-invalid" };
  }

  const text = typeof input.text === "string" ? input.text.trim() : "";
  if (!text) {
    return { ok: false, error: "text-required" };
  }
  if (text.length > 280) {
    return { ok: false, error: "text-too-long" };
  }

  return { ok: true, value: { text } };
}

export function validateLikePatch(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return { ok: false, error: "body-invalid" };
  }
  if (typeof input.liked !== "boolean") {
    return { ok: false, error: "liked-required" };
  }
  return { ok: true, value: { liked: input.liked } };
}
