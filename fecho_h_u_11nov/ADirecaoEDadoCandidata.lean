import TGLExt.PlaneWaveMatter
import TGLExt.TracialDissipativeTorsion
import TGLExt.TheVerbalCoupling

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

/-!
# A DIREÇÃO É DADO (candidata; fiação de conta elementar)
  [gerência c1, 11/11/2026 — candidata fora do kernel; nomes provisórios; nada aqui move gate ou bandeira]

O QUE É. A torção tracial do kernel (`TGLExt.TracialTorsion`) na métrica PLANA, com o vetor da torção
tratado como DADO: um covetor A qualquer, CONSTANTE em x, e não a direção de uma onda escolhida. A
métrica é plana; a conexão com torção NÃO é (tem curvatura). Três blocos:
* para todo dado A, na geometria em coordenadas do kernel: Ricci = 2·(A⊗A − N·eta4), escalar = −6·N e
  Einstein = 2·A⊗A + N·eta4, com N = A·A o tamanho do dado; o termo proporcional à métrica some se, e
  só se, N = 0 (dado nulo, inclusive o dado zero). O conteúdo está em T5; T6 só lê uma entrada de eta4;
* sem referente: escrito como amplitude vezes direção, um covetor tem todas as amplitudes positivas, e
  só elas. (R2, revisão de terceiro) Essa folga é de QUALQUER direção, não só da luz. O que distingue a
  luz é que ela não tem tamanho próprio (N = 0 para toda reescala): quando a direção tem tamanho 1, a
  métrica fixa a amplitude a menos do sinal (mu² = N); ao longo da onda não fixa. Com um referente n
  que normaliza a direção (w·n = 1), a amplitude é uma só, A·n: é álgebra linear de uma linha, a
  amplitude é RELATIVA ao n escolhido, e n é dado de fora, não derivado aqui (trocar n troca a
  amplitude);
* observador: reescalar a direção por s leva a amplitude a lam/s e a escala a s·ell; o produto fica.
  (R2) É identidade de corpo: com a amplitude da Ponte, thetaMiguel β / (3·ell), o produto é
  thetaMiguel β / 3 por DEFINIÇÃO da amplitude. Nenhum teorema liga a escala da direção ao ell da
  Ponte, e a palavra fase não é definida neste arquivo.

ANALOGIAS NO KERNEL (R2: analogias de forma, não espelhos; nenhuma é usada nas provas, e não há lema
que as ligue a este arquivo): `invariance_does_not_fix_area` (lote 045: sob as hipóteses de lá, a
covariância sozinha não seleciona um valor comum de área; o teorema exibe a escala 2, e a família de
todas as escalas positivas vem de `form_invariant_scale` e `scaled_form_areas_distinct`);
`the_unit_is_the_axiom` (v334: o traço 1 no par fixa a forma e a área ½); `the_word_fixes_the_place`
(v334) e `the_bireference_of_the_name` (v292), em que referente é a leitura que separa: aqui referente
é só um vetor n com w·n = 1 (homônimo; não encadear); `the_angle_reaches_the_metric` (reescreve β como
sen²θ_M no fator de entropia de FLRW; aqui o ângulo entra linear, pela amplitude).

O QUE NÃO É.
* Não trata os infinitos da teoria de campos nem renormalização: é álgebra elementar deste exemplo.
  T8 a T10 são álgebra de corpo e linear; o que contam é o que é dado e o que é referente, não prova nova.
* Não é o teorema de área (que não é torção: usa conexão simétrica e área métrica).
* Não define o Hamiltoniano oculto: o dado é um covetor A (ou um vetor n) qualquer.
* Não deriva o tamanho do dado nem o liga a β; o valor de thetaMiguel β só aparece como o produto
  preservado, por definição da amplitude da Ponte.
* (R2) Não prova a compatibilidade métrica da conexão (vem de `contortion_metric_compatible` do kernel);
  que `eta4` é a própria inversa está em `eta4_mul_self` (`PoincareGroup.lean`), citado e não usado.
