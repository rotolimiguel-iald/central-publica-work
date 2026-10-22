from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
pat='scalarTomitaImaginaryPower_eq_regular_implementation|modular.{0,25}implementator|modular.{0,25}implementation|right.{0,20}average.{0,20}total'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),('tree',['rg','-n',pat,str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_modular_implementation'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351ModularFixedVectors.lean','regularAverage_square_modular_fixed'),('TGLExt/V351ScalarImaginaryCoreAction.lean','scalarTomitaImaginaryPower_core_conjugation'),('TGLExt/V350ScalarRegularPolarCommutation.lean','regularRightGNS_commutes_left'),('TGLExt/V350ScalarRegularPolarCommutation.lean','scalarTomitaPolar_regular_generator'),('TGLExt/V350ScalarRegularRightGNS.lean','regularRightGNS_intertwines'),('TGLExt/V350StrongOperatorIntegral.lean','operatorIntegral_commutes'),('TGLExt/V350ContractionAdjointLimit.lean','regularAverage_star_tendsto_identity'),('TGLExt/V350ScalarWeightAction.lean','scalarWeightGNSEmbedding_denseRange'),('TGLExt/V350ScalarWeightAction.lean','scalarWeightGNSAction_intertwines'),('TGLExt/V350ScalarGNSStrongContinuity.lean','scalarGNSRepresentation_tendsto_of_uniformly_bounded'),('TGLExt/V351ScalarRightActionAlgebra.lean','ScalarPolarRight'),('TGLExt/V350StrongBoundedApplication.lean','bounded_application_tendsto')]

providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:theorem|lemma|def) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    end=s.index(' :=',m.start());providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=s[m.start():end],decision='REUSAR'))
cp=K/'TGLExt/V351RegularCoreTraceContract.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('  tracial :'))
target='ADAPTAR: prove on ALL vectors of the SAME scalar GNS that U_t equals pi(lambda_t) R_{-t}. Use actual fixed vectors Lambda(z_delta), z_delta=e_delta* e_delta (star(e_delta)*e_delta), from delta31, plus existing all-core covariance. Prove the same W_t fixes Lambda(z_delta) by the actual left/right product identities and z_delta commutation with regular unitaries. That commutation reuses StrongIntegral.operatorIntegral_commutes, not the inaccessible private proof of delta29. Transfer the existing contraction strong/strong-star approximation z_delta to pi(z_delta), then conjugate by original J to obtain rho(z_delta) -> I strongly. Right identity gives rho(z_delta)Lambda(a)=pi(a)Lambda(z_delta), so limits plus dense original Lambda(n_nu) prove totality and equality. No premise of single-vector cyclicity, no inference of implementator identity from covariance alone. No new operator definition or general integration/CFC framework. One public theorem, local or private adapters only where type transport requires. Delta31 standalone underway when fiche created; final delivery depends on independent acceptance. Consumer tracial field remains INDIRECT: later half-power/Q domain compatibility still required, not furnished merely by this implementation identity. Same h, Delta_nu, nu, tau, GNS; never identify h=Delta_nu.'

d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__FICHE_BEFORE_MODULAR_IMPLEMENTATION',consumer=dict(source=pin(cp),line=line,statement='\n'.join(ls[line-1:line+1])),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_IMPLEMENTADOR_MODULAR.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à igualdade dos implementadores modulares]\n\n'+d['timestamp']+'\n\n'+target+'\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Buscas: '+str(A/'searches.json')+'. Ausência nominal não é ausência universal. Consulta2 V2 relida; consumidores futuros Q/meias potências/tracialidade continuam abertos. A fonte StrongIntegral.operatorIntegral_commutes foi lida integralmente antes de propor a adaptação; usar esse fornecedor evita reproduzir integração vetorial.\n'
put(R/'REAPROVEITAMENTO_A1B_IMPLEMENTADOR_MODULAR.md',s.encode('utf8'));print('FICHE',len(providers))
