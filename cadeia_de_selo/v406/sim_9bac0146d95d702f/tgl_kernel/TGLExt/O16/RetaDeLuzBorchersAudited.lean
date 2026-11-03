import Lean
import Mathlib.MeasureTheory.Function.Holder
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.MeasureTheory.Measure.Haar.Unique
import Mathlib.MeasureTheory.Group.Measure
import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.LinearAlgebra.Dimension.RankNullity
import Mathlib.Tactic

/-!
# A RETA DE LUZ: a representacao de energia positiva do grupo ax+b e a relacao de Borchers
  [RASCUNHO DE GERENCIA — frente forma_inscrita_da_luz/habitante_v3, 23/09/2026; scratchpad;
   NAO cunha nome reservado; NAO toca o kernel; NAO move o gate]

  Modelo: o espaco de uma particula da reta de luz, em RAPIDEZ xi = log p (p > 0 o momento nulo):
  L^2(R_+, dp/p) = L^2(R, dxi) (a medida invariante de dilatacao dp/p vira Lebesgue em xi).

    translacao nula   U(a) f (xi) = exp(i a e^xi) f(xi)       (gerador P = e^xi > 0: ENERGIA POSITIVA)
    dilatacao         D(s) f (xi) = f(xi - s)                  (o boost da cunha, lido na reta)

  O que este arquivo PROVA [DERIVED, kernel Lean, zero sorry]:
    (1) U e grupo:  U 0 = 1,  U (a + b) = U a * U b;
    (2) D e grupo de isometrias: D 0 = id, D (s + t) = D s ∘ D t, D s ∘ D (-s) = id;
    (3) ★ a RELACAO DE BORCHERS como identidade entre operadores concretos:
            D s * U a * D (-s) = U (e^{-s} a);
        e, com Delta^{it} := D(2 pi t) (a normalizacao de Bisognano--Wichmann),
            Delta^{it} U(a) Delta^{-it} = U(e^{-2 pi t} a);
    (4) FIDELIDADE na reta: U a = 1 -> a = 0;
    (5) a PAREDE DE TIPO: nenhuma representacao de R^4 que se fatora por UM funcional linear (a reta de luz
        sozinha) satisfaz a fidelidade em Fin 4 -> R: existe a /= 0 com U4 a = 1.

  O que este arquivo NAO prova [OPEN]:
    * que D(2 pi t) E o grupo modular de algum subespaco padrao K (a identificacao modular: Borchers/BGL
      Thm 3.2 dizem que, dado K com (3.1)-(3.2), U(a)K ⊆ K (a ≥ 0) <-> energia positiva; aqui Delta^{it} e
      DEFINIDO pela dilatacao, logo (3) com o fator 2 pi e DEFINICIONAL, nao o teorema de Borchers);
    * espectro continuo de D (ausencia de autovetores) — proximo elo;
    * a segunda quantizacao (vacuo, rede de von Neumann) — sem ela nao ha TGLSpecificAQFTWitness;
    * a cunha 3+1 (representacao de Wigner de massa zero).
  beta nao aparece. Nada aqui e fisica confirmada.
-/

set_option autoImplicit false

noncomputable section
open MeasureTheory Filter
open scoped ENNReal

namespace FormaInscrita.RetaDeLuz

/-- o espaco de uma particula da reta de luz, em rapidez. -/
abbrev L2R := Lp ℂ 2 (volume : Measure ℝ)

/-! ## 1. A translacao nula: multiplicacao por exp(i a e^xi) -/

/-- o momento nulo em rapidez: p(xi) = e^xi > 0. -/
def nullMomentum (ξ : ℝ) : ℝ := Real.exp ξ

theorem nullMomentum_pos (ξ : ℝ) : 0 < nullMomentum ξ := Real.exp_pos ξ

/-- [DERIVED] o espectro do gerador e EXATAMENTE (0, ∞): energia positiva, sem zero (sem modo invariante). -/
theorem nullMomentum_range : Set.range nullMomentum = Set.Ioi 0 := by
  ext p
  constructor
  · rintro ⟨ξ, rfl⟩; exact nullMomentum_pos ξ
  · intro hp; exact ⟨Real.log p, Real.exp_log hp⟩

/-- o simbolo da translacao nula por a. -/
def transSymbol (a ξ : ℝ) : ℂ := Complex.exp (Complex.I * ((a * nullMomentum ξ : ℝ) : ℂ))

theorem transSymbol_norm (a ξ : ℝ) : ‖transSymbol a ξ‖ = 1 := by
  unfold transSymbol
  rw [Complex.norm_exp]
  simp

theorem transSymbol_continuous (a : ℝ) : Continuous (transSymbol a) := by
  unfold transSymbol nullMomentum
  fun_prop

theorem transSymbol_zero (ξ : ℝ) : transSymbol 0 ξ = 1 := by
  simp [transSymbol]

