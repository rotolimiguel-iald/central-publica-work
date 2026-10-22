Data: 2026-09-14T21:51:11.066642-03:00

# Consulta — peso dos cortes em todos os positivos e limite

[DERIVED — proposta matemática, sem novos teoremas Lean ou testes nesta consulta]

**Há uma ponte concreta pelos regularizadores existentes. Ela paga recuperação de valores e permite transportar a ordem dos coeficientes aos pesos. A tracialidade continua sendo uma obrigação modular distinta.**

Escrevo N para o mesmo core, ν para scalarDualWeight, J para o polar original no H_I, Bε=(h+ε)⁻¹ e sε=√Bε, ε>0. Não identifico o gerador h na Hilbert regular com Δν no H_I.

1. **Definir os pesos não exige estender a inscrição.** Para X∈N₊, νε(X):=ν(sε X sε) já faz sentido em ENNReal, inclusive ∞. É necessário apenas empacotar a positividade e pertinência do sanduíche. PositiveCoreInput.conjugate não é esse adaptador: recebe um operador de dualFixedCore, enquanto os cortes estão em N. As leis zero/soma/escala vêm de ν; normalidade exige explicitar que o sanduíche leva o supremo interno positivo dirigido ao supremo correspondente, usando o limite forte já disponível. Nenhum novo predual é necessário aqui.

2. **Recuperação sem minorantes.** Tome δ_n=1/(n+1)>0 e e_n=regularAverage P δ_n. Para TODO a∈N, a e_n∈I⊆nν. A cota scalarWeight_right_average_le vale sem hipótese de finitude; a convergência scalarOrbit_right_average_tendsto também. Aplicar Fatou aos integrandos ENNReal de norma-quadrado, com a mesma constante positiva finita dualHaarFactor, dá

   ν(a*a) ≤ liminf_n ν((a e_n)*(a e_n)) ≤ limsup_n ν((a e_n)*(a e_n)) ≤ ν(a*a).

   Portanto há convergência no intervalo estendido, inclusive quando o valor final é ∞, e igualdade com o supremo desses valores. Não se afirma monotonia da sequência. O fornecedor lintegral_liminf_le aceita a sequência atTop; não é necessário nem alegado um Fatou para redes arbitrárias. A versão DCT da convergência GNS existente continua restrita a a∈nν.

3. **A comutação que falta explicitar.** Para aplicar a recuperação ao mesmo input X em todos os pesos dos cortes, provar [e_n,sε]=0. Uma rota já sustentada por fornecedores: regularSpectralCoordinates_character põe λ_t em multiplicação por caracteres nas coordenadas onde R é multiplicação por sigmoid; logo [λ_t,R]=0. CFC transporta isso para sε, e regularAverage_apply transporta ao integral de λ_t. Não localizei um lema pronto com essa conclusão na busca nominal delimitada; registro-o como adaptador a provar. Não deduzo essa comutação de b∈E para um b arbitrário.

4. **Extensão efetiva da comparação.** Para X≥0 ponha a=√X e X_n=e_n* X e_n=(a e_n)*(a e_n). Esses X_n têm peso ν finito. Com a comutação do item 3,

   νε(X_n)=ν(((a sε)e_n)*((a sε)e_n)),  νε(X)=sup_n νε(X_n).

   O novo teorema de norma, aplicado a a e_n, expressa νε(X_n) por ofReal da forma quadrática de π(Bε) no vetor J⁻¹Λ(a e_n). Assim Bε≤Bη implica νε(X_n)≤νη(X_n) e, tomando sup_n, νε(X)≤νη(X) para TODO X≥0. A ordem Bε≤Bη para ε≥η é uma comparação escalar dos mesmos cortes CFC de R. **Não** se utiliza sε X sε≤sη X sη. Tampouco X_n≤X: essas compressões não são a família falsa de minorantes finitos de ν.

5. **O limite ainda precisa de sua própria semifinitude.** Depois da ordem anterior, τ(X)=sup_m ν_{1/(m+1)}(X) é o candidato crescente; soma e normalidade seguem das respectivas leis e troca de supremos. A cofinalidade fornece a leitura sup_{ε>0}. Não basta dizer que cada νε é semifinito: um supremo crescente de pesos semifinitos pode perder essa propriedade.

   Uma opção concreta, sem PVM, é d_k=√(1−δ_k Bδ_k), δ_k=1/(k+1). São funções CFC do mesmo R, pertencem a E, e os símbolos dão d_k→1 fortemente e Bε d_k²≤δ_k⁻¹ I. A identidade de norma para b=d_k sε então dá τ((a d_k)*(a d_k))≤δ_k⁻¹ν(a*a) para a∈nν. Como a d_k→a fortemente e nν é fracamente denso, obtém-se a densidade usual de nτ. Estes cálculos e a transferência de limites ainda são lemas a formalizar, não resultados novos certificados por esta nota. A fidelidade pode ser tratada pela fidelidade de ν e imagem densa de sε. Só DEPOIS da tracialidade cabe pagar o campo de semifinitude por minorantes do contrato do traço.

