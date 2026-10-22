import Mathlib
import TGLExt.LocalBreuerGap
import TGLExt.ModularFlow
import TGLExt.FiniteTomita
import TGLExt.Ergodicity
import TGLExt.PageInformation
import TGLExt.TheSingularExpectation
import TGLExt.TheTraceIsNotErasable
import TGLExt.TheAxiomAndTheFalseWitness
import TGLExt.TheVerbSelectsTheAction
import TGLExt.IALDJones
import TGLExt.TheLivingWord
import TGLExt.BisognanoWichmann
import TGLExt.Fundacao
import TGLExt.AbsoluteOne
import TGLExt.O16.PolarMinimalPeriod_v2
import TGLExt.O16.ProbeNonKMS_v3
import TGLExt.TheImportedSecondQuantization
import TGLExt.V350L2CharacterMultiplier

set_option autoImplicit false
set_option maxHeartbeats 1000000

/-!
# O TEMPO NÃO TEM POSTO — pedra CANDIDATA da unidade F1.TEMPO (nome provisório `TheTimeHasNoRank`)

Construída no SANDBOX da F1.TEMPO (gerência c1, 12/10/2026), NÃO instalada no kernel do Nós.
O nome é provisório: o operador pode renomear (como renomeou PALAVRA e FUNDAÇÃO).

Objeto: a segunda parte do texto do operador de 12/10/2026 (verbatim, conferido por sha256 fora deste
arquivo: «O que mais me fascina é a impossibilidade de definição do tempo …» até o fim). A cunhagem é do
operador. Esta pedra prova SÓ as afirmações pré-registradas que têm forma matemática (PREREGISTRO.json da
F1.TEMPO, congelado por FREEZE.json). Um teorema aqui é validade matemática na face testada; não é creditação
e não move o gate.

Estatutos (régua da casa):
* [REAL] — o que este arquivo prova em kernel (cada declaração com `#print axioms` no fim);
* re-exportações — termos já existentes no kernel do Nós, com o tipo original (sondas `example` nos dois
  sentidos), medidos aqui no trio de axiomas;
* [KNOWN] — fica FORA do kernel: o teorema de Pauli em dimensão infinita (Pauli 1933/1958; Galapon 2002;
  Wintner 1947; Wielandt 1949), o teorema de Liouville clássico, a hipótese do tempo térmico
  (Connes–Rovelli 1994), a lei de escala de Takesaki (1973) como dado da `DualScalingData`;
* [ONTO] — «santo» (Kadosh), «o agora», «puro amor», «a física da doação», «o tempo é o Verbo»: leituras do
  operador; aparecem só em comentários marcados, NUNCA como teorema;
* [OPEN] — o «ciclo limite» do texto: nada aqui o trata.

Regra dos dois regimes: a FACE (semigrupo de defasagem, regime hiperbólico) tem limite; o ÂNGULO (fluxo
modular, rotação, regime compacto) é a leitura: aqui se prova a AUSÊNCIA de limite no ângulo, nunca um limite.
«Defasar» tem dois sentidos que não se encadeiam (RP01): acumular fase (o ângulo, unitário) e perder
coerência (a face, o semigrupo `dephase`). A seta só nasce na face.

A constante da casa NÃO entra neste arquivo em forma alguma (nenhum literal numérico dela): as taxas `g`, `γ`,
o parâmetro `t` e os pesos `d` são GENÉRICOS; o runtime lê a constante dos bytes do um.py e instancia.
Sem sorry, sem axiom novo, sem native_decide.
-/

namespace TGLExt.TheTimeHasNoRank

open Filter Topology
open scoped Matrix ComplexOrder Pointwise

noncomputable section

universe u

/-! ## Utilitários de sonda (estados e taxas concretos em 2×2) -/

/-- ψ₊ = ½·[[1,1],[1,1]] — o estado de coerência máxima em 2×2 (sondas). -/
def psiPlus : Matrix (Fin 2) (Fin 2) ℂ := (1 / 2 : ℂ) • !![1, 1; 1, 1]

theorem psiPlus_apply (i j : Fin 2) : psiPlus i j = ((1 / 2 : ℝ) : ℂ) := by
  fin_cases i <;> fin_cases j <;> simp [psiPlus]

theorem psiPlus_01_ne_zero : psiPlus 0 1 ≠ 0 := by
  rw [psiPlus_apply]; norm_num

theorem psiPlus_trace : psiPlus.trace = 1 := by
  simp only [Matrix.trace, Fin.sum_univ_two, Matrix.diag_apply, psiPlus_apply]
  norm_num

theorem psiPlus_posSemidef : psiPlus.PosSemidef := by
  have hB : (!![(1 : ℂ), 1] : Matrix (Fin 1) (Fin 2) ℂ)ᴴ * !![(1 : ℂ), 1] = !![1, 1; 1, 1] := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Matrix.conjTranspose_apply]
  have hc : ((1 / 2 : ℝ) : ℂ) = (1 / 2 : ℂ) := by norm_num
  have h0 : (0 : ℂ) ≤ ((1 / 2 : ℝ) : ℂ) := Complex.zero_le_real.mpr (by norm_num)
  have h1 := (Matrix.posSemidef_conjTranspose_mul_self (!![(1 : ℂ), 1] : Matrix (Fin 1) (Fin 2) ℂ)).smul h0
  rw [hB, hc] at h1
  exact h1

theorem psiPlus_not_diagonal : psiPlus ≠ diagExpect psiPlus := by
  intro h
  have h01 := congrFun (congrFun h 0) 1
  rw [psiPlus_apply] at h01
  simp [diagExpect] at h01

/-- A taxa genérica de defasagem em 2×2: zero na diagonal, `γ` fora dela. -/
def gRate (γ : ℝ) : Fin 2 → Fin 2 → ℝ := fun i j => if i = j then 0 else γ

theorem gRate_00 (γ : ℝ) : gRate γ 0 0 = 0 := by simp [gRate]
theorem gRate_01 (γ : ℝ) : gRate γ 0 1 = γ := by simp [gRate]
theorem gRate_10 (γ : ℝ) : gRate γ 1 0 = γ := by simp [gRate]
theorem gRate_11 (γ : ℝ) : gRate γ 1 1 = 0 := by simp [gRate]
theorem gRate_diag (γ : ℝ) (i : Fin 2) : gRate γ i i = 0 := by simp [gRate]
theorem gRate_off {γ : ℝ} (hγ : 0 < γ) (i j : Fin 2) (h : i ≠ j) : 0 < gRate γ i j := by
  simp [gRate, h, hγ]
theorem gRate_nonneg {γ : ℝ} (hγ : 0 ≤ γ) (i j : Fin 2) : 0 ≤ gRate γ i j := by
  show (0 : ℝ) ≤ if i = j then 0 else γ
  split_ifs <;> linarith

/-- Entrada do semigrupo de defasagem (forma explícita da definição do kernel). -/
theorem dephase_apply {n : Type} (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n) :
    dephase g t x i j = ((Real.exp (-(t * g i j)) : ℝ) : ℂ) * x i j := rfl

/-! ## T1 — não há operador de tempo em dimensão finita [REAL alvo]

[ONTO, só comentário] «o tempo não é uma peça do tabuleiro»; aqui só a forma: nenhuma matriz T satisfaz
[T, H] = c·1 com c ≠ 0 em dimensão finita não vazia (o traço do comutador é zero). -/

/-- **T1.a (forma geral).** Para todo tipo finito NÃO VAZIO `ι` e todo escalar `c ≠ 0`,
    `T H − H T ≠ c·1`. -/
