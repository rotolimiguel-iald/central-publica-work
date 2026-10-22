from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='regularInverseGeneratorCutoff_cfc|regularInverseGeneratorCutoff_sqrt_right|scalarRightAction_sqrt|inverseCutoffFunction'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_cutoff_cfc'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_graph_iff'),('TGLExt/V351RegularSpectralGraph.lean','regularPositiveGenerator_graph_iff'),('TGLExt/V351SineResolventApprox.lean','regularSpectralResolvent_right'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarRightAction_cfc'),('TGLExt/V351ScalarMultiplierCalculus.lean','realScalarMultiplier_cfc_ae'),('TGLExt/GeneralExpectationCP.lean','factor_positive_sqrt_mem'),('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean','sqrt_eq_real_sqrt'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/NonUnital.lean','cfcₙ_eq_cfc'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean','cfc_real_eq_complex')]



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
target='For epsilon>0 identify the EXISTING regularInverseGeneratorCutoff P epsilon with cfc F_epsilon (regularSpectralResolvent P), F_epsilon(z)=ofReal(z.re / max(min(1,epsilon),1+(epsilon-1)*z.re)). Prove global continuity from the positive clamped denominator and equality to 1/(epsilon+exp(-kappa)) at z=sigmoid(kappa). Use original graph_iff and inverse-cutoff graph_iff to identify candidate Y through (Yx,x-epsilonYx) in the SAME graph. This avoids a new inverse of I+(epsilon-1)R or a new shifted scalar multiplier. Then consume the already proved P(R), cfc membership and standard CFC.sqrt bridges to obtain the SAME CFC.sqrt B_epsilon right action on ALL n_nu. Consumer: norm identity for the bounded positive cut perturbations of the SAME scalar weight. Do not claim their limit, monotonicity or traciality in this target.'



stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_EXISTING_CUTOFF_CFC',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_CFC_CORTES.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à identificação CFC dos cortes existentes]\n\n# A1(b): o mesmo Bε, sua raiz positiva e a ação direita\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR: o inverso regular, seu grafo e P(R) já estão produzidos. A ponte é identidade escalar/CFC com a equação inversa existente, sem novo h, J ou GNS. factor_positive_sqrt_mem é molde somente: seu tipo é o fator da torre, não a álgebra da ação direita. Serão usados os conversores CFC existentes. Os aproximantes têm auditoria autoral rc0 e revisão pendente neste instante.\n\n'


for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_CFC_CORTES.md',s.encode('utf8'));print('FICHE',len(providers))
