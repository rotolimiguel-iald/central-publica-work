from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='scalarInverseCutoffWeight|scalarInverseLimitWeight|peso.{0,20}limite.{0,20}(normal|aditiv)|cutoff.{0,20}weight.{0,20}normal'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_limit_weight'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351RegulatorWeightOrder.lean','scalarWeight_inverseCutoff_antitone'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegral_zero'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegral_add'),('TGLExt/V350DualQuadraticLaws.lean','dualQuadraticIntegral_smul_operator'),('TGLExt/V350DualFormFaithfulness.lean','dualQuadraticIntegral_mono'),('TGLExt/V350DualFormNormality.lean','dualQuadraticIntegral_of_monotone_strong_limit'),('TGLExt/V350RegularNormality.lean','vonNeumann_exists_positive_isLUB'),('TGLExt/V350DualFixedWeightLaws.lean','PositiveCoreInput.conjugate'),('TGLExt/V350DualFixedWeightLaws.lean','positive_internal_isLUB_nonneg')]

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
target='Define scalarInverseCutoffWeight P epsilon on the EXISTING PositiveCoreInput as nu(star sqrt(B_epsilon) X sqrt(B_epsilon)). Prove zero, addition, NNReal homogeneity, input monotonicity and normality for internal positive directed suprema, using the old strong operator limit and old normality of dualQuadraticIntegral. Read scalarWeight_inverseCutoff_antitone as regulator order, and prove the natural-number sequence epsilon_n=1/(n+1) gives monotone weights. Define scalarInverseLimitWeight as that SAME sequence supremum; prove zero/add/homogeneous/monotone/normal and domination of each sequence cutoff. All values ENNReal, no finiteness premise. No separate GNS, trace structure inhabitant, final semifinitude, faithfulness, traciality or dual scaling claimed by these laws. Explicit two definitions are consumers of already constructed cutoffs and of the final RegularCoreTraceData value field. Existing PositiveCoreInput.conjugate is NOT usable directly: requires dualFixedCore; use raw integral laws without asserting that cuts are theta-fixed.'

stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_LIMIT_WEIGHT_LAWS',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_LEIS_PESO_LIMITE.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior às leis do peso limite]\n\n# A1(b): o peso limite pelos cortes já construídos\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR: leis integrais e supremos existentes; não criar outro espaço de estados. A normalidade do sanduíche segue por limite forte de redes positivas, não por presumir que uma conjugação não invertível preserva qualquer supremo. Fornecedores ENNReal serão registrados em adendo antes do alvo.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_LEIS_PESO_LIMITE.md',s.encode('utf8'));print('FICHE',len(providers))
