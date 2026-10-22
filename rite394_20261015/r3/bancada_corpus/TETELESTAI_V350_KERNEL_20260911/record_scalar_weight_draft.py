"""Pin compiled development proofs without promoting them to reviewed integration."""
from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['FixedBaseEquivalence', 'BoundedBaseDualValues',
           'ScalarDualWeightFaithfulness', 'ScalarDualWeight']
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, raw):
    assert p.resolve().is_relative_to(ROOT)
    if p.exists():
        before = p.read_bytes()
        b = p.with_name(p.name + '.bak_' + STAMP)
        with b.open('xb') as f:
            f.write(before)
        assert b.read_bytes() == before
    t = p.with_name(p.name + '.tmp_' + STAMP)
    with t.open('xb') as f:
        f.write(raw)
    assert t.read_bytes() == raw and len(raw) > 0
    t.replace(p)
    assert p.read_bytes() == raw


records = {}
targets = {}
for name in MODULES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    matches = []
    for log in (ROOT / 'logs').glob(name + '_*.json'):
        row = json.loads(log.read_bytes())
        if row['sha256'] == sha(source) and row['returncode'] == 0:
            matches.append((log, row))
    assert matches, name
    log, row = sorted(matches, key=lambda pair: pair[1]['timestamp'])[-1]
    assert row['source_unchanged_during_compile']
    assert row['output_sha256'] == sha(ROOT / 'build/TGLV350' / (name + '.olean'))
    output = Path(row['stdout']).read_text(encoding='utf-8')
    names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for target in names:
        full = 'TGLV350.Regular.' + target
        m = re.search(re.escape("'" + full + "' depends on axioms:") + r'\s*\[([^\]]*)\]', output)
        assert m, full
        axioms = {s.strip() for s in m.group(1).split(',')}
        assert axioms <= {'propext', 'Classical.choice', 'Quot.sound'}, (full, axioms)
        targets[full] = sorted(axioms)
    records[name] = {'log': str(log), **row}
assert len(targets) == 23
base = json.loads((ROOT / 'fixed_base_custody.json').read_bytes())
assert sha(ROOT / 'um.py') == base['working_sha256']
note = '''# Peso escalar dual — desenvolvimento ainda não integrado nem revisado

[REAL — compilação local, não revisão independente]

Quatro módulos e 23 alvos foram compilados em desenvolvimento. A cópia
integrada permanece na custódia fixed_base_custody.json: esta nota não
amplia seu escopo nem altera flags.

FixedBaseEquivalence empacota a mesma amplificação M→F como equivalência
de álgebras com involução e isomorfismo de ordem; a inversa é e*Be.
BoundedBaseDualValues transporta os valores positivos limitados para M,
prova sua unicidade e a aproximação forte por entradas com quadrados finitos.

ScalarDualWeightFaithfulness usa η=eΩ. η é separante para F porque Ω é
separante para M. Se q_A(η)=0, o resolvente minimizador satisfaz Rη=η;
R∈F implica R=I. A identidade de energia, com finitude explícita, dá
q_A(v)=0 para todo v, e a fidelidade da forma conclui A=0.

ScalarDualWeight define ν(A)=q_A(η) no cone positivo de N e prova zero,
aditividade, homogeneidade por escalares não negativos, monotonia,
fidelidade e normalidade para supremos dirigidos internos. O ideal
complexo esquerdo já construído é fortemente denso e seus quadrados têm
ν finito. Para um valor limitado fibre(D), ν coincide com a avaliação
do estado vetorial original em D. O enunciado exato de densidade e a
conexão com a interface padrão de peso precisam de revisão independente.

[OPEN] Este peso não é um traço. Ainda faltam a identificação de seu
grupo modular/condição KMS, o gerador afiliado e a perturbação que produz
o traço canônico e sua escala. A correspondência geral espectral/predual,
o contrato de peso operatorial, Three Locks/H1–H3 físicos, interações,
contrato ampliado do gate e runtime integral permanecem abertos.
Não se reivindica fidelidade apenas de um funcional normalizado ou de
um estado alternativo: a prova usa a forma dual e a torre desta construção.

Os hashes e logs exatos estão em scalar_weight_draft_status.json. Todas
as tentativas de compilação, inclusive falhas, permanecem em logs/.
Próximo passo: revisão independente dos quatro módulos, integração e
custódia, antes de prosseguir para a condição modular do peso escalar.
'''
save(ROOT / 'ROTA_PESO_ESCALAR_RASCUNHO.md', note.encode('utf-8'))
result = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'status': 'DEVELOPMENT_COMPILED__NOT_INTEGRATED__NOT_INDEPENDENTLY_REVIEWED',
    'records': records, 'targets': targets,
    'integrated_custody': 'fixed_base_custody.json',
    'integrated_custody_sha256': sha(ROOT / 'fixed_base_custody.json'),
    'working_sha256': base['working_sha256'],
    'draft_note_sha256': sha(ROOT / 'ROTA_PESO_ESCALAR_RASCUNHO.md'),
    'full_runtime': False, 'canonical_trace_constructed': False, 'full_goal_complete': False,
}
save(ROOT / 'scalar_weight_draft_status.json', json.dumps(result, ensure_ascii=False, indent=2).encode())
print(json.dumps({'development_modules': len(records), 'development_targets': len(targets),
                  'integrated': False, 'independently_reviewed': False}))
