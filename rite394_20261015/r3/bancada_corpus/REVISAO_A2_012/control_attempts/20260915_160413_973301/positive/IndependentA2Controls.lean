import TGLExt.V354TraceReaderWall

set_option autoImplicit false

namespace IndependentA2
open TGLExt TGLV350.Regular TGLV351 TGL.ContinuousCorner
noncomputable section

theorem trace_positive (P : SiteProfile) :
    scalarInverseLimitWeight P (regularFiniteSupport P) = 1 := regularFiniteSupport_trace P

theorem trace_not_zero (P : SiteProfile) :
    scalarInverseLimitWeight P (regularFiniteSupport P) ≠ 0 := by
  rw [regularFiniteSupport_trace]
  exact one_ne_zero

theorem trace_not_two (P : SiteProfile) :
    scalarInverseLimitWeight P (regularFiniteSupport P) ≠ 2 := by
  rw [regularFiniteSupport_trace]
  norm_num

theorem support_nonzero (P : SiteProfile) :
    (regularFiniteSupport P).val ≠ 0 := regularFiniteSupport_ne_zero P

theorem spectral_positive (P : SiteProfile) :
    (regularMinimalLock P).ker.starProjection = (regularFiniteSupport P).val :=
  regularMinimalLock_spectral_zero P

theorem spectral_not_zero (P : SiteProfile) :
    (regularMinimalLock P).ker.starProjection ≠ 0 := by
  rw [regularMinimalLock_spectral_zero]
  exact regularFiniteSupport_ne_zero P

theorem plus_half (P : SiteProfile) :
    (regularContinuousCorner P).normalizedTrace (regularContinuousCorner P).Pplus = 1/2 :=
  (regularContinuousCorner_readings P).2.1

theorem plus_not_one (P : SiteProfile) :
    (regularContinuousCorner P).normalizedTrace (regularContinuousCorner P).Pplus ≠ 1 := by
  rw [plus_half]
  norm_num

theorem reader_support (P : SiteProfile) :
    positiveTraceReader P ⟨(regularFiniteSupport P).val,(regularFiniteSupport P).property.1⟩ = 1 := by
  rw [positiveTraceReader_positive,regularFiniteSupport_trace]

theorem reader_agrees_on_cone (P : SiteProfile) (X : PositiveCoreInput P) :
    positiveTraceReader P ⟨X.val,X.property.1⟩ = scalarInverseLimitWeight P X :=
  positiveTraceReader_positive P X

theorem reader_outside_cone (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra) (ha : ¬ 0 ≤ a.val) :
    positiveTraceReader P a = 0 := by
  simp only [positiveTraceReader,dif_neg ha]

theorem reader_not_global_cyclic (P : SiteProfile) :
    ¬ ∀ a b : (regularCoreAlgebra P).toStarSubalgebra,
      positiveTraceReader P (a*b) = positiveTraceReader P (b*a) :=
  positiveTraceReader_not_cyclic P

theorem actual_equal_split (P : SiteProfile) :
    scalarInverseLimitWeight P (regularNormalizedFaces P).val.1 =
      scalarInverseLimitWeight P (regularNormalizedFaces P).val.2 :=
  (regularNormalizedFaces P).property.2.2.2.2

theorem reverse_orthogonality (P : SiteProfile) :
    (regularNormalizedFaces P).val.2.val * (regularNormalizedFaces P).val.1.val = 0 := by
  have h := congrArg star (regularNormalizedFaces P).property.2.2.1
  simpa only [star_mul,star_zero,
    (regularNormalizedFaces P).property.1.isSelfAdjoint.star_eq,
    (regularNormalizedFaces P).property.2.1.isSelfAdjoint.star_eq] using h

