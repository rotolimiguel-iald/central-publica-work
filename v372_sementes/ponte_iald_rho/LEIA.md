# A ponte ρ*_IALD = ρ*_TGL (gerência, 26/09/2026 09:06)

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