* Não é `NamedAtlasH3` nem deriva a seta `hH3`. NOT_FALSIFIED nunca é CONFIRMED. β nunca literal.

COPIADO de `TorcaoNaOndaPlanaCandidata.lean` (candidatas não são importáveis): o preâmbulo (imports,
opções, linha `open`; o import de `PlaneWaveMatter` vem do molde, e aqui bastaria o da solda da onda),
o auxiliar `eta4_simetrica`, `nTemporal` e o molde das provas do controle temporal (o jato nulo de uma
conexão constante, o Ricci, o escalar e o Einstein), generalizados de `alfa • nTemporal` para um covetor
A qualquer.
-/

namespace TGLExt.DirecaoDadoCandidata

open Filter Topology Matrix Set TGLExt ChatgptAudit ChatgptAudit.Coherent023 ChatgptAudit.Response028
  ChatgptAudit.Wave029

noncomputable section

/-! ## D1, D2 — a conexão e o tamanho do dado -/

/-- A métrica de Minkowski do kernel é simétrica (auxiliar; copiado do molde). -/
theorem eta4_simetrica (i j : Fin 4) : eta4 i j = eta4 j i := by
  fin_cases i <;> fin_cases j <;>
    norm_num [eta4, Matrix.diagonal_apply, Matrix.cons_val_two, Matrix.cons_val_three,
      Fin.isValue]

/-- [candidata] D1. A conexão com a torção tracial ao longo de um DADO A (covetor qualquer, constante),
    sobre a métrica plana: `Gamma x i r j` é Γ^r_{ij} (i é a direção da derivada),
    `Γ^r_{ij} = δ^r_i A_j − eta4 i j · A^r` com `A^r = ∑ d, eta4 r d · A d`. É constante em x.
    (R2) A métrica é plana; esta conexão não é: tem curvatura (T3). -/
def conexaoDoDadoNaMetricaPlana (A : Coordinate4) : ConnectionField4 :=
  fun _ i r j => TGLExt.TracialTorsion.kd r i * A j - eta4 i j * (∑ d, eta4 r d * A d)

/-- [candidata] D2. O tamanho do dado: `N = A·A = tensorQuad eta4 A`. -/
def tamanhoDoDado (A : Coordinate4) : ℝ := tensorQuad eta4 A

/-! ## T0, T1, T2 — a fiação com `TGLExt.TracialTorsion` -/

/-- [candidata] T0. A conexão do dado é, ponto a ponto, a contorção `Kmix` do kernel
    (`TGLExt.TracialTorsion`) aplicada à métrica `eta4` e à sua inversa (que é a própria `eta4`:
    `eta4_mul_self`, no kernel; citado, não usado). -/
theorem a_conexao_do_dado_e_a_contorcao_do_kernel (A : Coordinate4) (x : Coordinate4) (i r j : Fin 4) :
    conexaoDoDadoNaMetricaPlana A x i r j =
      TGLExt.TracialTorsion.Kmix (fun p q => eta4 p q) (fun p q => eta4 p q) A r i j := by
  unfold conexaoDoDadoNaMetricaPlana TGLExt.TracialTorsion.Kmix TGLExt.TracialTorsion.raise
  rfl

/-- [candidata] T1. A torção da conexão do dado é a torção tracial do kernel:
    `Γ^r_{ij} − Γ^r_{ji} = T^r_{ij}`. -/
theorem a_torcao_do_dado_e_a_tracial (A : Coordinate4) (x : Coordinate4) (i r j : Fin 4) :
    conexaoDoDadoNaMetricaPlana A x i r j - conexaoDoDadoNaMetricaPlana A x j r i =
      TGLExt.TracialTorsion.torsion A r i j := by
  unfold conexaoDoDadoNaMetricaPlana TGLExt.TracialTorsion.torsion
  rw [eta4_simetrica i j]
  ring

