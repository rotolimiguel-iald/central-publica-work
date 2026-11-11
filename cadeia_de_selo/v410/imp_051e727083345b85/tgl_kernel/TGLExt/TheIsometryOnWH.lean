import TGLExt.TheWitnessLinearOnWH

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A ISOMETRIA EM `WH` — o campo `isometric` do certificado
  [BANCADA — 27/08/2026 · marco M4 · rumo ao 4/4 fechado]

O certificado pede `‖J v‖ = ‖v‖` **em `WH`**. A isometria estava provada no
pré-espaço; aqui ela **atravessa** — pelo mesmo transporte por densidade que já pagou
cinco vezes nesta arquitetura, e que agora paga a sexta.

* ★★★ **`towerJ_norm`** — `‖J z‖ = ‖z‖` no completamento inteiro;
* ★★ `towerJ_isometry` — logo `J` é isometria de `WH`.

β jamais entra; nada move o gate.
-/

namespace TGLExt

open UniformSpace

variable {P : SiteProfile}

/-- ★★★ **A ISOMETRIA EM `WH`**: `‖J z‖ = ‖z‖` no completamento inteiro. -/
theorem towerJ_norm (P : SiteProfile) (z : TowerHilbert P) :
    ‖towerJ P z‖ = ‖z‖ := by
  have h1 : Continuous (fun w : TowerHilbert P => ‖towerJ P w‖) :=
    continuous_norm.comp (towerJ_continuous P)
  have h2 : Continuous (fun w : TowerHilbert P => ‖w‖) := continuous_norm
  refine Completion.induction_on z (isClosed_eq h1 h2) ?_
  intro a
  rw [towerJ_coe, Completion.norm_coe, Completion.norm_coe, profileJpre_norm]

/-- ★★ sinal e diferença em `WH`. -/
theorem towerJ_neg (P : SiteProfile) (z : TowerHilbert P) :
    towerJ P (-z) = - towerJ P z := by
  have h := towerJ_conj_smul P (-1 : ℂ) z
  rw [neg_one_smul] at h
  rw [h]
  simp

theorem towerJ_sub (P : SiteProfile) (z w : TowerHilbert P) :
    towerJ P (z - w) = towerJ P z - towerJ P w := by
  rw [sub_eq_add_neg, towerJ_add, towerJ_neg, ← sub_eq_add_neg]

/-- ★★ **LOGO É ISOMETRIA DE `WH`**. -/
theorem towerJ_isometry (P : SiteProfile) : Isometry (towerJ P) := by
  refine Isometry.of_dist_eq fun z w => ?_
  rw [dist_eq_norm, dist_eq_norm, ← towerJ_sub, towerJ_norm]

end TGLExt
