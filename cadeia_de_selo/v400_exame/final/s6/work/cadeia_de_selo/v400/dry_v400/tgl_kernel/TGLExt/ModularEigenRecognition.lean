-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_032 (06/09/2026), transposta em 06/09/2026
-- Lote 031..032: o OPERADOR MODULAR RELATIVO com dominio e fecho — S^0_{psi|omega}(A Omega) = A* Psi,
--   grafico relativo fechado por homeomorfismo dos graficos algebricos, dominio denso, adjunto antilinear
--   maximal, congruencia limitada (auto-adjunta, positiva) e Delta_rel = S*S com dominio, fecho,
--   auto-adjunticidade e positividade; e a COMUTACAO MODULAR: separacao de frequencias reais, reconhecimento
--   do grafico de Delta por testes fracos, B limitado auto-adjunto comutando com o fluxo preserva o dominio
--   de Delta e comuta; o filtro e o inverso preservam o dominio; IGUALDADE dos dominios de Delta relativo e
--   de referencia e igualdade dos operadores parciais (Delta_rel = produto de verossimilhanca x Delta_omega
--   como LinearPMap), positivo, auto-adjunto, fechado. Estatuto [REAL / INPUT / OPEN]: familia comutante
--   especificada (referencia 1/3,2/3; b somavel); calculo funcional/potencias relativas, identificacao
--   Connes/Araki completa, area geometrica e reconstrucao geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 12/12 + 12/12; manifestos 254/259; 2/2
--   auditores exit 0; recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao estatica no ROOT;
--   enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.PhaseFrequencySeparation
import TGLExt.ExpectationProjection

set_option autoImplicit false
set_option maxHeartbeats 400000
namespace ChatgptAudit.Commutation032
open Matrix Filter Topology Set TGLExt ChatgptAudit
noncomputable section

