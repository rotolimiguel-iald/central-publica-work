from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import re

REV = Path(__file__).resolve().parent
ROOT = REV.parent
FIRST = Path((REV / 'paired_right_first_latest_run.txt').read_text().strip())
SECOND = Path((REV / 'paired_right_second_latest_run.txt').read_text().strip())
RUN = Path((REV / 'paired_right_final_latest_run.txt').read_text().strip())
REPORT = REV / 'REVIEW_PAIRED_RIGHT_DEV.md'
for path in (FIRST, SECOND, RUN):
    assert path.resolve().is_relative_to(REV)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    return json.loads(p.read_bytes())
def link(label, p, line=None):
    return f'[{label}](<{p.resolve().as_posix()}' + (f':{line}' if line else '') + '>)'
def atomic(p, data):
    assert p.resolve().is_relative_to(REV)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup = None
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + stamp)
        with backup.open('xb') as f:
            f.write(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name + '.tmp_' + stamp)
    with temp.open('xb') as f:
        f.write(data)
    assert temp.read_bytes() == data
    os.replace(temp, p)
    assert p.read_bytes() == data
    return backup

draft = load(RUN / 'paired_right_draft_status.json')
manifest = load(RUN / 'manifest.json')
helper = load(RUN / 'helper_static_inspection.json')
assert not helper['findings'] and helper['targets'] == 29
assert sha(REPORT) == load(SECOND / 'partial_review_pin.json')['report_sha256']
assert len(draft['modules']) == 3 and len(draft['targets']) == 29
compilations = {str(p): load(p / 'compilation.json') for p in (FIRST, SECOND, RUN)}
records = {}
for base, name in zip((FIRST, SECOND, RUN), draft['modules']):
    c = compilations[str(base)]
    assert all(v for v in c.values() if isinstance(v, bool))
    row = next(r for r in c['records'] if r['module'] == 'TGLV350/' + name + '.lean')
    pin = draft['modules'][name]
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    binary = ROOT / 'build/TGLV350' / (name + '.olean')
    own_binary = Path(row['command'][2])
    assert row['returncode'] == 0 and row['axioms_allowed'] and row['exact_targets']
    assert sha(source) == row['source_sha256'] == pin['source_sha256']
    assert own_binary.resolve().is_relative_to(REV)
    assert own_binary.read_bytes() == binary.read_bytes()
    assert sha(binary) == row['output_sha256'] == pin['binary_sha256']
    log = Path(pin['final_log'])
    assert sha(log) == pin['final_log_sha256']
    author = load(log)
    assert author['returncode'] == author['lean_returncode'] == 0
    assert author['source_unchanged_during_compile'] and author['output_exists']
    assert author['sha256'] == sha(source) and author['output_sha256'] == sha(binary)
    for key in ('stdout', 'stderr'):
        assert sha(Path(author[key])) == pin[key + '_sha256']
        assert sha(Path(row[key])) == row[key + '_sha256']
    assert len(row['axioms']) == pin['targets']
    records[name] = {'own_run': base.as_posix(), 'source_sha256': sha(source),
                    'own_and_author_binary_sha256': sha(binary), 'seconds': row['seconds'],
                    'returncode': row['returncode'], 'targets': pin['targets'],
                    'author_final_log_sha256': sha(log), 'own_stdout_sha256': row['stdout_sha256'],
                    'own_compilation_sha256': sha(base / 'compilation.json')}

final = compilations[str(RUN)]
audit = final['records'][-1]
assert audit['module'] == 'PairedRightFullAudit.lean' and audit['returncode'] == 0
assert set(audit['axioms']) == set(draft['targets'])
assert all(sorted(v) == draft['targets'][k] == sorted(['propext', 'Classical.choice', 'Quot.sound'])
           for k, v in audit['axioms'].items())
