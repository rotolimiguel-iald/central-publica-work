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
import TGLExt.MetricRicciVariation

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.MetricEinsteinVariation
open Matrix Filter Topology Set
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci
  ChatgptAudit.CurvedConnection
noncomputable section
open scoped ContDiff

def scalarMetricVariation (g h : TensorField4) (x : Coordinate4) : ℝ :=
  ∑ i : Fin 4, ∑ j : Fin 4, (
    (-(g x)⁻¹*h x*(g x)⁻¹) i j *
      coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) x i j +
    (g x)⁻¹ i j * ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
      (metricConnectionVariation g h) x i j)

def einsteinMetricVariation (g h : TensorField4) (x : Coordinate4) : Tensor4 :=
  ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
    (metricConnectionVariation g h) x -
  (scalarMetricVariation g h x / 2) • g x -
  (coordinateScalarCurvature (fun y => (g y)⁻¹)
    (leviCivitaField g (fun y => (g y)⁻¹)) x / 2) • h x

theorem metric_scalar_first_variation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U) :
    HasDerivAt (fun t => coordinateScalarCurvature
      (perturbedMetricInverse g h t) (perturbedLeviCivita g h t) x)
      (scalarMetricVariation g h x) 0 := by
  have hinv := matrix_inverse_first_variation (g x) (h x) (hi x hx)
  have hterm (i j : Fin 4) :=
    ((hasDerivAt_pi.mp (hasDerivAt_pi.mp hinv i)) j).mul
      (metric_ricci_first_variation U hU g h hg hh hi x hx i j)
  have hall := HasDerivAt.fun_sum fun i (_ : i ∈ (Finset.univ : Finset (Fin 4))) =>
    HasDerivAt.fun_sum fun j (_ : j ∈ (Finset.univ : Finset (Fin 4))) => hterm i j
  convert! hall using 1
  simp only [scalarMetricVariation, zero_smul, add_zero,
    perturbed_levi_civita_at_zero, neg_mul]

theorem metric_einstein_first_variation_component
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U) (i j : Fin 4) :
    HasDerivAt (fun t => geometricEinsteinTensor (metricPerturbation g h t)
      (perturbedMetricInverse g h t) (perturbedLeviCivita g h t) x i j)
      (einsteinMetricVariation g h x i j) 0 := by
  have hsc := (metric_scalar_first_variation U hU g h hg hh hi x hx).div_const 2
  have hmetric := (hasDerivAt_pi.mp
    (hasDerivAt_pi.mp (matrix_affine_derivative (g x) (h x)) i)) j
  have H := (metric_ricci_first_variation U hU g h hg hh hi x hx i j).sub
    (hsc.mul hmetric)
  convert! H using 1
  simp only [einsteinMetricVariation, Matrix.sub_apply, Matrix.smul_apply,
      smul_eq_mul, coordinateScalarCurvature, perturbedMetricInverse, metricPerturbation,
      perturbed_levi_civita_at_zero, zero_smul, add_zero]
  ring

theorem metric_einstein_first_variation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U) :
    HasDerivAt (fun t => geometricEinsteinTensor (metricPerturbation g h t)
      (perturbedMetricInverse g h t) (perturbedLeviCivita g h t) x)
      (einsteinMetricVariation g h x) 0 := by
  apply hasDerivAt_pi.mpr
  intro i
  apply hasDerivAt_pi.mpr
  intro j
  exact metric_einstein_first_variation_component U hU g h hg hh hi x hx i j

#print axioms scalarMetricVariation
#print axioms einsteinMetricVariation
#print axioms metric_scalar_first_variation
#print axioms metric_einstein_first_variation_component
#print axioms metric_einstein_first_variation
end
end ChatgptAudit.MetricEinsteinVariation
