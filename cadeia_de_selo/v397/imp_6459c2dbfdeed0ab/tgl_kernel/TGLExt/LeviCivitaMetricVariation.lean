-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 058..062 (09/09/2026), transposta em 10/09/2026 (ENTREGA_062 = elo do lote)
-- Os 77 modulos da sessao de 09/09 da bancada (cadeia de copias integradas 63 -> 72 -> 77 sobre a base v337 lida),
--   1065 teoremas declarados pela bancada. Cinco entregas espontaneas:
--   058: ATLAS GRAVITACIONAL SELECIONADO — continuidade + amostras densas + cortes racionais determinam o registro em U;
--     a leitura geometricLogReading caracteriza a sequencia booleana; a selecao por classe instancia IALDState e os
--     teoremas do Nome; o decodificador devolve classe, g, T e os pesos; Einstein do registro decodificado decorre das
--     leis de area e conservacao do registro original (jets, Levi-Civita, Ricci, Einstein preservados).
--   059: caracter completo reconstroi g/T/Einstein condicionado a area e conservacao; COLAGEM da Lambda unico nas
--     cartas compativeis; naturalidade infinitesimal de Ricci/escalar/Einstein em carta curva; potencial XX somavel
--     auto-adjunto com cauda em norma; exemplo de acoplamento atestado.
--   060: COCICLO UNITARIO INFINITO do potencial XX somavel na acao modular canonica; controle uniforme dos cortes;
--     gerador iV e ODE; grupo beta_t = Ad_u(t) o alpha_t que preserva o fator; transformacao finita de
--     Levi-Civita/Ricci/escalar/Einstein e lei de transformacao de Einstein nas sobreposicoes metricas abertas.
--   061: interacao local somavel com termos NAO comutativos (testemunha explicita); unicidade potencial <-> cociclo;
--     fase central Z^{-it} (gerador i(V - logZ I)); colagem suave selecionada -> Lambda global unico; estado perturbado
--     de Araki [DERIVED + KNOWN, analitico — NAO Lean].
--   062: seletor canonico e Born; reconstrucao do registro pelo seletor; entrelacamento angular; caracter da fase
--     relativa (duas probabilidades de interferencia recuperam a fase); estimativas de localidade de vinculo.
--   Estatuto: [REAL] o compilado; [DERIVED + KNOWN] Araki; [INPUT] R (o registro) e a origem fisica; [OPEN]
--   correspondencia fisica seletor-registro, materia/conservacao/area para os mesmos dados, atlas fisico compativel,
--   alem da classe globalmente limitada, anomalias e UV. Nenhum nome ligado a H3, area fisica ou gate.
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (INTEGRATION_RESULT 77 -> 72
--   -> 63); 77/77 hashes lidos dos bytes contra os recibos; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   77/77 contra o kernel v337, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.MetricFieldConnection
import TGLExt.TensorNullCone
import TGLExt.SmoothMatrixCalculus
import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.Calculus.FDeriv.Mul

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.MetricVariation
open Matrix Filter Topology Set
open scoped ContDiff Matrix.Norms.Operator
noncomputable section

def metricPerturbation (g h : TensorField4) (t : ℝ) : TensorField4 :=
  fun x => g x + t • h x

def perturbedMetricInverse (g h : TensorField4) (t : ℝ) : TensorField4 :=
  fun x => (metricPerturbation g h t x)⁻¹

def perturbedLeviCivita (g h : TensorField4) (t : ℝ) :=
  leviCivitaField (metricPerturbation g h t) (perturbedMetricInverse g h t)

def metricConnectionVariation (g h : TensorField4) (x : Coordinate4) (i : Fin 4) : Tensor4 :=
  (-((g x)⁻¹ * h x * (g x)⁻¹)) * lowerChristoffelJet (tensorFieldJet g x) i +
    (g x)⁻¹ * lowerChristoffelJet (tensorFieldJet h x) i

theorem matrix_affine_derivative (g h : Tensor4) :
    HasDerivAt (fun t : ℝ => g+t • h) h 0 := by
  convert! (hasDerivAt_const (0:ℝ) g).add ((hasDerivAt_id (0:ℝ)).smul_const h) using 1
  simp