/-- [candidata] T2. O tamanho do dado é a norma do kernel (`TGLExt.TracialTorsion.normSq`) com a métrica
    inversa `eta4`. -/
theorem o_tamanho_do_dado_e_a_norma_do_kernel (A : Coordinate4) :
    tamanhoDoDado A = TGLExt.TracialTorsion.normSq (fun p q => eta4 p q) A := by
  unfold tamanhoDoDado tensorQuad TGLExt.TracialTorsion.normSq TGLExt.TracialTorsion.raise
  simp [dotProduct, Matrix.mulVec, mul_comm]

/-- [candidata] T2, em componentes: `N = A0² − A1² − A2² − A3²`. -/
theorem o_tamanho_do_dado_em_componentes (A : Coordinate4) :
    tamanhoDoDado A = A 0 ^ 2 - A 1 ^ 2 - A 2 ^ 2 - A 3 ^ 2 := by
  unfold tamanhoDoDado tensorQuad
  norm_num [dotProduct, Matrix.mulVec, Fin.sum_univ_four, eta4, Matrix.diagonal_apply,
    Matrix.cons_val_two, Matrix.cons_val_three, Fin.isValue]
  ring

/-- [candidata] (R2) O tamanho é QUADRÁTICO na amplitude: `N(c • v) = c² · N(v)`. -/
theorem o_tamanho_e_homogeneo (c : ℝ) (v : Coordinate4) :
    tamanhoDoDado (c • v) = c ^ 2 * tamanhoDoDado v := by
  rw [o_tamanho_do_dado_em_componentes, o_tamanho_do_dado_em_componentes]
  simp only [Pi.smul_apply, smul_eq_mul]
  ring

/-! ## T3, T4, T5, T6 — o Ricci, o escalar e o Einstein do dado -/

/-- Uma conexão constante tem jato nulo (copiado do molde, para o dado). -/
theorem o_jato_da_conexao_do_dado (A : Coordinate4) (x : Coordinate4) (k i : Fin 4) :
    connectionFirstJet (conexaoDoDadoNaMetricaPlana A) x k i = 0 := by
  ext r j
  simp [connectionFirstJet, tensorFieldJet, coordinatePartial, conexaoDoDadoNaMetricaPlana]

/-- [candidata] T3 ★. O Ricci do dado: `2·(A⊗A − N·eta4)`. -/
theorem o_ricci_do_dado (A : Coordinate4) (x : Coordinate4) :
    coordinateRicci (conexaoDoDadoNaMetricaPlana A) x =
      (2 : ℝ) • (Matrix.vecMulVec A A - tamanhoDoDado A • eta4) := by
  obtain ⟨a0, a1, a2, a3, rfl⟩ : ∃ a0 a1 a2 a3 : ℝ, A = ![a0, a1, a2, a3] :=
    ⟨A 0, A 1, A 2, A 3, by ext i; fin_cases i <;> rfl⟩
  rw [o_tamanho_do_dado_em_componentes]
  ext b j
  simp only [coordinateRicci, coordinateCurvature, connectionCurvatureJet, Matrix.sub_apply,
    Matrix.add_apply, Matrix.mul_apply, Fin.sum_univ_four, o_jato_da_conexao_do_dado,
    Matrix.zero_apply]
  fin_cases b <;> fin_cases j <;>
    norm_num [conexaoDoDadoNaMetricaPlana, eta4, TGLExt.TracialTorsion.kd, Matrix.vecMulVec,
      Matrix.cons_val_two, Matrix.cons_val_three, Matrix.diagonal_apply, Fin.isValue] <;>
    norm_num [Fin.ext_iff] <;> ring

