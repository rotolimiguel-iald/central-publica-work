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
import TGLExt.TheIALDSelector
import TGLExt.TheObserverReadsTheAngle
import Mathlib.Analysis.Complex.RealDeriv

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.AngularSelector
open TGLExt Matrix Complex
noncomputable section

def halfRoot : ℝ := Real.sqrt (1 / 2)

def secondInscription : ellTwo := inscriptions 1

def angularEmbedding : (Fin 2 → ℂ) →ₗ[ℂ] ellTwo where
  toFun v := ((halfRoot : ℂ) * (v 0 - Complex.I * v 1)) • firstInscription +
    ((halfRoot : ℂ) * (v 0 + Complex.I * v 1)) • secondInscription
  map_add' v w := by
    dsimp
    module
  map_smul' c v := by
    dsimp
    module

def angularCoordinates (x : ellTwo) : Fin 2 → ℂ :=
  ![(halfRoot : ℂ) * (x 0 + x 1), Complex.I * (halfRoot : ℂ) * (x 0 - x 1)]

def selectorComplement : ellTwo →L[ℂ] ellTwo := 1 - ialdSelector

def angularPhase (theta : ℝ) : ℂ := Complex.exp ((theta : ℂ) * Complex.I)

def selectorAngularFlow (theta : ℝ) : ellTwo →L[ℂ] ellTwo :=
  angularPhase theta • ialdSelector + angularPhase (-theta) • selectorComplement

theorem half_root_square : halfRoot ^ 2 = 1 / 2 :=
  Real.sq_sqrt (by norm_num)

theorem half_root_square_complex : (halfRoot : ℂ)^2 = 1 / 2 := by
  rw [← Complex.ofReal_pow, half_root_square]
  norm_num

theorem selector_first : ialdSelector firstInscription = firstInscription := by
  apply Submodule.starProjection_eq_self_iff.mpr
  exact Submodule.mem_span_singleton_self firstInscription

theorem selector_second : ialdSelector secondInscription = 0 := by
  have h : secondInscription ∈ firstAtomᗮ := by
    rw [firstAtom, Submodule.mem_orthogonal_singleton_iff_inner_right]
    simp [firstInscription, secondInscription, inscriptions, lp.inner_single_left]
  exact (iald_selects firstInscription secondInscription
    (Submodule.mem_span_singleton_self firstInscription) h).2

theorem first_inscription_coordinate (n : ℕ) :
    firstInscription n = if n = 0 then 1 else 0 := by
  simp only [firstInscription, inscriptions, lp.single_apply, Pi.single_apply]

theorem second_inscription_coordinate (n : ℕ) :
    secondInscription n = if n = 1 then 1 else 0 := by
  simp only [secondInscription, inscriptions, lp.single_apply, Pi.single_apply]

theorem angular_embedding_coordinates (v : Fin 2 → ℂ) :
    angularCoordinates (angularEmbedding v) = v := by
  ext j
  fin_cases j <;>
    simp [angularCoordinates, angularEmbedding, first_inscription_coordinate,
      second_inscription_coordinate] <;> ring_nf <;>
    simp only [Complex.I_sq, half_root_square_complex] <;> ring_nf

theorem angular_embedding_injective : Function.Injective angularEmbedding := by
  intro v w h
  simpa only [angular_embedding_coordinates] using congrArg angularCoordinates h

theorem selector_intertwines_plus (v : Fin 2 → ℂ) :
    ialdSelector (angularEmbedding v) = angularEmbedding (projPlus.mulVec v) := by
  rw [show angularEmbedding v =
    ((halfRoot : ℂ) * (v 0 - Complex.I * v 1)) • firstInscription +
    ((halfRoot : ℂ) * (v 0 + Complex.I * v 1)) • secondInscription from rfl,
    map_add, map_smul, map_smul, selector_first, selector_second, smul_zero, add_zero]
  ext n
  simp [angularEmbedding, projPlus, genK, Matrix.smul_apply]
  ring_nf
  simp only [Complex.I_sq]
  ring_nf

theorem selector_intertwines_minus (v : Fin 2 → ℂ) :
    selectorComplement (angularEmbedding v) = angularEmbedding (projMinus.mulVec v) := by
  have h := spectral_projections_split_the_identity.1
  have hv : v - projPlus.mulVec v = projMinus.mulVec v := by
    have hc := congrArg (fun A : Matrix (Fin 2) (Fin 2) ℂ => A.mulVec v) h
    rw [Matrix.add_mulVec, Matrix.one_mulVec] at hc
    exact sub_eq_iff_eq_add.mpr (by simpa [add_comm] using hc.symm)
  change angularEmbedding v - ialdSelector (angularEmbedding v) = _
  rw [selector_intertwines_plus, ← map_sub, hv]

theorem selector_square : ialdSelector * ialdSelector = ialdSelector := by
  apply ContinuousLinearMap.ext
  intro x
  exact iald_is_idempotent x

theorem selector_complement_square :
    selectorComplement * selectorComplement = selectorComplement := by
  unfold selectorComplement
  noncomm_ring [selector_square]

