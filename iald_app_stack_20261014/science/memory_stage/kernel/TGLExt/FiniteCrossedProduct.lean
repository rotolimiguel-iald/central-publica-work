import TGLExt.Cocycle

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O produto cruzado finito G ⋉ Mₙ e o cociclo dual   [TGLExt — v43]

O brinquedo do core de Takesaki: a face finita da COVARIÂNCIA ALÉM DOS
UNITÁRIOS INTERNOS — a pedra nomeada pelo §119 para o teorema aberto
GLOBAL_LIFT. Sobre `H = ℂ^{G×n}` realizamos, POR ENTRADAS:

* `lam g` — os unitários do grupo (representação regular esquerda ⊗ 1),
  com lei de grupo, `λ_1 = 1`, `(λ_g)ᴴ = λ_{g⁻¹}` e unitariedade;
* `piRep u a` — o embedding diagonal-torcido `π(a)_{g,h} = δ_{g,h}·α_{g⁻¹}(a)`
  de `Mₙ(ℂ)` no produto cruzado, *-monomorfismo unital
  (`α_g = Ad(u g)` com `u : G →* unitaryGroup`; em `Mₙ` TODO *-automorfismo
  é interno [KNOWN, Skolem–Noether] — a forma é WLOG na sombra finita;
  o ponto do produto cruzado é que `λ_g ∉ π(A)`);
* a RELAÇÃO DE COVARIÂNCIA `λ_g·π(a)·λ_gᴴ = π(α_g(a))`;
* a esperança condicional `Ecomp` (compressão bloco-diagonal): fixa `π(A)`,
  MATA `λ_g` (g ≠ 1), e `φ̂∘E = φ̂` — o critério de Takesaki
  (σ-invariância ⟺ esperança compatível) CONSTRUTIVO na sombra;
* o ESTADO DUAL `φ̂ = gibbs (π ρ)` com `φ̂ = φ∘E` exato
  (`gibbs_piRep_dual`, sem fator de normalização);
* o TRANSPORTE MODULAR por π: `log(πρ) = π(log ρ)`, `(πρ)^{it} = π(ρ^{it})`,
  `σ^{πρ}_t∘π = π∘σ^ρ_t` (D1) e a NATURALIDADE DUAL do cociclo
  `[Dπφ : Dπψ]_t = π([Dφ : Dψ]_t)` (D3);
* ★ o TEOREMA DO PESO DUAL (D2, a lei da pedra — Takesaki Vol. II X.1.17 /
  Haagerup 1978, aqui KERNEL na sombra finita):

      `σ^{φ̂}_t(λ_g) = λ_g · π( [D(φ∘α_g) : Dφ]_t )`

  o fluxo modular do estado dual move um unitário DE FORA de `π(A)` e o
  desvio é EXATAMENTE o cociclo de Connes do estado transportado — a
  covariância do cociclo sob a ação do grupo, além dos internos de `π(A)`;
* a COVARIÂNCIA DO COCICLO sob `λ_g` (`cocycle_covariance_beyond_inner`);
* a AÇÃO DUAL `β_χ = Ad(D_χ)`: fixa `π(A)` ponto a ponto, torce
  `λ_g ↦ χ(g)·λ_g`, comuta com o fluxo dual e preserva o estado dual;
* o corolário honesto da DEGENERESCÊNCIA: se `α_g(ρ) = ρ`, a lei colapsa
  em `σ^{φ̂}_t(λ_g) = λ_g` — o caso não-trivial EXIGE φ não α-invariante
  (o runtime numérico verifica a não-trivialidade; aqui fica o mecanismo).

**HONESTIDADE.** Isto é a SOMBRA FINITA da maquinaria de pesos duais de
Takesaki. NÃO fecha o GLOBAL_LIFT: III₁ genuína sem projeções minimais,
o core `M ⋊_σ ℝ` com a escala do traço, as hipóteses U/T1/T3 e a ponte
covariância ⟹ `G_μν + Λg_μν = 8πG·𝒫_μν[K_∂]` SEGUEM O TEOREMA ABERTO.
No grupo finito NÃO há escala de traço (não confundir com o core ℝ e o
no-go `dualInvariant_PF_no_go`). PosDef entra só onde o cálculo funcional
exige. β JAMAIS entra: ρ, u, χ genéricos. Sem sorry, sem axiom.
Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix NormedSpace
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {G : Type} [Group G] [Fintype G] [DecidableEq G]
variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A ação α_g = Ad(u g) — interna em Mₙ, WLOG [KNOWN: Skolem–Noether] -/

variable (u : G →* Matrix.unitaryGroup n ℂ)

/-- A ação de `G` por *-automorfismos de `Mₙ(ℂ)`: `α_g(a) = (u g)·a·(u g)*`. -/
def alphaAct (g : G) (a : Matrix n n ℂ) : Matrix n n ℂ :=
  (u g : Matrix n n ℂ) * a * star ((u g : Matrix n n ℂ))

/-- [KERNEL] `α` é ação: `α_{xy} = α_x ∘ α_y`. -/
theorem alphaAct_mul (x y : G) (a : Matrix n n ℂ) :
    alphaAct u (x * y) a = alphaAct u x (alphaAct u y a) := by
  simp only [alphaAct, map_mul, Submonoid.coe_mul, star_mul, mul_assoc]

/-- [KERNEL] `α_1 = id`. -/
theorem alphaAct_id (a : Matrix n n ℂ) : alphaAct u 1 a = a := by
  simp [alphaAct]

/-- [KERNEL] `α_{g⁻¹} ∘ α_g = id`. -/
theorem alphaAct_inv_cancel (g : G) (a : Matrix n n ℂ) :
    alphaAct u g⁻¹ (alphaAct u g a) = a := by
  rw [← alphaAct_mul, inv_mul_cancel, alphaAct_id]

