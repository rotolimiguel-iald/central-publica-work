import TGLExt.O16.LightRayGaussianDensity_v2
set_option autoImplicit false
set_option maxHeartbeats 1200000

/-!
# A concrete standard-subspace net on the light ray
[DERIVED — sandbox candidate]
The objects below are constructed from the existing O16 operators and the
existing Fourier-transported standard subspace. No standardness or isotony
field is postulated. This is a real-subspace net of one-particle half-lines;
it is not a von Neumann algebra net in four-dimensional spacetime.
The final negative control preserves the existing obstruction to promoting
a single null translation coordinate to faithful four-dimensional translations.
-/

noncomputable section
open MeasureTheory Filter
open FormaInscrita.RetaDeLuz ChatgptAudit.Continuous049
open ChatgptAudit.FourierBridge016 ChatgptAudit.LightRayCore016
open TGLV350.Regular

namespace F1Rede.LightRay

local instance : Module ℝ L2R := NormedSpace.complexToReal.toModule
local instance : NormedSpace ℝ L2R := NormedSpace.complexToReal

theorem translation_add_apply (a b : ℝ) (f : L2R) :
    U (a+b) f = U a (U b f) := by
  rw [U_add]
  rfl

theorem translation_inv_apply (a : ℝ) (f : L2R) : U (-a) (U a f) = f := by
  rw [← translation_add_apply, neg_add_cancel, U_zero]
  rfl

/-- The concrete null translations are continuous complex linear equivalences. -/
def translationEquiv (a : ℝ) : L2R ≃L[ℂ] L2R where
  toLinearEquiv :=
    { (U a).toLinearMap with
      invFun := U (-a)
      left_inv := translation_inv_apply a
      right_inv := by
        intro f
        change U a (U (-a) f) = f
        simpa only [neg_neg] using translation_inv_apply (-a) f }
  continuous_toFun := (U a).continuous
  continuous_invFun := (U (-a)).continuous

theorem transport_mulI (e : L2R ≃L[ℂ] L2R) (S : ClosedSubmodule ℝ L2R) :
    S.mulI.mapEquiv (e.restrictScalars ℝ) =
      (S.mapEquiv (e.restrictScalars ℝ)).mulI := by
  ext x
  change x ∈ S.mulI.mapEquiv (e.restrictScalars ℝ) ↔
    x ∈ (S.mapEquiv (e.restrictScalars ℝ)).mulI
  simp only [ClosedSubmodule.mulI, ClosedSubmodule.mem_mapEquiv_iff,
    scalarSMulCLE_symm_apply, Units.smul_def, Units.val_inv_eq_inv_val,
    Complex.val_UnitI, Complex.inv_I]
  change (-Complex.I) • e.symm x ∈ S ↔ e.symm ((-Complex.I) • x) ∈ S
  rw [map_smul]

/-- Standardness is proved by transport through a complex linear equivalence. -/
def transportStandard (e : L2R ≃L[ℂ] L2R) (K : StandardSubspace L2R) :
    StandardSubspace L2R where
  toClosedSubmodule := K.toClosedSubmodule.mapEquiv (e.restrictScalars ℝ)
  IsSeparating := by
    rw [← transport_mulI, ← ClosedSubmodule.mapEquiv_inf_eq,
      K.IsSeparating, ClosedSubmodule.mapEquiv_bot_eq_bot]
  IsCyclic := by
    rw [← transport_mulI, ← ClosedSubmodule.mapEquiv_sup_eq,
      K.IsCyclic, ClosedSubmodule.mapEquiv_top_eq_top]

/-- K(a) = U(a) K(0), with the existing O16 standard subspace at a=0. -/
def halfline (a : ℝ) : StandardSubspace L2R :=
  transportStandard (translationEquiv a) (rapidityStandardSubspace (2 * Real.pi^2))