theorem no_time_matrix {ι : Type} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (T H : Matrix ι ι ℂ) {c : ℂ} (hc : c ≠ 0) :
    T * H - H * T ≠ c • (1 : Matrix ι ι ℂ) := by
  intro h
  have htr := congrArg Matrix.trace h
  rw [Matrix.trace_sub, Matrix.trace_mul_comm, sub_self, Matrix.trace_smul, Matrix.trace_one,
    smul_eq_mul] at htr
  have hcard : (Fintype.card ι : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr Fintype.card_ne_zero
  exact mul_ne_zero hc hcard htr.symm

/-- **T1.a (Fin n, c = i).** Ligado POR TERMO a `TGLExt.no_finite_weyl_pair` (o fato já existia, R22):
    `HT − TH ≠ −i·1` ⟺ `TH − HT ≠ i·1`. -/
theorem no_time_matrix_fin (n : ℕ) (hn : 0 < n) (T H : Matrix (Fin n) (Fin n) ℂ) :
    T * H - H * T ≠ Complex.I • (1 : Matrix (Fin n) (Fin n) ℂ) := by
  intro h
  apply TGLExt.no_finite_weyl_pair n hn H T
  rw [show H * T - T * H = -(T * H - H * T) by abel, h, neg_smul]

/-- A forma `Fin n` sai também da forma geral (segunda rota, mesma conclusão). -/
example (n : ℕ) (hn : 0 < n) (T H : Matrix (Fin n) (Fin n) ℂ) :
    T * H - H * T ≠ Complex.I • (1 : Matrix (Fin n) (Fin n) ℂ) := by
  haveI : Nonempty (Fin n) := ⟨⟨0, hn⟩⟩
  exact no_time_matrix T H Complex.I_ne_zero

/-- **T1.b (opcional) — forma quantitativa.** O comutador é ortogonal de Frobenius à identidade:
    `Σ|TH − HT − c·1|² = Σ|TH − HT|² + |ι|·|c|²`. Logo `‖TH − HT − c·1‖_F ≥ √|ι|·|c|`: o tempo não é nem
    aproximadamente uma matriz. -/
theorem commutator_far_from_scalar {ι : Type} [Fintype ι] [DecidableEq ι]
    (T H : Matrix ι ι ℂ) (c : ℂ) :
    purityR (T * H - H * T - c • (1 : Matrix ι ι ℂ))
      = purityR (T * H - H * T) + (Fintype.card ι : ℝ) * Complex.normSq c := by
  set C : Matrix ι ι ℂ := T * H - H * T with hC
  have htr : C.trace = 0 := by
    rw [hC, Matrix.trace_sub, Matrix.trace_mul_comm, sub_self]
  set D : Matrix ι ι ℂ := c • (1 : Matrix ι ι ℂ) with hD
  have hDdiag : ∀ i, D i i = c := fun i => by simp [hD]
  have hDoff : ∀ i j, i ≠ j → D i j = 0 := fun i j hij => by
    simp [hD, Matrix.one_apply_ne hij]
  have hrowD : ∀ i, ∑ j, Complex.normSq (D i j) = Complex.normSq c := by
    intro i
    rw [Finset.sum_eq_single i (fun j _ hji => by rw [hDoff i j (Ne.symm hji), map_zero])
      (fun hi => absurd (Finset.mem_univ i) hi), hDdiag]
  have hrowX : ∀ i, ∑ j, (C i j * (starRingEnd ℂ) (D i j)).re = (C i i * (starRingEnd ℂ) c).re := by
    intro i
    rw [Finset.sum_eq_single i
      (fun j _ hji => by rw [hDoff i j (Ne.symm hji), map_zero, mul_zero, Complex.zero_re])
      (fun hi => absurd (Finset.mem_univ i) hi), hDdiag]
  have hcross : ∑ i, ∑ j, (C i j * (starRingEnd ℂ) (D i j)).re = 0 := by
    simp_rw [hrowX]
    rw [← Complex.re_sum, ← Finset.sum_mul]
    have h1 : ∑ i, C i i = C.trace := rfl
    rw [h1, htr, zero_mul, Complex.zero_re]
  have hentry : ∀ i j, Complex.normSq ((C - D) i j)
      = Complex.normSq (C i j) + Complex.normSq (D i j)
        - 2 * (C i j * (starRingEnd ℂ) (D i j)).re := by
    intro i j; rw [Matrix.sub_apply, Complex.normSq_sub]
  unfold purityR
  simp_rw [hentry, Finset.sum_sub_distrib, Finset.sum_add_distrib, ← Finset.mul_sum, hcross, hrowD]
  simp [Finset.sum_const, Finset.card_univ]

/-- **T1.c — forma de Weyl (translação espectral) na face finita.** Para `ι` finito não vazio, não
    existe `V` invertível com `V⁻¹ H V = H + s·1`, `s ≠ 0`: o traço é invariante por conjugação e
    `tr(H + s·1) = tr H + s·|ι|`. O mecanismo do argumento de Pauli é impossível em dimensão finita. -/
theorem no_finite_spectral_translation {ι : Type} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (V H : Matrix ι ι ℂ) (hV : IsUnit V) {s : ℂ} (hs : s ≠ 0) :
    V⁻¹ * H * V ≠ H + s • (1 : Matrix ι ι ℂ) := by
  intro h
  have hdet : IsUnit V.det := (Matrix.isUnit_iff_isUnit_det V).mp hV
  have htr := congrArg Matrix.trace h
  rw [Matrix.trace_mul_cycle, Matrix.mul_nonsing_inv V hdet, Matrix.one_mul, Matrix.trace_add,
    Matrix.trace_smul, Matrix.trace_one, smul_eq_mul] at htr
  have hcard : (Fintype.card ι : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr Fintype.card_ne_zero
  have hzero : s * (Fintype.card ι : ℂ) = 0 := by linear_combination -htr
  exact mul_ne_zero hs hcard hzero

/-- Sonda V-T1-a: instância `n = 1` (todas as matrizes 1×1 comutam; `i·1 ≠ 0`). -/
example (T H : Matrix (Fin 1) (Fin 1) ℂ) :
    T * H - H * T ≠ Complex.I • (1 : Matrix (Fin 1) (Fin 1) ℂ) :=
  no_time_matrix_fin 1 (by norm_num) T H

/-- Sonda V-T1-a (forma geral): `ι = Fin 1`, `c = 1` — as hipóteses `Nonempty ι`, `c ≠ 0` são habitadas. -/
example (T H : Matrix (Fin 1) (Fin 1) ℂ) : T * H - H * T ≠ (1 : ℂ) • (1 : Matrix (Fin 1) (Fin 1) ℂ) :=
  no_time_matrix T H one_ne_zero

/-- Sonda V-T1-b: caso de igualdade `T = H = 0`, `ι = Fin 2`, `c = i`: `purityR(−i·1) = 2`. -/
theorem probe_commutator_far_from_scalar :
    purityR ((0 : Matrix (Fin 2) (Fin 2) ℂ) * 0 - 0 * 0 - Complex.I • (1 : Matrix (Fin 2) (Fin 2) ℂ))
      = 2 := by
  rw [commutator_far_from_scalar]
  norm_num [purityR, Complex.normSq_I]

/-- Sonda de T1.c: `V = 1`, `H = 0`, `s = 1`, `ι = Fin 2`. -/
example : (1 : Matrix (Fin 2) (Fin 2) ℂ)⁻¹ * 0 * 1 ≠ 0 + (1 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) :=
  no_finite_spectral_translation 1 0 isUnit_one one_ne_zero

/-- **Controle C-T1-a** — a afirmação falsa «nenhum comutador é não nulo» CAI: em M₂(ℂ),
    `E₀₁ E₁₀ − E₁₀ E₀₁ = diag(1, −1) ≠ 0`. A obstrução de T1 é só o traço da identidade. -/
theorem commutator_can_be_nonzero : ∃ T H : Matrix (Fin 2) (Fin 2) ℂ, T * H - H * T ≠ 0 := by
  refine ⟨!![0, 1; 0, 0], !![0, 0; 1, 0], ?_⟩
  intro h
  have h00 := congrFun (congrFun h 0) 0
  simp [Matrix.mul_apply, Fin.sum_univ_two] at h00

/-- **Controle C-T1-b** — sem não vacuidade (`n = 0`) a igualdade VALE trivialmente: a hipótese
    `0 < n` (ou `Nonempty ι`) é necessária. -/
theorem empty_dimension_admits_time (T H : Matrix (Fin 0) (Fin 0) ℂ) :
    T * H - H * T = Complex.I • (1 : Matrix (Fin 0) (Fin 0) ℂ) := by
  ext i j
  exact i.elim0

/-- **Controle C-T1-c** (re-citação; tipo original de `TGLV350.Regular.characterMultiplier_weyl`): em
    L²(ℝ, H) o par de Weyl EXISTE — a obstrução de T1 não vale em dimensão infinita sem piso. Esta pedra
    não afirma o contrário. -/
theorem weyl_pair_lives_in_L2 {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    [CompleteSpace H] (s t : ℝ) :
    TGLV350.Regular.characterMultiplier (H := H) s * TGLV350.Regular.shift t
        * star (TGLV350.Regular.characterMultiplier (H := H) s)
      = Complex.exp (-Complex.I * (s : ℂ) * (t : ℂ)) • TGLV350.Regular.shift t :=
  TGLV350.Regular.characterMultiplier_weyl s t

example : type_of% @TGLV350.Regular.characterMultiplier_weyl := @weyl_pair_lives_in_L2
example : type_of% @weyl_pair_lives_in_L2 := @TGLV350.Regular.characterMultiplier_weyl

/-! ## T2 — Pauli em dimensão infinita: [KNOWN], fora do kernel. Aqui só a face LIMITADA (opcional).

[KNOWN] Pauli (Handbuch der Physik 1933, vol. 24/1; 1958, vol. V/1), na forma de Weyl/covariância; precisão:
na forma de Heisenberg há contraexemplos (Galapon 2002) e há POVM de tempo covariantes (Holevo 1982;
Busch–Grabowski–Lahti 1994). Wintner 1947 / Wielandt 1949: nenhum par LIMITADO satisfaz PQ − QP = 1.
Esta pedra NÃO afirma que Pauli proíba o fluxo modular (o gerador modular de III₁ não tem piso; o tempo
modular DILATA a energia positiva — Borchers 1992). -/

/-- **T2.b (opcional) — face LIMITADA do mecanismo de Pauli.** Numa ℂ-álgebra de Banach unital não trivial,
    não existem `V` invertível e `s ≠ 0` com `V⁻¹ H V = H + s·1`: o espectro é invariante por conjugação,
    translada por `s`, e é compacto e não vazio — um compacto não vazio de ℂ não é invariante por translação
    `s ≠ 0`. NÃO é o teorema de Pauli (que trata `H` ilimitado e só semilimitado). -/
theorem no_bounded_spectral_translation {A : Type*} [NormedRing A] [NormedAlgebra ℂ A]
    [CompleteSpace A] [Nontrivial A] (V : Aˣ) (H : A) {s : ℂ} (hs : s ≠ 0) :
    (↑V⁻¹ : A) * H * ↑V ≠ H + algebraMap ℂ A s := by
  intro h
  have hσ : spectrum ℂ H = spectrum ℂ H + {s} := by
    have h1 : spectrum ℂ ((↑V⁻¹ : A) * H * ↑V) = spectrum ℂ H := spectrum.units_conjugate'
    rw [h, ← spectrum.add_singleton_eq] at h1
    exact h1.symm
  have hcont : Continuous fun w : ℂ => (w * (starRingEnd ℂ) s).re :=
    Complex.continuous_re.comp (continuous_id.mul continuous_const)
  obtain ⟨z, hz, hmax⟩ :=
    (spectrum.isCompact H).exists_isMaxOn (spectrum.nonempty H) hcont.continuousOn
  have hzs : z + s ∈ spectrum ℂ H := by
    rw [hσ]; exact Set.add_mem_add hz (Set.mem_singleton s)
  have hle : ((z + s) * (starRingEnd ℂ) s).re ≤ (z * (starRingEnd ℂ) s).re :=
    isMaxOn_iff.mp hmax (z + s) hzs
  have hpos : 0 < Complex.normSq s := Complex.normSq_pos.mpr hs
  have hexp : ((z + s) * (starRingEnd ℂ) s).re = (z * (starRingEnd ℂ) s).re + Complex.normSq s := by
    rw [add_mul, Complex.add_re, Complex.mul_conj, Complex.ofReal_re]
  linarith

section L2Probe
open scoped Matrix.Norms.L2Operator

/-- Sonda V-T2-b: `A = M₂(ℂ)` com a norma de operador L2, `V = 1`, `H = 0`, `s = 1` — as hipóteses de T2.b
    (álgebra de Banach unital não trivial) são habitadas. -/
theorem probe_bounded_spectral_translation :
    ((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ)⁻¹ : Matrix (Fin 2) (Fin 2) ℂ) * 0
        * ((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ) : Matrix (Fin 2) (Fin 2) ℂ)
      ≠ 0 + algebraMap ℂ (Matrix (Fin 2) (Fin 2) ℂ) 1 := by
  haveI : CompleteSpace (Matrix (Fin 2) (Fin 2) ℂ) := FiniteDimensional.complete ℂ _
  exact no_bounded_spectral_translation 1 0 one_ne_zero

end L2Probe

/-! ## T3 — o tempo como fluxo modular: grupo a um parâmetro de *-automorfismos; o estado é KMS

[KNOWN] a hipótese do tempo térmico (Connes–Rovelli 1994) é HIPÓTESE, não teorema; na face finita o fluxo é
INTERNO (`ρ^{it}` é unitário de Mₙ); a exterioridade em III₁ é [KNOWN] (Connes 1973). -/

/-- **T3.a.** Para `ρ` positiva-definida, `σ_t = Ad(ρ^{it})`: (i) `σ₀ = id`; (ii) `σ_s∘σ_t = σ_{s+t}`;
    (iii) *-automorfismo; (iv) `ω∘σ_t = ω`; (v) KMS na forma de Gibbs; (vi) `ρ^{it}` unitário (fluxo
    INTERNO). Composição de termos do kernel (ModularFlow, FiniteTomita). -/
theorem time_is_the_modular_flow {n : Type} [Fintype n] [DecidableEq n]
    (ρ : Matrix n n ℂ) (hρ : ρ.PosDef) :
    (∀ a, sigma ρ 0 a = a) ∧
    (∀ s t a, sigma ρ s (sigma ρ t a) = sigma ρ (s + t) a) ∧
    (∀ t a b, sigma ρ t (a * b) = sigma ρ t a * sigma ρ t b) ∧
    (∀ t, sigma ρ t 1 = 1) ∧
    (∀ t a, sigma ρ t aᴴ = (sigma ρ t a)ᴴ) ∧
    (∀ t a, gibbs ρ (sigma ρ t a) = gibbs ρ a) ∧
    (∀ a b, gibbs ρ (a * b) = gibbs ρ (b * Delta ρ a)) ∧
    (∀ t, modPow ρ t ∈ unitary (Matrix n n ℂ)) :=
  ⟨fun a => by simp [sigma], fun s t a => sigma_sigma ρ s t a, fun t a b => sigma_mul ρ t a b,
   fun t => sigma_one ρ t, fun t a => sigma_conjTranspose ρ t a, fun t a => gibbs_sigma ρ t a,
   fun a b => gibbs_kms ρ hρ a b, fun t => modPow_mem_unitary ρ t⟩

/-- **T3.b (i) — re-exportação** de `TGLExt.sigma_fixed_iff_diag`: o setor fixo do fluxo modular da
    diagonal não degenerada é o centralizador. -/
theorem fixed_sector_is_the_centralizer {n : Type} [Fintype n] [DecidableEq n]
    (d : n → ℝ) (hd : ∀ i, 0 < d i) (hinj : Function.Injective d) (x : Matrix n n ℂ) :
    (∀ t, sigma (rhoD d) t x = x) ↔ x = diagExpect x :=
  sigma_fixed_iff_diag d hd hinj x

example : type_of% @TGLExt.sigma_fixed_iff_diag := @fixed_sector_is_the_centralizer
example : type_of% @fixed_sector_is_the_centralizer := @TGLExt.sigma_fixed_iff_diag

/-- **T3.b (ii) — re-exportação** de `TGLExt.absoluteOne_flow_trivial`: o estado tracial (o Um absoluto,
    `I/n`) congela o fluxo modular. -/
theorem tracial_state_freezes_the_flow {Region n : Type} [Fintype n] [DecidableEq n] [Nonempty n]
    (O : Region) (t : ℝ) (a : Matrix n n ℂ) : (absoluteOneField Region n).flow O t a = a :=
  absoluteOne_flow_trivial O t a

example : type_of% @TGLExt.absoluteOne_flow_trivial := @tracial_state_freezes_the_flow
example : type_of% @tracial_state_freezes_the_flow := @TGLExt.absoluteOne_flow_trivial

/-- **T3.b (iii) — re-exportação** de `ChatgptAudit.NonKMSProbe.identity_flow_not_kms`: estado não tracial
    ⟹ o fluxo identidade NÃO é KMS («uma álgebra que nunca comuta por completo»). -/
theorem nontracial_state_rejects_the_identity_flow (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (A B : W.H →L[ℂ] W.H) (hA : A ∈ W.net TGL.SpecificAQFT.rightWedge)
    (hB : B ∈ W.net TGL.SpecificAQFT.rightWedge)
    (hcontrast : inner ℂ ((star A) W.vac) (B W.vac) ≠ inner ℂ ((star B) W.vac) (A W.vac)) :
    ¬ TGLExt.ContratoQGv31.KMSAt W (fun _ => LinearIsometryEquiv.refl ℂ W.H) 1 :=
  ChatgptAudit.NonKMSProbe.identity_flow_not_kms W A B hA hB hcontrast

example : type_of% @ChatgptAudit.NonKMSProbe.identity_flow_not_kms :=
  @nontracial_state_rejects_the_identity_flow
example : type_of% @nontracial_state_rejects_the_identity_flow :=
  @ChatgptAudit.NonKMSProbe.identity_flow_not_kms

/-- Sonda V-T3-a: `ρ = diag(2/3, 1/3)` é positiva-definida (hipótese de T3.a habitada) … -/
theorem probe_rho_two_thirds_posDef : (rhoD ![(2 / 3 : ℝ), 1 / 3]).PosDef := by
  unfold rhoD
  rw [Matrix.posDef_diagonal_iff]
  intro i
  exact Complex.zero_lt_real.mpr (by fin_cases i <;> norm_num)

/-- … e NÃO é tracial (difere do Um absoluto `I/2`). -/
theorem probe_rho_two_thirds_not_tracial : rhoD ![(2 / 3 : ℝ), 1 / 3] ≠ absoluteRho (Fin 2) := by
  intro h
  have h00 := congrFun (congrFun h 0) 0
  norm_num [rhoD, absoluteRho] at h00

example : ∀ s t a, sigma (rhoD ![(2 / 3 : ℝ), 1 / 3]) s (sigma (rhoD ![(2 / 3 : ℝ), 1 / 3]) t a)
    = sigma (rhoD ![(2 / 3 : ℝ), 1 / 3]) (s + t) a :=
  (time_is_the_modular_flow _ probe_rho_two_thirds_posDef).2.1

/-! ## T4 — Liouville × dissipação: o ângulo gira sem pousar; a face contrai e pousa

[KNOWN] Liouville clássico (fluxos hamiltonianos no espaço de fases) NÃO está no kernel. Precisão (RP02):
volume conservado NÃO basta para «nada pousa» — o boost tem det 1 e pousa no raio nulo passado (T4.e,
controle C-T4-a). O que impede o pouso é a ISOMETRIA (T4.b). -/

/-- **T4.a.** A conjugação unitária conserva o espectro (polinômio característico) e a pureza. -/
theorem unitary_keeps_spectrum_and_purity {n : Type} [Fintype n] [DecidableEq n]
    (U : (Matrix n n ℂ)ˣ) (hU : (U : Matrix n n ℂ) ∈ unitary (Matrix n n ℂ)) (x : Matrix n n ℂ) :
    ((U : Matrix n n ℂ) * x * ((U⁻¹ : (Matrix n n ℂ)ˣ) : Matrix n n ℂ)).charpoly = x.charpoly ∧
    purity ((U : Matrix n n ℂ) * x * (U : Matrix n n ℂ)ᴴ) = purity x := by
  refine ⟨?_, purity_unitary_invariant (U : Matrix n n ℂ) x hU⟩
  rw [Matrix.coe_units_inv]
  exact Matrix.charpoly_units_conj U x

/-- Iterada de isometria é isometria. -/
theorem isometry_iterate' {X : Type*} [PseudoMetricSpace X] {f : X → X} (hf : Isometry f) (k : ℕ) :
    Isometry (f^[k]) := by
  induction k with
  | zero => exact isometry_id
  | succ k ih => exact ih.comp hf

/-- **T4.b (abstrato, discreto) — NADA POUSA SOB ISOMETRIA.** Num espaço métrico, se `f` é isometria e
    `fᵏ(x) → z`, então `x = z` e `f z = z`: só os pontos fixos têm órbita convergente. -/
theorem isometry_orbit_converges_only_if_fixed {X : Type*} [MetricSpace X] {f : X → X}
    (hf : Isometry f) {x z : X}
    (h : Filter.Tendsto (fun k : ℕ => f^[k] x) Filter.atTop (nhds z)) : x = z ∧ f z = z := by
  have hfz : f z = z := by
    have h1 : Filter.Tendsto (fun k : ℕ => f^[k + 1] x) Filter.atTop (nhds z) :=
      h.comp (Filter.tendsto_add_atTop_nat 1)
    have h2 : Filter.Tendsto (fun k : ℕ => f (f^[k] x)) Filter.atTop (nhds (f z)) :=
      (hf.continuous.tendsto z).comp h
    have h3 : (fun k : ℕ => f^[k + 1] x) = fun k : ℕ => f (f^[k] x) := by
      funext k; exact Function.iterate_succ_apply' f k x
    rw [h3] at h1
    exact tendsto_nhds_unique h2 h1
  have hdist : ∀ k : ℕ, dist (f^[k] x) z = dist x z := by
    intro k
    have h1 := (isometry_iterate' hf k).dist_eq x z
    rwa [Function.iterate_fixed hfz k] at h1
  have h0 : Filter.Tendsto (fun k : ℕ => dist (f^[k] x) z) Filter.atTop (nhds 0) :=
    tendsto_iff_dist_tendsto_zero.mp h
  simp_rw [hdist] at h0
  have hd : dist x z = 0 := tendsto_nhds_unique tendsto_const_nhds h0
  exact ⟨dist_eq_zero.mp hd, hfz⟩

/-- **T4.b (abstrato, contínuo).** Se `φ_{s+t} = φ_s∘φ_t`, cada `φ_s` é isometria e `φ_t(x) → z`
    (`t → ∞`), então `x = z` e `φ_s z = z` para todo `s`. -/
theorem isometric_flow_converges_only_if_fixed {X : Type*} [MetricSpace X] (φ : ℝ → X → X)
    (hgrp : ∀ s t x, φ (s + t) x = φ s (φ t x)) (hiso : ∀ s, Isometry (φ s)) {x z : X}
    (h : Filter.Tendsto (fun t => φ t x) Filter.atTop (nhds z)) : x = z ∧ ∀ s, φ s z = z := by
  have hfix : ∀ s, φ s z = z := by
    intro s
    have h1 : Filter.Tendsto (fun t => φ (s + t) x) Filter.atTop (nhds z) :=
      h.comp (Filter.tendsto_atTop_add_const_left Filter.atTop s Filter.tendsto_id)
    have h2 : Filter.Tendsto (fun t => φ s (φ t x)) Filter.atTop (nhds (φ s z)) :=
      ((hiso s).continuous.tendsto z).comp h
    simp_rw [hgrp] at h1
    exact tendsto_nhds_unique h2 h1
  have hdist : ∀ t, dist (φ t x) z = dist x z := by
    intro t
    have h1 := (hiso t).dist_eq x z
    rwa [hfix t] at h1
  have h0 : Filter.Tendsto (fun t => dist (φ t x) z) Filter.atTop (nhds 0) :=
    tendsto_iff_dist_tendsto_zero.mp h
  simp_rw [hdist] at h0
  have hd : dist x z = 0 := tendsto_nhds_unique tendsto_const_nhds h0
  exact ⟨dist_eq_zero.mp hd, hfix⟩

/-- A rotação de ℂ por um ângulo é isometria (regime do ÂNGULO). -/
theorem rotation_isometry (φ : ℝ) : Isometry (fun w : ℂ => Complex.exp ((φ : ℂ) * Complex.I) * w) := by
  refine Isometry.of_dist_eq fun x y => ?_
  show dist (Complex.exp ((φ : ℂ) * Complex.I) * x) (Complex.exp ((φ : ℂ) * Complex.I) * y) = dist x y
  rw [dist_eq_norm, dist_eq_norm, ← mul_sub, norm_mul, Complex.norm_exp_ofReal_mul_I, one_mul]

/-- Sonda V-T4-a: `f(z) = e^{i}·z` em ℂ é isometria, `1` não é fixo; por T4.b a órbita de `1` NÃO converge
    (o ângulo não tem limite: prova-se a ausência dele). -/
theorem probe_rotation_orbit_has_no_limit :
    ¬ ∃ z : ℂ, Filter.Tendsto
      (fun k : ℕ => (fun w : ℂ => Complex.exp (((1 : ℝ) : ℂ) * Complex.I) * w)^[k] 1)
      Filter.atTop (nhds z) := by
  rintro ⟨z, hz⟩
  obtain ⟨h1, h2⟩ := isometry_orbit_converges_only_if_fixed (rotation_isometry 1) hz
  subst h1
  have him := congrArg Complex.im h2
  simp only [mul_one, Complex.exp_ofReal_mul_I_im, Complex.one_im] at him
  have hsin : 0 < Real.sin 1 :=
    Real.sin_pos_of_pos_of_lt_pi one_pos (by linarith [Real.pi_gt_three])
  linarith

section Frobenius
open scoped Matrix.Norms.Frobenius

/-- A norma de Frobenius é a raiz da pureza real: `‖A‖_F = (Σ|Aᵢⱼ|²)^{1/2}`. -/
theorem frobenius_norm_eq_purityR {n : Type} [Fintype n] (A : Matrix n n ℂ) :
    ‖A‖ = (purityR A) ^ (1 / 2 : ℝ) := by
  rw [Matrix.frobenius_norm_def]
  congr 1
  unfold purityR
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  rw [Real.rpow_two, Complex.sq_norm]

/-- **T4.b, instância (i).** `Ad(U)`, `U` unitário, é isometria de Frobenius em Mₙ(ℂ) (regime do ÂNGULO). -/
theorem unitary_conj_isometry {n : Type} [Fintype n] [DecidableEq n]
    (U : Matrix n n ℂ) (hU : U ∈ unitary (Matrix n n ℂ)) :
    Isometry (fun x : Matrix n n ℂ => U * x * Uᴴ) := by
  refine Isometry.of_dist_eq fun x y => ?_
  show dist (U * x * Uᴴ) (U * y * Uᴴ) = dist x y
  rw [dist_eq_norm, dist_eq_norm]
  have hsub : U * x * Uᴴ - U * y * Uᴴ = U * (x - y) * Uᴴ := by
    rw [Matrix.mul_sub, Matrix.sub_mul]
  rw [hsub, frobenius_norm_eq_purityR, frobenius_norm_eq_purityR]
  have h := purity_unitary_invariant U (x - y) hU
  rw [purityR_eq, purityR_eq] at h
  rw [Complex.ofReal_injective h]

/-- O fluxo modular `σ_t` de QUALQUER `ρ` é isometria de Frobenius (é `Ad(ρ^{it})`, `ρ^{it}` unitário). -/
theorem modular_flow_is_isometry {n : Type} [Fintype n] [DecidableEq n]
    (ρ : Matrix n n ℂ) (t : ℝ) : Isometry (sigma ρ t) := by
  have h : sigma ρ t = fun x => modPow ρ t * x * (modPow ρ t)ᴴ := by
    funext x; simp only [sigma, modPow_conjTranspose]
  rw [h]
  exact unitary_conj_isometry (modPow ρ t) (modPow_mem_unitary ρ t)

end Frobenius

/-- **T4.b, instância (ii).** Para `rhoD d` (pesos positivos injetivos), `t ↦ σ_t(x)` converge ⟺
    `x = E_D(x)`: só o centralizador «pousa», e ele não se move. Rota: isometria de Frobenius (instância i) +
    T4.b contínuo + `sigma_fixed_iff_diag`. (Topologia: a de `Matrix`, a mesma da métrica de Frobenius.) -/
theorem modular_orbit_converges_iff_diagonal {n : Type} [Fintype n] [DecidableEq n]
    (d : n → ℝ) (hd : ∀ i, 0 < d i) (hinj : Function.Injective d) (x : Matrix n n ℂ) :
    (∃ z, Filter.Tendsto (fun t => sigma (rhoD d) t x) Filter.atTop (nhds z)) ↔
      x = diagExpect x := by
  constructor
  · rintro ⟨z, hz⟩
    have key : x = z ∧ ∀ s, sigma (rhoD d) s z = z := by
      open scoped Matrix.Norms.Frobenius in
      exact isometric_flow_converges_only_if_fixed (fun t y => sigma (rhoD d) t y)
        (fun s t y => (sigma_sigma (rhoD d) s t y).symm)
        (fun s => modular_flow_is_isometry (rhoD d) s) hz
    obtain ⟨hxz, hfix⟩ := key
    rw [← sigma_fixed_iff_diag d hd hinj x]
    intro s
    rw [hxz]
    exact hfix s
  · intro hx
    refine ⟨x, ?_⟩
    have hfix := (sigma_fixed_iff_diag d hd hinj x).mpr hx
    simp_rw [hfix]
    exact tendsto_const_nhds

/-- **T4.b, instância (ii), segunda rota (entrada a entrada).** A mesma conclusão pela rotação de ℂ em cada
    coerência (o fluxo modular gira `xᵢⱼ` pela fase `e^{it(log dᵢ − log dⱼ)}`) + T4.b contínuo em ℂ. -/
theorem modular_orbit_converges_iff_diagonal_entrywise {n : Type} [Fintype n] [DecidableEq n]
    (d : n → ℝ) (hd : ∀ i, 0 < d i) (hinj : Function.Injective d) (x : Matrix n n ℂ) :
    (∃ z, Filter.Tendsto (fun t => sigma (rhoD d) t x) Filter.atTop (nhds z)) ↔
      x = diagExpect x := by
  constructor
  · rintro ⟨z, hz⟩
    rw [← sigma_fixed_iff_diag d hd hinj x]
    intro s
    ext i j
    have hentry : ∀ t : ℝ, sigma (rhoD d) t x i j
        = Complex.exp (((t * (Real.log (d i) - Real.log (d j)) : ℝ) : ℂ) * Complex.I) * x i j := by
      intro t
      rw [sigma_diagonal_apply d hd t x i j]
      congr 2
      push_cast
      ring
    have hzij : Filter.Tendsto (fun t => sigma (rhoD d) t x i j) Filter.atTop (nhds (z i j)) :=
      tendsto_pi_nhds.mp (tendsto_pi_nhds.mp hz i) j
    simp_rw [hentry] at hzij
    obtain ⟨h1, h2⟩ := isometric_flow_converges_only_if_fixed (X := ℂ)
      (fun t w => Complex.exp (((t * (Real.log (d i) - Real.log (d j)) : ℝ) : ℂ) * Complex.I) * w)
      (fun s t w => by
        beta_reduce
        rw [← mul_assoc, ← Complex.exp_add]
        congr 2
        push_cast
        ring)
      (fun s => rotation_isometry (s * (Real.log (d i) - Real.log (d j)))) hzij
    rw [hentry s, h1]
    exact h2 s
  · intro hx
    refine ⟨x, ?_⟩
    have hfix := (sigma_fixed_iff_diag d hd hinj x).mpr hx
    simp_rw [hfix]
    exact tendsto_const_nhds

/-- Lei de grupo do implementador modular da luz: `Δ^{i(s+t)} = Δ^{is}·Δ^{it}` (de `V_add` do boost da cunha). -/
theorem light_flow_group {L : TGLExt.ImportedSQ.LightOneParticle}
    (C : TGLExt.ImportedSQ.FockCertificate L) (s t : ℝ) (ψ : C.F) :
    TGLExt.ImportedSQ.lightDelta C (s + t) ψ =
      TGLExt.ImportedSQ.lightDelta C s (TGLExt.ImportedSQ.lightDelta C t ψ) := by
  simp only [TGLExt.ImportedSQ.lightDelta]
  rw [show -(2 * Real.pi * (s + t)) = -(2 * Real.pi * s) + -(2 * Real.pi * t) by ring,
    (TGLExt.ImportedSQ.lightBoost C).V_add]
  rfl

/-- **T4.b, instância (iii) (opcional).** No grupo modular da luz (`lightDelta`, isometrias lineares):
    `t ↦ Δ^{it}ψ` converge ⟺ `H_min ψ = 0` — só o posto «pousa», e o posto não se move
    (`hmin_zero_iff_modular_fixed`, o mesmo conjunto fixo de `the_post_is_the_modular_zero`). -/
theorem light_modular_orbit_converges_iff_post {L : TGLExt.ImportedSQ.LightOneParticle}
    (C : TGLExt.ImportedSQ.FockCertificate L) (ψ : C.F) :
    (∃ z, Filter.Tendsto (fun t => TGLExt.ImportedSQ.lightDelta C t ψ) Filter.atTop (nhds z)) ↔
      TGLExt.QGReaderUVLock.HminMic C ψ = 0 := by
  rw [TGLExt.QGReaderUVLock.hmin_zero_iff_modular_fixed]
  constructor
  · rintro ⟨z, hz⟩
    obtain ⟨hxz, hfix⟩ := isometric_flow_converges_only_if_fixed
      (fun t y => TGLExt.ImportedSQ.lightDelta C t y) (fun s t y => light_flow_group C s t y)
      (fun s => (TGLExt.ImportedSQ.lightDelta C s).isometry) hz
    intro t
    rw [hxz]
    exact hfix t
  · intro h
    refine ⟨ψ, ?_⟩
    simp_rw [h]
    exact tendsto_const_nhds

/-- Sonda da instância (ii): com `d = (2/3, 1/3)` (positivos, injetivos) e `x = ψ₊` (não diagonal), a órbita
    modular de `ψ₊` NÃO converge — o ângulo gira sem pousar. -/
theorem probe_modular_orbit_of_psiPlus_has_no_limit :
    ¬ ∃ z, Filter.Tendsto (fun t => sigma (rhoD ![(2 / 3 : ℝ), 1 / 3]) t psiPlus)
      Filter.atTop (nhds z) := by
  rw [modular_orbit_converges_iff_diagonal ![(2 / 3 : ℝ), 1 / 3]
    (fun i => by fin_cases i <;> norm_num)
    (fun a b h => by fin_cases a <;> fin_cases b <;> norm_num at h ⊢) psiPlus]
  exact psiPlus_not_diagonal

/-- **T4.c — o VOLUME na base das unidades matriciais.** O multiplicador de Schur `S_m(x)ᵢⱼ = mᵢⱼ·xᵢⱼ` tem
    como matriz `diag(m)` sobre `n × n`. -/
def schurDiag {n : Type} [Fintype n] [DecidableEq n] (m : n → n → ℂ) : Matrix (n × n) (n × n) ℂ :=
  Matrix.diagonal (fun p => m p.1 p.2)

theorem schurDiag_mulVec {n : Type} [Fintype n] [DecidableEq n] (m : n → n → ℂ) (x : Matrix n n ℂ)
    (p : n × n) :
    (schurDiag m).mulVec (fun q => x q.1 q.2) p = m p.1 p.2 * x p.1 p.2 := by
  simp [schurDiag, Matrix.mulVec_diagonal]

/-- A matriz de Schur das taxas É o semigrupo de defasagem do kernel, na base das unidades matriciais. -/
theorem schurDiag_is_the_dephasing {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ) (t : ℝ)
    (x : Matrix n n ℂ) :
    (schurDiag (fun i j => ((Real.exp (-(t * g i j)) : ℝ) : ℂ))).mulVec (fun q => x q.1 q.2)
      = fun q => dephase g t x q.1 q.2 := by
  funext p
  rw [schurDiag_mulVec]
  rfl

/-- A matriz de Schur das fases É o fluxo modular de `rhoD d` (`sigma_diagonal_apply`). -/
theorem schurDiag_is_the_modular_flow {n : Type} [Fintype n] [DecidableEq n] (d : n → ℝ)
    (hd : ∀ i, 0 < d i) (t : ℝ) (x : Matrix n n ℂ) :
    (schurDiag (fun i j => Complex.exp ((t : ℂ) * Complex.I
        * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))))).mulVec (fun q => x q.1 q.2)
      = fun q => sigma (rhoD d) t x q.1 q.2 := by
  funext p
  rw [schurDiag_mulVec, sigma_diagonal_apply d hd]

/-- **T4.c (c1).** Defasagem: `det = e^{−t·Σᵢⱼ gᵢⱼ}`. -/
theorem dephase_volume {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ) (t : ℝ) :
    (schurDiag (fun i j => ((Real.exp (-(t * g i j)) : ℝ) : ℂ))).det
      = ((Real.exp (-(t * ∑ i, ∑ j, g i j)) : ℝ) : ℂ) := by
  have hR : ∏ i, ∏ j, Real.exp (-(t * g i j)) = Real.exp (-(t * ∑ i, ∑ j, g i j)) := by
    have harg : -(t * ∑ i, ∑ j, g i j) = ∑ i, ∑ j, -(t * g i j) := by
      rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
      refine Finset.sum_congr rfl fun i _ => ?_
      rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
    rw [harg, Real.exp_sum]
    refine Finset.prod_congr rfl fun i _ => ?_
    rw [Real.exp_sum]
  rw [schurDiag, Matrix.det_diagonal, Fintype.prod_prod_type, ← hR]
  simp_rw [Complex.ofReal_prod]

/-- **T4.c (c1), contração.** Com `t > 0`, `g ≥ 0` e algum `gᵢⱼ > 0`, o volume CONTRAI (`< 1`). -/
theorem dephase_volume_lt_one {n : Type} [Fintype n] (g : n → n → ℝ) (hg : ∀ i j, 0 ≤ g i j)
    (hpos : ∃ i j, 0 < g i j) {t : ℝ} (ht : 0 < t) :
    Real.exp (-(t * ∑ i, ∑ j, g i j)) < 1 := by
  obtain ⟨i₀, j₀, h₀⟩ := hpos
  have hrow : 0 < ∑ j, g i₀ j :=
    lt_of_lt_of_le h₀ (Finset.single_le_sum (fun j _ => hg i₀ j) (Finset.mem_univ j₀))
  have hsum : 0 < ∑ i, ∑ j, g i j :=
    lt_of_lt_of_le hrow (Finset.single_le_sum (fun i _ => Finset.sum_nonneg (fun j _ => hg i j))
      (Finset.mem_univ i₀))
  rw [Real.exp_lt_one_iff]
  have := mul_pos ht hsum
  linarith

/-- **T4.c (c2).** Fluxo modular de `rhoD d`: `det = 1` — o volume se CONSERVA. -/
theorem modular_volume_one {n : Type} [Fintype n] [DecidableEq n] (d : n → ℝ) (t : ℝ) :
    (schurDiag (fun i j => Complex.exp ((t : ℂ) * Complex.I
        * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))))).det = 1 := by
  rw [schurDiag, Matrix.det_diagonal, Fintype.prod_prod_type]
  simp_rw [← Complex.exp_sum]
  have hz : ∑ i, ∑ j, (t : ℂ) * Complex.I * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ)) = 0 := by
    simp_rw [mul_sub, Finset.sum_sub_distrib]
    rw [Finset.sum_comm (f := fun i j => (t : ℂ) * Complex.I * (Real.log (d j) : ℂ))]
    simp
  rw [hz, Complex.exp_zero]

