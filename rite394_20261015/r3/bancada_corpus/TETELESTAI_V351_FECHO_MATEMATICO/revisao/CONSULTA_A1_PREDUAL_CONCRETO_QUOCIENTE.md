# Consulta A1 — cone vetorial concreto, quociente e consumidor

2026-09-14T09:22:15.633699-03:00

**[DERIVED] A construção proposta é válida e paga uma ponte efetiva de avaliação dual. O quociente, sozinho, não certifica cobertura de todo o predual.** Classicamente séries vetoriais quadrado-somáveis representam os funcionais normais positivos de uma álgebra de von Neumann concreta. A questão restante é qual caracterização foi efetivamente demonstrada no kernel, não uma alegação de impossibilidade ou de que esse modelo seja matematicamente menor.

Consulta somente leitura de fontes/biblioteca; nenhum Lean escrito ou compilado, nenhuma alteração de memória ou de parecer anterior.

## Construção econômica e independência

Seja H=TowerHilbert P e M=theFactorObject P. Para v:ℕ→H com Σ‖v_k‖²<∞, ponha

    Ψ_v(x)=Σ_k ⟨v_k,x v_k⟩,  x∈M.

Cada termo é um funcional complexo linear em x, com norma ≤‖v_k‖². A série converge em norma no espaço de funcionais contínuos; não se precisa pressupor CompleteSpace do subtipo M para a completude de seu dual. Temos Ψ_v positivo, Ψ_v(1)=Σ‖v_k‖² e ‖Ψ_v‖≤Σ‖v_k‖². A normalidade por ordem no mesmo M pode ser provada diretamente: supremo interno positivo dirigido → limite forte ambiente existente → convergência dos termos vetoriais → troca de supremo crescente e soma. Isto dá **série ⇒ normalidade por ordem** sem usar o converso.

Identificar v~w quando Ψ_v=Ψ_w em todo M é correto. Formalmente, pode ser mais econômico representar o cone como o subtipo dos funcionais contínuos que admitem tal representação; sua igualdade já é extensional. É a mesma informação do quociente, sem transportar toda operação por Quotient.lift. Adição de representações usa intercalação/união enumerável, não v_k+w_k (que criaria termos cruzados); escala r≥0 usa √r v_k. Não confundir esse cone com um espaço vetorial complexo.

Com os D_n(A) já aprovados, defina sobre esse cone C_M:

    m_A(Ψ)=sup_n ofReal(Re Ψ(D_n(A))).

A definição independe do representante **imediatamente**, pois v~w implica igualdade em cada D_n∈M. A troca de supremo/soma prova depois a identidade de ligação

    m_A(Ψ_v)=Σ_k q_A(testVector v_k).

Usam-se positividade de D_n e seu crescimento. Todas as somas dessa última igualdade são em ENNReal e permitem infinito; a somabilidade quadrática só controla Ψ_v nos operadores limitados. Não assumir Σq_A(testVector v_k)<∞. A soma finita→supremo dá também extensionalidade e independência de qualquer escolha de aproximantes que represente a mesma forma.

Para realmente obter um **valor positivo estendido**, provar também no argumento Ψ: aditividade, homogeneidade NNReal (inclusive 0·∞), monotonicidade e semicontinuidade inferior. Adição e escala vêm do supremo da mesma sequência crescente de avaliações; cada Ψ↦ofReal(Re Ψ(D_n)) é contínua para a topologia de avaliação em M, logo seu supremo é semicontínuo inferior, também para a norma herdada do dual. Isso fornece a estrutura no cone C_M, sem presumir que C_M já seja todo M_*⁺. A fidelidade relevante é da família A↦m_A: m_A identicamente zero em C_M implica A=0; não se afirma fidelidade de cada Ψ individual.

## O que se pode chamar de predual — e a ponte que falta

Há três estatutos distintos:

