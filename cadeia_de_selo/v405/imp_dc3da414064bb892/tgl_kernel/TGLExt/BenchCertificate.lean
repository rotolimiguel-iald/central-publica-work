import TGLExt.IdealLimit

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O CERTIFICADO DE BANCADA E O ENDURECIMENTO DO GATE
  [TGLExt — v103, o incremento 20 do programa SemifiniteAnalysis]

A DESCOBERTA DESTA PEDRA (a sonda que morde o próprio certificado): o
tipo `QGClosureCertificate` (v99) é HABITÁVEL COM CONTEÚDO DE BANCADA —
e nós o habitamos, DE PROPÓSITO, sob nome NÃO-reservado:

* `theBenchDirac : UnboundedDiracData ellTwo` — T = 1−P₀ como
  `LinearPMap` em domínio ⊤: star(D) = D (pelo adjunto ilimitado da
  mathlib), kernel = o átomo do Nome, GAP = 1 = ω(I). O tipo NÃO exige
  ilimitação — e este habitante o PROVA (`benchDirac_is_bounded`);
* `theConstantFrame : SmoothFrameData` — o frame constante 1: suave,
  det invertível, e o coframe paralelo SAI DE GRAÇA (a face plana);
* ★★★ `theBenchCertificate : QGClosureCertificate` — O CERTIFICADO v1
  INTEIRO habitado (rede v101 + Dirac de bancada + canto τ=1 + frame
  constante). O GATE NÃO SE MOVE: o termo NÃO usa os nomes reservados —
  e o runtime re-deriva que o veredito segue CONDITIONAL.

A CONSEQUÊNCIA (fail-closed fica MAIS fechado): a letra do tipo v1 não
força o espírito (ilimitado; fibra ∞-dim; frame não-constante). Esta
pedra TIPA o endurecimento e prova que a bancada NÃO o alimenta:

* `GenuinelyUnboundedDiracData` — Dirac + ilimitação EXIGIDA;
  ★ `bench_cannot_feed_strong` — theBenchDirac NÃO entra (é limitado);
* `QGClosureCertificateStrong` — certificado + `core_infinite` (alguma
  fibra ∞-dim) + Dirac genuinamente ilimitado + `frame_nonconstant`
  (o `coframe_parallel` do v1 CAI: forçava a face plana — curvatura e
  covariância são o v2);
  ★ `isotone_cannot_feed_strong_core` — as fibras do v101 são TODAS
  finito-dim; ★ `constant_cannot_feed_strong_frame` — o frame constante
  não entra. O gate do runtime REAPONTA os nomes reservados para o tipo
  FORTE (`qgStrongCertificate_*`): conteúdo de bancada JAMAIS moverá o
  gate, agora por teorema + construção.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/-! ## A — o Dirac de bancada: T = 1−P₀ como operador parcial em ⊤ -/

theorem topDense : Dense ((⊤ : Submodule ℂ ellTwo) : Set ellTwo) := by
  rw [Submodule.top_coe]
  exact dense_univ

/-- T = 1 − P₀ como `LinearPMap` de domínio ⊤ (a moldura do ilimitado,
    ocupada por um limitado — de propósito: a sonda). -/
def benchDiracPMap : ellTwo →ₗ.[ℂ] ellTwo := eraseFirst.toPMap ⊤

theorem benchDiracPMap_apply (x : benchDiracPMap.domain) :
    benchDiracPMap x = eraseFirst (x : ellTwo) :=
  LinearMap.toPMap_apply _ ⊤ x

/-- [KERNEL] ★ star(D) = D no sentido do adjunto ILIMITADO da mathlib
    (via `toPMap_adjoint_eq_adjoint_toPMap_of_dense` + auto-adjunção
    limitada do v95). -/
theorem benchDiracPMap_selfadjoint : IsSelfAdjoint benchDiracPMap := by
  rw [LinearPMap.isSelfAdjoint_def]
  show (eraseFirst.toPMap ⊤).adjoint = eraseFirst.toPMap ⊤
  rw [ContinuousLinearMap.toPMap_adjoint_eq_adjoint_toPMap_of_dense
    eraseFirst topDense, eraseFirst_selfadjoint]

theorem eraseFirst_kills_first : eraseFirst firstInscription = 0 := by
  have hmem : firstInscription ∈ firstAtom :=
    Submodule.mem_span_singleton_self firstInscription
  rw [eraseFirst_apply, Submodule.starProjection_eq_self_iff.mpr hmem, sub_self]

theorem firstInscription_mem_benchDomain :
    firstInscription ∈ benchDiracPMap.domain := by
  show firstInscription ∈ (⊤ : Submodule ℂ ellTwo)
  exact Submodule.mem_top

/-- [KERNEL] ★ o GAP QUADRÁTICO com gap = 1 = ω(I): ortogonal ao kernel
    ⟹ ‖Dx‖ = ‖x‖ (T é a projeção complementar do Nome). -/
