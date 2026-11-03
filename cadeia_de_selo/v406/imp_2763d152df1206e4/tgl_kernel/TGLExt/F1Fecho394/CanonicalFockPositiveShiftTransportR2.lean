import TGLExt.F1Fecho394.CanonicalFockActualTracialExtensionR1
import TGLExt.F1Fecho394.CanonicalFockInverseSupremumR2
import TGLExt.V354PolarIntertwining
import TGLExt.V354TraceShiftEquivalence

/-! DECLARADO / UNCOMPILED CANDIDATE, R50, 2026-10-16.
R2 unfolds positiveAsCore explicitly in the two power-coercion proofs.
The square-pair proof from V354PositiveTraceTransport is reused at a generic
von Neumann algebra. Its quadratic-value premise is discharged in the concrete
Fock consumer by R49, rather than assumed as a trace on the final interface.
The already constructed boundedPolar and its shift-support theorem are reused.
PositiveInput, inverseSupremum and value are the existing Fock objects.
No SiteProfile, replacement GNS, positive weight or polar construction is added.
Compilation and independent review remain required; full R7/PF is not asserted. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 8
noncomputable section
namespace F1Fecho.CanonicalFockPositiveShiftTransportR2
open TGLV350.Regular (positive_sqrt_intertwines vonNeumann_norm_closed RegularHilbert)
open TGLV354 (boundedPolar boundedPolar_mem)
open TGLV354.TraceCompletion (ShiftRelated boundedPolar_transports_shift_factors)
open F1Fecho.CanonicalFockRegular (core fockFlow)
open F1Fecho.CanonicalFockWeight (PositiveInput regularFockVacuum)
open F1Fecho.CanonicalFockInverseSupremum (value)
open F1Fecho.RegularInverseWeight (inverseSupremum)
open scoped ENNReal

theorem positive_transport_square_pair {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H) (p q u : N.toStarSubalgebra) (hq : 0 ≤ q.val)
    (htransport : p.val = u.val*q.val*star u.val)
    (hsupport : (star u.val*u.val)*q.val = q.val) :
    ∃ a : N.toStarSubalgebra,
      star a.val*a.val=q.val ∧ a.val*star a.val=p.val := by
  let e := star u.val*u.val
  let d := CFC.sqrt q.val
  have hqs := hq.isSelfAdjoint.star_eq
  have hqe : q.val*e=q.val := by
    have h := congrArg star hsupport
    simpa only [star_mul,hqs,star_star] using h
  have hzero : q.val*(e-1)=(e-1)*0 := by
    rw [mul_sub,hqe,mul_one,sub_self,mul_zero]
  have hroot : d*(e-1)=0 := by
    have h := positive_sqrt_intertwines q.val 0 (e-1) hq le_rfl hzero
    simpa only [CFC.sqrt_zero,mul_zero] using h
  have hde : d*e=d := by
    rw [mul_sub,mul_one,sub_eq_zero] at hroot
    exact hroot
  letI : IsClosed (N.toStarSubalgebra : Set (H →L[ℂ] H)) := vonNeumann_norm_closed N
  have hdmem : d ∈ N := by
    dsimp [d]
    rw [CFC.sqrt_eq_real_sqrt q.val hq]
    exact cfcₙ_mem (𝕜' := ℂ) (s := N.toStarSubalgebra) Real.sqrt q.property
  let a : N.toStarSubalgebra := u*⟨d,hdmem⟩
  have hds : star d=d := (CFC.sqrt_nonneg q.val).isSelfAdjoint.star_eq
  have hdd : d*d=q.val := CFC.sqrt_mul_sqrt_self q.val hq
  have haa : star a.val*a.val=q.val := by
    change star (u.val*d)*(u.val*d)=q.val
    calc
      _ = d*(star u.val*u.val)*d := by rw [star_mul,hds]; noncomm_ring
      _ = d*d := by rw [hde]
      _ = q.val := hdd
  have haa' : a.val*star a.val=p.val := by
    change (u.val*d)*star (u.val*d)=p.val
    calc
      _ = u.val*(d*d)*star u.val := by rw [star_mul,hds]; noncomm_ring
      _ = p.val := by rw [hdd,← htransport]
  exact ⟨a,haa,haa'⟩

#print axioms positive_transport_square_pair

/-- Generic algebraic consumer. The concrete theorem below supplies hquadratic. -/
theorem quadraticValue_transport_of_support {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H) (W : (H →L[ℂ] H) → ℝ≥0∞)
    (hquadratic : ∀ a : N.toStarSubalgebra,
      W (star a.val * a.val) = W (a.val * star a.val))
    (p q u : N.toStarSubalgebra) (hq : 0 ≤ q.val)
    (htransport : p.val = u.val * q.val * star u.val)
    (hsupport : (star u.val * u.val) * q.val = q.val) :
    W p.val = W q.val := by
  obtain ⟨a, haa, haa'⟩ := positive_transport_square_pair N p q u hq htransport hsupport
  exact (congrArg W haa'.symm).trans ((hquadratic a).symm.trans (congrArg W haa))
#print axioms quadraticValue_transport_of_support

/-- The positive operator embedded into the same represented Fock core. -/
def positiveAsCore (p : PositiveInput) : core.toStarSubalgebra := ⟨p.val, p.property.1⟩

/-- R49 supplies the quadratic law of the existing inverse supremum. -/
theorem value_transport_of_support (p q : PositiveInput) (u : core.toStarSubalgebra)
    (htransport : p.val = u.val * q.val * star u.val)
    (hsupport : (star u.val * u.val) * q.val = q.val) :
    value p = value q :=
  quadraticValue_transport_of_support core
    (inverseSupremum fockFlow regularFockVacuum)
    F1Fecho.CanonicalFockActualTracialExtensionR1.inverseSupremum_tracial
    (positiveAsCore p) (positiveAsCore q) u q.property.2 htransport hsupport
#print axioms value_transport_of_support

/-- The actual polar in the same core gives positive shift compatibility.
No trace, support equality, or polar existence premise is added. -/
theorem positiveShift_value_compatible (p q : PositiveInput)
    (h : ShiftRelated (positiveAsCore p) (positiveAsCore q)) :
    value p = value q := by
  obtain ⟨n, hn, r, s, hr, _, hp, hq⟩ := h
  have hr' : p.val * r.val = r.val * q.val :=
    congrArg (fun x : core.toStarSubalgebra => x.val) hr
  have hp' : p.val ^ n = r.val * s.val := by
    simpa [positiveAsCore] using congrArg (fun x : core.toStarSubalgebra => x.val) hp
  have hq' : q.val ^ n = s.val * r.val := by
    simpa [positiveAsCore] using congrArg (fun x : core.toStarSubalgebra => x.val) hq
  have hpol := boundedPolar_transports_shift_factors
    (H := RegularHilbert F1Rede.BosonicFock.F) p.val q.val r.val s.val
    p.property.2.isSelfAdjoint q.property.2.isSelfAdjoint n hn hr' hp' hq'
  let u : core.toStarSubalgebra :=
    ⟨boundedPolar r.val, boundedPolar_mem core r.val r.property⟩
  exact value_transport_of_support p q u hpol.1 hpol.2
#print axioms positiveShift_value_compatible

end F1Fecho.CanonicalFockPositiveShiftTransportR2