1. **Cone concreto C_M de funcionais representáveis**, com normalidade por ordem demonstrada na direção acima: objeto legítimo e suficiente para construir m_A e os consumidores explicitados abaixo. Não declarar cobertura ainda.
2. **Todos os funcionais positivos normais por ordem de M.** Para ligar a essa interface, basta o converso restrito ao mesmo M:

       Ψ positivo, complexo linear, limitado e normal para supremos positivos
       dirigidos não vazios ⇒ ∃v, Σ‖v_k‖²<∞ e Ψ(x)=Σ⟨v_k,xv_k⟩ (∀x∈M).

   Este é o lema de cobertura realmente faltante; não exige a equivalência geral VonNeumannAlgebra↔WStarAlgebra nem outro GNS. Normalidade somente sequencial não deve substituir silenciosamente a normalidade para redes no enunciado de entrada.
3. **Predual de Banach definido por quociente.** Um quociente apenas de sequências positivas ainda não é esse objeto. Uma rota suficiente é construir um espaço linear complexo de funcionais de séries/operadores de classe traço, o quociente pelo anulador de M, sua norma e completude, provar que a avaliação identifica isometricamente seu dual com M e identificar o cone positivo do quociente com C_M. Essa rota pode dispensar de saída o lema order-normal⇒série se o consumidor só usa o predual assim construído; a identificação de dualidade/positividade não pode ser dispensada por escolher a palavra “predual”. Para este marco ela parece mais cara que manter C_M e um consumidor explícito.

