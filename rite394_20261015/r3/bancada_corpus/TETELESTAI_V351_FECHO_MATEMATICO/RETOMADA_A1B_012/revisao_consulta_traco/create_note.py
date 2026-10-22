from pathlib import Path
from datetime import datetime
import hashlib,json,os,re
R=Path(__file__).resolve().parent.parent;O=Path(__file__).resolve().parent;V=R/'v/TGLExt'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
 assert p.parent==O and not p.exists(),p
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b;os.replace(t,p)
spec=[
 ('V350ScalarDualWeight.lean','scalarDualWeight_normal','Normalidade de ν em supremos internos; não tracialidade.'),
 ('V350ScalarDualWeight.lean','scalarDualWeight_square_finite_strong_density','Semifinitude usual: quadrados finitos em ideal fortemente denso.'),
 ('V350ScalarWeightTomitaIdentification.lean','scalarWeightTomitaGraph_closure_eq','Mesmo Tomita do peso completo, sem exigir I=nν.'),
 ('V351ScalarImaginaryCoreAction.lean','scalarTomitaImaginaryPower_core_conjugation','Implementação por Δν e Adλ em todo core.'),
 ('V351RegularImaginaryPowers.lean','regularPositiveGenerator_imaginaryPower','h^{it}=λ_t pelo resolvente existente.'),
 ('V351RegularGeneratorAffiliation.lean','regularSpectralResolvent_mem','R∈N; CFC bounded de R reutilizável.'),
 ('V351RegularGeneratorAffiliation.lean','regularPositiveGenerator_commutant_graph','Afiliação do mesmo grafo fechado.'),
 ('V350ScalarRegularRightGNS.lean','regularRightGNS_intertwines','Multiplicação direita por λ_t no domínio nν completo.'),
 ('V350ScalarRegularRightPolar.lean','scalarTomitaPolar_conjugate_regular_right','J original liga ação direita e π(λ_t*) nos geradores.'),
 ('V350ScalarGNSStrongContinuity.lean','scalarGNSRepresentation_tendsto_of_uniformly_bounded','Passagem de redes fortes limitadas à mesma π.'),
 ('V351ScalarMultiplierCalculus.lean','realScalarMultiplier_cfc_ae','Cálculo funcional pontual do multiplicador já usado para as potências.')]
rows=[]
for fn,nm,role in spec:
 p=V/fn;s=p.read_text(encoding='utf8');m=re.search(r'^theorem '+nm+r'\b',s,re.M);assert m,(p,nm)
 rows.append(dict(name=nm,line=s[:m.start()].count('\n')+1,source=pin(p),role=role))
