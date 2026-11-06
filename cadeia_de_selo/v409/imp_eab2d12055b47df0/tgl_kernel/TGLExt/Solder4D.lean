import TGLExt.NoFullWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A solda 4D: so(1,3), a marca não-compacta e a curvatura recuperada
  [TGLExt — v63, o enfrentamento solo da segunda metade do aberto]

Das duas metades do único teorema aberto (Dirac de Breuer–Fredholm + solda
4D operádica), esta pedra ataca a SEGUNDA na sua face kernelizável:

* `eta4` — a métrica de Minkowski 4D; ★ `solderMetric4_symm` +
  `solderMetric4_det` + `solder4_lorentzian` — a métrica soldada 4D é
  simétrica, `det g = −(det e)²`, e o caráter lorentziano (det < 0)
  sobrevive a QUALQUER solda invertível (a face determinante; a assinatura
  plena de Sylvester é \[KNOWN clássico, kernel OPEN]);
* os SEIS geradores de so(1,3) (boosts K₁K₂K₃, rotações J₁J₂J₃) com
  ★ `generators_in_so13` — a propriedade DEFINIDORA `XᵀΗ + ΗX = 0` provada
  para todos;
* ★ `bracket_in_so_eta` — o FECHAMENTO SOB COLCHETE para η GERAL (álgebra
  pura, qualquer dimensão): o espaço das η-antissimétricas é uma álgebra
  de Lie — a solda tem onde morar;
* ★ `so_eta_infinitesimal_isometry` — METRICIDADE: os geradores de so(η)
  são exatamente as isometrias infinitesimais de η (a face algébrica de
  `∇g = 0` para conexão so(1,3)-valuada);
* ★ `boosts_close_in_minus_rotation` + `rotations_close_in_rotation` —
  A MARCA NÃO-COMPACTA: `[K₁,K₂] = −J₃` mas `[J₁,J₂] = +J₃` — o sinal
  que distingue Lorentz de Euclides está em kernel; e o corolário físico
  ★ `boosts_curvature_is_rotation`: A CURVATURA DE DOIS BOOSTS É UMA
  ROTAÇÃO (a face algébrica da precessão de Thomas–Wigner) — o análogo
  4D do R = 2c₁c₂ do v60;
* ★ `lorentzRep_injective` — a representação 6-paramétrica é FIEL; e
  ★ `curvature4_recovered` — a curvatura 4D dos boosts determina seus
  SEIS coeficientes de forma ÚNICA (instância 4D do
  `solder_recovers_curvature`, v56);
* ★ `susy_discrete_threshold` — bônus para a PRIMEIRA metade: na face
  discreta, `H = BᴴB + c•1 ⪰ c•1` — o limiar ¼ do parceiro SUSY (v59)
  como teorema de matrizes (o espectro do contínuo começa ACIMA de ¼;
  o zero de H₋ fica isolado).

HONESTIDADE. O que segue aberto após esta pedra: a solda como CAMPO
(x-dependente, ∇e = 0 diferencial) gerada pela dinâmica de Ψ; a assinatura
plena (1,3) de Sylvester em kernel; e a metade de Breuer–Fredholm no core
semifinito genuíno — esta última é a PAREDE (a mathlib não tem traços
semifinitos/Breuer; formalizar do zero é pesquisa de meses) e vai à
Pergunta 8. β JAMAIS entra. Sem sorry, sem axiom. Negativo honesto é
resultado.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ## A — a métrica soldada 4D -/

/-- a métrica de Minkowski 4D: `η = diag(1,−1,−1,−1)`. -/
def eta4 : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal ![1, -1, -1, -1]

theorem eta4_symm : eta4ᵀ = eta4 := by
  unfold eta4
  rw [Matrix.diagonal_transpose]

theorem eta4_det : eta4.det = -1 := by
  unfold eta4
  rw [Matrix.det_diagonal]
  simp [Fin.prod_univ_four]

/-- a métrica soldada 4D: `g = eᵀ η e`. -/
def solderMetric4 (e : Matrix (Fin 4) (Fin 4) ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  eᵀ * eta4 * e

/-- [KERNEL] ★ g é simétrica. -/
theorem solderMetric4_symm (e : Matrix (Fin 4) (Fin 4) ℝ) :
    (solderMetric4 e)ᵀ = solderMetric4 e := by
  unfold solderMetric4
  rw [Matrix.transpose_mul, Matrix.transpose_mul, Matrix.transpose_transpose,
    eta4_symm, Matrix.mul_assoc]

/-- [KERNEL] ★ `det g = −(det e)²`. -/
theorem solderMetric4_det (e : Matrix (Fin 4) (Fin 4) ℝ) :
    (solderMetric4 e).det = -(e.det ^ 2) := by
  unfold solderMetric4
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose, eta4_det]
  ring

/-- [KERNEL] ★ O CARÁTER LORENTZIANO SOBREVIVE EM 4D: solda invertível ⟹
    `det g < 0` (a face determinante; Sylvester pleno = KNOWN clássico). -/
