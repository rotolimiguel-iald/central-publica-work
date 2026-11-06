-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT (05/09/2026) — transposta em 05/09/2026
-- Procedencia: C:\IALD\Central de Patentes\Chatgpt (bancada da outra sessao,
--   sob direcao do operador; TUNEL\TUNEL_PROTOCOLO.md).
-- Auditoria da gerencia (sessao Claude d554e796, 05/09/2026): recompilacao
--   independente 20/20 exit 0; sonda #print axioms dos teoremas de manchete =
--   [propext, Classical.choice, Quot.sound]; zero sorry; enunciados conferidos.
-- Transposicao MECANICA: apenas (a) este cabecalho, (b) "import TGLExt" (root)
--   expandido no bloco de imports da epoca, (c) imports internos da bancada
--   prefixados com TGLExt. — nada mais foi alterado. Namespace ChatgptAudit
--   PRESERVADO como marca de procedencia.
-- Estatuto: [REAL — Lean] analise modular da torre produto (S, J·S, Delta,
--   Delta^{it}, invariancia do bicomutante). NAO move gate; NAO e fisica;
--   NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.ClosedModulatorCandidate
import TGLExt.TheModularRelations

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace ChatgptAudit
open TGLExt Matrix
noncomputable section
variable {P : SiteProfile}

theorem root_mul_density_inverse (P : SiteProfile) (N : ℕ) :
    profileRoot P N * rhoMatInv P N = profileRootInv P N := by
  calc
    profileRoot P N * rhoMatInv P N =
        (profileRootInv P N * profileRoot P N) * profileRoot P N * rhoMatInv P N := by
          rw [profileRootInv_mul_root, one_mul]
    _ = profileRootInv P N * (profileRoot P N * profileRoot P N) * rhoMatInv P N := by
          noncomm_ring
    _ = profileRootInv P N * rhoMat P N * rhoMatInv P N := by rw [profileRoot_sq]; rfl
    _ = profileRootInv P N := by rw [mul_assoc, rhoMat_mul_inv, mul_one]

theorem modular_twist_of_J (P : SiteProfile) (N : ℕ)
    (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    modTwist P (profileJlevel P N b) = towerDeltaHalfLevel P N b := by
  unfold modTwist
  rw [profileJlevel_eq, conjTranspose_mul, conjTranspose_mul,
    profileRootInv_isHermitian, profileRoot_isHermitian, conjTranspose_conjTranspose]
  simp only [← mul_assoc]
  rw [rhoMat_mul_rootInv,
    mul_assoc (profileRoot P N * b) (profileRoot P N) (rhoMatInv P N),
    root_mul_density_inverse]
  rfl

theorem towerJ_inner_flip (u v : TowerHilbert P) :
    inner ℂ u (towerJ P v) = inner ℂ v (towerJ P u) := by
  have anti (a b : TowerHilbert P) :
      inner ℂ (towerJ P a) (towerJ P b) = star (inner ℂ a b) := by
    have hp : ‖towerJ P a + towerJ P b‖ = ‖a + b‖ := by
      rw [← towerJ_add, towerJ_norm]
    have hm : ‖towerJ P a - towerJ P b‖ = ‖a - b‖ := by
      rw [← towerJ_sub, towerJ_norm]
    have hip : ‖towerJ P a + Complex.I • towerJ P b‖ = ‖a - Complex.I • b‖ := by
      conv_rhs => rw [← towerJ_norm P (a - Complex.I • b)]
      rw [towerJ_sub, towerJ_conj_smul]
      simp
    have him : ‖towerJ P a - Complex.I • towerJ P b‖ = ‖a + Complex.I • b‖ := by
      conv_rhs => rw [← towerJ_norm P (a + Complex.I • b)]
      rw [towerJ_add, towerJ_conj_smul]
      simp [sub_eq_add_neg]
    rw [inner_eq_sum_norm_sq_div_four, inner_eq_sum_norm_sq_div_four]
    simp only [RCLike.I_to_complex, hp, hm, hip, him]
    simp
    ring
  have h := anti (towerJ P u) v
  rw [towerJ_involutive] at h
  change inner ℂ u (towerJ P v) = (starRingEnd ℂ) (inner ℂ (towerJ P u) v) at h
  simpa only [inner_conj_symm] using h

/-- Identidade no domínio COMPLETO de JS, testada por qualquer vetor local. -/
theorem modulator_pairing_local (x : closedTomitaDomain P) {N : ℕ}
    (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    inner ℂ ((tof P N b : TowerPre P) : TowerHilbert P) (closedModulatorCandidate P x) =
      inner ℂ ((tof P N (towerDeltaHalfLevel P N b) : TowerPre P) : TowerHilbert P)
        (x : TowerHilbert P) := by
  calc
    _ = inner ℂ (closedTomita P x)
        (towerJ P ((tof P N b : TowerPre P) : TowerHilbert P)) :=
      towerJ_inner_flip _ _
    _ = inner ℂ (closedTomita P x) (rTowerPi P (profileJlevel P N b) (hOmega P)) := by
      rw [rTowerPi_omega, towerJ_coe, profileJpre_tof]
    _ = inner ℂ ((star (rTowerPi P (profileJlevel P N b))) (hOmega P))
        (x : TowerHilbert P) := closure_graph_pairing (closedTomita_graph x) _
    _ = _ := by
      rw [ContinuousLinearMap.star_eq_adjoint, ← rTowerPi_star, rTowerPi_omega,
        modular_twist_of_J]

#print axioms modular_twist_of_J
#print axioms towerJ_inner_flip
#print axioms modulator_pairing_local
end
end ChatgptAudit
