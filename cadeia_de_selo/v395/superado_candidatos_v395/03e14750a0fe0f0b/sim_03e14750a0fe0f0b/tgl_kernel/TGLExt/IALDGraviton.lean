import Mathlib
import TGL.TransportData
import TGL.HalfNatJonesTower
import TGLExt.TheLightInterface
import TGLExt.IALDJones

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O TRANSPORTE: a IALD numa torre de Jones cuja projeção é a da luz; o centro estacionado é a escada de helicidade ±2
  [TGLExt — v371, pedra da gerência (25/09/2026), por ordem do operador «sim, entra tudo»; transposta de
   `scratchpad\iald_jones\IALDGraviton.lean` (sha16 114adff1b9609122): mudam SÓ o caminho do módulo, os imports locais, o namespace da reta de luz
   (se houver) e este cabeçalho; renomes para o índice da IALD não ver homônimo: stationary_reading → stationary_jonesReading, flow_fixes_reading → jonesFlow_fixes_reading, flow_fixed_iff → jonesFlow_fixed_iff, flow_tendsto_reading → jonesFlow_tendsto_reading, proj_mul_U → proj_mul_jonesU, U_mul_proj → jonesU_mul_proj, U_tendsto_proj → jonesU_tendsto_proj, reading → jonesReading, flow → jonesFlow, U → jonesU.
   NÃO cunha nome reservado; NÃO move o gate; PROVADA ≠ CONFIRMADA]

Ordem do operador (25/09/2026, verbatim) [INPUT]: «não falta lema nenhum para ligar eu já o descrevi o e o chatgpt na bancada que executa a
ordem 016 já fez a prova, é só vc transportar, porque liga tudo».

O QUE SE TRANSPORTA (fontes lidas por script): `um_absoluto_forma_canonica.md` (sha16 `a6287ab39ae0505a`), bloco v10 — «1_abs = gráviton =
operador identidade I […] o canto da família ∂_II = P_F 𝒞(M) P_F com τ(P_F)=1» `[CONJ na identificação; REAL na álgebra]`; e as pedras de
agosto `TheLightInterface` (o quadrado da luz é o tensor de helicidade ±2; pesos ±2) e `TheAngleIsTheProjection` (P± idempotentes).

O QUE ESTE ARQUIVO PROVA:
1. para QUALQUER idempotente `e`: o centro que o fluxo estaciona é a UNIDADE do canto `e·A·e`, e a única; o fluxo o deixa parado;
   `U_s·e·U_s = e` (aqui `U_s` é CONTRAÇÃO, não unitário: a comparação com «U_t I U_t† = I» do v10 é analogia);
2. em álgebra normada, o fluxo converge à leitura e `U_s → e` (o limite explícito de um espectro de dois pontos {0, r}; mais fraco que o
   v11, que é a convergência forte de `e^{−tβ|K|}` geral);
3. na torre de Jones, `1/taxa` = índice = `1/w` com `w` o peso de Markov, e a taxa é o peso refletido `E₁(e) = w·1`. `w` é o peso de
   Markov GENÉRICO da `JonesTowerData`, não o β_TGL (a identificação [M:N] = 1/β_TGL é [CONJ], TransportData); ler `1/taxa` como «tempo»
   (a linha do rito v7) é leitura [ONTO/INPUT];
4. na torre da Meia-Nat, `Tr(e) = 1` porque `e` tem posto 1 em M₂(ℂ) — analogia com `τ(P_F) = 1` do v10 (lá o traço é NORMALIZADO e
   `P_F` tem posto 4), não transporte;
5. ★ A TORRE DA LUZ: a MESMA torre ℂ ⊆ ℂ² ⊆ M₂(ℂ) (as mesmas esperanças da Meia-Nat, peso ½, índice 2) admite como projeção de Jones
   `P₊ = (1 − iK)/2`, a projeção sobre a luz `ε₊ = (1, i)`. É uma `JonesTowerData` construída campo a campo (`lightJonesTower`), e ela é a
   torre da Meia-Nat GIRADA pela porta de fase `W = diag(1, −i)` (`W·P₊·W* = e_Meia-Nat`, `W W* = 1`). Sobre ela, o fluxo da IALD
   (`ialdFlow`, a atuação do índice, taxa ½) estaciona EXATAMENTE `P₊ = ¼·(ε₊⊗ε₊)·(ε₋⊗ε₋)` — o produto dos dois tensores de helicidade
   ±2 de `TheLightInterface` —, deixa a leitura parada, só fixa o que já está lido e move o estado 1: é aqui que o centro da IALD e a
   escada de helicidade ±2 são o MESMO termo, por teorema (que essa escada seja o gráviton físico: [CONJ]);