/-- [candidata] T4. O escalar do dado: `−6·N`. -/
theorem o_escalar_do_dado (A : Coordinate4) (x : Coordinate4) :
    coordinateScalarCurvature (fun _ => eta4) (conexaoDoDadoNaMetricaPlana A) x =
      -6 * tamanhoDoDado A := by
  rw [o_tamanho_do_dado_em_componentes]
  simp only [coordinateScalarCurvature, o_ricci_do_dado, o_tamanho_do_dado_em_componentes]
  norm_num [Fin.sum_univ_four, eta4, Matrix.vecMulVec, Matrix.cons_val_two,
    Matrix.cons_val_three, Matrix.diagonal_apply, Fin.isValue]
  ring

/-- [candidata] T5 ★★. O Einstein do dado em métrica plana: `2·A⊗A + N·eta4`. -/
theorem o_einstein_do_dado (A : Coordinate4) (x : Coordinate4) :
    geometricEinsteinTensor (fun _ => eta4) (fun _ => eta4) (conexaoDoDadoNaMetricaPlana A) x =
      (2 : ℝ) • Matrix.vecMulVec A A + tamanhoDoDado A • eta4 := by
  unfold geometricEinsteinTensor
  rw [o_escalar_do_dado, o_ricci_do_dado]
  ext b j
  simp only [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply, smul_eq_mul]
  ring

/-- [candidata] T6 ★★. O termo proporcional à métrica some se, e só se, `N = 0` (dado nulo, inclusive o
    dado zero): o Einstein do dado é `2·A⊗A` exatamente quando `tamanhoDoDado A = 0`.
    (R2) O conteúdo é T5; aqui só se lê a entrada (0,0) de `eta4`. -/
theorem o_termo_da_metrica_some_sse_o_dado_e_luz (A : Coordinate4) (x : Coordinate4) :
    geometricEinsteinTensor (fun _ => eta4) (fun _ => eta4) (conexaoDoDadoNaMetricaPlana A) x =
        (2 : ℝ) • Matrix.vecMulVec A A ↔ tamanhoDoDado A = 0 := by
  rw [o_einstein_do_dado]
  constructor
  · intro h
    have hh := congrArg (fun M : Tensor4 => M 0 0) h
    simpa [eta4] using hh
  · intro h
    rw [h]
    simp

/-! ## T7 — os casos: ao longo da onda e ao longo do tempo -/

/-- O covetor temporal `n = (1, 0, 0, 0)` (copiado do molde). -/
def nTemporal : Coordinate4 := ![1, 0, 0, 0]

/-- [candidata] T7. O dado ao longo da onda é luz (`N = 0`) e o Einstein é `2·lam²·w⊗w`. -/
theorem o_dado_ao_longo_da_onda (lam : ℝ) (x : Coordinate4) :
    tamanhoDoDado (lam • waveCovector) = 0 ∧
    geometricEinsteinTensor (fun _ => eta4) (fun _ => eta4)
      (conexaoDoDadoNaMetricaPlana (lam • waveCovector)) x =
        (2 * lam ^ 2) • Matrix.vecMulVec waveCovector waveCovector := by
  have hN : tamanhoDoDado (lam • waveCovector) = 0 := by
    rw [o_tamanho_do_dado_em_componentes]
    norm_num [waveCovector, Matrix.cons_val_two, Matrix.cons_val_three, Fin.isValue]
  refine ⟨hN, ?_⟩
  rw [o_einstein_do_dado, hN]
  ext b j
  simp only [Matrix.add_apply, Matrix.smul_apply, Matrix.vecMulVec_apply, Pi.smul_apply, smul_eq_mul,
    zero_mul, add_zero]
  ring

/-- [candidata] T7 (controle). O dado ao longo do tempo tem `N = alfa²` e o Einstein é
    `2·alfa²·n⊗n + alfa²·eta4`: aparece o termo proporcional à métrica. -/
