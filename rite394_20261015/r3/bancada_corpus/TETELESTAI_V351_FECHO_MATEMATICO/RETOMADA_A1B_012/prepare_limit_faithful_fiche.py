from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='scalarInverse(CutoffWeight_one|LimitWeight)_faithful|inverse.{0,20}limit.{0,20}faithful|peso.{0,20}limite.{0,20}fiel'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_limit_weight_faithful'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V350ResolventSquareRoot.lean','positive_sqrt_injective'),('TGLExt/V350ResolventSquareRoot.lean','resolventSquareRoot_dense'),('TGLExt/V350ScalarDualWeightFaithfulness.lean','dualQuadraticIntegral_vacuum_faithful'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_injective'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_nonneg'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_one'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseCutoffWeight_le_limit'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseLimitWeight_zero')]

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
target='Prove scalarInverseCutoffWeight P 1 faithful on PositiveCoreInput P using B_1=R, membership of the existing sqrt(R) in N and faithfulness of the SAME vacuum dual weight. The ORIGINAL positive_sqrt_injective and resolventSquareRoot_dense imply injectivity and dense range of the bounded CFC root; adapt the wrapper only. If star sqrt(R) X sqrt(R)=0, injectivity cancels the left root and continuity/dense range cancels the right root, giving X=0. Then scalarInverseLimitWeight dominates n=0 (epsilon_0=1), so it is faithful. No new GNS/root/resolvent and no need to prove every regulator inverse injective. Consumer: faithful field of RegularCoreTraceData for the candidate value. Neither semifinitude, traciality nor dual scaling follows from this.'

stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_LIMIT_WEIGHT_FAITHFUL',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_FIDELIDADE_PESO_LIMITE.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à fidelidade do peso limite]\n\n# A1(b): um corte já basta para a fidelidade do limite\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR: o domínio do fornecedor resolventSquareRoot_dense é a imagem da raiz LIMITADA CFC.sqrt R. Não confundir essa raiz com o operador parcial resolventSquareRoot. A dupla injetividade/densidade é reutilizada; não é pressuposta a fidelidade do limite.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_FIDELIDADE_PESO_LIMITE.md',s.encode('utf8'));print('FICHE',len(providers))
