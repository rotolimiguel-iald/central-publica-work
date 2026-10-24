-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_027 (06/09/2026), transposta em 06/09/2026
-- Lote 027..028: EQUIVALENCIA UNITARIA entre os GNS de perfis com afinidade positiva e o TRANSPORTE
--   MODULAR com dominios — Tomita do estado global Phi no Hilbert original (grafo fechado, S, J, Delta,
--   JS = Delta^{1/2} positivo auto-adjunto), grupo modular fortemente continuo que preserva fator e
--   estado, instancia nao trivial (perfil gradual: autovalor transportado 5/7); RESPOSTA GLOBAL finita
--   sem corte (familia de amplitude somavel, fiel), limite conjunto corte/tempo, contraexemplo
--   HARMONICO (entropia relativa finita com incremento modular e entropia DIVERGENTES);
--   einstein_from_summable_area_matching (condicional). Estatuto [REAL / INPUT / OPEN]: a lei de area
--   microscopica NAO foi derivada da torre (controle plano o impede); selecao fisica, H3 dinamico,
--   assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 20/20 + 20/20; manifestos 231/238;
--   2/2 auditores da bancada exit 0; recompilacao INDEPENDENTE 16/16, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ProfileFactorTransport
import Mathlib.Analysis.InnerProductSpace.LinearPMap

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Transport027
open Filter Topology Set
noncomputable section
variable {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]

def unitaryPartialDomain (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E) : Submodule ℂ F :=
  T.domain.comap e.symm.toLinearEquiv.toLinearMap

def unitaryPartialInput (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E) :
    unitaryPartialDomain e T →ₗ[ℂ] T.domain where
  toFun x := ⟨e.symm (x : F),x.property⟩
  map_add' x y := Subtype.ext (e.symm.map_add (x : F) (y : F))
  map_smul' c x := Subtype.ext (e.symm.map_smul c (x : F))

def unitaryPartial (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E) : F →ₗ.[ℂ] F where
  domain := unitaryPartialDomain e T
  toFun := e.toLinearEquiv.toLinearMap.comp (T.toFun.comp (unitaryPartialInput e T))

theorem unitary_partial_domain_iff (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E) (x : F) :
    x∈(unitaryPartial e T).domain ↔ e.symm x∈T.domain := Iff.rfl

theorem unitary_partial_apply (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E)
    (x : (unitaryPartial e T).domain) :
    unitaryPartial e T x=e (T (unitaryPartialInput e T x)) := rfl

theorem unitary_partial_input_coe (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E)
    (x : (unitaryPartial e T).domain) :
    (unitaryPartialInput e T x : E)=e.symm (x : F) := rfl

def unitaryPartialLift (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E) (x : T.domain) :
    (unitaryPartial e T).domain :=
  ⟨e (x : E),by
    change e.symm (e (x : E))∈T.domain
    rw [e.symm_apply_apply]
    exact x.property⟩

theorem unitary_partial_lift_coe (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E) (x : T.domain) :
    (unitaryPartialLift e T x : F)=e (x : E) := rfl

theorem unitary_partial_input_lift (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E) (x : T.domain) :
    unitaryPartialInput e T (unitaryPartialLift e T x)=x := by
  apply Subtype.ext
  exact e.symm_apply_apply (x : E)

theorem unitary_partial_lift_apply (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E) (x : T.domain) :
    unitaryPartial e T (unitaryPartialLift e T x)=e (T x) := by
  rw [unitary_partial_apply,unitary_partial_input_lift]

theorem unitary_partial_graph_iff (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E) (x y : F) :
    (x,y)∈(unitaryPartial e T).graph ↔ (e.symm x,e.symm y)∈T.graph := by
  rw [LinearPMap.mem_graph_iff,LinearPMap.mem_graph_iff]
  constructor
  · rintro ⟨z,hx,hy⟩
    refine ⟨unitaryPartialInput e T z,?_,?_⟩
    · rw [unitary_partial_input_coe,hx]
    · change T (unitaryPartialInput e T z)=e.symm y
      exact (e.symm_apply_apply _).symm.trans (congrArg e.symm hy)
  · rintro ⟨z,hx,hy⟩
    refine ⟨unitaryPartialLift e T z,?_,?_⟩
    · rw [unitary_partial_lift_coe,hx,e.apply_symm_apply]
    · rw [unitary_partial_lift_apply,hy,e.apply_symm_apply]

theorem unitary_partial_domain_dense (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E)
    (hD : Dense (T.domain : Set E)) : Dense ((unitaryPartial e T).domain : Set F) := by
  have hl : (T.domain : Set E) ⊆ e ⁻¹' closure ((unitaryPartial e T).domain : Set F) := by
    intro x hx
    apply subset_closure
    change e.symm (e x)∈T.domain
    rw [e.symm_apply_apply]
    exact hx
  have hc := closure_minimal hl (isClosed_closure.preimage e.continuous)
  rw [hD.closure_eq] at hc
  intro x
  have hh := hc (mem_univ (e.symm x))
  simpa only [mem_preimage,e.apply_symm_apply] using hh

