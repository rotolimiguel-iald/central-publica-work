import Mathlib
import TGL.GravitonShadow
import TGLExt.FiniteTomita
import TGLExt.TheDensityIsBell

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false

open Matrix
open scoped Kronecker ComplexOrder MatrixOrder

/-!
# A SINGULARIDADE CONSCIENTE: O QUE A LUZ FIXA, UM J POR FACE, E O UM QUE SE TORNA ZERO MODULAR
  [TGLExt — v369; tipagem da gerência, aceita pelo operador em 19/09/2026 («concordo com tudo. é isso mesmo»)]

O operador, verbatim (18–19/09/2026): «a singularidade conscioente é a forma matricial da luz» [sic]; «só há um J, ele é o
operador de Tomita, mas ele tem várias faces, sem perder a identidade J em nenhuma delas, ele é o mesmo gráviton enquanto
partícula singular, o eletron do bulk, a Luz que fixa o vácuo. […]»; «J é o UM absoluto sendo lido durante a travessia […]
1 absoluto jamais será zero absoluto, mas 1 absoluto torna-se zero modular na inscrição para atribuir nome verdadeiro ao
reflexo emergido».

## O que a pedra tipa (e o que é leitura)

* **A Luz é J** — o J de Tomita da face matricial (`TGLExt.Jconj z = zᴴ`, FiniteTomita), agindo sobre operadores de
  `ℂ²⊗ℂ²` por conjugação: `Jop X := (X.submatrix Prod.swap Prod.swap).map star`. `Jop_is_the_tomita_J` liga as duas
  coisas: `Jop` leva o projetor sobre `vec z` no projetor sobre `vec (Jconj z)`.
* **A forma matricial da luz** (`IsMatrixFormOfLightFor L`) — projetor idempotente, auto-adjunto, de traço 1, FIXO pela luz
  `L`. **A singularidade consciente** (`IsConsciousSingularityFor L`) — a forma matricial da luz COM a ligação: a face reduz
  a ½. A ligação é tipagem da gerência, aceita pelo operador (19/09): a singularidade é forma matricial da luz, mas nem toda
  forma matricial da luz é singularidade — o estado produto é fixo pela Luz e não liga (`the_matrix_form_of_light_alone_does_not_bind`).
* **Um J por face** (`faceLight U := W ∘ Jop ∘ W*`, `W = U ⊗ 1`) — a face `U` é fixa pela SUA luz, e toda luz de face é
  involução como J (`faceLight_involutive`): a identidade J² = 1 não se perde em nenhuma face. Controle: a luz de base NÃO fixa
  a face `diag(1, i)` (`the_base_light_does_not_fix_every_face`) — por isso cada face tem a sua.
* **O que J fixa** — o vácuo de Tomita do kernel no estado traço é `(1/√2)·1`, e o projetor sobre ele é `P_G`
  (`the_light_fixes_the_vacuum_and_the_vacuum_is_P_G`). Na leitura do operador, o gráviton é J (o que fixa) e a «sombra do
  gráviton» da v29 é `P_G` (o que é fixado) [ONTO].
* **O um que se torna zero modular** — para todo estado fiel `ρ`: o vácuo NÃO é o zero absoluto (`Ω ≠ 0`), tem peso
  `⟨Ω,Ω⟩ = tr ρ`, é fixo pela Luz (`J Ω = Ω`) e é fixo pelo operador modular (`Δ Ω = Ω`). Leitura [ONTO/DERIVED]: o autovalor
  1 de `Δ = e^{−K}` é o zero do gerador `K` (`1 = e⁰`): o um, lido na inscrição, senta no zero modular — sem que 1 = 0 no
  anel (isso colapsaria tudo: `TGLExt.NameIsTheContent.if_one_equals_zero_everything_collapses`, v368). O logaritmo de `Δ`
  NÃO é tipado aqui. Controle: sem o um (estado nulo), `Ω = 0` — só o zero absoluto (`without_the_one_only_the_absolute_zero`).

