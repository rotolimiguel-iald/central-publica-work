# Continuação 035 — deformações observáveis e área de Fisher

06/09/2026. [REAL / DERIVED / INPUT / OPEN] Continuação espontânea da ordem007, em resposta à hipótese angular do operador. A meta ampla permanece aberta.

## A distinção proposta pelo operador

A hipótese pode ser formulada assim: uma grandeza geradora e a geometria obtida por uma leitura angular quadrática dela são objetos diferentes. Essa distinção faz sentido matemático. Identificar o primeiro objeto como poço/cauda e a leitura como luz que se dobra e retorna tem, por enquanto, estatuto [ONTO/CONJECTURE].

Há três operações distintas. Para uma fase escalar u=exp(iθ), |u|²=1. Para sua diferença em relação à identidade, |u−1|²=4sin²(θ/2), uma resposta angular positiva e variável. Para uma superfície com duas direções, a densidade de área é sqrt(g_ss g_tt−g_st²). A existência da segunda expressão não fornece, por si só, a terceira: faltam as duas direções, sua correlação e uma métrica justificada.

Na bancada, o L das etapas030–033 é o likelihoodGenerator, identificado com log H para a densidade relativa limitada H. O Atlas usa também L_phi na sequência luminodinâmica de angulação/radicalização, com «ONTO na direção; REAL nas identidades». Não demonstramos uma identificação tipada desses dois objetos. A lagrangiana radicalizada registrada no Atlas é outro objeto, com estatuto DECLARADO na origem. Não transportamos teoremas por homonímia.

Referências locais consultadas somente em leitura: TGL_ATLAS.md, verbetes “Luz = razão = radicalizar = encontrar”, “TÚNEL LUMINODINÂMICO” e “O ângulo como projeção”, em C:/IALD/Central de Patentes/memory/TGL_ATLAS.md.

## O ponto pago pela etapa anterior

[REAL — etapa034 selada] As fases do centralizador de omega podem produzir tangentes horizontais e Gram positivo no espaço de purificações, enquanto o estado restrito a M permanece constante. Nessa órbita, as derivadas de qualquer família finita de observáveis fixos em M são zero. Uma matriz induzida por essas leituras não recupera aquele Gram positivo.

Isso também se aplica à invariância já demonstrada para o cociclo particular u_s=exp(isL) da bancada. Não é uma proibição de toda geometria: fixa o escopo em que essa leitura não detecta movimento. Observáveis dependentes do parâmetro, referências interferométricas, outros estados ou observáveis fora de M exigem análises próprias.

## Construção efetiva na torre

[INPUT] Escolhemos dois sítios distintos n,m; as matrizes de Pauli X, Y, Z em cada sítio; e a família
U(s,t)=exp(is X_n)exp(it X_m).
Esses são operadores da representação da torre existente, pertencentes a M. Não se substitui a torre por um modelo finito alheio.

O estado medido é psi_(s,t)(B)=omega(U* B U), que coincide com o estado vetorial de U Omega. Para A limitado autoadjunto,
d/ds omega(exp(-isA) B exp(isA))|_0 = i omega(BA−AB).
O código prova HasDerivAt dessa expectativa, por composição com o funcional contínuo; não toma apenas um comutador formal por derivada.

Com p_n=P.w n e r_n=2p_n−1, os valores locais são omega(X_n)=omega(Y_n)=0 e omega(Z_n)=r_n. A fatorização omega(A_n B_m)=omega(A_n)omega(B_m) foi provada para quaisquer matrizes locais em sítios distintos.

Como i[Y,X]=2Z, as leituras reais de Y_n e Y_m têm Jacobiano
J_obs(0)=diag(2r_n,2r_m).
As derivadas cruzadas são zero. Seu determinante é4r_n r_m, não nulo se ambos p_n,p_m diferem de1/2. Pode ser negativo se os vieses tiverem sinais opostos. J_obs aqui designa o Jacobiano das leituras, não o operador J de Tomita.

## A inscrição quadrática como probabilidade

A medição fixa de Y tem projetores P_n^a=(I+aY_n)/2, a=±1. Para n≠m, os quatro E_ab=P_n^a P_m^b são projetores autoadjuntos, positivos, ortogonais entre si e pertencentes a M, com soma I.

As probabilidades foram definidas pelas expectativas efetivas e ligadas à norma quadrada:
q_ab(s,t)=psi_(s,t)(E_ab)=||E_ab U(s,t)Omega||².
O código prova que a expectativa complexa já é real, e prova não negatividade e soma1. Assim, neste exemplo, uma projeção seguida de norma quadrada fornece uma inscrição operacional da rotação.

Na origem:
q_ab=1/4,
partial_s q_ab=a r_n/2,
partial_t q_ab=b r_m/2.
São derivadas das funções efetivamente definidas, obtidas dos comutadores e da fatorização. Não são coeficientes postulados de uma distribuição escolhida depois.

## A métrica e a densidade de área

Definimos o Fisher clássico da medição na origem pelas probabilidades e suas derivadas:
g_ij(0)=sum_ab (partial_i q_ab)(partial_j q_ab)/q_ab.
Os denominadores são estritamente positivos ali. A soma resulta em
g_F(0)=diag(4r_n²,4r_m²),
det g_F(0)=16r_n² r_m²,
a_F(0)=sqrt(det g_F(0))=4|r_n r_m|.

