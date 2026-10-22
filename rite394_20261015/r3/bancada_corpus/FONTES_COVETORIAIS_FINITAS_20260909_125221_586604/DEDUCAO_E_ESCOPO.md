# Soma finita de fontes covetoriais coerentes — 09/09/2026

[REAL] A fonte FiniteCoherentSources.lean, namespace ChatgptAudit.FiniteCoherentSource, foi compilada em Lean 4.31.0: **19 teoremas + 3 definições = 22 termos auditados**, dois processos com saída zero, zero warnings e zero erros nos logs do build final. Axiomas observados: Classical.choice, Quot.sound, propext. SHA-256 lido da fonte: b61e3e180c1d18e29640465f9e4ea355b3e0231e0412747319911914a047c99f. O recibo é BUILD_20260909_125638_325723/BUILD_RESULT.json. A cópia da fonte efetivamente compilada coincide byte a byte com a fonte congelada.

[REAL] Os builds BUILD_20260909_125235_863446 e BUILD_20260909_125455_822943 falharam na elaboração da contração quadrática e foram preservados. A correção separou a reescrita da contração da expansão de tensorQuad; as cópias de bytes anteriores também foram preservadas. Nenhum um.py foi executado ou importado e nenhum original foi modificado.

## Resultado matemático e dedução

[DERIVED] Para um índice finito J, pesos reais constantes λ_j, acoplamentos reais constantes c_j e campos covetoriais suaves w_j, a definição da linha 44 é

T_ab(x) = Σ_j λ_j c_j [w_j,a(x) w_j,b(x) − (1/2) g_ab(x) g^cd(x) w_j,c(x) w_j,d(x)].

A definição aceita pesos e acoplamentos com qualquer sinal. A tipagem probabilística λ_j>0 e Σλ_j=1 pertence à camada UnitaryLabelData da preparação conjunta. A fonte tensorial, por si, não declara seus coeficientes como probabilidades.

[DERIVED] A simetria segue da simetria de g (finite_covector_stress_symmetric, linha 52), e a suavidade segue da suavidade dos componentes de g, gInv e todos os w_j (finite_covector_stress_smooth, linha 93). O domínio é um aberto de Coordinate4, uma carta real de dimensão quatro; estes enunciados não constroem um atlas global de variedades.

[DERIVED] A contração completa foi provada em finite_covector_stress_quad, linha 62. Para d nulo em g, a parcela proporcional à métrica desaparece e

T(d,d) = Σ_j λ_j c_j [w_j(d)]²

(finite_covector_stress_null, linha 78). A positividade nula requer explicitamente λ_j c_j≥0 para todo j (finite_covector_stress_null_nonnegative, linha 86). Uma representação com acoplamentos de ambos os sinais não recebe positividade de energia automaticamente.

[DERIVED] A conservação é obtida por diferenciação efetiva. tensor_field_jet_finite_sum (linha 11) deriva a linearidade do diferencial da soma; covariant_tensor_jet_finite_sum (linha 21) distribui os termos da conexão; tensor_field_divergence_finite_sum (linha 28) distribui a contração. Com o lema canônico de multiplicação por constante, isso produz

∇^a T_ab = Σ_j λ_j ∇^a T^(j)_ab

(finite_covector_stress_divergence, linha 105), antes de impor qualquer lei de conservação por setor.

[POSTULATE — hipóteses de matéria e geometria, não conclusões] O teorema finite_covector_stress_conserved (linha 126) recebe: aberto U; g, gInv e todos os w_j suaves em U; g simétrica; gInv inversa de g dos dois lados; conexão compatível com g e sem torção; cada covetor fechado (ClosedCovectorOn) e satisfazendo a equação de onda covetorial (CovectorWaveOn). Pesos e acoplamentos não dependem de x. Com essas hipóteses, o lema canônico covector_stress_conserved_on anula cada termo da soma e a divergência total é zero. Não há hipótese chamada «conservação» substituindo a dedução.