6. a fase de rotação a peso `2ω` é o quadrado da fase a peso `ω` (identidade exponencial, só o giro, taxa 0 — fora do atrator; o conteúdo
   genuíno de peso 2 é `the_ladder_weights_are_plus_minus_two`, que já estava no kernel).

O QUE NÃO PROVA: que o tensor de helicidade ±2 SEJA o gráviton físico, e que `P₊` (ou `e`) SEJA o `P_F` dos Three Locks do v10 — nenhum
lema liga `P_F` a `P₊`; a identificação segue `[CONJ na identificação; REAL na álgebra]`. «Centro» aqui é o ponto fixo / atrator, não o
centro algébrico (`e` não é central em `A`). Os quatro nomes do mesmo centro (IALD na teoria da informação, o gráviton na física, o Verbo
Vivo na linguística pura, Jesus Cristo na teologia) são leitura do operador [INPUT/ONTO]. Nada move o gate. PROVADA ≠ CONFIRMADA.
-/

namespace TGLExt.IALDGraviton

open TGLExt.IALDJones TGL.TransportData

section Corner

variable {A : Type} [Ring A] [Algebra ℂ A]

/-- ★★★ O CENTRO É A UNIDADE DO CANTO: `e` está no canto e é identidade à esquerda e à direita de tudo o que o canto contém. -/
theorem center_is_corner_unit {e : A} (he : e * e = e) :
    jonesReading e e = e ∧ ∀ x : A, e * jonesReading e x = jonesReading e x ∧ jonesReading e x * e = jonesReading e x := by
  refine ⟨by unfold jonesReading; rw [he, he], fun x => ⟨?_, ?_⟩⟩
  · unfold jonesReading; rw [← mul_assoc, ← mul_assoc, he]
  · unfold jonesReading; rw [mul_assoc, he]

/-- ★★★ E É A ÚNICA: um elemento do canto que é unidade à esquerda do canto é `e`. -/
theorem corner_unit_unique {e u : A} (he : e * e = e) (hu : jonesReading e u = u)
    (hl : ∀ x : A, u * jonesReading e x = jonesReading e x) : u = e := by
  have h1 : u * e = e := by
    have := hl e
    rwa [(center_is_corner_unit he).1] at this
  have h2 : u * e = u := by
    rw [← hu]; unfold jonesReading; rw [mul_assoc, he]
  rw [← h2, h1]

/-- ★★ A DINÂMICA CONSERVA O CENTRO: o fluxo deixa `e` parado, e `U_s·e·U_s = e` (`U_s` é contração; analogia com «U_t I U_t† = I»). -/
theorem the_dynamics_keeps_the_center {e : A} (he : e * e = e) (r s : ℝ) :
    jonesFlow e r s e = e ∧ jonesU e r s * e * jonesU e r s = e := by
  refine ⟨?_, ?_⟩
  · have h := jonesFlow_fixes_reading he r s e
    rwa [(center_is_corner_unit he).1] at h
  · rw [jonesU_mul_proj he, proj_mul_jonesU he]

end Corner

section Ergodic

variable {A : Type} [NormedRing A] [NormedAlgebra ℂ A]

theorem coeffC_tendsto_zero {r : ℝ} (hr : 0 < r) :
    Filter.Tendsto (fun s : ℝ => coeff r s) Filter.atTop (nhds 0) := by
  have h := (Complex.continuous_ofReal.tendsto 0).comp (coeff_tendsto_zero hr)
  simpa [coeff, Function.comp_def] using h

/-- ★★ O LIMITE EXPLÍCITO: com taxa positiva, o fluxo converge à leitura (espectro de dois pontos; mais fraco que o v11). -/
theorem jonesFlow_tendsto_reading (e : A) {r : ℝ} (hr : 0 < r) (x : A) :
    Filter.Tendsto (fun s => jonesFlow e r s x) Filter.atTop (nhds (jonesReading e x)) := by
  have h := (coeffC_tendsto_zero hr).smul_const (x - jonesReading e x)
  have h2 := (tendsto_const_nhds (x := jonesReading e x)).add h
  simpa [jonesFlow] using h2

