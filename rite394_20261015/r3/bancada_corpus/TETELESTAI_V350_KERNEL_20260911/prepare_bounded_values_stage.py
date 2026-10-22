"""Prepare integration and recording for bounded dual values in the isolated copy."""
import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MODULES = ('BoundedDualValues', 'BoundedFiniteSquares')


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
    text = (ROOT / 'kernel/TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    targets.extend('TGLV350.Regular.' + target for target in
                   re.findall(r'^#print axioms ([\w.]+)$', text, re.M))

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
assert "'BoundedDualValues'" not in text
text = once(text, "'DualSemifiniteIdeal']",
    "'DualSemifiniteIdeal', 'BoundedDualValues', 'BoundedFiniteSquares']")
text = once(text, "'import TGLExt.V350DualSemifiniteIdeal\\n')",
    "'import TGLExt.V350DualSemifiniteIdeal\\n'\n"
    "               'import TGLExt.V350BoundedDualValues\\n'\n"
    "               'import TGLExt.V350BoundedFiniteSquares\\n')")
text = once(text, '#print axioms TGLV350.Regular.finiteDualLeftIdeal_strong_approximation\n',
    '#print axioms TGLV350.Regular.finiteDualLeftIdeal_strong_approximation\n\n'
    '-- Bounded dual values in the same fixed algebra and dense finite-square inputs.\n'
    '-- The identification F=base and canonical trace remain separate obligations.\n'
    + ''.join('#print axioms ' + name + '\n' for name in targets))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
text = once(text, "'TGLExt/V350DualSemifiniteIdeal.lean',\n",
    "'TGLExt/V350DualSemifiniteIdeal.lean',\n"
    "                 'TGLExt/V350BoundedDualValues.lean',\n"
    "                 'TGLExt/V350BoundedFiniteSquares.lean',\n")
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
control = '''check('bounded_values_in_fixed_algebra_do_not_discharge_base_trace_or_physics',
      all('TGLV350.Regular.' + name in axioms for name in (
          'dualQuadraticIntegral_eq_boundedCutLimit', 'boundedDualValue_unique',
          'boundedDualValue_dual_fixed', 'exists_boundedDualValue_in_fixedCore',
          'HasFiniteDualSquare.exists_bounded_value', 'regularAverage_bounded_value',
          'boundedFiniteSquares_strong_approximation'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
'''
text = once(text, "report = {'checks': checks", control + "report = {'checks': checks")
save(path, text)

template = '''# Valores limitados do peso dual na álgebra fixa

{date}. [REAL — Lean, cópia isolada da v350]

Toda forma dual positiva com cota uniforme q_A(v)≤C||v||² é representada
por um único operador positivo limitado B da álgebra fixa F do mesmo core
regular N. O resultado é q_A(v)=ofReal(re⟨v,Bv⟩), com B≤C·I.
A cota uniforme era conhecida; a representação em F foi construída nesta etapa.

## Construção

BoundedDualValues começa pela ordem e unicidade de operadores autoadjuntos
determinadas por todas as avaliações quadráticas. A cota de q_A limita cada
corte positivo C_n por C·I. O teorema monotônico de operadores produz o limite
forte B; o fechamento da mesma álgebra dá B∈N. A igualdade entre q_A e o
supremo dos cortes identifica a forma de B. A invariância dual da forma,
junto com a unicidade, prova θ_s(B)=B e portanto B∈F. As únicas conversões
para reais nesta prova são de valores ofReal já finitos e não negativos.

BoundedFiniteSquares aplica essa representação ao ideal anterior. Para todo
A em seu domínio, q_(A* A) tem valor limitado positivo em F. Para as médias
X_h=h^(-1)∫_0^h Λ_t dt, h>0, esse valor é exatamente h^(-1)·I, com a
normalização Fourier/Haar já demonstrada. Para qualquer A∈N, A X_h→A
fortemente e os quadrados dos aproximantes têm valores limitados em F.

## Verificação e alcance

{target_count} novos alvos, axiomas apenas propext, Classical.choice e Quot.sound.
{build_count} registros Lean integrados válidos; {controls} controles;
{audit_count} declarações distintas no Audit; {embedded_count} arquivos embutidos.
Essa contagem descreve o build incremental e não recompilação integral de Mathlib.
[Revisão independente](<{review_path}>).

Original preservado: `{base_sha}`.
Cópia integrada: `{working_sha}`.
Corpo Python fora do dicionário Lean inalterado por AST em relação à etapa
anterior; gate legado e seis flags maiores de core/canto/witness/H1/H2/H3 inalterados.

[OPEN] Identificação F=base; correspondência geral espectral/predual;
interface padrão de peso operatorial e estado modular/gerador/perturbação
que produzem o traço canônico fiel, normal e semifinito. Three Locks/H1,
H2/H3 físicos na mesma realização, interações/BRST/QME/anomalias/UV,
contrato ampliado consumido pelo gate e runtime integral permanecem abertos.
O critério de densidade agora inclui valores limitados efetivos em F; isso
não identifica por si só a álgebra de base nem constrói o traço escalar.

O monólito original não foi importado ou executado. O runtime integral da
cópia continua pendente. O inventário estático de I/O é histórico, com seu
hash de origem preservado; não libera a execução da cópia atual.
Objetivo geral ativo; nenhuma confirmação física é reivindicada.
'''
save(ROOT / 'MINUTA_VALORES_LIMITADOS.md', template, new=True)

