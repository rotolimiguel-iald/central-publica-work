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
import TGLExt.JointCurvatureVariation
import TGLExt.LeviCivitaMetricVariation

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.MetricRicci
open Matrix Filter Topology Set ChatgptAudit.CurvedConnection
  ChatgptAudit.JointCurvature ChatgptAudit.MetricVariation
open scoped ContDiff
noncomputable section

def JointSmoothMatrixOn (W : Set ParameterSpace) (A : ParameterSpace → Tensor4) : Prop :=
  ∀ i j, ContDiffOn ℝ ∞ (fun z => A z i j) W

#print axioms JointSmoothMatrixOn

def metricJointField (g h : TensorField4) (z : ParameterSpace) : Tensor4 :=
  g z.2 + z.1 • h z.2

#print axioms metricJointField

def metricNonsingularDomain (U : Set Coordinate4) (g h : TensorField4) : Set ParameterSpace :=
  {z | z.2∈U ∧ (metricJointField g h z).det≠0}

#print axioms metricNonsingularDomain

theorem joint_matrix_determinant_smooth
    (W : Set ParameterSpace) (A : ParameterSpace → Tensor4) (hA : JointSmoothMatrixOn W A) :
    ContDiffOn ℝ ∞ (fun z => (A z).det) W := by
  simp_rw [Matrix.det_apply']
  unfold JointSmoothMatrixOn at hA
  fun_prop

#print axioms joint_matrix_determinant_smooth

theorem joint_matrix_adjugate_smooth
    (W : Set ParameterSpace) (A : ParameterSpace → Tensor4) (hA : JointSmoothMatrixOn W A) :
    JointSmoothMatrixOn W (fun z => (A z).adjugate) := by
  intro i j
  simp_rw [Matrix.adjugate_apply]
  apply joint_matrix_determinant_smooth W (fun z => (A z).updateRow j (Pi.single i 1))
  intro a b
  by_cases he : a=j
  · simp only [Matrix.updateRow_apply, he, if_true]
    exact contDiffOn_const
  · simp only [Matrix.updateRow_apply, he, if_false]
    exact hA a b

#print axioms joint_matrix_adjugate_smooth

theorem joint_matrix_inverse_smooth
    (W : Set ParameterSpace) (A : ParameterSpace → Tensor4) (hA : JointSmoothMatrixOn W A)
    (hdet : ∀ z∈W, (A z).det≠0) :
    JointSmoothMatrixOn W (fun z => (A z)⁻¹) := by
  have hd := (joint_matrix_determinant_smooth W A hA).inv hdet
  have ha := joint_matrix_adjugate_smooth W A hA
  intro i j
  simpa only [Matrix.inv_def, Ring.inverse_eq_inv', Matrix.smul_apply, smul_eq_mul] using
    hd.mul (ha i j)

#print axioms joint_matrix_inverse_smooth

theorem metric_joint_field_smooth (U : Set Coordinate4) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h) :
    JointSmoothMatrixOn {z : ParameterSpace | z.2∈U} (metricJointField g h) := by
  intro i j
  change ContDiffOn ℝ ∞ (fun z : ParameterSpace => g z.2 i j + z.1*h z.2 i j) _
  exact ((hg i j).comp contDiffOn_snd (fun z hz => hz)).add
    (contDiffOn_fst.mul ((hh i j).comp contDiffOn_snd (fun z hz => hz)))

#print axioms metric_joint_field_smooth

theorem metric_nonsingular_domain_open (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h) :
    IsOpen (metricNonsingularDomain U g h) := by
  let V : Set ParameterSpace := {z | z.2∈U}
  have hV : IsOpen V := hU.preimage continuous_snd
  have hD := joint_matrix_determinant_smooth V (metricJointField g h)
    (metric_joint_field_smooth U g h hg hh)
  apply isOpen_iff_mem_nhds.mpr
  intro z hz
  have hcont : ContinuousAt (fun w => (metricJointField g h w).det) z :=
    hD.continuousOn.continuousAt (hV.mem_nhds hz.1)
  have hne : {r : ℝ | r≠0} ∈ 𝓝 ((metricJointField g h z).det) :=
    isOpen_ne.mem_nhds hz.2
  filter_upwards [hV.mem_nhds hz.1, hcont.eventually hne] with y hy hd
  exact ⟨hy,hd⟩

#print axioms metric_nonsingular_domain_open

theorem metric_zero_in_domain (U : Set Coordinate4) (g h : TensorField4)
    (x : Coordinate4) (hx : x∈U) (hi : IsUnit (g x)) :
    (0,x)∈metricNonsingularDomain U g h := by
  change x∈U ∧ (g x+(0:ℝ) • h x).det≠0
  simpa only [zero_smul, add_zero] using
    And.intro hx (isUnit_iff_ne_zero.mp ((Matrix.isUnit_iff_isUnit_det (g x)).mp hi))

#print axioms metric_zero_in_domain

theorem lower_metric_jet_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hg : SmoothMatrixOn U g) (i a b : Fin 4) :
    ContDiffOn ℝ ∞ (fun x => lowerChristoffelJet (tensorFieldJet g x) i a b) U :=
  (((tensorFieldJet_smooth U hU g hg i a b).add
    (tensorFieldJet_smooth U hU g hg b i a)).sub
      (tensorFieldJet_smooth U hU g hg a i b)).div_const 2

