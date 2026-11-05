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
import TGLExt.FiniteCommutatorEvolution
import Mathlib.Analysis.Normed.Group.Tannery
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Data.Nat.Factorial.BigOperators
import Mathlib.Data.Nat.Choose.Basic

set_option autoImplicit false
set_option maxHeartbeats 1200000
set_option synthInstance.maxHeartbeats 200000
namespace ChatgptAudit.SmallTimeLocalLimit
open TGLExt Filter Topology ChatgptAudit.BondLocality ChatgptAudit.FiniteCommutatorSeries
noncomputable section
open scoped Nat

def commutatorSeriesTerm {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (t : ℝ) (k : ℕ) : BondOperator P :=
  (((t : ℂ) * Complex.I) ^ k / (k.factorial : ℂ)) • iteratedCutoffBracket D N A k

def localSeriesMajorant (J : ℝ) (R : ℕ) (a t : ℝ) (k : ℕ) : ℝ :=
  (2 * J * |t|) ^ k * ((k + R).choose R : ℝ) * a

theorem growth_product_factorial_choose (R k : ℕ) :
    (∏ r ∈ Finset.range k, ((R + r + 1 : ℕ) : ℝ)) =
      (k.factorial : ℝ) * ((R + k).choose k : ℝ) := by
  have hn : (∏ r ∈ Finset.range k, (R + r + 1)) =
      k.factorial * (R + k).choose k := by
    rw [← Nat.ascFactorial_eq_factorial_mul_choose]
    simp only [Nat.ascFactorial_eq_prod_range, Nat.add_right_comm]
  exact_mod_cast hn

theorem growth_factorial_quotient (J t : ℝ) (R k : ℕ) :
    (|t| ^ k / (k.factorial : ℝ)) * commutatorGrowth J R k =
      (2 * J * |t|) ^ k * ((k + R).choose R : ℝ) := by
  have hk : (k.factorial : ℝ) ≠ 0 := by exact_mod_cast k.factorial_ne_zero
  have hc : (R + k).choose k = (k + R).choose R := by
    rw [Nat.add_comm R k]
    exact Nat.choose_symm_add
  rw [commutatorGrowth,growth_product_factorial_choose,hc]
  rw [mul_pow]
  field_simp
  ring

theorem commutator_series_term_norm {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (t : ℝ) (k : ℕ) :
    ‖commutatorSeriesTerm D N A t k‖ =
      (|t| ^ k / (k.factorial : ℝ)) * ‖iteratedCutoffBracket D N A k‖ := by
  simp [commutatorSeriesTerm,norm_smul,norm_pow]

theorem commutator_series_uniform_bound {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (N : ℕ) (t : ℝ) (k : ℕ) :
    ‖commutatorSeriesTerm D N A t k‖ ≤ localSeriesMajorant D.bound R ‖A‖ t k := by
  rw [commutator_series_term_norm]
  calc
    (|t| ^ k / (k.factorial : ℝ)) * ‖iteratedCutoffBracket D N A k‖
        ≤ (|t| ^ k / (k.factorial : ℝ)) *
            (commutatorGrowth D.bound R k * ‖A‖) :=
      mul_le_mul_of_nonneg_left (iterated_bracket_uniform_bound D hA N k) (by positivity)
    _ = localSeriesMajorant D.bound R ‖A‖ t k := by
      rw [← mul_assoc,growth_factorial_quotient]
      rfl

theorem local_series_majorant_summable (J : ℝ) (R : ℕ) (a t : ℝ)
    (hJ : 0 ≤ J) (ht : 2 * J * |t| < 1) :
    Summable (localSeriesMajorant J R a t) := by
  have hq : ‖2 * J * |t|‖ < 1 := by
    rw [Real.norm_eq_abs,abs_of_nonneg (by positivity)]
    exact ht
  have hs := (summable_choose_mul_geometric_of_norm_lt_one R hq).mul_right a
  apply hs.congr
  intro k
  dsimp [localSeriesMajorant]
  ring

def stabilizedSeriesTerm {P : SiteProfile} (D : BondInteractionData P)
    (R : ℕ) (A : BondOperator P) (t : ℝ) (k : ℕ) : BondOperator P :=
  commutatorSeriesTerm D (R + k) A t k

theorem commutator_series_term_stabilizes {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (t : ℝ) (k N : ℕ)
    (hN : R + k ≤ N) :
    commutatorSeriesTerm D N A t k = stabilizedSeriesTerm D R A t k := by
  unfold commutatorSeriesTerm stabilizedSeriesTerm
  rw [iterated_bracket_cutoff_independent D hA k N (R + k) hN le_rfl]
  rfl

theorem commutator_series_term_tendsto {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (t : ℝ) (k : ℕ) :
    Tendsto (fun N => commutatorSeriesTerm D N A t k) atTop
      (𝓝 (stabilizedSeriesTerm D R A t k)) := by
  apply tendsto_const_nhds.congr'
  filter_upwards [eventually_ge_atTop (R + k)] with N hN
  exact (commutator_series_term_stabilizes D hA t k N hN).symm

theorem stabilized_series_summable {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (t : ℝ)
    (ht : 2 * D.bound * |t| < 1) :
    Summable (stabilizedSeriesTerm D R A t) := by
  exact (local_series_majorant_summable D.bound R ‖A‖ t D.bound_nonnegative ht).of_norm_bounded
    (fun k => commutator_series_uniform_bound D hA (R + k) t k)

def localSeriesEvolution {P : SiteProfile} (D : BondInteractionData P)
    (R : ℕ) (t : ℝ) (A : BondOperator P) : BondOperator P :=
  ∑' k, stabilizedSeriesTerm D R A t k

theorem finite_evolution_tendsto_local_series {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (t : ℝ)
    (ht : 2 * D.bound * |t| < 1) :
    Tendsto (fun N => finiteEvolution D N t A) atTop
      (𝓝 (localSeriesEvolution D R t A)) := by
  have hl := tendsto_tsum_of_dominated_convergence
    (local_series_majorant_summable D.bound R ‖A‖ t D.bound_nonnegative ht)
    (commutator_series_term_tendsto D hA t)
    (Eventually.of_forall (fun N k => commutator_series_uniform_bound D hA N t k))
  simpa only [localSeriesEvolution,commutatorSeriesTerm,← finite_evolution_eq_tsum] using hl

theorem finite_evolution_cauchy_local {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (t : ℝ)
    (ht : 2 * D.bound * |t| < 1) :
    CauchySeq (fun N => finiteEvolution D N t A) :=
  (finite_evolution_tendsto_local_series D hA t ht).cauchySeq

theorem local_series_evolution_norm {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (t : ℝ)
    (ht : 2 * D.bound * |t| < 1) :
    ‖localSeriesEvolution D R t A‖ = ‖A‖ := by
  have hn := (finite_evolution_tendsto_local_series D hA t ht).norm
  simp only [finite_evolution_isometry] at hn
  exact tendsto_nhds_unique hn tendsto_const_nhds

theorem local_series_evolution_independent_prefix {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R S : ℕ}
    (hR : A ∈ chainLocalAlgebra P (Set.Iic R))
    (hS : A ∈ chainLocalAlgebra P (Set.Iic S)) (t : ℝ)
    (ht : 2 * D.bound * |t| < 1) :
    localSeriesEvolution D R t A = localSeriesEvolution D S t A :=
  tendsto_nhds_unique (finite_evolution_tendsto_local_series D hR t ht)
    (finite_evolution_tendsto_local_series D hS t ht)

#print axioms commutatorSeriesTerm
#print axioms localSeriesMajorant
#print axioms growth_product_factorial_choose
#print axioms growth_factorial_quotient
#print axioms commutator_series_term_norm
#print axioms commutator_series_uniform_bound
#print axioms local_series_majorant_summable
#print axioms stabilizedSeriesTerm
#print axioms commutator_series_term_stabilizes
#print axioms commutator_series_term_tendsto
#print axioms stabilized_series_summable
#print axioms localSeriesEvolution
#print axioms finite_evolution_tendsto_local_series
#print axioms finite_evolution_cauchy_local
#print axioms local_series_evolution_norm
#print axioms local_series_evolution_independent_prefix
end
end ChatgptAudit.SmallTimeLocalLimit
