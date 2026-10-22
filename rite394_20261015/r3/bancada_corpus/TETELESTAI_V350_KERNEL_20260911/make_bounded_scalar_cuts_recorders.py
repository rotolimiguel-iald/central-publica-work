"""Prepare the next scoped custody scripts without executing them."""
from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parent


def create(name, text):
    ast.parse(text)
    p = ROOT / name
    assert not p.exists(), p
    raw = text.encode('utf-8')
    t = p.with_name(p.name + '.new')
    with t.open('xb') as f:
        f.write(raw)
    assert t.read_bytes() == raw and len(raw) > 0
    t.replace(p)
    assert p.read_bytes() == raw


s = (ROOT / 'record_gns_normality_progress.py').read_text(encoding='utf-8')
s = re.sub(r'^MODULES = .*$', "MODULES = ['DualCutLinearMap', 'ScalarBoundedCuts', 'ScalarCutNormality']", s, flags=re.M)
s = s.replace('TETELESTAI_V350_GNS_NORMALITY_20260912', 'TETELESTAI_V350_BOUNDED_SCALAR_CUTS_20260912')
s = s.replace("review = ROOT / 'revisao/REVIEW_GNS_NORMALITY.md'", "review = ROOT / 'revisao/REVIEW_BOUNDED_SCALAR_CUTS.md'")
s = s.replace("previous = json.loads((ROOT / 'tomita_domain_custody.json').read_bytes())", "previous = json.loads((ROOT / 'gns_normality_custody.json').read_bytes())")
s = s.replace("report_path = ROOT / 'RELATORIO_NORMALIDADE_GNS.md'", "report_path = ROOT / 'RELATORIO_FUNCIONAIS_LIMITADOS.md'")
s = s.replace('MINUTA_NORMALIDADE_GNS.md', 'MINUTA_FUNCIONAIS_LIMITADOS.md')
s = s.replace("write_atomic(ROOT / 'gns_normality_custody.json',", "write_atomic(ROOT / 'bounded_scalar_cuts_custody.json',")
s = s.replace("for name in ['DualCutLinearMap', 'ScalarBoundedCuts', 'ScalarCutNormality']:", "for name in ['ScalarGNSCutMaps', 'ScalarGNSCutNorm']:")
s = s.replace('assert development_targets == 11', 'assert development_targets == 9')
s = s.replace('ROTA_FUNCIONAIS_LIMITADOS_RASCUNHO.md', 'ROTA_MAPAS_GNS_DE_CORTE_RASCUNHO.md')
a = s.index('note = f"""')
b = s.index('surfaces = ', a)
s = s[:a] + '''note = f"""

## {MARKER} — {DATE}

[REAL — Lean em cópia, revisão independente] Cortes C_R são mapas
complexo-lineares limitados; ψ_R(A)=c⟨η,C_R(A)η⟩ é funcional limitado,
positivo para R≥0 (realidade e sinal). No cone positivo de N, Re ψ_R≤ν;
ν=sup_n Re ψ_n, com inclusão em ENNReal. Não se afirma fidelidade de
cada corte, ψ_n(1)=1 ou finitude do supremo. O fator c é o mesmo de ν.
O critério de convergência monótona foi provado para supremos internos
positivos dirigidos não vazios; o limite forte é construído na prova.
Não se reivindica nova interface predual nem equivalência geral Lean.
Três módulos/{len(targets)} alvos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Python fora do dicionário Lean
inalterado por AST, gate legado inalterado, seis flags maiores false.
[Relatório](<{report_path.as_posix()}>).
[Parecer independente](<{review.as_posix()}>).

[OPEN] Fechabilidade do gráfico inicial de Tomita, domínio escalar máximo,
operador fechado, KMS/identificação modular, gerador afiliado e traço com
escala dual, interfaces gerais necessárias, Three Locks/H1, H2/H3 físicos,
setor interagente/BRST/QME/anomalias/UV e certificado completo consumido
pelo gate. Runtime integral pendente. Objetivo ativo. Original não
executado/importado; inventário I/O histórico não é liberação de runtime.

[REAL — DEV posterior, não revisado nem integrado] Dois módulos/nove
alvos constroem T_R:H_I→L² ambiente como corte por 1_(-R,R], contrações
que entrelaçam π_I e a representação ambiente. Para A∈I e R≥0,
‖T_RΛ(A)‖²=Re ψ_R(A*A), com o mesmo fator c. T_n v=0 para todo natural
n implica v=0; isso é injetividade conjunta, não fidelidade individual.
Não se afirma T_R(H_I)⊆H_I ou construção de novo GNS cíclico/separante.
Falta (0,y)∈fecho(G)⇒T_n y=0; os mapas não demonstram fechabilidade.
Pins DEV separados do escopo e contagens do parecer integrado.
[Rota](<{(ROOT / 'ROTA_MAPAS_GNS_DE_CORTE_RASCUNHO.md').as_posix()}>).
"""
''' + s[b:]
s = s.replace("'RELATORIO_REPRESENTACAO_GNS.md', 'RELATORIO_DOMINIO_INICIAL_TOMITA.md')]", "'RELATORIO_REPRESENTACAO_GNS.md', 'RELATORIO_DOMINIO_INICIAL_TOMITA.md', 'RELATORIO_NORMALIDADE_GNS.md')]")
s = s.replace("'prior_tomita_review_sha256': digest(ROOT / 'revisao/REVIEW_TOMITA_INITIAL_DOMAIN.md'),", "'prior_gns_normality_review_sha256': digest(ROOT / 'revisao/REVIEW_GNS_NORMALITY.md'),")
s = s.replace("'GNS_representation_normality_proved': True,", "'bounded_scalar_positive_cuts_constructed': True,\n    'scalar_weight_is_supremum_of_bounded_cuts': True,\n    'bounded_cuts_monotone_convergence_criterion_proved': True,\n    'bounded_cuts_GNS_intertwiners_constructed': False,\n    'GNS_representation_normality_proved': True,")
create('record_bounded_scalar_cuts_progress.py', s)