theorem benchDirac_quad_gap (x : benchDiracPMap.domain)
    (h : ∀ y : benchDiracPMap.domain, benchDiracPMap y = 0 →
      inner ℂ (y : ellTwo) (x : ellTwo) = 0) :
    (1 : ℝ) * ‖(x : ellTwo)‖ ≤ ‖benchDiracPMap x‖ := by
  have h0 : inner ℂ firstInscription (x : ellTwo) = 0 :=
    h ⟨firstInscription, firstInscription_mem_benchDomain⟩
      (by rw [benchDiracPMap_apply]; exact eraseFirst_kills_first)
  have hP : firstAtom.starProjection (x : ellTwo) = 0 := by
    unfold firstAtom
    rw [Submodule.starProjection_singleton ℂ, h0, zero_div, zero_smul]
  have hDx : benchDiracPMap x = (x : ellTwo) := by
    rw [benchDiracPMap_apply, eraseFirst_apply, hP, sub_zero]
  rw [hDx, one_mul]

/-- [KERNEL] ★★ O HABITANTE DO TIPO v1: `UnboundedDiracData ellTwo` tem
    termo — com gap 1 = ω(I) e kernel = o átomo do Nome. (A sonda: o
    tipo não exigiu ilimitação.) -/
def theBenchDirac : UnboundedDiracData ellTwo where
  D := benchDiracPMap
  selfadjoint := benchDiracPMap_selfadjoint
  gap := 1
  gap_pos := one_pos
  ker_witness :=
    ⟨⟨firstInscription, firstInscription_mem_benchDomain⟩,
      inscriptions_orthonormal.ne_zero 0,
      by rw [benchDiracPMap_apply]; exact eraseFirst_kills_first⟩
  quad_gap := benchDirac_quad_gap

/-- [KERNEL] ★ o canto do Dirac de bancada é o kernel do v95:
    kerSub = ker(1−P₀) = o átomo do Nome. -/
theorem benchDirac_kerSub : theBenchDirac.kerSub = eraseFirst.ker := by
  show ((LinearMap.ker ((↑eraseFirst : ellTwo →ₗ[ℂ] ellTwo).comp
      (⊤ : Submodule ℂ ellTwo).subtype)).map
      (⊤ : Submodule ℂ ellTwo).subtype) = eraseFirst.ker
  rw [LinearMap.ker_comp, Submodule.map_comap_subtype, top_inf_eq]

theorem dimOrTop_firstAtom : dimOrTop ℂ firstAtom = 1 := by
  have h : dimOrTop ℂ firstAtom = (Module.finrank ℂ firstAtom : ℝ≥0∞) :=
    dimOrTop_of_finite ℂ inferInstance
  have h2 : Module.finrank ℂ firstAtom = 1 := by
    unfold firstAtom
    exact finrank_span_singleton (inscriptions_orthonormal.ne_zero 0)
  rw [h, h2, Nat.cast_one]

theorem benchDirac_corner_pos : 0 < dimOrTop ℂ theBenchDirac.kerSub := by
  rw [benchDirac_kerSub, ker_eraseFirst, dimOrTop_firstAtom]
  exact zero_lt_one

theorem benchDirac_corner_finite : dimOrTop ℂ theBenchDirac.kerSub < ⊤ := by
  rw [benchDirac_kerSub, ker_eraseFirst, dimOrTop_firstAtom]
  exact ENNReal.one_lt_top

/-! ## B — o frame constante (a face plana habita SmoothFrameData) -/

/-- o frame constante 1: suave, det = 1 invertível. -/
def theConstantFrame : SmoothFrameData where
  E := fun _ => (1 : Matrix (Fin 4) (Fin 4) ℝ)
  smooth := fun _ _ => contDiff_const
  det_unit := fun _ => by rw [Matrix.det_one]; exact isUnit_one

/-! ## C — O CERTIFICADO DE BANCADA (nome NÃO-reservado, de propósito) -/

/-- [KERNEL] ★★★ O CERTIFICADO v1 HABITADO EM BANCADA: rede v101 +
    Dirac de bancada + canto τ=1 em morada ∞-dim + frame constante.
    O NOME NÃO É RESERVADO — o gate não lê este termo; o que este termo
    PROVA é que a letra do tipo v1 não força o espírito (e por isso o
    gate REAPONTA para o tipo forte). -/
def theBenchCertificate : QGClosureCertificate where
  Region := ℕ
  leR := (· ≤ ·)
  H := fun n => fiber n
  W := fun n => fiber n
  core := theIsotoneNet
  ℍ := ellTwo
  dirac := theBenchDirac
  home_infinite := ellTwo_not_finiteDimensional
  corner_pos := benchDirac_corner_pos
  corner_finite := benchDirac_corner_finite
  frame := theConstantFrame
  coframe_parallel := by
    intro x i j
    have h : (fun y : Fin 4 → ℝ =>
        ((theConstantFrame.E y)⁻¹ : Matrix (Fin 4) (Fin 4) ℝ) i j)
        = fun _ => ((1 : Matrix (Fin 4) (Fin 4) ℝ)⁻¹) i j := rfl
    rw [h]
    exact fderiv_const_apply _

