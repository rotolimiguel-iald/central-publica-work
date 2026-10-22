"""Freeze the involutive polar development, separate from the integrated antiunitary stage."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
NAMES = ['ScalarTomitaResolventFlip', 'ScalarTomitaPolarResolvent', 'AntiunitaryPositiveConjugation', 'ScalarTomitaPolarInvolution']

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
assert len(targets) == 19
report = ROOT / 'RELATORIO_INVOLUCAO_POLAR_TOMITA_DEV.md'
create(report, f"""# Involução do fator polar no H_I original — DEV

{DATE}. [REAL — quatro módulos/19 alvos compilados; revisão independente e integração pendentes]

O pacote precedente integrou nove módulos/41 alvos e construiu U antiunitário,
S=UB e D(B)=D(S). Este pacote separado prova U²=I usando esse mesmo S, B e U.

1. As involuções de S e S†, com a equação do resolvente, dão SR=(I−R)S em D(S).
2. R preserva o gráfico de B. S=UB e a densidade de Ran B dão UR=(I−R)U em H_I.
3. A conjugação U T U⁻¹ é linear complexa e preserva positividade, pelo produto
   interno antiunitário já provado em GenericAntilinearAdjoint. Não se usa U=U⁻¹.
   CFC.sqrt_unique dá a conjugação das raízes positivas limitadas.
4. Escrevendo P₀=√R e Q=√(I−R), obtêm-se UP₀=QU e UQ=P₀U.
5. B(P₀v)=Qv e S=UB dão S(P₀v)=UQv. A segunda troca permite aplicar S novamente;
   S²=I e a primeira troca dão U²P₀v=P₀v. Ran P₀ é denso, logo U²=I em todo H_I.

Os 19 alvos usam somente propext, Classical.choice e Quot.sound. Os tipos finais
recebem P e vetores, não a involução polar como hipótese. O núcleo GNS, espaço,
produto interno, raiz positiva e fator U são os objetos construídos anteriormente.
Os logs rc1 permanecem no manifesto, sem servir de evidência: timeout de reescrita,
simplificação da parte real, extensionalidade excessiva até igualdade quase em toda
parte e limites de busca de instâncias. A fonte final e seus parâmetros efetivos
estão pinados. A tentativa alternativa de instâncias locais no probe foi
descartada e não é importada. A definição genérica hilbertPositiveSqrt fixa
as instâncias canônicas antes de especializar H; nenhuma mudança de orçamento de elaboração é tratada como axioma.

[OPEN] Isto não identifica a álgebra/peso com seu domínio máximo nem prova KMS,
fluxo modular, traço/escala dual, canto Three Locks, H1/H2/H3 físicos compatíveis,
setor quântico interagente, certificado completo ou runtime integral. U pode ser
usado como conjugação da decomposição polar deste S; sua identificação com os
outros candidatos chamados J exige uma ponte explícita. Não se promove gate.

O relato anterior de dois/quatro alvos permanece histórico. Seu caminho até U²=I
foi aqui percorrido em DEV. Os nove/41 integrados e seus relatórios continuam no
estado selado; estes quatro/19 ainda não entraram no embutido nem no Audit integrado.
Mãe integrada `{sha(ROOT / 'tomita_polar_custody.json')}`; cópia
`{sha(ROOT / 'um.py')}`. Original não executado/importado/modificado.
""".encode('utf-8'))
record = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_sha256': sha(report),
    'parent_custody_sha256': sha(ROOT / 'tomita_polar_custody.json'),
    'previous_resolvent_flip_draft_sha256': sha(ROOT / 'tomita_resolvent_flip_draft_status.json'),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'polar_involution_proved': True, 'sqrt_flip_proved': True,
    'modular_weight_identified': False, 'KMS_proved': False,
    'canonical_trace_constructed': False, 'integrated': False,
    'gate_changed': False, 'full_goal_complete': False,
    'discarded_probe_logs': [str(p) for p in sorted((ROOT/'logs').glob('ScalarTomitaRealEndProbe_*.json'))]}
manifest = ROOT / 'tomita_involution_draft_status.json'
create(manifest, json.dumps(record, ensure_ascii=False, indent=2).encode())
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'manifest_sha256': sha(manifest)}))
