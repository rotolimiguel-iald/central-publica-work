"""Prepare the scalar dual weight stage without promoting it to a trace."""
import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MODULES = ['FixedBaseEquivalence', 'BoundedBaseDualValues', 'ScalarDualWeightFaithfulness', 'ScalarDualWeight']


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def save(path, text, new=False):
    assert path.resolve().is_relative_to(ROOT)
    if new:
        assert not path.exists(), path
    if path.exists():
        before = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as handle:
            handle.write(before)
        assert backup.read_bytes() == before
    raw = text.encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as handle:
        handle.write(raw)
    assert temporary.read_bytes() == raw and len(raw) > 0
    temporary.replace(path)
    assert path.read_bytes() == raw


targets = []
for name in MODULES:
    source = (ROOT / 'kernel/TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    targets += ['TGLV350.Regular.' + t for t in re.findall(r'^#print axioms ([\w.]+)$', source, re.M)]
assert len(targets) == 23

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
assert "'ScalarDualWeight'" not in text
text = once(text, "'FixedCoreBaseIdentification']", "'FixedCoreBaseIdentification', " + ', '.join(map(repr, MODULES)) + ']')
text = once(text, "'import TGLExt.V350FixedCoreBaseIdentification\\n')",
            "'import TGLExt.V350FixedCoreBaseIdentification\\n'\n" +
            '\n'.join("               'import TGLExt.V350" + n + "\\n'" for n in MODULES) + ')')
anchor = '#print axioms TGLV350.Regular.dualFixedCore_existsUnique_base\n'
text = once(text, anchor, anchor + '\n-- Faithful normal scalar dual weight and square-finite strong density; no trace yet.\n' +
            ''.join('#print axioms ' + n + '\n' for n in targets))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350FixedCoreBaseIdentification.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + n + ".lean',\n" for n in MODULES))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
control = '''check('scalar_dual_weight_does_not_discharge_canonical_trace_or_physical_obligations',
      all('TGLV350.Regular.' + name in axioms for name in (
          'fixedBaseOrderIso', 'finiteBaseValues_strong_approximation',
          'dualQuadraticIntegral_vacuum_faithful', 'scalarDualWeight_add',
          'scalarDualWeight_scale', 'scalarDualWeight_faithful',
          'scalarDualWeight_normal', 'scalarDualWeight_square_finite_strong_density',
          'scalarDualWeight_bounded_base_value'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
'''
text = once(text, "report = {'checks': checks", control + "report = {'checks': checks")
save(path, text)

template = '''# Peso escalar dual fiel e normal

{date}. [REAL — Lean, cópia isolada da v350]

O peso ν(A)=q_A(η), com η=1_(0,1]Ω, foi construído no cone positivo da
mesma álgebra regular N. É aditivo, homogêneo para escalares não negativos,
monótono, fiel e normal para supremos dirigidos internos. O ideal complexo
esquerdo já construído é fortemente denso e todos os seus quadrados têm ν
finito. Estas são as propriedades expressas pelos teoremas deste pacote.
ν ainda não foi identificado como traço nem teve seu grupo modular provado.

## Construção e ligação à base

FixedBaseEquivalence empacota a amplificação M→F como equivalência de
álgebras com involução e isomorfismo de ordem; a inversa é e*Be.
BoundedBaseDualValues coloca os valores positivos limitados efetivamente
em M, prova sua unicidade e a aproximação forte por entradas com quadrados
finitos. A composição usa F=imagem amplificada de M já provada.

ScalarDualWeightFaithfulness prova que η é separante para F usando Ω
separante para a mesma M. Se q_A(η)=0, o resolvente R minimizador dá Rη=η.
Como R∈F, segue R=I. Sua identidade de energia, depois da prova de finitude,
dá q_A(v)=0 para todo v, e a fidelidade da forma conclui A=0.
Não se usa toReal para disfarçar um valor infinito como zero.

ScalarDualWeight fornece as leis do peso escalar. A normalidade parte do
supremo interno em N, sem receber um limite forte externo como hipótese.
A densidade usa A·X_h→A fortemente, h>0, com X_h a média regular já
construída. A condição de quadrado finito fornece uma única cota para todos
os vetores e, em η de norma 1, um valor escalar finito. Não se reivindica
convergência em norma de operadores nem finitude de ν em toda N+.

Quando o valor operatorial é limitado e vale fibre(D), a leitura escalar
é exatamente ofReal⟨Ω,DΩ⟩. A ligação com o estado original é demonstrada
nesse caso. A correspondência geral espectral/predual permanece separada.

## Verificação e alcance

{target_count} alvos novos, axiomas somente propext, Classical.choice e Quot.sound.
{build_count} registros Lean integrados válidos; {controls} controles;
{audit_count} declarações no Audit; {embedded_count} arquivos embutidos.
Build incremental, sem recompilação integral de Mathlib.
[Revisão independente](<{review_path}>).

Original preservado: `{base_sha}`. Cópia integrada: `{working_sha}`.
Corpo Python fora do dicionário Lean inalterado por AST em relação à etapa
anterior; gate legado e seis flags maiores preservados.

[OPEN] Identificação do grupo modular de ν/condição KMS, gerador afiliado,
perturbação e traço canônico com escala dual. Permanecem a interface geral
de peso operatorial/predual, Three Locks/H1, H2/H3 físicos na mesma
realização, interações/BRST/QME/anomalias/UV, contrato ampliado consumido
pelo gate e runtime integral isolado. Invariância por um fluxo candidato
não basta para identificá-lo como grupo modular. As propriedades de ν
não substituem essas construções. Inventário I/O histórico; original não
importado/executado. Objetivo geral ativo.
'''
save(ROOT / 'MINUTA_PESO_ESCALAR_DUAL.md', template, new=True)

