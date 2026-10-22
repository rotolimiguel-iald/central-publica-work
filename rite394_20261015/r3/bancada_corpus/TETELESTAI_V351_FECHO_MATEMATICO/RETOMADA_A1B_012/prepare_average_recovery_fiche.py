from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='scalarWeight_square_eq_iSup_averages|scalarWeight.{0,60}(recover|Fatou|exhaustion)|(Fatou|fatou).{0,120}(peso|weight|regular)'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_weight_average_recovery'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V350ScalarRightAverage.lean','scalarWeight_right_average_le'),('TGLExt/V350ScalarRightAverage.lean','scalarOrbit_right_average_tendsto'),('TGLExt/V350DualSemifiniteIdeal.lean','regularAverage_hasFiniteDualSquare'),('TGLExt/V350DualSemifiniteIdeal.lean','HasFiniteDualSquare.left_mul'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegral'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegrand_measurable'),('TGLExt/V350RegularFiniteWeight.lean','dualQuadraticIntegrand_star_mul'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Add.lean','lintegral_liminf_le'),('.lake/packages/mathlib/Mathlib/Analysis/SpecificLimits/Basic.lean','tendsto_one_div_add_atTop_nhds_zero_nat')]

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
target='For EVERY A in regularCoreAlgebra P, prove nu(A*A)=iSup_n nu((A e_n)*(A e_n)), e_n=regularAverage P (1/(n+1)). No finite-weight hypothesis on A; values may be infinity. Consume pointwise orbit convergence and the existing upper bound under right averages, via Fatou for a SEQUENCE atTop. No monotonicity of e_n or of its squares asserted. A e_n is already uniformly square-finite by existing ideal lemmas. Consumer: extend the cut-weight order from square-finite inputs to all positive inputs, after proving commutation of cuts with the SAME averages. This does not claim finite positive minorants or normal-weight semifiniteness in that stronger sense.'

stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_WEIGHT_AVERAGE_RECOVERY',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_RECUPERACAO_PELAS_MEDIAS.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à recuperação de valores estendidos por médias]\n\n# A1(b): recuperar todos os valores sem supor minorantes finitos\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR: limite pontual e cota já pagos, compostos com Fatou. Reutilizar a família regularAverage, sem novo regularizador ou novo peso. Consulta independente TODOS_POSITIVOS é roteiro, não prova.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_RECUPERACAO_PELAS_MEDIAS.md',s.encode('utf8'));print('FICHE',len(providers))
