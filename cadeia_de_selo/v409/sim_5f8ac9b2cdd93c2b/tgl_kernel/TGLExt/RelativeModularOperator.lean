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
import TGLExt.RelativeTomitaClosure
import TGLExt.BoundedPositiveCongruence
import TGLExt.TomitaAdjoint

set_option autoImplicit false
set_option maxHeartbeats 300000
namespace ChatgptAudit.Relative031
open Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Cocycle030
  ChatgptAudit.Response028 ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

def relativeTomitaLift (b : SummableAmplitude) (t : ℝ)
    (x : closedTomitaDomain thirdThermalReference) : relativeTomitaDomain b t :=
  boundedCongruenceLift (likelihoodFilterEquiv b t) (closedModulatorCandidate thirdThermalReference) x

theorem relative_tomita_input_lift (b : SummableAmplitude) (t : ℝ)
    (x : closedTomitaDomain thirdThermalReference) :
    relativeTomitaInput b t (relativeTomitaLift b t x)=x :=
  bounded_congruence_input_lift (likelihoodFilterEquiv b t)
    (closedModulatorCandidate thirdThermalReference) x

theorem relative_tomita_lift_apply (b : SummableAmplitude) (t : ℝ)
    (x : closedTomitaDomain thirdThermalReference) :
    relativeTomita b t (relativeTomitaLift b t x)=closedTomita thirdThermalReference x := by
  rw [relative_tomita_apply,relative_tomita_input_lift]

