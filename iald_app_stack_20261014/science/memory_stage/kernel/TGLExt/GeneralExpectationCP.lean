-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_047 (06-07/09/2026), transposta em 07/09/2026
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
import TGLExt.ExpectationBlockPositive
import TGLExt.OperatorBlockRepresentation
import TGLExt.SummableLikelihoodGenerator
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Expectation047

open TGLExt
open scoped ComplexOrder

noncomputable section

/-- Norm closure supplies the actual C-star structure on the factor subtype. -/
instance factor_subalgebra_closed (P : SiteProfile) :
    IsClosed ((theFactorObject P).toStarSubalgebra :
      Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :=
  ChatgptAudit.Cocycle030.factor_norm_closed P

/-- The ambient positive square root remains in the norm-closed factor. -/
theorem factor_positive_sqrt_mem (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) (hA : 0 ≤ A) :
    CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P) ∈
      (theFactorObject P).toStarSubalgebra := by
  have hAop : 0 ≤ (A : TowerHilbert P →L[ℂ] TowerHilbert P) := hA
  rw [CFC.sqrt_eq_real_sqrt _ hAop]
  exact cfcₙ_mem (𝕜' := ℂ) Real.sqrt A.property

/-- The inherited operator order is exactly the star-square order on the factor. -/
theorem factor_nonnegative_iff_star_square (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) :
    0 ≤ A ↔ ∃ B : (theFactorObject P).toStarSubalgebra, A = star B * B := by
  constructor
  · intro hA
    have hAop : 0 ≤ (A : TowerHilbert P →L[ℂ] TowerHilbert P) := hA
    let B : (theFactorObject P).toStarSubalgebra :=
      ⟨CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P),
        factor_positive_sqrt_mem P A hA⟩
    refine ⟨B, Subtype.ext ?_⟩
    change (A : TowerHilbert P →L[ℂ] TowerHilbert P) =
      star (CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P)) *
        CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    rw [(CFC.sqrt_nonneg (A : TowerHilbert P →L[ℂ] TowerHilbert P)).isSelfAdjoint.star_eq,
      CFC.sqrt_mul_sqrt_self _ hAop]
  · rintro ⟨B, rfl⟩
    change 0 ≤ star (B : TowerHilbert P →L[ℂ] TowerHilbert P) *
      (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    exact star_mul_self_nonneg _

/-- This instance keeps the subtype order inherited from bounded operators. -/
instance factor_subalgebra_star_ordered (P : SiteProfile) :
    StarOrderedRing (theFactorObject P).toStarSubalgebra :=
  StarOrderedRing.of_nonneg_iff'
    (fun {x y} h z => by
      change (z : TowerHilbert P →L[ℂ] TowerHilbert P) +
          (x : TowerHilbert P →L[ℂ] TowerHilbert P) ≤
        (z : TowerHilbert P →L[ℂ] TowerHilbert P) +
          (y : TowerHilbert P →L[ℂ] TowerHilbert P)
      have hxy : (x : TowerHilbert P →L[ℂ] TowerHilbert P) ≤
          (y : TowerHilbert P →L[ℂ] TowerHilbert P) := h
      simpa only [add_comm] using
        add_le_add_left hxy (z : TowerHilbert P →L[ℂ] TowerHilbert P))
    (factor_nonnegative_iff_star_square P)

/-- Genuine C-star matrix positivity follows from the represented block form. -/
theorem expectation_cstarMatrix_nonnegative (P : SiteProfile) (I : ExpectationInput P)
    (k : ℕ)
    (M : CStarMatrix (Fin k) (Fin k) (theFactorObject P).toStarSubalgebra)
    (hM : 0 ≤ M) :
    0 ≤ M.map (expectationLinearMap P I) := by
  have hinc :
      0 ≤ M.map (theFactorObject P).toStarSubalgebra.subtype :=
    CompletelyPositiveMapClass.map_cstarMatrix_nonneg'
      (theFactorObject P).toStarSubalgebra.subtype k M hM
  have hblock :
      BlockPositive P k
        (fun i j => (M i j : TowerHilbert P →L[ℂ] TowerHilbert P)) :=
    (operator_block_nonneg_iff (TowerHilbert P) k _).mp hinc
  apply (operator_block_nonneg_iff (TowerHilbert P) k _).mpr
  exact general_expectation_block_positive P I k
    (fun i j => (M i j : TowerHilbert P →L[ℂ] TowerHilbert P))
    (fun i j => (M i j).property) hblock

/-- The constructed expectation, restricted to its actual algebra, as a genuine CP map. -/
def generalExpectationCompletelyPositiveMap (P : SiteProfile) (I : ExpectationInput P) :
    CompletelyPositiveMap (theFactorObject P).toStarSubalgebra
      (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toLinearMap := expectationLinearMap P I
  map_cstarMatrix_nonneg' := expectation_cstarMatrix_nonnegative P I

theorem general_expectation_cp_apply (P : SiteProfile) (I : ExpectationInput P)
    (A : (theFactorObject P).toStarSubalgebra) :
    generalExpectationCompletelyPositiveMap P I A = I.E A := rfl

theorem general_expectation_cp_toLinearMap (P : SiteProfile) (I : ExpectationInput P) :
    (generalExpectationCompletelyPositiveMap P I).toLinearMap =
      expectationLinearMap P I := rfl

#print axioms factor_subalgebra_closed
#print axioms factor_positive_sqrt_mem
#print axioms factor_nonnegative_iff_star_square
#print axioms factor_subalgebra_star_ordered
#print axioms expectation_cstarMatrix_nonnegative
#print axioms generalExpectationCompletelyPositiveMap
#print axioms general_expectation_cp_apply
#print axioms general_expectation_cp_toLinearMap

end

end ChatgptAudit.Expectation047