other=[V/'SemifiniteWeight.lean',V/'TracialCentralizerExpectation.lean',V/'TowerGibbsPerturbation.lean',R.parent/'kernel/TGLExt/V351RegularCoreTraceContract.lean',R.parent/'kernel/TGLExt/V351BaseFunctionalWeightLaws.lean']
note='''# Consulta delimitada — perturbação de ν e tracialidade

[DERIVED / OPEN] Consulta sem novo Lean, sem compilação e sem alteração de fonte ou memória. Os aceites separados de cálculo5, potências4 e afiliação3 permanecem intactos. A consulta não entrega RegularCoreTraceData nem altera gate.

O fornecedor matemático específico é Pedersen–Takesaki: para ν NSF e q positivo não singular afiliado ao centralizador, a perturbação ν_q é NSF e σ_t^{ν_q}=Ad(q^{it})∘σ_t^ν. Hiai §9, Proposição 9.3 e Teorema 9.4, e a prova do Teorema 9.9 aplicam isso a q=h⁻¹ quando σ_t^ν=Ad(h^{it}), obtendo σ_t^τ=id e tracialidade. A regularização q(1+εq)⁻¹ é (h+ε)⁻¹. O Lema 9.1(4) fornece a ordem das avaliações perturbadas, não a ordem dos sanduíches. [KNOWN, fonte relida](https://arxiv.org/pdf/2004.02383#page=83). Não é teorema Lean localizado nesta consulta.

[REAL — interfaces locais] A base ν normal/fiel/semifinita, o seu GNS/Tomita, a implementação core5, as potências do h regular e sua afiliação já têm fornecedores distintos abaixo. Não pedi novamente esses resultados. O dado atual separa Δν, no GNS do peso, de h, no espaço regular; as duas implementações têm papéis diferentes e não requerem Δν=h.

[DERIVED — adaptação econômica] Nem sequer é preciso começar criando um objeto h⁻¹ não limitado. Para R=(1+h)⁻¹ e ε>0, usar fε(x)=x/(1−x+εx) em [0,1] e rε=fε(R), sε=√rε. O denominador é ≥min(1,ε)>0. A equação do grafo verifica rε=(h+ε)⁻¹; afiliação e CFC por comutação dão rε,sε∈N. São funções de R e ficam fixas por Ad(h^{it}). Essa adaptação continua proposta, não compilada aqui.

O primeiro elo concreto de peso é provar, para estes cortes, a ação direita por sε no GNS completo e sua identificação com Jπ(sε)J. Já há regularRightGNS_intertwines para λ_t e scalarTomitaPolar_conjugate_regular_right para o mesmo J. Estender essa identidade ao cálculo funcional/cierre adequado dos geradores é trabalho residual explícito, usando a continuidade forte limitada já existente e controle do domínio da inscrição. Não é consequência automática de uma troca de nomes de operadores.

Uma meta intermediária útil é ν(sε a*a sε)=‖π(sε)JΛν(a)‖² para a∈nν, com todos os domínios justificados. Ela ordena essas avaliações pela ordem de rε. Para afirmar a ordem em TODO N+ ainda é preciso a versão estendida do lema de perturbação; não cobrir esse passo silenciosamente com minorantes finitos de ν. Mesmo b≤c não implica b*x*b≤c*x*c para x≥0 em uma álgebra não comutativa. Portanto scalarDualWeight_mono/normal, sozinhos, não justificam a direção do supremo proposto.

Depois disso, a meta que efetivamente paga tracialidade é a identidade modular da perturbação (ou uma prova direta equivalente de τ(a*a)=τ(aa*) para TODO a∈N). A mera invariância de cada corte ou do limite por Adλ não a substitui. Não é necessário refazer GNS, construir predual abstrato completo, ou exigir um gap de h. O campo de minorantes positivos finitos continua sendo uma obrigação de τ após tracialidade; a semifinitude usual de ν permanece aceita.

[REAL — escopo da busca] Li somente os fornecedores listados e três candidatos históricos. SemifiniteWeight.opWeight usa ellTwo; não fornece a perturbação no core atual. TracialCentralizerExpectation exige perfil constante 1/2 para seu resultado global e trata omegaState na base; não é um fornecedor para ν arbitrário no core. TowerGibbsPerturbation trata filtros/vetores de Gibbs nos níveis, sem a lei modular desta perturbação não limitada. Não localizei nos recortes lidos o lema PT concreto pronto; isso não é uma afirmação de inexistência no acervo inteiro. Duas primeiras consultas por nomes em v não encontraram módulos V351 antigos de contrato/leis, então li suas fontes em OLD/kernel, sem copiar ou recompilar.

Próximo consumidor mínimo sugerido: um lema específico de perturbação pelos cortes rε, com monotonicidade das avaliações e fórmula GNS, seguido da lei modular da perturbação que cancela Ad(h^{it}). O supremo ε>0 pode ser substituído por ε=1/(n+1), mas somente depois de provar a cofinalidade e a monotonicidade corretas. Escala dual e τ final não foram pagos por esta consulta.

Fornecedores relidos e pinados:

| Declaração | Fonte/linha | Papel | SHA256 fonte |
|---|---|---|---|
'''
for r in rows:note+=f"| `{r['name']}` | [{Path(r['source']['path']).name}](<{r['source']['path']}:{r['line']}>) | {r['role']} | `{r['source']['sha256']}` |\n"
note+='\nData da leitura: '+datetime.now().astimezone().isoformat()+'.\n'
md=O/'CONSULTA_PERTURBACAO_TRACIALIDADE.md';fresh(md,note.encode('utf8'))
data=dict(status='CONCEPTUAL_ONLY__NO_NEW_LEAN__TRACE_OPEN',report=pin(md),providers=rows,other_sources_read=[pin(p) for p in other],primary_reference=dict(url='https://arxiv.org/pdf/2004.02383',sections=['Lemma 9.1(4)','Proposition 9.3','Theorem 9.4','Theorem 9.9']),exhaustive_search=False,new_lean_objects=0,builds_executed_for_consultation=0,memories_modified=False,previous_reviews_modified=False)
fresh(O/'CONSULTA_PERTURBACAO_TRACIALIDADE.json',(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
print(json.dumps(dict(report=pin(md),json=pin(O/'CONSULTA_PERTURBACAO_TRACIALIDADE.json')),ensure_ascii=False))
