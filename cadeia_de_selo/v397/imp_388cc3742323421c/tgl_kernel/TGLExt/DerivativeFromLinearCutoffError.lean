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
import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Topology.MetricSpace.Pseudo.Basic
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.CutoffDerivative
open Filter Topology
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

theorem slope_norm_error_le (f g : ℝ → E) (e : ℝ) (he : 0 ≤ e)
    (hzero : g 0 = f 0) (hbound : ∀ t : ℝ, ‖f t-g t‖ ≤ |t| * e) (t : ℝ) :
    ‖slope f 0 t-slope g 0 t‖ ≤ e := by
  by_cases ht : t = 0
  · subst t
    simpa only [slope_def_module,sub_zero,inv_zero,zero_smul,sub_self,norm_zero] using he
  have hdiff : (f t-f 0)-(g t-g 0)=f t-g t := by
    rw [hzero]
    abel
  simp only [slope_def_module,sub_zero,←smul_sub,hdiff,norm_smul,norm_inv,Real.norm_eq_abs]
  calc
    |t|⁻¹ * ‖f t-g t‖ ≤ |t|⁻¹ * (|t| * e) :=
      mul_le_mul_of_nonneg_left (hbound t) (inv_nonneg.mpr (abs_nonneg t))
    _ = e := by rw [←mul_assoc,inv_mul_cancel₀ (abs_ne_zero.mpr ht),one_mul]

theorem hasDerivAt_of_linear_cutoff_error
    (f : ℝ → E) (fN : ℕ → ℝ → E) (dN : ℕ → E) (d : E) (e : ℕ → ℝ)
    (hzero : ∀ N, fN N 0=f 0)
    (hderiv : ∀ N, HasDerivAt (fN N) (dN N) 0)
    (hd : Tendsto dN atTop (𝓝 d))
    (he : ∀ N, 0≤e N) (he0 : Tendsto e atTop (𝓝 0))
    (hbound : ∀ N t, ‖f t-fN N t‖≤ |t| * e N) :
    HasDerivAt f d 0 := by
  apply hasDerivAt_iff_tendsto_slope.mpr
  apply Metric.tendsto_nhds.mpr
  intro ε hε
  have hthird : 0<ε/3 := by positivity
  have hev := he0.eventually (gt_mem_nhds hthird)
  have hdv := Metric.tendsto_nhds.mp hd (ε/3) hthird
  obtain ⟨N,heN,hdN⟩ := (hev.and hdv).exists
  have hsv := Metric.tendsto_nhds.mp (hderiv N).tendsto_slope (ε/3) hthird
  filter_upwards [hsv] with t ht
  have herr : dist (slope f 0 t) (slope (fN N) 0 t)≤e N := by
    rw [dist_eq_norm]
    exact slope_norm_error_le f (fN N) (e N) (he N) (hzero N) (hbound N) t
  have h1 := dist_triangle (slope f 0 t) (slope (fN N) 0 t) d
  have h2 := dist_triangle (slope (fN N) 0 t) (dN N) d
  linarith

omit [NormedSpace ℝ E] in
theorem cutoff_base_value_eq (f : ℝ → E) (fN : ℕ → ℝ → E) (e : ℕ → ℝ)
    (hbound : ∀ N t, ‖f t-fN N t‖≤ |t| * e N) (N : ℕ) :
    fN N 0=f 0 := by
  have hb := hbound N 0
  simp only [abs_zero,zero_mul] at hb
  exact (sub_eq_zero.mp (norm_eq_zero.mp (le_antisymm hb (norm_nonneg _)))).symm

theorem hasDerivAt_of_linear_cutoff_error_auto_base
    (f : ℝ → E) (fN : ℕ → ℝ → E) (dN : ℕ → E) (d : E) (e : ℕ → ℝ)
    (hderiv : ∀ N, HasDerivAt (fN N) (dN N) 0)
    (hd : Tendsto dN atTop (𝓝 d))
    (he : ∀ N, 0≤e N) (he0 : Tendsto e atTop (𝓝 0))
    (hbound : ∀ N t, ‖f t-fN N t‖≤ |t| * e N) :
    HasDerivAt f d 0 :=
  hasDerivAt_of_linear_cutoff_error f fN dN d e
    (cutoff_base_value_eq f fN e hbound) hderiv hd he he0 hbound

#print axioms slope_norm_error_le
#print axioms hasDerivAt_of_linear_cutoff_error
#print axioms cutoff_base_value_eq
#print axioms hasDerivAt_of_linear_cutoff_error_auto_base
end
end ChatgptAudit.CutoffDerivative