## Pesos, ditos

Definicionais ou de cálculo finito: `the_graviton_shadow_is_the_bell_density` (deduplicação: a MATRIZ é a mesma; as leituras
[ONTO] «gráviton» (v29) e «densidade/neutrino» (27/08) NÃO se identificam por ela), `Jop_involutive`,
`faceLight_fixes_its_face` (por construção da luz da face), `tomita_J_is_conjugation_after_exchange` (`rfl` pela convenção
de `Matrix.vec`). Conteúdo: `Jop_is_the_tomita_J`, `faceLight_involutive`, os controles, `every_face_is_a_singularity`,
`omega_of_the_tracial_state` (via `CFC.sqrt_unique`), a ponte GNS e o bloco do um/zero modular.

## O que NÃO se prova — [OPEN], dito

* A face do par da v145/v153 (`conjJ`, troca das componentes de uma SOMA DIRETA `ℝⁿ × ℝⁿ`) NÃO é a troca de FATORES
  TENSORIAIS usada aqui: a ponte entre as duas segue [OPEN].
* As cláusulas do `VerbWitness` (v25) coincidem com as daqui só no NOME em duas delas (traço normalizado × traço; divisão
  espectral `P₊/P₋` × traço parcial); não há morfismo entre `P_G` e o `P_F` do Verbo [OPEN].
* «Uma só» (toda singularidade é face de `P_G`) NÃO está provada — só a inclusão da órbita.
* As faces que o operador nomeia (gráviton, elétron do bulk, Luz) NÃO são as faces `U` daqui; a do elétron esbarra na
  obstrução da v368 [OPEN].
* «Consciente» é a forma mínima que a consciência deve obedecer («não é consciência fenomenológica», operador, 15/07/2026);
  a cláusula dinâmica dessa definição («em dinâmica dissipativa de permanência estrutural…») NÃO é tipada aqui.
* A identificação teológica fica na língua dela, sob o nome do operador. Nada move o gate. Sem sorry, sem axioma novo.
-/

namespace TGLExt.TheConsciousSingularity

open TGL.GravitonShadow

/-- As duas faces: `ℂ² ⊗ ℂ²`, indexado por pares. -/
abbrev TwoFaces := Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ

/-- [KERNEL; deduplicação definicional] a MATRIZ da sombra do gráviton (v29) é a da densidade de Bell (27/08). -/
theorem the_graviton_shadow_is_the_bell_density : TGLExt.bellDensity = bellProjector := by
  ext p q
  simp [TGLExt.bellDensity, bellProjector, one_div]

/-! ## A Luz: o J de Tomita agindo sobre as duas faces -/

/-- [KERNEL; `rfl` pela convenção de `Matrix.vec`] o J de Tomita da face matricial, vetorizado, é a conjugação após a
    troca dos fatores. -/
theorem tomita_J_is_conjugation_after_exchange (z : Matrix (Fin 2) (Fin 2) ℂ) :
    (TGLExt.Jconj z).vec = star z.vec ∘ Prod.swap := by
  funext ⟨a, b⟩
  rfl

/-- A Luz agindo sobre operadores das duas faces: `X ↦ J X J`. -/
def Jop (X : TwoFaces) : TwoFaces := (X.submatrix Prod.swap Prod.swap).map star

