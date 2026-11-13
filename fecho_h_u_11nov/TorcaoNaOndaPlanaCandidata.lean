import TGLExt.PlaneWaveMatter
import TGLExt.TracialDissipativeTorsion
import TGLExt.TheVerbalCoupling

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

/-!
# A TORÇÃO NA ONDA PLANA (candidata; fiação)
  [gerência c1, 11/11/2026 — candidata fora do kernel; nomes provisórios; nada aqui move gate ou bandeira]

O QUE É. Fiação entre duas peças que o kernel já tem e não ligava:
* a torção tracial da Ponte Einstein–Cartan–Miguel (`TGLExt.TracialTorsion`; o um.py data a pedra da
  v364, de 17/09/2026: contorção K^a_{bc} = δ^a_b A_c − g_{bc} A^a), e
* a onda plana do lote 029 (`waveSolder a c`, métrica eta4 + H·w⊗w, conexão de Levi-Civita sem torção).
Aqui o vetor da torção é posto ao longo da própria onda, A = lam • waveCovector. Calcula-se, na geometria
em coordenadas do kernel (`coordinateRicci`, `geometricEinsteinTensor`), o Ricci, o escalar e o tensor de
Einstein da conexão com torção: (a + c + 2·lam²) • w⊗w. Logo a onda CHATA com torção tem o tensor de
Einstein da onda CURVA sem torção com a' + c' = 2·lam². Com a amplitude da Ponte,
lam = thetaMiguel β / (3·ell) (a alfa = θ_M/((n−1)ℓ) de `TracialDissipativeTorsion.lean`, em n = 4),
a soma dos perfis é 2·θ_M²/(9·ell²).

O QUE ENTRA POR DEFINIÇÃO (não é provado aqui).
* A forma da torção (tracial) e a sua amplitude θ_M/((n−1)ℓ): são a definição da Ponte.
* A DIREÇÃO do vetor da torção (ao longo da onda) é escolha deste arquivo. O controle da torção temporal
  mostra o que muda com a direção do tempo: aparece um termo proporcional a eta4.
* A escala ell fica como entrada; `a_escala_que_resta_e_unica` diz que, dados eta > 0, o acoplamento > 0
  e o ângulo > 0, existe exatamente uma.
* (R2, revisão de terceiro) O VALOR de `thetaMiguel β` não entra em nenhuma prova deste arquivo: só a
  positividade (de β > 0). Quando `ell` percorre os reais positivos, `thetaMiguel β / (3·ell)` cobre TODAS
  as amplitudes positivas; logo T6 é T5 com `lam` substituído, e T8 é a inversão elementar de `ell` (com
  `eta` e o acoplamento livres). Nada aqui liga `ell` a β.
* (R2) O vetor A é NULO e não tem norma invariante. Reescalar `waveCovector` por `s` (um boost ao longo da
  onda) leva `lam` a `lam/s`, o acoplamento a `acoplamento/s²` e `ell` a `s·ell`; só a relação entre eles
  é invariante. `lam` e `ell` só têm sentido na normalização fixa `waveCovector = (1,0,0,1)` da carta (a
  componente temporal do covetor é 1). A amplitude θ_M/((n−1)ℓ) do kernel é escrita para um vetor UNITÁRIO
  temporal (A = alfa·n); para a direção nula não há análogo invariante.

O QUE NÃO É.
* Não iguala as curvaturas completas: a igualdade é entre tensores de Einstein (e de Ricci).
* (R2) Em T5 só a soma `a' + c'` é comparada: a diferença `a' − c'` (o cisalhamento) não é vista, e as
  métricas diferem (`eta4` contra `eta4 + H·w⊗w`).
* Não é a lei de área com torção: o teorema de área do kernel usa a conexão de Levi-Civita.
* (R2) Não impõe equação de campo à torção: A é dado de fundo, sem fonte de spin. O Einstein daqui é
  Ric − (R/2)·g com o Ricci da conexão com torção; não é a equação de Einstein–Cartan.
* (R2) T7 tem o balanço como HIPÓTESE: só reescreve T4b com `wave_matter_formula`; não decide `a`, `c`,
  `lam` nem `ell`. Não aparece termo cosmológico porque Einstein e fonte são múltiplos de w⊗w e a métrica
  não é (comentário, não teorema deste arquivo).
* Não é `NamedAtlasH3` nem deriva a seta `hH3` do fecho condicional.
* Não deriva a amplitude nem a escala; não identifica a torção com um grau físico.
* NOT_FALSIFIED nunca é CONFIRMED. β nunca literal.

COMO SE LIGA (fiação, não homônimo). `a_conexao_com_torcao_e_levi_civita_mais_a_contorcao_do_kernel` prova,
ponto a ponto, que a conexão definida aqui é a de Levi-Civita do kernel (`frameLeviCivita`) mais a contorção
`TGLExt.TracialTorsion.Kmix` aplicada às métricas do kernel (`frameMetricField`, `inverseFrameMetricField`) e
ao vetor A = lam • waveCovector; `a_torcao_da_onda_e_a_tracial` prova que a torção dela é
`TGLExt.TracialTorsion.torsion`. O Ricci é calculado dentro da geometria em coordenadas do kernel
(`coordinateRicci`, a mesma contração do `wave_ricci`), sem passar por nenhuma cópia da álgebra da torção;
`ricciOf_e_coordinateRicci` liga as duas contrações para toda conexão. Por fim,
`o_ricci_da_onda_com_torcao_pela_forma_fechada_do_kernel` (T11) obtém o mesmo Ricci pela forma fechada do
kernel (`TGLExt.TracialTorsion.ricci_of_tracial_connection`, usando T10, T0, T2a, T2b e a compatibilidade
métrica de Levi-Civita do kernel): Levi-Civita mais (n − 2)·A_b A_d, em acordo com T3.
(R2) `os_dois_caminhos_dao_o_mesmo_ricci` junta T11 com `wave_ricci` e reobtém, entrada a entrada, o Ricci
de T3 sem usar T3.

CONVENÇÃO (R2). O Ricci é R_{bd} = R^a_{bad}, a mesma contração em `coordinateRicci` e em `ricciOf` (T10).
O resultado é simétrico porque ∇A = 0 (T2b): a parte antissimétrica −((n−2)/2)(∇_d A_b − ∇_b A_d) do kernel
é nula. A compatibilidade métrica da conexão com torção vem de `contortion_metric_compatible` do kernel
mais Levi-Civita e NÃO é teorema deste arquivo. Que `a = c = 0` é o caso plano nas definições do kernel
(métrica `eta4` em todo ponto, conexão de Levi-Civita nula) está em `a_onda_chata_e_plana`.
-/

namespace TGLExt.TorcaoOndaCandidata

open Filter Topology Matrix Set TGLExt ChatgptAudit ChatgptAudit.Coherent023 ChatgptAudit.Response028
  ChatgptAudit.Wave029

noncomputable section

/-! ## D1 — a conexão da onda com a torção tracial ao longo da onda -/

/-- A métrica de Minkowski do kernel é simétrica (auxiliar). -/
theorem eta4_simetrica (i j : Fin 4) : eta4 i j = eta4 j i := by
  fin_cases i <;> fin_cases j <;>
    norm_num [eta4, Matrix.diagonal_apply, Matrix.cons_val_two, Matrix.cons_val_three,
      Fin.isValue]