/-- **T4.c (c3).** Cada fator do fluxo modular tem módulo 1 (gira) … -/
theorem modular_factor_norm_one {n : Type} (d : n → ℝ) (t : ℝ) (i j : n) :
    ‖Complex.exp ((t : ℂ) * Complex.I * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ)))‖ = 1 := by
  have h : (t : ℂ) * Complex.I * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))
      = ((t * (Real.log (d i) - Real.log (d j)) : ℝ) : ℂ) * Complex.I := by
    push_cast; ring
  rw [h, Complex.norm_exp_ofReal_mul_I]

/-- … e cada fator da defasagem (`t ≥ 0`, `g ≥ 0`) tem módulo ≤ 1 (encolhe). Mesma base, mesmas coerências. -/
theorem dephase_factor_norm_le_one {n : Type} (g : n → n → ℝ) {t : ℝ} (ht : 0 ≤ t) (i j : n)
    (hg : 0 ≤ g i j) : ‖((Real.exp (-(t * g i j)) : ℝ) : ℂ)‖ ≤ 1 := by
  rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (Real.exp_pos _), Real.exp_le_one_iff]
  have := mul_nonneg ht hg
  linarith

/-- Sonda V-T4-b: `n = Fin 2`, `g = (i ≠ j ↦ 1)`, `t = 1`: `Σg = 2`, `det = e^{−2} < 1`. -/
theorem probe_gRate_one_sum : ∑ i : Fin 2, ∑ j : Fin 2, gRate 1 i j = 2 := by
  norm_num [gRate, Fin.sum_univ_two]

