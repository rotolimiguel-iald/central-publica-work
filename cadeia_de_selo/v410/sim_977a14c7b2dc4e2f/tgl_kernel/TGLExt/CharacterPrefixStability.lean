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
import TGLExt.SelectedGravitationalAtlas
import TGLExt.InfiniteCocycleDecoding
import TGLExt.GeometricLikelihoodSeparation

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.CharacterPrecision
open Filter Topology Set TGLExt ChatgptAudit.CocycleRealization
  ChatgptAudit.Response028 ChatgptAudit.Cocycle030 ChatgptAudit.SelectedAtlas
  ChatgptAudit.GravitationalRecord
noncomputable section

/-- Agreement of the first N encoded bits. No field topology is implied. -/
def SamePrefix (u v : ℕ → Bool) (N : ℕ) : Prop := ∀ n, n < N → u n = v n

/-- The strict gap between a digit and all subsequent digits. -/
def siteGap (t : ℝ) (n : ℕ) : ℝ :=
  geometricContrast t n - ∑' k, geometricContrast t (n + 1 + k)

/-- For N >= 1, the minimum of the first N digit gaps; N=0 uses the first gap. -/
def prefixGap (t : ℝ) : ℕ → ℝ
  | 0 => siteGap t 0
  | N + 1 => min (prefixGap t N) (siteGap t N)

theorem site_gap_positive {t : ℝ} (ht : t ≠ 0) (n : ℕ) :
    0 < siteGap t n := by
  exact sub_pos.mpr (geometric_contrast_dominates_entire_tail ht n)

theorem prefix_gap_positive {t : ℝ} (ht : t ≠ 0) (N : ℕ) :
    0 < prefixGap t N := by
  induction N with
  | zero => exact site_gap_positive ht 0
  | succ N ih => exact lt_min ih (site_gap_positive ht N)

theorem prefix_gap_le_site_gap (t : ℝ) (N n : ℕ) (hn : n < N) :
    prefixGap t N ≤ siteGap t n := by
  induction N with
  | zero => omega
  | succ N ih =>
      rcases Nat.lt_succ_iff_lt_or_eq.mp hn with hlt | rfl
      · exact (min_le_left _ _).trans (ih hlt)
      · exact min_le_right _ _

theorem binary_code_split_before {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u : ℕ → Bool) (N : ℕ) :
    binaryCode a u = (∑ n ∈ Finset.range N, digitTerm a u n) +
      ∑' k, digitTerm a u (N + k) := by
  have h := (digit_summable ha hs u).sum_add_tsum_nat_add N
  simpa only [binaryCode, Nat.add_comm] using h.symm

theorem binary_code_prefix_error {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u v : ℕ → Bool) (N : ℕ) (hp : SamePrefix u v N) :
    |binaryCode a u - binaryCode a v| ≤ ∑' k, a (N + k) := by
  have he : (∑ n ∈ Finset.range N, digitTerm a u n) =
      ∑ n ∈ Finset.range N, digitTerm a v n := by
    apply Finset.sum_congr rfl
    intro n hn
    simp only [digitTerm, hp n (Finset.mem_range.mp hn)]
  have hsu : Summable (fun k => digitTerm a u (N + k)) :=
    (digit_summable ha hs u).comp_injective (fun _ _ h => Nat.add_left_cancel h)
  have hsv : Summable (fun k => digitTerm a v (N + k)) :=
    (digit_summable ha hs v).comp_injective (fun _ _ h => Nat.add_left_cancel h)
  have hsa : Summable (fun k => a (N + k)) :=
    hs.comp_injective (fun _ _ h => Nat.add_left_cancel h)
  have hu0 : 0 ≤ ∑' k, digitTerm a u (N + k) :=
    tsum_nonneg (fun k => (digit_term_bounds ha u (N + k)).1)
  have hv0 : 0 ≤ ∑' k, digitTerm a v (N + k) :=
    tsum_nonneg (fun k => (digit_term_bounds ha v (N + k)).1)
  have hua := Summable.tsum_le_tsum (fun k => (digit_term_bounds ha u (N + k)).2) hsu hsa
  have hva := Summable.tsum_le_tsum (fun k => (digit_term_bounds ha v (N + k)).2) hsv hsa
  rw [binary_code_split_before ha hs u N, binary_code_split_before ha hs v N, he]
  exact abs_le.mpr ⟨by linarith, by linarith⟩

