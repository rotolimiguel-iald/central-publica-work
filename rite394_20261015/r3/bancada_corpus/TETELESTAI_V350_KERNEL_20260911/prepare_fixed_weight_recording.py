"""Prepare the next stage recorder from the verified byte-custody protocol."""
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
    assert temp.read_bytes() == raw
    temp.replace(path)


old = (ROOT / 'record_fixed_form_affiliation_progress.py').read_text(encoding='utf-8')
prefix = old.split("report_path = ROOT / 'RELATORIO_AFILIACAO_DA_FORMA_FIXA.md'")[0]
prefix = once(prefix,
    "MODULES = ['ResolventGraphTransport', 'DualSupportTransport', 'DualFixedFormAffiliation']",
    "MODULES = ['PositiveFormCone', 'DualFixedWeightLaws']")
prefix = prefix.replace('TETELESTAI_V350_DUAL_FIXED_FORM_AFFILIATION_20260912',
                        'TETELESTAI_V350_DUAL_FIXED_WEIGHT_20260912')
prefix = prefix.replace('REVIEW_DUAL_FIXED_FORM_AFFILIATION.md', 'REVIEW_DUAL_FIXED_WEIGHT.md')
prefix = once(prefix, "ROOT / 'fixed_resolvent_custody.json'", "ROOT / 'fixed_form_affiliation_custody.json'")
prefix = once(prefix, "runtime_inventory['source_sha256'] == integration['working_sha256']",
                      "runtime_inventory['source_sha256'] == previous['working_sha256']")
body = r"""
report_path = ROOT / 'RELATORIO_PESO_FORMA_FIXA.md'
template = ROOT / 'MINUTA_PESO_FORMA_FIXA.md'
report = template.read_text(encoding='utf-8').format(
    date=DATE, target_count=len(targets), build_count=len(build['records']),
    controls=tests['passed'], audit_count=tests['axiom_report_entries'],
    embedded_count=integration['embedded_files'], base_sha=integration['base_sha256'],
    working_sha=integration['working_sha256'], review_path=review.as_posix())
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] PositiveFormCone e DualFixedWeightLaws entregam
operações/ordem de formas afiliadas e o mapa T: N_+ → AffiliatedPositiveForm F.
T é aditivo, homogêneo para NNReal, monótono, fiel, normal por IsLUB interno
de redes dirigidas positivas e bimodular para todo B∈F. T(A)(v) é a mesma
integral q_A(v), inclusive ∞. Sem subtração ou conversão indevida de infinito.
{len(targets)} alvos novos; {len(build['records'])} registros Lean,
{tests['passed']} controles, {tests['axiom_report_entries']} declarações
distintas no Audit, {integration['embedded_files']} arquivos embutidos.
Base `{integration['base_sha256']}`; cópia `{integration['working_sha256']}`.
Corpo Python fora do dicionário Lean inalterado por AST; gate legado inalterado.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] F=base, correspondência geral espectral/predual e semifinitude do peso
na álgebra; estado modular/gerador/perturbação/traço canônico; Three Locks/H1;
H2/H3 na mesma realização; interações/BRST/QME/anomalias/UV; contrato ampliado
consumido pelo gate e runtime integral. Seis flags maiores false, objetivo ativo.
A v350 canônica continua preservada: as flags qgf/gpf não entram no gate legado;
a H2 experimental com pycbc não é H2 geométrica. O inventário de I/O é histórico,
da cópia anterior, sem importação/execução do monólito ou liberação de isolamento.
'''
"""
suffix = 'surfaces = ' + old.split('surfaces = ', 1)[1]
suffix = once(suffix, "'RELATORIO_REPRESENTACAO_DA_FORMA_DUAL.md', 'RELATORIO_RESOLVENTE_FIXO_DUAL.md')]",
    "'RELATORIO_REPRESENTACAO_DA_FORMA_DUAL.md', 'RELATORIO_RESOLVENTE_FIXO_DUAL.md',\n"
    "    'RELATORIO_AFILIACAO_DA_FORMA_FIXA.md')]")
suffix = suffix.replace("'fixed_form_affiliation_including_infinity': True,\n    'unitary_graph_equivalences_on_support': True,",
    "'ordered_affiliated_form_cone': True,\n    'faithful_normal_fixed_form_weight': True,\n"
    "    'bimodule_over_entire_fixed_algebra': True,\n    'general_spectral_predual_correspondence': False,")
suffix = suffix.replace("'runtime_io_inventory_sha256': digest(ROOT / 'runtime_io_inventory.json'),",
    "'runtime_io_inventory_sha256': digest(ROOT / 'runtime_io_inventory.json'),\n"
    "    'runtime_io_inventory_source_sha256': runtime_inventory['source_sha256'],\n"
    "    'reviewed_template_sha256': digest(template),")
suffix = suffix.replace("ROOT / 'fixed_form_affiliation_custody.json'", "ROOT / 'fixed_weight_custody.json'")
text = prefix + body + suffix
compile(text, 'record_fixed_weight_progress.py', 'exec')
create('record_fixed_weight_progress.py', text)

verifier = (ROOT / 'verify_fixed_form_affiliation_custody.py').read_text(encoding='utf-8')
verifier = verifier.replace('fixed_form_affiliation_custody', 'fixed_weight_custody')
verifier = verifier.replace('RELATORIO_AFILIACAO_DA_FORMA_FIXA.md', 'RELATORIO_PESO_FORMA_FIXA.md')
verifier = verifier.replace('REVIEW_DUAL_FIXED_FORM_AFFILIATION.md', 'REVIEW_DUAL_FIXED_WEIGHT.md')
verifier = verifier.replace('TETELESTAI_V350_DUAL_FIXED_FORM_AFFILIATION_20260912',
                            'TETELESTAI_V350_DUAL_FIXED_WEIGHT_20260912')
verifier = verifier.replace('dual_fixed_form_affiliation_integrated_and_reviewed',
                            'dual_fixed_weight_integrated_and_reviewed')
verifier = once(verifier, "for name, expected in c['modules'].items():",
    "assert digest(ROOT / 'MINUTA_PESO_FORMA_FIXA.md') == c['reviewed_template_sha256']\n"
    "for name, expected in c['modules'].items():")
compile(verifier, 'verify_fixed_weight_custody.py', 'exec')
create('verify_fixed_weight_custody.py', verifier)
print('Prepared recorder and verifier; no memories written.')
