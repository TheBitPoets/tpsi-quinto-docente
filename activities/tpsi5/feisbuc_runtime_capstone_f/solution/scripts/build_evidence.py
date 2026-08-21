from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import create_app
from app.settings import RuntimeSettings

def canonical(obj): return (json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()

def build(output: Path, build_sha: str):
    output.mkdir(parents=True,exist_ok=True)
    app=create_app(RuntimeSettings("test","sqlite:///:memory:",build_sha))
    openapi=canonical(app.openapi()); app.state.engine.dispose()
    manifest=canonical({"schema":"thebitlab.capstone-evidence.v1","milestone":"feisbuc-mirror-04-runtime-capstone","contentPack":"1.0.0","buildSha":build_sha,"contracts":["runtime-config","health-liveness","database-readiness","posts-http-contract","restart-persistence","live-uvicorn-process"],"files":["manifest.json","openapi.json","SHA256SUMS.txt"]})
    (output/"manifest.json").write_bytes(manifest); (output/"openapi.json").write_bytes(openapi)
    lines=[]
    for name in ("manifest.json","openapi.json"):
        digest=hashlib.sha256((output/name).read_bytes()).hexdigest(); lines.append(f"{digest}  {name}")
    (output/"SHA256SUMS.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--output",default="evidence"); p.add_argument("--build-sha",default="dev"); a=p.parse_args(); build(Path(a.output),a.build_sha)
if __name__=="__main__": main()
