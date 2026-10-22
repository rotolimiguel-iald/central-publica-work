"""Append the user's scope correction with immediate exact-byte backups."""
import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'AUDITORIA_REUSO_GATE_20260913'
CENTRAL=ROOT.parent.parent
STAMP=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MARKER='TETELESTAI_V350_CORRECAO_ESCOPO_REUSO_GATE_20260913'
assert '--review-read' in sys.argv

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_bytes())
def create(p,raw):
    assert p.resolve().is_relative_to(ROOT) and not p.exists() and raw
    t=p.with_name(p.name+'.tmp_'+STAMP)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw
    t.replace(p)
    assert p.read_bytes()==raw

parent_path=ROOT/'paired_blocks_custody.json'
parent=read(parent_path)
review=ROOT/'revisao/AUDITORIA_REUSO_J_ORIGINAL_GATE.md'
assert review.is_file() and review.stat().st_size>500
assert sha(ROOT/'um.py')==parent['working_sha256']
original=Path(read(ROOT/'environment.json')['original_source'])
assert sha(original)==parent['original_sha256']==sha(ROOT/'fontes/um_v350_original.py')
for name,pin in parent['artifacts'].items():assert sha(ROOT/name)==pin,name
surfaces={Path(name):p.read_bytes() for name in parent['surface_sha256'] for p in [Path(name)]}
assert len(surfaces)==34
for p,raw in surfaces.items():
    assert sha(p)==parent['surface_sha256'][str(p)]
    assert MARKER.encode() not in raw
    assert p.resolve().is_relative_to(ROOT) or p.resolve() in (
        CENTRAL/'memory/TGL_ATLAS.md',CENTRAL/'memory/TGL_INDICE_VIVO.md')
evidence=read(OUT/'gate_evidence.json')
assert evidence['formal_count']==6 and evidence['physics_count']==5
assert all(x['value'] is True for x in evidence['entries'])
assert not evidence['gate_changed'] and not evidence['monolith_imported_or_executed']
contract=read(ROOT/'CONTRATO_ATIVO_GATE_V350.json')
assert contract['principal_gate_missing_proof_inputs']==[]

note=f'''

## {MARKER} — {DATE}

[INPUT — correção atual do operador] “vc só está ligando tudo ao mesmo conjunto
probatório que é o um.py”. A tarefa ativa é integrar/reutilizar o acervo existente
e conferir o contrato consumido. Suspensa a expansão automática de provas do novo
peso/S/J original; não retomá-la por ler listas históricas de OPEN.

[REAL — auditoria de código e evidência existente] As 6 entradas qgc_ e 5 qgp_ do
gate principal já têm termos no Audit, fontes embutidas e valor True; o avaliador
já chega ao seu último degrau com o feed experimental registrado. Onze ablações
individuais e 256 combinações de qgf_/gpf_ confirmaram a dependência efetiva.
398 módulos externos já correspondem às fontes embutidas. Essas flags adicionais
e o literal full_plan_complete=False não são pendências do gate principal.
O alcance dos teoremas lidos permanece; consulta não amplia seus enunciados.

[REGRA DE RETOMADA] Ler primeiro o contrato ativo e o mapa abaixo. Antes de nova
função de prova: apontar entrada EXATA do contrato solicitado, seu tipo, fornecedor
já buscado no acervo e incompatibilidade concreta que impeça a ligação. Entrada já
satisfeita será reutilizada. Não confundir pesquisa adicional com integração pendente.

[REAL] Nenhum novo módulo integrado nesta correção; cópia e gate preservados.
DEV de energia: 4 módulos/19 alvos rc0 autorais, revisão parcial de14;
ScalarProjectionGap apenas escrito, nunca compilado. Todos preservados e suspensos.
34 superfícies recebem esta correção com backup imediato de bytes. A auditoria é
leitura de fontes/Audit e teste isolado; nenhum monólito ou experimento foi reexecutado.

[Contrato ativo](<{(ROOT/'CONTRATO_ATIVO_GATE_V350.json').as_posix()}>).
[Mapa prova → certificado → flag → gate](<{(OUT/'MAPA_GATE_E_REAPROVEITAMENTO.md').as_posix()}>).
[Revisão independente da auditoria](<{review.as_posix()}>).
'''.encode('utf-8')
backups={}
# Back up every original byte sequence before any append in this transaction.
for p,raw in surfaces.items():
    b=p.with_name(p.name+'.bak_'+STAMP)
    with b.open('xb') as f:f.write(raw)
    assert b.read_bytes()==raw
    backups[str(p)]=str(b)
