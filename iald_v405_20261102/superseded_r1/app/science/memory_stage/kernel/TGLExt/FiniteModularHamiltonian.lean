-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 058..062 (09/09/2026), transposta em 10/09/2026 (ENTREGA_062 = elo do lote)
-- Os 77 modulos da sessao de 09/09 da bancada (cadeia de copias integradas 63 -> 72 -> 77 sobre a base v337 lida),
--   1065 teoremas declarados pela bancada. Cinco entregas espontaneas:
--   058: ATLAS GRAVITACIONAL SELECIONADO — continuidade + amostras densas + cortes racionais determinam o registro em U;
--     a leitura geometricLogReading caracteriza a sequencia booleana; a selecao por classe instancia IALDState e os
--     teoremas do Nome; o decodificador devolve classe, g, T e os pesos; Einstein do registro decodificado decorre das
--     leis de area e conservacao do registro original (jets, Levi-Civita, Ricci, Einstein preservados).
--   059: caracter completo reconstroi g/T/Einstein condicionado a area e conservacao; COLAGEM da Lambda unico nas
--     cartas compativeis; naturalidade infinitesimal de Ricci/escalar/Einstein em carta curva; potencial XX somavel
--     auto-adjunto com cauda em norma; exemplo de acoplamento atestado.
--   060: COCICLO UNITARIO INFINITO do potencial XX somavel na acao modular canonica; controle uniforme dos cortes;
--     gerador iV e ODE; grupo beta_t = Ad_u(t) o alpha_t que preserva o fator; transformacao finita de
--     Levi-Civita/Ricci/escalar/Einstein e lei de transformacao de Einstein nas sobreposicoes metricas abertas.
--   061: interacao local somavel com termos NAO comutativos (testemunha explicita); unicidade potencial <-> cociclo;
--     fase central Z^{-it} (gerador i(V - logZ I)); colagem suave selecionada -> Lambda global unico; estado perturbado
--     de Araki [DERIVED + KNOWN, analitico — NAO Lean].
--   062: seletor canonico e Born; reconstrucao do registro pelo seletor; entrelacamento angular; caracter da fase
--     relativa (duas probabilidades de interferencia recuperam a fase); estimativas de localidade de vinculo.
--   Estatuto: [REAL] o compilado; [DERIVED + KNOWN] Araki; [INPUT] R (o registro) e a origem fisica; [OPEN]
--   correspondencia fisica seletor-registro, materia/conservacao/area para os mesmos dados, atlas fisico compativel,
--   alem da classe globalmente limitada, anomalias e UV. Nenhum nome ligado a H3, area fisica ou gate.
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (INTEGRATION_RESULT 77 -> 72
--   -> 63); 77/77 hashes lidos dos bytes contra os recibos; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   77/77 contra o kernel v337, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.LikelihoodPreparedState
import TGLExt.ModularFlowAlgebra
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Tactic.NoncommRing

set_option autoImplicit false
set_option maxHeartbeats 900000
namespace ChatgptAudit.FiniteModular
open TGLExt ChatgptAudit ChatgptAudit.Cocycle030 Matrix
open scoped Matrix.Norms.Operator Kronecker
noncomputable section

