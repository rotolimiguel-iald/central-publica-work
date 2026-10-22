"""Commit one memory update for the reviewed repair and the live third run."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'r'
PARENT=ROOT/'runtime_formal_stage_custody.json'
OUT=ROOT/'runtime_reader_correction_custody.json'
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MARKER='TETELESTAI_V350_LEITORES_CORRIGIDOS_RODADA03_20260913'
REVIEW=ROOT/'revisao/REVIEW_READER_CORRECTION_V2.md'
ROUND_REVIEW=ROOT/'revisao/REVIEW_FULL_RUNTIME_ROUND02_AND_REGRESSIONS.md'

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def encoded(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def atomic(path,raw):
    temp=path.with_name(path.name+'.tmp_'+STAMP)
    with temp.open('xb') as stream:stream.write(raw)
    assert temp.read_bytes()==raw
    os.replace(temp,path)
    assert path.read_bytes()==raw

assert not OUT.exists()
parent=json.loads(PARENT.read_bytes())
integration=json.loads((RUN/'reader_integration_manifest.json').read_bytes())
state=json.loads((RUN/'runtime_process_03.json').read_bytes())
prior=json.loads((RUN/'completed_attempt_02/verification.json').read_bytes())
assert state['status']=='RUNNING'
assert sha(ROOT/'um.py')==sha(RUN/'um.py')==integration['working_sha256']==state['working_sha256']
assert integration['review_sha256']==sha(REVIEW)
assert 'Nenhum P0–P2 pendente' in REVIEW.read_text(encoding='utf-8')
assert prior['selftest']=='FAIL_CLOSED_SELFTEST_PASSED'
original=Path(json.loads((ROOT/'environment.json').read_bytes())['original_source'])
original_hash=sha(original)
assert original_hash==parent['original_sha256']

surfaces=[Path(name) for name in parent['surface_sha256']]
extras=[ROOT/'RELATORIO_EXECUCAO_INTEGRAL.md',ROOT/'RUNTIME_ATIVO.json',ROOT/'CONTRATO_ATIVO_GATE_V350.json']
before={path:path.read_bytes() for path in surfaces+extras}
for path in surfaces:
    assert sha(path)==parent['surface_sha256'][str(path)]
    assert MARKER.encode() not in before[path]
note=f'''

## {MARKER} — {datetime.now().astimezone().isoformat(timespec='seconds')}

[REAL] A rodada 02 terminou rc0 em 13/09/2026 às 10:08:08 BRT. As onze entradas
do gate reproduziram o terminal existente; autoteste FAIL_CLOSED_SELFTEST_PASSED;
13 hashes do selo conferidos e 922 fontes formais restauradas. O Audit explícito
contém 7.133 nomes; a união build+Audit contém 7.985, igual ao JSON e manifesto.
O primeiro teste autoral que igualava essas contagens falhou por escopos distintos;
a correção foi no teste, sem alterar o parser. A rodada e as recusas efetivamente
emitidas foram preservadas byte a byte em r/completed_attempt_02 (46 arquivos).

[REAL — correção de ligação] A revisão identificou duas checagens históricas:
montagem exigia exatamente 7/8 apesar de medir 8/8; Atlas exigia todas as flags
qgf/gpf apagadas apesar de suas doze entradas próprias estarem provadas. Somente
essas duas funções existentes foram corrigidas. A montagem reutiliza a guarda
de termo + ponte de tipo exato já existente. Atlas conserva flags alheias como
diagnóstico. Nenhuma função ou prova Lean foi adicionada, nenhum contrato ou
condição do gate foi alterado. 38 regressões autorais; 39 verificações do revisor,
incluindo o quarto insumo; nenhum P0–P2 no candidato aceito.
[Parecer do patch](<{REVIEW.as_posix()}>).
[Parecer da rodada anterior](<{ROUND_REVIEW.as_posix()}>).

[REAL — insumos] Dois catálogos REVOLVER, documento Stokes e results.json já
existiam no acervo, mas não na preparação da cópia. Os quatro foram copiados e
conferidos por hash. Não se mudou limiar nem resultado experimental. A primeira
tentativa de iniciar o Python científico foi negada pelo sandbox antes de criar
processo; as capturas vazias foram preservadas. O lançamento autorizado seguinte
iniciou a rodada 03 em {state['started']}, PID {state['pid']}, sessão 76735.

[EM CURSO] Programa corrigido SHA256 {integration['working_sha256']}.
Rodada 03 usa os mesmos Lean, gate, ambiente e autoteste, agora com quatro insumos
repostos. A rodada anterior não aprova antecipadamente seus resultados. Aguardar
o processo existente; conferir saídas, recusas, selo e autoteste; não reiniciar.
Nenhuma exigência original-S/KMS/UV foi reaberta. O contrato continua consolidar
o conjunto probatório do um.py. Gate principal sem entradas de prova faltantes.
Originais canônicos foram apenas lidos e seu hash permanece {original_hash}.
Objetivo integral permanece pendente da rodada 03 e sua conferência final.
'''.encode('utf-8')
backups={}
for path,raw in before.items():
    backup=path.with_name(path.name+'.bak_'+STAMP)
    with backup.open('xb') as stream:stream.write(raw)
    assert backup.read_bytes()==raw
    backups[str(path)]=str(backup)
for path in surfaces+[extras[0]]:
    assert path.read_bytes()==before[path]
    atomic(path,before[path]+note)
    assert path.read_bytes().startswith(before[path])
locator=json.loads(before[extras[1]])
locator.update(dict(attempt=3,pid_at_start=state['pid'],session_id=76735,
    status='RUNNING_REVIEWED_READER_CORRECTION_WITH_RESTORED_INPUTS',
    process_status_file=str(RUN/'runtime_process_03.json'),
    stdout=str(RUN/'runtime_stdout_03.txt'),stderr=str(RUN/'runtime_stderr_03.txt'),
    custody=str(OUT),previous_completed_run_archive=str(RUN/'completed_attempt_02'),
    previous_completed_run_selftest=prior['selftest'],
    formal_stage_verified=False,formal_stage_independent_review_completed=False,
    reviewed_formal_sources_unchanged=True,full_runtime_result_pending=True,
    working_sha256=integration['working_sha256'],
    remaining_action='Observe existing run03; validate its outputs, auxiliary readers, restored data, seals and selftest. No new proofs.'))
atomic(extras[1],encoded(locator))
contract=json.loads(before[extras[2]])
contract.update(dict(working_sha256=integration['working_sha256'],
    last_integration_correction='Two existing readers corrected; four omitted existing inputs restored; Lean and principal gate unchanged.',
    correction_review=str(REVIEW),last_completed_runtime_archive=str(RUN/'completed_attempt_02'),
    corrected_runtime_pending=True,new_functions_added=0,new_lean_proofs_added=0))
atomic(extras[2],encoded(contract))

# Re-anchor old run-specific artifact references to their immutable archive.
artifacts={}
redirects={}
for name,pin in parent['artifacts'].items():
    path=ROOT/name
    archived=RUN/'completed_attempt_02'/path.name
    if path.parent==RUN and archived.exists() and path.name in integration['cleared_previous_outputs']:
        new_name=archived.relative_to(ROOT).as_posix()
        artifacts[new_name]=sha(archived);redirects[name]=new_name
    elif path.exists():
        artifacts[name]=sha(path)
    else:
        raise FileNotFoundError(str(path))
additions=[Path(__file__),*extras,REVIEW,ROUND_REVIEW,
    ROOT/'reader_correction_v2/verification.json',ROOT/'reader_correction_v2/um.py',
    ROOT/'revisao/reader_candidate_v2_review_20260913_102521_881121/verification.json',
    RUN/'completed_attempt_02/verification.json',RUN/'reader_integration_manifest.json',
    ROOT/'runtime_inputs_pending/manifest.json',ROOT/'runtime_inputs_pending/manifest_results.json',
    ROOT/'run_full_runtime_attempt03.py',ROOT/'install_reviewed_reader_correction.py']
for path in additions:artifacts[path.relative_to(ROOT).as_posix()]=sha(path)
custody=dict(parent)
custody.update(dict(timestamp=datetime.now().astimezone().isoformat(),
    status='REVIEWED_READERS_INTEGRATED__RUN03_RUNNING',
    previous_custody_path=str(PARENT),previous_custody_sha256=sha(PARENT),marker=MARKER,
    working_sha256=integration['working_sha256'],previous_working_sha256=integration['previous_working_sha256'],
    original_sha256=original_hash,original_unchanged=True,
    surface_before_sha256=parent['surface_sha256'],surface_sha256={str(path):sha(path) for path in surfaces},
    backups=backups,artifacts=artifacts,archived_artifact_redirects=redirects,
    report_sha256=sha(extras[0]),runtime_result_pending=True,new_full_runtime_performed=True,
    last_completed_run=2,last_completed_run_selftest=prior['selftest'],current_runtime_attempt=3,
    current_runtime_pid=state['pid'],current_runtime_session=76735,
    corrected_candidate_full_runtime_completed=False,full_goal_complete=False,
    runtime_formal_stage_verified=False,runtime_formal_stage_independently_reviewed=False,
    current_audit_stdout_path=str(RUN/'completed_attempt_02/audit_principal.stdout.txt'),
    current_audit_stdout_scope='LAST_COMPLETED_RUN02__NOT_CURRENT_RUN03',
    new_modules_integrated_this_record=0,new_functions_added=0,principal_gate_changed=False,
    reader_review_path=str(REVIEW),reader_review_sha256=sha(REVIEW),input_files_restored=4))
atomic(OUT,encoded(custody))
print(json.dumps(dict(recorded=True,memory_surfaces=len(surfaces),backups=len(backups),
    custody_sha256=sha(OUT),runtime_pid=state['pid'],runtime_session=76735,
    working_sha256=integration['working_sha256'],full_task_pending=True)))
