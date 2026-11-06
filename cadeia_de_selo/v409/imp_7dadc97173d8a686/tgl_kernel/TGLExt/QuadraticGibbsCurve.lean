-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_024 (06/09/2026), transposta em 06/09/2026
-- Lote 024..026: a perturbacao de GIBBS realizada no mesmo Hilbert da torre (estado fiel,
--   normalizado, distinto da orbita modular; resposta quadratica; calor/fonte por normalizacao);
--   o LIMITE TERMICO: para perfil constante nao tracial a preparacao NAO tem limite em norma
--   (nao-Cauchy) e o acoplamento da torre e ilimitado; corte com escala escolhida; AFINIDADE:
--   criterio exato (Cauchy <=> afinidade-limite > 0), estado global no Hilbert original, fiel e
--   ciclico; perfil gradual (muda em infinitos sitios, ainda fiel). Estatuto [REAL / INPUT / OPEN]:
--   selecao fisica, area, H3 dinamico, dimensao/assinatura, globalizacao e a classificacao geral
--   dos estados normais (disjuncao) seguem INPUT/OPEN — a bancada NAO promoveu nao-Cauchy a teorema
--   geral de disjuncao nem importou Kakutani.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100%; manifestos 202/206/220;
--   3/3 auditores da bancada exit 0; recompilacao INDEPENDENTE 22/22, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.GibbsVarianceResponse

set_option autoImplicit false
set_option maxHeartbeats 10000000
namespace ChatgptAudit.Thermal024
open Matrix Filter Topology Set ChatgptAudit.Micro021
noncomputable section

theorem quadratic_reparameterization_limit (f : ℝ → ℝ) (derivative frequency : ℝ)
    (hf : HasDerivAt f derivative 0) :
    Tendsto (fun t => (f ((frequency*t)^2)-f 0)/t^2) (𝓝[<] 0) (𝓝 (frequency^2*derivative)) := by
  by_cases hz : frequency=0
  · subst frequency
    simp only [zero_mul,zero_pow (by decide : 2≠0),sub_self,zero_div]
    exact tendsto_const_nhds
  have hc : Tendsto (fun t : ℝ => (frequency*t)^2) (𝓝[<] 0) (𝓝 0) := by
    have hh : ContinuousAt (fun t : ℝ => (frequency*t)^2) 0 := by fun_prop
    simpa only [mul_zero,zero_pow (by decide : 2≠0)] using hh.tendsto.mono_left nhdsWithin_le_nhds
  have hn : Tendsto (fun t : ℝ => (frequency*t)^2) (𝓝[<] 0) (𝓝[≠] 0) := by
    apply tendsto_nhdsWithin_iff.mpr
    refine ⟨hc,?_⟩
    filter_upwards [self_mem_nhdsWithin] with t ht
    change (frequency*t)^2≠0
    exact pow_ne_zero 2 (mul_ne_zero hz (ne_of_lt ht))
  have hs : Tendsto (fun s => (f s-f 0)/s) (𝓝[≠] 0) (𝓝 derivative) := by
    simpa only [zero_add,smul_eq_mul,div_eq_mul_inv,mul_comm] using hf.tendsto_slope_zero
  have hl := (hs.comp hn).mul_const (frequency^2)
  have he : (fun t => (f ((frequency*t)^2)-f 0)/t^2)=ᶠ[𝓝[<] (0:ℝ)]
      (fun t => ((f ((frequency*t)^2)-f 0)/(frequency*t)^2)*frequency^2) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    have ht0 : t≠0 := ne_of_lt ht
    field_simp [hz,ht0]
  simpa only [mul_comm] using hl.congr' he.symm

theorem quadratic_parameter_derivative (frequency t : ℝ) :
    HasDerivAt (fun s : ℝ => (frequency*s)^2) (2*frequency^2*t) t := by
  have hh := ((hasDerivAt_id t).const_mul frequency).pow 2
  convert hh using 1 <;> first | rfl | (simp only [id_eq]; ring)

variable {ι : Type} [Fintype ι] [Nonempty ι]

def quadraticGibbsWeights (p : ι → ℝ) (frequency t : ℝ) : ι → ℝ :=
  gibbsWeights p ((frequency*t)^2)

def quadraticGibbsTangent (p : ι → ℝ) (frequency t : ℝ) (i : ι) : ℝ :=
  gibbsTangent p ((frequency*t)^2) i*(2*frequency^2*t)

