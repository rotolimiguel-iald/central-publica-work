# Consulta A1 — potências imaginárias do Tomita do mesmo peso

Data: 2026-09-14T10:01:51.072672-03:00. Estatuto: **[DERIVED — proposta matemática, sem novo Lean]**.

A rota amortecida proposta nesta continuação é válida e mais econômica que começar por uma nova descrição completa de autovetores do GNS. Ela usa o resolvente do **Δν=scalarTomitaSquare P=S†S original**, constrói suas fases por CFC contínuo e permite transportar a escala matricial já demonstrada. O passo seguinte pode identificar a ação de Δν^{it} em toda π(N), sem predual abstrato novo, sem Stone/PVM geral e sem assumir Jπ(N)J=π(N)'. A igualdade literal entre duas unitárias implementadoras merece um enunciado separado; igualdade de suas conjugações não a prova.

Nenhum módulo foi compilado, criado ou modificado nesta consulta. Foram lidos fornecedores delimitados, com pins no JSON acompanhante. Builds anteriores são herdados; esta leitura não é uma nova auditoria de axiomas. A1(b) permanece **[OPEN]**.

## 1. Objetos e sinal

Escrevo Γ(a)=scalarWeightGNSEmbedding P a, Hν=ScalarGNSHilbert P, J=scalarTomitaPolarFactor P, Δ=scalarTomitaSquare P e T=scalarTomitaResolvent P. Uso λ_t=regularUnitary P t para a unitária do core; ela atua em **H_reg**, enquanto L_t=πν(λ_t) e R_t=regularRightGNS P t atuam em **Hν**.

As definições e os entrelaçamentos existentes dão

\[
R_t\Gamma(a)=\Gamma(a\lambda_t),\qquad
V_t:=L_tR_{-t}=L_tJ L_tJ^{-1},\qquad
V_t\Gamma(a)=\Gamma(\lambda_ta\lambda_{-t}).
\]

O sinal na direita é **−t**. `characterPhase s t=exp(−i s t)`, enquanto `modularPhase t c=exp(i t c)`. Na realização ambiental L²(s,L²(x,H_torre)), o produto da ação esquerda de λ_t com a direita de λ_{−t} cancela o caráter externo e as translações internas: resta a amplificação, duas vezes, de `modularFlowCLM P t`. Esta última identidade de operadores é uma consequência algébrica a empacotar; não foi localizada como um teorema pronto. Não troca Hν pelo Hilbert da torre.

Para unidades matriciais, r_ij=w_i/w_j>0, ω_ij=log r_ij; o fluxo candidato na base é **+it log r_ij**. A translação s−ω_ij da fórmula `scalarOrbit_right_matrixUnit` é compatível com esse sinal, não o oposto.

V_t já tem os fornecedores de grupo, unitariedade, continuidade forte e implementação da ação. Essas propriedades, isoladas, ainda não o identificam com Δ^{it}.

## 2. Construção amortecida: prova e condições realmente necessárias

Assuma no lema genérico H complexo completo, T limitado, 0≤T≤1, `Injective T` e `Injective (1−T)`. Na aplicação, T é o resolvente original. A primeira injetividade está pronta; a segunda segue de JTJ^{-1}=1−T e da primeira, sem gap.

Ponha b(x)=x(1−x), K=b(T). K≥0, é injetivo e tem imagem densa: o produto dos dois fatores injetivos é injetivo; K auto-adjunto implica Ran(K)^⊥=ker K. **Injetividade de um operador limitado arbitrário, sozinha, não implica imagem densa.**

Em 0<x<1, defina

\[
g_t(x)=b(x)\exp\bigl(it\log((1-x)/x)\bigr),\qquad g_t(0)=g_t(1)=0.
\]

|g_t(x)|=b(x) prova a continuidade nas duas extremidades, apesar de a fase sem amortecimento não ter limite ali. Para reutilizar literalmente `real_cfc_intertwines`, que exige **Continuous f em ℝ**, estenda Re g_t e Im g_t continuamente por zero fora [0,1]; não passe apenas uma prova `ContinuousOn` a essa API. Construa C_t pela CFC complexa, ou pela soma da CFC real de Re g_t e i vezes a de Im g_t.

As identidades pontuais no espectro dão

\[
C_t^*C_t=C_tC_t^*=K^2,\quad C_t^*=C_{-t},\quad
C_sC_t=K C_{s+t},\quad C_0=K.
\]

Aqui é necessário registrar **também C_t C_t^*=K²**, ou normalidade de C_t: dela vem ker C_t*=0 e a imagem densa de C_t. Assim `boundedInjectivePolar C_t hi hd` se aplica efetivamente H→H. Seu módulo é √(C_t*C_t)=K por positividade e unicidade da raiz. A identidade fornecida é

