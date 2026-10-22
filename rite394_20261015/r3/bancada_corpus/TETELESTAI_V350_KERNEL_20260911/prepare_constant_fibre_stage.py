"""Prepare constant-fibre identification in the isolated monolith copy."""
import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MODULES = ['UnitIntervalProjection', 'TranslationCorrelation', 'UnitIntervalShiftProjection',
           'ConstantFibreCandidate', 'L2CutIntegral', 'ZeroFromTranslatedCuts', 'ConstantFibreIdentification']


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
assert len(targets) == 26

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
assert "'ConstantFibreIdentification'" not in text
text = once(text, "'FixedCoreLocality']", "'FixedCoreLocality', " + ', '.join(map(repr, MODULES)) + ']')
text = once(text, "'import TGLExt.V350FixedCoreLocality\\n')",
            "'import TGLExt.V350FixedCoreLocality\\n'\n" +
            '\n'.join("               'import TGLExt.V350" + n + "\\n'" for n in MODULES) + ')')
anchor = '#print axioms TGLV350.Regular.dualFixedCore_commutes_measurableCut\n'
text = once(text, anchor, anchor + '\n-- Constant fibre action on the entire regular Hilbert space.\n'
            '-- Membership of that fibre operator in the original base remains open.\n' +
            ''.join('#print axioms ' + n + '\n' for n in targets))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350FixedCoreLocality.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + n + ".lean',\n" for n in MODULES))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
control = '''check('constant_fibre_identification_does_not_discharge_base_membership_trace_or_physics',
      all('TGLV350.Regular.' + name in axioms for name in (
          'unitIntervalProjection_eq_cut_shift_integral', 'commutation_fibreCandidate_read',
          'unitCut_mul_eq_zero_of_zero_read', 'eq_zero_of_shift_commutation_unitCut_zero',
          'eq_fibre_of_shift_character_commutation',
          'existsUnique_fibre_of_shift_character_commutation', 'dualFixedCore_eq_fibre_candidate'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
'''
text = once(text, "report = {'checks': checks", control + "report = {'checks': checks")
save(path, text)

template = '''# Ação constante na fibra da álgebra fixa

{date}. [REAL — Lean, cópia isolada da v350]

Todo operador B da álgebra fixa F é a amplificação de um único operador
C sobre o Hilbert da torre: B=fibre(C), em todo L²(ℝ,H). O candidato é
construído explicitamente por C=e*Be, com e(v)=1_(0,1]v.
Não se exige separabilidade de H. A pertença de C à álgebra original M
ainda está aberta; este resultado não conclui F=base.

## Construção

UnitIntervalProjection constrói a isometria e, sua leitura e*f=∫_(0,1]f
e a projeção ortogonal Q=e e*. TranslationCorrelation prova integrabilidade
da correlação e sua integral por Fubini para funções L1. Com duas funções
recortadas no intervalo unitário, a correlação se anula fora de [-2,2].
UnitIntervalShiftProjection identifica Q=P_I (∫_[-2,2] S_t dt) P_I.
As integrais de operadores são construídas fortemente em vetores, sem
hipótese de continuidade em norma de B(H).

A comutação de B∈F com translações e recortes implica QB=BQ.
ConstantFibreCandidate extrai C=e*Be e prova Be=eC e e*B=Ce*.
L2CutIntegral aplica a unicidade por todos os integrais de conjuntos
finitos: um operador A local com e*A=0 satisfaz P_I A=0.
ZeroFromTranslatedCuts propaga essa nulidade pela cobertura contável de
translações inteiras de I e conclui A=0. ConstantFibreIdentification aplica
a cadeia a A=B−fibre(C). A unicidade de C usa a injetividade da amplificação.

A prova não reúne conjuntos excepcionais ae para uma família não enumerável
de vetores, nem presume avaliação pontual contínua em L². O uso de inteiros
é na cobertura da reta; os grupos de translação e caracteres continuam reais
contínuos. Não se substitui o core contínuo por uma versão discreta.

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

[OPEN] Falta C∈M para concluir F=base. Também permanecem a correspondência
geral espectral/predual, a interface padrão de peso operatorial, estado
modular/gerador/perturbação e o traço canônico fiel, normal e semifinito.
Three Locks/H1, H2/H3 físicos na mesma realização, interações/BRST/QME,
anomalias/UV, contrato ampliado consumido pelo gate e runtime integral
continuam abertos. Nenhuma dessas obrigações foi acesa por nomes de provas.

O original não foi importado ou executado. O inventário I/O continua
histórico e não libera o runtime da cópia atual. Objetivo geral ativo.
'''
save(ROOT / 'MINUTA_FIBRA_CONSTANTE.md', template, new=True)

