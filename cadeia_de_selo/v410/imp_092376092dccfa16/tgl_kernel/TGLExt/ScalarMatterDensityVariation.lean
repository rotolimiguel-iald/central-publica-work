-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 063..066 (09/09/2026, noite), transposta em 10/09/2026 (ENTREGA_067 = elo do lote)
-- Os 21 modulos restantes da bancada (elos 83 -> 93 -> 98 da cadeia de copias integradas; 77 ja na v338).
--   063 (6 modulos, 113 teoremas): RESPOSTA GIBBS ANTES DA FONTE — protocolo misto (W = X + Z, medicao Z, s = v^2 t^2):
--     igualdade das respostas de entropia e energia de referencia na ordem quadratica; a fonte calculada da resposta com
--     conservacao por closed/wave; o seletor transporta o registro; O LIMITE LOCAL DE INTERACOES EXTENSIVAS (Lean);
--     a lei fisica de area e a metrica seguem entradas. [DERIVED, escrito]: Araki/GNS, tempo global, KMS no fecho C*.
--   065 (10 modulos, 108 teoremas): estabilidade do prefixo do caracter, resolucao finita, controle de malha do
--     registro, cotas de erro da resposta finita, precisao finita de Gibbs misto, janela de amostragem; METRICA DE
--     FISHER-LORENTZ SELECIONADA, variacao da densidade de materia escalar, ponte Fisher-Gibbs, CONSERVACAO sigma.
--   066 (5 modulos, 67 teoremas): sigma DOS MESMOS P (phi_j = sqrt(P_j/(1 - P_s))), resposta de Gibbs ASSINADA (dois
--     sinais com probabilidades positivas), esperanca negativa renormalizada, cobertura, reconstrucao por DEZ LIMITES
--     (SignedGibbsFiniteRecord); T e entrada; nao se identifica o observavel com stress de QFT.
--   Estatuto: [REAL] o compilado; [INPUT] a lei de area, a metrica, T, a acao/particao; [DERIVED + KNOWN] Araki, GNS,
--   KMS C*; [OPEN] correspondencia geral de selecao/materia/protocolo/area, realizacao interagente, anomalias, UV.
--   As ENTREGAS 067..087 sao MATEMATICA ESCRITA REVISADA (CAS, sem Lean) — registradas no diario e no Atlas como
--   [DERIVED], nao como flags; a propria bancada: "nao promover demonstracoes escritas a flags de compilacao".
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (98 -> 93 -> 83 -> 77...),
--   77 ja no kernel pulados; 21/21 hashes lidos dos bytes; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   21/21 contra o kernel v338, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.MetricEinsteinVariation
import TGLExt.MixedGibbsGravitationalBridge
import TGLExt.ConeVolumeReconstruction
import Mathlib.Analysis.Calculus.FDeriv.Analytic
import Mathlib.Analysis.Calculus.Deriv.Abs
import Mathlib.Analysis.SpecialFunctions.Sqrt

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.ScalarMatterVariation
open Matrix Filter Topology Set
  ChatgptAudit.MetricVariation ChatgptAudit.Coherent023
  ChatgptAudit.FiniteCoherentSource ChatgptAudit.ConeVolume
noncomputable section

def determinantMultilinear : ContinuousMultilinearMap ℝ (fun _ : Fin 4 => Fin 4 → ℝ) ℝ :=
  { Matrix.detRowAlternating.toMultilinearMap with cont := continuous_id.matrix_det }

theorem determinant_row_first_variation (g h : Tensor4) :
    HasDerivAt (fun t : ℝ => (g+t • h).det)
      (∑ i : Fin 4, (Matrix.updateRow g i (h i)).det) 0 := by
  have H := (determinantMultilinear.hasFDerivAt g).comp_hasDerivAt_of_eq
    (0:ℝ) (matrix_affine_derivative g h) (by simp)
  convert! H using 1

theorem determinant_row_replacement (g h : Tensor4) (hg : IsUnit g) (i : Fin 4) :
    (Matrix.updateRow g i (h i)).det = (h*g⁻¹) i i * g.det := by
  have hl : h*g⁻¹*g=h := by rw [Matrix.mul_assoc,Matrix.nonsing_inv_mul _ (g.isUnit_iff_isUnit_det.mp hg),Matrix.mul_one]
  have he : h i = ∑ j : Fin 4, (h*g⁻¹) i j • g j := by
    funext k
    simpa only [Matrix.mul_apply,Finset.sum_apply,Pi.smul_apply,smul_eq_mul] using congrFun (congrFun hl i) k |>.symm
  rw [he,Matrix.det_updateRow_sum]
  rfl

theorem determinant_first_variation (g h : Tensor4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => (g+t • h).det) (g.det*(h*g⁻¹).trace) 0 := by
  convert! determinant_row_first_variation g h using 1
  simp only [determinant_row_replacement g h hg,Matrix.trace,Matrix.diag,←Finset.sum_mul]
  ring

