# Consulta — semifinitude usual do peso limite

2026-09-14T22:59:23.744274-03:00

[DERIVED — argumento matemático e adaptadores propostos; nenhuma compilação ou prova Lean nova nesta consulta]

A rota com dδ=√(1−δBδ) é válida. Para obter apenas densidade do domínio finito, há uma versão menor: usar qδ=1−δBδ diretamente. Ela evita o transporte de raiz no limite forte e não exige novo CFC, DCT, PVM, GNS ou tracialidade. Não afirmo que estes novos adaptadores estejam compilados; os fornecedores abaixo foram lidos nas fontes e pinados.

Fixe o mesmo Hilbert regular H, core N, R=regularSpectralResolvent P, Bε=regularInverseGeneratorCutoff P ε, sε=hilbertPositiveSqrt(Bε), E=scalarPolarRightAlgebra P e τ=scalarInverseLimitWeight P. ν é a avaliação original em regularVacuum; h não é confundido com Δν no GNS.

1. **Identidade que reduz a cota.** Para ε,δ>0, a comutação e a identidade resolvente já provadas implicam, SEM dividir por δ−ε,

   Bε qδ = Bδ − ε Bδ Bε.

   Como 0≤δBδ≤1, temos 0≤qδ≤1. Os operadores Bε,Bδ,qδ comutam entre si. Commute.mul_nonneg dá

   0 ≤ Bε qδ ≤ Bδ ≤ δ⁻¹1.

   Esta é uma identidade de CLM LIMITADOS, deduzida do grafo já aceito. Não se escreve h fora de D(h), não se inverte h nem se precisa de gap. Os coeficientes de smul são reais positivos inseridos em ℂ; reutilizar a conversão por IsPositive.smul_of_nonneg dos módulos dos cortes evita exigir uma instância de reflexão de ordem escalar do subtipo.

2. **Sua raiz dδ funciona, mas não é indispensável.** A álgebra E é uma StarSubalgebra complexa unital. Bδ∈E está provado; logo qδ∈E por operações algébricas. scalarRightAction_sqrt fornece dδ∈E e dδ²=qδ pela raiz ORIGINAL. A comutação de dδ com Bε vem da CFC da mesma família, não de dδ∈E isoladamente. Assim Bε dδ²=Bεqδ≤δ⁻¹1, exatamente a cota solicitada.

   Para usar qδ em vez de dδ, observe que qδ−qδ²=qδ(1−qδ)≥0 e comuta com Bε. Logo também

   0 ≤ Bε qδ² ≤ Bε qδ ≤ δ⁻¹1.

   Só é necessário aplicar positividade de produtos COMUTANTES; nunca usar que sanduíches com conjugadores ordenados estejam ordenados. A variante qδ deixa todo o novo corte de domínio dentro da álgebra já existente por soma, produto e escala.

3. **Cota de peso no domínio original.** Para a:scalarWeightLeftIdeal P e kδ igual a dδ ou qδ, ponha b=kδ sε∈E e c=√(δ⁻¹)1∈E. A auto-adjunção e a comutação dos cortes dão

   b b*=Bε kδ² ≤ δ⁻¹1=c c*.

   Aplique scalarWeight_right_perturbed_mono a ESTE a, b e c. O lado esquerdo é exatamente Wε((a kδ)*(a kδ)); não se comuta a através dos cortes. O direito reduz por homogeneidade integral a ENNReal.ofReal(δ⁻¹) * ν(a*a). Portanto, por iSup_le nos ε_n=1/(n+1),

   τ((a kδ)*(a kδ)) ≤ ofReal(δ⁻¹) ν(a*a) < ∞.

   A finitude usa a.property e ENNReal.mul_lt_top ENNReal.ofReal_lt_top, como no fornecedor HasFiniteScalarSquare.left_mul. A cota depende de δ, mas é uniforme em ε — justamente o necessário para o supremo que define τ. Não é preciso o lema all-positive com comutação das médias: a aqui já pertence a nν. Não se exige ν finito em todo positivo, nem kδ comutando com a, nem igualdade entre os dois domínios finitos.

