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
import TGLExt.LocalInteractionData
import TGLExt.SpectatorCancellation
import TGLExt.FiniteModularHamiltonian
import TGLExt.FiniteLevelExponentials
import TGLExt.CocycleNormLimit

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.LocalCocycle
open TGLExt Matrix Filter Topology Set ChatgptAudit ChatgptAudit.Observable035
  ChatgptAudit.UnitaryDuhamel ChatgptAudit.BoundedPerturbation
  ChatgptAudit.SpectatorCancellation ChatgptAudit.FiniteModular ChatgptAudit.FiniteLevel
  ChatgptAudit.SummableInteraction ChatgptAudit.LocalInteraction
  ChatgptAudit.InteractionOrbit ChatgptAudit.CocycleLimit
noncomputable section

def localCutoffCocycle (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) (t : ℝ) :
    Operator P := boundedCocycle (finiteModularHamiltonian P N) (localPrefix P c N) t

theorem local_cutoff_zero (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) :
    localCutoffCocycle P c N 0 = 1 := bounded_cocycle_zero _ _

theorem local_cutoff_unitary (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) (t : ℝ) :
    localCutoffCocycle P c N t ∈ unitary _ :=
  bounded_cocycle_unitary _ _ (finite_hamiltonian_selfadjoint P N)
    (local_prefix_selfadjoint P c N) t

theorem local_cutoff_continuous (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) :
    Continuous (localCutoffCocycle P c N) := bounded_cocycle_continuous _ _

theorem local_cutoff_mem_level (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) (t : ℝ) :
    localCutoffCocycle P c N t ∈ levelOperatorAlgebra P N := by
  simpa only [localCutoffCocycle, boundedCocycle, evolution, Complex.ofReal_neg] using
    finite_level_cocycle_mem P N _ _ (finite_hamiltonian_mem_level P N)
      (local_prefix_mem_level P c N) t

theorem local_cutoff_mem_factor (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) (t : ℝ) :
    localCutoffCocycle P c N t ∈ theFactorObject P := by
  obtain ⟨a,ha⟩ := local_cutoff_mem_level P c N t
  rw [← ha]
  exact towerPi_mem_factor a

theorem finite_inner_action_is_canonical (P : SiteProfile) (N : ℕ) (t : ℝ)
    (A : Operator P) (hA : A ∈ levelOperatorAlgebra P N) :
    innerAction (finiteModularHamiltonian P N) t A = modularConjugation P t A :=
  finite_modular_action_eq_canonical P N t A hA

/-- The finite certificate uses the canonical modular action, not a substituted action. -/
theorem local_cutoff_twisted (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) (s t : ℝ) :
    localCutoffCocycle P c N (s+t) =
      localCutoffCocycle P c N s * modularConjugation P s (localCutoffCocycle P c N t) := by
  calc
    _ = localCutoffCocycle P c N s *
        innerAction (finiteModularHamiltonian P N) s (localCutoffCocycle P c N t) :=
      bounded_cocycle_twisted _ _ s t
    _ = _ := by rw [finite_inner_action_is_canonical P N s _ (local_cutoff_mem_level P c N t)]

theorem local_cutoff_derivative (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) (t : ℝ) :
    HasDerivAt (localCutoffCocycle P c N)
      (localCutoffCocycle P c N t *
        modularConjugation P t (Complex.I • localPrefix P c N)) t := by
  have h := bounded_cocycle_derivative_right (finiteModularHamiltonian P N)
    (localPrefix P c N) t
  rw [finite_inner_action_is_canonical P N t _
    ((levelOperatorAlgebra P N).smul_mem (local_prefix_mem_level P c N) Complex.I)] at h
  exact h

theorem local_cutoff_generator (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) :
    HasDerivAt (localCutoffCocycle P c N) (Complex.I • localPrefix P c N) 0 :=
  bounded_cocycle_generator _ _

theorem local_cutoff_ordered_bound (P : SiteProfile) (c : LocalInteractionData P)
    (N M : ℕ) (hNM : N ≤ M) (t : ℝ) :
    ‖localCutoffCocycle P c N t - localCutoffCocycle P c M t‖ ≤
      (2 * normTail P c N) * |t| := by
  have h := varying_background_duhamel
    (finiteModularHamiltonian P N) (finiteModularHamiltonian P M)
    (localPrefix P c N) (localPrefix P c M)
    (finite_hamiltonian_selfadjoint P M) (local_prefix_selfadjoint P c N)
    (local_prefix_selfadjoint P c M) (finite_spectator_commutes_base P hNM)
    (finite_spectator_commutes P hNM _ (local_prefix_mem_level P c N)) t
  exact h.trans (mul_le_mul_of_nonneg_right (local_prefix_difference P c N M hNM)
    (abs_nonneg t))

def localCutoffError (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) : ℝ := 2 * normTail P c N

