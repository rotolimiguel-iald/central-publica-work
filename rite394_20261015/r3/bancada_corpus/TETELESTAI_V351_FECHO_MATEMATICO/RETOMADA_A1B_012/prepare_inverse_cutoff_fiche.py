from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='regularInverseGeneratorCutoff|inverse_generator_cutoff|pedersen_takesaki_inverse_generator_trace'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_inverse_cutoff'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_nonneg'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_le_one'),('TGLExt/V351RegularGeneratorAffiliation.lean','regularSpectralResolvent_mem'),('TGLExt/V351RegularGeneratorDualScaling.lean','regularPositiveGenerator_dual_graph'),('TGLExt/V350RegularDualAction.lean','dualAmbient_add'),('TGLExt/V350RegularDualAction.lean','regularDualAction'),('TGLExt/V350ResolventGraph.lean','resolvent_graph_resolvent_equation'),('TGLExt/V350L2CharacterMultiplier.lean','characterMultiplier_inverse')]


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
target='Construct the actual bounded inverse-generator cutoffs B_epsilon=(h+epsilon)^(-1) for epsilon>0 as epsilon^(-1) theta_(log epsilon)(R), with the SAME R=(1+h)^(-1). Prove core membership, positivity, bound by epsilon^(-1), graph equation h(B_epsilon x)=x-epsilon B_epsilon x, and dual transport theta_s B_epsilon=exp(s) B_(epsilon exp(s)). Consumer: the existing inverse-generator trace formula in LACUNAS_A1 item4. Reuse dual action and graph scaling; no new CFC, generator, base L2 or substitute trace. No assertion of additivity or traciality of a supremum before its monotonicity is established.'


stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_INVERSE_GENERATOR_CUTOFF',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_CORTES_INVERSO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior aos cortes do inverso do mesmo gerador]\n\n# A1(b): cortes limitados para a perturbação do peso\n\n'+stamp+'\n\n'+target+'\n\nR é o resolvente já pago; a escala dual fornece os demais parâmetros sem uma segunda construção espectral. ε é regulador positivo do limite, não parâmetro físico. A entrada consumidora é a fórmula de τ no item4 de LACUNAS_A1.md. As propriedades do traço seguem pendentes.\n\n'

for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_CORTES_INVERSO.md',s.encode('utf8'));print('FICHE',len(providers))
