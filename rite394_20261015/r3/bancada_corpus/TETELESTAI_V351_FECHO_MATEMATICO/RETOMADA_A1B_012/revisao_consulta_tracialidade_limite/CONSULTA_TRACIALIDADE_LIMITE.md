# Consulta — tracialidade do MESMO peso limite

[DERIVED / OPEN] Consulta de leitura, sem código Lean novo, sem compilação e sem aceite do DEV26. Pareceres 1–25, fontes, objetos e memórias permanecem intactos.

A rota curta na literatura é a perturbação de Pedersen–Takesaki: para ν NSF e h não singular afiliado, com σν_t=Ad(h^{it}), a perturbação por h⁻¹ tem grupo modular trivial e é tracial. A regularização é exatamente (h+ε)⁻¹. A prova e suas hipóteses estão em Hiai, Prop.9.3, Teo.9.4 e prova do Teo.9.9, pp.83–88. Isso é [KNOWN], não fornecedor Lean localizado. [Fonte primária relida](https://arxiv.org/pdf/2004.02383#page=84).

[REAL — alcance do mapa] LACUNAS_A1.md é um mapa histórico, não fotografia atual de cada entrega. A ação de Δν^{it} em π(N) já é fornecida por scalarTomitaImaginaryPower_core_conjugation; h^{it}=λ_t e a afiliação pertencem a outros módulos já entregues. A forma do supremo dos cortes, sua ordem, leis, fidelidade e escala também já têm fontes. Não pedir novamente esses pagamentos, nem identificação h=Δν: h atua no Hilbert regular e Δν no GNS original. O que falta aqui é a passagem modular/estrela que torna TRACIAL o mesmo scalarInverseLimitWeight.

[REAL — hipótese sugerida versus resultado existente] Ponha U_t=scalarTomitaImaginaryPower P t, J=scalarTomitaPolarFactor P, L_t=π(regularRightCoreElement P t). O resultado core5 é
U_t π(a)=π(λ_t a λ_t*) U_t.
Não localizei, na busca delimitada das fontes V350/V351 pertinentes, a igualdade adicional
(**U**) U_t=L_t · antiunitaryConjugate J L_t = L_t regularRightGNS P (−t).
O sinal −t na ação direita é determinado por scalarTomitaPolarFactor_regular_left; J é antilinear e J²=I. A fórmula proposta J U_t J=U_t está paga, não J U_t J=U_−t.

A ação direita nas inscrições e a ação esquerda existentes já identificam o segundo membro de (**U**) como Λν(a)↦Λν(λ_t a λ_t*). Para fechar (**U**) falta demonstrar essa mesma identidade para U_t nas inscrições densas, ou sua igualdade amortecida exigida por scalarTomitaImaginaryPower_unique. Este último NÃO é unicidade de quem implementa a mesma conjugação: sua premissa exata é W b(Tν)=g_t(Tν), para Tν=scalarTomitaResolvent P. Covariância sozinha só coloca a diferença dos implementadores no comutante; não a torna identidade. Não receber (**U**) como campo novo. Ela pode servir à via espectral, mas não é pré-requisito extra da via PT se a lei de perturbação for provada diretamente para a ação modular já identificada.

[DERIVED — alvo vetorial mínimo sem novo GNS] Para δn=1/(n+1), escreva s_n=hilbertPositiveSqrt(Bδn), L_n=π(⟨s_n,mem⟩), e, APENAS como notação desta consulta,
Q(v)=sup_n ENNReal.ofReal(||L_n v||²).
Não se afirma Q finito em todo Hν e não se cria operador h⁻¹/² na representação por decreto. Por scalarWeight_inverseCutoff_perturbed_norm, para a∈nν:
τ(a*a)=Q(J⁻¹Λν(a))=Q(JΛν(a)).
Para a∈scalarWeightStarCore P, seja x=Λν(a). O MESMO S estende estrela e S=J Bν, Bν=scalarTomitaPositiveRoot P, D(Bν)=D(S); portanto
τ(aa*)=Q(J Sx)=Q(Bν x).

Assim uma meta concreta, suficiente já sobre o núcleo finiteDualStarCore (não é necessário começar por TODO D(S)), é
(**Q**) Q(Bν Λν(a)) = Q(J Λν(a)).
A aplicação de Bν usa a inclusão de domínio fornecida por scalarWeightStar_mem_closedTomitaDomain e scalarClosedTomitaDomain_le_root. Igualdade em ENNReal deve incluir ∞. S=J Bν e a isometria de J NÃO provam (**Q**): Q não é a norma original e L_n não comuta com J em geral. Esta é precisamente a nova compatibilidade do peso perturbado com a estrela, não algo aceito por renomear τ.

Se for escolhida a via (**U**), ainda se deve transportar a identidade dos grupos para a forma/domínio de meia potência e identificar os cortes representados L_n. O cancelamento escrito informalmente Δν=π(h)·Jπ(h⁻¹)J envolve operadores não limitados; igualdade dos grupos não autoriza multiplicá-los em domínio não declarado. O menor consumidor é (**Q**) nos vetores do núcleo. Evita construir GNS de τ, mas o passo de cálculo funcional/continuação modular que prova (**Q**) continua real e aberto. Alternativa equivalente: prova KMS na faixa para elementos regularizados, com ação no tempo imaginário identificada; só invariância em tempos reais não basta. A nota não decide que uma dessas adaptações já esteja compilada.

[DERIVED — extensão econômica do núcleo a TODO a∈N] Este passo tem fornecedores concretos e não exige minorantes positivos finitos de ν nem graph-core de τ. Tome e_m=regularAverage P(1/(m+1)), a_m=e_m* a e_m=regularSandwich P a(1/(m+1)).
1. finiteDualStarCore_strongStar_approximation já dá a_m no núcleo, ||a_m||≤||a|| e convergência forte de a_m E a_m*. Não é hipótese nova de continuidade forte da estrela.
2. Para cada corte fixo ε, regularInverseCutoffSqrt_commutes_average e scalarWeight_right_average_le dão
   Wε((a e_m)*(a e_m))≤Wε(a*a):
   (a e_m)sε=(a sε)e_m. O fornecedor de média vale para TODO operador do core, mesmo com peso infinito.
   À esquerda, e_m e_m*≤I porque ||e_m||≤1; logo
   (e_m* a e_m)*(e_m* a e_m)≤(a e_m)*(a e_m).
   A monotonicidade já provada de Wε/τ conclui τ(a_m*a_m)≤τ(a*a). Aplicar a mesma construção a a* dá a estimativa correspondente. Não se ordenam sanduíches por sε≤sη.
3. Para cada ε, a_m sε→a sε fortemente. Para cada parâmetro dual s, dualAmbient s é conjugação por unidade, portanto a órbita aplicada a Ω converge. O integrando é ofReal(dualHaarFactor) vezes uma norma ao quadrado: Fatou, como em scalarWeight_square_eq_iSup_averages, dá
   Wε(a*a)≤liminf_m Wε(a_m*a_m)≤liminf_m τ(a_m*a_m).
   Passando ao supremo ε=δn: τ(a*a)≤liminf_m τ(a_m*a_m).
   Idem para aa*. Measurabilidade e Haar são os existentes; não se usa normalidade só para uma sequência não monótona.
4. Se (**Q**) foi provado no núcleo, então τ(a_m*a_m)=τ(a_m a_m*). A semicontinuidade do passo3 e a cota do passo2 dão τ(aa*)≤τ(a*a); repetir com a* dá igualdade, inclusive ∞.

Logo uma vez paga (**Q**), este adaptador Fatou+sanduíches fecha o campo exato
∀ a:(regularCoreAlgebra P).toStarSubalgebra,
scalarInverseLimitWeight P (TGLV351.positiveSquare P a)
=scalarInverseLimitWeight P (TGLV351.positiveSquare P (star a)).
Não depende da conclusão ainda DEV26. Semifinitude usual e o campo de minorantes do contrato continuam separados.

[REAL — fornecedores de perturbação examinados] BoundedPerturbationCocycle constrói cociclos de operadores limitados na torre; sua própria introdução marca Araki como analítico/não Lean. RelativeTomitaClosure usa TowerHilbert thirdThermalReference e filtro limitado invertível: não o peso ν no regularCore nem h⁻¹ sem gap. Seus padrões de transporte podem inspirar uma adaptação, mas nenhum é um exact para (**Q**) ou para o campo tracial deste candidato. A busca foi nominal e pelos tipos desses arquivos e da cadeia atual, não exaustiva no acervo inteiro.

Próximo alvo recomendado: compatibilidade (**Q**) no núcleo original, com escolha explícita da ponte modular que a prova; em seguida o adaptador do passo1–4. Não abrir predual, GNS novo ou nova definição de traço. Esta consulta não declara nenhum desses enunciados como teorema existente.


Leitura/pins: 2026-09-14T23:22:30.389311-03:00

Fornecedores principais (os enunciados completos e hashes lidos estão no JSON):

| Nome | Fonte/linha | Papel |
|---|---|---|
| scalarTomitaImaginaryPower_core_conjugation | [V351ScalarImaginaryCoreAction.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarImaginaryCoreAction.lean:47>) | Covariância pelo grupo do Δν original, todo a. |
| scalarTomitaImaginaryPower | [V351ScalarTomitaImaginaryPowers.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryPowers.lean:24>) | Grupo definido pelo resolvente do S†S original. |
| scalarTomitaImaginaryPower_unique | [V351ScalarTomitaImaginaryPowers.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryPowers.lean:35>) | Unicidade somente mediante identidade amortecida, não mera covariância. |
| scalarTomitaImaginaryPower_polar_commutes | [V351ScalarTomitaImaginaryConjugation.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryConjugation.lean:14>) | J U_t = U_t J, com J antilinear original. |
| scalarTomitaPolarFactor_regular_left | [V350ScalarRegularRightPolar.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRegularRightPolar.lean:113>) | Jπ(λ_t*)=R_t J, portanto Jπ(λ_t)J=R_-t. |
| regularRightGNS_intertwines | [V350ScalarRegularRightGNS.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRegularRightGNS.lean:98>) | Ação direita na inscrição completa. |
| scalarWeightGNSAction_intertwines | [V350ScalarWeightAction.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightAction.lean:38>) | Ação esquerda na inscrição completa. |
| scalarClosedTomita_graph_eq_weight | [V350ScalarWeightTomitaIdentification.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightTomitaIdentification.lean:58>) | Mesmo S é o fecho do grafo do peso completo. |
| scalarWeightStar_mem_closedTomitaDomain | [V350ScalarWeightTomitaIdentification.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightTomitaIdentification.lean:65>) | Domínio original para Λ(a), a no núcleo estrela do peso. |
| scalarClosedTomita_extends_weight_star | [V350ScalarWeightTomitaIdentification.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightTomitaIdentification.lean:71>) | SΛ(a)=Λ(a*). |
| scalarTomitaPolarFactor_factorization | [V350ScalarTomitaPolarFactor.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarTomitaPolarFactor.lean:54>) | S=J√Δν no domínio completo original. |
| scalarTomitaPositiveRoot_domain_eq | [V350ScalarTomitaRootDomain.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarTomitaRootDomain.lean:51>) | Domínios √Δν e S coincidem. |
| scalarWeight_inverseCutoff_perturbed_norm | [V351PerturbedWeightNorm.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351PerturbedWeightNorm.lean:37>) | Norma ponderada no mesmo Hν com J original. |
| scalarInverseLimitWeight | [V351InverseLimitWeight.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351InverseLimitWeight.lean:87>) | Supremo de cortes atual; não suposto traço. |
| finiteDualStarCore_strongStar_approximation | [V350FiniteDualStarCore.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350FiniteDualStarCore.lean:108>) | Sanduíches no núcleo, limite forte-* e cota uniforme. |
| regularInverseCutoffSqrt_commutes_average | [V351CutoffAverageCommutation.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351CutoffAverageCommutation.lean:49>) | Comuta a raiz original do corte com a média. |
| scalarWeight_square_eq_iSup_averages | [V351WeightAverageRecovery.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351WeightAverageRecovery.lean:16>) | Modelo já compilado de Fatou, Haar e recuperação. |
