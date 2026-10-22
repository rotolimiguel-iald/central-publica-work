# Consulta: rota finita versus identificação do implementador original

[DERIVED / OPEN — consulta matemática, não revisão DEV]

Data: 2026-09-15T00:00:09.472583-03:00. Objetos: o mesmo ν=scalarDualWeight, τ=scalarInverseLimitWeight, S, F=S†, Δν=FS, J=scalarTomitaPolarFactor e U=scalarTomitaImaginaryPower. Nenhuma compilação, alteração Lean ou atualização de memória nesta consulta. Os fornecedores abaixo foram relidos; seus pins e trechos estão no JSON ao lado. A aceitação anterior das construções é herdada, não uma nova auditoria de axiomas.

A rota finita tem uma expressão candidata concreta que cancela a densidade matricial no MESMO τ. Porém, os fornecedores atuais não entregam automaticamente a leitura espectral desse peso nem a extensão dos níveis à álgebra inteira. O passo menor que identifiquei para a rota Q é provar a ação direita das médias, extrair vetores simultaneamente fixos por S e F e identificar U em um conjunto total. Isso reduz uma obrigação efetiva; a compatibilidade de meias potências/Q e a tracialidade continuam separadas.

## 1. Correção da sugestão das médias

[REAL — fonte] [regularAverage](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350RegularApproximation.lean:36>) define
eδ = δ⁻¹ ∫₀^δ λ_t dt, como integral FORTE de operadores, δ>0.
É uma média unilateral; não é auto-adjunta em geral. O programa não fornece SΛ(eδ)=Λ(eδ), muito menos FΛ(eδ)=Λ(eδ). Pertencer à álgebra das translações ou preservar ν não basta para essas igualdades.

[DERIVED] Use zδ=eδ*eδ. Ele é positivo, é quadrado-finito por eδ∈nν e pela propriedade de ideal à esquerda, e pertence também ao domínio algébrico da estrela. Os fornecedores são [regularAverage_hasFiniteDualSquare](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350DualSemifiniteIdeal.lean:108>), [finiteDualLeftIdeal_le_scalarWeight](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightDomain.lean:50>) e [scalarClosedTomita_extends_weight_star](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightTomitaIdentification.lean:71>).

A obrigação nova mais imediata pode ser enunciada matematicamente assim (nomes propostos, não constantes Lean existentes):

• **average_mem_polar_right**: δ>0 ⇒ eδ ∈ scalarPolarRightAlgebra P.
• **average_square_fixed_original_pair**: para ζδ=Λν(zδ), ζδ∈D(S)∩D(F) e Sζδ=Fζδ=ζδ.

Não receber essas conclusões como campos. A segunda segue da primeira e dos pares já construídos, conforme o argumento abaixo.

## 2. Prova menor da identificação U=πλ R₋ₜ

[REAL — fornecedores] [scalarPolarRightAlgebra_regular_mem](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarRightActionAlgebra.lean:164>) dá a pertinência das translações à álgebra direita E; [scalarPolarRightAlgebra](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarRightActionAlgebra.lean:94>) exige a propriedade direita tanto para b quanto para b*. [scalarRightAction_closed_of_bounded_strongStar](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarRightActionLimits.lean:26>) transporta a identidade para uma família uniformemente limitada convergente forte-*; a existência da família não está embutida no teorema.

[OPEN — adaptador efetivo] Para obter eδ∈E, construir somas finitas
b_m = m⁻¹ Σ_{k<m} λ_(δ k/m), m≥1.
Cada b_m está em E, tem norma ≤1 e converge fortemente a eδ; as somas adjuntas convergem a eδ*. A continuidade forte de λ no intervalo compacto paga a aproximação por somas de Riemann em cada vetor. Aplicar o fechamento forte-* duas vezes, para b_m e b_m*. Não invocar integral de Bochner de λ em B(H): a continuidade em norma dos operadores não está disponível. O fechamento EM NORMA de E, isoladamente, também não paga esta passagem. [operatorIntegral_apply](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350StrongOperatorIntegral.lean:51>) e [operatorIntegral_norm_le](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350StrongOperatorIntegral.lean:54>) fornecem a integral e a cota; não localizei nesta consulta um lema pronto que já faça toda a aproximação de E pela média.