theorem mem_halfline (a : ℝ) (f : L2R) :
    f ∈ (halfline a).toClosedSubmodule ↔
      U (-a) f ∈ (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule :=
  ClosedSubmodule.mem_mapEquiv_iff _ _ _

theorem mem_halfline_image (a : ℝ) (f : L2R) :
    f ∈ (halfline a).toClosedSubmodule ↔
      ∃ g ∈ (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule, U a g = f := by
  rw [mem_halfline]
  constructor
  · intro hf
    refine ⟨U (-a) f, hf, ?_⟩
    simpa only [neg_neg] using translation_inv_apply (-a) f
  · rintro ⟨g, hg, rfl⟩
    simpa only [translation_inv_apply] using hg

theorem halfline_zero :
    (halfline 0).toClosedSubmodule =
      (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule := by
  ext f
  change f ∈ (halfline 0).toClosedSubmodule ↔
    f ∈ (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule
  rw [mem_halfline]
  simp only [neg_zero, U_zero, one_apply_eq_self]

/-- Inclusion follows from the proved O16 half-sided isotony. -/
theorem halfline_antitone {a b : ℝ} (hab : a ≤ b) :
    (halfline b).toClosedSubmodule ≤ (halfline a).toClosedSubmodule := by
  intro f hf
  obtain ⟨g, hg, rfl⟩ := (mem_halfline_image b f).mp hf
  rw [mem_halfline, ← translation_add_apply]
  exact halfline_isotony (-a+b) (by linarith) g hg

/-- Every real translation transports the actual half-line, in both directions. -/
theorem translation_covariance (t a : ℝ) (f : L2R) :
    U t f ∈ (halfline (t+a)).toClosedSubmodule ↔
      f ∈ (halfline a).toClosedSubmodule := by
  rw [mem_halfline, mem_halfline, ← translation_add_apply]
  have heq : -(t+a)+t = -a := by ring
  rw [heq]

theorem translation_image (t a : ℝ) :
    (halfline a).toClosedSubmodule.mapEquiv ((translationEquiv t).restrictScalars ℝ) =
      (halfline (t+a)).toClosedSubmodule := by
  ext f
  change f ∈ (halfline a).toClosedSubmodule.mapEquiv
    ((translationEquiv t).restrictScalars ℝ) ↔ f ∈ (halfline (t+a)).toClosedSubmodule
  rw [ClosedSubmodule.mem_mapEquiv_iff]
  change U (-t) f ∈ (halfline a).toClosedSubmodule ↔
    f ∈ (halfline (t+a)).toClosedSubmodule
  have h := translation_covariance t a (U (-t) f)
  simpa only [show U t (U (-t) f) = f from by
    simpa only [neg_neg] using translation_inv_apply (-t) f] using h.symm

/-- The ray cannot supply faithful four-dimensional translations through one
linear coordinate. This is a proved negative control, not a missing import. -/
theorem no_four_dimensional_promotion (ell : (Fin 4 → ℝ) →ₗ[ℝ] ℝ) :
    ∃ a : Fin 4 → ℝ, a ≠ 0 ∧ U (ell a) = 1 :=
  lightray_not_faithful_in_four U 1 U_zero ell

theorem phase_reflection (s x : ℝ) :
    star (characterPhase s (-x)) = characterPhase s x := by
  simp only [characterPhase, Complex.star_def, ← Complex.exp_conj]
  congr 1
  simp

/-- The multiplier preserves the actual domain and fixed-point equation of
Tomita. Domain membership is obtained from the proved multiplier graph. -/
theorem character_preserves_standard (c s : ℝ) (f : L2R)
    (hf : f ∈ (continuousStandardSubspace c).toClosedSubmodule) :
    characterMultiplier s f ∈ (continuousStandardSubspace c).toClosedSubmodule := by
  obtain ⟨hdom, hfixed⟩ := (continuous_standard_fixed_iff c f).mp hf
  have hgraph : (characterMultiplier s f,
      characterMultiplier s (continuousModularOperator c ⟨f, hdom⟩)) ∈
      (continuousModularOperator c).graph := by
    apply (continuous_modular_graph_iff c _ _).mpr
    filter_upwards [characterMultiplier_ae s (continuousModularOperator c ⟨f, hdom⟩),
      continuous_modular_apply_ae c ⟨f, hdom⟩, characterMultiplier_ae s f]
      with x h1 h2 h3
    simp only [smul_eq_mul] at h1 h3
    rw [h1, h2, h3]
    ring
  have hdom' := LinearPMap.mem_domain_of_mem_graph hgraph
  apply (continuous_standard_fixed_iff c _).mpr
  refine ⟨hdom', ?_⟩
  apply Lp.ext
  have hfix := continuous_tomita_apply_ae c ⟨f, hdom⟩
  rw [hfixed] at hfix
  have hcharNeg := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (characterMultiplier_ae s f)
  filter_upwards [continuous_tomita_apply_ae c ⟨characterMultiplier s f, hdom'⟩,
    characterMultiplier_ae s f, hcharNeg, hfix] with x h1 h2 h3 h4
  simp only [smul_eq_mul] at h2 h3
  change characterMultiplier s f (-x) = characterPhase s (-x) * f (-x) at h3
  change characterMultiplier s f x = characterPhase s x * f x at h2
  rw [h1, h3, star_mul, phase_reflection, h2, h4]
  ring

theorem dilation_preserves_origin (s : ℝ) (f : L2R)
    (hf : f ∈ (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule) :
    D s f ∈ (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule := by
  rw [rapidity_standard_mem, fourier_dilation]
  exact character_preserves_standard _ _ _ ((rapidity_standard_mem _ _).mp hf)

theorem dilation_origin_iff (s : ℝ) (f : L2R) :
    D s f ∈ (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule ↔
      f ∈ (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule := by
  constructor
  · intro hf
    have h := dilation_preserves_origin (-s) (D s f) hf
    have hinv : D (-s) (D s f) = f := by simpa only [neg_neg] using D_inv (-s) f
    rwa [hinv] at h
  · exact dilation_preserves_origin s f

theorem dilation_intertwines (s a : ℝ) (f : L2R) :
    D s (U a f) = U (Real.exp (-s) * a) (D s f) := by
  have hinv : D (-s) (D s f) = f := by simpa only [neg_neg] using D_inv (-s) f
  simpa only [hinv] using borchers_dilation s a (D s f)

/-- Exact dilation covariance of the constructed half-lines. -/
theorem dilation_covariance (s a : ℝ) (f : L2R) :
    D s f ∈ (halfline (Real.exp (-s) * a)).toClosedSubmodule ↔
      f ∈ (halfline a).toClosedSubmodule := by
  rw [mem_halfline, mem_halfline]
  have heq : -(Real.exp (-s) * a) = Real.exp (-s) * (-a) := by ring
  rw [heq, ← dilation_intertwines]
  exact dilation_origin_iff s (U (-a) f)

/-- Non-vacuity follows from cyclicity and the already proved faithfulness
of the concrete null translations, without a new inhabitedness hypothesis. -/
theorem halfline_ne_bot (a : ℝ) : (halfline a).toClosedSubmodule ≠ ⊥ := by
  intro hbot
  have hc := (halfline a).IsCyclic
  have hzero : (⊥ : ClosedSubmodule ℝ L2R) = ⊤ := by
    simpa only [hbot, ClosedSubmodule.mulI, ClosedSubmodule.mapEquiv_bot_eq_bot,
      sup_bot_eq] using hc
  have all_zero (f : L2R) : f = 0 := by
    have hm : f ∈ (⊥ : ClosedSubmodule ℝ L2R) := by rw [hzero]; trivial
    exact hm
  have hu : U 1 = 1 := by
    ext1 f
    change U 1 f = f
    rw [all_zero (U 1 f), all_zero f]
  have impossible := U_faithful 1 hu
  norm_num at impossible

theorem halfline_exists_nonzero (a : ℝ) :
    ∃ f ∈ (halfline a).toClosedSubmodule, f ≠ 0 := by
  by_contra h
  push Not at h
  apply halfline_ne_bot a
  apply le_antisymm _ bot_le
  intro f hf
  change f = 0
  exact h f hf

#print axioms translationEquiv
#print axioms transportStandard
#print axioms halfline
#print axioms mem_halfline_image
#print axioms halfline_antitone
#print axioms translation_covariance
#print axioms translation_image
#print axioms no_four_dimensional_promotion
#print axioms character_preserves_standard
#print axioms dilation_preserves_origin
#print axioms dilation_origin_iff
#print axioms dilation_intertwines
#print axioms dilation_covariance
#print axioms halfline_ne_bot
#print axioms halfline_exists_nonzero

end F1Rede.LightRay

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    match ci with
    | .axiomInfo _ => throwError "NEW_AXIOM_REFUSED: {n}"
    | _ => pure ()
