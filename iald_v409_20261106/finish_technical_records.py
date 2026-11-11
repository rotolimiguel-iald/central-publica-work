"""Scope reconciliation and local memory deposit, separate from final acceptance."""
import json
import hashlib
import subprocess
from pathlib import Path
import task
W = Path(__file__).resolve().parent
def pin(p): return {'path': str(p), 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}
opinion_path = W / 'review/VERIFY_SCOPE_OPINION_R2.json'
opinion = json.loads(opinion_path.read_bytes())
assert opinion['status'] == 'FAVORABLE_TO_EXPLICIT_TECHNICAL_SCOPE_AMENDMENT'
if not (W / 'VERIFY_SCOPE_AMENDMENT.json').exists():
    result = task.act('amend', task_id='verify', criterion=opinion['criterion_proposed'],
                      reason='Align inherited verification template to ORDEM_009 technical release scope and no paid generation; explicitly preserve absent live/physical checks as limitations, not success.',
                      sources=[pin(opinion_path), pin(Path(r'C:\IALD\TUNEL_CLAUDE_APP\ORDEM_009_release_v409_do_app.md'))],
                      event_id='v409-verify-technical-scope-explicit-amend')
    task.new('VERIFY_SCOPE_AMENDMENT.json', result)
if (W / 'MEMORY_DELIVERY_RECEIPT.json').exists():
    raise RuntimeError('Existing deposit receipt: inspect before any new deposit')
command = [r'C:\Python314\python.exe', '-B', '-X', 'utf8',
           r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\memoria.py',
           'depositar', '--quem', task.OWNER, '--tipo', 'project', '--estatuto', 'REAL',
           '--alvo', 'app-ciencia-propria-v395-24out.md', '--casa', 'IALD Nativa',
           '--fonte', str(W / 'TECHNICAL_DELIVERY_R1.json'),
           '--fonte', str(W / 'INSTALLED_VERIFICATION.json'),
           '--texto-arquivo', str(W / 'MEMORY_DEPOSIT_v409.md'), '--slug', 'app-v409-ativado-06nov']
p = subprocess.run(command, capture_output=True, text=True, encoding='utf8')
if p.returncode:
    task.new('MEMORY_DELIVERY_FAILURE.json', {'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
    raise RuntimeError('Memory deposit failed; receipt preserved')
receipt = json.loads(p.stdout)
task.new('MEMORY_DELIVERY_RECEIPT.json', receipt)
print(json.dumps({'deposit_returncode': p.returncode, 'receipt': receipt}, ensure_ascii=False))