[DERIVED] Defina ρ(z)=Jπ(z*)J⁻¹, com os mesmos objetos. Para z=zδ, a propriedade E e [scalarWeightGNSAction_intertwines](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightAction.lean:38>) dão
ρ(z)Λ(a)=Λ(az)=π(a)Λ(z), para TODO a∈nν.
Como z=z*, ρ(z) é auto-adjunto. Portanto essas duas identidades fornecem os campos reais de [ScalarRightAdjointPair](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRightAdjointPair.lean:17>), ambos com vetor Λ(z). [scalarRightAdjointPair_maximal](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRightAdjointPair.lean:128>) dá FΛ(z)=Λ(z) no adjunto máximo ORIGINAL. A extensão da estrela dá SΛ(z)=Λ(z). Não se presume continuidade de S nem domínio total.

[DERIVED] Pelo domínio EXATO de [scalarTomitaSquare_domain_iff](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarTomitaSquare.lean:40>), ζδ∈D(Δν) e Δνζδ=ζδ. Então [scalarTomitaResolvent_inverse](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarTomitaResolvent.lean:24>) dá Tνζδ=½ζδ, onde Tν=(1+Δν)⁻¹. A igualdade U_tζδ=ζδ pode ser obtida diretamente de [scalarTomitaImaginaryPower_damping](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryPowers.lean:29>): b(½)=¼ e g_t(½)=¼. Um adaptador CFC para um autovetor basta; [complex_cfc_selfadjoint_intertwines](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ResolventImaginaryIntertwining.lean:15>) permite produzi-lo usando um operador de posto um e (½)I. Tratar ζδ=0 sem pressupor vetor não nulo/separante. Essa aplicação do CFC ainda é obrigação nova, não execução desta consulta.

[REAL — sinal] [scalarTomitaPolar_regular_generator](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRegularPolarCommutation.lean:50>) prova Jπ(λ_t)J⁻¹=R₋ₜ, com R_t=regularRightGNS P t. Assim o candidato correto é
W_t=π(λ_t)R₋ₜ=π(λ_t)Jπ(λ_t)J⁻¹.
Não substituir por π(λ_t), nem por π(λ_t)R_t. [regularRightGNS_commutes_left](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRegularPolarCommutation.lean:13>) vale para toda a álgebra representada.

[DERIVED] zδ comuta com todas as λ_t, por [operatorIntegral_commutes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350StrongOperatorIntegral.lean:59>) e a lei de grupo. Logo W_tΛ(zδ)=Λ(zδ). U já implementa a mesma ação no core inteiro por [scalarTomitaImaginaryPower_core_conjugation](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarImaginaryCoreAction.lean:47>). Portanto U e W coincidem em π(a)Λ(zδ), para todo a∈N.

Falta apenas uma totalidade que tem fornecedores diretos, sem escolher outro GNS. [regularAverage_tendsto_identity](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350RegularApproximation.lean:68>) e [regularAverage_star_tendsto_identity](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ContractionAdjointLimit.lean:51>) dão zδ→1 forte, com norma ≤1. [scalarGNSRepresentation_tendsto_of_uniformly_bounded](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarGNSStrongContinuity.lean:16>) dá π(zδ)→I e, conjugando pelo J limitado, ρ(zδ)→I. Como π(a)Λ(zδ)=ρ(zδ)Λ(a), a densidade de [scalarWeightGNSEmbedding_denseRange](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightAction.lean:54>) torna a união dessas órbitas total. Não é necessário afirmar que UMA média produz vetor cíclico.

Resultado alvo: igualdade dos operadores limitados U_t=W_t em TODO H_I. Covariância sozinha só coloca W_t⁻¹U_t no comutante; os vetores fixos e a totalidade são o passo que elimina esse resíduo. A unicidade [scalarTomitaImaginaryPower_unique](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryPowers.lean:35>) exige a identidade amortecida, não apenas implementar a mesma ação.

