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
import TGLExt.ModularFlowHilbert

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit
open TGLExt Matrix UniformSpace
noncomputable section
variable {P : SiteProfile}

theorem modularPhase_cocycle (t a b c : ℝ) :
    modularPhase t (a-b) * modularPhase t (b-c) = modularPhase t (a-c) := by
  unfold modularPhase
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

theorem flowLevel_mul (t : ℝ) (N : ℕ) (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    flowLevel P t N (a*b) = flowLevel P t N a * flowLevel P t N b := by
  ext i k
  simp only [flowLevel, Matrix.mul_apply, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  rw [← modularPhase_cocycle t (Real.log (towerW P N i))
    (Real.log (towerW P N j)) (Real.log (towerW P N k))]
  ring

theorem flowPre_lmul (t : ℝ) {N : ℕ} (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (v : TowerPre P) : flowPre P t (lmulPre P a v) =
      lmulPre P (flowLevel P t N a) (flowPre P t v) := by
  obtain ⟨M,b,rfl⟩ := exists_tof v
  rw [lmulPre_tof_at (K := N ⊔ M) le_sup_left le_sup_right,
    flowPre_tof, flowPre_tof,
    lmulPre_tof_at (K := N ⊔ M) le_sup_left le_sup_right]
  congr 1
  rw [flowLevel_mul, flowLevel_push, flowLevel_push]

theorem modularFlow_intertwines (t : ℝ) {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (x : TowerHilbert P) :
    modularFlow P t (towerPi P a x) = towerPi P (flowLevel P t N a) (modularFlow P t x) := by
  refine Completion.induction_on x (isClosed_eq
    ((modularFlow_continuous t).comp (towerPi P a).continuous)
    ((towerPi P (flowLevel P t N a)).continuous.comp (modularFlow_continuous t))) ?_
  intro v
  rw [towerPi_coe, modularFlow_coe, flowPre_lmul, modularFlow_coe, towerPi_coe]

def modularConjugation (P : SiteProfile) (t : ℝ) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) ≃⋆ₐ[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  (modularFlowUnitary P t).conjStarAlgEquiv

theorem modularConjugation_local (t : ℝ) {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    modularConjugation P t (towerPi P a) = towerPi P (flowLevel P t N a) := by
  ext x
  change modularFlow P t (towerPi P a (modularFlow P (-t) x)) = _
  rw [modularFlow_intertwines, modularFlow_group, add_neg_cancel, modularFlow_zero_time]

theorem modularConjugation_towerImage (t : ℝ)
    (a : TowerHilbert P →L[ℂ] TowerHilbert P) :
    a ∈ towerImage P ↔ modularConjugation P t a ∈ towerImage P := by
  constructor
  · rintro ⟨N,b,rfl⟩
    rw [modularConjugation_local]
    exact towerPi_mem_towerImage _
  · rintro ⟨N,b,hb⟩
    refine ⟨N,flowLevel P (-t) N b,?_⟩
    apply (modularConjugation P t).injective
    change modularConjugation P t a = modularConjugation P t (towerPi P (flowLevel P (-t) N b))
    rw [hb, modularConjugation_local, flowLevel_group, add_neg_cancel, flowLevel_zero_time]

theorem centralizer_transport
    (e : (TowerHilbert P →L[ℂ] TowerHilbert P) ≃⋆ₐ[ℂ]
      (TowerHilbert P →L[ℂ] TowerHilbert P))
    (s : Set (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hs : ∀ a, a ∈ s ↔ e a ∈ s)
    (a : TowerHilbert P →L[ℂ] TowerHilbert P) :
    a ∈ StarSubalgebra.centralizer ℂ s ↔ e a ∈ StarSubalgebra.centralizer ℂ s := by
  simp only [StarSubalgebra.mem_centralizer_iff]
  constructor
  · intro ha b hb
    have hpre : e.symm b ∈ s := (hs _).mpr (by simpa using hb)
    obtain ⟨h1,h2⟩ := ha (e.symm b) hpre
    exact ⟨by simpa only [map_mul, StarAlgEquiv.apply_symm_apply] using congrArg e h1,
      by simpa only [map_mul, map_star, StarAlgEquiv.apply_symm_apply] using congrArg e h2⟩
  · intro ha b hb
    obtain ⟨h1,h2⟩ := ha (e b) ((hs b).mp hb)
    constructor
    · apply e.injective
      change e (b*a) = e (a*b)
      simpa only [map_mul] using h1
    · apply e.injective
      change e (star b*a) = e (a*star b)
      simpa only [map_mul, map_star] using h2

/-- A invariância modular é construída sobre o bicomutante efetivo da torre. -/
theorem modularConjugation_preserves_factor (P : SiteProfile) (t : ℝ)
    (a : TowerHilbert P →L[ℂ] TowerHilbert P) :
    a ∈ theFactorObject P ↔ modularConjugation P t a ∈ theFactorObject P := by
  exact centralizer_transport (modularConjugation P t) _
    (centralizer_transport (modularConjugation P t) (towerImage P)
      (modularConjugation_towerImage t)) a

#print axioms modularFlow_intertwines
#print axioms modularConjugation_local
#print axioms modularConjugation_preserves_factor
end
end ChatgptAudit
