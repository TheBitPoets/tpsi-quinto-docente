import hashlib
from pathlib import Path
from scripts.build_evidence import build

def test_evidence_is_deterministic_and_checksummed(tmp_path):
    a=tmp_path/"a"; b=tmp_path/"b"; build(a,"abc123"); build(b,"abc123")
    for name in ("manifest.json","openapi.json","SHA256SUMS.txt"):
        assert (a/name).read_bytes()==(b/name).read_bytes()
    checks={}
    for line in (a/"SHA256SUMS.txt").read_text().splitlines():
        digest,name=line.split("  ",1); checks[name]=digest
    for name in ("manifest.json","openapi.json"):
        assert hashlib.sha256((a/name).read_bytes()).hexdigest()==checks[name]
    manifest=(a/"manifest.json").read_text()
    for forbidden in (str(tmp_path),"sqlite:///","127.0.0.1",":8000","timestamp","pid"):
        assert forbidden.lower() not in manifest.lower()
