import TGLExt.TheImportedSecondQuantization

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# A PONTE DO TENSOR DE MAXWELL: o objeto da LITERATURA habita o certificado — no domínio, literalmente   [TGLExt — v375, pedra da gerência (27/09/2026)]

O livro-razão da v374 marcou `MaxwellWickExpectationLocalMeasured` como CITED_NONSTANDARD_TYPE: o certificado
`MaxwellCertificate` pede um tensor TOTAL (`StressTensorDataLocalV32.T : C.F → …`, para TODO ψ), e a literatura dá
⟨ψ, :T_ab(x): ψ⟩ como FORMA QUADRÁTICA só num domínio invariante de estados suaves de finitas partículas
[KNOWN — Wightman–Gårding 1964 (Ark. Fys. 28): produtos de Wick de campos livres como formas quadráticas no domínio de finitas
partículas, invariante sob Poincaré; a seção exata de Reed–Simon II e o enunciado para Maxwell: a conferir].

Esta pedra tipa o objeto da literatura COMO ELE É (`MaxwellQuadraticForm`: todos os campos quantificados SÓ sobre o
domínio) e constrói POR TERMO o tensor total do certificado pela EXTENSÃO POR ZERO fora do domínio. Dentro do domínio o
tensor do certificado É a forma da literatura, literalmente (`toStress_on_dom`, por `if_pos`); fora dele é extensão por zero
SEM conteúdo físico. Nenhuma prova do caminho da declaração o consome fora do domínio (aferição de 27/09, pelo fecho em Lean:
`Regular` exige ψ ∈ Dom); os teoremas genéricos do contrato que valem para todo ψ valem trivialmente fora de Dom. A lacuna
«T total, não forma quadrática» vira FIAÇÃO provada no domínio.

Estatuto: a forma da literatura é CITADA (campo de estrutura com fonte); a ponte é POR TERMO. Sem sorry, sem axiom.
PROVADA ≠ CONFIRMADA.
-/

noncomputable section
namespace TGLExt.MaxwellBridge
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 TGLExt.ImportedSQ
open MeasureTheory

variable {L : LightOneParticle} (C : FockCertificate L)

/-- **o objeto da LITERATURA**: ⟨ψ, :T_ab(x): ψ⟩ do campo de Maxwell livre como forma quadrática SÓ no domínio nomeado,
    invariante sob translações e boosts, com o vácuo [KNOWN — Wightman–Gårding 1964; a seção de Reed–Simon II e o enunciado para Maxwell: a conferir]. Nenhum campo
    fala de ψ fora do domínio. -/
