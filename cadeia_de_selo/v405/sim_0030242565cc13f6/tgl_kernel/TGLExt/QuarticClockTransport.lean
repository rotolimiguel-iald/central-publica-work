-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_037 (06/09/2026), transposta em 06/09/2026
-- Lote 035..037 (processo da ORDEM_008 cumprido pela bancada: zero instancias anonimas, lote compilado junto
--   num diretorio limpo). 035: DEFORMACOES OBSERVAVEIS e AREA DE FISHER — derivadas da conjugacao unitaria e
--   do estado, observaveis de Pauli por sitio na torre real, duas leituras independentes (jacobiano nao
--   degenerado), medicao conjunta efetiva (sitios distintos), probabilidades normalizadas e suas derivadas,
--   matriz de Fisher na origem, densidade de area de Fisher (4/9 como area de coordenadas). 036: AREA OPTICA e
--   LIBERDADE RADIATIVA — a area induzida dos campos de Jacobi da metrica 029 ligada a curvatura real
--   (A2(0) = -Ric(d,d); A4(0) = 2(tr K)^2 - 2 tr(K_TF^T K_TF)); germes de area distintos para shears
--   distintos. 037: QUARTA ORDEM, AREA e RELOGIO — limites entropicos e de area em 4a ordem; NEGATIVO
--   MEDIDO: o casamento adicional em 4a ordem com parametro comum fixo FALHA (delta4 >= (7/48) B > 0);
--   a reparametrizacao do relogio t + lambda t^3 cancela o defeito ate 4a ordem (controle do relogio relativo).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: X, Y, sitios e normalizacao sao INPUT; a familia optica
--   lorentziana e INPUT; identificacao da inscricao angular com area fisica, retorno estabilizador, ponte
--   regiao-algebra, escala, assinatura, dinamica gravitacional e H3 geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 14/14, 8/8 (via manifesto), 10/10; manifestos
--   1051/977; 3/3 auditores exit 0; recompilacao INDEPENDENTE 15/15, axiomas no trio; guarda de colisao;
--   enunciados lidos. Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito: zero anonimas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Topology.Order.Basic
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.Quartic037
open Filter
open scoped Topology
noncomputable section

def cubicClock (lam t : ℝ) : ℝ := t + lam * t^3

theorem cubic_clock_zero (lam : ℝ) : cubicClock lam 0 = 0 := by
  simp [cubicClock]

theorem cubic_clock_factor (lam t : ℝ) :
    cubicClock lam t = t * (1 + lam * t^2) := by
  unfold cubicClock
  ring

theorem cubic_clock_hasDerivAt_zero (lam : ℝ) :
    HasDerivAt (cubicClock lam) 1 0 := by
  have hpow : HasDerivAt (fun t : ℝ => t^3)
      ((3 : ℝ) * (0 : ℝ)^(3-1) * 1) 0 :=
    HasDerivAt.pow (hasDerivAt_id (0 : ℝ)) 3
  have hscaled : HasDerivAt (fun t : ℝ => lam * t^3)
      (lam * ((3 : ℝ) * (0 : ℝ)^(3-1) * 1)) 0 :=
    HasDerivAt.const_mul lam hpow
  have h : HasDerivAt (cubicClock lam)
      (1 + lam * ((3 : ℝ) * (0 : ℝ)^(3-1) * 1)) 0 :=
    HasDerivAt.add (hasDerivAt_id (0 : ℝ)) hscaled
  simpa using h

theorem cubic_clock_factor_tendsto (lam : ℝ) :
    Tendsto (fun t : ℝ => 1 + lam * t^2) (𝓝 0) (𝓝 1) := by
  have hc : Continuous (fun t : ℝ => 1 + lam * t^2) := by fun_prop
  simpa using (hc.continuousAt (x := 0)).tendsto

theorem cubic_clock_factor_positive (lam : ℝ) :
    ∀ᶠ t : ℝ in 𝓝 0, 0 < 1 + lam * t^2 :=
  (cubic_clock_factor_tendsto lam).eventually (lt_mem_nhds (by norm_num))

theorem punctured_time_nonzero : ∀ᶠ t : ℝ in 𝓝[≠] 0, t ≠ 0 := by
  filter_upwards [self_mem_nhdsWithin] with t ht
  simpa using ht

theorem cubic_clock_nonzero (lam : ℝ) :
    ∀ᶠ t : ℝ in 𝓝[≠] 0, cubicClock lam t ≠ 0 := by
  filter_upwards [(cubic_clock_factor_positive lam).filter_mono nhdsWithin_le_nhds,
    punctured_time_nonzero] with t hp ht
  rw [cubic_clock_factor]
  exact mul_ne_zero ht (ne_of_gt hp)

theorem cubic_clock_preserves_negative (lam : ℝ) :
    ∀ᶠ t : ℝ in 𝓝 0, t < 0 → cubicClock lam t < 0 := by
  filter_upwards [cubic_clock_factor_positive lam] with t hp ht
  rw [cubic_clock_factor]
  exact mul_neg_of_neg_of_pos ht hp

theorem cubic_clock_tendsto_zero (lam : ℝ) :
    Tendsto (cubicClock lam) (𝓝[≠] 0) (𝓝 0) := by
  have h := (cubic_clock_hasDerivAt_zero lam).continuousAt.tendsto
  rw [cubic_clock_zero] at h
  exact h.mono_left nhdsWithin_le_nhds

theorem cubic_clock_tendsto_punctured (lam : ℝ) :
    Tendsto (cubicClock lam) (𝓝[≠] 0) (𝓝[≠] 0) := by
  refine tendsto_nhdsWithin_iff.mpr ⟨cubic_clock_tendsto_zero lam, ?_⟩
  simpa using cubic_clock_nonzero lam

