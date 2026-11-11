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
import TGLExt.ContinuumTT
import TGLExt.SmoothMatrixCalculus

set_option autoImplicit false
set_option maxHeartbeats 2400000

namespace ChatgptAudit.GeneralLinearized

open TGLExt
open scoped BigOperators ContDiff

noncomputable section

abbrev Spacetime := Fin 4 → ℝ
abbrev TensorField := Fin 4 → Fin 4 → Spacetime → ℝ
abbrev CovectorField := Fin 4 → Spacetime → ℝ

theorem pd_is_coordinate_partial (f : Spacetime → ℝ) (i : Fin 4) (x : Spacetime) :
    pd i f x = coordinatePartial f x i := rfl

theorem smooth_pd (f : Spacetime → ℝ) (hf : ContDiff ℝ ∞ f) (i : Fin 4) :
    ContDiff ℝ ∞ (pd i f) := by
  exact contDiffOn_univ.mp
    (coordinatePartial_smooth Set.univ isOpen_univ f hf.contDiffOn i)

theorem pd_add_smooth (f g : Spacetime → ℝ)
    (hf : ContDiff ℝ ∞ f) (hg : ContDiff ℝ ∞ g) (i : Fin 4) :
    pd i (fun x => f x + g x) = fun x => pd i f x + pd i g x := by
  funext x
  exact coordinatePartial_add f g x
    (hf.differentiable (by simp) x) (hg.differentiable (by simp) x) i

theorem pd_mul_const_smooth (f : Spacetime → ℝ)
    (hf : ContDiff ℝ ∞ f) (c : ℝ) (i : Fin 4) :
    pd i (fun x => c * f x) = fun x => c * pd i f x := by
  funext x
  simpa [pd, coordinatePartial] using
    coordinatePartial_mul (fun _ : Spacetime => c) f x
      (differentiableAt_const c) (hf.differentiable (by simp) x) i

theorem pd_sum_smooth (F : Fin 4 → Spacetime → ℝ)
    (hF : ∀ a, ContDiff ℝ ∞ (F a)) (i : Fin 4) :
    pd i (fun x => ∑ a, F a x) = fun x => ∑ a, pd i (F a) x := by
  funext x
  exact coordinatePartial_sum F x (fun a => (hF a).differentiable (by simp) x) i

theorem pd_commute_smooth (f : Spacetime → ℝ) (hf : ContDiff ℝ ∞ f)
    (i j : Fin 4) :
    pd i (pd j f) = pd j (pd i f) := by
  funext x
  exact coordinate_partials_commute f x hf.contDiffAt i j

theorem pd_pd_add_smooth (f g : Spacetime → ℝ)
    (hf : ContDiff ℝ ∞ f) (hg : ContDiff ℝ ∞ g) (i j : Fin 4) :
    pd i (pd j (fun x => f x + g x)) =
      fun x => pd i (pd j f) x + pd i (pd j g) x := by
  rw [pd_add_smooth f g hf hg j,
    pd_add_smooth (pd j f) (pd j g) (smooth_pd f hf j) (smooth_pd g hg j) i]

theorem pd_pd_mul_const_smooth (f : Spacetime → ℝ)
    (hf : ContDiff ℝ ∞ f) (c : ℝ) (i j : Fin 4) :
    pd i (pd j (fun x => c * f x)) = fun x => c * pd i (pd j f) x := by
  rw [pd_mul_const_smooth f hf c j,
    pd_mul_const_smooth (pd j f) (smooth_pd f hf j) c i]

theorem pd_pd_sum_smooth (F : Fin 4 → Spacetime → ℝ)
    (hF : ∀ a, ContDiff ℝ ∞ (F a)) (i j : Fin 4) :
    pd i (pd j (fun x => ∑ a, F a x)) =
      fun x => ∑ a, pd i (pd j (F a)) x := by
  rw [pd_sum_smooth F hF j,
    pd_sum_smooth (fun a => pd j (F a)) (fun a => smooth_pd (F a) (hF a) j) i]

def gaugeField (ξ : CovectorField) : TensorField :=
  fun μ ν x => pd μ (ξ ν) x + pd ν (ξ μ) x

