from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
pat='scalarInverseLimitWeight_core_tracial|inverse.{0,12}(cut|Cut).{0,25}(quadratic|Quadratic)|quadratic.{0,20}(trace|tracial|cut)|compatibilidade.{0,20}quadr.tica'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),('tree',['rg','-n',pat,str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_quadratic_trace'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
with ThreadPoolExecutor(max_workers=7) as pool:
    jobs=[pool.submit(subprocess.run,cmd,capture_output=True) for _,cmd in queries]
    for (label,cmd),job in zip(queries,jobs):
        p=job.result();out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
        rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(x['returncode'] in (0,1) and x['stderr']['bytes']==0 for x in rows)
specs='''V351ModularCutBalance|scalarTomitaResolvent_double_cut_balance
V350PositiveRootIntertwining|positive_sqrt_intertwines
V350ResolventSquareRoot|resolventSquareRoot_domain
BoundedGraphOperator|bounded_graph_parameter_apply
BoundedGraphOperator|bounded_graph_apply
V350ScalarTomitaPositiveRoot|scalarTomitaPositiveRoot
V350ScalarTomitaPolarFactor|scalarTomitaPolarFactor_factorization
V351RegularDomainCut|regularDomainCut_bounds
V351RegularDomainCut|regularDomainCut_tendsto_identity
V350ScalarGNSStrongContinuity|scalarGNSRepresentation_tendsto_of_uniformly_bounded
V351PerturbedWeightNorm|scalarWeight_inverseCutoff_perturbed_norm
V351InverseLimitWeight|scalarInverseLimitWeight
V351InverseLimitTracialExtension|scalarInverseLimitWeight_tracial_iff_core
V351InverseLimitFiniteMinorants|scalarInverseLimitWeight_finite_minorants'''
def statement_end(s,start,name):
    if name=='scalarTomitaResolvent_double_cut_balance':return s.index(' := by',start)
    depth=0
    for i in range(start,len(s)):
        if depth==0 and (s.startswith(' :=',i) or s.startswith(' where',i)):return i
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
    raise ValueError(name)
providers=[]
for row in specs.splitlines():
    mod,name=row.split('|');p=K/'TGLExt'/(mod+'.lean');s=p.read_text(encoding='utf8')
    m=re.search(r'^(?:theorem|lemma|def) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=s[m.start():statement_end(s,m.start(),name)],decision='REUSAR'))
target='''[OPEN] Construir, nos objetos originais, para A:N e ha:A in finiteDualStarCore P, scalarInverseLimitWeight P (positiveSquare P A)=scalarInverseLimitWeight P (positiveSquare P (star A)). O balanço33 e as duas comutações passaram compilação própria e controle negativo; revisão independente33 ainda pendente nesta ficha. Não assumir Q nem tracialidade como campo, e não reabrir as entregas1–32. Reaproveitar o grafo original da raiz: x=sqrt(T)u, B_nu x=sqrt(1-T)u. A partir do balanço, obter igualdade de formas limitadas Re<y,C_epsilon q_eta y>=Re<x,p_epsilon D_eta x>. Retirar um corte de cada vez na sequência 1/(n+1), usando positividade e contração de p/q, e comparar supremos em ENNReal, inclusive infinito. Identificar normas quadradas das raízes representadas com as formas por map_star/map_mul/sqrt_mul_sqrt_self e a identidade de peso perturbado existente. Não criar limite forte de sqrt(p_n), outro GNS, outra medida, h=Delta_nu ou produto ilimitado sem domínio. A extensão do núcleo para todo N e os minorantes finitos já existem27–28; depois deste consumidor devem ser aplicados, não reprovados. Ausência nas buscas limitadas não demonstra ausência universal.'''
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__FICHE_BEFORE_QUADRATIC_TRACE_CONSUMER',exact_target=target,providers=providers,searches=pin(A/'searches.json'),balance_author_audit=pin(R/'AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO.json'),prior_consumer=pin(R/'ADENDO_CONSUMIDOR_Q_DO_BALANCO.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_COMPATIBILIDADE_QUADRATICA.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
body=target+'\n\n'+d['timestamp']+'\n\n'
for x in providers:body+=x['source']['path']+':'+str(x['line'])+'\n```lean\n'+x['statement']+'\n```\n\n'
body+='Buscas: '+str(A/'searches.json')+'\n'
put(R/'REAPROVEITAMENTO_A1B_COMPATIBILIDADE_QUADRATICA.md',body.encode('utf8'));print('FICHE',len(providers),A)
