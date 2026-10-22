# Potências imaginárias e invariância modular — 05/09/2026

## Resultado verificado

**[REAL — Lean] Foi construído um grupo unitário fortemente contínuo U_t no próprio `TowerHilbert P`, com a caracterização espectral λ↦exp(it log λ) numa família total de autovetores do Δ já construído. Sua conjugação preserva `theFactorObject P` e o estado `omegaState P`.**

O objeto `deltaImaginaryPower P t` reúne essa construção específica da potência imaginária Δ^{it}. A ligação a Δ é verificada por `delta_eigenvector`, `modularFlow_eigenvector`, `localEigenvectors_total` e `modularFlow_spectral_unique`. Não se supõe um grupo modular como campo de um contrato.

O trabalho não implementa uma biblioteca geral de cálculo funcional para todos os operadores não limitados. Ele constrói e caracteriza o multiplicador espectral específico necessário nesta torre de estados produto.

## 1. Fórmula local e coerência

No andar N, sejam w_i=`towerW P N i`>0. Defina

\[
(U_{t,N}a)_{ij}
=\exp\bigl(it(\log w_i-\log w_j)\bigr)a_{ij}.
\]

**[REAL] `ModularFlowLevel.lean`** verifica linearidade, U_{0,N}=I, U_{s,N}U_{t,N}=U_{s+t,N}, preservação da norma GNS e continuidade em t. Como a fase tem módulo 1, a soma ponderada dos módulos quadrados das entradas permanece igual.

Na inclusão a↦a⊗I, apenas as entradas com o mesmo índice no novo sítio podem ser não nulas. Nessas entradas, o termo adicional no logaritmo do peso cancela entre linha e coluna. O teorema `flowLevel_step` verifica essa conta; `flowLevel_push` a transporta a qualquer inclusão N≤M.

**[REAL] `ModularFlowPre.lean`** usa essa compatibilidade para definir `flowPre` no quociente que constitui o colimite. São verificadas boa definição, linearidade, isometria e lei de grupo. A consistência entre representantes é parte da prova.

## 2. Extensão unitária e continuidade forte

**[REAL] `ModularFlowHilbert.lean`.** A isometria fornece continuidade uniforme, permitindo estender cada U_t ao completamento H. A extensão concorda com a ação local. As identidades lineares, de norma e de grupo são transportadas por densidade. U_{−t} é a inversa, portanto `modularFlowUnitary P t` é uma equivalência linear isométrica de H sobre H.

Para a continuidade forte, fixe x∈H e um instante s. Escolha z local próximo de x. A continuidade local controla U_tz−U_sz, enquanto a isometria fornece, uniformemente em t,

\[
\|U_tx-U_sx\|
\le 2\|x-z\|+\|U_tz-U_sz\|.
\]

Escolhendo cada parcela com tolerância ε/3, obtém-se U_tx→U_sx quando t→s. O teorema `modularFlow_strongly_continuous` formaliza essa passagem para TODO x∈H. Não se presume continuidade em norma de operadores.

## 3. Ligação espectral ao Δ existente

**[REAL] `ModularFlowSpectrum.lean`.** Para cada unidade matricial E_ij no andar N, defina e_{Nij}=[E_ij]∈H e λ_{Nij}=w_i/w_j>0. Foram provadas as duas identidades com os objetos exatos:

\[
\Delta e_{Nij}=\lambda_{Nij}e_{Nij},\qquad
U_te_{Nij}=\exp(it\log\lambda_{Nij})e_{Nij}.
\]

A primeira usa `square_local`, que já ligava Δ ao `towerDeltaLevel`. A segunda usa a fórmula de fluxo e a identidade log(w_i/w_j)=log w_i−log w_j, com positividade dos pesos verificada.

Todo vetor de um andar é soma finita de unidades matriciais. Como os andares têm união densa, o span da família e_{Nij} é denso em H. Isso está em `localEigenvectors_total`. Não é preciso declarar que a coleção de unidades de TODOS os andares seja uma base ortonormal global.

`modularFlow_spectral_unique` verifica: se um operador contínuo linear T age em cada e_{Nij} pelo multiplicador exp(it log λ_{Nij}), então T=U_t em todo H. A prova usa linearidade no span e continuidade na passagem ao fecho.

