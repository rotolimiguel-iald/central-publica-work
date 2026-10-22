import Lean
import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace ChatgptAudit.WignerOrbit016

def phase (x : ℝ) : ℂ := Complex.exp ((x : ℂ) * Complex.I)

theorem phase_positive_ray_faithful (c : ℝ)
    (h : ∀ r : ℝ, 0 < r → phase (r*c) = 1) : c = 0 := by
  by_contra hc
  have hm : (-1 : ℂ) ≠ 1 := by norm_num
  rcases lt_or_gt_of_ne hc with hn | hp
  · have hr : 0 < -Real.pi / c := div_pos_of_neg_of_neg (neg_neg_of_pos Real.pi_pos) hn
    have hh := h (-Real.pi / c) hr
    rw [div_mul_cancel₀ _ hc] at hh
    have he : phase (-Real.pi) = -1 := by
      simp [phase, Complex.exp_neg, Complex.exp_pi_mul_I]
    exact hm (he.symm.trans hh)
  · have hh := h (Real.pi / c) (div_pos Real.pi_pos hp)
    rw [div_mul_cancel₀ _ hc] at hh
    have he : phase Real.pi = -1 := by simp [phase, Complex.exp_pi_mul_I]
    exact hm (he.symm.trans hh)

theorem phase_difference {x y : ℝ} (hx : phase x = 1) (hy : phase y = 1) :
    phase (x-y) = 1 := by
  unfold phase at *
  rw [Complex.ofReal_sub, sub_mul, Complex.exp_sub, hx, hy]
  simp

/-- Explicit (+---) pairing; no identification with a reserved physical witness. -/
def orbitPairing (a p : Fin 4 → ℝ) : ℝ :=
  a 0*p 0-a 1*p 1-a 2*p 2-a 3*p 3

def futureMassShell (m : ℝ) : Set (Fin 4 → ℝ) :=
  {p | 0 < p 0 ∧ p 0^2 = p 1^2+p 2^2+p 3^2+m^2}

def axisMomentum (energy q : ℝ) (j : Fin 3) : Fin 4 → ℝ :=
  ![energy, if j=0 then q else 0, if j=1 then q else 0, if j=2 then q else 0]

theorem pairing_axis (a : Fin 4 → ℝ) (energy q : ℝ) (j : Fin 3) :
    orbitPairing a (axisMomentum energy q j) = a 0*energy-a j.succ*q := by
  fin_cases j <;> simp [orbitPairing, axisMomentum] <;> ring

theorem axis_in_shell (m energy q : ℝ) (j : Fin 3)
    (he : 0 < energy) (heq : energy^2=q^2+m^2) :
    axisMomentum energy q j ∈ futureMassShell m := by
  fin_cases j <;> simp [axisMomentum, futureMassShell] <;> exact ⟨he, by nlinarith⟩

theorem null_orbit_faithful (a : Fin 4 → ℝ)
    (h : ∀ p ∈ futureMassShell 0, phase (orbitPairing a p)=1) : a=0 := by
  have hm (j : Fin 3) : a 0-a j.succ=0 := by
    apply phase_positive_ray_faithful
    intro r hr
    have hh := h (axisMomentum r r j) (axis_in_shell 0 r r j hr (by ring))
    rw [pairing_axis] at hh
    convert hh using 1 <;> congr 1 <;> ring
  have hp (j : Fin 3) : a 0+a j.succ=0 := by
    apply phase_positive_ray_faithful
    intro r hr
    have hh := h (axisMomentum r (-r) j) (axis_in_shell 0 r (-r) j hr (by ring))
    rw [pairing_axis] at hh
    convert hh using 1 <;> congr 1 <;> ring
  have ht : a 0=0 := by have := hm 0; have := hp 0; simpa using (show a 0=0 by linarith [hm 0,hp 0])
  ext i
  fin_cases i
  · exact ht
  · simpa using (show a 1=0 by have := hm 0; simpa [ht] using (hm 0).symm)
  · have := hm 1; simpa [ht] using this.symm
  · have := hm 2; simpa [ht] using this.symm

theorem massive_orbit_faithful (m : ℝ) (hm : 0<m) (a : Fin 4 → ℝ)
    (h : ∀ p ∈ futureMassShell m, phase (orbitPairing a p)=1) : a=0 := by
  have hs (j : Fin 3) : a j.succ=0 := by
    have hc : -2*a j.succ=0 := by
      apply phase_positive_ray_faithful
      intro q hq
      let e := Real.sqrt (q^2+m^2)
      have he : 0<e := Real.sqrt_pos.mpr (by nlinarith [sq_pos_of_pos hm])
      have heq : e^2=q^2+m^2 := Real.sq_sqrt (by positivity)
      have hh := phase_difference
        (h (axisMomentum e q j) (axis_in_shell m e q j he heq))
        (h (axisMomentum e (-q) j) (axis_in_shell m e (-q) j he (by nlinarith [heq])))
      simp only [pairing_axis] at hh
      convert hh using 1 <;> congr 1 <;> ring
    linarith
  have ht : a 0=0 := by
    apply phase_positive_ray_faithful
    intro r hr
    let e := m+r
    let q := Real.sqrt (e^2-m^2)
    have he : 0<e := by dsimp [e]; linarith
    have heq : e^2=q^2+m^2 := by
      have hh : q^2=e^2-m^2 := Real.sq_sqrt (by dsimp [e]; nlinarith)
      linarith
    have hh := phase_difference
      (h (axisMomentum e q 0) (axis_in_shell m e q 0 he heq))
      (h (axisMomentum m 0 0) (axis_in_shell m m 0 0 hm (by ring)))
    simp only [pairing_axis] at hh
    have hs1 : a 1=0 := hs 0
    simp only [Fin.succ_zero_eq_one, hs1, zero_mul, sub_zero] at hh
    convert hh using 1 <;> congr 1 <;> dsimp [e] <;> ring
  ext i
  fin_cases i
  · exact ht
  · exact hs 0
  · exact hs 1
  · exact hs 2

/-- Both helicities have the same scalar translation character on the null orbit.
This only discharges pointwise faithfulness, not the helicity boost representation. -/
theorem doubled_null_character_faithful (a : Fin 4 → ℝ)
    (h : ∀ p ∈ futureMassShell 0,
      (phase (orbitPairing a p), phase (orbitPairing a p)) = (1,1)) : a=0 := by
  apply null_orbit_faithful a
  intro p hp
  exact congrArg Prod.fst (h p hp)

#print axioms phase_positive_ray_faithful
#print axioms phase_difference
#print axioms pairing_axis
#print axioms axis_in_shell
#print axioms null_orbit_faithful
#print axioms massive_orbit_faithful
#print axioms doubled_null_character_faithful
end ChatgptAudit.WignerOrbit016


-- Engineering audit: all declarations introduced by this compilation unit.
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
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
