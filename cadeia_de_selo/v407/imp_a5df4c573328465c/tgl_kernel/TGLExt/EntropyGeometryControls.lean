-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_011 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.BoundaryEntropyBridge

set_option autoImplicit false
set_option maxHeartbeats 2200000
namespace ChatgptAudit
open Matrix TGLExt
open scoped Kronecker ComplexOrder
noncomputable section
variable {ι : Type} [DecidableEq ι]

theorem pure_cut_coherence_entry (p : ι → ℝ) (i j : ι) :
    pureCutDensity p (i,i) (j,j)=(Real.sqrt (p i):ℂ)*(Real.sqrt (p j):ℂ) := by
  simp [pureCutDensity,Matrix.vecMulVec,schmidtAmplitude]

theorem pure_cut_not_product (p : ι → ℝ) (i j : ι) (hij : i≠j)
    (hi : 0<p i) (hj : 0<p j) :
    pureCutDensity p≠
      (Matrix.diagonal (fun k => (p k:ℂ)) ⊗ₖ Matrix.diagonal (fun k => (p k:ℂ))) := by
  intro heq
  have he := congrArg (fun A : Matrix (ι × ι) (ι × ι) ℂ => A (i,i) (j,j)) heq
  rw [pure_cut_coherence_entry] at he
  have hd : (Matrix.diagonal (fun k => (p k:ℂ)) ⊗ₖ
      Matrix.diagonal (fun k => (p k:ℂ))) (i,i) (j,j)=0 := by
    simp only [Matrix.kroneckerMap_apply,Matrix.diagonal_apply_ne _ hij,zero_mul]
  rw [hd] at he
  exact (mul_ne_zero (Complex.ofReal_ne_zero.mpr (ne_of_gt (Real.sqrt_pos.2 hi)))
    (Complex.ofReal_ne_zero.mpr (ne_of_gt (Real.sqrt_pos.2 hj)))) he

theorem half_cut_positive_normalized_pure :
    (pureCutDensity (siteW (1/2))).PosSemidef ∧
    Matrix.trace (pureCutDensity (siteW (1/2)))=1 ∧
    pureCutDensity (siteW (1/2))*pureCutDensity (siteW (1/2))=
      pureCutDensity (siteW (1/2)) := by
  have hp : ∀ i : Fin 2, 0 ≤ siteW (1/2) i :=
    fun i => (siteW_pos (by norm_num) (by norm_num) i).le
  exact ⟨pure_cut_positive _,pure_cut_trace_one _ hp (siteW_sum _),
    pure_cut_idempotent _ hp (siteW_sum _)⟩

theorem half_cut_entropy :
    reducedDiagonalEntropy (pureCutDensity (siteW (1/2)))=Real.log 2 := by
  have hp : ∀ i : Fin 2, 0 ≤ siteW (1/2) i :=
    fun i => (siteW_pos (by norm_num) (by norm_num) i).le
  unfold reducedDiagonalEntropy
  rw [pure_cut_right_reduction _ hp]
  simp only [Matrix.diagonal_apply_eq,Complex.ofReal_re]
  rw [site_entropy_binary]
  simpa only [one_div] using Real.binEntropy_two_inv

theorem half_cut_not_product :
    pureCutDensity (siteW (1/2))≠
      (Matrix.diagonal (fun k => (siteW (1/2) k:ℂ)) ⊗ₖ
       Matrix.diagonal (fun k => (siteW (1/2) k:ℂ))) := by
  exact pure_cut_not_product _ (0:Fin 2) (1:Fin 2) (by decide)
    (by norm_num [siteW]) (by norm_num [siteW])

theorem product_control_information :
    diagonalMutualInformation (productWeights (siteW (1/2)) (siteW (1/2)))=0 :=
  product_mutual_information_zero _ _ (siteW_sum _) (siteW_sum _)

theorem complement_entropy_invariance (p : ℝ) :
    finiteEntropy (siteW (1-p))=finiteEntropy (siteW p) := by
  rw [site_entropy_binary,site_entropy_binary,Real.binEntropy_one_sub]

theorem two_area_calibrations (P : SiteProfile) (p : ℝ) (hp : ∀ n, P.w n=p) (N : ℕ) :
    reducedDiagonalEntropy (towerCutDensity P N)=Real.binEntropy p*countArea 1 N ∧
    reducedDiagonalEntropy (towerCutDensity P N)=(Real.binEntropy p/2)*countArea 2 N ∧
    countArea 1 N≠countArea 2 N := by
  refine ⟨?_,tower_cut_chosen_area P p hp 2 (by norm_num) N,?_⟩
  · simpa using tower_cut_chosen_area P p hp 1 (by norm_num) N
  · unfold countArea
    have hn : (0:ℝ)≤N := Nat.cast_nonneg N
    intro he
    linarith

theorem chosen_area_rescales_einstein_coefficient (p areaUnit scale : ℝ) :
    2*Real.pi/(Real.binEntropy p/(scale*areaUnit))=
      scale*(2*Real.pi/(Real.binEntropy p/areaUnit)) := by
  simp only [div_eq_mul_inv,_root_.mul_inv_rev,_root_.inv_inv]
  ring

#print axioms pure_cut_coherence_entry
#print axioms pure_cut_not_product
#print axioms half_cut_positive_normalized_pure
#print axioms half_cut_entropy
#print axioms half_cut_not_product
#print axioms product_control_information
#print axioms complement_entropy_invariance
#print axioms two_area_calibrations
#print axioms chosen_area_rescales_einstein_coefficient
end
end ChatgptAudit