theorem absolute_determinant_first_variation (g h : Tensor4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => |(g+t • h).det|) (|g.det| * (h*g⁻¹).trace) 0 := by
  have hd := determinant_first_variation g h hg
  have hn : g.det ≠ 0 := (g.isUnit_iff_isUnit_det.mp hg).ne_zero
  rcases lt_or_gt_of_ne hn with hn | hn
  · have H := (hasDerivAt_abs_neg hn).comp_of_eq 0 hd (by simp)
    simpa only [Function.comp_def,abs_of_neg hn,neg_one_mul,neg_mul,one_mul] using H
  · have H := (hasDerivAt_abs_pos hn).comp_of_eq 0 hd (by simp)
    simpa only [Function.comp_def,abs_of_pos hn,one_mul] using H

theorem metric_volume_first_variation (g h : Tensor4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => metricVolumeDensity (g+t • h))
      (metricVolumeDensity g/2*(h*g⁻¹).trace) 0 := by
  have hn : |g.det| ≠ 0 := abs_ne_zero.mpr (g.isUnit_iff_isUnit_det.mp hg).ne_zero
  have H := (absolute_determinant_first_variation g h hg).sqrt (by simpa using hn)
  have hs : Real.sqrt |g.det| ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr (abs_pos.mpr (g.isUnit_iff_isUnit_det.mp hg).ne_zero))
  convert! H using 1
  simp only [zero_smul,add_zero,metricVolumeDensity]
  field_simp
  rw [Real.sq_sqrt (abs_nonneg g.det)]
  ring

theorem quadratic_inverse_first_variation (g h : Tensor4) (w : Coordinate4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => tensorQuad (g+t • h)⁻¹ w)
      (-tensorQuad (g⁻¹*h*g⁻¹) w) 0 := by
  have hi := matrix_inverse_first_variation g h hg
  have H := HasDerivAt.fun_sum fun i (_ : i∈(Finset.univ : Finset (Fin 4))) =>
    (HasDerivAt.fun_sum fun j (_ : j∈(Finset.univ : Finset (Fin 4))) =>
      (((hasDerivAt_pi.mp (hasDerivAt_pi.mp hi i)) j).mul_const (w j))).const_mul (w i)
  convert! H using 1
  simp only [tensorQuad,Matrix.mulVec,dotProduct,Matrix.neg_apply,neg_mul,
    Finset.sum_neg_distrib,mul_neg]

def scalarMatterDensity {J : Type} [Fintype J] (g : Tensor4) (w : J → Coordinate4) (c : J → ℝ) : ℝ :=
  metricVolumeDensity g/2 * ∑ j, c j * tensorQuad g⁻¹ (w j)

theorem scalar_density_raw_first_variation {J : Type} [Fintype J]
    (g h : Tensor4) (w : J → Coordinate4) (c : J → ℝ) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => scalarMatterDensity (g+t • h) w c)
      (metricVolumeDensity g/2*((h*g⁻¹).trace/2*∑ j, c j*tensorQuad g⁻¹ (w j))-
        metricVolumeDensity g/2*∑ j, c j*tensorQuad (g⁻¹*h*g⁻¹) (w j)) 0 := by
  have Hv := (metric_volume_first_variation g h hg).div_const 2
  have Hq := HasDerivAt.fun_sum fun j (_ : j∈(Finset.univ : Finset J)) =>
    (quadratic_inverse_first_variation g h (w j) hg).const_mul (c j)
  convert! Hv.mul Hq using 1
  simp only [zero_smul,add_zero,mul_neg,Finset.sum_neg_distrib]
  ring

def scalarMatterStress {J : Type} [Fintype J] (g : Tensor4) (w : J → Coordinate4) (c : J → ℝ) : Tensor4 :=
  finiteCovectorStressField (fun _ => g) (fun _ => g⁻¹) (fun j _ => w j) (fun _ => 1) c 0

theorem scalar_matter_stress_formula {J : Type} [Fintype J]
    (g : Tensor4) (w : J → Coordinate4) (c : J → ℝ) :
    scalarMatterStress g w c =
      ∑ j, c j • (Matrix.vecMulVec (w j) (w j)-(tensorQuad g⁻¹ (w j)/2) • g) := by
  simp only [scalarMatterStress,finiteCovectorStressField,covectorStressField,covectorStress,one_smul]

theorem quadratic_trace_outer (A : Tensor4) (w : Coordinate4) :
    (A*Matrix.vecMulVec w w).trace=tensorQuad A w := by
  rw [Matrix.mul_vecMulVec,Matrix.trace_vecMulVec,dotProduct_comm]
  rfl

