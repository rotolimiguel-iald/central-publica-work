[REAL — avaliação e leis no cone representado verificadas; OPEN — existência do traço de A1(b)]

# A1 — avaliação funcional, leis do peso e normalidade das séries

Data: 2026-09-14T09:44:55.963818-03:00

Este é adendo ao marco anterior, sem reescrever suas fontes, memórias ou lacunas. Os três módulos novos são fornecedores Lean em bancada, ainda não embutidos no programa. A1(a) permanece pago; A1(c) está pago nestas 37 declarações; A1(b) não tem habitante de RegularCoreTraceData nem impossibilidade tipada.

## Reutilizar, sem reconstruir

Fixe M=theFactorObject P e N=regularCoreAlgebra P. A sequência D_n(A) positiva e crescente na mesma M já existia. Agora:

    m_A(ψ) = sup_n ofReal Re ψ(D_n(A)).

O domínio da definição é o dual contínuo complexo de M. Positividade, normalidade e representação não são inferidas desse nome: as hipóteses e teoremas abaixo determinam quando cada lei vale.

1. baseVectorFunctional é um funcional contínuo na própria M; sua norma é ≤‖v‖². exists_base_series_functional constrói ψ por uma série vetorial quadrado-somável, prova HasSum complexo em todo D∈M e positividade complexa. Não recebe ψ como testemunha pronta. No sentido inverso elementar, avaliar uma representação HasSum na unidade recupera a soma dos quadrados das normas.
2. baseDualEvaluation_vector identifica m_A(ω_v)=q_A(testVector v); baseDualEvaluation_vacuum identifica m_A(ω_Ω)=ν(A), incluindo infinito. São ligações de objetos, não novos pesos de mesmo nome.
3. Adição em ψ exige funcionais positivos; homogeneidade NNReal cobre 0·∞. A semicontinuidade inferior demonstrada é na norma do dual contínuo. Não é uma identificação de preduais de Banach.
4. Para uma representação HasSum, m_A(ψ)=Σ_k q_A(testVector v_k). A soma ENNReal pode ser infinita. Duas decomposições do mesmo ψ dão o mesmo resultado após média. Não foi afirmada independência do levantamento vetorial ao core antes da média.
5. O segundo módulo transfere zero/soma/escala/ordem, normalidade em A para supremos positivos internos de REDES DIRIGIDAS ARBITRÁRIAS, bimódulo e outputs limitados. ennreal_tsum_iSup_directed fornece exatamente a troca de supremo/série necessária; não impõe enumerabilidade ao índice da rede.
6. baseDualEvaluation_eq_dual_integral prova a identidade com a integral da soma dos dualQuadraticIntegrand, usando a mesma dualAmbient e dualHaarFactor=(2π)⁻¹. Tonelli foi aplicado a termos mensuráveis não negativos, permitindo infinito. O bimódulo mantém χ explicitamente representado por Bv_k; ainda não define um transporte canônico de funcionais por B.
7. baseSeriesFunctional_normal prova normalidade por ordem do próprio ψ na BASE, a partir de HasSum. baseVectorFunctional_normal reutiliza o limite forte existente de vonNeumann_exists_positive_isLUB. A igualdade é ofReal Re ψ(S)=sup_i ofReal Re ψ(A_i) para A_i≥0; positividade complexa está provada separadamente. Esta normalidade de ψ em M é distinta da normalidade de A↦m_A(ψ) em N.
8. A fidelidade é da família de avaliações, suficiente para recusar A≠0 com todas as leituras zero. O controle da média normalizada vale 1; o input unidade tem saída infinita em cada vetor não zero. Não se afirma que cada funcional ψ seja fiel.

## O endereço da obrigação seguinte

A direção **série vetorial ⇒ funcional positivo normal** está provada no mesmo M, e a avaliação média independe da decomposição. A direção inversa permanece nomeada:

    ψ : M→L[ℂ]ℂ positivo; para todo índice dirigido não vazio ι,
    A_i∈M positivos e crescentes, IsLUB(range A) S ⇒
    ofReal Re ψ(S)=sup_i ofReal Re ψ(A_i)
      ⟹ ∃v:ℕ→TowerHilbert P,
           Summable (‖v_k‖²) ∧
           ∀D∈M, HasSum (⟨v_k,Dv_k⟩) (ψ(D)).

Esse é o lema de cobertura, não uma alegação de impossibilidade. [KNOWN] O Teorema 2.41 de Bryder, pp. 50–51, enuncia e demonstra a equivalência na álgebra de von Neumann concreta, sem hipótese de Hilbert separável. A fonte foi aberta e o enunciado/prova relidos; não foi convertido em axiom Lean: https://web.math.ku.dk/~musat/Injective_and_semidiscrete_von_Neumann_algebras_final.pdf#page=67.

A construção do predual abstrato inteiro não deve virar uma nova camada obrigatória por conveniência de nome. O próximo CONSUMIDOR é regular_dual_weight_modular_implementation de LACUNAS_A1: identificar σ^ν_t=Ad Λ_t no GNS do mesmo ν. Se a prova consumir diretamente a construção escalar e as formas concretas existentes, reutilizá-las; se consumir o cone predual padrão inteiro, pagar antes a cobertura/tipagem efetivamente exigida. Não reabrir GNS, fechamento da estrela ou Moreau já construídos.

Depois permanecem regular_unitary_positive_generator e pedersen_takesaki_inverse_generator_trace: h positivo afiliado, h^{it}=Λ_t; perturbação pelo inverso de h produzindo τ fiel normal semifinito, tracial e τ∘θ_s=e^{-s}τ. A invariância do peso ν não substitui essa escala do traço. Nenhuma dessas etapas finais foi promovida por este marco.

## Validação e alcance

São três módulos, 34 teoremas e três definições: 37 declarações. Compilação autora e reprodução independente com Lean 4.31.0, sem avisos, somente propext/Classical.choice/Quot.sound, objetos idênticos. Dois controles matemáticos adulterados foram recusados: m_A(0)=0→1 e média=1→2. Tentativas rc1 e seus sorryAx de elaboração permanecem no histórico e foram excluídas. Não houve nova rodada integral de um.py: seu Python não foi modificado nem executado.

Todos os arquivos dos dois manifestos anteriores foram reconferidos. A cópia v351 continua intacta. Durante o marco o canônico mudou: a comparação está em CUSTODIA_A1_FUNCIONAIS_CANONICO_ATUAL.json; os monólitos diferem, mas os 922 fontes formais embutidos eram exatamente idênticos na leitura. Essa medição não declara o canônico congelado para sempre. A gerência deve aplicar os fornecedores sobre sua versão corrente.

Nenhuma bandeira de fronteira foi alterada, nenhum gate foi movido por esta entrega, A2–A7 não foram iniciados e nenhum resultado físico foi examinado. O objetivo A1 permanece ativo.