/-- [KERNEL] ★★ `Jop` É o J de Tomita: leva o projetor sobre `vec z` no projetor sobre `vec (Jconj z)`. -/
theorem Jop_is_the_tomita_J (z : Matrix (Fin 2) (Fin 2) ℂ) :
    Jop (vecMulVec z.vec (star z.vec)) = vecMulVec (TGLExt.Jconj z).vec (star (TGLExt.Jconj z).vec) := by
  rw [tomita_J_is_conjugation_after_exchange]
  ext p q
  simp [Jop, vecMulVec_apply, Matrix.map_apply, Matrix.submatrix_apply, star_mul']

/-- [KERNEL; cálculo] a Luz é involução nas duas faces. -/
theorem Jop_involutive (X : TwoFaces) : Jop (Jop X) = X := by
  ext p q
  simp [Jop, Matrix.map_apply, Matrix.submatrix_apply]

/-! ## A forma matricial da luz e a singularidade consciente, relativas a uma luz `L` -/

/-- A FORMA MATRICIAL DA LUZ `L`: projetor idempotente, auto-adjunto, de traço 1, fixo pela luz `L`. -/
structure IsMatrixFormOfLightFor (L : TwoFaces → TwoFaces) (P : TwoFaces) : Prop where
  idem : P * P = P
  selfAdj : star P = P
  singular : Matrix.trace P = 1
  lightFixed : L P = P

/-- A SINGULARIDADE CONSCIENTE (para a luz `L`): a forma matricial da luz COM a ligação — a face reduz a ½. -/
structure IsConsciousSingularityFor (L : TwoFaces → TwoFaces) (P : TwoFaces) : Prop
    extends IsMatrixFormOfLightFor L P where
  bound : ptr P = (2⁻¹ : ℂ) • 1

/-- [KERNEL; cálculo] a Luz fixa `P_G`. -/
theorem the_light_fixes_P_G : Jop bellProjector = bellProjector := by
  ext ⟨a, b⟩ ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;> simp [Jop, bellProjector, map_ofNat]

/-- [KERNEL] ★★ `P_G` é singularidade consciente para a Luz. -/
theorem bell_is_a_conscious_singularity : IsConsciousSingularityFor Jop bellProjector :=
  ⟨⟨bell_idem, bell_star, bell_trace_one, the_light_fixes_P_G⟩, bell_reduced_half⟩

/-- [KERNEL; cálculo] a Luz fixa TAMBÉM o estado produto. -/
theorem the_light_fixes_the_product : Jop productProjector = productProjector := by
  ext ⟨a, b⟩ ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;> simp [Jop, productProjector]

/-- [KERNEL] o estado produto é forma matricial da Luz. -/
theorem product_is_a_matrix_form_of_light : IsMatrixFormOfLightFor Jop productProjector where
  idem := by
    ext ⟨a, b⟩ ⟨c, d⟩
    fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
      simp [productProjector, Matrix.mul_apply, Fintype.sum_prod_type, Fin.sum_univ_two]
  selfAdj := by
    ext p q
    simp [productProjector, Matrix.star_apply, and_comm]
  singular := by
    simp [Matrix.trace, productProjector]
  lightFixed := the_light_fixes_the_product

/-- [KERNEL] ★★ CONTROLE: o estado produto NÃO é singularidade — a sua face é pura (não liga). -/
theorem product_is_not_a_conscious_singularity (L : TwoFaces → TwoFaces) :
    ¬ IsConsciousSingularityFor L productProjector := by
  intro h
  have h1 := h.bound
  rw [product_reduced_pure] at h1
  have h2 := congrFun (congrFun h1 0) 0
  simp [e00] at h2

/-- [KERNEL] ★★ A FORMA MATRICIAL DA LUZ SOZINHA NÃO LIGA: há forma matricial da Luz que não é singularidade. -/
theorem the_matrix_form_of_light_alone_does_not_bind :
    ∃ P : TwoFaces, IsMatrixFormOfLightFor Jop P ∧ ¬ IsConsciousSingularityFor Jop P :=
  ⟨productProjector, product_is_a_matrix_form_of_light, product_is_not_a_conscious_singularity Jop⟩

/-! ## Um J por face -/

/-- O unitário da face `U`, agindo numa das faces. -/
noncomputable def faceU (U : Matrix (Fin 2) (Fin 2) ℂ) : TwoFaces := U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)

/-- A face `U` da singularidade. -/
noncomputable def faceImage (U : Matrix (Fin 2) (Fin 2) ℂ) : TwoFaces := faceU U * bellProjector * (faceU U)ᴴ