A forma quadrática é não negativa. Se p_n,p_m≠1/2, o determinante e a densidade de área são positivos. A igualdade a_F=|det J_obs| é consequência dessas contas; não foi imposta como definição de métrica.

[KNOWN] A definição de Fisher a partir das probabilidades de uma medição e sua distinção em relação à informação quântica estão discutidas por Barndorff-Nielsen e Gill, “Fisher information in quantum statistics”, §2, pp.3–4, https://arxiv.org/pdf/quant-ph/9808009 . Esta etapa formaliza o Fisher da medição escolhida; não invoca um teorema geral de otimização para chamá-lo de Fisher quântico.

Controles exatos: no perfil p=1/3, J_obs=diag(-2/3,-2/3), g_F=diag(4/9,4/9) e a_F=4/9. Se qualquer um dos sítios tem p=1/2, sua direção de resposta desaparece e a área é zero. Para o perfil inteiramente tracional, a matriz de Fisher na origem é zero.

A hipótese n≠m é essencial às fórmulas de quatro resultados positivos. A existência de definições totais de divisão em Lean não permite interpretar o caso n=m com probabilidades nulas como se tivesse os mesmos denominadores positivos.

## Limites que continuam explícitos

O resultado é local na origem e nas coordenadas escolhidas. Foram provadas derivadas por eixos, uma matriz de Fisher e sua densidade de área nesse ponto. Não foi formalizada aqui a fórmula trigonométrica global das probabilidades, uma métrica sobre toda a órbita, SLD, otimização de medição ou igualdade global com Bures.

A escolha de X e Y continua INPUT. X_n não foi identificado com o L=log H centralizante, nem com L_phi. O resultado mostra como obter mudança observável e uma inscrição quadrática positiva; falta uma regra da própria teoria que selecione esses geradores e leituras.

A densidade4/9 é adimensional e depende da normalização dos parâmetros. Não é uma área física em unidades de comprimento ao quadrado. Para chegar a uma área gravitacional é necessário construir a correspondência com regiões/superfícies, justificar escala e normalização, recuperar assinatura e dinâmica, e demonstrar que os objetos coincidem. Dar o nome de área física a a_F não cumpre essa obrigação.

A expressão (u−I)^*(u−I) é positiva, mas não distingue s de −s quando é par nesse parâmetro. O retorno de uma evolução unitária também não demonstra atração assintótica. “Fluxo de estabilização” exigirá especificar a leitura ou norma em que ocorre convergência e provar sua lei, preservando a distinção entre regime hiperbólico da face e regime compacto da projeção. Não há nesta etapa derivação de helicidade de gráviton, poço gravitacional ou reconstrução gravitacional geral.

## Evidência e custódia

A ordem008 chegou durante a preparação deste lote. Ela exige instâncias nomeadas e uma compilação nova em diretório limpo, com um arquivo que importe conjuntamente o lote. O relato da gerência sobre incorporações anteriores tem estatuto [DECLARADO]; não substitui nossa leitura dos artefatos. Para aplicar o procedimento, as instâncias035 foram nomeadas e uma bancada limpa reconstruiu033–035, alterando somente nomes de instâncias nas cópias033–034. Os selados anteriores ficam intactos.

Os módulos novos são UnitaryStateDerivative, SitePauliObservables, PauliOperationalSurface, PauliProbabilityModel e PauliMeasurementFisher, todos no namespace ChatgptAudit.Observable035. O último integra os demais. Cada declaração theorem e def nova tem #print axioms; as duas instâncias locais são nomeadas e censadas separadamente.

Validação final [REAL]: 13 etapas aprovadas em diretório novo (12 módulos e o importador conjunto). Nos cinco módulos novos, o censo mediu 131 teoremas, 23 declarações def e 2 instâncias locais nomeadas, com zero instância anônima. Os fontes035 compilados são cópias exatas dos fontes entregues. Todas as saídas têm exit0, zero erros/avisos/sorryAx e axiomas apenas no trio permitido. O consumidor do manifesto limpo também passou em verificação somente leitura.

A validação final exige exit0, fonte estável, nenhum erro/aviso/sorryAx e dependências apenas propext, Classical.choice e Quot.sound. O auditor035 confere o fonte exato, logs, versões anteriores em backups de bytes, artefatos, dependências locais e entrega. Os registros antigos de verify_stage.ps1 documentam o hash do fonte, mas não todos os inputs de cada execução: pin posterior de um olean não comprova sozinho sua proveniência. A validação limpa da ordem008 acrescenta registros específicos de inputs e saídas, com sua fronteira de dependências explicitada; não é recompilação completa de Lean/mathlib nem auditoria da gerência. Contagens e hashes são calculados no manifesto, não transcritos de memória.

Uma revisão independente dos cinco fontes não identificou falha matemática material nem circularidade na definição das probabilidades e de Fisher; ressaltou as restrições n≠m, não tracialidade para positividade estrita e escopo local. Essa revisão não substitui compilação nem auditoria/incorporação pela gerência.

Tentativas de compilação rejeitadas são preservadas, incluindo um timeout de inferência do nível da torre corrigido com argumentos explícitos, e correções de simplificação matricial e projeção real. Não contam como verificações aprovadas.

Todas as escritas desta continuação ocorreram apenas em Chatgpt. Originais, um.py, kernel canônico, Atlas, memórias, gates e entregas seladas anteriores permanecem somente em leitura. Nenhum gate foi movido. A atualização canônica depende da gerência no túnel.
