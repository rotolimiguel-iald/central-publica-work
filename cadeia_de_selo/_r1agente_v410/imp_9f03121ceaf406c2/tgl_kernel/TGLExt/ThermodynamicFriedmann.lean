import TGLExt.SectorFriedmann
import Mathlib.Analysis.Calculus.MeanValue

set_option autoImplicit false

/-!
# Explicit horizon inputs and the thermodynamic route (Order 012, B4)

Natural units are used. Cai--Kim (2005), eqs. 2.3, 2.12--2.16, supplies the
apparent-radius and heat-flux prescription; H*r_A is part of that flux.
The modified differential entropy law is an explicit input. It is not inferred
from a time-varying quotient A/(4G Phi). These data do not discharge local H3
or construct a global horizon. Consumers: B4 route comparison and B5 rewrite.
-/

namespace ChatgptAudit.FLRW
open TGLExt
noncomputable section

def hubbleArea (H : ℝ → ℝ) (t : ℝ) : ℝ := 4*Real.pi/(H t)^2
def entropyFactor (c : TGLCoupling) (w : ℝ) : ℝ := 1+c.beta*|1+w|

theorem entropy_factor_pos (c : TGLCoupling) (w : ℝ) : 0 < entropyFactor c w := by
  unfold entropyFactor
  have hb := mul_nonneg c.beta_pos.le (abs_nonneg (1+w))
  linarith

theorem hubble_area_derivative (H : ℝ → ℝ) (t : ℝ)
    (hh : DifferentiableAt ℝ H t) (hz : H t ≠ 0) :
    HasDerivAt (hubbleArea H) (-8*Real.pi*deriv H t/(H t)^3) t := by
  convert! (hasDerivAt_const t (4*Real.pi)).div (hh.hasDerivAt.pow 2) (pow_ne_zero _ hz) using 1
  simp only [Pi.pow_apply]
  field_simp
  ring

/-- Imported physical prescriptions, with the modified differential law named.
    The definitions of A, T and r_A are displayed directly in the fields. -/
structure HubbleHorizonInput (H : ℝ → ℝ) (t G Phi enthalpy : ℝ) where
  H_pos : 0 < H t
  G_pos : 0 < G
  Phi_pos : 0 < Phi
  H_diff : DifferentiableAt ℝ H t
  entropyRate : ℝ
  heatRate : ℝ
  differential_entropy : entropyRate = deriv (hubbleArea H) t/(4*G*Phi)
  enthalpy_flux : heatRate = hubbleArea H t*enthalpy*H t*(H t)⁻¹
  clausius : heatRate = (H t/(2*Real.pi))*entropyRate

/-- The old coefficient provider is consumed with the modified area differential. -/
theorem modified_clausius_coefficient (H dA G Phi : ℝ) (hg : G ≠ 0) :
    (H/(2*Real.pi))*(dA/(4*G*Phi)) = H*(dA/Phi)/(8*Real.pi*G) := by
  convert einstein_coefficient_from_clausius H (dA/Phi) G hg using 1
  congr 1
  ring

theorem tgl_second_friedmann_from_clausius (H : ℝ → ℝ) (t G Phi enthalpy : ℝ)
    (D : HubbleHorizonInput H t G Phi enthalpy) :
    deriv H t = -4*Real.pi*G*Phi*enthalpy := by
  have hh := D.H_pos.ne'
  have hg := D.G_pos.ne'
  have hp := D.Phi_pos.ne'
  have hc := D.clausius
  rw [D.enthalpy_flux, D.differential_entropy,
    modified_clausius_coefficient _ _ _ _ hg,
    (hubble_area_derivative H t D.H_diff hh).deriv] at hc
  dsimp [hubbleArea] at hc
  field_simp at hc
  nlinarith [hc]

/-- The literal radius-free flux in the errata has an extra H in its consequence. -/
theorem radius_free_flux_consequence (H Hdot G Phi enthalpy : ℝ)
    (hh : H ≠ 0) (hg : G ≠ 0) (hp : Phi ≠ 0)
    (h : (4*Real.pi/H^2)*enthalpy*H =
      (H/(2*Real.pi))*((-8*Real.pi*Hdot/H^3)/(4*G*Phi))) :
    Hdot = -4*Real.pi*G*Phi*H*enthalpy := by
  have hpi := Real.pi_ne_zero
  field_simp at h
  nlinarith [h]

