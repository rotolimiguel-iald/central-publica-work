"""Prepare the same-representation fixed-base theorem in the isolated copy."""
import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MODULES = ['StrongOperatorField', 'OperatorFieldFaithfulness', 'TwistedCommutantField',
           'RegularCoreCommutant', 'FixedCoreBaseIdentification']


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
    targets.extend('TGLV350.Regular.' + target for target in re.findall(r'^#print axioms ([\w.]+)$', text, re.M))
assert len(targets) == 23

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
assert "'FixedCoreBaseIdentification'" not in text
text = once(text, "'ConstantFibreIdentification']", "'ConstantFibreIdentification', " + ', '.join(map(repr, MODULES)) + ']')
text = once(text, "'import TGLExt.V350ConstantFibreIdentification\\n')",
            "'import TGLExt.V350ConstantFibreIdentification\\n'\n" +
            '\n'.join("               'import TGLExt.V350" + n + "\\n'" for n in MODULES) + ')')
anchor = '#print axioms TGLV350.Regular.dualFixedCore_eq_fibre_candidate\n'
text = once(text, anchor, anchor + '\n-- Same-representation identification of the dual-fixed algebra with the base.\n' +
            ''.join('#print axioms ' + n + '\n' for n in targets))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350ConstantFibreIdentification.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + n + ".lean',\n" for n in MODULES))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
# The earlier control checks these six flags, not a theorem of nonmembership.
text = once(text, 'constant_fibre_identification_does_not_discharge_base_membership_trace_or_physics',
            'constant_fibre_identification_preserves_six_remaining_frontier_flags')
control = '''check('fixed_base_identification_preserves_trace_corner_and_physical_obligations',
      all('TGLV350.Regular.' + name in axioms for name in (
          'operatorFieldLift', 'operatorFieldLift_faithful',
          'operatorFieldLift_commutation_reflects', 'twistedCommutantLift_mem',
          'fibre_mem_regularCore_iff', 'dualFixedCore_fibreCandidate_mem',
          'dualFixedCore_eq_amplified_base', 'dualFixedCore_existsUnique_base'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
'''
text = once(text, "report = {'checks': checks", control + "report = {'checks': checks")
save(path, text)

template = '''# A álgebra fixa é a base amplificada

{date}. [REAL — Lean, cópia isolada da v350]

Na representação regular construída sobre a mesma torre e o mesmo fluxo,
a álgebra fixa da ação dual é exatamente a amplificação da álgebra original:
B∈F se, e somente se, existe C∈M com B=fibre(C). C é único e é dado por e*Be.
Isso resolve a pertença à base que estava aberta no relatório da fibra constante.

## Construção

StrongOperatorField constrói o operador de multiplicação de um campo de
operadores fortemente contínuo e uniformemente limitado no espaço L²(ℝ,H).
OperatorFieldFaithfulness prova que sua ação em L² determina o campo ponto
a ponto. A continuidade e a positividade da medida de abertos elevam a
igualdade quase sempre a igualdade em todo ponto. Para cada vetor fixado,
somente uma família enumerável de testes intervalares é reunida. Não há
hipótese de separabilidade de H nem avaliação pontual contínua em L².

Para D∈M', TwistedCommutantField constrói T_D(x)=Δ^(ix)DΔ^(-ix), com o mesmo
fluxo da torre. O campo permanece em M', é fortemente contínuo, uniformemente
limitado por ||D|| e satisfaz T_D(x)Δ^(it)=Δ^(it)T_D(x−t).
Seu operador de multiplicação comuta com as duas famílias geradoras de N.
RegularCoreCommutant estende a comutação à álgebra gerada, tratando os
adjuntos explicitamente, e coloca o operador de multiplicação em N'.

Se fibre(C)∈N, essa comutação reflete-se no campo e, no ponto zero, dá
DC=CD para todo D∈M'. Pelo bicomutante, C∈M. A etapa anterior já deu
B=fibre(C) para todo B∈F. A composição fornece F=base amplificada; a
recíproca usa a inclusão fixa já provada e a unicidade usa a fidelidade.

Nenhum estado, fator, parâmetro de torre ou representação é trocado para
obter a conclusão. A identificação é interna ao modelo modular construído;
ela não identifica esse modelo com uma geometria física de horizonte.

## Verificação e alcance

{target_count} alvos novos, com axiomas apenas propext, Classical.choice e Quot.sound.
{build_count} registros Lean integrados válidos; {controls} controles;
{audit_count} declarações no Audit; {embedded_count} arquivos embutidos.
Build incremental, sem recompilação integral de Mathlib.
[Revisão independente](<{review_path}>).

Original preservado: `{base_sha}`. Cópia integrada: `{working_sha}`.
Corpo Python fora do dicionário Lean inalterado por AST em relação à etapa
anterior. A identificação não acende as seis flags maiores nem muda o gate legado.

[OPEN] Correspondência geral espectral/predual, interface padrão de peso
operatorial, estado modular/gerador/perturbação e traço canônico fiel, normal
e semifinito. Permanecem Three Locks/H1, H2/H3 físicos na mesma realização,
interações/BRST/QME/anomalias/UV, contrato ampliado consumido pelo gate e
runtime integral isolado. A prova de F=base não fornece essas construções.
O inventário I/O permanece histórico e não libera o runtime atual.
Original não importado/executado. Objetivo geral ativo.
'''
save(ROOT / 'MINUTA_BASE_FIXA.md', template, new=True)

