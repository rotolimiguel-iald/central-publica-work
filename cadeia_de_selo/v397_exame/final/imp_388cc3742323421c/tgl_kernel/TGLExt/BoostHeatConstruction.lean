-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_044 (06/09/2026), transposta em 06/09/2026
-- Lote 044..045 (ORDEM_008 cumprida). 044: BOOST APROXIMADO e orientacao do calor — o peso -kappa t realizado
--   por um campo de boost chi = -kappa u d_u + kappa v d_v e seu fluxo (grupo, inversa, jacobiano); pullback da
--   metrica e defeito de Lie -2kappa(aX^2+cY^2)du^2 (zera com o 1o jato na central); controle negativo: nao e
--   Killing em aberto se kappa != 0 e (a,c) != 0; T(chi,d) = -kappa t T(d,d); Q_boost = opticalHeat041 globalmente,
--   = opticalScreenHeat043 como germe; orientacao do passado certificada (calor e area invertem sinal juntos).
--   045 (resposta a ORDEM_010): swapHorizon P p hp i j — troca de sitios no perfil estacionario e um TowerHorizon
--   por prova (unitario, normaliza M, preserva omega); permutacoes finitas com lei de grupo e covariancia das
--   esperancas estacionaria/tracial (horizontes algebricos; identificacao fisica OPEN); shift unilateral NAO
--   construido; aperiodico OPEN (rota Cesaro nomeada); StateClock: classe cinematica (origem, derivada 1, jato) —
--   DICOTOMIA: para todo relogio comum g alguma tela falha (duas telas sigma = 0, r/4, mesmo estado e Ricci:
--   diferenca dos residuos/t^4 -> +eta r^2/96), cada tela isolada admite relogio que cancela a 4a ordem;
--   area: covariancia por horizontes NAO fixa a normalizacao (h e alpha h ambos invariantes; area x alpha).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: familia, carta e kappa sao INPUT; kappa/(2pi) e normalizacao
--   herdada (sem Unruh/KMS); H3 fisico, lei finita geral, ponte regiao-algebra, shift e aperiodico OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10 + 8/8; 2/2 auditores exit 0;
--   recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito). As fontes v329 (gerencia) NAO sao
--   reincorporadas: a bancada as recompilou como dependencia, sem novidade contada.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.BoostMetricJets

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Boost044
open Matrix Filter Set TGLExt ChatgptAudit ChatgptAudit.Flow019 ChatgptAudit.Flow020
  ChatgptAudit.Wave029 ChatgptAudit.Optical036 ChatgptAudit.Heat041 ChatgptAudit.Optical043
open scoped Topology
noncomputable section

/-- Boost energy flux on the literal central Jacobi pencil. -/
def boostEnergyFlux (a c rate : ℝ) (T : TensorField4) (t : ℝ) : ℝ :=
  tensorPair (T (centralNullCurve t)) (boostField rate (centralNullCurve t))
    centralNullDirection * geometricJacobiArea a c t

theorem boost_energy_contraction (rate t : ℝ) (A : Tensor4) :
    tensorPair A (boostField rate (centralNullCurve t)) centralNullDirection =
      (-rate*t)*tensorQuad A centralNullDirection := by
  rw [boost_field_central]
  simp only [tensorPair,tensorQuad,dotProduct,Pi.smul_apply,smul_eq_mul,
    Finset.mul_sum,mul_assoc]

theorem boost_energy_flux_formula (a c rate : ℝ) (T : TensorField4) (t : ℝ) :
    boostEnergyFlux a c rate T t =
      -rate*t*tensorQuad (T (centralNullCurve t)) centralNullDirection *
        geometricJacobiArea a c t := by
  unfold boostEnergyFlux
  rw [boost_energy_contraction]

/-- The current agrees with the existing screen flux for every tensor field. -/
theorem boost_energy_flux_constructed (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate : ℝ) (T : TensorField4) (t : ℝ) :
    boostEnergyFlux a c rate T t =
      screenHeatFlux (opticalEquilibriumScreen a c ha hc) T rate t := by
  unfold screenHeatFlux
  rw [optical_equilibrium_velocity_central a c ha hc t]
  change boostEnergyFlux a c rate T t =
    -rate*t*tensorQuad (T (centralNullCurve t)) centralNullDirection *
      geometricJacobiArea a c t
  exact boost_energy_flux_formula a c rate T t