theorem quadratic_gibbs_derivative (p : ι → ℝ) (hp : ∀ i, 0<p i) (frequency t : ℝ) (i : ι) :
    HasDerivAt (fun s => quadraticGibbsWeights p frequency s i) (quadraticGibbsTangent p frequency t i) t := by
  simpa only [quadraticGibbsWeights,quadraticGibbsTangent,Function.comp_def] using
    (gibbs_weights_derivative p hp ((frequency*t)^2) i).comp t (quadratic_parameter_derivative frequency t)

theorem quadratic_gibbs_tangent_continuous (p : ι → ℝ) (hp : ∀ i, 0<p i) (frequency : ℝ) (i : ι) :
    Continuous (fun t => quadraticGibbsTangent p frequency t i) :=
  ((gibbs_tangent_continuous p hp i).comp (by fun_prop)).mul (by fun_prop)

def quadraticGibbsCurve (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) (frequency : ℝ) :
    DiagonalStateCurve p where
  weights := quadraticGibbsWeights p frequency
  tangent := quadraticGibbsTangent p frequency
  at_zero := by
    intro i
    simpa only [quadraticGibbsWeights,mul_zero,zero_pow (by decide : 2≠0)] using gibbs_weights_zero p hs i
  trace_one := fun t => gibbs_weights_normalized p hp ((frequency*t)^2)
  derivative_zero := quadratic_gibbs_derivative p hp frequency 0
  derivative_past := by
    filter_upwards [] with t
    exact quadratic_gibbs_derivative p hp frequency t
  tangent_continuous := fun i => (quadratic_gibbs_tangent_continuous p hp frequency i).continuousAt

theorem quadratic_gibbs_positive (p : ι → ℝ) (hp : ∀ i, 0<p i) (frequency t : ℝ) (i : ι) :
    0<quadraticGibbsWeights p frequency t i := gibbs_weights_positive p hp _ i

theorem quadratic_gibbs_tangent_zero (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) (frequency : ℝ) :
    (quadraticGibbsCurve p hp hs frequency).tangent 0=0 := by
  ext i
  simp [quadraticGibbsCurve,quadraticGibbsTangent]

theorem quadratic_gibbs_relative_entropy_zero (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) (frequency : ℝ) :
    Tendsto (fun t => diagonalRelativeEntropy (quadraticGibbsWeights p frequency t) p/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  (relative_entropy_quadratic_zero_iff (quadraticGibbsCurve p hp hs frequency) hp).mpr
    (quadratic_gibbs_tangent_zero p hp hs frequency)

theorem quadratic_gibbs_modular_limit (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) (frequency : ℝ) :
    Tendsto (fun t => modularIncrement p (quadraticGibbsWeights p frequency t)/t^2)
      (𝓝[<] 0) (𝓝 (-frequency^2*modularVariance p)) := by
  have hh := quadratic_reparameterization_limit (fun s => modularIncrement p (gibbsWeights p s))
    (-modularVariance p) frequency (gibbs_modular_increment_derivative_zero p hp hs)
  have h0 : gibbsWeights p 0=p := funext (gibbs_weights_zero p hs)
  simpa only [quadraticGibbsWeights,h0,modular_increment_self,sub_zero,mul_neg,neg_mul] using hh

theorem quadratic_gibbs_entropy_limit (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) (frequency : ℝ) :
    Tendsto (fun t => (finiteEntropy (quadraticGibbsWeights p frequency t)-finiteEntropy p)/t^2)
      (𝓝[<] 0) (𝓝 (-frequency^2*modularVariance p)) := by
  have hh := quadratic_reparameterization_limit (fun s => finiteEntropy (gibbsWeights p s))
    (-modularVariance p) frequency (gibbs_entropy_derivative_zero p hp hs)
  have h0 : gibbsWeights p 0=p := funext (gibbs_weights_zero p hs)
  simpa only [quadraticGibbsWeights,h0,mul_neg,neg_mul] using hh

#print axioms quadratic_reparameterization_limit
#print axioms quadratic_parameter_derivative
#print axioms quadratic_gibbs_derivative
#print axioms quadratic_gibbs_tangent_continuous
#print axioms quadraticGibbsCurve
#print axioms quadratic_gibbs_positive
#print axioms quadratic_gibbs_tangent_zero
#print axioms quadratic_gibbs_relative_entropy_zero
#print axioms quadratic_gibbs_modular_limit
#print axioms quadratic_gibbs_entropy_limit
end
end ChatgptAudit.Thermal024
