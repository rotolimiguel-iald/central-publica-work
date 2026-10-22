"""Prepare the isolated fixed-core locality stage; preserve byte backups."""
import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MODULES = ['FixedCoreShiftCommutation', 'FourierUniqueness', 'CharacterLocality',
           'L2MeasurableCut', 'FixedCoreLocality']


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
    ns = 'TGLV350.Fourier.' if name == 'FourierUniqueness' else 'TGLV350.Regular.'
    targets.extend(ns + target for target in re.findall(r'^#print axioms ([\w.]+)$', text, re.M))
assert len(targets) == 16

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
assert "'FixedCoreShiftCommutation'" not in text
text = once(text, "'BoundedFiniteSquares']", "'BoundedFiniteSquares', " + ', '.join(map(repr, MODULES)) + ']')
text = once(text, "'import TGLExt.V350BoundedFiniteSquares\\n')",
            "'import TGLExt.V350BoundedFiniteSquares\\n'\n" +
            '\n'.join("               'import TGLExt.V350" + n + "\\n'" for n in MODULES) + ')')
anchor = '#print axioms TGLV350.Regular.boundedFiniteSquares_strong_approximation\n'
text = once(text, anchor, anchor + '\n-- Locality of the fixed algebra, not yet constant-fibre identification.\n' +
            ''.join('#print axioms ' + n + '\n' for n in targets))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350BoundedFiniteSquares.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + n + ".lean',\n" for n in MODULES))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
control = '''check('fixed_core_locality_does_not_discharge_base_trace_or_physics',
      all(name in axioms for name in (
          'TGLV350.Fourier.fourier_integral_ae_injective',
          'TGLV350.Regular.dualFixedCore_commutes_shift_and_character',
          'TGLV350.Regular.character_commutation_local_pairing',
          'TGLV350.Regular.character_commutation_measurableCut',
          'TGLV350.Regular.dualFixedCore_commutes_measurableCut'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
'''
text = once(text, "report = {'checks': checks", control + "report = {'checks': checks")
save(path, text)

template = '''# Localidade da álgebra fixa do core regular

{date}. [REAL — Lean, cópia isolada da v350]

Se B pertence à álgebra fixa F da ação dual no core regular N, B comuta
com as translações ordinárias e preserva todo recorte mensurável do espaço.
Não há hipótese de medida finita para o conjunto recortado nem de
continuidade pontual dos vetores L².

## Construção

FixedCoreShiftCommutation prova que as translações ordinárias comutam com
os geradores do core e portanto pertencem ao seu comutante. A condição
de ponto fixo da ação dual dá a comutação com os caracteres.

FourierUniqueness prova unicidade quase em toda parte de funções L1 a
partir de suas integrais de Fourier, usando inversão em testes de Schwartz.
CharacterLocality aplica esse resultado aos pareamentos integráveis
⟨B* f(x),g(x)⟩ e ⟨f(x),B g(x)⟩. A comutação com todos os caracteres
iguala suas transformadas e por isso os pareamentos locais quase em toda parte.

L2MeasurableCut constrói multiplicação por indicadora como operador
linear contínuo de norma no máximo um. FixedCoreLocality integra a
igualdade dos pareamentos sobre cada conjunto mensurável e conclui
P_S B = B P_S. O argumento não usa avaliação pontual contínua em L².

## Verificação e alcance

{target_count} novos alvos; axiomas apenas propext, Classical.choice e Quot.sound.
{build_count} registros Lean integrados válidos; {controls} controles;
{audit_count} declarações distintas no Audit; {embedded_count} arquivos embutidos.
Build incremental, sem recompilação integral de Mathlib.
[Revisão independente](<{review_path}>).

Original preservado: `{base_sha}`.
Cópia integrada: `{working_sha}`.
Corpo Python fora do dicionário Lean inalterado por AST em relação à etapa
anterior; gate legado e seis flags maiores de core/canto/witness/H1/H2/H3 inalterados.

[OPEN] Ainda é necessário provar que a ação local é uma mesma ação na fibra
em todos os pontos, e que essa ação pertence à álgebra original. A inclusão
F⊆base não foi concluída. Não se usou Stone–von Neumann nem um teorema de
decomposição espectral como hipótese disfarçada.

Permanecem a correspondência geral espectral/predual, a interface padrão
de peso operatorial e estado modular/gerador/perturbação para o traço
canônico fiel, normal e semifinito. Three Locks/H1, H2/H3 físicos na mesma
realização, interações/BRST/QME/anomalias/UV, contrato ampliado consumido
pelo gate e runtime integral permanecem abertos.

O original não foi importado ou executado. O inventário estático de I/O
continua histórico e não libera a execução da cópia atual. Objetivo geral ativo.
'''
save(ROOT / 'MINUTA_LOCALIDADE_FIXA.md', template, new=True)

