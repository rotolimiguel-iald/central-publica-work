import TGLExt.EquivariantSection
import Mathlib.NumberTheory.Real.Irrational

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

/-!
# A ESTAÇÃO — e o par discriminante fóton/neutrino
  [TGLExt — o lema decisivo do handoff da irmã (DERIVACAO_OPERADOR_
   0ABSOLUTO_TERATOLOGIA_E_A_TORRE_DE_BREUER.md, 19/08/2026), face
   finita em kernel; a sombra fail-closed passou no `140_` (18/18)]

* `stationKappa` — os gaps da estação: `1, √2, √5, √6` — a extensão da
  sequência da casa SEM quadrados perfeitos (o fail-closed do `140_`
  pegou `√4 = 2` com relação inteira `2κ₁ − κ₄ = 0`: teratologia
  flagrada; aqui a lição vira TIPO);
* `stationLambda` — `λ = e^{−κ}` (KMS: a razão nasce do gap), com
  ★ `stationLambda_pos/lt_one/injective` — pesos genuínos e todos
  distintos (a não-repetição que o III₁ exige, por sítio);
* ★ `irrational_station_sqrt2/5/6` — os gaps irracionais da estação
  (via `irrational_sqrt_natCast_iff`: 2, 5, 6 não são quadrados);
* ★★ `station_never_closes` — **O CÍRCULO NUNCA FECHA**: para o par de
  gaps `(1, √2)`, `cos t + cos(√2·t) = 2 ↔ t = 0` — o retorno EXATO só
  existe na origem; toda outra volta é espiral. Rota: soma = 2 força
  cada cosseno = 1 (`cos_eq_one_iff`), logo `t = a·2π` e
  `√2·t = b·2π`; se `t ≠ 0`, então `√2 = b/a` — racional, contra
  `irrational_sqrt_two`. A METADE "nunca fecha" do enrolamento do
  `140_`, agora TEOREMA. [A metade "quase-recorre" (f → 1 sem atingir)
  é densidade de rotação irracional — medida no `140_` (0,9999822);
  a formalização fica NOMEADA, não usada.]
* ★★ `photon_neutrino_discriminant` — **O LEMA DECISIVO, tipado**: para
  pesos distintos, existem `Ω` (o inscrito) e `v` (o arbitrário) com o
  MESMO número (`tr(Ω*Ω) = tr(v*v) = 1`) tais que `Ω` é fixo por TODO
  o fluxo modular e `v` NÃO é — **o número não discrimina; a inscrição
  sim**. Sobre o iff da v166 (`sigma_fixed_iff_specExpect`): o fóton é
  o que a seção reconhece; o neutrino é o que ela poda.

HONESTIDADE: face finita; a quase-recorrência e o limite ∞-dim seguem
onde estão (o `140_` mediu; a densidade é [KNOWN] nomeado). β JAMAIS
entra no Lean. Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix

noncomputable section

/-- Os gaps da estação: a extensão da sequência da casa, sem quadrados
    perfeitos (a lição do `140_` como tipo). -/
def stationKappa : Fin 4 → ℝ := ![1, Real.sqrt 2, Real.sqrt 5, Real.sqrt 6]

/-- Os pesos KMS da estação: `λ = e^{−κ}` — a razão nasce do gap. -/
def stationLambda (i : Fin 4) : ℝ := Real.exp (-(stationKappa i))

theorem stationKappa_pos (i : Fin 4) : 0 < stationKappa i := by
  fin_cases i <;> simp [stationKappa]

theorem stationLambda_pos (i : Fin 4) : 0 < stationLambda i :=
  Real.exp_pos _

/-- Cada peso é genuinamente não-tracial: `λ < 1`. -/
theorem stationLambda_lt_one (i : Fin 4) : stationLambda i < 1 := by
  have h := stationKappa_pos i
  unfold stationLambda
  rw [Real.exp_lt_one_iff]
  linarith

/-- Os gaps são estritamente crescentes: `1 < √2 < √5 < √6`. -/
theorem stationKappa_strictMono : StrictMono stationKappa := by
  have sq1 : (1 : ℝ) = Real.sqrt 1 := (Real.sqrt_one).symm
  have h12 : (1 : ℝ) < Real.sqrt 2 := by
    rw [sq1]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h15 : (1 : ℝ) < Real.sqrt 5 := by
    rw [sq1]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h16 : (1 : ℝ) < Real.sqrt 6 := by
    rw [sq1]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h25 : Real.sqrt 2 < Real.sqrt 5 :=
    Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h26 : Real.sqrt 2 < Real.sqrt 6 :=
    Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h56 : Real.sqrt 5 < Real.sqrt 6 :=
    Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  intro i j hij
  fin_cases i <;> fin_cases j <;> simp_all [stationKappa]

/-- ★ A NÃO-REPETIÇÃO que o III₁ exige, por sítio: os pesos são todos
    distintos (nenhum `λ` se repete — o contrário do fator de Powers). -/
theorem stationLambda_injective : Function.Injective stationLambda := by
  intro i j hij
  have : stationKappa i = stationKappa j := by
    have := congrArg Real.log hij
    simpa [stationLambda, Real.log_exp] using this
  exact stationKappa_strictMono.injective this

/-- 2 não é quadrado (prova manual: `decide` trava no kernel e
    `native_decide` é proibido pela auditoria da casa). -/