/-- [candidata] D1. A conexão da onda plana com torção: `Gamma x i r j` é Γ^r_{ij} (i é a direção da
    derivada). É a de Levi-Civita da onda (`waveConnection`) mais a contorção tracial
    `δ^r_i A_j − g_{ij} A^r` com `A = lam • waveCovector`, escrita em forma polinomial explícita
    (`g_{ij} = eta4 i j + H·w_i·w_j`, `A^r = lam · waveRaised r`). -/
def conexaoDaOndaComTorcao (a c lam : ℝ) : ConnectionField4 :=
  fun x i r j => waveConnection a c x i r j +
    lam * (TGLExt.TracialTorsion.kd r i * waveCovector j -
      (eta4 i j + waveProfile a c x * waveCovector i * waveCovector j) * waveRaised r)

/-! ## T0, T1, T2 — a fiação com `TGLExt.TracialTorsion` -/

/-- O vetor da torção levantado pela métrica inversa da onda é `lam · waveRaised` (constante em x). -/
theorem o_levantamento_do_vetor_da_onda (a c lam : ℝ) (x : Coordinate4) (r : Fin 4) :
    TGLExt.TracialTorsion.raise
      (fun p q => inverseFrameMetricField (waveInverseSolder a c) x p q)
      (fun d => lam * waveCovector d) r = lam * waveRaised r := by
  unfold TGLExt.TracialTorsion.raise
  rw [wave_inverse_metric_formula]
  fin_cases r <;>
    norm_num [Fin.sum_univ_four, eta4, Matrix.vecMulVec, waveCovector, waveRaised,
      Matrix.diagonal_apply, Matrix.cons_val_two, Matrix.cons_val_three, Fin.isValue] <;>
    norm_num [Fin.ext_iff] <;> ring

/-- [candidata] T0. A conexão com torção é, ponto a ponto, a de Levi-Civita do kernel mais a contorção
    `Kmix` do kernel (`TGLExt.TracialTorsion`), aplicada às métricas do kernel e a `A = lam • waveCovector`.
    Isto impede o homônimo: a parcela somada É a contorção do kernel. -/
theorem a_conexao_com_torcao_e_levi_civita_mais_a_contorcao_do_kernel (a c lam : ℝ) (x : Coordinate4)
    (i r j : Fin 4) :
    conexaoDaOndaComTorcao a c lam x i r j =
      frameLeviCivita (waveSolder a c) (waveInverseSolder a c) x i r j +
        TGLExt.TracialTorsion.Kmix (fun p q => frameMetricField (waveSolder a c) x p q)
          (fun p q => inverseFrameMetricField (waveInverseSolder a c) x p q)
          (fun d => lam * waveCovector d) r i j := by
  rw [wave_levi_civita]
  simp only [TGLExt.TracialTorsion.Kmix, conexaoDaOndaComTorcao]
  rw [o_levantamento_do_vetor_da_onda, wave_metric_formula]
  simp only [Matrix.add_apply, Matrix.smul_apply, Matrix.vecMulVec_apply, smul_eq_mul]
  ring

/-- [candidata] T1. A torção da conexão da onda é a torção tracial do kernel:
    `Γ^r_{ij} − Γ^r_{ji} = T^r_{ij}` com `A = lam • waveCovector`. -/
theorem a_torcao_da_onda_e_a_tracial (a c lam : ℝ) (x : Coordinate4) (i r j : Fin 4) :
    conexaoDaOndaComTorcao a c lam x i r j - conexaoDaOndaComTorcao a c lam x j r i =
      TGLExt.TracialTorsion.torsion (fun d => lam * waveCovector d) r i j := by
  unfold conexaoDaOndaComTorcao TGLExt.TracialTorsion.torsion
  rw [wave_connection_torsion_free a c x i j r, eta4_simetrica i j]
  ring

/-- Controle de não-vacuidade: com `lam ≠ 0` a torção não é nula (a conexão de Levi-Civita da onda é sem
    torção: `wave_connection_torsion_free`). -/
theorem a_torcao_da_onda_nao_e_nula (a c lam : ℝ) (hlam : lam ≠ 0) (x : Coordinate4) :
    conexaoDaOndaComTorcao a c lam x 0 0 3 - conexaoDaOndaComTorcao a c lam x 3 0 0 ≠ 0 := by
  rw [a_torcao_da_onda_e_a_tracial]
  have h : TGLExt.TracialTorsion.torsion (fun d => lam * waveCovector d) 0 0 3 = lam := by
    norm_num [TGLExt.TracialTorsion.torsion, TGLExt.TracialTorsion.kd, waveCovector,
      Matrix.cons_val_two, Matrix.cons_val_three, Fin.isValue, Fin.ext_iff]
  rw [h]
  exact hlam

/-- [candidata] T2a. O vetor da torção posto ao longo da onda é NULO para a métrica inversa da onda:
    `A_a A^a = 0`. -/
theorem o_vetor_da_torcao_na_onda_e_nulo (a c lam : ℝ) (x : Coordinate4) :
    TGLExt.TracialTorsion.normSq
      (fun p q => inverseFrameMetricField (waveInverseSolder a c) x p q)
      (fun d => lam * waveCovector d) = 0 := by
  unfold TGLExt.TracialTorsion.normSq
  simp only [o_levantamento_do_vetor_da_onda]
  norm_num [Fin.sum_univ_four, waveCovector, waveRaised, Matrix.cons_val_two,
    Matrix.cons_val_three, Fin.isValue]

/-- [candidata] T2b. O covetor da onda é paralelo para a conexão de Levi-Civita da onda:
    `Γ^e_{ij} w_e = 0`; logo `∇_i A_j = ∂_i A_j − Γ^e_{ij} A_e = 0` para `A = lam • waveCovector`. -/
theorem o_vetor_da_torcao_e_covariantemente_constante (a c : ℝ) (x : Coordinate4) (i j : Fin 4) :
    ∑ e, waveConnection a c x i e j * waveCovector e = 0 := by
  fin_cases i <;> fin_cases j <;>
    norm_num [Fin.sum_univ_four, waveConnection, waveTransverse, waveCovector, waveRaised,
      Matrix.cons_val_two, Matrix.cons_val_three, Fin.isValue]

/-! ## T3 — o Ricci da onda com torção, calculado na geometria em coordenadas do kernel -/

/-- Derivada parcial da soma (auxiliar). -/
theorem coordinatePartial_soma (f g : Coordinate4 → ℝ) (x : Coordinate4) (i : Fin 4)
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) :
    coordinatePartial (fun y => f y + g y) x i = coordinatePartial f x i + coordinatePartial g x i := by
  unfold coordinatePartial
  rw [fderiv_fun_add hf hg]
  simp

/-- Derivada parcial de `u + v · f` (auxiliar). -/
theorem coordinatePartial_afim (u v : ℝ) (f : Coordinate4 → ℝ) (x : Coordinate4) (i : Fin 4)
    (hf : DifferentiableAt ℝ f x) :
    coordinatePartial (fun y => u + v * f y) x i = v * coordinatePartial f x i := by
  unfold coordinatePartial
  rw [((hf.hasFDerivAt.const_mul v).const_add u).fderiv]
  simp

