import TGLExt.BisognanoWichmann
import TGLExt.Solder4D
import TGLExt.O16.BoostRepresentationBridges
import TGLExt.FalsidadeDaInercia

set_option autoImplicit false
set_option maxHeartbeats 2000000

/-!
[DERIVED] Explicit longitudinal Lorentz realization of the dual scaling law.
Coordinates are (E,p) in c=1 units, pPlus=E+p, pMinus=E-p (unnormalized).
Thus massSquared=pPlus*pMinus; normalized null coordinates require factor 2.
The inherited boost was described in (x,t) coordinates: its same symmetric
matrix acts here on (E,p), with chosen metric E^2-p^2, and rapidity -s.
Neither this realization nor the generic lift identifies the canonical core
trace with a physical body's energy, or the dual action with the BW modular
group. No dimension, signature, Einstein-H3, or empirical identification follows.
`Inertial` means fixed by every boost, not force-free inertial motion.
-/
namespace TGLExt.PonteDaEscalaDual
open Matrix
noncomputable section

abbrev Momentum := Fin 2 → ℝ
def energy (v : Momentum) : ℝ := v 0
def momentum (v : Momentum) : ℝ := v 1
def pPlus (v : Momentum) : ℝ := energy v + momentum v
def pMinus (v : Momentum) : ℝ := energy v - momentum v
def theta (s : ℝ) (v : Momentum) : Momentum := (TGLExt.boost (-s)).mulVec v
def massSquared (v : Momentum) : ℝ := pPlus v * pMinus v