local instance finiteModularNormedAlgebraRat (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance finiteModularScalarTowerRatComplex (P : SiteProfile) : IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

def levelLogHamiltonian (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  Matrix.diagonal (fun i => (Real.log (towerW P N i) : ℂ))

def levelModularUnitary (P : SiteProfile) (N : ℕ) (t : ℝ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  Matrix.diagonal (fun i => modularPhase t (Real.log (towerW P N i)))

def finiteModularHamiltonian (P : SiteProfile) (N : ℕ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  towerPi P (levelLogHamiltonian P N)

def finiteModularUnitary (P : SiteProfile) (N : ℕ) (t : ℝ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  NormedSpace.exp (((t : ℂ)*Complex.I) • finiteModularHamiltonian P N)

def levelHamiltonianCommutator (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :=
  levelLogHamiltonian P N * a - a * levelLogHamiltonian P N

theorem level_hamiltonian_selfadjoint (P : SiteProfile) (N : ℕ) :
    (levelLogHamiltonian P N)ᴴ = levelLogHamiltonian P N := by
  simp [levelLogHamiltonian]

theorem finite_hamiltonian_selfadjoint (P : SiteProfile) (N : ℕ) :
    IsSelfAdjoint (finiteModularHamiltonian P N) := by
  change star (towerPi P (levelLogHamiltonian P N)) = _
  rw [ContinuousLinearMap.star_eq_adjoint, ← towerPi_star, level_hamiltonian_selfadjoint]
  rfl

theorem finite_hamiltonian_mem_level (P : SiteProfile) (N : ℕ) :
    finiteModularHamiltonian P N ∈ levelOperatorAlgebra P N :=
  ⟨levelLogHamiltonian P N,rfl⟩

theorem finite_hamiltonian_mem_factor (P : SiteProfile) (N : ℕ) :
    finiteModularHamiltonian P N ∈ theFactorObject P :=
  towerPi_mem_factor _

theorem level_hamiltonian_exp (P : SiteProfile) (N : ℕ) (t : ℝ) :
    NormedSpace.exp (((t : ℂ)*Complex.I) • levelLogHamiltonian P N) =
      levelModularUnitary P N t := by
  rw [levelLogHamiltonian, ← Matrix.diagonal_smul, Matrix.exp_diagonal]
  congr 1
  funext i
  simp only [Pi.coe_exp, Pi.smul_apply, smul_eq_mul, ← Complex.exp_eq_exp_ℂ]
  unfold modularPhase
  congr 1
  push_cast
  ring

theorem finite_modular_unitary_eq_towerPi (P : SiteProfile) (N : ℕ) (t : ℝ) :
    finiteModularUnitary P N t = towerPi P (levelModularUnitary P N t) := by
  unfold finiteModularUnitary finiteModularHamiltonian
  rw [← towerPi_smul, ← tower_pi_exp, level_hamiltonian_exp]

theorem finite_modular_unitary_unitary (P : SiteProfile) (N : ℕ) (t : ℝ) :
    finiteModularUnitary P N t ∈ unitary (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedSpace.exp_mem_unitary_of_mem_skewAdjoint
    ((finite_hamiltonian_selfadjoint P N).smul_mem_skewAdjoint
      (by simp : star ((t : ℂ)*Complex.I) = -((t : ℂ)*Complex.I)))

theorem modular_phase_difference (t a b : ℝ) :
    modularPhase t a * modularPhase (-t) b = modularPhase t (a-b) := by
  unfold modularPhase
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

theorem level_modular_action (P : SiteProfile) (N : ℕ) (t : ℝ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    levelModularUnitary P N t * a * levelModularUnitary P N (-t) =
      flowLevel P t N a := by
  ext i j
  simp only [levelModularUnitary, Matrix.diagonal_mul, Matrix.mul_diagonal, flowLevel]
  calc
    modularPhase t (Real.log (towerW P N i)) * a i j *
        modularPhase (-t) (Real.log (towerW P N j)) =
      (modularPhase t (Real.log (towerW P N i)) *
        modularPhase (-t) (Real.log (towerW P N j))) * a i j := by ring
    _ = _ := by rw [modular_phase_difference]

theorem finite_modular_action_towerPi (P : SiteProfile) (N : ℕ) (t : ℝ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    finiteModularUnitary P N t * towerPi P a * finiteModularUnitary P N (-t) =
      towerPi P (flowLevel P t N a) := by
  rw [finite_modular_unitary_eq_towerPi, finite_modular_unitary_eq_towerPi,
    ← towerPi_mul, ← towerPi_mul, level_modular_action]

theorem finite_modular_action_eq_canonical (P : SiteProfile) (N : ℕ) (t : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ levelOperatorAlgebra P N) :
    finiteModularUnitary P N t * A * finiteModularUnitary P N (-t) =
      modularConjugation P t A := by
  rcases hA with ⟨a,rfl⟩
  rw [finite_modular_action_towerPi, modularConjugation_local]

theorem level_commutator_apply (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (i j : chainIdx N) :
    levelHamiltonianCommutator P N a i j =
      ((Real.log (towerW P N i) - Real.log (towerW P N j) : ℝ) : ℂ) * a i j := by
  simp only [levelHamiltonianCommutator, levelLogHamiltonian, Matrix.sub_apply,
    Matrix.diagonal_mul, Matrix.mul_diagonal, Complex.ofReal_sub]
  ring

theorem level_commutator_step (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    levelHamiltonianCommutator P (N+1) (towerStep a) =
      towerStep (levelHamiltonianCommutator P N a) := by
  ext ⟨i,u⟩ ⟨j,v⟩
  by_cases huv : u = v
  · subst v
    have hu : siteW (P.w (N+1)) u ≠ 0 :=
      ne_of_gt (siteW_pos (P.pos _) (P.lt_one _) u)
    simp only [level_commutator_apply, towerW,
      Real.log_mul (ne_of_gt (towerW_pos P N i)) hu,
      Real.log_mul (ne_of_gt (towerW_pos P N j)) hu,
      towerStep, Matrix.kroneckerMap_apply, Matrix.one_apply_eq, mul_one]
    push_cast
    ring
  · simp [level_commutator_apply, towerStep, Matrix.kroneckerMap_apply,
      Matrix.one_apply_ne huv]

theorem level_commutator_push (P : SiteProfile) :
    ∀ {N M : ℕ} (h : N ≤ M) (a : Matrix (chainIdx N) (chainIdx N) ℂ),
      levelHamiltonianCommutator P M (tPush h a) =
        tPush h (levelHamiltonianCommutator P N a) := by
  intro N M h a
  induction M,h using Nat.le_induction with
  | base => rw [tPush_self,tPush_self]
  | succ M hNM ih => rw [tPush_succ hNM,tPush_succ hNM,level_commutator_step,ih]

theorem tower_pi_sub (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P (a-b) = towerPi P a - towerPi P b :=
  (towerPiLinear P N).map_sub a b

theorem finite_commutator_local (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    finiteModularHamiltonian P N * towerPi P a -
        towerPi P a * finiteModularHamiltonian P N =
      towerPi P (levelHamiltonianCommutator P N a) := by
  unfold finiteModularHamiltonian levelHamiltonianCommutator
  rw [tower_pi_sub, towerPi_mul, towerPi_mul]

theorem finite_commutator_extension (P : SiteProfile) {N M : ℕ} (h : N ≤ M)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    finiteModularHamiltonian P M * towerPi P a -
        towerPi P a * finiteModularHamiltonian P M =
      finiteModularHamiltonian P N * towerPi P a -
        towerPi P a * finiteModularHamiltonian P N := by
  calc
    _ = finiteModularHamiltonian P M * towerPi P (tPush h a) -
        towerPi P (tPush h a) * finiteModularHamiltonian P M := by
      rw [towerPi_compat]
    _ = towerPi P (levelHamiltonianCommutator P M (tPush h a)) :=
      finite_commutator_local P M (tPush h a)
    _ = towerPi P (tPush h (levelHamiltonianCommutator P N a)) := by
      rw [level_commutator_push]
    _ = _ := by rw [towerPi_compat, finite_commutator_local]

theorem finite_spectator_commutes (P : SiteProfile) {N M : ℕ} (h : N ≤ M)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ levelOperatorAlgebra P N) :
    Commute (finiteModularHamiltonian P M - finiteModularHamiltonian P N) A := by
  rcases hA with ⟨a,rfl⟩
  have hc := finite_commutator_extension P h a
  change (_ - _) * _ = _ * (_ - _)
  rw [sub_mul,mul_sub]
  apply sub_eq_sub_iff_add_eq_add.mpr
  simpa only [add_comm] using sub_eq_sub_iff_add_eq_add.mp hc

theorem finite_spectator_commutes_base (P : SiteProfile) {N M : ℕ} (h : N ≤ M) :
    Commute (finiteModularHamiltonian P M - finiteModularHamiltonian P N)
      (finiteModularHamiltonian P N) :=
  finite_spectator_commutes P h _ (finite_hamiltonian_mem_level P N)

theorem finite_spectator_selfadjoint (P : SiteProfile) (N M : ℕ) :
    IsSelfAdjoint (finiteModularHamiltonian P M - finiteModularHamiltonian P N) :=
  (finite_hamiltonian_selfadjoint P M).sub (finite_hamiltonian_selfadjoint P N)

#print axioms finiteModularNormedAlgebraRat
#print axioms finiteModularScalarTowerRatComplex
#print axioms levelLogHamiltonian
#print axioms levelModularUnitary
#print axioms finiteModularHamiltonian
#print axioms finiteModularUnitary
#print axioms levelHamiltonianCommutator
#print axioms level_hamiltonian_selfadjoint
#print axioms finite_hamiltonian_selfadjoint
#print axioms finite_hamiltonian_mem_level
#print axioms finite_hamiltonian_mem_factor
#print axioms level_hamiltonian_exp
#print axioms finite_modular_unitary_eq_towerPi
#print axioms finite_modular_unitary_unitary
#print axioms modular_phase_difference
#print axioms level_modular_action
#print axioms finite_modular_action_towerPi
#print axioms finite_modular_action_eq_canonical
#print axioms level_commutator_apply
#print axioms level_commutator_step
#print axioms level_commutator_push
#print axioms tower_pi_sub
#print axioms finite_commutator_local
#print axioms finite_commutator_extension
#print axioms finite_spectator_commutes
#print axioms finite_spectator_commutes_base
#print axioms finite_spectator_selfadjoint
end
end ChatgptAudit.FiniteModular