theorem transSymbol_add (a b ξ : ℝ) :
    transSymbol (a + b) ξ = transSymbol a ξ * transSymbol b ξ := by
  unfold transSymbol
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

/-- [DERIVED] a covariancia do simbolo sob a dilatacao: o nucleo da relacao de Borchers. -/
theorem transSymbol_shift (a s ξ : ℝ) :
    transSymbol a (ξ + -s) = transSymbol (Real.exp (-s) * a) ξ := by
  unfold transSymbol nullMomentum
  congr 1
  rw [Real.exp_add]
  push_cast
  ring

/-- o simbolo como vetor de L^∞. -/
def symbolLinf (a : ℝ) : Lp ℂ ∞ (volume : Measure ℝ) :=
  (memLp_top_of_bound (transSymbol_continuous a).aestronglyMeasurable 1
    (Eventually.of_forall fun ξ => (transSymbol_norm a ξ).le)).toLp _

theorem symbolLinf_ae (a : ℝ) : symbolLinf a =ᵐ[volume] transSymbol a :=
  MemLp.coeFn_toLp _

/-- **U(a)** — a translacao nula, pelo mapa de Holder L^∞ × L^2 → L^2. -/
def U (a : ℝ) : L2R →L[ℂ] L2R :=
  (ContinuousLinearMap.lsmul ℂ ℂ).holderL volume ∞ 2 2 (symbolLinf a)

theorem U_ae (a : ℝ) (f : L2R) : U a f =ᵐ[volume] fun ξ => transSymbol a ξ * f ξ := by
  have h := (ContinuousLinearMap.lsmul ℂ ℂ).coeFn_holder (r := 2) (symbolLinf a) f
  filter_upwards [h, symbolLinf_ae a] with ξ hξ hs
  simpa only [U, ContinuousLinearMap.holderL_apply_apply, ContinuousLinearMap.lsmul_apply,
    smul_eq_mul, hs] using hξ

/-- [DERIVED] U 0 = 1. -/
theorem U_zero : U 0 = 1 := by
  ext1 f
  apply Lp.ext
  filter_upwards [U_ae 0 f] with ξ hξ
  rw [hξ, transSymbol_zero, one_mul]
  rfl

/-- [DERIVED] U (a + b) = U a * U b. -/
theorem U_add (a b : ℝ) : U (a + b) = U a * U b := by
  ext1 f
  apply Lp.ext
  filter_upwards [U_ae (a + b) f, U_ae a (U b f), U_ae b f] with ξ h1 h2 h3
  change (U (a + b) f) ξ = (U a (U b f)) ξ
  rw [h1, h2, h3, transSymbol_add, mul_assoc]

/-! ## 2. A dilatacao (o boost lido na reta): D(s) f (xi) = f(xi - s) -/

theorem shift_mp (s : ℝ) : MeasurePreserving (fun ξ : ℝ => ξ + -s) volume volume :=
  measurePreserving_add_right volume (-s)

/-- **D(s)** — a dilatacao, como isometria linear de L^2 (composicao com xi ↦ xi - s). -/
def D (s : ℝ) : L2R →ₗᵢ[ℂ] L2R :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun ξ : ℝ => ξ + -s) (shift_mp s)

theorem D_ae (s : ℝ) (f : L2R) : D s f =ᵐ[volume] fun ξ => f (ξ + -s) :=
  Lp.coeFn_compMeasurePreserving f (shift_mp s)

/-- [DERIVED] D (s + t) = D s ∘ D t (lei de grupo). -/
theorem D_add (s t : ℝ) (f : L2R) : D (s + t) f = D s (D t f) := by
  apply Lp.ext
  have hq := (shift_mp s).quasiMeasurePreserving
  have hcomp : (fun ξ => (D t f) (ξ + -s)) =ᵐ[volume] fun ξ => f (ξ + -s + -t) :=
    hq.ae_eq_comp (D_ae t f)
  filter_upwards [D_ae (s + t) f, D_ae s (D t f), hcomp] with ξ h1 h2 h3
  rw [h1, h2, h3]
  congr 1
  ring

theorem D_zero (f : L2R) : D 0 f = f := by
  apply Lp.ext
  filter_upwards [D_ae 0 f] with ξ h
  rw [h]
  simp

theorem D_inv (s : ℝ) (f : L2R) : D s (D (-s) f) = f := by
  rw [← D_add, add_neg_cancel, D_zero]

/-! ## 3. ★ A RELACAO DE BORCHERS entre os operadores concretos -/

