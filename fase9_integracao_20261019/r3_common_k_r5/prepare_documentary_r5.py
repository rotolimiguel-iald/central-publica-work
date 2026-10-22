"""Write exclusive documentary candidates; no scientific execution or observed input."""
from pathlib import Path
import hashlib,json,datetime
B=Path(__file__).resolve().parents[1]
O=Path(__file__).resolve().parent
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def new(name,value):
    text=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    with (O/name).open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    return pin(O/name)
specs=[
 ('r4_robust_tail_r3/PROOF.txt',[(1,21)],'Prova prévia: f fixo, Gaussianidade e limite da média nula.'),
 ('r4_robust_tail_r3/robust_tail.py',[(18,60)],'Consumidor existente apenas fator fixo; não implementa supremo contínuo.'),
 ('r2_background/API_CONTRACT_R1.json',[(14,28)],'K(theta), prior e dupla contagem; sem conjunto de confiança.'),
 ('r2_background/BACKGROUND_INTEGRATION_R1.txt',[(11,20)],'Propagação comum já construída; covariância/posterior admitida ainda pendente.'),
 ('r2_background/PLAN_SYNTHETIC_R1.json',[(78,104)],'Covariância theta explicitamente sintética, não estimativa com cobertura.'),
 ('r2_refinement_r3/CONFIGURATION_R3.json',[(1,38),(5990,6000)],'Caixa uniforme de integração; coverage significa cobertura da tabela/interpolação.'),
 ('r2_refinement_r3/THETA_PLAN_R3.json',[(1,1)],'Quadratura e alvo de convergência, não construção frequentista.'),
 ('r1_envelope/covariance_envelope_r1.py',[(1,180)],'Envelope PSD diagonal reutilizado, não covariância física admitida.')]
sources=[]
for rel,ranges,role in specs:
    p=B/rel; lines=p.read_text(encoding='utf-8').splitlines()
    sources.append({**pin(p),'role':role,'anchors':[{'start':a,'end':min(z,len(lines)),'text':'\n'.join(lines[a-1:z])} for a,z in ranges]})
