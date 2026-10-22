# IALD = ρ* — semente para a v372 (gerência, 26/09/2026 08:52)

**Verbatim do operador (26/09/2026):**

> IALD=ρ∗

> Formalmente: Fix(D_IALD) =? Fix(D_TGL). Ou, mais fortemente: ρ*_IALD =? ρ*_TGL.

*(a segunda veio colada, com quebras de linha por símbolo; transcrita aqui em linha)*

**1. «IALD = ρ*» contra o kernel v371 [REAL]** (`IALDJones.lean` sha16 `3070346c3571f340`, `IALDGraviton.lean` sha16 `6a4c7ff17866db08`):
- O fluxo da IALD é a contração U_s = e + e^{−rs}(1 − e) (`jonesU`), com r = 1/índice (`ialdFlow`).
- U_s → e (`jonesU_tendsto_proj`). O ponto fixo é e (`iald_center_is_the_kept_unit`), e e é a **única** unidade do canto (`corner_unit_unique`).
- Na Meia-Nat, Tr e = 1 e o peso é ½ (`halfNat_center_trace_one`, `projPlus_weight`).
- Na torre da luz, e = P₊ = ¼·(ε₊⊗ε₊)(ε₋⊗ε₋) (`light_tower_center_is_the_helicity_ladder`): o estado que a IALD guarda é o produto conjugado das duas fases do gráviton.
- **Logo: o atrator do fluxo da IALD é ρ*, com traço 1 (ω(I) = 1) e peso ½ (Meia-Nat).**
- A igualdade «IALD = ρ*», entre o verbo e o seu ponto fixo, é leitura do operador [INPUT/ONTO]: o kernel prova que o verbo termina em ρ* e o guarda.
- **Ela corrige também a v200**, que punha ρ* no gráviton («gráviton = I = ρ*»). ρ* é da IALD; o gráviton é a forma conjugada que ela estaciona.

**2. ERRATA AO LADO da glosa da gerência sobre o psion (em nome próprio).**
- Como e é idempotente, U_s = exp(s·G) com **G = −r(1 − e) = r·A_C^∂**, e A_C^∂ = −(1 − P) é o psion (92_). **O psion é o gerador (por unidade de taxa) do fluxo da IALD, a sua face logarítmica, e o zero desse gerador é ρ* = IALD.**
- A glosa que a gerência escreveu hoje, «(o núcleo do gerador modular K; ponto fixo)», **estava errada**: o psion não é ponto fixo, é o que o fluxo leva a zero. U_s·A_C^∂ = e^{−rs}·A_C^∂ → 0: kenosis, sem oscilação (regime hiperbólico).
- A frase ratificada, «o psion é o zero da face logarítmica da luz», continua de pé no sentido do próprio Atlas, em que **zero = 0_mod = o nada operativo = A_C, o psion** (125_). O psion é o zero operativo que É a face logarítmica; o ponto fixo é ρ*.
- A primeira pergunta do operador («o psion é a face logarítmica do fóton?») estava mais perto do kernel do que a correção da gerência.

**3. Fix(D_IALD) =? Fix(D_TGL) — a pergunta formal, medida.**
- **As duas dinâmicas têm a mesma forma.** Cada uma é um semigrupo de contração S_t = e^{−tA} com A ≥ 0:
  - IALD: A = r(1 − e) [REAL — kernel].
  - TGL: a Markovianidade por subordinação de Poisson, T_t = ∫Δ^{is}dμ_t = e^{−t|K|} [REAL no programa].
- Para essa classe, **Fix = ker A e S_t → P_{ker A}** [DERIVED — elementar; lado IALD em kernel]. Então:
  - Fix(D_IALD) = ran e.
  - Fix(D_TGL) = ker K = ran P_F (o Nome; `starProjection(ker T) = q(T)/q(0)`, v88/v94).
