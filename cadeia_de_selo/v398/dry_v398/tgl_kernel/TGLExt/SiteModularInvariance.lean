-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_006 (05/09/2026), transposta em 05/09/2026
-- A ESPERANCA DO CENTRALIZADOR: habitante LOCAL (pinching espectral de cada
--   andar entra no centralizador GLOBAL de omega; into/fixes/ortho; unico) e
--   habitante TRACIAL do contrato original (w=1/2: M_omega = M, E = id);
--   invariancia de sitios sob sigma_t para TODO t (caudas nunca comprimem
--   estritamente); ponte: todo habitante global RESTRINGE-SE ao pinching.
-- Auditoria da gerencia (sessao d554e796): hashes 14/14 + manifesto 408/408;
--   recompilacao independente 5/5 exit 0; 34/34 no trio
--   [propext, Classical.choice, Quot.sound]; zero sorry/warning.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports da
--   bancada; nada mais. Namespace ChatgptAudit = procedencia.
-- [OPEN] declarados pela bancada: habitante global NAO tracial (parede exata:
--   operador medio do periodo + comutacao da media com E_N); nao-ciclicidade
--   da cauda em Lean; translacao de energia positiva nao trivial.
-- NAO move gate; nao e fisica. NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.ChainSiteFlow
import TGLExt.ChainTailClosure

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

theorem modularConjugation_inverse_time (t : ℝ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    modularConjugation P (-t) (modularConjugation P t x) = x := by
  ext v
  change modularFlow P (-t) (modularFlow P t
    (x (modularFlow P (-t) (modularFlow P (-(-t)) v)))) = x v
  rw [modularFlow_group,neg_add_cancel,modularFlow_zero_time,
    modularFlow_group,add_neg_cancel,modularFlow_zero_time]

theorem chain_flow_into (t : ℝ) (I : Set ℕ)
    {x : TowerHilbert P →L[ℂ] TowerHilbert P} (hx : x ∈ chainLocalAlgebra P I) :
    modularConjugation P t x ∈ chainLocalAlgebra P I := by
  have h : chainLocalAlgebra P I ≤
      (chainLocalAlgebra P I).comap (StarAlgHomClass.toStarAlgHom (modularConjugation P t)) := by
    apply StarAlgebra.adjoin_le
    rintro a ⟨n,hn,b,rfl⟩
    change modularConjugation P t (siteOperator P n b) ∈ chainLocalAlgebra P I
    rw [modularConjugation_site]
    exact StarAlgebra.subset_adjoin ℂ (chainGenerators P I) ⟨n,hn,_,rfl⟩
  exact h hx

theorem chain_flow_iff (t : ℝ) (I : Set ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    x ∈ chainLocalAlgebra P I ↔ modularConjugation P t x ∈ chainLocalAlgebra P I := by
  constructor
  · exact chain_flow_into t I
  · intro hx
    have h := chain_flow_into (-t) I hx
    rwa [modularConjugation_inverse_time] at h

theorem chain_flow_image (t : ℝ) (I : Set ℕ) :
    modularConjugation P t '' (chainLocalAlgebra P I : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) =
    (chainLocalAlgebra P I : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := by
  ext x
  constructor
  · rintro ⟨a,ha,rfl⟩
    exact chain_flow_into t I ha
  · intro hx
    refine ⟨(modularConjugation P t).symm x,?_,(modularConjugation P t).apply_symm_apply x⟩
    exact (chain_flow_iff t I _).mpr (by simpa using hx)

theorem tail_flow_iff (t : ℝ) (N : ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    x ∈ chainTailClosure P N ↔ modularConjugation P t x ∈ chainTailClosure P N := by
  exact centralizer_transport (modularConjugation P t) _
    (centralizer_transport (modularConjugation P t) _ (chain_flow_iff t (Set.Ici N))) x

theorem tail_flow_image (t : ℝ) (N : ℕ) :
    modularConjugation P t '' (chainTailClosure P N : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) =
    (chainTailClosure P N : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := by
  ext x
  constructor
  · rintro ⟨a,ha,rfl⟩
    exact (tail_flow_iff t N a).mp ha
  · intro hx
    refine ⟨(modularConjugation P t).symm x,?_,(modularConjugation P t).apply_symm_apply x⟩
    exact (tail_flow_iff t N _).mpr (by simpa using hx)

theorem invariant_is_not_strict {X : Type*} (f : X → X) (s : Set X)
    (h : f '' s = s) : ¬ f '' s ⊂ s := by
  rw [h]
  exact lt_irrefl s

theorem tail_never_strict (t : ℝ) (N : ℕ) :
    ¬ modularConjugation P t '' (chainTailClosure P N : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) ⊂
      (chainTailClosure P N : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :=
  invariant_is_not_strict _ _ (tail_flow_image t N)

#print axioms modularConjugation_inverse_time
#print axioms chain_flow_into
#print axioms chain_flow_iff
#print axioms chain_flow_image
#print axioms tail_flow_iff
#print axioms tail_flow_image
#print axioms invariant_is_not_strict
#print axioms tail_never_strict
end
end ChatgptAudit
