-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_021 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.RelativeEntropyFisherLimit

set_option autoImplicit false
set_option maxHeartbeats 6000000
namespace ChatgptAudit.Micro021
open Matrix Filter Topology Set
noncomputable section
variable {ι : Type} [Fintype ι]

def affineStateCurve (p q : ι → ℝ) (hs : ∑ i, p i=1) (hq : ∑ i, q i=0) :
    DiagonalStateCurve p where
  weights := fun t i => p i+t*q i
  tangent := fun _ => q
  at_zero := by intro i; simp
  trace_one := by
    intro t
    simp only [Finset.sum_add_distrib,←Finset.mul_sum,hq,mul_zero,add_zero,hs]
  derivative_zero := by
    intro i
    simpa using ((hasDerivAt_id (0:ℝ)).mul_const (q i)).const_add (p i)
  derivative_past := by
    filter_upwards [] with t
    intro i
    simpa using ((hasDerivAt_id t).mul_const (q i)).const_add (p i)
  tangent_continuous := fun _ => continuousAt_const

def quadraticStateCurve (p q : ι → ℝ) (hs : ∑ i, p i=1) (hq : ∑ i, q i=0) :
    DiagonalStateCurve p where
  weights := fun t i => p i+t^2*q i
  tangent := fun t i => 2*t*q i
  at_zero := by intro i; simp
  trace_one := by
    intro t
    simp only [Finset.sum_add_distrib,←Finset.mul_sum,hq,mul_zero,add_zero,hs]
  derivative_zero := by
    intro i
    simpa using (((hasDerivAt_id (0:ℝ)).pow 2).mul_const (q i)).const_add (p i)
  derivative_past := by
    filter_upwards [] with t
    intro i
    simpa using (((hasDerivAt_id t).pow 2).mul_const (q i)).const_add (p i)
  tangent_continuous := by
    intro i
    fun_prop

theorem modular_increment_affine (p q : ι → ℝ) (t : ℝ) :
    modularIncrement p (fun i => p i+t*q i)=t*(∑ i, q i*(-Real.log (p i))) := by
  unfold modularIncrement
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem modular_increment_quadratic (p q : ι → ℝ) (t : ℝ) :
    modularIncrement p (fun i => p i+t^2*q i)=t^2*(∑ i, q i*(-Real.log (p i))) :=
  modular_increment_affine p q (t^2)

theorem affine_relative_entropy_quadratic_limit (p q : ι → ℝ)
    (hs : ∑ i, p i=1) (hq : ∑ i, q i=0) (hp : ∀ i, 0<p i) :
    Tendsto (fun t => diagonalRelativeEntropy ((affineStateCurve p q hs hq).weights t) p/t^2)
      (𝓝[<] 0) (𝓝 (diagonalFisher p q/2)) :=
  relative_entropy_curve_quadratic_limit (affineStateCurve p q hs hq) hp

theorem quadratic_relative_entropy_zero (p q : ι → ℝ)
    (hs : ∑ i, p i=1) (hq : ∑ i, q i=0) (hp : ∀ i, 0<p i) :
    Tendsto (fun t => diagonalRelativeEntropy ((quadraticStateCurve p q hs hq).weights t) p/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  apply (relative_entropy_quadratic_zero_iff (quadraticStateCurve p q hs hq) hp).mpr
  ext i
  simp [quadraticStateCurve]

theorem quadratic_modular_limit (p q : ι → ℝ) (hs : ∑ i, p i=1) (hq : ∑ i, q i=0) :
    Tendsto (fun t => modularIncrement p ((quadraticStateCurve p q hs hq).weights t)/t^2)
      (𝓝[<] 0) (𝓝 (∑ i, q i*(-Real.log (p i)))) := by
  have he : (fun t => modularIncrement p ((quadraticStateCurve p q hs hq).weights t)/t^2)
      =ᶠ[𝓝[<] (0:ℝ)] (fun _ => ∑ i, q i*(-Real.log (p i))) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    change modularIncrement p (fun i => p i+t^2*q i)/t^2=_
    rw [modular_increment_quadratic]
    change t<0 at ht
    have hn : t≠0 := ne_of_lt ht
    field_simp [hn]
  have hc : Tendsto (fun _ : ℝ => ∑ i, q i*(-Real.log (p i)))
      (𝓝[<] 0) (𝓝 (∑ i, q i*(-Real.log (p i)))) := tendsto_const_nhds
  exact hc.congr' he.symm

theorem quadratic_entropy_limit (p q : ι → ℝ) (hs : ∑ i, p i=1) (hq : ∑ i, q i=0)
    (hp : ∀ i, 0<p i) :
    Tendsto (fun t => (finiteEntropy ((quadraticStateCurve p q hs hq).weights t)-finiteEntropy p)/t^2)
      (𝓝[<] 0) (𝓝 (∑ i, q i*(-Real.log (p i)))) := by
  let X := quadraticStateCurve p q hs hq
  have hl := (quadratic_modular_limit p q hs hq).sub (quadratic_relative_entropy_zero p q hs hq hp)
  have hf : (fun t => (finiteEntropy (X.weights t)-finiteEntropy p)/t^2)=
      (fun t => modularIncrement p (X.weights t)/t^2-diagonalRelativeEntropy (X.weights t) p/t^2) := by
    funext t
    rw [relative_entropy_identity]
    ring
  change Tendsto (fun t => (finiteEntropy (X.weights t)-finiteEntropy p)/t^2) _ _
  rw [hf]
  simpa only [sub_zero] using hl

#print axioms affineStateCurve
#print axioms quadraticStateCurve
#print axioms modular_increment_affine
#print axioms modular_increment_quadratic
#print axioms affine_relative_entropy_quadratic_limit
#print axioms quadratic_relative_entropy_zero
#print axioms quadratic_modular_limit
#print axioms quadratic_entropy_limit
end
end ChatgptAudit.Micro021