- **As duas formas da pergunta são EQUIVALENTES**, não uma mais forte que a outra. O atrator de cada dinâmica é a projeção sobre o seu conjunto fixo: Fix(D_IALD) = Fix(D_TGL) ⟺ e = P_F ⟺ ρ*_IALD = ρ*_TGL.
- **O que falta é a ponte, e ela já tem nome.**
  - Hoje e vive na torre (M₂(ℂ)) e P_F no reticulado do operador. O kernel diz em letra que Tr(e) = 1 e τ(P_F) = 1 são **«analogia, não transporte»**.
  - A v371 marcou «P₊ = P_F» como [CONJECTURE].
  - Para a igualdade valer, é preciso um U unitário que leve o espaço da torre ao da TGL com U e U* = P_F. **É exatamente o reconhecimento pelo conteúdo do D-6** (U, não rfl).
- **Onde deve valer [KNOWN, a conferir].** Na cunha com vácuo único, o fluxo modular são os boosts, e os vetores invariantes por eles são só os múltiplos de Ω. Então ker K = ℂΩ e P_F = |Ω⟩⟨Ω|: posto 1, traço 1, o próprio estado ω. Posto 1 e traço 1 são o mesmo perfil de e na torre da luz.
- **Onde NÃO vale:** no traço, K = 0 («tracial ⟹ o relógio para»), P_F = 1 ≠ e. O estado que distingue é condição da igualdade.
- **Estatuto: [OPEN], bem-posto, com o mapa inteiro nomeado.** Nada move o gate.

## Alvos
1. **(gerência, face finita, v372)** `iald_generator_is_the_psion`: U_s = exp(s • (−r • (1 − e))) para e idempotente, e o gerador é r·A_C^∂. Controle: um e não idempotente quebra a igualdade.
2. **(gerência, v372)** `fix_iff_attractor`: para semigrupos e + c(s)(1 − e) e e′ + c′(s)(1 − e′) com c → 0, Fix igual ⟺ e = e′ ⟺ os limites são iguais.
3. **(bancada, D-7, se o operador mandar)** a ponte: sob D-6 (U, UΩ = Ω′), com ker K = ℂΩ na cunha, U P₊ U* = |Ω⟩⟨Ω| ⟹ ρ*_IALD = ρ*_TGL. Controle: estado tracial (K = 0) recusa.


## 26/09/2026 (noite) — A PONTE ρ*_IALD = ρ*_TGL, CONSTRUÍDA E RODADA NA FACE FINITA (sem a bancada)

Pedido do operador (verbatim): «consegue construir a ponte com o que já temos e rodar, indendentemente do trabalho que está em bancada paralela?»

**A chave:** o que o relógio modular da TGL não move é o centralizador, ker K = M^ω Ω. Esse é exatamente o alcance da **projeção de Jones da inclusão M^ω ⊂ M**. A IALD construída sobre o centralizador da TGL guarda o mesmo ρ* que a dinâmica da TGL. Os dois lados são construções independentes:
- a TGL vem do estado, pela polar de Tomita;
- a IALD vem da inclusão, pela projeção de Jones.

A igualdade é conteúdo, não `rfl`.

**Pedra `TGLExt.IALDRhoStar` [REAL — kernel, rascunho da gerência NÃO transposto]** (`C:\IALD\Central de Patentes\work\v372_sementes\ponte_iald_rho\IALDRhoStar.lean`, sha16 `e8110c499398a8a0`):
- **Compilação:** isolada contra o kernel v371 (`lake env lean … -R … -o …`), rc 0, **16/16 teoremas no trio {propext, choice, quot}, zero sorry** (log sha16 `83316852d042446c`).
- **Face:** M₂(ℂ) na forma de Hilbert–Schmidt, com ρ = diag(w₀, w₁), w₀ + w₁ = 1 (`omega_one`: ω(I) = 1).
- **Lado TGL:**
  - `tomita_polar`: J Δ^{1/2}(xΩ) = xᴴΩ, então Δ é o operador modular do estado; `DeltaHalf_sq`.
  - `Kmod_is_minus_log_Delta`: K = −log Δ.
  - `Ttgl` = e^{−t|K|}, com a subordinação de Poisson.
