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
import TGLExt.TensorNullCone

set_option autoImplicit false
set_option maxHeartbeats 2400000

namespace ChatgptAudit.ConeVolume
open Matrix TGLExt ChatgptAudit
noncomputable section

/-- Coordinate volume density; its change of chart is not asserted here. -/
def metricVolumeDensity (g : Tensor4) : ℝ := Real.sqrt |g.det|

theorem tensor_quad_smul (c : ℝ) (g : Tensor4) (v : SpacetimeVector) :
    tensorQuad (c • g) v = c * tensorQuad g v := by
  simp [tensorQuad, Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul]

theorem positive_fourth_power_one (c : ℝ) (hc : 0 < c) (hp : c^4 = 1) : c = 1 := by
  have hfactor : (c^2-1)*(c^2+1) = 0 := by nlinarith only [hp]
  have hplus : c^2+1 ≠ 0 := by positivity
  have hsq : c^2 = 1 := sub_eq_zero.mp ((mul_eq_zero.mp hfactor).resolve_right hplus)
  have hfactor2 : (c-1)*(c+1) = 0 := by nlinarith only [hsq]
  have hplus2 : c+1 ≠ 0 := by positivity
  exact sub_eq_zero.mp ((mul_eq_zero.mp hfactor2).resolve_right hplus2)

/-- Null directions first force conformality; a common positive direction fixes its sign. -/
theorem common_positive_null_cone_proportional
    (A g : Tensor4) (hA : Aᵀ = A) (hg : LorentzByCongruence g)
    (hcone : ∀ v, tensorQuad g v = 0 → tensorQuad A v = 0)
    (u : SpacetimeVector) (hgu : 0 < tensorQuad g u) (hAu : 0 < tensorQuad A u) :
    ∃ c : ℝ, 0 < c ∧ A = c • g := by
  obtain ⟨c,hc⟩ := lorentz_tensor_null_rigidity A g hA hg hcone
  refine ⟨c,?_,hc⟩
  rw [hc,tensor_quad_smul] at hAu
  exact (mul_pos_iff_of_pos_right hgu).mp hAu

/-- Equality of the signed determinant is a useful intermediate normalization. -/
theorem same_null_cone_determinant_and_sign
    (A g : Tensor4) (hA : Aᵀ = A) (hg : LorentzByCongruence g)
    (hcone : ∀ v, tensorQuad g v = 0 → tensorQuad A v = 0)
    (hdet : A.det = g.det) (hne : g.det ≠ 0)
    (u : SpacetimeVector) (hgu : 0 < tensorQuad g u) (hAu : 0 < tensorQuad A u) :
    A = g := by
  obtain ⟨c,hc,hAg⟩ := common_positive_null_cone_proportional A g hA hg hcone u hgu hAu
  rw [hAg,Matrix.det_smul] at hdet
  simp only [Fintype.card_fin] at hdet
  have hp : c^4 = 1 := mul_right_cancel₀ hne (hdet.trans (one_mul g.det).symm)
  rw [hAg,positive_fourth_power_one c hc hp,one_smul]

/-- Equal nonnegative volume densities determine equal absolute determinants. -/
theorem equal_volume_density_absolute_determinant (A g : Tensor4)
    (hv : metricVolumeDensity A = metricVolumeDensity g) : |A.det| = |g.det| := by
  have h := congrArg (fun r : ℝ => r^2) hv
  simpa only [metricVolumeDensity,Real.sq_sqrt (abs_nonneg _)] using h

/-- Pointwise uniqueness for arbitrary Lorentzian metrics, without a metric ansatz.
The causal origin of the cone and the origin of the volume reading remain inputs. -/
theorem same_null_cone_volume_and_sign
    (A g : Tensor4) (hA : Aᵀ = A) (hg : LorentzByCongruence g)
    (hcone : ∀ v, tensorQuad g v = 0 → tensorQuad A v = 0)
    (hvolume : metricVolumeDensity A = metricVolumeDensity g) (hne : g.det ≠ 0)
    (u : SpacetimeVector) (hgu : 0 < tensorQuad g u) (hAu : 0 < tensorQuad A u) :
    A = g := by
  obtain ⟨c,hc,hAg⟩ := common_positive_null_cone_proportional A g hA hg hcone u hgu hAu
  have habs := equal_volume_density_absolute_determinant A g hvolume
  rw [hAg,Matrix.det_smul] at habs
  simp only [Fintype.card_fin,abs_mul,abs_of_nonneg (by positivity : 0 ≤ c^4)] at habs
  have hp : c^4 = 1 := mul_right_cancel₀ (abs_ne_zero.mpr hne)
    (habs.trans (one_mul |g.det|).symm)
  rw [hAg,positive_fourth_power_one c hc hp,one_smul]

/-- A mathematical record schema, not a construction of physical observables. -/
structure ConeVolumeRecord where
  nullDirections : Set SpacetimeVector
  density : ℝ
  positiveDirection : SpacetimeVector

