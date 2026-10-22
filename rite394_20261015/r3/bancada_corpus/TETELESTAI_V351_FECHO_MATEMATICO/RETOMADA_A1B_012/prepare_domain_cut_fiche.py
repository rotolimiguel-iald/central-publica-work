from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='regularDomainCut|inverseLimitWeight_domainCut|inverseLimitWeight_square_finite|corte.{0,20}dominio.{0,20}limite'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_domain_cut'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_nonneg'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_le'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_one'),('TGLExt/V351RegulatorWeightOrder.lean','regularInverseGeneratorCutoff_commutes'),('TGLExt/V351RegulatorWeightOrder.lean','regularInverseGeneratorCutoff_resolvent_identity'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_right'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarPolarRightAlgebra'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_complement_injective'),('TGLExt/BoundedGraphOperator.lean','bounded_graph_domain_dense'),('.lake/packages/mathlib/Mathlib/Topology/UniformSpace/Equicontinuity.lean','Equicontinuous.isClosed_setOf_tendsto'),('TGLExt/V351PerturbedWeightOrder.lean','scalarWeight_right_perturbed_mono'),('TGLExt/V351ScalarWeightSemifiniteness.lean','scalarWeight_square_finite_wot_closure'),('TGLExt/V350RegularNormality.lean','strong_tendsto_wot'),('TGLExt/V350RegularTopology.lean','regularCore_wot_closed')]

providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:noncomputable )?(?:def|theorem|lemma) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    start=m.start();depth=0;end=None
    for i in range(start,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and (s.startswith(' :=',i) or s.startswith(' where',i)):end=i;break
    assert end is not None
    providers.append(dict(name=name,source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end],decision='REUSAR'))
target='Use q_delta=1-delta*B_delta, in the SAME regular core and polar right algebra. Prove positivity/contraction, the uniform product bound B_epsilon*q_delta^2 <= delta^(-1)*I and strong convergence q_(1/(n+1)) to I. Reuse the inverse identity, positivity of commuting products and dense range of 1-R. Consumers: finite-domain cutoff estimate of scalarInverseLimitWeight and WOT density of its square-finite set. This fiche covers that sequential route; it does not assert any new theorem or semifinal contract. No new root, spectral calculus, GNS, traciality or positive finite minorants of the original nontracial weight.'

stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_DOMAIN_CUT',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_CORTE_DOMINIO_LIMITE.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior ao corte de domínio do peso limite]\n\n# A1(b): corte algébrico sem outra raiz\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR a rota menor q_delta da consulta independente revisao_consulta_semifinitude_limite/CONSULTA_SEMIFINITUDE_LIMITE. A cota pode depender de delta, mas deve ser uniforme em epsilon antes do supremo. Semifinitude usual e minorantes positivos do contrato são obrigações distintas.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_CORTE_DOMINIO_LIMITE.md',s.encode('utf8'));print('FICHE',len(providers))