/-- When Phi varies, the quotient entropy has a second derivative term. -/
theorem variable_entropy_derivative (A Phi : ℝ → ℝ) (t G : ℝ)
    (ha : DifferentiableAt ℝ A t) (hp : DifferentiableAt ℝ Phi t)
    (hg : G ≠ 0) (hz : Phi t ≠ 0) :
    HasDerivAt (fun u => A u/(4*G*Phi u))
      (deriv A t/(4*G*Phi t)-A t*deriv Phi t/(4*G*(Phi t)^2)) t := by
  convert! ha.hasDerivAt.div (hp.hasDerivAt.const_mul (4*G)) (by positivity) using 1
  field_simp

/-- General integration by a specified primitive of Phi*rho'. -/
theorem tgl_first_friedmann_from_primitive (I : Set ℝ) (hI : IsOpen I)
    (hconn : IsPreconnected I) (H rho pressure Phi primitive : ℝ → ℝ) (G : ℝ)
    (hh : ∀ t∈I, DifferentiableAt ℝ H t)
    (hprimitive : ∀ t∈I, HasDerivAt primitive (Phi t*deriv rho t) t)
    (hsecond : ∀ t∈I, deriv H t = -4*Real.pi*G*Phi t*(rho t+pressure t))
    (hcontinuity : ∀ t∈I, deriv rho t = -3*H t*(rho t+pressure t)) :
    ∃ C : ℝ, ∀ t∈I, (H t)^2 = (8*Real.pi*G/3)*primitive t+C := by
  have hd (t : ℝ) (ht : t∈I) :
      HasDerivAt (fun u => (H u)^2-(8*Real.pi*G/3)*primitive u) 0 t := by
    convert! ((hh t ht).hasDerivAt.pow 2).sub
      ((hprimitive t ht).const_mul (8*Real.pi*G/3)) using 1
    rw [hsecond t ht, hcontinuity t ht]
    ring
  obtain ⟨C,hC⟩ := hI.exists_is_const_of_deriv_eq_zero hconn
    (fun t ht => (hd t ht).differentiableAt.differentiableWithinAt)
    (fun t ht => (hd t ht).deriv)
  exact ⟨C, fun t ht => by linarith [hC t ht]⟩

theorem tgl_first_friedmann_constant_w (I : Set ℝ) (hI : IsOpen I)
    (hconn : IsPreconnected I) (H rho : ℝ → ℝ) (c : TGLCoupling) (G w : ℝ)
    (hr : ∀ t∈I, DifferentiableAt ℝ rho t)
    (D : ∀ t∈I, HubbleHorizonInput H t G (entropyFactor c w) (rho t+w*rho t))
    (H_singlefluid_continuity : ∀ t∈I, deriv rho t = -3*H t*(rho t+w*rho t)) :
    ∃ C : ℝ, ∀ t∈I,
      (H t)^2 = (8*Real.pi*G/3)*entropyFactor c w*rho t+C := by
  obtain ⟨C,hC⟩ := tgl_first_friedmann_from_primitive I hI hconn H rho
    (fun t => w*rho t) (fun _ => entropyFactor c w)
    (fun t => entropyFactor c w*rho t) G
    (fun t ht => (D t ht).H_diff)
    (fun t ht => (hr t ht).hasDerivAt.const_mul _)
    (fun t ht => tgl_second_friedmann_from_clausius H t G _ _ (D t ht)) H_singlefluid_continuity
  refine ⟨C, fun t ht => ?_⟩
  simpa [mul_assoc] using hC t ht

/-- This is the term lost by replacing the primitive with Phi(t)*rho(t). -/
theorem variable_factor_first_equation_defect (H rho Phi : ℝ → ℝ)
    (t G pressure : ℝ) (hh : DifferentiableAt ℝ H t)
    (hr : DifferentiableAt ℝ rho t) (hp : DifferentiableAt ℝ Phi t)
    (hsecond : deriv H t = -4*Real.pi*G*Phi t*(rho t+pressure))
    (hcontinuity : deriv rho t = -3*H t*(rho t+pressure)) :
    HasDerivAt (fun u => (H u)^2-(8*Real.pi*G/3)*Phi u*rho u)
      (-(8*Real.pi*G/3)*deriv Phi t*rho t) t := by
  convert! (hh.hasDerivAt.pow 2).sub
    ((hp.hasDerivAt.const_mul (8*Real.pi*G/3)).mul hr.hasDerivAt) using 1
  rw [hsecond,hcontinuity]
  ring

end
end ChatgptAudit.FLRW
