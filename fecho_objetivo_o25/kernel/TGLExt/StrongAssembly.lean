import TGLExt.TailNet

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A MONTAGEM DO FORTE — e os TRÊS PRIMEIROS FLIPS honestos do gate
  [TGLExt — v106, o incremento 26 do programa SemifiniteAnalysis]

Com o Dirac genuíno (v105), a rede de caudas ∞-dim (v106a) e o frame
curvo (v104), o certificado FORTE se monta:

* ★ `genuineDirac_kerSub` — ker(N) = o átomo do Nome (span{e₀}):
  N z = 0 ⟹ z_n = 0 ∀n≥1 ⟹ z = z₀·e₀; o canto pesa τ = 1 = ω(I);
* ★★★ `theStrongCertificate : QGClosureCertificateStrong` — MONTADO
  sob nome não-reservado (rede ∞-dim + Dirac ilimitado + canto 1 +
  frame não-constante);
* ★★★ OS TRÊS FLIPS: `qgStrongCertificate_core` / `_corner` / `_frame`
  — os nomes RESERVADOS pelo gate (v103) ganham termos com contratos
  Σ' que FORÇAM o conteúdo forte. Na próxima rodada, o parser v99 lê
  os axiomas e flipa as três flags SOZINHO — a PRIMEIRA movimentação
  de flag da história do gate, POR CONSTRUÇÃO, jamais por declaração.
  O VEREDITO NÃO SE MOVE: solder/einstein/witness seguem False; o selo
  só escala com as SEIS formais + física + dado.

HONESTIDADE: a rede de caudas tem ação trivial nas regiões e não é
III₁ — isso é conteúdo da TESTEMUNHA (v2, FullWitnessData), não do
Strong; o Strong exige exatamente o que estes termos provam.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/-! ## A — o canto do Dirac genuíno: ker(N) = o átomo do Nome -/

theorem genuineDirac_kerSub :
    theGenuineDirac.toUnboundedDiracData.kerSub = firstAtom := by
  apply le_antisymm
  · rintro x ⟨z, hz, rfl⟩
    -- z ∈ ker N.toFun: todas as coordenadas n≥1 morrem
    have hz0 : ∀ n : ℕ, (n : ℂ) * (z : ellTwo) n = 0 := by
      intro n
      have hker : theGenuineDirac.D.toFun z = 0 := LinearMap.mem_ker.mp hz
      have h : ((theGenuineDirac.D.toFun z : ellTwo)) n = ((0 : ellTwo)) n :=
        congrArg (fun w : ellTwo => w n) hker
      have hzero : ((0 : ellTwo)) n = 0 := by rw [lp.coeFn_zero]; rfl
      rw [hzero] at h
      exact h
    have hcoord : ∀ n : ℕ, 1 ≤ n → (z : ellTwo) n = 0 := by
      intro n hn
      have h := hz0 n
      have hne : (n : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
      exact (mul_eq_zero.mp h).resolve_left hne
    -- então z = z₀ • e₀
    have hzeq : (z : ellTwo) = ((z : ellTwo) 0) • firstInscription := by
      apply Subtype.ext
      funext n
      rw [lp.coeFn_smul, Pi.smul_apply]
      unfold firstInscription
      rw [inscriptions_apply]
      rcases Nat.eq_zero_or_pos n with rfl | hn
      · simp [smul_eq_mul]
      · rw [if_neg (by omega : n ≠ 0), hcoord n hn]
        simp
    show (z : ellTwo) ∈ firstAtom
    rw [hzeq]
    exact Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self _)
  · intro x hx
    obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hx
    refine ⟨⟨x, ?_⟩, ?_, rfl⟩
    · -- x = c • e₀ mora no domínio
      rw [← hc]
      exact Submodule.smul_mem numberDomain c (single_mem_numberDomain 0)
    · -- e N x = 0
      apply LinearMap.mem_ker.mpr
      apply Subtype.ext
      funext n
      show (n : ℂ) * x n = (0 : ellTwo) n
      rw [lp.coeFn_zero]
      rw [← hc, lp.coeFn_smul, Pi.smul_apply]
      unfold firstInscription
      rw [inscriptions_apply]
      rcases Nat.eq_zero_or_pos n with rfl | hn
      · simp
      · rw [if_neg (by omega : n ≠ 0)]
        simp

theorem genuineDirac_corner_pos :
    0 < dimOrTop ℂ theGenuineDirac.toUnboundedDiracData.kerSub := by
  rw [genuineDirac_kerSub, dimOrTop_firstAtom]
  exact zero_lt_one

theorem genuineDirac_corner_finite :
    dimOrTop ℂ theGenuineDirac.toUnboundedDiracData.kerSub < ⊤ := by
  rw [genuineDirac_kerSub, dimOrTop_firstAtom]
  exact ENNReal.one_lt_top

/-! ## B — A MONTAGEM (nome não-reservado primeiro: a ordem do rito) -/

/-- [KERNEL] ★★★ O CERTIFICADO FORTE MONTADO: rede ∞-dim + Dirac
    genuinamente ilimitado + canto τ=1=ω(I) + frame não-constante. -/
def theStrongCertificate : QGClosureCertificateStrong where
  Region := ℕ
  leR := fun a b => b ≤ a
  H := fun n => tailSub n
  W := fun n => tailSub n
  core := theTailNet
  core_infinite := ⟨0, tailSub_not_finiteDimensional 0⟩
  ℍ := ellTwo
  dirac := theGenuineDirac
  home_infinite := ellTwo_not_finiteDimensional
  corner_pos := genuineDirac_corner_pos
  corner_finite := genuineDirac_corner_finite
  frame := theCurvedFrame
  frame_nonconstant := curvedFrame_nonconstant

/-! ## C — OS TRÊS FLIPS (os nomes reservados ganham termos) -/

/-- [KERNEL] ★★★ FLIP 1 — o núcleo AQFT forte: rede genuinamente
    isótona, grupo não-trivial, fibra ∞-DIMENSIONAL. -/
def qgStrongCertificate_core :
    Σ' (_ : PhysicalNetData ℕ (fun a b => b ≤ a)
        (fun n => tailSub n) (fun n => tailSub n)),
      ∃ O : ℕ, ¬ FiniteDimensional ℂ (tailSub O) :=
  ⟨theTailNet, 0, tailSub_not_finiteDimensional 0⟩

/-- [KERNEL] ★★★ FLIP 2 — o canto de Breuer forte: Dirac genuinamente
    ILIMITADO auto-adjunto com canto 0 < τ < ∞ (τ = 1 = ω(I)). -/
def qgStrongCertificate_corner :
    Σ' (d : GenuinelyUnboundedDiracData ellTwo),
      0 < dimOrTop ℂ d.toUnboundedDiracData.kerSub
        ∧ dimOrTop ℂ d.toUnboundedDiracData.kerSub < ⊤ :=
  ⟨theGenuineDirac, genuineDirac_corner_pos, genuineDirac_corner_finite⟩

/-- [KERNEL] ★★★ FLIP 3 — o four-frame forte: campo suave, det
    invertível em toda parte, NÃO-constante. -/
def qgStrongCertificate_frame :
    Σ' (f : SmoothFrameData), ∃ x y : Fin 4 → ℝ, f.E x ≠ f.E y :=
  ⟨theCurvedFrame, curvedFrame_nonconstant⟩

end

end TGLExt
