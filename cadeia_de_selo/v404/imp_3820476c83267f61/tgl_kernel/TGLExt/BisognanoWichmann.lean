import TGLExt.Ergodicity

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# Bisognano–Wichmann na face finita: a geometria do boost e o gerador
  modular a 2π   [TGLExt — v47, o gate 4 do roadmap]

O gate: "fluxo modular local = fluxo causal geométrico local". As DUAS
METADES kernelizáveis hoje:

* **A GEOMETRIA DO BOOST** (a metade causal): `boost s` em 1+1
  (coordenadas (x,t), forma de Minkowski η = diag(1,−1)):
  - grupo a um parâmetro (`boost_zero`, `boost_add`);
  - ISOMETRIA de Minkowski (`boost_preserves_eta`: BᵀηB = η) com det 1;
  - os RAIOS NULOS são autodireções com dilatação `e^{±s}`
    (`boost_null_expand/contract`) — **a MESMA forma exponencial da
    escala do traço `τ∘θ_s = e^{−s}τ` (v45): a face geométrica da
    escala de Takesaki** [leitura; a identificação física é o BW];
  - PRESERVAÇÃO DA CUNHA (`boost_preserves_wedge`): `|t| < x` é
    invariante — o boost é o fluxo causal DA cunha.

* **O GERADOR MODULAR A 2π** (a metade modular): para o estado de Gibbs
  `ρ = exp(−2π•K)` com `K` autoadjunto:
  - `logRho_gibbs_boost`: `log ρ = −2π•K` (CFC.log_exp);
  - `modPow_gibbs_boost`: `ρ^{it} = exp(−2πt·i•K)` — **o fluxo modular
    percorre o grupo gerado por K com velocidade 2π** — a temperatura de
    Unruh `T = 1/2π` (em unidades do gerador) como TEOREMA da face
    finita;
  - `sigma_gibbs_boost`: `σ_t = Ad(exp(−2πt·i•K))`.

**HONESTIDADE.** A IDENTIFICAÇÃO das duas metades — K = gerador do boost
da cunha na AQFT genuína, Δ^{it}_W = U(Λ_W(2πt)) — é o teorema de
Bisognano–Wichmann [KNOWN, 1975/76, campos de Wightman; wedges]. O que
segue ABERTO (o resíduo real do gate 4): a identificação ALÉM das cunhas
(regiões gerais/não-Killing — a rota nomeada é inclusões modulares
meio-laterais de Wiesbrock/CGMA de Buchholz–Summers, §16 do
TGL_COCYCLE_GRAVITON_PLANE_EXACTNESS.md) e a reconstrução da métrica a
partir dos dados modulares. Aqui vivem as duas metades EM KERNEL, com a
costura declarada. β JAMAIS entra. Sem sorry, sem axiom. Negativo
honesto é resultado.
-/

namespace TGLExt

open Matrix NormedSpace

noncomputable section

/-! ## A — a geometria do boost (a metade causal) -/

/-- O BOOST em 1+1, coordenadas (x, t):
    `B(s) = [[cosh s, sinh s], [sinh s, cosh s]]`. -/
def boost (s : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cosh s, Real.sinh s; Real.sinh s, Real.cosh s]

/-- A forma de Minkowski `η = diag(1, −1)` (assinatura x²−t²). -/
def minkEta : Matrix (Fin 2) (Fin 2) ℝ := !![1, 0; 0, -1]

/-- `B(0) = 1`. -/
theorem boost_zero : boost 0 = 1 := by
  unfold boost
  ext i j
  fin_cases i <;> fin_cases j <;> simp

/-- [KERNEL] LEI DE GRUPO DO BOOST: `B(s)·B(t) = B(s+t)` — o fluxo causal
    da cunha é um grupo a um parâmetro (adição hiperbólica). -/
theorem boost_add (s t : ℝ) : boost s * boost t = boost (s + t) := by
  unfold boost
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Real.cosh_add, Real.sinh_add] <;>
    ring

/-- [KERNEL] O BOOST É ISOMETRIA DE MINKOWSKI: `B(s)ᵀ·η·B(s) = η` —
    a causalidade é preservada (cosh² − sinh² = 1). -/
theorem boost_preserves_eta (s : ℝ) :
    (boost s)ᵀ * minkEta * boost s = minkEta := by
  unfold boost minkEta
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two] <;>
    nlinarith [Real.cosh_sq_sub_sinh_sq s]

/-- [KERNEL] `det B(s) = 1`: orientação preservada (isometria própria). -/
theorem boost_det (s : ℝ) : (boost s).det = 1 := by
  unfold boost
  rw [Matrix.det_fin_two_of]
  nlinarith [Real.cosh_sq_sub_sinh_sq s]

/-- [KERNEL] ★ O RAIO NULO FUTURO DILATA: `B(s)·(1,1) = e^s·(1,1)` — o
    horizonte é autodireção do boost com autovalor `e^s`. A MESMA forma
    exponencial da escala do traço `τ∘θ_s = e^{−s}τ` (v45): a face
    geométrica da escala de Takesaki. -/
theorem boost_null_expand (s : ℝ) :
    (boost s).mulVec ![1, 1] = Real.exp s • ![1, 1] := by
  unfold boost
  funext i
  fin_cases i <;>
    simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two, ← Real.cosh_add_sinh]