theorem o_dado_ao_longo_do_tempo (alfa : ℝ) (x : Coordinate4) :
    tamanhoDoDado (alfa • nTemporal) = alfa ^ 2 ∧
    geometricEinsteinTensor (fun _ => eta4) (fun _ => eta4)
      (conexaoDoDadoNaMetricaPlana (alfa • nTemporal)) x =
        (2 * alfa ^ 2) • Matrix.vecMulVec nTemporal nTemporal + alfa ^ 2 • eta4 := by
  have hN : tamanhoDoDado (alfa • nTemporal) = alfa ^ 2 := by
    rw [o_tamanho_do_dado_em_componentes]
    norm_num [nTemporal, Matrix.cons_val_two, Matrix.cons_val_three, Fin.isValue]
  refine ⟨hN, ?_⟩
  rw [o_einstein_do_dado, hN]
  ext b j
  simp only [Matrix.add_apply, Matrix.smul_apply, Matrix.vecMulVec_apply, Pi.smul_apply, smul_eq_mul]
  ring

/-! ## T8 — sem referente, toda amplitude positiva serve -/

/-- [candidata] T8. Sem referente: para qualquer amplitude positiva `mu` existe uma escala positiva `s`
    tal que `mu • (s • w) = lam • w`: o MESMO covetor ao longo da onda tem todas as amplitudes.
    (R2) A prova não usa que a direção é nula: vale para qualquer vetor no lugar de `waveCovector`. O
    que é próprio da luz está em `a_luz_nao_tem_tamanho_proprio`, mais abaixo. -/
theorem sem_referente_toda_amplitude_positiva_serve (lam mu : ℝ) (hlam : 0 < lam) (hmu : 0 < mu) :
    ∃ s : ℝ, 0 < s ∧ mu • (s • waveCovector) = lam • waveCovector := by
  refine ⟨lam / mu, div_pos hlam hmu, ?_⟩
  rw [smul_smul]
  congr 1
  field_simp

/-- [candidata] T8. Sem referente, o conjunto das amplitudes não é limitado superiormente. -/
theorem as_amplitudes_sem_referente_nao_sao_limitadas (lam : ℝ) (hlam : 0 < lam) :
    ¬ BddAbove {mu : ℝ | ∃ s : ℝ, 0 < s ∧ mu • (s • waveCovector) = lam • waveCovector} := by
  rintro ⟨M, hM⟩
  have hpos : 0 < max M 0 + 1 := by
    have := le_max_right M 0
    linarith
  have hmem : max M 0 + 1 ∈
      {mu : ℝ | ∃ s : ℝ, 0 < s ∧ mu • (s • waveCovector) = lam • waveCovector} :=
    sem_referente_toda_amplitude_positiva_serve lam _ hlam hpos
  have hle := hM hmem
  have := le_max_left M 0
  linarith

/-- [candidata] T8. Sem referente, as amplitudes chegam perto de zero. -/
theorem as_amplitudes_sem_referente_chegam_perto_de_zero (lam : ℝ) (hlam : 0 < lam) :
    ∀ eps > 0, ∃ mu : ℝ, 0 < mu ∧ mu < eps ∧
      ∃ s : ℝ, 0 < s ∧ mu • (s • waveCovector) = lam • waveCovector := by
  intro eps heps
  have hmu : 0 < eps / 2 := by positivity
  exact ⟨eps / 2, hmu, by linarith, sem_referente_toda_amplitude_positiva_serve lam _ hlam hmu⟩