s = (ROOT / 'verify_gns_normality_custody.py').read_text(encoding='utf-8')
s = s.replace('gns_normality', 'bounded_scalar_cuts')
s = s.replace('RELATORIO_NORMALIDADE_GNS.md', 'RELATORIO_FUNCIONAIS_LIMITADOS.md')
s = s.replace('REVIEW_GNS_NORMALITY.md', 'REVIEW_BOUNDED_SCALAR_CUTS.md')
s = s.replace('MINUTA_NORMALIDADE_GNS.md', 'MINUTA_FUNCIONAIS_LIMITADOS.md')
s = s.replace("digest(ROOT / 'revisao/REVIEW_TOMITA_INITIAL_DOMAIN.md') == c['prior_tomita_review_sha256']", "digest(ROOT / 'revisao/REVIEW_GNS_NORMALITY.md') == c['prior_gns_normality_review_sha256']")
s = s.replace('ROTA_FUNCIONAIS_LIMITADOS_RASCUNHO.md', 'ROTA_MAPAS_GNS_DE_CORTE_RASCUNHO.md')
s = s.replace("c['post_scope_development_targets'] == 11", "c['post_scope_development_targets'] == 9")
s = s.replace('TETELESTAI_V350_GNS_NORMALITY_20260912', 'TETELESTAI_V350_BOUNDED_SCALAR_CUTS_20260912')
create('verify_bounded_scalar_cuts_custody.py', s)

s = (ROOT / 'record_bounded_scalar_cuts_draft.py').read_text(encoding='utf-8')
s = re.sub(r'^MODULES = .*$', "MODULES = ['ScalarGNSCutMaps', 'ScalarGNSCutNorm']", s, flags=re.M)
s = s.replace('len(targets) == 11', 'len(targets) == 9')
s = s.replace('gns_normality_custody.json', 'bounded_scalar_cuts_custody.json')
s = s.replace('ROTA_FUNCIONAIS_LIMITADOS_RASCUNHO.md', 'ROTA_MAPAS_GNS_DE_CORTE_RASCUNHO.md')
s = s.replace('bounded_scalar_cuts_draft_status.json', 'gns_cut_maps_draft_status.json')
s = s.replace("'bounded_cuts_GNS_intertwiners_constructed': False,", "'bounded_cuts_GNS_intertwiners_constructed': True,\n    'bounded_cuts_GNS_target': 'EXISTING_AMBIENT_L2_NOT_NEW_CYCLIC_GNS_SPACE',\n    'bounded_cuts_GNS_norm_identity_proved': True,\n    'bounded_cuts_GNS_joint_injectivity_proved': True,")
create('record_gns_cut_maps_draft.py', s)
print('Created custody/verifier and later DEV recorder; none executed.')
