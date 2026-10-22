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
set_option maxHeartbeats 1000000
namespace ChatgptAudit.RecordMeshPrecision
open Filter Topology Set TGLExt ChatgptAudit.SelectedAtlas
  ChatgptAudit.GravitationalRecord ChatgptAudit.CharacterPrecision
noncomputable section
variable {U : Set Coordinate4} [Nonempty U]

/-- A resolved pair of rational cuts bounds the second record at an actual dense probe. -/
theorem close_character_preserves_probe_interval
    (t : ℝ) (R S : GravitationalResponseRecord U) (N n : ℕ)
    (k : RecordComponent) (lower upper : ℚ)
    (hlowIndex : Encodable.encode (n, k, lower) < N)
    (huppIndex : Encodable.encode (n, k, upper) < N)
    (hclose : |recordCharacter t R - recordCharacter t S| < prefixGap t N)
    (hlow : (lower : ℝ) ≤ recordValue R (TopologicalSpace.denseSeq U n) k)
    (hupp : recordValue R (TopologicalSpace.denseSeq U n) k < (upper : ℝ)) :
    (lower : ℝ) ≤ recordValue S (TopologicalSpace.denseSeq U n) k ∧
      recordValue S (TopologicalSpace.denseSeq U n) k < (upper : ℝ) := by
  have hlo := near_record_characters_same_rational_cut t R S N n k lower hlowIndex hclose
  have hup := near_record_characters_same_rational_cut t R S N n k upper huppIndex hclose
  constructor
  · exact le_of_not_gt (fun hs => (not_lt_of_ge hlow) (hlo.mpr hs))
  · exact hup.mp hupp

theorem close_character_controls_probe_value
    (t : ℝ) (R S : GravitationalResponseRecord U) (N n : ℕ)
    (k : RecordComponent) (lower upper : ℚ) (error : ℝ)
    (hlowIndex : Encodable.encode (n, k, lower) < N)
    (huppIndex : Encodable.encode (n, k, upper) < N)
    (hclose : |recordCharacter t R - recordCharacter t S| < prefixGap t N)
    (hlow : (lower : ℝ) ≤ recordValue R (TopologicalSpace.denseSeq U n) k)
    (hupp : recordValue R (TopologicalSpace.denseSeq U n) k < (upper : ℝ))
    (hwidth : (upper : ℝ) - (lower : ℝ) ≤ error) :
    |recordValue R (TopologicalSpace.denseSeq U n) k -
      recordValue S (TopologicalSpace.denseSeq U n) k| ≤ error := by
  obtain ⟨hslo, hsupp⟩ := close_character_preserves_probe_interval
    t R S N n k lower upper hlowIndex huppIndex hclose hlow hupp
  exact abs_le.mpr ⟨by linarith, by linarith⟩

omit [Nonempty U] in
/-- Finite sample control propagates under a shared, explicit spatial Lipschitz bound. -/
theorem record_mesh_error_from_samples (R S : GravitationalResponseRecord U)
    (K : Set U) (M : ℕ) (samples : Fin M → U) (L radius error : ℝ)
    (hL : 0 ≤ L)
    (hR : ∀ x y : U, ∀ k, |recordValue R x k - recordValue R y k| ≤ L * dist x y)
    (hS : ∀ x y : U, ∀ k, |recordValue S x k - recordValue S y k| ≤ L * dist x y)
    (hcover : ∀ x ∈ K, ∃ j : Fin M, dist x (samples j) ≤ radius)
    (hsamples : ∀ j : Fin M, ∀ k,
      |recordValue R (samples j) k - recordValue S (samples j) k| ≤ error) :
    ∀ x ∈ K, ∀ k, |recordValue R x k - recordValue S x k| ≤ error + 2 * L * radius := by
  intro x hx k
  obtain ⟨j, hj⟩ := hcover x hx
  have hbound := mul_le_mul_of_nonneg_left hj hL
  have hr := (hR x (samples j) k).trans hbound
  have hs := (hS x (samples j) k).trans hbound
  have hc := hsamples j k
  have htriangle1 := abs_sub_le (recordValue R x k) (recordValue R (samples j) k)
    (recordValue S x k)
  have htriangle2 := abs_sub_le (recordValue R (samples j) k)
    (recordValue S (samples j) k) (recordValue S x k)
  rw [abs_sub_comm (recordValue S (samples j) k)] at htriangle2
  linarith

/-- Actual character proximity yields a uniform finite-mesh error for record components.
It does not create a physical metric, the mesh, regularity, or a noisy decoder outside the image. -/
theorem near_characters_control_record_fields_on_mesh
    (t : ℝ) (R S : GravitationalResponseRecord U) (N M : ℕ) (K : Set U)
    (L radius error : ℝ) (lower upper : Fin M → RecordComponent → ℚ)
    (hL : 0 ≤ L)
    (hR : ∀ x y : U, ∀ k, |recordValue R x k - recordValue R y k| ≤ L * dist x y)
    (hS : ∀ x y : U, ∀ k, |recordValue S x k - recordValue S y k| ≤ L * dist x y)
    (hcover : ∀ x ∈ K, ∃ j : Fin M,
      dist x (TopologicalSpace.denseSeq U j.val) ≤ radius)
    (hlowIndex : ∀ j : Fin M, ∀ k, Encodable.encode (j.val, k, lower j k) < N)
    (huppIndex : ∀ j : Fin M, ∀ k, Encodable.encode (j.val, k, upper j k) < N)
    (hclose : |recordCharacter t R - recordCharacter t S| < prefixGap t N)
    (hlow : ∀ j : Fin M, ∀ k,
      (lower j k : ℝ) ≤ recordValue R (TopologicalSpace.denseSeq U j.val) k)
    (hupp : ∀ j : Fin M, ∀ k,
      recordValue R (TopologicalSpace.denseSeq U j.val) k < (upper j k : ℝ))
    (hwidth : ∀ j : Fin M, ∀ k, (upper j k : ℝ) - (lower j k : ℝ) ≤ error) :
    ∀ x ∈ K, ∀ k, |recordValue R x k - recordValue S x k| ≤ error + 2 * L * radius := by
  apply record_mesh_error_from_samples R S K M
    (fun j => TopologicalSpace.denseSeq U j.val) L radius error hL hR hS hcover
  intro j k
  exact close_character_controls_probe_value t R S N j.val k (lower j k) (upper j k)
    error (hlowIndex j k) (huppIndex j k) hclose (hlow j k) (hupp j k) (hwidth j k)

#print axioms close_character_preserves_probe_interval
#print axioms close_character_controls_probe_value
#print axioms record_mesh_error_from_samples
#print axioms near_characters_control_record_fields_on_mesh
end
end ChatgptAudit.RecordMeshPrecision
