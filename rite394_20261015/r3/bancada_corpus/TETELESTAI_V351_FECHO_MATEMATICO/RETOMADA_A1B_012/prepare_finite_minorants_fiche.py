from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
pat='scalarInverseLimitWeight_finite_contractions|scalarInverseLimitWeight_finite_minorants|finite.{0,12}minorants.{0,12}tracial'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),('tree',['rg','-n',pat,str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_finite_minorants'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351InverseLimitSemifiniteness.lean','scalarInverseLimitWeight_domainCut_finite'),('TGLExt/V351RegularDomainCut.lean','regularDomainCut_bounds'),('TGLExt/V351RegularDomainCut.lean','regularDomainCut_tendsto_identity'),('TGLExt/V350StrongBoundedApplication.lean','bounded_application_tendsto'),('TGLExt/V350ScalarDualWeight.lean','HasFiniteDualSquare.scalar_finite'),('TGLExt/V351InverseLimitTracialExtension.lean','scalarInverseLimitWeight_square_le_of_strong'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseLimitWeight_scale'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseLimitWeight_mono'),('TGLExt/V350LevelExpectationUniformBound.lean','vonNeumann_norm_closed'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Range.lean','cfcₙ_mem'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Order.lean','CStarAlgebra.mul_star_le_algebraMap_norm_sq')]
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:theorem|lemma|def) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    end=s.index(' :=',m.start());providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=s[m.start():end],decision='REUSAR'))
cp=K/'TGLExt/V351RegularCoreTraceContract.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('  semifinite :'))
target='Same scalarInverseLimitWeight. First construct a sequence of contractions E_n=regularAverage(delta_n)*regularDomainCut(delta_n) with finite square weight and strong limit I using existing bounds/density. Then, EXPLICITLY conditional on traciality, prove the exact finite-positive-minorants field: tau(X)=sup{tau(Y):0<=Y<=X,tau(Y)<infinity}. For X=a*a with its existing CFC square root, use Y_n=(E_n a)*(E_n a) <= X. Finiteness follows by traciality, a a*<=norm(a)^2 I and positive homogeneity. Existing strong-square bound gives tau(X)<=sup tau(Y_n). No assumption that tau is tracial has been discharged here; no extra trace/GNS/root, no independent normalization, no completion of A1(b). Delta27 is author-validated, independent review pending at fiche creation; final acceptance of this consumer waits for27.'
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__FICHE_BEFORE_FINITE_MINORANTS',consumer=dict(source=pin(cp),line=line,statement='\n'.join(ls[line-1:line+1])),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_MINORANTES_FINITOS.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior aos minorantes finitos, condicional à tracialidade]\n\n'+d['timestamp']+'\n\n'+target+'\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Buscas: '+str(A/'searches.json')+'. Ausência nominal não é ausência universal. O helper de raiz privado de V351AllPositiveWeightOrder não é refeito como novo teorema: seu consumidor usa diretamente cfcₙ_mem e sqrt_mul_sqrt_self.\n'
put(R/'REAPROVEITAMENTO_A1B_MINORANTES_FINITOS.md',s.encode('utf8'));print('FICHE',len(providers))
