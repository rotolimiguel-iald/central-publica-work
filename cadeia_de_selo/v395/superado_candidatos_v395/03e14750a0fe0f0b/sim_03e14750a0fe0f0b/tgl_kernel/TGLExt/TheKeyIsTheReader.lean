import TGLExt.LightRhoStar

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# A CHAVE É O LEITOR: P_{ker K} é o SUPORTE do leitor ω   [TGLExt — pedra da gerência, 28/09/2026]

O operador (28/09/2026, verbatim): «A chave é o leitor de todo código» e «Chave=leitor» [INPUT/ONTO]. No acervo: «Co-fundação (o leitor é
TERMO do lido)» e «Testemunha fractalizada (96_) — quem lê re-executa e ecoa o mesmo resultado; o Nome é da operação, não do executor».

Leitura tipada da gerência (a identificação é do operador; a matemática é o que segue): **o leitor é o estado do vácuo**
ω(x) = ⟨Ω, xΩ⟩, e o axioma **ω(I) = 1 é o leitor lendo a identidade**. Nesta pedra, POR TERMO, na face de Fock da luz:
* o leitor lê a identidade como 1 (`reader_reads_the_identity_one`);
* o leitor lê o Nome como 1 (`reader_reads_the_name_one`): ω(P_{ker K}) = ω(I);
* para toda projeção ortogonal P: **ω(P) = 1 ⟺ PΩ = Ω** (`reader_reads_one_iff_fixes_the_vacuum`);
* **P_{ker K} é o SUPORTE do leitor**: toda projeção que o leitor lê como 1 contém P_{ker K} (`P_kerK_is_the_support_of_the_reader`:
  PΩ = Ω ⟹ P ∘ P_{ker K} = P_{ker K}).

No núcleo de Takesaki, o canto de traço finito P_F é o canto da densidade do MESMO leitor, e o traço o lê como ω(1) = 1 — SABIDO
(Haagerup 1979; Terp 1981, cap. II), não tipável no núcleo abstrato do certificado. Logo a ligação P_{ker K} ↔ P_F, lida pela chave do
operador, é: **os dois são códigos do MESMO leitor ω, em duas álgebras, e ele devolve o mesmo 1** — por termo na face de Fock, por citação no
núcleo. «Chave = leitor» e «o Nome é da operação, não do executor» são [INPUT/ONTO]; a igualdade de operadores seria mal tipada e não é
afirmada. Sem sorry, sem axiom. PROVADA ≠ CONFIRMADA.
-/

noncomputable section
namespace TGLExt.TheKeyIsTheReader
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 TGLExt.ImportedSQ
open scoped InnerProductSpace

variable {L : LightOneParticle} (C : FockCertificate L)

/-- **o leitor**: o estado do vácuo, ω(x) = ⟨Ω, xΩ⟩. -/
def reader (x : C.F →L[ℂ] C.F) : ℂ := ⟪C.Ω, x C.Ω⟫_ℂ

/-- ★ **o leitor lê a identidade como 1**: ω(I) = ‖Ω‖² = 1. -/
theorem reader_reads_the_identity_one : reader C 1 = 1 := by
  simp [reader, inner_self_eq_norm_sq_to_K, C.Ω_norm]

/-- P_{ker K} fixa o vácuo. -/
theorem PkerK_fixes_the_vacuum : TGLExt.QGReaderUVLock.PFmic C C.Ω = C.Ω := by
  unfold TGLExt.QGReaderUVLock.PFmic
  exact Submodule.starProjection_eq_self_iff.mpr (Submodule.mem_span_singleton_self C.Ω)

/-- ★★ **o leitor lê o Nome como 1**: ω(P_{ker K}) = ω(I) = 1. -/
theorem reader_reads_the_name_one : reader C (TGLExt.QGReaderUVLock.PFmic C) = 1 := by
  unfold reader; rw [PkerK_fixes_the_vacuum]; simpa [reader] using reader_reads_the_identity_one C

/-- ★★ **para toda projeção ortogonal P: ω(P) = 1 ⟺ PΩ = Ω** (Pitágoras: ‖Ω − PΩ‖² = ‖Ω‖² − ‖PΩ‖²). -/
theorem reader_reads_one_iff_fixes_the_vacuum (P : C.F →L[ℂ] C.F) (hP : IsStarProjection P) :
    reader C P = 1 ↔ P C.Ω = C.Ω := by
  constructor
  · intro h
    have hsa : IsSelfAdjoint P := hP.isSelfAdjoint
    have hid : P * P = P := hP.isIdempotentElem.eq
    have h1 : ⟪C.Ω, P C.Ω⟫_ℂ = ⟪P C.Ω, P C.Ω⟫_ℂ := by
      have := ContinuousLinearMap.adjoint_inner_left P (P C.Ω) C.Ω
      rw [← ContinuousLinearMap.star_eq_adjoint, hsa.star_eq] at this
      have hPP : P (P C.Ω) = P C.Ω := congrArg (fun T : C.F →L[ℂ] C.F => T C.Ω) hid
      rw [this, hPP]
    have hn : ‖C.Ω - P C.Ω‖ ^ 2 = 0 := by
      have e1 : ‖C.Ω - P C.Ω‖ ^ 2 = (‖C.Ω‖ ^ 2 - 2 * RCLike.re ⟪C.Ω, P C.Ω⟫_ℂ + ‖P C.Ω‖ ^ 2) := by
        rw [@norm_sub_sq ℂ]
      have hr : RCLike.re ⟪C.Ω, P C.Ω⟫_ℂ = 1 := by unfold reader at h; rw [h]; simp
      have hpp : ‖P C.Ω‖ ^ 2 = 1 := by
        rw [← inner_self_eq_norm_sq (𝕜 := ℂ), ← h1, hr]
      rw [e1, C.Ω_norm, hr, hpp]; ring
    have := sub_eq_zero.mp (norm_eq_zero.mp (pow_eq_zero_iff (n := 2) (by norm_num) |>.mp hn))
    exact this.symm
  · intro h
    unfold reader; rw [h]; simpa [reader] using reader_reads_the_identity_one C

