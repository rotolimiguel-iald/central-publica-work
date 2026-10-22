from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='character_commutation_realScalarMultiplier|regularSpectralResolvent_mem|regularPositiveGenerator_commutant_graph'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_regular_affiliation'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V350CharacterLocality.lean','character_commutation_local_pairing'),('TGLExt/V350L2PositiveMultiplier.lean','realScalarMultiplier_ae'),('TGLExt/V351RegularImaginaryPowers.lean','regularSpectralCoordinates_character'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent'),('TGLExt/V350ResolventGraph.lean','resolvent_graph_equation'),('TGLExt/V350RegularGeneratedAlgebra.lean','regularUnitary_mem'),('.lake/packages/mathlib/Mathlib/Analysis/VonNeumannAlgebra/Basic.lean','mem_commutant_iff'),('.lake/packages/mathlib/Mathlib/Analysis/VonNeumannAlgebra/Basic.lean','commutant_commutant')]

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
target='Prove on the existing regular space: regularSpectralResolvent P belongs to regularCoreAlgebra P; every B in its commutant preserves the graph of the already constructed positive generator. Reuse local pairings from character commutation, conjugation by V=W F^-1 and the double commutant. No simple-function approximation machinery, new affiliated-form object or replacement generator. This is the commutant criterion of affiliation of the closed operator; dual scaling and trace remain separate.'

stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_REGULAR_AFFILIATION',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=31,name='regular_unitary_positive_generator'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_AFILIACAO_REGULAR.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à afiliação do mesmo gerador regular]\n\n# A1(b): o resolvente pertence ao core\n\n'+stamp+'\n\n'+target+'\n\nA prova usa character_commutation_local_pairing antes de tentar reconstruir funções simples. O critério de afiliação é a preservação do grafo por todo operador do comutante. O grafo anterior é mantido intacto; não se confunde com as formas afiliadas de outro contrato.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_AFILIACAO_REGULAR.md',s.encode('utf8'));print('FICHE',len(providers))