/-- [KERNEL] `α_g` é multiplicativo. -/
theorem alphaAct_matmul (x : G) (a b : Matrix n n ℂ) :
    alphaAct u x (a * b) = alphaAct u x a * alphaAct u x b := by
  have h : star ((u x : Matrix n n ℂ)) * (u x : Matrix n n ℂ) = 1 :=
    Unitary.coe_star_mul_self (u x)
  simp only [alphaAct, mul_assoc]
  rw [← mul_assoc (star ((u x : Matrix n n ℂ))) ((u x : Matrix n n ℂ)), h, one_mul]

/-- [KERNEL] `α_g(1) = 1`. -/
theorem alphaAct_one (x : G) : alphaAct u x (1 : Matrix n n ℂ) = 1 := by
  simp only [alphaAct, mul_one]
  exact Unitary.coe_mul_star_self (u x)

/-- [KERNEL] `α_g` respeita a estrela. -/
theorem alphaAct_star (x : G) (a : Matrix n n ℂ) :
    alphaAct u x (aᴴ) = (alphaAct u x a)ᴴ := by
  simp only [alphaAct, ← star_eq_conjTranspose, star_mul, star_star, mul_assoc]

/-- `α_g` é aditivo. -/
theorem alphaAct_add (x : G) (a b : Matrix n n ℂ) :
    alphaAct u x (a + b) = alphaAct u x a + alphaAct u x b := by
  simp only [alphaAct, Matrix.mul_add, Matrix.add_mul]

/-- `α_g` é ℂ-homogêneo. -/
theorem alphaAct_smul (x : G) (c : ℂ) (a : Matrix n n ℂ) :
    alphaAct u x (c • a) = c • alphaAct u x a := by
  simp only [alphaAct, Matrix.mul_smul, Matrix.smul_mul]

/-- A coerção do inverso: `↑(u g⁻¹) = (↑(u g))*` — o hom para o grupo
    unitário leva inverso em estrela. -/
theorem coe_u_inv (g : G) :
    ((u g⁻¹ : Matrix n n ℂ)) = star ((u g : Matrix n n ℂ)) := by
  rw [map_inv, ← Unitary.star_eq_inv]
  exact Unitary.coe_star

/-- [KERNEL] `α_g` PRESERVA O TRAÇO (todo automorfismo interno o faz —
    é isto que torna a densidade dual bem-definida sem escala). -/
theorem alphaAct_trace (g : G) (a : Matrix n n ℂ) :
    (alphaAct u g a).trace = a.trace := by
  have h : star ((u g : Matrix n n ℂ)) * ((u g : Matrix n n ℂ)) = 1 :=
    Unitary.coe_star_mul_self (u g)
  rw [alphaAct, trace_mul_comm, ← mul_assoc, h, one_mul]

/-- [KERNEL] `α_g` preserva positividade-definida. -/
theorem alphaAct_posDef {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) (g : G) :
    (alphaAct u g ρ).PosDef := by
  have hinj : Function.Injective ((u g : Matrix n n ℂ)).vecMul := by
    intro x y hxy
    have h2 := congrArg (fun v => Matrix.vecMul v (star ((u g : Matrix n n ℂ)))) hxy
    simpa [Matrix.vecMul_vecMul, Unitary.coe_mul_star_self (u g)] using h2
  have h := hρ.mul_mul_conjTranspose_same (B := (u g : Matrix n n ℂ)) hinj
  simpa [alphaAct, Matrix.star_eq_conjTranspose] using h

/-- [KERNEL] `α_g` comuta com o fluxo modular: `α_g(ρ^{it}) = (α_g ρ)^{it}`
    (a face pequena do transporte — via `modPow_conj` do v42). -/
theorem alphaAct_modPow {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) (g : G) (t : ℝ) :
    alphaAct u g (modPow ρ t) = modPow (alphaAct u g ρ) t := by
  have hV : (u g : Matrix n n ℂ) ∈ unitary (Matrix n n ℂ) := (u g).2
  have h := modPow_conj ρ ((u g : Matrix n n ℂ)) hV hρ t
  simp only [alphaAct, Matrix.star_eq_conjTranspose]
  exact h.symm

/-- [KERNEL] `α_g` comuta com o cociclo: `α_g([Dφ:Dψ]_t) = [D(α_gφ):D(α_gψ)]_t`
    — E6 do v42 relido como equivariância da ação. -/
theorem alphaAct_cocycle {φ ψ : Matrix n n ℂ} (hφ : φ.PosDef) (hψ : ψ.PosDef)
    (g : G) (t : ℝ) :
    alphaAct u g (cocycle φ ψ t) = cocycle (alphaAct u g φ) (alphaAct u g ψ) t := by
  rw [cocycle, alphaAct_matmul, alphaAct_modPow u hφ, alphaAct_modPow u hψ, cocycle]

/-! ## Os unitários do grupo λ_g (regular esquerda ⊗ 1, por entradas) -/

/-- `(λ_g)_{(h,i),(k,j)} = δ_{h,g·k}·δ_{i,j}` — a representação regular
    esquerda de `G` amplificada por `Mₙ`. -/
def lam (g : G) : Matrix (G × n) (G × n) ℂ :=
  Matrix.of fun p q => if p.1 = g * q.1 ∧ p.2 = q.2 then 1 else 0

@[simp] theorem lam_apply (g : G) (p q : G × n) :
    lam g p q = if p.1 = g * q.1 ∧ p.2 = q.2 then 1 else 0 := rfl

