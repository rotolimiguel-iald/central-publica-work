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
import TGLExt.SummableGravityBridge

set_option autoImplicit false
set_option maxHeartbeats 6000000
namespace ChatgptAudit.Response028
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021 ChatgptAudit.Coherent023
  ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.Screen014
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def geometricAmplitude : SummableAmplitude where
  value n := (1/24)*(1/2)^n
  nonnegative n := by positivity
  bound n := by
    have hp : (1/2:ℝ)^n≤1 := pow_le_one₀ (by norm_num) (by norm_num)
    nlinarith
  summable := (summable_geometric_of_lt_one (by norm_num : (0:ℝ)≤1/2) (by norm_num)).mul_left (1/24)

def zeroAmplitude : SummableAmplitude where
  value _ := 0
  nonnegative _ := le_rfl
  bound _ := by norm_num
  summable := summable_zero

theorem geometric_amplitude_positive (n : ℕ) : 0<geometricAmplitude.value n := by
  change 0<(1/24:ℝ)*(1/2)^n
  positivity

theorem geometric_amplitude_mass : amplitudeMass geometricAmplitude=1/12 := by
  change (∑' n : ℕ, (1/24:ℝ)*(1/2)^n)=1/12
  rw [tsum_mul_left,tsum_geometric_of_lt_one (by norm_num : (0:ℝ)≤1/2) (by norm_num)]
  norm_num

theorem geometric_amplitude_square_mass : amplitudeSquareMass geometricAmplitude=1/432 := by
  change (∑' n : ℕ, ((1/24:ℝ)*(1/2)^n)^2)=1/432
  have he : ∀ n : ℕ, ((1/24:ℝ)*(1/2)^n)^2=(1/576)*(1/4)^n := by
    intro n
    rw [mul_pow,←pow_mul,Nat.mul_comm n 2,pow_mul]
    norm_num
  simp_rw [he]
  rw [tsum_mul_left,tsum_geometric_of_lt_one (by norm_num : (0:ℝ)≤1/4) (by norm_num)]
  norm_num

theorem geometric_coupling : amplitudeCoupling geometricAmplitude=Real.log 2/(12*Real.pi) := by
  rw [amplitudeCoupling,geometric_amplitude_mass]
  ring

theorem geometric_coupling_positive : 0<amplitudeCoupling geometricAmplitude := by
  rw [geometric_coupling]
  exact div_pos (Real.log_pos (by norm_num)) (by positivity)

theorem geometric_profile_changes_every_site (t : ℝ) (ht : t≠0) (n : ℕ) :
    (amplitudeProfile geometricAmplitude t).w n≠thirdThermalReference.w n := by
  have h : (amplitudeProfile geometricAmplitude t).w n-1/3<0 := by
    rw [amplitude_profile_deviation]
    exact mul_neg_of_neg_of_pos (neg_neg_of_pos (regular_parameter_positive t ht)) (geometric_amplitude_positive n)
  exact ne_of_lt (sub_neg.mp h)

theorem geometric_state_not_reference (t : ℝ) (ht : t≠0) :
    amplitudeState geometricAmplitude t≠omegaState thirdThermalReference := by
  intro he
  have h := congrArg Complex.re (congrFun he
    (towerPi thirdThermalReference (N := 0) (Matrix.single 0 0 (1:ℂ))))
  rw [amplitude_state_local,omegaState_pi,tState_single_diag,tState_single_diag] at h
  exact geometric_profile_changes_every_site t ht 0 h

theorem geometric_joint_entropy {α : Type} {l : Filter α} (frequency : ℝ)
    (cutoff : α → ℕ) (time : α → ℝ) (hN : Tendsto cutoff l atTop)
    (ht : Tendsto time l (𝓝 0)) (hne : ∀ᶠ x in l, time x≠0) :
    Tendsto (fun x => prefixEntropyIncrement thirdThermalReference
      (amplitudeProfile geometricAmplitude (frequency*time x)) (cutoff x)/(time x)^2) l
      (𝓝 (-(Real.log 2/12)*frequency^2)) := by
  have h := amplitude_prefix_entropy_joint geometricAmplitude frequency cutoff time hN ht hne
  have he : amplitudeResponse geometricAmplitude frequency= -(Real.log 2/12)*frequency^2 := by
    rw [amplitudeResponse,geometric_amplitude_mass]
    ring
  rwa [he] at h

theorem site_profiles_eq_of_weights (P Q : SiteProfile) (h : P.w=Q.w) : P=Q := by
  cases P
  cases Q
  cases h
  rfl

theorem zero_amplitude_profile (t : ℝ) : amplitudeProfile zeroAmplitude t=thirdThermalReference := by
  apply site_profiles_eq_of_weights
  funext n
  simp only [amplitudeProfile,zeroAmplitude,thirdThermalReference,zero_mul,sub_zero]

theorem zero_amplitude_state (t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference) :
    amplitudeState zeroAmplitude t A=omegaState thirdThermalReference A := by
  have h : ∀ (Q : SiteProfile) (hp : 0<profileAffinityLimit thirdThermalReference Q),
      Q=thirdThermalReference → globalProfileState thirdThermalReference Q hp A=omegaState thirdThermalReference A := by
    intro Q hp hQ
    subst Q
    unfold globalProfileState
    rw [global_profile_vector_same]
    rfl
  exact h _ _ (zero_amplitude_profile t)

theorem zero_amplitude_response (frequency : ℝ) : amplitudeResponse zeroAmplitude frequency=0 := by
  simp [amplitudeResponse,amplitudeMass,zeroAmplitude]

theorem zero_amplitude_entropy (t : ℝ) : amplitudeEntropyIncrement zeroAmplitude t=0 := by
  have hD : amplitudeRelativeEntropy zeroAmplitude t=0 := by
    unfold amplitudeRelativeEntropy
    rw [zero_amplitude_profile]
    simp [profileRelativeTotal,siteRelativeEntropy,relative_entropy_self]
  rw [amplitudeEntropyIncrement,hD,sub_zero]
  simp [amplitudeModularIncrement,amplitudeMass,zeroAmplitude]

def amplitudeFlatMatter (b : SummableAmplitude) : TensorField4 :=
  frameCovectorStress flatSolder flatSolder constantTimeCovector (amplitudeCoupling b)

theorem amplitude_flat_matter_smooth (b : SummableAmplitude) : SmoothMatrixOn univ (amplitudeFlatMatter b) :=
  frame_covector_stress_smooth univ flatSolder flatSolder constantTimeCovector (amplitudeCoupling b)
    flat_solder_smooth flat_solder_smooth constant_time_smooth

theorem amplitude_flat_matter_conserved (b : SummableAmplitude) : ∀ x∈(univ : Set Coordinate4), ∀ j,
    tensorFieldDivergence (inverseFrameMetricField flatSolder) (frameLeviCivita flatSolder flatSolder)
      (amplitudeFlatMatter b) x j=0 :=
  frame_covector_stress_conserved univ isOpen_univ flatSolder flatSolder constantTimeCovector
    (amplitudeCoupling b) flat_solder_inverse flat_solder_inverse flat_solder_smooth
    flat_solder_smooth constant_time_smooth constant_time_closed constant_time_wave

theorem amplitude_flat_null_value (b : SummableAmplitude) :
    tensorQuad (amplitudeFlatMatter b 0) horizonControlDirection=amplitudeCoupling b := by
  change tensorQuad (covectorStress _ _ _ _) horizonControlDirection=_
  rw [covector_stress_null _ _ _ _ _ flat_control_null]
  norm_num [covectorRead,constantTimeCovector,timeCovector,horizonControlDirection,dotProduct,
    Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]

theorem amplitude_flat_heat_matching (b : SummableAmplitude) :
    Tendsto (fun t => amplitudeHeatDefect b (covectorRead (constantTimeCovector 0) horizonControlDirection)
      1 (constructedHeat flatConstructedScreen (amplitudeFlatMatter b) 1 isOpen_univ
        (frame_metric_smooth univ flatSolder flat_solder_smooth)
        (fun i j => (amplitude_flat_matter_smooth b i j).differentiableOn (by simp))) t/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  amplitude_heat_matching flatConstructedScreen (inverseFrameMetricField flatSolder) constantTimeCovector
    b 1 isOpen_univ (frame_metric_smooth univ flatSolder flat_solder_smooth)
    (fun i j => (amplitude_flat_matter_smooth b i j).differentiableOn (by simp)) flat_control_null

theorem geometric_flat_area_not_matching (eta : ℝ) :
    ¬Tendsto (fun t => amplitudeAreaDefect geometricAmplitude
      (covectorRead (constantTimeCovector 0) horizonControlDirection) eta
      (inducedArea (frameMetricField flatSolder) flatConstructedScreen.curve
        flatConstructedScreen.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) := by
  have hG : SmoothConnectionOn univ (frameLeviCivita flatSolder flatSolder) := by
    rw [flat_connection_zero]
    exact fun _ _ _ => contDiffOn_const
  have ht : ∀ i j k, frameLeviCivita flatSolder flatSolder 0 i k j=
      frameLeviCivita flatSolder flatSolder 0 j k i := by
    simp only [flat_connection_zero,Matrix.zero_apply,implies_true]
  intro hh
  have he := (amplitude_area_matching_iff_ricci flatConstructedScreen
    (inverseFrameMetricField flatSolder) constantTimeCovector geometricAmplitude eta isOpen_univ
    (frame_metric_smooth univ flatSolder flat_solder_smooth) hG ht flat_control_null).mp hh
  change eta*tensorQuad (coordinateRicci (frameLeviCivita flatSolder flatSolder) 0)
    horizonControlDirection=2*Real.pi*tensorQuad (amplitudeFlatMatter geometricAmplitude 0) horizonControlDirection at he
  rw [flat_ricci_zero,amplitude_flat_null_value] at he
  have hp : 0<2*Real.pi*amplitudeCoupling geometricAmplitude := by
    exact mul_pos (mul_pos (by norm_num) Real.pi_pos) geometric_coupling_positive
  have hz : tensorQuad (0 : Tensor4) horizonControlDirection=0 := by simp [tensorQuad]
  rw [hz,mul_zero] at he
  linarith only [he,hp]

#print axioms geometricAmplitude
#print axioms zeroAmplitude
#print axioms geometric_amplitude_positive
#print axioms geometric_amplitude_mass
#print axioms geometric_amplitude_square_mass
#print axioms geometric_coupling
#print axioms geometric_coupling_positive
#print axioms geometric_profile_changes_every_site
#print axioms geometric_state_not_reference
#print axioms geometric_joint_entropy
#print axioms site_profiles_eq_of_weights
#print axioms zero_amplitude_profile
#print axioms zero_amplitude_state
#print axioms zero_amplitude_response
#print axioms zero_amplitude_entropy
#print axioms amplitude_flat_matter_smooth
#print axioms amplitude_flat_matter_conserved
#print axioms amplitude_flat_null_value
#print axioms amplitude_flat_heat_matching
#print axioms geometric_flat_area_not_matching
end
end ChatgptAudit.Response028
