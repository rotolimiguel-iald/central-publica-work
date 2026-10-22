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
import TGLExt.RelativeFilterInverse
import TGLExt.BoundedPositiveCongruence

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit.Relative031
open Matrix Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Cocycle030
  ChatgptAudit.Response028 ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

def relativePairHomeomorph (b : SummableAmplitude) (t : ℝ) :
    (TowerHilbert thirdThermalReference×TowerHilbert thirdThermalReference) ≃ₜ
      (TowerHilbert thirdThermalReference×TowerHilbert thirdThermalReference) :=
  (likelihoodFilterEquiv b t).symm.toHomeomorph.prodCongr (Homeomorph.refl _)

def relativeTomitaGraph (b : SummableAmplitude) (t : ℝ) :
    Set (TowerHilbert thirdThermalReference×TowerHilbert thirdThermalReference) :=
  {p | ∃ A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference,
    A∈theFactorObject thirdThermalReference ∧
      p=(A (hOmega thirdThermalReference),(star A) (amplitudeVector b t))}

theorem relative_tomita_graph_image (b : SummableAmplitude) (t : ℝ) :
    relativePairHomeomorph b t '' tomitaGraph thirdThermalReference=relativeTomitaGraph b t := by
  ext p
  constructor
  · rintro ⟨q,⟨A,hA,rfl⟩,rfl⟩
    refine ⟨inverseLikelihoodFilter b t*A,
      (theFactorObject thirdThermalReference).mul_mem (inverse_filter_mem_factor b t) hA,?_⟩
    change (inverseLikelihoodFilter b t (A (hOmega thirdThermalReference)),
      (star A) (hOmega thirdThermalReference))=_
    apply Prod.ext
    · rfl
    · change (star A) (hOmega thirdThermalReference)=
        (star (inverseLikelihoodFilter b t*A)) (amplitudeVector b t)
      rw [star_mul,(inverse_filter_selfadjoint b t).star_eq]
      change (star A) (hOmega thirdThermalReference)=
        (star A) (inverseLikelihoodFilter b t (amplitudeVector b t))
      rw [inverse_filter_vector]
  · rintro ⟨A,hA,rfl⟩
    refine ⟨((likelihoodFilter b t*A) (hOmega thirdThermalReference),
      (star (likelihoodFilter b t*A)) (hOmega thirdThermalReference)),
      ⟨likelihoodFilter b t*A,
        (theFactorObject thirdThermalReference).mul_mem (likelihood_filter_mem_factor b t) hA,rfl⟩,?_⟩
    change (inverseLikelihoodFilter b t ((likelihoodFilter b t*A) (hOmega thirdThermalReference)),
      (star (likelihoodFilter b t*A)) (hOmega thirdThermalReference))=_
    apply Prod.ext
    · change ((inverseLikelihoodFilter b t*likelihoodFilter b t)*A) (hOmega thirdThermalReference)=_
      rw [inverse_mul_filter,one_mul]
    · change (star (likelihoodFilter b t*A)) (hOmega thirdThermalReference)=
        (star A) (amplitudeVector b t)
      rw [star_mul,(likelihood_filter_selfadjoint b t).star_eq]
      change (star A) (likelihoodFilter b t (hOmega thirdThermalReference))=
        (star A) (amplitudeVector b t)
      rw [likelihood_filter_vector]

theorem relative_tomita_closed_graph_image (b : SummableAmplitude) (t : ℝ) :
    relativePairHomeomorph b t '' closure (tomitaGraph thirdThermalReference)=
      closure (relativeTomitaGraph b t) := by
  rw [(relativePairHomeomorph b t).image_closure,relative_tomita_graph_image]

theorem relative_tomita_closed_graph_iff (b : SummableAmplitude) (t : ℝ)
    (x y : TowerHilbert thirdThermalReference) :
    (x,y)∈closure (relativeTomitaGraph b t) ↔
      (likelihoodFilter b t x,y)∈closure (tomitaGraph thirdThermalReference) := by
  rw [←relative_tomita_closed_graph_image]
  change (x,y)∈relativePairHomeomorph b t '' closure (tomitaGraph thirdThermalReference) ↔
    (relativePairHomeomorph b t).symm (x,y)∈closure (tomitaGraph thirdThermalReference)
  constructor
  · rintro ⟨p,hp,hp'⟩
    rw [←hp',(relativePairHomeomorph b t).symm_apply_apply]
    exact hp
  · intro hp
    exact ⟨(relativePairHomeomorph b t).symm (x,y),hp,
      (relativePairHomeomorph b t).apply_symm_apply (x,y)⟩

def relativeTomitaDomain (b : SummableAmplitude) (t : ℝ) :
    Submodule ℂ (TowerHilbert thirdThermalReference) :=
  (closedTomitaDomain thirdThermalReference).comap (likelihoodFilter b t).toLinearMap

def relativeTomitaInput (b : SummableAmplitude) (t : ℝ) :
    relativeTomitaDomain b t →ₗ[ℂ] closedTomitaDomain thirdThermalReference where
  toFun x := ⟨likelihoodFilter b t (x : TowerHilbert thirdThermalReference),x.property⟩
  map_add' x y := Subtype.ext ((likelihoodFilter b t).map_add
    (x : TowerHilbert thirdThermalReference) (y : TowerHilbert thirdThermalReference))
  map_smul' c x := Subtype.ext ((likelihoodFilter b t).map_smul c (x : TowerHilbert thirdThermalReference))

