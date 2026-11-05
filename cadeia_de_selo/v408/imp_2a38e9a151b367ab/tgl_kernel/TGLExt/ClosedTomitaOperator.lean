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
import TGLExt.TomitaClosability
import Mathlib.Analysis.InnerProductSpace.LinearPMap

set_option autoImplicit false
set_option maxHeartbeats 2000000

open Filter Topology

namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

theorem tomita_graph_zero : (0, 0) ∈ tomitaGraph P := by
  refine ⟨0, (theFactorObject P).zero_mem, ?_⟩
  simp

theorem tomita_graph_add {p q : TowerHilbert P × TowerHilbert P}
    (hp : p ∈ tomitaGraph P) (hq : q ∈ tomitaGraph P) :
    p + q ∈ tomitaGraph P := by
  obtain ⟨A, hA, rfl⟩ := hp
  obtain ⟨B, hB, rfl⟩ := hq
  refine ⟨A + B, (theFactorObject P).add_mem hA hB, ?_⟩
  simp [star_add]

theorem tomita_graph_conj_smul (c : ℂ)
    {p : TowerHilbert P × TowerHilbert P} (hp : p ∈ tomitaGraph P) :
    (c • p.1, (starRingEnd ℂ c) • p.2) ∈ tomitaGraph P := by
  obtain ⟨A, hA, rfl⟩ := hp
  refine ⟨c • A, (theFactorObject P).smul_mem hA c, ?_⟩
  simp only [star_smul, smul_apply, starRingEnd_apply]

theorem tomita_graph_swap {p : TowerHilbert P × TowerHilbert P}
    (hp : p ∈ tomitaGraph P) : p.swap ∈ tomitaGraph P := by
  obtain ⟨A, hA, rfl⟩ := hp
  refine ⟨star A, star_mem hA, ?_⟩
  simp

theorem closed_graph_add {p q : TowerHilbert P × TowerHilbert P}
    (hp : p ∈ closure (tomitaGraph P)) (hq : q ∈ closure (tomitaGraph P)) :
    p + q ∈ closure (tomitaGraph P) := by
  have hleft : ∀ a ∈ tomitaGraph P, ∀ b ∈ closure (tomitaGraph P),
      a + b ∈ closure (tomitaGraph P) := by
    intro a ha
    exact closure_minimal (fun b hb => subset_closure (tomita_graph_add ha hb))
      (isClosed_closure.preimage (continuous_const.add continuous_id))
  exact closure_minimal (fun a ha => hleft a ha q hq)
    (isClosed_closure.preimage (continuous_id.add continuous_const)) hp

theorem closed_graph_conj_smul (c : ℂ)
    {p : TowerHilbert P × TowerHilbert P}
    (hp : p ∈ closure (tomitaGraph P)) :
    (c • p.1, (starRingEnd ℂ c) • p.2) ∈ closure (tomitaGraph P) := by
  apply closure_minimal (t := {p : TowerHilbert P × TowerHilbert P |
    (c • p.1, (starRingEnd ℂ c) • p.2) ∈ closure (tomitaGraph P)}) ?_ ?_ hp
  · intro p hp
    exact subset_closure (tomita_graph_conj_smul c hp)
  · apply isClosed_closure.preimage
    fun_prop

theorem closed_graph_swap {p : TowerHilbert P × TowerHilbert P}
    (hp : p ∈ closure (tomitaGraph P)) : p.swap ∈ closure (tomitaGraph P) := by
  apply closure_minimal (t := {p : TowerHilbert P × TowerHilbert P |
    p.swap ∈ closure (tomitaGraph P)}) ?_ ?_ hp
  · intro p hp
    exact subset_closure (tomita_graph_swap hp)
  · exact isClosed_closure.preimage continuous_swap

/-- Domínio efetivo do fecho, como subespaço complexo, não todo H por decreto. -/
def closedTomitaDomain (P : SiteProfile) : Submodule ℂ (TowerHilbert P) where
  carrier := {x | ∃ y, (x, y) ∈ closure (tomitaGraph P)}
  zero_mem' := ⟨0, subset_closure tomita_graph_zero⟩
  add_mem' := by
    rintro x z ⟨y, hy⟩ ⟨w, hw⟩
    exact ⟨y + w, closed_graph_add hy hw⟩
  smul_mem' := by
    rintro c x ⟨y, hy⟩
    exact ⟨(starRingEnd ℂ c) • y, closed_graph_conj_smul c hy⟩

