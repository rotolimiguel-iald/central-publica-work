import TGLExt.F1Fecho394.SchwartzCutoffDerivativeR4

/-! Quantitative compact-cutoff approximation in every Schwartz seminorm.
The rate is obtained from one extra spatial weight of the given test. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open Filter SchwartzMap
open scoped Topology ContDiff
namespace F1Fecho.SchwartzCutoff
variable {F:Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]

def cutoff (s:ℝ) (f:SchwartzMap E F) : SchwartzMap E F :=
  SchwartzMap.smulLeftCLM F (fun x:E=>bump (s • x)) f

theorem scaled_temperate (s:ℝ) : (fun x:E=>bump (s • x)).HasTemperateGrowth := by
  have hb:Function.HasTemperateGrowth (fun x:E=>bump x) := bumpSchwartz.hasTemperateGrowth
  fun_prop

theorem cutoff_apply (s:ℝ) (f:SchwartzMap E F) (x:E) :
    cutoff s f x=bump (s • x) • f x :=
  SchwartzMap.smulLeftCLM_apply_apply (scaled_temperate s) f x

theorem error_apply (s:ℝ) (f:SchwartzMap E F) :
    ((f-cutoff s f:SchwartzMap E F):E→F)=(fun x=>residual s x • f x) := by
  funext x
  change f x-cutoff s f x=residual s x • f x
  simp only [cutoff_apply,residual,sub_smul,one_smul]

def errorBound (k n:ℕ) (f:SchwartzMap E F) : ℝ :=
  ∑i∈Finset.range (n+1),(n.choose i:ℝ)*bound i*SchwartzMap.seminorm ℝ (k+1) (n-i) f

theorem bound_nonneg (i:ℕ) : 0≤bound i := by unfold bound;positivity

theorem errorBound_nonneg (k n:ℕ) (f:SchwartzMap E F) : 0≤errorBound k n f := by
  apply Finset.sum_nonneg
  intro i hi
  exact mul_nonneg (mul_nonneg (Nat.cast_nonneg _) (bound_nonneg _)) (apply_nonneg _ _)

theorem weighted_tail_bound (s:ℝ) (hs:0≤s) (f:SchwartzMap E F) (k n:ℕ) (x:E)
    (hx:1≤s*‖x‖) :
    ‖x‖^k*‖iteratedFDeriv ℝ n f x‖≤s*SchwartzMap.seminorm ℝ (k+1) n f := by
  calc
    ‖x‖^k*‖iteratedFDeriv ℝ n f x‖≤
        (s*‖x‖)*(‖x‖^k*‖iteratedFDeriv ℝ n f x‖) :=
      le_mul_of_one_le_left (by positivity) hx
    _ = s*(‖x‖^(k+1)*‖iteratedFDeriv ℝ n f x‖) := by rw [pow_succ];ring
    _ ≤s*SchwartzMap.seminorm ℝ (k+1) n f :=
      mul_le_mul_of_nonneg_left (f.le_seminorm ℝ (k+1) n x) hs

theorem error_pointwise_bound (s:ℝ) (hs:0≤s) (hs1:s≤1)
    (f:SchwartzMap E F) (k n:ℕ) (x:E) :
    ‖x‖^k*‖iteratedFDeriv ℝ n (f-cutoff s f) x‖≤s*errorBound k n f := by
  rw [error_apply]
  by_cases hx:‖s • x‖<1
  · rw [residual_product_derivative_zero s f n x hx,norm_zero,mul_zero]
    exact mul_nonneg hs (errorBound_nonneg k n f)
  · have hx':1≤s*‖x‖ := by
      simpa only [norm_smul,Real.norm_of_nonneg hs] using le_of_not_gt hx
    have hprod:=norm_iteratedFDeriv_smul_le (residual_smooth s) (f.smooth ⊤) x (n:=n)
      (WithTop.coe_le_coe.mpr (show (n:ℕ∞)≤⊤ from le_top))
    apply (mul_le_mul_of_nonneg_left hprod (by positivity)).trans
    unfold errorBound
    rw [Finset.mul_sum,Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i hi
    have hb:=residual_derivative_bound s hs hs1 i x
    have htail:=weighted_tail_bound s hs f k (n-i) x hx'
    calc
      ‖x‖^k*((n.choose i:ℝ)*‖iteratedFDeriv ℝ i (residual s) x‖*
          ‖iteratedFDeriv ℝ (n-i) f x‖)≤
        (n.choose i:ℝ)*bound i*(‖x‖^k*‖iteratedFDeriv ℝ (n-i) f x‖) := by
          nlinarith [mul_le_mul_of_nonneg_left hb
            (show 0≤‖x‖^k*(n.choose i:ℝ)*‖iteratedFDeriv ℝ (n-i) f x‖ by positivity)]
      _ ≤ (n.choose i:ℝ)*bound i*(s*SchwartzMap.seminorm ℝ (k+1) (n-i) f) :=
        mul_le_mul_of_nonneg_left htail (mul_nonneg (Nat.cast_nonneg _) (bound_nonneg _))
      _ =s*((n.choose i:ℝ)*bound i*SchwartzMap.seminorm ℝ (k+1) (n-i) f) := by ring

theorem error_seminorm_bound (s:ℝ) (hs:0≤s) (hs1:s≤1)
    (f:SchwartzMap E F) (k n:ℕ) :
    SchwartzMap.seminorm ℝ k n (f-cutoff s f)≤s*errorBound k n f :=
  (f-cutoff s f).seminorm_le_bound ℝ k n
    (mul_nonneg hs (errorBound_nonneg k n f)) (error_pointwise_bound s hs hs1 f k n)

end F1Fecho.SchwartzCutoff
#print axioms F1Fecho.SchwartzCutoff.error_pointwise_bound
#print axioms F1Fecho.SchwartzCutoff.error_seminorm_bound
