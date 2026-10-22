"""Create the next custody helpers without changing any accepted artifact."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)

def create(name, text):
    ast.parse(text)
    path = ROOT / name
    assert not path.exists(), path
    raw = text.encode('utf-8')
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw
    temporary.replace(path)
    assert path.read_bytes() == raw

source = (ROOT / 'record_tomita_polar_progress.py').read_text(encoding='utf-8')
source = source.replace('TOMITA_POLAR_INTEGRATED', 'TOMITA_INVOLUTION_INTEGRATED')
source = once(source, "parent_path = ROOT / 'tomita_root_custody.json'", "parent_path = ROOT / 'tomita_polar_custody.json'")
source = once(source, "parent = json.loads(parent_path.read_bytes())", """parent = json.loads(parent_path.read_bytes())
memory_path = ROOT / 'tomita_involution_dev_memory_custody.json'
memory = json.loads(memory_path.read_bytes())
assert memory['parent_custody_sha256'] == sha(parent_path)
assert memory['working_sha256'] == parent['working_sha256']""")
source = once(source, "draft_names = ['tomita_root_domain_draft_status.json', 'tomita_polar_draft_status.json']", "draft_names = ['tomita_involution_draft_status.json']")
source = source.replace('REVIEW_SCALAR_TOMITA_POLAR_INTEGRATED', 'REVIEW_SCALAR_TOMITA_INVOLUTION_INTEGRATED')
source = source.replace('INTEGRATED_TOMITA_POLAR_REVIEW', 'INTEGRATED_TOMITA_INVOLUTION_REVIEW')
source = once(source, "assert len(modules) == 9 and len(targets) == 41", "assert len(modules) == 4 and len(targets) == 19")
source = source.replace("parent['surface_sha256']", "memory['surface_sha256']")
source = once(source, "report_path = ROOT / 'RELATORIO_FATOR_POLAR_TOMITA_INTEGRADO.md'", "report_path = ROOT / 'RELATORIO_INVOLUCAO_POLAR_TOMITA_INTEGRADA.md'")
start = source.index("report = f'''")
end = source.index("write(report_path, report.encode('utf-8'))", start)
source = source[:start] + """report = f'''# Involução polar no H_I original — integração revisada

{DATE}. [REAL — quatro módulos/19 alvos integrados e revisados]

O fator U construído a partir do S fechado e da raiz B no mesmo H_I satisfaz
U²=I. Isso foi provado a partir de SR=(I−R)S em D(S), UR=(I−R)U, conjugação
positiva das raízes e S²=I sobre Ran √R densa. A prova de conjugação usa
antiunitariedade, sem assumir involução. A igualdade exata D(B)=D(S) e S=UB
do pacote anterior são consumidas. As quatro fontes e suas dezenove declarações
receberam revisão DEV e foram transportadas literalmente, exceto importações,
para TGLExt.V350; as raízes e o Audit da cópia foram compilados.

{len(build['records'])} registros incrementais rc0, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações Audit, {integration['embedded_files']}
arquivos Lean embutidos. Os alvos novos usam apenas propext, Classical.choice e
Quot.sound. A execução reutilizou dependências anteriores com pins; não é um
rebuild global nem runtime integral. O corpo Python fora do embutido é idêntico
ao estágio polar anterior. Os testes verificam também que a nova involução não
descarrega indevidamente KMS, traço ou as hipóteses físicas do gate.

[OPEN] Identificar S com o domínio máximo do peso, realizar o fluxo modular/KMS,
construir o traço canônico com sua escala dual e o canto Three Locks no mesmo
modelo. Entregar H1/H2/H3 físicos compatíveis e consumi-los na ponte de Einstein
já existente. Completar o setor quântico interagente/BRST/QME e o certificado
integral consumido pelo gate. U²=I sozinho não fornece essas etapas nem identifica
U com qualquer outro objeto chamado J. O original permanece preservado; seis
flags maiores falsas, gate legado inalterado e objetivo integral ativo.

O ideal inicial I exige limite uniforme da forma em todos os vetores
(`HasFiniteDualSquare`); o domínio n_ν exige finitude do peso escalar. A rota
de identificação deve justificar o completamento e o núcleo do gráfico no
domínio máximo. Não se presume nem se impõe aqui igualdade literal I=n_ν.

[Prova DEV, domínios e falhas preservadas](<{(ROOT / 'RELATORIO_INVOLUCAO_POLAR_TOMITA_DEV.md').as_posix()}>).
[Revisão independente DEV](<{(ROOT / 'revisao/REVIEW_SCALAR_TOMITA_INVOLUTION.md').as_posix()}>).
[Revisão integrada](<{review.as_posix()}>).
[Reaproveitamento do acervo Chatgpt](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`.
Mãe matemática `{sha(parent_path)}`; mãe de memória `{sha(memory_path)}`.
Os relatos anteriores de U²=I aberto e de DEV pendente permanecem históricos.
'''
""" + source[end:]
start = source.index("note = f'''")
end = source.index('for path in surfaces:\n    raw = before_surfaces', start)
source = source[:start] + """note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] U²=I foi agora integrado na cópia, no mesmo H_I e
para o mesmo fator de S=UB. Quatro módulos/19 alvos, com tipos e domínios exatos,
somente o trio lógico permitido. A troca do resolvente e das raízes positivas
usa a antiunitariedade de U; a involução é conclusão, não hipótese inserida.
Os registros anteriores, inclusive o DEV sem integração, permanecem históricos.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']}
embutidos. Revisões DEV e integrada lidas. Dependências reutilizadas com pins,
sem runtime integral do monólito. Original preservado, gate legado inalterado.