/-- [DERIVED] ★ D(s) U(a) D(-s) = U(e^{-s} a): a dilatacao contrai a translacao nula. -/
theorem borchers_dilation (s a : ℝ) (f : L2R) :
    D s (U a (D (-s) f)) = U (Real.exp (-s) * a) f := by
  apply Lp.ext
  have hq := (shift_mp s).quasiMeasurePreserving
  have hU : (fun ξ => (U a (D (-s) f)) (ξ + -s)) =ᵐ[volume]
      fun ξ => transSymbol a (ξ + -s) * (D (-s) f) (ξ + -s) :=
    hq.ae_eq_comp (U_ae a (D (-s) f))
  have hD : (fun ξ => (D (-s) f) (ξ + -s)) =ᵐ[volume] fun ξ => f (ξ + -s + - -s) :=
    hq.ae_eq_comp (D_ae (-s) f)
  filter_upwards [D_ae s (U a (D (-s) f)), hU, hD, U_ae (Real.exp (-s) * a) f]
    with ξ h1 h2 h3 h4
  rw [h1, h2, h3, h4, transSymbol_shift]
  congr 2
  ring

/-- o grupo «modular» na normalizacao de Bisognano--Wichmann: Delta^{it} := D(2 pi t).
    ⚠ DEFINICAO: que isto seja o grupo modular de um subespaco padrao e [OPEN] neste arquivo. -/
def modularCandidate (t : ℝ) : L2R →ₗᵢ[ℂ] L2R := D (2 * Real.pi * t)

/-- [DERIVED, definicional no fator 2 pi] Delta^{it} U(a) Delta^{-it} = U(e^{-2 pi t} a). -/
theorem borchers_bw_form (t a : ℝ) (f : L2R) :
    modularCandidate t (U a (modularCandidate (-t) f)) = U (Real.exp (-(2 * Real.pi * t)) * a) f := by
  have h : 2 * Real.pi * -t = -(2 * Real.pi * t) := by ring
  unfold modularCandidate
  rw [h]
  exact borchers_dilation (2 * Real.pi * t) a f

/-! ## 4. FIDELIDADE na reta: U a = 1 → a = 0 -/

/-- [DERIVED] o simbolo nao e identicamente 1 se a ≠ 0: em xi0 = log(pi/|a|) ele vale −1. -/
theorem transSymbol_ne_one {a : ℝ} (ha : a ≠ 0) : ∃ ξ : ℝ, transSymbol a ξ ≠ 1 := by
  have hm1 : (-1 : ℂ) ≠ 1 := by norm_num
  rcases lt_or_gt_of_ne ha with h | h
  · refine ⟨Real.log (Real.pi / -a), ?_⟩
    have hp : a * nullMomentum (Real.log (Real.pi / -a)) = -Real.pi := by
      unfold nullMomentum
      rw [Real.exp_log (div_pos Real.pi_pos (neg_pos.mpr h))]
      field_simp
    unfold transSymbol
    rw [hp]
    have e : Complex.I * ((-Real.pi : ℝ) : ℂ) = -(Real.pi * Complex.I) := by push_cast; ring
    rw [e, Complex.exp_neg, Complex.exp_pi_mul_I]
    norm_num
  · refine ⟨Real.log (Real.pi / a), ?_⟩
    have hp : a * nullMomentum (Real.log (Real.pi / a)) = Real.pi := by
      unfold nullMomentum
      rw [Real.exp_log (div_pos Real.pi_pos h)]
      field_simp
    unfold transSymbol
    rw [hp]
    have e : Complex.I * ((Real.pi : ℝ) : ℂ) = Real.pi * Complex.I := by ring
    rw [e, Complex.exp_pi_mul_I]
    exact hm1

/-- [DERIVED] ★ FIDELIDADE: so a translacao nula age trivialmente na reta de luz. -/
theorem U_faithful (a : ℝ) (h : U a = 1) : a = 0 := by
  by_contra ha
  obtain ⟨ξ₀, hξ₀⟩ := transSymbol_ne_one ha
  -- o conjunto aberto onde o simbolo difere de 1, cortado a um intervalo limitado
  set S : Set ℝ := {ξ | transSymbol a ξ ≠ 1} ∩ Set.Ioo (ξ₀ - 1) (ξ₀ + 1) with hSdef
  have hSopen : IsOpen S :=
    (isOpen_ne_fun (transSymbol_continuous a) continuous_const).inter isOpen_Ioo
  have hSne : S.Nonempty := ⟨ξ₀, hξ₀, by constructor <;> linarith⟩
  have hSpos : 0 < volume S := hSopen.measure_pos volume hSne
  -- o vetor teste: o indicador de [ξ₀ - 1, ξ₀ + 1]
  have hmeas : MeasurableSet (Set.Icc (ξ₀ - 1) (ξ₀ + 1)) := measurableSet_Icc
  have hfin : volume (Set.Icc (ξ₀ - 1) (ξ₀ + 1)) ≠ ∞ := by
    rw [Real.volume_Icc]; exact ENNReal.ofReal_ne_top
  let f : L2R := indicatorConstLp 2 hmeas hfin (1 : ℂ)
  have hf : U a f = f := by rw [h]; rfl
  have hfae : (f : ℝ → ℂ) =ᵐ[volume] (Set.Icc (ξ₀ - 1) (ξ₀ + 1)).indicator (fun _ => (1 : ℂ)) :=
    indicatorConstLp_coeFn
  have hbad : ∀ᵐ ξ ∂volume, ξ ∈ Set.Icc (ξ₀ - 1) (ξ₀ + 1) → transSymbol a ξ = 1 := by
    have h1 := U_ae a f
    rw [hf] at h1
    filter_upwards [h1, hfae] with ξ hU hI
    intro hξ
    rw [hI, Set.indicator_of_mem hξ] at hU
    simpa using hU.symm
  have hzero : volume S = 0 := by
    rw [ae_iff] at hbad
    apply measure_mono_null _ hbad
    intro ξ hξ himp
    exact hξ.1 (himp (Set.Ioo_subset_Icc_self hξ.2))
  exact (ne_of_gt hSpos) hzero

