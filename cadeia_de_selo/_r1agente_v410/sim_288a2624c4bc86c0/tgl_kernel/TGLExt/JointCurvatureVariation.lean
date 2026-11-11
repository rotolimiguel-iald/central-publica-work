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
import TGLExt.CurvatureNonlinearVariation
import Mathlib.Analysis.Calculus.Deriv.Prod

set_option autoImplicit false
set_option maxHeartbeats 2500000
namespace ChatgptAudit.JointCurvature
open Matrix Filter Topology Set ChatgptAudit.CurvedConnection
open scoped ContDiff
noncomputable section

abbrev ParameterSpace := ℝ × Coordinate4

def jointPartial (F : ParameterSpace → ℝ) (v : ParameterSpace) (z : ParameterSpace) : ℝ :=
  fderiv ℝ F z v

def JointSmoothConnectionOn (W : Set ParameterSpace) (Gamma : ℝ → ConnectionField4) : Prop :=
  ∀ i a b, ContDiffOn ℝ ∞ (fun z : ParameterSpace => Gamma z.1 z.2 i a b) W

def connectionTimeDerivative (Gamma : ℝ → ConnectionField4) (t : ℝ) : ConnectionField4 :=
  fun x i a b => jointPartial (fun z => Gamma z.1 z.2 i a b) (1,0) (t,x)

theorem joint_partial_smooth (W : Set ParameterSpace) (hW : IsOpen W)
    (F : ParameterSpace → ℝ) (hF : ContDiffOn ℝ ∞ F W) (v : ParameterSpace) :
    ContDiffOn ℝ ∞ (jointPartial F v) W := by
  exact (hF.fderiv_of_isOpen hW (by simp)).clm_apply contDiffOn_const

theorem joint_partial_second (F : ParameterSpace → ℝ) (z : ParameterSpace)
    (hF : ContDiffAt ℝ ∞ F z) (v w : ParameterSpace) :
    jointPartial (jointPartial F v) w z = fderiv ℝ (fderiv ℝ F) z w v := by
  have hd : DifferentiableAt ℝ (fderiv ℝ F) z :=
    (hF.fderiv_right (m := 1) (by
      exact WithTop.coe_le_coe.mpr (show (2 : ℕ∞) ≤ ⊤ from le_top))).differentiableAt
        (by norm_num)
  unfold jointPartial
  rw [fderiv_clm_apply hd (differentiableAt_const v)]
  simp

theorem joint_partials_commute (F : ParameterSpace → ℝ) (z : ParameterSpace)
    (hF : ContDiffAt ℝ ∞ F z) (v w : ParameterSpace) :
    jointPartial (jointPartial F v) w z = jointPartial (jointPartial F w) v z := by
  rw [joint_partial_second F z hF v w, joint_partial_second F z hF w v]
  exact (hF.isSymmSndFDerivAt (by
    simp only [minSmoothness_of_isRCLikeNormedField]
    exact WithTop.coe_le_coe.mpr le_top)).eq _ _

theorem time_slice_derivative (F : ParameterSpace → ℝ) (t : ℝ) (x : Coordinate4)
    (hF : DifferentiableAt ℝ F (t,x)) :
    HasDerivAt (fun s => F (s,x)) (jointPartial F (1,0) (t,x)) t := by
  have h := hF.hasFDerivAt.comp_hasDerivAt t
    ((hasDerivAt_id t).prodMk (hasDerivAt_const t x))
  simpa only [Function.comp_def, jointPartial, id_eq] using h

theorem space_slice_partial (F : ParameterSpace → ℝ) (t : ℝ) (x : Coordinate4)
    (hF : DifferentiableAt ℝ F (t,x)) (i : Fin 4) :
    coordinatePartial (fun y => F (t,y)) x i =
      jointPartial F (0,Pi.single i 1) (t,x) := by
  have h := hF.hasFDerivAt.comp x
    ((hasFDerivAt_const t x).prodMk (hasFDerivAt_id x))
  simp only [Function.comp_def] at h
  unfold coordinatePartial jointPartial
  rw [h.fderiv]
  rfl