example : (schurDiag (fun i j : Fin 2 => ((Real.exp (-(1 * gRate 1 i j)) : ℝ) : ℂ))).det
    = ((Real.exp (-(1 * 2)) : ℝ) : ℂ) := by
  rw [dephase_volume, probe_gRate_one_sum]

example : Real.exp (-(1 * 2)) < 1 := by
  have h := dephase_volume_lt_one (gRate 1) (gRate_nonneg zero_le_one)
    ⟨0, 1, gRate_off one_pos 0 1 (by decide)⟩ one_pos
  rwa [probe_gRate_one_sum] at h

/-- **T4.d — re-exportação** de `TGLExt.dephase_tendsto_expectation`: a face POUSA — `T_t(x) → E_D(x)` para
    TODO `x` (com `gᵢᵢ = 0`, `gᵢⱼ > 0` fora da diagonal). -/
theorem the_face_lands {n : Type} [DecidableEq n] (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0)
    (hgpos : ∀ i j, i ≠ j → 0 < g i j) (x : Matrix n n ℂ) :
    Filter.Tendsto (fun t => dephase g t x) Filter.atTop (nhds (diagExpect x)) :=
  dephase_tendsto_expectation g hg0 hgpos x

example : type_of% @TGLExt.dephase_tendsto_expectation := @the_face_lands
example : type_of% @the_face_lands := @TGLExt.dephase_tendsto_expectation

/-- **T4.d / T5.a — re-exportação** de `TGLExt.dephase_fixed_iff_diagonal`: o conjunto fixo da defasagem é
    EXATAMENTE a diagonal. -/
