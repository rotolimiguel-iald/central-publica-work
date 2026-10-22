from pathlib import Path
import os,json,hashlib,re,datetime
root=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
out=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes();return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def new(p,b):
    assert p.resolve().is_relative_to(root) and not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.replace(t,p);assert p.read_bytes()==b
specs=[
 ('TransverseGibbsResponse','RESPOSTA_GIBBS_TRANSVERSAL_20260909_180432_151368','Uniform reference has zero modular increment; nonzero Shannon response is measured Fisher, not intrinsic heat.'),
 ('MixedQuadraticGibbsResponse','RESPOSTA_GIBBS_MISTA_QUADRATICA_20260909_181702_377524','Positive normalized real weights; k>0; quadratic clock has zero tangent and equal entropy/modular coefficients. Matrix realization remains a written deduction.'),
 ('ProbeResponseRecord','RESPOSTA_MICROSCOPICA_FONTE_20260909','Response-first construction; metric supplied; positive null source; conservation uses closed and wave equations.'),
 ('MixedGibbsGravitationalBridge','PONTE_GIBBS_GRAVITACIONAL_20260909','Finite sum of probe responses; same coefficients transfer area matching, without identifying distinct states. Physical area correspondence remains explicit.'),
 ('FiniteCommutatorEvolution','SERIE_EVOLUCAO_FINITA_20260909_180052_668471','Actual finite conjugation equals the commutator series. Named local scalar/topological instances do not add axioms.'),
 ('SmallTimeLocalDynamics','LIMITE_LOCAL_TEMPO_CURTO_20260909_182022_034959','Dominated convergence and coefficient stabilization derive the local norm limit when 2J|t|<1, pointwise in time. No assumed infinite limit.')
]
rows=[]
for name,folder,scope in specs:
    source=root/folder/(name+'.lean'); raw=source.read_bytes(); s=raw.decode('utf8')
    decl=re.findall(r'(?m)^(?:local\s+)?(?:noncomputable\s+)?(abbrev|def|theorem|structure|instance)\s+(\w+)',s)
    prints=re.findall(r'(?m)^#print axioms (\w+)$',s)
    assert len(decl)==len(prints)==len(set(prints)) and {n for _,n in decl}==set(prints)
    good=[]
    for rp in sorted((root/folder).glob('BUILD_*/BUILD_RESULT.json')):
        r=json.loads(rp.read_bytes())
        if r['status']=='PASS_COMPILED_SCOPE' and any(z['sha256']==pin(source)['sha256'] for z in r['sources']):
            assert (rp.parent/(name+'.lean')).read_bytes()==raw
            assert len(r['runs'])==2 and all(z['exit_code']==0 for z in r['runs'])
            assert len(r['axiom_rows'])==len(decl)
            assert all(set(z['axioms'])<={'propext','Classical.choice','Quot.sound'} for z in r['axiom_rows'])
            good.append(rp)
    assert good,name
    rows.append({'module':name,'source':pin(source),'receipt':pin(good[-1]),'theorems':sum(k=='theorem' for k,n in decl),'other_declarations':sum(k!='theorem' for k,n in decl),'axiom_audits':len(decl),'scope_analysis':scope})
data={'status':'SIX_FROZEN_LEAVES_MEASURED','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'modules':rows,'counts':{'modules':len(rows),'theorems':sum(r['theorems'] for r in rows),'other_declarations':sum(r['other_declarations'] for r in rows),'axiom_audits':sum(r['axiom_audits'] for r in rows)},'joint_integration':False,'um_py_executed':False,'originals_written':False,'analysis':'Scope notes record the main task analysis. They do not attribute approval to a different reviewer. Separate reviewer notes retain their own authorship.'}
new(out/'INVENTARIO_SEIS_FONTES.json',(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode())
dp=root/'DINAMICA_EXTENSIVA_DEMONSTRACAO_20260909_1813'/'DEMONSTRACAO_DINAMICA_EXTENSIVA.md'
review={'status':'MAIN_TASK_WRITTEN_PROOF_ANALYSIS','source':pin(dp),'analysis_document':pin(out/'DEDUCAO_RESPOSTA_E_FRONTEIRA.md'),'method':'The main task read the proof text and inspected the local source contracts. The analysis checks the factorial bound, Volterra order, compact-input globalization, Gaussian KMS passage, and normality counterexample.','outcome':'No mathematical gap identified in the stated C-star dynamics scope. Infinite global dynamics and KMS arguments are written derivations, not Lean compilation claims.','external_reviewer_approval_attributed':False,'changes_to_reviewed_source':False}
new(out/'ANALISE_DINAMICA_TAREFA_PRINCIPAL.json',(json.dumps(review,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(data['counts']))