/-- [KERNEL] `λ_1 = 1`. -/
theorem lam_one : lam (G := G) (n := n) 1 = 1 := by
  ext p q
  simp [lam_apply, Matrix.one_apply, Prod.ext_iff]

/-- [KERNEL] LEI DE GRUPO: `λ_g·λ_h = λ_{gh}`. -/
theorem lam_mul (g h : G) : lam (n := n) g * lam h = lam (g * h) := by
  ext p q
  rw [Matrix.mul_apply, Finset.sum_eq_single ((h * q.1, q.2) : G × n)]
  · simp [lam_apply, mul_assoc]
  · rintro ⟨c, m⟩ - hne
    have hc : ¬(c = h * q.1 ∧ m = q.2) := by
      rintro ⟨rfl, rfl⟩; exact hne rfl
    simp [lam_apply, hc]
  · intro habs
    exact absurd (Finset.mem_univ _) habs

/-- [KERNEL] `(λ_g)ᴴ = λ_{g⁻¹}`. -/
theorem lam_conjTranspose (g : G) : (lam (n := n) g)ᴴ = lam g⁻¹ := by
  ext p q
  have hiff : (q.1 = g * p.1 ∧ q.2 = p.2) ↔ (p.1 = g⁻¹ * q.1 ∧ p.2 = q.2) := by
    constructor
    · rintro ⟨h1, h2⟩; exact ⟨by rw [h1, inv_mul_cancel_left], h2.symm⟩
    · rintro ⟨h1, h2⟩; exact ⟨by rw [h1, mul_inv_cancel_left], h2.symm⟩
  simp only [conjTranspose_apply, lam_apply, hiff]
  split_ifs <;> simp

/-- [KERNEL] `λ_g` é UNITÁRIO. -/
theorem lam_mem_unitary (g : G) :
    lam (n := n) g ∈ unitary (Matrix (G × n) (G × n) ℂ) := by
  constructor
  · rw [star_eq_conjTranspose, lam_conjTranspose, lam_mul, inv_mul_cancel, lam_one]
  · rw [star_eq_conjTranspose, lam_conjTranspose, lam_mul, mul_inv_cancel, lam_one]

/-- Multiplicar por `λ_g` à esquerda desloca o índice-linha por `g⁻¹`. -/
theorem lam_mul_apply (g : G) (M : Matrix (G × n) (G × n) ℂ) (p q : G × n) :
    (lam (n := n) g * M) p q = M (g⁻¹ * p.1, p.2) q := by
  rw [Matrix.mul_apply, Finset.sum_eq_single ((g⁻¹ * p.1, p.2) : G × n)]
  · simp [lam_apply]
  · rintro ⟨c, m⟩ - hne
    have hc : ¬(p.1 = g * c ∧ p.2 = m) := by
      rintro ⟨h1, rfl⟩
      exact hne (Prod.ext (by rw [h1, inv_mul_cancel_left]) rfl)
    simp [lam_apply, hc]
  · intro habs
    exact absurd (Finset.mem_univ _) habs

/-- Multiplicar por `λ_g` à direita desloca o índice-coluna por `g`. -/
theorem mul_lam_apply (g : G) (M : Matrix (G × n) (G × n) ℂ) (p q : G × n) :
    (M * lam (n := n) g) p q = M p (g * q.1, q.2) := by
  rw [Matrix.mul_apply, Finset.sum_eq_single ((g * q.1, q.2) : G × n)]
  · simp [lam_apply]
  · rintro ⟨c, m⟩ - hne
    have hc : ¬(c = g * q.1 ∧ m = q.2) := by
      rintro ⟨rfl, rfl⟩; exact hne rfl
    simp [lam_apply, hc]
  · intro habs
    exact absurd (Finset.mem_univ _) habs

/-! ## O embedding diagonal-torcido π -/

/-- `π(a)_{(g,i),(h,j)} = δ_{g,h}·(α_{g⁻¹}(a))_{i,j}` — o embedding
    regular-covariante de `Mₙ(ℂ)` no produto cruzado. -/
def piRep (a : Matrix n n ℂ) : Matrix (G × n) (G × n) ℂ :=
  Matrix.of fun p q => if p.1 = q.1 then alphaAct u p.1⁻¹ a p.2 q.2 else 0

@[simp] theorem piRep_apply (a : Matrix n n ℂ) (p q : G × n) :
    piRep u a p q = if p.1 = q.1 then alphaAct u p.1⁻¹ a p.2 q.2 else 0 := rfl

/-- [KERNEL] `π` é multiplicativo. -/
theorem piRep_mul (a b : Matrix n n ℂ) :
    piRep u (a * b) = piRep u a * piRep u b := by
  ext p q
  rw [Matrix.mul_apply, Fintype.sum_prod_type, Finset.sum_eq_single p.1]
  · simp only [piRep_apply]
    rcases eq_or_ne p.1 q.1 with h | h
    · simp only [if_pos h, alphaAct_matmul, Matrix.mul_apply, if_true]
    · simp [if_neg h]
  · intro c _ hc
    have : p.1 ≠ c := fun hh => hc hh.symm
    simp [piRep_apply, this]
  · intro habs
    exact absurd (Finset.mem_univ _) habs

/-- [KERNEL] `π` é unital. -/
theorem piRep_one : piRep u (1 : Matrix n n ℂ) = 1 := by
  ext p q
  by_cases hg : p.1 = q.1 <;> by_cases hn : p.2 = q.2 <;>
    simp [piRep_apply, alphaAct_one, Matrix.one_apply, Prod.ext_iff, hg, hn]