4. **Limite forte sem novo cálculo espectral.** Basta a sequência δ_n=1/(n+1). Defina D_n=δ_n B_(δ_n), q_n=1−D_n e S=1−R. Todos D_n e q_n são contrações positivas. O fornecedor regularSpectralResolvent_complement_injective, auto-adjunção de S e ChatgptAudit.Continuous049.bounded_graph_domain_dense S 0 ... dão DenseRange S: o domínio daquele boundedGraphOperator é sua imagem, independentemente do segundo operador.

   A identidade resolvente com ε=δ_n, η=1 e B1=R dá

   D_n S = δ_n R q_n,
   ‖D_n(Sv)‖ ≤ δ_n ‖v‖ → 0.

   Como ‖D_n‖≤1, cada D_n é 1-Lipschitz. A cadeia de APIs realmente localizada é:
   LipschitzWith.uniformEquicontinuous (fun n => (D_n : H→H)) 1,
   UniformEquicontinuous.equicontinuous,
   Equicontinuous.isClosed_setOf_tendsto com função limite zero,
   e densidade de Ran S. Equivalentemente, aplicar EquicontinuousAt.tendsto_of_mem_closure ponto a ponto. Isso prova D_n→0 e q_n→1 fortemente. Não há convergência em norma de operadores afirmada, nem hipótese de separabilidade.

   Se conservar d_n=√q_n, há uma etapa extra: positividade/contração da raiz e a desigualdade escalar CFC (1−√x)²≤1−x em [0,1] dão ‖(1−d_n)v‖²≤Re⟨v,D_n v⟩→0. Essa etapa é dispensável para a variante q_n. O helper DCT de V351SineResolventApprox é PRIVATE; sua prova não deve ser citada como API pública reaproveitável sem um novo adaptador.

5. **Densidade usual, sem diagonalização de duas famílias.** Defina apenas o conjunto de operadores do mesmo N com τ(x*x)<∞, representando x*x como PositiveCoreInput pela pertinência/positividade canônicas. A conclusão desejada tem o MESMO tipo WOT do teorema TGLV351.scalarWeight_square_finite_wot_closure, substituindo HasFiniteScalarSquare por esse critério para τ.

   Para todo a∈nν, a q_n pertence ao conjunto finito de τ pelo item3 e tende fortemente a a: composição pela aplicação contínua do CLM a. strong_tendsto_wot e mem_closure_of_tendsto dão a∈closure_WOT(nτ). A inclusão de nν nesse fecho, junto do teorema WOT antigo, dá N⊆closure_WOT(nτ). A inclusão oposta vem de regularCore_wot_closed. Não é necessário construir uma sequência única aproximando simultaneamente todo N, nem inventar um novo GNS.

   Se o consumidor exigir um Submodule nomeado, as leis zero/soma/escala/mono de τ já entregues permitem o adaptador usual de ideal de quadrados finitos, pelo molde HasFiniteScalarSquare (desigualdade de soma e (ba)*(ba)≤‖b‖²a*a). Não é uma hipótese adicional de semifinitude: a densidade acima é a conclusão efetiva a provar.

[OPEN — próximos alvos propostos, nomes apenas de trabalho]
- regularDomainCut_product_bound: para ε,δ>0, qδ∈E e Bε qδ²≤(δ⁻¹:ℂ)•1.
- inverseLimitWeight_domainCut_finite: para δ>0 e a:scalarWeightLeftIdeal P, τ((a qδ)*(a qδ))≤ofReal(δ⁻¹)ν(a*a)<∞.
- regularDomainCut_tendsto_identity: ∀v, Tendsto(fun n => q_(1/(n+1)) v) atTop (𝓝 v).
- inverseLimitWeight_square_finite_wot_closure: fecho WOT do conjunto de quadrados τ-finitos igual ao mesmo core. Sem premissa de densidade desse próprio conjunto.

Esses alvos formam uma rota concreta menor para a SEMIFINITUDE USUAL. Nenhum deles paga ainda o campo de minorantes positivos finitos de RegularCoreTraceData, que deve ser tratado no regime tracial. Não se infere semifinitude do supremo apenas porque os cortes individuais seriam semifinitos. Tracialidade, escala dual e emissão de contrato/flags não são conclusões desta consulta.

Escopo de leitura: K, consultas anteriores autorizadas e índices documentais canônicos somente para localização. Duas tentativas nominais de caminho (V350RegularWeakOperator e V350ScalarWeightGNSProperties) não localizaram arquivos; não são fornecedores. O primeiro foi resolvido pelas fontes reais V350RegularNormality/V350RegularTopology, e o segundo não é necessário à rota. A pesquisa foi delimitada, sem alegação de exaustividade. Nenhuma fonte, memória, parecer selado ou build foi alterado/executado.


