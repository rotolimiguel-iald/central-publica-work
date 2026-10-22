# Consulta — ação direita fechada, CFC e aproximantes por seno

[DERIVED — análise matemática e interfaces locais; nenhuma implementação ou compilação desta rota.]

A proposta é válida com as duas propriedades, de b e b*, e com o sinal abaixo. Ela oferece uma rota mais curta para o consumidor R do que a construção adicional por grafos/projeções: mantém diretamente o J original e fornece aproximantes explícitos. O fechamento GNS3 e os dois lemas de limites já foram reproduzidos em pareceres separados. Esta nota não aprova a fonte de álgebra ainda em DEV, nem acrescenta novos alvos aos aceites anteriores.

1. **A propriedade e a ordem do produto.** Escreva N=regularCoreAlgebra P, π=scalarGNSRepresentation P, J=scalarTomitaPolarFactor P e ρ(b)=Jπ(b*)J⁻¹. A função ρ é complexa-linear em b porque as duas conjugações escalares se cancelam; é antirrepresentação: ρ(bc)=ρ(c)ρ(b), e ρ(b*)=ρ(b)*. Isso não exige comutatividade de N nem igualdade global de comutantes. Seja P(b) a identidade, para TODO a∈nν, de pertença ab∈nν e Λν(ab)=ρ(b)Λν(a). Para produto, primeiro use P(b) em a e depois P(c) em ab: Λν((ab)c)=ρ(c)ρ(b)Λν(a). O resultado tem exatamente a ordem de ρ(bc). Soma/escala/unidade usam a linearidade da inscrição e do ideal já existentes. NÃO se deve deduzir P(b*) de P(b) sem prova. Definir E={b∈N | P(b)∧P(b*)} torna legítima a estrela; no produto, a componente estrelada usa c*b* nessa ordem.

2. **Fechamento em norma sem novos vetores escolhidos.** Os dois teoremas dos cortes dão a equivalência exata

   P(b) ↔ ∀ a∈nν, ∀ n∈ℕ, C_n(ρ(b)Λν(a)) = D(ab)Ω_n,

   onde C_n=scalarGNSCutMap P n, D=dualOrbitRepresentation e Ω_n=scalarCutVacuum P n. O sentido direto é scalarGNSCutMap_weight_embedding; o reverso usa scalarWeightGNSEmbedding_of_cut_actions para o vetor já definido ρ(b)Λν(a). Assim não há tentativa de provar fechado um conjunto definido por uma escolha existencial descontínua. Para cada a,n ambos os lados são contínuos na NORMA de b. As cotas de operatorFieldLift/dualIntegralFamily dão ||D(b)||≤||b||; a restrição que define π preserva essa cota, e J é isométrico. A norma da estrela é contínua. A interseção de conjuntos isClosed_eq é fechada, mesmo sobre todos a; isso é interseção topológica, não interseção a.e. não enumerável. P e P∘star fechados dão E fechado em N.

3. **Levar E ao ambiente corretamente.** N é fechado na norma do CLM porque N=(N′)′ e Set.isClosed_centralizer vale para qualquer conjunto no ambiente Hausdorff com multiplicação separadamente contínua. A inclusão de N é uma closed embedding, por IsClosed.isClosedEmbedding_subtypeVal; sua imagem de E fechado é fechada, por IsClosed.isClosedMap_subtype_val. Não se está usando a afirmação falsa de que toda imagem contínua de fechado é fechada. E.map N.subtype é uma StarSubalgebra ℂ de B(H_regular) fechada. cfc_mem, em Range.lean, recebe exatamente esse IsClosed local e o elemento pertencente: não pede CompleteSpace N nem WStarAlgebra N. O CFC é feito no B(H_regular) completo já disponível. O transporte de volta ao subtipo é uma igualdade/injetividade da inclusão, não uma nova equivalência de álgebras de von Neumann.