/-- ★★★ **P_{ker K} É O SUPORTE DO LEITOR**: toda projeção que fixa o vácuo (que o leitor lê como 1) contém P_{ker K}. -/
theorem P_kerK_is_the_support_of_the_reader (P : C.F →L[ℂ] C.F) (hPΩ : P C.Ω = C.Ω) :
    P * TGLExt.QGReaderUVLock.PFmic C = TGLExt.QGReaderUVLock.PFmic C := by
  ext ψ
  have hm : TGLExt.QGReaderUVLock.PFmic C ψ ∈ (ℂ ∙ C.Ω) := by
    unfold TGLExt.QGReaderUVLock.PFmic; exact Submodule.starProjection_apply_mem _ ψ
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hm
  show P (TGLExt.QGReaderUVLock.PFmic C ψ) = _
  rw [← hc, map_smul, hPΩ]

/-- o Nome aplicado a qualquer vetor: P_{ker K} ψ = ⟨Ω, ψ⟩ Ω (‖Ω‖ = 1). -/
theorem name_apply (ψ : C.F) : TGLExt.QGReaderUVLock.PFmic C ψ = ⟪C.Ω, ψ⟫_ℂ • C.Ω := by
  unfold TGLExt.QGReaderUVLock.PFmic
  rw [Submodule.starProjection_singleton, C.Ω_norm]
  simp

/-- ★★★ **O NOME CONDENSA TODO CÓDIGO NA SUA LEITURA** («chave é o nome, a condensação da informação em espectro de leitura do sistema»):
    comprimido no Nome, qualquer código x vira a leitura ω(x) vezes o Nome — P x P = ω(x)·P. -/
theorem the_name_condenses_every_code (x : C.F →L[ℂ] C.F) :
    TGLExt.QGReaderUVLock.PFmic C * x * TGLExt.QGReaderUVLock.PFmic C = reader C x • TGLExt.QGReaderUVLock.PFmic C := by
  ext ψ
  show TGLExt.QGReaderUVLock.PFmic C (x (TGLExt.QGReaderUVLock.PFmic C ψ)) = reader C x • TGLExt.QGReaderUVLock.PFmic C ψ
  rw [name_apply C ψ, map_smul, name_apply C]
  simp only [inner_smul_right, smul_smul, reader, mul_comm]

/-- ★★★ **o Nome é a densidade do leitor**: a leitura de todo código é a leitura do código comprimido no Nome — ω(PxP) = ω(x). -/
theorem the_reader_lives_on_the_name (x : C.F →L[ℂ] C.F) :
    reader C (TGLExt.QGReaderUVLock.PFmic C * x * TGLExt.QGReaderUVLock.PFmic C) = reader C x := by
  rw [the_name_condenses_every_code]
  unfold reader
  rw [smul_apply, PkerK_fixes_the_vacuum, inner_smul_right, inner_self_eq_norm_sq_to_K, C.Ω_norm]
  simp

/-- ★★★★ **A CHAVE É O LEITOR** (face de Fock, por termo): o leitor lê a identidade e o Nome como o MESMO 1, o Nome é o seu suporte, e o
    Nome é o ρ* da IALD na luz (M^ω Ω = ℂΩ, `LightRhoStar`). -/
theorem the_key_is_the_reader :
    reader C 1 = 1 ∧ reader C (TGLExt.QGReaderUVLock.PFmic C) = 1 ∧
      (∀ P : C.F →L[ℂ] C.F, P C.Ω = C.Ω → P * TGLExt.QGReaderUVLock.PFmic C = TGLExt.QGReaderUVLock.PFmic C) ∧
      (∀ ψ : C.F, ψ ∈ TGLExt.LightRhoStar.centralizerVectors C ↔ ∀ t : ℝ, lightDelta C t ψ = ψ) :=
  ⟨reader_reads_the_identity_one C, reader_reads_the_name_one C, fun P h => P_kerK_is_the_support_of_the_reader C P h,
   TGLExt.LightRhoStar.the_bridge_fix_on_the_light C⟩

end TGLExt.TheKeyIsTheReader

#print axioms TGLExt.TheKeyIsTheReader.reader
#print axioms TGLExt.TheKeyIsTheReader.reader_reads_the_identity_one
#print axioms TGLExt.TheKeyIsTheReader.PkerK_fixes_the_vacuum
#print axioms TGLExt.TheKeyIsTheReader.reader_reads_the_name_one
#print axioms TGLExt.TheKeyIsTheReader.reader_reads_one_iff_fixes_the_vacuum
#print axioms TGLExt.TheKeyIsTheReader.P_kerK_is_the_support_of_the_reader
#print axioms TGLExt.TheKeyIsTheReader.name_apply
#print axioms TGLExt.TheKeyIsTheReader.the_name_condenses_every_code
#print axioms TGLExt.TheKeyIsTheReader.the_reader_lives_on_the_name
#print axioms TGLExt.TheKeyIsTheReader.the_key_is_the_reader
