"""Derive new stage helpers without modifying the sealed previous helpers."""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parent
NAMES = ['ScalarRegularRightGNS', 'ScalarRegularRightTomita', 'ScalarRegularRightSquare']

def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)

def create(name, text):
    ast.parse(text)
    path = ROOT / name
    assert not path.exists()
    raw = text.encode('utf-8')
    temp = path.with_suffix('.py.tmp')
    with temp.open('xb') as f:
        f.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

def common(text):
    return (text.replace('scalar_right_tomita_custody.json', 'right_square_custody.json')
        .replace('right_square_draft', 'regular_right_draft')
        .replace('RIGHT_SQUARE', 'REGULAR_RIGHT')
        .replace('ESCALA_DIREITA_SQUARED', 'DIREITA_UNITARIA_REGULAR')
        .replace("['HomogeneousRightSquareDomain', 'MatrixUnitRightSquare']", repr(NAMES))
        .replace('same_actual_square_domain_right_invariant', 'same_actual_square_domain_regular_invariant')
        .replace('matrix_unit_right_scaling_on_full_square_domain', 'regular_right_commutes_on_full_square_domain'))

draft = common((ROOT / 'record_right_square_draft.py').read_text(encoding='utf-8'))
draft = draft.replace("parent['both_intertwinings_on_full_domains']", "parent['matrix_unit_right_scaling_on_full_square_domain']")
draft = draft.replace('assert len(targets) == 13', 'assert len(targets) == 36')
start = draft.index("create(report, f'''")
end = draft.index("'''.encode('utf-8'))", start) + len("'''.encode('utf-8'))")
draft = draft[:start] + """create(report, f'''# Direita unitária regular no mesmo GNS — DEV

{DATE}. [REAL — três módulos/36 alvos compilados; revisão e integração pendentes]

Reutilizada scalarOrbit_right_regular para construir R_t Λ(A)=Λ(A λ_t)
no GNS do peso escalar completo. No espaço de órbitas, R_t é o multiplicador
de caráter na coordenada exterior composto com o shift na fibra interior.
São coordenadas diferentes. O produto A λ_t preserva n_ν e sua seminorma.
R_0=I, R_s R_t=R_(s+t), R_t*=R_(-t): a ação GNS é unitária.

No mesmo S fechado e seu adjunto máximo F=S†, o transporte do gráfico prova
R_t D(S)⊆D(S), S R_t=π(λ_t*)S; π(λ_t)D(F)⊆D(F), Fπ(λ_t)=R_t*F.
Daí, no MESMO A=S†S e em TODO domínio composto:

    R_t x ∈ D(A) ↔ x ∈ D(A),       A R_t x = R_t A x.

A equivalência de domínio usa a inversa já construída R_(-t). Nenhum campo
KMS ou igualdade de fluxo foi acrescentado como hipótese. A construção
atua na família λ_t; ainda não é uma representação direita provada de N inteiro.

[OPEN] Identificar A^it com o fluxo candidato e provar KMS global; traço,
escala dual, canto Three Locks, H1/H2/H3 físicos compatíveis, setor quântico
interagente e consumo integral pelo certificado/runtime. Seis flags falsas.
O vínculo de domínio antes aberto para λ_t foi reduzido por prova concreta.

Integração anterior: {parent['integrated_records']} registros,
{parent['controls']} controles, {parent['audit_declarations']} declarações Audit.
Este DEV ainda não altera um.py nem as 34 memórias: atualização pendente
após revisão nesta sessão. Cópia `{sha(ROOT / 'um.py')}`, mãe `{sha(parent_path)}`.
Monólito original e cópia não foram executados/importados integralmente.
Falha auxiliar de impressão cp1252 não afetou bytes da fonte nova; foi
conferida por releitura e pela compilação. Não houve falha matemática por isso.
'''.encode('utf-8'))""" + draft[end:]
create('record_regular_right_draft.py', draft)

prep = common((ROOT / 'prepare_right_square_stage.py').read_text(encoding='utf-8'))
prep = prep.replace("len(draft['targets']) == 13", "len(draft['targets']) == 36")
prep = prep.replace('count == 347', 'count == 360')
a = prep.index('text = once(text, "\'ScalarRightClosedTomita\'')
b = prep.index('save(path, text)', a)
prep = prep[:a] + '''text = once(text, "'HomogeneousRightSquareDomain', 'MatrixUnitRightSquare']",
    "'HomogeneousRightSquareDomain', 'MatrixUnitRightSquare',\\n                " +
    ', '.join(map(repr, names)) + ']')
text = once(text, '== 360', '== 396')
''' + prep[b:]
prep = prep.replace('V350ScalarRightTomitaAdjoint.lean', 'V350MatrixUnitRightSquare.lean')
a = prep.index('anchor = "        \'scalarTomitaAdjoint_left_intertwines')
b = prep.index('save(path, text)', a)
prep = prep[:a] + '''anchor = "        'matrixUnit_TomitaSquare_right_scaling'),\\n"
text = once(text, anchor, anchor + \'''    'same_square_regular_right_unitary_full_domain': (
        'regularRightGNS_unitary', 'regularRightGNS_intertwines',
        'scalarClosedTomita_regular_right_intertwines',
        'scalarTomitaAdjoint_regular_left_intertwines',
        'scalarTomitaSquare_regular_right_commutes', 'scalarRegularRight_squareDomain_iff'),
\''')
''' + prep[b:]
prep = prep.replace("'new_targets': 13", "'new_targets': 36").replace('count + 13', 'count + 36')
create('prepare_regular_right_stage.py', prep)