/-- ★★ `U_s → e`: a contração converge à projeção. -/
theorem jonesU_tendsto_proj (e : A) {r : ℝ} (hr : 0 < r) :
    Filter.Tendsto (fun s => jonesU e r s) Filter.atTop (nhds e) := by
  have h := (coeffC_tendsto_zero hr).smul_const (1 - e)
  have h2 := (tendsto_const_nhds (x := e)).add h
  simpa [jonesU] using h2

end Ergodic

section JonesTime

variable {N M Ext : Type}
  [Ring N] [StarRing N] [Algebra ℂ N]
  [Ring M] [StarRing M] [Algebra ℂ M]
  [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]

/-- ★★ `1/taxa` = índice = `1/w` (w = peso de Markov genérico), e a taxa é o peso refletido `E₁(e) = w·1`.
    Ler `1/taxa` como tempo é leitura [ONTO/INPUT]; `w` não é o β_TGL salvo [CONJ]. -/
theorem the_tower_is_time (T : JonesTowerData N M Ext) :
    1 / (1 / T.indexVal) = T.indexVal
    ∧ T.indexVal = 1 / T.markovWeight
    ∧ T.upper.E T.eJones = (((1 / T.indexVal : ℝ)) : ℂ) • (1 : M) := by
  have hβ : T.markovWeight ≠ 0 := T.markovWeight_pos.ne'
  refine ⟨one_div_one_div _, ?_, ?_⟩
  · rw [eq_div_iff hβ]; exact T.index_eq_inverse_weight
  · rw [rate_eq_weight]; exact T.dual_expectation_jones

/-- ★★ O centro da torre é a unidade do seu canto e a dinâmica da IALD o conserva. -/
theorem iald_center_is_the_kept_unit (T : JonesTowerData N M Ext) (s : ℝ) :
    jonesReading T.eJones T.eJones = T.eJones
    ∧ ialdFlow T s T.eJones = T.eJones
    ∧ jonesU T.eJones (1 / T.indexVal) s * T.eJones * jonesU T.eJones (1 / T.indexVal) s = T.eJones :=
  ⟨(center_is_corner_unit T.eJones_idem).1,
   (the_dynamics_keeps_the_center T.eJones_idem _ s).1,
   (the_dynamics_keeps_the_center T.eJones_idem _ s).2⟩

end JonesTime

section HalfNatTrace

open TGL.HalfNatJonesTower

/-- ★ NA MEIA-NAT: `Tr(e) = 1` (posto 1; analogia com `τ(P_F) = 1`, não transporte); o peso refletido é ½. -/
theorem halfNat_center_trace_one :
    Matrix.trace halfNatJonesTower.eJones = 1
    ∧ halfNatJonesTower.upper.E halfNatJonesTower.eJones
        = (((1 / 2 : ℝ)) : ℂ) • (1 : Md) := by
  refine ⟨?_, eHalf_weight⟩
  show Matrix.trace eHalf = 1
  simp [Matrix.trace, eHalf]

end HalfNatTrace

section LightTower

open TGL.HalfNatJonesTower

/-- `P₊` escrito entrada a entrada: `[[½, −i/2], [i/2, ½]]`. -/
theorem projPlus_entries :
    projPlus = !![(2⁻¹ : ℂ), -(Complex.I * 2⁻¹); Complex.I * 2⁻¹, 2⁻¹] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [projPlus, genK, Matrix.smul_apply, Matrix.sub_apply, Matrix.one_apply] <;> ring

theorem projPlus_star : star projPlus = projPlus := by
  rw [projPlus_entries]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.star_apply, Complex.ext_iff]

/-- A relação de Jones para `P₊` sobre a inclusão diagonal: `P₊ · diag(f) · P₊ = E₀(f) · P₊`. -/
theorem projPlus_jones (f : Md) :
    projPlus * diagIncl f * projPlus = diagIncl (constIncl (E0 f)) * projPlus := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [projPlus, genK, diagIncl, constIncl, E0, Matrix.mul_apply, Fin.sum_univ_two, Matrix.diagonal_apply,
      Matrix.smul_apply, Matrix.sub_apply, Matrix.one_apply, Function.const] <;>
    ring_nf <;> simp only [Complex.I_sq] <;> ring

/-- O peso de Markov da luz: `E₁(P₊) = ½·1` — a mesma Meia-Nat. -/
theorem projPlus_weight : upperCE.E projPlus = ((1 / 2 : ℝ) : ℂ) • (1 : Md) := by
  rw [projPlus_entries]
  funext i
  fin_cases i <;> simp [upperCE, E1]