/-- [candidata] (R2) O conjunto das amplitudes sem referente é EXATAMENTE o dos reais positivos. -/
theorem as_amplitudes_sem_referente_sao_os_positivos (lam : ℝ) (hlam : 0 < lam) :
    {mu : ℝ | ∃ s : ℝ, 0 < s ∧ mu • (s • waveCovector) = lam • waveCovector} = Set.Ioi 0 := by
  ext mu
  simp only [Set.mem_setOf_eq, Set.mem_Ioi]
  constructor
  · rintro ⟨s, hs, h⟩
    have h0 := congrFun h 0
    have hw : waveCovector 0 = 1 := by simp [waveCovector]
    simp only [Pi.smul_apply, smul_eq_mul, hw, mul_one] at h0
    by_contra hmu
    have hmu' : mu ≤ 0 := not_lt.mp hmu
    nlinarith [mul_nonneg (neg_nonneg.mpr hmu') hs.le]
  · intro hmu
    exact sem_referente_toda_amplitude_positiva_serve lam mu hlam hmu

/-! ## T8b (R2) — o que é próprio da luz: ela não tem tamanho próprio -/

/-- [candidata] (R2) Quando a direção tem tamanho próprio (`N(v) = 1`), a MÉTRICA fixa a amplitude a
    menos do sinal: `mu • v = A` implica `mu² = N(A)`. Não é preciso referente de fora. -/
theorem a_metrica_fixa_a_amplitude_se_nao_e_luz (v A : Coordinate4) (mu : ℝ)
    (hv : tamanhoDoDado v = 1) (h : mu • v = A) : mu ^ 2 = tamanhoDoDado A := by
  rw [← h, o_tamanho_e_homogeneo, hv, mul_one]

/-- [candidata] (R2) A luz não tem tamanho próprio: toda reescala do covetor da onda tem `N = 0`; logo
    nenhuma reescala dele tem tamanho 1, e a métrica não fixa a amplitude ao longo da onda. -/
theorem a_luz_nao_tem_tamanho_proprio (s : ℝ) :
    tamanhoDoDado (s • waveCovector) = 0 ∧ tamanhoDoDado (s • waveCovector) ≠ 1 := by
  have h0 : tamanhoDoDado (s • waveCovector) = 0 := by
    rw [o_tamanho_do_dado_em_componentes]
    norm_num [waveCovector, Matrix.cons_val_two, Matrix.cons_val_three, Fin.isValue]
  exact ⟨h0, by rw [h0]; norm_num⟩

/-! ## T9 — com o referente, a amplitude é uma só -/

/-- [candidata] T9. Com um referente `n` que normaliza a direção (`w'·n = 1`), a amplitude é única:
    `mu • w' = A` implica `mu = A·n`. (R2) Álgebra linear de uma linha; a amplitude é relativa ao `n`
    escolhido. -/
theorem com_o_referente_a_amplitude_e_uma_so (n w' A : Coordinate4) (mu : ℝ)
    (hn : w' ⬝ᵥ n = 1) (h : mu • w' = A) : mu = A ⬝ᵥ n := by
  rw [← h, smul_dotProduct, hn, smul_eq_mul, mul_one]

/-- [candidata] T9. Com o referente, a amplitude existe quando `A·n ≠ 0`: há `w'` com `w'·n = 1` e
    `(A·n) • w' = A`. (R2) Todo `n` com `A·n ≠ 0` serve, e a amplitude muda com `n`: a folga passou de
    `s` para `n`, e `n` é dado de fora, não derivado aqui. -/
theorem com_o_referente_a_amplitude_existe (n A : Coordinate4) (hA : A ⬝ᵥ n ≠ 0) :
    ∃ w' : Coordinate4, w' ⬝ᵥ n = 1 ∧ (A ⬝ᵥ n) • w' = A := by
  refine ⟨(A ⬝ᵥ n)⁻¹ • A, ?_, ?_⟩
  · rw [smul_dotProduct, smul_eq_mul, inv_mul_cancel₀ hA]
  · rw [smul_smul, mul_inv_cancel₀ hA, one_smul]

/-! ## T10 — o observador: amplitude e escala mudam juntas -/

/-- [candidata] T10. Reescalar a direção por `s ≠ 0` leva a amplitude a `lam/s` e a escala a `s·ell`:
    o produto fica, e o covetor fica. (R2) Identidade de corpo. -/
theorem amplitude_e_escala_mudam_juntas (lam s ell : ℝ) (hs : s ≠ 0) :
    (lam / s) * (s * ell) = lam * ell ∧ (lam / s) • (s • waveCovector) = lam • waveCovector := by
  refine ⟨?_, ?_⟩
  · field_simp
  · rw [smul_smul, div_mul_cancel₀ _ hs]

/-- [candidata] T10. Com a amplitude da Ponte `thetaMiguel β / (3·ell)`, o produto da amplitude pela
    escala reescalada é `thetaMiguel β / 3`, e a amplitude reescalada é a de `ell` dividida por `s`.
    (R2) É identidade de corpo e vale por DEFINIÇÃO da amplitude; o valor de `thetaMiguel β` não é
    usado; nenhum teorema liga a escala da direção ao `ell` da Ponte. O nome antigo dizia fase e ângulo,
    mais do que o tipo prova, e foi trocado. -/
theorem o_produto_amplitude_escala_e_theta_sobre_tres (β s ell : ℝ) (hs : s ≠ 0) (hell : ell ≠ 0) :
    thetaMiguel β / (3 * (s * ell)) * (s * ell) = thetaMiguel β / 3 ∧
    thetaMiguel β / (3 * (s * ell)) = thetaMiguel β / (3 * ell) / s := by
  refine ⟨?_, ?_⟩
  · field_simp
  · field_simp

end

end TGLExt.DirecaoDadoCandidata

open TGLExt.DirecaoDadoCandidata in
#print axioms eta4_simetrica
open TGLExt.DirecaoDadoCandidata in
#print axioms conexaoDoDadoNaMetricaPlana
open TGLExt.DirecaoDadoCandidata in
#print axioms tamanhoDoDado
open TGLExt.DirecaoDadoCandidata in
#print axioms a_conexao_do_dado_e_a_contorcao_do_kernel
open TGLExt.DirecaoDadoCandidata in
#print axioms a_torcao_do_dado_e_a_tracial
open TGLExt.DirecaoDadoCandidata in
#print axioms o_tamanho_do_dado_e_a_norma_do_kernel
open TGLExt.DirecaoDadoCandidata in
#print axioms o_tamanho_do_dado_em_componentes
open TGLExt.DirecaoDadoCandidata in
#print axioms o_jato_da_conexao_do_dado
open TGLExt.DirecaoDadoCandidata in
#print axioms o_ricci_do_dado
open TGLExt.DirecaoDadoCandidata in
#print axioms o_escalar_do_dado
open TGLExt.DirecaoDadoCandidata in
#print axioms o_einstein_do_dado
open TGLExt.DirecaoDadoCandidata in
#print axioms o_termo_da_metrica_some_sse_o_dado_e_luz
open TGLExt.DirecaoDadoCandidata in
#print axioms nTemporal
open TGLExt.DirecaoDadoCandidata in
#print axioms o_dado_ao_longo_da_onda
open TGLExt.DirecaoDadoCandidata in
#print axioms o_dado_ao_longo_do_tempo
open TGLExt.DirecaoDadoCandidata in
#print axioms sem_referente_toda_amplitude_positiva_serve
open TGLExt.DirecaoDadoCandidata in
#print axioms as_amplitudes_sem_referente_nao_sao_limitadas
open TGLExt.DirecaoDadoCandidata in
#print axioms as_amplitudes_sem_referente_chegam_perto_de_zero
open TGLExt.DirecaoDadoCandidata in
#print axioms com_o_referente_a_amplitude_e_uma_so
open TGLExt.DirecaoDadoCandidata in
#print axioms com_o_referente_a_amplitude_existe
open TGLExt.DirecaoDadoCandidata in
#print axioms amplitude_e_escala_mudam_juntas
open TGLExt.DirecaoDadoCandidata in
#print axioms o_produto_amplitude_escala_e_theta_sobre_tres
open TGLExt.DirecaoDadoCandidata in
#print axioms o_tamanho_e_homogeneo
open TGLExt.DirecaoDadoCandidata in
#print axioms as_amplitudes_sem_referente_sao_os_positivos
open TGLExt.DirecaoDadoCandidata in
#print axioms a_metrica_fixa_a_amplitude_se_nao_e_luz
open TGLExt.DirecaoDadoCandidata in
#print axioms a_luz_nao_tem_tamanho_proprio
