"""Freeze the same-Hilbert-space polar construction, without claiming modular conjugation."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
NAMES = ['PartialSelfadjointRange', 'DenseAntilinearExtension', 'ScalarTomitaPolarFactor']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert not path.exists() and raw
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw
    temporary.replace(path)
    assert path.read_bytes() == raw

modules, targets = {}, {}
for name in NAMES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    binary = ROOT / 'build/TGLV350' / (name + '.olean')
    history = [(p, json.loads(p.read_bytes())) for p in sorted((ROOT / 'logs').glob(name + '_*.json'))]
    accepted = [(p, v) for p, v in history if v['returncode'] == 0 and
                v['sha256'] == sha(source) and v['output_sha256'] == sha(binary)]
    assert accepted, name
    log, row = accepted[-1]
    stdout = Path(row['stdout'])
    text = stdout.read_text(encoding='utf-8')
    names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for short in names:
        full = 'TGLV350.Regular.' + short
        match = re.search(re.escape("'" + full + "' depends on axioms: [") + r'([^]]*)\]', text)
        assert match, full
        axioms = sorted(x.strip() for x in match.group(1).split(','))
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        targets[full] = axioms
    modules[name] = {'source_sha256': sha(source), 'binary_sha256': sha(binary),
        'targets': len(names), 'final_log': str(log), 'final_log_sha256': sha(log),
        'stdout_sha256': sha(stdout),
        'failed_attempts': [str(p) for p, v in history if v['returncode']]}
assert len(targets) == 16
parent = ROOT / 'tomita_root_custody.json'
domain = ROOT / 'tomita_root_domain_draft_status.json'
domain_review = ROOT / 'revisao/REVIEW_SCALAR_TOMITA_DOMAIN.md'
assert sha(ROOT / 'um.py') == json.loads(parent.read_bytes())['working_sha256']
for name, row in json.loads(domain.read_bytes())['modules'].items():
    assert sha(ROOT / 'kernel/TGLV350' / (name + '.lean')) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']
report = ROOT / 'RELATORIO_FATOR_POLAR_TOMITA_DEV.md'
create(report, f'''# Fator antiunitário polar do S original — DEV

{DATE}. [REAL — três módulos/16 alvos compilados; revisão e integração pendentes]

O domínio D(B)=D(S) e a igualdade de normas já passaram pela revisão independente
de seis módulos/25 alvos. No mesmo ScalarGNSHilbert P, a raiz B é auto-adjunta,
densamente definida e tem núcleo zero. Um vetor ortogonal à imagem de B pertence
ao domínio do adjunto, com B†z=0; auto-adjunção e núcleo zero dão z=0. Logo Ran B
é denso. Isso não afirma que Ran B=H_I ou que haja inverso limitado/gap.

Sobre D(B), f(x)=Sx é conjugado-linear e tem norma igual à de Bx. Mathlib
LinearMap.extendOfNorm estende a regra U(Bx)=Sx a um mapa conjugado-linear contínuo
em todo H_I. A identidade das normas estende-se por densidade. Ran S contém
D(S), pela involutividade de S; portanto Ran f é denso. A imagem da isometria U
é fechada por completude e contém Ran f, logo U é sobrejetiva e antiunitária.

A aplicação concreta não recebe antiunitário, densidade das imagens ou igualdade
das normas como premissas novas: usa P e os resultados construídos. Conclui
Sx=U(Bx) para TODO x∈D(S), preservando o espaço, as inclusões e o operador S.
Todos os 16 alvos dependem somente de propext, Classical.choice e Quot.sound.
Tentativas rc1 ficam no manifesto, excluídas da evidência aceita.

[OPEN] Este pacote NÃO prova U²=I, a identificação de U como conjugação modular J,
o domínio máximo do peso, KMS, traço e escala dual, canto Three Locks nem
H1/H2/H3 físicos. Antiunitariedade e fatoração não são promovidas a essas condições.
O setor quântico interagente, o contrato completo consumido pelo gate e o runtime
integral também permanecem pendentes. As seis flags maiores não foram alteradas.

Mãe integrada `{sha(parent)}`; domínio DEV `{sha(domain)}`;
parecer do domínio `{sha(domain_review)}`. Cópia integrada ainda
`{sha(ROOT / 'um.py')}`. Nenhuma execução/importação do monólito.
'''.encode('utf-8'))
record = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_sha256': sha(report),
    'parent_custody_sha256': sha(parent), 'domain_manifest_sha256': sha(domain),
    'domain_review_sha256': sha(domain_review), 'integrated_working_sha256': sha(ROOT / 'um.py'),
    'polar_antiunitary_constructed': True, 'factorization_on_full_domain': True,
    'polar_involution_proved': False, 'modular_weight_identified': False,
    'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'integrated': False, 'full_goal_complete': False}
manifest = ROOT / 'tomita_polar_draft_status.json'
create(manifest, json.dumps(record, ensure_ascii=False, indent=2).encode())
print(json.dumps({'modules': len(modules), 'targets': len(targets),
    'manifest_sha256': sha(manifest), 'status': record['status']}))
