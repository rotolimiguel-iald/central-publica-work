-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 063..066 (09/09/2026, noite), transposta em 10/09/2026 (ENTREGA_067 = elo do lote)
-- Os 21 modulos restantes da bancada (elos 83 -> 93 -> 98 da cadeia de copias integradas; 77 ja na v338).
--   063 (6 modulos, 113 teoremas): RESPOSTA GIBBS ANTES DA FONTE — protocolo misto (W = X + Z, medicao Z, s = v^2 t^2):
--     igualdade das respostas de entropia e energia de referencia na ordem quadratica; a fonte calculada da resposta com
--     conservacao por closed/wave; o seletor transporta o registro; O LIMITE LOCAL DE INTERACOES EXTENSIVAS (Lean);
--     a lei fisica de area e a metrica seguem entradas. [DERIVED, escrito]: Araki/GNS, tempo global, KMS no fecho C*.
--   065 (10 modulos, 108 teoremas): estabilidade do prefixo do caracter, resolucao finita, controle de malha do
--     registro, cotas de erro da resposta finita, precisao finita de Gibbs misto, janela de amostragem; METRICA DE
--     FISHER-LORENTZ SELECIONADA, variacao da densidade de materia escalar, ponte Fisher-Gibbs, CONSERVACAO sigma.
--   066 (5 modulos, 67 teoremas): sigma DOS MESMOS P (phi_j = sqrt(P_j/(1 - P_s))), resposta de Gibbs ASSINADA (dois
--     sinais com probabilidades positivas), esperanca negativa renormalizada, cobertura, reconstrucao por DEZ LIMITES
--     (SignedGibbsFiniteRecord); T e entrada; nao se identifica o observavel com stress de QFT.
--   Estatuto: [REAL] o compilado; [INPUT] a lei de area, a metrica, T, a acao/particao; [DERIVED + KNOWN] Araki, GNS,
--   KMS C*; [OPEN] correspondencia geral de selecao/materia/protocolo/area, realizacao interagente, anomalias, UV.
--   As ENTREGAS 067..087 sao MATEMATICA ESCRITA REVISADA (CAS, sem Lean) — registradas no diario e no Atlas como
--   [DERIVED], nao como flags; a propria bancada: "nao promover demonstracoes escritas a flags de compilacao".
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (98 -> 93 -> 83 -> 77...),
--   77 ja no kernel pulados; 21/21 hashes lidos dos bytes; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   21/21 contra o kernel v338, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.BondLocalityEstimates
import TGLExt.UnitaryDuhamel
import Mathlib.Analysis.Normed.Operator.Mul
import Mathlib.Topology.Algebra.InfiniteSum.Module

set_option autoImplicit false
set_option maxHeartbeats 1200000
set_option synthInstance.maxHeartbeats 200000
namespace ChatgptAudit.FiniteCommutatorSeries
open TGLExt NormedSpace ChatgptAudit.BondLocality ChatgptAudit.UnitaryDuhamel
noncomputable section
open scoped Nat