structure MaxwellQuadraticForm where
  Dom : Set C.F
  Dom_vac : C.Ω ∈ Dom
  Dom_translate : ∀ (b : Fin 4 → ℝ) (ψ : C.F), C.Γ (U1 b) ψ ∈ Dom ↔ ψ ∈ Dom
  Dom_boost : ∀ (s : ℝ) (ψ : C.F), C.Γ (B0 s) ψ ∈ Dom ↔ ψ ∈ Dom
  Q : C.F → (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  Q_vac : ∀ x : Fin 4 → ℝ, Q C.Ω x = 0
  Q_covariant : ∀ (a : Fin 4 → ℝ) (ψ : C.F) (x : Fin 4 → ℝ), ψ ∈ Dom → Q (C.Γ (U1 a) ψ) x = Q ψ (x - a)
  Q_symmetric : ∀ (ψ : C.F) (x : Fin 4 → ℝ), ψ ∈ Dom → (Q ψ x).transpose = Q ψ x
  Q_test_integrable : ∀ (ψ : C.F), ψ ∈ Dom → ∀ (ν μ : Fin 4) (f : (Fin 4 → ℝ) → ℝ),
    ContDiff ℝ (⊤ : ℕ∞) f → HasCompactSupport f →
    Integrable (fun x => metricSignV32 μ * Q ψ x μ ν * testDerivativeV32 f μ x)
  Q_conserved : ∀ (ψ : C.F), ψ ∈ Dom → ∀ (ν : Fin 4) (f : (Fin 4 → ℝ) → ℝ),
    ContDiff ℝ (⊤ : ℕ∞) f → HasCompactSupport f →
    (∑ μ : Fin 4, ∫ x : Fin 4 → ℝ, metricSignV32 μ * Q ψ x μ ν * testDerivativeV32 f μ x) = 0
  Q_boost_covariant : ∀ (s : ℝ) (ψ : C.F) (x : Fin 4 → ℝ), ψ ∈ Dom →
    Q (C.Γ (B0 s) ψ) x = (TGLExt.boostMat (-s)).transpose * Q ψ (wedgeBoostMap (-s) x) * TGLExt.boostMat (-s)

variable {C}

open Classical in
/-- a EXTENSÃO POR ZERO: a forma da literatura dentro do domínio, zero fora. -/
def extendByZero (Q : MaxwellQuadraticForm C) : C.F → (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ :=
  fun ψ x => if ψ ∈ Q.Dom then Q.Q ψ x else 0

theorem extendByZero_on_dom (Q : MaxwellQuadraticForm C) {ψ : C.F} (h : ψ ∈ Q.Dom) (x : Fin 4 → ℝ) :
    extendByZero Q ψ x = Q.Q ψ x := by
  classical
  simp [extendByZero, h]

theorem extendByZero_off_dom (Q : MaxwellQuadraticForm C) {ψ : C.F} (h : ψ ∉ Q.Dom) (x : Fin 4 → ℝ) :
    extendByZero Q ψ x = 0 := by
  classical
  simp [extendByZero, h]

/-- ★★ o tensor TOTAL do certificado, construído POR TERMO a partir da forma da literatura. -/
def toStress (Q : MaxwellQuadraticForm C) : StressTensorDataLocalV32 (lightNet C) (lightBoost C) where
  T := extendByZero Q
  T_vac := fun x => by
    show extendByZero Q C.Ω x = 0
    rw [extendByZero_on_dom Q Q.Dom_vac, Q.Q_vac]
  T_covariant := fun a ψ x => by
    show extendByZero Q (C.Γ (U1 a) ψ) x = extendByZero Q ψ (x - a)
    by_cases h : ψ ∈ Q.Dom
    · rw [extendByZero_on_dom Q ((Q.Dom_translate a ψ).mpr h), extendByZero_on_dom Q h, Q.Q_covariant a ψ x h]
    · have h' : C.Γ (U1 a) ψ ∉ Q.Dom := fun hm => h ((Q.Dom_translate a ψ).mp hm)
      rw [extendByZero_off_dom Q h', extendByZero_off_dom Q h]
  symmetric := fun ψ x => by
    by_cases h : ψ ∈ Q.Dom
    · rw [extendByZero_on_dom Q h]; exact Q.Q_symmetric ψ x h
    · rw [extendByZero_off_dom Q h]; exact Matrix.transpose_zero
  test_integrable := fun ψ ν μ f hf hc => by
    by_cases h : ψ ∈ Q.Dom
    · simp only [extendByZero_on_dom Q h]; exact Q.Q_test_integrable ψ h ν μ f hf hc
    · simp only [extendByZero_off_dom Q h, Matrix.zero_apply, mul_zero, zero_mul]
      exact integrable_zero _ _ _
  conserved := fun ψ ν f hf hc => by
    by_cases h : ψ ∈ Q.Dom
    · simp only [extendByZero_on_dom Q h]; exact Q.Q_conserved ψ h ν f hf hc
    · simp only [extendByZero_off_dom Q h, Matrix.zero_apply, mul_zero, zero_mul, integral_zero,
        Finset.sum_const_zero]
  boost_covariant := fun s ψ x => by
    show extendByZero Q (C.Γ (B0 s) ψ) x =
      (TGLExt.boostMat (-s)).transpose * extendByZero Q ψ (wedgeBoostMap (-s) x) * TGLExt.boostMat (-s)
    by_cases h : ψ ∈ Q.Dom
    · rw [extendByZero_on_dom Q ((Q.Dom_boost s ψ).mpr h), extendByZero_on_dom Q h, Q.Q_boost_covariant s ψ x h]
    · have h' : C.Γ (B0 s) ψ ∉ Q.Dom := fun hm => h ((Q.Dom_boost s ψ).mp hm)
      rw [extendByZero_off_dom Q h', extendByZero_off_dom Q h, Matrix.mul_zero, Matrix.zero_mul]

/-- ★★ dentro do domínio, o tensor do certificado É a forma da literatura (nada inventado). -/
theorem toStress_on_dom (Q : MaxwellQuadraticForm C) {ψ : C.F} (h : ψ ∈ Q.Dom) :
    (toStress Q).T ψ = Q.Q ψ := funext fun x => extendByZero_on_dom Q h x

/-- ★ fora do domínio o tensor é zero (sem conteúdo físico) — nenhuma prova do caminho o consome ali (`Regular` exige ψ ∈ Dom). -/
theorem toStress_off_dom (Q : MaxwellQuadraticForm C) {ψ : C.F} (h : ψ ∉ Q.Dom) :
    (toStress Q).T ψ = 0 := funext fun x => extendByZero_off_dom Q h x

theorem regular_in_dom (Q : MaxwellQuadraticForm C) {ψ : C.F}
    (h : Regular Q.Dom (toStress Q).toStressTensorData ψ) : ψ ∈ Q.Dom := h.1

/-- ★★★ **o certificado de Maxwell a partir do objeto da LITERATURA**: o domínio e a forma são os citados; o tensor
    total é a extensão por zero (por termo); os dois fatos de estado seguem CITADOS [CTT 2017/Wall 2011 — física;
    Longo 2019], quantificados só sobre estados regulares (logo DENTRO do domínio). -/
def toCertificate (Q : MaxwellQuadraticForm C)
    (charge_link : ∀ ψ, Regular Q.Dom (toStress Q).toStressTensorData ψ → ∀ k : ℝ,
      HasModularEnergy (lightDelta C) ψ k → k = 2 * Real.pi * nullPlaneCharge (toStress Q).toStressTensorData ψ)
    (nontrivial : ∃ ψ, Regular Q.Dom (toStress Q).toStressTensorData ψ ∧
      ∃ k : ℝ, HasModularEnergy (lightDelta C) ψ k ∧ k ≠ 0) : MaxwellCertificate C where
  Dom := Q.Dom
  Dom_vac := Q.Dom_vac
  Dom_translate := fun b ψ h => (Q.Dom_translate b ψ).mpr h
  T := toStress Q
  charge_link := charge_link
  nontrivial := nontrivial

/-- ★★ o certificado construído não inventa: o domínio é o citado e, nele, o tensor é a forma citada. -/
theorem toCertificate_is_the_literature (Q : MaxwellQuadraticForm C) (cl) (nt) :
    (toCertificate Q cl nt).Dom = Q.Dom ∧
      ∀ ψ ∈ (toCertificate Q cl nt).Dom, (toCertificate Q cl nt).T.T ψ = Q.Q ψ :=
  ⟨rfl, fun ψ h => toStress_on_dom Q h⟩

end TGLExt.MaxwellBridge

#print axioms TGLExt.MaxwellBridge.MaxwellQuadraticForm
#print axioms TGLExt.MaxwellBridge.extendByZero
#print axioms TGLExt.MaxwellBridge.extendByZero_on_dom
#print axioms TGLExt.MaxwellBridge.extendByZero_off_dom
#print axioms TGLExt.MaxwellBridge.toStress
#print axioms TGLExt.MaxwellBridge.toStress_on_dom
#print axioms TGLExt.MaxwellBridge.toStress_off_dom
#print axioms TGLExt.MaxwellBridge.regular_in_dom
#print axioms TGLExt.MaxwellBridge.toCertificate
#print axioms TGLExt.MaxwellBridge.toCertificate_is_the_literature
