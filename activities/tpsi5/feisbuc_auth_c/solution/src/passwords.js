import {
  randomBytes,
  scrypt,
  timingSafeEqual,
} from "node:crypto";
import { promisify } from "node:util";

const derive = promisify(scrypt);
const KEY_LENGTH = 32;
const COST = 2 ** 14;
const BLOCK_SIZE = 8;
const PARALLELIZATION = 5;
const MAXMEM = 64 * 1024 * 1024;

const options = {
  cost: COST,
  blockSize: BLOCK_SIZE,
  parallelization: PARALLELIZATION,
  maxmem: MAXMEM,
};

export async function hashPassword(password) {
  const salt = randomBytes(16);
  const key = await derive(password, salt, KEY_LENGTH, options);
  return [
    "scrypt",
    COST,
    BLOCK_SIZE,
    PARALLELIZATION,
    salt.toString("base64url"),
    Buffer.from(key).toString("base64url"),
  ].join("$");
}

export async function verifyPassword(password, encoded) {
  const parts = String(encoded ?? "").split("$");
  if (parts.length !== 6 || parts[0] !== "scrypt") return false;

  const [, rawCost, rawBlock, rawParallel, rawSalt, rawHash] = parts;
  const cost = Number(rawCost);
  const blockSize = Number(rawBlock);
  const parallelization = Number(rawParallel);
  if (![cost, blockSize, parallelization].every(Number.isSafeInteger)) return false;

  const salt = Buffer.from(rawSalt, "base64url");
  const expected = Buffer.from(rawHash, "base64url");
  if (salt.length < 16 || expected.length !== KEY_LENGTH) return false;

  const actual = Buffer.from(await derive(password, salt, expected.length, {
    cost,
    blockSize,
    parallelization,
    maxmem: MAXMEM,
  }));

  return actual.length === expected.length && timingSafeEqual(actual, expected);
}

export const PASSWORD_KDF = Object.freeze({
  algorithm: "scrypt",
  cost: COST,
  blockSize: BLOCK_SIZE,
  parallelization: PARALLELIZATION,
  keyLength: KEY_LENGTH,
});