theorem theta_energy (s : ℝ) (v : Momentum) :
    energy (theta s v) = Real.cosh s * energy v - Real.sinh s * momentum v := by
  simp [theta, energy, momentum, TGLExt.boost, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  ring

theorem theta_momentum (s : ℝ) (v : Momentum) :
    momentum (theta s v) = -Real.sinh s * energy v + Real.cosh s * momentum v := by
  simp [theta, energy, momentum, TGLExt.boost, Matrix.mulVec, dotProduct, Fin.sum_univ_two]

theorem pPlus_scaling (s : ℝ) (v : Momentum) :
    pPlus (theta s v) = Real.exp (-s) * pPlus v := by
  unfold pPlus
  rw [theta_energy, theta_momentum, ← Real.cosh_sub_sinh]
  ring

theorem pMinus_scaling (s : ℝ) (v : Momentum) :
    pMinus (theta s v) = Real.exp s * pMinus v := by
  unfold pMinus
  rw [theta_energy, theta_momentum, ← Real.cosh_add_sinh]
  ring

def momentumScaling : TGLExt.DualScalingData Momentum where
  tau := pPlus
  theta := theta
  scaling := pPlus_scaling

theorem theta_zero (v : Momentum) : theta 0 v = v := by
  simp [theta, TGLExt.boost_zero]

theorem theta_add (s t : ℝ) (v : Momentum) :
    theta (s+t) v = theta s (theta t v) := by
  simp only [theta, Matrix.mulVec_mulVec, TGLExt.boost_add, neg_add]

theorem inertial_momentum_is_zero {v : Momentum}
    (h : FalsidadeDaInercia.Inertial momentumScaling v) : pPlus v = 0 :=
  FalsidadeDaInercia.the_inertia_is_the_absolute_zero momentumScaling h

theorem rest_post_exists_and_moves :
    FalsidadeDaInercia.IsPost momentumScaling ![1,0] ∧
    ¬ FalsidadeDaInercia.Inertial momentumScaling ![1,0] := by
  have h : FalsidadeDaInercia.IsPost momentumScaling ![1,0] := by
    norm_num [FalsidadeDaInercia.IsPost, momentumScaling, pPlus, energy, momentum]
  exact ⟨h, FalsidadeDaInercia.a_post_is_not_inertial momentumScaling h⟩

theorem positive_weight_stays_positive {v : Momentum} (h : 0 < pPlus v) (s : ℝ) :
    0 < pPlus (theta s v) := by
  rw [pPlus_scaling]
  exact mul_pos (Real.exp_pos _) h

theorem mass_is_the_invariant (s : ℝ) (v : Momentum) :
    massSquared (theta s v) = massSquared v := by
  unfold massSquared
  rw [pPlus_scaling, pMinus_scaling]
  calc
    _ = (Real.exp (-s) * Real.exp s) * (pPlus v * pMinus v) := by ring
    _ = pPlus v * pMinus v := by rw [← Real.exp_add]; simp

theorem mass_is_minkowski (v : Momentum) :
    massSquared v = energy v ^ 2 - momentum v ^ 2 := by
  unfold massSquared pPlus pMinus
  ring

theorem energy_is_the_reading (s : ℝ) (v : Momentum) :
    energy (theta s v) = (Real.exp (-s) * pPlus v + Real.exp s * pMinus v) / 2 := by
  have hp := pPlus_scaling s v
  have hm := pMinus_scaling s v
  unfold pPlus pMinus at hp hm
  linarith

theorem observer_energy_changes (s : ℝ) (h : s ≠ 0) :
    energy (theta s ![1,1]) ≠ energy ![1,1] := by
  rw [theta_energy]
  simp only [energy, momentum, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
  simp only [mul_one]
  rw [Real.cosh_sub_sinh]
  intro he
  have hn := Real.exp_eq_one_iff.mp he
  exact h (neg_eq_zero.mp hn)

def embed (v : Momentum) : Fin 4 → ℝ := ![energy v, momentum v, 0, 0]
theorem mass_is_eta4 (v : Momentum) :
    massSquared v = embed v ⬝ᵥ (TGLExt.eta4.mulVec (embed v)) := by
  rw [mass_is_minkowski]
  simp [embed, TGLExt.eta4, Matrix.mulVec, dotProduct, Fin.sum_univ_four]
  ring

theorem boost_is_existing_4D_block (s : ℝ) (i j : Fin 2) :
    TGLExt.boost (-s) i j = TGLExt.boostMat (-s)
      (Fin.castLE (by decide : 2 ≤ 4) i) (Fin.castLE (by decide : 2 ≤ 4) j) :=
  ChatgptAudit.BoostBridges016.boost_is_first_block (-s) i j

/-- Rest-energy theorem from the mass shell with c explicit and positive energy.
    Shell, rest, and positive c are stated premises, not derived matter physics. -/
theorem rest_energy_eq_mc2 (E p m c : ℝ) (hc : 0 < c) (hE : 0 ≤ E) (hm : 0 ≤ m)
    (hshell : E^2 - c^2*p^2 = m^2*c^4) (hrest : p = 0) : E = m*c^2 := by
  rw [hrest] at hshell
  have hmc : 0 ≤ m*c^2 := mul_nonneg hm (sq_nonneg c)
  nlinarith [sq_nonneg (E-m*c^2)]

/-- Noncanonical lift: each chosen invariant mu2 gives a realization. -/
def lift {M : Type} (D : TGLExt.DualScalingData M) (mu2 : ℝ) (a : M) : Momentum :=
  ![(D.tau a + mu2 / D.tau a)/2, (D.tau a - mu2 / D.tau a)/2]

theorem lift_pPlus {M : Type} (D : TGLExt.DualScalingData M) (mu2 : ℝ) (a : M) :
    pPlus (lift D mu2 a) = D.tau a := by
  simp [pPlus, lift, energy, momentum]
  ring

theorem lift_pMinus {M : Type} (D : TGLExt.DualScalingData M) (mu2 : ℝ) (a : M) :
    pMinus (lift D mu2 a) = mu2 / D.tau a := by
  simp [pMinus, lift, energy, momentum]
  ring

theorem lift_mass {M : Type} (D : TGLExt.DualScalingData M) (mu2 : ℝ) (a : M)
    (h : D.tau a ≠ 0) : massSquared (lift D mu2 a) = mu2 := by
  rw [massSquared, lift_pPlus, lift_pMinus]
  field_simp

theorem null_coordinates_injective (v w : Momentum)
    (hp : pPlus v = pPlus w) (hm : pMinus v = pMinus w) : v = w := by
  unfold pPlus pMinus energy momentum at hp hm
  funext i
  fin_cases i <;> linarith

theorem lift_equivariant {M : Type} (D : TGLExt.DualScalingData M) (mu2 : ℝ)
    (a : M) (s : ℝ) : lift D mu2 (D.theta s a) = theta s (lift D mu2 a) := by
  apply null_coordinates_injective
  · rw [lift_pPlus, pPlus_scaling, lift_pPlus, D.scaling]
  · rw [lift_pMinus, pMinus_scaling, lift_pMinus, D.scaling, Real.exp_neg]
    field_simp

theorem lift_mass_not_selected {M : Type} (D : TGLExt.DualScalingData M) (a : M)
    (ha : D.tau a ≠ 0) (u v : ℝ) (huv : u ≠ v) : lift D u a ≠ lift D v a := by
  intro h
  have he := congrArg massSquared h
  rw [lift_mass D u a ha, lift_mass D v a ha] at he
  exact huv he

end
end TGLExt.PonteDaEscalaDual

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("O25_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