Fornecedores lidos e pins medidos:

- [regularInverseGeneratorCutoff_nonneg/le/one](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:24>) — SHA256 f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227.
- [regularInverseGeneratorCutoff_commutes/resolvent_identity](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegulatorWeightOrder.lean:22>) — SHA256 b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838.
- [regularInverseGeneratorCutoff_right](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:94>) — SHA256 cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490.
- [scalarRightAction_sqrt; raiz original em E](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:116>) — SHA256 cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490.
- [scalarPolarRightAlgebra; fechamento por operações](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:94>) — SHA256 68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af.
- [scalarWeight_right_perturbed_mono](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightOrder.lean:29>) — SHA256 9af750ad0099449655e5350b76219d51986849e434584359bd09de475fe936d6.
- [scalarWeight_right_perturbed_norm; J original](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightNorm.lean:12>) — SHA256 9b4edeb94844ded88ec595b50160936d42e34637f4432493d02894dd7731bab9.
- [positividade, contração e injetividade do complemento do mesmo R](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:84>) — SHA256 d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390.
- [ChatgptAudit.Continuous049.bounded_graph_domain_dense](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\BoundedGraphOperator.lean:118>) — SHA256 4d70d27d25f31fed13b73a7ae60601478718e41bbc38c24c38117b0cc26dc84f.
- [LipschitzWith.uniformEquicontinuous](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\MetricSpace\UniformConvergence.lean:94>) — SHA256 01ed18a99a0f7b7183c033776cddfcd198c3e9b9000809d4c7572d6436c63e3a.
- [UniformEquicontinuous.equicontinuous](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\UniformSpace\Equicontinuity.lean:323>) — SHA256 dd3e8de0798b50489e45f0e117af17473290e2e1c1fc26218e7beccd3cdce692.
- [EquicontinuousAt.tendsto_of_mem_closure; Equicontinuous.isClosed_setOf_tendsto](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\UniformSpace\Equicontinuity.lean:963>) — SHA256 dd3e8de0798b50489e45f0e117af17473290e2e1c1fc26218e7beccd3cdce692.
- [Commute.mul_nonneg](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Instances.lean:291>) — SHA256 f05652edd12f24ddd2aa058ceb8762cceabda14a4580d7d237dcde26aaf8d6f4.
- [CStarAlgebra.norm_le_norm_of_nonneg_of_le](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Order.lean:449>) — SHA256 0802a500623d378e8c953961cac3c6391932515a7236d44dbceea11e2eb4611b.
- [tendsto_one_div_add_atTop_nhds_zero_nat](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecificLimits\Basic.lean:69>) — SHA256 dbbeb301e5b9dacc96ecd233fd05a02846a1fc88c9606f1b1d413d08aff5142e.
- [HasFiniteScalarSquare e scalarWeightLeftIdeal; critérios e exemplo ENNReal.mul_lt_top](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightDomain.lean:14>) — SHA256 e83ada9b5abbf2c179c28b03d3c020be83861681ba3ae450999c1c64ea8e2f0f.
- [scalarDualWeight_square_finite_strong_density](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeight.lean:66>) — SHA256 e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53.
- [TGLV351.scalarWeight_square_finite_wot_closure](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarWeightSemifiniteness.lean:16>) — SHA256 f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a.
- [strong_tendsto_wot](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularNormality.lean:19>) — SHA256 bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a.
- [regularCore_wot_closed](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTopology.lean:39>) — SHA256 13c92b1d8948bc4d2c3891d4cbfa9bf43ac353a95e9126e2c128b1379db0ebd5.
- [scalarInverseLimitWeight e leis aceitas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:87>) — SHA256 cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e.
- [dualQuadraticIntegral_smul_operator](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualQuadraticLaws.lean:61>) — SHA256 7085d5ad460720e87ea5e1e3cc8bcbf5b55193be77b2ba283988fbf03120c1f3.
- [scalarMultiplier_sequence_tendsto é PRIVATE; não fornecedor público genérico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351SineResolventApprox.lean:159>) — SHA256 a1c6f5e77916ee527da3716f634431ddaf1f36c9dd80376ceee83aeb63c20c01.
