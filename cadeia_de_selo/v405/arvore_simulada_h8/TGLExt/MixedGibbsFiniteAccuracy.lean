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
import TGLExt.FiniteResponseErrorBounds
import Mathlib.Analysis.Calculus.Taylor

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit.GibbsAccuracy
open Set Matrix TGLExt ChatgptAudit ChatgptAudit.MixedQuadraticGibbs
  ChatgptAudit.MixedGibbsGravity ChatgptAudit.ProbeSource
  ChatgptAudit.Coherent023 ChatgptAudit.FiniteResponseRecord
  ChatgptAudit.FullSourceResponse ChatgptAudit.ResponseError
open scoped ContDiff
noncomputable section
variable {J : Type} [Fintype J]

theorem mixed_entropy_smooth {k : ℝ} (hk : 0 < k) :
    ContDiff ℝ ∞ (fun s => finiteEntropy (mixedWeights k s)) := by
  unfold finiteEntropy entropyAtom
  apply ContDiff.sum
  intro i _
  exact ((mixed_weights_smooth hk i).mul
    ((mixed_weights_smooth hk i).log (fun s => ne_of_gt (mixed_weights_interior hk s i).1))).neg

theorem first_order_taylor_interval_bound (f : ℝ → ℝ) (a : ℝ)
    (hf : ContDiff ℝ ∞ f) (hderiv : HasDerivAt f a 0) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ s ∈ Icc (0 : ℝ) 1, |f s-f 0-a*s| ≤ C*s^2 := by
  have hd : derivWithin f (Icc (0 : ℝ) 1) 0 = a :=
    hderiv.hasDerivWithinAt.derivWithin
      ((uniqueDiffOn_Icc (show (0 : ℝ)<1 by norm_num)) 0 (by simp))
  have ht (s : ℝ) : taylorWithinEval f 1 (Icc (0 : ℝ) 1) 0 s = f 0 + s*a := by
    rw [show (1 : ℕ)=0+1 from rfl,taylorWithinEval_succ]
    simp [iteratedDerivWithin_one,hd]
  obtain ⟨C,hC⟩ := exists_taylor_mean_remainder_bound (n:=1)
    (show (0 : ℝ)≤1 by norm_num) (hf.of_le (ENat.natCast_le_of_coe_top_le_withTop le_rfl 2)).contDiffOn
  refine ⟨max C 0,le_max_right _ _,fun s hs => ?_⟩
  have h := hC s hs
  rw [ht,Real.norm_eq_abs] at h
  calc
    |f s-f 0-a*s| = |f s-(f 0+s*a)| := by congr 1; ring
    _ ≤ C*s^2 := by simpa using h
    _ ≤ max C 0*s^2 := mul_le_mul_of_nonneg_right (le_max_left _ _) (sq_nonneg s)

theorem mixed_entropy_parameter_remainder {k : ℝ} (hk : 0 < k) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ s ∈ Icc (0 : ℝ) 1,
      |finiteEntropy (mixedWeights k s)-finiteEntropy (mixedBase k)-
        (-k/Real.cosh k^2)*s| ≤ C*s^2 := by
  have h := first_order_taylor_interval_bound _ _ (mixed_entropy_smooth hk)
    (mixed_entropy_first_jet hk)
  have hz : mixedWeights k 0=mixedBase k := funext (mixed_weights_zero hk)
  simpa only [hz] using h

theorem quadratic_entropy_remainder {k : ℝ} (hk : 0 < k) (velocity : ℝ) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ t : ℝ, velocity^2*t^2 ≤ 1 →
      |finiteEntropy (quadraticWeights k velocity t)-finiteEntropy (mixedBase k)-
        (-k/Real.cosh k^2*velocity^2)*t^2| ≤ C*t^4 := by
  obtain ⟨C,hC,h⟩ := mixed_entropy_parameter_remainder hk
  refine ⟨C*velocity^4,by positivity,fun t ht => ?_⟩
  have hs := h (velocity^2*t^2) ⟨by positivity,ht⟩
  simpa only [quadraticWeights,mul_pow,←pow_mul,mul_assoc] using hs

