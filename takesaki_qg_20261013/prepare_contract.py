"""Create an additive scientific contract for the existing Takesaki job."""
from pathlib import Path
import hashlib, json, sqlite3
BASE = Path(r'C:\IALD\Central de Patentes')
OUT = BASE / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TAKESAKI'
OUT.mkdir(parents=True, exist_ok=True)
WORK = BASE / 'work/takesaki_qg_20261013'
QUEUE = BASE / 'Chatgpt/IALD_ORQUESTRACAO_20260923'
K = BASE / 'work/cadeia_de_selo/v392/kb_stub_v392/TGLExt'
def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
def write(name, data):
    with (OUT/name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
con=sqlite3.connect((QUEUE/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True)
con.row_factory=sqlite3.Row
job=dict(con.execute('SELECT * FROM coordination_jobs WHERE id=?',('ff9a08c5-5b3a-4b17-b0ea-319d59a978a2',)).fetchone())
assert job['request_id']=='9fec8d26-d3b7-4262-b4e6-e3a5aa450760'
assert job['stage']=='awaiting_dispatch' and not job['execution_task_id']
sources=[K/n for n in ['Fundacao.lean','GlobalLiftLadder.lean','V351RegularCoreTraceConstruction.lean','V351DualScalingBridge.lean','AgapeNonVacuity.lean']]
sources += [BASE/'work/identidade_cordeiro_13out/5_R2/pedra/TheIdentityHasAName.lean',BASE/'work/cunhagens_13out/OPERADOR_13out_invariancia_escala_identidade_verbatim.txt']
contract={
 'schema':'iald-scientific-contract-supplement/v1',
 'unit':'F1.TAKESAKI','board_events':{'created':732,'claimed':733},
 'request_id':job['request_id'],'job_id':job['id'],
 'original_prompt_sha256':hashlib.sha256(job['prompt'].encode()).hexdigest(),
 'original_memory_context_id':job['memory_context_id'],
 'preserve_original':True,
 'execution_constraints':{'mission_id':'TGL_BANCADA_OFICIAL','branch_id':'F1.TAKESAKI','lemma_id':'takesaki_from_modular_identity_v1','role':'draft','required_provider':'kimi','max_calls':1,'max_projection_chars':None},
 'authenticated_scope_order':{'source':pin(WORK/'OPERADOR_13out_autorizacao_verbatim.txt'),'origin':'direct human user message in official Codex thread','thread_id':'01a11878-6e36-7d10-83c4-cd72e757fdd0','authorization':'create a dedicated Takesaki unit, complete this existing contract, proceed through orchestration; v392 valid working basis pending ratification'},
 'primary_source_pins':[pin(p) for p in sources],
 'working_v392':pin(BASE/'work/cadeia_de_selo/v392/um_v392_candidato.py'),
 'bibliography_to_verify':[{'author':'Masamichi Takesaki','year':1973,'title':'Duality for crossed products and the structure of von Neumann algebras of type III','doi':'10.1007/BF02392041','url':'https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6158-11511_2006_Article_BF02392041.pdf','status':'KNOWN bibliographic item; external bytes not yet pinned in this supplement'},{'author':'Fumio Hiai','title':'Concise lectures on selected topics of von Neumann algebras','url':'https://arxiv.org/abs/2004.02383','status':'KNOWN bibliographic item; inspect continuous-core theorem and conventions'}],
 'scientific_acceptance':[
 'Reuse the existing V351 scaling law and positive finite witness; do not claim the full crossed product is already constructed.',
 'Name separately: faithful normal state/weight, modular/KMS characterization, crossed product, dual action convention, affiliated positive operator and its domain, invariant dual weight, canonical normal semifinite faithful trace.',
 'Identify exactly which hypotheses imply the exponential law; normalization omega(I)=1 alone and state preservation under an arbitrary flow must not be silently promoted to the complete modular construction.',
 'Fix signs: theta_s(lambda(t))=exp(-i*s*t)lambda(t); h^(it)=lambda(t); theta_s(h)=exp(-s)h. Prove scaling via dual-weight invariance and inverse-density transformation, with unbounded operators handled by spectral cutoffs.',
 'A family tau_s=exp(-s)tau_0 is only a rescaled family unless an actual algebra automorphism and its trace covariance are constructed. A finite unital algebra with positive finite tau(1) cannot support nontrivial exponential scaling of that same trace under unital automorphisms.',
 'Give falsifiers/counterexamples with well-typed domains; own modular invariance is a theorem, so distinguish dropping it from replacing the modular flow by a different flow.',
 'Return textual derivation, exact dependencies, proposed Lean statements, what already compiles vs remains OPEN; no sorry or axioms masquerading as proved mathematics.',
 'No production modifications, no data opening, no gate change; model response remains DECLARADO pending local verification.'
 ],
 'dispatch_instruction':'Supplement the existing identity through a reviewed protocol/CAS transition if needed; do not submit a replacement request or change the original inscription. Worker coordination owns the transition. If the installed API cannot bind previously-null constraints, return the exact technical blocker and a minimal candidate fix, preserving identities.',
 'context_delivery':'Common canonical memory remains required. Add explicit v392 source excerpts/pins from this contract; label the installed common memory generation separately if older. Never silently substitute generation or claim v392 was received from a v391-only packet.'
}
write('CONTRATO_TAKESAKI_R1.json',contract)
write('SOURCE_PINS_R1.json',contract['primary_source_pins'])
write('QUEUE_IDENTITY_R0.json',{k:job.get(k) for k in ['id','request_id','stage','version','execution_constraints','execution_task_id','memory_context_id']})
print(json.dumps({'contract':pin(OUT/'CONTRATO_TAKESAKI_R1.json'),'sources':len(sources)},ensure_ascii=False))
