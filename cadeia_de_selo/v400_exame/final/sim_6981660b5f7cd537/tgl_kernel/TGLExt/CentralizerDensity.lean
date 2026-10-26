-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_033 (06/09/2026), transposta em 06/09/2026
-- Lote 033: DENSIDADE CENTRALIZANTE, logaritmo e cociclo canonico — a algebra do centralizador de omega
--   definida sem o fluxo (fechada, soma, produto, exponencial); L, R, H e u no centralizador; densidade
--   positiva, auto-adjunta, invertivel, no fator e NORMALIZADA; logaritmo genuino e unico (CFC.log_exp);
--   potencia imaginaria limitada = cociclo, unitaria; estado da densidade e UNICIDADE da densidade no fator
--   (H, K no fator; sem supor positividade das concorrentes); controle da leitura angular (par no tempo;
--   estado de referencia invariante pelo cociclo). Estatuto [REAL / KNOWN / DERIVED / INPUT / OPEN]:
--   a identificacao de Connes e especializacao explicita de Hiai 9.4(2) [KNOWN/DERIVED], nao teorema novo
--   do kernel; Pedersen-Takesaki geral, area, retorno estabilizante e gravidade geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10; manifesto 265/265; auditor exit 0;
--   recompilacao INDEPENDENTE 3/3 apos a REGRA 3, axiomas no trio; guarda de colisao; enunciados lidos.
-- TRANSPOSICAO: cabecalho + prefixo TGLExt. + REGRA 3 (instancias LOCAIS anonimas nomeadas
--   inst_<Modulo>_<k>): Lean gerava o MESMO nome automatico (Density033.instNormedAlgebraRat...) em
--   CentralizerDensity e LikelihoodDensityLog e o ROOT nao os importa juntos; so o NOME da declaracao muda,
--   nenhuma prova. Os oleans da bancada traziam sufixos de arquivo que um compilador limpo nao gera
--   (ambiente da bancada com oleans reaproveitados) — ORDEM_008 pede instancias NOMEADAS daqui em diante.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.SummableLikelihoodGenerator
import TGLExt.LikelihoodCocycle

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace ChatgptAudit.Density033
open Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Cocycle030
  ChatgptAudit.Response028 ChatgptAudit.Thermal025
noncomputable section

