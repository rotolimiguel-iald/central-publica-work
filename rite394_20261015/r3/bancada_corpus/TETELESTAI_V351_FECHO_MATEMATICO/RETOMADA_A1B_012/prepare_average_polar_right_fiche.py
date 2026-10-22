from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
pat='scalarPolarRight.{0,40}average|regularAverage.{0,40}(partition|sum|polar)|average_mem_polar_right'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),('tree',['rg','-n',pat,str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_average_polar_right'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351ScalarRightActionAlgebra.lean','scalarPolarRightAlgebra_regular_mem'),('TGLExt/V351ScalarRightActionLimits.lean','scalarRightAction_closed_of_bounded_strongStar'),('TGLExt/V350RegularApproximation.lean','regularAverage_apply'),('TGLExt/V350RegularApproximation.lean','regularAverage_tendsto_identity'),('TGLExt/V350ContractionAdjointLimit.lean','regularAverage_star_tendsto_identity'),('TGLExt/V350StrongOperatorIntegral.lean','operatorIntegral_commutes'),('TGLExt/V350RegularTowerRepresentation.lean','regular_mul'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean','sum_integral_adjacent_intervals'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean','integral_comp_add_right')]

providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:theorem|lemma|def) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    end=s.index(' :=',m.start());providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=s[m.start():end],decision='REUSAR'))
cp=K/'TGLExt/V350ScalarRightAdjointPair.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('structure ScalarRightAdjointPair'))
target='ADAPTAR: prove the EXISTING regularAverage delta (delta>0) belongs to the EXISTING scalarPolarRightAlgebra, supplying the right action for z=e*e needed by ScalarRightAdjointPair with the same weight/GNS/S/F. Construct bounded finite sums of the existing regular unitaries b_n=(n+1)^(-1) sum_{k<n+1} lambda_(delta*k/(n+1)). Exact interval partition gives e_delta=b_n e_(delta/(n+1)), so contraction bounds and existing small-average convergence give strong convergence; commuting factors and the existing adjoint convergence give strong-star. Apply already proved bounded strong-star closure twice. This avoids a new generic Riemann-integral framework, operator-norm continuity, Bochner integration in B(H), alternate average, GNS or trace. The fixed S/F vector, modular implementator identity, Q and traciality remain later obligations. No claim average is selfadjoint; use e*e for later fixed vector.'

d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__FICHE_BEFORE_AVERAGE_POLAR_RIGHT',consumer=dict(source=pin(cp),line=line,statement='\n'.join(ls[line-1:line+1])),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_MEDIA_ACAO_DIREITA.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à pertença da média à álgebra direita]\n\n'+d['timestamp']+'\n\n'+target+'\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Buscas: '+str(A/'searches.json')+'. Ausência nominal não é ausência universal. Consulta2 corrigida V2 já lida; rota reduzida à partição exata da integral e limites existentes.\n'
put(R/'REAPROVEITAMENTO_A1B_MEDIA_ACAO_DIREITA.md',s.encode('utf8'));print('FICHE',len(providers))