theorem stress_trace_variation {J : Type} [Fintype J]
    (g h : Tensor4) (w : J → Coordinate4) (c : J → ℝ) (hg : IsUnit g) :
    ((g⁻¹*h*g⁻¹)*scalarMatterStress g w c).trace =
      (∑ j, c j*tensorQuad (g⁻¹*h*g⁻¹) (w j))-
        (h*g⁻¹).trace/2*(∑ j, c j*tensorQuad g⁻¹ (w j)) := by
  have hl : g⁻¹*h*g⁻¹*g=g⁻¹*h := by
    rw [Matrix.mul_assoc (g⁻¹*h),Matrix.nonsing_inv_mul _ (g.isUnit_iff_isUnit_det.mp hg),Matrix.mul_one]
  rw [scalar_matter_stress_formula,Matrix.mul_sum,Matrix.trace_sum]
  simp only [Matrix.mul_smul,Matrix.trace_smul,Matrix.mul_sub,Matrix.trace_sub,
    quadratic_trace_outer,hl,Matrix.trace_mul_comm g⁻¹ h,smul_eq_mul]
  rw [Finset.mul_sum,←Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem scalar_matter_density_first_variation {J : Type} [Fintype J]
    (g h : Tensor4) (w : J → Coordinate4) (c : J → ℝ) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => scalarMatterDensity (g+t • h) w c)
      (-metricVolumeDensity g/2*((g⁻¹*h*g⁻¹)*scalarMatterStress g w c).trace) 0 := by
  convert! scalar_density_raw_first_variation g h w c hg using 1
  rw [stress_trace_variation g h w c hg]
  ring

theorem scalar_matter_density_raised_trace {J : Type} [Fintype J]
    (g h : Tensor4) (w : J → Coordinate4) (c : J → ℝ) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => scalarMatterDensity (g+t • h) w c)
      (-metricVolumeDensity g/2*(h*(g⁻¹*scalarMatterStress g w c*g⁻¹)).trace) 0 := by
  convert! scalar_matter_density_first_variation g h w c hg using 1
  congr 1
  simpa only [Matrix.mul_assoc] using
    (Matrix.trace_mul_comm (h*g⁻¹*scalarMatterStress g w c) g⁻¹)

theorem symmetric_trace_pairing (h R : Tensor4) (hh : hᵀ=h) :
    (h*R).trace=∑ i : Fin 4, ∑ j : Fin 4, R i j*h i j := by
  simp only [Matrix.trace,Matrix.diag,Matrix.mul_apply]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  have hs : h j i=h i j := congrFun (congrFun hh i) j
  rw [hs,mul_comm]

theorem scalar_matter_density_covariant_variation {J : Type} [Fintype J]
    (g h : Tensor4) (w : J → Coordinate4) (c : J → ℝ) (hg : IsUnit g) (hh : hᵀ=h) :
    HasDerivAt (fun t : ℝ => scalarMatterDensity (g+t • h) w c)
      (-metricVolumeDensity g/2*(∑ a : Fin 4, ∑ b : Fin 4,
        (g⁻¹*scalarMatterStress g w c*g⁻¹) a b*h a b)) 0 := by
  simpa only [symmetric_trace_pairing h _ hh] using
    scalar_matter_density_raised_trace g h w c hg

theorem scalar_stress_equals_finite_field {J : Type} [Fintype J]
    (g : TensorField4) (w : J → CovectorField4) (c : J → ℝ) (x : Coordinate4) :
    scalarMatterStress (g x) (fun j => w j x) c=
      finiteCovectorStressField g (fun y => (g y)⁻¹) w (fun _ => 1) c x := rfl

theorem gibbs_scalar_coupling_positive (k : ℝ) (hk : 0<k) :
    0<k/(Real.pi*Real.cosh k^2) := by positivity

theorem gibbs_scalar_matter_density_first_variation {J : Type} [Fintype J]
    (g h : TensorField4) (w : J → CovectorField4) (k : J → ℝ)
    (x : Coordinate4) (hg : IsUnit (g x)) (hh : (h x)ᵀ=h x) :
    HasDerivAt (fun t : ℝ => scalarMatterDensity (g x+t • h x) (fun j => w j x)
      (fun j => k j/(Real.pi*Real.cosh (k j)^2)))
      (-metricVolumeDensity (g x)/2*(∑ a : Fin 4, ∑ b : Fin 4,
        ((g x)⁻¹*(finiteCovectorStressField g (fun y => (g y)⁻¹) w (fun _ => 1)
          (fun j => k j/(Real.pi*Real.cosh (k j)^2)) x)*(g x)⁻¹) a b*h x a b)) 0 := by
  simpa only [scalar_stress_equals_finite_field] using
    scalar_matter_density_covariant_variation (g x) (h x) (fun j => w j x)
      (fun j => k j/(Real.pi*Real.cosh (k j)^2)) hg hh

#print axioms determinantMultilinear
#print axioms determinant_row_first_variation
#print axioms determinant_row_replacement
#print axioms determinant_first_variation
#print axioms absolute_determinant_first_variation
#print axioms metric_volume_first_variation
#print axioms quadratic_inverse_first_variation
#print axioms scalarMatterDensity
#print axioms scalar_density_raw_first_variation
#print axioms scalarMatterStress
#print axioms scalar_matter_stress_formula
#print axioms quadratic_trace_outer
#print axioms stress_trace_variation
#print axioms scalar_matter_density_first_variation
#print axioms scalar_matter_density_raised_trace
#print axioms symmetric_trace_pairing
#print axioms scalar_matter_density_covariant_variation
#print axioms scalar_stress_equals_finite_field
#print axioms gibbs_scalar_coupling_positive
#print axioms gibbs_scalar_matter_density_first_variation
end
end ChatgptAudit.ScalarMatterVariation
