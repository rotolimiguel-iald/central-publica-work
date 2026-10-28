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
import TGLExt.HarmonicEnergyObstruction

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Response028
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

structure SummableAmplitude where
  value : ℕ → ℝ
  nonnegative : ∀ n, 0 ≤ value n
  bound : ∀ n, value n≤1/12
  summable : Summable value

def amplitudeMass (b : SummableAmplitude) : ℝ := ∑' n, b.value n
def amplitudeSquareMass (b : SummableAmplitude) : ℝ := ∑' n, (b.value n)^2
def regularParameter (t : ℝ) : ℝ := t^2/(1+t^2)

theorem amplitude_square_summable (b : SummableAmplitude) :
    Summable (fun n => (b.value n)^2) := by
  apply Summable.of_nonneg_of_le (fun _ => sq_nonneg _) _ b.summable
  intro n
  have hn := b.nonnegative n
  have hb := b.bound n
  nlinarith

theorem amplitude_mass_nonnegative (b : SummableAmplitude) : 0 ≤ amplitudeMass b :=
  tsum_nonneg b.nonnegative

theorem amplitude_square_mass_nonnegative (b : SummableAmplitude) : 0 ≤ amplitudeSquareMass b :=
  tsum_nonneg (fun _ => sq_nonneg _)

theorem amplitude_prefix_le_mass (b : SummableAmplitude) (N : ℕ) :
    (∑ n∈Finset.range (N+1), b.value n)≤amplitudeMass b :=
  b.summable.sum_le_tsum _ (fun n _ => b.nonnegative n)

theorem amplitude_square_prefix_le_mass (b : SummableAmplitude) (N : ℕ) :
    (∑ n∈Finset.range (N+1), (b.value n)^2)≤amplitudeSquareMass b :=
  (amplitude_square_summable b).sum_le_tsum _ (fun _ _ => sq_nonneg _)

theorem amplitude_prefix_tendsto (b : SummableAmplitude) :
    Tendsto (fun N => ∑ n∈Finset.range (N+1), b.value n) atTop (𝓝 (amplitudeMass b)) :=
  b.summable.hasSum.tendsto_sum_nat.comp (tendsto_add_atTop_nat 1)

theorem regular_parameter_nonnegative (t : ℝ) : 0 ≤ regularParameter t := by
  unfold regularParameter
  positivity

theorem regular_parameter_lt_one (t : ℝ) : regularParameter t<1 := by
  unfold regularParameter
  apply (div_lt_one (by positivity : 0<1+t^2)).mpr
  linarith

theorem regular_parameter_le_square (t : ℝ) : regularParameter t≤t^2 := by
  unfold regularParameter
  apply (div_le_iff₀ (by positivity : 0<1+t^2)).mpr
  nlinarith [sq_nonneg (t^2)]

theorem regular_parameter_zero : regularParameter 0=0 := by norm_num [regularParameter]

theorem regular_parameter_positive (t : ℝ) (ht : t≠0) : 0<regularParameter t := by
  exact div_pos (sq_pos_of_ne_zero ht) (by positivity)

def amplitudeProfile (b : SummableAmplitude) (t : ℝ) : SiteProfile where
  w n := 1/3-b.value n*regularParameter t
  pos n := by
    have hm := mul_le_of_le_one_right (b.nonnegative n) (regular_parameter_lt_one t).le
    have hb := b.bound n
    linarith
  lt_one n := by
    have hn := mul_nonneg (b.nonnegative n) (regular_parameter_nonnegative t)
    linarith

theorem amplitude_profile_deviation (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    (amplitudeProfile b t).w n-1/3= -regularParameter t*b.value n := by
  change 1/3-b.value n*regularParameter t-1/3=_
  ring

theorem amplitude_profile_square_summable (b : SummableAmplitude) (t : ℝ) :
    Summable (fun n => ((amplitudeProfile b t).w n-1/3)^2) := by
  apply ((amplitude_square_summable b).mul_left ((regularParameter t)^2)).congr
  intro n
  rw [amplitude_profile_deviation]
  ring

theorem amplitude_profile_affinity_positive (b : SummableAmplitude) (t : ℝ) :
    0<profileAffinityLimit thirdThermalReference (amplitudeProfile b t) := by
  apply profile_square_summable_positive _ _ (9/4)
  · intro n
    exact binary_third_affinity_bound _ ((amplitudeProfile b t).pos n) ((amplitudeProfile b t).lt_one n)
  · apply (amplitude_profile_square_summable b t).congr
    intro n
    change ((amplitudeProfile b t).w n-1/3)^2=(1/3-(amplitudeProfile b t).w n)^2
    ring

def amplitudeVector (b : SummableAmplitude) (t : ℝ) : TowerHilbert thirdThermalReference :=
  globalProfileVector _ _ (amplitude_profile_affinity_positive b t)

def amplitudeState (b : SummableAmplitude) (t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference) : ℂ :=
  globalProfileState _ _ (amplitude_profile_affinity_positive b t) A

def amplitudeUnitary (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert (amplitudeProfile b t) ≃ₗᵢ[ℂ] TowerHilbert thirdThermalReference :=
  profileGNSUnitary _ _ (amplitude_profile_affinity_positive b t)

theorem amplitude_vector_norm (b : SummableAmplitude) (t : ℝ) : ‖amplitudeVector b t‖=1 :=
  global_profile_vector_norm _ _ _

theorem amplitude_state_local (b : SummableAmplitude) (t : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    amplitudeState b t (towerPi thirdThermalReference a)=tState (amplitudeProfile b t) N a :=
  global_profile_state_local _ _ _ N a

theorem amplitude_state_faithful (b : SummableAmplitude) (t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A∈theFactorObject thirdThermalReference) (hz : amplitudeState b t (star A*A)=0) : A=0 :=
  global_profile_state_faithful _ _ _ A hA hz

theorem amplitude_unitary_omega (b : SummableAmplitude) (t : ℝ) :
    amplitudeUnitary b t (hOmega (amplitudeProfile b t))=amplitudeVector b t :=
  profile_gns_unitary_omega _ _ _

#print axioms amplitude_square_summable
#print axioms amplitude_mass_nonnegative
#print axioms amplitude_square_mass_nonnegative
#print axioms amplitude_prefix_le_mass
#print axioms amplitude_square_prefix_le_mass
#print axioms amplitude_prefix_tendsto
#print axioms regular_parameter_nonnegative
#print axioms regular_parameter_lt_one
#print axioms regular_parameter_le_square
#print axioms regular_parameter_zero
#print axioms regular_parameter_positive
#print axioms amplitudeProfile
#print axioms amplitude_profile_deviation
#print axioms amplitude_profile_square_summable
#print axioms amplitude_profile_affinity_positive
#print axioms amplitudeVector
#print axioms amplitudeState
#print axioms amplitudeUnitary
#print axioms amplitude_vector_norm
#print axioms amplitude_state_local
#print axioms amplitude_state_faithful
#print axioms amplitude_unitary_omega
end
end ChatgptAudit.Response028
