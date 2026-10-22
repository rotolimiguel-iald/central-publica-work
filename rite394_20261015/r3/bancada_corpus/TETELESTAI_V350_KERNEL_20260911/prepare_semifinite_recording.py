"""Prepare reviewed recording; do not write memories until review is read."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def create(name, text):
    path = ROOT / name
    assert not path.exists()
    raw = text.encode('utf-8')
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as f:
        f.write(raw)
    assert temp.read_bytes() == raw and len(raw) > 0
    temp.replace(path)


old = (ROOT / 'record_fixed_weight_progress.py').read_text(encoding='utf-8')
prefix = old.split("report_path = ROOT / 'RELATORIO_PESO_FORMA_FIXA.md'")[0]
prefix = once(prefix, "MODULES = ['PositiveFormCone', 'DualFixedWeightLaws']",
    "MODULES = ['RegularApproximation', 'FourierL1L2', 'RegularFiniteWeight', 'DualSemifiniteIdeal']")
prefix = prefix.replace('TETELESTAI_V350_DUAL_FIXED_WEIGHT_20260912', 'TETELESTAI_V350_SEMIFINITE_IDEAL_20260912')
prefix = prefix.replace('REVIEW_DUAL_FIXED_WEIGHT.md', 'REVIEW_REGULAR_SEMIFINITE_ROUTE.md')
prefix = once(prefix, "ROOT / 'fixed_form_affiliation_custody.json'", "ROOT / 'fixed_weight_custody.json'")
prefix = once(prefix, "targets.update('TGLV350.Regular.' + target for target in",
    "namespace = 'TGLV350.Fourier.' if name == 'FourierL1L2' else 'TGLV350.Regular.'\n"
    "    targets.update(namespace + target for target in")
prefix = once(prefix, "assert runtime_inventory['source_sha256'] == previous['working_sha256']",
    "assert runtime_inventory['source_sha256'] == previous['runtime_io_inventory_source_sha256']\n"
    "assert digest(ROOT / 'runtime_io_inventory.json') == previous['runtime_io_inventory_sha256']")
body = r"""
report_path = ROOT / 'RELATORIO_IDEAL_SEMIFINITO.md'
template = ROOT / 'MINUTA_IDEAL_SEMIFINITO.md'
report = template.read_text(encoding='utf-8').format(
    date=DATE, target_count=len(targets), build_count=len(build['records']),
    controls=tests['passed'], audit_count=tests['axiom_report_entries'],
    embedded_count=integration['embedded_files'], base_sha=integration['base_sha256'],
    working_sha=integration['working_sha256'], review_path=review.as_posix())
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] RegularApproximation, FourierL1L2, RegularFiniteWeight
e DualSemifiniteIdeal: as médias X_h=h^(-1)∫_0^h Λ_t dt pertencem ao mesmo core,
||X_h||≤1 e X_h→I fortemente. Para h>0, q_(X_h* X_h)(v)=ofReal(h^(-1)||v||²),
com a normalização dual (2π)^(-1) preservada. A ponte L1∩L2 identifica a integral
de Fourier com a transformada isométrica quase em toda parte. O domínio dos
quadrados com uma única cota para todos os vetores é submódulo complexo e ideal
à esquerda; A X_h aproxima fortemente todo A∈N com A X_h nesse domínio.
Isso entrega o critério de densidade de quadrados finitos para a forma construída.
{len(targets)} alvos novos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações no Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python fora do dicionário Lean
inalterado por AST; gate legado inalterado.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] F=base; representação dos valores finitos por operadores limitados de F
e correspondência espectral/predual geral; peso operatorial padrão e estado
modular/gerador/perturbação/traço canônico; Three Locks/H1; H2/H3 na mesma realização;
interações/BRST/QME/anomalias/UV; contrato ampliado consumido pelo gate; runtime integral.
Seis flags maiores permanecem false, objetivo ativo. O inventário de I/O permanece
histórico, com hash da cópia à qual pertence; não é liberação da cópia atual.
Nenhuma importação/execução do monólito original ou do runtime integral foi feita.
'''
"""
suffix = 'surfaces = ' + old.split('surfaces = ', 1)[1]
suffix = once(suffix, "'RELATORIO_AFILIACAO_DA_FORMA_FIXA.md')]",
    "'RELATORIO_AFILIACAO_DA_FORMA_FIXA.md', 'RELATORIO_PESO_FORMA_FIXA.md')]")
suffix = once(suffix, "'ordered_affiliated_form_cone': True,",
    "'finite_square_left_ideal_constructed': True,\n"
    "    'finite_square_left_ideal_strong_approximation': True,\n"
    "    'exact_regular_average_weight': True,\n"
    "    'ordinary_fourier_agrees_with_L2_on_L1_L2': True,\n"
    "    'finite_values_as_bounded_operators_in_F': False,\n"
    "    'ordered_affiliated_form_cone': True,")
suffix = suffix.replace("ROOT / 'fixed_weight_custody.json'", "ROOT / 'semifinite_ideal_custody.json'")
text = prefix + body + suffix
compile(text, 'record_semifinite_ideal_progress.py', 'exec')
create('record_semifinite_ideal_progress.py', text)
verifier = (ROOT / 'verify_fixed_weight_custody.py').read_text(encoding='utf-8')
verifier = verifier.replace('fixed_weight_custody', 'semifinite_ideal_custody')
verifier = verifier.replace('RELATORIO_PESO_FORMA_FIXA.md', 'RELATORIO_IDEAL_SEMIFINITO.md')
verifier = verifier.replace('MINUTA_PESO_FORMA_FIXA.md', 'MINUTA_IDEAL_SEMIFINITO.md')
verifier = verifier.replace('REVIEW_DUAL_FIXED_WEIGHT.md', 'REVIEW_REGULAR_SEMIFINITE_ROUTE.md')
verifier = verifier.replace('TETELESTAI_V350_DUAL_FIXED_WEIGHT_20260912', 'TETELESTAI_V350_SEMIFINITE_IDEAL_20260912')
verifier = verifier.replace('dual_fixed_weight_integrated_and_reviewed', 'semifinite_ideal_integrated_and_reviewed')
compile(verifier, 'verify_semifinite_ideal_custody.py', 'exec')
create('verify_semifinite_ideal_custody.py', verifier)
print('Prepared recorder and verifier; memories not yet touched.')
