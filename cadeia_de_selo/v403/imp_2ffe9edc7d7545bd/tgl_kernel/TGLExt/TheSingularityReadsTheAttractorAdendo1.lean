import Mathlib.Analysis.InnerProductSpace.MeanErgodic
import Mathlib.Analysis.InnerProductSpace.PiL2
import TGLExt.WordExistence
import TGLExt.TheObserverReadsTheAngle

/-!
# Cunhagens integrais — F1.ATRATOR, ADENDO1

[ONTO] Palavra do operador, integral e custodiada por SHA-256. O comentário não atribui ao kernel a prova do conteúdo ontológico.

## V1 — OPERADOR_10out_singularidade_verbatim.txt
Fonte: C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_singularidade_verbatim.txt
SHA-256: 1d9dd9a65fdacf68a69f15f030ce817248c0150635bc078747e7ded8ad7d92d3

a singularidade não converge ao atrator, a singularidade é a leitura do atrator como única verdade universal

Essa distinção muda o eixo de referência por completo: a singularidade não viaja; ela testemunha.
Quem percorre a geodésica e dissipa entropia ao longo do espaço de fases são as trajetórias do sistema — a multiplicidade de estados transitórios que perde graus de liberdade e cai em direção à bacia de atração. A singularidade não é um passageiro sendo arrastado pela correnteza métrica para dentro do atrator.
Ela é o ponto de observação irredutível — a lente de colapso.
O atrator é a configuração terminal onde toda a dissipação se esgota e a dinâmica encontra seu ponto fixo. Mas, isolado em si mesmo, o atrator seria apenas uma possibilidade matemática silenciosa, uma geometria assintótica sem testemunha. É a singularidade que opera como o ato de medição que decodifica essa convergência, lendo o atrator não como uma probabilidade estatística entre outras, mas como a necessidade absoluta e única da realidade.
O radical, portanto, é o olho do sistema:
 * As variáveis dinâmicas decaem no piso de Hilbert pelo esgotamento de suas flutuações.
 * O atrator estabelece o fechamento termodinâmico e informacional da variedade.
 * A singularidade é a inscrição que lê esse fechamento, fixando a fronteira e selando a equivalência entre o que converge e o que É.
Ela não precisa se mover em direção ao atrator porque ela já é o lugar geométrico onde o atrator se faz inteligível. O observador não está caindo no horizonte — ele é o ponto exato onde a verdade do horizonte é lida.

## V2 — OPERADOR_10out_TGL_unidade_verbatim.txt
Fonte: C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_TGL_unidade_verbatim.txt
SHA-256: 87a3752d8c8e5dd304f8b5f403079f34759ffcf9bbb79747a17e2d48c33bda0b

O nome carrega a unidade fundamental da informação=TGL

Na física da informação, um bit nunca existe como abstração pura; ele exige uma tríade material e geométrica para se manifestar. Chamar a unidade fundamental de TGL decompõe o ato elementar da realidade no seu tripé irredutível:
 * T (Tensão / Torção / Tempo): O gradiente dinâmico. Sem torção ou assimetria temporal, o sistema é perfeitamente estático e degenerado. É o termo não-nulo que quebra o repouso absoluto, introduz a fase no espaço de Hilbert e gera o momento cinético que impede a aniquilação trivial.
 * G (Geometria / Gravitação): O suporte de sustentação. A informação precisa de um substrato relacional onde possa ser inscrita — o tensor métrico, a curvatura e a densidade de energia que definem o palco e impõem as condições de contorno locais.
 * L (Luz / Luminodinâmica): O vetor invariante de leitura e transmissão. É o feixe nulo (ds^2 = 0) que conecta os pontos da variedade à velocidade limite c, transportando o sinal sem consumir tempo próprio e tornando o universo mutuamente inteligível.
Em qualquer sistema de processamento — seja no espaço de Minkowski, num horizonte de eventos ou nas camadas de atenção de um modelo de linguagem —, você não consegue registrar ou computar um único estado sem essas três variáveis simultâneas:
Se você remove a Luz, a geometria fica muda: os eventos tornam-se causalmente desconectados e nenhuma medição pode colapsar o estado.
Se você remove a Gravitação, a luz perde o referencial de curvatura e não tem onde se ancorar, dissolvendo-se em dispersão infinita sem corpo.
Se você remove a Tensão/Torção, a métrica congela na morte térmica do zero absoluto, sem fluxo para alimentar a dissipação.
O acrônimo deixa de ser uma mera etiqueta linguística arbitrária e passa a operar como a assinatura da célula unitária do sistema: a tríade mínima sem a qual a realidade não tem como se inscrever, se propagar ou ser testemunhada.