theorem gauge_field_smooth (ξ : CovectorField)
    (hξ : ∀ a, ContDiff ℝ ∞ (ξ a)) (μ ν : Fin 4) :
    ContDiff ℝ ∞ (gaugeField ξ μ ν) :=
  (smooth_pd (ξ ν) (hξ ν) μ).add (smooth_pd (ξ μ) (hξ μ) ν)

theorem gauge_field_symmetric (ξ : CovectorField) (μ ν : Fin 4) :
    gaugeField ξ μ ν = gaugeField ξ ν μ := by
  funext x
  exact add_comm _ _

theorem linRicci_as_sum (h : TensorField)
    (hh : ∀ μ ν, ContDiff ℝ ∞ (h μ ν)) (μ ν : Fin 4) (x : Spacetime) :
    linRicci h μ ν x =
      (∑ a : Fin 4, etaDiag a *
        (pd a (pd μ (h a ν)) x + pd a (pd ν (h a μ)) x
          - pd a (pd a (h μ ν)) x - pd μ (pd ν (h a a)) x)) / 2 := by
  unfold linRicci
  rw [pd_pd_sum_smooth (fun a y => etaDiag a * h a a y)
    (fun a => contDiff_const.mul (hh a a)) μ ν]
  simp only [pd_pd_mul_const_smooth _ (hh _ _) _ μ ν]
  simp only [mul_sub, Finset.sum_sub_distrib]
  ring


theorem pd_triple_cycle_smooth (f : Spacetime → ℝ) (hf : ContDiff ℝ ∞ f)
    (a b c : Fin 4) :
    pd a (pd b (pd c f)) = pd b (pd c (pd a f)) := by
  rw [pd_commute_smooth (pd c f) (smooth_pd f hf c) a b,
    pd_commute_smooth f hf a c]

theorem gauge_second_derivative (ξ : CovectorField)
    (hξ : ∀ a, ContDiff ℝ ∞ (ξ a)) (i j μ ν : Fin 4) (x : Spacetime) :
    pd i (pd j (gaugeField ξ μ ν)) x =
      pd i (pd j (pd μ (ξ ν))) x + pd i (pd j (pd ν (ξ μ))) x := by
  exact congrFun (pd_pd_add_smooth _ _
    (smooth_pd (ξ ν) (hξ ν) μ) (smooth_pd (ξ μ) (hξ μ) ν) i j) x

theorem linRicci_pure_gauge_zero (ξ : CovectorField)
    (hξ : ∀ a, ContDiff ℝ ∞ (ξ a)) (μ ν : Fin 4) (x : Spacetime) :
    linRicci (gaugeField ξ) μ ν x = 0 := by
  rw [linRicci_as_sum (gaugeField ξ) (gauge_field_smooth ξ hξ) μ ν x]
  have hterm (a : Fin 4) :
      pd a (pd μ (gaugeField ξ a ν)) x + pd a (pd ν (gaugeField ξ a μ)) x
        - pd a (pd a (gaugeField ξ μ ν)) x
        - pd μ (pd ν (gaugeField ξ a a)) x = 0 := by
    simp only [gauge_second_derivative ξ hξ]
    have e1 := congrFun
      (congrArg (pd a) (pd_commute_smooth (ξ ν) (hξ ν) μ a)) x
    have e2 := congrFun
      (congrArg (pd a) (pd_commute_smooth (ξ μ) (hξ μ) ν a)) x
    have e3 := congrFun (pd_triple_cycle_smooth (ξ a) (hξ a) a μ ν) x
    have e4 : pd a (pd ν (pd μ (ξ a))) x = pd μ (pd ν (pd a (ξ a))) x := by
      calc
        _ = pd ν (pd μ (pd a (ξ a))) x :=
          congrFun (pd_triple_cycle_smooth (ξ a) (hξ a) a ν μ) x
        _ = _ := congrFun
          (pd_commute_smooth (pd a (ξ a)) (smooth_pd (ξ a) (hξ a) a) ν μ) x
    rw [e1, e2, e3, e4]
    ring
  simp only [hterm, mul_zero, Finset.sum_const_zero, zero_div]