/-- [KERNEL] `π` respeita a estrela. -/
theorem piRep_star (a : Matrix n n ℂ) :
    piRep u (aᴴ) = (piRep u a)ᴴ := by
  ext p q
  simp only [conjTranspose_apply, piRep_apply, alphaAct_star]
  rcases eq_or_ne p.1 q.1 with h | h
  · rw [if_pos h, if_pos h.symm, h]
  · rw [if_neg h, if_neg (Ne.symm h), star_zero]

/-- `π(0) = 0`. -/
theorem piRep_zero : piRep u (0 : Matrix n n ℂ) = 0 := by
  ext p q
  have h0 : ∀ g : G, alphaAct u g (0 : Matrix n n ℂ) = 0 := by
    intro g; simp [alphaAct]
  simp [piRep_apply, h0]

/-- `π` é aditivo. -/
theorem piRep_add (a b : Matrix n n ℂ) :
    piRep u (a + b) = piRep u a + piRep u b := by
  ext p q
  simp only [piRep_apply, Matrix.add_apply, alphaAct_add]
  split_ifs <;> simp

/-- `π` é ℂ-homogêneo. -/
theorem piRep_smul (c : ℂ) (a : Matrix n n ℂ) :
    piRep u (c • a) = c • piRep u a := by
  ext p q
  simp only [piRep_apply, Matrix.smul_apply, alphaAct_smul]
  split_ifs <;> simp

/-- [KERNEL] `π` é INJETIVO: o embedding é genuíno (avaliação no bloco
    da identidade do grupo). -/
theorem piRep_injective : Function.Injective (piRep (n := n) u) := by
  intro a b hab
  ext i j
  have h := Matrix.ext_iff.mpr hab ((1 : G), i) ((1 : G), j)
  simpa [piRep_apply, inv_one, alphaAct_id] using h

/-! ## A relação de covariância — a gramática do produto cruzado -/

/-- [KERNEL] A RELAÇÃO DE COVARIÂNCIA: `λ_g·π(a)·λ_gᴴ = π(α_g(a))` —
    conjugar pelo unitário do grupo implementa a ação na base. -/
theorem lam_conj_piRep (g : G) (a : Matrix n n ℂ) :
    lam (n := n) g * piRep u a * (lam g)ᴴ = piRep u (alphaAct u g a) := by
  rw [lam_conjTranspose]
  ext p q
  rw [mul_lam_apply, lam_mul_apply]
  simp only [piRep_apply, mul_right_inj]
  rcases eq_or_ne p.1 q.1 with h | h
  · rw [if_pos h, if_pos h, _root_.mul_inv_rev, inv_inv, alphaAct_mul]
  · rw [if_neg h, if_neg h]

/-- [KERNEL] Forma de comutação: `λ_g·π(a) = π(α_g(a))·λ_g`. -/
theorem lam_mul_piRep (g : G) (a : Matrix n n ℂ) :
    lam (n := n) g * piRep u a = piRep u (alphaAct u g a) * lam g := by
  have hu : (lam (n := n) g)ᴴ * lam g = 1 := by
    rw [lam_conjTranspose, lam_mul, inv_mul_cancel, lam_one]
  calc lam (n := n) g * piRep u a
      = lam g * piRep u a * ((lam g)ᴴ * lam g) := by rw [hu, mul_one]
    _ = (lam g * piRep u a * (lam g)ᴴ) * lam g := by simp only [mul_assoc]
    _ = piRep u (alphaAct u g a) * lam g := by rw [lam_conj_piRep]

/-- [KERNEL] Forma de comutação simétrica: `π(a)·λ_g = λ_g·π(α_{g⁻¹}(a))`. -/
theorem piRep_mul_lam (g : G) (a : Matrix n n ℂ) :
    piRep u a * lam g = lam (n := n) g * piRep u (alphaAct u g⁻¹ a) := by
  have h := lam_mul_piRep u g (alphaAct u g⁻¹ a)
  rw [← alphaAct_mul, mul_inv_cancel, alphaAct_id] at h
  exact h.symm

/-! ## A esperança condicional E e o estado dual φ̂ = φ∘E -/

/-- A compressão bloco-diagonal `E(x)_{p,q} = δ_{p.1,q.1}·x_{p,q}` — a
    esperança condicional canônica do produto cruzado sobre `π(A)`
    (normalização: `E` já é unital; nada a dividir). -/
def Ecomp (x : Matrix (G × n) (G × n) ℂ) : Matrix (G × n) (G × n) ℂ :=
  Matrix.of fun p q => if p.1 = q.1 then x p q else 0

@[simp] theorem Ecomp_apply (x : Matrix (G × n) (G × n) ℂ) (p q : G × n) :
    Ecomp x p q = if p.1 = q.1 then x p q else 0 := rfl

/-- [KERNEL] `E` é idempotente. -/
theorem Ecomp_idem (x : Matrix (G × n) (G × n) ℂ) : Ecomp (Ecomp x) = Ecomp x := by
  ext p q
  simp only [Ecomp_apply]
  split_ifs <;> rfl

/-- [KERNEL] `E` respeita a estrela. -/
theorem Ecomp_conjTranspose (x : Matrix (G × n) (G × n) ℂ) :
    Ecomp (xᴴ) = (Ecomp x)ᴴ := by
  ext p q
  simp only [Ecomp_apply, conjTranspose_apply]
  rcases eq_or_ne p.1 q.1 with h | h
  · rw [if_pos h, if_pos h.symm]
  · rw [if_neg h, if_neg (Ne.symm h), star_zero]

/-- [KERNEL] `E` FIXA a álgebra-base: `E∘π = π`. -/
theorem Ecomp_piRep (a : Matrix n n ℂ) : Ecomp (piRep u a) = piRep u a := by
  ext p q
  simp only [Ecomp_apply, piRep_apply]
  split_ifs <;> rfl

