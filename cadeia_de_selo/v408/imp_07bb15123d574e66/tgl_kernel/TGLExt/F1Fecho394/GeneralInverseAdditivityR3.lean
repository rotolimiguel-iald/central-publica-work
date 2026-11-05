import TGLExt.V350DualFormNormality
import TGLExt.F1Fecho394.GeneralInverseFiniteApproximationR1
/-! Comparison extends from the existing finite-square ideal by the actual
regular averages. Additivity of the inverse supremum consumes regulator
antitonicity explicitly; it is not inferred from an arbitrary supremum. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular Filter
open F1Fecho.RegularCovariantCore F1Fecho.RegularCoreAverage
open scoped ENNReal Topology
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:UnitaryFlow H) (M:VonNeumannAlgebra H) (zeta:RegularHilbert H)
variable (hzeta:∀t:ℝ,fibre (boostCLM B t) zeta=zeta)

include hzeta in
theorem perturbed_comparison_all_squares
    (b c:(RegularCovariantCore.core B M).toStarSubalgebra)
    (hbe:∀d:ℝ,Commute b.val (RegularCoreAverage.regularAverage B d))
    (hce:∀d:ℝ,Commute c.val (RegularCoreAverage.regularAverage B d))
    (hfinite:∀A:(RegularCovariantCore.core B M).toStarSubalgebra,
      HasFiniteDualSquare A.val →
      dualQuadraticIntegral (star b.val*(star A.val*A.val)*b.val) zeta ≤
        dualQuadraticIntegral (star c.val*(star A.val*A.val)*c.val) zeta)
    (A:(RegularCovariantCore.core B M).toStarSubalgebra) :
    dualQuadraticIntegral (star b.val*(star A.val*A.val)*b.val) zeta ≤
      dualQuadraticIntegral (star c.val*(star A.val*A.val)*c.val) zeta := by
  let d:ℕ→ℝ:=fun n=>1/((n:ℝ)+1)
  have hd(n:ℕ):0<d n:=by dsimp[d]; positivity
  obtain ⟨hf,hm,_⟩:=RegularCoreFiniteWeight.finiteDualLeftIdeal_strong_approximation B M A
  let An(n:ℕ):(RegularCovariantCore.core B M).toStarSubalgebra:=
    ⟨A.val*RegularCoreAverage.regularAverage B (d n),hm (d n)⟩
  have he(b':(RegularCovariantCore.core B M).toStarSubalgebra)
      (hb':∀d:ℝ,Commute b'.val (RegularCoreAverage.regularAverage B d)) (n:ℕ):
      (A.val*b'.val)*RegularCoreAverage.regularAverage B (d n)=
        (A.val*RegularCoreAverage.regularAverage B (d n))*b'.val:=by
    rw [mul_assoc,(hb' (d n)).eq,←mul_assoc]
  have hab:=dualSquare_eq_iSup_averages B M zeta hzeta (A*b)
  have hac:=dualSquare_eq_iSup_averages B M zeta hzeta (A*c)
  have hs:(⨆n:ℕ,dualQuadraticIntegral
      (star ((A.val*b.val)*RegularCoreAverage.regularAverage B (d n))*
        ((A.val*b.val)*RegularCoreAverage.regularAverage B (d n))) zeta)≤
      ⨆n:ℕ,dualQuadraticIntegral
      (star ((A.val*c.val)*RegularCoreAverage.regularAverage B (d n))*
        ((A.val*c.val)*RegularCoreAverage.regularAverage B (d n))) zeta:=by
    apply iSup_le
    intro n
    apply le_iSup_of_le n
    rw [he b hbe n,he c hce n]
    have hh:=hfinite (An n) (hf (d n) (hd n))
    simpa only [An,star_mul,mul_assoc] using hh
  change dualQuadraticIntegral (star (A.val*b.val)*(A.val*b.val)) zeta=
    (⨆n:ℕ,dualQuadraticIntegral
      (star ((A.val*b.val)*RegularCoreAverage.regularAverage B (d n))*
        ((A.val*b.val)*RegularCoreAverage.regularAverage B (d n))) zeta) at hab
  change dualQuadraticIntegral (star (A.val*c.val)*(A.val*c.val)) zeta=
    (⨆n:ℕ,dualQuadraticIntegral
      (star ((A.val*c.val)*RegularCoreAverage.regularAverage B (d n))*
        ((A.val*c.val)*RegularCoreAverage.regularAverage B (d n))) zeta) at hac
  rw [←hab,←hac] at hs
  simpa only [star_mul,mul_assoc] using hs

private theorem core_positive_square_source {E:Type} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] [CompleteSpace E]
    (N:VonNeumannAlgebra E) (X:N.toStarSubalgebra)
    (hX:0≤X.val) : ∃a:N.toStarSubalgebra, star a.val*a.val=X.val := by
  let r:=hilbertPositiveSqrt X.val
  have hr:r∈N:=sqrt_mem_core _ _ X.property hX
  refine ⟨⟨r,hr⟩,?_⟩
  change star (CFC.sqrt X.val)*CFC.sqrt X.val=X.val
  rw [(CFC.sqrt_nonneg X.val).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self X.val hX]

include hzeta in
theorem perturbed_comparison_all_positive
    (b c:(RegularCovariantCore.core B M).toStarSubalgebra)
    (hbe:∀d:ℝ,Commute b.val (RegularCoreAverage.regularAverage B d))
    (hce:∀d:ℝ,Commute c.val (RegularCoreAverage.regularAverage B d))
    (hfinite:∀A:(RegularCovariantCore.core B M).toStarSubalgebra,
      HasFiniteDualSquare A.val →
      dualQuadraticIntegral (star b.val*(star A.val*A.val)*b.val) zeta ≤
        dualQuadraticIntegral (star c.val*(star A.val*A.val)*c.val) zeta)
    (X:(RegularCovariantCore.core B M).toStarSubalgebra) (hX:0≤X.val):
    dualQuadraticIntegral (star b.val*X.val*b.val) zeta ≤
      dualQuadraticIntegral (star c.val*X.val*c.val) zeta := by
  obtain ⟨a,ha⟩:=core_positive_square_source (RegularCovariantCore.core B M) X hX
  have hh:=perturbed_comparison_all_squares B M zeta hzeta b c hbe hce hfinite a
  simpa only [ha] using hh

theorem inverseSupremum_add_of_antitone
    (X Y:RegularHilbert H→L[ℂ]RegularHilbert H) (hX:0≤X) (hY:0≤Y)
    (hx:∀e d:PositiveRegulator,e.val≤d.val→cutoffWeight B zeta d.val X≤cutoffWeight B zeta e.val X)
    (hy:∀e d:PositiveRegulator,e.val≤d.val→cutoffWeight B zeta d.val Y≤cutoffWeight B zeta e.val Y):
    inverseSupremum B zeta (X+Y)=inverseSupremum B zeta X+inverseSupremum B zeta Y := by
  unfold inverseSupremum
  simp only [cutoffWeight_add B zeta _ X Y hX hY]
  symm
  apply ENNReal.iSup_add_iSup
  intro e d
  let m:PositiveRegulator:=⟨min e.val d.val,lt_min e.property d.property⟩
  exact ⟨m,add_le_add (hx m e (min_le_left _ _)) (hy m d (min_le_right _ _))⟩

theorem cutoff_sequence_mono_of_antitone
    (X:RegularHilbert H→L[ℂ]RegularHilbert H)
    (hx:∀e d:PositiveRegulator,e.val≤d.val→cutoffWeight B zeta d.val X≤cutoffWeight B zeta e.val X):
    Monotone (fun n:ℕ=>cutoffWeight B zeta (1/((n:ℝ)+1)) X) := by
  intro n m hnm
  apply hx ⟨1/((m:ℝ)+1),by positivity⟩ ⟨1/((n:ℝ)+1),by positivity⟩
  apply one_div_le_one_div_of_le (by positivity : 0<(n:ℝ)+1)
  exact_mod_cast (Nat.add_le_add_right hnm 1)
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.perturbed_comparison_all_squares
#print axioms F1Fecho.RegularInverseWeight.perturbed_comparison_all_positive
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_add_of_antitone
#print axioms F1Fecho.RegularInverseWeight.cutoff_sequence_mono_of_antitone

-- Appended order-normality consumer; prepared source preserved separately.
/-! Order normality of the same inverse supremum, including internal suprema
in the represented von Neumann algebra. Strong convergence is constructed
from monotone bounded operators rather than supplied as an extra premise. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular Filter
open scoped Topology ENNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:RegularCovariantCore.UnitaryFlow H) (zeta:RegularHilbert H)
variable {ι:Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]

theorem inverseSupremum_preserves_positive_isLUB
    (A:ι→RegularHilbert H→L[ℂ]RegularHilbert H)
    (S:RegularHilbert H→L[ℂ]RegularHilbert H)
    (hpos:∀i,0≤A i) (hmono:Monotone A) (hS:IsLUB (Set.range A) S) :
    inverseSupremum B zeta S=⨆i,inverseSupremum B zeta (A i) := by
  have hbound:∀i,‖A i‖≤‖S‖:=fun i=>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hS.1 (Set.mem_range_self i))
  obtain ⟨L,_,_,hlim,hL⟩:=ChatgptAudit.Expectation047.monotone_operator_limit
    A hpos hmono ‖S‖ (norm_nonneg S) hbound
  have hLS:L=S:=hL.unique hS
  subst L
  exact inverseSupremum_normal B zeta A S hpos hmono hlim

theorem inverseSupremum_preserves_internal_isLUB
    (N:VonNeumannAlgebra (RegularHilbert H))
    (A:ι→N.toStarSubalgebra) (S:N.toStarSubalgebra)
    (hpos:∀i,0≤A i) (hmono:Monotone A) (hS:IsLUB (Set.range A) S) :
    inverseSupremum B zeta S.val=⨆i,inverseSupremum B zeta (A i).val :=
  inverseSupremum_preserves_positive_isLUB B zeta
    (fun i=>(A i).val) S.val hpos hmono (vonNeumann_isLUB_coe N A S hpos hmono hS)

end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_preserves_positive_isLUB
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_preserves_internal_isLUB