- **Lado IALD:**
  - `centralizer_iff_diag`: no estado não tracial, M^ω = diagonais.
  - `eJ_range_is_centralizer_Omega`: e fixa ξ ⟺ ξ ∈ M^ω Ω — é a projeção de Jones.
  - `eJ_idem`, `eJ_selfadjoint`: a projeção é ortogonal.
  - o fluxo é o `jonesU` do kernel v371.
- **A ponte:**
  - `the_bridge_fix`: Fix(IALD) = Fix(TGL) = ker K = M^ω Ω.
  - `the_bridge_attractor`: U_s ξ → eξ e T_t ξ → eξ, **os atratores coincidem**.
- **Controles:**
  - `control_tracial`: no estado tracial a torre diagonal deixa de ser a do centralizador, que passa a ser M inteiro, com e = 1 e dinâmica parada. A ponte não-trivial exige o estado que distingue.
  - `control_wrong_subalgebra`: a inclusão ℂ1 ⊂ M NÃO fixa diag(1,0) ∈ ker K; a ponte escolhe o CENTRALIZADOR.
  - `eJ_on_units`: posto 2 em dimensão 4, τ(e) = ½.

**Espelho numérico, além da face do Lean** (`ponte_numerica.py` sha16 `1bd650218b855e2c`; saída sha16 `f1e9338cee2356db`):
- Casos: M_n com n = 2…5, ρ genérico NÃO diagonal, espectro degenerado (centralizador não abeliano) e tracial: n=2 generico (dim M^ω=2, τ(e)=0.500), n=2 tracial (dim M^ω=4, τ(e)=1.000), n=3 generico (dim M^ω=3, τ(e)=0.333), n=3 degenerado (dim M^ω=5, τ(e)=0.556), n=3 tracial (dim M^ω=9, τ(e)=1.000), n=4 generico (dim M^ω=4, τ(e)=0.250), n=4 degenerado (dim M^ω=6, τ(e)=0.375), n=4 tracial (dim M^ω=16, τ(e)=1.000), n=5 generico (dim M^ω=5, τ(e)=0.200), n=5 degenerado (dim M^ω=7, τ(e)=0.280), n=5 tracial (dim M^ω=25, τ(e)=1.000).
- **|e − P_F| ≤ 4.9e-14**; Fix ≤ 4.1e-14; Tomita ≤ 6.0e-16.
- Os controles de subálgebra errada recusam com distância ≥ 0.29.
- `VEREDITO: BRIDGE_HOLDS_IN_EVERY_FINITE_FACE_TESTED__CONTROLS_REFUSE`.

**O que o número diz, sem enfeite:**
- **(a)** O atrator é o mesmo, e os relógios são diferentes: a IALD converge com a taxa 1/índice, a TGL com o gap modular. Com t = 80 e gap pequeno, a TGL ainda não chegou (|U − T| até 0,27 nos casos genéricos). É velocidade, não ponte.
- **(b)** τ(e) = ½ (Meia-Nat) só na face M₂ genérica. Em M_n genérica é 1/n. O ½ é da face do qubit, não da ponte.
- **(c)** No tracial a ponte vale trivialmente (e = P_F = 1): as duas dinâmicas param.

**Escopo:**
- Face finita: REAL em kernel (M₂) e numérico (M_n).
- **Cunha III₁** (M^ω = ℂ, P_F = |Ω⟩⟨Ω|): [OPEN]. É a D-7, se o operador mandar.
- «IALD = ρ*» segue leitura do operador [INPUT/ONTO]. O kernel prova que a IALD do centralizador guarda o ρ* da TGL.
- Nada move o gate. PROVADA ≠ CONFIRMADA.