theorem matrix_inverse_first_variation (g h : Tensor4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => (g+t • h)⁻¹) (-(g⁻¹*h*g⁻¹)) 0 := by
  rcases hg with ⟨u,rfl⟩
  have hd := (hasFDerivAt_ringInverse (𝕜 := ℝ) u).comp_hasDerivAt_of_eq
    (0:ℝ) (matrix_affine_derivative (u:Tensor4) h) (by simp)
  have he : ((u⁻¹ : Tensor4ˣ) : Tensor4) = (u:Tensor4)⁻¹ := by
    rw [Matrix.nonsing_inv_eq_ringInverse,Ring.inverse_unit]
  simp only [Function.comp_def, _root_.neg_apply,
    ContinuousLinearMap.mulLeftRight_apply, he] at hd
  convert! hd using 1
  simp only [Matrix.nonsing_inv_eq_ringInverse]

theorem lower_christoffel_add (dg dh : Fin 4 → Tensor4) (i : Fin 4) :
    lowerChristoffelJet (dg+dh) i = lowerChristoffelJet dg i + lowerChristoffelJet dh i := by
  ext a b
  simp only [lowerChristoffelJet,Pi.add_apply,Matrix.add_apply]
  ring

theorem lower_christoffel_smul (t : ℝ) (dh : Fin 4 → Tensor4) (i : Fin 4) :
    lowerChristoffelJet (t • dh) i = t • lowerChristoffelJet dh i := by
  ext a b
  simp only [lowerChristoffelJet,Pi.smul_apply,Matrix.smul_apply,smul_eq_mul]
  ring

