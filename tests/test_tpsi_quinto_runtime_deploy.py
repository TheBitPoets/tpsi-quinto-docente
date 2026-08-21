from __future__ import annotations
import hashlib, json, os, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'content/tpsi5/content-pack.json'
DESIGN=ROOT/'doc/course_designs/tpsi_quinto_2026_2027.json'
LESSON=ROOT/'content/tpsi5/18_RUNTIME_DEPLOY_HEALTH_CAPSTONE.md'
A=ROOT/'activities/tpsi5/runtime_deploy_microscope_a'
B=ROOT/'activities/tpsi5/runtime_config_contract_b'
C=ROOT/'activities/tpsi5/health_readiness_c'
D=ROOT/'activities/tpsi5/runtime_debug_d'
E=ROOT/'activities/tpsi5/evidence_bundle_e'
F=ROOT/'activities/tpsi5/feisbuc_runtime_capstone_f'

def load(path): return json.loads(path.read_text(encoding='utf-8'))

def test_closeout_registered_and_week_budget_unchanged():
    pack=load(PACK); design=load(DESIGN)
    assert pack['version']=='1.0.0'
    item=next(x for x in pack['content_items'] if x['id']=='tpsi5-content-runtime-deploy-capstone')
    assert item['order']==19 and item['path']==str(LESSON.relative_to(ROOT)).replace('\\','/')
    assert item['activity_ids']==[
        'tpsi5-activity-a-runtime-deploy-microscope-001','tpsi5-activity-b-runtime-config-contract-001','tpsi5-activity-c-health-readiness-001','tpsi5-activity-d-debug-runtime-deploy-001','tpsi5-activity-e-evidence-bundle-001','tpsi5-activity-f-feisbuc-runtime-capstone-001']
    uda=next(x for x in design['years'][0]['udas'] if x['id']=='uda-26')
    assert uda['weeks']=='4'
    assert [x['source'] for x in uda['items']]==[
        'content/tpsi5/15_FASTAPI_OPENAPI_MIRROR.md','content/tpsi5/16_SQLALCHEMY_PERSISTENCE_MIRROR.md','content/tpsi5/17_TESTING_INTEGRATION_BOUNDARIES.md','content/tpsi5/18_RUNTIME_DEPLOY_HEALTH_CAPSTONE.md']
    assert design['years'][0]['weeks']==33 and sum(int(x['weeks']) for x in design['years'][0]['udas'])==33

def test_activity_b_is_real_python_autograding_contract():
    activity=load(B/'activity.json')
    assert activity['correzione']=={'compila':False,'test':True,'sandbox':True,'ai_feedback':False}
    assert len(activity['test_cases'])==5
    solution=B/'solution/main.py'
    source=solution.read_text(); assert 'fastapi' not in source.lower() and 'sqlalchemy' not in source.lower() and 'uvicorn' not in source.lower()
    for case in activity['test_cases']:
        result=subprocess.run([sys.executable,str(solution)],input=case['stdin'],text=True,capture_output=True,timeout=10)
        assert result.returncode==0, result.stderr
        assert result.stdout.strip()==case['expected_stdout']

def test_runtime_capstone_reference_contract_and_evidence():
    solution=F/'solution'
    source=(solution/'app/main.py').read_text()
    assert '@app.get("/health")' in source and '@app.get("/ready")' in source
    health=source.split('@app.get("/health")',1)[1].split('@app.get("/ready")',1)[0]
    assert 'session_factory' not in health and 'PostRow' not in health
    assert 'Base.metadata.create_all' not in source
    prepare=(solution/'app/prepare.py').read_text(); assert 'Base.metadata.create_all' in prepare and 'ensure_seed' in prepare
    settings=(solution/'app/settings.py').read_text(); assert 'production' in settings and 'FEISBUC_DATABASE_URL is required' in settings
    runbook=(solution/'RUNBOOK.md').read_text(); assert 'python -m app.prepare' in runbook and '--workers 1' in runbook and '--reload' in runbook  # deliberate limit sentence
    probe=(solution/'tests/probe_live.py').read_text(); assert 'subprocess.Popen' in probe and 'time.monotonic()' in probe and 'proc.terminate()' in probe
    evidence=(solution/'scripts/build_evidence.py').read_text(); assert 'SHA256SUMS.txt' in evidence and 'sort_keys=True' in evidence

def test_capstone_pytest_reference_passes():
    result=subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=F/'solution',capture_output=True,text=True,timeout=90)
    assert result.returncode==0, result.stdout+result.stderr
    assert 'passed' in result.stdout

def test_live_uvicorn_probe_passes():
    result=subprocess.run([sys.executable,'tests/probe_live.py'],cwd=F/'solution',capture_output=True,text=True,timeout=30)
    assert result.returncode==0, result.stdout+result.stderr
    assert 'live-process-probe: PASS' in result.stdout

def test_evidence_is_deterministic():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        a=Path(td)/'a'; b=Path(td)/'b'
        for out in (a,b):
            r=subprocess.run([sys.executable,'scripts/build_evidence.py','--output',str(out),'--build-sha','abc123'],cwd=F/'solution',capture_output=True,text=True,timeout=30)
            assert r.returncode==0, r.stdout+r.stderr
        for name in ('manifest.json','openapi.json','SHA256SUMS.txt'): assert (a/name).read_bytes()==(b/name).read_bytes()
        manifest=(a/'manifest.json').read_text().lower()
        for forbidden in (td.lower(),'sqlite:///','127.0.0.1','timestamp','pid'): assert forbidden not in manifest

def test_debug_diagnosis_covers_operational_smells():
    diagnosis=(D/'solution/DIAGNOSI.md').read_text().lower()
    for concept in ('fallback','liveness','readiness','leak','prestart','reload','cleanup'): assert concept in diagnosis
