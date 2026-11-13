import TGLExt.TracialDissipativeTorsion
import TGLExt.TheVerbalCoupling
import TGLExt.TheSameBetaReadsThreeFaces

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A NORMAL DA TELA DE LUZ (candidata; tipagem por definição)
  [gerência c1, 11/11/2026 — candidata fora do kernel; nomes provisórios; nada aqui move gate ou bandeira]

O QUE É. A tipagem, aprovada pelo operador em 11/11/2026, de uma cadeia de três elos:
* o traço da torção tracial do kernel em quatro dimensões é 3·A (`torsion_trace`, com n − 1 = 3);
* a FASE é DEFINIDA aqui como esse traço lido no referente e multiplicado pela escala do observador:
  `faseDaTorcao lam ell = 3·lam·ell`; `a_fase_e_o_traco_da_torcao_lido_no_referente` mostra que ela é
  o covetor do traço aplicado ao vetor `ell • n`, para qualquer referente n que normaliza a direção;
* com a amplitude da Ponte (thetaMiguel β / (3·ell)) a fase é thetaMiguel β; ela é a mesma para toda
  reescala s ≠ 0; para 0 ≤ β ≤ 1 o peso sen² dessa fase é β e o peso cos² é 1 − β.
(R2, revisão de terceiro) A ligação com o kernel fica provada: a matriz S do kernel (`Smat`) avaliada na
fase é a matriz S no ângulo de Miguel, e o peso sen² da fase é o peso REFLETIDO dela (`normSq_reflection`);
com o acoplamento do kernel (`TGLCoupling`) é o `reflection_weight` dele.

É VERDADEIRA POR DEFINIÇÃO. A fase vale thetaMiguel β porque a amplitude da Ponte é definida como
thetaMiguel β / (3·ell); e sen²(thetaMiguel β) = β porque thetaMiguel β é definido como arcsin √β
(`sin_thetaMiguel`, no kernel). Nada aqui deriva β, nem a amplitude, nem a escala. (R2) O 3 da amplitude
é o n − 1 do cabeçalho de `TracialDissipativeTorsion.lean`, que o kernel marca como entrada; ele cancela
com o 3 da definição da fase, e qualquer constante no lugar dele daria as mesmas identidades. O conteúdo
que vem do kernel é o traço (N1, N2) e a matriz S (N9 a N12); N3 a N8 são identidades depois da definição.

O QUE NÃO É.
* Não prova que o peso sen² da fase seja a normal geométrica de uma tela: as palavras normal, tela e luz
  ficam na fala do operador; nenhum objeto deste arquivo é tela, luz ou normal. O que o arquivo tipa é o
  peso da fase, que é o peso refletido da matriz S do kernel.
* (R2) Os nomes são provisórios e sóbrios de propósito: não tipam observador físico. O que aqui se chama
  reescala é só a dilatação s ≠ 0 (inclui s negativo), e a lei amplitude ↦ amplitude/s é POSTA (é a
  reescala da direção), não derivada.
* Não liga a escala do observador a nenhuma grandeza medida; não define o Hamiltoniano oculto.
* Não é o teorema de área, não é `NamedAtlasH3`, não deriva a seta `hH3`.
* NOT_FALSIFIED nunca é CONFIRMED. β nunca literal.
-/

namespace TGLExt.NormalDaTelaCandidata

open Matrix TGLExt

noncomputable section

/-! ## N1 — o traço da torção em quatro dimensões -/

/-- [candidata] N1. Em quatro dimensões o traço da torção tracial do kernel é `3·A` (é
    `TGLExt.TracialTorsion.torsion_trace` com `n − 1 = 3`). -/
theorem o_traco_da_torcao_em_quatro_dimensoes (A : Fin 4 → ℝ) (c : Fin 4) :
    ∑ a, TGLExt.TracialTorsion.torsion A a a c = 3 * A c := by
  rw [TGLExt.TracialTorsion.torsion_trace]
  simp only [Fintype.card_fin]
  norm_num

/-! ## N2 — a fase: o traço da torção lido no referente, vezes a escala do observador -/

/-- [candidata] N2 (DEFINIÇÃO). A fase da torção para a amplitude `lam` e a escala `ell`:
    `3·lam·ell`. O 3 é o `n − 1` do traço (N1), amarrado pelo lema seguinte. -/
def faseDaTorcao (lam ell : ℝ) : ℝ := 3 * lam * ell

/-- [candidata] N2. A fase é o covetor do traço da torção de `A = lam • w` aplicado ao vetor `ell • n`,
    para qualquer referente `n` que normaliza a direção (`w·n = 1`). (R2) Não pede direção nula; não
    mostra que `n` seja observador físico. -/