def relativeTomita (b : SummableAmplitude) (t : ℝ) :
    relativeTomitaDomain b t →ₛₗ[starRingEnd ℂ] TowerHilbert thirdThermalReference :=
  (closedTomita thirdThermalReference).comp (relativeTomitaInput b t)

theorem relative_tomita_apply (b : SummableAmplitude) (t : ℝ)
    (x : relativeTomitaDomain b t) :
    relativeTomita b t x=closedTomita thirdThermalReference (relativeTomitaInput b t x) := rfl

theorem relative_tomita_graph (b : SummableAmplitude) (t : ℝ)
    (x : relativeTomitaDomain b t) :
    ((x : TowerHilbert thirdThermalReference),relativeTomita b t x)∈closure (relativeTomitaGraph b t) := by
  apply (relative_tomita_closed_graph_iff b t _ _).mpr
  exact closedTomita_graph (relativeTomitaInput b t x)

theorem relative_tomita_domain_iff (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    x∈relativeTomitaDomain b t ↔ ∃ y, (x,y)∈closure (relativeTomitaGraph b t) := by
  constructor
  · intro hx
    exact ⟨relativeTomita b t ⟨x,hx⟩,relative_tomita_graph b t ⟨x,hx⟩⟩
  · rintro ⟨y,hxy⟩
    exact ⟨y,(relative_tomita_closed_graph_iff b t x y).mp hxy⟩

theorem relative_tomita_single_valued (b : SummableAmplitude) (t : ℝ)
    (x y z : TowerHilbert thirdThermalReference)
    (hy : (x,y)∈closure (relativeTomitaGraph b t))
    (hz : (x,z)∈closure (relativeTomitaGraph b t)) : y=z :=
  tomita_graph_closure_single_valued _ _ _
    ((relative_tomita_closed_graph_iff b t x y).mp hy)
    ((relative_tomita_closed_graph_iff b t x z).mp hz)

theorem unique_graph_range {E F : Type} (D : Set E) (G : Set (E×F)) (f : D→F)
    (hd : ∀ x, x∈D ↔ ∃ y, (x,y)∈G)
    (hf : ∀ x : D, ((x : E),f x)∈G)
    (hu : ∀ x y z, (x,y)∈G → (x,z)∈G → y=z) :
    range (fun x : D => ((x : E),f x))=G := by
  apply Set.Subset.antisymm
  · rintro _ ⟨x,rfl⟩
    exact hf x
  · rintro ⟨x,y⟩ hxy
    have hx : x∈D := (hd x).mpr ⟨y,hxy⟩
    have heq : f ⟨x,hx⟩=y := hu x _ y (hf ⟨x,hx⟩) hxy
    exact ⟨⟨x,hx⟩,congrArg (fun z : F => (x,z)) heq⟩

theorem relative_tomita_closed_graph_eq (b : SummableAmplitude) (t : ℝ) :
    range (fun x : relativeTomitaDomain b t =>
      ((x : TowerHilbert thirdThermalReference),relativeTomita b t x))=
        closure (relativeTomitaGraph b t) :=
  unique_graph_range (relativeTomitaDomain b t) (closure (relativeTomitaGraph b t))
    (relativeTomita b t) (relative_tomita_domain_iff b t)
    (relative_tomita_graph b t) (relative_tomita_single_valued b t)

theorem relative_tomita_closed (b : SummableAmplitude) (t : ℝ) :
    IsClosed (range (fun x : relativeTomitaDomain b t =>
      ((x : TowerHilbert thirdThermalReference),relativeTomita b t x))) := by
  rw [relative_tomita_closed_graph_eq]
  exact isClosed_closure

theorem relative_tomita_domain_dense (b : SummableAmplitude) (t : ℝ) :
    Dense (relativeTomitaDomain b t : Set (TowerHilbert thirdThermalReference)) :=
  bounded_congruence_domain_dense (likelihoodFilterEquiv b t)
    (closedModulatorCandidate thirdThermalReference) closedTomita_domain_dense

theorem relative_factor_vector_mem (b : SummableAmplitude) (t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A∈theFactorObject thirdThermalReference) :
    A (hOmega thirdThermalReference)∈relativeTomitaDomain b t := by
  rw [relative_tomita_domain_iff]
  exact ⟨(star A) (amplitudeVector b t),subset_closure ⟨A,hA,rfl⟩⟩

theorem relative_tomita_extends_star (b : SummableAmplitude) (t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A∈theFactorObject thirdThermalReference) :
    relativeTomita b t ⟨A (hOmega thirdThermalReference),relative_factor_vector_mem b t A hA⟩=
      (star A) (amplitudeVector b t) :=
  relative_tomita_single_valued b t _ _ _
    (relative_tomita_graph b t ⟨_,relative_factor_vector_mem b t A hA⟩)
    (subset_closure ⟨A,hA,rfl⟩)

#print axioms relativeTomitaGraph
#print axioms relativeTomitaDomain
#print axioms relativeTomita
#print axioms relative_tomita_graph_image
#print axioms relative_tomita_closed_graph_image
#print axioms relative_tomita_closed_graph_iff
#print axioms relative_tomita_apply
#print axioms relative_tomita_graph
#print axioms relative_tomita_domain_iff
#print axioms relative_tomita_single_valued
#print axioms unique_graph_range
#print axioms relative_tomita_closed_graph_eq
#print axioms relative_tomita_closed
#print axioms relative_tomita_domain_dense
#print axioms relative_factor_vector_mem
#print axioms relative_tomita_extends_star
end
end ChatgptAudit.Relative031