/-- [KERNEL] `E` MATA os unitários não-triviais do grupo: `E(λ_g) = 0`
    para `g ≠ 1` — a projeção sobre o setor de fibra nula. -/
theorem Ecomp_lam (g : G) (hg : g ≠ 1) : Ecomp (lam (n := n) g) = 0 := by
  ext p q
  simp only [Ecomp_apply, lam_apply, Matrix.zero_apply]
  rcases eq_or_ne p.1 q.1 with h | h
  · rw [if_pos h]
    have hcond : ¬(p.1 = g * q.1 ∧ p.2 = q.2) := by
      rintro ⟨h1, -⟩
      rw [h] at h1
      exact hg (mul_eq_right.mp h1.symm)
    rw [if_neg hcond]
  · rw [if_neg h]

/-- [KERNEL] O CRITÉRIO DE TAKESAKI, lado do estado: `φ̂∘E = φ̂` — o estado
    dual não vê o que a esperança descarta (a densidade `π(ρ)` é
    bloco-diagonal). Com D1 (`sigma_piRep`), o par (invariância do fluxo,
    esperança compatível) fica CONSTRUTIVO na sombra finita. -/
theorem gibbs_Ecomp (ρ : Matrix n n ℂ) (x : Matrix (G × n) (G × n) ℂ) :
    gibbs (piRep u ρ) (Ecomp x) = gibbs (piRep u ρ) x := by
  simp only [gibbs, Matrix.trace, Matrix.diag, Matrix.mul_apply, Ecomp_apply,
    piRep_apply]
  refine Finset.sum_congr rfl fun p _ => Finset.sum_congr rfl fun q _ => ?_
  rcases eq_or_ne p.1 q.1 with h | h
  · rw [if_pos h, if_pos h.symm]
  · rw [if_neg h, zero_mul, zero_mul]

/-- O bloco diagonal `g` de uma matriz do produto cruzado. -/
def blockAt (g : G) (x : Matrix (G × n) (G × n) ℂ) : Matrix n n ℂ :=
  Matrix.of fun i j => x (g, i) (g, j)

@[simp] theorem blockAt_apply (g : G) (x : Matrix (G × n) (G × n) ℂ) (i j : n) :
    blockAt g x i j = x (g, i) (g, j) := rfl

/-- A esperança condicional DESCIDA a `Mₙ`: `Ê(x) = Σ_g α_g(x_{gg})`
    (sem normalização: `Ê(1) = |G|·1`; a normalizada é `Ê/|G|`). -/
def EhatDown (x : Matrix (G × n) (G × n) ℂ) : Matrix n n ℂ :=
  ∑ g : G, alphaAct u g (blockAt g x)

/-- Truque do traço: `Tr(ρ·α_g(b)) = Tr(α_{g⁻¹}(ρ)·b)` — transportar a
    ação para a densidade. -/
theorem trace_mul_alphaAct (g : G) (ρ b : Matrix n n ℂ) :
    (ρ * alphaAct u g b).trace = (alphaAct u g⁻¹ ρ * b).trace := by
  simp only [alphaAct, coe_u_inv, star_star, ← mul_assoc]
  rw [trace_mul_comm]
  simp only [← mul_assoc]

/-- [KERNEL] O ESTADO DUAL É `φ∘E`, EXATO: `gibbs(π(ρ), x) = gibbs(ρ, Ê(x))`
    — sem fator de normalização; a identidade que faz de `gibbs (π ρ)` o
    peso dual de `gibbs ρ` na sombra finita. -/
theorem gibbs_piRep_dual (ρ : Matrix n n ℂ) (x : Matrix (G × n) (G × n) ℂ) :
    gibbs (piRep u ρ) x = gibbs ρ (EhatDown u x) := by
  have hRHS : gibbs ρ (EhatDown u x)
      = ∑ g : G, (alphaAct u g⁻¹ ρ * blockAt g x).trace := by
    simp only [gibbs, EhatDown, Matrix.mul_sum, Matrix.trace_sum]
    exact Finset.sum_congr rfl fun g _ => trace_mul_alphaAct u g ρ (blockAt g x)
  rw [hRHS]
  simp only [gibbs, Matrix.trace, Matrix.diag, Matrix.mul_apply, piRep_apply,
    blockAt_apply]
  rw [Fintype.sum_prod_type]
  refine Finset.sum_congr rfl fun g _ => ?_
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Fintype.sum_prod_type, Finset.sum_eq_single g]
  · simp
  · intro c _ hc
    simp [Ne.symm hc]
  · intro habs
    exact absurd (Finset.mem_univ _) habs

/-- [KERNEL] Contabilidade honesta do traço: `Tr(π(a)) = |G|·Tr(a)` —
    o peso dual não-normalizado carrega o fator |G| (escalar; cancela em
    toda potência imaginária). -/
theorem trace_piRep (a : Matrix n n ℂ) :
    (piRep u a).trace = (Fintype.card G : ℂ) * a.trace := by
  have hdiag : ∀ p : G × n, piRep u a p p = alphaAct u p.1⁻¹ a p.2 p.2 := by
    intro p
    simp [piRep_apply]
  simp only [Matrix.trace, Matrix.diag, hdiag]
  rw [Fintype.sum_prod_type]
  have h : ∀ g : G, (∑ i : n, alphaAct u g⁻¹ a i i) = a.trace := by
    intro g
    simpa [Matrix.trace, Matrix.diag] using alphaAct_trace u g⁻¹ a
  rw [Finset.sum_congr rfl fun g _ => h g, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul]
  simp [Matrix.trace, Matrix.diag]