theorem reading_difference_eq_code_difference (t : ℝ) (u v : ℕ → Bool) :
    |geometricLogReading t u - geometricLogReading t v| =
      |binaryCode (geometricContrast t) u - binaryCode (geometricContrast t) v| := by
  unfold geometricLogReading
  rw [show (∑' n, logOneRatio (geometricArgument t n)) - binaryCode (geometricContrast t) u -
      ((∑' n, logOneRatio (geometricArgument t n)) - binaryCode (geometricContrast t) v) =
      -(binaryCode (geometricContrast t) u - binaryCode (geometricContrast t) v) by ring]
  exact abs_neg _

theorem contrast_tail_explicit_bound (t : ℝ) (N : ℕ) :
    (∑' k, geometricContrast t (N + k)) ≤ regularParameter t / 2 * (1 / 2 : ℝ) ^ N := by
  have hpoint (k : ℕ) : geometricContrast t (N + k) ≤
      (regularParameter t / 4 * (1 / 2 : ℝ) ^ N) * (1 / 2 : ℝ) ^ k := by
    have h := contrast_upper (geometric_argument_bounds t (N + k)).1
      (geometric_argument_bounds t (N + k)).2
    change geometricContrast t (N + k) ≤
      6 * ((1 / 24) * (1 / 2 : ℝ) ^ (N + k) * regularParameter t) at h
    rw [pow_add] at h
    convert h using 1
    ring
  have hsa : Summable (fun k => geometricContrast t (N + k)) :=
    (geometric_contrast_summable t).comp_injective (fun _ _ h => Nat.add_left_cancel h)
  have hsg : Summable (fun k => (regularParameter t / 4 * (1 / 2 : ℝ) ^ N) * (1 / 2 : ℝ) ^ k) :=
    (summable_geometric_of_lt_one (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num)).mul_left _
  calc
    (∑' k, geometricContrast t (N + k)) ≤
        ∑' k, (regularParameter t / 4 * (1 / 2 : ℝ) ^ N) * (1 / 2 : ℝ) ^ k :=
      Summable.tsum_le_tsum hpoint hsa hsg
    _ = regularParameter t / 2 * (1 / 2 : ℝ) ^ N := by
      rw [tsum_mul_left, tsum_geometric_of_lt_one (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num)]
      ring

theorem geometric_reading_prefix_error_bound (t : ℝ) (u v : ℕ → Bool)
    (N : ℕ) (hp : SamePrefix u v N) :
    |geometricLogReading t u - geometricLogReading t v| ≤
      regularParameter t / 2 * (1 / 2 : ℝ) ^ N := by
  rw [reading_difference_eq_code_difference]
  exact (binary_code_prefix_error (geometric_contrast_nonnegative t)
    (geometric_contrast_summable t) u v N hp).trans (contrast_tail_explicit_bound t N)

theorem oriented_first_difference_gap (t : ℝ) (u v : ℕ → Bool) (n : ℕ)
    (hp : SamePrefix u v n) (hu : u n = false) (hv : v n = true) :
    siteGap t n ≤ binaryCode (geometricContrast t) v - binaryCode (geometricContrast t) u := by
  have he : (∑ k ∈ Finset.range n, digitTerm (geometricContrast t) u k) =
      ∑ k ∈ Finset.range n, digitTerm (geometricContrast t) v k := by
    apply Finset.sum_congr rfl
    intro k hk
    simp only [digitTerm, hp k (Finset.mem_range.mp hk)]
  rw [code_prefix_tail (geometric_contrast_nonnegative t) (geometric_contrast_summable t) u n,
    code_prefix_tail (geometric_contrast_nonnegative t) (geometric_contrast_summable t) v n, he]
  have htu := (digit_tail_bounds (geometric_contrast_nonnegative t) (geometric_contrast_summable t) u n).2
  have htv := (digit_tail_bounds (geometric_contrast_nonnegative t) (geometric_contrast_summable t) v n).1
  have du : digitTerm (geometricContrast t) u n = 0 := by simp [digitTerm, hu]
  have dv : digitTerm (geometricContrast t) v n = geometricContrast t n := by simp [digitTerm, hv]
  rw [du, dv]
  unfold siteGap
  linarith

theorem first_difference_reading_gap (t : ℝ) (u v : ℕ → Bool) (n : ℕ)
    (hp : SamePrefix u v n) (hne : u n ≠ v n) :
    siteGap t n ≤ |geometricLogReading t u - geometricLogReading t v| := by
  rw [reading_difference_eq_code_difference]
  cases hu : u n <;> cases hv : v n
  · exact False.elim (hne (hu.trans hv.symm))
  · have h := oriented_first_difference_gap t u v n hp hu hv
    exact h.trans (by simpa only [abs_sub_comm] using
      (le_abs_self (binaryCode (geometricContrast t) v - binaryCode (geometricContrast t) u)))
  · have h := oriented_first_difference_gap t v u n (fun k hk => (hp k hk).symm) hv hu
    exact h.trans (le_abs_self _)
  · exact False.elim (hne (hu.trans hv.symm))

theorem near_readings_have_same_prefix (t : ℝ) (u v : ℕ → Bool) (N : ℕ)
    (hclose : |geometricLogReading t u - geometricLogReading t v| < prefixGap t N) :
    SamePrefix u v N := by
  by_contra hnot
  have hex : ∃ n, n < N ∧ u n ≠ v n := by
    unfold SamePrefix at hnot
    push Not at hnot
    exact hnot
  let n := Nat.find hex
  have hn : n < N ∧ u n ≠ v n := Nat.find_spec hex
  have hp : SamePrefix u v n := by
    intro k hk
    by_contra hne
    exact Nat.find_min hex hk ⟨lt_trans hk hn.1, hne⟩
  have hgap := (prefix_gap_le_site_gap t N n hn.1).trans
    (first_difference_reading_gap t u v n hp hn.2)
  exact (not_lt_of_ge hgap) hclose

theorem noisy_candidates_have_same_prefix (t z error : ℝ) (u v : ℕ → Bool) (N : ℕ)
    (hu : |geometricLogReading t u - z| ≤ error)
    (hv : |geometricLogReading t v - z| ≤ error)
    (hresolution : 2 * error < prefixGap t N) : SamePrefix u v N := by
  apply near_readings_have_same_prefix t u v N
  have h := abs_sub_le (geometricLogReading t u) z (geometricLogReading t v)
  rw [abs_sub_comm z] at h
  linarith

theorem record_character_prefix_error_bound {U : Set Coordinate4} [Nonempty U]
    (t : ℝ) (R S : GravitationalResponseRecord U) (N : ℕ)
    (hp : SamePrefix (recordBits R) (recordBits S) N) :
    |recordCharacter t R - recordCharacter t S| ≤
      regularParameter t / 2 * (1 / 2 : ℝ) ^ N :=
  geometric_reading_prefix_error_bound t (recordBits R) (recordBits S) N hp

theorem near_record_characters_have_same_prefix {U : Set Coordinate4} [Nonempty U]
    (t : ℝ) (R S : GravitationalResponseRecord U) (N : ℕ)
    (hclose : |recordCharacter t R - recordCharacter t S| < prefixGap t N) :
    SamePrefix (recordBits R) (recordBits S) N :=
  near_readings_have_same_prefix t (recordBits R) (recordBits S) N hclose

theorem near_record_characters_same_rational_cut {U : Set Coordinate4} [Nonempty U]
    (t : ℝ) (R S : GravitationalResponseRecord U) (N n : ℕ) (k : RecordComponent) (q : ℚ)
    (hindex : Encodable.encode (n, k, q) < N)
    (hclose : |recordCharacter t R - recordCharacter t S| < prefixGap t N) :
    (recordValue R (TopologicalSpace.denseSeq U n) k < (q : ℝ) ↔
      recordValue S (TopologicalSpace.denseSeq U n) k < (q : ℝ)) := by
  have h := near_record_characters_have_same_prefix t R S N hclose _ hindex
  simpa only [record_bit_at_probe, decide_eq_decide] using h

#print axioms SamePrefix
#print axioms siteGap
#print axioms prefixGap
#print axioms site_gap_positive
#print axioms prefix_gap_positive
#print axioms prefix_gap_le_site_gap
#print axioms binary_code_split_before
#print axioms binary_code_prefix_error
#print axioms reading_difference_eq_code_difference
#print axioms contrast_tail_explicit_bound
#print axioms geometric_reading_prefix_error_bound
#print axioms oriented_first_difference_gap
#print axioms first_difference_reading_gap
#print axioms near_readings_have_same_prefix
#print axioms noisy_candidates_have_same_prefix
#print axioms record_character_prefix_error_bound
#print axioms near_record_characters_have_same_prefix
#print axioms near_record_characters_same_rational_cut
end
end ChatgptAudit.CharacterPrecision