theorem finite_gibbs_entropy_remainder (k : J → ℝ) (hk : ∀ j, 0 < k j)
    (w : J → Coordinate4) (d : Coordinate4) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ t : ℝ, (∀ j, (covectorRead (w j) d)^2*t^2 ≤ 1) →
      |gibbsEntropyIncrement k w d t-
        probeEntropyResponse (fun j => gibbsSlope (k j)) w d*t^2| ≤ C*t^4 := by
  choose C hC h using fun j => quadratic_entropy_remainder (hk j) (covectorRead (w j) d)
  refine ⟨∑ j,C j,Finset.sum_nonneg (fun j _ => hC j),fun t ht => ?_⟩
  simp only [gibbsEntropyIncrement,probeEntropyResponse,
    gibbs_response_coefficient _ _ (hk _),Finset.sum_mul,←Finset.sum_sub_distrib]
  exact (Finset.abs_sum_le_sum_abs _ _).trans
    (Finset.sum_le_sum (fun j _ => h j t (ht j)))

def ProbeClockWindow (w : J → Coordinate4) (t : ℝ) : Prop :=
  ∀ i : Fin 10, ∀ j, (covectorRead (w j) (probeDirections i))^2*t^2 ≤ 1

theorem ten_probe_gibbs_remainder (k : J → ℝ) (hk : ∀ j, 0 < k j)
    (w : J → Coordinate4) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ t : ℝ, ProbeClockWindow w t → ∀ i : Fin 10,
      |gibbsEntropyIncrement k w (probeDirections i) t-
        sampleResponse (probeEntropyResponse (fun j => gibbsSlope (k j)) w) i*t^2| ≤ C*t^4 := by
  choose C hC h using fun i : Fin 10 => finite_gibbs_entropy_remainder k hk w (probeDirections i)
  refine ⟨∑ i,C i,Finset.sum_nonneg (fun i _ => hC i),fun t ht i => ?_⟩
  exact (h i t (ht i)).trans (mul_le_mul_of_nonneg_right
    (Finset.single_le_sum (fun j _ => hC j) (Finset.mem_univ i)) (by positivity))

/-- The quartic truncation error is derived for the actual Gibbs protocol; noise is an input bound. -/
theorem gibbs_measured_source_error (k : J → ℝ) (hk : ∀ j, 0 < k j)
    (w : J → Coordinate4) (g gi : Tensor4) {B G : ℝ} (hB : 0≤B)
    (hg : ∀ i j, |g i j|≤G) (hgi : ∀ i j, |gi i j|≤B) :
    ∃ C : ℝ, 0≤C ∧ ∀ (t noise : ℝ) (observed : ResponseSamples),
      t≠0 → 0≤noise → ProbeClockWindow w t →
      (∀ i, |observed i-gibbsEntropyIncrement k w (probeDirections i) t|≤noise) →
      TensorErrorBound ((1+8*G*B)*(3*(noise/t^2+C*t^2)/(2*Real.pi)))
        (decodeSource g gi (fun i => observed i/t^2))
        (decodeSource g gi (sampleResponse (probeEntropyResponse (fun j => gibbsSlope (k j)) w))) := by
  obtain ⟨C,hC,h⟩ := ten_probe_gibbs_remainder k hk w
  refine ⟨C,hC,fun t noise observed ht hn hw hobs => ?_⟩
  exact measured_source_error ht hn hC hB g gi hg hgi observed
    (fun i => gibbsEntropyIncrement k w (probeDirections i) t) _ hobs (h t hw)

#print axioms mixed_entropy_smooth
#print axioms first_order_taylor_interval_bound
#print axioms mixed_entropy_parameter_remainder
#print axioms quadratic_entropy_remainder
#print axioms finite_gibbs_entropy_remainder
#print axioms ProbeClockWindow
#print axioms ten_probe_gibbs_remainder
#print axioms gibbs_measured_source_error
end
end ChatgptAudit.GibbsAccuracy
