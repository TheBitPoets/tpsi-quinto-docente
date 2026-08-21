from __future__ import annotations
import json, os, socket, subprocess, sys, tempfile, time
from pathlib import Path
from urllib.request import urlopen

def get_json(url):
    with urlopen(url, timeout=1.0) as response:
        return response.status, json.loads(response.read())

def main():
    with tempfile.TemporaryDirectory() as td:
        db=Path(td)/"live.db"
        env=os.environ.copy(); env.update({"FEISBUC_ENV":"test","FEISBUC_DATABASE_URL":f"sqlite:///{db.as_posix()}","FEISBUC_BUILD_SHA":"live-probe"})
        subprocess.run([sys.executable,"-m","app.prepare"],check=True,env=env)
        with socket.socket() as s:
            s.bind(("127.0.0.1",0)); port=s.getsockname()[1]
        proc=subprocess.Popen([sys.executable,"-m","uvicorn","app.main:app","--host","127.0.0.1","--port",str(port),"--workers","1"],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            deadline=time.monotonic()+12
            while True:
                if proc.poll() is not None: raise RuntimeError(f"uvicorn exited early: {proc.returncode}")
                try:
                    status, body=get_json(f"http://127.0.0.1:{port}/health")
                    if status==200: break
                except Exception:
                    pass
                if time.monotonic()>deadline: raise TimeoutError("uvicorn health deadline exceeded")
                time.sleep(0.1)
            assert body=={"status":"ok","build":"live-probe"}
            assert get_json(f"http://127.0.0.1:{port}/ready")[0]==200
            status, posts=get_json(f"http://127.0.0.1:{port}/api/posts"); assert status==200 and posts[0]["id"]=="seed-1"
            print("live-process-probe: PASS")
        finally:
            proc.terminate()
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill(); proc.wait(timeout=5)

if __name__=="__main__": main()
