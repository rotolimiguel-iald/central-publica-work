-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_046 (06-07/09/2026), transposta em 07/09/2026
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
import TGLExt.AperiodicPhaseAverage
import TGLExt.BoundedOmegaLimit

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Aperiodic046

open TGLExt MeasureTheory Filter
open scoped Topology

noncomputable section

/-- A normalized interval average of the actual modular flow on Hilbert vectors. -/
def modularAverageVector (P : SiteProfile) (T : ℝ)
    (v : TowerHilbert P) : TowerHilbert P :=
  T⁻¹ • ∫ t in (0 : ℝ)..T, modularFlow P t v

theorem modular_average_vector_add (P : SiteProfile) (T : ℝ)
    (v w : TowerHilbert P) :
    modularAverageVector P T (v+w) =
      modularAverageVector P T v + modularAverageVector P T w := by
  simp only [modularAverageVector, modularFlow_add]
  rw [intervalIntegral.integral_add
    ((modularFlow_strongly_continuous v).intervalIntegrable 0 T)
    ((modularFlow_strongly_continuous w).intervalIntegrable 0 T), smul_add]

theorem modular_average_vector_smul (P : SiteProfile) (T : ℝ)
    (c : ℂ) (v : TowerHilbert P) :
    modularAverageVector P T (c • v) = c • modularAverageVector P T v := by
  simp only [modularAverageVector, modularFlow_smul, intervalIntegral.integral_smul]
  exact smul_comm _ _ _

/-- This vector estimate, rather than an estimate only on AΩ, permits dense approximation. -/
theorem modular_average_vector_bound (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (v : TowerHilbert P) :
    ‖modularAverageVector P T v‖ ≤ ‖v‖ := by
  have hb := intervalIntegral.norm_integral_le_of_norm_le_const
    (a := (0 : ℝ)) (b := T)
    (fun t _ => le_of_eq (modularFlow_norm (P := P) t v))
  simp only [sub_zero, abs_of_pos hT] at hb
  calc
    ‖modularAverageVector P T v‖ =
        T⁻¹ * ‖∫ t in (0 : ℝ)..T, modularFlow P t v‖ := by
      rw [modularAverageVector, norm_smul, Real.norm_eq_abs,
        abs_of_pos (inv_pos.mpr hT)]
    _ ≤ T⁻¹ * (‖v‖ * T) :=
      mul_le_mul_of_nonneg_left hb (le_of_lt (inv_pos.mpr hT))
    _ = ‖v‖ := by field_simp

/-- The vector average as a complex continuous linear contraction. -/
def modularVectorAverage (P : SiteProfile) (T : ℝ) (hT : 0 < T) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  ({ toFun := modularAverageVector P T
     map_add' := modular_average_vector_add P T
     map_smul' := fun c v => modular_average_vector_smul P T c v } :
    TowerHilbert P →ₗ[ℂ] TowerHilbert P).mkContinuous 1
      (fun v => by
        change ‖modularAverageVector P T v‖ ≤ 1 * ‖v‖
        simpa only [one_mul] using modular_average_vector_bound P T hT v)

theorem modular_vector_average_apply (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (v : TowerHilbert P) :
    modularVectorAverage P T hT v =
      T⁻¹ • ∫ t in (0 : ℝ)..T, modularFlow P t v := rfl

theorem modular_vector_average_norm_le_one (P : SiteProfile) (T : ℝ) (hT : 0 < T) :
    ‖modularVectorAverage P T hT‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro v
  change ‖modularAverageVector P T v‖ ≤ 1 * ‖v‖
  simpa only [one_mul] using modular_average_vector_bound P T hT v

/-- Local convergence is spectral pinching, with no common phase period. -/
theorem modular_vector_average_local_limit (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Tendsto
      (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity)
        (levelEmbedding P N a))
      atTop (𝓝 (levelEmbedding P N (specExpect (towerW P N) a))) := by
  simpa only [modular_vector_average_apply] using local_average_limit P N a

/-- The uniform contraction bound extends Cauchy convergence from the dense pre-Hilbert space. -/
theorem modular_vector_average_cauchy (P : SiteProfile) (v : TowerHilbert P) :
    CauchySeq
      (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity) v) := by
  apply bounded_local_cauchy P
    (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity))
    1 (by norm_num)
    (fun n => modular_vector_average_norm_le_one P ((n : ℝ)+1) (by positivity))
    ?_ v
  intro w
  obtain ⟨N, a, rfl⟩ := exists_tof w
  change CauchySeq
    (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity)
      (levelEmbedding P N a))
  exact (modular_vector_average_local_limit P N a).cauchySeq

