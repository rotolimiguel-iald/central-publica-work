from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
pat='average.{0,30}fixed.{0,30}(pair|tomita)|scalarWeightStar_fixed_pair|regularAverage_square_fixed_pair'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),('tree',['rg','-n',pat,str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_average_fixed_pair'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351AveragePolarRight.lean','regularAverage_mem_scalarPolarRightAlgebra'),('TGLExt/V350ScalarRightAdjointPair.lean','scalarRightAdjointPair_maximal'),('TGLExt/V350ScalarWeightTomitaIdentification.lean','scalarClosedTomita_extends_weight_star'),('TGLExt/V350ScalarWeightAction.lean','scalarWeightGNSAction_intertwines'),('TGLExt/V351AntiunitaryResolventPhase.lean','antiunitaryConjugate_selfadjoint'),('TGLExt/V350ScalarWeightDomain.lean','HasFiniteScalarSquare.left_mul'),('TGLExt/V350DualSemifiniteIdeal.lean','regularAverage_hasFiniteDualSquare')]

providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:theorem|lemma|def) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    end=s.index(' :=',m.start());providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=s[m.start():end],decision='REUSAR'))
cp=K/'TGLExt/V350ScalarTomitaSquare.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('theorem scalarTomitaSquare_domain_iff'))
target='ADAPTAR: within original scalarWeightStarCore/GNS/S/F, prove a selfadjoint A with A.val in scalarPolarRightAlgebra has Lambda(A) simultaneously fixed by S and F. Construct the actual ScalarRightAdjointPair (right and adjoint vectors both Lambda(A)) from polar-right identity and the old left-action identity; use maximality, not a supplied fixed-vector hypothesis. Then exhibit such an A whose ambient value is EXACTLY regularAverage(delta)* star-squared, specifically star(e_delta)*e_delta, delta>0. E-membership follows from accepted algebra operations and preceding delta29; finite domain from e_delta finite and left ideal, selfadjoint by star laws. No new operator/GNS/weight/J, no average-selfadjoint assertion, no normalization or trace. Consumer: scalarTomitaSquare_domain_iff and scalarTomitaResolvent_inverse for the next eigenvector/implementator step. These later consequences are not delivered merely by naming them. Delta29 standalone audit/review in progress at fiche, wait for acceptance before final consumer delivery.'

d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__FICHE_BEFORE_AVERAGE_FIXED_PAIR',consumer=dict(source=pin(cp),line=line,statement='\n'.join(ls[line-1:line+1])),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_MEDIA_PAR_FIXO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior ao par fixo de Tomita]\n\n'+d['timestamp']+'\n\n'+target+'\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Buscas: '+str(A/'searches.json')+'. Ausência nominal não é ausência universal. Consulta2 V2 lida; delta29 fornece a ação direita da média, usada no quadrado auto-adjunto.\n'
put(R/'REAPROVEITAMENTO_A1B_MEDIA_PAR_FIXO.md',s.encode('utf8'));print('FICHE',len(providers))
