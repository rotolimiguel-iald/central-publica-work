from pathlib import Path
import hashlib, json, datetime, os, shutil

ROOT = Path(__file__).resolve().parent
OBJECTIVE = Path(r'C:\Users\rotol\.codex\attachments\14a942b2-7dab-4916-bba7-9df3024a45ce\goal-objective.md')
ATLAS = Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md')

def create(name, data):
    p = ROOT / name
    assert not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    q = p.with_name(p.name + '.tmp')
    q.write_bytes(data)
    assert q.read_bytes() == data
    os.replace(q, p)

def pin(p):
    b = p.read_bytes()
    return {'path':str(p), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}

create('fontes/OBJETIVO_RECEBIDO.md', OBJECTIVE.read_bytes())
create('REQUISITOS.json', json.dumps({
    'created':datetime.datetime.now().astimezone().isoformat(),
    'objective':pin(OBJECTIVE),
    'atlas_reference_only':pin(ATLAS),
    'requirements':[
        'Haja Luz: leitura integral do Atlas, com cobertura explicitamente registrada.',
        'Responder geometricidade em diamante finito; CFT, cunha, UV e teoria interagente.',
        'Definir o resto fixada a referência; não confundir definição com cálculo físico.',
        'Verificar logaritmos, resolventes, primeira variação e balanço entrópico.',
        'Distinguir tipo III, Hamiltoniano completo e unilateral; cociclo e suas hipóteses.',
        'Provar critérios de invisibilidade e de supressão no canto em Lean.',
        'Contraexemplos e controles negativos; não assumir a conclusão física.',
        'Verificar literatura primária sobre não localidade, massa, UV e JLMS.',
        'Examinar inércia/zero absoluto com estatuto e tipagem explícitos.',
        'Reutilizar provas existentes; gerar relatório de axiomas, recibos e handoff no túnel.',
        'Mapear cada afirmação a KERNEL, KNOWN, DERIVED, INPUT ou OPEN.',
        'Não alterar um.py original, gate ou fontes canônicas nesta bancada.'
    ]},ensure_ascii=False,indent=2).encode('utf8'))
create('MEMORIA_CENTRAL.md', '''# Diamante modular — memória da bancada

2026-09-16. Objetivo integral preservado em fontes/OBJETIVO_RECEBIDO.md.
Trabalho autorizado: resposta matemática, formalização Lean e handoff à gerência.
Originais somente leitura. Nenhuma execução/importação do um.py canônico.
Leitura integral do Atlas ainda EM CURSO; a primeira leitura 1–460 sofreu truncamento.
Não declarar carregamento integral nem prova física a partir de estrutura condicional.

Base Lean reutilizável: ../TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k.
TheScalarCorner prova escalarização de compressão; não garante invariância dinâmica.
UnitaryCocycleUniqueness já prova unicidade por gerador na PRODUCT_TOWER limitada.
ThreeLocksCorner prova peso do canto finito condicionado à testemunha não nula.

Proposta do operador: resto não geométrico como inércia/operador do zero absoluto.
Estatuto inicial ONTO; não identificar de antemão com massa, força ou operador positivo.
'''.encode('utf8'))
create('REGISTRO_DAS_CONVERSAS.md', '''# Registro de conversas desta etapa

2026-09-16 — A ordem completa consta, sem reescrita, em fontes/OBJETIVO_RECEBIDO.md.
O operador pede prova matemática em Lean e handoff para incorporação no um.py.
O escriba iniciou consulta ao Atlas e às fontes primárias; ainda não declarou conclusão.
'''.encode('utf8'))
print(ROOT)