4. **Sinal e aproximação concretos.** Use m=n+1>0 e U_t=regularUnitary P t. A fonte characterPhase é exp(−i s ξ), e regularSpectralCoordinates_character fornece V⁻¹U_t V=M_exp(−i 2πtξ). Logo a escolha

   A_m = (m/(2i))·(U_(−1/m) − U_(1/m))

   tem símbolo +m sin(2πξ/m), e é auto-adjunta. Inverter a ordem produz o sinal oposto. Se k significar log h, seu símbolo é −2πξ: nesse vocabulário R=sigmoid(−k), não sigmoid(k). Evite introduzir um novo operador log apenas para nomear a aproximação. A convenção acima já fixa o símbolo positivo desejado para R.

   Para reutilizar SEM GENERALIZAR o fornecedor realScalarMultiplier_cfc_ae, ponha

   X_m=(I+A_m/m)/2,  g_m(ξ)=(1+sin(2πξ/m))/2,
   f_m(z)=ofReal(sigmoid(m·(2 Re z−1))),  R_m=cfc f_m X_m.

   X_m∈E, tem símbolo g_m∈[0,1] e 0≤X_m≤I. O fornecedor existente exige precisamente um g contínuo entre 0 e 1; aplicá-lo diretamente a m sin seria erro de hipótese. Aplicá-lo a g_m, usando a naturalidade do CFC pela mesma V, dá o símbolo

   q_m(ξ)=sigmoid(m sin(2πξ/m)).

   A função f_m é globalmente contínua em ℂ, compatível com a hipótese explícita do fornecedor. cfc_mem dá R_m∈E; positividade e cota R_m≤I também seguem de 0≤q_m≤1 e do multiplicador positivo já existente. A pertença dos U_± a E vem do novo scalarRightAction_regular, aplicado também a −t e à identidade de estrela do grupo. Nenhuma geração forte abstrata foi assumida.

5. **Limite forte-* realmente suficiente.** Para cada ξ fixo, m sin(2πξ/m)→2πξ, pela derivada de sin em zero, portanto q_m(ξ)→sigmoid(2πξ). Para cada u∈L² vetorial, ||(q_m(ξ)−q(ξ))u(ξ)||²≤||u(ξ)||². DCT em norma² dá a convergência forte dos multiplicadores; conjugação pela MESMA V dá R_m→regularSpectralResolvent P. Como R_m e R são auto-adjuntos, os adjuntos convergem fortemente sem invocar continuidade forte geral da estrela. A cota uniforme é 1. O teorema scalarRightAction_closed_of_bounded_strongStar agora produz P(R), e a auto-adjunção dá R∈E. Não se afirma convergência na norma de operadores, monotonia dos R_m ou cota uniforme dos A_m. As oscilações do seno no infinito impedem inferir essas propriedades da convergência pontual; nenhuma delas é necessária.

6. **O consumidor sqrt(Bε) não pode ser só homônimo.** Para ε>0, o cálculo esperado no MESMO R é

   Bε = cfc (x ↦ x/(1+(ε−1)x)) R,
   sqrt(Bε) = cfc (x ↦ sqrt(x/(1+(ε−1)x))) R.

   No espectro [0,1], 1+(ε−1)x≥min(1,ε)>0. Resta provar a primeira igualdade com regularInverseGeneratorCutoff já definido, não criar outro corte com o mesmo nome. Uma ponte curta usa Dε=I+(ε−1)R, sua inversibilidade pela cota, o par (R y,(I−R)y) do grafo h e regularInverseGeneratorCutoff_graph_iff: em y=Dε⁻¹x, a soma da segunda componente com ε vezes a primeira é x, logo Bε x=R Dε⁻¹x. CFC identifica essa expressão racional. A segunda igualdade usa unicidade da raiz positiva ou composição CFC. A função racional tem apenas continuidade garantida no espectro; se o adaptador escolhido exigir continuidade global, deve-se estendê-la explicitamente, sem tratar o denominador como não nulo em toda ℝ. Por exemplo substituir o denominador por max(min(1,ε),1+(ε−1)x) fornece extensão contínua que coincide em [0,1]. A raiz real continua globalmente contínua. Depois cfc_mem e R∈E dão a ação direita desse sqrt(Bε), com o J original.

**Próximas obrigações concretas [OPEN].** (i) equivalência pelos cortes, leis e fechamento de E/map — fonte autoral em DEV, não examinada como final; (ii) identidade espectral do X_m, CFC do símbolo e DCT forte-* do R_m; (iii) consumo do lema de limites para R; (iv) igualdade do corte racional com o Bε existente e sua raiz. Nenhuma exige Schwartz, Fourier-L¹, Kaplansky, novo GNS, novo J ou novos domínios máximos. Em comparação, a rota por grafos/projeções exigiria adaptadores de representação diagonal e geração adicionais; não é necessária para este consumidor se a construção acima for implementada. Tracialidade, ordem das avaliações perturbadas e conclusão de A1(b) permanecem separadas; esta nota não as paga e não move gate.