text = (ROOT / 'record_constant_fibre_progress.py').read_text(encoding='utf-8')
text = text.replace('Record the reviewed constant-fibre identification', 'Record the reviewed fixed-base identification')
text = re.sub(r'^MODULES = .*$', 'MODULES = ' + repr(MODULES), text, flags=re.M)
for old, new in (
    ('TETELESTAI_V350_CONSTANT_FIBRE_20260912', 'TETELESTAI_V350_FIXED_BASE_20260912'),
    ('REVIEW_UNIT_INTERVAL_PROJECTION.md', 'REVIEW_FIXED_CORE_BASE.md'),
    ("ROOT / 'fixed_locality_custody.json'", "ROOT / 'constant_fibre_custody.json'"),
    ('RELATORIO_FIBRA_CONSTANTE.md', 'RELATORIO_BASE_FIXA.md'),
    ('MINUTA_FIBRA_CONSTANTE.md', 'MINUTA_BASE_FIXA.md')):
    text = text.replace(old, new)
start, end = text.index("note = f'''"), text.index('surfaces = ')
note = """note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] F=base amplificada na mesma representação regular:
B∈F ↔ ∃ C∈M, B=fibre(C), com C único e dado por e*Be. A pertença C∈M é
provada pelo campo T_D(x)=Δ^(ix)DΔ^(-ix), D∈M': seu lift pertence a N',
a comutação em L² reflete-se ponto a ponto e em zero fornece DC=CD.
O bicomutante conclui C∈M. Cinco módulos, sem separabilidade de H nem
avaliação pontual contínua em L²; campos fortemente contínuos com limite
uniforme de norma. O OPEN C∈M/F=base do estrato anterior foi resolvido.
{len(targets)} alvos novos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações no Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python fora do dicionário Lean
inalterado por AST; gate legado inalterado.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Correspondência espectral/predual, interface de peso operatorial,
estado/gerador/perturbação/traço canônico, Three Locks/H1, H2/H3 físicos,
interações/BRST/QME/anomalias/UV, contrato ampliado e runtime integral.
Seis flags maiores false. Inventário I/O histórico, sem liberação do runtime
atual. Objetivo ativo; original não importado/executado.
'''
"""
text = text[:start] + note + text[end:]
text = once(text, "'RELATORIO_LOCALIDADE_FIXA.md')]", "'RELATORIO_LOCALIDADE_FIXA.md', 'RELATORIO_FIBRA_CONSTANTE.md')]")
text = once(text, "'constant_fibre_belongs_to_original_base': False", "'constant_fibre_belongs_to_original_base': True")
text = once(text, "'fixed_algebra_identified_with_base': False", "'fixed_algebra_identified_with_base': True")
text = once(text, "write_atomic(ROOT / 'constant_fibre_custody.json'", "write_atomic(ROOT / 'fixed_base_custody.json'")
compile(text, 'record_fixed_base_progress.py', 'exec')
save(ROOT / 'record_fixed_base_progress.py', text, new=True)

text = (ROOT / 'verify_constant_fibre_custody.py').read_text(encoding='utf-8')
for old, new in (
    ('constant_fibre_custody', 'fixed_base_custody'),
    ('constant_fibre_integrated_and_reviewed', 'fixed_base_integrated_and_reviewed'),
    ('RELATORIO_FIBRA_CONSTANTE.md', 'RELATORIO_BASE_FIXA.md'),
    ('MINUTA_FIBRA_CONSTANTE.md', 'MINUTA_BASE_FIXA.md'),
    ('REVIEW_UNIT_INTERVAL_PROJECTION.md', 'REVIEW_FIXED_CORE_BASE.md'),
    ('TETELESTAI_V350_CONSTANT_FIBRE_20260912', 'TETELESTAI_V350_FIXED_BASE_20260912')):
    text = text.replace(old, new)
compile(text, 'verify_fixed_base_custody.py', 'exec')
save(ROOT / 'verify_fixed_base_custody.py', text, new=True)
print({'prepared_targets': len(targets), 'recording_pending_review': True})