theorem unitary_partial_closed (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E)
    (hT : T.IsClosed) : (unitaryPartial e T).IsClosed := by
  have hg : ((unitaryPartial e T).graph : Set (F×F))=
      (fun p : F×F => (e.symm p.1,e.symm p.2)) ⁻¹' (T.graph : Set (E×E)) := by
    ext p
    exact unitary_partial_graph_iff e T p.1 p.2
  change IsClosed ((unitaryPartial e T).graph : Set (F×F))
  rw [hg]
  exact hT.preimage ((e.symm.continuous.comp continuous_fst).prodMk
    (e.symm.continuous.comp continuous_snd))

theorem unitary_partial_formal_adjoint (e : E ≃ₗᵢ[ℂ] F) (T R : E →ₗ.[ℂ] E)
    (hTR : T.IsFormalAdjoint R) :
    (unitaryPartial e T).IsFormalAdjoint (unitaryPartial e R) := by
  intro x y
  change inner ℂ (e (T (unitaryPartialInput e T x))) (y : F)=
    inner ℂ (x : F) (e (R (unitaryPartialInput e R y)))
  calc
    _=inner ℂ (T (unitaryPartialInput e T x)) (e.symm (y : F)) := by
      rw [←e.inner_map_map (T (unitaryPartialInput e T x)) (e.symm (y : F)),e.apply_symm_apply]
    _=inner ℂ (e.symm (x : F)) (R (unitaryPartialInput e R y)) :=
      hTR (unitaryPartialInput e T x) (unitaryPartialInput e R y)
    _=_ := by
      rw [←e.inner_map_map (e.symm (x : F)) (R (unitaryPartialInput e R y)),e.apply_symm_apply]

theorem selfadjoint_weak_graph [CompleteSpace E] (T : E →ₗ.[ℂ] E) (hD : Dense (T.domain : Set E))
    (hT : IsSelfAdjoint T) (x y : E)
    (hxy : ∀ z : T.domain, inner ℂ y (z : E)=inner ℂ x (T z)) : (x,y)∈T.graph := by
  have hx := LinearPMap.mem_adjoint_domain_of_exists (T := T) x ⟨y,hxy⟩
  have hv := LinearPMap.adjoint_apply_eq (T := T) hD ⟨x,hx⟩ hxy
  have hg : (x,y)∈(LinearPMap.adjoint T).graph := by
    rw [LinearPMap.mem_graph_iff]
    exact ⟨⟨x,hx⟩,rfl,hv⟩
  simpa only [LinearPMap.isSelfAdjoint_def.mp hT] using hg

theorem unitary_partial_selfadjoint [CompleteSpace E] [CompleteSpace F] (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E)
    (hD : Dense (T.domain : Set E)) (hT : IsSelfAdjoint T) :
    IsSelfAdjoint (unitaryPartial e T) := by
  have hd := unitary_partial_domain_dense e T hD
  have hs : T.IsFormalAdjoint T := by
    simpa only [LinearPMap.isSelfAdjoint_def.mp hT] using
      (LinearPMap.adjoint_isFormalAdjoint (T := T) hD)
  have hs' := unitary_partial_formal_adjoint e T T hs
  have ha : LinearPMap.adjoint (unitaryPartial e T)≤unitaryPartial e T := by
    apply LinearPMap.le_of_le_graph
    rintro ⟨x,y⟩ hp
    rw [LinearPMap.mem_graph_iff] at hp
    obtain ⟨u,hu,hv⟩ := hp
    apply (unitary_partial_graph_iff e T x y).mpr
    apply selfadjoint_weak_graph T hD hT
    intro z
    have hh := LinearPMap.adjoint_isFormalAdjoint (T := unitaryPartial e T) hd u
      (unitaryPartialLift e T z)
    have hh' : inner ℂ y (e (z : E))=inner ℂ x (e (T z)) := by
      simpa only [unitary_partial_lift_coe,unitary_partial_lift_apply,hu,hv] using hh
    rw [←e.inner_map_map (e.symm y) (z : E),←e.inner_map_map (e.symm x) (T z)]
    simpa only [e.apply_symm_apply] using hh'
  rw [LinearPMap.isSelfAdjoint_def]
  exact le_antisymm ha (hs'.le_adjoint hd)

theorem unitary_partial_positive (e : E ≃ₗᵢ[ℂ] F) (T : E →ₗ.[ℂ] E)
    (hT : ∀ z : T.domain, 0≤(inner ℂ (z : E) (T z)).re)
    (x : (unitaryPartial e T).domain) :
    0≤(inner ℂ (x : F) (unitaryPartial e T x)).re := by
  have hx : (x : F)=e (unitaryPartialInput e T x : E) := (e.apply_symm_apply (x : F)).symm
  change 0≤(inner ℂ (x : F) (e (T (unitaryPartialInput e T x)))).re
  rw [hx,e.inner_map_map]
  exact hT (unitaryPartialInput e T x)

#print axioms unitaryPartial
#print axioms unitary_partial_domain_iff
#print axioms unitary_partial_apply
#print axioms unitary_partial_input_coe
#print axioms unitary_partial_lift_coe
#print axioms unitary_partial_input_lift
#print axioms unitary_partial_lift_apply
#print axioms unitary_partial_graph_iff
#print axioms unitary_partial_domain_dense
#print axioms unitary_partial_closed
#print axioms unitary_partial_formal_adjoint
#print axioms selfadjoint_weak_graph
#print axioms unitary_partial_selfadjoint
#print axioms unitary_partial_positive
end
end ChatgptAudit.Transport027
