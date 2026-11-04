-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_028 (06/09/2026), transposta em 06/09/2026
-- Lote 027..028: EQUIVALENCIA UNITARIA entre os GNS de perfis com afinidade positiva e o TRANSPORTE
--   MODULAR com dominios — Tomita do estado global Phi no Hilbert original (grafo fechado, S, J, Delta,
--   JS = Delta^{1/2} positivo auto-adjunto), grupo modular fortemente continuo que preserva fator e
--   estado, instancia nao trivial (perfil gradual: autovalor transportado 5/7); RESPOSTA GLOBAL finita
--   sem corte (familia de amplitude somavel, fiel), limite conjunto corte/tempo, contraexemplo
--   HARMONICO (entropia relativa finita com incremento modular e entropia DIVERGENTES);
--   einstein_from_summable_area_matching (condicional). Estatuto [REAL / INPUT / OPEN]: a lei de area
--   microscopica NAO foi derivada da torre (controle plano o impede); selecao fisica, H3 dinamico,
--   assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 20/20 + 20/20; manifestos 231/238;
--   2/2 auditores da bancada exit 0; recompilacao INDEPENDENTE 16/16, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.SummableProfileCurve

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Response028
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

def amplitudeModularIncrement (b : SummableAmplitude) (t : ℝ) : ℝ :=
  -Real.log 2*amplitudeMass b*regularParameter t

def amplitudeRelativeEntropy (b : SummableAmplitude) (t : ℝ) : ℝ :=
  profileRelativeTotal thirdThermalReference (amplitudeProfile b t)

def amplitudeEntropyIncrement (b : SummableAmplitude) (t : ℝ) : ℝ :=
  amplitudeModularIncrement b t-amplitudeRelativeEntropy b t

def amplitudeReadWeights (b : SummableAmplitude) (t : ℝ) (N : ℕ) (i : chainIdx N) : ℝ :=
  (amplitudeState b t (towerPi thirdThermalReference (Matrix.single i i (1:ℂ)))).re

