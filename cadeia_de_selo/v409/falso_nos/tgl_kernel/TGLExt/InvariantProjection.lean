import TGLExt.ClosedLattice

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A PROJEÇÃO NO COMUTANTE: o primeiro contato com a subálgebra
  [TGLExt — v83, o incremento 5 do programa SemifiniteAnalysis]

O v82 deu o reticulado FECHADO (projeções de B(H)). O canto de Breuer
genuíno, porém, pede projeções DA ÁLGEBRA — isto é, projeções que COMUTAM
com os operadores dados: o comutante. Esta pedra prova o dicionário
fundamental de von Neumann entre subespaços invariantes e projeções no
comutante, e o aplica ao kernel de um operador auto-adjunto:

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★ `closed_projection_idempotent` — P_S é idempotente para todo S com
  projeção ortogonal (o caráter de projeção em Hilbert geral);
* ★ `starProjection_eq_zero_of_mem_orthogonal` — P_S anula a contra-face
  (P_S y = 0 para y ⊥ S; via S ⊓ Sᗮ = ⊥ do v82);
* ★ `orthogonal_invariant_of_adjoint_invariant` — se S é invariante sob
  a†, então Sᗮ é invariante sob a (o papel do adjunto: a estrela troca
  face por contra-face);
* ★★ `starProjection_commutes_of_invariant` — O DICIONÁRIO DE VON
  NEUMANN (ida): S invariante sob a e a† ⟹ P_S ∘ a = a ∘ P_S — a
  projeção pertence ao COMUTANTE {a}′;
* ★ `invariant_of_starProjection_commutes` — (volta): se P_S comuta com
  a, então S é a-invariante;
* ★★ `selfadjoint_invariant_iff_commutes` — para a = a†: S invariante ⟺
  P_S ∈ {a}′ — subespaços invariantes E projeções do comutante são O
  MESMO OBJETO (a porta de entrada da teoria de von Neumann);
* ★★ `selfadjoint_ker_projection_in_commutant` — o kernel de um operador
  AUTO-ADJUNTO comuta com ele: P_{ker T} ∈ {T}′ — a primeira projeção
  genuinamente DA álgebra (o canto pertence ao comutante do operador);
* ★★★ `breuer_corner_projection_in_commutant` — O CANTO DE BREUER COMO
  PROJEÇÃO NO COMUTANTE (v80 × v82 × v83): para T auto-adjunto com
  kernel ≠ ⊥ sob gap de dimensão finita, em H ∞-dim: P_{ker T} COMUTA
  com T ∧ 0 < τ(ker T) < ∞ ∧ τ((ker T)ᗮ) = ⊤ — a inscrição é uma
  projeção finita DO COMUTANTE dentro de um complemento infinito.

HONESTIDADE: comutante de UM operador (a face {T}′) — a subálgebra de
von Neumann completa (bicomutante contínuo, normalidade do τ na álgebra,
fator) segue o programa; nada aqui é III₁; nenhuma flag do fecho se
move. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [DEF] invariância de um subespaço sob um operador contínuo. -/
def Invariant (a : H →L[ℂ] H) (S : Submodule ℂ H) : Prop :=
  ∀ x ∈ S, a x ∈ S

/-- [KERNEL] ★ o caráter de projeção em Hilbert geral: P_S ∘ P_S = P_S. -/
theorem closed_projection_idempotent (S : Submodule ℂ H)
    [S.HasOrthogonalProjection] :
    IsIdempotentElem S.starProjection :=
  Submodule.isIdempotentElem_starProjection S

/-- [KERNEL] ★ a projeção anula a contra-face: P_S y = 0 para y ⊥ S
    (composição com S ⊓ Sᗮ = ⊥ do v82). -/
theorem starProjection_eq_zero_of_mem_orthogonal (S : Submodule ℂ H)
    [S.HasOrthogonalProjection] {y : H} (hy : y ∈ Sᗮ) :
    S.starProjection y = 0 := by
  have h1 : S.starProjection y ∈ S := Submodule.starProjection_apply_mem _ y
  have h2 : y - S.starProjection y ∈ Sᗮ :=
    Submodule.sub_starProjection_mem_orthogonal y
  have h5 : y - (y - S.starProjection y) = S.starProjection y :=
    sub_sub_cancel y _
  have h3 : S.starProjection y ∈ Sᗮ := by
    rw [← h5]
    exact Submodule.sub_mem _ hy h2
  have h4 : S.starProjection y ∈ S ⊓ Sᗮ := Submodule.mem_inf.mpr ⟨h1, h3⟩
  rw [orthocomplement_meet_bot S, Submodule.mem_bot] at h4
  exact h4

/-- [KERNEL] ★ o papel do adjunto: S invariante sob a† ⟹ Sᗮ invariante
    sob a (a estrela troca face por contra-face). -/
theorem orthogonal_invariant_of_adjoint_invariant (a : H →L[ℂ] H)
    (S : Submodule ℂ H)
    (hadj : Invariant (ContinuousLinearMap.adjoint a) S) :
    Invariant a Sᗮ := by
  intro y hy
  rw [Submodule.mem_orthogonal] at hy ⊢
  intro u hu
  have h0 : inner ℂ ((ContinuousLinearMap.adjoint a) u) y = 0 :=
    hy _ (hadj u hu)
  have hL := ContinuousLinearMap.adjoint_inner_left a y u
  rw [← hL]
  exact h0