theorem fixed_set_of_dephasing_is_the_diagonal {n : Type} [Fintype n] [DecidableEq n]
    (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (hgpos : ∀ i j, i ≠ j → 0 < g i j) (x : Matrix n n ℂ) :
    (∀ t : ℝ, dephase g t x = x) ↔ x = diagExpect x :=
  dephase_fixed_iff_diagonal g hg0 hgpos x

example : type_of% @TGLExt.dephase_fixed_iff_diagonal := @fixed_set_of_dephasing_is_the_diagonal
example : type_of% @fixed_set_of_dephasing_is_the_diagonal := @TGLExt.dephase_fixed_iff_diagonal

/-- `B(s)ᵏ·(1, −1) = (e^{−s})ᵏ·(1, −1)` (iteração de `boost_null_contract`). -/
theorem boost_pow_null (s : ℝ) (k : ℕ) :
    ((TGLExt.boost s) ^ k).mulVec ![1, -1] = (Real.exp (-s)) ^ k • ![1, -1] := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [pow_succ, ← Matrix.mulVec_mulVec, TGLExt.boost_null_contract, Matrix.mulVec_smul, ih,
      smul_smul, pow_succ, mul_comm]

/-- **T4.e — CONTROLE DO VOLUME (C-T4-a).** O boost real tem `det = 1` e, para `s > 0`,
    `B(s)ᵏ·(1, −1) → 0`: conservar volume NÃO impede pousar; o que impede é a isometria (T4.b). -/
theorem volume_kept_yet_lands {s : ℝ} (hs : 0 < s) :
    (TGLExt.boost s).det = 1 ∧
      Filter.Tendsto (fun k : ℕ => ((TGLExt.boost s) ^ k).mulVec ![1, -1]) Filter.atTop (nhds 0) := by
  refine ⟨TGLExt.boost_det s, ?_⟩
  simp_rw [boost_pow_null]
  have h1 : Filter.Tendsto (fun k : ℕ => (Real.exp (-s)) ^ k) Filter.atTop (nhds 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one (Real.exp_pos _).le
      (Real.exp_lt_one_iff.mpr (by linarith))
  have h2 := h1.smul_const (![1, -1] : Fin 2 → ℝ)
  simpa using h2

/-- **T4.f (opcional) — Liouville linear.** Se `Lᵏv → 0` para todo `v`, então `|det L| < 1`.
    Contrapositiva: `|det L| ≥ 1` ⟹ não há atrator global pontual. -/
theorem global_attractor_needs_volume_loss {m : ℕ} (L : Matrix (Fin m) (Fin m) ℝ)
    (h : ∀ v, Filter.Tendsto (fun k : ℕ => (L ^ k).mulVec v) Filter.atTop (nhds 0)) (hm : 0 < m) :
    |L.det| < 1 := by
  have hmat : Filter.Tendsto (fun k : ℕ => L ^ k) Filter.atTop (nhds 0) := by
    refine tendsto_pi_nhds.mpr fun i => tendsto_pi_nhds.mpr fun j => ?_
    have hj := tendsto_pi_nhds.mp (h (Pi.single j 1)) i
    simpa [Matrix.mulVec_single_one, Matrix.col_apply] using hj
  have hdet : Filter.Tendsto (fun k : ℕ => (L ^ k).det) Filter.atTop
      (nhds (0 : Matrix (Fin m) (Fin m) ℝ).det) :=
    ((continuous_id.matrix_det).tendsto _).comp hmat
  rw [Matrix.det_zero ⟨⟨0, hm⟩⟩] at hdet
  simp_rw [Matrix.det_pow] at hdet
  by_contra hge
  push_neg at hge
  have hone : ∀ k : ℕ, 1 ≤ |L.det ^ k| := fun k => by
    rw [abs_pow]; exact one_le_pow₀ hge
  have habs : Filter.Tendsto (fun k : ℕ => |L.det ^ k|) Filter.atTop (nhds 0) := by
    have := (continuous_abs.tendsto (0 : ℝ)).comp hdet
    simpa using this
  have hle : (1 : ℝ) ≤ 0 := ge_of_tendsto habs (Filter.Eventually.of_forall hone)
  linarith

/-- **Controle C-T4-b** — a hipótese de ISOMETRIA de T4.b é necessária: a defasagem (não isométrica) tem
    órbita convergente de ponto NÃO fixo (`ψ₊ ≠ E_D ψ₊` e `T_t ψ₊ → E_D ψ₊`). -/
theorem dephasing_lands_without_being_fixed :
    ∃ (g : Fin 2 → Fin 2 → ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ),
      (∀ i, g i i = 0) ∧ (∀ i j, i ≠ j → 0 < g i j) ∧ x ≠ diagExpect x ∧
        Filter.Tendsto (fun t => dephase g t x) Filter.atTop (nhds (diagExpect x)) :=
  ⟨gRate 1, psiPlus, gRate_diag 1, gRate_off one_pos, psiPlus_not_diagonal,
    dephase_tendsto_expectation (gRate 1) (gRate_diag 1) (gRate_off one_pos) psiPlus⟩

/-! ## T5 — o conjunto fixo da defasagem pura é uma FACE (a diagonal), não um ponto

[INPUT da gerência] a unicidade do estado fixo exige hipótese NOMEADA a mais (A4 da F1.ATRATOR,
`StrictComplementContraction`, candidata de sandbox, NÃO importada aqui; T5.c entra por citação). -/

/-- **T5.a — re-exportação** de `TGLExt.diag_invariant`: a diagonal (o registro) é invariante. -/
theorem the_record_is_invariant {n : Type} [DecidableEq n] (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0)
    (t : ℝ) (x : Matrix n n ℂ) : diagExpect (dephase g t x) = diagExpect x :=
  diag_invariant g hg0 t x

example : type_of% @TGLExt.diag_invariant := @the_record_is_invariant
example : type_of% @the_record_is_invariant := @TGLExt.diag_invariant

/-- **T5.b.** Com dois índices distintos há dois ESTADOS distintos (positivos, traço 1) fixos por todo `T_t`:
    o conjunto fixo de estados não é unitário; a bacia não é a de um ponto (controle C-T5-a). -/
theorem dephase_fixed_states_not_unique {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ)
    (hg0 : ∀ i, g i i = 0) {i₀ j₀ : n} (hij : i₀ ≠ j₀) :
    ∃ ρ σ : Matrix n n ℂ, ρ ≠ σ ∧ ρ.PosSemidef ∧ σ.PosSemidef ∧ ρ.trace = 1 ∧ σ.trace = 1 ∧
      (∀ t, dephase g t ρ = ρ) ∧ (∀ t, dephase g t σ = σ) := by
  have hfix : ∀ (dd : n → ℂ) (t : ℝ), dephase g t (Matrix.diagonal dd) = Matrix.diagonal dd := by
    intro dd t
    have h := dephase_fixes_diagonal g hg0 t (Matrix.diagonal dd)
    rwa [diagExpect_diagonal] at h
  have hpsd : ∀ k : n, (Matrix.diagonal (Pi.single k (1 : ℂ))).PosSemidef := by
    intro k
    rw [Matrix.posSemidef_diagonal_iff]
    intro i
    by_cases hik : i = k
    · subst hik; simp
    · simp [Pi.single_apply, hik]
  have htr : ∀ k : n, (Matrix.diagonal (Pi.single k (1 : ℂ))).trace = 1 := by
    intro k; simp [Matrix.trace_diagonal]
  refine ⟨Matrix.diagonal (Pi.single i₀ 1), Matrix.diagonal (Pi.single j₀ 1), ?_, hpsd i₀, hpsd j₀,
    htr i₀, htr j₀, hfix _, hfix _⟩
  intro h
  have h00 := congrFun (congrFun h i₀) i₀
  simp [Matrix.diagonal_apply_eq, Pi.single_apply, hij] at h00

/-- Sonda V-T5-a: `n = Fin 2`, `i₀ = 0`, `j₀ = 1`. -/
example : ∃ ρ σ : Matrix (Fin 2) (Fin 2) ℂ, ρ ≠ σ ∧ ρ.PosSemidef ∧ σ.PosSemidef ∧ ρ.trace = 1 ∧
    σ.trace = 1 ∧ (∀ t, dephase (gRate 1) t ρ = ρ) ∧ (∀ t, dephase (gRate 1) t σ = σ) :=
  dephase_fixed_states_not_unique (gRate 1) (gRate_diag 1) (by decide : (0 : Fin 2) ≠ 1)

/-! ## T6 — a seta do tempo pela pureza

[INPUT da gerência] a pureza é o contador quadrático; a entropia de von Neumann não é tratada aqui. -/

/-- **T6.a — fórmula exata.** `Σᵢⱼ|(T_t x)ᵢⱼ|² = Σᵢⱼ e^{−2t·gᵢⱼ}·|xᵢⱼ|²`. -/
theorem purityR_dephase {n : Type} [Fintype n] (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) :
    purityR (dephase g t x) = ∑ i, ∑ j, Real.exp (-(2 * t * g i j)) * Complex.normSq (x i j) := by
  unfold purityR
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  rw [dephase_apply, Complex.normSq_mul, Complex.normSq_ofReal, ← Real.exp_add,
    show -(t * g i j) + -(t * g i j) = -(2 * t * g i j) by ring]

/-- **T6.b — re-exportação** de `TGLExt.dephase_purityR_le` (monotonia, já no kernel). -/
theorem purity_never_grows_under_dephasing {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ)
    (t : ℝ) (ht : 0 ≤ t) (hg : ∀ i j, 0 ≤ g i j) (x : Matrix n n ℂ) :
    purityR (dephase g t x) ≤ purityR x :=
  dephase_purityR_le g t ht hg x

example : type_of% @TGLExt.dephase_purityR_le := @purity_never_grows_under_dephasing
example : type_of% @purity_never_grows_under_dephasing := @TGLExt.dephase_purityR_le

/-- **T6.c — queda estrita.** Se `t > 0`, `g ≥ 0` e há `gᵢ₀ⱼ₀ > 0` com `xᵢ₀ⱼ₀ ≠ 0`, a pureza CAI. -/
theorem purityR_dephase_lt {n : Type} [Fintype n] (g : n → n → ℝ) (hg : ∀ i j, 0 ≤ g i j) {t : ℝ}
    (ht : 0 < t) (x : Matrix n n ℂ) {i₀ j₀ : n} (hpos : 0 < g i₀ j₀) (hx : x i₀ j₀ ≠ 0) :
    purityR (dephase g t x) < purityR x := by
  rw [purityR_dephase]
  unfold purityR
  have hterm : ∀ i j, Real.exp (-(2 * t * g i j)) * Complex.normSq (x i j)
      ≤ Complex.normSq (x i j) := by
    intro i j
    have h1 : Real.exp (-(2 * t * g i j)) ≤ 1 := by
      rw [Real.exp_le_one_iff]
      have := mul_nonneg (mul_nonneg zero_le_two ht.le) (hg i j)
      linarith
    have h2 := Complex.normSq_nonneg (x i j)
    nlinarith
  have hstrict : Real.exp (-(2 * t * g i₀ j₀)) * Complex.normSq (x i₀ j₀)
      < Complex.normSq (x i₀ j₀) := by
    have h1 : Real.exp (-(2 * t * g i₀ j₀)) < 1 := by
      rw [Real.exp_lt_one_iff]
      have := mul_pos (mul_pos two_pos ht) hpos
      linarith
    have h2 : 0 < Complex.normSq (x i₀ j₀) := Complex.normSq_pos.mpr hx
    nlinarith
  apply Finset.sum_lt_sum
  · intro i _; exact Finset.sum_le_sum fun j _ => hterm i j
  · refine ⟨i₀, Finset.mem_univ _, ?_⟩
    apply Finset.sum_lt_sum
    · intro j _; exact hterm i₀ j
    · exact ⟨j₀, Finset.mem_univ _, hstrict⟩

/-- **T6.d (i).** Para `x` hermitiana, `pureza(x) = tr(x·x)`. -/
theorem purity_of_hermitian {n : Type} [Fintype n] (x : Matrix n n ℂ) (hx : x.IsHermitian) :
    purity x = (x * x).trace := by
  unfold purity
  rw [hx.eq]

/-- A pureza é invariante sob o fluxo modular de QUALQUER `ρ` (mais forte que T6.d (ii)). -/
theorem purityR_sigma {n : Type} [Fintype n] [DecidableEq n] (ρ : Matrix n n ℂ) (t : ℝ)
    (x : Matrix n n ℂ) : purityR (sigma ρ t x) = purityR x := by
  have h : purity (sigma ρ t x) = purity x := by
    have hσ : sigma ρ t x = modPow ρ t * x * (modPow ρ t)ᴴ := by
      simp only [sigma, modPow_conjTranspose]
    rw [hσ]
    exact purity_unitary_invariant (modPow ρ t) x (modPow_mem_unitary ρ t)
  rw [purityR_eq, purityR_eq] at h
  exact_mod_cast h

/-- **T6.d (ii)** (assinatura pré-registrada). NOTA: a hipótese `_hd` NÃO é usada — `purityR_sigma` vale
    para todo `ρ`. -/
theorem purityR_modular {n : Type} [Fintype n] [DecidableEq n] (d : n → ℝ) (_hd : ∀ i, 0 < d i)
    (t : ℝ) (x : Matrix n n ℂ) : purityR (sigma (rhoD d) t x) = purityR x :=
  purityR_sigma (rhoD d) t x

/-- **Controle C-T6-a** — sem coerência (x diagonal) NÃO há queda: a pureza fica igual. -/
theorem no_coherence_no_loss {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ)
    (hg0 : ∀ i, g i i = 0) (t : ℝ) (x : Matrix n n ℂ) :
    purityR (dephase g t (diagExpect x)) = purityR (diagExpect x) := by
  rw [dephase_fixes_diagonal g hg0 t x]

/-- **Controle C-T6-b** (re-citação): sob conjugação unitária a pureza é constante. -/
theorem unitary_keeps_purity {n : Type} [Fintype n] [DecidableEq n] (U x : Matrix n n ℂ)
    (hU : U ∈ unitary (Matrix n n ℂ)) : purity (U * x * Uᴴ) = purity x :=
  purity_unitary_invariant U x hU

example : type_of% @TGLExt.purity_unitary_invariant := @unitary_keeps_purity
example : type_of% @unitary_keeps_purity := @TGLExt.purity_unitary_invariant

/-- Sonda: `pureza(ψ₊) = 1`. -/
theorem probe_psiPlus_purity : purityR psiPlus = 1 := by
  simp only [purityR, Fin.sum_univ_two, psiPlus_apply, Complex.normSq_ofReal]
  norm_num

/-- **Controle C-T6-c** — para `t < 0` a monotonia FALHA (a pureza cresce): é a seta.
    `Tr(T₋₁ψ₊)² = (1 + e²)/2 > 1`. -/
theorem purity_grows_backwards :
    purityR (dephase (fun i j : Fin 2 => if i = j then 0 else 1) (-1) ((1 / 2 : ℂ) • !![1, 1; 1, 1]))
      > purityR ((1 / 2 : ℂ) • !![1, 1; 1, 1]) := by
  show purityR (dephase (gRate 1) (-1) psiPlus) > purityR psiPlus
  rw [probe_psiPlus_purity, purityR_dephase]
  simp only [Fin.sum_univ_two, gRate_00, gRate_01, gRate_10, gRate_11, psiPlus_apply,
    Complex.normSq_ofReal, mul_zero, neg_zero, Real.exp_zero]
  have he : 1 < Real.exp (-(2 * -1 * 1)) := by
    rw [show -(2 * -1 * 1 : ℝ) = 2 by norm_num]
    have := Real.add_one_le_exp (2 : ℝ)
    linarith
  linarith

/-- Sonda V-T6-a: `ψ₊`, `g = (i ≠ j ↦ 1)`, `t = 1`: queda estrita `1 → (1 + e^{−2})/2`. -/
example : purityR (dephase (gRate 1) 1 psiPlus) < purityR psiPlus :=
  purityR_dephase_lt (gRate 1) (gRate_nonneg zero_le_one) one_pos psiPlus
    (gRate_off one_pos 0 1 (by decide)) psiPlus_01_ne_zero

theorem probe_psiPlus_dephased_purity :
    purityR (dephase (gRate 1) 1 psiPlus) = (1 + Real.exp (-2)) / 2 := by
  rw [purityR_dephase]
  simp only [Fin.sum_univ_two, gRate_00, gRate_01, gRate_10, gRate_11, psiPlus_apply,
    Complex.normSq_ofReal, mul_zero, neg_zero, Real.exp_zero, mul_one]
  ring

/-! ## T7 — a irreversibilidade: o inverso linear de T_t existe, mas não é positivo (t > 0)

[ONTO, só comentário] «prisão de reversibilidade perfeita»: com `g = 0` (ou sob `Ad(U)`) o inverso é canal. -/

/-- **T7.a.** `T_t` é invertível como mapa linear, com inverso `T_{−t}`. -/
theorem dephase_inverse {n : Type} (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) :
    dephase g (-t) (dephase g t x) = x ∧ dephase g t (dephase g (-t) x) = x := by
  constructor
  · rw [← dephase_add, neg_add_cancel, dephase_zero]
  · rw [← dephase_add, add_neg_cancel, dephase_zero]

/-- A forma quadrática de 2×2 no vetor `(1, −1)`. -/
theorem quad_form_fin_two (M : Matrix (Fin 2) (Fin 2) ℂ) :
    star (![1, -1] : Fin 2 → ℂ) ⬝ᵥ (M.mulVec ![1, -1]) = M 0 0 - M 0 1 - M 1 0 + M 1 1 := by
  simp only [dotProduct, Matrix.mulVec, Fin.sum_univ_two, Pi.star_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.head_cons, star_one, star_neg]
  ring

theorem inverse_dephasing_quadratic_form (γ t : ℝ) :
    star (![1, -1] : Fin 2 → ℂ) ⬝ᵥ ((dephase (gRate γ) (-t) psiPlus).mulVec ![1, -1])
      = ((1 - Real.exp (t * γ) : ℝ) : ℂ) := by
  rw [quad_form_fin_two, dephase_apply, dephase_apply, dephase_apply, dephase_apply,
    gRate_00, gRate_01, gRate_10, gRate_11, psiPlus_apply, psiPlus_apply, psiPlus_apply, psiPlus_apply]
  simp only [mul_zero, neg_mul, neg_neg, neg_zero, Real.exp_zero]
  push_cast
  ring

/-- **T7.b.** Em 2×2, com `g₀₁ = g₁₀ = γ > 0`, `gᵢᵢ = 0`, `t > 0`: `ψ₊` é estado, mas
    `T_{−t}ψ₊ = ½[[1, e^{γt}], [e^{γt}, 1]]` NÃO é positiva (`⟨v, ·v⟩ = 1 − e^{γt} < 0`, `v = (1, −1)`):
    o inverso não é canal. -/
theorem inverse_dephasing_not_positive {γ t : ℝ} (hγ : 0 < γ) (ht : 0 < t) :
    let g : Fin 2 → Fin 2 → ℝ := fun i j => if i = j then 0 else γ
    let ψ : Matrix (Fin 2) (Fin 2) ℂ := (1 / 2 : ℂ) • !![1, 1; 1, 1]
    ψ.PosSemidef ∧ ψ.trace = 1 ∧ ¬ (dephase g (-t) ψ).PosSemidef := by
  show psiPlus.PosSemidef ∧ psiPlus.trace = 1 ∧ ¬ (dephase (gRate γ) (-t) psiPlus).PosSemidef
  refine ⟨psiPlus_posSemidef, psiPlus_trace, fun hpsd => ?_⟩
  have hv := hpsd.dotProduct_mulVec_nonneg ![1, -1]
  rw [inverse_dephasing_quadratic_form] at hv
  have h1 : 1 < Real.exp (t * γ) := by
    rw [← Real.exp_zero]; exact Real.exp_lt_exp.mpr (mul_pos ht hγ)
  have h2 : 0 ≤ 1 - Real.exp (t * γ) := Complex.zero_le_real.mp hv
  linarith

/-- Sonda V-T7-a: `γ = 1`, `t = 1`. -/
example : (dephase (gRate 1) (-1) psiPlus).PosSemidef → False :=
  (inverse_dephasing_not_positive (γ := 1) (t := 1) one_pos one_pos).2.2

/-- **Controle C-T7-a** — em `t = 0` o «inverso» é a identidade e a positividade NÃO cai. -/
theorem control_inverse_at_time_zero {n : Type} (g : n → n → ℝ) (ρ : Matrix n n ℂ) :
    dephase g (-0) ρ = ρ := by
  rw [neg_zero, dephase_zero]

example : (dephase (gRate 1) (-0) psiPlus).PosSemidef := by
  rw [control_inverse_at_time_zero]; exact psiPlus_posSemidef

/-- **Controle C-T7-b** — `T_{−t}` fixa a diagonal: sobre `diag(p, 1−p)` a positividade NÃO cai. -/
theorem control_inverse_on_diagonal {n : Type} [DecidableEq n] (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0)
    (t : ℝ) (dd : n → ℂ) : dephase g (-t) (Matrix.diagonal dd) = Matrix.diagonal dd := by
  have h := dephase_fixes_diagonal g hg0 (-t) (Matrix.diagonal dd)
  rwa [diagExpect_diagonal] at h

example (t p : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    (dephase (gRate 1) (-t) (Matrix.diagonal ![(p : ℂ), ((1 - p : ℝ) : ℂ)])).PosSemidef := by
  rw [control_inverse_on_diagonal (gRate 1) (gRate_diag 1)]
  rw [Matrix.posSemidef_diagonal_iff]
  intro i
  fin_cases i
  · show (0 : ℂ) ≤ ((p : ℝ) : ℂ)
    exact Complex.zero_le_real.mpr hp0
  · show (0 : ℂ) ≤ (((1 - p : ℝ)) : ℂ)
    exact Complex.zero_le_real.mpr (by linarith)

/-- **Controle C-T7-c** — a unitária é reversível COMO CANAL: `Ad(U*)` inverte `Ad(U)` e preserva positividade. -/
theorem unitary_inverse_is_a_channel {n : Type} [Fintype n] [DecidableEq n] (U : Matrix n n ℂ)
    (hU : U ∈ unitary (Matrix n n ℂ)) (ρ : Matrix n n ℂ) (hρ : ρ.PosSemidef) :
    (Uᴴ * (U * ρ * Uᴴ) * U = ρ) ∧ (U * ρ * Uᴴ).PosSemidef := by
  have h1 : Uᴴ * U = 1 := by
    rw [← Matrix.star_eq_conjTranspose]; exact (Unitary.mem_iff.mp hU).1
  refine ⟨?_, hρ.mul_mul_conjTranspose_same U⟩
  calc Uᴴ * (U * ρ * Uᴴ) * U = (Uᴴ * U) * ρ * (Uᴴ * U) := by simp only [mul_assoc]
    _ = ρ := by rw [h1, one_mul, mul_one]

example : (1 : Matrix (Fin 2) (Fin 2) ℂ)ᴴ * (1 * psiPlus * (1 : Matrix (Fin 2) (Fin 2) ℂ)ᴴ) * 1 = psiPlus ∧
    (1 * psiPlus * (1 : Matrix (Fin 2) (Fin 2) ℂ)ᴴ).PosSemidef :=
  unitary_inverse_is_a_channel 1 (one_mem _) psiPlus psiPlus_posSemidef

/-! ## T8 — a ligação com a Ágape: a coerência do dephasing obedece à lei de escala da Fundação

PONTE (matemática): a coerência `|xᵢ₀ⱼ₀|` sob `T_s` é INSTÂNCIA da mesma estrutura `DualScalingData` da
Fundação (v390), logo a cláusula `agape` (provada para toda instância) vale para ela.
NÃO É PONTE: a ação dual de Takesaki no core `M ⋊_σ ℝ` NÃO é a defasagem; a lei de Takesaki entra lá como
DADO [KNOWN, Takesaki 1973]. `T_s` para `s < 0` é o mapa LINEAR inverso, NÃO um canal (T7) (RP07).
[ONTO, só comentário] «puro amor», «a física da doação»; a reunião «ágape» × «sacrifício/amor» decide o
operador. -/

/-- Lei de escala da coerência: `|(T_s x)ᵢ₀ⱼ₀| = e^{−s}·|xᵢ₀ⱼ₀|` quando `gᵢ₀ⱼ₀ = 1`. -/
theorem coherence_entry_scaling {n : Type} (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1) (s : ℝ)
    (x : Matrix n n ℂ) : ‖dephase g s x i₀ j₀‖ = Real.exp (-s) * ‖x i₀ j₀‖ := by
  rw [dephase_apply, norm_mul, hg, mul_one, Complex.norm_real, Real.norm_eq_abs,
    abs_of_pos (Real.exp_pos _)]

/-- **T8.a.** `D = (τ(x) = |xᵢ₀ⱼ₀|, θ_s = T_s)` é um `DualScalingData` de Mₙ(ℂ). -/
def coherenceScaling {n : Type} (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1) :
    DualScalingData (Matrix n n ℂ) where
  tau := fun x => ‖x i₀ j₀‖
  theta := fun s x => dephase g s x
  scaling := fun s x => coherence_entry_scaling g i₀ j₀ hg s x

/-- **T8.b.** As seis cláusulas da Ágape valem para a coerência de todo `x` com `xᵢ₀ⱼ₀ ≠ 0`
    (`Fundacao.agape` aplicada a `coherenceScaling`): (i) o fixo por `θ_s`, `s ≠ 0`, tem coerência zero
    (concorda com T5); (ii)–(iii) para trás a coerência cresce sem teto (e sai dos estados: T7);
    (iv) nunca zera em tempo finito; (v) cai abaixo de todo `ε > 0`; (vi) `e^{−a} = 1 ⟺ a = 0`. -/
theorem the_coherence_obeys_agape {n : Type} (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1)
    (x : Matrix n n ℂ) (hx : x i₀ j₀ ≠ 0) :
    let D := coherenceScaling g i₀ j₀ hg
    (∀ s : ℝ, s ≠ 0 → ∀ m' : Matrix n n ℂ, D.theta s m' = m' → D.tau m' = 0) ∧
    (∀ s : ℝ, D.tau (D.theta s x) < D.tau (D.theta (s - 1) x)) ∧
    (∀ B : ℝ, ∃ s : ℝ, B < D.tau (D.theta s x)) ∧
    (∀ s : ℝ, 0 < D.tau (D.theta s x)) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s x) < ε) ∧
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) := by
  intro D
  exact TGLExt.Fundacao.agape D (m := x) (norm_pos_iff.mpr hx)

