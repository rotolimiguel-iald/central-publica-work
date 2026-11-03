-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_019 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.EquilibriumNullCongruence

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.Flow019
open Matrix Filter Topology Set ChatgptAudit.Screen014
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

structure EquilibriumScreenData (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (p v : Coordinate4) where
  neighborhood : Set Coordinate4
  neighborhood_open : IsOpen neighborhood
  neighborhood_subset : neighborhood⊆U
  point_mem : p∈neighborhood
  velocity : VectorField4
  velocity_smooth : SmoothVectorOn neighborhood velocity
  velocity_at_point : velocity p=v
  velocity_nonzero : ∀ x∈neighborhood, velocity x≠0
  velocity_null : ∀ x∈neighborhood, tensorQuad (g x) (velocity x)=0
  geodesic : EqOn (vectorAcceleration Gamma velocity) (fun _ => 0) neighborhood
  equilibrium_gradient : covariantVectorGradient Gamma velocity p=0
  curve : ℝ → Coordinate4
  curve_zero : curve 0=p
  curve_tangent : HasDerivAt curve v 0
  screen : GeometricScreenAlong g Gamma velocity curve
  screen_gram_zero : screenGram (g p) (screen.vectors 0)= -1
  area_rate : ∀ᶠ t in 𝓝[<] (0:ℝ),
    HasDerivAt (inducedArea g curve screen.vectors)
      (vectorExpansion Gamma velocity (curve t)*inducedArea g curve screen.vectors t) t

def localEquilibriumScreen (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (p v : Coordinate4) (hp : p∈U) (hv : v≠0)
    (hn : tensorQuad (frameMetricField A p) v=0) :
    EquilibriumScreenData U (frameMetricField A) (frameLeviCivita A B) p v := Classical.choice (by
  obtain ⟨N,hN,hNU,hpN,V,hV,hVp,hvN,hnN,hgeo,hgrad⟩ :=
    local_levi_civita_equilibrium_congruence U hU A B hAB hBA hA hB p v hp hv hn
  obtain ⟨curve,hcp,hcv,S,hGram,hArea⟩ :=
    local_levi_civita_transported_screen N hN A B V
      (fun x hx => hAB x (hNU hx)) (fun x hx => hBA x (hNU hx))
      (fun a b => (hA a b).mono hNU) (fun a b => (hB a b).mono hNU)
      hV hnN hgeo p hpN (hvN p hpN)
  exact ⟨{
    neighborhood := N
    neighborhood_open := hN
    neighborhood_subset := hNU
    point_mem := hpN
    velocity := V
    velocity_smooth := hV
    velocity_at_point := hVp
    velocity_nonzero := hvN
    velocity_null := hnN
    geodesic := hgeo
    equilibrium_gradient := hgrad
    curve := curve
    curve_zero := hcp
    curve_tangent := by simpa only [hVp] using hcv
    screen := S
    screen_gram_zero := hGram
    area_rate := hArea }⟩)

theorem equilibrium_screen_expansion_zero (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (p v : Coordinate4) (P : EquilibriumScreenData U g Gamma p v) :
    vectorExpansion Gamma P.velocity p=0 := by
  simp [vectorExpansion,P.equilibrium_gradient]

theorem equilibrium_screen_optical_form_zero (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (p v : Coordinate4) (P : EquilibriumScreenData U g Gamma p v) :
    (P.screen.vectors 0)ᵀ*g p*covariantVectorGradient Gamma P.velocity p*P.screen.vectors 0=0 := by
  simp only [P.equilibrium_gradient,Matrix.mul_zero,Matrix.zero_mul]

theorem equilibrium_screen_area_initial (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (p v : Coordinate4) (P : EquilibriumScreenData U g Gamma p v) :
    inducedArea g P.curve P.screen.vectors 0=1 := by
  rw [inducedArea,P.curve_zero,P.screen_gram_zero,screenArea]
  norm_num [Matrix.det_fin_two]

theorem equilibrium_screen_focusing (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (p v : Coordinate4) (P : EquilibriumScreenData U g Gamma p v)
    (ht : ∀ i j a, Gamma p i a j=Gamma p j a i) :
    HasDerivAt (fun t => vectorExpansion Gamma P.velocity (P.curve t))
      (-tensorQuad (coordinateRicci Gamma p) v) 0 := by
  have hh := curve_expansion_focusing P.neighborhood P.neighborhood_open Gamma P.velocity
    (fun i a b => (hG i a b).mono P.neighborhood_subset) P.velocity_smooth P.geodesic
    p P.point_mem ht P.equilibrium_gradient P.curve P.curve_zero
    (by simpa only [P.velocity_at_point] using P.curve_tangent)
  simpa only [P.velocity_at_point] using hh

theorem local_equilibrium_screen_with_focusing (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (p v : Coordinate4) (hp : p∈U) (hv : v≠0)
    (hn : tensorQuad (frameMetricField A p) v=0) :
    ∃ P : EquilibriumScreenData U (frameMetricField A) (frameLeviCivita A B) p v,
      vectorExpansion (frameLeviCivita A B) P.velocity p=0 ∧
      inducedArea (frameMetricField A) P.curve P.screen.vectors 0=1 ∧
      HasDerivAt (fun t => vectorExpansion (frameLeviCivita A B) P.velocity (P.curve t))
        (-tensorQuad (coordinateRicci (frameLeviCivita A B) p) v) 0 := by
  let P := localEquilibriumScreen U hU A B hAB hBA hA hB p v hp hv hn
  have hg := frame_metric_smooth U A hA
  have hG : SmoothConnectionOn U (frameLeviCivita A B) :=
    levi_civita_field_smooth U hU (frameMetricField A) (inverseFrameMetricField B)
      hg (inverse_frame_metric_smooth U B hB)
  have ht := levi_civita_field_torsion_free U hU (frameMetricField A) (inverseFrameMetricField B)
    (fun x _ => frame_metric_symmetric A x)
  exact ⟨P,equilibrium_screen_expansion_zero _ _ _ p v P,
    equilibrium_screen_area_initial _ _ _ p v P,
    equilibrium_screen_focusing U _ _ hG p v P (ht p hp)⟩

#print axioms localEquilibriumScreen
#print axioms equilibrium_screen_expansion_zero
#print axioms equilibrium_screen_optical_form_zero
#print axioms equilibrium_screen_area_initial
#print axioms equilibrium_screen_focusing
#print axioms local_equilibrium_screen_with_focusing
end
end ChatgptAudit.Flow019