theorem a_fase_e_o_traco_da_torcao_lido_no_referente (lam ell : ℝ) (w n : Fin 4 → ℝ)
    (hn : w ⬝ᵥ n = 1) :
    (fun c => ∑ a, TGLExt.TracialTorsion.torsion (fun d => lam * w d) a a c) ⬝ᵥ (ell • n) =
      faseDaTorcao lam ell := by
  have h : (fun c => ∑ a, TGLExt.TracialTorsion.torsion (fun d => lam * w d) a a c) =
      (3 * lam) • w := by
    funext c
    rw [o_traco_da_torcao_em_quatro_dimensoes]
    simp only [Pi.smul_apply, smul_eq_mul]
    ring
  rw [h, smul_dotProduct, dotProduct_smul, hn]
  simp only [smul_eq_mul, faseDaTorcao]
  ring

/-! ## N3, N4 — com a amplitude da Ponte a fase é o ângulo, para toda reescala -/

/-- [candidata] N3. Com a amplitude da Ponte, `thetaMiguel β / (3·ell)`, a fase é `thetaMiguel β`.
    Vale por DEFINIÇÃO da amplitude. -/
theorem a_fase_com_a_amplitude_da_ponte (β ell : ℝ) (hell : ell ≠ 0) :
    faseDaTorcao (thetaMiguel β / (3 * ell)) ell = thetaMiguel β := by
  unfold faseDaTorcao
  field_simp

/-- [candidata] N4. A fase é a mesma para toda reescala: com `s ≠ 0`, a amplitude `lam/s` e a escala
    `s·ell` dão a mesma fase. Identidade de corpo; a lei da reescala é posta, não derivada. -/
theorem a_fase_e_a_mesma_para_toda_reescala (lam s ell : ℝ) (hs : s ≠ 0) :
    faseDaTorcao (lam / s) (s * ell) = faseDaTorcao lam ell := by
  unfold faseDaTorcao
  field_simp

/-! ## N5, N6, N7, N8 — o peso da fase (identidades depois da definição) -/

/-- [candidata] N5. O peso sen² da fase, com a amplitude da Ponte, é β. Vale por definição: a fase é
    `thetaMiguel β` (N3) e `sen(thetaMiguel β) = √β` (`sin_thetaMiguel`, no kernel).
    (R2) O TIPO é só `sen²(fase) = β`; não há tela, luz nem normal geométrica no enunciado. -/
theorem o_peso_da_fase_e_beta (β ell : ℝ) (h0 : 0 ≤ β) (h1 : β ≤ 1) (hell : ell ≠ 0) :
    Real.sin (faseDaTorcao (thetaMiguel β / (3 * ell)) ell) ^ 2 = β := by
  rw [a_fase_com_a_amplitude_da_ponte β ell hell, sin_thetaMiguel h0 h1, Real.sq_sqrt h0]

/-- [candidata] N6. O peso sen² da fase é β para TODA reescala: com a amplitude dividida por `s` e a
    escala multiplicada por `s`, o peso é o mesmo. -/
theorem o_peso_da_fase_e_beta_para_toda_reescala (β s ell : ℝ) (h0 : 0 ≤ β) (h1 : β ≤ 1)
    (hs : s ≠ 0) (hell : ell ≠ 0) :
    Real.sin (faseDaTorcao (thetaMiguel β / (3 * ell) / s) (s * ell)) ^ 2 = β := by
  rw [a_fase_e_a_mesma_para_toda_reescala _ s ell hs]
  exact o_peso_da_fase_e_beta β ell h0 h1 hell

/-- [candidata] N7. O peso cos² da mesma fase é `1 − β`. -/
theorem o_peso_complementar_da_fase_e_um_menos_beta (β ell : ℝ) (h0 : 0 ≤ β) (h1 : β ≤ 1)
    (hell : ell ≠ 0) :
    Real.cos (faseDaTorcao (thetaMiguel β / (3 * ell)) ell) ^ 2 = 1 - β := by
  have h := o_peso_da_fase_e_beta β ell h0 h1 hell
  have hsc := Real.sin_sq_add_cos_sq (faseDaTorcao (thetaMiguel β / (3 * ell)) ell)
  linarith

/-- [candidata] N8. Para `0 < β < 1` a fase é positiva e fica estritamente antes do ângulo reto. -/
theorem a_fase_fica_antes_do_angulo_reto (β ell : ℝ) (h0 : 0 < β) (h1 : β < 1) (hell : ell ≠ 0) :
    0 < faseDaTorcao (thetaMiguel β / (3 * ell)) ell ∧
      faseDaTorcao (thetaMiguel β / (3 * ell)) ell < Real.pi / 2 := by
  rw [a_fase_com_a_amplitude_da_ponte β ell hell]
  unfold thetaMiguel
  refine ⟨Real.arcsin_pos.mpr (Real.sqrt_pos.mpr h0), ?_⟩
  rw [Real.arcsin_lt_pi_div_two]
  calc Real.sqrt β < Real.sqrt 1 := Real.sqrt_lt_sqrt h0.le h1
    _ = 1 := Real.sqrt_one

