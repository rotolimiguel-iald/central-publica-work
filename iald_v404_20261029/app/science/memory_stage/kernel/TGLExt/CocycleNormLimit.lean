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
import TGLExt.SummableInteractionModularOrbit
import Mathlib.Topology.UniformSpace.UniformApproximation
import Mathlib.Topology.UniformSpace.LocallyUniformConvergence
import Mathlib.Analysis.Normed.Group.Bounded
import Mathlib.Topology.Algebra.Star.Unitary

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.CocycleLimit
open TGLExt Filter Topology Set
  ChatgptAudit ChatgptAudit.SummableInteraction
  ChatgptAudit.InteractionOrbit ChatgptAudit.Cocycle030
noncomputable section

/-- Finite certificates are input; a limiting cocycle is not a field of this record. -/
structure CocycleApproximation (P : SiteProfile) where
  cutoff : ℕ → ℝ → InteractionOperator P
  error : ℕ → ℝ
  error_nonnegative : ∀ N, 0≤error N
  error_tendsto : Tendsto error atTop (𝓝 0)
  difference_bound : ∀ N M t, ‖cutoff N t-cutoff M t‖≤|t| *error (min N M)
  cutoff_continuous : ∀ N, Continuous (cutoff N)
  cutoff_unitary : ∀ N t, cutoff N t∈unitary _
  cutoff_factor : ∀ N t, cutoff N t∈theFactorObject P
  cutoff_twisted : ∀ N s t,
    cutoff N (s+t)=cutoff N s*modularConjugation P s (cutoff N t)

theorem cutoff_cauchy {P : SiteProfile} (D : CocycleApproximation P) (t : ℝ) :
    CauchySeq (fun N => D.cutoff N t) := by
  apply Metric.cauchySeq_iff.mpr
  intro ε hε
  have hδ : 0<ε/(|t|+1) := div_pos hε (by positivity)
  have hev := D.error_tendsto.eventually (gt_mem_nhds hδ)
  obtain ⟨N,hN⟩ := eventually_atTop.mp hev
  refine ⟨N,fun m hm n hn => ?_⟩
  have he := hN (min m n) (le_min hm hn)
  have hmul : (|t|+1)*D.error (min m n)<ε :=
    by simpa only [mul_comm] using (lt_div_iff₀ (by positivity : 0 < |t|+1)).mp he
  have hb := D.difference_bound m n t
  rw [dist_eq_norm]
  nlinarith [D.error_nonnegative (min m n)]

theorem cutoff_limit_exists {P : SiteProfile} (D : CocycleApproximation P) (t : ℝ) :
    ∃ A : InteractionOperator P, Tendsto (fun N => D.cutoff N t) atTop (𝓝 A) :=
  cauchySeq_tendsto_of_complete (cutoff_cauchy D t)

def limitCocycle {P : SiteProfile} (D : CocycleApproximation P) (t : ℝ) :
    InteractionOperator P := Classical.choose (cutoff_limit_exists D t)

theorem cutoff_tendsto_limit {P : SiteProfile} (D : CocycleApproximation P) (t : ℝ) :
    Tendsto (fun N => D.cutoff N t) atTop (𝓝 (limitCocycle D t)) :=
  Classical.choose_spec (cutoff_limit_exists D t)

theorem limit_cocycle_unique {P : SiteProfile} (D : CocycleApproximation P)
    (v : ℝ → InteractionOperator P)
    (hv : ∀ t, Tendsto (fun N => D.cutoff N t) atTop (𝓝 (v t))) :
    v=limitCocycle D := by
  funext t
  exact tendsto_nhds_unique (hv t) (cutoff_tendsto_limit D t)

theorem limit_cutoff_bound {P : SiteProfile} (D : CocycleApproximation P) (N : ℕ) (t : ℝ) :
    ‖limitCocycle D t-D.cutoff N t‖≤|t| *D.error N := by
  have hl := ((cutoff_tendsto_limit D t).sub_const (D.cutoff N t)).norm
  apply le_of_tendsto hl
  filter_upwards [eventually_ge_atTop N] with M hM
  simpa only [min_eq_right hM] using D.difference_bound M N t

theorem limit_uniform_error {P : SiteProfile} (D : CocycleApproximation P)
    (T : ℝ) (hT : 0≤T) (ε : ℝ) (hε : 0<ε) :
    ∃ N : ℕ, ∀ n≥N, ∀ t : ℝ, |t|≤T →
      ‖limitCocycle D t-D.cutoff n t‖<ε := by
  have hδ : 0<ε/(T+1) := div_pos hε (by positivity)
  obtain ⟨N,hN⟩ := eventually_atTop.mp
    (D.error_tendsto.eventually (gt_mem_nhds hδ))
  refine ⟨N,fun n hn t ht => ?_⟩
  have he := hN n hn
  have he' : (T+1)*D.error n<ε :=
    by simpa only [mul_comm] using (lt_div_iff₀ (by positivity : 0<T+1)).mp he
  have hb := (limit_cutoff_bound D n t).trans
    (mul_le_mul_of_nonneg_right ht (D.error_nonnegative n))
  nlinarith [D.error_nonnegative n]

