"""Append the integrated review. Reads author artifacts; writes only reviewer files."""
from pathlib import Path
import datetime
import hashlib
import json
import os

REV = Path(__file__).resolve().parent
ROOT = REV.parent
RUN = Path((REV / 'paired_right_integrated_latest_run.txt').read_text().strip())
REPORT = REV / 'REVIEW_PAIRED_RIGHT_INTEGRATED.md'
assert RUN.resolve().is_relative_to(REV)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    return json.loads(p.read_bytes())
def link(label, p):
    return f'[{label}](<{p.resolve().as_posix()}>)'
def atomic(p, raw):
    assert p.resolve().is_relative_to(REV)
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup = None
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + stamp)
        with backup.open('xb') as stream:
            stream.write(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name + '.tmp_' + stamp)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    os.replace(temp, p)
    assert p.read_bytes() == raw
    return backup

v = load(RUN / 'verification.json')
s = load(RUN / 'static_verification.json')
g = load(RUN / 'gate_tests.json')
e = load(RUN / 'kernel_incremental_evidence.json')
parent = load(RUN / 'right_regularization_custody.json')
assert v['mode'] == 'FINAL_INTEGRATION_INSPECTION_NO_REBUILD'
assert v['integrated_records'] == 194 and v['unchanged_parent_records'] == 189
assert v['new_author_compilations'] == 5 and len(v['new_records']) == 5
assert v['audit_distinct'] == 6930 and v['new_axioms_equal_own_DEV'] == 29
assert v['gate_passed_author_records'] == 99
assert not v['P0'] and not v['P1'] and not v['P2']
assert all(sha(ROOT / name) == pin for name,pin in v['artifact_pins'].items())
assert sha(ROOT / 'um.py') == v['working_sha256']
assert sha(REV / 'REVIEW_PAIRED_RIGHT_DEV.md') == v['own_DEV_review_sha256']
assert sha(REPORT) == load(RUN / 'preliminary_review_pin.json')['report_sha256']
assert g['frontier']['scope'] == e['v350_modular_scope'] == 'PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT'
assert not g['frontier']['legacy_gate_changed'] and not g['frontier']['full_plan_complete']
assert not g['full_monolithic_runtime_run']
assert len(v['six_flags']) == 6 and not any(v['six_flags'].values())
assert all(e[k] is False for k in v['six_flags'])
assert len(g['checks']) == len({r['name'] for r in g['checks']}) == 99
assert all(r['passed'] for r in g['checks'])
assert v['current_Audit_global_hashes_verified'] and v['parent_Audit_no_loss']
audit = v['final_Audit_record']
assert sha(Path(audit['stdout_path'])) == audit['stdout_sha256']
assert e['audit_stdout_sha256'] == e['audit_capture_sha256_full'] == audit['stdout_sha256']
assert e['audit_hash_scope'] == 'CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES'
assert e['historical_v350_audit_metadata'] == v['historical_Audit_metadata_preserved']
original = Path(load(ROOT / 'environment.json')['original_source'])
original_sha = sha(original)
assert original_sha == sha(ROOT / 'fontes/um_v350_original.py') == v['original_sha256']
assert original_sha == parent['original_sha256']
assert len(s['memory_surfaces']) == 34
assert not any((ROOT / n).exists() for n in s['future_custody_artifacts_absent'])
now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
readback = {'timestamp': now, 'original_path': str(original),
    'original_sha256_fresh_read': original_sha, 'working_sha256_fresh_read': sha(ROOT / 'um.py'),
    'verification_sha256': sha(RUN / 'verification.json'),
    'current_Audit_raw_stdout_sha256': audit['stdout_sha256'],
    'scope': g['frontier']['scope'], 'flags': v['six_flags'],
    'frozen_artifact_pins_reread': True, 'reviewed_DEV_preserved': True,
    'memory_and_custody_recorders_not_executed_by_reviewer': True,
    'new_custody_verifier_and_integrated_author_report_absent': s['future_custody_artifacts_absent'],
    'findings': [], 'integration_review_complete': True}