theorem solder4_lorentzian {e : Matrix (Fin 4) (Fin 4) ℝ} (he : e.det ≠ 0) :
    (solderMetric4 e).det < 0 := by
  rw [solderMetric4_det]
  have h2 : 0 < e.det * e.det := mul_self_pos.mpr he
  rw [sq]
  linarith

/-! ## B — os seis geradores de so(1,3) e a propriedade definidora -/

def K1 : Matrix (Fin 4) (Fin 4) ℝ := !![0,1,0,0; 1,0,0,0; 0,0,0,0; 0,0,0,0]
def K2 : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,1,0; 0,0,0,0; 1,0,0,0; 0,0,0,0]
def K3 : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,0,1; 0,0,0,0; 0,0,0,0; 1,0,0,0]
def J1 : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,0,0; 0,0,0,0; 0,0,0,-1; 0,0,1,0]
def J2 : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,0,0; 0,0,0,1; 0,0,0,0; 0,-1,0,0]
def J3 : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,0,0; 0,0,-1,0; 0,1,0,0; 0,0,0,0]

/-- a propriedade DEFINIDORA de so(η): `Xᵀ η + η X = 0`. -/
def InSOEta {n : Type} [Fintype n] (η X : Matrix n n ℝ) : Prop :=
  Xᵀ * η + η * X = 0

/-- [KERNEL] ★ OS SEIS GERADORES ESTÃO EM so(1,3): a propriedade definidora
    provada para todos (boosts e rotações). -/
theorem generators_in_so13 :
    InSOEta eta4 K1 ∧ InSOEta eta4 K2 ∧ InSOEta eta4 K3 ∧
    InSOEta eta4 J1 ∧ InSOEta eta4 J2 ∧ InSOEta eta4 J3 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
  · simp only [InSOEta, eta4, K1, K2, K3, J1, J2, J3]
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four,
        Matrix.diagonal_apply]

/-! ## C — o fechamento sob colchete e a metricidade (η geral) -/

/-- [KERNEL] ★ FECHAMENTO SOB COLCHETE (η GERAL, qualquer dimensão): o
    colchete de duas η-antissimétricas é η-antissimétrica — so(η) é uma
    álgebra de Lie: a solda tem onde morar. -/
theorem bracket_in_so_eta {n : Type} [Fintype n]
    {η X Y : Matrix n n ℝ} (hX : InSOEta η X) (hY : InSOEta η Y) :
    InSOEta η (X * Y - Y * X) := by
  unfold InSOEta at *
  have hX' : Xᵀ * η = -(η * X) := add_eq_zero_iff_eq_neg.mp hX
  have hY' : Yᵀ * η = -(η * Y) := add_eq_zero_iff_eq_neg.mp hY
  have step : (X * Y - Y * X)ᵀ * η + η * (X * Y - Y * X)
      = Yᵀ * (Xᵀ * η) - Xᵀ * (Yᵀ * η) + η * (X * Y) - η * (Y * X) := by
    rw [Matrix.transpose_sub, Matrix.transpose_mul, Matrix.transpose_mul]
    noncomm_ring
  rw [step, hX', hY']
  have step2 : Yᵀ * -(η * X) - Xᵀ * -(η * Y) + η * (X * Y) - η * (Y * X)
      = -((Yᵀ * η) * X) + (Xᵀ * η) * Y + η * (X * Y) - η * (Y * X) := by
    noncomm_ring
  rw [step2, hX', hY']
  noncomm_ring

/-- [KERNEL] ★ METRICIDADE: os elementos de so(η) são as ISOMETRIAS
    INFINITESIMAIS de η — `⟨Xv, ηw⟩ + ⟨v, η(Xw)⟩ = 0` (a face algébrica
    de `∇g = 0` para conexão so(1,3)-valuada). -/
theorem so_eta_infinitesimal_isometry {n : Type} [Fintype n]
    {η X : Matrix n n ℝ} (hX : InSOEta η X) (v w : n → ℝ) :
    (X.mulVec v) ⬝ᵥ (η.mulVec w) + v ⬝ᵥ (η.mulVec (X.mulVec w)) = 0 := by
  have h1 : (X.mulVec v) ⬝ᵥ (η.mulVec w) = v ⬝ᵥ ((Xᵀ * η).mulVec w) := by
    rw [dotProduct_comm, dotProduct_mulVec, ← Matrix.mulVec_transpose,
      ← Matrix.mulVec_mulVec, dotProduct_comm]
  have h2 : v ⬝ᵥ (η.mulVec (X.mulVec w)) = v ⬝ᵥ ((η * X).mulVec w) := by
    rw [Matrix.mulVec_mulVec]
  rw [h1, h2, ← dotProduct_add, ← Matrix.add_mulVec, hX]
  simp

/-! ## D — a marca não-compacta e a curvatura dos boosts -/

/-- a curvatura da conexão 4D constante: `F₁₂ = [A₁, A₂]`. -/
def curv4 (A₁ A₂ : Matrix (Fin 4) (Fin 4) ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  A₁ * A₂ - A₂ * A₁

/-- [KERNEL] ★ A MARCA NÃO-COMPACTA (metade 1): `[K₁, K₂] = −J₃` — dois
    boosts fecham em MENOS uma rotação. -/
theorem boosts_close_in_minus_rotation : curv4 K1 K2 = -J3 := by
  unfold curv4 K1 K2 J3
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_four]