[OPEN] Essa identificação não é, sozinha, a identidade quadrática Q do peso perturbado. Ainda se precisa transportar o dado de potências reais para a compatibilidade de domínios/formas de meia potência que compara os limites das normas de a e a*. Não identificar h com Δν. A consulta anterior de tracialidade permanece válida nesse limite.

## 3. O que a rota finita realmente entregaria

[REAL — objetos] Os níveis gerais usam towerW P N, estritamente positivo e de soma 1, não a família estacionária chainWeights l N de outro contexto. [tState](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/TowerDefinite.lean:102>) é Σ_i w_i a_ii; [omegaState_pi](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/TheFactorObject.lean:109>) identifica essa avaliação com o vetor da MESMA torre. [flowLevel_single](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/ModularFlowSpectrum.lean:49>) fornece o peso de E_ij. O nome informal “finiteMatrix” não identifica um fornecedor separado: os objetos encontrados são Matrix, towerPi, tState e rhoMat.

[DERIVED — coordenadas propostas, ainda sem lema Lean] Fixado um nível, escreva ρ=diag(w_i). No subespaço redutor L²(ℝ,levelSpace P N), a Fourier ordinária transforma λ_t, na entrada i,j, em
exp(it(log w_i − log w_j − 2πξ)).
O sinal vem de [fourier_shift](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351FourierTranslation.lean:47>) e [regularUnitary](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350RegularTowerRepresentation.lean:16>). Faça p=2πξ+log w_j, por coluna j, incluindo o fator (2π)⁻¹/² na mudança unitária de L². Nestas coordenadas as ações esquerdas seriam
π_n(a)=a,  λ_t=ρ^{it} exp(−itp),  h=ρ exp(−p).

O subespaço redutor e a restrição precisam ser identificados efetivamente com as inserções existentes. [project_flow_commutes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/ExpectationProjection.lean:58>) e a comutação da projeção de nível com a ação esquerda finita fornecem os ingredientes. A absorção [regularFlowAbsorptionUnitary](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351RegularFlowAbsorption.lean:51>) não pode ser citada como se deixasse a base constante: sua conjugação também move a ação da base. A leitura acima usa Fourier e mudança por coluna explicitamente. Para o MESMO h, transportar [regularPositiveGenerator_graph_iff](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351RegularSpectralGraph.lean:40>) ou as potências já identificadas, sem nomear um gerador novo e declará-lo igual.

[DERIVED — avaliação candidata a provar] Para um operador positivo do nível representado pelo campo matricial limitado X(p), as identidades alvo são, com valores em ENNReal,
ν(X) = (2π)⁻¹ ∫ Σ_i w_i X_ii(p) dp,
νε(X) = (2π)⁻¹ ∫ Σ_i w_i/(ε+w_i exp(−p)) X_ii(p) dp,
τ(X) = (2π)⁻¹ ∫ exp(p) Tr(X(p)) dp.

A primeira não é uma definição alternativa de ν. Deve seguir de [dualQuadraticIntegral](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350DualWeightForm.lean:62>), [dualHaarFactor](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350DualWeightForm.lean:17>), do vetor [regularVacuum](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarDualWeightFaithfulness.lean:15>), da norma do indicador testVector, e de Tonelli/Plancherel. A integração na variável dual elimina a densidade espectral do indicador de norma 1. A segunda avalia o corte ORIGINAL por sua identidade de grafo; a terceira usa convergência monótona dos coeficientes, inclusive valor infinito. O fator (2π)⁻¹ não pode ser omitido. A verificação de sinal é θ_sX(p)=X(p+s), compatível com θ_sh=e⁻ˢh e τ∘θ_s=e⁻ˢτ.

A fórmula final daria τ(a*a)=τ(aa*) nesse nível por ciclicidade da matriz finita, sem um novo GNS ou peso. Mas é um ALVO derivado, não teorema encontrado. Nem todo operador do core já vem acompanhado do campo X e da prova dessa avaliação. Mesmo num nível, adjoinar todas as λ_t deixa uma variável espectral contínua; a álgebra resultante não é simplesmente M_d.