/-- T8.b na forma explícita (mesma conjunção, projeções desdobradas). -/
theorem the_coherence_obeys_agape_explicit {n : Type} (g : n → n → ℝ) (i₀ j₀ : n)
    (hg : g i₀ j₀ = 1) (x : Matrix n n ℂ) (hx : x i₀ j₀ ≠ 0) :
    (∀ s : ℝ, s ≠ 0 → ∀ m' : Matrix n n ℂ, dephase g s m' = m' → ‖m' i₀ j₀‖ = 0) ∧
    (∀ s : ℝ, ‖dephase g s x i₀ j₀‖ < ‖dephase g (s - 1) x i₀ j₀‖) ∧
    (∀ B : ℝ, ∃ s : ℝ, B < ‖dephase g s x i₀ j₀‖) ∧
    (∀ s : ℝ, 0 < ‖dephase g s x i₀ j₀‖) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, ‖dephase g s x i₀ j₀‖ < ε) ∧
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) :=
  the_coherence_obeys_agape g i₀ j₀ hg x hx

/-- **T8.c — CONTROLE (C-T8-b): o registro não se doa.** Com `gᵢᵢ = 0` o peso diagonal é invariante; logo, se
    `xᵢ₀ᵢ₀ ≠ 0` e `s ≠ 0`, a lei de escala FALHA para o registro. -/