theorem amplitude_read_weights (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    amplitudeReadWeights b t N=towerW (amplitudeProfile b t) N := by
  funext i
  rw [amplitudeReadWeights,amplitude_state_local,tState_single_diag]
  rfl

theorem amplitude_read_entropy (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    finiteEntropy (amplitudeReadWeights b t N)-finiteEntropy (towerW thirdThermalReference N)=
      prefixEntropyIncrement thirdThermalReference (amplitudeProfile b t) N := by
  rw [amplitude_read_weights]
  rfl

theorem amplitude_state_generator (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    amplitudeState b t (towerPi thirdThermalReference (diagonalModularGenerator (towerW thirdThermalReference N)))=
      (referenceEnergy (towerW thirdThermalReference N) (towerW (amplitudeProfile b t) N):ℂ) := by
  rw [amplitude_state_local]
  simp only [tState,diagonalModularGenerator,Matrix.diagonal_apply_eq,referenceEnergy,
    Complex.ofReal_sum,Complex.ofReal_mul]

theorem reference_state_generator (P : SiteProfile) (N : ℕ) :
    omegaState P (towerPi P (diagonalModularGenerator (towerW P N)))=(finiteEntropy (towerW P N):ℂ) := by
  rw [omegaState_pi]
  exact (entropy_diagonal_modular_expectation _).symm

theorem amplitude_read_modular_increment (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    (amplitudeState b t (towerPi thirdThermalReference (diagonalModularGenerator (towerW thirdThermalReference N)))-
      omegaState thirdThermalReference (towerPi thirdThermalReference
        (diagonalModularGenerator (towerW thirdThermalReference N)))).re=
      prefixModularIncrement thirdThermalReference (amplitudeProfile b t) N := by
  rw [amplitude_state_generator,reference_state_generator,Complex.sub_re]
  exact (modular_increment_energy _ _).symm

theorem amplitude_deviation_summable (b : SummableAmplitude) (t : ℝ) :
    Summable (fun n => (amplitudeProfile b t).w n-1/3) := by
  simpa only [amplitude_profile_deviation] using b.summable.mul_left (-regularParameter t)

theorem amplitude_relative_summable (b : SummableAmplitude) (t : ℝ) :
    Summable (siteRelativeEntropy thirdThermalReference (amplitudeProfile b t)) :=
  third_relative_sites_summable _ (amplitude_profile_square_summable b t)

theorem amplitude_prefix_modular_formula (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    prefixModularIncrement thirdThermalReference (amplitudeProfile b t) N=
      -Real.log 2*(∑ n∈Finset.range (N+1), b.value n)*regularParameter t := by
  rw [third_prefix_modular_formula]
  simp only [amplitude_profile_deviation,←Finset.mul_sum]
  ring

theorem amplitude_modular_tendsto (b : SummableAmplitude) (t : ℝ) :
    Tendsto (prefixModularIncrement thirdThermalReference (amplitudeProfile b t)) atTop
      (𝓝 (amplitudeModularIncrement b t)) := by
  have h := third_prefix_modular_tendsto (amplitudeProfile b t) (amplitude_deviation_summable b t)
  have he : Real.log 2*(∑' n, ((amplitudeProfile b t).w n-1/3))=amplitudeModularIncrement b t := by
    simp only [amplitude_profile_deviation,tsum_mul_left,amplitudeModularIncrement,amplitudeMass]
    ring
  rwa [he] at h

theorem amplitude_relative_tendsto (b : SummableAmplitude) (t : ℝ) :
    Tendsto (prefixRelativeEntropy thirdThermalReference (amplitudeProfile b t)) atTop
      (𝓝 (amplitudeRelativeEntropy b t)) :=
  prefix_relative_tendsto _ _ (amplitude_relative_summable b t)

theorem amplitude_entropy_tendsto (b : SummableAmplitude) (t : ℝ) :
    Tendsto (prefixEntropyIncrement thirdThermalReference (amplitudeProfile b t)) atTop
      (𝓝 (amplitudeEntropyIncrement b t)) :=
  prefix_entropy_tendsto _ _ _ (amplitude_modular_tendsto b t) (amplitude_relative_summable b t)

theorem amplitude_relative_nonnegative (b : SummableAmplitude) (t : ℝ) :
    0 ≤ amplitudeRelativeEntropy b t := profile_relative_total_nonnegative _ _

theorem amplitude_relative_bound (b : SummableAmplitude) (t : ℝ) :
    amplitudeRelativeEntropy b t≤(9/2)*(regularParameter t)^2*amplitudeSquareMass b := by
  have h := third_relative_total_bound (amplitudeProfile b t) (amplitude_profile_square_summable b t)
  have he : (∑' n, ((amplitudeProfile b t).w n-1/3)^2)=
      (regularParameter t)^2*amplitudeSquareMass b := by
    simp only [amplitude_profile_deviation,mul_pow,neg_sq,tsum_mul_left,amplitudeSquareMass]
  rw [he] at h
  simpa only [amplitudeRelativeEntropy,mul_assoc] using h

theorem amplitude_prefix_relative_bound (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    0 ≤ prefixRelativeEntropy thirdThermalReference (amplitudeProfile b t) N ∧
      prefixRelativeEntropy thirdThermalReference (amplitudeProfile b t) N≤
        (9/2)*(regularParameter t)^2*amplitudeSquareMass b :=
  ⟨prefix_relative_nonnegative _ _ _,
    (prefix_relative_le_total _ _ (amplitude_relative_summable b t) N).trans (amplitude_relative_bound b t)⟩

theorem amplitude_modular_zero (b : SummableAmplitude) : amplitudeModularIncrement b 0=0 := by
  rw [amplitudeModularIncrement,regular_parameter_zero,mul_zero]

theorem amplitude_relative_zero (b : SummableAmplitude) : amplitudeRelativeEntropy b 0=0 := by
  have h := amplitude_relative_bound b 0
  rw [regular_parameter_zero] at h
  norm_num at h
  exact le_antisymm h (amplitude_relative_nonnegative b 0)

theorem amplitude_entropy_zero (b : SummableAmplitude) : amplitudeEntropyIncrement b 0=0 := by
  rw [amplitudeEntropyIncrement,amplitude_modular_zero,amplitude_relative_zero,sub_self]

theorem amplitude_read_entropy_tendsto (b : SummableAmplitude) (t : ℝ) :
    Tendsto (fun N => finiteEntropy (amplitudeReadWeights b t N)-finiteEntropy (towerW thirdThermalReference N))
      atTop (𝓝 (amplitudeEntropyIncrement b t)) := by
  simpa only [amplitude_read_entropy] using amplitude_entropy_tendsto b t

#print axioms amplitude_read_weights
#print axioms amplitude_read_entropy
#print axioms amplitude_state_generator
#print axioms reference_state_generator
#print axioms amplitude_read_modular_increment
#print axioms amplitude_deviation_summable
#print axioms amplitude_relative_summable
#print axioms amplitude_prefix_modular_formula
#print axioms amplitude_modular_tendsto
#print axioms amplitude_relative_tendsto
#print axioms amplitude_entropy_tendsto
#print axioms amplitude_relative_nonnegative
#print axioms amplitude_relative_bound
#print axioms amplitude_prefix_relative_bound
#print axioms amplitude_modular_zero
#print axioms amplitude_relative_zero
#print axioms amplitude_entropy_zero
#print axioms amplitude_read_entropy_tendsto
end
end ChatgptAudit.Response028