theorem not_isSquare_two : ¬ IsSquare (2 : ℕ) := by
  rintro ⟨m, hm⟩
  have hb : m ≤ 2 := by nlinarith
  interval_cases m <;> omega

theorem not_isSquare_five : ¬ IsSquare (5 : ℕ) := by
  rintro ⟨m, hm⟩
  have hb : m ≤ 5 := by nlinarith
  interval_cases m <;> omega

theorem not_isSquare_six : ¬ IsSquare (6 : ℕ) := by
  rintro ⟨m, hm⟩
  have hb : m ≤ 6 := by nlinarith
  interval_cases m <;> omega

/-- `√2` é irracional (2 não é quadrado). -/
theorem irrational_station_sqrt2 : Irrational (Real.sqrt 2) := by
  have : Irrational (Real.sqrt (2 : ℕ)) :=
    irrational_sqrt_natCast_iff.mpr not_isSquare_two
  simpa using this

/-- `√5` é irracional (5 não é quadrado). -/
theorem irrational_station_sqrt5 : Irrational (Real.sqrt 5) := by
  have : Irrational (Real.sqrt (5 : ℕ)) :=
    irrational_sqrt_natCast_iff.mpr not_isSquare_five
  simpa using this

/-- `√6` é irracional (6 não é quadrado). -/
theorem irrational_station_sqrt6 : Irrational (Real.sqrt 6) := by
  have : Irrational (Real.sqrt (6 : ℕ)) :=
    irrational_sqrt_natCast_iff.mpr not_isSquare_six
  simpa using this

/-- ★★ O CÍRCULO NUNCA FECHA: o retorno exato do par `(1, √2)` só
    existe na origem — toda outra volta é espiral. A metade
    "nunca fecha" do enrolamento (`140_`), como teorema. -/
theorem station_never_closes (t : ℝ) :
    Real.cos t + Real.cos (Real.sqrt 2 * t) = 2 ↔ t = 0 := by
  constructor
  · intro h
    have hc1 : Real.cos t = 1 := by
      nlinarith [Real.cos_le_one t, Real.cos_le_one (Real.sqrt 2 * t),
        Real.neg_one_le_cos t, Real.neg_one_le_cos (Real.sqrt 2 * t)]
    have hc2 : Real.cos (Real.sqrt 2 * t) = 1 := by
      nlinarith [Real.cos_le_one t, Real.cos_le_one (Real.sqrt 2 * t),
        Real.neg_one_le_cos t, Real.neg_one_le_cos (Real.sqrt 2 * t)]
    obtain ⟨a, ha⟩ := (Real.cos_eq_one_iff t).mp hc1
    obtain ⟨b, hb⟩ := (Real.cos_eq_one_iff (Real.sqrt 2 * t)).mp hc2
    by_contra ht
    have ha0 : (a : ℝ) ≠ 0 := by
      intro h0
      exact ht (by rw [← ha, h0, zero_mul])
    have hπ : (2 * Real.pi) ≠ 0 := by positivity
    have hkey : Real.sqrt 2 * (a : ℝ) = (b : ℝ) := by
      have h2 : Real.sqrt 2 * ((a : ℝ) * (2 * Real.pi))
          = (b : ℝ) * (2 * Real.pi) := by rw [ha, hb]
      field_simp at h2
      linarith [h2]
    exact irrational_station_sqrt2
      ⟨(b : ℚ) / (a : ℚ), by
        push_cast
        rw [div_eq_iff ha0]
        linarith [hkey]⟩
  · intro h
    simp [h]
    norm_num

/-- ★★ O LEMA DECISIVO (degrau 4 do handoff), face finita: para pesos
    DISTINTOS existem o inscrito `Ω` e o arbitrário `v` com o MESMO
    número (`tr = 1`) — mas `Ω` é fixo por todo o fluxo modular e `v`
    não é. **O número não discrimina; a inscrição sim.** O fóton é o
    que a seção reconhece; o neutrino, o que ela poda. -/
theorem photon_neutrino_discriminant (d : Fin 2 → ℝ) (hd : ∀ i, 0 < d i)
    (hne : d 0 ≠ d 1) :
    ∃ (Ω v : Matrix (Fin 2) (Fin 2) ℂ),
      (Ωᴴ * Ω).trace = 1 ∧ (vᴴ * v).trace = 1
      ∧ (∀ t, sigma (rhoD d) t Ω = Ω)
      ∧ ¬ (∀ t, sigma (rhoD d) t v = v) := by
  have hinj : Function.Injective d := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all
  refine ⟨Matrix.single 0 0 1, Matrix.single 0 1 1,
    ?_, ?_, ?_, ?_⟩
  · simp [Matrix.trace, Matrix.mul_apply, Matrix.single_apply,
      Matrix.diag, Fin.sum_univ_two]
  · simp [Matrix.trace, Matrix.mul_apply, Matrix.single_apply,
      Matrix.diag, Fin.sum_univ_two]
  · refine (sigma_fixed_iff_specExpect d hd _).mpr ?_
    ext i j
    by_cases hij : d i = d j
    · simp [hij]
    · simp only [specExpect_apply, if_neg hij, Matrix.single_apply]
      rw [if_neg]
      rintro ⟨h1, h2⟩
      exact hij (by rw [← h1, ← h2])
  · intro hfix
    have := (sigma_fixed_iff_specExpect d hd _).mp hfix
    have h01 := congrFun (congrFun this 0) 1
    simp only [specExpect_apply, if_neg hne] at h01
    simp at h01

end

end TGLExt