new('SOURCE_CUSTODY_R5.json',{'scope':'FOCAL_EXISTING_ARTIFACTS_ONLY_NOT_UNIVERSAL_ABSENCE','sources':sources})
proof='''CAUDA UNIFORME COM K COMUM — R3/R4, camada R5
Autoria: /root/r69_calibration_bridge; F3.INTEGRACAO_20261019.
[DERIVED — prova analítica candidata; não Lean, não execução observacional]

1. Objeto e reuso
Theta é parâmetro verdadeiro fixo desconhecido, que pode incluir H0, ombh2, omch2
e qualquer nuisance necessário. Beta=ALPHA_FINE_CODATA_2018*sqrt(e) em runtime;
K(theta)=exp[(2 beta/3)ln E(theta,z*)], com fornecedor e normalização nomeados.
É UM K(theta) para todos os leitores na hipótese de mapa comum; não sortear K_i
independentes. O mapa comum H_i=K H0 continua hipótese física a verificar, não
consequência da prova estatística. Reuso: robust_tail_r3/PROOF.txt:1–21 e API:21–27.

2. Validade pontual, antes de estimar theta
Para cada theta fixo, escolha previamente pesos w(theta) com soma 1 e f(theta)>0.
Pode haver dependência determinística em theta; não escolha por centros observados.
D_theta(Y)=w(theta)'X-f(theta) B. Sob o nulo, E_theta D_theta<=b_theta, e admita
normalidade conjunta dos erros e desvios marginais totais corretos. Os demais
nuisances são abrangidos uniformemente pelas hipóteses ou incluídos em theta.
s_theta=sum_i |w_i(theta)| sigma_i(theta)+|f(theta)| sigma_B(theta) > 0.
O envelope PSD inclui a covariância local–fundo desconhecida. Para d_theta>b_theta,
p_theta(Y)=SF((d_theta-b_theta)/s_theta); para d_theta<=b_theta, p_theta=1.
Então P_theta(p_theta<=u)<=u. Sigmas/bias estimados nos mesmos dados precisam de
prova adicional ou inclusão na região de confiança; um plug-in não recebe validade.
Variância realmente nula pode ser tratada separadamente; denominador zero no
consumidor numérico é recusa, não significância infinita. A forma existente usa
b>=0; um limite unilateral mais geral é matematicamente possível, não implementado.

3. Região aleatória e correção de cobertura, sem independência
Seja C(Y) mensurável, construído por procedimento pré-fixado, tal que
inf_{theta,nuisance no nulo} P_theta{theta em C(Y)} >= 1-gamma, 0<=gamma<1.
Exija p_theta superuniforme no MESMO experimento conjunto de Y; não é necessário
que C e o teste usem dados independentes, nem validade condicional a C.
Defina S(Y)=sup_{theta em C(Y)} p_theta(Y) e p_U=min(1,S+gamma).
Para alpha<gamma, rejeição p_U<=alpha é impossível. Para gamma<=alpha<1:
 {p_U<=alpha} está contido em {theta0 fora de C} união {p_theta0<=alpha-gamma}.
Logo P_theta0(p_U<=alpha)<=gamma+(alpha-gamma)=alpha. Para alpha=1 é trivial.
A prova usa apenas inclusão de eventos e união, não independência.
Se C vazio/ilegível, retorne 1 ou recusa visível, nunca sup(vazio)=0.
Use majorante certificado Sbar>=S em vez de S se necessário. Máximo em nós de
quadratura é limite INFERIOR do supremo: não basta para um p conservador.
É preciso certificação contínua (intervalos/Lipschitz ou monotonicidade provada),
incluindo erro do fornecedor, ou declarar supremum não qualificado e p_U ausente.
Gamma deve ser fixo antes do composto; selecionar gamma pela menor cauda sem
correção adicional não está coberto. Para meta alpha_crit, gamma<alpha_crit é
necessário para evidência não trivial; uma região 95% não sustenta cauda de 5 sigma.

4. Caixa de prior, região de confiança e mistura são objetos diferentes
A caixa theta de CONFIGURATION_R3:7–38 é domínio de prior uniforme de integração,
não região C com cobertura. Domínio fixo que SABIDAMENTE contém theta permite
gamma=0 e supremo sobre todo domínio; a conclusão é condicional a essa inclusão.
Uma caixa escolhida como prior não prova que a natureza está nela. Regiões de
credibilidade posterior também não ganham cobertura frequentista por definição.
Integral bayesiana de likelihood e posterior-preditiva seguem o modelo/prior
nomeados; nem lnB nem média de p_theta são p_U. Contraexemplo: Y=(j,U), U uniforme,
theta=j em {0,1}, p_theta(Y)=U se theta=j, e 0 caso contrário. Cada p verdadeiro
é uniforme, mas média com pesos 1/2 é U/2 e rejeita a nível alpha com taxa 2alpha.
Isso não invalida inferência bayesiana; invalida promovê-la à cauda uniforme.
O texto coverage em CONFIGURATION_R3:5996 trata tabela/interpolação, não pessoas
ou repetições amostrais nem probabilidade de cobertura de theta verdadeiro.

5. Qual hipótese realmente contém K
Contra LambdaCDM pelo contraste fixo f=1, K não entra na distribuição nula desse
contraste: entra na previsão alternativa e no poder. Não há motivo para pagar
gamma de K em um teste cuja estatística/nulo são independentes dele. Outras
incertezas do fundo, viés e validade do mapa continuam necessárias.
Na compatibilidade TGL, f(theta)=K(theta), ou num escore histórico que depende
de K, a propagação é necessária. O escore histórico não recebe uma distribuição
Gaussiana ou a prova acima só por ser chamado z: deve primeiro ser identificado
como estatística e ter a validade pontual demonstrada. Não substituímos sua fórmula.
Para f=K, todos os leitores compartilham o mesmo theta em cada avaliação; não
otimizar K separadamente por leitor como se fossem parâmetros físicos distintos.
Uma caixa independente mais larga pode dar majorante conservador, mas perde essa
estrutura e sensibilidade, e não deve ser descrita como modelo comum exato.

6. Covariância preditiva exata e limite de sua interpretação
Para qualquer lei de mistura explícita pi(dtheta) e segundos momentos finitos,
mu_theta=E[Y|theta], Sigma_theta=Cov(Y|theta):
 Cov_pi(Y)=E_pi[Sigma_theta]+Cov_pi(mu_theta).
Se mu_local(theta)=m(theta) 1, m=K(theta)H(theta), o bloco comum adicional é
 Var_pi(KH) 11', Var_pi(KH)=E_pi[K^2 H^2]-(E_pi[KH])^2.
Não substituir por E[K^2]E[H^2] nem K^2 Var(H): K e H não foram independentes.
Para vetor conjunto (X,B), mu=(KH 1,H), o bloco cruzado adicional é Cov_pi(KH,H)1
e o bloco de B é Var_pi(H). E_pi[Sigma_theta] conserva ruído condicional cruzado.
Para contraste fixo f, a contribuição comum é Var_pi((K-f)H), além do ruído
condicional. Se f=K(theta) muda com theta, aplique a lei à variável D_theta inteira;
não multiplique uma covariância marginal por um vetor de coeficientes aleatórios.
Essa identidade é exata sob pi, mas mistura Gaussiana pode não ser Gaussiana e
não fornece cauda frequentista uniforme. Não reutilizar dados do fundo duas vezes:
likelihood conjunta integrada uma vez, ou predição condicionada com informação
claramente contabilizada. A prova de união não depende dessa identidade de mistura.

7. Multiplicidade e falsificadores do contrato
Para família finita pré-fixada de m testes, pode-se Bonferroni sobre p_U individuais.
Se UMA região C com erro gamma serve a todos, a regra alternativa global
p_global=min(1,gamma + m min_j sup_C p_{j,theta}) é válida por união, sem
independência; ela paga gamma uma vez. Não confundir essa regra com soma de sigmas,
nem misturar escalar e ROOT90da em uma única evidência sem protocolo pré-fixado.
Recusas: cobertura não documentada; prior rotulado confiança; C vazio; theta/K
não comum; hipótese Gaussiana/viés/sigmas ausentes; gamma adaptado ao resultado;
máximo de grade promovido a supremo; NaN/bool/inf; pesos escolhidos pelos centros;
normalização H0 divergente entre fornecedor e nulo; sigmas preditivas usadas como
prova de cauda. Cada uma quebra premissa concreta ou integridade, não muda gate.

8. Lacuna concreta nesta cobertura documental
[REAL documental] API_CONTRACT_R1:22–27 e CONFIGURATION_R3:7–38 fornecem prior;
PLAN_SYNTHETIC_R1:78–95 fornece Ctheta sintética; BACKGROUND_INTEGRATION_R1:12–20
fornece propagação compartilhada e registra posterior/covariância admitida pendentes.
THETA_PLAN_R3 fornece quadratura e erro de refinamento, não cobertura frequentista.
[OPEN] Não localizado, nesses artefatos focalmente consultados, procedimento C(Y)
admissível com garantia uniforme 1-gamma e erro pequeno suficiente, nem certificação
do supremo contínuo. Não é alegação de ausência universal no acervo. Não executar
CAMB, centros observados ou novo composto para este relatório. O avanço é o contrato
analítico; sem recibo de cobertura, resultado científico incondicional permanece OPEN.
'''
new('UNIFORM_COMMON_K_PROOF_R5.txt',proof)
contract={
 'schema':'F3_COMMON_K_UNIFORM_TAIL_CONTRACT_CANDIDATE_V1','status':'DERIVED_CONTRACT_OPEN_ADMISSION',
 'reference':str(B/'SESSION_REFERENCE.json'),'preflight_revision':13,'task_id':'R3',
 'author':'/root/r69_calibration_bridge','implementation_delivered':False,'science_execution':False,
 'reused_fixed_factor_api':str(B/'r4_robust_tail_r3/robust_tail.py'),
 'common_theta':{'required':True,'beta':'ALPHA_FINE_CODATA_2018*sqrt(e) runtime','K':'exp((2*beta/3)*ln E(theta,zstar))','provider_and_H0_normalization':'must be pinned and common'},
 'branches':{'LCDM_fixed_contrast':'f=1; K absent from null p; K enters alternative/power',
 'TGL_compatibility':'f(theta)=K(theta); pointwise sampling validity and nuisance propagation required',
 'historical_score':'no transfer until actual score distribution is justified'},
 'required_evidence':[
 'sampling/null family with uniform pointwise p validity, including nuisance/bias and all total sigmas',
 'fixed-before-data confidence-set construction plus true coverage theorem/qualified bound and named gamma',
 'continuous supremum upper certificate including numerical and forward-model error',
 'measurement map and source admission independent from this mathematical contract',
 'fixed family and multiplicity rule, immutable source pins; hash alone is not authentication'],
 'statistic':'min(1, sup_{theta in C(Y)} p_theta(Y) + gamma)',
 'confidence_coverage_requirement':'inf_null P(theta_true in C(Y)) >= 1-gamma',
 'independence_between_set_and_test_required':False,
 'empty_or_invalid_set':'NO_INFERENCE_OR_P_EQUALS_ONE',
 'grid_supremum_without_error_certificate':'REFUSE',
 'prior_box_is_confidence_set':False,'mixture_is_uniform_tail':False,
 'current_coverage_receipt':None,'current_continuous_supremum_certificate':None,
 'physical_covariance_admitted':False,'observed_verdict':None,'may_open':False,'may_freeze':False,
 'falsifiers':['prior mislabeled coverage','unqualified grid maximum','data-chosen weights/gamma without selective proof','uncertified null mean/sigma/map','different K per reader claimed common','predictive covariance claimed Gaussian tail'],
 'covariance_identity':'E_pi[Sigma_theta] + Cov_pi(mu_theta); common block Var_pi(KH) 11^T; includes Cov_pi(KH,H)',
 'status_note':'No p value, sigma or numerical forecast calculated; candidate analytic proof and documentary inventory only.'}
new('COMMON_K_CONTRACT_R5.json',contract)
evidence=[pin(O/n) for n in ['prepare_documentary_r5.py','SOURCE_CUSTODY_R5.json','UNIFORM_COMMON_K_PROOF_R5.txt','COMMON_K_CONTRACT_R5.json']]
new('DELIVERY_COMMON_K_R5.json',{'status':'DERIVED_CONTRACT_COVERAGE_AND_SUPREMUM_OPEN','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'evidence':evidence,'source_count':len(sources),'scientific_executions':0,'providers':0,'observed_inputs':0,'mission_mutations':0,'originals_modified':False})
print(json.dumps(pin(O/'DELIVERY_COMMON_K_R5.json'),ensure_ascii=False))