Assim, a notação Δ^{it} nesta bancada corresponde ao único multiplicador espectral limitado com essa ação na família total de autovetores de Δ. **[REAL] `ModularPower.lean`** oferece o objeto `deltaImaginaryPower` e reúne sua caracterização espectral, a lei de grupo e a continuidade forte.

[OPEN — escopo geral] Não há aqui uma API geral de medida espectral, uma implementação geral de f(Δ) para toda função boreliana, ou um teorema genérico de Stone. A potência imaginária específica está construída e caracterizada; esses desenvolvimentos gerais não foram anunciados como prontos.

## 4. Invariância da álgebra efetiva

**[REAL] `ModularFlowAlgebra.lean`.** A identidade de fases

\[
e^{it(a-b)}e^{it(b-c)}=e^{it(a-c)}
\]

prova a multiplicatividade de U_{t,N} na álgebra matricial. No colimite, ela fornece a relação com a multiplicação à esquerda. No completamento:

\[
U_t\pi(a)x=\pi(U_{t,N}a)U_tx,
\qquad U_t\pi(a)U_t^{-1}=\pi(U_{t,N}a).
\]

A conjugação unitária é um automorfismo que preserva produto e adjunto dos operadores limitados. Ela transporta a imagem da torre sobre si mesma. O lema `centralizer_transport` transporta, então, seu centralizador e o centralizador deste. Como o fator da casa é definido pelo duplo centralizador, segue

\[
\boxed{U_t M U_t^{-1}=M,\qquad M=\operatorname{theFactorObject}(P).}
\]

O teorema `modularConjugation_preserves_factor` é a equivalência de pertinência que expressa essa igualdade. A invariância foi construída no bicomutante real do projeto; não foi importada como hipótese de uma estrutura.

## 5. Vácuo e estado

**[REAL] `ModularPower.lean`.** A identidade é fixa no andar, pois suas entradas fora da diagonal são zero e a fase diagonal é 1. Portanto U_tΩ=Ω. Pela unitariedade,

\[
\omega(U_tAU_t^{-1})=\omega(A)
\]

para todo operador limitado A em H. Isso foi provado em `modularConjugation_preserves_state`. A invariância não foi inferida somente da normalização ω(I)=1: usa a ação explícita e o vetor Ω fixo.

## 6. Estado após esta continuação

| Frente | Estatuto |
|---|---|
| S fechado, JS positivo auto-adjunto, Δ=(JS)²=S†S | [REAL — Lean], etapas anteriores |
| Potência imaginária pelo multiplicador espectral numa família total de autovetores de Δ | [REAL — Lean] |
| Grupo unitário, inversa U_{−t}, continuidade forte | [REAL — Lean] |
| Conjugação local e invariância do bicomutante M | [REAL — Lean] |
| Ω fixo e estado preservado | [REAL — Lean] |
| Biblioteca geral de cálculo funcional não limitado | [OPEN] |
| Construção interna da esperança condicional para as subálgebras pretendidas | [OPEN]; a invariância de cada subálgebra precisa ser demonstrada |
| Rede geométrica, dimensão, assinatura e escala métrica | [OPEN] |
| Realização física das hipóteses gravitacionais | [OPEN] |

O parâmetro modular real t não foi identificado automaticamente com tempo próprio, aceleração ou uma coordenada de espaço-tempo. Essas identificações exigem pontes geométricas adicionais, que não são consequências apenas da existência do grupo.

## Verificação e preservação

Ordem de compilação: `ModularFlowLevel`, `ModularFlowPre`, `ModularFlowHilbert`, `ModularFlowAlgebra`, `ModularFlowSpectrum`, `ModularPower`, por `verify_stage.ps1 -Module NOME`. Os resultados principais dos fontes finais imprimiram apenas `propext`, `Classical.choice` e `Quot.sound`. Os logs datados e o registro consolidado identificam fontes e objetos compilados por hashes lidos do disco.

Foram usadas as dependências compiladas existentes, abertas em leitura. Não houve reconstrução integral dessas dependências, rito integral do `um.py`, aprovação adversarial independente, selo novo ou mudança do gate. As tentativas recusadas permanecem no histórico e não são a verificação final.

Todas as escritas ficaram na pasta `Chatgpt`, com backups byte a byte antes dos adendos às memórias da bancada. Atlas, memórias canônicas e demais originais não foram editados. O resultado é matemático e formal para a torre especificada; não estabelece confirmação física de gravidade quântica.
