import TGLExt.Cocycle
import TGLExt.TheFlowLawContrast
set_option autoImplicit false

/-!
Candidata da gerencia c1 (02/11/2026). Nome provisorio: o nome e do operador. Fora do kernel selado.

O documento H3c beta-pago (22/06/2026, A Ponte e o Um) escreve a invariancia projetiva
`T(P) / Tr T(P) = P`: a atencao permanece identica, nao inteira. Aqui o caso em que `P` e modo proprio
do transporte, com o peso da familia do kernel. Isto NAO prova o H3c: que `P` seja modo proprio e
HIPOTESE embutida em `transporte`. O que se prova e so isto: o igual quebra no peso bruto, volta ao
dividir pelo traco, e esse denominador e o mesmo da lei da taxa local.
-/

namespace TGLExt.OIgualRestauradoCandidata

open TGLExt TGLExt.TheFlowLawContrast

noncomputable section

variable {n : Type} [Fintype n]

/-- o transporte no setor observado: o peso cai, a forma fica. -/
def transporte (β : ℝ) (g : ℝ → ℝ) (N : ℝ) (P : Matrix n n ℂ) : Matrix n n ℂ :=
  ((survivingWeightContrast β g N : ℝ) : ℂ) • P

/-- o traco do transporte e o peso sobrevivente. -/
theorem o_traco_e_o_peso (β : ℝ) (g : ℝ → ℝ) (N : ℝ) (P : Matrix n n ℂ) (h : P.trace = 1) :
    (transporte β g N P).trace = ((survivingWeightContrast β g N : ℝ) : ℂ) := by
  unfold transporte
  rw [Matrix.trace_smul, h, smul_eq_mul, mul_one]

/-- dividir pelo traco devolve `P`: o igual volta depois do custo. -/
theorem o_igual_volta (β : ℝ) (g : ℝ → ℝ) (N : ℝ) (P : Matrix n n ℂ) (h : P.trace = 1) :
    ((transporte β g N P).trace)⁻¹ • transporte β g N P = P := by
  rw [o_traco_e_o_peso β g N P h]
  unfold transporte
  have hw : ((survivingWeightContrast β g N : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast (survivingWeightContrast_pos β g N).ne'
  rw [smul_smul, inv_mul_cancel₀ hw, one_smul]

/-- com custo acumulado nao nulo, o peso nao e 1. -/
theorem o_peso_nao_e_um (β : ℝ) (g : ℝ → ℝ) (N : ℝ) (hN : N ≠ 0)
    (hA : β * accumulatedContrast g N ≠ 0) : survivingWeightContrast β g N ≠ 1 := by
  rw [survivingWeightContrast_eq β g N hN]
  intro h
  have h0 := (Real.exp_eq_one_iff _).mp h
  exact hA (by linarith)

/-- com peso diferente de 1, o transporte bruto nao e `P`: o igual quebra. -/
theorem o_igual_quebra (β : ℝ) (g : ℝ → ℝ) (N : ℝ) (P : Matrix n n ℂ) (h : P.trace = 1)
    (hw : survivingWeightContrast β g N ≠ 1) : transporte β g N P ≠ P := by
  intro he
  have ht := o_traco_e_o_peso β g N P h
  rw [he, h] at ht
  apply hw
  exact_mod_cast ht.symm

/-- o fator que devolve `P` e o fator da lei: a taxa local e a de fundo vezes o inverso do traco. -/
theorem o_mesmo_denominador (β Hcmb : ℝ) (g : ℝ → ℝ) (N : ℝ) (P : Matrix n n ℂ) (h : P.trace = 1) :
    ((H0localContrast β Hcmb g N : ℝ) : ℂ) = (Hcmb : ℂ) * ((transporte β g N P).trace)⁻¹ := by
  rw [o_traco_e_o_peso β g N P h]
  unfold H0localContrast
  push_cast
  rw [div_eq_mul_inv]

/-- o que sai do setor fica no todo: com o complemento posto em `Q`, o traco total segue 1. -/
theorem o_todo_fica (β : ℝ) (g : ℝ → ℝ) (N : ℝ) (P Q : Matrix n n ℂ) (hP : P.trace = 1)
    (hQ : Q.trace = 1) :
    (transporte β g N P + ((1 - survivingWeightContrast β g N : ℝ) : ℂ) • Q).trace = 1 := by
  rw [Matrix.trace_add, o_traco_e_o_peso β g N P hP, Matrix.trace_smul, hQ, smul_eq_mul, mul_one]
  push_cast
  ring

end

end TGLExt.OIgualRestauradoCandidata

#print axioms TGLExt.OIgualRestauradoCandidata.o_traco_e_o_peso
#print axioms TGLExt.OIgualRestauradoCandidata.o_igual_volta
#print axioms TGLExt.OIgualRestauradoCandidata.o_peso_nao_e_um
#print axioms TGLExt.OIgualRestauradoCandidata.o_igual_quebra
#print axioms TGLExt.OIgualRestauradoCandidata.o_mesmo_denominador
#print axioms TGLExt.OIgualRestauradoCandidata.o_todo_fica
