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
import TGLExt.ContinuousModularDomain

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Continuous050

open MeasureTheory Filter Set
open ChatgptAudit.Continuous049
open scoped ENNReal
noncomputable section

/-- The actual domain of two successive applications, with no invariance assumption. -/
def partialSquareDomain {H : Type*} [AddCommGroup H] [Module ℂ H]
    (T : H →ₗ.[ℂ] H) : Submodule ℂ H where
  carrier := {f | ∃ hf : f ∈ T.domain,
    T ⟨f,hf⟩ ∈ T.domain}
  zero_mem' := by
    refine ⟨T.domain.zero_mem, ?_⟩
    change T 0 ∈ T.domain
    rw [LinearPMap.map_zero]
    exact T.domain.zero_mem
  add_mem' := by
    rintro f g ⟨hf,hTf⟩ ⟨hg,hTg⟩
    refine ⟨T.domain.add_mem hf hg, ?_⟩
    change T
      ((⟨f,hf⟩ : T.domain) + ⟨g,hg⟩) ∈ _
    rw [LinearPMap.map_add]
    exact T.domain.add_mem hTf hTg
  smul_mem' := by
    rintro z f ⟨hf,hTf⟩
    refine ⟨T.domain.smul_mem z hf, ?_⟩
    change T
      (z • (⟨f,hf⟩ : T.domain)) ∈ _
    rw [LinearPMap.map_smul]
    exact T.domain.smul_mem z hTf

/-- Specialization of the genuine composition domain to the continuous model. -/
def continuousModularSquareDomain (c : ℝ) : Submodule ℂ SpectralHilbert :=
  partialSquareDomain (continuousModularOperator c)

/-- Inclusion of the composition domain into the domain of its first application. -/
def continuousModularSquareInput (c : ℝ) :
    continuousModularSquareDomain c →ₗ[ℂ] (continuousModularOperator c).domain :=
  Submodule.inclusion (fun _ hf => hf.choose)

/-- T_c composed with itself on the domain on which both applications exist. -/
def continuousModularSquare (c : ℝ) : SpectralHilbert →ₗ.[ℂ] SpectralHilbert where
  domain := continuousModularSquareDomain c
  toFun := (continuousModularOperator c).toFun.comp
    (((continuousModularOperator c).toFun.comp (continuousModularSquareInput c)).codRestrict
      (continuousModularOperator c).domain (fun f => f.property.choose_spec))

theorem continuous_modular_square_domain_iff (c : ℝ) (f : SpectralHilbert) :
    f ∈ (continuousModularSquare c).domain ↔
      ∃ hf : f ∈ (continuousModularOperator c).domain,
        continuousModularOperator c ⟨f,hf⟩ ∈ (continuousModularOperator c).domain :=
  Iff.rfl

theorem continuous_modular_square_apply (c : ℝ)
    (f : (continuousModularSquare c).domain) :
    continuousModularSquare c f =
      continuousModularOperator c
        ⟨continuousModularOperator c ⟨(f : SpectralHilbert), f.property.choose⟩,
          f.property.choose_spec⟩ := rfl

theorem continuous_modular_square_graph_iff (c : ℝ) (f g : SpectralHilbert) :
    (f,g) ∈ (continuousModularSquare c).graph ↔
      ∃ h : SpectralHilbert, (f,h) ∈ (continuousModularOperator c).graph ∧
        (h,g) ∈ (continuousModularOperator c).graph := by
  rw [LinearPMap.mem_graph_iff]
  constructor
  · rintro ⟨x,hx,hy⟩
    let u : (continuousModularOperator c).domain := ⟨x, x.property.choose⟩
    let v : (continuousModularOperator c).domain :=
      ⟨continuousModularOperator c u, x.property.choose_spec⟩
    refine ⟨continuousModularOperator c u, ?_, ?_⟩
    · rw [LinearPMap.mem_graph_iff]
      exact ⟨u,hx,rfl⟩
    · rw [LinearPMap.mem_graph_iff]
      exact ⟨v,rfl,hy⟩
  · rintro ⟨h,hfh,hhg⟩
    rw [LinearPMap.mem_graph_iff] at hfh hhg
    obtain ⟨u,hu,hTu⟩ := hfh
    obtain ⟨v,hv,hTv⟩ := hhg
    dsimp only [Prod.fst, Prod.snd] at hu hTu hv hTv
    have hTuD : continuousModularOperator c u ∈ (continuousModularOperator c).domain := by
      rw [hTu, ← hv]
      exact v.property
    let x : (continuousModularSquare c).domain :=
      ⟨u, ⟨u.property,hTuD⟩⟩
    refine ⟨x,hu,?_⟩
    change continuousModularOperator c ⟨continuousModularOperator c u,hTuD⟩ = g
    have he : (⟨continuousModularOperator c u,hTuD⟩ :
        (continuousModularOperator c).domain) = v :=
      Subtype.ext (hTu.trans hv.symm)
    rw [he]
    exact hTv

theorem continuous_weight_double (c x : ℝ) :
    Real.exp (-(2*c) * x) = Real.exp (-c * x) ^ 2 := by
  rw [pow_two, ← Real.exp_add]
  congr 1
  ring

theorem continuous_weight_double_complex (c x : ℝ) :
    (Real.exp (-(2*c) * x) : ℂ) =
      (Real.exp (-c * x) : ℂ) * (Real.exp (-c * x) : ℂ) := by
  exact_mod_cast (continuous_weight_double c x).trans (pow_two _)