theorem wave_matter_pair (a c mass : ℝ) (x u v : Coordinate4) :
    tensorPair (waveMatter a c mass x) u v =
      mass*(dotProduct waveCovector u)*(dotProduct waveCovector v) := by
  rw [wave_matter_formula]
  simp [tensorPair,Matrix.mulVec,dotProduct,vecMulVec,waveCovector,
    Fin.sum_univ_four,Matrix.smul_apply,Matrix.cons_val_two,Matrix.cons_val_three]
  ring

/-- This contraction holds off the central ray for the special null source;
it does not identify the two vector fields there. -/
theorem boost_wave_contraction (a c rate mass : ℝ) (x : Coordinate4) :
    tensorPair (waveMatter a c mass x) (boostField rate x) (opticalNullVelocity a c x) =
      -rate*opticalPhaseCoordinate x*mass := by
  have hV : dotProduct waveCovector (opticalNullVelocity a c x) = 1 := by
    simpa [dotProduct,waveCovector,Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]
      using optical_null_velocity_frequency a c x
  rw [wave_matter_pair,boost_field_frequency,hV]
  ring

theorem boost_energy_flux_wave (a c rate mass t : ℝ) :
    boostEnergyFlux a c rate (waveMatter a c mass) t =
      opticalHeatFlux a c rate mass t := by
  rw [boost_energy_flux_formula,wave_matter_quad]
  have hw : ChatgptAudit.Coherent023.covectorRead waveCovector centralNullDirection = 1 :=
    central_direction_frequency
  simp only [hw,one_pow,mul_one,opticalHeatFlux]

def boostEnergyHeat (a c rate : ℝ) (T : TensorField4) (t : ℝ) : ℝ :=
  ∫ s in (0:ℝ)..t, boostEnergyFlux a c rate T s

theorem boost_energy_heat_wave (a c rate mass t : ℝ) :
    boostEnergyHeat a c rate (waveMatter a c mass) t = opticalHeat a c rate mass t := by
  unfold boostEnergyHeat opticalHeat
  apply intervalIntegral.integral_congr
  intro s _
  exact boost_energy_flux_wave a c rate mass s

theorem boost_energy_heat_constructed (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass : ℝ) :
    boostEnergyHeat a c rate (waveMatter a c mass) =ᶠ[𝓝[<] (0:ℝ)]
      opticalScreenHeat a c ha hc rate mass := by
  filter_upwards [optical_screen_heat_germ a c ha hc rate mass] with t ht
  rw [boost_energy_heat_wave]
  exact ht.symm

/-- Orientation from the past endpoint to the origin, as in a physical segment integral. -/
def boostSegmentHeat (a c rate : ℝ) (T : TensorField4) (t : ℝ) : ℝ :=
  ∫ s in t..(0:ℝ), boostEnergyFlux a c rate T s

theorem boost_segment_heat_orientation (a c rate : ℝ) (T : TensorField4) (t : ℝ) :
    boostSegmentHeat a c rate T t = -boostEnergyHeat a c rate T t := by
  unfold boostSegmentHeat boostEnergyHeat
  exact intervalIntegral.integral_symm (0:ℝ) t

theorem boost_segment_heat_wave (a c rate mass t : ℝ) :
    boostSegmentHeat a c rate (waveMatter a c mass) t = -opticalHeat a c rate mass t := by
  rw [boost_segment_heat_orientation,boost_energy_heat_wave]

theorem boost_segment_heat_constructed (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass : ℝ) :
    boostSegmentHeat a c rate (waveMatter a c mass) =ᶠ[𝓝[<] (0:ℝ)]
      (fun t => -opticalScreenHeat a c ha hc rate mass t) := by
  filter_upwards [boost_energy_heat_constructed a c ha hc rate mass] with t ht
  rw [boost_segment_heat_orientation,ht]

theorem boost_energy_flux_nonnegative (a c rate mass t : ℝ)
    (hrate : 0 ≤ rate) (hmass : 0 ≤ mass) (ht : t ≤ 0) :
    0≤boostEnergyFlux a c rate (waveMatter a c mass) t := by
  rw [boost_energy_flux_wave]
  unfold opticalHeatFlux
  have hp : 0≤ -rate*t :=
    mul_nonneg_of_nonpos_of_nonpos (neg_nonpos.mpr hrate) ht
  have hA : 0≤geometricJacobiArea a c t := by
    rw [geometric_jacobi_area_abs]
    exact abs_nonneg _
  exact mul_nonneg (mul_nonneg hp hmass) hA

