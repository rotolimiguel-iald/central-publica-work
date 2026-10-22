from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='scalarInverseLimitWeight.*(strong|sandwich|tracial)|tracial.{0,40}finiteDualStarCore|dualQuadraticIntegral.*strong.*bound'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_tracial_extension'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351InverseLimitWeight.lean','scalarInverseCutoffWeight_le_limit'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseLimitWeight_mono'),('TGLExt/V350DualCutNormality.lean','dualAmbient_tendsto_strong'),('TGLExt/V350ScalarRightAverage.lean','scalarWeight_right_average_le'),('TGLExt/V351CutoffAverageCommutation.lean','regularInverseCutoffSqrt_commutes_average'),('TGLExt/V350FiniteDualStarCore.lean','regularSandwich_star'),('TGLExt/V350FiniteDualStarCore.lean','regularSandwich_mem_finiteDualStarCore'),('TGLExt/V350FiniteDualStarCore.lean','regularSandwich_tendsto'),('TGLExt/V351WeightAverageRecovery.lean','scalarWeight_square_eq_iSup_averages')]

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
target='ADAPTAR: for the SAME scalarInverseLimitWeight, prove bounded square values survive strong limits, tau(positiveSquare(regularSandwich a delta)) <= tau(positiveSquare a), then traciality on the EXISTING finiteDualStarCore iff traciality on all regularCoreAlgebra. Consumer: RegularCoreTraceData.tracial, V351RegularCoreTraceContract.lean:59 (recheck line). No traciality assumed globally, no new weight/core/GNS, no replacement trace contract. The core equality remains an explicit missing lemma; this extension alone does not inhabit the trace contract. Strong convergence of adjoints is taken from existing sandwich theorem, never presumed for arbitrary strong limits.'

stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_TRACIAL_EXTENSION',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_EXTENSAO_TRACIAL.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à extensão tracial]\n\n# A1(b): o núcleo existente basta para a igualdade tracial\n\n'+stamp+'\n\n'+target+'\n\nA prova usa Fatou em cada corte e a comutação já paga com as médias. Não compara sanduíches por ordem do conjugador. As buscas nominais abaixo são complementadas pela leitura dos enunciados e fontes destes fornecedores. Nenhuma ausência universal é alegada.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_EXTENSAO_TRACIAL.md',s.encode('utf8'));print('FICHE',len(providers))