local instance operatorRationalAlgebra (P : SiteProfile) : NormedAlgebra ℚ (BondOperator P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance operatorRationalTower (P : SiteProfile) : IsScalarTower ℚ ℂ (BondOperator P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

abbrev SuperOperator (P : SiteProfile) := BondOperator P →L[ℂ] BondOperator P

local instance superRationalAlgebra (P : SiteProfile) : NormedAlgebra ℚ (SuperOperator P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance superRationalTower (P : SiteProfile) : IsScalarTower ℚ ℂ (SuperOperator P) where
  smul_assoc r z F := by
    apply ContinuousLinearMap.ext
    intro A
    exact smul_assoc r z (F A)

local instance superTopologicalRing (P : SiteProfile) : IsTopologicalRing (SuperOperator P) :=
  @NonUnitalSeminormedRing.toIsTopologicalRing (SuperOperator P) inferInstance

def leftMultiplier {P : SiteProfile} (H : BondOperator P) : SuperOperator P :=
  ContinuousLinearMap.mul ℂ (BondOperator P) H

def rightMultiplier {P : SiteProfile} (H : BondOperator P) : SuperOperator P :=
  (ContinuousLinearMap.mul ℂ (BondOperator P)).flip H

theorem left_multiplier_apply {P : SiteProfile} (H A : BondOperator P) :
    leftMultiplier H A = H * A := rfl

theorem right_multiplier_apply {P : SiteProfile} (H A : BondOperator P) :
    rightMultiplier H A = A * H := rfl

theorem left_multiplier_power_apply {P : SiteProfile} (H A : BondOperator P) (k : ℕ) :
    (leftMultiplier H ^ k) A = H ^ k * A := by
  induction k with
  | zero => simp
  | succ k ih =>
      rw [pow_succ',mul_apply_eq_comp,left_multiplier_apply,ih,pow_succ']
      exact (mul_assoc _ _ _).symm

theorem right_multiplier_power_apply {P : SiteProfile} (H A : BondOperator P) (k : ℕ) :
    (rightMultiplier H ^ k) A = A * H ^ k := by
  induction k with
  | zero => simp
  | succ k ih =>
      rw [pow_succ',mul_apply_eq_comp,right_multiplier_apply,ih,pow_succ]
      exact mul_assoc _ _ _

theorem multipliers_commute {P : SiteProfile} (H K : BondOperator P) :
    Commute (leftMultiplier H) (rightMultiplier K) := by
  apply ContinuousLinearMap.ext
  intro A
  exact (mul_assoc H A K).symm

theorem exp_left_multiplier_apply {P : SiteProfile} (H A : BondOperator P) :
    (NormedSpace.exp (leftMultiplier H)) A = NormedSpace.exp H * A := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) (leftMultiplier H)).mapL
    (ContinuousLinearMap.apply ℂ (BondOperator P) A)
  have ht := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) H).mapL (rightMultiplier A)
  simp only [ContinuousLinearMap.apply_apply,smul_apply,
    left_multiplier_power_apply] at hs
  simp only [map_smul,right_multiplier_apply] at ht
  exact hs.unique ht

theorem exp_right_multiplier_apply {P : SiteProfile} (H A : BondOperator P) :
    (NormedSpace.exp (rightMultiplier H)) A = A * NormedSpace.exp H := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) (rightMultiplier H)).mapL
    (ContinuousLinearMap.apply ℂ (BondOperator P) A)
  have ht := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) H).mapL (leftMultiplier A)
  simp only [ContinuousLinearMap.apply_apply,smul_apply,
    right_multiplier_power_apply] at hs
  simp only [map_smul,left_multiplier_apply] at ht
  exact hs.unique ht

def bracketOperator {P : SiteProfile} (H : BondOperator P) : SuperOperator P :=
  leftMultiplier H - rightMultiplier H

theorem bracket_operator_apply {P : SiteProfile} (H A : BondOperator P) :
    bracketOperator H A = operatorBracket H A := rfl

theorem scaled_bracket_split {P : SiteProfile} (H : BondOperator P) (z : ℂ) :
    z • bracketOperator H = leftMultiplier (z • H) + rightMultiplier ((-z) • H) := by
  apply ContinuousLinearMap.ext
  intro A
  change z • (H * A - A * H) = (z • H) * A + A * ((-z) • H)
  simp only [smul_mul_assoc,mul_smul_comm,neg_smul,mul_neg,sub_eq_add_neg,smul_add,smul_neg]

theorem exp_scaled_bracket_apply {P : SiteProfile} (H A : BondOperator P) (z : ℂ) :
    (NormedSpace.exp (z • bracketOperator H)) A =
      NormedSpace.exp (z • H) * A * NormedSpace.exp ((-z) • H) := by
  have he : NormedSpace.exp (leftMultiplier (z • H) + rightMultiplier ((-z) • H)) =
      NormedSpace.exp (leftMultiplier (z • H)) *
        NormedSpace.exp (rightMultiplier ((-z) • H)) :=
    NormedSpace.exp_add_of_commute (𝔸 := SuperOperator P)
      (multipliers_commute (z • H) ((-z) • H))
  rw [scaled_bracket_split,he,
    mul_apply_eq_comp,exp_right_multiplier_apply,exp_left_multiplier_apply]
  exact (mul_assoc _ _ _).symm

