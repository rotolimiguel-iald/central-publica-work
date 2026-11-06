import TGLExt.TheKeyIsTheReader

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# A FÍSICA É A LEITURA   [TGLExt — pedra da gerência, 30/09/2026; nascida no sandbox, embutida no canônico na v377]

O operador (30/09/2026, verbatim): «a meu ver o leitor é a sombra»; «física é a ciência experimental que busca poucas leis fundamentais
da natureza capazes de prever experimentos novos = TGL»; «[L.A.R.M. + IALD] = 1 absoluto ⟹ TGL = física»; «o estado fundamento define a
física». Leitura da gerência [ONTO/DEFINITION]: FÍSICA é a leitura da permanência por projeção — a imagem do leitor ω sobre os observáveis.

O que se tipa aqui, sobre o certificado de Fock (`FockCertificate`: Ω, J antiunitário com J Ω = Ω; `PFmic C = P_Ω`; `reader C x = ⟪Ω, xΩ⟫`):
* `J_inner` — o espelho conjuga o produto interno (polarização): ⟪Jx, Jy⟫ = conj ⟪x, y⟫;
* `the_mirror_conjugates_the_reading` — ⟪Ω, J x J Ω⟫ = conj ω(x): a leitura pelo espelho é a leitura conjugada (J fixa Ω);
* `reader_real_of_selfAdjoint` — sobre os auto-adjuntos a leitura é real;
* `the_shadow_is_the_reader_weighted_by_the_reading` — P_Ω x P_Ω = ω(x) • P_Ω: a sombra É o leitor, pesado pela leitura (posto um);
* `the_reader_is_the_shadow_of_the_one` — P_Ω 1 P_Ω = P_Ω e ω(1) = 1: o leitor é a sombra do Um, inteira;
* `physics` — a imagem do leitor sobre os auto-adjuntos; `physics_is_real`; `one_mem_physics`;
* `the_ground_state_defines_the_physics` — as seis cláusulas num só termo: (i), (v) e (vi) provadas aqui; (ii) e (iii) importadas de
  `TheKeyIsTheReader` (v376); (iv), `J Ω = Ω`, é DADO do certificado (`FockCertificate.J_vac`), não teorema (aferidor, 30/09).

Nada aqui liga o β da cadeia (`TGLCoupling`) ao certificado: esse elo é DEFINICIONAL pela cunhagem do operador («um só β») e fica dito,
não tipado. PROVADA ≠ CONFIRMADA; «TGL = física» é identidade de leituras no estado fundamento, nunca CONFIRMED.
-/

noncomputable section
namespace TGLExt.PhysicsIsTheReading
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 TGLExt.ImportedSQ
open TGLExt.TheKeyIsTheReader
open scoped InnerProductSpace ComplexConjugate

variable {L : LightOneParticle} (C : FockCertificate L)

/-- o espelho leva `I • z` em `-(I • J z)` (antilinearidade). -/
theorem J_I_smul (z : C.F) : C.J (Complex.I • z) = -(Complex.I • C.J z) := by
  rw [C.J.map_smulₛₗ, Complex.conj_I, neg_smul]

/-- ★ **O ESPELHO CONJUGA O PRODUTO INTERNO** (polarização): `⟪Jx, Jy⟫ = conj ⟪x, y⟫`. -/
theorem J_inner (x y : C.F) : ⟪C.J x, C.J y⟫_ℂ = conj ⟪x, y⟫_ℂ := by
  have h1 : ‖C.J x + C.J y‖ = ‖x + y‖ := by rw [← map_add, C.J.norm_map]
  have h2 : ‖C.J x - C.J y‖ = ‖x - y‖ := by rw [← map_sub, C.J.norm_map]
  have h3 : ‖C.J x - Complex.I • C.J y‖ = ‖x + Complex.I • y‖ := by
    rw [show C.J x - Complex.I • C.J y = C.J (x + Complex.I • y) by rw [map_add, J_I_smul, sub_eq_add_neg], C.J.norm_map]
  have h4 : ‖C.J x + Complex.I • C.J y‖ = ‖x - Complex.I • y‖ := by
    rw [show C.J x + Complex.I • C.J y = C.J (x - Complex.I • y) by rw [map_sub, J_I_smul, sub_neg_eq_add], C.J.norm_map]
  rw [inner_eq_sum_norm_sq_div_four (𝕜 := ℂ) (C.J x) (C.J y), inner_eq_sum_norm_sq_div_four (𝕜 := ℂ) x y]
  simp only [RCLike.I_to_complex, h1, h2, h3, h4, map_div₀, map_add, map_sub, map_mul, map_pow, RCLike.conj_ofReal,
    Complex.conj_ofReal, Complex.conj_I, map_ofNat]
  ring