rec = common((ROOT / 'record_right_square_progress.py').read_text(encoding='utf-8'))
# Preserve the current parent before renaming only the OUTPUT custody.
rec = rec.replace('record_right_square_progress.py', 'record_regular_right_progress.py')
rec = rec.replace('prepare_right_square_stage.py', 'prepare_regular_right_stage.py')
rec = rec.replace('verify_right_square_custody.py', 'verify_regular_right_custody.py')
rec = rec.replace('SCALING_INTEGRATED', 'UNITARY_INTEGRATED')
rec = rec.replace('len(modules) == 2 and len(targets) == 13', 'len(modules) == 3 and len(targets) == 36')
a = rec.index("write(report, f'''")
b = rec.index('for p in surfaces:\n    raw = before', a)
rec = rec[:a] + """write(report, f'''# Direita unitária regular — integração revisada

{DATE}. [REAL — três módulos/36 alvos integrados e revisados]

No mesmo GNS H_I do peso escalar completo, R_t Λ(a)=Λ(a λ_t), R_0=I,
R_s R_t=R_(s+t) e R_t*=R_(-t). A órbita já existente foi reaproveitada
como caráter na coordenada exterior vezes shift na fibra interior.

O MESMO S fechado satisfaz S R_t=π(λ_t*)S em D(S), e seu adjunto máximo
F=S† satisfaz Fπ(λ_t)=R_t*F em D(F). A composição A=S†S, já provada
positiva e auto-adjunta nos estágios anteriores, agora satisfaz:

    R_t x ∈ D(A) ↔ x ∈ D(A),        A R_t x = R_t A x.

A igualdade usa TODO o domínio composto. A inversa R_(-t) dá o retorno;
não se assume continuidade de S, KMS ou igualdade com um fluxo candidato.
Este resultado resolve a pendência para o gerador regular registrada no
[relatório anterior](<{(ROOT / 'RELATORIO_ESCALA_DIREITA_SQUARED_INTEGRADA.md').as_posix()}>).
As unidades matriciais locais já tinham A R_y=(w_i/w_j)R_y A; os dois
resultados agora se referem ao mesmo operador e ao mesmo GNS.

[OPEN] Isto não identifica A^it com o fluxo modular completo, nem prova
KMS global, nem estende por si só a ação direita a toda N. Não foi provada
nova continuidade forte de R_t nesta etapa. Restam traço/escala/canto
Three Locks, H1/H2/H3 físicos no mesmo modelo, setor quântico interagente
e consumo pelos certificados/runtime. Einstein/Fisher/gauge encontrados
na pasta Chatgpt serão reutilizados com suas hipóteses. Seis flags falsas.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']}
fontes embutidas. Revisões DEV e integrada lidas, dependências reutilizadas
com pins. Corpo Python fora do embutido preservado; metadados Audit atuais
verificados. Nenhum monólito executado/importado. Gate legado inalterado.

[Revisão DEV](<{reviews[0].as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
[Reaproveitamento de Chatgpt](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`;
mãe integrada e de memória `{sha(parent_path)}`. Objetivo integral ativo.
'''.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] Três módulos/36 alvos constroem a direita
unitária R_t do gerador regular λ_t no mesmo GNS H_I e provam, no MESMO
A=S†S, R_t x∈D(A) ↔ x∈D(A) e A R_t x=R_t A x. A fórmula de órbita
scalarOrbit_right_regular foi reutilizada; os domínios completos de S e
S† foram transportados antes da composição. Não se postulou KMS.
Esta pendência para λ_t no registro anterior está resolvida. A relação
matricial local de escala anterior e a nova comutação usam o mesmo A.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit. Revisões DEV e integrada lidas.
Cópia {sha(ROOT / 'um.py')}; original preservado; seis flags maiores falsas.
Metadados Audit atuais conferidos; sem runtime integral; gate inalterado.

[OPEN] Potências de A e identificação do fluxo/KMS global; continuidade
forte e extensão da direita ainda não demonstradas neste novo módulo;
traço/escala/canto Three Locks, H1/H2/H3 físicos compatíveis, interação
quântica e consumo pelo certificado. Reutilizar Einstein/Fisher/gauge já
encontrados, descarregando suas hipóteses. Objetivo integral ativo.

[Prova, revisão e limites](<{report.as_posix()}>).
'''
""" + rec[b:]
rec = once(rec, "write(ROOT / 'right_square_custody.json'", "write(ROOT / 'regular_right_custody.json'")
rec = once(rec, "'custody': 'right_square_custody.json'", "'custody': 'regular_right_custody.json'")
create('record_regular_right_progress.py', rec)

ver = (ROOT / 'verify_right_square_custody.py').read_text(encoding='utf-8')
ver = ver.replace('right_square_custody', 'regular_right_custody')
ver = ver.replace('same_actual_square_domain_right_invariant', 'same_actual_square_domain_regular_invariant')
ver = ver.replace('matrix_unit_right_scaling_on_full_square_domain', 'regular_right_commutes_on_full_square_domain')
create('verify_regular_right_custody.py', ver)
print('Four new helpers created and syntax checked; previous sealed helpers untouched.')