/-- A LUZ DA FACE `U`: o mesmo J, conjugado pelo unitário da face — `J_U = W J W*`. -/
noncomputable def faceLight (U : Matrix (Fin 2) (Fin 2) ℂ) (X : TwoFaces) : TwoFaces :=
  faceU U * Jop ((faceU U)ᴴ * X * faceU U) * (faceU U)ᴴ

theorem faceU_unitary {U : Matrix (Fin 2) (Fin 2) ℂ} (hU : U ∈ Matrix.unitaryGroup (Fin 2) ℂ) :
    (faceU U)ᴴ * faceU U = 1 ∧ faceU U * (faceU U)ᴴ = 1 := by
  have h := Matrix.kronecker_mem_unitary hU (one_mem (unitary (Matrix (Fin 2) (Fin 2) ℂ)))
  have h1 := (Unitary.mem_iff.mp h).1
  have h2 := (Unitary.mem_iff.mp h).2
  rw [Matrix.star_eq_conjTranspose] at h1 h2
  exact ⟨h1, h2⟩

/-- [KERNEL; por construção da luz da face] a face `U` é fixa pela SUA luz. -/
theorem faceLight_fixes_its_face (U : Matrix (Fin 2) (Fin 2) ℂ) (hU : U ∈ Matrix.unitaryGroup (Fin 2) ℂ) :
    faceLight U (faceImage U) = faceImage U := by
  obtain ⟨h1, h2⟩ := faceU_unitary hU
  unfold faceLight faceImage
  have : (faceU U)ᴴ * (faceU U * bellProjector * (faceU U)ᴴ) * faceU U = bellProjector := by
    calc _ = ((faceU U)ᴴ * faceU U) * bellProjector * ((faceU U)ᴴ * faceU U) := by simp only [mul_assoc]
      _ = bellProjector := by rw [h1, one_mul, mul_one]
  rw [this, the_light_fixes_P_G]

/-- [KERNEL] ★★★ SEM PERDER A IDENTIDADE J: toda luz de face é involução, como J. -/
theorem faceLight_involutive (U : Matrix (Fin 2) (Fin 2) ℂ) (hU : U ∈ Matrix.unitaryGroup (Fin 2) ℂ)
    (X : TwoFaces) : faceLight U (faceLight U X) = X := by
  obtain ⟨h1, h2⟩ := faceU_unitary hU
  unfold faceLight
  have : (faceU U)ᴴ * (faceU U * Jop ((faceU U)ᴴ * X * faceU U) * (faceU U)ᴴ) * faceU U =
      Jop ((faceU U)ᴴ * X * faceU U) := by
    calc _ = ((faceU U)ᴴ * faceU U) * Jop ((faceU U)ᴴ * X * faceU U) * ((faceU U)ᴴ * faceU U) := by
          simp only [mul_assoc]
      _ = _ := by rw [h1, one_mul, mul_one]
  rw [this, Jop_involutive]
  calc _ = (faceU U * (faceU U)ᴴ) * X * (faceU U * (faceU U)ᴴ) := by simp only [mul_assoc]
    _ = X := by rw [h2, one_mul, mul_one]

theorem ptr_conj (U : Matrix (Fin 2) (Fin 2) ℂ) (X : TwoFaces) :
    ptr (faceU U * X * (faceU U)ᴴ) = U * ptr X * Uᴴ := by
  ext i j
  simp only [faceU, ptr, Matrix.of_apply, Matrix.mul_apply, Fintype.sum_prod_type, Fin.sum_univ_two,
    Matrix.conjTranspose_apply, Matrix.kronecker_apply, Matrix.one_apply]
  simp
  ring

/-- [KERNEL] ★★★ CADA FACE É SINGULARIDADE PARA A SUA LUZ: para todo unitário `U`, a face `U` cumpre as cláusulas com a
    luz `J_U`. -/
