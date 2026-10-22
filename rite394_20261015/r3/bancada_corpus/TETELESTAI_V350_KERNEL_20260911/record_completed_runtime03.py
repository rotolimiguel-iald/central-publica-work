"""Record verified completion using byte backups and existing memory surfaces."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import sys

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'r'
ARCHIVE=RUN/'completed_attempt_03'
PARENT=ROOT/'runtime_reader_correction_custody.json'
OUTPUT=ROOT/'runtime_final_custody.json'
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MARKER='TETELESTAI_V350_INTEGRACAO_CONCLUIDA_RODADA03_20260913'
REVIEW=Path(sys.argv[1]).resolve()
assert REVIEW.is_relative_to((ROOT/'revisao').resolve()) and REVIEW.is_file()
REVIEW_EVIDENCE=ROOT/'revisao/runtime03_final_review_20260913_112807_208914/evidence.json'
assert REVIEW_EVIDENCE.is_file()
assert 'nenhum P0–P2 pendente' in REVIEW.read_text(encoding='utf-8')

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def encode(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def atomic(path,raw):
    temp=path.with_name(path.name+'.tmp_'+STAMP)
    with temp.open('xb') as stream:stream.write(raw)
    assert temp.read_bytes()==raw
    os.replace(temp,path)
    assert path.read_bytes()==raw

assert not OUTPUT.exists()
parent=json.loads(PARENT.read_bytes())
proof=json.loads((ARCHIVE/'verification.json').read_bytes())
state=json.loads((RUN/'runtime_process_03.json').read_bytes())
seal=json.loads((RUN/'um_absoluto_selo.json').read_bytes())
result=json.loads((RUN/'um_absoluto.json').read_bytes())
core=result['core']
assert state['status']=='PROCESS_EXITED' and state['returncode']==0
assert seal['fail_closed_selftest']==proof['selftest']=='FAIL_CLOSED_SELFTEST_PASSED'
assert sha(ROOT/'um.py')==sha(RUN/'um.py')==sha(ARCHIVE/'um.py')==parent['working_sha256']
assert proof['new_unsealed_vs_baseline']=={'formais':[],'recusas_de_dado':[]}
assert all(value is True for value in proof['gate'].values()) and len(proof['gate'])==11
assert core['kernel_formalization']['all_verified'] is True
assert core['kernel_formalization']['formal_release_ready'] is True
for name,pin in seal['sha256'].items():assert sha(RUN/name)==pin==sha(ARCHIVE/name)
for item in proof['recovered_inputs_verified']:
    assert sha(Path(item['runtime_destination']))==item['sha256']
original=Path(json.loads((ROOT/'environment.json').read_bytes())['original_source'])
original_hash=sha(original)
assert original_hash==parent['original_sha256']

paths=[Path(path) for path in parent['surface_sha256']]
extras=[ROOT/'RELATORIO_EXECUCAO_INTEGRAL.md',ROOT/'RUNTIME_ATIVO.json',ROOT/'CONTRATO_ATIVO_GATE_V350.json']
before={path:path.read_bytes() for path in paths+extras}
for path in paths:
    assert before[path] and MARKER.encode() not in before[path]
observed_before={str(path):sha(path) for path in paths}
concurrent=[name for name,pin in observed_before.items() if pin!=parent['surface_sha256'][name]]
note=f'''

## {MARKER} — {datetime.now().astimezone().isoformat(timespec='seconds')}

[REAL — execução integral e revisão] A cópia corrigida terminou rc0 em
{state['finished']} ({state['elapsed_seconds']:.2f}s). Build/Audit passaram;
o autoteste recusou a adulteração com sorryAx, restaurou a fonte e registrou
FAIL_CLOSED_SELFTEST_PASSED. A rodada usou a chave de checkpoints desligada.
Os 13 arquivos do selo conferem por hash; as 922 fontes formais foram restauradas
e conferidas. Audit explícito: 7.133 nomes; união build+Audit: 7.985 entradas,
igual ao JSON e manifesto, sem axiomas fora do trio permitido.

[REAL — ligação concluída] As onze entradas do gate principal permanecem
verdadeiras e o terminal já existente foi reproduzido. O reparo foi restrito a
duas funções existentes: montagem lê 8/8 e seu certificado com a guarda de termo
e ponte já disponível; Atlas/Índice lê 6+6 entradas próprias e conserva as flags
alheias como diagnóstico. Nenhuma função, prova Lean ou entrada de gate foi
acrescentada. A montagem declara o alcance PRODUCT_TOWER; não amplia os teoremas.
38 testes autorais e 39 verificações independentes do candidato passaram.

[REAL — insumos e regressões] Dois REVOLVER, documento Stokes e results.json
existentes foram repostos na cópia com hashes conferidos. Os 13 itens adicionais
que falharam na rodada 02 não se repetiram. O selo mantém exatamente as quatro
entradas históricas não seladas e as seis recusas de dado da referência; não se
apagou recusa nem se transformou NOT_FALSIFIED em confirmação. Rodadas 02 e 03
preservadas em completed_attempt_02 e completed_attempt_03 (esta: 53 arquivos).
O JSON inicial, antes dos leitores tardios, não é o JSON final: a segunda gravação
do próprio main inclui ambos. A observação prematura foi corrigida pela leitura
da saída final; não exigiu alteração do programa.

[Parecer final independente](<{REVIEW.as_posix()}>).
[Verificação e arquivo da rodada 03](<{(ARCHIVE/'verification.json').as_posix()}>).
[Programa executado](<{(RUN/'um.py').as_posix()}>).
[Selo final](<{(RUN/'um_absoluto_selo.json').as_posix()}>).

Programa SHA256 {sha(RUN/'um.py')}.
Original apenas lido, hash preservado: {original_hash}.
Gate emitido: `{seal['qg_closure_verdict']}`.

[CONCLUSÃO DO ESCOPO AUTORIZADO] Consolidação, reuso e ligação do conjunto
probatório existente ao contrato do um.py concluídos, com execução e revisão.
Não há nova entrada de prova faltante no gate principal. As extensões separadas
original-S/KMS/UV permanecem fora desta tarefa; os seus campos históricos não
reabrem automaticamente a pesquisa. Não há processo desta rodada a aguardar ou
reiniciar. Esta conclusão trata da integração computacional verificada; preserva
os estatutos e as limitações matemáticas/físicas já declarados pelos artefatos.
'''.encode('utf-8')
backups={}
for path,raw in before.items():
    backup=path.with_name(path.name+'.bak_'+STAMP)
    with backup.open('xb') as stream:stream.write(raw)
    assert backup.read_bytes()==raw
    backups[str(path)]=str(backup)
for path in paths+[extras[0]]:
    assert path.read_bytes()==before[path]
    atomic(path,before[path]+note)
    assert path.read_bytes().startswith(before[path])
locator=json.loads(before[extras[1]])
locator.update(dict(status='VERIFIED_COMPLETE',process_ended=True,
    full_runtime_result_pending=False,formal_stage_verified=True,
    formal_stage_independent_review_completed=True,remaining_action=None,
    last_completed_run_selftest=seal['fail_closed_selftest'],
    latest_completed_run_archive=str(ARCHIVE),final_review=str(REVIEW),
    custody=str(OUTPUT),completed_at=state['finished'],
    do_not_launch_duplicate=True,goal_scope='Existing proof integration completed; no new proof obligation.'))
atomic(extras[1],encode(locator))
contract=json.loads(before[extras[2]])
contract.update(dict(status='COMPLETED_USER_SCOPE__EXISTING_PROOF_INTEGRATION',
    corrected_runtime_pending=False,full_execution_verified=True,
    last_completed_runtime_archive=str(ARCHIVE),completion_review=str(REVIEW),
    emitted_gate_verdict=seal['qg_closure_verdict'],
    principal_gate_missing_proof_inputs=[],full_runtime_selftest=seal['fail_closed_selftest']))
atomic(extras[2],encode(contract))

artifacts={name:sha(ROOT/name) for name in parent['artifacts']}
additional=[Path(__file__),*extras,REVIEW,REVIEW_EVIDENCE,ROOT/'verify_and_archive_runtime03.py',
    RUN/'runtime_process_03.json',RUN/'runtime_stdout_03.txt',RUN/'runtime_stderr_03.txt',
    ARCHIVE/'verification.json',RUN/'um_absoluto_selo.json']
additional += [RUN/name for name in seal['sha256']]
additional += list(RUN.glob('*capture_selftest*'))
additional += [RUN/'tgl_kernel_build_capture.txt',RUN/'tgl_kernel_audit_capture.txt']
for path in additional:artifacts[path.relative_to(ROOT).as_posix()]=sha(path)
report_line=before[extras[0]].decode('utf-8').count('\n')+3
custody=dict(parent)
custody.update(dict(timestamp=datetime.now().astimezone().isoformat(),
    status='EXISTING_PROOF_INTEGRATION_COMPLETE__RUN03_VERIFIED_AND_REVIEWED',
    previous_custody_path=str(PARENT),previous_custody_sha256=sha(PARENT),marker=MARKER,
    surface_before_sha256=observed_before,surface_sha256={str(path):sha(path) for path in paths},
    concurrent_memory_updates_preserved=concurrent,backups=backups,artifacts=artifacts,
    original_unchanged=True,original_sha256=original_hash,
    runtime_result_pending=False,last_completed_run=3,
    last_completed_run_selftest=seal['fail_closed_selftest'],
    current_runtime_pid=None,current_runtime_session=None,
    completed_runtime_pid=state['pid'],completed_runtime_session=76735,
    corrected_candidate_full_runtime_completed=True,full_goal_complete=True,
    runtime_formal_stage_verified=True,runtime_formal_stage_independently_reviewed=True,
    current_audit_stdout_scope='COMPLETED_RUN03__AUDIT_BYTE_IDENTICAL_TO_REVIEWED_RUN02',
    full_runtime_review_path=str(REVIEW),full_runtime_review_sha256=sha(REVIEW),
    full_runtime_review_evidence_path=str(REVIEW_EVIDENCE),full_runtime_review_evidence_sha256=sha(REVIEW_EVIDENCE),
    report_sha256=sha(extras[0]),report_completion_line=report_line,
    final_runtime_verification_sha256=sha(ARCHIVE/'verification.json'),
    extra_unsealed_vs_baseline=proof['new_unsealed_vs_baseline'],
    new_functions_added=0,new_modules_integrated_this_record=0,principal_gate_changed=False))
atomic(OUTPUT,encode(custody))
print(json.dumps(dict(recorded=True,memory_surfaces=len(paths),backups=len(backups),
    custody_sha256=sha(OUTPUT),report_completion_line=report_line,
    original_unchanged=True,scope_completed=True,
    concurrent_memory_updates_preserved=concurrent)))