Fornecedores e localizadores abaixo são lidos nesta consulta; seus hashes completos estão no JSON acompanhante. A lista é delimitada, não uma busca exaustiva. Nenhuma fonte autoral, memória ou parecer anterior foi alterado.

Data: 2026-09-14T20:50:16.282961-03:00

| Fonte | Declaração e linha lidas |
|---|---|
| [V351ScalarGNSClosedness.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351ScalarGNSClosedness.lean:14>) | `scalarGNSCutMap_weight_embedding` — 14 |
| [V351ScalarGNSClosedness.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351ScalarGNSClosedness.lean:35>) | `scalarWeightGNSEmbedding_of_cut_actions` — 35 |
| [V351ScalarRightActionLimits.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351ScalarRightActionLimits.lean:15>) | `scalarRightAction_regular` — 15 |
| [V351ScalarRightActionLimits.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351ScalarRightActionLimits.lean:26>) | `scalarRightAction_closed_of_bounded_strongStar` — 26 |
| [V350AntiunitaryPositiveConjugation.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350AntiunitaryPositiveConjugation.lean:25>) | `antiunitaryConjugate_apply` — 25 |
| [V350AntiunitaryPositiveConjugation.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350AntiunitaryPositiveConjugation.lean:28>) | `antiunitaryConjugate_mul` — 28 |
| [V350ScalarGNSAction.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarGNSAction.lean:25>) | `scalarGNSAmbientAction_norm_le` — 25 |
| [V350ScalarGNSRepresentation.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarGNSRepresentation.lean:14>) | `scalarGNSRepresentation` — 14 |
| [V350StrongOperatorField.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350StrongOperatorField.lean:71>) | `operatorFieldLift_norm_le` — 71 |
| [V350DualWeightCuts.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350DualWeightCuts.lean:14>) | `dualIntegralFamily` — 14 |
| [V350L2CharacterMultiplier.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350L2CharacterMultiplier.lean:21>) | `characterPhase` — 21 |
| [V350L2CharacterMultiplier.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350L2CharacterMultiplier.lean:98>) | `characterMultiplier_ae` — 98 |
| [V351RegularPositiveGraph.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularPositiveGraph.lean:72>) | `regularSpectralCoordinates` — 72 |
| [V351RegularPositiveGraph.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularPositiveGraph.lean:78>) | `regularSpectralResolvent` — 78 |
| [V351RegularImaginaryPowers.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularImaginaryPowers.lean:65>) | `regularSpectralCoordinates_character` — 65 |
| [V351ScalarMultiplierCalculus.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351ScalarMultiplierCalculus.lean:26>) | `compactScalarRepresentation` — 26 |
| [V351ScalarMultiplierCalculus.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351ScalarMultiplierCalculus.lean:73>) | `realScalarMultiplier_cfc_ae` — 73 |
| [V351InverseGeneratorCutoff.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351InverseGeneratorCutoff.lean:99>) | `regularInverseGeneratorCutoff_graph_iff` — 99 |
| [Range.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Range.lean:96>) | `cfc_mem` — 96 |
| [Basic.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra\Basic.lean:118>) | `centralizer_centralizer` — 118 |
| [Basic.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Topology\Algebra\Group\Basic.lean:49>) | `Set.isClosed_centralizer` — 49 |
| [Constructions.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Topology\Constructions.lean:400>) | `IsClosed.isClosedEmbedding_subtypeVal` — 400 |
| [Constructions.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Topology\Constructions.lean:403>) | `IsClosed.isClosedMap_subtype_val` — 403 |
| [Deriv.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Trigonometric\Deriv.lean:46>) | `hasDerivAt_sin` — 46 |
| [Deriv.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Trigonometric\Deriv.lean:320>) | `hasDerivAt_sin` — 320 |
| [Sigmoid.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Sigmoid.lean:207>) | `continuous_sigmoid` — 207 |
| [Sigmoid.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Sigmoid.lean:249>) | `continuous_sigmoid` — 249 |