[KNOWN] A distinção entre predual, normalidade e dualidade de Banach é a convencional: [Hiai, §§1.1–1.3](https://arxiv.org/pdf/2004.02383) define o predual pelas formas lineares σ-fracamente contínuas e enuncia a caracterização positiva por normalidade. Essa literatura não é prova Lean da cobertura. Não é necessário reconstruir tudo isso para uma igualdade que só consome o estado vetorial Ω; é necessário fornecer a ponte escolhida antes de aplicar um teorema cujo domínio seja **todo** M_*⁺.

A cobertura por séries está enunciada e demonstrada explicitamente em [Rasmus S. Bryder, Theorem 2.41, pp. 50–51](https://web.math.ku.dk/~musat/Injective_and_semidiscrete_von_Neumann_algebras_final.pdf#page=67): funcional positivo normal ⇔ ultrafracamente contínuo ⇔ série de funcionais vetoriais com soma dos quadrados das normas finita, no mesmo H, sem assumir H separável. A convenção de produto interno da referência é linear na primeira variável; a fórmula desta consulta foi escrita na convenção Lean. Isso identifica precisamente a ponte clássica disponível, não um novo alvo Lean aceito.

## Consumidor real para A1, sem impor WStar ao contrato

O [contrato RegularCoreTraceData](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351RegularCoreTraceContract.lean:43>) recebe uma função no cone positivo do core e suas leis; não contém um campo WStar/predual. Não há requisito intrínseco novo de equivalência abstrata. A identificação predual pertence à rota escolhida em LACUNAS_A1, não substitui a produção final de τ.

O próximo termo útil é uma versão concreta da média dual T(A), avaliada em C_M, com:

- m_A(ω_Ω)=ν(A), usando a representação de um só vetor (demais termos zero) e a [igualdade escalar existente](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351ExtendedBaseDualWeight.lean:48>);
- zero, soma, escala, ordem, fidelidade e normalidade no input A, transportadas das formas, com valores infinitos preservados;
- m_(ι(b)*Aι(b))(Ψ)=m_A(Ψ_b), com Ψ_b(x)=Ψ(b*xb), representado pela sequência b v_k;
- output limitado q_A=forma de fibre(D) ⇒ m_A(Ψ)=ofReal(Re Ψ(D)). Isso liga o ideal fortemente denso de quadrados com outputs limitados à semifinitude operatorial concreta usada; não depende de I=nν.

**Cuidado de descida importante:** o levantamento Φ_v(X)=Σ⟨testVector v_k,X testVector v_k⟩ ao core não precisa ser independente do representante v de Ψ em M. Não criar esse mapa no quociente por decreto. A identidade que realmente desce é a **média**:

    dualHaarFactor · ∫ ofReal(Re Φ_v(dualAmbient_s(A))) ds
      = Σ_k q_A(testVector v_k) = m_A(Ψ_v).

Tonelli para termos não negativos e a definição da integral dual dão a primeira igualdade; os aproximantes dão a segunda e portanto a independência após a média. Assim T é ligado à mesma ação dual e ao mesmo fator Haar, não somente a uma nova função com leis semelhantes. Não se deve aplicar Ψ diretamente a dualAmbient_s(A), pois seu domínio é M.

Esta versão concreta paga a identidade ν=φ̄∘T **com esses objetos e esse domínio expressos**. Se o próximo teorema de implementação modular/perturbação for provado diretamente para ela, não se cria uma obrigação universal dispensável. Se for importado com hipótese T:N⁺→M̂⁺ padrão, é indispensável transportar C_M ao cone predual esperado por uma das pontes acima; nenhuma troca de nomes satisfaz essa hipótese. A1(b) como existência de τ permanece [OPEN].

## Fornecedores locais efetivamente encontrados

| Interface lida | Uso e limite |
|---|---|
| [innerSL](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/LinearMap.lean:164>) e [ContinuousLinearMap.apply](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Bilinear.lean:249>) | Formar x↦⟨v,xv⟩ por composição; não são representação de todos os funcionais normais. |
| [Summable.of_norm_bounded](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/Normed/Group/InfiniteSum.lean:111>) | Somar os funcionais em norma usando Σ‖v_k‖². |
| [ContinuousLinearMap.map_tsum](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Topology/Algebra/InfiniteSum/Module.lean:134>) | Avaliação de uma série convergente de funcionais. |
| [ENNReal.tsum_eq_iSup_sum](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Topology/Algebra/InfiniteSum/ENNReal.lean:71>) e [ENNReal.tsum_sigma](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Topology/Algebra/InfiniteSum/ENNReal.lean:81>) | Reduzir troca sup/tsum a somas finitas e reunir séries. Não foi localizado um lema único pronto para toda a ponte. |
| [vonNeumann_exists_positive_isLUB](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350RegularNormality.lean:52>) e [vonNeumann_isLUB_coe](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350RegularNormality.lean:71>) | Passagem de supremo interno a ambiente/limite forte; serve à direção série⇒normal por ordem. |
| [exists_monotone_base_dual_approximation](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351BaseMoreauApproximants.lean:115>) | Fornecedor específico de D_n e supremo em todos os vetores regulares, já revisado. |
| [baseDualWeight_bimodule](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351ExtendedBaseDualWeight.lean:72>) e [baseDualWeight_preserves_internal_isLUB](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351ExtendedBaseDualWeight.lean:98>) | Leis do input a transportar, sem reprová-las. |
| [WStarAlgebra.exists_predual](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/VonNeumannAlgebra/Basic.lean:45>) / [VonNeumannAlgebra](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/VonNeumannAlgebra/Basic.lean:67>) | São definições distintas. O arquivo local declara explicitamente a equivalência como trabalho futuro; não há fornecedor pronto ali para a cobertura. |
| [PiTensorProduct/projectiveSeminorm](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/Normed/Module/PiTensorProduct/ProjectiveSeminorm.lean:58>) | Há infraestrutura parcial de seminorma projetiva; não foi encontrada ali uma identificação completa classe-traço/predual de M. |
| [GNSBridge.boundaryState](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/GNSBridge.lean:86>) / [scalarCutVacuum_inner_action](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarCutVectorFunctional.lean:13>) | Estado matricial finito / funcional específico de corte; não fornecem cobertura do predual da base concreta inteira. |

Busca delimitada a nomes/arquivos de Mathlib/Analysis e fornecedores de ROOT/kernel/TGLExt; não afirma inexistência em todo acervo. O arquivo local InnerProductSpace/Trace trata traço finito-dimensional e não fornece classe traço infinita. Fonte/modelo/locadores e hashes foram registrados no JSON desta consulta. Nenhum fornecedor ausente foi substituído por hipótese nova ou por axiom.

**Recomendação:** construir primeiro C_M como imagem de séries e o lema de descida da média, seguido da avaliação em Ω e das leis necessárias ao próximo consumidor. Isso é avanço consumível. Manter separada a cobertura padrão, necessária apenas quando a assinatura desse consumidor realmente a exigir. Não declarar “todo o predual” antes de provar cobertura ou dualidade concreta.