/-- The Hilbert limit is constructed by completeness for every vector. -/
theorem modular_vector_average_limit_exists (P : SiteProfile) (v : TowerHilbert P) :
    ∃ z : TowerHilbert P,
      Tendsto
        (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity) v)
        atTop (𝓝 z) :=
  cauchySeq_tendsto_of_complete (modular_vector_average_cauchy P v)

/-- Conjugation averages on Ω are exactly the vector averages of AΩ. -/
theorem period_average_omega_eq_vector_average (P : SiteProfile) (T : ℝ)
    (hT : 0 < T) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    periodAverage P T hT A (hOmega P) =
      modularVectorAverage P T hT (A (hOmega P)) := by
  change T⁻¹ • (∫ t in (0 : ℝ)..T, modularConjugation P t A (hOmega P)) =
    T⁻¹ • (∫ t in (0 : ℝ)..T, modularFlow P t (A (hOmega P)))
  congr 1
  apply intervalIntegral.integral_congr
  intro t _
  change modularFlow P t (A (modularFlow P (-t) (hOmega P))) =
    modularFlow P t (A (hOmega P))
  rw [modularFlow_fixes_omega]

/-- Aperiodic convergence on Ω follows without assuming A belongs to the factor. -/
theorem aperiodic_average_omega_limit (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    ∃ z : TowerHilbert P,
      Tendsto
        (fun n : ℕ => periodAverage P ((n : ℝ)+1) (by positivity) A (hOmega P))
        atTop (𝓝 z) := by
  obtain ⟨z, hz⟩ := modular_vector_average_limit_exists P (A (hOmega P))
  refine ⟨z, ?_⟩
  simpa only [period_average_omega_eq_vector_average] using hz

/-- The limiting factor element and its strong convergence are conclusions.
No expectation, periodicity, or operator limit is supplied as a hypothesis. -/
theorem aperiodic_average_operator (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    ∃ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P ∧ ‖B‖ ≤ ‖A‖ ∧
      ∀ v : TowerHilbert P,
        Tendsto
          (fun n : ℕ => periodAverage P ((n : ℝ)+1) (by positivity) A v)
          atTop (𝓝 (B v)) := by
  obtain ⟨z, hz⟩ := aperiodic_average_omega_limit P A
  obtain ⟨B, hB, hnorm, _, hlim⟩ := bounded_omega_limit_lift P
    (fun n : ℕ => periodAverage P ((n : ℝ)+1) (by positivity) A)
    ‖A‖ (norm_nonneg A)
    (fun n => period_average_mem_factor (P := P) ((n : ℝ)+1) (by positivity) A hA)
    (fun n => (period_average_operator (P := P) ((n : ℝ)+1) (by positivity) A).2)
    z hz
  exact ⟨B, hB, hnorm, hlim⟩

#print axioms modularAverageVector
#print axioms modular_average_vector_add
#print axioms modular_average_vector_smul
#print axioms modular_average_vector_bound
#print axioms modularVectorAverage
#print axioms modular_vector_average_apply
#print axioms modular_vector_average_norm_le_one
#print axioms modular_vector_average_local_limit
#print axioms modular_vector_average_cauchy
#print axioms modular_vector_average_limit_exists
#print axioms period_average_omega_eq_vector_average
#print axioms aperiodic_average_omega_limit
#print axioms aperiodic_average_operator

end
end ChatgptAudit.Aperiodic046