/-- O primeiro jato da conexão com torção: o de `waveConnection` (linear em x,
    `wave_connection_jet`) menos `lam · ∂_k H · w_i w_j w^r`, que vem da parte da contorção que depende
    de x (a métrica `g_{ij} = eta4 i j + H w_i w_j`). -/
theorem o_jato_da_conexao_com_torcao (a c lam : ℝ) (x : Coordinate4) (k i r j : Fin 4) :
    connectionFirstJet (conexaoDaOndaComTorcao a c lam) x k i r j =
      waveConnection a c (Pi.single k 1) i r j -
        lam * coordinatePartial (waveProfile a c) x k *
          (waveCovector i * waveCovector j * waveRaised r) := by
  have hW : DifferentiableAt ℝ (fun y => waveConnection a c y i r j) x :=
    smooth_matrix_differentiableAt univ isOpen_univ _ ((wave_connection_smooth a c) i) x
      (mem_univ x) r j
  have hH : DifferentiableAt ℝ (waveProfile a c) x :=
    (wave_profile_smooth a c).differentiable (by simp) x
  have he : (fun y => conexaoDaOndaComTorcao a c lam y i r j) = fun y =>
      waveConnection a c y i r j +
        (lam * (TGLExt.TracialTorsion.kd r i * waveCovector j - eta4 i j * waveRaised r) +
          (-(lam * (waveCovector i * waveCovector j * waveRaised r))) * waveProfile a c y) := by
    funext y
    unfold conexaoDaOndaComTorcao
    ring
  have hJ : coordinatePartial (fun y => waveConnection a c y i r j) x k =
      waveConnection a c (Pi.single k 1) i r j := by
    have := congrFun (congrFun (wave_connection_jet a c x k i) r) j
    exact this
  change coordinatePartial (fun y => conexaoDaOndaComTorcao a c lam y i r j) x k = _
  rw [he, coordinatePartial_soma _ _ x k hW ((hH.const_mul _).const_add _),
    coordinatePartial_afim _ _ _ x k hH, hJ]
  ring

/-- [candidata] T3 ★. O Ricci da onda com torção ao longo da onda: `(a + c + 2·lam²) • w⊗w`. A parcela
    `2·lam²` é a de `(n − 2)·A_b A_d` com `n = 4` na forma fechada da torção tracial do kernel
    (`TGLExt.TracialTorsion.ricci_closed_form`); aqui ela sai do cálculo direto em `coordinateRicci`, e
    T11 (mais abaixo) confere que a forma fechada do kernel dá o mesmo número. -/
theorem o_ricci_da_onda_com_torcao (a c lam : ℝ) (x : Coordinate4) :
    coordinateRicci (conexaoDaOndaComTorcao a c lam) x =
      (a + c + 2 * lam ^ 2) • Matrix.vecMulVec waveCovector waveCovector := by
  ext b j
  simp only [coordinateRicci, coordinateCurvature, connectionCurvatureJet, Matrix.sub_apply,
    Matrix.add_apply, Matrix.mul_apply, Fin.sum_univ_four, o_jato_da_conexao_com_torcao,
    wave_profile_partial]
  fin_cases b <;> fin_cases j <;>
    norm_num [conexaoDaOndaComTorcao, waveConnection, waveTransverse, waveProfile, waveCovector,
      waveRaised, eta4, TGLExt.TracialTorsion.kd, Pi.single_apply, Matrix.vecMulVec,
      Matrix.cons_val_two, Matrix.cons_val_three, Matrix.diagonal_apply, Fin.isValue] <;>
    norm_num [Fin.ext_iff] <;> ring

/-- [candidata] T3, caso chato (a = c = 0). O núcleo: o Ricci da torção ao longo da onda numa métrica
    plana é `(2·lam²) • w⊗w`. -/
theorem o_ricci_da_onda_chata_com_torcao (lam : ℝ) (x : Coordinate4) :
    coordinateRicci (conexaoDaOndaComTorcao 0 0 lam) x =
      (2 * lam ^ 2) • Matrix.vecMulVec waveCovector waveCovector := by
  rw [o_ricci_da_onda_com_torcao]
  congr 1
  ring

/-- [candidata] (R2) A onda com `a = c = 0` é PLANA nas definições do kernel: a métrica é `eta4` em todo
    ponto e a conexão de Levi-Civita é nula. É o que dá sentido a "onda chata" neste arquivo. -/
theorem a_onda_chata_e_plana (x : Coordinate4) :
    frameMetricField (waveSolder 0 0) x = eta4 ∧ ∀ i r j, waveConnection 0 0 x i r j = 0 := by
  refine ⟨?_, ?_⟩
  · rw [wave_metric_formula]
    simp [waveProfile]
  · intro i r j
    fin_cases i <;> fin_cases r <;> fin_cases j <;>
      norm_num [waveConnection, waveTransverse, waveCovector, waveRaised, Matrix.cons_val_two,
        Matrix.cons_val_three, Fin.isValue]

/-! ## T4 — o escalar e o Einstein -/

/-- [candidata] T4a. O escalar de curvatura da onda com torção é nulo. -/
theorem o_escalar_da_onda_com_torcao (a c lam : ℝ) (x : Coordinate4) :
    coordinateScalarCurvature (inverseFrameMetricField (waveInverseSolder a c))
      (conexaoDaOndaComTorcao a c lam) x = 0 := by
  simp only [coordinateScalarCurvature, o_ricci_da_onda_com_torcao, wave_inverse_metric_formula]
  norm_num [Fin.sum_univ_four, eta4, Matrix.vecMulVec, waveCovector, waveRaised,
    Matrix.cons_val_two, Matrix.cons_val_three, Matrix.diagonal_apply, Fin.isValue]
  norm_num [Fin.ext_iff]
  ring

/-- [candidata] T4b. O tensor de Einstein da onda com torção: igual ao Ricci, `(a + c + 2·lam²) • w⊗w`. -/
theorem o_einstein_da_onda_com_torcao (a c lam : ℝ) (x : Coordinate4) :
    geometricEinsteinTensor (frameMetricField (waveSolder a c))
      (inverseFrameMetricField (waveInverseSolder a c)) (conexaoDaOndaComTorcao a c lam) x =
      (a + c + 2 * lam ^ 2) • Matrix.vecMulVec waveCovector waveCovector := by
  unfold geometricEinsteinTensor
  rw [o_escalar_da_onda_com_torcao, o_ricci_da_onda_com_torcao]
  simp only [zero_div, zero_smul, sub_zero]

/-! ## T5 — a onda chata com torção é a onda curva sem torção -/

/-- Auxiliar: `w⊗w` não é nula (entrada (0,0) = 1). -/
theorem a_matriz_da_onda_nao_e_nula : (Matrix.vecMulVec waveCovector waveCovector : Tensor4) ≠ 0 := by
  intro h
  have hh := congrArg (fun M : Tensor4 => M 0 0) h
  simp [Matrix.vecMulVec, waveCovector] at hh