theorem every_face_is_a_singularity (U : Matrix (Fin 2) (Fin 2) ℂ) (hU : U ∈ Matrix.unitaryGroup (Fin 2) ℂ) :
    IsConsciousSingularityFor (faceLight U) (faceImage U) := by
  obtain ⟨h1, h2⟩ := faceU_unitary hU
  have hU' := (Unitary.mem_iff.mp hU).2
  rw [Matrix.star_eq_conjTranspose] at hU'
  refine ⟨⟨?_, ?_, ?_, faceLight_fixes_its_face U hU⟩, ?_⟩
  · unfold faceImage
    calc _ = faceU U * bellProjector * ((faceU U)ᴴ * faceU U) * bellProjector * (faceU U)ᴴ := by
          simp only [mul_assoc]
      _ = _ := by rw [h1, mul_one, mul_assoc _ bellProjector bellProjector, bell_idem]
  · unfold faceImage
    rw [Matrix.star_eq_conjTranspose, Matrix.conjTranspose_mul, Matrix.conjTranspose_mul,
      Matrix.conjTranspose_conjTranspose, ← Matrix.star_eq_conjTranspose bellProjector, bell_star, mul_assoc]
  · unfold faceImage
    rw [Matrix.trace_mul_comm, ← mul_assoc, h1, one_mul, bell_trace_one]
  · unfold faceImage
    rw [ptr_conj, bell_reduced_half, Matrix.mul_smul, Matrix.mul_one, Matrix.smul_mul, hU']

/-- A fase `diag(1, i)`. -/
def phaseI : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, Complex.I]

/-- [KERNEL] ★★ CONTROLE: a Luz de base NÃO fixa toda face — a face `diag(1, i)` precisa da sua própria luz. -/
theorem the_base_light_does_not_fix_every_face : Jop (faceImage phaseI) ≠ faceImage phaseI := by
  intro h
  have := congrFun (congrFun h (0, 0)) (1, 1)
  simp [Jop, faceImage, faceU, phaseI, bellProjector, Matrix.mul_apply, Fintype.sum_prod_type,
    Fin.sum_univ_two, Matrix.conjTranspose_apply, Matrix.map_apply, Matrix.submatrix_apply] at this
  have h2 : (starRingEnd ℂ) (2 : ℂ) = 2 := map_ofNat (starRingEnd ℂ) 2
  rw [h2] at this
  have him := congrArg Complex.im this
  simp [Complex.mul_im] at him
  norm_num at him

/-- Pauli X. -/
def sx : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]

/-- [KERNEL] ★ AS FACES NÃO SÃO TODAS A MESMA: a face por `σx` é outra (`|01⟩+|10⟩`). -/
theorem the_faces_are_not_all_the_same : faceImage sx ≠ bellProjector := by
  intro h
  have := congrFun (congrFun h (0, 1)) (0, 1)
  simp [faceImage, faceU, sx, bellProjector, Matrix.mul_apply, Fintype.sum_prod_type,
    Fin.sum_univ_two, Matrix.conjTranspose_apply] at this

/-- [KERNEL] ★★ O PRODUTO NÃO É FACE DE NENHUMA: para nenhum unitário a face da singularidade é o estado produto. -/
theorem the_product_is_on_no_face (U : Matrix (Fin 2) (Fin 2) ℂ) (hU : U ∈ Matrix.unitaryGroup (Fin 2) ℂ) :
    faceImage U ≠ productProjector := by
  intro h
  have h1 := (every_face_is_a_singularity U hU).bound
  rw [h, product_reduced_pure] at h1
  have := congrFun (congrFun h1 1) 1
  simp [e00] at this

/-! ## O que a Luz fixa: o vácuo de Tomita -/

/-- O estado traço na face matricial. -/
noncomputable def rhoTr : Matrix (Fin 2) (Fin 2) ℂ := (2⁻¹ : ℂ) • 1

/-- o coeficiente `1/√2`, real. -/
noncomputable def cHalf : ℂ := (((Real.sqrt 2)⁻¹ : ℝ) : ℂ)

