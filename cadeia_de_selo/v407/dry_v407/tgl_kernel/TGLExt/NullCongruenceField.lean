-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_018 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.GeodesicShooting
import TGLExt.ShootingLocalInverse

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Flow018
open Matrix Filter Topology Set ChatgptAudit.Flow016 ChatgptAudit.Flow017
  ChatgptAudit.Screen014 ChatgptAudit.Screen015
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

variable {U : Set Coordinate4} {Gamma : ConnectionField4} {p v : Coordinate4}
  (F : LipschitzLocalFlow (variationalField (geodesicSpray Gamma))
    (variationalDomain (regularPhaseDomain U)) ((p,v),ContinuousLinearMap.id ℝ Phase4))
  (ell : Coordinate4 →L[ℝ] ℝ) (W : VectorField4)
  (C : SmoothLocalChart (shootingPosition F ell W) (shootingDomain F ell W) 0)

def shootingCongruence (x : Coordinate4) : Coordinate4 :=
  shootingVelocity F ell W (C.chart.symm x)

theorem chart_position_inverse (x : Coordinate4) (hx : x∈C.chart.target) :
    shootingPosition F ell W (C.chart.symm x)=x := by
  simpa only [C.map_eq] using C.chart.right_inv hx

theorem congruence_smooth (hU : IsOpen U) (hG : SmoothConnectionOn U Gamma)
    (hW : ContDiffOn ℝ ∞ W U) :
    SmoothVectorOn C.chart.target (shootingCongruence F ell W C) := by
  have hs := (shooting_phase_smooth F ell W hU hG hW).snd
  have hv : ContDiffOn ℝ ∞ (shootingCongruence F ell W C) C.chart.target :=
    hs.comp C.inverse_smooth (fun _ hx => C.source_subset (C.chart.map_target hx))
  exact contDiffOn_pi.1 hv

theorem congruence_target_subset : C.chart.target ⊆ U := by
  intro x hx
  have hr := (shooting_regular F ell W (C.chart.symm x)
    (C.source_subset (C.chart.map_target hx))).1
  rwa [chart_position_inverse F ell W C x hx] at hr

theorem congruence_nonzero (x : Coordinate4) (hx : x∈C.chart.target) :
    shootingCongruence F ell W C x≠0 :=
  (shooting_regular F ell W (C.chart.symm x)
    (C.source_subset (C.chart.map_target hx))).2

theorem congruence_base_mem (hWp : W p=v) : p∈C.chart.target := by
  have hxp : shootingPosition F ell W 0=p :=
    congrArg Prod.fst (shooting_phase_zero F ell W hWp)
  have hpC : C.chart (0:Coordinate4)=p := by rw [C.map_eq]; exact hxp
  simpa only [hpC] using C.chart.map_source C.base_mem

theorem congruence_base_value (hWp : W p=v) :
    shootingCongruence F ell W C p=v := by
  have hxp : shootingPosition F ell W 0=p :=
    congrArg Prod.fst (shooting_phase_zero F ell W hWp)
  change shootingVelocity F ell W (C.chart.symm p)=v
  have hpC : C.chart (0:Coordinate4)=p := by rw [C.map_eq]; exact hxp
  have hi : C.chart.symm p=0 := by
    simpa only [hpC] using C.chart.left_inv C.base_mem
  rw [hi]
  exact congrArg Prod.snd (shooting_phase_zero F ell W hWp)

theorem congruence_null (g : TensorField4) (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hm : MetricCompatibleOn U g Gamma) (hn : ∀ x∈U, tensorQuad (g x) (W x)=0)
    (x : Coordinate4) (hx : x∈C.chart.target) :
    tensorQuad (g x) (shootingCongruence F ell W C x)=0 := by
  have hn' := shooting_null F ell W g hU hg hm hn (C.chart.symm x)
    (C.source_subset (C.chart.map_target hx))
  rwa [chart_position_inverse F ell W C x hx] at hn'

theorem congruence_geodesic (hell : ell v=1) (hU : IsOpen U)
    (hG : SmoothConnectionOn U Gamma) (hW : ContDiffOn ℝ ∞ W U) :
    EqOn (vectorAcceleration Gamma (shootingCongruence F ell W C)) (fun _ => 0)
      C.chart.target := by
  intro x hx
  let V := shootingCongruence F ell W C
  let z := C.chart.symm x
  have hz : z∈C.chart.source := C.chart.map_target hx
  have hzD : z∈shootingDomain F ell W := C.source_subset hz
  let c := fun s : ℝ => shootingPosition F ell W (z+s • v)
  have hcx : c 0=x := by
    simpa only [c,zero_smul,add_zero] using chart_position_inverse F ell W C x hx
  have hc : HasDerivAt c (V (c 0)) 0 := by
    rw [hcx]
    exact shooting_position_along_time F ell W hell z hzD
  have hVD : ∀ a, DifferentiableAt ℝ (fun y => V y a) (c 0) := by
    rw [hcx]
    exact smooth_vector_differentiableAt C.chart.target C.chart.open_target V
      (congruence_smooth F ell W C hU hG hW) x hx
  have h1 := velocity_along_flow_derivative Gamma V c 0 hVD hc
  have heq : (fun s : ℝ => V (c s)) =ᶠ[𝓝 0]
      (fun s : ℝ => shootingVelocity F ell W (z+s • v)) := by
    have ht : ContinuousAt (fun s : ℝ => z+s • v) 0 := by fun_prop
    have he : ∀ᶠ s : ℝ in 𝓝 0, z+s • v∈C.chart.source :=
      ht.eventually (by simpa only [zero_smul,add_zero] using C.chart.open_source.eventually_mem hz)
    filter_upwards [he] with s hs
    change shootingVelocity F ell W
      (C.chart.symm (shootingPosition F ell W (z+s • v)))=_
    have hi : C.chart.symm (shootingPosition F ell W (z+s • v))=z+s • v := by
      simpa only [C.map_eq] using C.chart.left_inv hs
    exact congrArg (shootingVelocity F ell W) hi
  have h2 := shooting_velocity_along_time F ell W hell z hzD
  have hid := h1.unique (h2.congr_of_eventuallyEq heq)
  rw [hcx] at hid
  change (transportGenerator Gamma V x).mulVec (V x)=
    sprayAcceleration Gamma (shootingPosition F ell W z) (V x) at hid
  rw [chart_position_inverse F ell W C x hx] at hid
  change (transportGenerator Gamma V x).mulVec (V x)=
    -((connectionAlong Gamma x (V x)).mulVec (V x)) at hid
  rw [transportGenerator,Matrix.sub_mulVec] at hid
  change (covariantVectorGradient Gamma V x).mulVec (V x)=0
  simpa only [neg_add_cancel] using (sub_eq_iff_eq_add).mp hid

#print axioms chart_position_inverse
#print axioms congruence_smooth
#print axioms congruence_target_subset
#print axioms congruence_nonzero
#print axioms congruence_base_mem
#print axioms congruence_base_value
#print axioms congruence_null
#print axioms congruence_geodesic
end
end ChatgptAudit.Flow018
