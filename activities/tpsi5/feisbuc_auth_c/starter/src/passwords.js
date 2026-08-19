import { scrypt } from "node:crypto";
import { promisify } from "node:util";

const derive = promisify(scrypt);

export async function hashPassword(password) {
  // TODO: random salt + scrypt + formato auto-descrittivo.
  throw new Error("TODO hashPassword");
}

export async function verifyPassword(password, encoded) {
  // TODO: parse formato, deriva con gli stessi parametri e usa timingSafeEqual.
  return false;
}
