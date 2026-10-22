# Consulta — identificação do corte por CFC e equação do grafo

[DERIVED — proposta matemática; nenhuma nova prova Lean nesta consulta]

A terceira rota proposta pelo agente principal é a mais econômica entre as três nas interfaces atuais. Mantém o MESMO R, V, h e Bε. Não precisa novamente conjugar representantes por shifts, nem construir inversão CFC de Dε. A aplicação concreta abaixo ainda deve ser compilada pelo autor; o DEV dos aproximantes é revisão separada.

Para ε>0, ponha δ=min(1,ε)>0 e Fε(z)=ofReal(Re z / max(δ,1+(ε−1)Re z)). Esta função ℂ→ℂ é globalmente contínua: o denominador é sempre ≥δ. Em z∈[0,1], 1+(ε−1)z=(1−z)+εz≥δ, logo a extensão coincide com rε(z)=z/(1+(ε−1)z). Os extremos são rε(0)=0 e rε(1)=1/ε; não há singularidade espectral nos extremos.

Se Y=cfc Fε R, naturalidade pelo V original e realScalarMultiplier_cfc_ae dão, para cada x e quase todo ξ, V⁻¹(Yx)(ξ)=rε(sigmoid κ)u(ξ), onde κ=2πξ e u=V⁻¹x. A identidade escalar é rε(sigmoid κ)=1/(ε+exp(−κ)). Assim 1−εrε(sigmoid κ)=exp(−κ)rε(sigmoid κ). Usando somente as igualdades a.e. de subtração e escala, regularPositiveGenerator_graph_iff conclui (Yx,x−εYx)∈graph(h).

Agora regularInverseGeneratorCutoff_graph_iff, aplicado precisamente a (Yx,x−εYx), dá Bε((x−εYx)+εYx)=Yx. A soma cancela e produz Bεx=Yx para TODO x. Extensionalidade de operadores entrega Bε=cfc Fε R. Esta direção do iff já contém a unicidade pela positividade do MESMO h. Não se assume igualdade dos cortes, não se redefine h, e não se exige que todo x pertença a D(h): a primeira componente Yx é que tem pertinência ao domínio provada.

Ônus efetivo: (1) continuidade da extensão max e simplificação no intervalo; (2) identidade escalar sigmoid/racional e naturalidade CFC; (3) um transporte a.e. finito para o grafo, seguido do iff existente. O resultado de naturalidade pode ser escrito para todo u já em coordenadas e então aplicado a V⁻¹x. Não há evento a.e. simultâneo para todos os vetores. Quando ε<1, Y pode ter norma >1: realScalarMultiplier deve continuar aplicado ao símbolo sigmoid κ∈[0,1], com Fε no CFC; não se deve tentar usar Y inteiro como multiplicador contratante.

Comparação: a rota por deslocamento também é válida, com sinal +log ε: ε⁻¹sigmoid(κ+log ε)=1/(ε+exp(−κ)). Porém acrescenta transporte do conjunto a.e. por uma translação e cancelamento dos shifts. A rota Dε=I+(ε−1)R também é válida, mas acrescenta cota estritamente positiva, isUnit, inversão CFC e álgebra de resolventes. Nenhum destes adaptadores é necessário para a terceira rota, porque a equação inversa única já foi paga.

Consumidor: uma vez aceito R∈E, scalarRightAction_cfc e a igualdade exata transferem Bε para E. Para a RAIZ ORIGINAL, a opção que permanece inteiramente no mesmo CFC é qε(z)=ofReal(sqrt(Re z/max(δ,1+(ε−1)Re z))). A função é contínua globalmente; no espectro [0,1] é não negativa e qε²=Fε. CFC/ação pontual dão Q=cfc qε R≥0 e Q²=Bε; CFC.sqrt_unique tem tipo Q*Q=Bε → 0≤Q → CFC.sqrt Bε=Q. Isto identifica a raiz existente, não cria uma raiz homônima. scalarRightAction_cfc fornece Q∈E. Positividade e igualdade quadrática precisam ser provadas, não decorrem apenas do nome sqrt na função.

[OPEN] Esta consulta não aceita o DEV seno, não prova perturbação/tracialidade, nem ordenação dos sanduíches por ε. A ação direita de R será conferida na revisão própria do candidato congelado. Nenhum fonte autoral, memória, monólito ou relatório selado foi alterado; nenhum build foi executado para esta consulta.

Fontes lidas (pins completos no JSON):

- [regularInverseGeneratorCutoff_graph_iff](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351InverseGeneratorCutoff.lean:99>).
- [regularPositiveGenerator_graph_iff](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularSpectralGraph.lean:40>).
- [realScalarMultiplier_cfc_ae](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351ScalarMultiplierCalculus.lean:73>).
- [scalarRightAction_cfc](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351ScalarRightActionAlgebra.lean:173>).
- [CFC.sqrt_unique](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:283>).
