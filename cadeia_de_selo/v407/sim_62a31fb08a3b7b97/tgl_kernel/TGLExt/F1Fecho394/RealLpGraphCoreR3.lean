import TGLExt.F1Fecho394.LpIntervalTotalityR3

/-! Real Hilbert-valued interval totality, for the real graph Hilbert space
of an antilinear Tomita operator. The total family is named explicitly;
its actual Weyl-graph consumer must supply totality by closure. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory
namespace F1Fecho.RealLpGraphCore
variable {E:Type} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

def intervalVector (a b:ℝ) (v:E) : Lp E 2 (volume:Measure ℝ) :=
  indicatorConstLp (s:=Set.Ioc a b) 2 measurableSet_Ioc (by simp [Real.volume_Ioc]) v

theorem interval_inner (a b:ℝ) (v:E) (f:Lp E 2 (volume:Measure ℝ)) :
    inner ℝ (intervalVector a b v) f=inner ℝ v (∫ t in Set.Ioc a b,f t) :=
  L2.inner_indicatorConstLp_eq_inner_setIntegral (s:=Set.Ioc a b) ℝ measurableSet_Ioc
    (by simp [Real.volume_Ioc]) v f

theorem closed_submodule_eq_top
    (S:Submodule ℝ (Lp E 2 (volume:Measure ℝ)))
    (hs:IsClosed (S:Set (Lp E 2 (volume:Measure ℝ))))
    (hi:∀ a b v,intervalVector a b v∈S) : S=⊤ := by
  letI : CompleteSpace S := hs.completeSpace_coe
  apply Submodule.orthogonal_eq_bot_iff.mp
  apply le_antisymm ?_ bot_le
  intro f hf
  change f=0
  apply LpIntervalTotality.vector_eq_zero_of_intervals f
  have hz (a b:ℝ) : (∫ t in Set.Ioc a b,f t)=0 := by
    apply (inner_self_eq_zero (𝕜:=ℝ)).mp
    rw [←interval_inner]
    exact Submodule.inner_right_of_mem_orthogonal (hi a b _) hf
  intro a b
  simp only [intervalIntegral,hz,sub_self]

theorem intervalVector_continuous (a b:ℝ) : Continuous (intervalVector (E:=E) a b) := by
  let c : NNReal := ⟨volume.real (Set.Ioc a b) ^ (1/(2 : ENNReal).toReal),by positivity⟩
  have h:LipschitzWith c (intervalVector (E:=E) a b) := by
    apply LipschitzWith.of_dist_le_mul
    intro x y
    rw [dist_eq_norm,dist_eq_norm]
    change ‖indicatorConstLp 2 measurableSet_Ioc (by simp [Real.volume_Ioc]) x -
      indicatorConstLp 2 measurableSet_Ioc (by simp [Real.volume_Ioc]) y‖ ≤ _
    rw [indicatorConstLp_sub,norm_indicatorConstLp (by norm_num) (by norm_num)]
    exact le_of_eq (mul_comm _ _)
  exact h.continuous

theorem interval_family_total (D:Set E) (hD:Dense D)
    (S:Submodule ℝ (Lp E 2 (volume:Measure ℝ)))
    (hs:IsClosed (S:Set (Lp E 2 (volume:Measure ℝ))))
    (hi:∀ a b v,v∈D→intervalVector a b v∈S) : S=⊤ := by
  apply closed_submodule_eq_top S hs
  intro a b v
  have hc:IsClosed {v:E|intervalVector a b v∈S}:=hs.preimage (intervalVector_continuous a b)
  apply hD.induction (P:=fun v=>intervalVector a b v∈S) (fun v hv=>hi a b v hv) hc v

end F1Fecho.RealLpGraphCore
#print axioms F1Fecho.RealLpGraphCore.interval_inner
#print axioms F1Fecho.RealLpGraphCore.closed_submodule_eq_top
#print axioms F1Fecho.RealLpGraphCore.intervalVector_continuous
#print axioms F1Fecho.RealLpGraphCore.interval_family_total