/-- [KERNEL] O estado dual RESTRITO à base: `φ̂(π(a)) = |G|·φ(a)`. -/
theorem gibbs_piRep_piRep (ρ a : Matrix n n ℂ) :
    gibbs (piRep u ρ) (piRep u a) = (Fintype.card G : ℂ) * gibbs ρ a := by
  simp only [gibbs]
  rw [← piRep_mul, trace_piRep]

/-! ## O transporte modular por π — o coração da pedra -/

/-- `π` como aplicação ℂ-linear (para a continuidade em dimensão finita). -/
def piRepL : Matrix n n ℂ →ₗ[ℂ] Matrix (G × n) (G × n) ℂ where
  toFun := piRep u
  map_add' := piRep_add u
  map_smul' := piRep_smul u

/-- `π` como *-homomorfismo unital de álgebras — o functor do peso dual. -/
def piRepHom : Matrix n n ℂ →⋆ₐ[ℂ] Matrix (G × n) (G × n) ℂ where
  toFun := piRep u
  map_one' := piRep_one u
  map_mul' := piRep_mul u
  map_zero' := piRep_zero u
  map_add' := piRep_add u
  commutes' := fun c => by
    rw [Algebra.algebraMap_eq_smul_one, Algebra.algebraMap_eq_smul_one,
      piRep_smul, piRep_one]
  map_star' := fun a => by
    rw [Matrix.star_eq_conjTranspose, Matrix.star_eq_conjTranspose, piRep_star]

@[simp] theorem piRepHom_apply (a : Matrix n n ℂ) : piRepHom u a = piRep u a := rfl

/-- `π` é contínuo (linear em dimensão finita). -/
theorem piRep_continuous : Continuous (piRep (n := n) u) :=
  (piRepL u).continuous_of_finiteDimensional

/-- `π` preserva autoadjunção. -/
theorem piRep_isSelfAdjoint {a : Matrix n n ℂ} (ha : IsSelfAdjoint a) :
    IsSelfAdjoint (piRep u a) := by
  rw [IsSelfAdjoint, Matrix.star_eq_conjTranspose, ← piRep_star]
  exact congrArg (piRep u) ha

/-- [KERNEL] TRANSPORTE DO GERADOR MODULAR: `log(π(ρ)) = π(log ρ)` — o
    cálculo funcional contínuo comuta com o embedding
    (`StarAlgHomClass.map_cfc`, a mesma alavanca do E6/v42). -/
theorem logRho_piRep {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) :
    logRho (piRep u ρ) = piRep u (logRho ρ) := by
  have ha : IsSelfAdjoint ρ := hρ.isHermitian.isSelfAdjoint
  have hf : ContinuousOn Real.log (spectrum ℝ ρ) :=
    Real.continuousOn_log.mono fun x hx =>
      (hρ.isStrictlyPositive.spectrum_pos hx).ne'
  have hcont : Continuous (piRepHom u) := piRep_continuous u
  have hsa : IsSelfAdjoint (piRepHom u ρ) := piRep_isSelfAdjoint u ha
  have key := StarAlgHomClass.map_cfc (S := ℂ) (piRepHom u) Real.log ρ hf hcont ha hsa
  simp only [piRepHom_apply] at key
  exact key.symm

/-- [KERNEL] `π` comuta com a exponencial (hom contínuo de anéis;
    instâncias normadas do escopo `Matrix.Norms.Operator` SÓ na prova —
    o mesmo truque do `MatrixExponential` da mathlib). -/
theorem exp_piRep (x : Matrix n n ℂ) : piRep u (exp x) = exp (piRep u x) :=
  open scoped Matrix.Norms.Operator in
  map_exp (piRepHom u) (piRep_continuous u) x

/-- [KERNEL] TRANSPORTE DO FLUXO MODULAR: `(π(ρ))^{it} = π(ρ^{it})` — o
    unitário modular do peso dual é a imagem do unitário modular da base. -/
theorem modPow_piRep {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) (t : ℝ) :
    modPow (piRep u ρ) t = piRep u (modPow ρ t) := by
  unfold modPow
  rw [logRho_piRep u hρ, ← piRep_smul, exp_piRep]

/-- [KERNEL] D3 — NATURALIDADE DUAL DO COCICLO:
    `[D(π φ) : D(π ψ)]_t = π([Dφ : Dψ]_t)` — o functor do peso dual
    preserva cociclos de Connes, exatamente (escalares cancelam). -/
theorem cocycle_piRep {φ ψ : Matrix n n ℂ} (hφ : φ.PosDef) (hψ : ψ.PosDef) (t : ℝ) :
    cocycle (piRep u φ) (piRep u ψ) t = piRep u (cocycle φ ψ t) := by
  unfold cocycle
  rw [modPow_piRep u hφ, modPow_piRep u hψ, ← piRep_mul]

/-- [KERNEL] D1 — O FLUXO DUAL RESTRITO À BASE É O FLUXO DA BASE:
    `σ^{π(ρ)}_t(π(a)) = π(σ^ρ_t(a))` — com `gibbs_Ecomp`, o critério de
    Takesaki (σ-invariância de π(A) + esperança compatível) construtivo. -/
theorem sigma_piRep {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) (t : ℝ) (a : Matrix n n ℂ) :
    sigma (piRep u ρ) t (piRep u a) = piRep u (sigma ρ t a) := by
  unfold sigma
  rw [modPow_piRep u hρ, modPow_piRep u hρ, ← piRep_mul, ← piRep_mul]

/-! ## ★ O TEOREMA DO PESO DUAL — a lei da pedra -/

