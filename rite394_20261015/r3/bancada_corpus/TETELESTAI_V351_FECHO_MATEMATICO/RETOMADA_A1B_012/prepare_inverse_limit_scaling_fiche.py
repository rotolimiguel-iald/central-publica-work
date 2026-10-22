from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='scalarInverse(CutoffWeight_dual|LimitWeight_(scaled_sequence|dual))|regularInverseCutoffSqrt_dual|peso.{0,20}limite.{0,20}escala'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_inverse_limit_scaling'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_dual'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_nonneg'),('TGLExt/V350DualWeightCuts.lean','dualAmbient_nonneg'),('TGLExt/V350RegularDualAction.lean','dualAmbient_symm'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegral_dual_invariant'),('TGLExt/V350DualQuadraticLaws.lean','dualQuadraticIntegral_smul_operator'),('TGLExt/V351RegularCoreTraceContract.lean','positiveDual'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseCutoffWeight_antitone'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseLimitWeight'),('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean','mul_self_eq_mul_self_iff'),('.lake/packages/mathlib/Mathlib/Algebra/Order/Archimedean/Basic.lean','exists_nat_one_div_lt'),('.lake/packages/mathlib/Mathlib/Data/ENNReal/Inv.lean','mul_iSup')]

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
target='Prove dual scaling of the SAME scalarInverseLimitWeight on existing TGLV351.positiveDual: tau(theta_s X)=ofReal(exp(-s))*tau(X). Adapt positive-square uniqueness for the existing hilbertPositiveSqrt, actual inverse-cutoff dual identity, original dual weight invariance and real homogeneity; no new root/GNS/cone. Then prove cofinality of r/(n+1) for r>0 using two supremum inequalities and existing regulator antitonicity, including infinite values. Four consumer-linked targets: root transport, cutoff weight transport, scaled sequence cofinality, limit dual scaling. Consumer is the exact dual_scaling field of RegularCoreTraceData, not a substitute trace contract. Semifinitude and traciality remain open.'

stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_INVERSE_LIMIT_SCALING',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_ESCALA_PESO_LIMITE.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à escala dual do peso limite]\n\n# A1(b): ação dual no mesmo candidato\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR. A escala do peso tem sinal MENOS, obtida transportando o sanduíche por theta_(-s). A sequência de reguladores muda e sua cofinalidade precisa ser paga. Não confundir invariância do peso dual com tracialidade.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_ESCALA_PESO_LIMITE.md',s.encode('utf8'));print('FICHE',len(providers))
