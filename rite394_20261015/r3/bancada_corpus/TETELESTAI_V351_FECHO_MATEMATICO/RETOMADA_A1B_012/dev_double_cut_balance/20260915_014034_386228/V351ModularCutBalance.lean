import TGLExt.V351ModularImplementation
import TGLExt.PhaseFrequencySeparation
import Mathlib.Analysis.CStarAlgebra.GelfandDuality

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open ChatgptAudit
open scoped ComplexOrder
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
  letI : PartialOrder S := CStarAlgebra.spectralOrder S
  letI : StarOrderedRing S := CStarAlgebra.spectralOrderedRing S
  have hmem (X : H →L[ℂ] H) (hx : X ∈ ({T,A,B} : Set (H →L[ℂ] H))) : X ∈ S :=
    StarSubalgebra.le_topologicalClosure U (StarAlgebra.subset_adjoin hx)
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
      rw [(IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg X.val)).star_eq, CFC.sqrt_mul_self X.val hX]
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
      apply S.subtype.injective
      simp only [map_mul, map_sub, map_one, hcfc]
      exact hphase t)
  have he : ((T*(1-T))*(A*(1-A))*(B*(1-B))) * ((1-T)*A*(1-B)-T*(1-A)*B) = 0 := by
    have hh := congrArg S.subtype hs
    simpa only [map_mul, map_sub, map_one, map_zero] using hh
  apply sub_eq_zero.mp
  ext1 x
  apply (resolventDampingOperator_injective T hiT hjT).comp
    ((resolventDampingOperator_injective A hiA hjA).comp
      (resolventDampingOperator_injective B hiB hjB))
  have hh := congrArg (fun W : H →L[ℂ] H => W x) he
  simpa only [map_zero] using hh

#print axioms damped_phase_scalar_balance
#print axioms damped_phase_commutative_balance
#print axioms damped_phase_operator_balance
end
end TGLV350.Regular