[OPEN] Domínio máximo do peso/KMS, traço/canto Three Locks, H1/H2/H3 físicos
no mesmo modelo, setor quântico interagente e consumo pelo certificado completo.
Seis flags maiores falsas; objetivo integral ativo. Reutilizar os teoremas de
Einstein, métrica e gauge já localizados em Chatgpt, mantendo suas hipóteses.
O ideal inicial uniforme e o domínio escalar n_ν são condições distintas;
identificar completamento e núcleo do gráfico não pressupõe I=n_ν.

[Relatório](<{report_path.as_posix()}>).
[Revisão integrada](<{review.as_posix()}>).
'''
""" + source[end:]
start = source.index('artifact_names = [')
end = source.index('custody = {', start)
source = source[:start] + """artifact_names = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'RELATORIO_INVOLUCAO_POLAR_TOMITA_DEV.md',
    'record_tomita_involution_draft.py', 'record_tomita_involution_memory.py',
    'prepare_tomita_involution_stage.py', 'record_tomita_involution_progress.py',
    'verify_tomita_involution_custody.py', 'generate_tomita_involution_record_helpers.py',
    'tomita_involution_dev_memory_custody.json'] + draft_names
reviews = [review, ROOT / 'revisao/REVIEW_SCALAR_TOMITA_INVOLUTION.md']
""" + source[end:]
source = once(source, "'previous_custody_sha256': sha(parent_path), 'original_sha256': sha(original),", """'previous_custody_sha256': sha(parent_path), 'original_sha256': sha(original),
    'previous_memory_custody_path': str(memory_path),
    'previous_memory_custody_sha256': sha(memory_path),""")
source = once(source, "'polar_involution_proved': False", "'polar_involution_proved': True")
source = once(source, "write(ROOT / 'tomita_polar_custody.json'", "write(ROOT / 'tomita_involution_custody.json'")
source = once(source, "'custody': 'tomita_polar_custody.json'", "'custody': 'tomita_involution_custody.json'")
create('record_tomita_involution_progress.py', source)

source = (ROOT / 'verify_tomita_polar_custody.py').read_text(encoding='utf-8')
source = source.replace('tomita_polar_custody', 'tomita_involution_custody')
source = once(source, "assert sha(Path(c['previous_custody_path'])) == c['previous_custody_sha256']", """assert sha(Path(c['previous_custody_path'])) == c['previous_custody_sha256']
assert sha(Path(c['previous_memory_custody_path'])) == c['previous_memory_custody_sha256']
memory = json.loads(Path(c['previous_memory_custody_path']).read_bytes())
assert c['surface_before_sha256'] == memory['surface_sha256']
assert c['polar_involution_proved'] and not c['modular_weight_identified']""")
create('verify_tomita_involution_custody.py', source)
print('Created record and verifier helpers; no integrated source or memory modified.')