local instance inst_CentralizerDensity_1 (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance inst_CentralizerDensity_2 (P : SiteProfile) : IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

theorem omega_state_add (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    omegaState P (A+B)=omegaState P A+omegaState P B := by
  simp only [omegaState,_root_.add_apply,inner_add_right]

theorem omega_state_smul (P : SiteProfile) (c : ℂ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    omegaState P (c • A)=c*omegaState P A := by
  simp only [omegaState,_root_.smul_apply,inner_smul_right]

theorem omega_centralizer_zero (P : SiteProfile) :
    (0 : TowerHilbert P →L[ℂ] TowerHilbert P)∈omegaCentralizer P := by
  refine ⟨(theFactorObject P).zero_mem,?_⟩
  intro B _
  simp

theorem omega_centralizer_one (P : SiteProfile) :
    (1 : TowerHilbert P →L[ℂ] TowerHilbert P)∈omegaCentralizer P := by
  refine ⟨(theFactorObject P).one_mem,?_⟩
  intro B _
  simp

theorem omega_centralizer_add (P : SiteProfile)
    {A C : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hA : A∈omegaCentralizer P) (hC : C∈omegaCentralizer P) :
    A+C∈omegaCentralizer P := by
  refine ⟨(theFactorObject P).add_mem hA.1 hC.1,?_⟩
  intro B hB
  rw [add_mul,mul_add,omega_state_add,omega_state_add,hA.2 B hB,hC.2 B hB]

theorem omega_centralizer_smul (P : SiteProfile) (c : ℂ)
    {A : TowerHilbert P →L[ℂ] TowerHilbert P} (hA : A∈omegaCentralizer P) :
    c • A∈omegaCentralizer P := by
  refine ⟨(theFactorObject P).toStarSubalgebra.smul_mem hA.1 c,?_⟩
  intro B hB
  rw [smul_mul_assoc,mul_smul_comm,omega_state_smul,omega_state_smul,hA.2 B hB]

theorem omega_centralizer_mul (P : SiteProfile)
    {A C : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hA : A∈omegaCentralizer P) (hC : C∈omegaCentralizer P) :
    A*C∈omegaCentralizer P := by
  refine ⟨(theFactorObject P).mul_mem hA.1 hC.1,?_⟩
  intro B hB
  calc
    omegaState P ((A*C)*B)=omegaState P (A*(C*B)) := by rw [mul_assoc]
    _=omegaState P ((C*B)*A) :=
      hA.2 (C*B) ((theFactorObject P).mul_mem hC.1 hB)
    _=omegaState P (C*(B*A)) := by rw [mul_assoc]
    _=omegaState P ((B*A)*C) :=
      hC.2 (B*A) ((theFactorObject P).mul_mem hB hA.1)
    _=omegaState P (B*(A*C)) := by rw [mul_assoc]

def omegaCentralizerAlgebra (P : SiteProfile) :
    Subalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) where
  carrier := omegaCentralizer P
  zero_mem' := omega_centralizer_zero P
  one_mem' := omega_centralizer_one P
  add_mem' := by
    intro A C hA hC
    exact omega_centralizer_add P hA hC
  mul_mem' := by
    intro A C hA hC
    exact omega_centralizer_mul P hA hC
  algebraMap_mem' := by
    intro c
    rw [Algebra.algebraMap_eq_smul_one]
    exact omega_centralizer_smul P c (omega_centralizer_one P)

theorem omega_centralizer_algebra_membership (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    A∈omegaCentralizerAlgebra P ↔
      A∈theFactorObject P ∧ ∀ B∈theFactorObject P, omegaState P (A*B)=omegaState P (B*A) :=
  Iff.rfl

theorem omega_centralizer_algebra_closed (P : SiteProfile) :
    IsClosed (omegaCentralizerAlgebra P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :=
  centralizer_norm_closed P

theorem omega_centralizer_exp_mem (P : SiteProfile)
    {A : TowerHilbert P →L[ℂ] TowerHilbert P} (hA : A∈omegaCentralizer P) :
    NormedSpace.exp A∈omegaCentralizer P :=
  NormedSpace.exp_mem (R := ℂ) (s := omegaCentralizerAlgebra P)
    (omega_centralizer_algebra_closed P) hA

theorem likelihood_term_mem_centralizer (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    likelihoodTerm b t n∈omegaCentralizer thirdThermalReference :=
  site_likelihood_mem_centralizer thirdThermalReference n (b.value n*regularParameter t)

theorem likelihood_prefix_mem_centralizer (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    likelihoodPrefix b t N∈omegaCentralizer thirdThermalReference := by
  change (∑ n∈Finset.range (N+1), likelihoodTerm b t n)∈
    omegaCentralizerAlgebra thirdThermalReference
  exact sum_mem (fun n _ => likelihood_term_mem_centralizer b t n)

theorem likelihood_generator_mem_centralizer (b : SummableAmplitude) (t : ℝ) :
    likelihoodGenerator b t∈omegaCentralizer thirdThermalReference :=
  (centralizer_norm_closed thirdThermalReference).mem_of_tendsto
    (likelihood_prefix_tendsto b t)
    (Filter.Eventually.of_forall (fun N => likelihood_prefix_mem_centralizer b t N))

theorem likelihood_filter_mem_centralizer (b : SummableAmplitude) (t : ℝ) :
    likelihoodFilter b t∈omegaCentralizer thirdThermalReference :=
  omega_centralizer_exp_mem thirdThermalReference
    (omega_centralizer_smul thirdThermalReference (1/2 : ℂ)
      (likelihood_generator_mem_centralizer b t))

theorem likelihood_density_mem_centralizer (b : SummableAmplitude) (t : ℝ) :
    NormedSpace.exp (likelihoodGenerator b t)∈omegaCentralizer thirdThermalReference :=
  omega_centralizer_exp_mem thirdThermalReference (likelihood_generator_mem_centralizer b t)

theorem likelihood_cocycle_mem_centralizer (b : SummableAmplitude) (t s : ℝ) :
    likelihoodCocycle b t s∈omegaCentralizer thirdThermalReference :=
  omega_centralizer_exp_mem thirdThermalReference
    (omega_centralizer_smul thirdThermalReference ((s : ℂ)*Complex.I)
      (likelihood_generator_mem_centralizer b t))

#print axioms omega_state_add
#print axioms omega_state_smul
#print axioms omega_centralizer_zero
#print axioms omega_centralizer_one
#print axioms omega_centralizer_add
#print axioms omega_centralizer_smul
#print axioms omega_centralizer_mul
#print axioms omegaCentralizerAlgebra
#print axioms omega_centralizer_algebra_membership
#print axioms omega_centralizer_algebra_closed
#print axioms omega_centralizer_exp_mem
#print axioms likelihood_term_mem_centralizer
#print axioms likelihood_prefix_mem_centralizer
#print axioms likelihood_generator_mem_centralizer
#print axioms likelihood_filter_mem_centralizer
#print axioms likelihood_density_mem_centralizer
#print axioms likelihood_cocycle_mem_centralizer

end
end ChatgptAudit.Density033