text = (ROOT / 'record_fixed_base_progress.py').read_text(encoding='utf-8')
text = text.replace('Record the reviewed fixed-base identification', 'Record the reviewed scalar dual weight')
text = re.sub(r'^MODULES = .*$', 'MODULES = ' + repr(MODULES), text, flags=re.M)
for old, new in (
    ('TETELESTAI_V350_FIXED_BASE_20260912', 'TETELESTAI_V350_SCALAR_WEIGHT_20260912'),
    ('REVIEW_FIXED_CORE_BASE.md', 'REVIEW_SCALAR_DUAL_WEIGHT.md'),
    ("ROOT / 'constant_fibre_custody.json'", "ROOT / 'fixed_base_custody.json'"),
    ('RELATORIO_BASE_FIXA.md', 'RELATORIO_PESO_ESCALAR_DUAL.md'),
    ('MINUTA_BASE_FIXA.md', 'MINUTA_PESO_ESCALAR_DUAL.md')):
    text = text.replace(old, new)
start, end = text.index("note = f'''"), text.index('surfaces = ')
note = """note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] Peso escalar ν(A)=q_A(η), η=eΩ, no cone positivo
da mesma N: zero, aditividade, homogeneidade positiva, monotonia, fidelidade
e normalidade para supremos dirigidos internos. O ideal complexo esquerdo
de quadrados finitos já construído é fortemente denso e seus quadrados têm
ν finito. A prova de fidelidade usa η separante para F e Rη=η⇒R=I,
seguida da identidade de energia com finitude explícita.
A amplificação M→F está empacotada como equivalência de álgebras e ordem;
valores positivos limitados do peso estão em M e ν=f_Ω nesses valores.
Quatro módulos; {len(targets)} alvos novos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações no Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python fora do dicionário Lean
inalterado por AST; gate legado inalterado.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Grupo modular de ν/KMS, gerador afiliado, perturbação e traço
canônico com escala dual; correspondência geral espectral/predual e
interface padrão de peso operatorial; Three Locks/H1, H2/H3 físicos,
interações/BRST/QME/anomalias/UV, contrato ampliado e runtime integral.
ν não é promovido a traço. Seis flags maiores false. Inventário I/O histórico,
sem liberação do runtime atual. Objetivo ativo; original não importado/executado.
'''
"""
text = text[:start] + note + text[end:]
text = once(text, "'RELATORIO_LOCALIDADE_FIXA.md', 'RELATORIO_FIBRA_CONSTANTE.md')]",
            "'RELATORIO_LOCALIDADE_FIXA.md', 'RELATORIO_FIBRA_CONSTANTE.md', 'RELATORIO_BASE_FIXA.md')]")
text = once(text, "'fixed_algebra_identified_with_base': True,",
            "'fixed_algebra_identified_with_base': True,\n"
            "    'fixed_base_algebra_and_order_equivalence': True,\n"
            "    'bounded_positive_dual_values_in_original_base': True,\n"
            "    'faithful_normal_scalar_dual_weight': True,\n"
            "    'scalar_square_finite_left_ideal_strongly_dense': True,\n"
            "    'scalar_weight_modular_group_identified': False,")
text = once(text, "write_atomic(ROOT / 'fixed_base_custody.json'", "write_atomic(ROOT / 'scalar_weight_custody.json'")
compile(text, 'record_scalar_weight_progress.py', 'exec')
save(ROOT / 'record_scalar_weight_progress.py', text, new=True)

text = (ROOT / 'verify_fixed_base_custody.py').read_text(encoding='utf-8')
for old, new in (
    ('fixed_base_custody', 'scalar_weight_custody'),
    ('fixed_base_integrated_and_reviewed', 'scalar_weight_integrated_and_reviewed'),
    ('RELATORIO_BASE_FIXA.md', 'RELATORIO_PESO_ESCALAR_DUAL.md'),
    ('MINUTA_BASE_FIXA.md', 'MINUTA_PESO_ESCALAR_DUAL.md'),
    ('REVIEW_FIXED_CORE_BASE.md', 'REVIEW_SCALAR_DUAL_WEIGHT.md'),
    ('TETELESTAI_V350_FIXED_BASE_20260912', 'TETELESTAI_V350_SCALAR_WEIGHT_20260912')):
    text = text.replace(old, new)
compile(text, 'verify_scalar_weight_custody.py', 'exec')
save(ROOT / 'verify_scalar_weight_custody.py', text, new=True)
print({'prepared_targets': len(targets), 'recording_pending_review': True})
