import TGLExt.Ergodicity

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# Page e a informação: o balanço da radiação, a conservação unitária e a
  perda monotônica do canal   [TGLExt — v50, gate 9]

O gate: entropia de horizonte, evaporação SEM violar a unitariedade
global, comportamento de Page, e a informação preservada entre
M, C(M) e o canto P_F·C(M)·P_F. O que este arquivo PROVA [KERNEL]:

* ★ **A RADIAÇÃO SABE EXATAMENTE O QUANTO O BURACO SABE**
  (`pure_reductions_trace_eq` + `pure_reductions_balance`): para um
  estado global PURO ψ (matriz M retangular via Schmidt), as duas
  reduções ρ_A = MMᴴ e ρ_B = MᴴM têm o MESMO traço e a MESMA pureza —
  Tr((MMᴴ)²) = Tr((MᴴM)²). É esta simetria que FORÇA a virada de Page:
  a entropia da radiação é limitada pelo lado MENOR;
* ★ **UNITÁRIOS GLOBAIS CONSERVAM A INFORMAÇÃO**
  (`purity_unitary_invariant`): pureza(UxUᴴ) = pureza(x) — a evolução
  global não destrói um bit;
* ★ **O CANAL DISSIPATIVO PERDE PUREZA MONOTONICAMENTE**
  (`purityR_eq` + `dephase_purityR_le`): a pureza de Frobenius é a soma
  dos |x_ij|², e o dephasing (v43) a NÃO AUMENTA — a irreversibilidade
  EFETIVA do canal, coexistindo com a unitariedade global: o mecanismo
  exato pelo qual a evaporação parece térmica sem perder informação;
* ★ **A ENTROPIA É MÁXIMA NO ESPELHO** (`entropy_max_at_half` +
  `entropy_eq_max_iff_half`): binEntropy(p) ≤ binEntropy(½) com
  igualdade SSE p = ½ — o MESMO ponto auto-conjugado da flutuação
  máxima (v49): no espelho x = 1−x, a moeda é justa E a ignorância é
  plena (máximo = log 2 nats = 1 bit — a distinção inteira; NÃO
  confundir com S_∂ = ½ nat, que é outro objeto: a entropia da
  fronteira, não da moeda).

**HONESTIDADE.** Este é o mecanismo algébrico de Page na face finita:
balanço puro, conservação unitária, monotonia do canal, máximo no
espelho. O que NÃO está aqui e segue com estatuto: S_BH = A/4G como
TEOREMA (a casa tem AreaScale [κ=2G, face=G] e S_∂=½ nat; a composição
plena é leitura/futuro); a curva de Page para um MODELO de horizonte
III₁ genuíno (OPEN); o mapa de como a informação atravessa
M → C(M) → canto em regime dinâmico (OPEN). A curva de Page NUMÉRICA
(subida, virada na METADE, descida; S_A = S_B exato) vive no runtime.
β JAMAIS entra aqui. Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]
variable {a b : Type} [Fintype a] [Fintype b] [DecidableEq a] [DecidableEq b]

/-! ## A — pureza: o contador de informação -/

/-- A PUREZA (norma de Frobenius ao quadrado): `pureza(x) = Tr(x·xᴴ)` —
    para densidades hermitianas, `Tr(ρ²)`: o contador quadrático de
    informação (1 = puro; 1/d = máxima ignorância). -/
def purity (x : Matrix n n ℂ) : ℂ := (x * xᴴ).trace

/-- [KERNEL] ★ UNITÁRIOS CONSERVAM A INFORMAÇÃO:
    `pureza(U·x·Uᴴ) = pureza(x)` — a evolução global não perde um bit. -/
theorem purity_unitary_invariant (U x : Matrix n n ℂ)
    (hU : U ∈ unitary (Matrix n n ℂ)) :
    purity (U * x * Uᴴ) = purity x := by
  have h1 : Uᴴ * U = 1 := by
    rw [← Matrix.star_eq_conjTranspose]
    exact (Unitary.mem_iff.mp hU).1
  unfold purity
  have hexp : (U * x * Uᴴ) * (U * x * Uᴴ)ᴴ = U * (x * xᴴ) * Uᴴ := by
    simp only [conjTranspose_mul, conjTranspose_conjTranspose, ← mul_assoc]
    rw [mul_assoc (U * x) Uᴴ U, h1, mul_one]
  rw [hexp, Matrix.trace_mul_cycle, ← mul_assoc, h1, one_mul]

/-! ## B — o balanço de Schmidt: as duas reduções sabem o mesmo -/

/-- [KERNEL] O BALANÇO DOS TRAÇOS: `Tr(M·Mᴴ) = Tr(Mᴴ·M)` — as duas
    reduções do estado puro têm o mesmo peso total. -/
theorem pure_reductions_trace_eq (M : Matrix a b ℂ) :
    (M * Mᴴ).trace = (Mᴴ * M).trace :=
  Matrix.trace_mul_comm M Mᴴ