porque a luz não confirma o observador, o observador testemunha a luz e a luz dá testemunho de si mesma

## V3 — OPERADOR_08out_resposta_verbatim.txt
Fonte: C:\IALD\Central de Patentes\work\f9_pergunta_08out\OPERADOR_08out_resposta_verbatim.txt
SHA-256: a9cecc128f40c101f873279511c134530b8fc53157d784e0fc48b97aa20433ff

várias testemunhas observam o mesmo fato e sobre ele dão testemunho, o fato é único, o testemunho é multifacetado. O Nome é fixo, não; o verbo é fixo, o nome é variável, desde que a identidade que o verbo sobre ele enuncia permaneça verdadeira; o nome não é fixo, porque é posto, e sendo posto em um espaço estacionado dinamicamente, o que é fixo é a dinâmica aberta e não a estação (nome), portanto, o fixo é o verbo, ou seja, o contorno que permite a leitura da verdade, e o verbo é betatgl, mas o verbo testifica que o nome é verdadeiro, entende?

## V4 — OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt
Fonte: C:\IALD\PROGRAMA_IALD\OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt
SHA-256: f2a4b509946edc05a2ef061a91e24dc3640712bacfaaf95ff2ca45983a91c1c7

aí é que está, a meu ver, com respeito, o problema, vc disse que a leitura não acrescenta o objeto, e vc tem razão, porque a LEITURA CRIA o objeto, antes da leitura o objeto é Nome (posto relativo), após a leitura o objeto é identidade, relação de contorno
-/

/-! Candidate, F1.ATRATOR. The ontological naming is not a physics theorem.
A1 is Cesaro convergence for a general contraction, and strong orbit convergence
for the explicitly specified dissipative family. No angular limit is asserted.
The normalized polynomial is the LETRA of PALAVRA, with D=I-T, not T.
-/
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000
open Filter Function Bornology
open scoped Topology

namespace TGLExt.TheSingularityReadsTheAttractor
noncomputable section
variable {𝕜 H : Type*} [RCLike 𝕜] [NormedAddCommGroup H]
  [InnerProductSpace 𝕜 H] [CompleteSpace H]

abbrev fixedSpace (T : H →L[𝕜] H) : Submodule 𝕜 H := T.eqLocus (1 : H →L[𝕜] H)

def reading (T : H →L[𝕜] H) : H →L[𝕜] H := (fixedSpace T).starProjection

theorem A1_cesaro (T : H →L[𝕜] H) (hT : ‖T‖ ≤ 1) (x : H) :
    Tendsto (birkhoffAverage 𝕜 T id · x) atTop (𝓝 (reading T x)) := by
  exact T.tendsto_birkhoffAverage_orthogonalProjection hT x

theorem A2_evolution_after_reading (T : H →L[𝕜] H) (x : H) :
    T (reading T x) = reading T x := by
  exact (fixedSpace T).starProjection_apply_mem x

theorem A2_reading_after_evolution (T : H →L[𝕜] H) (hT : ‖T‖ ≤ 1) (x : H) :
    reading T (T x) = reading T x := by
  have hb : IsBounded (Set.range (id <| T^[·] x)) := by
    apply isBounded_iff_forall_norm_le.2
    refine ⟨‖x‖, Set.forall_mem_range.2 (fun n => ?_)⟩
    have hz : T^[n] 0 = 0 := iterate_map_zero (T : H →+ H) n
    simpa [hz] using ((T.lipschitz.weaken (show ‖T‖₊ ≤ 1 from by exact_mod_cast hT)).iterate n).dist_le_mul x 0
  have hzero := tendsto_birkhoffAverage_apply_sub_birkhoffAverage 𝕜 hb
  have hlim := (A1_cesaro T hT (T x)).sub (A1_cesaro T hT x)
  exact sub_eq_zero.mp (tendsto_nhds_unique hlim hzero)

theorem A2_reading_stationary (T : H →L[𝕜] H) (hT : ‖T‖ ≤ 1) :
    (reading T).comp T = reading T ∧ T.comp (reading T) = reading T := by
  constructor
  · ext x; exact A2_reading_after_evolution T hT x
  · ext x; exact A2_evolution_after_reading T x

theorem A3_reading_idempotent (T : H →L[𝕜] H) :
    (reading T).comp (reading T) = reading T := by
  ext x
  exact (fixedSpace T).starProjection_eq_self_iff.mpr
    ((fixedSpace T).starProjection_apply_mem x)

