from pathlib import Path
import json,hashlib,os,re
from datetime import datetime

R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012')
K=R/'k'; OUT=R/'revisao_quadratica_consulta'
D=R/'dev_quadratic_trace/20260915_025534_427264'

def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def fresh(p,b):
    assert p.parent==OUT and not p.exists()
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b
    os.replace(tmp,p)

specs=[
 ('TGLExt/V350ScalarClosedTomita.lean',159,168,'Domínio e estrela diretamente no núcleo uniforme'),
 ('TGLExt/V350ScalarGNSStarDensity.lean',13,14,'Embedding uniforme concreto'),
 ('TGLExt/V350ScalarWeightStarCore.lean',43,55,'Inclusão do núcleo uniforme no núcleo do peso e igualdade dos embeddings'),
 ('TGLExt/V350ScalarWeightTomitaIdentification.lean',65,78,'Alternativa direta no núcleo pleno do peso'),
 ('TGLExt/V350ScalarWeightDomain.lean',43,52,'Inclusão I em n_nu, sem igualdade de ideais'),
 ('TGLExt/V350ScalarWeightCompletion.lean',90,95,'Embedding do peso pleno coincide com o antigo na inclusão'),
 ('TGLExt/V351PerturbedWeightNorm.lean',37,49,'Norma de corte com raiz e J originais'),
 ('TGLExt/V350AntiunitaryPositiveConjugation.lean',14,26,'Wrapper da raiz e conjugação antiunitária'),
 ('TGLExt/V350ScalarTomitaPolarInvolution.lean',56,72,'Lift do grafo, S da raiz e involução original'),
 ('TGLExt/V350ScalarTomitaPolarFactor.lean',49,58,'Fatorização no domínio original'),
 ('TGLExt/V350ScalarTomitaRootDomain.lean',30,53,'Identidade dos domínios S e raiz'),
 ('TGLExt/V350ResolventSquareRoot.lean',33,40,'Domínio exatamente range sqrt(T)'),
 ('TGLExt/BoundedGraphOperator.lean',76,85,'Valor no lift do grafo'),
 ('TGLExt/V351InverseLimitWeight.lean',13,18,'Definição do peso cortado'),
 ('TGLExt/V351InverseLimitWeight.lean',85,88,'Supremo sequencial do MESMO peso'),
 ('TGLExt/V351PerturbedWeightOrder.lean',11,25,'Exemplo privado de adaptação da identidade de norma; não fornecedor público'),
 ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean',143,150,'Identidade pública de norma do operador limitado'),
 ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean',79,79,'Troca da ordem dos vetores na parte real')]
providers=[]
for rel,first,last,role in specs:
    p=K/rel;ls=p.read_text(encoding='utf-8-sig').splitlines()
    providers.append(dict(role=role,source=pin(p),line=first,end_line=last,excerpt='\n'.join(ls[first-1:last])))
run=json.loads((D/'run.json').read_bytes());source=pin(D/'V351QuadraticTrace.lean')
assert all(source[k]==run['source'][k] for k in ['bytes','sha256'])
for field in ['stdout','stderr']:
    p=Path(run[field]['path']);assert pin(p)==run[field]
stdout=(D/'stdout.txt').read_text(encoding='utf-8-sig')
axs=re.findall(r"'([^']+)'\s+depends on axioms:\s*\[([^]]*)\]",stdout)
assert run['returncode']==0 and len(axs)==3
assert all({x.strip() for x in ax.split(',')}<={'propext','Classical.choice','Quot.sound'} for _,ax in axs)
analysis=[
 '[STATIC] Não identifiquei falha matemática nos três privados do snapshot. root_quadratic_commutation usa somente R>=0 e Commute R A; não exige A positivo/auto-adjunto. bounded_root_form_balance recebe explicitamente 0<=T<=1, comutações com U/V e balanço limitado, e entrega igualdade complexa de formas. double_cut_form_supremum usa upper bounds p,q<=1, positividade de C,D, comutações cruzadas e limites fortes; passa ao limite um índice por vez em ENNReal. Não exige finitude, monotonicidade das famílias, cota uniforme de C/D ou produto ilimitado. As metades 0<=p e 0<=q não são usadas nessa prova; são hipóteses redundantes benignas, não motivo para alterar o candidato. O rc0/trio é relido do DEV autoral, não compilação própria nem aceite34.',
 '[REAL — fornecedor direto] Para a:coreSubtype e ha:a in finiteDualStarCore P, forme Aa:finiteDualStarCore P com valor a. scalarStarCore_mem_closedTomitaDomain (P:=P) Aa e scalarClosedTomita_extends_star (P:=P) Aa fornecem exatamente o domínio e S x=Lambda(a*) para x=scalarGNSStarEmbedding P Aa. Não é necessário reusar toda a prova de fechamento do peso para este caso.',
 '[REAL — identidade dos embeddings] scalarUniformToWeightStar P Aa inclui no núcleo pleno, scalarWeightStarEmbedding_uniform iguala seu embedding ao x antigo e scalarUniformToWeightStar_star compatibiliza a estrela. Alternativamente, Aa determina ai:finiteDualLeftIdeal P com prova Aa.property.1; scalarWeightGNSEmbedding_uniform P ai iguala o embedding de Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P) ai ao embedding antigo. Isto fornece o A:scalarWeightLeftIdeal P exigido pela identidade do peso perturbado, sem assumir I=n_nu. Se o código já usa scalarWeightStarCore, scalarWeightStar_mem_closedTomitaDomain e scalarClosedTomita_extends_weight_star são a alternativa pronta.',
 '[DERIVED/OPEN — forma do peso] Para epsilon>0, ponha s=hilbertPositiveSqrt(B_epsilon), b=\u27e8s,hb\u27e9 com a prova de pertença devolvida por scalarWeight_inverseCutoff_perturbed_norm, e L=pi(star b). O fornecedor dá nu(s* a*a s)=ofReal ||L(J^-1 Lambda a)||^2. Usando map_star/map_mul, IsSelfAdjoint.of_nonneg da raiz e CFC.sqrt_mul_sqrt_self no MESMO B_epsilon, obtenha star L * L=pi(B_epsilon). ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left dá a forma com (pi B)v na primeira posição; inner_re_symm troca para Re<v,pi B v>. A ponte RCLike.re_eq_complex_re já é usada em PerturbedWeightOrder. Por scalarTomitaPolarFactor_involutive, J^-1 v=J v. Assim a forma desejada é ENNReal.ofReal(Re<J Lambda a,pi(B_epsilon) J Lambda a>), não uma igualdade do peso com um número complexo. Não é preciso identificar pi(sqrt B) com sqrt(pi B) ou definir outra raiz. Este último adaptador de norma/forma não foi compilado nesta consulta.',
 '[DERIVED/OPEN — ligação final] Domínio de S implica domínio da raiz por scalarClosedTomitaDomain_le_root, cujo domínio é range sqrt(T). Escolha u representando x; y=sqrt(1-T)u é o valor da raiz por bounded_graph_lift_apply. Há ainda um atalho de tipos: scalarTomita_sqrt_factor P u entrega diretamente S aplicado ao lift no domínio original = J y; scalarTomitaRootLift_coe e Subtype.ext ligam esse lift a x. Com S x=Lambda(a*), fica J Lambda(a*)=y usando a involução. A forma do peso para a dá o supremo em Jx; para a* dá o supremo em y. double_cut_form_supremum então tem o consumidor correto quando suas hipóteses concretas forem descarregadas. finiteDualStarCore não é aqui chamado núcleo analítico; nenhum domínio de produto ilimitado é acrescentado.',
 '[OPEN] Falta a instanciação concreta destes três privados e os adaptadores de embeddings/Gram/supremos. Nenhuma dessas pontes foi certificada por esta consulta. O snapshot não prova fulltrace, Q global ou gate. Não foi lida a fonte mutável K/V351QuadraticTrace.lean, nem houve compilação/escrita Lean.'
]
j=dict(timestamp=datetime.now().astimezone().isoformat(),status='STATIC_CONSULTATION__NOT_INDEPENDENT_DELTA34_ACCEPTANCE',snapshot=source,author_run=pin(D/'run.json'),historical_source_location=run['source']['path'],author_stdout=run['stdout'],author_stderr=run['stderr'],author_returncode=0,private_declarations=[dict(name=n,axioms=[x.strip() for x in ax.split(',')]) for n,ax in axs],own_compilation_performed=False,mutable_candidate_read=False,providers=providers,analysis=analysis,formal_acceptance=False,gate_modified=False)
name='CONSULTA_QUADRATICA_LIGACAO_GNS'
fresh(OUT/(name+'.json'),(json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode())
md=j['timestamp']+'\n\n[STATIC/DERIVED — consulta, não aceite34]\n\n'+'\n\n'.join(analysis)+'\n\nSnapshot lido: '+source['path']+'; '+str(source['bytes'])+' bytes; SHA256 '+source['sha256']+'.\n\nFornecedores relidos, com tipos/trechos exatos:\n\n'
for p in providers:
    md+=p['role']+' — ['+Path(p['source']['path']).name+'](<'+p['source']['path']+':'+str(p['line'])+'>)\n\n~~~lean\n'+p['excerpt']+'\n~~~\n\n'
fresh(OUT/(name+'.md'),md.encode('utf-8'))
print(json.dumps({'note':pin(OUT/(name+'.md')),'evidence':pin(OUT/(name+'.json')),'own_compilation_performed':False},ensure_ascii=False))