theorem local_cutoff_error_nonnegative (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) :
    0 ≤ localCutoffError P c N := mul_nonneg (by norm_num) (norm_tail_nonnegative P c N)

theorem local_cutoff_error_tendsto (P : SiteProfile) (c : LocalInteractionData P) :
    Tendsto (localCutoffError P c) atTop (𝓝 0) := by
  change Tendsto (fun N : ℕ => (2 : ℝ) * normTail P c N) atTop (𝓝 0)
  convert! (norm_tail_tendsto P c).const_mul (2 : ℝ) using 1
  norm_num

theorem local_cutoff_difference_bound (P : SiteProfile) (c : LocalInteractionData P)
    (N M : ℕ) (t : ℝ) :
    ‖localCutoffCocycle P c N t - localCutoffCocycle P c M t‖ ≤
      |t| * localCutoffError P c (min N M) := by
  rcases le_total N M with h | h
  · simpa only [min_eq_left h, localCutoffError, mul_comm] using
      local_cutoff_ordered_bound P c N M h t
  · rw [norm_sub_rev, min_eq_right h]
    simpa only [localCutoffError, mul_comm] using local_cutoff_ordered_bound P c M N h t

/-- Every finite hypothesis is discharged by the general local self-adjoint norm-summable construction. -/
def localApproximation (P : SiteProfile) (c : LocalInteractionData P) : CocycleApproximation P where
  cutoff := localCutoffCocycle P c
  error := localCutoffError P c
  error_nonnegative := local_cutoff_error_nonnegative P c
  error_tendsto := local_cutoff_error_tendsto P c
  difference_bound := local_cutoff_difference_bound P c
  cutoff_continuous := local_cutoff_continuous P c
  cutoff_unitary := local_cutoff_unitary P c
  cutoff_factor := local_cutoff_mem_factor P c
  cutoff_twisted := local_cutoff_twisted P c

def localCocycle (P : SiteProfile) (c : LocalInteractionData P) : ℝ → Operator P :=
  limitCocycle (localApproximation P c)

theorem local_cocycle_zero (P : SiteProfile) (c : LocalInteractionData P) :
    localCocycle P c 0 = 1 := limit_cocycle_zero (localApproximation P c)

theorem local_cocycle_unitary (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ) :
    localCocycle P c t ∈ unitary _ := limit_cocycle_unitary (localApproximation P c) t

theorem local_cocycle_mem_factor (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ) :
    localCocycle P c t ∈ theFactorObject P := limit_cocycle_factor (localApproximation P c) t

theorem local_cocycle_continuous (P : SiteProfile) (c : LocalInteractionData P) :
    Continuous (localCocycle P c) := limit_cocycle_continuous (localApproximation P c)

theorem local_cocycle_twisted (P : SiteProfile) (c : LocalInteractionData P) (s t : ℝ) :
    localCocycle P c (s+t) = localCocycle P c s * modularConjugation P s (localCocycle P c t) :=
  limit_cocycle_twisted (localApproximation P c) s t

theorem local_cutoff_tendsto (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ) :
    Tendsto (fun N => localCutoffCocycle P c N t) atTop (𝓝 (localCocycle P c t)) :=
  cutoff_tendsto_limit (localApproximation P c) t

theorem local_cutoff_uniform_on_compact (P : SiteProfile) (c : LocalInteractionData P)
    (K : Set ℝ) (hK : IsCompact K) :
    TendstoUniformlyOn (localCutoffCocycle P c) (localCocycle P c) atTop K :=
  cutoff_uniform_on_compact (localApproximation P c) K hK

theorem local_cocycle_cutoff_bound (P : SiteProfile) (c : LocalInteractionData P) (N : ℕ) (t : ℝ) :
    ‖localCocycle P c t - localCutoffCocycle P c N t‖ ≤ |t| * localCutoffError P c N :=
  limit_cutoff_bound (localApproximation P c) N t


#print axioms localCutoffCocycle
#print axioms local_cutoff_zero
#print axioms local_cutoff_unitary
#print axioms local_cutoff_continuous
#print axioms local_cutoff_mem_level
#print axioms local_cutoff_mem_factor
#print axioms finite_inner_action_is_canonical
#print axioms local_cutoff_twisted
#print axioms local_cutoff_derivative
#print axioms local_cutoff_generator
#print axioms local_cutoff_ordered_bound
#print axioms localCutoffError
#print axioms local_cutoff_error_nonnegative
#print axioms local_cutoff_error_tendsto
#print axioms local_cutoff_difference_bound
#print axioms localApproximation
#print axioms localCocycle
#print axioms local_cocycle_zero
#print axioms local_cocycle_unitary
#print axioms local_cocycle_mem_factor
#print axioms local_cocycle_continuous
#print axioms local_cocycle_twisted
#print axioms local_cutoff_tendsto
#print axioms local_cutoff_uniform_on_compact
#print axioms local_cocycle_cutoff_bound
end
end ChatgptAudit.LocalCocycle