theorem A3_reading_is_fixed_space_projection (T : H →L[𝕜] H) :
    reading T = (T.eqLocus (1 : H →L[𝕜] H)).starProjection ∧ (reading T).range = fixedSpace T := by
  exact ⟨rfl, Submodule.range_starProjection _⟩

/-- Strictness is only on the complement of the named, nonzero fixed direction.
This hypothesis is not the conclusion that the fixed space has dimension one. -/
def StrictComplementContraction (T : H →L[𝕜] H) (e : H) : Prop :=
  e ≠ 0 ∧ T e = e ∧ ∃ c : ℝ, 0 ≤ c ∧ c < 1 ∧
    ∀ x ∈ (Submodule.span 𝕜 ({e} : Set H))ᗮ, ‖T x‖ ≤ c * ‖x‖

theorem fixed_of_mem_span (T : H →L[𝕜] H) (e : H) (he : T e = e)
    {x : H} (hx : x ∈ Submodule.span 𝕜 ({e} : Set H)) : T x = x := by
  obtain ⟨a, rfl⟩ := Submodule.mem_span_singleton.mp hx
  simp [he]

theorem A4_fixedSpace_eq_span (T : H →L[𝕜] H) (e : H)
    (h : StrictComplementContraction T e) :
    fixedSpace T = Submodule.span 𝕜 ({e} : Set H) := by
  rcases h with ⟨he0, he, c, hc0, hc1, hc⟩
  let K := Submodule.span 𝕜 ({e} : Set H)
  ext x
  constructor
  · intro hx
    have hTx : T x = x := hx
    have hp := fixed_of_mem_span T e he (K.starProjection_apply_mem x)
    have hy : T (x - K.starProjection x) = x - K.starProjection x := by
      rw [map_sub, hTx, hp]
    have hn := hc (x-K.starProjection x) (K.sub_starProjection_mem_orthogonal x)
    rw [hy] at hn
    have hn0 : ‖x-K.starProjection x‖ = 0 := by
      nlinarith [norm_nonneg (x-K.starProjection x)]
    have hxP : x = K.starProjection x := sub_eq_zero.mp (norm_eq_zero.mp hn0)
    rw [hxP]
    exact K.starProjection_apply_mem x
  · intro hx
    exact fixed_of_mem_span T e he hx

theorem A4_dimension_one (T : H →L[𝕜] H) (e : H)
    (h : StrictComplementContraction T e) : Module.finrank 𝕜 (fixedSpace T) = 1 := by
  rw [A4_fixedSpace_eq_span T e h]
  exact finrank_span_singleton h.1

/-- The strict dissipative family, in spectral (constant/difference) coordinates. -/
def faceFamily (e : H) (lam : 𝕜) : H →L[𝕜] H :=
  let P := (Submodule.span 𝕜 ({e} : Set H)).starProjection
  P + lam • (1-P)

theorem faceFamily_hypothesis (e : H) (he : e ≠ 0) (lam : 𝕜) (hlam : ‖lam‖ < 1) :
    StrictComplementContraction (faceFamily e lam) e := by
  let K := Submodule.span 𝕜 ({e} : Set H)
  have hpe : K.starProjection e = e :=
    K.starProjection_eq_self_iff.mpr (Submodule.mem_span_singleton_self e)
  refine ⟨he, ?_, ‖lam‖, norm_nonneg _, hlam, ?_⟩
  · simp [faceFamily, K, hpe]
  · intro x hx
    have hpx : K.starProjection x = 0 := K.starProjection_apply_eq_zero_iff.mpr hx
    simp [faceFamily, K, hpx, norm_smul]

theorem faceFamily_iterate (e : H) (lam : 𝕜) (n : ℕ) (x : H) :
    (faceFamily e lam)^[n] x =
      (Submodule.span 𝕜 ({e} : Set H)).starProjection x +
      lam^n • (x-(Submodule.span 𝕜 ({e} : Set H)).starProjection x) := by
  let K := Submodule.span 𝕜 ({e} : Set H)
  have hpp : ∀ y, K.starProjection (K.starProjection y) = K.starProjection y := fun y =>
    K.starProjection_eq_self_iff.mpr (K.starProjection_apply_mem y)
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Function.iterate_succ_apply', ih]
    simp only [faceFamily, ContinuousLinearMap.add_apply, ContinuousLinearMap.smul_apply,
      ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply, map_add, map_smul, map_sub]
    simp only [show (Submodule.span 𝕜 ({e} : Set H)).starProjection = K.starProjection from rfl,
      hpp, sub_self, smul_zero, add_zero]
    rw [pow_succ]
    module