6. **Onde entra Tomita/KMS de verdade.** A norma atual já consome o J original pela ação direita. Isso não demonstra que o limite é traço. O fornecedor scalarTomitaImaginaryPower_core_conjugation identifica a ação das potências do Tomita original com Ad λ_t, e regularPositiveGenerator_imaginaryPower identifica λ_t com h^{it}. A ponte de perturbação ainda necessária é a especialização

   σ_t^τ(X)=h^(−it) σ_t^ν(X) h^(it),

   para o τ efetivamente construído acima; então os fatores cancelam e o grupo modular de τ é trivial. A literatura fornece precisamente a perturbação por operador positivo afiliado ao centralizador modular, com construção crescente e fórmula do grupo modular: Hiai, §9, Lema 9.1, Proposição 9.3, Teorema 9.4 e aplicação 9.9. Essa é a etapa modular/KMS, não mera invariância. Aqui ela permanece uma obrigação de transporte formal para os objetos concretos, não um axioma admitido. [Fonte primária](https://arxiv.org/pdf/2004.02383).

   Alternativamente, provar diretamente τ(a*a)=τ(aa*) para todo a∈N, incluindo valores infinitos, exige a correspondente identidade de formas e um domínio/core que justifique sua extensão. A fórmula de norma isolada não fornece essa identidade. Não é necessário reconstruir GNS nem exigir uma equivalência geral de preduais; também não basta renomear a covariância já paga como o teorema de perturbação.

[OPEN] Menor sequência restante: recuperação ENNReal por médias; comutação média/corte; comparação e leis dos pesos em todos os positivos; construção e densidade do domínio do limite; identidade de perturbação modular/tracialidade. A consulta não acrescenta requisitos a gate/métrica, não modifica a errata de semifinitude de ν e não altera os pareceres entregues.


[REAL — fornecedores locais consultados; leitura, não recompilação nesta nota]

- [scalarOrbit_right_average_norm_le](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarRightAverage.lean:56>), [scalarOrbit_right_average_tendsto](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarRightAverage.lean:63>), [scalarWeight_right_average_le](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarRightAverage.lean:70>) — SHA256 `64d49e1de18504e9e66e7559f48df9f6811c80821524b85324ee0a1305793aed`.
- [HasFiniteDualSquare.left_mul](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350DualSemifiniteIdeal.lean:51>), [regularAverage_hasFiniteDualSquare](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350DualSemifiniteIdeal.lean:108>) — SHA256 `63c88763eaa1c837ed0a28057d044a7627e57f993f4fcc4c7bddf44dcea07cbe`.
- [regularAverage_apply](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350RegularApproximation.lean:41>), [regularAverage_tendsto_identity](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350RegularApproximation.lean:68>) — SHA256 `d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44`.
- [finiteDualLeftIdeal_le_scalarWeight](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarWeightDomain.lean:50>) — SHA256 `e83ada9b5abbf2c179c28b03d3c020be83861681ba3ae450999c1c64ea8e2f0f`.
- [dualQuadraticIntegrand_measurable](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350DualWeightForm.lean:47>), [dualQuadraticIntegral](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350DualWeightForm.lean:62>) — SHA256 `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`.
- [scalarWeightOrbit_rightRegularization_tendsto](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarWeightCompletion.lean:16>) — SHA256 `b8a87c9b03f233e8e0a04a92aaa7c6cd4499fb8421746902f2b0b90feb883d7c`.
- [scalarDualWeight](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarDualWeight.lean:15>), [scalarDualWeight_normal](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ScalarDualWeight.lean:46>) — SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`.
- [PositiveCoreInput.conjugate](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350DualFixedWeightLaws.lean:38>) — SHA256 `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`.
- [vonNeumann_exists_positive_isLUB](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350RegularNormality.lean:52>), [vonNeumann_isLUB_coe](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350RegularNormality.lean:71>) — SHA256 `bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a`.
- [scalarTomitaImaginaryPower_core_conjugation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351ScalarImaginaryCoreAction.lean:47>) — SHA256 `db4109dceeab1e948d7d5e664e8d76b347c719b00e62031761aaf5e924862a83`.
- [regularSpectralCoordinates_character](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularImaginaryPowers.lean:65>), [regularPositiveGenerator_imaginaryPower](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularImaginaryPowers.lean:90>) — SHA256 `066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a`.
- [regularInverseGeneratorCutoff_cfc](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351InverseCutoffCFC.lean:62>), [regularInverseGeneratorCutoff_sqrt_right](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351InverseCutoffCFC.lean:125>) — SHA256 `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`.
- [scalarWeight_right_perturbed_norm](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351PerturbedWeightNorm.lean:12>), [scalarWeight_inverseCutoff_perturbed_norm](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351PerturbedWeightNorm.lean:37>) — SHA256 `9b4edeb94844ded88ec595b50160936d42e34637f4432493d02894dd7731bab9`.
- [lintegral_liminf_le](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\Lebesgue\Add.lean:214>) — SHA256 `e330b98eb9686290a3257802c38ad756150b110deb39fe32c66da46cf1211e4f`.