assert sha(Path(audit['stdout'])) == audit['stdout_sha256']
assert sha(Path(audit['stderr'])) == audit['stderr_sha256']
audit_source = Path(audit['command'][-1]).read_text(encoding='utf-8')
assert len(re.findall(r'^#check ', audit_source, re.M)) == 29
assert len(re.findall(r'^#print axioms ', audit_source, re.M)) == 29
assert len(re.findall(r'^set_option pp.universes true in$', audit_source, re.M)) == 29
assert all(sha(ROOT / p) == h for p, h in manifest['artifact_pins'].items())
assert sha(ROOT / 'um.py') == manifest['working_sha256']
assert sha(ROOT / 'gate_extension.py') == manifest['gate_sha256']
assert len(manifest['six_flags']) == 6 and not any(manifest['six_flags'].values())
assert len(manifest['dependencies']) == 414 and len(manifest['reused_current_modules']) == 2
assert not (ROOT / 'paired_right_custody.json').exists()
assert not (ROOT / 'paired_right_custody_verification.json').exists()
history = load(RUN / 'author_history.json')
failures = {name: sum(r['module'] == name and r['returncode'] != 0 for r in history) for name in records}
now = datetime.now().astimezone().isoformat(timespec='seconds')
verification = {'timestamp': now, 'status': 'DEV_REVIEWED__INTEGRATION_PENDING',
    'modules': records, 'targets': audit['axioms'], 'exact_29_types_and_axioms': True,
    'three_independent_module_compilations_rc0': True, 'all_three_binaries_byte_equal_author': True,
    'full_auditor': audit, 'compilations': {p: sha(Path(p) / 'compilation.json') for p in compilations},
    'draft_sha256': sha(RUN / 'paired_right_draft_status.json'),
    'dev_report_sha256': sha(RUN / 'RELATORIO_ALGEBRA_DIREITA_ADJUNTO_DEV.md'),
    'helper_static_inspection_sha256': sha(RUN / 'helper_static_inspection.json'),
    'parent_custody_sha256': sha(RUN / 'right_regularization_custody.json'),
    'project_dependency_pairs_frozen': 414, 'current_module_binaries_reused': 2,
    'historical_rc1_excluded_by_module': failures,
    'preservation_checks': {k: v for k, v in final.items() if isinstance(v, bool)},
    'helpers_executed_by_reviewer': False, 'new_integration_certified': False,
    'new_memory_or_custody_written_by_reviewer': False, 'findings': [], 'dev_analysis_pending': False}
