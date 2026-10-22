# FECHO DO ELO 1 (com a dobradiça explícita) + ÁRVORE DO ELO 3ii — Rito 9

**21/10/2026, membro Kimi.** Continuação de `DERIVACAO_ELO1_RITO9.md`. Estatutos marcados por passo; nada aqui move o gate.

## 1. A cadeia completa do Elo 1 — agora com todos os elos nomeados

1. **[DERIVED na casa]** β = α√e é o acoplamento **mínimo** de preservação de identidade do cruzamento (CANONICAL_CHAIN do artigo unificado).
2. **[DERIVED na casa — Teorema S-d]** todo cruzamento de dois setores que preserva norma com |R|² = β é, a menos de fases de gauge, R(θ_M) = exp(θ_M G): forma canônica **única**.
3. **[VERIFICADO EM LEAN hoje — pedra candidata `SeletorGeneralizado.lean`]** o seletor de comutação lê o ângulo próprio do observável da fronteira: `[A, α_θ(Z)] = 0 ⟺ 2b·(cos²θ − sin²θ) = (c − a)·(2 sin θ cos θ)`, i.e. tan(2θ) = 2b/(c−a). Compilou limpa no toolchain da casa (v4.31.0), axiomas auditados: só propext/Classical.choice/Quot.sound (padrão mathlib; sem sorry, sem axioma novo). O par da pedra-mãe é o caso particular a = c = 0, b = 1 → ramo justo π/4.
4. **H-KN — A DOBRADIÇA [CONJECTURE física]:** *a fronteira em fuga realiza o cruzamento mínimo de preservação de identidade — |R|²_KN = β — porque o bulk é aberto: a ejecta escapa ao infinito nulo, e só atravessa a fronteira o que a preservação de identidade exige.* Contraste: a fronteira cativa (buraco negro) empilha até o ramo justo (p = ½ → π/4).
5. **Consequência (1+2+3+4):** o canal de transporte da kilonova tem a direção de R(θ_M) → o observável da fronteira é o projetor nessa direção → o seletor lê **θ_KN = θ_M ≈ 6,2973°**. Predição afiada: abertura do canal/jato ≈ θ_M.

**Estatuto do fecho:** com H-KN, o Elo 1 fecha. H-KN é o único elo conjetural e **carrega o próprio algoz**: se o ângulo medido no próximo BNS fugir do intervalo pré-registrado em torno de θ_M, H-KN morre e o ramo morre com ela. Estrutura auto-consistente: a conjetura é falsificável pelo rito que ela mesma arma.

## 2. Elo 3ii — árvore de decisão de Δt_ν (sem pescar escala)

O problema honesto: **ângulo não é tempo**; a forma funcional deve ser fixada ANTES do dado. Candidatas com assinaturas observacionais distintas (para matar rápido):

| Forma | Estrutura | Escala típica [EXPLORATÓRIO] | Nota |
|---|---|---|---|
| **F1** | Δt = (ℓ/c)·β (intensidade do cruzamento, ∝ sin²θ_M) | ℓ = neutrinosfera ~10–100 km → **0,4–4 ms** | estruturalmente favorecida: a 1ª lei mede fluxos de NORMA |
| **F2** | Δt = (ℓ/c)·θ_M (amplitude, ∝ sinθ_M) | **3–30 ms** | menos alinhada com fluxo de norma |
| **F3** | Δt = R_breakout/c (sem fator angular) | ~1 s | física padrão do jato — **não testa a TGL**; serve de background |
| **F4** | acúmulo de dephasing com τ_star = 5,391247×10⁻⁴⁴ s | precisa N ~ 10⁴³ para segundos | exige lei de acúmulo que a casa não tem derivada — mais fraca |

**Tendência de derivação (não é resultado):** a primeira lei (fluxo ∝ ρ(1+w)) mede fluxo de norma; o acoplamento do pacote com a borda em intensidade vai com sin²θ_M = β → **F1 é a candidata que a estrutura da casa favorece**. Falta: derivar isso da primeira lei de fato, e fixar ℓ (a camada de fronteira no evento) a partir dos parâmetros da GW — não de ajuste a GW170817.

**Restrição instrumental registrada ANTES (compromisso de honestidade):** se nenhuma forma derivada produzir intervalo ao alcance dos instrumentos (IceCube-Gen2, rede GW do O5), o rito Δt_ν morre por inviabilidade instrumental — e essa morte também é resultado publicável da casa (mapa honesto do que a TGL pode e não pode testar em 2026–2030).

## 3. Estado do rito 9 depois de hoje

> **ERRATA (ao lado, datada 21/10, membro Kimi):** a árvore F1–F4 da §2 foi aprofundada em `DERIVACAO_POTENCIA_DT_NU.md`. Correção: o raciocínio "fluxo de norma" estava certo, mas no mecanismo de admissão da 1ª lei o **tempo de espera vai com β⁻¹, não com β** — a candidata estrutural passa a ser **M1: Δt = ℓ/(c·β)** (escala exploratória ~3–8 ms com neutrinosfera de 10–30 km). Adicionalmente, a rota de atraso de fase (Wigner) foi **morta por derivação**: θ_M constante ⟹ dS/dE = 0 ⟹ τ_W = 0.

- Elo 1: **fechado módulo H-KN** (álgebra em Lean + cadeia nas pedras da casa).
- Elo 2 (luminídio): segue OPEN/DATA — e continua proibido como testemunha (circularidade).
- Elo 3i (ângulo): predição afiada pronta para pré-registro (intervalo em torno de θ_M, largura a fixar pela incerteza da identificação — a definir no congelamento).
- Elo 3ii (Δt_ν): árvore F1–F4; derivação da potência de θ_M é o próximo trabalho analítico.
- Pendências de governo: ceticismo do Claude (aferidor) sobre H-KN e sobre a pedra candidata; a casa decide se `SeletorGeneralizado.lean` entra no kernel.