/-- A candidate metric realizes the recorded cone, volume and sign convention. -/
def RealizesConeVolume (R : ConeVolumeRecord) (g : Tensor4) : Prop :=
  gᵀ = g ∧ LorentzByCongruence g ∧ g.det ≠ 0 ∧
  (∀ v, v ∈ R.nullDirections ↔ tensorQuad g v = 0) ∧
  metricVolumeDensity g = R.density ∧ 0 < tensorQuad g R.positiveDirection

/-- At most one metric realizes a record; existence is a separate obligation. -/
theorem cone_volume_record_unique (R : ConeVolumeRecord) (A g : Tensor4)
    (hA : RealizesConeVolume R A) (hg : RealizesConeVolume R g) : A = g := by
  rcases hA with ⟨hAs,_,_,hAn,hAv,hAu⟩
  rcases hg with ⟨_,hgL,hgn,hgc,hgv,hgu⟩
  exact same_null_cone_volume_and_sign A g hAs hgL
    (fun v hv => (hAn v).mp ((hgc v).mpr hv)) (hAv.trans hgv.symm)
    hgn R.positiveDirection hgu hAu

/-- Field uniqueness is pointwise on any coordinate domain; no constant factor is assumed. -/
theorem cone_volume_field_unique {X : Type} (R : X → ConeVolumeRecord)
    (A g : X → Tensor4)
    (hA : ∀ x, RealizesConeVolume (R x) (A x))
    (hg : ∀ x, RealizesConeVolume (R x) (g x)) : A = g := by
  funext x
  exact cone_volume_record_unique (R x) (A x) (g x) (hA x) (hg x)

/-- Rescaling preserves all null directions if its factor is nonzero. -/
theorem nonzero_rescaling_preserves_null_cone (g : Tensor4) (c : ℝ) (hc : c ≠ 0)
    (v : SpacetimeVector) : tensorQuad (c • g) v = 0 ↔ tensorQuad g v = 0 := by
  rw [tensor_quad_smul,mul_eq_zero]
  simp only [hc,false_or]

/-- Without volume normalization, a positive rescaling preserves the cone and sign. -/
theorem volume_omission_control :
    (∀ v, tensorQuad ((2:ℝ) • eta4) v = 0 ↔ tensorQuad eta4 v = 0) ∧
    0 < tensorQuad eta4 (![1,0,0,0] : SpacetimeVector) ∧
    0 < tensorQuad ((2:ℝ) • eta4) (![1,0,0,0] : SpacetimeVector) ∧
    (2:ℝ) • eta4 ≠ eta4 := by
  refine ⟨fun v => nonzero_rescaling_preserves_null_cone eta4 2 (by norm_num) v,?_,?_,?_⟩
  · norm_num [tensorQuad_eta]
  · rw [tensor_quad_smul,tensorQuad_eta]
    norm_num
  · intro h
    have he := congrArg (fun A : Tensor4 => tensorQuad A ![1,0,0,0]) h
    rw [tensor_quad_smul,tensorQuad_eta] at he
    norm_num at he

/-- Reversing the metric sign preserves the volume in dimension four. -/
theorem sign_reversal_volume (g : Tensor4) :
    metricVolumeDensity ((-1:ℝ) • g) = metricVolumeDensity g := by
  unfold metricVolumeDensity
  rw [Matrix.det_smul]
  norm_num

/-- Without a sign convention, cone and volume cannot distinguish g from -g. -/
theorem sign_omission_control :
    (∀ v, tensorQuad ((-1:ℝ) • eta4) v = 0 ↔ tensorQuad eta4 v = 0) ∧
    metricVolumeDensity ((-1:ℝ) • eta4) = metricVolumeDensity eta4 ∧
    (-1:ℝ) • eta4 ≠ eta4 := by
  refine ⟨fun v => nonzero_rescaling_preserves_null_cone eta4 (-1) (by norm_num) v,
    sign_reversal_volume eta4,?_⟩
  intro h
  have he := congrArg (fun A : Tensor4 => tensorQuad A ![1,0,0,0]) h
  rw [tensor_quad_smul,tensorQuad_eta] at he
  norm_num at he

#print axioms metricVolumeDensity
#print axioms tensor_quad_smul
#print axioms positive_fourth_power_one
#print axioms common_positive_null_cone_proportional
#print axioms same_null_cone_determinant_and_sign
#print axioms equal_volume_density_absolute_determinant
#print axioms same_null_cone_volume_and_sign
#print axioms ConeVolumeRecord
#print axioms RealizesConeVolume
#print axioms cone_volume_record_unique
#print axioms cone_volume_field_unique
#print axioms nonzero_rescaling_preserves_null_cone
#print axioms volume_omission_control
#print axioms sign_reversal_volume
#print axioms sign_omission_control

end
end ChatgptAudit.ConeVolume
