from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='scalarWeight_right_perturbed_mono_all|perturbed.{0,35}(all_positive|all_squares)|peso.{0,35}perturbado.{0,25}todos'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_all_positive_weight_order'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351PerturbedWeightOrder.lean','scalarWeight_right_perturbed_mono'),('TGLExt/V351WeightAverageRecovery.lean','scalarWeight_square_eq_iSup_averages'),('TGLExt/V350ScalarDualWeight.lean','scalarDualWeight_square_finite_strong_density'),('TGLExt/V351CutoffAverageCommutation.lean','regularInverseCutoffSqrt_commutes_average'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('TGLExt/V350AntiunitaryPositiveConjugation.lean','hilbertPositiveSqrt'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarRightAction_cfc')]

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
target='Extend scalarWeight_right_perturbed_mono from A in n_nu to EVERY A in N, using exact average recovery for A*b and A*c, finite averages A*e_n, and explicit hypotheses that b and c commute with the SAME regularAverage P delta. Then for EVERY positive X in the SAME N instantiate A as the EXISTING hilbertPositiveSqrt(X), proving its membership in N by norm closure and existing real CFC membership, and A*A=X by existing sqrt identity. Keep b b* <= c c*, membership in scalarPolarRightAlgebra and average commutation explicit. No new definition of weight, root, GNS, core or regularizer. The actual cutoff roots discharge those hypotheses via existing suppliers; regulator-order B_epsilon <= B_eta itself is a separate consumer/obligation. Infinite values allowed. This does not prove traciality, final semifinitude, or completion of A1(b).'

stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_ALL_POSITIVE_WEIGHT_ORDER',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_ORDEM_TODOS_POSITIVOS.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à extensão de ordem]\n\n# A1(b): ordem em todos os positivos do mesmo core\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR: compor os três fornecedores já provados; não criar outro ideal ou peso. A aproximação é dos VALORES e não de minorantes positivos. Reusar CFC.sqrt_eq_real_sqrt, cfcₙ_mem e CFC.sqrt_mul_sqrt_self para o mesmo wrapper de raiz. O adendo dos fornecedores mathlib será anexado antes do alvo.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_ORDEM_TODOS_POSITIVOS.md',s.encode('utf8'));print('FICHE',len(providers))
