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
import TGLExt.BoostMetricPullback

set_option autoImplicit false
set_option maxHeartbeats 12000000
set_option maxRecDepth 4096

namespace ChatgptAudit.Boost044
open Matrix Filter Set TGLExt ChatgptAudit ChatgptAudit.Wave029
  ChatgptAudit.Optical036 ChatgptAudit.Optical043
open scoped Topology ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem scalar_fixed_tensor_jet (f : Coordinate4 → ℝ) (K : Tensor4)
    (x : Coordinate4) (hf : DifferentiableAt ℝ f x) (d : Fin 4) :
    tensorFieldJet (fun y => f y • K) x d=coordinatePartial f x d • K := by
  ext i j
  change coordinatePartial (fun y => f y*K i j) x d=coordinatePartial f x d*K i j
  rw [coordinatePartial_mul f (fun _ => K i j) x hf (differentiableAt_const _) d]
  simp [coordinatePartial]

/-- The complete first spatial jet of the coordinate Lie derivative. -/
theorem boost_metric_lie_first (a c rate : ℝ) (x : Coordinate4) (d : Fin 4) :
    tensorFieldJet
      (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate)) x d =
      (-4*rate*waveTransverse a c x d) • Matrix.vecMulVec waveCovector waveCovector := by
  have he : coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate) =
      (fun y => waveProfile a c y •
        ((-2*rate) • Matrix.vecMulVec waveCovector waveCovector)) := by
    funext y
    rw [boost_metric_lie_formula]
    ext i j
    simp only [Matrix.smul_apply,smul_eq_mul]
    ring
  have hf : DifferentiableAt ℝ (waveProfile a c) x :=
    (wave_profile_smooth a c).differentiable (by simp) x
  rw [he,scalar_fixed_tensor_jet _ _ x hf d,wave_profile_partial]
  ext i j
  fin_cases d <;>
    norm_num [waveTransverse,Pi.single_apply,Matrix.smul_apply,
      Matrix.cons_val_two,Matrix.cons_val_three,Fin.ext_iff]
  all_goals ring

/-- The complete second spatial jet; this is an ordinary derivative of the first jet. -/
theorem boost_metric_lie_second (a c rate : ℝ) (x : Coordinate4) (d e : Fin 4) :
    tensorFieldJet
      (fun y => tensorFieldJet
        (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate)) y d) x e =
      (-4*rate*(if e=d then (if d=1 then a else if d=2 then c else 0) else 0)) •
        Matrix.vecMulVec waveCovector waveCovector := by
  have he : (fun y => tensorFieldJet
      (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate)) y d) =
      (fun y => waveTransverse a c y d •
        ((-4*rate) • Matrix.vecMulVec waveCovector waveCovector)) := by
    funext y
    rw [boost_metric_lie_first]
    ext i j
    simp only [Matrix.smul_apply,smul_eq_mul]
    ring
  have hf : DifferentiableAt ℝ (fun y => waveTransverse a c y d) x := by
    fin_cases d <;> dsimp [waveTransverse] <;> fun_prop
  rw [he,scalar_fixed_tensor_jet _ _ x hf e,wave_transverse_partial]
  ext i j
  simp only [Matrix.smul_apply,smul_eq_mul]
  ring

theorem boost_metric_lie_second_one (a c rate : ℝ) (x : Coordinate4) :
    tensorFieldJet
      (fun y => tensorFieldJet
        (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate)) y 1) x 1 =
      (-4*rate*a) • Matrix.vecMulVec waveCovector waveCovector := by
  simpa using boost_metric_lie_second a c rate x 1 1

theorem boost_metric_lie_second_two (a c rate : ℝ) (x : Coordinate4) :
    tensorFieldJet
      (fun y => tensorFieldJet
        (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate)) y 2) x 2 =
      (-4*rate*c) • Matrix.vecMulVec waveCovector waveCovector := by
  have h := boost_metric_lie_second a c rate x 2 2
  norm_num [Fin.ext_iff] at h
  simpa only [neg_mul,neg_smul] using h

theorem boost_metric_lie_central (a c rate t : ℝ) :
    coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate)
      (centralNullCurve t)=0 := by
  rw [boost_metric_lie_formula]
  simp [waveProfile,centralNullCurve,centralNullDirection]

