import TGLExt.F1Fecho394.GeneralDampedPhaseBalanceR1
import TGLExt.V351ModularCutBalance
/-! Generic auxiliary steps from v393: CFC transport through a closed representation and cancellation of the two existing regular cuts. The phase balance and domain equations remain explicit inputs. -/
set_option autoImplicit false
set_option maxHeartbeats 2400000
noncomputable section
namespace F1Fecho.ModularCutBalance
open TGLV350.Regular TGLExt
open scoped CStarAlgebra in
theorem closed_representation_cfc {H K : Type} [NormedAddCommGroup H]
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

theorem cut_balance_after_multiplication {R : Type*} [Ring R]
    (T A B C D p q : R)
    (hbase : (1-T)*A*(1-B) = T*(1-A)*B)
    (hTA : Commute T A) (hTB : Commute T B)
    (hBC : Commute B C) (hBp : Commute B p)
    (hAp : A*p = (1-A)*C) (hBq : B*q = (1-B)*D) :
    (A*B)*((1-T)*C*q) = (A*B)*(T*p*D) := by
  have hT : Commute T (A*B) := hTA.mul_right hTB
  have h1 : Commute (1-T) (A*B) := (Commute.one_left (A*B)).sub_left hT
  have hC : Commute C (1-B) := (Commute.one_right C).sub_right hBC.symm
  calc
    (A*B)*((1-T)*C*q) = (1-T)*((A*B)*(C*q)) := by
      rw [mul_assoc (1-T) C q]
      exact h1.symm.left_comm (C*q)
    _ = (1-T)*(A*(C*(B*q))) := by
      rw [mul_assoc A B (C*q), hBC.left_comm q]
    _ = (1-T)*(A*(C*((1-B)*D))) := by rw [hBq]
    _ = ((1-T)*A*(1-B))*(C*D) := by
      rw [hC.left_comm D]
      simp only [mul_assoc]
    _ = (T*(1-A)*B)*(C*D) := by rw [hbase]
    _ = T*((1-A)*(C*(B*D))) := by
      simp only [mul_assoc]
      rw [hBC.left_comm D]
    _ = T*((A*p)*(B*D)) := by
      rw [← mul_assoc (1-A) C (B*D), ← hAp]
    _ = T*(A*(B*(p*D))) := by
      rw [mul_assoc A p (B*D), hBp.symm.left_comm D]
    _ = (A*B)*(T*p*D) := by
      rw [← mul_assoc A B (p*D), mul_assoc T p D]
      exact hT.left_comm (p*D)


end F1Fecho.ModularCutBalance
#print axioms F1Fecho.ModularCutBalance.closed_representation_cfc
#print axioms F1Fecho.ModularCutBalance.cut_balance_after_multiplication
