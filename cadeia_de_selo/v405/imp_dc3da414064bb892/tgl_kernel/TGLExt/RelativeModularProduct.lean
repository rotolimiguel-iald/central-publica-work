-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_032 (06/09/2026), transposta em 06/09/2026
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
import TGLExt.RelativeModularOperator
import TGLExt.ModularDomainCommutation

set_option autoImplicit false
set_option maxHeartbeats 400000
namespace ChatgptAudit.Commutation032
open Matrix Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Cocycle030
  ChatgptAudit.Relative031 ChatgptAudit.Response028 ChatgptAudit.Profile026
  ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

local instance (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _
local instance (P : SiteProfile) : IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

theorem inverse_filter_modular_fixed (b : SummableAmplitude) (t s : ℝ) :
    modularConjugation thirdThermalReference s (inverseLikelihoodFilter b t)=
      inverseLikelihoodFilter b t := by
  unfold inverseLikelihoodFilter
  rw [NormedSpace.map_exp (modularConjugation thirdThermalReference s)
    (modular_conjugation_continuous _ s),map_smul,likelihood_generator_modular_fixed]

theorem filter_flow_commutes (b : SummableAmplitude) (t s : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    modularFlow thirdThermalReference s (likelihoodFilter b t x)=
      likelihoodFilter b t (modularFlow thirdThermalReference s x) :=
  modular_fixed_commutes_with_flow thirdThermalReference (likelihoodFilter b t)
    (likelihood_filter_modular_fixed b t) s x

theorem inverse_filter_flow_commutes (b : SummableAmplitude) (t s : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    modularFlow thirdThermalReference s (inverseLikelihoodFilter b t x)=
      inverseLikelihoodFilter b t (modularFlow thirdThermalReference s x) :=
  modular_fixed_commutes_with_flow thirdThermalReference (inverseLikelihoodFilter b t)
    (inverse_filter_modular_fixed b t) s x

theorem filter_preserves_delta_domain (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) (hx : x∈modularSquareDomain thirdThermalReference) :
    likelihoodFilter b t x∈modularSquareDomain thirdThermalReference :=
  commuting_operator_preserves_delta_domain thirdThermalReference (likelihoodFilter b t)
    (likelihood_filter_selfadjoint b t) (filter_flow_commutes b t) x hx

theorem inverse_filter_preserves_delta_domain (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) (hx : x∈modularSquareDomain thirdThermalReference) :
    inverseLikelihoodFilter b t x∈modularSquareDomain thirdThermalReference :=
  commuting_operator_preserves_delta_domain thirdThermalReference (inverseLikelihoodFilter b t)
    (inverse_filter_selfadjoint b t) (inverse_filter_flow_commutes b t) x hx

theorem filter_delta_commutes (b : SummableAmplitude) (t : ℝ)
    (x : modularSquareDomain thirdThermalReference) :
    towerDeltaClosed thirdThermalReference
      ⟨likelihoodFilter b t (x : TowerHilbert thirdThermalReference),
        filter_preserves_delta_domain b t (x : TowerHilbert thirdThermalReference) x.property⟩=
      likelihoodFilter b t (towerDeltaClosed thirdThermalReference x) :=
  commuting_operator_delta_apply thirdThermalReference (likelihoodFilter b t)
    (likelihood_filter_selfadjoint b t) (filter_flow_commutes b t) x

theorem inverse_filter_delta_commutes (b : SummableAmplitude) (t : ℝ)
    (x : modularSquareDomain thirdThermalReference) :
    towerDeltaClosed thirdThermalReference
      ⟨inverseLikelihoodFilter b t (x : TowerHilbert thirdThermalReference),
        inverse_filter_preserves_delta_domain b t (x : TowerHilbert thirdThermalReference) x.property⟩=
      inverseLikelihoodFilter b t (towerDeltaClosed thirdThermalReference x) :=
  commuting_operator_delta_apply thirdThermalReference (inverseLikelihoodFilter b t)
    (inverse_filter_selfadjoint b t) (inverse_filter_flow_commutes b t) x

theorem filter_delta_domain_iff (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    likelihoodFilter b t x∈modularSquareDomain thirdThermalReference ↔
      x∈modularSquareDomain thirdThermalReference := by
  constructor
  · intro hx
    have hv := inverse_filter_preserves_delta_domain b t (likelihoodFilter b t x) hx
    have he : inverseLikelihoodFilter b t (likelihoodFilter b t x)=x :=
      (likelihoodFilterEquiv b t).symm_apply_apply x
    rwa [he] at hv
  · exact filter_preserves_delta_domain b t x

theorem relative_delta_original_domain (b : SummableAmplitude) (t : ℝ) :
    (relativeDelta b t).domain=(towerDeltaClosed thirdThermalReference).domain := by
  apply Submodule.ext
  intro x
  exact (relative_delta_domain_iff b t x).trans (filter_delta_domain_iff b t x)

theorem relative_delta_product_value (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference)
    (hx : x∈(towerDeltaClosed thirdThermalReference).domain)
    (hr : x∈(relativeDelta b t).domain) :
    relativeDelta b t ⟨x,hr⟩=
      NormedSpace.exp (likelihoodGenerator b t) (towerDeltaClosed thirdThermalReference ⟨x,hx⟩) := by
  calc
    _=likelihoodFilter b t (likelihoodFilter b t
        (towerDeltaClosed thirdThermalReference ⟨x,hx⟩)) :=
      congrArg (likelihoodFilter b t) (filter_delta_commutes b t ⟨x,hx⟩)
    _=(likelihoodFilter b t*likelihoodFilter b t)
        (towerDeltaClosed thirdThermalReference ⟨x,hx⟩) := rfl
    _=_ := congrArg (fun A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference =>
      A (towerDeltaClosed thirdThermalReference ⟨x,hx⟩)) (likelihood_filter_square b t)

def likelihoodModularProduct (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference →ₗ.[ℂ] TowerHilbert thirdThermalReference where
  domain := (towerDeltaClosed thirdThermalReference).domain
  toFun := (NormedSpace.exp (likelihoodGenerator b t)).toLinearMap.comp
    (towerDeltaClosed thirdThermalReference).toFun

theorem relative_delta_eq_likelihood_product (b : SummableAmplitude) (t : ℝ) :
    relativeDelta b t=likelihoodModularProduct b t := by
  apply LinearPMap.ext (f := relativeDelta b t) (g := likelihoodModularProduct b t)
    (relative_delta_original_domain b t)
  intro x hr hx
  exact relative_delta_product_value b t x hx hr

theorem likelihood_modular_product_selfadjoint (b : SummableAmplitude) (t : ℝ) :
    IsSelfAdjoint (likelihoodModularProduct b t) := by
  rw [←relative_delta_eq_likelihood_product]
  exact relative_delta_selfadjoint b t

theorem likelihood_modular_product_closed (b : SummableAmplitude) (t : ℝ) :
    (likelihoodModularProduct b t).IsClosed := by
  rw [←relative_delta_eq_likelihood_product]
  exact relative_delta_closed b t

theorem likelihood_modular_product_positive (b : SummableAmplitude) (t : ℝ)
    (x : (likelihoodModularProduct b t).domain) :
    0≤(inner ℂ (x : TowerHilbert thirdThermalReference) (likelihoodModularProduct b t x)).re := by
  have hr : (x : TowerHilbert thirdThermalReference)∈(relativeDelta b t).domain :=
    (relative_delta_original_domain b t).symm ▸ x.property
  have hp := relative_delta_positive b t ⟨(x : TowerHilbert thirdThermalReference),hr⟩
  rw [relative_delta_product_value b t (x : TowerHilbert thirdThermalReference) x.property hr] at hp
  exact hp

theorem generator_preserves_delta_domain (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) (hx : x∈modularSquareDomain thirdThermalReference) :
    likelihoodGenerator b t x∈modularSquareDomain thirdThermalReference :=
  commuting_operator_preserves_delta_domain thirdThermalReference (likelihoodGenerator b t)
    (likelihood_generator_selfadjoint b t)
    (modular_fixed_commutes_with_flow thirdThermalReference (likelihoodGenerator b t)
      (likelihood_generator_modular_fixed b t)) x hx

theorem generator_delta_commutes (b : SummableAmplitude) (t : ℝ)
    (x : modularSquareDomain thirdThermalReference) :
    towerDeltaClosed thirdThermalReference
      ⟨likelihoodGenerator b t (x : TowerHilbert thirdThermalReference),
        generator_preserves_delta_domain b t (x : TowerHilbert thirdThermalReference) x.property⟩=
      likelihoodGenerator b t (towerDeltaClosed thirdThermalReference x) :=
  commuting_operator_delta_apply thirdThermalReference (likelihoodGenerator b t)
    (likelihood_generator_selfadjoint b t)
    (modular_fixed_commutes_with_flow thirdThermalReference (likelihoodGenerator b t)
      (likelihood_generator_modular_fixed b t)) x

theorem relative_delta_reference_control (b : SummableAmplitude) :
    relativeDelta b 0=towerDeltaClosed thirdThermalReference := by
  rw [relative_delta_eq_likelihood_product]
  apply LinearPMap.ext (f := likelihoodModularProduct b 0)
    (g := towerDeltaClosed thirdThermalReference) rfl
  intro x hf hg
  change NormedSpace.exp (likelihoodGenerator b 0)
    (towerDeltaClosed thirdThermalReference ⟨x,hf⟩)=towerDeltaClosed thirdThermalReference ⟨x,hg⟩
  rw [likelihood_generator_zero,NormedSpace.exp_zero]
  rfl

#print axioms inverse_filter_modular_fixed
#print axioms filter_flow_commutes
#print axioms inverse_filter_flow_commutes
#print axioms filter_preserves_delta_domain
#print axioms inverse_filter_preserves_delta_domain
#print axioms filter_delta_commutes
#print axioms inverse_filter_delta_commutes
#print axioms filter_delta_domain_iff
#print axioms relative_delta_original_domain
#print axioms relative_delta_product_value
#print axioms likelihoodModularProduct
#print axioms relative_delta_eq_likelihood_product
#print axioms likelihood_modular_product_selfadjoint
#print axioms likelihood_modular_product_closed
#print axioms likelihood_modular_product_positive
#print axioms generator_preserves_delta_domain
#print axioms generator_delta_commutes
#print axioms relative_delta_reference_control
end
end ChatgptAudit.Commutation032
