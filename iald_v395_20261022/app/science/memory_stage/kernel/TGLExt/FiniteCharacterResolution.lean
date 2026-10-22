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
import TGLExt.CharacterPrefixStability

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.FiniteCharacterPrecision
open TGLExt ChatgptAudit.CocycleRealization ChatgptAudit.CharacterPrecision
  ChatgptAudit.SelectedAtlas ChatgptAudit.GravitationalRecord
noncomputable section

/-- A finite expression below the gap to the entire infinite tail. -/
def finiteSiteResolution (t : ℝ) (n : ℕ) : ℝ :=
  geometricContrast t n - 2 * geometricContrast t (n + 1)

/-- A finite minimum, using no infinite sum; the zero-prefix convention uses site zero. -/
def finitePrefixResolution (t : ℝ) : ℕ → ℝ
  | 0 => finiteSiteResolution t 0
  | N + 1 => min (finitePrefixResolution t N) (finiteSiteResolution t N)

theorem finite_site_resolution_positive {t : ℝ} (ht : t ≠ 0) (n : ℕ) :
    0 < finiteSiteResolution t n :=
  sub_pos.mpr (geometric_contrast_strict_succ ht n)

theorem finite_site_resolution_le_gap (t : ℝ) (n : ℕ) :
    finiteSiteResolution t n ≤ siteGap t n := by
  have h := geometric_contrast_tail_le t n
  unfold finiteSiteResolution siteGap
  linarith

theorem finite_prefix_resolution_positive {t : ℝ} (ht : t ≠ 0) (N : ℕ) :
    0 < finitePrefixResolution t N := by
  induction N with
  | zero => exact finite_site_resolution_positive ht 0
  | succ N ih => exact lt_min ih (finite_site_resolution_positive ht N)

theorem finite_prefix_resolution_le_gap (t : ℝ) (N : ℕ) :
    finitePrefixResolution t N ≤ prefixGap t N := by
  induction N with
  | zero => exact finite_site_resolution_le_gap t 0
  | succ N ih => exact min_le_min ih (finite_site_resolution_le_gap t N)

theorem finite_threshold_resolves_prefix (t : ℝ) (u v : ℕ → Bool) (N : ℕ)
    (hclose : |geometricLogReading t u - geometricLogReading t v| < finitePrefixResolution t N) :
    SamePrefix u v N :=
  near_readings_have_same_prefix t u v N
    (lt_of_lt_of_le hclose (finite_prefix_resolution_le_gap t N))

theorem finite_threshold_resolves_noisy_candidates (t z error : ℝ)
    (u v : ℕ → Bool) (N : ℕ)
    (hu : |geometricLogReading t u - z| ≤ error)
    (hv : |geometricLogReading t v - z| ≤ error)
    (hresolution : 2 * error < finitePrefixResolution t N) : SamePrefix u v N :=
  noisy_candidates_have_same_prefix t z error u v N hu hv
    (lt_of_lt_of_le hresolution (finite_prefix_resolution_le_gap t N))

theorem finite_threshold_resolves_record_prefix {U : Set Coordinate4} [Nonempty U]
    (t : ℝ) (R S : GravitationalResponseRecord U) (N : ℕ)
    (hclose : |recordCharacter t R - recordCharacter t S| < finitePrefixResolution t N) :
    SamePrefix (recordBits R) (recordBits S) N :=
  finite_threshold_resolves_prefix t (recordBits R) (recordBits S) N hclose

theorem finite_threshold_resolves_record_cut {U : Set Coordinate4} [Nonempty U]
    (t : ℝ) (R S : GravitationalResponseRecord U) (N n : ℕ) (k : RecordComponent) (q : ℚ)
    (hindex : Encodable.encode (n, k, q) < N)
    (hclose : |recordCharacter t R - recordCharacter t S| < finitePrefixResolution t N) :
    (recordValue R (TopologicalSpace.denseSeq U n) k < (q : ℝ) ↔
      recordValue S (TopologicalSpace.denseSeq U n) k < (q : ℝ)) :=
  near_record_characters_same_rational_cut t R S N n k q hindex
    (lt_of_lt_of_le hclose (finite_prefix_resolution_le_gap t N))

#print axioms finiteSiteResolution
#print axioms finitePrefixResolution
#print axioms finite_site_resolution_positive
#print axioms finite_site_resolution_le_gap
#print axioms finite_prefix_resolution_positive
#print axioms finite_prefix_resolution_le_gap
#print axioms finite_threshold_resolves_prefix
#print axioms finite_threshold_resolves_noisy_candidates
#print axioms finite_threshold_resolves_record_prefix
#print axioms finite_threshold_resolves_record_cut
end
end ChatgptAudit.FiniteCharacterPrecision
