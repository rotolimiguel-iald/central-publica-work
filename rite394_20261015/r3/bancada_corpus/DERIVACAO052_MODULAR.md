# Continuação052 — quarto de volta modular no primeiro sítio
[DERIVED — derivação anterior ao fonte; sem resultado de compilação052]

Para um SiteProfile P, seja p=P.w 0, r=2p−1 e ν=log p−log(1−p).
As hipóteses do perfil dão 0<p<1. A monotonicidade estrita do logaritmo
implica ν>0 se e somente se r>0, ν<0 se e somente se r<0, e ν=0 se e
somente se p=1/2. Portanto a hipótese não tracial local p≠1/2 legitima
a divisão por ν e por |ν|, sem impor que o perfil inteiro seja estacionário.

Os operadores usados são sitePauliX P 0 e sitePauliY P 0 da035.
O horizonte é literalmente modularHorizon P t da045. A identidade
adT_modularHorizon e modularConjugation_local no nível N=0 reduzem sua
ação à multiplicação da entrada (i,j) por exp(it(log w_i−log w_j)).
Calculando as quatro entradas das matrizes de Pauli, obtém-se:
σ_t(X)=cos(tν)X−sin(tν)Y; σ_t(Y)=sin(tν)X+cos(tν)Y.
É uma igualdade de operadores da torre, não uma rotação abstrata sem ligação.

No tempo τ=−π/(2ν), tν=−π/2: X passa a Y e Y a −X.
No tempo τ_o=−π/(2|ν|), que é estritamente negativo, a mesma conta dá
X↦sign(r)Y e Y↦−sign(r)X. A divisão em ν>0 e ν<0 e a igualdade dos
sinais de ν e r pagam explicitamente essa orientação.
Assim, para Ω_q(u,v)=r(u0v1−u1v0), a convenção Ω_q(u,Qv) pode dar
|r| vezes o produto euclidiano; essa última ponte pertence a outro módulo.
O quarto no tempo positivo teria a orientação contrária nesta convenção.

Controle tracial: p=1/2 torna ν=0 e a ação modular local em X,Y é a
identidade para todo tempo. Não se aplicam ali os corolários não degenerados.
Q não é a conjugação modular J: a rotação do plano é real linear e tem
quadrado −I; nenhuma nova identificação de J é proposta.

[OPEN] Esta construção é local a um sítio e serve à isotropia da órbita
unitária. Não seleciona um relógio de uma curva de estados, nem mede uma
área espacial/gravitacional. A calibração e a identificação física são
obrigações distintas. Nenhum resultado de H3 ou QG geral é afirmado.

Custódia: somente os novos DERIVACAO052_MODULAR.md e
ModularHorizontalRotation.lean em Chatgpt. Originais, memórias, Atlas,
um.py e artefatos selados≤051 permanecem somente leitura. Toda revisão
terá cópia imediata dos bytes, temporário verificado e substituição.