/-! ## N9 a N12 (R2) — a ligação com a matriz S do kernel -/

/-- [candidata] (R2) N9. A matriz S do kernel avaliada na fase é a matriz S no ângulo de Miguel. -/
theorem a_matriz_s_na_fase_e_a_do_angulo_de_miguel (β ell : ℝ) (hell : ell ≠ 0) :
    Smat (faseDaTorcao (thetaMiguel β / (3 * ell)) ell) = Smat (thetaMiguel β) := by
  rw [a_fase_com_a_amplitude_da_ponte β ell hell]

/-- [candidata] (R2) N10. O peso sen² da fase é o peso REFLETIDO da matriz S do kernel
    (`normSq_reflection`): com a amplitude da Ponte, vale β. -/
theorem o_peso_da_fase_e_o_peso_refletido_da_matriz_s (β ell : ℝ) (h0 : 0 ≤ β) (h1 : β ≤ 1)
    (hell : ell ≠ 0) :
    Complex.normSq ((Smat (faseDaTorcao (thetaMiguel β / (3 * ell)) ell)).mulVec e1 1) = β := by
  rw [normSq_reflection]
  exact o_peso_da_fase_e_beta β ell h0 h1 hell

/-- [candidata] (R2) N11. O peso cos² da fase é o peso TRANSMITIDO da matriz S do kernel
    (`normSq_transmission`): com a amplitude da Ponte, vale `1 − β`. -/
theorem o_peso_complementar_e_o_peso_transmitido_da_matriz_s (β ell : ℝ) (h0 : 0 ≤ β) (h1 : β ≤ 1)
    (hell : ell ≠ 0) :
    Complex.normSq ((Smat (faseDaTorcao (thetaMiguel β / (3 * ell)) ell)).mulVec e1 0) = 1 - β := by
  rw [normSq_transmission]
  exact o_peso_complementar_da_fase_e_um_menos_beta β ell h0 h1 hell

/-- [candidata] (R2) N12. Com o acoplamento do kernel (`TGLCoupling`, o β único da casa), o peso refletido
    da matriz S na fase é `c.beta`, para toda reescala `s ≠ 0`: é o `reflection_weight` do kernel. -/
theorem o_peso_refletido_no_acoplamento_para_toda_reescala (c : TGLCoupling) (s ell : ℝ)
    (hs : s ≠ 0) (hell : ell ≠ 0) :
    Complex.normSq
      ((Smat (faseDaTorcao (thetaMiguel c.beta / (3 * ell) / s) (s * ell))).mulVec e1 1) = c.beta := by
  rw [a_fase_e_a_mesma_para_toda_reescala _ s ell hs, a_fase_com_a_amplitude_da_ponte c.beta ell hell]
  exact c.reflection_weight

end

end TGLExt.NormalDaTelaCandidata

open TGLExt.NormalDaTelaCandidata in
#print axioms o_traco_da_torcao_em_quatro_dimensoes
open TGLExt.NormalDaTelaCandidata in
#print axioms faseDaTorcao
open TGLExt.NormalDaTelaCandidata in
#print axioms a_fase_e_o_traco_da_torcao_lido_no_referente
open TGLExt.NormalDaTelaCandidata in
#print axioms a_fase_com_a_amplitude_da_ponte
open TGLExt.NormalDaTelaCandidata in
#print axioms a_fase_e_a_mesma_para_toda_reescala
open TGLExt.NormalDaTelaCandidata in
#print axioms o_peso_da_fase_e_beta
open TGLExt.NormalDaTelaCandidata in
#print axioms o_peso_da_fase_e_beta_para_toda_reescala
open TGLExt.NormalDaTelaCandidata in
#print axioms o_peso_complementar_da_fase_e_um_menos_beta
open TGLExt.NormalDaTelaCandidata in
#print axioms a_fase_fica_antes_do_angulo_reto
open TGLExt.NormalDaTelaCandidata in
#print axioms a_matriz_s_na_fase_e_a_do_angulo_de_miguel
open TGLExt.NormalDaTelaCandidata in
#print axioms o_peso_da_fase_e_o_peso_refletido_da_matriz_s
open TGLExt.NormalDaTelaCandidata in
#print axioms o_peso_complementar_e_o_peso_transmitido_da_matriz_s
open TGLExt.NormalDaTelaCandidata in
#print axioms o_peso_refletido_no_acoplamento_para_toda_reescala
