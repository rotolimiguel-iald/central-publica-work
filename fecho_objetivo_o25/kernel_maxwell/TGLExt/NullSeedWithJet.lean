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
import TGLExt.PrescribedCovariantJet

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.Flow019
open Matrix Filter Topology Set ChatgptAudit.Flow018 ChatgptAudit.Screen014
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem null_companion_of_frame (g : Tensor4) (v : Coordinate4)
    (F : Screen013.NormalizedNullFrame g v) :
    ∃ n : Coordinate4, tensorQuad g n=0 ∧ tensorPair g v n= -1 := by
  let n := fun a => F.frame a 1
  refine ⟨n,?_,?_⟩
  · have h := congrArg (fun M : Tensor4 => M 1 1) F.gram
    rw [frame_pair_entry] at h
    change tensorQuad g n=0 at h
    exact h
  · simpa [nullScreenGram] using normalized_initial_pair g v F 1

theorem null_seed_with_companion (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (hg : SmoothMatrixOn U g)
    (hm : MetricCompatibleOn U g Gamma) (hgs : ∀ x∈U, (g x)ᵀ=g x)
    (n : VectorField4) (hns : SmoothVectorOn U n)
    (hnn : ∀ x∈U, tensorQuad (g x) (n x)=0)
    (p v : Coordinate4) (hp : p∈U) (hnv : tensorQuad (g p) v=0)
    (hpair : tensorPair (g p) v (n p)≠0) :
    ∃ D : Set Coordinate4, IsOpen D ∧ D⊆U ∧ p∈D ∧
      ∃ W : VectorField4, SmoothVectorOn D W ∧ W p=v ∧
        (∀ x∈D, tensorQuad (g x) (W x)=0) ∧
        HasFDerivAt W (connectionInitialJet Gamma p v) p ∧
        covariantVectorGradient Gamma W p=0 := by
  let R := affineInitialSeed Gamma p v
  have hRp : R p=v := affine_seed_initial Gamma p v
  let D := interior {x | x∈U ∧ tensorPair (g x) (R x) (n x)≠0}
  let W := fun x => nullCorrection (g x) (R x) (n x)
  have hR : SmoothVectorOn U R := contDiffOn_pi.1 (affine_seed_smooth Gamma p v).contDiffOn
  have hb := tensor_pair_smooth U g R n hg hR hns
  have hbp : tensorPair (g p) (R p) (n p)≠0 := by
    simpa only [R,affine_seed_initial] using hpair
  have hbc := ((hb p hp).contDiffAt (hU.mem_nhds hp)).continuousAt
  have hpD : p∈D := by
    apply mem_interior_iff_mem_nhds.2
    have he : ∀ᶠ x in 𝓝 p, tensorPair (g x) (R x) (n x)≠0 :=
      hbc.eventually_ne hbp
    filter_upwards [hU.mem_nhds hp,he] with x hx hn
    exact ⟨hx,hn⟩
  have hDU : D⊆U := fun _ hx => (interior_subset hx).1
  have hWp : W p=v := by
    change nullCorrection (g p) (R p) (n p)=v
    rw [hRp]
    exact null_correction_fixes_null (g p) v (n p) hnv
  have hDW : HasFDerivAt W (connectionInitialJet Gamma p v) p :=
    null_correction_preserves_derivative g R n p (connectionInitialJet Gamma p v)
      (affine_seed_derivative Gamma p v p)
      ((((contDiffOn_pi.2 hns) p hp).contDiffAt (hU.mem_nhds hp)).differentiableAt (by simp))
      (affine_seed_energy_derivative_zero U hU g Gamma hg hm p v hp (hgs p hp))
      (by simpa only [R,affine_seed_initial] using hnv)
      ((((contDiffOn_const.mul hb) p hp).contDiffAt (hU.mem_nhds hp)).differentiableAt (by simp))
      (mul_ne_zero (by norm_num) hbp)
  refine ⟨D,isOpen_interior,hDU,hpD,W,?_,hWp,?_,hDW,?_⟩
  · exact null_correction_smooth D g R n
      (fun a b => (hg a b).mono hDU) (fun a => (hR a).mono hDU)
      (fun a => (hns a).mono hDU) (fun _ hx => (interior_subset hx).2)
  · intro x hx
    exact null_correction_null (g x) (R x) (n x) (hgs x (hDU hx))
      (hnn x (hDU hx)) (interior_subset hx).2
  · have he : covariantVectorGradient Gamma W p=covariantVectorGradient Gamma R p := by
      ext a i
      simp only [covariantVectorGradient,covariantVectorDerivative,
        vector_partial_of_derivative W p _ hDW,
        vector_partial_of_derivative R p _ (affine_seed_derivative Gamma p v p),
        hWp,hRp]
    exact he.trans (affine_seed_gradient_zero Gamma p v)

theorem local_null_seed_with_zero_covariant_jet (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (p v : Coordinate4) (hp : p∈U) (hv : v≠0)
    (hn : tensorQuad (frameMetricField A p) v=0) :
    ∃ D : Set Coordinate4, IsOpen D ∧ D⊆U ∧ p∈D ∧
      ∃ W : VectorField4, SmoothVectorOn D W ∧ W p=v ∧
        (∀ x∈D, tensorQuad (frameMetricField A x) (W x)=0) ∧
        HasFDerivAt W (connectionInitialJet (frameLeviCivita A B) p v) p ∧
        covariantVectorGradient (frameLeviCivita A B) W p=0 := by
  let F := Screen013.solderedNullFrame (A p) (B p) (hAB p hp) (hBA p hp) v hv hn
  obtain ⟨n0,hn0,hpair⟩ := null_companion_of_frame (frameMetricField A p) v F
  let n := transportedNullSeed A B p n0
  have hns : SmoothVectorOn U n := contDiffOn_pi.1 (transported_seed_smooth U A B hB p n0)
  have hnp : n p=n0 := transported_seed_initial A B p n0 (hBA p hp)
  have hm : MetricCompatibleOn U (frameMetricField A) (frameLeviCivita A B) :=
    levi_civita_field_metric_compatible U hU (frameMetricField A) (inverseFrameMetricField B)
      (fun x _ => frame_metric_symmetric A x)
      (fun x hx => inverse_frame_metric_left A B x (hAB x hx) (hBA x hx))
      (fun x hx => inverse_frame_metric_right A B x (hAB x hx) (hBA x hx))
  apply null_seed_with_companion U hU (frameMetricField A) (frameLeviCivita A B)
    (frame_metric_smooth U A hA) hm (fun x _ => frame_metric_symmetric A x) n hns
    (fun x hx => transported_seed_null A B p n0 x (hAB x hx) hn0) p v hp hn
  rw [hnp,hpair]
  norm_num

#print axioms null_companion_of_frame
#print axioms null_seed_with_companion
#print axioms local_null_seed_with_zero_covariant_jet
end
end ChatgptAudit.Flow019
