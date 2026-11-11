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
import TGLExt.GibbsTilt

set_option autoImplicit false
set_option maxHeartbeats 10000000
namespace ChatgptAudit.Thermal024
open Matrix Filter Topology Set ChatgptAudit.Micro021
noncomputable section
variable {ι : Type} [Fintype ι]

def modularMean (p : ι → ℝ) : ℝ := ∑ i, p i*modularScore p i
def modularVariance (p : ι → ℝ) : ℝ := ∑ i, p i*(modularScore p i-modularMean p)^2

theorem gibbs_mean_zero (p : ι → ℝ) (hs : ∑ i, p i=1) :
    gibbsMean p 0=modularMean p := by
  simp only [gibbsMean,gibbs_weights_zero p hs,modularMean]

theorem gibbs_tangent_zero (p : ι → ℝ) (hs : ∑ i, p i=1) (i : ι) :
    gibbsTangent p 0 i=p i*(modularMean p-modularScore p i) := by
  rw [gibbsTangent,gibbs_weights_zero p hs,gibbs_mean_zero p hs]

theorem modular_variance_nonnegative (p : ι → ℝ) (hp : ∀ i, 0<p i) :
    0 ≤ modularVariance p :=
  Finset.sum_nonneg (fun i _ => mul_nonneg (le_of_lt (hp i)) (sq_nonneg _))

theorem modular_variance_second_moment (p : ι → ℝ) (hs : ∑ i, p i=1) :
    modularVariance p=(∑ i, p i*(modularScore p i)^2)-(modularMean p)^2 := by
  calc
    modularVariance p=∑ i, (p i*(modularScore p i)^2-
        2*modularMean p*(p i*modularScore p i)+(modularMean p)^2*p i) := by
      apply Finset.sum_congr rfl
      intro i _
      ring
    _=(∑ i, p i*(modularScore p i)^2)-2*modularMean p*modularMean p+(modularMean p)^2 := by
      rw [Finset.sum_add_distrib,Finset.sum_sub_distrib,←Finset.mul_sum,←Finset.mul_sum,hs,mul_one]
      rfl
    _=_ := by ring

theorem modular_variance_zero_iff_centered (p : ι → ℝ) (hp : ∀ i, 0<p i) :
    modularVariance p=0 ↔ ∀ i, modularScore p i=modularMean p := by
  constructor
  · intro hz i
    by_contra hn
    have hpos : 0<p i*(modularScore p i-modularMean p)^2 :=
      mul_pos (hp i) (sq_pos_of_ne_zero (sub_ne_zero.mpr hn))
    have hle : p i*(modularScore p i-modularMean p)^2 ≤ modularVariance p :=
      Finset.single_le_sum (fun j _ => mul_nonneg (le_of_lt (hp j))
        (sq_nonneg (modularScore p j-modularMean p))) (Finset.mem_univ i)
    rw [hz] at hle
    linarith
  · intro hh
    simp [modularVariance,hh]

theorem modular_variance_zero_iff_tracial (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) :
    modularVariance p=0 ↔ ∀ i j, p i=p j := by
  rw [modular_variance_zero_iff_centered p hp]
  constructor
  · intro hh i j
    apply Real.log_injOn_pos (hp i) (hp j)
    have he := (hh i).trans (hh j).symm
    unfold modularScore at he
    linarith only [he]
  · intro hh i
    have hmean : modularMean p=modularScore p i := by
      unfold modularMean
      have he : ∀ j, modularScore p j=modularScore p i := fun j => congrArg (fun a => -Real.log a) (hh j i)
      simp only [he,←Finset.sum_mul,hs,one_mul]
    exact hmean.symm

theorem modular_variance_positive (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1)
    (hn : ∃ i j, p i≠p j) : 0 < modularVariance p := by
  have hne : modularVariance p≠0 := by
    intro hz
    obtain ⟨i,j,hij⟩ := hn
    exact hij ((modular_variance_zero_iff_tracial p hp hs).mp hz i j)
  exact lt_of_le_of_ne (modular_variance_nonnegative p hp) (Ne.symm hne)