theorem boost_metric_lie_first_central (a c rate t : ℝ) (d : Fin 4) :
    tensorFieldJet
      (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate))
      (centralNullCurve t) d=0 := by
  rw [boost_metric_lie_first]
  fin_cases d <;> simp [waveTransverse,centralNullCurve,centralNullDirection]

theorem boost_metric_pullback_central (a c rate s t : ℝ) :
    boostMetricPullback a c rate s (centralNullCurve t)=
      frameMetricField (waveSolder a c) (centralNullCurve t) := by
  rw [boost_metric_pullback_formula]
  simp [waveProfile,centralNullCurve,centralNullDirection]

theorem boost_metric_lie_zero_rate (a c : ℝ) (x : Coordinate4) :
    coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField 0) x=0 := by
  rw [boost_metric_lie_formula]
  simp

theorem boost_metric_lie_flat (rate : ℝ) (x : Coordinate4) :
    coordinateMetricLie (frameMetricField (waveSolder 0 0)) (boostField rate) x=0 := by
  rw [boost_metric_lie_formula]
  simp [waveProfile]

theorem boost_metric_pullback_zero_rate (a c s : ℝ) (x : Coordinate4) :
    boostMetricPullback a c 0 s x=frameMetricField (waveSolder a c) x := by
  rw [boost_metric_pullback_formula]
  simp

theorem boost_metric_pullback_flat (rate s : ℝ) (x : Coordinate4) :
    boostMetricPullback 0 0 rate s x=frameMetricField (waveSolder 0 0) x := by
  rw [boost_metric_pullback_formula]
  simp [waveProfile]

/-- This specified boost field is not exactly Killing on any open neighborhood of zero.
The conclusion neither excludes other Killing fields nor asserts an obstruction to
an approximate local boost, a KMS state, or any thermodynamic identification. -/
theorem boost_not_killing_near_origin (a c rate : ℝ)
    (hRate : rate≠0) (hac : a≠0 ∨ c≠0)
    (U : Set Coordinate4) (hU : IsOpen U) (h0 : (0:Coordinate4)∈U) :
    ¬ (∀ x∈U, coordinateMetricLie
      (frameMetricField (waveSolder a c)) (boostField rate) x=0) := by
  intro hK
  have hJ (d : Fin 4) : Set.EqOn
      (fun x => tensorFieldJet
        (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate)) x d)
      (fun _ => (0:Tensor4)) U := by
    intro x hx
    change tensorFieldJet
      (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate)) x d=0
    rw [tensorFieldJet_congr_on U hU
      (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate))
      (fun _ => (0:Tensor4)) (fun y hy => hK y hy) x hx]
    ext i j
    simp [tensorFieldJet,coordinatePartial]
  have hS (d : Fin 4) :
      tensorFieldJet
        (fun x => tensorFieldJet
          (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate)) x d)
        0 d=0 := by
    rw [tensorFieldJet_congr_on U hU _ (fun _ => (0:Tensor4)) (hJ d) 0 h0]
    ext i j
    simp [tensorFieldJet,coordinatePartial]
  rcases hac with ha | hc
  · have hz := congrArg (fun K : Tensor4 => K 0 0) (hS 1)
    rw [boost_metric_lie_second_one] at hz
    norm_num [Matrix.smul_apply,Matrix.vecMulVec,waveCovector] at hz
    exact hz.elim hRate ha
  · have hz := congrArg (fun K : Tensor4 => K 0 0) (hS 2)
    rw [boost_metric_lie_second_two] at hz
    norm_num [Matrix.smul_apply,Matrix.vecMulVec,waveCovector] at hz
    exact hz.elim hRate hc

#print axioms scalar_fixed_tensor_jet
#print axioms boost_metric_lie_first
#print axioms boost_metric_lie_second
#print axioms boost_metric_lie_second_one
#print axioms boost_metric_lie_second_two
#print axioms boost_metric_lie_central
#print axioms boost_metric_lie_first_central
#print axioms boost_metric_pullback_central
#print axioms boost_metric_lie_zero_rate
#print axioms boost_metric_lie_flat
#print axioms boost_metric_pullback_zero_rate
#print axioms boost_metric_pullback_flat
#print axioms boost_not_killing_near_origin
end
end ChatgptAudit.Boost044
