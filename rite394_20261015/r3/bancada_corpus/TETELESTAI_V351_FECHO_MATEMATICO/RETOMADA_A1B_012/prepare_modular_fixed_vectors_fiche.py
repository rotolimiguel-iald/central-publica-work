from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
pat='scalarTomitaImaginaryPower_fixed_of_fixed_pair|regularAverage_square_modular_fixed|resolventPhaseOperator_fixed_at_half|cfc.{0,25}eigenvector'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),('tree',['rg','-n',pat,str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_modular_fixed_vectors'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351AverageFixedPair.lean','regularAverage_square_fixed_pair'),('TGLExt/V350ScalarTomitaSquare.lean','scalarTomitaSquare_domain_iff'),('TGLExt/V350ScalarTomitaSquare.lean','scalarTomitaSquare_apply'),('TGLExt/V350ScalarTomitaResolvent.lean','scalarTomitaResolvent_inverse'),('TGLExt/V351ScalarTomitaImaginaryPowers.lean','scalarTomitaImaginaryPower_damping'),('TGLExt/V351ResolventImaginaryIntertwining.lean','resolventPhaseOperator_intertwines'),('TGLExt/V351ResolventPhaseFunctions.lean','resolventPhaseFunction_continuous'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean','cfc_algebraMap')]

providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:theorem|lemma|def) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    end=s.index(' :=',m.start());providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=s[m.start():end],decision='REUSAR'))
cp=K/'TGLExt/V351ScalarImaginaryCoreAction.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('theorem scalarTomitaImaginaryPower_core_conjugation'))
target='ADAPTAR: for the SAME S,F,Delta_nu=FS,T_nu and U_t, prove a vector fixed by S and F in their actual domains is fixed by every U_t. Use the exact composition domain, the inverse identity to get T_nu*x=(1/2)*x, then the existing damped phase intertwiner with rankOne(x,x) and (1/2)I to read g_t(1/2)=1/4. Evaluate at x and cancel norm squared only when x is nonzero; handle zero separately. Damping is also (1/4)*x, so existing U*damping=phase fixes x. Then consume the preceding fixed pair of star(e_delta)*e_delta to exhibit those same modular-fixed vectors. Consumer is core covariance for equality of U with pi(lambda)R_-t on pi(N)Lambda(z_delta), followed by a separate totality argument. No new CFC, imaginary group, generator, GNS, weight, normalization, or claim that a single vector is cyclic. Delta30 standalone/review pending when fiche created; source frozen and target delivery depends on its acceptance. One generic private phase/eigenvector adapter is anticipated; no generic CFC framework.'

d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__FICHE_BEFORE_MODULAR_FIXED_VECTORS',consumer=dict(source=pin(cp),line=line,statement='\n'.join(ls[line-1:line+1])),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_VETORES_FIXOS_MODULARES.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior aos vetores fixos do grupo modular]\n\n'+d['timestamp']+'\n\n'+target+'\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Buscas: '+str(A/'searches.json')+'. Ausência nominal não é ausência universal. Consulta2 V2 e consulta curta do revisor de 15/09 relidas: usar o intertwiner de fase já especializado, sem construir o grupo de (1/2)I. rankOne_apply consultado na Mathlib Analysis/InnerProductSpace/LinearMap.lean:322; enumeração de fornecedores registra também o contexto desse import.\n'
put(R/'REAPROVEITAMENTO_A1B_VETORES_FIXOS_MODULARES.md',s.encode('utf8'));print('FICHE',len(providers))
