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
import TGLExt.BinaryRelativeQuartic
import Mathlib.Analysis.Normed.Group.Tannery

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace ChatgptAudit.Quartic037

open Filter Topology Set TGLExt ChatgptAudit.Micro021 ChatgptAudit.Response028

noncomputable section

/- These are limits of the existing global states and their existing entropy.
No moving finite cutoff is asserted here. Centering a finite-cutoff entropy by
the full amplitudeMass at fourth order would require quantitative tail control,
or a different centering using the mass actually retained by the cutoff. -/

theorem amplitude_relative_as_binary_sum (b : SummableAmplitude) (t : ℝ) :
    amplitudeRelativeEntropy b t = ∑' n, binaryRelativeAt (b.value n) t := rfl

theorem amplitude_relative_quartic_sum (b : SummableAmplitude) (t : ℝ) :
    amplitudeRelativeEntropy b t / t ^ 4 =
      ∑' n, binaryRelativeAt (b.value n) t / t ^ 4 := by
  rw [amplitude_relative_as_binary_sum, tsum_div_const]

theorem amplitude_relative_quartic_limit (b : SummableAmplitude) :
    Tendsto (fun t : ℝ => amplitudeRelativeEntropy b t / t ^ 4)
      (𝓝[≠] 0) (𝓝 ((9 / 4) * amplitudeSquareMass b)) := by
  have hbound : ∀ᶠ t : ℝ in 𝓝[≠] 0, ∀ n : ℕ,
      ‖binaryRelativeAt (b.value n) t / t ^ 4‖ ≤ (9 / 2) * (b.value n) ^ 2 := by
    apply Filter.Eventually.of_forall
    intro t n
    obtain ⟨h0, h1⟩ := binary_relative_quartic_bound (b.value n)
      (b.nonnegative n) (b.bound n) t
    simpa only [Real.norm_eq_abs, abs_of_nonneg h0] using h1
  have h : Tendsto
      (fun t : ℝ => ∑' n, binaryRelativeAt (b.value n) t / t ^ 4)
      (𝓝[≠] 0) (𝓝 (∑' n, (9 / 4) * (b.value n) ^ 2)) :=
    tendsto_tsum_of_dominated_convergence
      ((amplitude_square_summable b).mul_left (9 / 2))
      (fun n => binary_relative_quartic_limit (b.value n)) hbound
  have hsum : (∑' n, (9 / 4) * (b.value n) ^ 2) =
      (9 / 4) * amplitudeSquareMass b := by
    rw [tsum_mul_left]
    rfl
  rw [hsum] at h
  apply h.congr'
  exact Filter.Eventually.of_forall (fun t => (amplitude_relative_quartic_sum b t).symm)

theorem amplitude_entropy_quartic_identity (b : SummableAmplitude) (t : ℝ) (ht : t ≠ 0) :
    (amplitudeEntropyIncrement b t + Real.log 2 * amplitudeMass b * t ^ 2) / t ^ 4 =
      Real.log 2 * amplitudeMass b / (1 + t ^ 2) -
        amplitudeRelativeEntropy b t / t ^ 4 := by
  have hd : 1 + t ^ 2 ≠ 0 := ne_of_gt (by positivity : 0 < 1 + t ^ 2)
  unfold amplitudeEntropyIncrement amplitudeModularIncrement regularParameter
  field_simp [ht, hd]; ring

theorem amplitude_entropy_quartic_limit (b : SummableAmplitude) :
    Tendsto
      (fun t : ℝ => (amplitudeEntropyIncrement b t +
        Real.log 2 * amplitudeMass b * t ^ 2) / t ^ 4)
      (𝓝[≠] 0)
      (𝓝 (Real.log 2 * amplitudeMass b - (9 / 4) * amplitudeSquareMass b)) := by
  have hden : Tendsto (fun t : ℝ => 1 + t ^ 2) (𝓝[≠] 0) (𝓝 (1 : ℝ)) := by
    simpa only [zero_pow (by decide : 2 ≠ 0), add_zero] using
      (quartic_time_tendsto_zero.pow 2).const_add 1
  have hconst : Tendsto (fun _ : ℝ => Real.log 2 * amplitudeMass b)
      (𝓝[≠] 0) (𝓝 (Real.log 2 * amplitudeMass b)) := tendsto_const_nhds
  have hmod : Tendsto (fun t : ℝ => Real.log 2 * amplitudeMass b / (1 + t ^ 2))
      (𝓝[≠] 0) (𝓝 (Real.log 2 * amplitudeMass b)) := by
    have hq := hconst.div hden (by norm_num : (1 : ℝ) ≠ 0)
    change Tendsto (fun t : ℝ => Real.log 2 * amplitudeMass b / (1 + t ^ 2))
      (𝓝[≠] 0) (𝓝 ((Real.log 2 * amplitudeMass b) / 1)) at hq
    simpa only [div_one] using hq
  have h := hmod.sub (amplitude_relative_quartic_limit b)
  apply h.congr'
  filter_upwards [quartic_punctured_time_nonzero] with t ht
  exact (amplitude_entropy_quartic_identity b t ht).symm

theorem amplitude_square_mass_le_mass_twelfth (b : SummableAmplitude) :
    amplitudeSquareMass b ≤ amplitudeMass b / 12 := by
  have hterm (n : ℕ) : (b.value n) ^ 2 ≤ b.value n / 12 := by
    have hn := b.nonnegative n
    have hb := b.bound n
    nlinarith
  have hsum : Summable (fun n => b.value n / 12) := by
    simpa only [div_eq_mul_inv] using b.summable.mul_right ((12 : ℝ)⁻¹)
  have h := (amplitude_square_summable b).tsum_le_tsum hterm hsum
  simpa only [tsum_div_const, amplitudeSquareMass, amplitudeMass] using h

#print axioms amplitude_relative_as_binary_sum
#print axioms amplitude_relative_quartic_sum
#print axioms amplitude_relative_quartic_limit
#print axioms amplitude_entropy_quartic_identity
#print axioms amplitude_entropy_quartic_limit
#print axioms amplitude_square_mass_le_mass_twelfth

end

end ChatgptAudit.Quartic037