theorem cubic_clock_fourth_ratio (lam t : ℝ) (ht : t ≠ 0) :
    (cubicClock lam t)^4 / t^4 = (1 + lam*t^2)^4 := by
  rw [cubic_clock_factor, mul_pow]
  field_simp

theorem cubic_clock_quadratic_correction (lam t : ℝ) (ht : t ≠ 0) :
    ((cubicClock lam t)^2 - t^2) / t^4 = 2*lam + lam^2*t^2 := by
  rw [cubic_clock_factor]
  field_simp
  ring

theorem cubic_clock_fourth_ratio_limit (lam : ℝ) :
    Tendsto (fun t : ℝ => (cubicClock lam t)^4 / t^4) (𝓝[≠] 0) (𝓝 1) := by
  have hfactor : Tendsto (fun t : ℝ => 1 + lam * t^2) (𝓝[≠] 0) (𝓝 1) :=
    (cubic_clock_factor_tendsto lam).mono_left nhdsWithin_le_nhds
  have h := hfactor.pow 4
  have he : (fun t : ℝ => (cubicClock lam t)^4 / t^4) =ᶠ[𝓝[≠] 0]
      (fun t : ℝ => (1 + lam*t^2)^4) := by
    filter_upwards [punctured_time_nonzero] with t ht
    exact cubic_clock_fourth_ratio lam t ht
  exact (Filter.tendsto_congr' he).mpr (by simpa using h)

theorem cubic_clock_quadratic_correction_limit (lam : ℝ) :
    Tendsto (fun t : ℝ => ((cubicClock lam t)^2-t^2)/t^4)
      (𝓝[≠] 0) (𝓝 (2*lam)) := by
  have hc : Continuous (fun t : ℝ => 2*lam + lam^2*t^2) := by fun_prop
  have h : Tendsto (fun t : ℝ => 2*lam + lam^2*t^2) (𝓝[≠] 0) (𝓝 (2*lam)) := by
    simpa using (hc.continuousAt (x := 0)).tendsto.mono_left nhdsWithin_le_nhds
  have he : (fun t : ℝ => ((cubicClock lam t)^2-t^2)/t^4) =ᶠ[𝓝[≠] 0]
      (fun t : ℝ => 2*lam + lam^2*t^2) := by
    filter_upwards [punctured_time_nonzero] with t ht
    exact cubic_clock_quadratic_correction lam t ht
  exact (Filter.tendsto_congr' he).mpr h

theorem quartic_remainder_clock_transport (f : ℝ → ℝ) (a C lam : ℝ)
    (hf : Tendsto (fun t : ℝ => (f t-a*t^2)/t^4) (𝓝[≠] 0) (𝓝 C)) :
    Tendsto (fun t : ℝ => (f (cubicClock lam t)-a*t^2)/t^4)
      (𝓝[≠] 0) (𝓝 (C+2*a*lam)) := by
  have hbase := hf.comp (cubic_clock_tendsto_punctured lam)
  have h := (hbase.mul (cubic_clock_fourth_ratio_limit lam)).add
    ((cubic_clock_quadratic_correction_limit lam).const_mul a)
  have hlim : C * 1 + a * (2 * lam) = C + 2*a*lam := by ring
  rw [hlim] at h
  have h' : Tendsto
      (fun t : ℝ => ((f (cubicClock lam t)-a*(cubicClock lam t)^2)/(cubicClock lam t)^4) *
          ((cubicClock lam t)^4/t^4) +
        a*(((cubicClock lam t)^2-t^2)/t^4))
      (𝓝[≠] 0) (𝓝 (C+2*a*lam)) := by
    simpa only [Function.comp_def] using h
  apply h'.congr'
  filter_upwards [punctured_time_nonzero, cubic_clock_nonzero lam] with t ht hp
  field_simp [ht, hp]
  ring

theorem quartic_coefficient_clock_invariant (f : ℝ → ℝ) (C lam : ℝ)
    (hf : Tendsto (fun t : ℝ => f t/t^4) (𝓝[≠] 0) (𝓝 C)) :
    Tendsto (fun t : ℝ => f (cubicClock lam t)/t^4) (𝓝[≠] 0) (𝓝 C) := by
  simpa using quartic_remainder_clock_transport f 0 C lam (by simpa using hf)

theorem common_clock_preserves_quartic_defect (f g : ℝ → ℝ) (C lam : ℝ)
    (h : Tendsto (fun t : ℝ => (f t-g t)/t^4) (𝓝[≠] 0) (𝓝 C)) :
    Tendsto (fun t : ℝ => (f (cubicClock lam t)-g (cubicClock lam t))/t^4)
      (𝓝[≠] 0) (𝓝 C) :=
  quartic_coefficient_clock_invariant (fun t => f t-g t) C lam h

#print axioms cubicClock
#print axioms cubic_clock_zero
#print axioms cubic_clock_factor
#print axioms cubic_clock_hasDerivAt_zero
#print axioms cubic_clock_factor_tendsto
#print axioms cubic_clock_factor_positive
#print axioms punctured_time_nonzero
#print axioms cubic_clock_nonzero
#print axioms cubic_clock_preserves_negative
#print axioms cubic_clock_tendsto_zero
#print axioms cubic_clock_tendsto_punctured
#print axioms cubic_clock_fourth_ratio
#print axioms cubic_clock_quadratic_correction
#print axioms cubic_clock_fourth_ratio_limit
#print axioms cubic_clock_quadratic_correction_limit
#print axioms quartic_remainder_clock_transport
#print axioms quartic_coefficient_clock_invariant
#print axioms common_clock_preserves_quartic_defect
end
end ChatgptAudit.Quartic037
