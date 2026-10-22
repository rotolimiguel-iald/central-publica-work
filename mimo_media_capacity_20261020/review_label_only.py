"""Coordinator's distinct technical review of Hypatia's one-constant edit."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
D=W/'client_stage/media_label_R8'
old="const MEDIA_LIMIT_TEXT = 'Áudio/vídeo: até 50 MB em base64 (aproximadamente 37,5 MB de arquivo). O servidor verifica o contexto preservando a memória TGL; não há limite fixo de duração.';".encode()
new="const MEDIA_LIMIT_TEXT = 'Áudio e vídeo: até 37,5 MB por arquivo. A duração disponível depende do contexto da conversa; a memória da TGL é preservada.';".encode()
def digest(raw):return hashlib.sha256(raw).hexdigest()
def write(path,value):
    raw=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False,indent=2).encode()
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(raw)
    assert path.read_bytes()==raw
planraw=(D/'install_plan_LABEL_R8.json').read_bytes()
plan=json.loads(planraw)
assert len(plan['files'])==4
hashes=set()
for item in plan['files']:
    before=Path(item['destination']).read_bytes();after=Path(item['source']).read_bytes()
    assert digest(before)==item['baseline'] and digest(after)==item['sha256']
    assert before.count(old)==1 and before.replace(old,new,1)==after
    hashes.add(digest(after))
assert len(hashes)==1
for item in json.loads((W/'SCIENCE_BASELINE.json').read_bytes())['files']:
    assert digest(Path(item['path']).read_bytes())==item['sha256']
write(D/'install_plan.json',planraw)
for name in ('transaction.py','maintenance.py','deploy_controlled.py'):
    write(D/name,(W/name).read_bytes())
review=dict(status='PASS',actor='codex-app-01a094df',producer='Hypatia',
 scope='Distinct coordinator review: exactly one display constant changed in each of four identical assets; all other bytes and logic identical. No final mission acceptance implied.',
 plan_sha256=digest(planraw),transaction_sha256=digest((D/'transaction.py').read_bytes()),
 maintenance_sha256=digest((D/'maintenance.py').read_bytes()),files=4,
 input_limits_changed=False,science_preserved=True,provider_calls=0)
write(D/'validation/final_checks.json',dict(passed=True,plan_sha256=digest(planraw),text_only=True))
write(D/'validation/review_final.json',review)
print('PASS distinct text-only review; no runtime changes')