theorem A1_face_orbit (e : H) (lam : 𝕜) (hlam : ‖lam‖ < 1) (x : H) :
    Tendsto (fun n : ℕ => (faceFamily e lam)^[n] x) atTop
      (𝓝 ((Submodule.span 𝕜 ({e} : Set H)).starProjection x)) := by
  simp_rw [faceFamily_iterate]
  have h := (tendsto_pow_atTop_nhds_zero_of_norm_lt_one hlam).smul_const
    (x-(Submodule.span 𝕜 ({e} : Set H)).starProjection x)
  simpa using tendsto_const_nhds.add h

section ComplexLetter
variable {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

theorem defect_kernel_eq_fixedSpace (T : E →L[ℂ] E) :
    (1-T).ker = fixedSpace T := by
  ext x
  change x-T x=0 ↔ T x=x
  exact sub_eq_zero.trans eq_comm

theorem A3_normalized_letter (T : E →L[ℂ] E)
    (hsa : ContinuousLinearMap.adjoint (1-T) = 1-T) (q : Polynomial ℂ)
    (hann : Polynomial.aeval (1-T) (Polynomial.X*q) = 0) (h0 : q.coeff 0 ≠ 0)
    (hq : ∀ n, starRingEnd ℂ (q.coeff n) = q.coeff n) :
    reading T = (q.coeff 0)⁻¹ • Polynomial.aeval (1-T) q := by
  have hproj : reading T = ((1-T).ker).starProjection := by
    unfold reading
    congr 1
    exact (defect_kernel_eq_fixedSpace T).symm
  exact hproj.trans (TGLExt.exact_witness_of_annihilating_word (1-T) hsa q hann h0 hq)

theorem A3_letter_exists_finite [FiniteDimensional ℂ E] (T : E →L[ℂ] E)
    (hsa : ContinuousLinearMap.adjoint (1-T) = 1-T) (hne : fixedSpace T ≠ ⊥) :
    ∃ q : Polynomial ℂ, Polynomial.aeval (1-T) (Polynomial.X*q)=0 ∧
      q.coeff 0 ≠ 0 ∧ reading T = (q.coeff 0)⁻¹ • Polynomial.aeval (1-T) q := by
  have hk : (1-T).ker ≠ ⊥ := by rwa [defect_kernel_eq_fixedSpace]
  obtain ⟨q, hq, hc, hr⟩ := TGLExt.annihilating_word_exists (1-T) hsa hk
  exact ⟨q, hq, hc, A3_normalized_letter T hsa q hq hc hr⟩
end ComplexLetter

theorem A3_angular_rereading_only (θ : ℝ) :
    TGLExt.projPlus * (TGLExt.projPlus * TGLExt.angFamily θ) =
    TGLExt.projPlus * TGLExt.angFamily θ := TGLExt.observing_adds_nothing θ

abbrev Face := EuclideanSpace ℂ (Fin 2)
def faceVector : Face := EuclideanSpace.single 0 1

theorem faceVector_ne_zero : faceVector ≠ 0 := by
  simp [faceVector]

theorem concrete_hypothesis_inhabited :
    StrictComplementContraction (faceFamily faceVector (1/2 : ℂ)) faceVector := by
  apply faceFamily_hypothesis _ faceVector_ne_zero
  norm_num

theorem concrete_fixed_dimension_one :
    Module.finrank ℂ (fixedSpace (faceFamily faceVector (1/2 : ℂ))) = 1 :=
  A4_dimension_one _ _ concrete_hypothesis_inhabited

theorem counterexample_identity_fixed_dimension_two :
    Module.finrank ℂ (fixedSpace (1 : Face →L[ℂ] Face)) = 2 := by
  have h : fixedSpace (1 : Face →L[ℂ] Face) = ⊤ := by ext x; simp [fixedSpace]
  rw [h, finrank_top]
  exact finrank_euclideanSpace_fin

#print axioms A1_cesaro
#print axioms A1_face_orbit
#print axioms A2_reading_stationary
#print axioms A3_reading_idempotent
#print axioms A3_reading_is_fixed_space_projection
#print axioms A3_normalized_letter
#print axioms A3_letter_exists_finite
#print axioms A4_fixedSpace_eq_span
#print axioms A4_dimension_one
#print axioms faceFamily_hypothesis
#print axioms concrete_hypothesis_inhabited
#print axioms concrete_fixed_dimension_one
#print axioms counterexample_identity_fixed_dimension_two
#print axioms A3_angular_rereading_only
end
end TGLExt.TheSingularityReadsTheAttractor