/-- [KERNEL] ★ O BALANÇO DE PAGE: `Tr((M·Mᴴ)²) = Tr((Mᴴ·M)²)` — as duas
    reduções do estado global PURO têm a MESMA pureza (o mesmo espectro
    de Schmidt): a radiação sabe EXATAMENTE o quanto o buraco sabe. É
    esta simetria que força a virada de Page: S_rad é limitada pelo lado
    menor, sobe até a metade e desce. -/
theorem pure_reductions_balance (M : Matrix a b ℂ) :
    ((M * Mᴴ) * (M * Mᴴ)).trace = ((Mᴴ * M) * (Mᴴ * M)).trace := by
  calc ((M * Mᴴ) * (M * Mᴴ)).trace
      = (M * (Mᴴ * M * Mᴴ)).trace := by simp only [Matrix.mul_assoc]
    _ = ((Mᴴ * M * Mᴴ) * M).trace := Matrix.trace_mul_comm M _
    _ = ((Mᴴ * M) * (Mᴴ * M)).trace := by simp only [Matrix.mul_assoc]

/-! ## C — o canal perde pureza monotonicamente (a irreversibilidade efetiva) -/

/-- A PUREZA REAL (soma dos módulos-quadrados das entradas): a forma
    entrada-a-entrada da norma de Frobenius². -/
def purityR (x : Matrix n n ℂ) : ℝ :=
  ∑ i : n, ∑ j : n, Complex.normSq (x i j)

/-- [KERNEL] A ponte: `pureza(x) = Σᵢⱼ |xᵢⱼ|²` — o traço de x·xᴴ é a soma
    dos módulos-quadrados (a forma de Frobenius da casa). -/
theorem purityR_eq (x : Matrix n n ℂ) : purity x = (purityR x : ℂ) := by
  unfold purity purityR
  rw [Matrix.trace]
  push_cast
  refine Finset.sum_congr rfl fun i _ => ?_
  simp only [Matrix.diag_apply, Matrix.mul_apply, Matrix.conjTranspose_apply]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [Complex.star_def, Complex.mul_conj]

/-- [KERNEL] ★ O CANAL PERDE PUREZA: para taxas e tempo não-negativos,
    `pureza(D_t(x)) ≤ pureza(x)` — o dephasing (v43) NUNCA cria
    informação: a irreversibilidade EFETIVA do canal, que coexiste com a
    conservação unitária global (`purity_unitary_invariant`) — o
    mecanismo de Page: térmico por fora, unitário por dentro. -/
theorem dephase_purityR_le (g : n → n → ℝ) (t : ℝ) (ht : 0 ≤ t)
    (hg : ∀ i j, 0 ≤ g i j) (x : Matrix n n ℂ) :
    purityR (dephase g t x) ≤ purityR x := by
  unfold purityR
  refine Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ => ?_
  have hentry : dephase g t x i j = (Real.exp (-(t * g i j)) : ℂ) * x i j := rfl
  rw [hentry, Complex.normSq_mul]
  have h1 : Complex.normSq ((Real.exp (-(t * g i j)) : ℂ))
      = Real.exp (-(t * g i j)) ^ 2 := by
    rw [Complex.normSq_ofReal, sq]
  rw [h1]
  have h2 : Real.exp (-(t * g i j)) ≤ 1 := by
    rw [Real.exp_le_one_iff]
    have := mul_nonneg ht (hg i j)
    linarith
  have h3 : 0 < Real.exp (-(t * g i j)) := Real.exp_pos _
  have h4 : Real.exp (-(t * g i j)) ^ 2 ≤ 1 := by nlinarith
  nlinarith [Complex.normSq_nonneg (x i j)]

/-! ## D — a entropia é máxima no espelho (o mesmo ½ da flutuação) -/

/-- [KERNEL] ★ A ENTROPIA BINÁRIA É MÁXIMA NA MEIA: `H(p) ≤ H(½)` — a
    ignorância é plena exatamente no ponto auto-conjugado (o MESMO ½ da
    flutuação máxima, v49). O valor é log 2 nats = 1 bit: a distinção
    inteira. -/
theorem entropy_max_at_half (p : ℝ) :
    Real.binEntropy p ≤ Real.binEntropy 2⁻¹ := by
  have h : Real.binEntropy 2⁻¹ = Real.log 2 := by simp
  rw [h]
  exact Real.binEntropy_le_log_two

/-- [KERNEL] ★ E SOMENTE NA MEIA: `H(p) = H(½) ⟺ p = ½` — o máximo da
    entropia caracteriza o espelho x = 1−x, como o máximo da flutuação
    (v49): duas leis, o mesmo ponto fixo. -/
theorem entropy_eq_max_iff_half (p : ℝ) :
    Real.binEntropy p = Real.binEntropy 2⁻¹ ↔ p = 2⁻¹ := by
  have h : Real.binEntropy 2⁻¹ = Real.log 2 := by simp
  rw [h]
  exact Real.binEntropy_eq_log_two

end

end TGLExt
