-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_031 (06/09/2026), transposta em 06/09/2026
-- Lote 031..032: o OPERADOR MODULAR RELATIVO com dominio e fecho — S^0_{psi|omega}(A Omega) = A* Psi,
--   grafico relativo fechado por homeomorfismo dos graficos algebricos, dominio denso, adjunto antilinear
--   maximal, congruencia limitada (auto-adjunta, positiva) e Delta_rel = S*S com dominio, fecho,
--   auto-adjunticidade e positividade; e a COMUTACAO MODULAR: separacao de frequencias reais, reconhecimento
--   do grafico de Delta por testes fracos, B limitado auto-adjunto comutando com o fluxo preserva o dominio
--   de Delta e comuta; o filtro e o inverso preservam o dominio; IGUALDADE dos dominios de Delta relativo e
--   de referencia e igualdade dos operadores parciais (Delta_rel = produto de verossimilhanca x Delta_omega
--   como LinearPMap), positivo, auto-adjunto, fechado. Estatuto [REAL / INPUT / OPEN]: familia comutante
--   especificada (referencia 1/3,2/3; b somavel); calculo funcional/potencias relativas, identificacao
--   Connes/Araki completa, area geometrica e reconstrucao geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 12/12 + 12/12; manifestos 254/259; 2/2
--   auditores exit 0; recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao estatica no ROOT;
--   enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.UnitaryPartialTransport

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace ChatgptAudit.Relative031
open Filter Topology Set ChatgptAudit.Transport027
noncomputable section
variable {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

def boundedCongruenceDomain (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E) : Submodule ℂ E :=
  T.domain.comap e.toLinearMap

def boundedCongruenceInput (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E) :
    boundedCongruenceDomain e T →ₗ[ℂ] T.domain where
  toFun x := ⟨e (x : E),x.property⟩
  map_add' x y := Subtype.ext (e.map_add (x : E) (y : E))
  map_smul' c x := Subtype.ext (e.map_smul c (x : E))

def boundedCongruence (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E) : E →ₗ.[ℂ] E where
  domain := boundedCongruenceDomain e T
  toFun := e.toLinearMap.comp (T.toFun.comp (boundedCongruenceInput e T))

theorem bounded_congruence_domain_iff (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E) (x : E) :
    x∈(boundedCongruence e T).domain ↔ e x∈T.domain := Iff.rfl

theorem bounded_congruence_apply (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E)
    (x : (boundedCongruence e T).domain) :
    boundedCongruence e T x=e (T (boundedCongruenceInput e T x)) := rfl

theorem bounded_congruence_input_coe (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E)
    (x : (boundedCongruence e T).domain) :
    (boundedCongruenceInput e T x : E)=e (x : E) := rfl

def boundedCongruenceLift (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E) (x : T.domain) :
    (boundedCongruence e T).domain :=
  ⟨e.symm (x : E),by
    change e (e.symm (x : E))∈T.domain
    rw [e.apply_symm_apply]
    exact x.property⟩

theorem bounded_congruence_lift_coe (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E) (x : T.domain) :
    (boundedCongruenceLift e T x : E)=e.symm (x : E) := rfl

theorem bounded_congruence_input_lift (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E) (x : T.domain) :
    boundedCongruenceInput e T (boundedCongruenceLift e T x)=x := by
  apply Subtype.ext
  exact e.apply_symm_apply (x : E)

theorem bounded_congruence_lift_apply (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E) (x : T.domain) :
    boundedCongruence e T (boundedCongruenceLift e T x)=e (T x) := by
  rw [bounded_congruence_apply,bounded_congruence_input_lift]

theorem bounded_congruence_graph_iff (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E) (x y : E) :
    (x,y)∈(boundedCongruence e T).graph ↔ (e x,e.symm y)∈T.graph := by
  rw [LinearPMap.mem_graph_iff,LinearPMap.mem_graph_iff]
  constructor
  · rintro ⟨z,hx,hy⟩
    refine ⟨boundedCongruenceInput e T z,?_,?_⟩
    · rw [bounded_congruence_input_coe,hx]
    · change T (boundedCongruenceInput e T z)=e.symm y
      exact (e.symm_apply_apply _).symm.trans (congrArg e.symm hy)
  · rintro ⟨z,hx,hy⟩
    refine ⟨boundedCongruenceLift e T z,?_,?_⟩
    · rw [bounded_congruence_lift_coe,hx,e.symm_apply_apply]
    · rw [bounded_congruence_lift_apply,hy,e.apply_symm_apply]

theorem bounded_congruence_domain_dense (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E)
    (hD : Dense (T.domain : Set E)) : Dense ((boundedCongruence e T).domain : Set E) := by
  have hl : (T.domain : Set E) ⊆ e.symm ⁻¹' closure ((boundedCongruence e T).domain : Set E) := by
    intro x hx
    apply subset_closure
    change e (e.symm x)∈T.domain
    rw [e.apply_symm_apply]
    exact hx
  have hc := closure_minimal hl (isClosed_closure.preimage e.symm.continuous)
  rw [hD.closure_eq] at hc
  intro x
  have hh := hc (mem_univ (e x))
  simpa only [mem_preimage,e.symm_apply_apply] using hh

theorem bounded_congruence_closed (e : E ≃L[ℂ] E) (T : E →ₗ.[ℂ] E)
    (hT : T.IsClosed) : (boundedCongruence e T).IsClosed := by
  have hg : ((boundedCongruence e T).graph : Set (E×E))=
      (fun p : E×E => (e p.1,e.symm p.2)) ⁻¹' (T.graph : Set (E×E)) := by
    ext p
    exact bounded_congruence_graph_iff e T p.1 p.2
  change IsClosed ((boundedCongruence e T).graph : Set (E×E))
  rw [hg]
  exact hT.preimage ((e.continuous.comp continuous_fst).prodMk
    (e.symm.continuous.comp continuous_snd))

variable [CompleteSpace E]

theorem bounded_equiv_inner (e : E ≃L[ℂ] E)
    (he : IsSelfAdjoint e.toContinuousLinearMap) (x y : E) :
    inner ℂ (e x) y=inner ℂ x (e y) := by
  have hs : ContinuousLinearMap.adjoint e.toContinuousLinearMap=e.toContinuousLinearMap :=
    he.star_eq
  change inner ℂ (e.toContinuousLinearMap x) y=
    inner ℂ x (e.toContinuousLinearMap y)
  rw [←ContinuousLinearMap.adjoint_inner_right,hs]

theorem bounded_congruence_formal_adjoint (e : E ≃L[ℂ] E)
    (he : IsSelfAdjoint e.toContinuousLinearMap) (T R : E →ₗ.[ℂ] E)
    (hTR : T.IsFormalAdjoint R) :
    (boundedCongruence e T).IsFormalAdjoint (boundedCongruence e R) := by
  intro x y
  change inner ℂ (e (T (boundedCongruenceInput e T x))) (y : E)=
    inner ℂ (x : E) (e (R (boundedCongruenceInput e R y)))
  calc
    _=inner ℂ (T (boundedCongruenceInput e T x)) (e (y : E)) :=
      bounded_equiv_inner e he _ _
    _=inner ℂ (e (x : E)) (R (boundedCongruenceInput e R y)) :=
      hTR (boundedCongruenceInput e T x) (boundedCongruenceInput e R y)
    _=_ := bounded_equiv_inner e he _ _

theorem bounded_congruence_selfadjoint (e : E ≃L[ℂ] E)
    (he : IsSelfAdjoint e.toContinuousLinearMap)
    (hi : IsSelfAdjoint e.symm.toContinuousLinearMap)
    (T : E →ₗ.[ℂ] E) (hD : Dense (T.domain : Set E)) (hT : IsSelfAdjoint T) :
    IsSelfAdjoint (boundedCongruence e T) := by
  have hd := bounded_congruence_domain_dense e T hD
  have hs : T.IsFormalAdjoint T := by
    simpa only [LinearPMap.isSelfAdjoint_def.mp hT] using
      (LinearPMap.adjoint_isFormalAdjoint (T := T) hD)
  have hs' := bounded_congruence_formal_adjoint e he T T hs
  have ha : LinearPMap.adjoint (boundedCongruence e T)≤boundedCongruence e T := by
    apply LinearPMap.le_of_le_graph
    rintro ⟨x,y⟩ hp
    rw [LinearPMap.mem_graph_iff] at hp
    obtain ⟨u,hu,hv⟩ := hp
    apply (bounded_congruence_graph_iff e T x y).mpr
    apply selfadjoint_weak_graph T hD hT
    intro z
    have hh := LinearPMap.adjoint_isFormalAdjoint (T := boundedCongruence e T) hd u
      (boundedCongruenceLift e T z)
    have hh' : inner ℂ y (e.symm (z : E))=inner ℂ x (e (T z)) := by
      simpa only [bounded_congruence_lift_coe,bounded_congruence_lift_apply,hu,hv] using hh
    calc
      inner ℂ (e.symm y) (z : E)=inner ℂ y (e.symm (z : E)) :=
        bounded_equiv_inner e.symm hi y (z : E)
      _=inner ℂ x (e (T z)) := hh'
      _=inner ℂ (e x) (T z) := (bounded_equiv_inner e he x (T z)).symm
  rw [LinearPMap.isSelfAdjoint_def]
  exact le_antisymm ha (hs'.le_adjoint hd)

theorem bounded_congruence_quadratic (e : E ≃L[ℂ] E)
    (he : IsSelfAdjoint e.toContinuousLinearMap) (T : E →ₗ.[ℂ] E)
    (x : (boundedCongruence e T).domain) :
    inner ℂ (x : E) (boundedCongruence e T x)=
      inner ℂ (boundedCongruenceInput e T x : E) (T (boundedCongruenceInput e T x)) :=
  (bounded_equiv_inner e he (x : E) (T (boundedCongruenceInput e T x))).symm

theorem bounded_congruence_positive (e : E ≃L[ℂ] E)
    (he : IsSelfAdjoint e.toContinuousLinearMap) (T : E →ₗ.[ℂ] E)
    (hT : ∀ z : T.domain, 0≤(inner ℂ (z : E) (T z)).re)
    (x : (boundedCongruence e T).domain) :
    0≤(inner ℂ (x : E) (boundedCongruence e T x)).re := by
  rw [bounded_congruence_quadratic e he T x]
  exact hT (boundedCongruenceInput e T x)

#print axioms boundedCongruenceDomain
#print axioms boundedCongruenceInput
#print axioms boundedCongruence
#print axioms bounded_congruence_domain_iff
#print axioms bounded_congruence_apply
#print axioms bounded_congruence_input_coe
#print axioms boundedCongruenceLift
#print axioms bounded_congruence_lift_coe
#print axioms bounded_congruence_input_lift
#print axioms bounded_congruence_lift_apply
#print axioms bounded_congruence_graph_iff
#print axioms bounded_congruence_domain_dense
#print axioms bounded_congruence_closed
#print axioms bounded_equiv_inner
#print axioms bounded_congruence_formal_adjoint
#print axioms bounded_congruence_selfadjoint
#print axioms bounded_congruence_quadratic
#print axioms bounded_congruence_positive

end
end ChatgptAudit.Relative031