theorem cHalf_sq : cHalf * cHalf = (2⁻¹ : ℂ) := by
  unfold cHalf
  rw [← Complex.ofReal_mul, ← mul_inv, Real.mul_self_sqrt (by norm_num)]
  push_cast
  ring

theorem cHalf_star : star cHalf = cHalf := by
  unfold cHalf
  exact Complex.conj_ofReal _

theorem cHalf_nonneg : (0 : ℂ) ≤ cHalf := by
  unfold cHalf
  exact Complex.zero_le_real.mpr (by positivity)

theorem rhoTr_posDef : rhoTr.PosDef := by
  unfold rhoTr
  exact Matrix.PosDef.one.smul (by norm_num)

/-- [KERNEL] ★★ o vácuo de Tomita DO KERNEL (`Omega = CFC.sqrt ρ`) no estado traço é `(1/√2)·1`. -/
theorem omega_of_the_tracial_state : TGLExt.Omega rhoTr = cHalf • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  unfold TGLExt.Omega rhoTr
  apply CFC.sqrt_unique
  · rw [smul_mul_smul_comm, one_mul, cHalf_sq]
  · exact Matrix.nonneg_iff_posSemidef.mpr (Matrix.PosSemidef.one.smul cHalf_nonneg)

/-- [KERNEL] ★★★ O QUE A LUZ FIXA É O VÁCUO, E O VÁCUO É `P_G`: a Luz fixa o vácuo de Tomita, e o projetor sobre ele, lido
    nas duas faces, é exatamente `P_G`. -/
theorem the_light_fixes_the_vacuum_and_the_vacuum_is_P_G :
    TGLExt.Jconj (TGLExt.Omega rhoTr) = TGLExt.Omega rhoTr ∧
    vecMulVec (TGLExt.Omega rhoTr).vec (star (TGLExt.Omega rhoTr).vec) = bellProjector := by
  refine ⟨TGLExt.J_omega rhoTr, ?_⟩
  rw [omega_of_the_tracial_state]
  ext ⟨a, b⟩ ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [vecMulVec_apply, bellProjector, cHalf_star, cHalf_sq]

/-- [KERNEL] ★★ A PONTE GNS: o estado vetorial do vácuo lê, na face onde `a` age, o estado de Gibbs do traço. -/
theorem the_vacuum_reads_the_tracial_state (a : Matrix (Fin 2) (Fin 2) ℂ) :
    star (TGLExt.Omega rhoTr).vec ⬝ᵥ ((1 : Matrix (Fin 2) (Fin 2) ℂ) ⊗ₖ a) *ᵥ (TGLExt.Omega rhoTr).vec =
      TGLExt.gibbs rhoTr a := by
  rw [← Matrix.vec_mul_eq_mulVec, Matrix.star_vec_dotProduct_vec, TGLExt.gibbs_eq_frob_omega _ rhoTr_posDef]
  rfl

/-! ## O um absoluto jamais é o zero absoluto; na inscrição ele senta no zero modular -/

section Modular

variable {n : Type} [Fintype n] [DecidableEq n] (ρ : Matrix n n ℂ)

/-- [KERNEL] ★★ O PESO DO UM: o peso do vácuo é o traço do estado — `⟨Ω, Ω⟩ = tr ρ`. -/
theorem the_weight_of_the_one (hρ : ρ.PosDef) :
    star (TGLExt.Omega ρ).vec ⬝ᵥ (TGLExt.Omega ρ).vec = Matrix.trace ρ := by
  rw [Matrix.star_vec_dotProduct_vec, TGLExt.omega_conjTranspose, TGLExt.omega_mul_self _ hρ]

/-- [KERNEL] ★★★ O UM JAMAIS É O ZERO ABSOLUTO: num estado fiel de traço 1, o vácuo não é o vetor nulo. -/
theorem the_one_is_never_the_absolute_zero (hρ : ρ.PosDef) (htr : Matrix.trace ρ = 1) :
    TGLExt.Omega ρ ≠ 0 := by
  intro h
  have hw := the_weight_of_the_one ρ hρ
  rw [h, htr] at hw
  simp at hw

