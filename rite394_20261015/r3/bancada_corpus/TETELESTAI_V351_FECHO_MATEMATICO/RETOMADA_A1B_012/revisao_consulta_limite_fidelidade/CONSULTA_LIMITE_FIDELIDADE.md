# Consulta — fidelidade e escala dual do limite
2026-09-14T22:39:34.941992-03:00

[DERIVED — proposta, não prova Lean nova] Use Wε(X)=ν(Sε* X Sε), Sε=hilbertPositiveSqrt(Bε), δn=1/(n+1), τ(X)=sup_n Wδn(X). É notação matemática para o candidato descrito; **não li V351InverseLimitWeight em DEV**. Os alvos sugeridos abaixo ainda não estão certificados nesta consulta.

**Fidelidade: basta n=0.** Se τ(X)=0, então W1(X)=0 por le_iSup. O fornecedor [regularInverseGeneratorCutoff_one](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V351InverseGeneratorCutoff.lean:43>) dá B1=R. A raiz S=√R pertence ao mesmo core pelo fornecedor já pago de raízes dos cortes; S*XS é positivo. Aplicar [dualQuadraticIntegral_vacuum_faithful](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V350ScalarDualWeightFaithfulness.lean:54>) dá SXS=0, usando S*=S.

É possível **evitar até um novo lema de imagem densa/injetividade da raiz**: como S²=R, multiplicar a igualdade por S dos dois lados dá RXR=0. [regularSpectralResolvent_injective](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V351RegularPositiveGraph.lean:98>) dá XR=0. A imagem de R é densa pela auto-adjunção de R≥0 e pelo fornecedor genérico [ChatgptAudit.Continuous049.bounded_graph_domain_dense](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/BoundedGraphOperator.lean:118>) aplicado a R e 0. Atenção ao tipo literal: ele conclui densidade do domínio de boundedGraphOperator; esse domínio é range(R). A conversão já é usada em [resolventDampingOperator_denseRange](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V351ResolventImaginaryPowers.lean:20>). Continuidade de X, ou DenseRange.induction com isClosed_eq, conclui X=0. O sentido inverso é zero do peso. Nenhuma finitude de ν(X), gap ou inversa limitada foi usada. graph_iff também permitiria investigar injetividade de cada Bε, mas isso excede o necessário para esta fidelidade.

**Raiz dual: a unicidade positiva pode ser menor que um adaptador mapCFC.** Já existe
θ_s(Bε)=exp(s) B_(ε exp(s)).
Com κ=√exp(s)>0, os operadores θ_s(Sε) e κ S_(ε exp(s)) são positivos e têm o mesmo quadrado. Usar [dualAmbient_nonneg](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V350DualWeightCuts.lean:40>), map_mul, Sε²=Bε e Real.sq_sqrt; [CFC.mul_self_eq_mul_self_iff](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean:294>) conclui:
θ_s(Sε)=√exp(s) • S_(ε exp(s)).
Também serve CFC.sqrt_unique (:283). Fixar instâncias numa Hilbert genérica e especializar o wrapper antigo evita repetir sua construção. Se optar por mapCFC, [StarAlgHomClass.map_cfc](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unique.lean:461>) exige continuidade do homomorfismo e os predicados CFC; dualAmbient é a equivalência estrela por conjugação unitária. Essa alternativa não é necessária para a igualdade pela unicidade.

**Sinal da escala: exp(−s).** O fornecedor certo de νθ=ν é [dualQuadraticIntegral_dual_invariant](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V350DualWeightForm.lean:87>), válido para todo A e vetor. Não o confundir com invariância por regularUnitary, que é outra ação.

Transportar o sanduíche inteiro por θ_(−s), usando θ_(−s)θ_s=id e a raiz transportada, fornece exatamente
Wε(θ_s X) = ofReal(exp(−s)) · W_(ε exp(−s))(X).
O coeficiente quadrático usa [dualQuadraticIntegral_smul_operator](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V350DualQuadraticLaws.lean:61>); √exp(−s) aparece duas vezes. A identidade equivalente de transporte simultâneo é Wε(X)=ofReal(exp(s)) W_(ε exp(s))(θ_s X). O fator positivo finito preserva o caso ∞. A ação sobre PositiveCoreInput deve manter o mesmo operador θ_s(X.val), com pertença via regularDualAction e positividade via dualAmbient_nonneg; nenhum novo cone ou GNS.

**Cofinalidade: duas desigualdades de supremo bastam.** Para r>0, provar sup_n W_(r δn)(X)=sup_n Wδn(X). O fornecedor [scalarWeight_inverseCutoff_antitone](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V351RegulatorWeightOrder.lean:66>) fornece a direção de comparação. Para cada n, escolher m com δm<rδn dá W_(rδn)≤Wδm; para a volta escolher m com δm<δn/r dá Wδn≤W_(rδm). Ambas escolhas vêm diretamente de [exists_nat_one_div_lt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/.lake/packages/mathlib/Mathlib/Algebra/Order/Archimedean/Basic.lean:213>). Aplicar iSup_le/le_iSup_of_le. Isso evita construir uma reindexação por bijeção, provar continuidade em ε ou usar atBot de ℝ (que significaria −∞, não 0 pela direita). [ENNReal.mul_iSup](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/.lake/packages/mathlib/Mathlib/Data/ENNReal/Inv.lean:807>) transporta o fator, sem hipótese de supremum finito.

Alvos propostos, nomes apenas sugestivos [DERIVED]:

1. inverseLimitWeight_faithful: τ(X)=0 ↔ X=0, X:PositiveCoreInput P.
2. regularInverseCutoffSqrt_dual: θ_s Sε=√exp(s) • S_(ε exp(s)), ε>0, s real.
3. inverseCutoffWeight_dual: Wε(θ_s X)=ofReal(exp(−s))·W_(ε exp(−s))(X).
4. inverseLimitWeight_scaled_sequence: para r>0, sup_n W_(rδn)(X)=τ(X).
5. inverseLimitWeight_dual: τ(θ_s X)=ofReal(exp(−s))·τ(X).

[OPEN] Fidelidade e escala dual do candidato ainda precisam dessas ligações compiladas. Nenhuma delas, isolada ou conjuntamente, demonstra tracialidade ou semifinitude de τ. Sem minorantes positivos finitos de ν, novo GNS, nova realização espectral ou antecipação do review22.

[REAL — alcance] Consulta local delimitada; fontes e APIs acima lidas, pins e excertos no JSON. Os objetos próprios dos deltas20/21 e relatórios entregues foram apenas referenciados. Nenhuma compilação, execução de monólito/recorder, alteração de fonte autoral ou memória. Aguardarei o congelamento para a revisão formal.