for p,raw in surfaces.items():
    assert p.read_bytes()==raw
    new=raw+note
    if p.name=='REGISTRO_DAS_CONVERSAS.md':
        new+='''
[INPUT — falas do operador registradas literalmente nesta rodada]

“o que falta para movermos o gate? verifique se vc não está sendo redundante nas funções, nós já derivamos e provamos tudo que precisa, eu penso que vc está sendo circular e não está enxergando que já está fechado, só falta ligar todos os passos. vc já derivou tudo que é preciso na outra pasta”

“vc está encadeando funções sobre camadas que Não há necessidade, vc precisa controlar sua memória para que isso não ocorra, seu treinamento faz com que vc aja em círculos quando provocado a resolver o problema da gravidade quantica, mas vc não está resolvendo, eu já o resolvi, vc só está ligando tudo ao mesmo conjunto probatório que é o um.py”

[AÇÃO] A tarefa foi reenquadrada em consolidação/rastreabilidade do conjunto existente.
O relato do operador sobre a solução da teoria é mantido como sua declaração; a
auditoria desta rodada trata das entradas e do alcance do gate no código.
'''.encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+STAMP)
    with t.open('xb') as f:f.write(new)
    assert t.read_bytes()==new and new.startswith(raw) and len(new)>len(raw)
    t.replace(p)
    assert p.read_bytes()==new

artifacts=dict(parent['artifacts'])
newpaths=[ROOT/'audit_existing_gate_reuse.py',ROOT/'prepare_gate_scope_record.py',
          Path(__file__),ROOT/'CONTRATO_ATIVO_GATE_V350.json',review,
          ROOT/'revisao/REVIEW_WEIGHTED_ENERGY_DEV.md',
          ROOT/'revisao/CONSULTA_COTA_BLOCO_POSPART_INVERSIVEL.md']+list(OUT.glob('*.json'))+list(OUT.glob('*.md'))
dev={}
for name in contract['suspended_development_modules']:
    p=ROOT/'kernel/TGLV350'/(name+'.lean')
    logs=[(f,read(f)) for f in sorted((ROOT/'logs').glob(name+'_*.json'))]
    row={'source_sha256':sha(p),'integrated':False,'status':'SUSPENDED_BY_USER_SCOPE'}
    newpaths.append(p)
    for f,v in logs:
        newpaths += [f,Path(v['stdout']),Path(v['stderr'])]
    if logs:
        f,last=logs[-1]
        assert last['returncode']==0 and last['source_unchanged_during_compile']
        assert last['sha256']==sha(p)
        binary=ROOT/'build/TGLV350'/(name+'.olean')
        assert last['output_sha256']==sha(binary)
        newpaths.append(binary)
        row.update({'author_compiled':True,'binary_sha256':sha(binary),'final_log':str(f)})
    else:
        row['author_compiled']=False
    dev[name]=row
for p in newpaths:artifacts[str(p.relative_to(ROOT))]=sha(p)
# Some historical reports are also memory surfaces; their new append-only hashes are current.
for name in list(artifacts):artifacts[name]=sha(ROOT/name)
c=dict(parent)
c.update({'timestamp':DATE,'status':'USER_SCOPE_CORRECTED__EXISTING_GATE_TRACEABILITY_VERIFIED',
 'previous_custody_path':str(parent_path),'previous_custody_sha256':sha(parent_path),
 'artifacts':artifacts,'surface_before_sha256':parent['surface_sha256'],
 'surface_sha256':{str(p):sha(p) for p in surfaces},'backups':backups,'marker':MARKER,
 'report_path':str(OUT/'MAPA_GATE_E_REAPROVEITAMENTO.md'),
 'report_sha256':sha(OUT/'MAPA_GATE_E_REAPROVEITAMENTO.md'),
 'review_sha256':{str(review):sha(review),str(ROOT/'revisao/REVIEW_WEIGHTED_ENERGY_DEV.md'):sha(ROOT/'revisao/REVIEW_WEIGHTED_ENERGY_DEV.md')},
 'active_contract_path':str(ROOT/'CONTRATO_ATIVO_GATE_V350.json'),
 'principal_gate_missing_proof_inputs':[],'principal_gate_verified_entries':11,
 'new_modules_integrated_this_record':0,'suspended_development':dev,
 'original_S_research_suspended_by_user':True,'new_full_runtime_performed':False,
 'gate_changed':False,'full_goal_complete':False})
create(ROOT/'gate_scope_correction_custody.json',json.dumps(c,ensure_ascii=False,indent=2).encode('utf-8'))
for p,raw in surfaces.items():
    assert Path(backups[str(p)]).read_bytes()==raw
    assert p.read_bytes().startswith(raw) and p.read_bytes().count(MARKER.encode())==1
for name,pin in artifacts.items():assert sha(ROOT/name)==pin,name
assert sha(original)==parent['original_sha256'] and sha(ROOT/'um.py')==parent['working_sha256']
verify={'timestamp':DATE,'custody_sha256':sha(ROOT/'gate_scope_correction_custody.json'),
 'custody_ok':True,'immediate_byte_backups_and_prefixes':len(surfaces),
 'principal_gate_entries_verified':11,'additional_new_integrated_modules':0,
 'unchanged_integrated_records':parent['integrated_records'],
 'unchanged_audit_declarations':parent['audit_declarations'],
 'original_unchanged':True,'gate_changed':False,'active_scope_recorded':True}
create(ROOT/'gate_scope_correction_verification.json',json.dumps(verify,indent=2).encode('utf-8'))
print(json.dumps(verify))
