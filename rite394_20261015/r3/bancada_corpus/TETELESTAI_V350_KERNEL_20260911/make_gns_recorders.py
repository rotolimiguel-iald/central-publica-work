"""Derive scoped recorders from the preceding verified recording workflow."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
modules = ['ScalarGNSOrbit', 'ScalarGNSLinear', 'ScalarGNSAction',
           'OperatorFieldAlgebra', 'ScalarGNSCompletion', 'DualOrbitRepresentation', 'ReducingStarRepresentation',
           'ScalarGNSRepresentation']


def create(name, text):
    p = ROOT / name
    assert not p.exists(), p
    raw = text.encode('utf-8')
    t = p.with_name(p.name + '.new')
    with t.open('xb') as f:
        f.write(raw)
    assert t.read_bytes() == raw and len(raw) > 0
    t.replace(p)
    assert p.read_bytes() == raw


text = (ROOT / 'record_modular_domain_progress.py').read_text(encoding='utf-8')
text = re.sub(r'^MODULES = .*$', 'MODULES = ' + repr(modules), text, flags=re.M)
text = text.replace('TETELESTAI_V350_MODULAR_DOMAIN_20260912', 'TETELESTAI_V350_GNS_REPRESENTATION_20260912')
text = text.replace('REVIEW_MODULAR_DOMAIN.md', 'REVIEW_GNS_REPRESENTATION.md')
text = text.replace("previous = json.loads((ROOT / 'scalar_weight_custody.json').read_bytes())",
                    "previous = json.loads((ROOT / 'modular_domain_custody.json').read_bytes())")
text = text.replace('RELATORIO_DOMINIO_MODULAR.md', 'RELATORIO_REPRESENTACAO_GNS.md')
text = text.replace('MINUTA_DOMINIO_MODULAR.md', 'MINUTA_REPRESENTACAO_GNS.md')
text = text.replace("ROOT / 'modular_domain_custody.json',", "ROOT / 'gns_representation_custody.json',")
start = text.index('note = f"""')
end = text.index('surfaces = ', start)
text = text[:start] + '''note = f"""

## {MARKER} — {DATE}

[REAL — Lean em cópia] Inscrição linear complexa e injetiva Λ_ν sobre o
ideal I de quadrados uniformemente limitados, com ||Λ_ν(A)||²=ν(A*A).
Seu fecho H_I é Hilbert completo, a inscrição tem imagem densa e a ação
π_I(B)Λ_ν(A)=Λ_ν(BA) estende-se a um *-homomorfismo unital fiel de N
sobre H_I, com ||π_I(B)||≤||B||. Fidelidade demonstrada por BA=0 para
todo A∈I e pelas médias X_h∈I, BX_h→B fortemente; não presumida.
Oito módulos; {len(targets)} alvos novos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Python fora do dicionário Lean
inalterado por AST, gate legado inalterado, seis flags maiores false.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] H_I completa I, não identifica I com o domínio escalar máximo.
A densidade de Λ_ν(I∩I*) na norma ν, normalidade de π_I e Tomita fechado
ainda precisam de prova. Invariância de ν não quita KMS. Permanecem
identificação modular, gerador afiliado, perturbação e traço com escala;
interface geral espectral/predual/peso operatorial; Three Locks/H1,
H2/H3 físicos, interações/BRST/QME/anomalias/UV, certificado consumido
e runtime integral isolado. Objetivo ativo. Original não importado/executado.
O inventário I/O anterior permanece histórico, sem liberação atual.
"""
''' + text[end:]
text = text.replace("'RELATORIO_PESO_ESCALAR_DUAL.md')]", "'RELATORIO_PESO_ESCALAR_DUAL.md', 'RELATORIO_DOMINIO_MODULAR.md')]")
text = text.replace("'review_sha256': digest(review),", "'review_sha256': digest(review),\n    'orbit_review_sha256': digest(ROOT / 'revisao/REVIEW_GNS_ORBIT.md'),")
text = text.replace("'KMS_proved': False,", "'GNS_finite_ideal_completion_constructed': True,\n    'GNS_finite_ideal_representation_faithful': True,\n    'GNS_maximal_scalar_domain_identified': False,\n    'GNS_representation_normality_proved': False,\n    'Tomita_operator_constructed_for_scalar_weight': False,\n    'KMS_proved': False,")
create('record_gns_representation_progress.py', text)

text = (ROOT / 'verify_modular_domain_custody.py').read_text(encoding='utf-8')
for a, b in [('modular_domain', 'gns_representation'),
             ('DOMINIO_MODULAR', 'REPRESENTACAO_GNS'),
             ('REVIEW_MODULAR_DOMAIN', 'REVIEW_GNS_REPRESENTATION'),
             ('TETELESTAI_V350_MODULAR_DOMAIN', 'TETELESTAI_V350_GNS_REPRESENTATION')]:
    text = text.replace(a, b)
text = text.replace("assert digest(ROOT / 'runtime_io_inventory.json')", "assert digest(ROOT / 'revisao/REVIEW_GNS_ORBIT.md') == c['orbit_review_sha256']\nassert digest(ROOT / 'runtime_io_inventory.json')", 1)
create('verify_gns_representation_custody.py', text)

text = (ROOT / 'record_gns_draft.py').read_text(encoding='utf-8')
text = re.sub(r'^MODULES = .*$', 'MODULES = ' + repr(modules), text, flags=re.M)
text = text.replace('assert len(targets) == 14', 'assert len(targets) == 35')
start = text.index('note = """')
end = text.index('result = {', start)
text = text[:start] + text[end:]
text = text.replace("'draft_note_sha256': sha(ROOT / 'ROTA_GNS_RASCUNHO.md'),", "'draft_note_sha256': sha(ROOT / 'MINUTA_REPRESENTACAO_GNS.md'),")
text = text.replace("'GNS_completed_representation_constructed': False,", "'GNS_finite_ideal_completion_constructed': True,\n    'GNS_finite_ideal_representation_faithful': True,\n    'GNS_maximal_scalar_domain_identified': False,")
text = text.replace("ROOT / 'gns_draft_status.json'", "ROOT / 'gns_representation_draft_status.json'")
create('record_gns_representation_draft.py', text)
print('Created recording scripts only; none executed, no memory or custody changed.')
