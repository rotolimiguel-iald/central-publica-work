"""Freeze a later resolvent-flip development without adding it to the polar integration."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
NAMES = ['ScalarTomitaResolventFlip', 'ScalarTomitaPolarResolvent']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert raw and not path.exists()
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
assert len(targets) == 4
report = ROOT / 'RELATORIO_TROCA_RESOLVENTE_TOMITA_DEV.md'
create(report, f'''# Troca do resolvente e preparação da involução polar — DEV

{DATE}. [REAL — dois módulos/quatro alvos compilados; sem revisão independente ou integração]

R=(I+S†S)⁻¹, no H_I já construído. O resolvente envia todo H_I para D(S).
Para x∈D(S), escreva u=Rx, w=x−u=S†Su e v=Sw. A involutividade de S
e de seu adjunto máximo põe v no domínio de S†S e dá S†Sv=Su.
Então v+S†Sv=Sx e a identidade inversa do resolvente dá R(Sx)=S(x−Rx).
Logo SRx=Sx−RSx, com todas as inclusões de domínios explícitas.

Os lemas existentes ResolventGraphTransport preservam o gráfico de B pela
ação de R. Com S=UB, obtém-se URz=(I−R)Uz inicialmente em Ran B.
A densidade de Ran B e a continuidade dos dois lados estendem a identidade
a todo H_I. Esse é o segundo resultado do pacote. Não foi assumido U²=I.

As quatro declarações usam apenas propext, Classical.choice e Quot.sound.
Uma tentativa de ScalarTomitaPolarResolvent terminou com timeout na reescrita;
foi substituída por congrArg explícito. O log rc1 foi preservado e excluído,
e o novo pin passou com rc0. Nenhum dos quatro alvos integra os nove/41.

[OPEN — rota proposta, ainda NÃO compilada] Para Q=√(I−R) e P₀=√R, provar
U P₀=Q U e U Q=P₀ U por conjugação antiunitária de operadores positivos e
unicidade da raiz limitada (Mathlib CFC.sqrt_unique). O candidato conjugado
U T U⁻¹ é linear complexo, embora U seja antilinear; sua positividade deve
ser demonstrada, sem supor previamente U=U⁻¹. O teorema já existente
ChatgptAudit.Continuous050.antiunitary_inner_conj pode ser reutilizado.

Se essas trocas forem provadas, S(P₀v)=UQv e S²=I dão U²P₀v=P₀v.
A densidade da imagem de P₀ permitirá U²=I. Essa é uma estratégia matemática
a verificar, não uma prova Lean já disponível. KMS, peso, traço e condições
físicas continuam posteriores. Não foi construído novo certificado de gate.

Mãe integrada histórica `{sha(ROOT / 'tomita_root_custody.json')}`;
pacote polar DEV `{sha(ROOT / 'tomita_polar_draft_status.json')}`.
Toda escrita restrita à cópia. Original não importado/executado/modificado.
'''.encode('utf-8'))
record = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_sha256': sha(report),
    'parent_polar_draft_sha256': sha(ROOT / 'tomita_polar_draft_status.json'),
    'resolvent_flip_on_Tomita_domain': True, 'polar_resolvent_flip_on_H': True,
    'sqrt_flip_proved': False, 'polar_involution_proved': False,
    'integrated': False, 'gate_changed': False, 'full_goal_complete': False}
manifest = ROOT / 'tomita_resolvent_flip_draft_status.json'
create(manifest, json.dumps(record, ensure_ascii=False, indent=2).encode())
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'manifest_sha256': sha(manifest)}))
