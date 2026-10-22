from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
R=Path(__file__).resolve().parent; K=R/'k'; CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='regularPositiveGenerator_graph_iff|sigmoid_resolvent_graph_iff|regularSpectralResolvent_coordinate'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_spectral_graph'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V350ResolventGraph.lean','resolvent_graph_equation'),
 ('TGLExt/V350L2PositiveMultiplier.lean','realScalarMultiplier_ae'),
 ('TGLExt/V351RegularPositiveGraph.lean','regularPositiveGenerator'),
 ('TGLExt/V351RegularPositiveGraph.lean','regularSpectralCoordinates'),
 ('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent'),
 ('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Sigmoid.lean','sigmoid_mul_rexp_neg'),
 ('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Sigmoid.lean','sigmoid_neg'),
 ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean','conjStarAlgEquiv_apply_apply')]
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:@\[[^\n]*\] )?(?:noncomputable )?(?:def|theorem|lemma) '+name+r'(?:\s|\()',s,re.M);assert m,name
    start=m.start();depth=0;end=None
    for i in range(start,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and (s.startswith(' :=',i) or s.startswith(' where',i)):end=i;break
    assert end is not None
    providers.append(dict(name=name,source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end],decision='REUSAR'))
stamp=datetime.datetime.now().astimezone().isoformat()
target='For every SiteProfile P and x,y in the existing regular Hilbert space: (x,y) in graph(regularPositiveGenerator P) iff almost everywhere xi, (V.symm y)(xi) = exp(-2*pi*xi) smul (V.symm x)(xi), with V=regularSpectralCoordinates P. No new Hilbert space, graph, multiplier, Fourier transform or generator. Exact identification needed by regular_unitary_positive_generator / future imaginary powers.'
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_SPECTRAL_GRAPH_IDENTIFICATION',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=31,name='regular_unitary_positive_generator'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR',not_claimed=['imaginary powers equal regularUnitary','affiliation','trace'])
put(R/'REAPROVEITAMENTO_A1B_GRAFO_ESPECTRAL.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à identificação espectral do grafo]\n\n# A1(b): o mesmo grafo nas coordenadas espectrais\n\n'+stamp+'\n\n'+target+'\n\nA busca nominal negativa não é ausência universal. A equação resolvente já foi paga: consumi-la. Novo módulo consumidor, sem editar o módulo de quinze declarações que está em revisão. Não promover prova DEV à aceitação.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Buscas nas seis modalidades e outras bancadas: '+str(A/'searches.json')+'.\n'
put(R/'REAPROVEITAMENTO_A1B_GRAFO_ESPECTRAL.md',s.encode('utf8'));print('FICHE',len(providers))
