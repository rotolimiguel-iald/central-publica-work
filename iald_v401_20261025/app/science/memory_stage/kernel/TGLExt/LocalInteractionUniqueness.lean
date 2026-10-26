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
import TGLExt.UnitaryCocycleUniqueness
import TGLExt.LocalInteractionGenerator
import TGLExt.LocalInteractionDynamics

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.LocalUniqueness
open TGLExt ChatgptAudit.UnitaryDuhamel ChatgptAudit.LocalInteraction
  ChatgptAudit.LocalCocycle ChatgptAudit.LocalGenerator ChatgptAudit.LocalDynamics
  ChatgptAudit.CocycleUniqueness
noncomputable section

theorem local_cocycle_unique (P : SiteProfile) (c : LocalInteractionData P)
    (u : ℝ → Operator P)
    (hc : ∀ s t, u (s+t) = u s * modularConjugation P s (u t))
    (hd : HasDerivAt u (Complex.I • localPotential P c) 0)
    (h0 : u 0 = 1) : u = localCocycle P c :=
  canonical_cocycle_unique_from_derivative P u (localCocycle P c) (localPotential P c)
    (local_potential_selfadjoint P c) hc (local_cocycle_twisted P c)
    hd (local_cocycle_generator_zero P c) h0 (local_cocycle_zero P c)
    (local_cocycle_unitary P c)

theorem same_potential_same_cocycle (P : SiteProfile) (c d : LocalInteractionData P)
    (h : localPotential P c = localPotential P d) :
    localCocycle P c = localCocycle P d := by
  apply local_cocycle_unique P d (localCocycle P c) (local_cocycle_twisted P c)
  · rw [← h]
    exact local_cocycle_generator_zero P c
  · exact local_cocycle_zero P c

theorem same_potential_same_dynamics (P : SiteProfile) (c d : LocalInteractionData P)
    (h : localPotential P c = localPotential P d) (t : ℝ) (A : Operator P) :
    localDynamics P c t A = localDynamics P d t A := by
  simp only [local_dynamics_formula, same_potential_same_cocycle P c d h]

theorem same_cocycle_same_potential (P : SiteProfile) (c d : LocalInteractionData P)
    (h : localCocycle P c = localCocycle P d) :
    localPotential P c = localPotential P d := by
  have hc := local_cocycle_generator_zero P c
  rw [h] at hc
  have he := hc.unique (local_cocycle_generator_zero P d)
  have hz : Complex.I • (localPotential P c - localPotential P d) = 0 := by
    rw [smul_sub, he, sub_self]
  exact sub_eq_zero.mp ((smul_eq_zero.mp hz).resolve_left Complex.I_ne_zero)

theorem potential_eq_iff_cocycle_eq (P : SiteProfile) (c d : LocalInteractionData P) :
    localPotential P c = localPotential P d ↔ localCocycle P c = localCocycle P d :=
  ⟨same_potential_same_cocycle P c d, same_cocycle_same_potential P c d⟩

#print axioms local_cocycle_unique
#print axioms same_potential_same_cocycle
#print axioms same_potential_same_dynamics
#print axioms same_cocycle_same_potential
#print axioms potential_eq_iff_cocycle_eq
end
end ChatgptAudit.LocalUniqueness
