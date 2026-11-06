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
import TGLExt.LocalInteractionCocycle
import TGLExt.DerivativeFromLinearCutoffError
import TGLExt.CanonicalCocycleDerivative

set_option autoImplicit false
set_option maxHeartbeats 700000
namespace ChatgptAudit.LocalGenerator
open TGLExt Filter Topology Set ChatgptAudit ChatgptAudit.UnitaryDuhamel
  ChatgptAudit.SummableInteraction ChatgptAudit.LocalInteraction
  ChatgptAudit.LocalCocycle ChatgptAudit.CutoffDerivative ChatgptAudit.CocycleDerivative
noncomputable section

theorem local_cutoff_generators_tendsto (P : SiteProfile) (c : LocalInteractionData P) :
    Tendsto (fun N => Complex.I • localPrefix P c N) atTop
      (𝓝 (Complex.I • localPotential P c)) :=
  tendsto_const_nhds.smul (local_prefix_tendsto P c)

/-- The derivative of the infinite cocycle is derived from its linear cutoff error. -/
theorem local_cocycle_generator_zero (P : SiteProfile) (c : LocalInteractionData P) :
    HasDerivAt (localCocycle P c) (Complex.I • localPotential P c) 0 :=
  hasDerivAt_of_linear_cutoff_error_auto_base
    (localCocycle P c) (localCutoffCocycle P c)
    (fun N => Complex.I • localPrefix P c N) (Complex.I • localPotential P c)
    (localCutoffError P c) (local_cutoff_generator P c) (local_cutoff_generators_tendsto P c)
    (local_cutoff_error_nonnegative P c) (local_cutoff_error_tendsto P c)
    (local_cocycle_cutoff_bound P c)

theorem local_cocycle_generator_equation (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ) :
    HasDerivAt (localCocycle P c)
      (localCocycle P c t * (Complex.I • modularConjugation P t (localPotential P c))) t :=
  canonical_cocycle_generator_equation P (localCocycle P c) (localPotential P c)
    (local_cocycle_twisted P c) (local_cocycle_generator_zero P c) t

theorem local_cocycle_differentiable (P : SiteProfile) (c : LocalInteractionData P) :
    Differentiable ℝ (localCocycle P c) :=
  fun t => (local_cocycle_generator_equation P c t).differentiableAt

theorem constant_local_cocycle_forces_zero_potential (P : SiteProfile) (c : LocalInteractionData P)
    (h : ∀ t, localCocycle P c t = 1) : localPotential P c = 0 := by
  have he : localCocycle P c = (fun _ : ℝ => (1 : Operator P)) := funext h
  have hd := local_cocycle_generator_zero P c
  rw [he] at hd
  have hz := hd.unique (hasDerivAt_const (0 : ℝ) (1 : Operator P))
  have hn := congrArg norm hz
  simp only [norm_smul, Complex.norm_I, one_mul, norm_zero] at hn
  exact norm_eq_zero.mp hn


theorem nonzero_local_potential_has_nontrivial_cocycle (P : SiteProfile) (c : LocalInteractionData P)
    (h : localPotential P c ≠ 0) : ¬ ∀ t : ℝ, localCocycle P c t = 1 := by
  intro ht
  exact h (constant_local_cocycle_forces_zero_potential P c ht)

#print axioms local_cutoff_generators_tendsto
#print axioms local_cocycle_generator_zero
#print axioms local_cocycle_generator_equation
#print axioms local_cocycle_differentiable
#print axioms constant_local_cocycle_forces_zero_potential
#print axioms nonzero_local_potential_has_nontrivial_cocycle
end
end ChatgptAudit.LocalGenerator