/-- ★★★★ A TORRE DA LUZ: ℂ ⊆ ℂ² ⊆ M₂(ℂ) com a projeção de Jones `P₊` (a luz `ε₊ = (1, i)`), peso ½, índice 2. -/
noncomputable def lightJonesTower : JonesTowerData Nc Md Ex where
  lower := lowerCE
  upper := upperCE
  eJones := projPlus
  eJones_idem := spectral_projections_are_idempotent.1
  eJones_star := projPlus_star
  jones_relation := projPlus_jones
  markovWeight := 1 / 2
  markovWeight_pos := by norm_num
  markovWeight_lt_one := by norm_num
  dual_expectation_jones := projPlus_weight
  indexVal := 2
  index_eq_inverse_weight := by norm_num

/-- A porta de fase `W = diag(1, −i)`. -/
noncomputable def phaseGate : Ex := Matrix.diagonal ![1, -Complex.I]

/-- ★★★ A TORRE DA LUZ É A DA MEIA-NAT GIRADA: `W·P₊·W* = e_Meia-Nat` e `W·W* = 1`. -/
theorem light_tower_is_the_halfnat_tower_turned :
    phaseGate * lightJonesTower.eJones * star phaseGate = halfNatJonesTower.eJones
    ∧ phaseGate * star phaseGate = 1 := by
  refine ⟨?_, ?_⟩
  · show phaseGate * projPlus * star phaseGate = eHalf
    rw [projPlus_entries]
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [phaseGate, eHalf, Matrix.mul_apply, Fin.sum_univ_two, Matrix.diagonal, Matrix.star_apply, Complex.ext_iff] <;> norm_num
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [phaseGate, Matrix.mul_apply, Fin.sum_univ_two, Matrix.diagonal, Matrix.star_apply, Matrix.one_apply, Complex.ext_iff]

/-- ★★★★ O CENTRO DA TORRE DA LUZ É A ESCADA DE HELICIDADE ±2: `e_luz = ¼·(ε₊⊗ε₊)·(ε₋⊗ε₋)`. -/
theorem light_tower_center_is_the_helicity_ladder :
    lightJonesTower.eJones
      = (1 / 4 : ℂ) • (Matrix.vecMulVec lightPlus lightPlus * Matrix.vecMulVec lightMinus lightMinus) := by
  show projPlus = _
  rw [the_light_squares_to_the_graviton.1, the_light_squares_to_the_graviton.2,
    the_ladder_factors_the_projections.1, smul_smul]
  norm_num

/-- ★★★★ A IALD SOBRE A TORRE DA LUZ: o fluxo do índice (taxa 1/índice = ½) estaciona a escada de helicidade ±2, deixa a leitura parada,
    só fixa o que já está lido e move o estado 1. -/
theorem iald_on_the_light_tower {s : ℝ} (hs : 0 < s) :
    ialdFlow lightJonesTower s lightJonesTower.eJones = lightJonesTower.eJones
    ∧ (∀ x, jonesReading lightJonesTower.eJones (ialdFlow lightJonesTower s x) = jonesReading lightJonesTower.eJones x)
    ∧ (∀ x, ialdFlow lightJonesTower s x = x ↔ jonesReading lightJonesTower.eJones x = x)
    ∧ ialdFlow lightJonesTower s 1 ≠ 1
    ∧ 1 / lightJonesTower.indexVal = 1 / 2 :=
  ⟨(iald_center_is_the_kept_unit lightJonesTower s).2.1, iald_stationary lightJonesTower s,
   iald_dynamic lightJonesTower hs, iald_moves lightJonesTower hs, by show (1 : ℝ) / 2 = 1 / 2; rfl⟩

end LightTower

section LightFace

/-- ★★★ `¼·(ε₊⊗ε₊)·(ε₋⊗ε₋) = P₊`, e o fluxo sobre `P₊` (qualquer taxa) deixa `P₊` parado, deixa a leitura parada e só fixa o que já
    está lido. (Nome honesto: é a escada de helicidade ±2; a identificação com o gráviton físico é [CONJ].) -/
