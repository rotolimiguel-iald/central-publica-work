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
import TGLExt.UnitaryDuhamel
import TGLExt.CanonicalCocycleDerivative
import Mathlib.Analysis.Calculus.Deriv.Star
import Mathlib.Analysis.Calculus.MeanValue

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.CocycleUniqueness
open TGLExt ChatgptAudit.UnitaryDuhamel ChatgptAudit.CocycleDerivative
noncomputable section

theorem same_generator_product_derivative (P : SiteProfile)
    (u v A : ℝ → Operator P) (hA : ∀ t, star (A t) = -A t)
    (hu : ∀ t, HasDerivAt u (u t * A t) t)
    (hv : ∀ t, HasDerivAt v (v t * A t) t) (t : ℝ) :
    HasDerivAt (fun s => u s * star (v s)) 0 t := by
  have hd := (hu t).mul ((hv t).star)
  convert! hd using 1;
    simp only [star_mul, hA t, neg_mul, mul_neg, mul_assoc, add_neg_cancel]

theorem same_generator_product_constant (P : SiteProfile)
    (u v A : ℝ → Operator P) (hA : ∀ t, star (A t) = -A t)
    (hu : ∀ t, HasDerivAt u (u t * A t) t)
    (hv : ∀ t, HasDerivAt v (v t * A t) t) (t : ℝ) :
    u t * star (v t) = u 0 * star (v 0) := by
  have hd := same_generator_product_derivative P u v A hA hu hv
  exact is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt)
    (fun s => (hd s).deriv) t 0

theorem unitary_right_generator_unique (P : SiteProfile)
    (u v A : ℝ → Operator P) (hA : ∀ t, star (A t) = -A t)
    (hu : ∀ t, HasDerivAt u (u t * A t) t)
    (hv : ∀ t, HasDerivAt v (v t * A t) t)
    (hu0 : u 0 = 1) (hv0 : v 0 = 1)
    (hvu : ∀ t, v t ∈ unitary _) : u = v := by
  funext t
  have he := same_generator_product_constant P u v A hA hu hv t
  rw [hu0, hv0, star_one, mul_one] at he
  have hc := congrArg (fun B : Operator P => B * v t) he
  simpa only [mul_assoc, Unitary.star_mul_self_of_mem (hvu t), mul_one,
    one_mul] using hc

theorem canonical_generator_skew (P : SiteProfile) (V : Operator P)
    (hV : IsSelfAdjoint V) (t : ℝ) :
    star (Complex.I • modularConjugation P t V) =
      -(Complex.I • modularConjugation P t V) := by
  rw [star_smul, ← map_star, hV.star_eq]
  simp only [Complex.star_def, Complex.conj_I, neg_smul]

theorem canonical_right_generator_unique (P : SiteProfile)
    (u v : ℝ → Operator P) (V : Operator P) (hV : IsSelfAdjoint V)
    (hu : ∀ t, HasDerivAt u (u t * (Complex.I • modularConjugation P t V)) t)
    (hv : ∀ t, HasDerivAt v (v t * (Complex.I • modularConjugation P t V)) t)
    (hu0 : u 0 = 1) (hv0 : v 0 = 1)
    (hvu : ∀ t, v t ∈ unitary _) : u = v :=
  unitary_right_generator_unique P u v _ (canonical_generator_skew P V hV)
    hu hv hu0 hv0 hvu

theorem canonical_cocycle_unique_from_derivative (P : SiteProfile)
    (u v : ℝ → Operator P) (V : Operator P) (hV : IsSelfAdjoint V)
    (huc : ∀ s t, u (s+t) = u s * modularConjugation P s (u t))
    (hvc : ∀ s t, v (s+t) = v s * modularConjugation P s (v t))
    (hud : HasDerivAt u (Complex.I • V) 0)
    (hvd : HasDerivAt v (Complex.I • V) 0)
    (hu0 : u 0 = 1) (hv0 : v 0 = 1)
    (hvu : ∀ t, v t ∈ unitary _) : u = v :=
  canonical_right_generator_unique P u v V hV
    (canonical_cocycle_generator_equation P u V huc hud)
    (canonical_cocycle_generator_equation P v V hvc hvd) hu0 hv0 hvu

#print axioms same_generator_product_derivative
#print axioms same_generator_product_constant
#print axioms unitary_right_generator_unique
#print axioms canonical_generator_skew
#print axioms canonical_right_generator_unique
#print axioms canonical_cocycle_unique_from_derivative
end
end ChatgptAudit.CocycleUniqueness