atomic(RUN / 'final_readback.json', (json.dumps(readback, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
old = REPORT.read_bytes()
old_sha = sha(REPORT)
assert b'PAIRED_RIGHT_INTEGRATED_REVIEW' not in old
addition = f'''

---

Adendo final — {now}

**PAIRED_RIGHT_INTEGRATED_REVIEW**

[REAL] **Revisão integrada encerrada, sem achados P0, P1 ou P2.** O preliminar está preservado por backup imediato de bytes e append. Captura conclusiva: {link('verification.json', RUN / 'verification.json')} (SHA `{sha(RUN / 'verification.json')}`) e {link('releitura final', RUN / 'final_readback.json')}.

Conferidos por leitura própria: **194 registros = 189 herdados idênticos + três módulos e duas raízes recompilados pelo autor**; todos os pares fonte/.olean, comandos, logs JSON e streams coincidem com seus pins. Os cinco novos rc0 registram fontes inalteradas, sem warnings, e dependências diretas com binários e frescor conferidos. As três transposições são literalmente apenas imports, embutidos iguais às fontes; as raízes acrescentam somente os imports e 29 alvos esperados. Total medido: **896 embutidos**.

O Audit atual `{audit['log_name']}` foi reparseado: **6930 declarações = 6901 anteriores preservadas + 29 do manifesto/DEV próprio**, todas limitadas ao trio lógico. Os mapas dos três streams integrados coincidem com os respectivos alvos da auditoria independente DEV. `audit_stdout_sha256` e `audit_capture_sha256_full` apontam ambos aos bytes atuais `{audit['stdout_sha256']}`; o escopo é `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES`. Os valores anteriores permanecem separados em `historical_v350_audit_metadata`.

**99/99 controles autorais**: preservados os 98 anteriores, acrescido `original_adjoint_pairs_and_generated_right_star_algebra_does_not_discharge_KMS_trace_or_physical_frontier`. Sua condição confere os quatro enunciados de fronteira, as seis flags falsas, gate inalterado e plano integral falso. A fronteira continua `{g['frontier']['scope']}`; esse escopo herdado não atribui ao novo pacote uma igualdade global de comutantes pelo J do peso. `legacy_gate_changed=false`, `full_plan_complete=false` e runtime integral não executado.

| Evidência | Alcance efetivamente conferido |
| --- | --- |
| DEV própria | Três recompilações anteriores e auditor29 rc0, reutilizados com pins; nenhuma repetição nesta integração |
| Integração autoral | Releitura independente dos 194 pares, logs/streams, cinco compilações novas, mapas de axiomas e dependências |
| Controles autorais | Relatório 99/99 e condições do novo grupo inspecionados; testes não reexecutados pelo revisor |

AST Python fora do embutido e `gate_extension.py` preservados contra a mãe. Os cinco helpers permanecem nos bytes revisados; os deltas executados de prepare/integrador/compilador/testes coincidem com os previstos. Recorder e verifier exigem as revisões e validam a mesma mãe para integração e memória, com 34 backups de bytes/append e releitura dos pares fonte/binário. **As 34 memórias ainda coincidem com a mãe; novo recorder/verifier/custódia não são declarados executados.** A inspeção estática desses mecanismos não substitui a verificação após sua execução futura.

Pins atuais: cópia `{v['working_sha256']}`; mãe `{v['parent_custody_sha256']}`; original canônico/base relidos `{original_sha}`. Fonte, hashes e logs completos estão na captura própria; não houve execução/importação de monólito, helper autoral, recompilação ou escrita em memória pelo revisor.

[OPEN] Resultado mantido: pares no F original, aproximação forte-* K_h(T) e álgebra de von Neumann gerada igual a π(N)'. Continuam fora desta conclusão: núcleo de grafo para F, reconstrução R=Jπ(b)J, inclusão inversa por J, plenitude de álgebra de Hilbert, identificação Δ^it/KMS e traço. **Nenhuma pendência desta revisão integrada delimitada; nenhuma promoção de gate ou fechamento global.**
'''
backup = atomic(REPORT, old + addition.encode('utf-8'))
assert REPORT.read_bytes().startswith(old) and sha(backup) == old_sha
assert REPORT.read_bytes().count(b'PAIRED_RIGHT_INTEGRATED_REVIEW') == 1
pin = {'timestamp': now, 'status': 'INTEGRATED_REVIEW_COMPLETE__AUTHOR_RECORDING_PENDING',
       'report': str(REPORT), 'report_sha256': sha(REPORT), 'immediate_backup': str(backup),
       'preserved_prefix_sha256': old_sha, 'preserved_prefix_bytes': len(old),
       'verification_sha256': sha(RUN / 'verification.json'),
       'final_readback_sha256': sha(RUN / 'final_readback.json'), 'findings': []}
atomic(RUN / 'final_review_pin.json', (json.dumps(pin, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps(pin, ensure_ascii=False))