def closedTomitaValue (x : closedTomitaDomain P) : TowerHilbert P :=
  Classical.choose x.property

theorem closedTomitaValue_graph (x : closedTomitaDomain P) :
    ((x : TowerHilbert P), closedTomitaValue x) ∈ closure (tomitaGraph P) :=
  Classical.choose_spec x.property

/-- Operador fechado antilinear, com domínio próprio e escolha unívoca. -/
def closedTomita (P : SiteProfile) :
    closedTomitaDomain P →ₛₗ[starRingEnd ℂ] TowerHilbert P where
  toFun := closedTomitaValue
  map_add' x z := by
    apply tomita_graph_closure_single_valued
      ((x + z : closedTomitaDomain P) : TowerHilbert P)
    · exact closedTomitaValue_graph (x + z)
    · exact closed_graph_add (closedTomitaValue_graph x) (closedTomitaValue_graph z)
  map_smul' c x := by
    apply tomita_graph_closure_single_valued
      ((c • x : closedTomitaDomain P) : TowerHilbert P)
    · exact closedTomitaValue_graph (c • x)
    · exact closed_graph_conj_smul c (closedTomitaValue_graph x)

theorem closedTomita_graph (x : closedTomitaDomain P) :
    ((x : TowerHilbert P), closedTomita P x) ∈ closure (tomitaGraph P) :=
  closedTomitaValue_graph x

theorem closedTomita_graph_eq :
    Set.range (fun x : closedTomitaDomain P => ((x : TowerHilbert P), closedTomita P x))
      = closure (tomitaGraph P) := by
  ext p
  constructor
  · rintro ⟨x, rfl⟩
    exact closedTomita_graph x
  · intro hp
    let x : closedTomitaDomain P := ⟨p.1, p.2, hp⟩
    refine ⟨x, ?_⟩
    apply Prod.ext
    · rfl
    · exact tomita_graph_closure_single_valued p.1 _ p.2 (closedTomita_graph x) hp

theorem closedTomita_is_closed :
    IsClosed (Set.range (fun x : closedTomitaDomain P =>
      ((x : TowerHilbert P), closedTomita P x))) := by
  rw [closedTomita_graph_eq]
  exact isClosed_closure

theorem closedTomita_domain_dense : Dense (closedTomitaDomain P : Set (TowerHilbert P)) := by
  apply Dense.mono ?_ (tomita_graph_domain_dense (P := P))
  rintro x ⟨p, hp, rfl⟩
  exact ⟨p.2, subset_closure hp⟩

theorem closedTomita_maps_domain (x : closedTomitaDomain P) :
    closedTomita P x ∈ closedTomitaDomain P :=
  ⟨(x : TowerHilbert P), closed_graph_swap (closedTomita_graph x)⟩

theorem closedTomita_involutive (x : closedTomitaDomain P) :
    closedTomita P ⟨closedTomita P x, closedTomita_maps_domain x⟩ = x := by
  exact tomita_graph_closure_single_valued (closedTomita P x) _ _
    (closedTomita_graph ⟨closedTomita P x, closedTomita_maps_domain x⟩)
    (closed_graph_swap (closedTomita_graph x))

theorem factor_vector_mem_closedTomitaDomain
    {A : TowerHilbert P →L[ℂ] TowerHilbert P} (hA : A ∈ theFactorObject P) :
    A (hOmega P) ∈ closedTomitaDomain P :=
  ⟨(star A) (hOmega P), subset_closure ⟨A, hA, rfl⟩⟩

theorem closedTomita_extends_adjoint
    {A : TowerHilbert P →L[ℂ] TowerHilbert P} (hA : A ∈ theFactorObject P) :
    closedTomita P ⟨A (hOmega P), factor_vector_mem_closedTomitaDomain hA⟩ =
      (star A) (hOmega P) := by
  exact tomita_graph_closure_single_valued (A (hOmega P)) _ _
    (closedTomita_graph ⟨A (hOmega P), factor_vector_mem_closedTomitaDomain hA⟩)
    (subset_closure ⟨A, hA, rfl⟩)

#print axioms closedTomita
#print axioms closedTomita_is_closed
#print axioms closedTomita_domain_dense
#print axioms closedTomita_involutive
#print axioms closedTomita_extends_adjoint

end
end ChatgptAudit