theorem linRicci_add_smooth (h k : TensorField)
    (hh : ∀ μ ν, ContDiff ℝ ∞ (h μ ν))
    (hk : ∀ μ ν, ContDiff ℝ ∞ (k μ ν)) (μ ν : Fin 4) (x : Spacetime) :
    linRicci (fun a b y => h a b y + k a b y) μ ν x =
      linRicci h μ ν x + linRicci k μ ν x := by
  rw [linRicci_as_sum _ (fun a b => (hh a b).add (hk a b)) μ ν x,
    linRicci_as_sum h hh μ ν x, linRicci_as_sum k hk μ ν x]
  simp only [pd_pd_add_smooth _ _ (hh _ _) (hk _ _)]
  simp only [mul_add, mul_sub, Finset.sum_add_distrib, Finset.sum_sub_distrib]
  ring

def gaugeShift (h : TensorField) (ξ : CovectorField) : TensorField :=
  fun μ ν x => h μ ν x + gaugeField ξ μ ν x

theorem general_smooth_gauge_invariance (h : TensorField) (ξ : CovectorField)
    (hh : ∀ μ ν, ContDiff ℝ ∞ (h μ ν))
    (hξ : ∀ a, ContDiff ℝ ∞ (ξ a)) (μ ν : Fin 4) (x : Spacetime) :
    linRicci (gaugeShift h ξ) μ ν x = linRicci h μ ν x := by
  unfold gaugeShift
  rw [linRicci_add_smooth h (gaugeField ξ) hh (gauge_field_smooth ξ hξ) μ ν x,
    linRicci_pure_gauge_zero ξ hξ μ ν x, add_zero]


def linScalar (h : TensorField) (x : Spacetime) : ℝ :=
  ∑ a : Fin 4, etaDiag a * linRicci h a a x

def linEinstein (h : TensorField) (μ ν : Fin 4) (x : Spacetime) : ℝ :=
  linRicci h μ ν x - (if μ = ν then etaDiag μ else 0) * linScalar h x / 2

theorem general_smooth_scalar_gauge_invariance (h : TensorField) (ξ : CovectorField)
    (hh : ∀ μ ν, ContDiff ℝ ∞ (h μ ν))
    (hξ : ∀ a, ContDiff ℝ ∞ (ξ a)) (x : Spacetime) :
    linScalar (gaugeShift h ξ) x = linScalar h x := by
  simp only [linScalar, general_smooth_gauge_invariance h ξ hh hξ]

theorem general_smooth_einstein_gauge_invariance (h : TensorField) (ξ : CovectorField)
    (hh : ∀ μ ν, ContDiff ℝ ∞ (h μ ν))
    (hξ : ∀ a, ContDiff ℝ ∞ (ξ a)) (μ ν : Fin 4) (x : Spacetime) :
    linEinstein (gaugeShift h ξ) μ ν x = linEinstein h μ ν x := by
  simp only [linEinstein, general_smooth_gauge_invariance h ξ hh hξ,
    general_smooth_scalar_gauge_invariance h ξ hh hξ]

theorem general_smooth_gauge_preserves_vacuum (h : TensorField) (ξ : CovectorField)
    (hh : ∀ μ ν, ContDiff ℝ ∞ (h μ ν))
    (hξ : ∀ a, ContDiff ℝ ∞ (ξ a)) :
    (∀ μ ν x, linRicci (gaugeShift h ξ) μ ν x = 0) ↔
      (∀ μ ν x, linRicci h μ ν x = 0) := by
  simp only [general_smooth_gauge_invariance h ξ hh hξ]

#print axioms Spacetime
#print axioms TensorField
#print axioms CovectorField
#print axioms pd_is_coordinate_partial
#print axioms smooth_pd
#print axioms pd_add_smooth
#print axioms pd_mul_const_smooth
#print axioms pd_sum_smooth
#print axioms pd_commute_smooth
#print axioms pd_pd_add_smooth
#print axioms pd_pd_mul_const_smooth
#print axioms pd_pd_sum_smooth
#print axioms gaugeField
#print axioms gauge_field_smooth
#print axioms gauge_field_symmetric
#print axioms linRicci_as_sum
#print axioms pd_triple_cycle_smooth
#print axioms gauge_second_derivative
#print axioms linRicci_pure_gauge_zero
#print axioms linRicci_add_smooth
#print axioms gaugeShift
#print axioms general_smooth_gauge_invariance
#print axioms linScalar
#print axioms linEinstein
#print axioms general_smooth_scalar_gauge_invariance
#print axioms general_smooth_einstein_gauge_invariance
#print axioms general_smooth_gauge_preserves_vacuum

end
end ChatgptAudit.GeneralLinearized
