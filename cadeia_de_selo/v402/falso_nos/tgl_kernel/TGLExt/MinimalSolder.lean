import TGLExt.GeometryFluctuation
import TGLExt.ContinuousModularZero

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A solda 2D mínima: onde o transporte vira geometria
  [TGLExt — v60, o primeiro passo geométrico genuíno]

O aberto da Resposta 7 tinha duas metades: o Dirac de Breuer–Fredholm e a
solda MULTIDIMENSIONAL ("uma curvatura gravitacional exige uma base com pelo
menos duas direções"). Esta pedra fecha a FACE MÍNIMA da segunda metade:

* ★ `minimal_curvature` — a curvatura da conexão 2D mínima (constante,
  não-abeliana, sobre as polarizações do gráviton): `F₁₂ = [A₁, A₂] =
  2c₁c₂ • J` — a curvatura FECHA no gerador de helicidade (v49);
* ★ `minimal_curvature_ne_zero` — **A GRAVIDADE LIGA**: `c₁c₂ ≠ 0 ⟹ F ≠ 0`
  (duas direções + geradores não-comutantes bastam); e o controle
  `curvature_flat_same` (mesmo gerador ⟹ plano — sem contraste de direção
  não há curvatura, o par do `excite_holonomy_flat`/`absoluteOne_flow_trivial`);
* ★ a SOLDA e a métrica: `g = eᵀ η e` com `η = polPlus` (**a
  polarização-mais É a métrica de Minkowski 2D** — a coincidência
  estrutural da casa): `solderMetric_symm` (g simétrica),
  `solderMetric_det` (`det g = −(det e)²`) e ★ `solder_lorentzian` — **o
  caráter lorentziano sobrevive a QUALQUER solda invertível** (det g < 0);
* ★ `minimal_curvature_recovered` — **A PRIMEIRA CURVATURA GRAVITACIONAL
  RECUPERADA EM KERNEL**: com a representação de helicidade
  `ρ*(r) = r • J` (injetiva), existe UM ÚNICO escalar `R` com
  `ρ*(R) = F₁₂`, e ele é `R = 2c₁c₂` — em 2D o tensor de Riemann tem
  exatamente 1 componente independente, e ela emerge da inscrição em duas
  direções (a instância trabalhada do `solder_recovers_curvature`, v56).

HONESTIDADE. Isto fecha a solda na sua face MÍNIMA (2D, conexão constante,
curvatura escalar). O que segue aberto: a solda 4D operádica GERADA pela
dinâmica de Ψ (com ∇e = 0 e representação fiel de so(1,3)) e o
`continuousModularDirac_isBreuerFredholm` (a outra metade). β JAMAIS entra.
Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ## A — a curvatura da conexão 2D mínima -/

/-- a curvatura da conexão CONSTANTE em duas direções: `F₁₂ = [A₁, A₂]`
    (os termos ∂ anulam-se para conexão constante; resta o não-abeliano). -/
def curv2 (A₁ A₂ : Matrix (Fin 2) (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  A₁ * A₂ - A₂ * A₁

/-- [KERNEL] ★ A CURVATURA MÍNIMA: para a conexão sobre as polarizações do
    gráviton, `F₁₂ = 2c₁c₂ • J` — a curvatura fecha no gerador de
    helicidade. -/
theorem minimal_curvature (c₁ c₂ : ℝ) :
    curv2 (c₁ • polPlus) (c₂ • polCross) = (2 * c₁ * c₂) • rotGen := by
  have h : curv2 (c₁ • polPlus) (c₂ • polCross)
      = (c₁ * c₂) • (polPlus * polCross - polCross * polPlus) := by
    unfold curv2
    rw [smul_mul_assoc, mul_smul_comm, smul_smul, smul_mul_assoc,
      mul_smul_comm, smul_smul, mul_comm c₂ c₁, ← smul_sub]
  rw [h, polarization_commutator, smul_smul]
  congr 1
  ring

/-- [KERNEL] ★ A GRAVIDADE LIGA: `c₁c₂ ≠ 0 ⟹ F₁₂ ≠ 0` — duas direções com
    geradores não-comutantes bastam para curvatura não-nula. -/
theorem minimal_curvature_ne_zero {c₁ c₂ : ℝ} (h : c₁ * c₂ ≠ 0) :
    curv2 (c₁ • polPlus) (c₂ • polCross) ≠ 0 := by
  rw [minimal_curvature]
  intro h0
  rcases smul_eq_zero.mp h0 with hc | hJ
  · have : (2 : ℝ) * (c₁ * c₂) = 0 := by linarith [hc]
    exact h (by linarith [mul_eq_zero.mp this |>.resolve_left two_ne_zero])
  · have hent := congrFun (congrFun hJ 0) 1
    simp [rotGen] at hent

/-- [KERNEL] O CONTROLE PLANO: um só gerador (sem contraste de direção)
    dá curvatura ZERO — sem a segunda direção não há gravidade. -/
theorem curvature_flat_same (c₁ c₂ : ℝ) (A : Matrix (Fin 2) (Fin 2) ℝ) :
    curv2 (c₁ • A) (c₂ • A) = 0 := by
  unfold curv2
  rw [smul_mul_assoc, mul_smul_comm, smul_smul, smul_mul_assoc,
    mul_smul_comm, smul_smul, mul_comm c₂ c₁, ← smul_sub, sub_self, smul_zero]

/-! ## B — a solda e a métrica lorentziana emergente -/

/-- a métrica soldada: `g = eᵀ η e` com `η = polPlus = diag(1,−1)` — a
    polarização-mais É a métrica de Minkowski 2D. -/
def solderMetric (e : Matrix (Fin 2) (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  eᵀ * polPlus * e

/-- [KERNEL] ★ a métrica soldada é SIMÉTRICA. -/
theorem solderMetric_symm (e : Matrix (Fin 2) (Fin 2) ℝ) :
    (solderMetric e)ᵀ = solderMetric e := by
  unfold solderMetric
  rw [Matrix.transpose_mul, Matrix.transpose_mul, Matrix.transpose_transpose,
    polPlus_symm, Matrix.mul_assoc]

/-- [KERNEL] ★ `det g = −(det e)²`: a não-degenerescência da métrica EMERGE
    da invertibilidade da solda. -/
theorem solderMetric_det (e : Matrix (Fin 2) (Fin 2) ℝ) :
    (solderMetric e).det = -(e.det ^ 2) := by
  unfold solderMetric
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose]
  have hη : polPlus.det = -1 := by
    simp [polPlus, Matrix.det_fin_two]
  rw [hη]
  ring

/-- [KERNEL] ★ O CARÁTER LORENTZIANO SOBREVIVE A QUALQUER SOLDA INVERTÍVEL:
    `det e ≠ 0 ⟹ det g < 0` — a assinatura indefinida (lorentziana em 2D)
    não é escolha: é herança estrutural da solda. -/
theorem solder_lorentzian {e : Matrix (Fin 2) (Fin 2) ℝ} (he : e.det ≠ 0) :
    (solderMetric e).det < 0 := by
  rw [solderMetric_det]
  have h2 : 0 < e.det * e.det := mul_self_pos.mpr he
  rw [sq]
  linarith

/-! ## C — a recuperação: R = 2c₁c₂ (a primeira curvatura em kernel) -/

/-- a representação da curvatura no gerador de helicidade: `ρ*(r) = r • J`. -/
def helicityRep : ℝ →ₗ[ℝ] Matrix (Fin 2) (Fin 2) ℝ where
  toFun r := r • rotGen
  map_add' := fun a b => add_smul a b rotGen
  map_smul' := fun c a => by simp [smul_smul]

/-- [KERNEL] ★ a representação de helicidade é FIEL (injetiva). -/
theorem helicityRep_injective : Function.Injective helicityRep := by
  intro a b hab
  have h : (a - b) • rotGen = 0 := by
    rw [sub_smul, sub_eq_zero]
    exact hab
  rcases smul_eq_zero.mp h with h0 | hJ
  · exact sub_eq_zero.mp h0
  · exfalso
    have hent := congrFun (congrFun hJ 0) 1
    simp [rotGen] at hent

/-- [KERNEL] ★ A PRIMEIRA CURVATURA GRAVITACIONAL RECUPERADA EM KERNEL:
    existe UM ÚNICO escalar `R` com `ρ*(R) = F₁₂`, e ele é `R = 2c₁c₂` —
    em 2D o Riemann tem exatamente 1 componente independente, e ela emerge
    da inscrição em duas direções (instância do v56). -/
theorem minimal_curvature_recovered (c₁ c₂ : ℝ) :
    ∃! R : ℝ, helicityRep R = curv2 (c₁ • polPlus) (c₂ • polCross) := by
  refine ⟨2 * c₁ * c₂, ?_, ?_⟩
  · show (2 * c₁ * c₂) • rotGen = _
    rw [minimal_curvature]
  · intro R' hR'
    apply helicityRep_injective
    rw [hR']
    show _ = (2 * c₁ * c₂) • rotGen
    rw [minimal_curvature]

end

end TGLExt