/-- A pointwise bound that proves the missing inclusion of domains. -/
theorem continuous_weight_half_norm_le (c x : ℝ) (z : ℂ) :
    ‖(Real.exp (-c*x) : ℂ) * z‖ ≤
      ‖z‖ + ‖(Real.exp (-(2*c)*x) : ℂ) * z‖ := by
  simp only [norm_mul, Complex.norm_real, Real.norm_eq_abs, Real.abs_exp]
  rw [continuous_weight_double]
  have h : Real.exp (-c*x) ≤ 1 + Real.exp (-c*x)^2 := by
    nlinarith [sq_nonneg (Real.exp (-c*x) - 1/2)]
  calc
    _ ≤ (1 + Real.exp (-c*x)^2) * ‖z‖ :=
      mul_le_mul_of_nonneg_right h (norm_nonneg z)
    _ = ‖z‖ + Real.exp (-c*x)^2 * ‖z‖ := by ring

/-- The input is arbitrary in H; membership in D_c is a conclusion. -/
theorem continuous_modular_double_domain_le (c : ℝ) :
    (continuousModularOperator (2*c)).domain ≤ (continuousModularOperator c).domain := by
  intro f hf
  apply (continuous_modular_domain_iff c f).mpr
  have h2 := (continuous_modular_domain_iff (2*c) f).mp hf
  have hdom := (Lp.memLp f).norm.add h2.norm
  have hw : AEStronglyMeasurable
      (fun x : ℝ => (Real.exp (-c*x) : ℂ) * f x) (volume : Measure ℝ) := by
    have hc : Continuous (fun x : ℝ => (Real.exp (-c*x) : ℂ)) := by fun_prop
    exact hc.aestronglyMeasurable.mul (Lp.aestronglyMeasurable f)
  apply hdom.mono' hw
  exact Eventually.of_forall (fun x => continuous_weight_half_norm_le c x (f x))

/-- Exact equality of partial operators, including their domains. -/
theorem continuous_modular_square_eq (c : ℝ) :
    continuousModularSquare c = continuousModularOperator (2*c) := by
  apply LinearPMap.eq_of_eq_graph
  ext p
  rcases p with ⟨f,g⟩
  rw [continuous_modular_square_graph_iff]
  constructor
  · rintro ⟨h,hfh,hhg⟩
    apply (continuous_modular_graph_iff (2*c) f g).mpr
    have h1 := (continuous_modular_graph_iff c f h).mp hfh
    have h2 := (continuous_modular_graph_iff c h g).mp hhg
    filter_upwards [h1,h2] with x hx hy
    rw [hy,hx,continuous_weight_double_complex]
    ring
  · intro hfg
    have hf2 := LinearPMap.mem_domain_of_mem_graph hfg
    have hf := continuous_modular_double_domain_le c hf2
    let h := continuousModularOperator c ⟨f,hf⟩
    refine ⟨h,(continuousModularOperator c).mem_graph ⟨f,hf⟩,?_⟩
    apply (continuous_modular_graph_iff c h g).mpr
    have h1 := continuous_modular_apply_ae c ⟨f,hf⟩
    have h2 := (continuous_modular_graph_iff (2*c) f g).mp hfg
    filter_upwards [h1,h2] with x hx hy
    change g x = (Real.exp (-c*x) : ℂ) * (continuousModularOperator c ⟨f,hf⟩) x
    rw [hy,hx,continuous_weight_double_complex]
    ring

theorem continuous_modular_square_domain_eq (c : ℝ) :
    (continuousModularSquare c).domain = (continuousModularOperator (2*c)).domain :=
  congrArg LinearPMap.domain (continuous_modular_square_eq c)

/-- Global composability criterion; no initial domain assumption is added. -/
theorem continuous_modular_composable_iff (c : ℝ) (f : SpectralHilbert) :
    (∃ hf : f ∈ (continuousModularOperator c).domain,
      continuousModularOperator c ⟨f,hf⟩ ∈ (continuousModularOperator c).domain) ↔
        f ∈ (continuousModularOperator (2*c)).domain := by
  rw [← continuous_modular_square_domain_iff, continuous_modular_square_domain_eq]

theorem continuous_modular_square_closed (c : ℝ) : (continuousModularSquare c).IsClosed := by
  rw [continuous_modular_square_eq]
  exact continuous_modular_closed (2*c)

theorem continuous_modular_square_selfadjoint (c : ℝ) :
    IsSelfAdjoint (continuousModularSquare c) := by
  rw [continuous_modular_square_eq]
  exact continuous_modular_selfadjoint (2*c)

#print axioms partialSquareDomain
#print axioms continuousModularSquareDomain
#print axioms continuousModularSquareInput
#print axioms continuousModularSquare
#print axioms continuous_modular_square_domain_iff
#print axioms continuous_modular_square_apply
#print axioms continuous_modular_square_graph_iff
#print axioms continuous_weight_double
#print axioms continuous_weight_double_complex
#print axioms continuous_weight_half_norm_le
#print axioms continuous_modular_double_domain_le
#print axioms continuous_modular_square_eq
#print axioms continuous_modular_square_domain_eq
#print axioms continuous_modular_composable_iff
#print axioms continuous_modular_square_closed
#print axioms continuous_modular_square_selfadjoint

end
end ChatgptAudit.Continuous050