/-! ## 5. A PAREDE DE TIPO: a reta sozinha NAO e fiel em Fin 4 → ℝ -/

/-- [DERIVED] ★ toda «translacao de R^4» que se fatora por UM funcional linear (U4 = F ∘ ℓ, F 0 = 1) tem
    uma translacao NAO nula agindo trivialmente: a reta de luz sozinha NAO habita `translations_faithful`
    do contrato v3/v3.1 (Fin 4 → ℝ). -/
theorem lightray_not_faithful_in_four {X : Type*} (F : ℝ → X) (x1 : X) (hF : F 0 = x1)
    (ℓ : (Fin 4 → ℝ) →ₗ[ℝ] ℝ) :
    ∃ a : Fin 4 → ℝ, a ≠ 0 ∧ F (ℓ a) = x1 := by
  have hrank := LinearMap.finrank_range_add_finrank_ker ℓ
  have hr : Module.finrank ℝ (LinearMap.range ℓ) ≤ 1 := by
    have := Submodule.finrank_le (LinearMap.range ℓ)
    simpa using this
  have hdim : Module.finrank ℝ (Fin 4 → ℝ) = 4 := by simp
  have hk : 0 < Module.finrank ℝ (LinearMap.ker ℓ) := by omega
  have hne : LinearMap.ker ℓ ≠ ⊥ := by
    intro hbot
    rw [hbot, finrank_bot] at hk
    exact lt_irrefl 0 hk
  obtain ⟨a, ha, ha0⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hne
  exact ⟨a, ha0, by rw [LinearMap.mem_ker.mp ha, hF]⟩

/-- a instancia: a reta de luz levantada a R^4 pela coordenada nula a⁺ = a⁰ + a¹ nao e fiel. -/
theorem lightray_lift_not_faithful :
    ∃ a : Fin 4 → ℝ, a ≠ 0 ∧ U (a 0 + a 1) = 1 := by
  let ℓ : (Fin 4 → ℝ) →ₗ[ℝ] ℝ :=
    (LinearMap.proj (R := ℝ) (φ := fun _ : Fin 4 => ℝ) 0) +
      (LinearMap.proj (R := ℝ) (φ := fun _ : Fin 4 => ℝ) 1)
  obtain ⟨a, ha0, ha⟩ := lightray_not_faithful_in_four U 1 U_zero ℓ
  exact ⟨a, ha0, by simpa [ℓ] using ha⟩

#print axioms nullMomentum_range
#print axioms U_zero
#print axioms U_add
#print axioms D_add
#print axioms D_inv
#print axioms borchers_dilation
#print axioms borchers_bw_form
#print axioms U_faithful
#print axioms lightray_not_faithful_in_four
#print axioms lightray_lift_not_faithful

end FormaInscrita.RetaDeLuz

/- Audit-only append: original source preserved byte-for-byte as prefix. -/
#print axioms FormaInscrita.RetaDeLuz.nullMomentum_pos
#print axioms FormaInscrita.RetaDeLuz.transSymbol_norm
#print axioms FormaInscrita.RetaDeLuz.transSymbol_continuous
#print axioms FormaInscrita.RetaDeLuz.transSymbol_zero
#print axioms FormaInscrita.RetaDeLuz.transSymbol_add
#print axioms FormaInscrita.RetaDeLuz.transSymbol_shift
#print axioms FormaInscrita.RetaDeLuz.symbolLinf_ae
#print axioms FormaInscrita.RetaDeLuz.U_ae
#print axioms FormaInscrita.RetaDeLuz.shift_mp
#print axioms FormaInscrita.RetaDeLuz.D_ae
#print axioms FormaInscrita.RetaDeLuz.D_zero
#print axioms FormaInscrita.RetaDeLuz.transSymbol_ne_one


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