/-! ## D — o ENDURECIMENTO: os tipos que a bancada NÃO alimenta -/

/-- [DATA — o alvo FORTE] o Dirac GENUINAMENTE ilimitado: o tipo v1
    MAIS a ilimitação exigida (nenhuma cota C serve). -/
structure GenuinelyUnboundedDiracData (ℍ : Type) [NormedAddCommGroup ℍ]
    [InnerProductSpace ℂ ℍ] [CompleteSpace ℍ]
    extends UnboundedDiracData ℍ where
  unbounded : ¬ ∃ C : ℝ, ∀ x : D.domain, ‖D x‖ ≤ C * ‖(x : ℍ)‖

/-- [DATA — O CERTIFICADO FORTE] o v1 endurecido: alguma fibra ∞-dim
    (`core_infinite`), Dirac genuinamente ILIMITADO, e frame
    NÃO-CONSTANTE. O `coframe_parallel` do v1 CAI: em ℝ⁴ conexo ele
    forçava coframe constante (a face plana) — curvatura e covariância
    pertencem ao v2. Os nomes de gate `qgStrongCertificate_*` ficam
    RESERVADOS para termos construídos DESTE tipo. -/
structure QGClosureCertificateStrong where
  Region : Type
  leR : Region → Region → Prop
  H : Region → Type
  W : Region → Type
  [instH₁ : ∀ O, NormedAddCommGroup (H O)]
  [instH₂ : ∀ O, InnerProductSpace ℂ (H O)]
  [instH₃ : ∀ O, CompleteSpace (H O)]
  [instW₁ : ∀ O, NormedAddCommGroup (W O)]
  [instW₂ : ∀ O, NormedSpace ℂ (W O)]
  core : PhysicalNetData Region leR H W
  core_infinite : ∃ O : Region, ¬ FiniteDimensional ℂ (H O)
  ℍ : Type
  [instD₁ : NormedAddCommGroup ℍ]
  [instD₂ : InnerProductSpace ℂ ℍ]
  [instD₃ : CompleteSpace ℍ]
  dirac : GenuinelyUnboundedDiracData ℍ
  home_infinite : ¬ FiniteDimensional ℂ ℍ
  corner_pos : 0 < dimOrTop ℂ dirac.toUnboundedDiracData.kerSub
  corner_finite : dimOrTop ℂ dirac.toUnboundedDiracData.kerSub < ⊤
  frame : SmoothFrameData
  frame_nonconstant : ∃ x y : Fin 4 → ℝ, frame.E x ≠ frame.E y

/-! ## E — os probes: a bancada NÃO alimenta o forte (os dentes) -/

/-- [KERNEL] ★ o Dirac de bancada é LIMITADO (C = ‖T‖ serve): o tipo v1
    não o excluiu — o forte o exclui. -/
theorem benchDirac_is_bounded :
    ∃ C : ℝ, ∀ x : theBenchDirac.D.domain,
      ‖theBenchDirac.D x‖ ≤ C * ‖(x : ellTwo)‖ := by
  refine ⟨‖eraseFirst‖, fun x => ?_⟩
  show ‖benchDiracPMap x‖ ≤ ‖eraseFirst‖ * ‖(x : ellTwo)‖
  rw [benchDiracPMap_apply]
  exact eraseFirst.le_opNorm _

/-- [KERNEL] ★ A BANCADA NÃO ALIMENTA O FORTE: nenhum habitante do tipo
    genuinamente ilimitado tem o Dirac de bancada por baixo. -/
theorem bench_cannot_feed_strong :
    ¬ ∃ g : GenuinelyUnboundedDiracData ellTwo,
      g.toUnboundedDiracData = theBenchDirac := by
  rintro ⟨g, hg⟩
  apply g.unbounded
  rw [hg]
  exact benchDirac_is_bounded

/-- [KERNEL] ★ as fibras da rede v101 são TODAS finito-dim: a rede de
    bancada NÃO testemunha `core_infinite`. -/
theorem isotone_cannot_feed_strong_core :
    ¬ ∃ O : ℕ, ¬ FiniteDimensional ℂ (fiber O) := by
  rintro ⟨O, hO⟩
  exact hO (fiber_fd O)

/-- [KERNEL — probe PURO] o frame constante não testemunha
    `frame_nonconstant`. -/
theorem constant_cannot_feed_strong_frame :
    ¬ ∃ x y : Fin 4 → ℝ, theConstantFrame.E x ≠ theConstantFrame.E y := by
  rintro ⟨x, y, hxy⟩
  exact hxy rfl

end

end TGLExt