theorem boost_segment_heat_nonnegative (a c rate mass t : ℝ)
    (hrate : 0 ≤ rate) (hmass : 0 ≤ mass) (ht : t ≤ 0) :
    0≤boostSegmentHeat a c rate (waveMatter a c mass) t := by
  unfold boostSegmentHeat
  apply intervalIntegral.integral_nonneg ht
  intro s hs
  exact boost_energy_flux_nonnegative a c rate mass s hrate hmass hs.2

/-- Both heat and area use the same past-to-origin orientation. -/
def boostSegmentArea (a c t : ℝ) : ℝ :=
  geometricJacobiArea a c 0-geometricJacobiArea a c t

/-- The normalization rate/(2*pi) is inherited, not derived as a temperature. -/
def boostSegmentDefect (a c rate mass eta t : ℝ) : ℝ :=
  boostSegmentHeat a c rate (waveMatter a c mass) t -
    (rate/(2*Real.pi)*eta)*boostSegmentArea a c t

theorem boost_segment_defect_orientation (a c rate mass eta t : ℝ) :
    boostSegmentDefect a c rate mass eta t = -opticalClausiusDefect a c rate mass eta t := by
  unfold boostSegmentDefect boostSegmentArea
  rw [boost_segment_heat_wave,geometric_jacobi_area_zero]
  unfold opticalClausiusDefect
  ring

theorem boost_segment_defect_constructed (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) :
    boostSegmentDefect a c rate mass eta =ᶠ[𝓝[<] (0:ℝ)]
      (fun t => -opticalScreenClausiusDefect a c ha hc rate mass eta t) := by
  filter_upwards [optical_screen_clausius_germ a c ha hc rate mass eta] with t ht
  rw [boost_segment_defect_orientation,ht]

theorem boost_segment_quadratic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) :
    Tendsto (fun t => boostSegmentDefect a c rate mass eta t/t^2) (𝓝[<] 0)
      (𝓝 (-(rate*(eta*(a+c)-2*Real.pi*mass)/(4*Real.pi)))) := by
  have h := (optical_screen_clausius_quadratic_limit a c ha hc rate mass eta).neg
  have he : (fun t => boostSegmentDefect a c rate mass eta t/t^2) =ᶠ[𝓝[<] (0:ℝ)]
      (fun t => -(opticalScreenClausiusDefect a c ha hc rate mass eta t/t^2)) := by
    filter_upwards [boost_segment_defect_constructed a c ha hc rate mass eta] with t ht
    simp only [ht,neg_div]
  exact (tendsto_congr' he).2 h

theorem boost_segment_quadratic_balance_iff (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) (hrate : rate≠0) :
    Tendsto (fun t => boostSegmentDefect a c rate mass eta t/t^2) (𝓝[<] 0) (𝓝 0) ↔
      eta*(a+c)=2*Real.pi*mass := by
  have he : (fun t => boostSegmentDefect a c rate mass eta t/t^2) =ᶠ[𝓝[<] (0:ℝ)]
      (fun t => -(opticalScreenClausiusDefect a c ha hc rate mass eta t/t^2)) := by
    filter_upwards [boost_segment_defect_constructed a c ha hc rate mass eta] with t ht
    simp only [ht,neg_div]
  rw [← optical_screen_quadratic_balance_iff a c ha hc rate mass eta hrate]
  constructor
  · intro h
    have hn := ((tendsto_congr' he).1 h).neg
    simpa only [neg_neg,neg_zero] using hn
  · intro h
    apply (tendsto_congr' he).2
    simpa only [neg_zero] using h.neg

#print axioms boostEnergyFlux
#print axioms boost_energy_contraction
#print axioms boost_energy_flux_formula
#print axioms boost_energy_flux_constructed
#print axioms wave_matter_pair
#print axioms boost_wave_contraction
#print axioms boost_energy_flux_wave
#print axioms boostEnergyHeat
#print axioms boost_energy_heat_wave
#print axioms boost_energy_heat_constructed
#print axioms boostSegmentHeat
#print axioms boost_segment_heat_orientation
#print axioms boost_segment_heat_wave
#print axioms boost_segment_heat_constructed
#print axioms boost_energy_flux_nonnegative
#print axioms boost_segment_heat_nonnegative
#print axioms boostSegmentArea
#print axioms boostSegmentDefect
#print axioms boost_segment_defect_orientation
#print axioms boost_segment_defect_constructed
#print axioms boost_segment_quadratic_limit
#print axioms boost_segment_quadratic_balance_iff
end
end ChatgptAudit.Boost044
