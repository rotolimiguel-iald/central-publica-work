from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
pat='regularPositiveGenerator|regularSpectralResolvent|realScalarMultiplier_nonneg|realScalarMultiplier_complement'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat+'|regular_unitary_positive_generator',str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|gerador|traço',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_positive_generator'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V350L2PositiveMultiplier.lean','realScalarMultiplier'),('TGLExt/V350L2PositiveMultiplier.lean','realScalarMultiplier_injective'),('TGLExt/V350L2PositiveMultiplier.lean','realScalarMultiplier_ae'),('TGLExt/V350OperatorFieldAlgebra.lean','operatorFieldLift_star'),('TGLExt/V350OperatorFieldAlgebra.lean','operatorFieldLift_mul'),('TGLExt/V350ResolventGraph.lean','resolventGraphOperator'),('TGLExt/V350ResolventGraph.lean','resolvent_graph_closed'),('TGLExt/V350ResolventGraph.lean','resolvent_graph_domain_dense'),('TGLExt/V350ResolventGraph.lean','resolvent_graph_selfadjoint'),('TGLExt/V350ResolventGraph.lean','resolvent_graph_positive'),('TGLExt/V351RegularFlowAbsorption.lean','regularFlowAbsorptionUnitary'),('.lake/packages/mathlib/Mathlib/Analysis/Fourier/LpSpace.lean','fourierTransformₗᵢ'),('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Sigmoid.lean','sigmoid'),('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean','conjStarAlgEquiv')]
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:noncomputable )?(?:def|theorem|lemma) '+name+r'(?:\s|\()',s,re.M);assert m,name
    start=m.start();depth=0;end=None
    for i in range(start,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and (s.startswith(' :=',i) or s.startswith(' where',i)):end=i;break
    assert end is not None
    providers.append(dict(name=name,source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end],decision='REUSAR'))
stamp=datetime.datetime.now().astimezone().isoformat()
target='For each SiteProfile P: V=W F^{-1}; R=V M[sigmoid(2*pi*xi)] V^{-1}. Construct R on the actual regular Hilbert space, prove 0<=R<=1 and injectivity of both R and 1-R. Define h=resolventGraphOperator R hi, prove its graph closed, domain dense, self-adjointness, positivity and zero kernel. Affiliation, imaginary powers, dual scaling and trace remain subsequent consumers, not hypotheses assumed true here.'
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_POSITIVE_REGULAR_GRAPH',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=31,name='regular_unitary_positive_generator'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR',not_claimed=['affiliation','h^it equals regularUnitary','dual scaling of h','inverse-generator trace','gate change'])
put(R/'REAPROVEITAMENTO_A1B_GERADOR_POSITIVO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à construção do grafo positivo regular]\n\n# A1(b): o candidato concreto ao gerador positivo\n\n'+stamp+'\n\nConsumidor: LACUNAS_A1.md:31, regular_unitary_positive_generator.\n\n'+target+'\n\nReal.sigmoid já existe: nenhum novo logistic/sigmoid. O resolventGraphOperator já constrói domínio e grafo; não reconstruí-los. O campo/multiplicador L² já existe; acrescentar apenas positividade/complemento que seus consumidores precisam. A transformação unitária é a Fourier existente com W já construído. Não se declara h afiliado nem identificado pelas potências antes das provas respectivas. O critério do módulo é produzir o objeto positivo, fechado, autoadjunto e não singular, com tipo e domínio; não fechar A1(b).\n\n## Fornecedores\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='## Buscas e aceitação\n\nSeis modalidades e outras bancadas registradas em '+str(A/'searches.json')+'. Ausência nos recortes não é ausência universal. Build, axiomas e controles/revisão separados antecedem aceite. Nenhum fornecedor antigo é alterado.\n'
put(R/'REAPROVEITAMENTO_A1B_GERADOR_POSITIVO.md',s.encode('utf8'));print('FICHE',len(providers))