def relativeTomitaAdjoint (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference →ₛₗ.[starRingEnd ℂ] TowerHilbert thirdThermalReference where
  domain := tomitaAdjointDomain thirdThermalReference
  toFun := (likelihoodFilter b t).toLinearMap.comp (closedTomitaAdjoint thirdThermalReference).toFun

theorem relative_tomita_adjoint_apply (b : SummableAmplitude) (t : ℝ)
    (y : tomitaAdjointDomain thirdThermalReference) :
    relativeTomitaAdjoint b t y=likelihoodFilter b t (closedTomitaAdjoint thirdThermalReference y) := rfl

theorem relative_tomita_adjoint_pairing (b : SummableAmplitude) (t : ℝ)
    (x : relativeTomitaDomain b t) (y : tomitaAdjointDomain thirdThermalReference) :
    inner ℂ (relativeTomita b t x) (y : TowerHilbert thirdThermalReference)=
      inner ℂ (relativeTomitaAdjoint b t y) (x : TowerHilbert thirdThermalReference) := by
  rw [relative_tomita_apply,tomita_adjoint_pairing]
  exact (bounded_equiv_inner (likelihoodFilterEquiv b t)
    (likelihood_filter_selfadjoint b t) _ _).symm

theorem relative_tomita_adjoint_maximal (b : SummableAmplitude) (t : ℝ)
    {y w : TowerHilbert thirdThermalReference}
    (h : ∀ x : relativeTomitaDomain b t,
      inner ℂ (relativeTomita b t x) y=inner ℂ w (x : TowerHilbert thirdThermalReference)) :
    ∃ hy : y∈(relativeTomitaAdjoint b t).domain, relativeTomitaAdjoint b t ⟨y,hy⟩=w := by
  have hh : ∀ z : closedTomitaDomain thirdThermalReference,
      inner ℂ (closedTomita thirdThermalReference z) y=
        inner ℂ (inverseLikelihoodFilter b t w) (z : TowerHilbert thirdThermalReference) := by
    intro z
    calc
      _=inner ℂ (relativeTomita b t (relativeTomitaLift b t z)) y := by
        rw [relative_tomita_lift_apply]
      _=inner ℂ w ((likelihoodFilterEquiv b t).symm (z : TowerHilbert thirdThermalReference)) :=
        h (relativeTomitaLift b t z)
      _=_ := (bounded_equiv_inner (likelihoodFilterEquiv b t).symm
        (inverse_filter_selfadjoint b t) _ _).symm
  obtain ⟨hy,hz⟩ := tomita_adjoint_maximal hh
  refine ⟨hy,?_⟩
  exact (congrArg (likelihoodFilter b t) hz).trans
    ((likelihoodFilterEquiv b t).apply_symm_apply w)

theorem relative_tomita_adjoint_domain_iff (b : SummableAmplitude) (t : ℝ)
    (y : TowerHilbert thirdThermalReference) :
    y∈(relativeTomitaAdjoint b t).domain ↔
      ∃ w : TowerHilbert thirdThermalReference, ∀ x : relativeTomitaDomain b t,
        inner ℂ (relativeTomita b t x) y=inner ℂ w (x : TowerHilbert thirdThermalReference) := by
  constructor
  · intro hy
    exact ⟨relativeTomitaAdjoint b t ⟨y,hy⟩,fun x => relative_tomita_adjoint_pairing b t x ⟨y,hy⟩⟩
  · rintro ⟨w,hw⟩
    exact (relative_tomita_adjoint_maximal b t hw).choose

def relativeDelta (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference →ₗ.[ℂ] TowerHilbert thirdThermalReference :=
  boundedCongruence (likelihoodFilterEquiv b t) (towerDeltaClosed thirdThermalReference)

theorem relative_delta_domain_iff (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    x∈(relativeDelta b t).domain ↔ likelihoodFilter b t x∈modularSquareDomain thirdThermalReference := Iff.rfl

theorem relative_delta_apply (b : SummableAmplitude) (t : ℝ)
    (x : (relativeDelta b t).domain) :
    relativeDelta b t x=likelihoodFilter b t
      (towerDeltaClosed thirdThermalReference
        (boundedCongruenceInput (likelihoodFilterEquiv b t) (towerDeltaClosed thirdThermalReference) x)) := rfl

theorem relative_delta_domain_dense (b : SummableAmplitude) (t : ℝ) :
    Dense ((relativeDelta b t).domain : Set (TowerHilbert thirdThermalReference)) :=
  bounded_congruence_domain_dense _ _ squareDomain_dense

theorem relative_delta_closed (b : SummableAmplitude) (t : ℝ) :
    (relativeDelta b t).IsClosed :=
  bounded_congruence_closed _ _ delta_closed

theorem relative_delta_selfadjoint (b : SummableAmplitude) (t : ℝ) :
    IsSelfAdjoint (relativeDelta b t) :=
  bounded_congruence_selfadjoint (likelihoodFilterEquiv b t) (likelihood_filter_selfadjoint b t)
    (inverse_filter_selfadjoint b t) (towerDeltaClosed thirdThermalReference)
    (squareDomain_dense (P := thirdThermalReference)) (delta_selfadjoint (P := thirdThermalReference))

theorem relative_delta_positive (b : SummableAmplitude) (t : ℝ)
    (x : (relativeDelta b t).domain) :
    0≤(inner ℂ (x : TowerHilbert thirdThermalReference) (relativeDelta b t x)).re :=
  bounded_congruence_positive (likelihoodFilterEquiv b t) (likelihood_filter_selfadjoint b t)
    (towerDeltaClosed thirdThermalReference) delta_positive x

theorem relative_composition_domain (b : SummableAmplitude) (t : ℝ)
    (x : relativeTomitaDomain b t) :
    relativeTomita b t x∈(relativeTomitaAdjoint b t).domain ↔
      (x : TowerHilbert thirdThermalReference)∈(relativeDelta b t).domain := by
  change closedTomita thirdThermalReference (relativeTomitaInput b t x)∈
    tomitaAdjointDomain thirdThermalReference ↔ _
  rw [tomita_composition_domain,relative_delta_domain_iff,squareDomain_iff]
  constructor
  · intro hx
    exact ⟨(relativeTomitaInput b t x).property,hx⟩
  · rintro ⟨_,hx⟩
    exact hx

theorem relative_delta_domain_le (b : SummableAmplitude) (t : ℝ) :
    (relativeDelta b t).domain≤relativeTomitaDomain b t := by
  intro x hx
  exact squareDomain_le hx

def relativeDeltaTomitaInput (b : SummableAmplitude) (t : ℝ) :
    (relativeDelta b t).domain →ₗ[ℂ] relativeTomitaDomain b t :=
  Submodule.inclusion (relative_delta_domain_le b t)

theorem relative_delta_tomita_mem_adjoint (b : SummableAmplitude) (t : ℝ)
    (x : (relativeDelta b t).domain) :
    relativeTomita b t (relativeDeltaTomitaInput b t x)∈(relativeTomitaAdjoint b t).domain :=
  (relative_composition_domain b t (relativeDeltaTomitaInput b t x)).mpr x.property

theorem relative_tomita_adjoint_comp_is_delta (b : SummableAmplitude) (t : ℝ)
    (x : (relativeDelta b t).domain) :
    relativeTomitaAdjoint b t
      ⟨relativeTomita b t (relativeDeltaTomitaInput b t x),relative_delta_tomita_mem_adjoint b t x⟩=
        relativeDelta b t x := by
  exact congrArg (likelihoodFilter b t)
    (tomita_adjoint_comp_is_delta
      (boundedCongruenceInput (likelihoodFilterEquiv b t) (towerDeltaClosed thirdThermalReference) x))

theorem relative_delta_quadratic_is_tomita_norm (b : SummableAmplitude) (t : ℝ)
    (x : (relativeDelta b t).domain) :
    (inner ℂ (x : TowerHilbert thirdThermalReference) (relativeDelta b t x)).re=
      ‖relativeTomita b t (relativeDeltaTomitaInput b t x)‖^2 := by
  exact (congrArg Complex.re (bounded_congruence_quadratic
    (likelihoodFilterEquiv b t) (likelihood_filter_selfadjoint b t)
    (towerDeltaClosed thirdThermalReference) x)).trans
      (delta_quadratic_is_tomita_norm
        (boundedCongruenceInput (likelihoodFilterEquiv b t) (towerDeltaClosed thirdThermalReference) x))

#print axioms relativeTomitaLift
#print axioms relative_tomita_input_lift
#print axioms relative_tomita_lift_apply
#print axioms relativeTomitaAdjoint
#print axioms relative_tomita_adjoint_apply
#print axioms relative_tomita_adjoint_pairing
#print axioms relative_tomita_adjoint_maximal
#print axioms relative_tomita_adjoint_domain_iff
#print axioms relativeDelta
#print axioms relative_delta_domain_iff
#print axioms relative_delta_apply
#print axioms relative_delta_domain_dense
#print axioms relative_delta_closed
#print axioms relative_delta_selfadjoint
#print axioms relative_delta_positive
#print axioms relative_composition_domain
#print axioms relative_delta_domain_le
#print axioms relativeDeltaTomitaInput
#print axioms relative_delta_tomita_mem_adjoint
#print axioms relative_tomita_adjoint_comp_is_delta
#print axioms relative_delta_quadratic_is_tomita_norm
end
end ChatgptAudit.Relative031
