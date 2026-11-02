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
import TGLExt.AdmissiblePauliInteraction

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.InteractionOrbit
open TGLExt Matrix Filter Topology
  ChatgptAudit ChatgptAudit.Observable035 ChatgptAudit.SummableInteraction
  ChatgptAudit.AdmissibleInteraction
noncomputable section

def interactionOrbit (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    InteractionOperator P := modularConjugation P t (certifiedInteraction P c)

def prefixOrbit (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (t : ℝ) :
    InteractionOperator P := modularConjugation P t (certifiedPrefix P c N)

def interactionCoefficient (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    InteractionOperator P := Complex.I • interactionOrbit P c t

theorem canonical_conjugation_group (P : SiteProfile) (s t : ℝ) (A : InteractionOperator P) :
    modularConjugation P s (modularConjugation P t A)=modularConjugation P (s+t) A := by
  ext x
  change modularFlow P s (modularFlow P t
    (A (modularFlow P (-t) (modularFlow P (-s) x)))) =
      modularFlow P (s+t) (A (modularFlow P (-(s+t)) x))
  rw [modularFlow_group,modularFlow_group]
  rw [show -t+-s=-(s+t) by ring]

theorem canonical_conjugation_zero (P : SiteProfile) (A : InteractionOperator P) :
    modularConjugation P 0 A=A := by
  ext x
  change modularFlow P 0 (A (modularFlow P (-0) x))=A x
  rw [neg_zero,modularFlow_zero_time,modularFlow_zero_time]

theorem canonical_conjugation_norm_le (P : SiteProfile) (t : ℝ) (A : InteractionOperator P) :
    ‖modularConjugation P t A‖≤‖A‖ := by
  apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg A)
  intro x
  change ‖modularFlow P t (A (modularFlow P (-t) x))‖≤‖A‖*‖x‖
  rw [modularFlow_norm]
  simpa only [modularFlow_norm] using A.le_opNorm (modularFlow P (-t) x)

theorem canonical_conjugation_norm (P : SiteProfile) (t : ℝ) (A : InteractionOperator P) :
    ‖modularConjugation P t A‖=‖A‖ := by
  apply le_antisymm (canonical_conjugation_norm_le P t A)
  have h:=canonical_conjugation_norm_le P (-t) (modularConjugation P t A)
  rw [canonical_conjugation_group,neg_add_cancel,canonical_conjugation_zero] at h
  exact h

theorem canonical_conjugation_isometry (P : SiteProfile) (t : ℝ) :
    Isometry (modularConjugation P t) := by
  apply isometry_iff_dist_eq.mpr
  intro A B
  rw [dist_eq_norm,dist_eq_norm,←map_sub]
  exact canonical_conjugation_norm P t (A-B)

theorem local_modular_orbit_norm_continuous (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Continuous (fun t : ℝ => modularConjugation P t (towerPi P a)) := by
  have h := (towerPiLinear P N).continuous_of_finiteDimensional.comp
    (flowLevel_continuous (P:=P) N a)
  change Continuous (fun t : ℝ => towerPi P (flowLevel P t N a)) at h
  simpa only [modularConjugation_local] using h

theorem site_modular_orbit_norm_continuous (P : SiteProfile) (j : ℕ)
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    Continuous (fun t : ℝ => modularConjugation P t (siteOperator P j a)) :=
  local_modular_orbit_norm_continuous P j (lastSiteMatrix j a)

theorem bond_modular_orbit_norm_continuous (P : SiteProfile) (j : ℕ) :
    Continuous (fun t : ℝ => modularConjugation P t (pauliBond P j)) := by
  simp only [pauliBond,map_mul,sitePauliX]
  exact (site_modular_orbit_norm_continuous P j pauliXMatrix).mul
    (site_modular_orbit_norm_continuous P (j+1) pauliXMatrix)

theorem prefix_orbit_continuous (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) :
    Continuous (prefixOrbit P c N) := by
  unfold prefixOrbit certifiedPrefix interactionPrefix interactionTerm
  simp only [map_sum,map_smul]
  exact continuous_finsetSum _ (fun j _ =>
    continuous_const.smul (bond_modular_orbit_norm_continuous P j))

theorem interaction_orbit_zero (P : SiteProfile) (c : SummableCouplingData) :
    interactionOrbit P c 0=certifiedInteraction P c :=
  canonical_conjugation_zero P _

theorem interaction_orbit_covariant (P : SiteProfile) (c : SummableCouplingData) (s t : ℝ) :
    modularConjugation P s (interactionOrbit P c t)=interactionOrbit P c (s+t) :=
  canonical_conjugation_group P s t _

theorem interaction_orbit_selfadjoint (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    IsSelfAdjoint (interactionOrbit P c t) := by
  change star (modularConjugation P t (certifiedInteraction P c))=
    modularConjugation P t (certifiedInteraction P c)
  rw [←map_star,(certified_interaction_selfadjoint P c).star_eq]

theorem interaction_orbit_mem_factor (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    interactionOrbit P c t ∈ theFactorObject P :=
  (modularConjugation_preserves_factor P t _).mp (certified_interaction_mem_factor P c)

theorem interaction_orbit_norm (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    ‖interactionOrbit P c t‖=‖certifiedInteraction P c‖ :=
  canonical_conjugation_norm P t _

theorem interaction_orbit_bound (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    ‖interactionOrbit P c t‖≤∑' j, |c.value j| := by
  rw [interaction_orbit_norm]
  exact certified_interaction_bound P c

theorem orbit_cutoff_error_exact (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (t : ℝ) :
    ‖interactionOrbit P c t-prefixOrbit P c N t‖=
      ‖certifiedInteraction P c-certifiedPrefix P c N‖ := by
  unfold interactionOrbit prefixOrbit
  rw [←map_sub,canonical_conjugation_norm]

theorem interaction_orbit_tail_bound (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (t : ℝ) :
    ‖interactionOrbit P c t-prefixOrbit P c N t‖≤couplingTail c.value N := by
  rw [orbit_cutoff_error_exact]
  exact certified_cutoff_error P c N

theorem interaction_orbit_continuous (P : SiteProfile) (c : SummableCouplingData) :
    Continuous (interactionOrbit P c) := by
  apply continuous_iff_continuousAt.mpr
  intro s
  rw [Metric.continuousAt_iff]
  intro ε hε
  obtain ⟨N,hN⟩ := Metric.tendsto_atTop.mp (certified_prefix_converges P c)
    (ε/3) (by positivity)
  have hnear : dist (certifiedPrefix P c N) (certifiedInteraction P c)<ε/3 :=
    hN N le_rfl
  obtain ⟨δ,hδ,hloc⟩ := Metric.continuousAt_iff.mp
    (prefix_orbit_continuous P c N).continuousAt (ε/3) (by positivity)
  refine ⟨δ,hδ,fun t ht => ?_⟩
  have h1 : dist (interactionOrbit P c t) (prefixOrbit P c N t) =
      dist (certifiedPrefix P c N) (certifiedInteraction P c) := by
    exact ((canonical_conjugation_isometry P t).dist_eq _ _).trans (dist_comm _ _)
  have h2 : dist (prefixOrbit P c N s) (interactionOrbit P c s) =
      dist (certifiedPrefix P c N) (certifiedInteraction P c) :=
    (canonical_conjugation_isometry P s).dist_eq _ _
  have h3 := dist_triangle (interactionOrbit P c t) (prefixOrbit P c N t)
    (interactionOrbit P c s)
  have h4 := dist_triangle (prefixOrbit P c N t) (prefixOrbit P c N s)
    (interactionOrbit P c s)
  have h5 := hloc ht
  rw [h1] at h3
  rw [h2] at h4
  linarith

theorem orbit_uniform_cutoff (P : SiteProfile) (c : SummableCouplingData)
    (ε : ℝ) (hε : 0<ε) :
    ∃ N : ℕ, ∀ n≥N, ∀ t : ℝ,
      ‖interactionOrbit P c t-prefixOrbit P c n t‖<ε := by
  obtain ⟨N,hN⟩ := Metric.tendsto_atTop.mp (certified_prefix_converges P c) ε hε
  refine ⟨N,fun n hn t => ?_⟩
  rw [orbit_cutoff_error_exact,←dist_eq_norm,dist_comm]
  exact hN n hn

theorem interaction_coefficient_continuous (P : SiteProfile) (c : SummableCouplingData) :
    Continuous (interactionCoefficient P c) :=
  continuous_const.smul (interaction_orbit_continuous P c)

theorem interaction_coefficient_skewadjoint (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    star (interactionCoefficient P c t)=-interactionCoefficient P c t := by
  simp only [interactionCoefficient,star_smul,Complex.star_def,Complex.conj_I,
    (interaction_orbit_selfadjoint P c t).star_eq,neg_smul]

theorem interaction_coefficient_mem_factor (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    interactionCoefficient P c t ∈ theFactorObject P :=
  (theFactorObject P).toStarSubalgebra.smul_mem (interaction_orbit_mem_factor P c t) _

theorem interaction_coefficient_norm (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    ‖interactionCoefficient P c t‖=‖certifiedInteraction P c‖ := by
  rw [interactionCoefficient,norm_smul,Complex.norm_I,one_mul,interaction_orbit_norm]

theorem interaction_coefficient_covariant (P : SiteProfile) (c : SummableCouplingData) (s t : ℝ) :
    modularConjugation P s (interactionCoefficient P c t)=interactionCoefficient P c (s+t) := by
  unfold interactionCoefficient
  rw [map_smul,interaction_orbit_covariant]


#print axioms interactionOrbit
#print axioms prefixOrbit
#print axioms interactionCoefficient
#print axioms canonical_conjugation_group
#print axioms canonical_conjugation_zero
#print axioms canonical_conjugation_norm_le
#print axioms canonical_conjugation_norm
#print axioms canonical_conjugation_isometry
#print axioms local_modular_orbit_norm_continuous
#print axioms site_modular_orbit_norm_continuous
#print axioms bond_modular_orbit_norm_continuous
#print axioms prefix_orbit_continuous
#print axioms interaction_orbit_zero
#print axioms interaction_orbit_covariant
#print axioms interaction_orbit_selfadjoint
#print axioms interaction_orbit_mem_factor
#print axioms interaction_orbit_norm
#print axioms interaction_orbit_bound
#print axioms orbit_cutoff_error_exact
#print axioms interaction_orbit_tail_bound
#print axioms interaction_orbit_continuous
#print axioms orbit_uniform_cutoff
#print axioms interaction_coefficient_continuous
#print axioms interaction_coefficient_skewadjoint
#print axioms interaction_coefficient_mem_factor
#print axioms interaction_coefficient_norm
#print axioms interaction_coefficient_covariant
end
end ChatgptAudit.InteractionOrbit
