-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_050 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ContinuousModularSquare
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace ChatgptAudit.Continuous050
open ChatgptAudit.Continuous049 MeasureTheory Filter
open scoped ENNReal ComplexOrder
noncomputable section

/-- Use the real action induced by the complex action, avoiding the Lp instance diamond. -/
local instance instSpectralOperatorRealModule :
    Module ℝ (SpectralHilbert →L[ℂ] SpectralHilbert) :=
  Module.restrictScalars ℝ ℂ (SpectralHilbert →L[ℂ] SpectralHilbert)

/-- The compatible action is pointwise the ordinary real action on the Hilbert space. -/
theorem spectral_operator_real_smul_apply (r : ℝ)
    (A : SpectralHilbert →L[ℂ] SpectralHilbert) (f : SpectralHilbert) :
    (r • A) f = r • (A f) := by
  change ((r : ℂ) • A) f = r • (A f)
  rw [smul_apply]
  exact algebraMap_smul ℂ r (A f)

/-- Nonnegative scalar weights produce positive bounded operators in the Loewner order. -/
theorem bounded_spectral_multiplier_nonneg (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) (hn : ∀ x, 0 ≤ w x) :
    0 ≤ boundedSpectralMultiplier w hw hb := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ContinuousLinearMap.isPositive_def'.mpr
  refine ⟨bounded_spectral_multiplier_selfadjoint w hw hb, ?_⟩
  intro f
  change 0 ≤ (inner ℂ (boundedSpectralMultiplier w hw hb f) f).re
  rw [L2.inner_def]
  change 0 ≤ RCLike.re (∫ x : ℝ,
    inner ℂ ((boundedSpectralMultiplier w hw hb f) x) (f x))
  rw [← integral_re (L2.integrable_inner (𝕜 := ℂ) (boundedSpectralMultiplier w hw hb f) f)]
  apply integral_nonneg_of_ae
  filter_upwards [bounded_spectral_multiplier_ae w hw hb f] with x hx
  rw [hx]
  change 0 ≤ (inner ℂ ((w x : ℂ) * f x) (f x)).re
  have he : (inner ℂ ((w x : ℂ) * f x) (f x)).re = w x * ‖f x‖ ^ 2 := by
    simp [RCLike.inner_apply, Complex.mul_re, Complex.normSq_apply, Complex.sq_norm, mul_add]
    ring
  rw [he]
  exact mul_nonneg (hn x) (sq_nonneg _)

theorem spectralA_nonneg (c : ℝ) : 0 ≤ spectralA c :=
  bounded_spectral_multiplier_nonneg _ _ _ (fun x => le_of_lt (spectral_weightA_pos c x))

theorem spectralB_nonneg (c : ℝ) : 0 ≤ spectralB c :=
  bounded_spectral_multiplier_nonneg _ _ _ (fun x => le_of_lt (spectral_weightB_pos c x))

/-- Its resolvent meaning is proved by the two domain identities below. -/
def continuousResolvent (c : ℝ) : SpectralHilbert →L[ℂ] SpectralHilbert :=
  spectralA c * spectralA c

theorem continuous_resolvent_complement (c : ℝ) :
    1 - continuousResolvent c = spectralB c * spectralB c := by
  have h := spectralAB_square_sum c
  unfold continuousResolvent
  exact sub_eq_iff_eq_add.mpr (by simpa only [add_comm] using h.symm)

theorem continuous_resolvent_sqrt (c : ℝ) :
    CFC.sqrt (continuousResolvent c) = spectralA c :=
  CFC.sqrt_unique rfl (spectralA_nonneg c)

theorem continuous_resolvent_complement_sqrt (c : ℝ) :
    CFC.sqrt (1 - continuousResolvent c) = spectralB c :=
  CFC.sqrt_unique (continuous_resolvent_complement c).symm (spectralB_nonneg c)

/-- The graph coordinates are genuine bounded CFC roots. -/
theorem continuous_modular_graph_from_cfc (c : ℝ) (f g : SpectralHilbert) :
    (f,g) ∈ (continuousModularOperator c).graph ↔
      ∃ h : SpectralHilbert,
        CFC.sqrt (continuousResolvent c) h = f ∧
        CFC.sqrt (1 - continuousResolvent c) h = g := by
  rw [continuous_resolvent_sqrt, continuous_resolvent_complement_sqrt]
  exact bounded_graph_param_iff (spectralA c) (spectralB c) (spectralA_injective c) f g

theorem continuous_modular_domain_from_cfc (c : ℝ) :
    (continuousModularOperator c).domain =
      (CFC.sqrt (continuousResolvent c)).range := by
  rw [continuous_resolvent_sqrt]
  rfl


/-- Pointwise meaning of the bounded resolvent, independent of its inverse identities. -/
theorem continuous_resolvent_ae (c : ℝ) (f : SpectralHilbert) :
    continuousResolvent c f =ᵐ[volume]
      fun x => (spectralWeightA c x : ℂ)^2 * f x := by
  filter_upwards [spectralA_ae c (spectralA c f), spectralA_ae c f] with x haa ha
  change (spectralA c (spectralA c f)) x = _
  rw [haa,ha]
  ring

