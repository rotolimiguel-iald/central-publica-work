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
import Mathlib.Algebra.Star.UnitaryStarAlgAut

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.LocalDynamics
open TGLExt Filter Topology Set ChatgptAudit
  ChatgptAudit.UnitaryDuhamel ChatgptAudit.LocalCocycle
  ChatgptAudit.SummableInteraction ChatgptAudit.LocalInteraction
  ChatgptAudit.InteractionOrbit
noncomputable section

def localCocycleUnitary (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ) :
    unitary (Operator P) := ⟨localCocycle P c t,local_cocycle_unitary P c t⟩

def localDynamics (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ) :
    Operator P ≃⋆ₐ[ℂ] Operator P :=
  (modularConjugation P t).trans
    (Unitary.conjStarAlgAut ℂ (Operator P) (localCocycleUnitary P c t))

theorem local_dynamics_formula (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ)
    (A : Operator P) :
    localDynamics P c t A =
      localCocycle P c t * modularConjugation P t A * star (localCocycle P c t) := rfl

theorem local_dynamics_zero (P : SiteProfile) (c : LocalInteractionData P) (A : Operator P) :
    localDynamics P c 0 A=A := by
  rw [local_dynamics_formula,local_cocycle_zero,canonical_conjugation_zero,star_one,
    one_mul,mul_one]

theorem local_dynamics_zero_equiv (P : SiteProfile) (c : LocalInteractionData P) :
    localDynamics P c 0=(StarAlgEquiv.refl : Operator P ≃⋆ₐ[ℂ] Operator P) := by
  apply StarAlgEquiv.ext
  intro A
  exact local_dynamics_zero P c A

theorem local_dynamics_group (P : SiteProfile) (c : LocalInteractionData P) (s t : ℝ)
    (A : Operator P) :
    localDynamics P c s (localDynamics P c t A)=localDynamics P c (s+t) A := by
  change localCocycle P c s *
    modularConjugation P s (localCocycle P c t * modularConjugation P t A *
      star (localCocycle P c t)) * star (localCocycle P c s) =
    localCocycle P c (s+t) * modularConjugation P (s+t) A * star (localCocycle P c (s+t))
  rw [map_mul,map_mul,map_star,canonical_conjugation_group]
  rw [local_cocycle_twisted P c s t]
  simp only [star_mul,mul_assoc]

theorem local_dynamics_inverse_left (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ)
    (A : Operator P) :
    localDynamics P c (-t) (localDynamics P c t A)=A := by
  rw [local_dynamics_group,neg_add_cancel,local_dynamics_zero]

theorem local_dynamics_inverse_right (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ)
    (A : Operator P) :
    localDynamics P c t (localDynamics P c (-t) A)=A := by
  rw [local_dynamics_group,add_neg_cancel,local_dynamics_zero]

theorem local_dynamics_symm (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ) :
    (localDynamics P c t).symm=localDynamics P c (-t) := by
  apply StarAlgEquiv.ext
  intro A
  apply (localDynamics P c t).injective
  change localDynamics P c t ((localDynamics P c t).symm A)=
    localDynamics P c t (localDynamics P c (-t) A)
  rw [StarAlgEquiv.apply_symm_apply,local_dynamics_inverse_right]

theorem local_dynamics_mul (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ)
    (A B : Operator P) :
    localDynamics P c t (A*B)=localDynamics P c t A*localDynamics P c t B :=
  map_mul _ A B

theorem local_dynamics_star (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ)
    (A : Operator P) :
    localDynamics P c t (star A)=star (localDynamics P c t A) :=
  map_star _ A

theorem local_dynamics_mem_factor (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ)
    (A : Operator P) (hA : A∈theFactorObject P) :
    localDynamics P c t A∈theFactorObject P := by
  rw [local_dynamics_formula]
  exact (theFactorObject P).mul_mem
    ((theFactorObject P).mul_mem (local_cocycle_mem_factor P c t)
      ((modularConjugation_preserves_factor P t A).mp hA))
    ((theFactorObject P).toStarSubalgebra.star_mem' (local_cocycle_mem_factor P c t))

theorem local_dynamics_factor_iff (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ)
    (A : Operator P) :
    A∈theFactorObject P ↔ localDynamics P c t A∈theFactorObject P := by
  constructor
  · exact local_dynamics_mem_factor P c t A
  · intro h
    have hb := local_dynamics_mem_factor P c (-t) (localDynamics P c t A) h
    rwa [local_dynamics_inverse_left] at hb

theorem local_dynamics_norm (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ)
    (A : Operator P) :
    ‖localDynamics P c t A‖=‖A‖ := by
  rw [local_dynamics_formula,
    CStarRing.norm_mul_mem_unitary _ (Unitary.star_mem (local_cocycle_unitary P c t)),
    CStarRing.norm_mem_unitary_mul _ (local_cocycle_unitary P c t),
    canonical_conjugation_norm]

theorem local_dynamics_isometry (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ) :
    Isometry (localDynamics P c t) := by
  apply isometry_iff_dist_eq.mpr
  intro A B
  rw [dist_eq_norm,dist_eq_norm,←map_sub,local_dynamics_norm]

theorem local_dynamics_operator_continuous (P : SiteProfile) (c : LocalInteractionData P)
    (t : ℝ) : Continuous (localDynamics P c t) :=
  (local_dynamics_isometry P c t).continuous

theorem local_dynamics_orbit_continuous (P : SiteProfile) (c : LocalInteractionData P)
    (A : Operator P) (hA : Continuous (fun t : ℝ => modularConjugation P t A)) :
    Continuous (fun t : ℝ => localDynamics P c t A) := by
  simp only [local_dynamics_formula]
  exact ((local_cocycle_continuous P c).mul hA).mul
    (local_cocycle_continuous P c).star

theorem local_dynamics_potential_orbit_continuous (P : SiteProfile) (c : LocalInteractionData P) :
    Continuous (fun t : ℝ => localDynamics P c t (localPotential P c)) :=
  local_dynamics_orbit_continuous P c _ (local_orbit_continuous P c)



#print axioms localCocycleUnitary
#print axioms localDynamics
#print axioms local_dynamics_formula
#print axioms local_dynamics_zero
#print axioms local_dynamics_zero_equiv
#print axioms local_dynamics_group
#print axioms local_dynamics_inverse_left
#print axioms local_dynamics_inverse_right
#print axioms local_dynamics_symm
#print axioms local_dynamics_mul
#print axioms local_dynamics_star
#print axioms local_dynamics_mem_factor
#print axioms local_dynamics_factor_iff
#print axioms local_dynamics_norm
#print axioms local_dynamics_isometry
#print axioms local_dynamics_operator_continuous
#print axioms local_dynamics_orbit_continuous
#print axioms local_dynamics_potential_orbit_continuous
end
end ChatgptAudit.LocalDynamics