theorem time_derivative_of_space_partial
    (W : Set ParameterSpace) (hW : IsOpen W) (F : ParameterSpace → ℝ)
    (hF : ContDiffOn ℝ ∞ F W) (t : ℝ) (x : Coordinate4) (hz : (t,x)∈W) (i : Fin 4) :
    HasDerivAt (fun s => coordinatePartial (fun y => F (s,y)) x i)
      (coordinatePartial (fun y => jointPartial F (1,0) (t,y)) x i) t := by
  have hfAt : ContDiffAt ℝ ∞ F (t,x) := (hF (t,x) hz).contDiffAt (hW.mem_nhds hz)
  have hsAt : DifferentiableAt ℝ (jointPartial F (0,Pi.single i 1)) (t,x) :=
    (((joint_partial_smooth W hW F hF (0,Pi.single i 1)) (t,x) hz).contDiffAt
      (hW.mem_nhds hz)).differentiableAt (by simp)
  have htAt : DifferentiableAt ℝ (jointPartial F (1,0)) (t,x) :=
    (((joint_partial_smooth W hW F hF (1,0)) (t,x) hz).contDiffAt
      (hW.mem_nhds hz)).differentiableAt (by simp)
  have hd := time_slice_derivative (jointPartial F (0,Pi.single i 1)) t x hsAt
  have hmem : ∀ᶠ s : ℝ in 𝓝 t, (s,x)∈W :=
    (continuousAt_id.prodMk continuousAt_const).eventually (hW.mem_nhds hz)
  have he : (fun s => coordinatePartial (fun y => F (s,y)) x i) =ᶠ[𝓝 t]
      (fun s => jointPartial F (0,Pi.single i 1) (s,x)) := by
    filter_upwards [hmem] with s hs
    exact space_slice_partial F s x
      (((hF (s,x) hs).contDiffAt (hW.mem_nhds hs)).differentiableAt (by simp)) i
  have H := hd.congr_of_eventuallyEq he
  convert! H using 1
  rw [space_slice_partial (jointPartial F (1,0)) t x htAt i]
  exact (joint_partials_commute F (t,x) hfAt (0,Pi.single i 1) (1,0)).symm

theorem connection_parameter_derivative
    (W : Set ParameterSpace) (hW : IsOpen W) (Gamma : ℝ → ConnectionField4)
    (hG : JointSmoothConnectionOn W Gamma) (t : ℝ) (x : Coordinate4)
    (hz : (t,x)∈W) (i a b : Fin 4) :
    HasDerivAt (fun s => Gamma s x i a b) (connectionTimeDerivative Gamma t x i a b) t :=
  time_slice_derivative (fun z => Gamma z.1 z.2 i a b) t x
    (((hG i a b (t,x) hz).contDiffAt (hW.mem_nhds hz)).differentiableAt (by simp))

theorem connection_first_jet_parameter_derivative
    (W : Set ParameterSpace) (hW : IsOpen W) (Gamma : ℝ → ConnectionField4)
    (hG : JointSmoothConnectionOn W Gamma) (t : ℝ) (x : Coordinate4)
    (hz : (t,x)∈W) (i j a b : Fin 4) :
    HasDerivAt (fun s => connectionFirstJet (Gamma s) x i j a b)
      (connectionFirstJet (connectionTimeDerivative Gamma t) x i j a b) t :=
  time_derivative_of_space_partial W hW (fun z => Gamma z.1 z.2 j a b) (hG j a b)
    t x hz i

theorem curvature_of_joint_family_derivative
    (W : Set ParameterSpace) (hW : IsOpen W) (Gamma : ℝ → ConnectionField4)
    (hG : JointSmoothConnectionOn W Gamma) (t : ℝ) (x : Coordinate4)
    (hz : (t,x)∈W) (i j a b : Fin 4) :
    HasDerivAt (fun s => coordinateCurvature (Gamma s) x i j a b)
      (curvatureVariation (Gamma t) (connectionTimeDerivative Gamma t) x i j a b) t := by
  have hjet := connection_first_jet_parameter_derivative W hW Gamma hG t x hz
  have hd := connection_parameter_derivative W hW Gamma hG t x hz
  have hp (i j : Fin 4) := HasDerivAt.fun_sum (u := Finset.univ)
    (fun k _ => (hd i a k).mul (hd j k b))
  have H := ((hjet i j a b).sub (hjet j i a b)).add (hp i j) |>.sub (hp j i)
  convert! H using 1
  simp only [curvatureVariation, Matrix.add_apply, Matrix.sub_apply, Matrix.mul_apply,
    Finset.sum_add_distrib]
  ring

theorem ricci_of_joint_family_derivative
    (W : Set ParameterSpace) (hW : IsOpen W) (Gamma : ℝ → ConnectionField4)
    (hG : JointSmoothConnectionOn W Gamma) (t : ℝ) (x : Coordinate4)
    (hz : (t,x)∈W) (b j : Fin 4) :
    HasDerivAt (fun s => coordinateRicci (Gamma s) x b j)
      (ricciVariation (Gamma t) (connectionTimeDerivative Gamma t) x b j) t := by
  simpa only [coordinateRicci, ricciVariation] using
    HasDerivAt.fun_sum (u := Finset.univ)
      (fun a _ => curvature_of_joint_family_derivative W hW Gamma hG t x hz a j a b)

#print axioms ParameterSpace
#print axioms jointPartial
#print axioms JointSmoothConnectionOn
#print axioms connectionTimeDerivative
#print axioms joint_partial_smooth
#print axioms joint_partial_second
#print axioms joint_partials_commute
#print axioms time_slice_derivative
#print axioms space_slice_partial
#print axioms time_derivative_of_space_partial
#print axioms connection_parameter_derivative
#print axioms connection_first_jet_parameter_derivative
#print axioms curvature_of_joint_family_derivative
#print axioms ricci_of_joint_family_derivative
end
end ChatgptAudit.JointCurvature