theorem gibbs_tangent_modular_coefficient (p : ι → ℝ) (hs : ∑ i, p i=1) :
    (∑ i, gibbsTangent p 0 i*modularScore p i)= -modularVariance p := by
  rw [modular_variance_second_moment p hs]
  calc
    (∑ i, gibbsTangent p 0 i*modularScore p i)=
        ∑ i, (modularMean p*(p i*modularScore p i)-p i*(modularScore p i)^2) := by
      apply Finset.sum_congr rfl
      intro i _
      rw [gibbs_tangent_zero p hs]
      ring
    _=modularMean p*modularMean p-(∑ i, p i*(modularScore p i)^2) := by
      rw [Finset.sum_sub_distrib,←Finset.mul_sum]
      rfl
    _=_ := by ring

variable [Nonempty ι]

theorem gibbs_modular_increment_derivative_zero (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) :
    HasDerivAt (fun s => modularIncrement p (gibbsWeights p s)) (-modularVariance p) 0 := by
  have hh := HasDerivAt.sum (u := Finset.univ)
    (fun i _ => ((gibbs_weights_derivative p hp 0 i).sub_const (p i)).mul_const (modularScore p i))
  rw [gibbs_tangent_modular_coefficient p hs] at hh
  have he : (∑ i, fun s => (gibbsWeights p s i-p i)*modularScore p i)=
      (fun s => modularIncrement p (gibbsWeights p s)) := by
    funext s
    simp only [Finset.sum_apply,modularIncrement,modularScore]
  rw [he] at hh
  exact hh

theorem gibbs_entropy_derivative_zero (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) :
    HasDerivAt (fun s => finiteEntropy (gibbsWeights p s)) (-modularVariance p) 0 := by
  have hK := gibbs_modular_increment_derivative_zero p hp hs
  have hD := relative_curve_derivative_zero (gibbsStateCurve p hp hs) hp
  have hd := hK.sub hD
  have he : (fun s => modularIncrement p (gibbsWeights p s)-diagonalRelativeEntropy (gibbsWeights p s) p)=
      (fun s => finiteEntropy (gibbsWeights p s)-finiteEntropy p) := by
    funext s
    rw [relative_entropy_identity]
    ring
  change HasDerivAt (fun s => modularIncrement p (gibbsWeights p s)-
    diagonalRelativeEntropy (gibbsWeights p s) p) (-modularVariance p-0) 0 at hd
  rw [he,sub_zero] at hd
  simpa only [sub_add_cancel] using hd.add_const (finiteEntropy p)

omit [Nonempty ι] in
theorem gibbs_fisher_is_modular_variance (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) :
    diagonalFisher p (gibbsTangent p 0)=modularVariance p := by
  unfold diagonalFisher modularVariance
  apply Finset.sum_congr rfl
  intro i _
  rw [gibbs_tangent_zero p hs]
  field_simp [ne_of_gt (hp i)]
  ring

theorem gibbs_relative_entropy_quadratic (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) :
    Tendsto (fun s => diagonalRelativeEntropy (gibbsWeights p s) p/s^2)
      (𝓝[<] 0) (𝓝 (modularVariance p/2)) := by
  have hh := relative_entropy_curve_quadratic_limit (gibbsStateCurve p hp hs) hp
  change Tendsto (fun s => diagonalRelativeEntropy (gibbsWeights p s) p/s^2)
    (𝓝[<] 0) (𝓝 (diagonalFisher p (gibbsTangent p 0)/2)) at hh
  rwa [gibbs_fisher_is_modular_variance p hp hs] at hh

#print axioms gibbs_mean_zero
#print axioms gibbs_tangent_zero
#print axioms modular_variance_nonnegative
#print axioms modular_variance_second_moment
#print axioms modular_variance_zero_iff_centered
#print axioms modular_variance_zero_iff_tracial
#print axioms modular_variance_positive
#print axioms gibbs_tangent_modular_coefficient
#print axioms gibbs_modular_increment_derivative_zero
#print axioms gibbs_entropy_derivative_zero
#print axioms gibbs_fisher_is_modular_variance
#print axioms gibbs_relative_entropy_quadratic
end
end ChatgptAudit.Thermal024