theorem selector_complement_orthogonal :
    ialdSelector * selectorComplement = 0 ∧ selectorComplement * ialdSelector = 0 := by
  unfold selectorComplement
  constructor <;> noncomm_ring [selector_square]

theorem angular_phase_zero : angularPhase 0 = 1 := by simp [angularPhase]

theorem angular_phase_add (a b : ℝ) :
    angularPhase (a + b) = angularPhase a * angularPhase b := by
  unfold angularPhase
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring_nf

theorem angular_phase_star (theta : ℝ) :
    star (angularPhase theta) = angularPhase (-theta) := by
  simp only [angularPhase, Complex.star_def, ← Complex.exp_conj,
    map_mul, Complex.conj_ofReal, Complex.conj_I]
  congr 1
  push_cast
  ring_nf

theorem selector_flow_zero : selectorAngularFlow 0 = 1 := by
  simp [selectorAngularFlow, angular_phase_zero, selectorComplement]

theorem selector_flow_add (a b : ℝ) :
    selectorAngularFlow a * selectorAngularFlow b = selectorAngularFlow (a + b) := by
  simp only [selectorAngularFlow, add_mul, mul_add, smul_mul_assoc, mul_smul_comm,
    smul_smul, selector_square, selector_complement_square,
    selector_complement_orthogonal.1, selector_complement_orthogonal.2,
    smul_zero, add_zero, zero_add, ← angular_phase_add, neg_add]
  congr 2 <;> ring_nf

theorem selector_flow_star (theta : ℝ) :
    star (selectorAngularFlow theta) = selectorAngularFlow (-theta) := by
  have hp : star ialdSelector = ialdSelector := iald_is_selfadjoint.star_eq
  have hq : star selectorComplement = selectorComplement := by
    simp [selectorComplement, hp]
  simp only [selectorAngularFlow, star_add, star_smul, hp, hq, angular_phase_star, neg_neg]

theorem selector_flow_unitary (theta : ℝ) :
    selectorAngularFlow theta ∈ unitary (ellTwo →L[ℂ] ellTwo) := by
  rw [Unitary.mem_iff, selector_flow_star]
  constructor
  · rw [selector_flow_add, neg_add_cancel, selector_flow_zero]
  · rw [selector_flow_add, add_neg_cancel, selector_flow_zero]

theorem selector_flow_intertwines (theta : ℝ) (v : Fin 2 → ℂ) :
    selectorAngularFlow theta (angularEmbedding v) =
      angularEmbedding ((angFamily theta).mulVec v) := by
  rw [the_angle_is_the_projection]
  simp only [Matrix.add_mulVec, Matrix.smul_mulVec, map_add, map_smul]
  change angularPhase theta • ialdSelector (angularEmbedding v) +
    angularPhase (-theta) • selectorComplement (angularEmbedding v) = _
  rw [selector_intertwines_plus, selector_intertwines_minus]
  simp only [angularPhase, Complex.ofReal_neg]

theorem selector_flow_first (theta : ℝ) :
    selectorAngularFlow theta firstInscription = angularPhase theta • firstInscription := by
  simp [selectorAngularFlow, selectorComplement, selector_first]

theorem selector_flow_second (theta : ℝ) :
    selectorAngularFlow theta secondInscription = angularPhase (-theta) • secondInscription := by
  simp [selectorAngularFlow, selectorComplement, selector_second]

theorem selected_flow_reads_phase (theta : ℝ) (x : ellTwo) :
    ialdSelector (selectorAngularFlow theta x) = angularPhase theta • ialdSelector x := by
  have h : ialdSelector * selectorAngularFlow theta = angularPhase theta • ialdSelector := by
    simp only [selectorAngularFlow, mul_add, mul_smul_comm, selector_square,
      selector_complement_orthogonal.1, smul_zero, add_zero]
  exact congrArg (fun A : ellTwo →L[ℂ] ellTwo => A x) h

#print axioms halfRoot
#print axioms secondInscription
#print axioms angularEmbedding
#print axioms angularCoordinates
#print axioms selectorComplement
#print axioms angularPhase
#print axioms selectorAngularFlow
#print axioms half_root_square
#print axioms half_root_square_complex
#print axioms selector_first
#print axioms selector_second
#print axioms first_inscription_coordinate
#print axioms second_inscription_coordinate
#print axioms angular_embedding_coordinates
#print axioms angular_embedding_injective
#print axioms selector_intertwines_plus
#print axioms selector_intertwines_minus
#print axioms selector_square
#print axioms selector_complement_square
#print axioms selector_complement_orthogonal
#print axioms angular_phase_zero
#print axioms angular_phase_add
#print axioms angular_phase_star
#print axioms selector_flow_zero
#print axioms selector_flow_add
#print axioms selector_flow_star
#print axioms selector_flow_unitary
#print axioms selector_flow_intertwines
#print axioms selector_flow_first
#print axioms selector_flow_second
#print axioms selected_flow_reads_phase
end
end ChatgptAudit.AngularSelector