/-- [KERNEL] ★ A MARCA NÃO-COMPACTA (metade 2): `[J₁, J₂] = +J₃` — duas
    rotações fecham em MAIS uma rotação. O SINAL relativo é o que separa
    Lorentz de Euclides — e ele está em kernel. -/
theorem rotations_close_in_rotation : curv4 J1 J2 = J3 := by
  unfold curv4 J1 J2 J3
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_four]

/-- [KERNEL] ★ A CURVATURA DE DOIS BOOSTS É UMA ROTAÇÃO (Thomas–Wigner,
    face algébrica): `F₁₂(c₁K₁, c₂K₂) = −c₁c₂·J₃` — o análogo 4D do
    `R = 2c₁c₂` do v60. -/
theorem boosts_curvature_is_rotation (c₁ c₂ : ℝ) :
    curv4 (c₁ • K1) (c₂ • K2) = (-(c₁ * c₂)) • J3 := by
  have h : curv4 (c₁ • K1) (c₂ • K2) = (c₁ * c₂) • curv4 K1 K2 := by
    unfold curv4
    rw [smul_mul_assoc, mul_smul_comm, smul_smul, smul_mul_assoc,
      mul_smul_comm, smul_smul, mul_comm c₂ c₁, ← smul_sub]
  rw [h, boosts_close_in_minus_rotation, smul_neg, ← neg_smul]

/-! ## E — a representação fiel e a recuperação da curvatura 4D -/

/-- a representação 6-paramétrica de so(1,3): `c ↦ Σ cᵢ Gᵢ`. -/
def lorentzRep (c : Fin 6 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  c 0 • K1 + c 1 • K2 + c 2 • K3 + c 3 • J1 + c 4 • J2 + c 5 • J3

theorem lorentzRep_zero_iff (c : Fin 6 → ℝ) :
    lorentzRep c = 0 ↔ c = 0 := by
  constructor
  · intro h
    have h01 := congrFun (congrFun h 0) 1
    have h02 := congrFun (congrFun h 0) 2
    have h03 := congrFun (congrFun h 0) 3
    have h23 := congrFun (congrFun h 2) 3
    have h13 := congrFun (congrFun h 1) 3
    have h12 := congrFun (congrFun h 1) 2
    simp [lorentzRep, K1, K2, K3, J1, J2, J3] at h01 h02 h03 h23 h13 h12
    funext i
    fin_cases i <;> simp <;> linarith
  · intro h
    rw [h]
    simp [lorentzRep]

/-- [KERNEL] ★ a representação de so(1,3) é FIEL (injetiva). -/
theorem lorentzRep_injective : Function.Injective lorentzRep := by
  intro a b hab
  have hdiff : lorentzRep (a - b) = 0 := by
    unfold lorentzRep at *
    simp only [Pi.sub_apply, sub_smul]
    rw [← sub_eq_zero] at hab
    rw [← hab]
    noncomm_ring
  have := (lorentzRep_zero_iff (a - b)).mp hdiff
  funext i
  have hi := congrFun this i
  simp at hi
  linarith

/-- [KERNEL] ★ A CURVATURA 4D RECUPERADA: a curvatura de dois boosts
    determina seus SEIS coeficientes de forma ÚNICA na representação fiel
    (a instância 4D do `solder_recovers_curvature`, v56) — e o único
    coeficiente não-nulo é a ROTAÇÃO J₃ com peso `−c₁c₂`. -/
theorem curvature4_recovered (c₁ c₂ : ℝ) :
    ∃! c : Fin 6 → ℝ, lorentzRep c = curv4 (c₁ • K1) (c₂ • K2) := by
  refine ⟨fun i => if i = 5 then -(c₁ * c₂) else 0, ?_, ?_⟩
  · rw [boosts_curvature_is_rotation]
    simp [lorentzRep]
  · intro c' hc'
    apply lorentzRep_injective
    rw [hc', boosts_curvature_is_rotation]
    simp [lorentzRep]

/-! ## F — bônus para a metade de Breuer: o limiar discreto -/

open scoped ComplexOrder MatrixOrder in
/-- [KERNEL] ★ O LIMIAR SUSY DISCRETO: `H = BᴴB + c•1 ⪰ c•1` — a face de
    matrizes do limiar ¼ (v59): o parceiro `H₊ = Laplaciano + ¼` fica
    ACIMA de ¼; o zero de `H₋` fica isolado do contínuo. -/
theorem susy_discrete_threshold {n m : Type} [Fintype n] [Fintype m]
    [DecidableEq n] (B : Matrix m n ℂ) (c : ℝ) :
    ((c : ℂ) • (1 : Matrix n n ℂ)) ≤ Bᴴ * B + (c : ℂ) • 1 := by
  rw [Matrix.le_iff, add_sub_cancel_right]
  exact Matrix.posSemidef_conjTranspose_mul_self B

end

end TGLExt