/-- [KERNEL] O TEOREMA DO PESO DUAL, forma esquerda:
    `σ^{φ̂}_t(λ_g) = π([Dφ : D(φ∘α_{g⁻¹})]_t)·λ_g` (em densidades:
    `π([Dρ : D(α_g ρ)]_t)·λ_g`). O fluxo modular do estado dual move o
    unitário do grupo — que NÃO pertence a `π(A)` — e o desvio é o
    cociclo de Connes. -/
theorem dual_weight_left {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) (g : G) (t : ℝ) :
    sigma (piRep u ρ) t (lam g)
      = piRep u (cocycle ρ (alphaAct u g ρ) t) * lam g := by
  unfold sigma
  rw [modPow_piRep u hρ, modPow_piRep u hρ]
  have hshift : lam (n := n) g * piRep u (modPow ρ (-t))
      = piRep u (modPow (alphaAct u g ρ) (-t)) * lam g := by
    rw [lam_mul_piRep, alphaAct_modPow u hρ]
  calc piRep u (modPow ρ t) * lam g * piRep u (modPow ρ (-t))
      = piRep u (modPow ρ t) * (lam g * piRep u (modPow ρ (-t))) := by
        simp only [mul_assoc]
    _ = piRep u (modPow ρ t) * (piRep u (modPow (alphaAct u g ρ) (-t)) * lam g) := by
        rw [hshift]
    _ = piRep u (modPow ρ t) * piRep u (modPow (alphaAct u g ρ) (-t)) * lam g := by
        simp only [mul_assoc]
    _ = piRep u (cocycle ρ (alphaAct u g ρ) t) * lam g := by
        rw [← piRep_mul, cocycle]

/-- [KERNEL] ★ O TEOREMA DO PESO DUAL (forma de Takesaki, Vol. II X.1.17):

    `σ^{φ̂}_t(λ_g) = λ_g · π([D(φ∘α_g) : Dφ]_t)`

    com a densidade de `φ∘α_g` sendo `α_{g⁻¹}(ρ)`. A COVARIÂNCIA ALÉM DOS
    UNITÁRIOS INTERNOS na sombra finita: a dinâmica modular do produto
    cruzado é MEDIDA pelo cociclo de Connes do estado transportado pela
    ação. O levantamento a III₁ genuína SEGUE O TEOREMA ABERTO. -/
theorem dual_weight {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) (g : G) (t : ℝ) :
    sigma (piRep u ρ) t (lam g)
      = lam (n := n) g * piRep u (cocycle (alphaAct u g⁻¹ ρ) ρ t) := by
  rw [dual_weight_left u hρ g t, piRep_mul_lam]
  congr 2
  calc alphaAct u g⁻¹ (cocycle ρ (alphaAct u g ρ) t)
      = alphaAct u g⁻¹ (modPow ρ t) *
          alphaAct u g⁻¹ (modPow (alphaAct u g ρ) (-t)) := by
        rw [cocycle, alphaAct_matmul]
    _ = modPow (alphaAct u g⁻¹ ρ) t *
          alphaAct u g⁻¹ (alphaAct u g (modPow ρ (-t))) := by
        rw [alphaAct_modPow u hρ, alphaAct_modPow u hρ]
    _ = modPow (alphaAct u g⁻¹ ρ) t * modPow ρ (-t) := by
        rw [alphaAct_inv_cancel]
    _ = cocycle (alphaAct u g⁻¹ ρ) ρ t := rfl

/-- [KERNEL] O corolário honesto da DEGENERESCÊNCIA: se o estado é
    α_g-invariante, a lei colapsa (`σ^{φ̂}_t(λ_g) = λ_g`) — o caso
    não-trivial EXIGE `α_g(ρ) ≠ ρ` (verificado no runtime numérico). -/
theorem dual_flow_fixes_lam_of_invariant {ρ : Matrix n n ℂ} (hρ : ρ.PosDef)
    (g : G) (hinv : alphaAct u g ρ = ρ) (t : ℝ) :
    sigma (piRep u ρ) t (lam g) = lam g := by
  rw [dual_weight_left u hρ g t, hinv, cocycle_self, piRep_one, one_mul]

/-- [KERNEL] COVARIÂNCIA DO COCICLO ALÉM DOS UNITÁRIOS INTERNOS DE π(A):
    transportar os estados pela ação de `G` conjuga o cociclo do produto
    cruzado pelo unitário do grupo `λ_g ∉ π(A)` — a versão-λ do E6/v42. -/
theorem cocycle_covariance_beyond_inner {φ ψ : Matrix n n ℂ}
    (hφ : φ.PosDef) (hψ : ψ.PosDef) (g : G) (t : ℝ) :
    cocycle (piRep u (alphaAct u g φ)) (piRep u (alphaAct u g ψ)) t
      = lam (n := n) g * cocycle (piRep u φ) (piRep u ψ) t * (lam g)ᴴ := by
  rw [cocycle_piRep u (alphaAct_posDef u hφ g) (alphaAct_posDef u hψ g) t,
    ← alphaAct_cocycle u hφ hψ, ← lam_conj_piRep, cocycle_piRep u hφ hψ]

/-! ## A ação dual β_χ (não-interna relativa a π(A)) -/

variable (chi : G →* ℂ)

/-- A matriz diagonal do caractere: `D_χ = diag(χ(g)·1ₙ)` — o implementador
    da ação dual `β_χ` no espaço amplificado. -/
def Dchi : Matrix (G × n) (G × n) ℂ :=
  Matrix.diagonal fun p => chi p.1

/-- [KERNEL] A LEI DA AÇÃO DUAL: `D_χ·λ_g = χ(g)·(λ_g·D_χ)`. -/
theorem Dchi_mul_lam (g : G) :
    Dchi (n := n) chi * lam g = chi g • (lam g * Dchi chi) := by
  ext p q
  rw [Dchi, Matrix.diagonal_mul, Matrix.smul_apply, Matrix.mul_diagonal]
  simp only [lam_apply]
  split_ifs with h
  · rw [h.1, map_mul]
    simp [mul_comm]
  · simp