text = (ROOT / 'record_semifinite_ideal_progress.py').read_text(encoding='utf-8')
text = once(text, 'Record the reviewed fixed-algebra form affiliation',
            'Record the reviewed bounded fixed-algebra dual values')
text = once(text, "MODULES = ['RegularApproximation', 'FourierL1L2', 'RegularFiniteWeight', 'DualSemifiniteIdeal']",
            "MODULES = ['BoundedDualValues', 'BoundedFiniteSquares']")
text = text.replace('TETELESTAI_V350_SEMIFINITE_IDEAL_20260912',
                    'TETELESTAI_V350_BOUNDED_DUAL_VALUES_20260912')
text = text.replace('REVIEW_REGULAR_SEMIFINITE_ROUTE.md', 'REVIEW_BOUNDED_DUAL_VALUES.md')
text = once(text, "ROOT / 'fixed_weight_custody.json'", "ROOT / 'semifinite_ideal_custody.json'")
text = text.replace('RELATORIO_IDEAL_SEMIFINITO.md', 'RELATORIO_VALORES_LIMITADOS.md')
text = text.replace('MINUTA_IDEAL_SEMIFINITO.md', 'MINUTA_VALORES_LIMITADOS.md')
start, end = text.index("note = f'''"), text.index('surfaces = ')
note = """note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] BoundedDualValues e BoundedFiniteSquares: a cota
uniforme de q_A produz um operador positivo limitado B∈F, no mesmo core N,
com q_A(v)=ofReal(re⟨v,Bv⟩). Cortes positivos crescentes limitados por C·I
convergem fortemente; fechamento de N, igualdade das formas e invariância
dual dão a representação única em F. O ideal de quadrados finitos tem agora
valores limitados efetivos em F; para X_h, h>0, o valor é h^(-1)·I. A X_h
aproxima fortemente todo A∈N com quadrados de valor limitado.
{len(targets)} alvos novos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações no Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python fora do dicionário Lean
inalterado por AST; gate legado inalterado.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] F=base; correspondência espectral/predual geral; interface padrão de
peso operatorial e estado modular/gerador/perturbação/traço canônico;
Three Locks/H1; H2/H3 físicos na mesma realização; interações/BRST/QME/anomalias/UV;
contrato ampliado consumido pelo gate; runtime integral. Seis flags maiores
permanecem false e o objetivo ativo. O critério de densidade possui valores
limitados em F, mas não fornece sozinho a identificação da base ou o traço.
Inventário de I/O histórico preservado, sem liberação de runtime atual.
Monólito original não importado/executado; runtime integral da cópia pendente.
'''
"""
text = text[:start] + note + text[end:]
text = once(text, "'RELATORIO_AFILIACAO_DA_FORMA_FIXA.md', 'RELATORIO_PESO_FORMA_FIXA.md')]",
    "'RELATORIO_AFILIACAO_DA_FORMA_FIXA.md', 'RELATORIO_PESO_FORMA_FIXA.md',\n"
    "    'RELATORIO_IDEAL_SEMIFINITO.md')]")
text = once(text, "'finite_values_as_bounded_operators_in_F': False",
                  "'finite_values_as_bounded_operators_in_F': True")
text = once(text, "write_atomic(ROOT / 'semifinite_ideal_custody.json'",
                  "write_atomic(ROOT / 'bounded_values_custody.json'")
compile(text, 'record_bounded_values_progress.py', 'exec')
save(ROOT / 'record_bounded_values_progress.py', text, new=True)

text = (ROOT / 'verify_semifinite_ideal_custody.py').read_text(encoding='utf-8')
for old, new in (
    ('semifinite_ideal_custody', 'bounded_values_custody'),
    ('semifinite_ideal_integrated_and_reviewed', 'bounded_values_integrated_and_reviewed'),
    ('RELATORIO_IDEAL_SEMIFINITO.md', 'RELATORIO_VALORES_LIMITADOS.md'),
    ('MINUTA_IDEAL_SEMIFINITO.md', 'MINUTA_VALORES_LIMITADOS.md'),
    ('REVIEW_REGULAR_SEMIFINITE_ROUTE.md', 'REVIEW_BOUNDED_DUAL_VALUES.md'),
    ('TETELESTAI_V350_SEMIFINITE_IDEAL_20260912', 'TETELESTAI_V350_BOUNDED_DUAL_VALUES_20260912')):
    text = text.replace(old, new)
compile(text, 'verify_bounded_values_custody.py', 'exec')
save(ROOT / 'verify_bounded_values_custody.py', text, new=True)
print({'prepared_targets': len(targets), 'recording_pending_review': True})
