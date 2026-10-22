# Continuação046 — média vetorial aperiódica

06/09/2026. Derivação registrada antes do novo fonte AperiodicVectorAverage.lean.

[DERIVED — alvo Lean] Para qualquer SiteProfile P, definir V_T(v)=T⁻¹∫₀ᵀ modularFlow P t v dt, com T>0. A continuidade forte garante integrabilidade; a linearidade complexa do fluxo passa pela integral. A igualdade de normas do fluxo dá ‖V_T(v)‖≤‖v‖, portanto V_T é um operador linear contínuo de norma no máximo1.

[DERIVED] Para T_n=n+1 e cada vetor local levelEmbedding P N a, local_average_limit de AperiodicPhaseAverage dá convergência para levelEmbedding P N (specExpect (towerW P N) a). A órbita local aqui é a mesma usada na definição do completamento; não é uma densidade nova assumida.

A convergência local implica Cauchy local. Aplicar bounded_local_cauchy de BoundedOmegaLimit à sequência V_(n+1), com bound=1, e usar a completude de TowerHilbert P. O resultado é existência de limite para TODO vetor v. Nenhum operador-limite ou esperança é pressuposto.

[DERIVED] Para qualquer A limitado, modularConjugation P t A Ω = modularFlow P t (AΩ), pois modularFlow P (-t) Ω=Ω. Logo periodAverage P T hT A Ω = V_T(AΩ). O limite vetorial construído fornece assim o limite das médias de A em Ω, sem circularidade.

Para A∈theFactorObject P, period_average_mem_factor e period_average_operator fornecem pertença ao fator e a cota uniforme ‖A‖. Aplicar bounded_omega_limit_lift com o limite em Ω obtido acima. Concluir existência de B no fator, ‖B‖≤‖A‖ e convergência forte de periodAverage P(n+1) A em todos os vetores. Essa passagem usa a ação direita densa e o bicomutante, já explicitados naquele módulo de apoio.

[INPUT] Perfil P, fluxo modular da torre, operador A e a hipótese A∈M para o levantamento em M. Não se assume LocalPhasePeriod, TakesakiInput, ExpectationInput ou existência de limite.

[OPEN] Os campos into/fixes/ortho da esperança serão outra etapa, a partir da identidade prefixal. Normalidade, positividade completa e identificação física não são consequências automáticas do limite vetorial. Nenhuma lei de relógio, área ou gravidade é concluída por este módulo.

Escrita exclusivamente nestes dois arquivos novos sob Chatgpt; revisões com backup byte a byte e temporário verificado. Nenhuma alteração de045, Atlas, memórias, um.py ou acervo canônico. Compilação somente pelo procedimento serial autorizado pelo orquestrador.
