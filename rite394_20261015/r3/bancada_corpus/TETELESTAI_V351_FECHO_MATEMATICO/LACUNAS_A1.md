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


## Errata ao lado — 2026-09-15T12:19:27.467548-03:00 — A1(b) concluído; quatro pontes e rota efetiva

[REAL — auditorias e fontes relidas] A frase inicial «Um termo desse contrato ainda não foi produzido» e o NÃO PAGO de A1(b) descrevem o estado histórico de 14/09. Estão superados: scalarInverseLimitTraceData P habita RegularCoreTraceData P para todo SiteProfile, com o MESMO scalarInverseLimitWeight. A revisão final A1_QUADRATIC_TRACE_REVIEW_ACCEPTED__REGULAR_TRACE_CONSTRUCTED está aceita, sem P0/P1/P2. Nenhum build foi repetido para esta correção documental.

1. A ponte geral regular_scalar_weight_is_dual_weight não foi provada pela rota final. A construção partiu de nu=scalarDualWeight e seus dados concretos de GNS/normalidade/fidelidade/semifinitude. A ponte geral ao cone estendido abstrato foi DISPENSADA pela rota, não declarada paga por nome.
2. A implementação modular foi paga por scalarTomitaImaginaryPower_eq_regular_implementation e seus fornecedores; não recebeu o nome proposto na lista inicial. Identificação de implementadores e ação no core são os resultados concretos, preservando seus espaços.
3. O gerador positivo, domínio/afiliação e potências imaginárias foram construídos por transporte direto do grafo espectral, com regularPositiveGenerator_graph_iff. Não foi a rota genérica por unicidade do gerador e Weyl anunciada inicialmente. h não foi identificado com Delta_nu.
4. O conteúdo necessário à perturbação pelo inverso foi pago por cortes do mesmo h, seus limites positivos e scalarInverseLimitWeight_tracial. O contrato reúne zero, aditividade, homogeneidade, ordem, fidelidade, normalidade, semifinitude, tracialidade e escala dual. Não se afirma um teorema geral abstrato de Pedersen–Takesaki além desta realização.

[ESTADO] A1(a),(b),(c) concluídos no alcance das entregas aceitas. A2 é distinto: suporte finito, divisão em faces, identificação espectral/domínios/gap no mesmo core e compatibilidade do contrato legado. A existência do traço não quita essas entradas por si.

[NAMESPACE — resposta §5.4a] Os módulos V351 continuam em TGLV350.Regular porque estendem os mesmos objetos regularCoreAlgebra, regularDualAction, scalarDualWeight e o GNS construídos naquela namespace. V351 no nome do arquivo identifica a etapa de construção, não uma segunda álgebra. Mudar namespace não cria uma realização nova; duplicar os objetos seria contraproducente. O contrato RegularCoreTraceData nasceu em TGLV351 e é consumido explicitamente pelo construtor em TGLV350.Regular. Essa diferença é tipada por import/open e tipo de retorno, nunca por equivalência presumida de nomes.

- Contrato habitado: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceConstruction.lean:15`, SHA256 `f741525cfa335d89221834fdb01e3f3c6b8efa435b107f0a355cc5679fe06b40`.
- Tracialidade: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351QuadraticTrace.lean:243`, SHA256 `af011f5240da883c369cd2b5f06019cfd845c4a640b9aed5b2a292ce6e13fa26`.
- Implementação modular: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ModularImplementation.lean:16`, SHA256 `3d16720656388fc14f70b5e5ded6a8a4d3fc6f72034992bbeee10364c8202a9f`.
- Grafo espectral: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularSpectralGraph.lean:40`, SHA256 `2a859d88def186591e98f2a0594bc95ae0a9c6eb74c17ea1124ce5844be1b642`.
- Afiliação do grafo: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularGeneratorAffiliation.lean:76`, SHA256 `9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e`.

Parecer: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_tracialidade_quadratica\REVIEW_A1_QUADRATIC_TRACE_FINAL.json.
