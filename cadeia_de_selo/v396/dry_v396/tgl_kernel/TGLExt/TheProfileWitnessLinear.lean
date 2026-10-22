import TGLExt.TheColimitIsometry

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA DO PERFIL É ADITIVA E ANTILINEAR — os pré-requisitos da extensão
  [BANCADA — 26/08/2026 · marco M4 · lote]

A v230 provou aditividade e antilinearidade para a conjugação da densidade uniforme.
A v231 corrigiu a densidade. Estas são as MESMAS provas, refeitas sobre a densidade
CERTA — e são pré-requisito da extensão: sem aditividade não há `‖J x − J y‖ = ‖x − y‖`,
e sem isso não há continuidade uniforme.

* ★★★ `profileJpre_add` — aditiva no colimite (atravessa o supremo de andares);
* ★★★ `profileJpre_conj_smul` — ANTIlinear no colimite;
* ★★ `profileJpre_zero` — zero em zero.

β jamais entra. Nada move o gate.
-/

namespace TGLExt

open Matrix

variable {P : SiteProfile}

theorem profileJlevel_add (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileJlevel P N (a + b) = profileJlevel P N a + profileJlevel P N b :=
  stateJG_add _ _ a b

theorem profileJlevel_conj_smul (P : SiteProfile) (N : ℕ) (c : ℂ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileJlevel P N (c • a) = (starRingEnd ℂ) c • profileJlevel P N a :=
  stateJG_conj_smul _ _ c a

/-- ★★★ **ADITIVA NO COLIMITE**, com a densidade certa. -/
theorem profileJpre_add (P : SiteProfile) (x y : TowerPre P) :
    profileJpre P (x + y) = profileJpre P x + profileJpre P y := by
  obtain ⟨N, a, rfl⟩ := exists_tof x
  obtain ⟨M, b, rfl⟩ := exists_tof y
  rw [tof_add_hetero, profileJpre_tof, profileJpre_tof, profileJpre_tof,
      tof_add_hetero]
  congr 1
  rw [profileJlevel_add, ← profileJ_commutes_with_tPush P le_sup_left,
      ← profileJ_commutes_with_tPush P le_sup_right]

/-- ★★★ **ANTILINEAR NO COLIMITE**, com a densidade certa. -/
theorem profileJpre_conj_smul (P : SiteProfile) (c : ℂ) (x : TowerPre P) :
    profileJpre P (c • x) = (starRingEnd ℂ) c • profileJpre P x := by
  obtain ⟨N, a, rfl⟩ := exists_tof x
  rw [tof_smul, profileJpre_tof, profileJpre_tof, tof_smul,
      profileJlevel_conj_smul]

/-- ★★ **ZERO EM ZERO**. -/
theorem profileJpre_zero (P : SiteProfile) :
    profileJpre P (0 : TowerPre P) = 0 := by
  show profileJpre P (tof P 0 0) = tof P 0 0
  rw [profileJpre_tof]
  congr 1
  unfold profileJlevel stateJG
  simp

end TGLExt