text = (ROOT / 'record_fixed_locality_progress.py').read_text(encoding='utf-8')
text = text.replace('Record the reviewed fixed-core locality', 'Record the reviewed constant-fibre identification')
text = re.sub(r'^MODULES = .*$', 'MODULES = ' + repr(MODULES), text, flags=re.M)
for old, new in (
    ('TETELESTAI_V350_FIXED_CORE_LOCALITY_20260912', 'TETELESTAI_V350_CONSTANT_FIBRE_20260912'),
    ('REVIEW_FIXED_CORE_LOCALITY.md', 'REVIEW_UNIT_INTERVAL_PROJECTION.md'),
    ("ROOT / 'bounded_values_custody.json'", "ROOT / 'fixed_locality_custody.json'"),
    ('RELATORIO_LOCALIDADE_FIXA.md', 'RELATORIO_FIBRA_CONSTANTE.md'),
    ('MINUTA_LOCALIDADE_FIXA.md', 'MINUTA_FIBRA_CONSTANTE.md')):
    text = text.replace(old, new)
text = once(text, "namespace = 'TGLV350.Fourier.' if name == 'FourierUniqueness' else 'TGLV350.Regular.'",
            "namespace = 'TGLV350.Regular.'")
start, end = text.index("note = f'''"), text.index('surfaces = ')
note = """note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] A álgebra fixa F tem ação constante na fibra:
B=fibre(C), C=e*Be, com unicidade em B(H). A projeção Q=e e* no intervalo
unitário é P_I (∫_[-2,2] S_t dt) P_I; B∈F comuta com Q, dando Be=eC e
e*B=Ce*. Para A=B−fibre(C), todos os integrais de recortes da leitura
se anulam e dão P_I A=0. As translações inteiras cobrem a reta e concluem
A=0. Sete módulos, sem separabilidade de H nem uniformização ae não enumerável.
{len(targets)} alvos novos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações no Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python fora do dicionário Lean
inalterado por AST; gate legado inalterado.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] C∈M, necessário para F=base. Correspondência espectral/predual,
interface de peso operatorial, estado/gerador/perturbação/traço canônico,
Three Locks/H1, H2/H3 físicos, interações/BRST/QME/anomalias/UV, contrato
ampliado e runtime integral permanecem abertos. Seis flags maiores false.
O inventário de I/O é histórico, sem liberação do runtime atual. Objetivo ativo.
Original não importado/executado; runtime integral da cópia pendente.
'''
"""
text = text[:start] + note + text[end:]
text = once(text, "'RELATORIO_IDEAL_SEMIFINITO.md', 'RELATORIO_VALORES_LIMITADOS.md')]",
            "'RELATORIO_IDEAL_SEMIFINITO.md', 'RELATORIO_VALORES_LIMITADOS.md',\n"
            "    'RELATORIO_LOCALIDADE_FIXA.md')]")
text = once(text, "'fixed_algebra_commutes_with_ordinary_translations': True,",
            "'fixed_algebra_commutes_with_ordinary_translations': True,\n"
            "    'fixed_algebra_operators_are_constant_fibres': True,\n"
            "    'constant_fibre_belongs_to_original_base': False,")
text = once(text, "write_atomic(ROOT / 'fixed_locality_custody.json'", "write_atomic(ROOT / 'constant_fibre_custody.json'")
compile(text, 'record_constant_fibre_progress.py', 'exec')
save(ROOT / 'record_constant_fibre_progress.py', text, new=True)

text = (ROOT / 'verify_fixed_locality_custody.py').read_text(encoding='utf-8')
for old, new in (
    ('fixed_locality_custody', 'constant_fibre_custody'),
    ('fixed_locality_integrated_and_reviewed', 'constant_fibre_integrated_and_reviewed'),
    ('RELATORIO_LOCALIDADE_FIXA.md', 'RELATORIO_FIBRA_CONSTANTE.md'),
    ('MINUTA_LOCALIDADE_FIXA.md', 'MINUTA_FIBRA_CONSTANTE.md'),
    ('REVIEW_FIXED_CORE_LOCALITY.md', 'REVIEW_UNIT_INTERVAL_PROJECTION.md'),
    ('TETELESTAI_V350_FIXED_CORE_LOCALITY_20260912', 'TETELESTAI_V350_CONSTANT_FIBRE_20260912')):
    text = text.replace(old, new)
compile(text, 'verify_constant_fibre_custody.py', 'exec')
save(ROOT / 'verify_constant_fibre_custody.py', text, new=True)
print({'prepared_targets': len(targets), 'recording_pending_review': True})