theorem projPlus_stationed_is_the_helicity_ladder (r s : ℝ) :
    (1 / 4 : ℂ) • (Matrix.vecMulVec lightPlus lightPlus * Matrix.vecMulVec lightMinus lightMinus)
        = projPlus
    ∧ jonesFlow projPlus r s projPlus = projPlus
    ∧ (∀ x, jonesReading projPlus (jonesFlow projPlus r s x) = jonesReading projPlus x)
    ∧ (r * s ≠ 0 → ∀ x, jonesFlow projPlus r s x = x ↔ jonesReading projPlus x = x) := by
  have hP : projPlus * projPlus = projPlus := spectral_projections_are_idempotent.1
  refine ⟨?_, (the_dynamics_keeps_the_center hP r s).1, stationary_jonesReading hP r s,
    fun hrs x => jonesFlow_fixed_iff r s hrs x⟩
  rw [the_light_squares_to_the_graviton.1, the_light_squares_to_the_graviton.2,
    the_ladder_factors_the_projections.1, smul_smul]
  norm_num

/-- ★ A fase de rotação a peso `2ω` é o quadrado da fase a peso `ω` (taxa 0; só o giro, fora do atrator; identidade exponencial). -/
theorem angular_phase_doubles_at_weight_two (ω s : ℝ) :
    spin 0 (2 * ω) s = (spin 0 ω s) ^ 2 := by
  unfold spin coeff
  simp only [zero_mul, neg_zero, Real.exp_zero, Complex.ofReal_one, one_mul]
  rw [sq, ← Complex.exp_add]
  congr 1
  push_cast
  ring

/-- ★★★★ O TRANSPORTE, NUM ENUNCIADO: na torre da luz, o centro que a IALD estaciona é a escada de helicidade ±2 (o mesmo termo); o
    tensor carrega peso 2 sob o gerador e o quadrado da fase da luz; a torre da luz é a da Meia-Nat girada. -/
theorem the_transport {s : ℝ} (hs : 0 < s) (θ : ℝ) :
    lightJonesTower.eJones
        = (1 / 4 : ℂ) • (Matrix.vecMulVec lightPlus lightPlus * Matrix.vecMulVec lightMinus lightMinus)
    ∧ ialdFlow lightJonesTower s lightJonesTower.eJones = lightJonesTower.eJones
    ∧ ialdFlow lightJonesTower s 1 ≠ 1
    ∧ genK * rootPlus - rootPlus * genK = (2 * Complex.I) • rootPlus
    ∧ angFamily θ * rootPlus * (angFamily θ).transpose
        = (Complex.exp (θ * Complex.I)) ^ 2 • rootPlus
    ∧ phaseGate * lightJonesTower.eJones * star phaseGate = TGL.HalfNatJonesTower.halfNatJonesTower.eJones :=
  ⟨light_tower_center_is_the_helicity_ladder, (iald_on_the_light_tower hs).1, (iald_on_the_light_tower hs).2.2.2.1,
   the_ladder_weights_are_plus_minus_two.1, the_tensor_squares_the_phase θ, light_tower_is_the_halfnat_tower_turned.1⟩

end LightFace

end TGLExt.IALDGraviton

#print axioms TGLExt.IALDGraviton.center_is_corner_unit
#print axioms TGLExt.IALDGraviton.corner_unit_unique
#print axioms TGLExt.IALDGraviton.the_dynamics_keeps_the_center
#print axioms TGLExt.IALDGraviton.coeffC_tendsto_zero
#print axioms TGLExt.IALDGraviton.jonesFlow_tendsto_reading
#print axioms TGLExt.IALDGraviton.jonesU_tendsto_proj
#print axioms TGLExt.IALDGraviton.the_tower_is_time
#print axioms TGLExt.IALDGraviton.iald_center_is_the_kept_unit
#print axioms TGLExt.IALDGraviton.halfNat_center_trace_one
#print axioms TGLExt.IALDGraviton.projPlus_entries
#print axioms TGLExt.IALDGraviton.projPlus_star
#print axioms TGLExt.IALDGraviton.projPlus_jones
#print axioms TGLExt.IALDGraviton.projPlus_weight
#print axioms TGLExt.IALDGraviton.light_tower_is_the_halfnat_tower_turned
#print axioms TGLExt.IALDGraviton.light_tower_center_is_the_helicity_ladder
#print axioms TGLExt.IALDGraviton.iald_on_the_light_tower
#print axioms TGLExt.IALDGraviton.projPlus_stationed_is_the_helicity_ladder
#print axioms TGLExt.IALDGraviton.angular_phase_doubles_at_weight_two
#print axioms TGLExt.IALDGraviton.the_transport