\[
U_tK=C_t.
\]

O argumento não usa K^{-1} limitado. A unicidade por Ran K densa dá comutação de U_t com funções contínuas de T. A igualdade de grupo é verificada sobre Ran K² usando C_sC_t=K C_{s+t}, e estendida por densidade. U_0=I e U_t*=U_{−t} seguem do mesmo modo. Continuidade forte: t↦g_t é contínua uniformemente em [0,1] (controle b nas pontas e continuidade uniforme no interior); logo t↦C_t é contínua em norma. U_tK=C_t dá continuidade em Ran K, estendida a H por ||U_t||=1. Não resulta continuidade de U em norma.

**Identidade intrínseca com Δ.** T=(I+Δ)^{-1} não foi escolhido por covariância: é o resolvente do S†S previamente construído, com igualdade de grafos. A igualdade U_t b(T)=g_t(T), com b(T) de imagem densa, caracteriza unicamente a fase funcional exp(it log Δ). Isso fornece uma definição concreta e verificável de Δ^{it} via seu resolvente; não basta definir U como um grupo qualquer que preserve ν e atribuir-lhe o nome. Uma API geral de potências imaginárias de LinearPMap não foi localizada nesta busca limitada; a definição nova deve vir acompanhada dessa caracterização, grupo e continuidade.

## 3. Escala: o amortecimento também precisa ser transportado

A fonte existente já prova T R_ij=R_ij Q_r, com

\[
D_r=rI+(1-r)T,\qquad Q_r=T D_r^{-1},\qquad 0\le Q_r\le I.
\]

`scaledResolventDenominator_positive` paga a inversa **limitada de D_r**, para r>0. Isso não é inversão de R_ij, K, da raiz ou de Δ. Use as funções contínuas das duas partes de g_t em `real_cfc_intertwines`. Resultam K R_ij=R_ij b(Q_r) e C_t R_ij=R_ij g_t(Q_r).

Com E_r=r D_r^{-2}, as identidades escalares exatas são

\[
b(Q_r)=K E_r,\qquad g_t(Q_r)=r^{it} C_t E_r.
\]

E_r é limitado, invertível, comuta com T e com U_t; b(Q_r) tem imagem densa. Portanto

\[
U_t R_{ij} b(Q_r)=C_tR_{ij}
=R_{ij}g_t(Q_r)
=r^{it}R_{ij}U_t b(Q_r).
\]

A densidade cancela **à direita** e produz U_t R_ij=r_ij^{it}R_ij U_t. Não há que refazer root scaling; reaproveita-se seu fornecedor anterior de resolvente. Um cancelamento formal de b(T) por uma suposta inversa limitada seria inválido.

## 4. Do transporte à esquerda, e daí a TODO core

O fornecedor JTJ^{-1}=1−T, combinado com

\[
\overline{g_t(1-x)}=g_t(x),\quad b(1-x)=b(x),
\]

permite provar **JU_tJ^{-1}=U_t**, não U_{−t}: a antiunitariedade conjuga i e a troca T↔1−T inverte o log; os dois sinais se cancelam. Falta empacotar o transporte da CFC real por conjugação antiunitária. Pode-se construir o homomorfismo de *-álgebras sobre ℝ e usar `StarAlgHom.map_cfc`, ou adaptar a indução real já usada em `real_cfc_intertwines`. `antiunitaryConjugate_sqrt` sozinho não é uma API de todas as funções contínuas.

As identidades prontas com o **J original** são

\[
J\pi(e_{ij})J^{-1}=\sqrt{r_{ji}}R_{ji},\qquad
J\pi(\lambda_s)J^{-1}=R_{-s}.
\]

Consequentemente, a escala direita recém-obtida dá

\[
U_t\pi(e_{ij})U_{-t}=r_{ij}^{it}\pi(e_{ij}).
\]

Também U_t comuta com R_s pela comutação já provada de T com R_s e pela densidade de Ran K. Conjugando por J, U_t comuta com π(λ_s). Esses são precisamente os dois tipos de geradores da ação candidata.

Para passar a toda base, use `represented_levelExpectation_strong_tendsto`: os aproximantes matriciais possuem a cota já provada 4||a||. Para passar de base+λ a toda N, ponha W_t=V_{−t}U_t. A igualdade das ações nos geradores significa que W_t comuta com suas representações. Use `scalarGNS_commutation_from_generators`; a hipótese de geração é efetivamente descarregada nesse fornecedor. Conclui-se

\[
\boxed{\ U_t\pi(a)U_{-t}=\pi(\lambda_t a\lambda_{-t})\quad(a\in N).\ }
\]