text = (ROOT / 'record_bounded_values_progress.py').read_text(encoding='utf-8')
text = text.replace('Record the reviewed bounded fixed-algebra dual values', 'Record the reviewed fixed-core locality')
text = once(text, "MODULES = ['BoundedDualValues', 'BoundedFiniteSquares']", 'MODULES = ' + repr(MODULES))
for old, new in (
    ('TETELESTAI_V350_BOUNDED_DUAL_VALUES_20260912', 'TETELESTAI_V350_FIXED_CORE_LOCALITY_20260912'),
    ('REVIEW_BOUNDED_DUAL_VALUES.md', 'REVIEW_FIXED_CORE_LOCALITY.md'),
    ("ROOT / 'semifinite_ideal_custody.json'", "ROOT / 'bounded_values_custody.json'"),
    ('RELATORIO_VALORES_LIMITADOS.md', 'RELATORIO_LOCALIDADE_FIXA.md'),
    ('MINUTA_VALORES_LIMITADOS.md', 'MINUTA_LOCALIDADE_FIXA.md'),
    ("name == 'FourierL1L2'", "name == 'FourierUniqueness'")):
    text = text.replace(old, new)
start, end = text.index("note = f'''"), text.index('surfaces = ')
note = """note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] FixedCoreShiftCommutation, FourierUniqueness,
CharacterLocality, L2MeasurableCut e FixedCoreLocality: operadores B∈F
comutam com as translações ordinárias e com todo recorte mensurável P_S.
Unicidade da transformada de Fourier em L1 identifica os pareamentos
locais; integração sobre S dá P_S B=B P_S. Nenhuma finitude de medida
de S nem avaliação pontual contínua em L² foi presumida.
{len(targets)} alvos novos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações no Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python fora do dicionário Lean
inalterado por AST; gate legado inalterado.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] F=base: falta identificar a ação na fibra como constante e como
elemento da álgebra original. Correspondência espectral/predual, interface
de peso operatorial, estado modular/gerador/perturbação/traço canônico,
Three Locks/H1, H2/H3 físicos, interações/BRST/QME/anomalias/UV, contrato
ampliado do gate e runtime integral continuam abertos. Seis flags maiores
false. O inventário de I/O é histórico, sem liberação do runtime atual.
Objetivo ativo; original não importado/executado.
'''
"""
text = text[:start] + note + text[end:]
text = once(text, "'RELATORIO_IDEAL_SEMIFINITO.md')]",
            "'RELATORIO_IDEAL_SEMIFINITO.md', 'RELATORIO_VALORES_LIMITADOS.md')]")
text = once(text, "'finite_values_as_bounded_operators_in_F': True,",
            "'finite_values_as_bounded_operators_in_F': True,\n"
            "    'fixed_algebra_commutes_with_all_measurable_cuts': True,\n"
            "    'fixed_algebra_commutes_with_ordinary_translations': True,")
text = once(text, "write_atomic(ROOT / 'bounded_values_custody.json'", "write_atomic(ROOT / 'fixed_locality_custody.json'")
compile(text, 'record_fixed_locality_progress.py', 'exec')
save(ROOT / 'record_fixed_locality_progress.py', text, new=True)

text = (ROOT / 'verify_bounded_values_custody.py').read_text(encoding='utf-8')
for old, new in (
    ('bounded_values_custody', 'fixed_locality_custody'),
    ('bounded_values_integrated_and_reviewed', 'fixed_locality_integrated_and_reviewed'),
    ('RELATORIO_VALORES_LIMITADOS.md', 'RELATORIO_LOCALIDADE_FIXA.md'),
    ('MINUTA_VALORES_LIMITADOS.md', 'MINUTA_LOCALIDADE_FIXA.md'),
    ('REVIEW_BOUNDED_DUAL_VALUES.md', 'REVIEW_FIXED_CORE_LOCALITY.md'),
    ('TETELESTAI_V350_BOUNDED_DUAL_VALUES_20260912', 'TETELESTAI_V350_FIXED_CORE_LOCALITY_20260912')):
    text = text.replace(old, new)
compile(text, 'verify_fixed_locality_custody.py', 'exec')
save(ROOT / 'verify_fixed_locality_custody.py', text, new=True)
print({'prepared_targets': len(targets), 'recording_pending_review': True})
