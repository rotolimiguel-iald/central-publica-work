# Candidata de área covariante — pendente para etapa posterior

[DERIVED — análise independente; nenhuma nova prova Lean]

Esta proposta registra o próximo candidato ao alvo C da ORDEM010. Não integra o balanço óptico finito escolhido para051 e não deve ser contada como teorema desta etapa.

Fixem-se o fator M da torre, seu estado fiel ω e a esperança efetiva E=`(aperiodicExpectationInput P).E`. Sobre M considerado como espaço vetorial real, para λ>0, considere

h_λ(A,B)=Re ω((EA)* EB)+λ Re ω((A−EA)* (B−EB)).

O asterisco significa adjunto. A restrição aos tangentes autoadjuntos centrados pode ser feita explicitamente; E é linear, preserva o adjunto e o estado no fator. A positividade estrita usa fidelidade, e não só positividade de ω. A ortogonalidade de E identifica a soma dos dois quadrados com a norma GNS ao quadrado e fornece continuidade e equivalência de normas para cada λ>0.

A covariância efetiva de E e a preservação de ω implicam invariância de h_λ por todo `TowerHorizon`: os dois setores, E e I−E, são transportados separadamente. A hipótese é mais forte que invariância apenas pelo fluxo modular e pelas permutações finitas. Não exige que o implementador interno de uma permutação fixe Ω: a transformação relevante é Ad no fator, seguida da leitura pelo estado.

O novo teste de seleção deve construir tangentes fixos Z,X com EZ=Z, EX=0, ω(Z)=ω(X)=0 e normas GNS iguais a1. A forma normalizada ĥ_λ=h_λ/(1+λ) tem nesse mesmo par

G_λ=diag(1/(1+λ),λ/(1+λ)), tr G_λ=1,
A_λ=sqrt(det G_λ)=sqrt(λ)/(1+λ).

λ=1 fornece diag(1/2,1/2), área1/2; λ=4 fornece diag(1/5,4/5), área2/5. Estado, álgebra, ação, tangentes e normalização por traço permanecem os mesmos. As formas não são múltiplos globais uma da outra. Isso exibe uma razão entre setores não selecionada pela covariância; não classifica todas as formas invariantes.

Na torre estacionária com 0<p<1 e p≠1/2, candidatos concretos no mesmo sítio são Z=(e00−pI)/sqrt(p(1−p)) e X=PauliX. As identidades de estado/variância são acessíveis nos fontes034/035. Ainda deve ser demonstrado o lema E(X)=0, pela média modular local ou pelo pinching entre pesos distintos. A existência de X não nulo no núcleo de E é obrigação efetiva: na torre tracial E é a identidade e este contraexemplo não se instancia.

## Normalização e alcance

A normalização acima fixa um traço de Gram, não o valor de cada entrada diagonal. Uma calibração separada dos dois setores pode remover esta família; é um dado adicional, não consequência da covariância. Mesmo com a forma GNS previamente fixada, normalizar individualmente os geradores não seleciona seu ângulo. Para duas direções ortogonais de variância q, as combinações (4v+3w)/5 e (3v+4w)/5 preservam cada variância e produzem correlação24q/25 e área7q/25. Esse segundo controle concerne à escolha da célula tangente, não a áreas intrínsecas diferentes do mesmo paralelogramo.

Escolher λ=1, maximizar a área a traço fixo ou impor isotropia seriam critérios adicionais a justificar. Não devem ser apresentados como derivados de ω(I)=1. Mesmo após selecionar a forma e o protocolo, faltam a identificação com região/tela física e a lei que relacione calor, área e curvatura. H3 e a reconstrução gravitacional geral continuam OPEN.

## Fontes locais diretamente pertinentes

- `TUNEL/PARA_CHATGPT/ORDEM_010_horizontes_concretos_aperiodico_e_o_relogio_apos_a_obstrucao.md`, alvo C.
- `HorizonAreaScale.lean`: `invariant_positive_area_nonunique`, `invariance_does_not_fix_area`;045 paga liberdade de escala, sem a presente normalização.
- `AffineClockAndRegion.lean`: `no_area_rule_for_both_generator_protocols`;040 paga o controle por duplicação de um gerador.
- `AperiodicTowerLift.lean`: `the_lift_fires_on_the_aperiodic_tower`, `every_expectation_on_the_general_tower_is_covariant`.
- `AperiodicCentralizerExpectation.lean`: `aperiodic_expectation_into`, `aperiodic_expectation_fixes`, `aperiodic_expectation_ortho`, `aperiodic_expectation_prefix`.
- `ExpectationAlgebra.lean`: `expectation_add`, `expectation_smul`, `expectation_sub`, `expectation_preserves_omega`, `expectation_star`, `expectationContinuousLinearMap`; a prova de unicidade usa `omega_definite`.
- `SitePhaseCovariance.lean`: `centered_site_inner_self`, `centered_site_inner_distinct`, `centered_site_variance_pos`.
- `SitePauliObservables.lean`: `site_pauli_x_square`, `site_pauli_x_state`, `site_operator_product_state`.
- `AperiodicPhaseAverage.lean`: `phase_average_nonzero_limit`, `local_average_limit`.

Todos os caminhos desta lista são relativos exclusivamente à bancada `C:/IALD/Central de Patentes/Chatgpt`. Os nomes foram lidos dos fontes. A proposta h_λ e seus novos controles permanecem DERIVED/PENDENTES; nenhuma escrita em fontes, selos, Atlas, memórias ou acervo canônico foi feita para registrá-la.