/-- [candidata] T5 ★★. O Einstein da onda com torção (em x) é o Einstein de Levi-Civita de uma onda
    curva sem torção (em x', perfil `a' c'`) se, e só se, `a' + c' = a + c + 2·lam²`.
    (R2) Todo o conteúdo está em T4b: T5 só compara dois múltiplos da mesma matriz não nula. Só a soma
    `a' + c'` é comparada; `a' − c'` não é vista; não é igualdade de métrica nem de curvatura completa. -/
theorem a_onda_plana_com_torcao_e_a_onda_plana_curva (a c lam a' c' : ℝ) (x x' : Coordinate4) :
    geometricEinsteinTensor (frameMetricField (waveSolder a c))
      (inverseFrameMetricField (waveInverseSolder a c)) (conexaoDaOndaComTorcao a c lam) x =
      frameEinsteinTensor (waveSolder a' c') (waveInverseSolder a' c') x' ↔
        a' + c' = a + c + 2 * lam ^ 2 := by
  rw [o_einstein_da_onda_com_torcao, wave_einstein]
  constructor
  · intro h
    have hh := congrArg (fun M : Tensor4 => M 0 0) h
    simpa [Matrix.vecMulVec, waveCovector, eq_comm] using hh
  · intro h
    rw [h]

/-- [candidata] T5, corolário. A onda CHATA com torção tem o Einstein da onda CURVA sem torção com
    `a' + c' = 2·lam²`. -/
theorem a_onda_chata_com_torcao_e_a_onda_curva_sem_torcao (lam a' c' : ℝ) (x x' : Coordinate4) :
    geometricEinsteinTensor (frameMetricField (waveSolder 0 0))
      (inverseFrameMetricField (waveInverseSolder 0 0)) (conexaoDaOndaComTorcao 0 0 lam) x =
      frameEinsteinTensor (waveSolder a' c') (waveInverseSolder a' c') x' ↔
        a' + c' = 2 * lam ^ 2 := by
  rw [a_onda_plana_com_torcao_e_a_onda_plana_curva]
  constructor <;> intro h <;> linarith

/-- [candidata] (R2) Não-vacuidade no TENSOR: com `lam ≠ 0` o Einstein da onda chata com torção não é
    nulo (é `(2·lam²) • w⊗w` e `w⊗w ≠ 0`). -/
theorem o_einstein_da_onda_chata_com_torcao_nao_e_nulo (lam : ℝ) (hlam : lam ≠ 0) (x : Coordinate4) :
    geometricEinsteinTensor (frameMetricField (waveSolder 0 0))
      (inverseFrameMetricField (waveInverseSolder 0 0)) (conexaoDaOndaComTorcao 0 0 lam) x ≠ 0 := by
  rw [o_einstein_da_onda_com_torcao]
  intro h
  have hh := congrArg (fun M : Tensor4 => M 0 0) h
  simp only [Matrix.smul_apply, Matrix.vecMulVec_apply, Matrix.zero_apply, smul_eq_mul] at hh
  have hw : waveCovector 0 = 1 := by simp [waveCovector]
  rw [hw] at hh
  have hl : lam ^ 2 = 0 := by linarith
  exact hlam ((pow_eq_zero_iff (n := 2) (by norm_num)).mp hl)

/-! ## T6 — a amplitude da Ponte -/

/-- [candidata] A amplitude da torção da Ponte em dimensão 4: `alfa = θ_M / ((n − 1)·ℓ)` com `n = 4`
    (cabeçalho de `TracialDissipativeTorsion.lean`), `θ_M = thetaMiguel β`. Entra por DEFINIÇÃO; a escala
    `ell` é entrada. (R2) No kernel essa amplitude é escrita para um vetor unitário temporal; ao longo da
    direção nula ela só tem sentido na normalização fixa de `waveCovector` (ver o cabeçalho). -/
def amplitudeDaTorcao (β ell : ℝ) : ℝ := thetaMiguel β / (3 * ell)

/-- [candidata] T6. Com `lam = amplitudeDaTorcao β ell`, o Einstein da onda chata com torção é
    `(2·θ_M²/(9·ell²)) • w⊗w` e iguala o da onda curva sem torção se, e só se, `a' + c'` é esse número.
    (Vale também para `ell = 0`, caso degenerado em que os dois lados são zero em ℝ; o caso de interesse
    é `ell ≠ 0`.) (R2) O VALOR de `thetaMiguel β` não é usado na prova: T6 é T5 com `lam` substituído. -/
theorem a_onda_plana_curva_e_o_angulo_de_miguel (β ell : ℝ) (a' c' : ℝ) (x x' : Coordinate4) :
    geometricEinsteinTensor (frameMetricField (waveSolder 0 0))
      (inverseFrameMetricField (waveInverseSolder 0 0))
      (conexaoDaOndaComTorcao 0 0 (amplitudeDaTorcao β ell)) x =
        (2 * thetaMiguel β ^ 2 / (9 * ell ^ 2)) • Matrix.vecMulVec waveCovector waveCovector ∧
    (geometricEinsteinTensor (frameMetricField (waveSolder 0 0))
      (inverseFrameMetricField (waveInverseSolder 0 0))
      (conexaoDaOndaComTorcao 0 0 (amplitudeDaTorcao β ell)) x =
        frameEinsteinTensor (waveSolder a' c') (waveInverseSolder a' c') x' ↔
          a' + c' = 2 * thetaMiguel β ^ 2 / (9 * ell ^ 2)) := by
  have hk : (0 : ℝ) + 0 + 2 * amplitudeDaTorcao β ell ^ 2 = 2 * thetaMiguel β ^ 2 / (9 * ell ^ 2) := by
    unfold amplitudeDaTorcao
    ring
  refine ⟨?_, ?_⟩
  · rw [o_einstein_da_onda_com_torcao, hk]
  · rw [a_onda_plana_com_torcao_e_a_onda_plana_curva, hk]

/-- [candidata] T6, não-vacuidade DO NÚMERO. Para `β > 0` e `ell ≠ 0` o número `2·θ_M²/(9·ell²)` não é
    nulo. (R2) Para o tensor, ver `o_einstein_da_onda_chata_com_torcao_nao_e_nulo`. -/
theorem a_curvatura_do_angulo_de_miguel_nao_e_nula (β ell : ℝ) (hβ : 0 < β) (hell : ell ≠ 0) :
    2 * thetaMiguel β ^ 2 / (9 * ell ^ 2) ≠ 0 := by
  have hθ : 0 < thetaMiguel β := Real.arcsin_pos.mpr (Real.sqrt_pos.mpr hβ)
  have hl : 0 < ell ^ 2 := by positivity
  positivity

/-! ## T7 — a equação de campo na onda com torção -/

/-- [candidata] T7. Dado `eta ≠ 0` e o balanço `eta · (a + c + 2·lam²) = 2π · acoplamento`, o Einstein da
    onda com torção é `(2π/eta)` vezes o tensor de matéria do covetor da onda
    (`frameCovectorStress … waveCovectorField acoplamento`). (R2) O balanço é HIPÓTESE: T7 é T4b reescrito
    com `wave_matter_formula`; não decide `a`, `c`, `lam` nem `ell`. -/
theorem a_equacao_de_campo_na_onda_com_torcao (a c lam eta acoplamento : ℝ) (x : Coordinate4)
    (heta : eta ≠ 0) (hbal : eta * (a + c + 2 * lam ^ 2) = 2 * Real.pi * acoplamento) :
    geometricEinsteinTensor (frameMetricField (waveSolder a c))
      (inverseFrameMetricField (waveInverseSolder a c)) (conexaoDaOndaComTorcao a c lam) x =
      (2 * Real.pi / eta) •
        frameCovectorStress (waveSolder a c) (waveInverseSolder a c) waveCovectorField
          acoplamento x := by
  have hm : frameCovectorStress (waveSolder a c) (waveInverseSolder a c) waveCovectorField
      acoplamento x = acoplamento • Matrix.vecMulVec waveCovector waveCovector :=
    wave_matter_formula a c acoplamento x
  rw [hm, o_einstein_da_onda_com_torcao, smul_smul]
  congr 1
  field_simp
  linarith

/-- [candidata] T7, recíproca: se o Einstein da onda com torção é `(2π/eta)` vezes a matéria, vale o
    balanço. -/
theorem a_equacao_de_campo_na_onda_com_torcao_reciproca (a c lam eta acoplamento : ℝ) (x : Coordinate4)
    (heta : eta ≠ 0)
    (h : geometricEinsteinTensor (frameMetricField (waveSolder a c))
      (inverseFrameMetricField (waveInverseSolder a c)) (conexaoDaOndaComTorcao a c lam) x =
      (2 * Real.pi / eta) •
        frameCovectorStress (waveSolder a c) (waveInverseSolder a c) waveCovectorField
          acoplamento x) :
    eta * (a + c + 2 * lam ^ 2) = 2 * Real.pi * acoplamento := by
  have hm : frameCovectorStress (waveSolder a c) (waveInverseSolder a c) waveCovectorField
      acoplamento x = acoplamento • Matrix.vecMulVec waveCovector waveCovector :=
    wave_matter_formula a c acoplamento x
  rw [hm, o_einstein_da_onda_com_torcao] at h
  have hh := congrArg (fun M : Tensor4 => M 0 0) h
  simp [Matrix.vecMulVec, waveCovector] at hh
  field_simp at hh
  linarith

/-! ## T8 — a escala que resta é única -/

/-- [candidata] T8. Dados `eta > 0`, `acoplamento > 0` e o ângulo `theta > 0`, existe exatamente uma escala
    `ell > 0` com `eta · 2·(theta/(3·ell))² = 2π · acoplamento` (o balanço de T7 com `a = c = 0` e a
    amplitude da Ponte). A escala não é derivada aqui: é a que o balanço pede. (R2) É a inversão elementar
    de `ell`; `eta` e o acoplamento são livres e nada liga `ell` a β; `ell` só tem sentido na normalização
    fixa de `waveCovector` (ver o cabeçalho). -/
theorem a_escala_que_resta_e_unica (eta acoplamento theta : ℝ) (heta : 0 < eta)
    (hac : 0 < acoplamento) (hθ : 0 < theta) :
    ∃! ell : ℝ, 0 < ell ∧ eta * (2 * (theta / (3 * ell)) ^ 2) = 2 * Real.pi * acoplamento := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have hq : 0 < Real.pi * acoplamento / eta := by positivity
  set s := Real.sqrt (Real.pi * acoplamento / eta) with hs
  have hs0 : 0 < s := Real.sqrt_pos.mpr hq
  have hs2 : s ^ 2 = Real.pi * acoplamento / eta := Real.sq_sqrt hq.le
  refine ⟨theta / (3 * s), ⟨by positivity, ?_⟩, ?_⟩
  · have : theta / (3 * (theta / (3 * s))) = s := by
      field_simp
    rw [this, hs2]
    field_simp
  · rintro ell ⟨hell, hbal⟩
    have hk : 0 < theta / (3 * ell) := by positivity
    have hk2 : (theta / (3 * ell)) ^ 2 = s ^ 2 := by
      rw [hs2, eq_div_iff heta.ne']
      linarith
    have hk3 : theta / (3 * ell) = s := (sq_eq_sq₀ hk.le hs0.le).mp hk2
    rw [div_eq_iff (by positivity)] at hk3
    rw [eq_div_iff (by positivity)]
    linarith

/-! ## T9 — controle: a torção ao longo do tempo (métrica plana) -/

/-- O covetor temporal `n = (1, 0, 0, 0)` (controle). -/
def nTemporal : Coordinate4 := ![1, 0, 0, 0]

/-- [candidata] T9. A conexão plana com a torção tracial ao longo do tempo: `Γ^r_{ij} = alfa·(δ^r_i n_j −
    eta4 i j · n^r)`, com `n^r = nTemporal r` (aqui `eta4 · n = n`). -/
def conexaoChataComTorcaoTemporal (alfa : ℝ) : ConnectionField4 :=
  fun _ i r j => alfa * (TGLExt.TracialTorsion.kd r i * nTemporal j - eta4 i j * nTemporal r)

/-- Uma conexão constante tem jato nulo (controle). -/
theorem o_jato_da_conexao_temporal (alfa : ℝ) (x : Coordinate4) (k i : Fin 4) :
    connectionFirstJet (conexaoChataComTorcaoTemporal alfa) x k i = 0 := by
  ext r j
  simp [connectionFirstJet, tensorFieldJet, coordinatePartial, conexaoChataComTorcaoTemporal]

/-- [candidata] T9. O Ricci da torção temporal: `2·alfa²·(n⊗n − eta4)`. -/
theorem o_ricci_da_torcao_temporal (alfa : ℝ) (x : Coordinate4) :
    coordinateRicci (conexaoChataComTorcaoTemporal alfa) x =
      (2 * alfa ^ 2) • (Matrix.vecMulVec nTemporal nTemporal - eta4) := by
  ext b j
  simp only [coordinateRicci, coordinateCurvature, connectionCurvatureJet, Matrix.sub_apply,
    Matrix.add_apply, Matrix.mul_apply, Fin.sum_univ_four, o_jato_da_conexao_temporal,
    Matrix.zero_apply]
  fin_cases b <;> fin_cases j <;>
    norm_num [conexaoChataComTorcaoTemporal, nTemporal, eta4, TGLExt.TracialTorsion.kd,
      Matrix.vecMulVec, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.diagonal_apply,
      Fin.isValue] <;> norm_num [Fin.ext_iff] <;> ring

/-- [candidata] T9. O escalar da torção temporal: `−6·alfa²`. -/
theorem o_escalar_da_torcao_temporal (alfa : ℝ) (x : Coordinate4) :
    coordinateScalarCurvature (fun _ => eta4) (conexaoChataComTorcaoTemporal alfa) x =
      -6 * alfa ^ 2 := by
  simp only [coordinateScalarCurvature, o_ricci_da_torcao_temporal]
  norm_num [Fin.sum_univ_four, nTemporal, eta4, Matrix.vecMulVec, Matrix.cons_val_two,
    Matrix.cons_val_three, Matrix.diagonal_apply, Fin.isValue]
  ring

/-- [candidata] T9 (controle). O Einstein da torção temporal em métrica plana: `2·alfa²·n⊗n + alfa²·eta4`.
    Escrito como `Einstein + (−alfa²)·eta4 = 2·alfa²·n⊗n`: com a torção ao longo do TEMPO aparece o termo
    proporcional a `eta4` (o que, ao longo da onda nula, não aparece: T4). -/
theorem o_einstein_da_torcao_temporal (alfa : ℝ) (x : Coordinate4) :
    geometricEinsteinTensor (fun _ => eta4) (fun _ => eta4) (conexaoChataComTorcaoTemporal alfa) x +
        (-alfa ^ 2) • eta4 = (2 * alfa ^ 2) • Matrix.vecMulVec nTemporal nTemporal := by
  unfold geometricEinsteinTensor
  rw [o_escalar_da_torcao_temporal, o_ricci_da_torcao_temporal]
  ext b j
  simp only [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply, smul_eq_mul]
  ring

/-! ## T10 — a ponte entre as duas contrações do Ricci -/

/-- [candidata] T10. A contração `ricciOf` da álgebra da torção (`TGLExt.TracialTorsion`) é o
    `coordinateRicci` da geometria em coordenadas do kernel, para toda conexão `Gamma` (com
    `Gam a c e := Gamma p c a e` e `dGam w a c e := connectionFirstJet Gamma p w c a e`). -/
theorem ricciOf_e_coordinateRicci (Gamma : ConnectionField4) (p : Coordinate4) (b d : Fin 4) :
    TGLExt.TracialTorsion.ricciOf (ι := Fin 4) (fun a c e => Gamma p c a e)
      (fun w a c e => connectionFirstJet Gamma p w c a e) b d = coordinateRicci Gamma p b d := by
  unfold TGLExt.TracialTorsion.ricciOf coordinateRicci
  refine Finset.sum_congr rfl (fun a _ => ?_)
  simp only [TGLExt.TracialTorsion.riemann, coordinateCurvature, connectionCurvatureJet,
    Matrix.sub_apply, Matrix.add_apply, Matrix.mul_apply, Finset.sum_sub_distrib]
  ring

/-! ## T11 — verificação cruzada: o mesmo Ricci pela forma fechada do kernel -/

/-- A métrica da onda é simétrica (auxiliar). -/
theorem a_metrica_da_onda_e_simetrica (a c : ℝ) (x : Coordinate4) (i j : Fin 4) :
    frameMetricField (waveSolder a c) x i j = frameMetricField (waveSolder a c) x j i := by
  rw [wave_metric_formula]
  simp only [Matrix.add_apply, Matrix.smul_apply, Matrix.vecMulVec_apply, smul_eq_mul]
  rw [eta4_simetrica i j]
  ring

/-- A métrica da onda e a sua inversa, componente a componente (auxiliar). -/
theorem a_metrica_da_onda_e_a_sua_inversa (a c : ℝ) (x : Coordinate4) (i j : Fin 4) :
    (∑ k, frameMetricField (waveSolder a c) x i k *
        inverseFrameMetricField (waveInverseSolder a c) x k j = TGLExt.TracialTorsion.kd i j) ∧
    (∑ k, inverseFrameMetricField (waveInverseSolder a c) x i k *
        frameMetricField (waveSolder a c) x k j = TGLExt.TracialTorsion.kd i j) := by
  have h1 := inverse_frame_metric_right (waveSolder a c) (waveInverseSolder a c) x
    (wave_solder_inverse a c x) (wave_inverse_solder a c x)
  have h2 := inverse_frame_metric_left (waveSolder a c) (waveInverseSolder a c) x
    (wave_solder_inverse a c x) (wave_inverse_solder a c x)
  constructor
  · have := congrFun (congrFun h1 i) j
    rw [Matrix.mul_apply, Matrix.one_apply] at this
    unfold TGLExt.TracialTorsion.kd
    exact this
  · have := congrFun (congrFun h2 i) j
    rw [Matrix.mul_apply, Matrix.one_apply] at this
    unfold TGLExt.TracialTorsion.kd
    exact this

/-- A conexão de Levi-Civita da onda é compatível com a métrica, em forma de componentes: vem do kernel
    (`levi_civita_field_metric_compatible`), não de uma conta nova. -/
theorem a_metrica_da_onda_e_compativel (a c : ℝ) (x : Coordinate4) (i d b : Fin 4) :
    tensorFieldJet (frameMetricField (waveSolder a c)) x i d b =
      ∑ e, (waveConnection a c x i e d * frameMetricField (waveSolder a c) x e b +
            waveConnection a c x i e b * frameMetricField (waveSolder a c) x d e) := by
  have hm := levi_civita_field_metric_compatible univ isOpen_univ
    (frameMetricField (waveSolder a c)) (inverseFrameMetricField (waveInverseSolder a c))
    (fun y _ => frame_metric_symmetric (waveSolder a c) y)
    (fun y _ => inverse_frame_metric_left _ _ y (wave_solder_inverse a c y)
      (wave_inverse_solder a c y))
    (fun y _ => inverse_frame_metric_right _ _ y (wave_solder_inverse a c y)
      (wave_inverse_solder a c y))
  have hf := metric_compatibility_formula univ (frameMetricField (waveSolder a c))
    (leviCivitaField (frameMetricField (waveSolder a c))
      (inverseFrameMetricField (waveInverseSolder a c))) hm x (mem_univ x) i
  have hL : leviCivitaField (frameMetricField (waveSolder a c))
      (inverseFrameMetricField (waveInverseSolder a c)) = waveConnection a c := wave_levi_civita a c
  rw [hL] at hf
  have h2 := congrFun (congrFun hf d) b
  rw [h2]
  simp only [Matrix.add_apply, Matrix.mul_apply, Matrix.transpose_apply, Finset.sum_add_distrib]
  congr 1
  exact Finset.sum_congr rfl (fun e _ => mul_comm _ _)

/-- `∂_k H = 2·T_k`, com `T = waveTransverse` (auxiliar). -/
theorem a_derivada_do_perfil_e_o_dobro_do_transverso (a c : ℝ) (x : Coordinate4) (k : Fin 4) :
    coordinatePartial (waveProfile a c) x k = 2 * waveTransverse a c x k := by
  rw [wave_profile_partial]
  fin_cases k <;>
    norm_num [waveTransverse, Pi.single_apply, Matrix.cons_val_two, Matrix.cons_val_three,
      Fin.isValue] <;> norm_num [Fin.ext_iff] <;> ring

/-- Troca de somas (auxiliar; é o passo `K1` de `TGLExt.TracialTorsion.covK_Kmix`). -/
theorem a_soma_da_derivada_da_inversa (gi dg : Fin 4 → Fin 4 → ℝ) (dgs : Fin 4 → Fin 4 → ℝ)
    (A : Fin 4 → ℝ) (a' : Fin 4)
    (hdgi : ∀ e, dgs a' e = -∑ f, ∑ h, gi a' f * dg f h * gi h e) :
    ∑ e, dgs a' e * A e =
      -∑ f, ∑ h, gi a' f * dg f h * TGLExt.TracialTorsion.raise gi A h := by
  simp only [hdgi]
  unfold TGLExt.TracialTorsion.raise
  simp only [Finset.mul_sum, Finset.sum_mul, neg_mul, Finset.sum_neg_distrib]
  congr 1
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl (fun f _ => ?_)
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl (fun h _ => Finset.sum_congr rfl (fun e _ => ?_))
  ring

/-- [candidata] T11, verificação cruzada. O Ricci da onda com torção sai também da FORMA FECHADA do kernel
    (`TGLExt.TracialTorsion.ricci_of_tracial_connection`, em `n = 4`): Levi-Civita mais `(n − 2)·A_b A_d`,
    porque nesta onda `∇A = 0` (T2b), `∇·A = 0` e `A² = 0` (T2a). Os dois caminhos (o cálculo direto de T3
    e a forma fechada) dão o mesmo número. -/
theorem o_ricci_da_onda_com_torcao_pela_forma_fechada_do_kernel (a c lam : ℝ) (x : Coordinate4)
    (b d : Fin 4) :
    coordinateRicci (conexaoDaOndaComTorcao a c lam) x b d =
      coordinateRicci (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x b d +
        ((Fintype.card (Fin 4) : ℝ) - 2) * ((lam * waveCovector b) * (lam * waveCovector d)) := by
  set g : Fin 4 → Fin 4 → ℝ := fun p q => frameMetricField (waveSolder a c) x p q with hgd
  set gi : Fin 4 → Fin 4 → ℝ := fun p q => inverseFrameMetricField (waveInverseSolder a c) x p q
    with hgid
  set A : Fin 4 → ℝ := fun e => lam * waveCovector e with hAd
  set G0 : Fin 4 → Fin 4 → Fin 4 → ℝ := fun r i j => waveConnection a c x i r j with hG0d
  set dG0 : Fin 4 → Fin 4 → Fin 4 → Fin 4 → ℝ :=
    fun w r i j => waveConnection a c (Pi.single w 1) i r j with hdG0d
  set dK : Fin 4 → Fin 4 → Fin 4 → Fin 4 → ℝ := fun w r i j =>
    -(2 * waveTransverse a c x w * lam) * (waveCovector i * waveCovector j * waveRaised r)
    with hdKd
  set dg : Fin 4 → Fin 4 → Fin 4 → ℝ := fun c' d' b' =>
    2 * waveTransverse a c x c' * (waveCovector d' * waveCovector b') with hdgd
  set dgi : Fin 4 → Fin 4 → Fin 4 → ℝ := fun c' a' e' =>
    -∑ f, ∑ h, gi a' f * dg c' f h * gi h e' with hdgid
  set dA : Fin 4 → Fin 4 → ℝ := fun _ _ => 0 with hdAd
  have hg : ∀ i j, g i j = g j i := fun i j => a_metrica_da_onda_e_simetrica a c x i j
  have hinv : ∀ i j, ∑ k, g i k * gi k j = TGLExt.TracialTorsion.kd i j :=
    fun i j => (a_metrica_da_onda_e_a_sua_inversa a c x i j).1
  have hinv' : ∀ i j, ∑ k, gi i k * g k j = TGLExt.TracialTorsion.kd i j :=
    fun i j => (a_metrica_da_onda_e_a_sua_inversa a c x i j).2
  have hsym : ∀ e p q, G0 e p q = G0 e q p :=
    fun e p q => wave_connection_torsion_free a c x p q e
  have hdg : ∀ c' d' b', dg c' d' b' = ∑ e, (G0 e c' d' * g e b' + G0 e c' b' * g d' e) := by
    intro c' d' b'
    have h1 := a_metrica_da_onda_e_compativel a c x c' d' b'
    have h2 := congrFun (congrFun (wave_metric_jet a c x c') d') b'
    simp only [Matrix.smul_apply, Matrix.vecMulVec_apply, smul_eq_mul] at h2
    show dg c' d' b' = ∑ e, (waveConnection a c x c' e d' * frameMetricField (waveSolder a c) x e b' +
      waveConnection a c x c' e b' * frameMetricField (waveSolder a c) x d' e)
    rw [← h1, h2]
  have hraise : ∀ r, TGLExt.TracialTorsion.raise gi A r = lam * waveRaised r :=
    fun r => o_levantamento_do_vetor_da_onda a c lam x r
  have hww : ∑ h, waveCovector h * waveRaised h = 0 := by
    norm_num [Fin.sum_univ_four, waveCovector, waveRaised, Matrix.cons_val_two,
      Matrix.cons_val_three, Fin.isValue]
  have hdK : ∀ c' a' d' b', dK c' a' d' b' = TGLExt.TracialTorsion.kd a' d' * dA c' b' -
      dg c' d' b' * TGLExt.TracialTorsion.raise gi A a' -
      g d' b' * (∑ e, dgi c' a' e * A e + ∑ e, gi a' e * dA c' e) := by
    intro c' a' d' b'
    have h2 : ∑ e, dgi c' a' e * A e = 0 := by
      rw [a_soma_da_derivada_da_inversa gi (dg c') (dgi c') A a' (fun e => rfl)]
      rw [neg_eq_zero]
      refine Finset.sum_eq_zero (fun f _ => ?_)
      have : ∀ h, gi a' f * dg c' f h * TGLExt.TracialTorsion.raise gi A h =
          (gi a' f * (2 * waveTransverse a c x c' * waveCovector f * lam)) *
            (waveCovector h * waveRaised h) := by
        intro h
        rw [hraise h]
        simp only [hdgd]
        ring
      simp only [this]
      rw [← Finset.mul_sum, hww, mul_zero]
    rw [h2, hraise a']
    simp only [hdAd, hdKd, hdgd, mul_zero, Finset.sum_const_zero, add_zero, sub_zero]
    ring
  have key := TGLExt.TracialTorsion.ricci_of_tracial_connection (ι := Fin 4) g gi hg hinv hinv'
    G0 dG0 dK A dg dgi dA hsym hdg (fun _ _ _ => rfl) hdK b d
  have e1 : (fun r i j => conexaoDaOndaComTorcao a c lam x i r j) =
      (fun p q r => G0 p q r + TGLExt.TracialTorsion.Kmix g gi A p q r) := by
    funext r i j
    rw [a_conexao_com_torcao_e_levi_civita_mais_a_contorcao_do_kernel, wave_levi_civita]
  have e2 : (fun w r i j => connectionFirstJet (conexaoDaOndaComTorcao a c lam) x w i r j) =
      (fun w p q r => dG0 w p q r + dK w p q r) := by
    funext w r i j
    rw [o_jato_da_conexao_com_torcao, a_derivada_do_perfil_e_o_dobro_do_transverso]
    simp only [hdG0d, hdKd]
    ring
  have e3 : (fun w r i j => connectionFirstJet (waveConnection a c) x w i r j) = dG0 := by
    funext w r i j
    exact congrFun (congrFun (wave_connection_jet a c x w i) r) j
  have hLC : coordinateRicci (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x b d =
      TGLExt.TracialTorsion.ricciOf G0 dG0 b d := by
    rw [wave_levi_civita, ← ricciOf_e_coordinateRicci (waveConnection a c) x b d, e3]
  have hcov : ∀ p q, ∑ e, G0 e p q * A e = 0 := by
    intro p q
    have := o_vetor_da_torcao_e_covariantemente_constante a c x p q
    simp only [hG0d, hAd]
    calc ∑ e, waveConnection a c x p e q * (lam * waveCovector e)
        = lam * ∑ e, waveConnection a c x p e q * waveCovector e := by
          rw [Finset.mul_sum]
          exact Finset.sum_congr rfl (fun e _ => by ring)
      _ = 0 := by rw [this, mul_zero]
  have hns : TGLExt.TracialTorsion.normSq gi A = 0 := o_vetor_da_torcao_na_onda_e_nulo a c lam x
  have hdiv : TGLExt.TracialTorsion.divA gi (fun p q => dA p q - ∑ e, G0 e p q * A e) = 0 := by
    unfold TGLExt.TracialTorsion.divA
    simp only [hcov, hdAd, sub_zero, mul_zero, Finset.sum_const_zero]
  rw [← ricciOf_e_coordinateRicci (conexaoDaOndaComTorcao a c lam) x b d, e1, e2, key, hLC, hdiv, hns]
  simp only [hcov, hdAd, sub_zero, mul_zero]
  ring

/-- [candidata] T11, em `n = 4`: o mesmo resultado com o número escrito, `(n − 2) = 2`. -/
theorem a_forma_fechada_da_onda_com_torcao_em_n4 (a c lam : ℝ) (x : Coordinate4) (b d : Fin 4) :
    coordinateRicci (conexaoDaOndaComTorcao a c lam) x b d =
      coordinateRicci (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x b d +
        2 * ((lam * waveCovector b) * (lam * waveCovector d)) := by
  rw [o_ricci_da_onda_com_torcao_pela_forma_fechada_do_kernel]
  simp only [Fintype.card_fin]
  norm_num

/-- [candidata] (R2) Os dois caminhos juntos: T11 (a forma fechada do kernel) mais `wave_ricci` (o Ricci de
    Levi-Civita da onda) dão, entrada a entrada, o Ricci de T3, sem usar T3. -/
theorem os_dois_caminhos_dao_o_mesmo_ricci (a c lam : ℝ) (x : Coordinate4) (b d : Fin 4) :
    coordinateRicci (conexaoDaOndaComTorcao a c lam) x b d =
      (a + c + 2 * lam ^ 2) * (waveCovector b * waveCovector d) := by
  rw [a_forma_fechada_da_onda_com_torcao_em_n4, wave_ricci]
  simp only [Matrix.smul_apply, Matrix.vecMulVec_apply, smul_eq_mul]
  ring

end

end TGLExt.TorcaoOndaCandidata

open TGLExt.TorcaoOndaCandidata in
#print axioms eta4_simetrica
open TGLExt.TorcaoOndaCandidata in
#print axioms conexaoDaOndaComTorcao
open TGLExt.TorcaoOndaCandidata in
#print axioms o_levantamento_do_vetor_da_onda
open TGLExt.TorcaoOndaCandidata in
#print axioms a_conexao_com_torcao_e_levi_civita_mais_a_contorcao_do_kernel
open TGLExt.TorcaoOndaCandidata in
#print axioms a_torcao_da_onda_e_a_tracial
open TGLExt.TorcaoOndaCandidata in
#print axioms a_torcao_da_onda_nao_e_nula
open TGLExt.TorcaoOndaCandidata in
#print axioms o_vetor_da_torcao_na_onda_e_nulo
open TGLExt.TorcaoOndaCandidata in
#print axioms o_vetor_da_torcao_e_covariantemente_constante
open TGLExt.TorcaoOndaCandidata in
#print axioms coordinatePartial_soma
open TGLExt.TorcaoOndaCandidata in
#print axioms coordinatePartial_afim
open TGLExt.TorcaoOndaCandidata in
#print axioms o_jato_da_conexao_com_torcao
open TGLExt.TorcaoOndaCandidata in
#print axioms o_ricci_da_onda_com_torcao
open TGLExt.TorcaoOndaCandidata in
#print axioms o_ricci_da_onda_chata_com_torcao
open TGLExt.TorcaoOndaCandidata in
#print axioms o_escalar_da_onda_com_torcao
open TGLExt.TorcaoOndaCandidata in
#print axioms o_einstein_da_onda_com_torcao
open TGLExt.TorcaoOndaCandidata in
#print axioms a_matriz_da_onda_nao_e_nula
open TGLExt.TorcaoOndaCandidata in
#print axioms a_onda_plana_com_torcao_e_a_onda_plana_curva
open TGLExt.TorcaoOndaCandidata in
#print axioms a_onda_chata_com_torcao_e_a_onda_curva_sem_torcao
open TGLExt.TorcaoOndaCandidata in
#print axioms amplitudeDaTorcao
open TGLExt.TorcaoOndaCandidata in
#print axioms a_onda_plana_curva_e_o_angulo_de_miguel
open TGLExt.TorcaoOndaCandidata in
#print axioms a_curvatura_do_angulo_de_miguel_nao_e_nula
open TGLExt.TorcaoOndaCandidata in
#print axioms a_equacao_de_campo_na_onda_com_torcao
open TGLExt.TorcaoOndaCandidata in
#print axioms a_equacao_de_campo_na_onda_com_torcao_reciproca
open TGLExt.TorcaoOndaCandidata in
#print axioms a_escala_que_resta_e_unica
open TGLExt.TorcaoOndaCandidata in
#print axioms nTemporal
open TGLExt.TorcaoOndaCandidata in
#print axioms conexaoChataComTorcaoTemporal
open TGLExt.TorcaoOndaCandidata in
#print axioms o_jato_da_conexao_temporal
open TGLExt.TorcaoOndaCandidata in
#print axioms o_ricci_da_torcao_temporal
open TGLExt.TorcaoOndaCandidata in
#print axioms o_escalar_da_torcao_temporal
open TGLExt.TorcaoOndaCandidata in
#print axioms o_einstein_da_torcao_temporal
open TGLExt.TorcaoOndaCandidata in
#print axioms ricciOf_e_coordinateRicci
open TGLExt.TorcaoOndaCandidata in
#print axioms a_metrica_da_onda_e_simetrica
open TGLExt.TorcaoOndaCandidata in
#print axioms a_metrica_da_onda_e_a_sua_inversa
open TGLExt.TorcaoOndaCandidata in
#print axioms a_metrica_da_onda_e_compativel
open TGLExt.TorcaoOndaCandidata in
#print axioms a_derivada_do_perfil_e_o_dobro_do_transverso
open TGLExt.TorcaoOndaCandidata in
#print axioms a_soma_da_derivada_da_inversa
open TGLExt.TorcaoOndaCandidata in
#print axioms o_ricci_da_onda_com_torcao_pela_forma_fechada_do_kernel
open TGLExt.TorcaoOndaCandidata in
#print axioms a_forma_fechada_da_onda_com_torcao_em_n4
open TGLExt.TorcaoOndaCandidata in
#print axioms a_onda_chata_e_plana
open TGLExt.TorcaoOndaCandidata in
#print axioms o_einstein_da_onda_chata_com_torcao_nao_e_nulo
open TGLExt.TorcaoOndaCandidata in
#print axioms os_dois_caminhos_dao_o_mesmo_ricci