theorem metric_perturbation_jet (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (x : Coordinate4) (hx : x∈U) (t : ℝ) :
    tensorFieldJet (metricPerturbation g h t) x =
      tensorFieldJet g x + t • tensorFieldJet h x := by
  have hgd := smooth_matrix_differentiableAt U hU g hg x hx
  have hhd := smooth_matrix_differentiableAt U hU h hh x hx
  have hScaled : ∀ a b, DifferentiableAt ℝ (fun y => (t • h y) a b) x :=
    fun a b => (hhd a b).const_mul t
  exact (tensorFieldJet_add g (fun y => t • h y) x hgd hScaled).trans
    (by rw [tensorFieldJet_const_smul t h x hhd])

theorem perturbed_levi_civita_jet_formula (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (x : Coordinate4) (hx : x∈U) (t : ℝ) (i : Fin 4) :
    perturbedLeviCivita g h t x i =
      (g x+t • h x)⁻¹ *
        (lowerChristoffelJet (tensorFieldJet g x) i +
          t • lowerChristoffelJet (tensorFieldJet h x) i) := by
  unfold perturbedLeviCivita leviCivitaField leviCivitaJet
  rw [metric_perturbation_jet U hU g h hg hh x hx t,lower_christoffel_add,lower_christoffel_smul]
  rfl

theorem levi_civita_metric_first_variation (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (x : Coordinate4) (hx : x∈U) (hunit : IsUnit (g x)) (i : Fin 4) :
    HasDerivAt (fun t : ℝ => perturbedLeviCivita g h t x i)
      (metricConnectionVariation g h x i) 0 := by
  have he : (fun t : ℝ => perturbedLeviCivita g h t x i) =
      (fun t => (g x+t • h x)⁻¹ *
        (lowerChristoffelJet (tensorFieldJet g x) i +
          t • lowerChristoffelJet (tensorFieldJet h x) i)) := by
    funext t
    exact perturbed_levi_civita_jet_formula U hU g h hg hh x hx t i
  rw [he]
  have hd := (matrix_inverse_first_variation (g x) (h x) hunit).mul
    (matrix_affine_derivative (lowerChristoffelJet (tensorFieldJet g x) i)
      (lowerChristoffelJet (tensorFieldJet h x) i))
  convert! hd using 1
  simp [metricConnectionVariation]

theorem metric_connection_variation_formula (g h : TensorField4)
    (x : Coordinate4) (i : Fin 4) :
    metricConnectionVariation g h x i =
      -(g x)⁻¹ * h x * leviCivitaField g (fun y => (g y)⁻¹) x i +
        (g x)⁻¹ * lowerChristoffelJet (tensorFieldJet h x) i := by
  simp only [metricConnectionVariation,leviCivitaField,leviCivitaJet]
  noncomm_ring


theorem metric_perturbation_symmetric (g h : TensorField4) (t : ℝ)
    (x : Coordinate4) (hg : (g x)ᵀ=g x) (hh : (h x)ᵀ=h x) :
    (metricPerturbation g h t x)ᵀ=metricPerturbation g h t x := by
  simp only [metricPerturbation,Matrix.transpose_add,Matrix.transpose_smul,hg,hh]

theorem matrix_perturbation_eventually_invertible (g h : Tensor4) (hg : IsUnit g) :
    ∀ᶠ t : ℝ in 𝓝 0, IsUnit (g+t • h) := by
  have hcont := (matrix_affine_derivative g h).continuousAt
  have hnb : {M : Tensor4 | IsUnit M} ∈ 𝓝 (g+(0:ℝ) • h) := by
    convert! (Units.isOpen (R := Tensor4)).mem_nhds hg using 1
    simp
    rfl
  exact hcont.eventually hnb

theorem perturbed_levi_civita_torsion_free (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : ∀ x∈U, (g x)ᵀ=g x) (hh : ∀ x∈U, (h x)ᵀ=h x)
    (t : ℝ) :
    ∀ x∈U, ∀ i j a, perturbedLeviCivita g h t x i a j =
      perturbedLeviCivita g h t x j a i :=
  levi_civita_field_torsion_free U hU (metricPerturbation g h t)
    (perturbedMetricInverse g h t)
    (fun x hx => metric_perturbation_symmetric g h t x (hg x hx) (hh x hx))


theorem perturbed_levi_civita_metric_compatible (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : ∀ x∈U, (g x)ᵀ=g x) (hh : ∀ x∈U, (h x)ᵀ=h x)
    (t : ℝ) (hi : ∀ x∈U, IsUnit (metricPerturbation g h t x)) :
    ∀ x∈U, ∀ i, covariantTensorJet (metricPerturbation g h t x)
      (tensorFieldJet (metricPerturbation g h t) x) (perturbedLeviCivita g h t x) i=0 := by
  exact levi_civita_field_metric_compatible U hU (metricPerturbation g h t)
    (perturbedMetricInverse g h t)
    (fun x hx => metric_perturbation_symmetric g h t x (hg x hx) (hh x hx))
    (fun x hx => Matrix.nonsing_inv_mul _ ((Matrix.isUnit_iff_isUnit_det _).mp (hi x hx)))
    (fun x hx => Matrix.mul_nonsing_inv _ ((Matrix.isUnit_iff_isUnit_det _).mp (hi x hx)))

theorem constant_metric_jet (G : Tensor4) (x : Coordinate4) :
    tensorFieldJet (fun _ => G) x=0 := by
  ext i a b
  simp [tensorFieldJet, coordinatePartial]

theorem constant_background_metric_variation (G : Tensor4) (h : TensorField4)
    (x : Coordinate4) (i : Fin 4) :
    metricConnectionVariation (fun _ => G) h x i =
      G⁻¹ * lowerChristoffelJet (tensorFieldJet h x) i := by
  have hz : lowerChristoffelJet (0 : Fin 4 → Tensor4) i=0 := by
    ext a b
    simp [lowerChristoffelJet]
  simp only [metricConnectionVariation, constant_metric_jet, hz, mul_zero, zero_add]

#print axioms metricPerturbation
#print axioms perturbedMetricInverse
#print axioms perturbedLeviCivita
#print axioms metricConnectionVariation
#print axioms matrix_affine_derivative
#print axioms matrix_inverse_first_variation
#print axioms lower_christoffel_add
#print axioms lower_christoffel_smul
#print axioms metric_perturbation_jet
#print axioms perturbed_levi_civita_jet_formula
#print axioms levi_civita_metric_first_variation
#print axioms metric_connection_variation_formula
#print axioms metric_perturbation_symmetric
#print axioms matrix_perturbation_eventually_invertible
#print axioms perturbed_levi_civita_torsion_free
#print axioms perturbed_levi_civita_metric_compatible
#print axioms constant_metric_jet
#print axioms constant_background_metric_variation
end
end ChatgptAudit.MetricVariation
