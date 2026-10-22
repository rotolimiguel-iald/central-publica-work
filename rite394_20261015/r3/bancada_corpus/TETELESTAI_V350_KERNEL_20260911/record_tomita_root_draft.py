"""Freeze compiled DEV root evidence; do not promote integrated or physical flags."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['PartialPositiveResolvent', 'ScalarTomitaResolvent', 'ScalarTomitaPositiveRoot',
         'PartialSquareEnergy', 'ScalarTomitaRootEnergy']
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert not path.exists() and raw
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

modules, targets = {}, {}
for name in NAMES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    binary = ROOT / 'build/TGLV350' / (name + '.olean')
    pin, outpin = digest(source), digest(binary)
    logs = [(p, json.loads(p.read_bytes())) for p in sorted(
        (ROOT / 'logs').glob(name + '_*.json'), reverse=True)]
    path, row = next((p,r) for p,r in logs if r['sha256'] == pin and r['returncode'] == 0
        and r['source_unchanged_during_compile'] and r['output_sha256'] == outpin)
    stdout = Path(row['stdout'])
    printed = {n: sorted(a.strip() for a in ax.split(',') if a.strip()) for n,ax in re.findall(
        r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", stdout.read_text(encoding='utf-8'))}
    names = ['TGLV350.Regular.'+n for n in re.findall(
        r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)]
    assert set(names) == set(printed)
    assert all(set(a) <= ALLOWED for a in printed.values())
    assert not set(targets).intersection(printed)
    targets.update(printed)
    modules[name] = {'source_sha256': pin, 'binary_sha256': outpin, 'targets': len(names),
        'final_log': str(path), 'final_log_sha256': digest(path), 'stdout_sha256': digest(stdout),
        'failed_attempts': [str(p) for p,r in logs if r['returncode'] != 0]}
assert len(targets) == 30
integration = json.loads((ROOT / 'integration.json').read_bytes())
assert digest(ROOT / 'um.py') == integration['working_sha256']
date = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
report = f'''# Resolvente e raiz positiva do mesmo S†S — desenvolvimento

{date}. [REAL — cinco módulos/30 declarações compiladas localmente]
[OPEN — revisão independente e integração deste lote ainda pendentes]

Construído R=(I+A)^(-1), A=S†S, no mesmo H_I. Positividade e a
sobrejetividade anterior fornecem uma equivalência linear entre D(A)
e H_I. A inclusão da inversa em H_I satisfaz ||Rz||≤||z||;
R é injetivo, auto-adjunto e 0≤R≤I. A igualdade
resolventGraphOperator R=A foi provada como mapas parciais.

Aplicada a construção anterior por cálculo funcional limitado:
B tem gráfico (sqrt(R)v,sqrt(I−R)v), é positivo, auto-adjunto,
fechado, densamente definido e B²=A como mapas parciais, com
igualdade dos domínios sucessivos. Seu núcleo é trivial.
Em D(A), foi provada a igualdade ||Bx||²=||Sx||².

[OPEN] Não foi provado D(B)=D(S), nem a igualdade de energia em
todo esse domínio. Portanto não se declara B como fator de uma
decomposição polar já identificada de S. J, identificação modular/KMS
do peso, traço/escala dual, Three Locks/H1–H3 e setor interagente
permanecem abertos. Núcleo trivial não implica gap.

Este lote DEV não está no monólito: a cópia integrada anterior
continua em `{integration['working_sha256']}`. Nenhum gate mudou,
nenhuma execução integral do monólito ocorreu e as contagens DEV
não se somam ao Audit integrado. Tentativas rc1 preservadas em logs;
somente logs finais rc0 e hashes coincidentes sustentam a compilação.
O manifesto tomita_root_draft_status.json discrimina as fontes,
binários, axiomas e tentativas. O plano integral continua incompleto.
'''
report_path = ROOT / 'RELATORIO_RAIZ_TOMITA_DEV.md'
create(report_path, report.encode('utf-8'))
status = {'timestamp': date, 'status': 'DEV_COMPILED__INDEPENDENT_REVIEW_AND_INTEGRATION_PENDING',
          'modules': modules, 'targets': targets, 'report_sha256': digest(report_path),
          'integrated_working_sha256': integration['working_sha256'],
          'integrated': False, 'root_square_equals_original_composition': True,
          'root_domain_equals_tomita_domain': False, 'polar_identified': False,
          'KMS_proved': False, 'canonical_trace_constructed': False,
          'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
create(ROOT / 'tomita_root_draft_status.json',
       json.dumps(status, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'status': status['status']}))