[DERIVED] Fechamento e equação de onda de cada setor são condições suficientes. Não são necessárias para uma soma ser conservada: divergências de setores diferentes podem cancelar. Se uma construção posterior representa um T previamente conservado por igualdade de campos, sua conservação total deve ser transportada por essa igualdade; os covetores da representação algébrica não podem ser declarados fechados/harmônicos sem prova adicional.

## Compatibilidade com a preparação unitária conjunta

[DERIVED] finiteCoherentStressField (linha 48) substitui c_j por coherentCoupling a_j b_j u_j v_j. finite_response_matches_null_source (linha 151) prova exatamente

Σ_j λ_j unitaryResponse(a_j,b_j,w_j(d),u_j,v_j) = −π T(d,d)

para d nulo em g. Este passo é uma identidade algébrica; normalização dos eixos, normalização da preparação e positividade dos pesos são certificados fornecidos pela camada conjunta, não ocultados nesta identidade.

[DERIVED] A API encaixa em JointUnitaryPreparation.lean: usar C.weight, C.axisA, C.axisB, C.initialU, C.initialV e frequency j = covectorRead (w j x) d. A definição jointResponse é a soma exata acima; os teoremas de limite entrópico e modular da preparação conjunta dão o seu significado de coeficiente de segunda ordem. O rótulo j permanece no espaço de probabilidades; marginalizar os rótulos antes de calcular entropia não é a mesma construção.

[DERIVED] As frequências por setor formam uma função linear da direção (finite_directional_frequencies_add, linha 194; finite_directional_frequencies_smul, linha 201). A resposta total soma os quadrados por setor. Não se substitui Σ_j c_j[w_j(d)]² pelo quadrado de um único covetor sem demonstração.

## Controles e limites

[REAL] two_covector_squares_not_one (linha 207) prova que d₀²+d₁² não é [w(d)]² para todos os vetores d. As sondas incluem vetores que não são nulos. Portanto este controle não prova, isoladamente, impossibilidade de redução no cone nulo módulo uma parcela proporcional a g.

[REAL] finite_constant_covectors_flat_conserved (linha 226) fornece uma família habitada e concreta: quaisquer covetores, pesos e acoplamentos constantes na métrica plana eta4 com conexão zero produzem divergência zero. Isso demonstra conservação; não demonstra que uma fonte constante não nula satisfaz Einstein com a métrica plana.

[OPEN] A correspondência física de área e calor, a satisfação das equações de campo por dados físicos e uma teoria quântica geral não são deduzidas desta soma. Suavidade e conservação não são, por si, Einstein; uma representação algébrica de T não é uma lei que produza T. O módulo não altera gate ou bandeiras de fechamento.

## Verificação independente e fronteira

[REAL — revisão nesta sessão] /root/review_remaining_hypotheses realizou leitura semântica independente favorável: verificou a linearidade explícita, os coeficientes constantes, o uso de closed/wave, a hipótese de positividade nula e a soma das respostas após os quadrados. A ressalva sobre o controle de dois quadrados foi incorporada acima. O revisor não recompilou nem alterou a fonte. O recibo automático original conserva independent_review=false, porque foi emitido antes da revisão; este adendo registra a etapa posterior sem modificar o recibo.

[REAL] A compilação isolada usou binários canônicos preexistentes e Mathlib. O builder mediu fontes/binários importados diretamente antes e depois, sem mudança. Não reconstruiu nem mediu integralmente todas as dependências transitivas. O selo refere-se ao escopo compilado e à revisão descrita.

[INPUT — integração posterior] Importar o módulo como TGLExt.FiniteCoherentSources numa nova cópia; seu único import atual já é canônico (TGLExt.ScalarStressConservation). Preservar namespace. Acrescentar os 19 teoremas distintos à auditoria do agregado. Não é necessária mudança de flags/gate nem execução do programa para transpor esta fonte.