theorem support_trace_positive_finite (P : SiteProfile) :
    0 < scalarInverseLimitWeight P (regularFiniteSupport P) ∧
      scalarInverseLimitWeight P (regularFiniteSupport P) < ⊤ := by
  rw [regularFiniteSupport_trace]
  exact ⟨zero_lt_one,ENNReal.one_lt_top⟩

/-- Bare orthogonal projections, even with a cyclic weight, do not force equal
readings. This commutative finite algebra is a control, not the regular core. -/
def leftFace : ℝ × ℝ := (1,0)
def rightFace : ℝ × ℝ := (0,1)
def unequalWeight (a : ℝ × ℝ) : ℝ := a.1 + 2*a.2

theorem unequal_weight_cyclic (a b : ℝ × ℝ) :
    unequalWeight (a*b) = unequalWeight (b*a) := by
  simp only [unequalWeight,Prod.fst_mul,Prod.snd_mul]
  ring

theorem orthogonality_does_not_force_equal_trace :
    leftFace*leftFace=leftFace ∧ rightFace*rightFace=rightFace ∧
    star leftFace=leftFace ∧ star rightFace=rightFace ∧
    leftFace*rightFace=0 ∧ leftFace+rightFace=1 ∧
    unequalWeight leftFace ≠ unequalWeight rightFace := by
  norm_num [leftFace,rightFace,unequalWeight,Prod.ext_iff]

theorem zero_positive_has_no_positive_finite_minorant (P : SiteProfile) :
    ¬ ∃ Y : PositiveCoreInput P, Y ≤ PositiveCoreInput.zero P ∧
      0 < scalarInverseLimitWeight P Y ∧ scalarInverseLimitWeight P Y < ⊤ := by
  rintro ⟨Y,hy,hpos,_⟩
  have hz : Y = PositiveCoreInput.zero P := Subtype.ext (le_antisymm hy Y.property.2)
  rw [hz,scalarInverseLimitWeight_zero] at hpos
  exact lt_irrefl _ hpos

/-- Relative gap cannot be upgraded to a lower bound on every vector, because
the constructed nonzero support supplies a nonzero vector in the kernel. -/
theorem nonzero_kernel_vector (P : SiteProfile) :
    ∃ x : RegularHilbert (TowerHilbert P), x ≠ 0 ∧ regularMinimalLock P x = 0 := by
  have hp := regularFiniteSupport_ne_zero P
  have hex : ∃ y, (regularFiniteSupport P).val y ≠ 0 := by
    by_contra h
    push Not at h
    apply hp
    exact ContinuousLinearMap.ext h
  obtain ⟨y,hy⟩ := hex
  refine ⟨(regularFiniteSupport P).val y,hy,?_⟩
  have hk : (regularFiniteSupport P).val y ∈ (regularMinimalLock P).ker := by
    rw [regularMinimalLock_ker]
    exact ⟨y,rfl⟩
  exact hk

theorem gap_not_global (P : SiteProfile) :
    ¬ ∀ x : RegularHilbert (TowerHilbert P), ‖regularMinimalLock P x‖ = ‖x‖ := by
  obtain ⟨x,hx,hzero⟩ := nonzero_kernel_vector P
  intro h
  have hn := h x
  rw [hzero,norm_zero] at hn
  exact hx (norm_eq_zero.mp hn.symm)

theorem relative_gap_positive (P : SiteProfile)
    (x : RegularHilbert (TowerHilbert P)) (hx : x ∈ (regularMinimalLock P).kerᗮ) :
    ‖regularMinimalLock P x‖ = ‖x‖ := regularMinimalLock_relative_gap P x hx

theorem actual_graph_affiliation (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hB : B ∈ (regularCoreAlgebra P).commutant)
    (x y : RegularHilbert (TowerHilbert P))
    (hxy : (x,y) ∈ (regularMinimalLockGraph P).graph) :
    (B x,B y) ∈ (regularMinimalLockGraph P).graph :=
  regularMinimalLockGraph_affiliated P B hB x y hxy

end
end IndependentA2