atomic(RUN / 'verification.json', (json.dumps(verification, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))

source = RUN / 'sources/TGLV350/ScalarPairedRightAlgebra.lean'
source_lines = source.read_text(encoding='utf-8').splitlines()
def at(needle):
    return next(i for i, s in enumerate(source_lines, 1) if needle in s)
table = '\n'.join(f'| {name} | {r["targets"]} | rc0 / {r["seconds"]} s | `{r["source_sha256"]}` | `{r["own_and_author_binary_sha256"]}` |' for name, r in records.items())
old = REPORT.read_bytes()
prefix_sha = sha(REPORT)
assert b'PAIRED_RIGHT_DEV_REVIEW' not in old
addition = f'''

---

Adendo cumulativo final — {now}

**PAIRED_RIGHT_DEV_REVIEW**

[REAL] **Revisão DEV encerrada: 3 módulos / 29 alvos (8+12+9), sem achados P0, P1 ou P2.** Os estratos anteriores permanecem como prefixo byte a byte. Foram lidos integralmente os três módulos, manifesto, relatório DEV e cinco helpers; tipos/universos e axiomas dos 29 alvos conferidos no auditor próprio. Nenhuma análise DEV delimitada resta pendente.

Na terceira fonte, {link('as operações sobre pares', source, at('def scalarRightAdjointPair_smul'))} preservam as coerções e a conjugação: cR tem vetores `(cη, conjugate(c)ζ)`; RS tem `(Rη_S, S*ζ_R)`; adjunto troca os vetores. O produto usa a comutação já deduzida das identidades direitas, sem presumir comutatividade entre R e S. A estrutura é uma `NonUnitalStarSubalgebra` de **operadores limitados** no mesmo H_I.

O {link('teorema de geração', source, at('theorem scalarPairedRightAlgebra_generated_eq_commutant'))} conclui exatamente `generatedAlgebra ↑(scalarPairedRightAlgebra P) = scalarGNSCommutant P`. A primeira inclusão usa pertinência dos pares ao comutante; a outra usa K_h(T), pertinência eventual e fechamento da VNA sob limites fortes no filtro não vazio `𝓝[>] 0`. Não há premissa residual de reconstrução por J ou de π(N) ser fechada. Não se afirma igualdade da subálgebra algébrica sem fecho com todo o comutante.

| Módulo | Alvos | Recompilação própria | SHA256 fonte | SHA256 .olean próprio = autoral |
| --- | --- | --- | --- | --- |
{table}

O {link('auditor cumulativo', Path(audit['stdout']))} passou rc0 em {audit['seconds']} s, com exatamente 29 `#check`/universos e 29 `#print axioms`, todos no trio `propext/Classical.choice/Quot.sound`. Os auxiliares privados estão cobertos transitivamente. Evidência consolidada: {link('verification.json', RUN / 'verification.json')} (SHA `{sha(RUN / 'verification.json')}`); {link('compilation.json final', RUN / 'compilation.json')}. As recompilações dos dois primeiros foram reutilizadas, sem repetição; o último processo compilou apenas a terceira fonte e o auditor29. As 414 dependências anteriores e os dois novos .olean próprios estão pinados na árvore final; a cadeia de origem das dependências é a documentada nos estratos anteriores. Pacotes externos permaneceram readonly, sem rebuild de biblioteca.

Pins lidos: manifesto autoral `{verification['draft_sha256']}`; relatório DEV `{verification['dev_report_sha256']}`; mãe `right_regularization_custody.json` `{verification['parent_custody_sha256']}`. Os logs finais e streams de cada módulo foram confrontados às fontes e binários atuais. O histórico contém {sum(failures.values())} rc1 ({'/'.join(str(failures[n]) for n in records)} por módulo), preservados e excluídos; nenhum print de tentativa recusada foi aceito.

[REAL — inspeção estática] {link('helper_static_inspection.json', RUN / 'helper_static_inspection.json')} (SHA `{verification['helper_static_inspection_sha256']}`) fixa os hashes dos cinco helpers. Maker/draft, preparador, recorder e verifier têm escopo 3/29 e a mesma mãe integrada/documental. A simulação textual somente em memória confirma três adições ao batch 544→573, ordem antes das raízes e um novo grupo de fronteira; não muda a lógica Audit atual/histórica. O recorder exige as leituras DEV e integrada, prevê 34 backups imediatos de bytes, append com prefixo e substituição atômica por arquivo; o verifier relê pares fonte/binário e a linhagem de backups. Relatório/templates distinguem geração do comutante, adjunto original, J preservado e obrigações abertas. **Nenhum desses helpers foi executado pelo revisor; execução futura, integração e custódia nova não são certificadas aqui.**

Fonte/binário autorais, helpers/documentos congelados, dependências, mãe, 34 memórias/backups, pareceres anteriores e hashes de monólito/gate preservados nas verificações próprias. A fiação integrada permanece a da mãe; este parecer não reaudita o runtime anterior nem executa o monólito. As seis flags maiores continuam falsas.

[OPEN] Permanecem fora deste resultado: plenitude de álgebra de Hilbert, densidade de núcleo no gráfico de F, reconstrução R=Jπ(b)J, inclusão inversa π(N)'⊆Jπ(N)J, fechamento von Neumann de π(N), identificação Δ^it/KMS, traço e consumo pelos certificados/gate. Não se assume I=nν nem continuidade geral de star em SOT. **Conclusão restrita: DEV revisado; integração pendente.**
'''
backup = atomic(REPORT, old + addition.encode('utf-8'))
assert REPORT.read_bytes().startswith(old)
assert REPORT.read_bytes().count(b'PAIRED_RIGHT_DEV_REVIEW') == 1
pin = {'timestamp': now, 'status': 'DEV_REVIEWED__INTEGRATION_PENDING', 'findings': [],
       'report': str(REPORT), 'report_sha256': sha(REPORT), 'report_bytes': REPORT.stat().st_size,
       'immediate_backup': str(backup), 'preserved_prefix_sha256': prefix_sha,
       'preserved_prefix_bytes': len(old), 'verification_sha256': sha(RUN / 'verification.json')}
assert sha(backup) == prefix_sha
atomic(RUN / 'final_review_pin.json', (json.dumps(pin, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps(pin, ensure_ascii=False))