theorem cutoff_scaled_bracket_power {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (z : ℂ) (k : ℕ) :
    ((z • bracketOperator (cutoffHamiltonian D N)) ^ k) A =
      z ^ k • iteratedCutoffBracket D N A k := by
  induction k with
  | zero => simp [iteratedCutoffBracket]
  | succ k ih =>
      rw [pow_succ',mul_apply_eq_comp,smul_apply,ih,
        map_smul,bracket_operator_apply,cutoff_hamiltonian_bracket,smul_smul]
      rw [pow_succ',iteratedCutoffBracket]

theorem cutoff_conjugation_hasSum {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (z : ℂ) :
    HasSum (fun k => (z ^ k / (k.factorial : ℂ)) • iteratedCutoffBracket D N A k)
      (NormedSpace.exp (z • cutoffHamiltonian D N) * A *
        NormedSpace.exp ((-z) • cutoffHamiltonian D N)) := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ)
      (z • bracketOperator (cutoffHamiltonian D N))).mapL
        (ContinuousLinearMap.apply ℂ (BondOperator P) A)
  simpa only [ContinuousLinearMap.apply_apply,smul_apply,
    cutoff_scaled_bracket_power,exp_scaled_bracket_apply,smul_smul,div_eq_mul_inv,mul_comm] using hs

def finiteEvolution {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (t : ℝ) (A : BondOperator P) : BondOperator P :=
  evolution (cutoffHamiltonian D N) t * A * evolution (cutoffHamiltonian D N) (-t)

theorem finite_evolution_hasSum {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (t : ℝ) :
    HasSum (fun k => (((t : ℂ) * Complex.I) ^ k / (k.factorial : ℂ)) •
      iteratedCutoffBracket D N A k) (finiteEvolution D N t A) := by
  simpa only [finiteEvolution,evolution,Complex.ofReal_neg,neg_mul] using
    cutoff_conjugation_hasSum D N A ((t : ℂ) * Complex.I)

theorem finite_evolution_eq_tsum {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (t : ℝ) :
    finiteEvolution D N t A =
      ∑' k, (((t : ℂ) * Complex.I) ^ k / (k.factorial : ℂ)) •
        iteratedCutoffBracket D N A k :=
  (finite_evolution_hasSum D N A t).tsum_eq.symm

theorem finite_evolution_series_summable {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (t : ℝ) :
    Summable (fun k => (((t : ℂ) * Complex.I) ^ k / (k.factorial : ℂ)) •
      iteratedCutoffBracket D N A k) :=
  (finite_evolution_hasSum D N A t).summable

theorem finite_evolution_isometry {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (t : ℝ) (A : BondOperator P) :
    ‖finiteEvolution D N t A‖ = ‖A‖ := by
  unfold finiteEvolution
  rw [CStarRing.norm_mul_mem_unitary _
      (evolution_unitary _ (cutoff_hamiltonian_selfadjoint D N) (-t)),
    CStarRing.norm_mem_unitary_mul _
      (evolution_unitary _ (cutoff_hamiltonian_selfadjoint D N) t)]

#print axioms operatorRationalAlgebra
#print axioms operatorRationalTower
#print axioms SuperOperator
#print axioms superRationalAlgebra
#print axioms superRationalTower
#print axioms superTopologicalRing
#print axioms leftMultiplier
#print axioms rightMultiplier
#print axioms left_multiplier_apply
#print axioms right_multiplier_apply
#print axioms left_multiplier_power_apply
#print axioms right_multiplier_power_apply
#print axioms multipliers_commute
#print axioms exp_left_multiplier_apply
#print axioms exp_right_multiplier_apply
#print axioms bracketOperator
#print axioms bracket_operator_apply
#print axioms scaled_bracket_split
#print axioms exp_scaled_bracket_apply
#print axioms cutoff_scaled_bracket_power
#print axioms cutoff_conjugation_hasSum
#print axioms finiteEvolution
#print axioms finite_evolution_hasSum
#print axioms finite_evolution_eq_tsum
#print axioms finite_evolution_series_summable
#print axioms finite_evolution_isometry
end
end ChatgptAudit.FiniteCommutatorSeries
