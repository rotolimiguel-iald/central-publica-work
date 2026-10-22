from pathlib import Path
import hashlib, json, datetime, os

root = Path(__file__).resolve().parent
chat = root.parent
base = chat / 'TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k'
prior = chat / 'TETELESTAI_V351_FECHO_MATEMATICO/A2_012'
sources = [base / 'TGL/ModularRealization.lean',
           base / 'TGLExt/V351RegularCoreTraceContract.lean',
           base / 'TGLExt/V350RegularDualAction.lean',
           prior / 'src/TGLExt/V354PositiveTraceReader.lean',
           prior / 'src/TGLExt/V354TraceReaderWall.lean',
           prior / 'AUDIT_NAMES_DELTA01.json']
def pin(path):
    b = path.read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def create(path, data):
    assert not path.exists(), path
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_bytes(data)
    assert temporary.read_bytes() == data
    os.replace(temporary, path)
record = {
 'created':datetime.datetime.now().astimezone().isoformat(),
 'status':'OPEN_CONSTRUCTION_NOT_A_DELIVERY',
 'consumer':'TGL.ContinuousCoreData.canonicalTrace, trace_tracial, trace_star, trace_dual_scaling',
 'reuse': [pin(p) for p in sources],
 'already_paid':'A1 positive normal faithful semifinite quadratic trace; A2 support, normalized split, minimal affiliated lock and relative gap (33 names).',
 'new_bridge':'Complete the positive trace along algebraic shift equivalence; preserve the legacy total reader signature.',
 'hard_lemma':'Positive shift-equivalent operators in the same regular core have the same A1 trace. NOT established by this fiche.',
 'plan':['Prove the algebraic equivalence and its star/automorphism covariance.',
         'Define the supremum of positive readings in an equivalence class.',
         'Prove cyclicity, star and dual transport; prove agreement with A1 only after the positive compatibility lemma.',
         'Seek the analytic positive compatibility proof; do not instantiate the old witness with an unproved premise.'],
 'coordination':'Poincare owns the actual projection-lattice/SUSY sidecar A2_SUSY_012. A generic polar operator, if constructed there, is a shared supplier; no duplicate implementation.',
 'searches':[{'root':str(base/'.lake/packages/mathlib/Mathlib'),'pattern':'ShiftEquiv|shiftEquiv|shift_equiv','result':'rg found no matching name'},
             {'scope':'Mathlib/Analysis generic polar names; existing tower polar is a different operator','result':'No generic bounded-operator polar supplier located in the searches recorded this turn; not a claim of mathematical nonexistence.'}],
 'limits':['No new theorem about nature.','No gate change.','A quotient/completion alone does not establish agreement with the positive trace.','Original program, canonical kernel and delivered A2 modules remain unchanged.']}
create(root/'REAPROVEITAMENTO.json',json.dumps(record,ensure_ascii=False,indent=2).encode('utf8'))
md = '''# A2 — extensão da leitura do traço

[OPEN] Ficha anterior ao código desta rota. A1 e os 33 termos de A2 já verificados são fornecedores; não serão reprovados.

O contrato antigo pede uma função no anel inteiro, cíclica em xy/yx. A convenção zero fora do cone positivo foi refutada para esse fim. Isso não refuta todas as extensões possíveis.

A proposta é completar a leitura por uma equivalência algébrica de deslocamento com lag. Produtos xy e yx pertencem à mesma classe. A leitura total será o supremo das leituras positivas da classe. O ponto analítico decisivo permanece explícito: dois positivos na mesma classe devem ter o mesmo traço A1. Sem essa prova, não se obtém a normalização de P_F nem o habitante completo de ContinuousCoreData.

Consumidor: os campos canonicalTrace, trace_tracial, trace_star e trace_dual_scaling de ContinuousCoreData. Fornecedores e hashes medidos constam do JSON adjunto. A relação e a leitura são instrumentos dessa ligação, não uma nova realização física.

Poincare trabalha separadamente no SUSY sobre projeções do core. Um eventual polar parcial genérico será compartilhado, não reimplementado. Nenhum arquivo canônico ou fonte da entrega anterior é alterado.
'''
create(root/'REAPROVEITAMENTO.md',md.encode('utf8'))
print(json.dumps({'created':str(root),'sources':len(sources),'status':record['status']}))
