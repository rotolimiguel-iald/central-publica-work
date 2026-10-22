from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='scalarWeightGNSEmbedding.*(closed|strong|tendsto)|scalarWeight.*(closedGraph|closed_graph)|bounded.*strong.*GNS|GNS.*closedness'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_gns_closedness'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V350ScalarHomogeneousRightOrbit.lean','hasFiniteScalarSquare_iff_memLp'),('TGLExt/V350ScalarWeightCompletion.lean','scalarWeightGNSEmbedding'),('TGLExt/V350ScalarWeightOrbit.lean','scalarWeightOrbit_ae'),('TGLExt/V350ScalarGNSCutMaps.lean','scalarGNSCutMap'),('TGLExt/V350ScalarCutVacuum.lean','scalarCutVacuum_ae'),('TGLExt/V350ScalarCutVacuum.lean','scalarGNSCutMap_embedding_eq_action'),('TGLExt/V350DualOrbitStrongLimits.lean','dualOrbit_tendsto_of_uniformly_bounded'),('TGLExt/V350ScalarRegularRightGNS.lean','regularRightGNS_intertwines'),('TGLExt/V350ScalarRegularRightPolar.lean','scalarTomitaPolar_conjugate_regular_right')]


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
target='Closedness of the EXISTING full weight GNS embedding: for any nontrivial filter l, A_i in n_nu uniformly bounded in operator norm, A_i converging strongly to A in the same core, and Lambda_nu(A_i) converging in GNS norm to v, prove A in n_nu and Lambda_nu(A)=v. Both convergences are hypotheses; strong convergence alone does not imply GNS convergence. Reuse existing finite cut maps and the dualOrbit factorization for arbitrary nets, and hasFiniteScalarSquare_iff_memLp. Consumer: extension of the already constructed right action of regular unitaries to bounded centralizer elements sqrt(B_epsilon) in pedersen_takesaki_inverse_generator_trace, LACUNAS_A1 item4. No new Hilbert space, state, trace or abstract predual.' 


stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_FULL_WEIGHT_GNS_CLOSEDNESS',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_FECHAMENTO_GNS.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior ao fechamento do mapa GNS do peso]\n\n# A1(b): fechamento da inscrição GNS do peso sob duas convergências\n\n'+stamp+'\n\n'+target+'\n\nO ideal, os cortes e a representação são os existentes. O lema só fecha o grafo da inscrição; não produz convergência GNS a partir da convergência forte. A entrada consumidora é a ação direita dos cortes inversos na fórmula de τ do item4 de LACUNAS_A1.md. As propriedades do traço seguem pendentes.\n\n'

for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_FECHAMENTO_GNS.md',s.encode('utf8'));print('FICHE',len(providers))
