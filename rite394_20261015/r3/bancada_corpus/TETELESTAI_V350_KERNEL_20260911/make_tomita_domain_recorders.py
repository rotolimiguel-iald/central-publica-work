"""Prepare recording scripts for the reviewed initial Tomita domain only."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['DualOrbitStrongLimits', 'ScalarGNSStarApproximation',
           'ScalarGNSStarDensity', 'ScalarTomitaGraph']


def create(name, text):
    path = ROOT / name
    assert not path.exists(), path
    raw = text.encode('utf-8')
    temp = path.with_name(path.name + '.new')
    with temp.open('xb') as handle:
        handle.write(raw)
    assert temp.read_bytes() == raw and len(raw) > 0
    temp.replace(path)
    assert path.read_bytes() == raw


text = (ROOT / 'record_gns_representation_progress.py').read_text(encoding='utf-8')
text = re.sub(r'^MODULES = .*$', 'MODULES = ' + repr(MODULES), text, flags=re.M)
text = text.replace('TETELESTAI_V350_GNS_REPRESENTATION_20260912',
                    'TETELESTAI_V350_TOMITA_INITIAL_DOMAIN_20260912')
text = text.replace('REVIEW_GNS_REPRESENTATION.md', 'REVIEW_TOMITA_INITIAL_DOMAIN.md')
text = text.replace("previous = json.loads((ROOT / 'modular_domain_custody.json').read_bytes())",
                    "previous = json.loads((ROOT / 'gns_representation_custody.json').read_bytes())")
text = text.replace('RELATORIO_REPRESENTACAO_GNS.md', 'RELATORIO_DOMINIO_INICIAL_TOMITA.md')
text = text.replace('MINUTA_REPRESENTACAO_GNS.md', 'MINUTA_DOMINIO_INICIAL_TOMITA.md')
text = text.replace("write_atomic(ROOT / 'gns_representation_custody.json',",
                    "write_atomic(ROOT / 'tomita_domain_custody.json',")
text = text.replace("for name in ['DualOrbitStrongLimits', 'ScalarGNSStarApproximation', 'ScalarGNSStarDensity', 'ScalarTomitaGraph']:",
                    "for name in ['ScalarGNSStrongContinuity', 'ScalarGNSNormality']:")
text = text.replace('assert development_targets == 14', 'assert development_targets == 7')
text = text.replace('ROTA_DOMINIO_TOMITA_RASCUNHO.md', 'ROTA_NORMALIDADE_GNS_RASCUNHO.md')
start = text.index('note = f"""')
end = text.index('surfaces = ', start)
text = text[:start] + '''note = f"""

## {MARKER} — {DATE}

[REAL — Lean em cópia, revisão independente] Λ_ν(I∩I*) é densa em H_I
na norma GNS, pela regularização esquerda X_h* A para h>0. O gráfico
G=(Λ_ν(A),Λ_ν(A*)) é univalente, invariante pela troca e tem domínio
denso. A fatoração ambiente transfere redes fortes uniformemente limitadas
sem interseção não enumerável de conjuntos conulos. Nenhuma dessas provas
afirma univalência do fecho(G), fechabilidade ou operador Tomita fechado.
Quatro módulos; {len(targets)} alvos novos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Python fora do dicionário Lean
inalterado por AST, gate legado inalterado, seis flags maiores false.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Provar (0,y)∈fecho(G) implica y=0; identificar domínio escalar
máximo, Tomita fechado, dados modulares/KMS, gerador afiliado e traço
canônico com escala dual; interface espectral/predual/operatorial;
Three Locks/H1, H2/H3 físicos, estado interagente/BRST/QME/anomalias/UV,
certificado completo consumido pelo gate e runtime isolado integral.
O objetivo permanece ativo. Original não importado/executado.

[REAL — DEV posterior, sem revisão independente nem integração]
Dois módulos/sete alvos adicionais provam transferência de limites
fortes limitados para π_I em H_I, positividade, monotonicidade e
preservação de supremos internos de redes/conjuntos positivos dirigidos.
É normalidade em ordem dessa representação, não construção de Tomita.
Fontes/logs/binários pinados separadamente, fora das contagens integradas
e do alcance do parecer acima. A fechabilidade continua OPEN.
[Rota e limites](<{(ROOT / 'ROTA_NORMALIDADE_GNS_RASCUNHO.md').as_posix()}>).
"""
''' + text[end:]
text = text.replace("'RELATORIO_PESO_ESCALAR_DUAL.md', 'RELATORIO_DOMINIO_MODULAR.md')]",
                    "'RELATORIO_PESO_ESCALAR_DUAL.md', 'RELATORIO_DOMINIO_MODULAR.md',\n    'RELATORIO_REPRESENTACAO_GNS.md')]")
text = text.replace("'orbit_review_sha256': digest(ROOT / 'revisao/REVIEW_GNS_ORBIT.md'),",
                    "'prior_gns_review_sha256': digest(ROOT / 'revisao/REVIEW_GNS_REPRESENTATION.md'),")
text = text.replace("'GNS_representation_normality_proved': False,",
                    "'GNS_representation_normality_proved': False,\n    'GNS_star_domain_norm_dense': True,\n    'Tomita_initial_graph_single_valued': True,\n    'Tomita_initial_graph_swap_invariant': True,\n    'Tomita_initial_domain_dense': True,\n    'Tomita_graph_closure_single_valued': False,")
create('record_tomita_domain_progress.py', text)

text = (ROOT / 'verify_gns_representation_custody.py').read_text(encoding='utf-8')
text = text.replace('gns_representation', 'tomita_domain')
text = text.replace('RELATORIO_REPRESENTACAO_GNS.md', 'RELATORIO_DOMINIO_INICIAL_TOMITA.md')
text = text.replace('REVIEW_GNS_REPRESENTATION.md', 'REVIEW_TOMITA_INITIAL_DOMAIN.md')
text = text.replace('MINUTA_REPRESENTACAO_GNS.md', 'MINUTA_DOMINIO_INICIAL_TOMITA.md')
text = text.replace("digest(ROOT / 'revisao/REVIEW_GNS_ORBIT.md') == c['orbit_review_sha256']",
                    "digest(ROOT / 'revisao/REVIEW_GNS_REPRESENTATION.md') == c['prior_gns_review_sha256']")
text = text.replace('ROTA_DOMINIO_TOMITA_RASCUNHO.md', 'ROTA_NORMALIDADE_GNS_RASCUNHO.md')
text = text.replace("c['post_scope_development_targets'] == 14", "c['post_scope_development_targets'] == 7")
text = text.replace('TETELESTAI_V350_GNS_REPRESENTATION_20260912',
                    'TETELESTAI_V350_TOMITA_INITIAL_DOMAIN_20260912')
create('verify_tomita_domain_custody.py', text)
print('Prepared recording scripts. No custody or memory changed.')