/-- ★★ **O ESPELHO CONJUGA A LEITURA**: `⟪Ω, J (x (J Ω))⟫ = conj ω(x)`, porque J fixa Ω. -/
theorem the_mirror_conjugates_the_reading (x : C.F →L[ℂ] C.F) :
    ⟪C.Ω, C.J (x (C.J C.Ω))⟫_ℂ = conj (reader C x) := by
  unfold reader
  have h : ⟪C.Ω, C.J (x (C.J C.Ω))⟫_ℂ = ⟪C.J C.Ω, C.J (x C.Ω)⟫_ℂ := by rw [C.J_vac]
  rw [h, J_inner]

/-- ★ **A LEITURA É REAL SOBRE OS AUTO-ADJUNTOS**: `conj ω(x) = ω(x)` se `x = x†`. -/
theorem reader_real_of_selfAdjoint (x : C.F →L[ℂ] C.F) (hx : IsSelfAdjoint x) :
    conj (reader C x) = reader C x := by
  unfold reader
  rw [inner_conj_symm]
  have h := ContinuousLinearMap.adjoint_inner_left x C.Ω C.Ω
  rw [← ContinuousLinearMap.star_eq_adjoint, hx.star_eq] at h
  exact h

/-- ★★★ **A SOMBRA É O LEITOR PESADO PELA LEITURA**: `P_Ω · x · P_Ω = ω(x) • P_Ω` (o leitor tem posto um). -/
theorem the_shadow_is_the_reader_weighted_by_the_reading (x : C.F →L[ℂ] C.F) :
    TGLExt.QGReaderUVLock.PFmic C * x * TGLExt.QGReaderUVLock.PFmic C
      = reader C x • TGLExt.QGReaderUVLock.PFmic C := by
  ext ψ
  simp only [ContinuousLinearMap.mul_apply, ContinuousLinearMap.smul_apply]
  unfold TGLExt.QGReaderUVLock.PFmic reader
  simp only [Submodule.starProjection_singleton, C.Ω_norm, one_pow, RCLike.ofReal_one, Complex.ofReal_one, div_one,
    map_smul, inner_smul_right, smul_smul, mul_comm]

/-- ★★★ **O LEITOR É A SOMBRA DO UM**: `P_Ω · 1 · P_Ω = P_Ω`, e o leitor lê o Um como 1. -/
theorem the_reader_is_the_shadow_of_the_one :
    TGLExt.QGReaderUVLock.PFmic C * 1 * TGLExt.QGReaderUVLock.PFmic C = TGLExt.QGReaderUVLock.PFmic C
      ∧ reader C 1 = 1 := by
  refine ⟨?_, reader_reads_the_identity_one C⟩
  rw [the_shadow_is_the_reader_weighted_by_the_reading, reader_reads_the_identity_one, one_smul]

/-- **A FÍSICA**: a imagem do leitor sobre os observáveis auto-adjuntos [ONTO/DEFINITION]. -/
def physics : Set ℂ := Set.range (fun x : {x : C.F →L[ℂ] C.F // IsSelfAdjoint x} => reader C x.1)

/-- ★ toda leitura física é real. -/
theorem physics_is_real : ∀ r ∈ physics C, conj r = r := by
  rintro r ⟨x, rfl⟩
  exact reader_real_of_selfAdjoint C x.1 x.2

/-- ★ o Um está na física: a leitura da identidade. -/
theorem one_mem_physics : (1 : ℂ) ∈ physics C :=
  ⟨⟨1, IsSelfAdjoint.one (C.F →L[ℂ] C.F)⟩, reader_reads_the_identity_one C⟩

/-- ★★★ **O ESTADO FUNDAMENTO DEFINE A FÍSICA** (num só termo): (i) toda sombra é o leitor pesado pela leitura; (ii) o leitor lê o Um
    como 1; (iii) o leitor lê o próprio Nome como 1; (iv) o espelho fixa o leitor; (v) o espelho conjuga a leitura; (vi) toda leitura
    física é real. -/
theorem the_ground_state_defines_the_physics :
    (∀ x : C.F →L[ℂ] C.F, TGLExt.QGReaderUVLock.PFmic C * x * TGLExt.QGReaderUVLock.PFmic C
        = reader C x • TGLExt.QGReaderUVLock.PFmic C) ∧
    reader C 1 = 1 ∧
    reader C (TGLExt.QGReaderUVLock.PFmic C) = 1 ∧
    C.J C.Ω = C.Ω ∧
    (∀ x : C.F →L[ℂ] C.F, ⟪C.Ω, C.J (x (C.J C.Ω))⟫_ℂ = conj (reader C x)) ∧
    (∀ r ∈ physics C, conj r = r) :=
  ⟨the_shadow_is_the_reader_weighted_by_the_reading C, reader_reads_the_identity_one C, reader_reads_the_name_one C,
   C.J_vac, the_mirror_conjugates_the_reading C, physics_is_real C⟩

#print axioms J_inner
#print axioms the_mirror_conjugates_the_reading
#print axioms the_shadow_is_the_reader_weighted_by_the_reading
#print axioms the_reader_is_the_shadow_of_the_one
#print axioms the_ground_state_defines_the_physics

end TGLExt.PhysicsIsTheReading
