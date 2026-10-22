import TGLV350.DualFormRepresentation
import TGLV350.ResolventGraphTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem selfAdjoint_inner_im_zero (Y : H →L[ℂ] H) (hY : star Y=Y) (v : H) :
    (inner ℂ (Y v) v).im=0 := by
  have hp : inner ℂ (Y v) v=inner ℂ v (Y v) := by
    have hYa : Y.adjoint=Y := hY
    simpa only [hYa] using Y.adjoint_inner_left v v
  have hh := congrArg Complex.im ((inner_conj_symm (𝕜:=ℂ) v (Y v)).trans hp.symm)
  change -(inner ℂ (Y v) v).im=(inner ℂ (Y v) v).im at hh
  linarith

theorem realPhaseEnergyIdentity (z a b w : ℂ) (hz : z.re=1)
    (ha : a.im=0) (hb : b.im=0) (he : 2*w=z*a+star z*b) :
    2*w.re=a.re+b.re := by
  have hza : (z*a).re=a.re := by rw [Complex.mul_re,hz,ha,mul_zero,sub_zero,one_mul]
  have hzb : (star z*b).re=b.re := by
    have hz' : (star z).re=1 := by simpa using hz
    rw [Complex.mul_re,hz',hb,mul_zero,sub_zero,one_mul]
  have hl : (2*w).re=2*w.re := by simp [Complex.mul_re]
  have hh := congrArg Complex.re he
  rw [hl,Complex.add_re,hza,hzb] at hh
  exact hh

theorem variationalPair_energy_bound (Y Z L : H →L[ℂ] H) (x η : H) (z : ℂ)
    (hz : z.re=1) (hY : star Y=Y) (hZ : Z=star L*L)
    (he : 2*inner ℂ x (Z η)=z*inner ℂ η (Z η)+star z*inner ℂ (Y η) η) :
    (inner ℂ (Y η) η).re ≤ ‖L x‖^2 := by
  have hp (u v : H) : inner ℂ u (Z v)=inner ℂ (L u) (L v) := by
    rw [hZ]
    exact L.adjoint_inner_right u (L v)
  have him : (inner ℂ η (Z η)).im=0 := by rw [hp]; exact inner_self_im (𝕜:=ℂ) (L η)
  have hh := realPhaseEnergyIdentity z (inner ℂ η (Z η)) (inner ℂ (Y η) η)
    (inner ℂ x (Z η)) hz him (selfAdjoint_inner_im_zero Y hY η) he
  have hnself : (inner ℂ (L η) (L η)).re=‖L η‖^2 := inner_self_eq_norm_sq (𝕜:=ℂ) _
  rw [hp,hp,hnself] at hh
  have hn : ‖L x-L η‖^2=‖L x‖^2-2*(inner ℂ (L x) (L η)).re+‖L η‖^2 :=
    norm_sub_sq (𝕜:=ℂ) (L x) (L η)
  nlinarith only [hh,hn,sq_nonneg ‖L x-L η‖]

theorem weightedBlock_Y_selfAdjoint (A B e : H →L[ℂ] H)
    (he : star e=e) (hBB : B*star B=A*(1-A)) (heA : Commute e A) :
    star (e*B*star B)=e*B*star B := by
  have hprod : Commute e (A*(1-A)) :=
    heA.mul_right (complement_commutes_of_commute A e heA.symm).symm
  calc
    star (e*B*star B) = (B*star B)*e := by rw [star_mul,star_mul,star_star,he,mul_assoc]
    _ = (A*(1-A))*e := by rw [hBB]
    _ = e*(A*(1-A)) := hprod.eq.symm
    _ = e*B*star B := by rw [← hBB,mul_assoc]

theorem weightedBlock_root_sandwich (B e : H →L[ℂ] H) (he : 0 ≤ e) :
    star (CFC.sqrt e*B)*(CFC.sqrt e*B)=star B*e*B := by
  have hs : star (CFC.sqrt e : H →L[ℂ] H)=CFC.sqrt e :=
    (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg e)).star_eq
  rw [star_mul,hs]
  calc
    (star B*CFC.sqrt e)*(CFC.sqrt e*B) = star B*(CFC.sqrt e*CFC.sqrt e)*B := by simp only [mul_assoc]
    _ = star B*e*B := by rw [CFC.sqrt_mul_sqrt_self e he]

