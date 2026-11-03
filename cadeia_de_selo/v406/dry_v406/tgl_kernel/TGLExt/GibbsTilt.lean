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
import TGLExt.CanonicalModularStationarity

set_option autoImplicit false
set_option maxHeartbeats 10000000
namespace ChatgptAudit.Thermal024
open Matrix Filter Topology Set ChatgptAudit.Micro021
noncomputable section
variable {ι : Type} [Fintype ι] [Nonempty ι]

def modularScore (p : ι → ℝ) (i : ι) : ℝ := -Real.log (p i)
def gibbsAtom (p : ι → ℝ) (s : ℝ) (i : ι) : ℝ := p i*Real.exp (-s*modularScore p i)
def gibbsPartition (p : ι → ℝ) (s : ℝ) : ℝ := ∑ i, gibbsAtom p s i
def gibbsWeights (p : ι → ℝ) (s : ℝ) (i : ι) : ℝ := gibbsAtom p s i/gibbsPartition p s
def gibbsMean (p : ι → ℝ) (s : ℝ) : ℝ := ∑ i, gibbsWeights p s i*modularScore p i
def gibbsTangent (p : ι → ℝ) (s : ℝ) (i : ι) : ℝ :=
  gibbsWeights p s i*(gibbsMean p s-modularScore p i)

omit [Fintype ι] [Nonempty ι] in
theorem gibbs_atom_positive (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) (i : ι) :
    0<gibbsAtom p s i := mul_pos (hp i) (Real.exp_pos _)

theorem gibbs_partition_positive (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) :
    0<gibbsPartition p s := by
  exact Finset.sum_pos (fun i _ => gibbs_atom_positive p hp s i) Finset.univ_nonempty

theorem gibbs_weights_positive (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) (i : ι) :
    0<gibbsWeights p s i :=
  div_pos (gibbs_atom_positive p hp s i) (gibbs_partition_positive p hp s)

theorem gibbs_weights_normalized (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) :
    ∑ i, gibbsWeights p s i=1 := by
  simp only [gibbsWeights,←Finset.sum_div]
  exact div_self (ne_of_gt (gibbs_partition_positive p hp s))

omit [Nonempty ι] in
theorem gibbs_partition_zero (p : ι → ℝ) (hs : ∑ i, p i=1) : gibbsPartition p 0=1 := by
  simpa [gibbsPartition,gibbsAtom] using hs

omit [Nonempty ι] in
theorem gibbs_weights_zero (p : ι → ℝ) (hs : ∑ i, p i=1) (i : ι) :
    gibbsWeights p 0 i=p i := by
  simp [gibbsWeights,gibbsAtom,gibbs_partition_zero p hs]

omit [Fintype ι] [Nonempty ι] in
theorem gibbs_atom_derivative (p : ι → ℝ) (s : ℝ) (i : ι) :
    HasDerivAt (fun t => gibbsAtom p t i) (-modularScore p i*gibbsAtom p s i) s := by
  have hh := ((((hasDerivAt_id s).neg).mul_const (modularScore p i)).exp).const_mul (p i)
  dsimp only [Pi.neg_apply,id_eq] at hh
  convert hh using 1 <;> first | rfl | (unfold gibbsAtom; ring)

omit [Nonempty ι] in
theorem gibbs_partition_derivative (p : ι → ℝ) (s : ℝ) :
    HasDerivAt (gibbsPartition p) (∑ i, -modularScore p i*gibbsAtom p s i) s := by
  have hh := HasDerivAt.sum (u := Finset.univ) (fun i _ => gibbs_atom_derivative p s i)
  have he : (∑ i, fun t => gibbsAtom p t i)=gibbsPartition p := by
    funext t
    simp only [Finset.sum_apply,gibbsPartition]
  rw [he] at hh
  exact hh

theorem gibbs_partition_rate (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) :
    (∑ i, -modularScore p i*gibbsAtom p s i)= -gibbsPartition p s*gibbsMean p s := by
  unfold gibbsMean gibbsWeights
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  field_simp [ne_of_gt (gibbs_partition_positive p hp s)]

theorem gibbs_weights_derivative (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) (i : ι) :
    HasDerivAt (fun t => gibbsWeights p t i) (gibbsTangent p s i) s := by
  have hh := (gibbs_atom_derivative p s i).div (gibbs_partition_derivative p s)
    (ne_of_gt (gibbs_partition_positive p hp s))
  rw [gibbs_partition_rate p hp s] at hh
  convert hh using 1 <;> try rfl
  unfold gibbsTangent gibbsWeights
  field_simp [ne_of_gt (gibbs_partition_positive p hp s)]
  ring

theorem gibbs_weights_continuous (p : ι → ℝ) (hp : ∀ i, 0<p i) (i : ι) :
    Continuous (fun s => gibbsWeights p s i) :=
  continuous_iff_continuousAt.mpr (fun s => (gibbs_weights_derivative p hp s i).continuousAt)

theorem gibbs_mean_continuous (p : ι → ℝ) (hp : ∀ i, 0<p i) :
    Continuous (gibbsMean p) := by
  unfold gibbsMean
  exact continuous_finsetSum _ (fun i _ => (gibbs_weights_continuous p hp i).mul continuous_const)

theorem gibbs_tangent_continuous (p : ι → ℝ) (hp : ∀ i, 0<p i) (i : ι) :
    Continuous (fun s => gibbsTangent p s i) := by
  exact (gibbs_weights_continuous p hp i).mul ((gibbs_mean_continuous p hp).sub continuous_const)

def gibbsStateCurve (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) : DiagonalStateCurve p where
  weights := gibbsWeights p
  tangent := gibbsTangent p
  at_zero := gibbs_weights_zero p hs
  trace_one := gibbs_weights_normalized p hp
  derivative_zero := gibbs_weights_derivative p hp 0
  derivative_past := by
    filter_upwards [] with s
    exact gibbs_weights_derivative p hp s
  tangent_continuous := fun i => (gibbs_tangent_continuous p hp i).continuousAt

theorem gibbs_log_weights (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) (i : ι) :
    Real.log (gibbsWeights p s i)= -(1+s)*modularScore p i-Real.log (gibbsPartition p s) := by
  rw [gibbsWeights,Real.log_div (ne_of_gt (gibbs_atom_positive p hp s i))
    (ne_of_gt (gibbs_partition_positive p hp s)),gibbsAtom,
    Real.log_mul (ne_of_gt (hp i)) (Real.exp_ne_zero _),Real.log_exp]
  unfold modularScore
  ring

#print axioms gibbs_atom_positive
#print axioms gibbs_partition_positive
#print axioms gibbs_weights_positive
#print axioms gibbs_weights_normalized
#print axioms gibbs_partition_zero
#print axioms gibbs_weights_zero
#print axioms gibbs_atom_derivative
#print axioms gibbs_partition_derivative
#print axioms gibbs_partition_rate
#print axioms gibbs_weights_derivative
#print axioms gibbs_weights_continuous
#print axioms gibbs_mean_continuous
#print axioms gibbs_tangent_continuous
#print axioms gibbsStateCurve
#print axioms gibbs_log_weights
end
end ChatgptAudit.Thermal024