O primeiro lema concreto da rota finita seria a avaliação dual normalizada na primeira fórmula, para campos matriciais positivos de uma classe especificada, com a identidade de representação comprovada. Começar por campos contínuos de suporte compacto reduz mensurabilidade, mas deixa explícita sua extensão posterior.

## 4. Expectativas e extensão: limites reais

[REAL] [expectation_preserves_state](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/TowerExpectation.lean:90>) preserva o estado da BASE. [expectation_flow_commutes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/ExpectationProjection.lean:65>) é equivariância modular dessa expectativa de base. [levelExpectation_strong_tendsto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350LevelExpectationStrongLimit.lean:16>) e [represented_levelExpectation_strong_tendsto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350LevelExpectationStrongLimit.lean:44>) dão convergência forte, incluindo a representação escalar. Não localizei no conjunto consultado uma expectativa já transportada para TODO core que preserve ν ou τ e tenha a desigualdade quadrática requerida. Isso é limite da consulta delimitada, não inexistência exaustiva no acervo.

A geração do core por base e λ, e a passagem de COMUTAÇÃO por geradores, não são um teorema de aproximação forte-* uniformemente limitada de todos os operadores por níveis finitos. Para extensão tracial seria necessário construir essa aproximação com controle de peso, ou uma expectativa do core com preservação/Schwarz adequadas. Igualdade em aproximantes mais semicontinuidade, sem controle superior, não basta.

[INPUT — autoria atual, não revisada aqui] O novo delta 27 foi anunciado com redução por sanduíches e Fatou. Sua revisão independente virá após esta consulta. Mesmo que a redução seja aceita, ela entrega “trace em finiteDualStarCore ⇔ trace global”; não identifica finiteDualStarCore com união dos níveis. [regularSandwich_mem_finiteDualStarCore](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350FiniteDualStarCore.lean:63>) admite eδ* a eδ para a arbitrário do core. Portanto esse conjunto não deve ser chamado inteiro de analítico, finito-matricial ou núcleo de autovetores homogêneos.

## 5. Decisão e estatutos

| Próximo passo | Estatuto nesta consulta | Redução real |
|---|---|---|
| eδ∈E por médias fortes-* de λ | OPEN, com fornecedores diretos | Fornece pares para zδ; nenhum peso/GNS novo |
| Sζδ=Fζδ=ζδ → Tνζδ=½ζδ → Uζδ=ζδ | DERIVED, aplicação Lean pendente | Fixa o implementador ORIGINAL em conjunto útil |
| Totalidade conjunta π(N)Λ(zδ), U=πλR₋ₜ | DERIVED após passos anteriores | Elimina resíduo de comutante; não supõe TT |
| Avaliação finita ν/νε/τ nas coordenadas p | DERIVED, ponte espectral integral OPEN | Cancelamento explícito de ρ no mesmo τ |
| Níveis → finiteDualStarCore → todo N | OPEN; segunda seta em revisão autoral separada | Exige aproximação/controladores reais |
| Q, tracialidade e minorantes do traço final | OPEN | Não pagos por isometria J, escala dual ou semifinitude usual |

Minha recomendação de custo é começar por **average_mem_polar_right**, em seguida o par fixo de zδ e a identificação dos implementadores por totalidade. A rota finita permanece alternativa concreta, mas a infraestrutura relida não a torna uma ligação imediata. Nenhuma parte desta consulta cobra novamente normalidade, fidelidade, escala dual ou semifinitude usual já entregues; a propriedade de minorantes positivos finitos continua reservada ao traço final.

Pins, locadores e blocos completos das declarações consultadas: [evidência JSON](./CONSULTA_ROTA_TRACIAL_2.json). A página primária de [Hiai, arXiv:2004.02383](https://arxiv.org/abs/2004.02383) foi consultada apenas como referência bibliográfica; nenhuma identificação local foi importada de TT/PT por citação. A busca foi limitada aos fornecedores indicados e seus imports relevantes. Ausências de nomes adivinhados foram corrigidas por busca; não são ausência de prova. Não houve varredura exaustiva, novo teorema, teste ou promoção de A1(b).