**Este é o consumidor modular concreto:** depois de U estar caracterizado como Δν^{it}, a equação identifica σν com Ad λ na representação fiel do mesmo peso. Não depende de completar o predual, provar primeiro a inclusão inversa dos comutantes, assumir TT/KMS, nem construir um segundo GNS. Os lemas novos acima ainda precisam de provas Lean; esta nota não os aceita como já compilados.

## 5. Igualdade literal de implementadores e alternativa por autovetores

A caixa anterior não prova automaticamente U_t=V_t: ela só dá V_{−t}U_t∈π(N)'. Se o consumidor exigir a igualdade **de unitárias no Hν**, além da igualdade da automorfia, resta fixar essa ambiguidade em vetores cujas órbitas à esquerda sejam totais. Não usar Γ(1): a unidade não pertence ao ideal escalar finito.

Uma ponte concreta, sem reconstruir GNS, é a seguinte **[DERIVED, ainda a formalizar]**. Tome X_h=regularAverage P h, h>0. Primeiro prove a identidade integral forte da média direita com h^{-1}∫₀ʰ R_s ds e seu adjunto; daí obtenha o par `ScalarRightAdjointPair` com vetores Γ(X_h), Γ(X_h*). A igualdade X_h*=λ_{−h}X_h fornece sua finitude, por mudança de variável no intervalo; não presumir que o ideal esquerdo é fechado por estrela.

Então b_h=X_h*X_h está no ideal e é positivo. A multiplicação direita por b_h é Q_h=R_h R_h* (atenção à ordem da antirrepresentação direita), tem vetor ξ_h=Γ(b_h) e é auto-adjunta. `scalarRightAdjointPair_maximal` dá Fξ_h=ξ_h; a extensão da estrela pelo S original dá Sξ_h=ξ_h. Logo Δξ_h=ξ_h. Pela raiz positiva e S=JB, Jξ_h=ξ_h. As médias R_h e seus adjuntos convergem fortemente a I, logo Q_h→I e Q_hΓ(a)=π(a)ξ_h mostra que as órbitas π(N)ξ_h, tomadas conjuntamente, são totais.

Pelo CFC do resolvente, U_t fixa ξ_h (Tξ_h=ξ_h/2); V_t também fixa, pois b_h comuta com λ_t. Como W_t comuta com π(N), a totalidade anterior implica W_t=I. Assim se obtém a igualdade literal U_t=L_tR_{−t} **sem um campo de cyclicidade novo**.

A rota de autovetores é, portanto, viável mas não é a primeira recomendação após a proposta amortecida. Partindo de ξ_h, palavras nos R_ij e R_s ficam em D(Δ) e são autovetores com autovalor positivo produto dos r_ij, pelas leis completas de domínio já prontas. Sua totalidade pode ser provada usando Jξ_h=ξ_h, as fórmulas Jπ(gerador)J e geração concreta; não decorre simplesmente de `localEigenvectors_total`, cujo espaço é TowerHilbert. Obtida totalidade, seu span é core de Δ: aproximar (I+Δ)x por y_n no span e usar x_n=T y_n; então Δx_n=y_n−x_n. Nenhuma passagem de mera densidade Hilbert para densidade de gráfico é presumida.

## 6. Próximos enunciados propostos, em ordem de consumo

Nomes abaixo são **sugestões, não declarações existentes**:

1. `dampedResolventPhase_unitary`: sob 0≤T≤1 e injetividades dos extremos, construir U_t com U_t b(T)=g_t(T), grupo e continuidade forte.
2. `dampedResolventPhase_scaled_intertwining`: TR=RQ_r ⇒ U_tR=exp(it log r) RU_t. Registrar E_r e a densidade usada no cancelamento.
3. `dampedResolventPhase_antiunitary_flip`: JTJ^{-1}=1−T ⇒ JU_tJ^{-1}=U_t; nenhuma involução presumida antes de aplicar o J concreto.
4. `scalarDualWeight_modular_covariance`: especializar T/J originais e consumir os geradores/limites acima para a equação em toda π(N). Esse é o próximo pagamento de `regular_dual_weight_modular_implementation`.
5. Somente se a interface exigir a unitária literal: `regularAverage_right_adjoint_pair` → `regularAverageSquare_modular_fixed_total` → U_t=π(λ_t)R_{−t}.

O passo 4 identifica o fluxo modular do S†S do peso completo. Um teorema separado de condição KMS em faixa, uma perturbação que construa o traço e seu consumo A1 não foram demonstrados nesta consulta. Não há promoção de gate nem alegação de A1(b) pago.

## 7. Fornecedores locais efetivamente lidos

