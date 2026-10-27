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
import TGLExt.MixedGibbsFiniteAccuracy

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit.GibbsWindow
open Matrix TGLExt ChatgptAudit ChatgptAudit.GibbsAccuracy
  ChatgptAudit.MixedGibbsGravity ChatgptAudit.ProbeSource ChatgptAudit.Coherent023
  ChatgptAudit.FiniteResponseRecord ChatgptAudit.FullSourceResponse ChatgptAudit.ResponseError
noncomputable section
variable {J : Type} [Fintype J]

def probeSpeedBudget (w : J → Coordinate4) : ℝ :=
  1 + ∑ i : Fin 10, ∑ j, |covectorRead (w j) (probeDirections i)|

def probeTimeRadius (w : J → Coordinate4) : ℝ := 1 / probeSpeedBudget w

theorem probe_speed_budget_positive (w : J → Coordinate4) : 0 < probeSpeedBudget w := by
  unfold probeSpeedBudget
  positivity

theorem probe_time_radius_positive (w : J → Coordinate4) : 0 < probeTimeRadius w :=
  one_div_pos.mpr (probe_speed_budget_positive w)

theorem probe_speed_le_budget (w : J → Coordinate4) (i : Fin 10) (j : J) :
    |covectorRead (w j) (probeDirections i)| ≤ probeSpeedBudget w := by
  have hj : |covectorRead (w j) (probeDirections i)| ≤
      ∑ j, |covectorRead (w j) (probeDirections i)| :=
    Finset.single_le_sum (f := fun l : J => |covectorRead (w l) (probeDirections i)|)
      (fun _ _ => abs_nonneg _) (Finset.mem_univ j)
  have hi : (∑ j, |covectorRead (w j) (probeDirections i)|) ≤
      ∑ i : Fin 10, ∑ j, |covectorRead (w j) (probeDirections i)| :=
    Finset.single_le_sum (f := fun l : Fin 10 => ∑ j : J, |covectorRead (w j) (probeDirections l)|)
      (fun _ _ => Finset.sum_nonneg (fun _ _ => abs_nonneg _))
      (Finset.mem_univ i)
  have h := hj.trans hi
  unfold probeSpeedBudget
  linarith

theorem probe_clock_window_of_small_time (w : J → Coordinate4) {t : ℝ}
    (ht : |t| ≤ probeTimeRadius w) : ProbeClockWindow w t := by
  intro i j
  have hb := probe_speed_budget_positive w
  have h := mul_le_mul (probe_speed_le_budget w i j) ht (abs_nonneg t) hb.le
  have hc : |covectorRead (w j) (probeDirections i)| * |t| ≤ 1 := by
    simpa [probeTimeRadius,ne_of_gt hb] using h
  have hnon : 0 ≤ |covectorRead (w j) (probeDirections i)| * |t| := by positivity
  have hs : (|covectorRead (w j) (probeDirections i)| * |t|)^2 ≤ 1 := by nlinarith
  simpa only [mul_pow,sq_abs] using hs

theorem nonzero_probe_time_exists (w : J → Coordinate4) :
    ∃ t : ℝ, t≠0 ∧ ProbeClockWindow w t := by
  refine ⟨probeTimeRadius w,ne_of_gt (probe_time_radius_positive w),?_⟩
  apply probe_clock_window_of_small_time
  rw [abs_of_pos (probe_time_radius_positive w)]

theorem noise_truncation_balance {noise C t : ℝ} (ht : t≠0) (hb : C*t^4=noise) :
    noise/t^2+C*t^2=2*C*t^2 := by
  rw [←hb]
  field_simp [ht]
  ring

/-- Finite source reconstruction has a proved nonempty sampling interval for the Gibbs protocol. -/
theorem gibbs_source_error_on_explicit_window (k : J → ℝ) (hk : ∀ j, 0 < k j)
    (w : J → Coordinate4) (g gi : Tensor4) {B G : ℝ} (hB : 0≤B)
    (hg : ∀ i j, |g i j|≤G) (hgi : ∀ i j, |gi i j|≤B) :
    ∃ C : ℝ, 0≤C ∧ ∀ (t noise : ℝ) (observed : ResponseSamples),
      t≠0 → |t|≤probeTimeRadius w → 0≤noise →
      (∀ i, |observed i-gibbsEntropyIncrement k w (probeDirections i) t|≤noise) →
      TensorErrorBound ((1+8*G*B)*(3*(noise/t^2+C*t^2)/(2*Real.pi)))
        (decodeSource g gi (fun i => observed i/t^2))
        (decodeSource g gi (sampleResponse (probeEntropyResponse (fun j => gibbsSlope (k j)) w))) := by
  obtain ⟨C,hC,h⟩ := gibbs_measured_source_error k hk w g gi hB hg hgi
  exact ⟨C,hC,fun t noise observed ht htime hn hobs =>
    h t noise observed ht hn (probe_clock_window_of_small_time w htime) hobs⟩

#print axioms probeSpeedBudget
#print axioms probeTimeRadius
#print axioms probe_speed_budget_positive
#print axioms probe_time_radius_positive
#print axioms probe_speed_le_budget
#print axioms probe_clock_window_of_small_time
#print axioms nonzero_probe_time_exists
#print axioms noise_truncation_balance
#print axioms gibbs_source_error_on_explicit_window
end
end ChatgptAudit.GibbsWindow
