import TGLExt.V351ModularImplementation
import TGLExt.V351SineResolventApprox
import TGLExt.V351AntiunitaryResolventPhase
import TGLExt.PhaseFrequencySeparation
import Mathlib.Analysis.CStarAlgebra.GelfandDuality

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open ChatgptAudit TGLExt MeasureTheory Filter
open scoped ComplexOrder Topology
noncomputable section

/-- Endpoint-safe scalar consumer of the previously proved frequency separation.
This private calculation alone does not assert the original operator balance. -/
private theorem damped_phase_scalar_balance (r a b : ℝ)
    (hr : r ∈ Set.Icc 0 1) (ha : a ∈ Set.Icc 0 1) (hb : b ∈ Set.Icc 0 1)
    (hphase : ∀ t : ℝ,
      resolventPhaseFunction t r * (resolventDamping a : ℂ) * (resolventDamping b : ℂ) =
      (resolventDamping r : ℂ) * resolventPhaseFunction t a * resolventPhaseFunction (-t) b) :
    (resolventDamping r * resolventDamping a * resolventDamping b) *
      ((1-r)*a*(1-b)-r*(1-a)*b) = 0 := by
  by_cases hz : resolventDamping r * resolventDamping a * resolventDamping b = 0
  · rw [hz, zero_mul]
  have hdr : resolventDamping r ≠ 0 := fun h => hz (by rw [h, zero_mul, zero_mul])
  have hda : resolventDamping a ≠ 0 := fun h => hz (by rw [h, mul_zero, zero_mul])
  have hdb : resolventDamping b ≠ 0 := fun h => hz (by rw [h, mul_zero])
  have hs (x : ℝ) (hx : x ∈ Set.Icc 0 1) (hd : resolventDamping x ≠ 0) :
      0 < x ∧ 0 < 1-x := by
    have h0 : x ≠ 0 := fun h => hd (by simp [resolventDamping,h])
    have h1 : x ≠ 1 := fun h => hd (by simp [resolventDamping,h])
    exact ⟨lt_of_le_of_ne hx.1 h0.symm, sub_pos.mpr (lt_of_le_of_ne hx.2 h1)⟩
  obtain ⟨hr0, hr1⟩ := hs r hr hdr
  obtain ⟨ha0, ha1⟩ := hs a ha hda
  obtain ⟨hb0, hb1⟩ := hs b hb hdb
  have hc : ((resolventDamping r * resolventDamping a * resolventDamping b : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast hz
  have hfreq : Real.log ((1-r)/r) = Real.log ((1-a)/a) - Real.log ((1-b)/b) := by
    apply Commutation032.modular_phase_frequency_separation _ _ _ hc
    intro t
    have hp : modularPhase t (Real.log ((1-a)/a) - Real.log ((1-b)/b)) =
        modularPhase t (Real.log ((1-a)/a)) * modularPhase (-t) (Real.log ((1-b)/b)) := by
      unfold modularPhase
      rw [← Complex.exp_add]
      congr 1
      push_cast
      ring
    rw [hp]
    have ht := hphase t
    simp only [resolventPhaseFunction] at ht
    push_cast
    calc
      _ = (resolventDamping r : ℂ) * modularPhase t (Real.log ((1-r)/r)) *
          (resolventDamping a : ℂ) * (resolventDamping b : ℂ) := by ring
      _ = _ := ht
      _ = _ := by ring
  have he : (1-r)/r = ((1-a)/a) / ((1-b)/b) := by
    calc
      _ = Real.exp (Real.log ((1-r)/r)) := (Real.exp_log (div_pos hr1 hr0)).symm
      _ = Real.exp (Real.log ((1-a)/a) - Real.log ((1-b)/b)) := congrArg Real.exp hfreq
      _ = _ := by rw [Real.exp_sub, Real.exp_log (div_pos ha1 ha0), Real.exp_log (div_pos hb1 hb0)]
  have he' : (1-r)*a*(1-b) = r*(1-a)*b := by
    field_simp [ne_of_gt hr0, ne_of_gt ha0, ne_of_gt hb0, ne_of_gt hb1] at he
    nlinarith [he]
  rw [he', sub_self, mul_zero]

private theorem damped_phase_commutative_balance {C : Type*} [CommCStarAlgebra C]
    [ContinuousFunctionalCalculus ℂ C IsStarNormal]
    [PartialOrder C] [StarOrderedRing C] (T A B : C)
    (hT : T ∈ Set.Icc 0 1) (hA : A ∈ Set.Icc 0 1) (hB : B ∈ Set.Icc 0 1)
    (hphase : ∀ t : ℝ,
      cfc (fun z : ℂ => resolventPhaseFunction t z.re) T * (A*(1-A)) * (B*(1-B)) =
      (T*(1-T)) * cfc (fun z : ℂ => resolventPhaseFunction t z.re) A *
        cfc (fun z : ℂ => resolventPhaseFunction (-t) z.re) B) :
    ((T*(1-T))*(A*(1-A))*(B*(1-B))) * ((1-T)*A*(1-B)-T*(1-A)*B) = 0 := by
  apply (gelfandTransform_isometry C).injective
  ext χ
  change χ (((T*(1-T))*(A*(1-A))*(B*(1-B))) * ((1-T)*A*(1-B)-T*(1-A)*B)) = χ 0
  have hrange (X : C) (hX : X ∈ Set.Icc 0 1) :
      (χ X).re ∈ Set.Icc 0 1 ∧ χ X = ((χ X).re : ℂ) := by
    have h0 : 0 ≤ χ X := by simpa only [map_zero] using (OrderHomClass.monotone χ hX.1)
    have h1 : χ X ≤ 1 := by simpa only [map_one] using (OrderHomClass.monotone χ hX.2)
    refine ⟨⟨(Complex.nonneg_iff.mp h0).1, h1.1⟩, ?_⟩
    apply Complex.ext
    · rfl
    · simpa using (Complex.nonneg_iff.mp h0).2.symm
  obtain ⟨htr, htc⟩ := hrange T hT
  obtain ⟨har, hac⟩ := hrange A hA
  obtain ⟨hbr, hbc⟩ := hrange B hB
  have heval (X : C) (t : ℝ) :
      χ (cfc (fun z : ℂ => resolventPhaseFunction t z.re) X) =
        resolventPhaseFunction t (χ X).re := by
    have hf : Continuous (fun z : ℂ => resolventPhaseFunction t z.re) :=
      (resolventPhaseFunction_continuous t).comp Complex.continuous_re
    have hh := StarAlgHomClass.map_cfc (S := ℂ) χ _ X hf.continuousOn
    exact hh.trans (by
      simpa using cfc_algebraMap (A := ℂ) (χ X) (fun z : ℂ => resolventPhaseFunction t z.re))
  have hs := damped_phase_scalar_balance (χ T).re (χ A).re (χ B).re htr har hbr (by
    intro t
    have hh := congrArg χ (hphase t)
    simp only [map_mul, map_sub, map_one, heval] at hh
    rw [htc, hac, hbc] at hh
    simpa only [Complex.ofReal_re, resolventDamping, Complex.ofReal_mul,
      Complex.ofReal_sub, Complex.ofReal_one] using hh)
  simp only [map_mul, map_sub, map_one, map_zero]
  rw [htc, hac, hbc]
  exact_mod_cast hs

open scoped IsMulCommutative in
private theorem damped_phase_operator_balance {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (T A B : H →L[ℂ] H)
    (hT : T ∈ Set.Icc 0 1) (hA : A ∈ Set.Icc 0 1) (hB : B ∈ Set.Icc 0 1)
    (hTA : Commute T A) (hTB : Commute T B) (hAB : Commute A B)
    (hiT : Function.Injective T) (hjT : Function.Injective (1-T : H →L[ℂ] H))
    (hiA : Function.Injective A) (hjA : Function.Injective (1-A : H →L[ℂ] H))
    (hiB : Function.Injective B) (hjB : Function.Injective (1-B : H →L[ℂ] H))
    (hphase : ∀ t : ℝ,
      resolventPhaseOperator T t * resolventDampingOperator A * resolventDampingOperator B =
      resolventDampingOperator T * resolventPhaseOperator A t * resolventPhaseOperator B (-t)) :
    (1-T)*A*(1-B) = T*(1-A)*B := by
  let U := StarAlgebra.adjoin ℂ ({T,A,B} : Set (H →L[ℂ] H))
  let S := U.topologicalClosure
  have hpair : ∀ x ∈ ({T,A,B} : Set (H →L[ℂ] H)), ∀ y ∈ ({T,A,B} : Set (H →L[ℂ] H)),
      x*y=y*x := by
    intro x hx y hy
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx hy
    rcases hx with rfl | rfl | rfl <;> rcases hy with rfl | rfl | rfl
    all_goals first | rfl | exact hTA.eq | exact hTA.eq.symm | exact hTB.eq |
      exact hTB.eq.symm | exact hAB.eq | exact hAB.eq.symm
  have hstar (x : H →L[ℂ] H) (hx : x ∈ ({T,A,B} : Set (H →L[ℂ] H))) : star x=x := by
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl | rfl
    · exact (IsSelfAdjoint.of_nonneg hT.1).star_eq
    · exact (IsSelfAdjoint.of_nonneg hA.1).star_eq
    · exact (IsSelfAdjoint.of_nonneg hB.1).star_eq
  haveI : IsMulCommutative U := StarAlgebra.isMulCommutative_adjoin ℂ hpair (by
    intro x hx y hy
    rw [hstar y hy]
    exact hpair x hx y hy)
  letI : CommRing S := U.commRingTopologicalClosure (fun x y => mul_comm x y)
  haveI : IsClosed (S : Set (H →L[ℂ] H)) := U.isClosed_topologicalClosure
  letI : CommCStarAlgebra S := { }
  letI : IsometricContinuousFunctionalCalculus ℂ S IsStarNormal :=
    IsStarNormal.instIsometricContinuousFunctionalCalculus
  letI : PartialOrder S := CStarAlgebra.spectralOrder S
  letI : Preorder S := (CStarAlgebra.spectralOrder S).toPreorder
  letI : LE S := (CStarAlgebra.spectralOrder S).toLE
  letI : StarOrderedRing S := CStarAlgebra.spectralOrderedRing S
  have hmem (X : H →L[ℂ] H) (hx : X ∈ ({T,A,B} : Set (H →L[ℂ] H))) : X ∈ S :=
    StarSubalgebra.le_topologicalClosure U (StarAlgebra.subset_adjoin ℂ _ hx)
  let Ts : S := ⟨T,hmem T (by simp)⟩
  let As : S := ⟨A,hmem A (by simp)⟩
  let Bs : S := ⟨B,hmem B (by simp)⟩
  have hpos (X : S) (hX : 0 ≤ X.val) : 0 ≤ X := by
    have hz : CFC.sqrt X.val ∈ S := by
      rw [CFC.sqrt_eq_real_sqrt X.val hX]
      exact cfcₙ_mem (𝕜' := ℂ) Real.sqrt X.property
    let Z : S := ⟨CFC.sqrt X.val,hz⟩
    have he : star Z * Z = X := by
      apply Subtype.ext
      change star (CFC.sqrt X.val) * CFC.sqrt X.val = X.val
      rw [(IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg X.val)).star_eq]
      exact (CFC.sqrt_eq_iff X.val (CFC.sqrt X.val) hX (CFC.sqrt_nonneg X.val)).mp rfl
    rw [← he]
    exact star_mul_self_nonneg Z
  have hbounds (X : S) (hX : X.val ∈ Set.Icc 0 1) : X ∈ Set.Icc 0 1 :=
    ⟨hpos X hX.1, sub_nonneg.mp (hpos (1-X) (sub_nonneg.mpr hX.2))⟩
  have hcfc (X : S) (t : ℝ) :
      S.subtype (cfc (fun z : ℂ => resolventPhaseFunction t z.re) X) =
        cfc (fun z : ℂ => resolventPhaseFunction t z.re) X.val :=
    S.subtype.map_cfc _ X ((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn
  have hs := damped_phase_commutative_balance Ts As Bs
    (hbounds Ts hT) (hbounds As hA) (hbounds Bs hB) (by
      intro t
      apply Subtype.val_injective
      change S.subtype (_ * _ * _) = S.subtype (_ * _ * _)
      simp only [map_mul, map_sub, map_one]
      erw [hcfc Ts t, hcfc As t, hcfc Bs (-t)]
      exact hphase t)
  have he : ((T*(1-T))*(A*(1-A))*(B*(1-B))) * ((1-T)*A*(1-B)-T*(1-A)*B) = 0 := by
    have hh := congrArg S.subtype hs
    simpa only [map_mul, map_sub, map_one, map_zero, StarSubalgebra.subtype_apply, Ts, As, Bs] using hh
  apply sub_eq_zero.mp
  ext1 x
  apply (resolventDampingOperator_injective T hiT hjT).comp
    ((resolventDampingOperator_injective A hiA hjA).comp
      (resolventDampingOperator_injective B hiB hjB))
  have hh := congrArg (fun W : H →L[ℂ] H => W x) he
  simpa only [resolventDampingOperator, Function.comp_apply, mul_apply_eq_comp,
    map_zero, zero_apply] using hh

private theorem scalar_representation_vector_injective (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra) (ha : Function.Injective a.val) :
    Function.Injective (scalarGNSRepresentation P a) := by
  have hi (s : ℝ) : Function.Injective (dualAmbient s a.val) := by
    rw [dualAmbient_apply, characterMultiplier_star]
    exact (characterMultiplierIsometry s).injective.comp
      (ha.comp (characterMultiplierIsometry (-s)).injective)
  intro x y h
  have he : operatorFieldLift (dualIntegralFamily a.val) x.val =
      operatorFieldLift (dualIntegralFamily a.val) y.val := congrArg Subtype.val h
  apply Subtype.ext
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily a.val) x.val,
    operatorFieldLift_ae (dualIntegralFamily a.val) y.val] with s hx hy
  apply hi s
  exact hx.symm.trans ((congrArg (fun f : RegularHilbert (RegularHilbert (TowerHilbert P)) => f s) he).trans hy)

open scoped CStarAlgebra in
private theorem closed_representation_cfc {H K : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] [NormedAddCommGroup K]
    [InnerProductSpace ℂ K] [CompleteSpace K]
    (N : StarSubalgebra ℂ (H →L[ℂ] H)) [IsClosed (N : Set (H →L[ℂ] H))]
    (π : N →⋆ₐ[ℂ] (K →L[ℂ] K)) (a : N) (ha : IsSelfAdjoint a.val)
    (f : ℂ → ℂ) (hf : Continuous f) :
    ∃ hm : cfc f a.val ∈ N, π ⟨cfc f a.val,hm⟩ = cfc f (π a) ∧
      ∀ T : K →L[ℂ] K, Commute T (π a) → Commute T (π ⟨cfc f a.val,hm⟩) := by
  letI : CStarAlgebra N := StarSubalgebra.cstarAlgebra N
  letI : IsometricContinuousFunctionalCalculus ℂ N IsStarNormal :=
    IsStarNormal.instIsometricContinuousFunctionalCalculus
  have haN : IsSelfAdjoint (a : N) := Subtype.ext ha.star_eq
  have hc : cfc f a.val ∈ N := cfc_mem (𝕜' := ℂ) f a.property
  have hsub := N.subtype.map_cfc f (a : N) hf.continuousOn
    continuous_subtype_val haN.isStarNormal ha.isStarNormal
  have hcont : Continuous π := map_continuous π
  have he : cfc f (a : N) = (⟨cfc f a.val,hc⟩ : N) := Subtype.ext hsub
  have hh := π.map_cfc f (a : N) hf.continuousOn hcont
    haN.isStarNormal (haN.map π).isStarNormal
  rw [he] at hh
  refine ⟨hc,hh,?_⟩
  intro T hT
  have hi := complex_cfc_selfadjoint_intertwines (π a) (π a) T
    (haN.map π) (haN.map π) hT.symm.eq f hf
  rw [← hh] at hi
  exact hi.symm

set_option maxHeartbeats 6000000 in
private theorem scalar_resolvent_commutes_represented_regular (P : SiteProfile) :
    Commute (scalarTomitaResolvent P)
      (scalarGNSRepresentation P ⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩) := by
  letI : NormedSpace ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := inferInstance
  letI : Module ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := ContinuousLinearMap.module
  letI : ContinuousFunctionalCalculus ℂ
      (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) IsStarNormal :=
    IsStarNormal.instContinuousFunctionalCalculus
      (A := ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
  letI : IsometricContinuousFunctionalCalculus ℂ
      (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) IsStarNormal :=
    IsStarNormal.instIsometricContinuousFunctionalCalculus
      (A := ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
  letI : SMulCommClass ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
      (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := ⟨by
    intro c a b
    ext1 x
    change c • a (b x) = a (c • b x)
    exact (a.map_smul c (b x)).symm⟩
  letI : IsScalarTower ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
      (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := ⟨by
    intro c a b
    ext1 x
    rfl⟩
  let T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P := scalarTomitaResolvent P
  let J := scalarTomitaPolarFactor P
  let N := (regularCoreAlgebra P).toStarSubalgebra
  let π : N →⋆ₐ[ℂ] (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := scalarGNSRepresentation P
  haveI : IsClosed (N : Set (RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))) := by
    change IsClosed (regularCoreAlgebra P : Set (RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)))
    rw [← VonNeumannAlgebra.centralizer_centralizer (regularCoreAlgebra P)]
    exact Set.isClosed_centralizer _
  have hflip : antiunitaryConjugate J T = 1-T := by
    ext1 x
    change J (T (J.symm x)) = x - T x
    rw [scalarTomitaPolarFactor_resolvent, LinearIsometryEquiv.apply_symm_apply]
  have hleft (t : ℝ) : Commute T (π (regularRightCoreElement P t)) := by
    have hh := (scalarTomitaResolvent_regular_right_commutes P (-t)).map
      (antiunitaryConjugateRealHom J)
    change Commute (antiunitaryConjugate J T) (antiunitaryConjugate J (regularRightGNS P (-t))) at hh
    rw [hflip, scalarTomitaPolar_conjugate_regular_right, regularRightCoreElement_star, neg_neg] at hh
    have hc := (Commute.one_left (π (regularRightCoreElement P t))).sub_left hh
    simpa only [sub_sub_cancel] using hc
  have hwin (m : ℝ) : Commute T (π (regularSineWindowCore P m)) := by
    change Commute T (π ((1/2 : ℂ) • 1 + (1/(4*Complex.I) : ℂ) •
      (regularRightCoreElement P (-1/m) - regularRightCoreElement P (1/m))))
    simp only [map_add, map_smul, map_sub, map_one]
    exact ((Commute.one_right T).smul_right (1/2 : ℂ)).add_right
      (((hleft (-1/m)).sub_right (hleft (1/m))).smul_right (1/(4*Complex.I) : ℂ))
  let b (n : ℕ) : N :=
    ⟨regularSineResolvent P ((n : ℝ)+1),(regularSineResolvent_right P ((n : ℝ)+1)).choose⟩
  have hb (n : ℕ) : Commute T (π (b n)) := by
    let m : ℝ := (n : ℝ)+1
    let w : N := regularSineWindowCore P m
    let f : ℂ → ℂ := fun z => (Real.sigmoid (m*(2*z.re-1)) : ℂ)
    have hf : Continuous f := by fun_prop
    have hw : IsSelfAdjoint w.val := by
      change IsSelfAdjoint (regularSineWindowCore P m).val
      rw [regularSineWindowCore_spectral]
      exact (IsSelfAdjoint.of_nonneg (realScalarMultiplier_nonneg (H := TowerHilbert P) _ _ _ _)).map _
    have hex : ∃ hm : cfc f w.val ∈ N,
        π ⟨cfc f w.val,hm⟩ = cfc (p := IsStarNormal) f (π w) ∧
        ∀ V : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P,
          Commute V (π w) → Commute V (π ⟨cfc f w.val,hm⟩) := by
      exact closed_representation_cfc
        (H := RegularHilbert (TowerHilbert P)) (K := ScalarGNSHilbert P) N π w hw f hf
    obtain ⟨hm, _, hc⟩ := hex
    have hbn : (⟨cfc f w.val,hm⟩ : N) = b n :=
      Subtype.ext (regularSineResolvent_cfc P m).symm
    specialize hc T (hwin m)
    rw [hbn] at hc
    exact hc
  let r : N := ⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩
  have hlim (x : ScalarGNSHilbert P) : Tendsto (fun n => π (b n) x) atTop (𝓝 (π r x)) :=
    scalarGNSRepresentation_tendsto_of_uniformly_bounded P b r 1
      (fun n => regularSineResolvent_norm_le P ((n : ℝ)+1))
      (regularSineResolvent_tendsto P) x
  apply ContinuousLinearMap.ext
  intro x
  have h1 := T.continuous.continuousAt.tendsto.comp (hlim x)
  have h2 := hlim (T x)
  have heq : (fun n => T (π (b n) x)) = (fun n => π (b n) (T x)) := by
    funext n
    exact congrArg (fun W : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => W x) (hb n).eq
  change Tendsto (fun n => T (π (b n) x)) atTop (𝓝 (T (π r x))) at h1
  rw [heq] at h1
  exact tendsto_nhds_unique h1 h2

set_option maxHeartbeats 4000000 in
private theorem scalar_represented_regular_damped_phase (P : SiteProfile) (t : ℝ) :
    scalarGNSRepresentation P (regularRightCoreElement P t) *
        resolventDampingOperator
          (scalarGNSRepresentation P ⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩) =
      resolventPhaseOperator
        (scalarGNSRepresentation P ⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩) t := by
  letI : NormedSpace ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := inferInstance
  letI : Module ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := ContinuousLinearMap.module
  letI : ContinuousFunctionalCalculus ℂ
      (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) IsStarNormal :=
    IsStarNormal.instContinuousFunctionalCalculus
      (A := ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
  let N := (regularCoreAlgebra P).toStarSubalgebra
  let π : N →⋆ₐ[ℂ] (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := scalarGNSRepresentation P
  let r : N := ⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩
  let f : ℂ → ℂ := fun z => resolventPhaseFunction t z.re
  have hf : Continuous f := (resolventPhaseFunction_continuous t).comp Complex.continuous_re
  haveI : IsClosed (N : Set (RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))) := by
    change IsClosed (regularCoreAlgebra P : Set (RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)))
    rw [← VonNeumannAlgebra.centralizer_centralizer (regularCoreAlgebra P)]
    exact Set.isClosed_centralizer _
  have hr : IsSelfAdjoint r.val := IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg P)
  have hex : ∃ hm : cfc f r.val ∈ N,
      π ⟨cfc f r.val,hm⟩ = cfc (p := IsStarNormal) f (π r) ∧
      ∀ V : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P,
        Commute V (π r) → Commute V (π ⟨cfc f r.val,hm⟩) :=
    closed_representation_cfc
      (H := RegularHilbert (TowerHilbert P)) (K := ScalarGNSHilbert P) N π r hr f hf
  obtain ⟨hm, hmap, _⟩ := hex
  have he : regularRightCoreElement P t * (r*(1-r)) = (⟨cfc f r.val,hm⟩ : N) := by
    apply Subtype.ext
    ext1 x
    change regularUnitary P t (resolventDampingOperator (regularSpectralResolvent P) x) =
      resolventPhaseOperator (regularSpectralResolvent P) t x
    rw [← regularPositiveGenerator_imaginaryPower P t]
    exact resolventImaginaryPower_damping _ _ _ _ _ t x
  have hπ := congrArg (fun a : N => π a) he
  simp only [map_mul, map_sub, map_one] at hπ
  change π (regularRightCoreElement P t) * (π r * (1-π r)) = _
  exact hπ.trans hmap

#print axioms scalar_represented_regular_damped_phase
#print axioms damped_phase_scalar_balance
#print axioms damped_phase_commutative_balance
#print axioms damped_phase_operator_balance
#print axioms scalar_representation_vector_injective
#print axioms closed_representation_cfc
#print axioms scalar_resolvent_commutes_represented_regular
end
end TGLV350.Regular