theorem cutoff_uniform_on_bounded {P : SiteProfile} (D : CocycleApproximation P)
    (K : Set ℝ) (T : ℝ) (hT : 0≤T) (hK : ∀ t∈K, |t|≤T) :
    TendstoUniformlyOn D.cutoff (limitCocycle D) atTop K := by
  apply Metric.tendstoUniformlyOn_iff.mpr
  intro ε hε
  obtain ⟨N,hN⟩ := limit_uniform_error D T hT ε hε
  filter_upwards [eventually_ge_atTop N] with n hn
  intro t ht
  rw [dist_eq_norm]
  exact hN n hn t (hK t ht)

theorem cutoff_uniform_on_compact {P : SiteProfile} (D : CocycleApproximation P)
    (K : Set ℝ) (hK : IsCompact K) :
    TendstoUniformlyOn D.cutoff (limitCocycle D) atTop K := by
  obtain ⟨T,hT,hbound⟩ := hK.isBounded.exists_pos_norm_le
  exact cutoff_uniform_on_bounded D K T hT.le (fun t ht => by
    simpa only [Real.norm_eq_abs] using hbound t ht)

theorem cutoff_locally_uniform {P : SiteProfile} (D : CocycleApproximation P) :
    TendstoLocallyUniformly D.cutoff (limitCocycle D) atTop :=
  tendstoLocallyUniformly_iff_forall_isCompact.mpr (cutoff_uniform_on_compact D)

theorem limit_cocycle_continuous {P : SiteProfile} (D : CocycleApproximation P) :
    Continuous (limitCocycle D) :=
  (cutoff_locally_uniform D).continuous
    (Filter.Eventually.frequently (Filter.Eventually.of_forall D.cutoff_continuous))

theorem limit_cocycle_unitary {P : SiteProfile} (D : CocycleApproximation P) (t : ℝ) :
    limitCocycle D t∈unitary _ :=
  isClosed_unitary.mem_of_tendsto (cutoff_tendsto_limit D t)
    (Filter.Eventually.of_forall (fun N => D.cutoff_unitary N t))

theorem limit_cocycle_factor {P : SiteProfile} (D : CocycleApproximation P) (t : ℝ) :
    limitCocycle D t∈theFactorObject P :=
  (factor_norm_closed P).mem_of_tendsto (cutoff_tendsto_limit D t)
    (Filter.Eventually.of_forall (fun N => D.cutoff_factor N t))

theorem limit_cocycle_twisted {P : SiteProfile} (D : CocycleApproximation P) (s t : ℝ) :
    limitCocycle D (s+t)=
      limitCocycle D s*modularConjugation P s (limitCocycle D t) := by
  have hr := (cutoff_tendsto_limit D s).mul
    (((canonical_conjugation_isometry P s).continuous.tendsto _).comp
      (cutoff_tendsto_limit D t))
  apply tendsto_nhds_unique (cutoff_tendsto_limit D (s+t))
  simpa only [Function.comp_def,←D.cutoff_twisted] using hr

theorem finite_cocycle_zero {P : SiteProfile} (D : CocycleApproximation P) (N : ℕ) :
    D.cutoff N 0=1 := by
  have he := D.cutoff_twisted N 0 0
  rw [zero_add,canonical_conjugation_zero] at he
  have hu : star (D.cutoff N 0)*D.cutoff N 0=1 :=
    (Unitary.mem_iff.mp (D.cutoff_unitary N 0)).1
  have h := congrArg (fun A : InteractionOperator P => star (D.cutoff N 0)*A) he
  rw [hu,←mul_assoc,hu,one_mul] at h
  exact h.symm

theorem limit_cocycle_zero {P : SiteProfile} (D : CocycleApproximation P) :
    limitCocycle D 0=1 := by
  apply tendsto_nhds_unique (cutoff_tendsto_limit D 0)
  simpa only [finite_cocycle_zero] using
    (tendsto_const_nhds : Tendsto (fun _ : ℕ => (1 : InteractionOperator P)) atTop (𝓝 1))


#print axioms CocycleApproximation
#print axioms cutoff_cauchy
#print axioms cutoff_limit_exists
#print axioms limitCocycle
#print axioms cutoff_tendsto_limit
#print axioms limit_cocycle_unique
#print axioms limit_cutoff_bound
#print axioms limit_uniform_error
#print axioms cutoff_uniform_on_bounded
#print axioms cutoff_uniform_on_compact
#print axioms cutoff_locally_uniform
#print axioms limit_cocycle_continuous
#print axioms limit_cocycle_unitary
#print axioms limit_cocycle_factor
#print axioms limit_cocycle_twisted
#print axioms finite_cocycle_zero
#print axioms limit_cocycle_zero
end
end ChatgptAudit.CocycleLimit