/-- [KERNEL] ★ O RAIO NULO PASSADO CONTRAI: `B(s)·(1,−1) = e^{−s}·(1,−1)`. -/
theorem boost_null_contract (s : ℝ) :
    (boost s).mulVec ![1, -1] = Real.exp (-s) • ![1, -1] := by
  unfold boost
  funext i
  fin_cases i <;>
    simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two] <;>
    rw [← Real.cosh_sub_sinh] <;> ring

/-- [KERNEL] ★ O BOOST PRESERVA A CUNHA: `|t| < x ⟹ |t'| < x'` — a cunha
    direita `W = {(x,t) : |t| < x}` é invariante pelo seu fluxo causal
    (nas coordenadas nulas `u = x+t`, `v = x−t`: `u' = e^s u > 0`,
    `v' = e^{−s} v > 0`). -/
theorem boost_preserves_wedge (s x t : ℝ) (h : |t| < x) :
    |(boost s).mulVec ![x, t] 1| < (boost s).mulVec ![x, t] 0 := by
  have hu : 0 < x + t := by
    rcases abs_lt.mp h with ⟨h1, _⟩
    linarith
  have hv : 0 < x - t := by
    rcases abs_lt.mp h with ⟨_, h2⟩
    linarith
  have hx' : (boost s).mulVec ![x, t] 0 = Real.cosh s * x + Real.sinh s * t := by
    unfold boost
    simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  have ht' : (boost s).mulVec ![x, t] 1 = Real.sinh s * x + Real.cosh s * t := by
    unfold boost
    simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  rw [hx', ht', abs_lt]
  constructor
  · have hkey : 0 < Real.exp s * (x + t) := mul_pos (Real.exp_pos s) hu
    rw [← Real.cosh_add_sinh] at hkey
    nlinarith
  · have hkey : 0 < Real.exp (-s) * (x - t) := mul_pos (Real.exp_pos (-s)) hv
    rw [← Real.cosh_sub_sinh] at hkey
    nlinarith

/-! ## B — o gerador modular a 2π (a metade modular) -/

variable {n : Type} [Fintype n] [DecidableEq n]

section TwoPiGenerator

open scoped Matrix.Norms.L2Operator

/-- [KERNEL] O GERADOR DO ESTADO DE GIBBS: `log(exp(−2π•K)) = −2π•K` —
    o logaritmo modular do estado térmico devolve o gerador na
    normalização de Unruh (CFC.log_exp sobre o autoadjunto real-escalado). -/
theorem logRho_gibbs_boost (K : Matrix n n ℂ) (hK : IsSelfAdjoint K) :
    logRho (exp ((-(2 * Real.pi) : ℝ) • K)) = (-(2 * Real.pi) : ℝ) • K := by
  have hsa : IsSelfAdjoint ((-(2 * Real.pi) : ℝ) • K) := by
    rw [IsSelfAdjoint, star_smul, star_trivial]
    exact congrArg _ hK
  have h : logRho (exp ((-(2 * Real.pi) : ℝ) • K)) =
      CFC.log (exp ((-(2 * Real.pi) : ℝ) • K)) := rfl
  rw [h]
  exact CFC.log_exp _ hsa

/-- [KERNEL] ★ O FLUXO MODULAR PERCORRE K A VELOCIDADE 2π:
    `ρ^{it} = exp(−2πt·i•K)` para `ρ = exp(−2π•K)` — a metade modular do
    BW na face finita: o parâmetro modular `t` é o parâmetro do grupo
    gerado por `K` reescalado por 2π (a temperatura de Unruh `1/2π`).
    A identificação `K = gerador do boost da cunha` é [KNOWN, BW 1975/76]
    na AQFT genuína; além das cunhas segue ABERTA. -/
theorem modPow_gibbs_boost (K : Matrix n n ℂ) (hK : IsSelfAdjoint K) (t : ℝ) :
    modPow (exp ((-(2 * Real.pi) : ℝ) • K)) t
      = exp ((((-(2 * Real.pi) * t : ℝ) : ℂ) * Complex.I) • K) := by
  unfold modPow
  rw [logRho_gibbs_boost K hK]
  have htower : (-(2 * Real.pi) : ℝ) • K = ((-(2 * Real.pi) : ℝ) : ℂ) • K := by
    rw [← algebraMap_smul ℂ (-(2 * Real.pi) : ℝ) K]
    norm_num
  rw [htower, smul_smul]
  congr 2
  push_cast
  ring

/-- [KERNEL] O FLUXO DO ESTADO TÉRMICO É A CONJUGAÇÃO PELO GRUPO DE K:
    `σ_t(a) = e^{−2πt·i•K} · a · e^{2πt·i•K}` — a dinâmica modular do
    Gibbs é EXATAMENTE o fluxo gerado por K (Ad do grupo a velocidade 2π). -/
theorem sigma_gibbs_boost (K : Matrix n n ℂ) (hK : IsSelfAdjoint K)
    (t : ℝ) (a : Matrix n n ℂ) :
    sigma (exp ((-(2 * Real.pi) : ℝ) • K)) t a
      = exp ((((-(2 * Real.pi) * t : ℝ) : ℂ) * Complex.I) • K) * a
        * exp ((((2 * Real.pi * t : ℝ) : ℂ) * Complex.I) • K) := by
  unfold sigma
  rw [modPow_gibbs_boost K hK t, modPow_gibbs_boost K hK (-t)]
  have harg : (-(2 * Real.pi) * -t : ℝ) = 2 * Real.pi * t := by ring
  rw [harg]

end TwoPiGenerator

end

end TGLExt