theorem matrix_inner_test_ext {m n E : Type} [Fintype m] [Fintype n]
    [DecidableEq m] [DecidableEq n] [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (f g : Matrix m n ℂ →ₗ[ℂ] E) (y x : E)
    (h : ∀ i j, inner ℂ (f (Matrix.single i j 1)) y=
      inner ℂ (g (Matrix.single i j 1)) x)
    (a : Matrix m n ℂ) :
    inner ℂ (f a) y=inner ℂ (g a) x := by
  rw [Matrix.matrix_eq_sum_single a]
  simp only [map_sum,sum_inner]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  have hs : Matrix.single i j (a i j)=(a i j) • Matrix.single i j (1 : ℂ) := by
    ext k l
    by_cases hij : i=k ∧ j=l <;> simp [hij]
  rw [hs,map_smul,map_smul,inner_smul_left,inner_smul_left,h i j]

def localDeltaInput (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ →ₗ[ℂ] modularSquareDomain P :=
  (levelEmbedding P N).codRestrict (modularSquareDomain P)
    (fun a => levelSpace_mem_squareDomain (P := P) (N := N) ⟨a,rfl⟩)

theorem local_delta_input_coe (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (localDeltaInput P N a : TowerHilbert P)=levelEmbedding P N a := rfl

theorem local_delta_input_single (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    towerDeltaClosed P (localDeltaInput P N (Matrix.single i j 1))=
      (localEigenvalue P N i j : ℂ) • localEigenvector P N i j :=
  delta_eigenvector N i j

theorem weak_delta_of_eigen_tests {P : SiteProfile} {x y : TowerHilbert P}
    (h : ∀ (N : ℕ) (i j : chainIdx N),
      inner ℂ (localEigenvector P N i j) y=
        inner ℂ ((localEigenvalue P N i j : ℂ) • localEigenvector P N i j) x) :
    WeakDeltaPair P x y := by
  rintro N ⟨_,a,rfl⟩
  apply matrix_inner_test_ext (levelEmbedding P N)
    ((towerDeltaClosed P).toFun.comp (localDeltaInput P N)) y x
  intro i j
  change inner ℂ (localEigenvector P N i j) y=
    inner ℂ (towerDeltaClosed P (localDeltaInput P N (Matrix.single i j 1))) x
  rw [local_delta_input_single]
  exact h N i j

theorem delta_graph_of_eigen_tests {P : SiteProfile} {x y : TowerHilbert P}
    (h : ∀ (N : ℕ) (i j : chainIdx N),
      inner ℂ (localEigenvector P N i j) y=
        inner ℂ ((localEigenvalue P N i j : ℂ) • localEigenvector P N i j) x) :
    (x,y)∈(towerDeltaClosed P).graph :=
  weak_delta_mem_graph (weak_delta_of_eigen_tests h)

theorem modular_phase_star_neg (s r : ℝ) :
    star (modularPhase (-s) r)=modularPhase s r := by
  unfold modularPhase
  rw [Complex.star_def,←Complex.exp_conj]
  congr 1
  simp only [map_mul,Complex.conj_ofReal,Complex.conj_I]
  push_cast
  ring

theorem flow_eigen_inner_frequencies (P : SiteProfile) (r : ℝ) (x : TowerHilbert P)
    (hx : ∀ s : ℝ, modularFlow P s x=modularPhase s r • x)
    (N : ℕ) (i j : chainIdx N) (s : ℝ) :
    modularPhase s r*inner ℂ (localEigenvector P N i j) x=
      modularPhase s (Real.log (localEigenvalue P N i j))*
        inner ℂ (localEigenvector P N i j) x := by
  calc
    _=inner ℂ (localEigenvector P N i j) (modularFlow P s x) := by
      rw [hx,inner_smul_right]
    _=inner ℂ (modularFlow P (-s) (localEigenvector P N i j)) x :=
      flow_inner_transport s _ x
    _=_ := by
      rw [modularFlow_eigenvector,inner_smul_left]
      change star (modularPhase (-s) (Real.log (localEigenvalue P N i j)))*
        inner ℂ (localEigenvector P N i j) x=_
      rw [modular_phase_star_neg]

theorem flow_eigen_coefficient (P : SiteProfile) (r : ℝ) (x : TowerHilbert P)
    (hx : ∀ s : ℝ, modularFlow P s x=modularPhase s r • x)
    (N : ℕ) (i j : chainIdx N) :
    inner ℂ (localEigenvector P N i j) x=0 ∨ r=Real.log (localEigenvalue P N i j) :=
  modular_phase_frequency_zero_or_equal r (Real.log (localEigenvalue P N i j))
    (inner ℂ (localEigenvector P N i j) x) (flow_eigen_inner_frequencies P r x hx N i j)

theorem flow_eigen_implies_delta_graph (P : SiteProfile) (r : ℝ) (x : TowerHilbert P)
    (hx : ∀ s : ℝ, modularFlow P s x=modularPhase s r • x) :
    (x,(Real.exp r : ℂ) • x)∈(towerDeltaClosed P).graph := by
  apply delta_graph_of_eigen_tests
  intro N i j
  rcases flow_eigen_coefficient P r x hx N i j with hc | hr
  · simp only [inner_smul_right,inner_smul_left,hc,mul_zero]
  · rw [hr,Real.exp_log (localEigenvalue_pos N i j)]
    simp only [inner_smul_right,inner_smul_left,Complex.conj_ofReal]

#print axioms matrix_inner_test_ext
#print axioms localDeltaInput
#print axioms local_delta_input_coe
#print axioms local_delta_input_single
#print axioms weak_delta_of_eigen_tests
#print axioms delta_graph_of_eigen_tests
#print axioms modular_phase_star_neg
#print axioms flow_eigen_inner_frequencies
#print axioms flow_eigen_coefficient
#print axioms flow_eigen_implies_delta_graph
end
end ChatgptAudit.Commutation032
