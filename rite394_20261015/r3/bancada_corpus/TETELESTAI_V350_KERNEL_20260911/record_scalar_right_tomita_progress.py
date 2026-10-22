"""Record the integrated domain bridges with their two distinct lineage parents."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MARKER = 'TETELESTAI_V350_RIGHT_TOMITA_ADJOINT_INTEGRATED_20260912'
BACKUPS = {}
assert '--review-read' in sys.argv

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(name):
    return json.loads((ROOT / name).read_bytes())

def write(path, raw, before=None):
    assert path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    assert raw
    if before is None:
        assert not path.exists(), path
    else:
        assert path.read_bytes() == before and raw.startswith(before) and len(raw) > len(before)
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as stream:
            stream.write(before)
        assert backup.read_bytes() == before
        BACKUPS[str(path)] = str(backup)
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    if before is not None:
        assert path.read_bytes() == before
    temp.replace(path)
    assert path.read_bytes() == raw

def body(path):
    tree = ast.parse(path.read_bytes())
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets))
    node.value = ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return ast.dump(tree, include_attributes=False)

parent_path = ROOT / 'homogeneous_right_custody.json'
memory_path = ROOT / 'scalar_right_tomita_draft_memory.json'
parent, memory = read(parent_path.name), read(memory_path.name)
draft, extra = read('scalar_right_tomita_draft_status.json'), read('scalar_right_adjoint_draft_status.json')
integration, build, tests = read('integration.json'), read('integrated_compile.json'), read('gate_tests.json')
evidence = read('kernel_incremental_evidence.json')
reviews = [ROOT / 'revisao/REVIEW_SCALAR_RIGHT_CLOSED_TOMITA.md',
           ROOT / 'revisao/REVIEW_SCALAR_RIGHT_TOMITA_INTEGRATED.md']
assert 'SCALAR_RIGHT_CLOSED_TOMITA_DEV_REVIEW' in reviews[0].read_text(encoding='utf-8')
assert 'SCALAR_RIGHT_TOMITA_INTEGRATED_REVIEW' in reviews[1].read_text(encoding='utf-8')
assert memory['previous_custody_sha256'] == draft['parent_custody_sha256'] == sha(parent_path)
assert extra['parent_memory_sha256'] == sha(memory_path)
assert extra['parent_draft_sha256'] == sha(ROOT / 'scalar_right_tomita_draft_status.json')
original = Path(read('environment.json')['original_source'])
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
assert sha(ROOT / 'um.py') == integration['working_sha256'] == tests['working_um_sha256']
prior = next(p for p in ROOT.glob('um.py.bak_*') if sha(p) == parent['working_sha256'])
assert body(prior) == body(ROOT / 'um.py')
assert build['incremental_build_ok']
for row in build['records']:
    source = Path(row['source']).resolve()
    assert source.is_relative_to(ROOT / 'kernel')
    binary = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and row['output_exists']
    assert sha(source) == row['sha256'] and sha(binary) == row['output_sha256']
assert tests['passed'] == len(tests['checks']) and all(c['passed'] for c in tests['checks'])
assert not tests['full_monolithic_runtime_run'] and not tests['frontier']['legacy_gate_changed']
audit_stdout = Path(build['records'][-1]['stdout'])
assert evidence['audit_stdout_sha256'] == evidence['audit_capture_sha256_full'] == sha(audit_stdout)
assert evidence['audit_stdout_path'] == str(audit_stdout)
baseline = read('fontes/um_absoluto.json')['core']['kernel_formalization']
assert evidence['historical_v350_audit_metadata'] == {key: baseline.get(key) for key in
    ('audit_stdout_sha256', 'audit_capture_sha256_full')}
assert all(evidence[k] is False for k in parent['remaining_flags'])
all_modules = dict(draft['modules'])
all_modules[extra['module']] = extra
expected = dict(draft['targets'])
assert not set(expected).intersection(extra['targets'])
expected.update(extra['targets'])
modules, targets = {}, {}
for name, row in all_modules.items():
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    final = ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')
    raw = source.read_text(encoding='utf-8')
    assert sha(source) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']
    assert re.sub(r'^import TGLV350\.', 'import TGLExt.V350', raw, flags=re.M) == final.read_text(encoding='utf-8')
    modules[name] = {'development_sha256': sha(source), 'integrated_sha256': sha(final),
        'development_binary_sha256': sha(ROOT / 'build/TGLV350' / (name + '.olean'))}
    for short in re.findall(r'^#print axioms ([\w.]+)$', raw, re.M):
        full = 'TGLV350.Regular.' + short
        axioms = evidence['axiom_report'][full]
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        assert sorted(axioms) == expected[full]
        targets[full] = axioms
assert len(modules) == 3 and len(targets) == 17 and set(targets) == set(expected)
surfaces = [Path(p) for p in memory['surface_sha256']]
before = {str(p): p.read_bytes() for p in surfaces}
assert len(surfaces) == 34
for p in surfaces:
    assert sha(p) == memory['surface_sha256'][str(p)] and MARKER.encode() not in before[str(p)]

report = ROOT / 'RELATORIO_DOMINIOS_TOMITA_ADJUNTO_INTEGRADOS.md'
report_text = f'''# Domínios do mesmo Tomita e de seu adjunto — integração revisada

{DATE}. [REAL — três módulos/17 alvos integrados e revisados]

Para os dados homogêneos construídos, inclusive cada unidade matricial local y:

    R_y D(S) ⊆ D(S),       S R_y x = π(y*) S x;
    π(y) D(S†) ⊆ D(S†),    S† π(y) z = R_y* S† z.

As igualdades valem nos domínios completos indicados, no mesmo GNS H_I e
para o mesmo operador fechado S e seu adjunto máximo. A primeira transporta
o gráfico do núcleo involutivo por um mapa contínuo de pares e passa ao fecho.
A segunda usa o pareamento para todo x∈D(S) e a definição máxima de S†.
S não é pressuposto limitado; D(S) não é identificado com a imagem algébrica.
O y* da primeira igualdade e o adjunto direito R_y* da segunda têm tipos
distintos. Para a instância local, R_y*=R_(ρy*ρ⁻¹), como provado antes.

Integração: {len(build['records'])} registros incrementais rc0,
{tests['passed']} controles aprovados, {tests['axiom_report_entries']} declarações
Audit e {integration['embedded_files']} arquivos embutidos. As dependências
anteriores foram reutilizadas com hashes conferidos. Revisões DEV e integrada
lidas. O corpo Python fora do embutido é igual ao estágio anterior.

[REAL — correção de metadados] Os campos globais de hash do Audit agora
apontam para os bytes do stdout corrente. Os valores herdados da v350 foram
preservados em historical_v350_audit_metadata. Dois controles verificam a
correspondência atual e a preservação histórica; o critério do gate não mudou.

O que falta para mover as seis obrigações maiores do gate:

| Obrigação | Parte já disponível | Resultado ainda exigido |
|---|---|---|
| Modular contínua | GNS do peso, S fechado, raiz e polar involutiva, novas relações nos domínios | Identificar o fluxo com (S†S)^it e demonstrar KMS global |
| Canto contínuo | Álgebra regular, ação dual e peso | Traço canônico, escala dual e canto finito Three Locks no mesmo modelo |
| H1 | Setor finito | Lacuna relativa SUSY além da face finita |
| H2 | Métrica refletida de Fisher | Dados suaves de posto quatro e identificação provenientes do mesmo estado/peso |
| H3 | Ponte condicional de Einstein e custos internos | Equilíbrio área-calor no mesmo horizonte físico, com fonte e limite exigidos |
| Testemunha completa | Contratos e resultados parciais | Interação quântica, BRST/QME, anomalias/escopo UV, composição e consumo efetivo |

As pontes de Einstein, Fisher e gauge geral linearizado já localizadas em
Chatgpt permanecem disponíveis com suas hipóteses. A tabela atual de consumo
tem três contratos anteriores; as novas obrigações exigirão seus próprios
termos e pontes de tipo exato compiladas, proveniência e consumo no certificado.
Mais declarações isoladas não bastam para mover essas flags.

[OPEN — próximo alvo preciso] Para y=e_ij e r=w_i/w_j, combinar os dois
entrelaçamentos exige identificar a instância torcida de y* com rR_y e
transportar o domínio composto D(S†S). O alvo é
R_yD(S†S)⊆D(S†S) e (S†S)R_yx=rR_y(S†S)x. Isso ainda não foi compilado.
Mesmo obtendo essa relação local, será necessário um argumento de domínio
e completude que identifique o fluxo inteiro; a relação local não o substitui.

[OPEN] KMS, identificação espectral completa, traço, hipóteses físicas e
runtime integral permanecem abertos. Nenhuma das seis flags foi promovida.
Gate legado preservado; original não executado/importado; objetivo ativo.

[Revisão DEV](<{reviews[0].as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
[Reaproveitamento em Chatgpt](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`.
Mãe integrada `{sha(parent_path)}`; mãe imediata de memória `{sha(memory_path)}`.
Os manifestos DEV anteriores permanecem como registros datados.
'''
write(report, report_text.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] Três módulos/17 alvos ligam a direita homogênea
ao mesmo Tomita fechado e seu adjunto máximo: R_yD(S)⊆D(S), S R_y=π(y*)S;
π(y)D(S†)⊆D(S†), S†π(y)=R_y*S†. As igualdades valem nos domínios completos.
Para cada unidade matricial local R_y*=R_(ρy*ρ⁻¹). Não se supõe S limitado,
KMS, nem igualdade do domínio fechado com a imagem do núcleo algébrico.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit. Revisões DEV e integrada lidas.
Cópia {sha(ROOT / 'um.py')}; original preservado; seis flags maiores falsas.
O histórico DEV12 e o adendo DEV5 permanecem preservados. Sem runtime integral.
Os dois hashes globais do Audit agora ancoram o stdout atual; os valores
herdados permanecem em campo histórico explícito, com dois controles novos.

[OPEN] Identificar (S†S)^it com o fluxo/KMS, traço/escala/canto Three Locks,
H1/H2/H3 físicos compatíveis, interação quântica e consumo pelo certificado.
Reutilizar Einstein/Fisher/gauge já encontrados com suas hipóteses.
As novas relações reduzem o trabalho de domínio; não quitam esses elos.
Objetivo integral ativo; gate legado inalterado.

[Relatório e tabela atuais](<{report.as_posix()}>).
[Revisão independente](<{reviews[1].as_posix()}>).
'''
for p in surfaces:
    raw = before[str(p)]
    newline = '\r\n' if b'\r\n' in raw else '\n'
    write(p, raw + note.replace('\n', newline).encode('utf-8'), raw)
artifacts = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'scalar_right_tomita_draft_status.json',
    'scalar_right_adjoint_draft_status.json', 'record_scalar_right_tomita_draft.py',
    'record_scalar_right_adjoint_draft.py', 'prepare_scalar_right_tomita_stage.py',
    'record_scalar_right_tomita_progress.py', 'verify_scalar_right_tomita_custody.py']
data = {'timestamp': DATE, 'previous_custody_path': str(memory_path),
    'previous_custody_sha256': sha(memory_path),
    'previous_integrated_custody_path': str(parent_path),
    'previous_integrated_custody_sha256': sha(parent_path),
    'original_sha256': sha(original), 'working_sha256': sha(ROOT / 'um.py'),
    'previous_working_copy': str(prior), 'python_body_unchanged_from_previous_stage': True,
    'modules': modules, 'targets': targets, 'integrated_records': len(build['records']),
    'controls': tests['passed'], 'audit_declarations': tests['axiom_report_entries'],
    'current_audit_stdout_path': str(audit_stdout), 'current_audit_stdout_sha256': sha(audit_stdout),
    'surface_sha256': {str(p): sha(p) for p in surfaces}, 'backups': BACKUPS,
    'surface_before_sha256': {str(p): sha(Path(BACKUPS[str(p)])) for p in surfaces},
    'review_sha256': {str(p): sha(p) for p in reviews}, 'report_path': str(report),
    'report_sha256': sha(report), 'artifacts': {name: sha(ROOT / name) for name in artifacts},
    'remaining_flags': {key: evidence[key] for key in parent['remaining_flags']},
    'same_closed_Tomita_domain_right_invariant': True,
    'same_maximal_adjoint_domain_left_invariant': True,
    'both_intertwinings_on_full_domains': True,
    'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write(ROOT / 'scalar_right_tomita_custody.json', json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'custody': 'scalar_right_tomita_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
