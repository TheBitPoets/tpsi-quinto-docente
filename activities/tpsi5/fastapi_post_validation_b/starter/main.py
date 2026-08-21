import json
import sys


def normalize_post_text(value):
    # TODO: string only -> strip -> required -> max 280
    raise NotImplementedError


def main() -> None:
    payload = json.loads(sys.stdin.read())
    result = normalize_post_text(payload.get("text"))
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
