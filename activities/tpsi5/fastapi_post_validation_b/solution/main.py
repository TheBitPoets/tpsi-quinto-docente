import json
import sys


def normalize_post_text(value):
    if not isinstance(value, str):
        return {"ok": False, "error": "post-text-required"}
    text = value.strip()
    if not text:
        return {"ok": False, "error": "post-text-required"}
    if len(text) > 280:
        return {"ok": False, "error": "post-text-too-long"}
    return {"ok": True, "text": text}


def main() -> None:
    payload = json.loads(sys.stdin.read())
    result = normalize_post_text(payload.get("text"))
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
