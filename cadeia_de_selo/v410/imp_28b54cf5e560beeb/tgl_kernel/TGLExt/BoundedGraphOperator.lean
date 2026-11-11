-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_049 (06-07/09/2026), transposta em 07/09/2026
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
import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.Algebra.Module.Submodule.Equiv

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Continuous049

open Set
noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- The inverse of A on its range is linear; continuity is not assumed. -/
def boundedGraphParameter (A : E →L[ℂ] E) (hAi : Function.Injective A) :
    A.range →ₗ[ℂ] E :=
  (LinearEquiv.ofInjective A.toLinearMap hAi).symm.toLinearMap

theorem bounded_graph_parameter_apply (A : E →L[ℂ] E) (hAi : Function.Injective A)
    (x : A.range) :
    A (boundedGraphParameter A hAi x) = (x : E) :=
  LinearEquiv.ofInjective_symm_apply A.toLinearMap x

/-- The domain is exactly range A, which need not be the full Hilbert space. -/
def boundedGraphOperator (A B : E →L[ℂ] E) (hAi : Function.Injective A) :
    E →ₗ.[ℂ] E where
  domain := A.range
  toFun := B.toLinearMap.comp (boundedGraphParameter A hAi)

theorem bounded_graph_domain_iff (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (x : E) :
    x ∈ (boundedGraphOperator A B hAi).domain ↔ ∃ h, A h = x := Iff.rfl

theorem bounded_graph_apply (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (x : (boundedGraphOperator A B hAi).domain) :
    boundedGraphOperator A B hAi x = B (boundedGraphParameter A hAi x) := rfl

def boundedGraphLift (A B : E →L[ℂ] E) (hAi : Function.Injective A) (h : E) :
    (boundedGraphOperator A B hAi).domain :=
  ⟨A h, ⟨h, rfl⟩⟩

theorem bounded_graph_lift_coe (A B : E →L[ℂ] E) (hAi : Function.Injective A) (h : E) :
    (boundedGraphLift A B hAi h : E) = A h := rfl

theorem bounded_graph_parameter_lift (A B : E →L[ℂ] E)
    (hAi : Function.Injective A) (h : E) :
    boundedGraphParameter A hAi (boundedGraphLift A B hAi h) = h := by
  apply hAi
  rw [bounded_graph_parameter_apply]
  rfl

theorem bounded_graph_lift_apply (A B : E →L[ℂ] E) (hAi : Function.Injective A) (h : E) :
    boundedGraphOperator A B hAi (boundedGraphLift A B hAi h) = B h := by
  rw [bounded_graph_apply, bounded_graph_parameter_lift]

theorem bounded_graph_param_iff (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (x y : E) :
    (x,y) ∈ (boundedGraphOperator A B hAi).graph ↔ ∃ h, A h = x ∧ B h = y := by
  rw [LinearPMap.mem_graph_iff]
  constructor
  · rintro ⟨z, hx, hy⟩
    refine ⟨boundedGraphParameter A hAi z, ?_, hy⟩
    exact (bounded_graph_parameter_apply A hAi z).trans hx
  · rintro ⟨h, hx, hy⟩
    refine ⟨boundedGraphLift A B hAi h, hx, ?_⟩
    rw [bounded_graph_lift_apply]
    exact hy

/-- The reverse implication constructs its parameter as Ax+By. -/
theorem bounded_graph_equation_iff (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (hcomm : A * B = B * A) (hsum : A * A + B * B = 1) (x y : E) :
    (x,y) ∈ (boundedGraphOperator A B hAi).graph ↔ B x = A y := by
  have hc (z : E) : A (B z) = B (A z) :=
    congrArg (fun F : E →L[ℂ] E => F z) hcomm
  have hs (z : E) : A (A z) + B (B z) = z :=
    congrArg (fun F : E →L[ℂ] E => F z) hsum
  rw [bounded_graph_param_iff]
  constructor
  · rintro ⟨h, rfl, rfl⟩
    exact (hc h).symm
  · intro hxy
    refine ⟨A x + B y, ?_, ?_⟩
    · rw [map_add, hc, ← hxy, hs]
    · rw [map_add, ← hc, hxy, hs]

/-- Density uses A*=A and injectivity, not a bounded inverse of A. -/
theorem bounded_graph_domain_dense [CompleteSpace E] (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (hA : IsSelfAdjoint A) :
    Dense ((boundedGraphOperator A B hAi).domain : Set E) := by
  have hsa : A.adjoint = A := hA.star_eq
  have hk : A.ker = ⊥ := LinearMap.ker_eq_bot.mpr hAi
  have hc : A.range.topologicalClosure = ⊤ := by
    rw [Submodule.topologicalClosure_eq_top_iff, A.orthogonal_range, hsa, hk]
  intro x
  change x ∈ (A.range.topologicalClosure : Set E)
  rw [hc]
  trivial

/-- Closedness is a closed relation in the ordinary product topology. -/
theorem bounded_graph_closed (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (hcomm : A * B = B * A) (hsum : A * A + B * B = 1) :
    (boundedGraphOperator A B hAi).IsClosed := by
  have hg : ((boundedGraphOperator A B hAi).graph : Set (E × E)) =
      {p | B p.1 = A p.2} := by
    ext p
    exact bounded_graph_equation_iff A B hAi hcomm hsum p.1 p.2
  change IsClosed ((boundedGraphOperator A B hAi).graph : Set (E × E))
  rw [hg]
  exact isClosed_eq (B.continuous.comp continuous_fst) (A.continuous.comp continuous_snd)

theorem bounded_graph_selfadjoint_inner [CompleteSpace E] (A : E →L[ℂ] E)
    (hA : IsSelfAdjoint A) (x y : E) :
    inner ℂ (A x) y = inner ℂ x (A y) := by
  have hs : A.adjoint = A := hA.star_eq
  rw [← ContinuousLinearMap.adjoint_inner_right, hs]

theorem bounded_graph_formal_adjoint [CompleteSpace E] (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) (hcomm : A * B = B * A) :
    (boundedGraphOperator A B hAi).IsFormalAdjoint (boundedGraphOperator A B hAi) := by
  intro x y
  obtain ⟨h, hx, hTx⟩ := (bounded_graph_param_iff A B hAi _ _).mp
    ((boundedGraphOperator A B hAi).mem_graph x)
  obtain ⟨k, hy, hTy⟩ := (bounded_graph_param_iff A B hAi _ _).mp
    ((boundedGraphOperator A B hAi).mem_graph y)
  have hc : A (B k) = B (A k) :=
    congrArg (fun F : E →L[ℂ] E => F k) hcomm
  calc
    inner ℂ (boundedGraphOperator A B hAi x) (y : E) = inner ℂ (B h) (A k) := by
      rw [hTx, hy]
    _ = inner ℂ h (B (A k)) := bounded_graph_selfadjoint_inner B hB h (A k)
    _ = inner ℂ h (A (B k)) := by rw [hc]
    _ = inner ℂ (A h) (B k) := (bounded_graph_selfadjoint_inner A hA h (B k)).symm
    _ = inner ℂ (x : E) (boundedGraphOperator A B hAi y) := by rw [hx, hTy]

/-- Maximality is proved using the actual densely defined Mathlib adjoint. -/
theorem bounded_graph_selfadjoint [CompleteSpace E] (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (hcomm : A * B = B * A) (hsum : A * A + B * B = 1) :
    IsSelfAdjoint (boundedGraphOperator A B hAi) := by
  have hd := bounded_graph_domain_dense A B hAi hA
  have hf := bounded_graph_formal_adjoint A B hAi hA hB hcomm
  have ha : LinearPMap.adjoint (boundedGraphOperator A B hAi) ≤
      boundedGraphOperator A B hAi := by
    apply LinearPMap.le_of_le_graph
    rintro ⟨x,y⟩ hp
    rw [LinearPMap.mem_graph_iff] at hp
    obtain ⟨u, hu, hv⟩ := hp
    apply (bounded_graph_equation_iff A B hAi hcomm hsum x y).mpr
    apply ext_inner_right ℂ
    intro h
    have hh := LinearPMap.adjoint_isFormalAdjoint
      (T := boundedGraphOperator A B hAi) hd u (boundedGraphLift A B hAi h)
    have hh' : inner ℂ y (A h) = inner ℂ x (B h) := by
      simpa only [bounded_graph_lift_coe, bounded_graph_lift_apply, hu, hv] using hh
    calc
      inner ℂ (B x) h = inner ℂ x (B h) := bounded_graph_selfadjoint_inner B hB x h
      _ = inner ℂ y (A h) := hh'.symm
      _ = inner ℂ (A y) h := (bounded_graph_selfadjoint_inner A hA y h).symm
  rw [LinearPMap.isSelfAdjoint_def]
  exact le_antisymm ha (hf.le_adjoint hd)

/-- The bounded-pair inequality yields positivity on the constructed domain. -/
theorem bounded_graph_positive (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (hpos : ∀ h : E, 0 ≤ (inner ℂ (A h) (B h)).re)
    (x : (boundedGraphOperator A B hAi).domain) :
    0 ≤ (inner ℂ (x : E) (boundedGraphOperator A B hAi x)).re := by
  obtain ⟨h, hx, hy⟩ := (bounded_graph_param_iff A B hAi _ _).mp
    ((boundedGraphOperator A B hAi).mem_graph x)
  rw [← hx, ← hy]
  exact hpos h

#print axioms boundedGraphParameter
#print axioms bounded_graph_parameter_apply
#print axioms boundedGraphOperator
#print axioms bounded_graph_domain_iff
#print axioms bounded_graph_apply
#print axioms boundedGraphLift
#print axioms bounded_graph_lift_coe
#print axioms bounded_graph_parameter_lift
#print axioms bounded_graph_lift_apply
#print axioms bounded_graph_param_iff
#print axioms bounded_graph_equation_iff
#print axioms bounded_graph_domain_dense
#print axioms bounded_graph_closed
#print axioms bounded_graph_selfadjoint_inner
#print axioms bounded_graph_formal_adjoint
#print axioms bounded_graph_selfadjoint
#print axioms bounded_graph_positive

end
end ChatgptAudit.Continuous049