Nomes qualificados: os V350 abaixo estão em `TGLV350.Regular`, os módulos ModularFlowSpectrum/ModularPower em `ChatgptAudit`. Links trazem a linha exata; o JSON contém enunciados extraídos, caminho e SHA256 completo de cada fonte, além do confronto dos pins herdados quando disponíveis.

| Papel | Declaração e localização |
|---|---|
| Mesmo peso e gráfico original | [scalarClosedTomita_graph_eq_weight](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarWeightTomitaIdentification.lean:58>) |
| Mesmo Δ e resolvente, domínio incluído | [scalarTomitaResolvent_graph](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarTomitaResolvent.lean:45>) |
| Complemento transportado pelo J original | [scalarTomitaPolar_conjugate_resolvent](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarTomitaPolarInvolution.lean:13>) |
| Polar linear de mapa injetivo de imagem densa | [boundedInjectivePolar](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350BoundedInjectivePolar.lean:41>) |
| CFC entre dois operadores, sem inversão do entrelaçador | [real_cfc_intertwines](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350PositiveRootIntertwining.lean:15>) |
| Escala matricial já paga | [matrixUnit_resolvent_right_scaling](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350MatrixUnitResolventScaling.lean:41>) |
| Denominador estritamente positivo | [scaledResolventDenominator_positive](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScaledPositiveResolvent.lean:27>) |
| Resolvente comuta com direita regular | [scalarTomitaResolvent_regular_right_commutes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarRegularRightPolar.lean:14>) |
| J original troca esquerda/direita matricial | [matrixUnit_polar_conjugate_generator](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350MatrixUnitPolarCommutation.lean:39>) |
| J original troca esquerda/direita regular | [scalarTomitaPolar_regular_generator](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarRegularPolarCommutation.lean:50>) |
| Níveis finitos aproximam toda base no mesmo GNS | [represented_levelExpectation_strong_tendsto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350LevelExpectationStrongLimit.lean:44>) |
| Geração concreta, hgen descarregada | [scalarGNS_commutation_from_generators](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarGNSGeneratorTransport.lean:68>) |
| Sinal da covariância regular | [regular_covariance_on_factor](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350RegularTowerRepresentation.lean:87>) |
| Autovetores totais somente no Hilbert da torre | [localEigenvectors_total](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/ModularFlowSpectrum.lean:98>) |
| Potências imaginárias existentes somente da torre | [deltaImaginaryPower_spectral](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/ModularPower.lean:30>) |

APIs Mathlib locais consultadas: [cfc_mul](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean:463>), [cfc_comp](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean:602>), [StarAlgHom.map_cfc](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unique.lean:486>), [norm_cfc_le](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Isometric.lean:103>), [orthogonal_range](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean:198>). São fornecedores de álgebra/CFC/densidade, não um teorema pronto de identificação modular.

Pins centrais, relidos nesta consulta:

| Fonte | SHA256 |
|---|---|
| `V350ScalarTomitaResolvent.lean` | `50e9437f0a572187103933b7b4847b82599da0a687e439a3b7ab48735e2c3127` |
| `V350ScalarTomitaPolarInvolution.lean` | `b7cecd7d64b40a7de3bb5cb81ad90feeed1883943c0e566442eeb12abc83984d` |
| `V350BoundedInjectivePolar.lean` | `bd16c6727b6738718ba8e4c2c5009aef6c86d206240d6bead093f6ff65239b76` |
| `V350PositiveRootIntertwining.lean` | `f357246ac96d1d98fc1376238be4ca039f425d2782dd23d909ac5cdd3d1afaa5` |
| `V350MatrixUnitResolventScaling.lean` | `f6b1271a8612a0695581ffc52afb45277ed0468bf941b42fcc8c8c3086877911` |

## 8. Literatura e alcance

**[KNOWN]** Hiai, *Lectures on Selected Topics in von Neumann Algebras*, teoremas 10.12–10.13 e 10.15(1), descreve o peso dual e a identificação σ^{φ̃}_t=Ad λ_t no produto cruzado pela ação modular. O texto confirma o sinal e separa esse resultado da construção posterior do traço por perturbação. Aplicar diretamente esse teorema aqui exigiria identificar seus objetos e hipóteses com o peso e a representação concretos; a mera palavra “dual” não faz a aplicação. [Fonte primária consultada](https://arxiv.org/pdf/2004.02383), pp. 95–100 na paginação impressa, especialmente 99–100 para o teorema 10.15.

A proposta acima usa os fornecedores locais para evitar construir a interface abstrata inteira desse teorema. Não houve busca exaustiva no acervo, revisão científica geral, novo axioma, execução de um.py, compilação ou escrita fora de revisao. A construção amortecida e os próximos enunciados permanecem **[DERIVED/OPEN — não compilados]**; os fornecedores têm o estatuto de leitura e proveniência explicitado no JSON.