theorem weightedBlock_phase_energy_bound (A B e : H →L[ℂ] H) (x η : H) (z : ℂ)
    (hz : z.re=1) (hA : star A=A) (he : 0 ≤ e)
    (hBB : B*star B=A*(1-A)) (heA : Commute e A)
    (hv : 2*inner ℂ x ((star B*e*B) η)=
      z*inner ℂ η ((star B*e*B) η)+star z*inner ℂ ((e*B*star B) η) η) :
    (inner ℂ ((e*B*star B) η) η).re ≤ ‖(CFC.sqrt e*B) x‖^2 :=
  variationalPair_energy_bound _ _ _ x η z hz
    (weightedBlock_Y_selfAdjoint A B e (IsSelfAdjoint.of_nonneg he).star_eq hBB heA)
    (weightedBlock_root_sandwich B e he).symm hv

theorem weightedBlock_multiplier_energy_bound (A B e T : H →L[ℂ] H) (x η : H) (z : ℂ)
    (hz : z.re=1) (hA : star A=A) (he : 0 ≤ e)
    (hBB : B*star B=A*(1-A)) (heA : Commute e A)
    (heT : Commute e T) (hAT : Commute A T) (hx : B x=A (T η))
    (hv : 2*inner ℂ x ((star B*e*B) η)=
      z*inner ℂ η ((star B*e*B) η)+star z*inner ℂ ((e*B*star B) η) η) :
    (inner ℂ ((e*B*star B) η) η).re ≤ ‖T‖^2*(inner ℂ ((e*A*A) η) η).re := by
  have hact : (CFC.sqrt e*B) x=T ((CFC.sqrt e*A) η) := by
    change CFC.sqrt e (B x)=T (CFC.sqrt e (A η))
    rw [hx]
    exact (congrArg (fun v : H => (CFC.sqrt e : H →L[ℂ] H) v) (congrArg (fun U : H →L[ℂ] H => U η) hAT.eq)).trans
      (congrArg (fun U : H →L[ℂ] H => U (A η)) (positive_sqrt_commutes_of_commute e T heT).eq)
  have hroot : star (CFC.sqrt e*A)*(CFC.sqrt e*A)=e*A*A := by
    rw [weightedBlock_root_sandwich A e he,hA,heA.eq.symm]
  have henergy : ‖(CFC.sqrt e*A) η‖^2=(inner ℂ ((e*A*A) η) η).re := by
    rw [← hroot]
    change ‖(CFC.sqrt e*A) η‖^2=(inner ℂ ((CFC.sqrt e*A).adjoint ((CFC.sqrt e*A) η)) η).re
    rw [ContinuousLinearMap.adjoint_inner_left]
    exact (inner_self_eq_norm_sq (𝕜:=ℂ) _).symm
  have hn := T.le_opNorm ((CFC.sqrt e*A) η)
  have hsq : ‖T ((CFC.sqrt e*A) η)‖^2 ≤ ‖T‖^2*‖(CFC.sqrt e*A) η‖^2 := by
    simpa only [mul_pow] using (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (norm_nonneg _) (norm_nonneg _))).mpr hn
  have hb := weightedBlock_phase_energy_bound A B e x η z hz hA he hBB heA hv
  rw [hact] at hb
  exact (hb.trans hsq).trans_eq (congrArg (fun t : ℝ => ‖T‖^2*t) henergy)

#print axioms selfAdjoint_inner_im_zero
#print axioms realPhaseEnergyIdentity
#print axioms variationalPair_energy_bound
#print axioms weightedBlock_Y_selfAdjoint
#print axioms weightedBlock_root_sandwich
#print axioms weightedBlock_phase_energy_bound
#print axioms weightedBlock_multiplier_energy_bound
end
end TGLV350.Regular