#print axioms lower_metric_jet_smooth

theorem perturbed_levi_civita_joint_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h) :
    JointSmoothConnectionOn (metricNonsingularDomain U g h) (perturbedLeviCivita g h) := by
  let W := metricNonsingularDomain U g h
  have hA : JointSmoothMatrixOn W (metricJointField g h) := by
    intro i j
    exact (metric_joint_field_smooth U g h hg hh i j).mono (fun z hz => hz.1)
  have hInv := joint_matrix_inverse_smooth W (metricJointField g h) hA (fun z hz => hz.2)
  have hLg (i a b : Fin 4) :
      ContDiffOn ℝ ∞ (fun z : ParameterSpace =>
        lowerChristoffelJet (tensorFieldJet g z.2) i a b) W :=
    (lower_metric_jet_smooth U hU g hg i a b).comp contDiffOn_snd (fun z hz => hz.1)
  have hLh (i a b : Fin 4) :
      ContDiffOn ℝ ∞ (fun z : ParameterSpace =>
        lowerChristoffelJet (tensorFieldJet h z.2) i a b) W :=
    (lower_metric_jet_smooth U hU h hh i a b).comp contDiffOn_snd (fun z hz => hz.1)
  intro i a b
  have hRhs : ContDiffOn ℝ ∞ (fun z : ParameterSpace =>
      ∑ k : Fin 4, (metricJointField g h z)⁻¹ a k *
        (lowerChristoffelJet (tensorFieldJet g z.2) i k b +
          z.1*lowerChristoffelJet (tensorFieldJet h z.2) i k b)) W := by
    apply ContDiffOn.sum
    intro k _
    exact (hInv a k).mul ((hLg i k b).add (contDiffOn_fst.mul (hLh i k b)))
  apply hRhs.congr
  intro z hz
  exact congrArg (fun M : Tensor4 => M a b)
    (perturbed_levi_civita_jet_formula U hU g h hg hh z.2 hz.1 z.1 i)

#print axioms perturbed_levi_civita_joint_smooth

theorem perturbed_levi_civita_at_zero (g h : TensorField4) :
    perturbedLeviCivita g h 0 = leviCivitaField g (fun x => (g x)⁻¹) := by
  unfold perturbedLeviCivita perturbedMetricInverse metricPerturbation
  simp only [zero_smul, add_zero]

#print axioms perturbed_levi_civita_at_zero

theorem metric_time_derivative_eq_on (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x∈U, IsUnit (g x)) :
    EqOn (connectionTimeDerivative (perturbedLeviCivita g h) 0)
      (metricConnectionVariation g h) U := by
  intro x hx
  funext i a b
  have H := connection_parameter_derivative (metricNonsingularDomain U g h)
    (metric_nonsingular_domain_open U hU g h hg hh) (perturbedLeviCivita g h)
    (perturbed_levi_civita_joint_smooth U hU g h hg hh) 0 x
    (metric_zero_in_domain U g h x hx (hi x hx)) i a b
  have M := levi_civita_metric_first_variation U hU g h hg hh x hx (hi x hx) i
  exact H.unique ((hasDerivAt_pi.mp (hasDerivAt_pi.mp M a)) b)

#print axioms metric_time_derivative_eq_on

theorem ricci_variation_congr_on (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C D : ConnectionField4) (hCD : EqOn C D U) (x : Coordinate4) (hx : x∈U) :
    ricciVariation Gamma C x=ricciVariation Gamma D x := by
  have hJ (i j : Fin 4) : connectionFirstJet C x i j=connectionFirstJet D x i j :=
    congrArg (fun J => J i) (tensorFieldJet_congr_on U hU
      (fun y => C y j) (fun y => D y j)
      (fun y hy => congrFun (hCD hy) j) x hx)
  ext b j
  simp only [ricciVariation]
  apply Finset.sum_congr rfl
  intro a _
  unfold curvatureVariation
  rw [hJ a j, hJ j a, hCD hx]

#print axioms ricci_variation_congr_on

/-- The derivative is of the actual metric-induced Levi-Civita family, with no jet hypothesis. -/
theorem metric_ricci_first_variation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) (b j : Fin 4) :
    HasDerivAt (fun t => coordinateRicci (perturbedLeviCivita g h t) x b j)
      (ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
        (metricConnectionVariation g h) x b j) 0 := by
  have H := ricci_of_joint_family_derivative (metricNonsingularDomain U g h)
    (metric_nonsingular_domain_open U hU g h hg hh) (perturbedLeviCivita g h)
    (perturbed_levi_civita_joint_smooth U hU g h hg hh) 0 x
    (metric_zero_in_domain U g h x hx (hi x hx)) b j
  rw [perturbed_levi_civita_at_zero] at H
  rw [ricci_variation_congr_on U hU _ _ _
    (metric_time_derivative_eq_on U hU g h hg hh hi) x hx] at H
  exact H

#print axioms metric_ricci_first_variation

end
end ChatgptAudit.MetricRicci
