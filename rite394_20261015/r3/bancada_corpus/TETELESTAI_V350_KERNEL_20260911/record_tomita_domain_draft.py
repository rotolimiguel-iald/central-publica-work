"""Freeze the exact-domain proof batch before independent review."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
NAMES = ['RealGraphCore', 'ScalarTomitaGraphCore', 'PartialSquareGraphCore',
         'GraphCoreNormTransfer', 'ScalarTomitaRootGraphCore', 'ScalarTomitaRootDomain']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert not path.exists() and raw
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

modules, targets = {}, {}
for name in NAMES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    binary = ROOT / 'build/TGLV350' / (name + '.olean')
    history = [(p, json.loads(p.read_bytes())) for p in sorted((ROOT / 'logs').glob(name + '_*.json'))]
    accepted = [(p,v) for p,v in history if v['returncode'] == 0 and
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
        'failed_attempts': [str(p) for p,v in history if v['returncode']]}
assert len(targets) == 25
parent = ROOT / 'tomita_root_custody.json'
parent_data = json.loads(parent.read_bytes())
assert sha(ROOT / 'um.py') == parent_data['working_sha256']
report_path = ROOT / 'RELATORIO_DOMINIO_RAIZ_TOMITA_DEV.md'
report = f'''# Igualdade exata D(B)=D(S) e energia no domínio inteiro — DEV

{DATE}. [REAL — seis módulos/25 alvos compilados; revisão independente e integração pendentes]

O operador continua sendo S, fecho do gráfico original A↦A* no H_I construído
para o ideal finito. Seu adjunto máximo fornece A=S†S e a etapa anterior fornece
a raiz positiva auto-adjunta B com B²=A como mapas parciais. Não se troca peso,
representação, suporte ou modelo espectral para obter a igualdade de domínios.

1. No gráfico REAL fechado de um mapa real-linear, uma família resolvente fraca
   com valores em C mostra que o gráfico restrito a C tem complemento ortogonal
   zero no gráfico inteiro. Seguem sequências convergentes em ambas as coordenadas.
2. Para S, a equação u+Au=z e o pareamento com o adjunto provam que D(A) é núcleo
   do gráfico de S. Não se usa somente densidade na norma de H_I.
3. Para B, simetria e B²=A fornecem o pareamento contra TODO D(B); a mesma família
   resolvente mostra que D(A) é núcleo do gráfico de B.
4. As normas de S e B em D(A) são iguais, pelo quadrado da energia já provado.
   Em cada aproximação de gráfico, a sequência de imagens pelo outro operador
   é Cauchy porque as normas de todas as diferenças coincidem. Completude de H_I
   e fechamento do gráfico do outro operador dão a inclusão de domínios.
5. Aplicado nos dois sentidos, isso dá D(B)=D(S). A continuidade da norma e a
   unicidade dos limites dão ‖Bx‖=‖Sx‖ e ‖Bx‖²=‖Sx‖² em TODO esse domínio.

Todos os 25 alvos usam apenas propext, Classical.choice e Quot.sound. Os lemas
genéricos exibem suas hipóteses; os seis alvos finais de ScalarTomitaRootDomain
usam somente P e os vetores tipados. Não recebem a igualdade final como premissa.
Os domínios são submódulos, com inclusões e igualdade de subtipos explícitas.

[OPEN] O fator antiunitário polar ainda não foi construído neste pacote. KMS,
identificação com o peso e seu domínio máximo, traço canônico e escala dual,
canto contínuo/Three Locks, H1/H2/H3 físicos compatíveis, setor quântico interagente,
contrato completo consumido pelo gate e runtime integral continuam pendentes.
D(B)=D(S) não afirma D(B)=H_I, invariância de D(B) sob B ou gap espectral.

Os relatórios anteriores que registravam esta igualdade como aberta permanecem
históricos. `graph_core_draft_status.json` era o corte de dois módulos/10 alvos;
este manifesto novo amplia esse corte sem editar seus bytes. O novo pacote não
foi incorporado às contagens integradas de cinco/30 da raiz.

Tentativas rc1 preservadas: colisão de nome de instância real, sentido de uma
identidade de produto interno, coerção de subtipo, inclusão explícita de uma
hipótese de seção e timeout de reescrita no tipo concreto. O timeout foi resolvido
com termos explícitos de igualdade, sem elevar a conclusão a axioma. Logs com
sorryAx ou sem binário válido não compõem a evidência aceita.

Cópia integrada antecedente: `{sha(ROOT / 'um.py')}`.
Mãe de custódia: `{sha(parent)}`. Nenhuma promoção de gate ou execução do monólito.
'''
if report_path.exists():
    existing = report_path.read_text(encoding='utf-8')
    previous_date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}', existing).group()
    assert report.replace(DATE, previous_date).encode('utf-8') == report_path.read_bytes()
else:
    create(report_path, report.encode('utf-8'))
record = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_sha256': sha(report_path),
    'parent_custody_sha256': sha(parent), 'integrated_working_sha256': sha(ROOT / 'um.py'),
    'root_domain_equals_tomita_domain': True, 'energy_on_full_Tomita_domain': True,
    'polar_antiunitary_constructed': False, 'KMS_proved': False,
    'canonical_trace_constructed': False, 'gate_changed': False, 'integrated': False,
    'full_goal_complete': False}
create(ROOT / 'tomita_root_domain_draft_status.json', json.dumps(record, ensure_ascii=False, indent=2).encode())
print(json.dumps({'modules': len(modules), 'targets': len(targets),
    'manifest_sha256': sha(ROOT / 'tomita_root_domain_draft_status.json'), 'status': record['status']}))