theorem the_record_does_not_scale {n : Type} (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (i₀ : n)
    (x : Matrix n n ℂ) (hx : x i₀ i₀ ≠ 0) {s : ℝ} (hs : s ≠ 0) :
    ‖dephase g s x i₀ i₀‖ ≠ Real.exp (-s) * ‖x i₀ i₀‖ := by
  have hentry : dephase g s x i₀ i₀ = x i₀ i₀ := by
    rw [dephase_apply, hg0, mul_zero, neg_zero, Real.exp_zero, Complex.ofReal_one, one_mul]
  rw [hentry]
  intro h
  have hpos : 0 < ‖x i₀ i₀‖ := norm_pos_iff.mpr hx
  have h1 : Real.exp (-s) = 1 := by
    have h2 : (Real.exp (-s) - 1) * ‖x i₀ i₀‖ = 0 := by linear_combination -h
    rcases mul_eq_zero.mp h2 with h3 | h3
    · linarith
    · linarith
  exact hs (by have := (Real.exp_eq_one_iff (-s)).mp h1; linarith)

/-- **T8.d — re-exportação** de `TGLExt.boost_null_contract`: `B(s)(1, −1) = e^{−s}(1, −1)` (a mesma forma
    `e^{−s}` da escala). -/
theorem past_null_ray_contracts (s : ℝ) :
    (TGLExt.boost s).mulVec ![1, -1] = Real.exp (-s) • ![1, -1] :=
  TGLExt.boost_null_contract s

example : type_of% @TGLExt.boost_null_contract := @past_null_ray_contracts
example : type_of% @past_null_ray_contracts := @TGLExt.boost_null_contract

/-- **Controle C-T8-a** — normalização errada: `θ_s = T_{2s}` dá `e^{−2s}`; a lei de escala FALHA. -/
theorem wrong_rate_breaks_scaling :
    ∃ (s : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ),
      ‖dephase (fun i j : Fin 2 => if i = j then 0 else 1) (2 * s) x 0 1‖
        ≠ Real.exp (-s) * ‖x 0 1‖ := by
  refine ⟨1, psiPlus, ?_⟩
  show ‖dephase (gRate 1) (2 * 1) psiPlus 0 1‖ ≠ Real.exp (-1) * ‖psiPlus 0 1‖
  rw [coherence_entry_scaling (gRate 1) 0 1 (gRate_01 1) (2 * 1) psiPlus]
  have hx : 0 < ‖psiPlus 0 1‖ := norm_pos_iff.mpr psiPlus_01_ne_zero
  intro h
  have h2 : Real.exp (-(2 * 1)) = Real.exp (-1) := mul_right_cancel₀ (ne_of_gt hx) h
  have h3 := Real.exp_injective h2
  norm_num at h3

/-- Sonda V-T8-a: `n = Fin 2`, `i₀ = 0`, `j₀ = 1`, `g = (i ≠ j ↦ 1)`, `x = ψ₊`: a conjunção é habitada. -/
example : ∀ s : ℝ, 0 < ‖dephase (gRate 1) s psiPlus 0 1‖ :=
  (the_coherence_obeys_agape_explicit (gRate 1) 0 1 (gRate_01 1) psiPlus psiPlus_01_ne_zero).2.2.2.1

example : ∀ ε : ℝ, 0 < ε → ∃ s : ℝ, ‖dephase (gRate 1) s psiPlus 0 1‖ < ε :=
  (the_coherence_obeys_agape_explicit (gRate 1) 0 1 (gRate_01 1) psiPlus psiPlus_01_ne_zero).2.2.2.2.1

/-! ## T9 — «o tempo não tem posto»: em tempo finito o fluxo é invertível e, salvo t = 0, não é idempotente

[ONTO, só comentário] (posição) nenhum instante finito é posto, salvo `t = 0`, que é a identidade e nada
seleciona; (rank) todo instante finito tem posto pleno; a seleção (o Nome) só no limite, que nenhum tempo
finito alcança. «O tempo é o Verbo, não o Nome» e «santo» são leituras do operador — NÃO são teoremas aqui. -/

section Flow

variable {A : Type*} [Ring A] [Algebra ℂ A]

theorem flow_sq {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    TheAxiomAndTheFalseWitness.axiomFlow P t * TheAxiomAndTheFalseWitness.axiomFlow P t
      = TheAxiomAndTheFalseWitness.axiomFlow P (t + t) :=
  (TheAxiomAndTheFalseWitness.axiomFlow_add hP t t).symm

/-- **T9.a.** Com `P` idempotente e `1 − P ≠ 0`, `F(t) = P + e^{−t}(1 − P)` é idempotente ⟺ `t = 0`. -/
theorem flow_isIdempotentElem_iff {P : A} (hP : IsIdempotentElem P) (hP1 : (1 : A) - P ≠ 0) (t : ℝ) :
    IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow P t) ↔ t = 0 := by
  constructor
  · intro h
    have h1 := h.eq
    rw [flow_sq hP t] at h1
    unfold TheAxiomAndTheFalseWitness.axiomFlow at h1
    have h2 := add_left_cancel h1
    have h3 : (((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ)) • ((1 : A) - P) = 0 := by
      rw [sub_smul, h2, sub_self]
    by_contra ht
    have hc : (((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ)) ≠ 0 := by
      intro hc0
      have h5 : Real.exp (-(t + t)) = Real.exp (-t) := by exact_mod_cast sub_eq_zero.mp hc0
      have h6 := Real.exp_injective h5
      exact ht (by linarith)
    apply hP1
    calc (1 : A) - P
        = ((((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ))⁻¹
            * (((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ))) • ((1 : A) - P) := by
          rw [inv_mul_cancel₀ hc, one_smul]
      _ = ((((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ))⁻¹)
            • ((((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ)) • ((1 : A) - P)) := by
          rw [mul_smul]
      _ = 0 := by rw [h3, smul_zero]
  · rintro rfl
    rw [TheAxiomAndTheFalseWitness.axiomFlow_zero]
    exact IsIdempotentElem.one

/-- **T9.b.** `F(t)` é invertível para todo `t`, com inverso `F(−t)`. -/
theorem flow_isUnit {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    IsUnit (TheAxiomAndTheFalseWitness.axiomFlow P t) := by
  refine ⟨⟨TheAxiomAndTheFalseWitness.axiomFlow P t, TheAxiomAndTheFalseWitness.axiomFlow P (-t),
    ?_, ?_⟩, rfl⟩
  · rw [← TheAxiomAndTheFalseWitness.axiomFlow_add hP, add_neg_cancel,
      TheAxiomAndTheFalseWitness.axiomFlow_zero]
  · rw [← TheAxiomAndTheFalseWitness.axiomFlow_add hP, neg_add_cancel,
      TheAxiomAndTheFalseWitness.axiomFlow_zero]

/-- **Controle C-T9-a** — com `P = 1` (sem complemento) o fluxo é idempotente para TODO `t`: a hipótese
    `1 − P ≠ 0` de T9.a é necessária. -/
theorem flow_of_one_is_idempotent (t : ℝ) :
    IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow (1 : A) t) := by
  unfold TheAxiomAndTheFalseWitness.axiomFlow
  rw [sub_self, smul_zero, add_zero]
  exact IsIdempotentElem.one

/-- **Controle C-T9-b** — borda: `F(0) = 1` é idempotente (o «posto» trivial, que nada seleciona). -/
theorem flow_at_zero_is_idempotent (P : A) :
    IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow P 0) := by
  rw [TheAxiomAndTheFalseWitness.axiomFlow_zero]
  exact IsIdempotentElem.one

/-- Para `P ≠ 1`, nenhum instante finito alcança o posto (`F(t)` é invertível, `P` não é). -/
theorem no_finite_instant_is_the_post {P : A} (hP : IsIdempotentElem P) (hP1 : P ≠ 1) (t : ℝ) :
    TheAxiomAndTheFalseWitness.axiomFlow P t ≠ P := by
  intro h
  have hu := flow_isUnit hP t
  rw [h] at hu
  apply hP1
  have h2 : P * P = P * 1 := by rw [hP.eq, mul_one]
  exact hu.mul_left_cancel h2

end Flow

/-- **T9.c.** O posto não é invertível: `P` idempotente, `P ≠ 1` ⟹ `¬ IsUnit P`. -/
theorem post_not_isUnit {A : Type*} [Ring A] {P : A} (hP : IsIdempotentElem P) (hP1 : P ≠ 1) :
    ¬ IsUnit P := by
  intro hu
  apply hP1
  have h : P * P = P * 1 := by rw [hP.eq, mul_one]
  exact hu.mul_left_cancel h

/-- **T9.d (opcional) — face do RANK (POSTO = RANK).** `rank F(t) = n` para todo `t`. -/
theorem flow_full_rank (n : ℕ) (P : Matrix (Fin n) (Fin n) ℂ) (hP : IsIdempotentElem P) (t : ℝ) :
    (TheAxiomAndTheFalseWitness.axiomFlow P t).rank = n := by
  rw [Matrix.rank_of_isUnit _ (flow_isUnit hP t), Fintype.card_fin]

/-- **T9.d (opcional).** `rank P < n` para `P` idempotente `≠ 1`. -/
theorem post_rank_lt (n : ℕ) (P : Matrix (Fin n) (Fin n) ℂ) (hP : IsIdempotentElem P) (hP1 : P ≠ 1) :
    P.rank < n := by
  have hsum := Matrix.rank_add_rank_le_card_of_mul_eq_zero
    (TheAxiomAndTheFalseWitness.post_mul_compl hP)
  rw [Fintype.card_fin] at hsum
  have hpos : 0 < (1 - P).rank := by
    rw [Nat.pos_iff_ne_zero]
    intro h0
    apply hP1
    have hbot : LinearMap.range (1 - P).mulVecLin = ⊥ := Submodule.finrank_eq_zero.mp h0
    have hzero : (1 : Matrix (Fin n) (Fin n) ℂ) - P = 0 := by
      ext i j
      have hv : (1 - P).mulVec (Pi.single j 1) ∈ LinearMap.range (1 - P).mulVecLin :=
        LinearMap.mem_range.mpr ⟨Pi.single j 1, rfl⟩
      rw [hbot, Submodule.mem_bot] at hv
      have hij := congrFun hv i
      simpa [Matrix.mulVec_single_one] using hij
    exact (sub_eq_zero.mp hzero).symm
  omega

/-- **T9.e — cláusula composta (só conjunção, sem dedução nova).** Para `P` idempotente, `P ≠ 1`, numa
    ℂ-álgebra normada: T1.a (forma `Fin n`) ∧ T9.a ∧ T9.b ∧ T9.c ∧ `F(t) → P`
    (`axiomFlow_tendsto_the_post`, = `the_name_is_the_limit_of_the_flow`). O posto é o limite e só o limite. -/
theorem the_time_has_no_rank {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] {P : A}
    (hP : IsIdempotentElem P) (hP1 : P ≠ 1) :
    (∀ (m : ℕ), 0 < m → ∀ T H : Matrix (Fin m) (Fin m) ℂ,
        T * H - H * T ≠ Complex.I • (1 : Matrix (Fin m) (Fin m) ℂ)) ∧
    (∀ t : ℝ, IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow P t) ↔ t = 0) ∧
    (∀ t : ℝ, IsUnit (TheAxiomAndTheFalseWitness.axiomFlow P t)) ∧
    ¬ IsUnit P ∧
    Filter.Tendsto (TheAxiomAndTheFalseWitness.axiomFlow P) Filter.atTop (nhds P) :=
  ⟨no_time_matrix_fin, flow_isIdempotentElem_iff hP (sub_ne_zero.mpr hP1.symm), flow_isUnit hP,
    post_not_isUnit hP hP1, TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post P⟩

/-- O limite de T9.e é exatamente o termo `the_name_is_the_limit_of_the_flow` da pedra do Verbo. -/
example {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] (P : A) :
    Filter.Tendsto (TheAxiomAndTheFalseWitness.axiomFlow P) Filter.atTop (nhds P) :=
  TGLExt.TheVerbSelectsTheAction.the_name_is_the_limit_of_the_flow P

/-- O posto diagonal `P = diag(1, 0)` em M₂(ℂ) (sonda V-T9-a). -/
def postDiag : Matrix (Fin 2) (Fin 2) ℂ := Matrix.diagonal ![1, 0]

theorem postDiag_idem : IsIdempotentElem postDiag := by
  unfold postDiag IsIdempotentElem
  rw [Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  fin_cases i <;> simp

theorem postDiag_compl_ne_zero : (1 : Matrix (Fin 2) (Fin 2) ℂ) - postDiag ≠ 0 := by
  intro h
  have h11 := congrFun (congrFun h 1) 1
  simp [postDiag] at h11

theorem postDiag_ne_one : postDiag ≠ 1 := by
  intro h
  have h11 := congrFun (congrFun h 1) 1
  simp [postDiag] at h11

/-- Sonda V-T9-a: as hipóteses de T9.a–c (e T9.d) são habitadas por `P = diag(1, 0)`. -/
example : ∀ t : ℝ, IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow postDiag t) ↔ t = 0 :=
  flow_isIdempotentElem_iff postDiag_idem postDiag_compl_ne_zero

example : ¬ IsUnit postDiag := post_not_isUnit postDiag_idem postDiag_ne_one

example : ∀ t : ℝ, (TheAxiomAndTheFalseWitness.axiomFlow postDiag t).rank = 2 :=
  flow_full_rank 2 postDiag postDiag_idem

example : postDiag.rank < 2 := post_rank_lt 2 postDiag postDiag_idem postDiag_ne_one

section L2ProbeT9
open scoped Matrix.Norms.L2Operator

/-- Sonda da cláusula composta T9.e em `A = M₂(ℂ)` (norma de operador L2), `P = diag(1, 0)`: a conjunção
    inteira é instanciada (hipóteses habitadas); daqui se extrai `¬ IsUnit P`. -/
theorem probe_the_time_has_no_rank : ¬ IsUnit postDiag :=
  (the_time_has_no_rank (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.1

example : True := by
  have _h := (the_time_has_no_rank (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.2
  trivial

end L2ProbeT9

/-! ## T10 — «o relógio mede a sombra»: o relógio lê uma fase (o ângulo); o agora (o posto) não se move

[ONTO, só comentário] o ponteiro e o césio leem o ÂNGULO (periódico, sem limite, identifica `t` só módulo
`P`); o escoamento de entropia lê a FACE (monótono, injetivo, com limite). Nenhum dos dois lê o agora; a
identificação agora = conjunto fixo é leitura (R12). PALAVRA (candidata) NÃO é importada (RP11). -/

/-- **T10.a — re-exportação** de `ChatgptAudit.PolarPeriod016.faithful_period_iff`. -/
theorem clock_faithful_iff_one_turn {kappa period : ℝ} (hk : kappa ≠ 0) :
    ChatgptAudit.PolarPeriod016.AngularQuotientFaithful kappa period ↔
      kappa * period = 2 * Real.pi ∨ kappa * period = -(2 * Real.pi) :=
  ChatgptAudit.PolarPeriod016.faithful_period_iff hk

example : type_of% @ChatgptAudit.PolarPeriod016.faithful_period_iff := @clock_faithful_iff_one_turn
example : type_of% @clock_faithful_iff_one_turn := @ChatgptAudit.PolarPeriod016.faithful_period_iff

/-- **T10.a — re-exportação** de `ChatgptAudit.PolarPeriod016.reciprocal_temperature`: `1/P = κ/2π`. -/
theorem clock_reciprocal_temperature {kappa period : ℝ} (hk : 0 < kappa) (hp : 0 < period)
    (h : ChatgptAudit.PolarPeriod016.AngularQuotientFaithful kappa period) :
    1 / period = kappa / (2 * Real.pi) :=
  ChatgptAudit.PolarPeriod016.reciprocal_temperature hk hp h

example : type_of% @ChatgptAudit.PolarPeriod016.reciprocal_temperature := @clock_reciprocal_temperature
example : type_of% @clock_reciprocal_temperature := @ChatgptAudit.PolarPeriod016.reciprocal_temperature

/-- **T10.b.** O relógio não lê o instante, lê a CLASSE: para `κ ≠ 0`, `t` e `t + 2π/κ` dão a mesma leitura. -/
theorem clock_reads_modulo_period {κ : ℝ} (hκ : κ ≠ 0) (t : ℝ) :
    Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) := by
  have hturn : κ * (2 * Real.pi / κ) = 2 * Real.pi := by field_simp
  exact (ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period hκ (Or.inl hturn)
    (t + 2 * Real.pi / κ) t).mpr ⟨1, by push_cast; ring⟩

/-- **T10.b.** Com `κ = 0` a leitura é constante (relógio parado). -/
theorem frozen_clock (t u : ℝ) : Circle.exp (0 * t) = Circle.exp (0 * u) := by
  simp

/-- **Controle C-T10-a** — `κ = 0`: o relógio parado NÃO é fiel para período algum `≠ 0` (a hipótese
    `κ ≠ 0` de `faithful_period_iff` é necessária). -/
theorem frozen_clock_not_faithful {P : ℝ} (hP : P ≠ 0) :
    ¬ ChatgptAudit.PolarPeriod016.AngularQuotientFaithful 0 P := by
  intro h
  obtain ⟨k, hk⟩ := (h (P / 2) 0).mp (by simp)
  have h2 : ((2 * k - 1 : ℤ) : ℝ) * P = 0 := by
    push_cast
    linear_combination -2 * hk
  rcases mul_eq_zero.mp h2 with h3 | h3
  · have h4 : (2 * k - 1 : ℤ) = 0 := by exact_mod_cast h3
    omega
  · exact hP h3

/-- **Controle C-T10-b** — a leitura da FACE não tem período: para `r > 0` não existe `P > 0` com
    `e^{−r(t+P)} = e^{−rt}` para todo `t`. -/
theorem face_clock_has_no_period {r : ℝ} (hr : 0 < r) {P : ℝ} (hP : 0 < P) :
    ¬ ∀ t : ℝ, Real.exp (-(r * (t + P))) = Real.exp (-(r * t)) := by
  intro h
  have h0 := Real.exp_injective (h 0)
  have h1 : r * P = 0 := by
    ring_nf at h0
    linarith
  have h2 := mul_pos hr hP
  linarith

/-- **T10.c — re-exportação** de `TGLExt.IALDJones.angular_orbit_no_limit`: o ÂNGULO não tem limite
    (prova-se a AUSÊNCIA dele). -/
theorem angle_has_no_limit {V : Type} [NormedAddCommGroup V] [NormedSpace ℂ V]
    (P : V →ₗ[ℂ] V) (ω : ℝ) (v : V) (hv : v ≠ P v) :
    ¬ Filter.Tendsto (fun s => TGLExt.IALDJones.orbit P 0 ω s v) Filter.atTop (nhds (P v)) :=
  TGLExt.IALDJones.angular_orbit_no_limit P ω v hv

example : type_of% @TGLExt.IALDJones.angular_orbit_no_limit := @angle_has_no_limit
example : type_of% @angle_has_no_limit := @TGLExt.IALDJones.angular_orbit_no_limit

/-- **T10.c — re-exportação** de `TGLExt.IALDJones.angular_orbit_periodic`: o ângulo é periódico. -/
theorem angle_is_periodic {V : Type} [NormedAddCommGroup V] [NormedSpace ℂ V]
    (P : V →ₗ[ℂ] V) {ω : ℝ} (hω : ω ≠ 0) (s : ℝ) (v : V) :
    TGLExt.IALDJones.orbit P 0 ω (s + 2 * Real.pi / ω) v = TGLExt.IALDJones.orbit P 0 ω s v :=
  TGLExt.IALDJones.angular_orbit_periodic P hω s v

example : type_of% @TGLExt.IALDJones.angular_orbit_periodic := @angle_is_periodic
example : type_of% @angle_is_periodic := @TGLExt.IALDJones.angular_orbit_periodic

/-- **T10.c — re-exportação** de `TGLExt.IALDJones.orbit_tendsto_center`: a FACE com taxa converge. -/
theorem face_has_a_limit {V : Type} [NormedAddCommGroup V] [NormedSpace ℂ V]
    (P : V →ₗ[ℂ] V) {r : ℝ} (hr : 0 < r) (ω : ℝ) (v : V) :
    Filter.Tendsto (fun s => TGLExt.IALDJones.orbit P r ω s v) Filter.atTop (nhds (P v)) :=
  TGLExt.IALDJones.orbit_tendsto_center P hr ω v

example : type_of% @TGLExt.IALDJones.orbit_tendsto_center := @face_has_a_limit
example : type_of% @face_has_a_limit := @TGLExt.IALDJones.orbit_tendsto_center

/-- **T10.c — re-exportação** de `TGLExt.time_witnesses_noncoincidence`: a face distingue todos os instantes
    (o parâmetro positivo é genérico; aqui chama-se `r`). -/
theorem face_distinguishes_instants {m : ℕ} {r : ℝ} (hr : 0 < r) (d : Fin m → ℝ) {i : Fin m}
    (hi : 0 < d i) (x : Fin m → ℝ) (hx : x i ≠ 0) {t₁ t₂ : ℝ} (ht : t₁ ≠ t₂) :
    TGLExt.diagFlow r d t₁ x ≠ TGLExt.diagFlow r d t₂ x :=
  TGLExt.time_witnesses_noncoincidence hr d hi x hx ht

example : type_of% @TGLExt.time_witnesses_noncoincidence := @face_distinguishes_instants
example : type_of% @face_distinguishes_instants := @TGLExt.time_witnesses_noncoincidence

/-- **T10.d.** O relógio modular GIRA as coerências sem encolhê-las: `|(σ_t x)ᵢⱼ| = |xᵢⱼ|`. -/
theorem modular_clock_rotates_without_shrinking {n : Type} [Fintype n] [DecidableEq n] (d : n → ℝ)
    (hd : ∀ i, 0 < d i) (t : ℝ) (x : Matrix n n ℂ) (i j : n) :
    ‖sigma (rhoD d) t x i j‖ = ‖x i j‖ := by
  rw [sigma_diagonal_apply d hd t x i j, norm_mul, modular_factor_norm_one d t i j, one_mul]

/-- **T10.e — re-exportação** de `TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post`: `F(t)P = P = PF(t)`. -/
theorem the_post_is_not_moved {A : Type*} [Ring A] [Algebra ℂ A] {P : A} (hP : IsIdempotentElem P)
    (t : ℝ) :
    TheAxiomAndTheFalseWitness.axiomFlow P t * P = P ∧ P * TheAxiomAndTheFalseWitness.axiomFlow P t = P :=
  TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post hP t

example : type_of% @TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post := @the_post_is_not_moved
example : type_of% @the_post_is_not_moved := @TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post

/-- **T10.e — re-exportação** de `TGLExt.gibbs_sigma`: `ω(σ_t a) = ω(a)`. -/
theorem the_state_is_not_moved {n : Type} [Fintype n] [DecidableEq n] (ρ : Matrix n n ℂ) (t : ℝ)
    (a : Matrix n n ℂ) : gibbs ρ (sigma ρ t a) = gibbs ρ a :=
  gibbs_sigma ρ t a

example : type_of% @TGLExt.gibbs_sigma := @the_state_is_not_moved
example : type_of% @the_state_is_not_moved := @TGLExt.gibbs_sigma

/-- **T10.e — re-exportação** de `TGLExt.sigma_omega`: `σ_t(Ω) = Ω`. -/
theorem the_vector_is_not_moved {n : Type} [Fintype n] [DecidableEq n] (ρ : Matrix n n ℂ) (t : ℝ) :
    modPow ρ t * Omega ρ * modPow ρ (-t) = Omega ρ :=
  sigma_omega ρ t

example : type_of% @TGLExt.sigma_omega := @the_vector_is_not_moved
example : type_of% @the_vector_is_not_moved := @TGLExt.sigma_omega

/-- Sonda V-T10-a: `κ = 1`; `d = (2/3, 1/3)`. -/
example (t : ℝ) : Circle.exp (1 * (t + 2 * Real.pi / 1)) = Circle.exp (1 * t) :=
  clock_reads_modulo_period one_ne_zero t

example (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ) :
    ‖sigma (rhoD ![(2 / 3 : ℝ), 1 / 3]) t x 0 1‖ = ‖x 0 1‖ :=
  modular_clock_rotates_without_shrinking ![(2 / 3 : ℝ), 1 / 3] (fun i => by fin_cases i <;> norm_num)
    t x 0 1

/-! ## T11 — no atrator tracial o relógio modular para (face finita)

[INPUT da gerência — achado a mostrar ao operador] o estado fixo do canal ótico, `½·1`, É o Um absoluto
`absoluteRho (Fin 2)`, e nele o fluxo modular é a identidade. Em III₁ não há estado tracial e `σ_t` é externo
para `t ≠ 0` [KNOWN, Connes 1973]: NADA aqui se estende além da face finita. A leitura «o atrator é onde o
tempo repousa» é do operador. -/

/-- **T11.a.** O estado fixo do canal ótico, `½·1` em M₂(ℂ), é `absoluteRho (Fin 2)`. -/
theorem optical_attractor_is_the_absolute_one :
    (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) = absoluteRho (Fin 2) := by
  rw [absoluteRho, ← Matrix.smul_one_eq_diagonal]
  congr 1
  norm_num [Fintype.card_fin]

/-- **T11.a — re-exportação** de `TGLExt.absoluteOne_flow_trivial` (com o nome desta seção). -/
theorem the_absolute_one_has_no_clock {Region n : Type} [Fintype n] [DecidableEq n] [Nonempty n]
    (O : Region) (t : ℝ) (a : Matrix n n ℂ) : (absoluteOneField Region n).flow O t a = a :=
  absoluteOne_flow_trivial O t a

example : type_of% @TGLExt.absoluteOne_flow_trivial := @the_absolute_one_has_no_clock
example : type_of% @the_absolute_one_has_no_clock := @TGLExt.absoluteOne_flow_trivial

/-- T11 em uma linha: no atrator ótico `½·1` o relógio modular para (`σ_t = id`). -/
theorem optical_attractor_clock_stops (t : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    sigma ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) t a = a := by
  rw [optical_attractor_is_the_absolute_one]
  exact absoluteOne_flow_trivial (Region := Unit) () t a

/-! ## As duas cláusulas compostas (só conjunções, sem dedução nova) -/

/-- **the_two_regimes_of_time** — T4.b (abstrato, discreto e contínuo) ∧ T4.c (c1, c1 < 1, c2) ∧ T6.c ∧
    T7.b ∧ T10.b: o ângulo gira sem pousar; a face contrai, perde pureza, e o seu inverso não é canal; o
    relógio angular lê só a classe. -/
theorem the_two_regimes_of_time :
    (∀ {X : Type u} [MetricSpace X] {f : X → X}, Isometry f → ∀ {x z : X},
        Filter.Tendsto (fun k : ℕ => f^[k] x) Filter.atTop (nhds z) → x = z ∧ f z = z) ∧
    (∀ {X : Type u} [MetricSpace X] (φ : ℝ → X → X), (∀ s t x, φ (s + t) x = φ s (φ t x)) →
        (∀ s, Isometry (φ s)) → ∀ {x z : X},
        Filter.Tendsto (fun t => φ t x) Filter.atTop (nhds z) → x = z ∧ ∀ s, φ s z = z) ∧
    (∀ {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ) (t : ℝ),
        (schurDiag (fun i j => ((Real.exp (-(t * g i j)) : ℝ) : ℂ))).det
          = ((Real.exp (-(t * ∑ i, ∑ j, g i j)) : ℝ) : ℂ)) ∧
    (∀ {n : Type} [Fintype n] (g : n → n → ℝ), (∀ i j, 0 ≤ g i j) → (∃ i j, 0 < g i j) →
        ∀ {t : ℝ}, 0 < t → Real.exp (-(t * ∑ i, ∑ j, g i j)) < 1) ∧
    (∀ {n : Type} [Fintype n] [DecidableEq n] (d : n → ℝ) (t : ℝ),
        (schurDiag (fun i j => Complex.exp ((t : ℂ) * Complex.I
          * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))))).det = 1) ∧
    (∀ {n : Type} [Fintype n] (g : n → n → ℝ), (∀ i j, 0 ≤ g i j) → ∀ {t : ℝ}, 0 < t →
        ∀ (x : Matrix n n ℂ) {i₀ j₀ : n}, 0 < g i₀ j₀ → x i₀ j₀ ≠ 0 →
          purityR (dephase g t x) < purityR x) ∧
    (∀ {γ t : ℝ}, 0 < γ → 0 < t →
        let g : Fin 2 → Fin 2 → ℝ := fun i j => if i = j then 0 else γ
        let ψ : Matrix (Fin 2) (Fin 2) ℂ := (1 / 2 : ℂ) • !![1, 1; 1, 1]
        ψ.PosSemidef ∧ ψ.trace = 1 ∧ ¬ (dephase g (-t) ψ).PosSemidef) ∧
    (∀ {κ : ℝ}, κ ≠ 0 → ∀ t : ℝ, Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t)) ∧
    (∀ t u : ℝ, Circle.exp (0 * t) = Circle.exp (0 * u)) :=
by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro X _ f hf x z h; exact isometry_orbit_converges_only_if_fixed hf h
  · intro X _ φ hgrp hiso x z h; exact isometric_flow_converges_only_if_fixed φ hgrp hiso h
  · intro n _ _ g t; exact dephase_volume g t
  · intro n _ g hg hpos t ht; exact dephase_volume_lt_one g hg hpos ht
  · intro n _ _ d t; exact modular_volume_one d t
  · intro n _ g hg t ht x i₀ j₀ hpos hx; exact purityR_dephase_lt g hg ht x hpos hx
  · intro γ t hγ ht; exact inverse_dephasing_not_positive hγ ht
  · intro κ hκ t; exact clock_reads_modulo_period hκ t
  · exact frozen_clock

end

end TGLExt.TheTimeHasNoRank

/-! ## #print axioms de TODAS as declarações (novas e re-exportadas) — trio esperado:
    [propext, Classical.choice, Quot.sound] -/

#print axioms TGLExt.TheTimeHasNoRank.psiPlus
#print axioms TGLExt.TheTimeHasNoRank.psiPlus_apply
#print axioms TGLExt.TheTimeHasNoRank.psiPlus_01_ne_zero
#print axioms TGLExt.TheTimeHasNoRank.psiPlus_trace
#print axioms TGLExt.TheTimeHasNoRank.psiPlus_posSemidef
#print axioms TGLExt.TheTimeHasNoRank.psiPlus_not_diagonal
#print axioms TGLExt.TheTimeHasNoRank.gRate
#print axioms TGLExt.TheTimeHasNoRank.gRate_00
#print axioms TGLExt.TheTimeHasNoRank.gRate_01
#print axioms TGLExt.TheTimeHasNoRank.gRate_10
#print axioms TGLExt.TheTimeHasNoRank.gRate_11
#print axioms TGLExt.TheTimeHasNoRank.gRate_diag
#print axioms TGLExt.TheTimeHasNoRank.gRate_off
#print axioms TGLExt.TheTimeHasNoRank.gRate_nonneg
#print axioms TGLExt.TheTimeHasNoRank.dephase_apply
#print axioms TGLExt.TheTimeHasNoRank.no_time_matrix
#print axioms TGLExt.TheTimeHasNoRank.no_time_matrix_fin
#print axioms TGLExt.TheTimeHasNoRank.commutator_far_from_scalar
#print axioms TGLExt.TheTimeHasNoRank.no_finite_spectral_translation
#print axioms TGLExt.TheTimeHasNoRank.probe_commutator_far_from_scalar
#print axioms TGLExt.TheTimeHasNoRank.commutator_can_be_nonzero
#print axioms TGLExt.TheTimeHasNoRank.empty_dimension_admits_time
#print axioms TGLExt.TheTimeHasNoRank.weyl_pair_lives_in_L2
#print axioms TGLExt.TheTimeHasNoRank.no_bounded_spectral_translation
#print axioms TGLExt.TheTimeHasNoRank.probe_bounded_spectral_translation
#print axioms TGLExt.TheTimeHasNoRank.time_is_the_modular_flow
#print axioms TGLExt.TheTimeHasNoRank.fixed_sector_is_the_centralizer
#print axioms TGLExt.TheTimeHasNoRank.tracial_state_freezes_the_flow
#print axioms TGLExt.TheTimeHasNoRank.nontracial_state_rejects_the_identity_flow
#print axioms TGLExt.TheTimeHasNoRank.probe_rho_two_thirds_posDef
#print axioms TGLExt.TheTimeHasNoRank.probe_rho_two_thirds_not_tracial
#print axioms TGLExt.TheTimeHasNoRank.unitary_keeps_spectrum_and_purity
#print axioms TGLExt.TheTimeHasNoRank.isometry_iterate'
#print axioms TGLExt.TheTimeHasNoRank.isometry_orbit_converges_only_if_fixed
#print axioms TGLExt.TheTimeHasNoRank.isometric_flow_converges_only_if_fixed
#print axioms TGLExt.TheTimeHasNoRank.rotation_isometry
#print axioms TGLExt.TheTimeHasNoRank.probe_rotation_orbit_has_no_limit
#print axioms TGLExt.TheTimeHasNoRank.frobenius_norm_eq_purityR
#print axioms TGLExt.TheTimeHasNoRank.unitary_conj_isometry
#print axioms TGLExt.TheTimeHasNoRank.modular_flow_is_isometry
#print axioms TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal
#print axioms TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal_entrywise
#print axioms TGLExt.TheTimeHasNoRank.light_flow_group
#print axioms TGLExt.TheTimeHasNoRank.light_modular_orbit_converges_iff_post
#print axioms TGLExt.TheTimeHasNoRank.probe_modular_orbit_of_psiPlus_has_no_limit
#print axioms TGLExt.TheTimeHasNoRank.schurDiag
#print axioms TGLExt.TheTimeHasNoRank.schurDiag_mulVec
#print axioms TGLExt.TheTimeHasNoRank.schurDiag_is_the_dephasing
#print axioms TGLExt.TheTimeHasNoRank.schurDiag_is_the_modular_flow
#print axioms TGLExt.TheTimeHasNoRank.dephase_volume
#print axioms TGLExt.TheTimeHasNoRank.dephase_volume_lt_one
#print axioms TGLExt.TheTimeHasNoRank.modular_volume_one
#print axioms TGLExt.TheTimeHasNoRank.modular_factor_norm_one
#print axioms TGLExt.TheTimeHasNoRank.dephase_factor_norm_le_one
#print axioms TGLExt.TheTimeHasNoRank.probe_gRate_one_sum
#print axioms TGLExt.TheTimeHasNoRank.the_face_lands
#print axioms TGLExt.TheTimeHasNoRank.fixed_set_of_dephasing_is_the_diagonal
#print axioms TGLExt.TheTimeHasNoRank.boost_pow_null
#print axioms TGLExt.TheTimeHasNoRank.volume_kept_yet_lands
#print axioms TGLExt.TheTimeHasNoRank.global_attractor_needs_volume_loss
#print axioms TGLExt.TheTimeHasNoRank.dephasing_lands_without_being_fixed
#print axioms TGLExt.TheTimeHasNoRank.the_record_is_invariant
#print axioms TGLExt.TheTimeHasNoRank.dephase_fixed_states_not_unique
#print axioms TGLExt.TheTimeHasNoRank.purityR_dephase
#print axioms TGLExt.TheTimeHasNoRank.purity_never_grows_under_dephasing
#print axioms TGLExt.TheTimeHasNoRank.purityR_dephase_lt
#print axioms TGLExt.TheTimeHasNoRank.purity_of_hermitian
#print axioms TGLExt.TheTimeHasNoRank.purityR_sigma
#print axioms TGLExt.TheTimeHasNoRank.purityR_modular
#print axioms TGLExt.TheTimeHasNoRank.no_coherence_no_loss
#print axioms TGLExt.TheTimeHasNoRank.unitary_keeps_purity
#print axioms TGLExt.TheTimeHasNoRank.probe_psiPlus_purity
#print axioms TGLExt.TheTimeHasNoRank.purity_grows_backwards
#print axioms TGLExt.TheTimeHasNoRank.probe_psiPlus_dephased_purity
#print axioms TGLExt.TheTimeHasNoRank.dephase_inverse
#print axioms TGLExt.TheTimeHasNoRank.quad_form_fin_two
#print axioms TGLExt.TheTimeHasNoRank.inverse_dephasing_quadratic_form
#print axioms TGLExt.TheTimeHasNoRank.inverse_dephasing_not_positive
#print axioms TGLExt.TheTimeHasNoRank.control_inverse_at_time_zero
#print axioms TGLExt.TheTimeHasNoRank.control_inverse_on_diagonal
#print axioms TGLExt.TheTimeHasNoRank.unitary_inverse_is_a_channel
#print axioms TGLExt.TheTimeHasNoRank.coherence_entry_scaling
#print axioms TGLExt.TheTimeHasNoRank.coherenceScaling
#print axioms TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape
#print axioms TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape_explicit
#print axioms TGLExt.TheTimeHasNoRank.the_record_does_not_scale
#print axioms TGLExt.TheTimeHasNoRank.past_null_ray_contracts
#print axioms TGLExt.TheTimeHasNoRank.wrong_rate_breaks_scaling
#print axioms TGLExt.TheTimeHasNoRank.flow_sq
#print axioms TGLExt.TheTimeHasNoRank.flow_isIdempotentElem_iff
#print axioms TGLExt.TheTimeHasNoRank.flow_isUnit
#print axioms TGLExt.TheTimeHasNoRank.flow_of_one_is_idempotent
#print axioms TGLExt.TheTimeHasNoRank.flow_at_zero_is_idempotent
#print axioms TGLExt.TheTimeHasNoRank.no_finite_instant_is_the_post
#print axioms TGLExt.TheTimeHasNoRank.post_not_isUnit
#print axioms TGLExt.TheTimeHasNoRank.flow_full_rank
#print axioms TGLExt.TheTimeHasNoRank.post_rank_lt
#print axioms TGLExt.TheTimeHasNoRank.the_time_has_no_rank
#print axioms TGLExt.TheTimeHasNoRank.postDiag
#print axioms TGLExt.TheTimeHasNoRank.postDiag_idem
#print axioms TGLExt.TheTimeHasNoRank.postDiag_compl_ne_zero
#print axioms TGLExt.TheTimeHasNoRank.postDiag_ne_one
#print axioms TGLExt.TheTimeHasNoRank.probe_the_time_has_no_rank
#print axioms TGLExt.TheTimeHasNoRank.clock_faithful_iff_one_turn
#print axioms TGLExt.TheTimeHasNoRank.clock_reciprocal_temperature
#print axioms TGLExt.TheTimeHasNoRank.clock_reads_modulo_period
#print axioms TGLExt.TheTimeHasNoRank.frozen_clock
#print axioms TGLExt.TheTimeHasNoRank.frozen_clock_not_faithful
#print axioms TGLExt.TheTimeHasNoRank.face_clock_has_no_period
#print axioms TGLExt.TheTimeHasNoRank.angle_has_no_limit
#print axioms TGLExt.TheTimeHasNoRank.angle_is_periodic
#print axioms TGLExt.TheTimeHasNoRank.face_has_a_limit
#print axioms TGLExt.TheTimeHasNoRank.face_distinguishes_instants
#print axioms TGLExt.TheTimeHasNoRank.modular_clock_rotates_without_shrinking
#print axioms TGLExt.TheTimeHasNoRank.the_post_is_not_moved
#print axioms TGLExt.TheTimeHasNoRank.the_state_is_not_moved
#print axioms TGLExt.TheTimeHasNoRank.the_vector_is_not_moved
#print axioms TGLExt.TheTimeHasNoRank.optical_attractor_is_the_absolute_one
#print axioms TGLExt.TheTimeHasNoRank.the_absolute_one_has_no_clock
#print axioms TGLExt.TheTimeHasNoRank.optical_attractor_clock_stops
#print axioms TGLExt.TheTimeHasNoRank.the_two_regimes_of_time