/-- The two bounded coordinates construct both successive domain witnesses. -/
theorem continuous_resolvent_square_graph (c : ℝ) (f : SpectralHilbert) :
    (continuousResolvent c f, spectralB c (spectralB c f)) ∈
      (continuousModularSquare c).graph := by
  rw [continuous_modular_square_graph_iff]
  refine ⟨spectralA c (spectralB c f), ?_, ?_⟩
  · apply (bounded_graph_param_iff (spectralA c) (spectralB c)
      (spectralA_injective c) _ _).mpr
    refine ⟨spectralA c f,rfl,?_⟩
    exact congrArg (fun F : SpectralHilbert →L[ℂ] SpectralHilbert => F f)
      (spectralAB_commute c).symm
  · apply (bounded_graph_param_iff (spectralA c) (spectralB c)
      (spectralA_injective c) _ _).mpr
    exact ⟨spectralB c f,rfl,rfl⟩

theorem continuous_resolvent_mem_square_domain (c : ℝ) (f : SpectralHilbert) :
    continuousResolvent c f ∈ (continuousModularSquare c).domain :=
  LinearPMap.mem_domain_of_mem_graph (continuous_resolvent_square_graph c f)

theorem continuous_resolvent_square_apply (c : ℝ) (f : SpectralHilbert) :
    continuousModularSquare c
      ⟨continuousResolvent c f, continuous_resolvent_mem_square_domain c f⟩ =
        spectralB c (spectralB c f) :=
  ((LinearPMap.image_iff (continuous_resolvent_mem_square_domain c f)).mpr
    (continuous_resolvent_square_graph c f)).symm

/-- (I+T_c²) C_c f=f, with C_c f proved to lie in the full square domain. -/
theorem continuous_resolvent_right_inverse (c : ℝ) (f : SpectralHilbert) :
    continuousResolvent c f +
      continuousModularSquare c
        ⟨continuousResolvent c f, continuous_resolvent_mem_square_domain c f⟩ = f := by
  rw [continuous_resolvent_square_apply]
  exact congrArg (fun F : SpectralHilbert →L[ℂ] SpectralHilbert => F f)
    (spectralAB_square_sum c)

/-- C_c (x+T_c²x)=x for every x in the actual composition domain. -/
theorem continuous_resolvent_left_inverse (c : ℝ)
    (x : (continuousModularSquare c).domain) :
    continuousResolvent c ((x : SpectralHilbert) + continuousModularSquare c x) =
      (x : SpectralHilbert) := by
  apply Lp.ext
  have hg : ((x : SpectralHilbert), continuousModularSquare c x) ∈
      (continuousModularOperator (2*c)).graph := by
    rw [← continuous_modular_square_eq]
    exact (continuousModularSquare c).mem_graph x
  have hq := (continuous_modular_graph_iff (2*c) _ _).mp hg
  filter_upwards [
      continuous_resolvent_ae c ((x : SpectralHilbert) + continuousModularSquare c x),
      Lp.coeFn_add (x : SpectralHilbert) (continuousModularSquare c x), hq]
    with ξ hC hadd hQ
  rw [hC,hadd,Pi.add_apply,hQ,continuous_weight_double_complex]
  have hs : (spectralWeightA c ξ : ℂ)^2 + (spectralWeightB c ξ : ℂ)^2 = 1 := by
    exact_mod_cast spectral_weight_square_sum c ξ
  have hr : (spectralWeightB c ξ : ℂ) =
      (Real.exp (-c*ξ) : ℂ) * (spectralWeightA c ξ : ℂ) := by
    exact_mod_cast spectral_weight_ratio c ξ
  calc
    _ = ((spectralWeightA c ξ : ℂ)^2 +
        ((Real.exp (-c*ξ) : ℂ) * (spectralWeightA c ξ : ℂ))^2) *
          (x : SpectralHilbert) ξ := by ring
    _ = (x : SpectralHilbert) ξ := by rw [← hr,hs,one_mul]

/-- Uniqueness of the bounded resolvent among maps satisfying the right-inverse domain law. -/
theorem continuous_resolvent_unique (c : ℝ)
    (R : SpectralHilbert →L[ℂ] SpectralHilbert)
    (hdom : ∀ f : SpectralHilbert, R f ∈ (continuousModularSquare c).domain)
    (hinv : ∀ f : SpectralHilbert,
      R f + continuousModularSquare c ⟨R f,hdom f⟩ = f) :
    R = continuousResolvent c := by
  apply ContinuousLinearMap.ext
  intro f
  have h := continuous_resolvent_left_inverse c ⟨R f,hdom f⟩
  rw [hinv f] at h
  exact h.symm

#print axioms instSpectralOperatorRealModule
#print axioms spectral_operator_real_smul_apply
#print axioms bounded_spectral_multiplier_nonneg
#print axioms spectralA_nonneg
#print axioms spectralB_nonneg
#print axioms continuousResolvent
#print axioms continuous_resolvent_complement
#print axioms continuous_resolvent_sqrt
#print axioms continuous_resolvent_complement_sqrt
#print axioms continuous_modular_graph_from_cfc
#print axioms continuous_modular_domain_from_cfc

#print axioms continuous_resolvent_ae
#print axioms continuous_resolvent_square_graph
#print axioms continuous_resolvent_mem_square_domain
#print axioms continuous_resolvent_square_apply
#print axioms continuous_resolvent_right_inverse
#print axioms continuous_resolvent_left_inverse
#print axioms continuous_resolvent_unique

end
end ChatgptAudit.Continuous050