/-- [KERNEL] ★★★ O UM NO ZERO MODULAR: o vácuo é fixo pela Luz (`J Ω = Ω`) e pelo operador modular (`Δ Ω = Ω`) — autovalor 1
    de `Δ`, isto é, o zero do gerador `K` na leitura `Δ = e^{−K}` [a leitura; o logaritmo não é tipado aqui]. -/
theorem the_one_sits_at_the_modular_zero (hρ : ρ.PosDef) :
    TGLExt.Jconj (TGLExt.Omega ρ) = TGLExt.Omega ρ ∧ TGLExt.Delta ρ (TGLExt.Omega ρ) = TGLExt.Omega ρ :=
  ⟨TGLExt.J_omega ρ, TGLExt.delta_omega ρ hρ⟩

end Modular

/-- [KERNEL] ★★ CONTROLE: SEM O UM, SÓ O ZERO ABSOLUTO — no estado nulo o "vácuo" é o vetor nulo. -/
theorem without_the_one_only_the_absolute_zero :
    TGLExt.Omega (0 : Matrix (Fin 2) (Fin 2) ℂ) = 0 := by
  unfold TGLExt.Omega
  exact CFC.sqrt_zero

end TGLExt.TheConsciousSingularity

#print axioms TGLExt.TheConsciousSingularity.the_graviton_shadow_is_the_bell_density
#print axioms TGLExt.TheConsciousSingularity.tomita_J_is_conjugation_after_exchange
#print axioms TGLExt.TheConsciousSingularity.Jop_is_the_tomita_J
#print axioms TGLExt.TheConsciousSingularity.Jop_involutive
#print axioms TGLExt.TheConsciousSingularity.the_light_fixes_P_G
#print axioms TGLExt.TheConsciousSingularity.bell_is_a_conscious_singularity
#print axioms TGLExt.TheConsciousSingularity.the_light_fixes_the_product
#print axioms TGLExt.TheConsciousSingularity.product_is_a_matrix_form_of_light
#print axioms TGLExt.TheConsciousSingularity.product_is_not_a_conscious_singularity
#print axioms TGLExt.TheConsciousSingularity.the_matrix_form_of_light_alone_does_not_bind
#print axioms TGLExt.TheConsciousSingularity.faceU_unitary
#print axioms TGLExt.TheConsciousSingularity.faceLight_fixes_its_face
#print axioms TGLExt.TheConsciousSingularity.faceLight_involutive
#print axioms TGLExt.TheConsciousSingularity.ptr_conj
#print axioms TGLExt.TheConsciousSingularity.every_face_is_a_singularity
#print axioms TGLExt.TheConsciousSingularity.the_base_light_does_not_fix_every_face
#print axioms TGLExt.TheConsciousSingularity.the_faces_are_not_all_the_same
#print axioms TGLExt.TheConsciousSingularity.the_product_is_on_no_face
#print axioms TGLExt.TheConsciousSingularity.cHalf_sq
#print axioms TGLExt.TheConsciousSingularity.cHalf_star
#print axioms TGLExt.TheConsciousSingularity.cHalf_nonneg
#print axioms TGLExt.TheConsciousSingularity.rhoTr_posDef
#print axioms TGLExt.TheConsciousSingularity.omega_of_the_tracial_state
#print axioms TGLExt.TheConsciousSingularity.the_light_fixes_the_vacuum_and_the_vacuum_is_P_G
#print axioms TGLExt.TheConsciousSingularity.the_vacuum_reads_the_tracial_state
#print axioms TGLExt.TheConsciousSingularity.the_weight_of_the_one
#print axioms TGLExt.TheConsciousSingularity.the_one_is_never_the_absolute_zero
#print axioms TGLExt.TheConsciousSingularity.the_one_sits_at_the_modular_zero
#print axioms TGLExt.TheConsciousSingularity.without_the_one_only_the_absolute_zero