/-- [KERNEL] `D_χ` COMUTA com toda a álgebra-base `π(A)`: a ação dual fixa
    `π(A)` ponto a ponto (sem exigir unimodularidade). -/
theorem Dchi_comm_piRep (a : Matrix n n ℂ) :
    Dchi (n := n) chi * piRep u a = piRep u a * Dchi chi := by
  ext p q
  simp only [Dchi, Matrix.diagonal_mul, Matrix.mul_diagonal, piRep_apply]
  rcases eq_or_ne p.1 q.1 with h | h
  · simp only [h]
    ring
  · simp only [if_neg h, mul_zero, zero_mul]

/-- [KERNEL] χ unimodular ⟹ `D_χ` é UNITÁRIA. -/
theorem Dchi_mem_unitary (hchi : ∀ g, star (chi g) * chi g = 1) :
    Dchi (n := n) chi ∈ unitary (Matrix (G × n) (G × n) ℂ) := by
  have h1 : star (Dchi (n := n) chi) * Dchi chi = 1 := by
    rw [Matrix.star_eq_conjTranspose, Dchi, diagonal_conjTranspose,
      diagonal_mul_diagonal, ← Matrix.diagonal_one]
    congr 1
    funext p
    simpa using hchi p.1
  exact ⟨h1, mul_eq_one_comm.mp h1⟩

/-- [KERNEL] A AÇÃO DUAL TORCE OS UNITÁRIOS DO GRUPO:
    `β_χ(λ_g) = D_χ·λ_g·D_χᴴ = χ(g)·λ_g` — o espelho do peso dual: quem
    fixa a base inteira ainda VÊ o setor do grupo, pelo caractere. -/
theorem Dchi_conj_lam (hchi : ∀ g, star (chi g) * chi g = 1) (g : G) :
    Dchi (n := n) chi * lam g * (Dchi chi)ᴴ = chi g • lam g := by
  have h1 : Dchi (n := n) chi * (Dchi chi)ᴴ = 1 := by
    have h := (Dchi_mem_unitary (n := n) chi hchi).2
    rwa [Matrix.star_eq_conjTranspose] at h
  have hD : lam (n := n) g * Dchi chi * (Dchi chi)ᴴ = lam g := by
    rw [mul_assoc, h1, mul_one]
  calc Dchi (n := n) chi * lam g * (Dchi chi)ᴴ
      = (chi g • (lam g * Dchi chi)) * (Dchi chi)ᴴ := by rw [Dchi_mul_lam]
    _ = chi g • (lam g * Dchi chi * (Dchi chi)ᴴ) := by
        rw [Matrix.smul_mul]
    _ = chi g • lam g := by rw [hD]

/-- [KERNEL] `β_χ` FIXA `π(A)` (forma conjugada). -/
theorem Dchi_conj_piRep (hchi : ∀ g, star (chi g) * chi g = 1)
    (a : Matrix n n ℂ) :
    Dchi (n := n) chi * piRep u a * (Dchi chi)ᴴ = piRep u a := by
  have h1 : Dchi (n := n) chi * (Dchi chi)ᴴ = 1 := by
    have h := (Dchi_mem_unitary (n := n) chi hchi).2
    rwa [Matrix.star_eq_conjTranspose] at h
  rw [Dchi_comm_piRep, mul_assoc, h1, mul_one]

/-- [KERNEL] A AÇÃO DUAL COMUTA COM O FLUXO DUAL: `D_χ·(πρ)^{it} = (πρ)^{it}·D_χ`
    — `β_χ` é simetria da dinâmica modular do peso dual (no grupo finito
    NÃO há escala de traço; o análogo-ℝ com escala é o core, ABERTO). -/
theorem Dchi_comm_modPow {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) (t : ℝ) :
    Dchi (n := n) chi * modPow (piRep u ρ) t = modPow (piRep u ρ) t * Dchi chi := by
  rw [modPow_piRep u hρ]
  exact Dchi_comm_piRep u chi (modPow ρ t)

/-- [KERNEL] O ESTADO DUAL É INVARIANTE PELA AÇÃO DUAL: `φ̂∘β_χ = φ̂`. -/
theorem gibbs_Dchi (hchi : ∀ g, star (chi g) * chi g = 1)
    (ρ : Matrix n n ℂ) (x : Matrix (G × n) (G × n) ℂ) :
    gibbs (piRep u ρ) (Dchi (n := n) chi * x * (Dchi chi)ᴴ)
      = gibbs (piRep u ρ) x := by
  have hDD : (Dchi (n := n) chi)ᴴ * Dchi chi = 1 := by
    have h := (Dchi_mem_unitary (n := n) chi hchi).1
    rwa [Matrix.star_eq_conjTranspose] at h
  simp only [gibbs]
  calc (piRep u ρ * (Dchi (n := n) chi * x * (Dchi chi)ᴴ)).trace
      = (piRep u ρ * Dchi chi * (x * (Dchi chi)ᴴ)).trace := by
        simp only [mul_assoc]
    _ = (Dchi (n := n) chi * (piRep u ρ * (x * (Dchi chi)ᴴ))).trace := by
        rw [← Dchi_comm_piRep]
        simp only [mul_assoc]
    _ = (piRep u ρ * (x * ((Dchi chi)ᴴ * Dchi chi))).trace := by
        rw [trace_mul_comm]
        simp only [mul_assoc]
    _ = (piRep u ρ * x).trace := by rw [hDD, mul_one]

end

end TGLExt