/-- [KERNEL] ★★ O DICIONÁRIO DE VON NEUMANN (ida): S invariante sob a e
    a† ⟹ P_S comuta com a — a projeção pertence ao COMUTANTE {a}′. -/
theorem starProjection_commutes_of_invariant (a : H →L[ℂ] H)
    (S : Submodule ℂ H) [S.HasOrthogonalProjection]
    (hinv : Invariant a S)
    (hadj : Invariant (ContinuousLinearMap.adjoint a) S) (x : H) :
    S.starProjection (a x) = a (S.starProjection x) := by
  have h1 : S.starProjection (a (S.starProjection x)) = a (S.starProjection x) :=
    Submodule.starProjection_eq_self_iff.mpr
      (hinv _ (Submodule.starProjection_apply_mem _ x))
  have hq : x - S.starProjection x ∈ Sᗮ :=
    Submodule.sub_starProjection_mem_orthogonal x
  have h2 : S.starProjection (a (x - S.starProjection x)) = 0 :=
    starProjection_eq_zero_of_mem_orthogonal S
      (orthogonal_invariant_of_adjoint_invariant a S hadj _ hq)
  calc S.starProjection (a x)
      = S.starProjection (a (S.starProjection x) + a (x - S.starProjection x)) := by
        rw [← map_add]
        congr 1
        abel
    _ = a (S.starProjection x) := by
        rw [map_add, h1, h2, add_zero]

/-- [KERNEL] ★ (volta): se P_S comuta com a, então S é a-invariante. -/
theorem invariant_of_starProjection_commutes (a : H →L[ℂ] H)
    (S : Submodule ℂ H) [S.HasOrthogonalProjection]
    (hcomm : ∀ x, S.starProjection (a x) = a (S.starProjection x)) :
    Invariant a S := by
  intro x hx
  have hx' : S.starProjection x = x := Submodule.starProjection_eq_self_iff.mpr hx
  have : S.starProjection (a x) = a x := by
    rw [hcomm x, hx']
  exact Submodule.starProjection_eq_self_iff.mp this

/-- [KERNEL] ★★ para a auto-adjunto: subespaço invariante ⟺ projeção no
    comutante — o dicionário completo (a porta da teoria de von Neumann). -/
theorem selfadjoint_invariant_iff_commutes (a : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint a = a)
    (S : Submodule ℂ H) [S.HasOrthogonalProjection] :
    Invariant a S ↔ ∀ x, S.starProjection (a x) = a (S.starProjection x) := by
  constructor
  · intro hinv
    have hadj : Invariant (ContinuousLinearMap.adjoint a) S := by
      rw [hsa]
      exact hinv
    exact starProjection_commutes_of_invariant a S hinv hadj
  · exact invariant_of_starProjection_commutes a S

/-- [INSTÂNCIA] o kernel de um operador contínuo tem projeção ortogonal
    (é fechado num Hilbert completo). -/
instance kerHasOrthogonalProjection (T : H →L[ℂ] H) :
    (T.ker).HasOrthogonalProjection :=
  haveI : CompleteSpace (T.ker) :=
    (ContinuousLinearMap.isClosed_ker T).completeSpace_coe
  inferInstance

/-- [KERNEL] ★★ o kernel de um operador AUTO-ADJUNTO comuta com ele:
    P_{ker T} ∈ {T}′ — a primeira projeção genuinamente DA álgebra. -/
theorem selfadjoint_ker_projection_in_commutant (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) (x : H) :
    (T.ker).starProjection (T x)
      = T ((T.ker).starProjection x) := by
  have hinv : Invariant T (T.ker) := by
    intro y hy
    have hy0 : T y = 0 := LinearMap.mem_ker.mp hy
    exact LinearMap.mem_ker.mpr (by rw [hy0, map_zero])
  have hadj : Invariant (ContinuousLinearMap.adjoint T) (T.ker) := by
    rw [hsa]
    exact hinv
  exact starProjection_commutes_of_invariant T _ hinv hadj x

/-- [KERNEL] ★★★ O CANTO DE BREUER COMO PROJEÇÃO NO COMUTANTE
    (v80 × v82 × v83): para T auto-adjunto com kernel não-trivial sob gap
    de dimensão finita, em H ∞-dim — P_{ker T} COMUTA com T, o peso do
    canto é POSITIVO e FINITO, e o complemento pesa ⊤: a inscrição é uma
    projeção finita DO COMUTANTE dentro de um complemento infinito. -/
theorem breuer_corner_projection_in_commutant (hH : ¬FiniteDimensional ℂ H)
    (T : H →L[ℂ] H) (hsa : ContinuousLinearMap.adjoint T = T)
    (gp : Submodule ℂ H) (hker : T.ker ≠ ⊥)
    (hle : T.ker ≤ gp) (hgp : FiniteDimensional ℂ gp) :
    (∀ x, (T.ker).starProjection (T x)
        = T ((T.ker).starProjection x)) ∧
      ((0 < (semifiniteDimTrace ℂ H).tau (T.ker) ∧
          (semifiniteDimTrace ℂ H).tau (T.ker) < ⊤) ∧
        (semifiniteDimTrace ℂ H).tau (T.ker)ᗮ = ⊤) := by
  have hw := closed_local_breuer_corner hH (T.ker) gp hker hle hgp
  exact ⟨selfadjoint_ker_projection_in_commutant T hsa, hw.1.1, hw.2⟩

end

end TGLExt
