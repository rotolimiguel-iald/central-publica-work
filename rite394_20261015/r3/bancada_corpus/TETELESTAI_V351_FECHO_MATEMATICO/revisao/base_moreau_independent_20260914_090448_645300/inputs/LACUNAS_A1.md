[OPEN — enunciados das pontes restantes; não são declarações de teoremas compilados]

# A1: onde a construção existente termina

O alvo é o cone positivo de `regularCoreAlgebra P`, para **todo** `P : SiteProfile`.
O peso de partida é `scalarDualWeight P`; a ação é `regularDualAction P` e as
unitárias são `regularUnitary P t`. O contrato fortalecido é
`TGLV351.RegularCoreTraceData P`. Um termo desse contrato ainda não foi produzido.

A recusa do peso dual como fornecedor direto não afirma inexistência do traço.
Ela impede ligar dois objetos diferentes apenas mudando o nome do campo.

## Enunciados exatos que a ponte deve fornecer

Fixe N = regularCoreAlgebra P, M = theFactorObject P, φ(X) = ⟨Ω,XΩ⟩,
ν = scalarDualWeight P, Λ(t) = regularUnitary P t e θ = regularDualAction P.

1. **`regular_scalar_weight_is_dual_weight`**. Seja T a integral positiva estendida
   de θ com a medida dual ds/(2π) já utilizada no código. Para todo A∈N₊,
   ν(A)=φ̄(π⁻¹T(A)), onde φ̄ é a extensão normal de φ ao cone positivo estendido.
   A igualdade deve incluir valores infinitos. A coincidência já demonstrada para
   T(A) limitado é fornecedor, não a igualdade geral. Exibir também a ponte entre
   o ideal finito fortemente denso existente e a semifinitude da definição usada.

2. **`regular_dual_weight_modular_implementation`**. Com os dados anteriores e a
   identificação do fluxo da base com σ^φ, o grupo modular do peso ν satisfaz
   σ^ν_t(A)=Λ(t) A Λ(t)* para todo A∈N e t∈ℝ. No GNS de ν, identificar o grupo
   de Δ_ν com esse transporte e os domínios usados. A invariância ν∘AdΛ=ν já
   provada não é a condição KMS nem caracteriza sozinha o grupo modular.

3. **`regular_unitary_positive_generator`**. Existe h positivo, autoadjunto,
   não singular, afiliado a N, com h^(it)=Λ(t) para todo t. A unicidade do
   gerador e a relação de Weyl existente dão θ_s(h)=e^(−s)h. O domínio é o do
   gerador do grupo regular inteiro em L²(ℝ,H), não somente o gerador da torre.

4. **`pedersen_takesaki_inverse_generator_trace`**. Para um peso ν fiel, normal
   e semifinito em N e h como acima, se σ^ν_t=Ad(h^(it)), ponha B=h⁻¹,
   B_ε=B(1+εB)⁻¹ e

   τ(A)=sup_{ε>0} ν(B_ε^(1/2) A B_ε^(1/2)), A∈N₊.

   Então τ é fiel, normal, semifinito, aditivo, positivamente homogêneo e
   τ(a*a)=τ(aa*). Se ν∘θ_s=ν e θ_s(h)=e^(−s)h, então
   τ(θ_s(A))=e^(−s)τ(A). Este é o termo que deverá fornecer o contrato;
   não se recebe sua existência como uma nova declaração `axiom`.

São enunciados matemáticos com antecedentes e objetos identificados. Não há
nesta entrega um tipo geral completo de peso modular/Pedersen–Takesaki na
mathlib que permita simplesmente escrever `exact` para os itens 1–4. Tampouco
se afirma uma prova de ausência em toda biblioteca possível: o alcance da busca
é o pin e os fornecedores registrados na ficha.

## Reaproveitamento e convenções

Usar `regularScalarWeightCertificate`, o domínio de `scalarWeightLeftIdeal`,
os resultados de Tomita já construídos no GNS e a normalidade interna existente.
Não reconstruir esses objetos. Cada identificação adicional precisa tratar os
mesmos espaços e operadores; o J da torre e o J polar do peso não são trocáveis
por homonímia.

Com Λ(t)=h^(it), L=log h desloca para L−s. Se K=−log h, desloca para K+s.
A normalização de τ vem da perturbação do peso ν fixado e da convenção de Haar;
a lei de escala sozinha permite multiplicar τ por uma constante positiva.

## Referência externa e estatuto

[KNOWN] A rota peso dual → implementação modular → perturbação pelo inverso do
gerador → traço com escala é a de Hiai, proposição 9.3 e teoremas 9.4, 9.9,
10.13 e 10.15. A fonte foi aberta nesta rodada. Isso sustenta o roteiro
matemático, sem substituir as identificações concretas e os termos Lean.
[Hiai, *Concise lectures*, pp. 83–100](https://arxiv.org/pdf/2004.02383).

## Critérios de A1

- (a) Contrato fortalecido e recusa do zero: candidato em compilação; só declarar
  PAGO depois do retorno e da auditoria de axiomas.
- (b) Habitante para todo SiteProfile ou parede contra sua existência: **NÃO PAGO**.
  As recusas de fornecedor não são tal parede. Itens 1–4 nomeiam a lacuna.
- (c) Axiomas restritos ao trio: aguarda o relatório da compilação do candidato.

O `um.py`, suas bandeiras e os vereditos experimentais permanecem inalterados.
A1 continua em execução; esta nota não declara a ordem integral concluída.


## Adendo de execução — 2026-09-14T08:24:31.970507

[REAL] A compilação final do contrato terminou rc0, sem avisos, com 11 declarações apenas no trio. A1(a) e A1(c) pagos neste módulo; A1(b) NÃO PAGO. O controle falso 1→2 foi recusado por elaboração e auditoria. O objetivo continua ativo. Ver AUDITORIA_A1.json e a entrega do marco.
