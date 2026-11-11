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
import TGLExt.SMatrix
import TGLExt.UnitaryStateDerivative
import TGLExt.SitePauliObservables

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.OpticalS

open Matrix TGLExt ChatgptAudit.Observable035
noncomputable section

/-- Exact displacement from identity; no small-parameter expansion. -/
def displacement {R : Type*} [Ring R] (S : R) : R := S - 1

/-- The optical balance in displacement convention. -/
def opticalBalance {R : Type*} [Ring R] [StarRing R] (S : R) : R :=
  displacement S + star (displacement S) + star (displacement S) * displacement S

theorem optical_balance_eq {R : Type*} [Ring R] [StarRing R] (S : R) :
    opticalBalance S = star S * S - 1 := by
  simp only [opticalBalance, displacement, star_sub, star_one]
  noncomm_ring

theorem optical_balance_zero_iff {R : Type*} [Ring R] [StarRing R] (S : R) :
    opticalBalance S = 0 ↔ star S * S = 1 := by
  rw [optical_balance_eq, sub_eq_zero]

theorem unitary_optical_balance {R : Type*} [Ring R] [StarRing R]
    (S : R) (hS : S ∈ unitary R) : opticalBalance S = 0 :=
  (optical_balance_zero_iff S).2 ((Unitary.mem_iff.mp hS).1)

theorem displacement_product {R : Type*} [Ring R] (S V : R) :
    displacement (S * V) =
      displacement S + displacement V + displacement S * displacement V := by
  unfold displacement
  noncomm_ring

/-- Order sensitivity survives in the exact quadratic term. -/
theorem displacement_order_difference {R : Type*} [Ring R] (S V : R) :
    displacement (S * V) - displacement (V * S) =
      displacement S * displacement V - displacement V * displacement S := by
  unfold displacement
  noncomm_ring

/-- Standard convention S = 1 + i T. -/
def transition {R : Type*} [Ring R] [Algebra ℂ R] (S : R) : R :=
  (-Complex.I) • displacement S

theorem transition_reconstructs {R : Type*} [Ring R] [Algebra ℂ R] (S : R) :
    1 + Complex.I • transition S = S := by
  simp [transition, smul_smul, displacement]

theorem transition_star {R : Type*} [Ring R] [StarRing R] [Algebra ℂ R]
    [StarModule ℂ R] (S : R) :
    star (transition S) = Complex.I • star (displacement S) := by
  simp [transition, star_smul]

theorem transition_positive_product {R : Type*} [Ring R] [StarRing R]
    [Algebra ℂ R] [StarModule ℂ R] (S : R) :
    star (transition S) * transition S =
      star (displacement S) * displacement S := by
  rw [transition_star]
  simp only [transition, smul_mul_assoc, mul_smul_comm, smul_smul]
  norm_num

/-- Exact optical identity, retaining the quadratic transition contribution. -/
theorem exact_optical_identity {R : Type*} [Ring R] [StarRing R]
    [Algebra ℂ R] [StarModule ℂ R] (S : R) (hS : S ∈ unitary R) :
    (-Complex.I) • (transition S - star (transition S)) =
      star (transition S) * transition S := by
  rw [transition_positive_product, transition_star]
  have hb := unitary_optical_balance S hS
  change displacement S + star (displacement S) +
    star (displacement S) * displacement S = 0 at hb
  calc
    (-Complex.I) • (transition S - Complex.I • star (displacement S)) =
        -(displacement S + star (displacement S)) := by
      simp only [transition, smul_sub, smul_smul]
      norm_num
      abel
    _ = star (displacement S) * displacement S -
        (displacement S + star (displacement S) +
          star (displacement S) * displacement S) := by abel
    _ = star (displacement S) * displacement S := by rw [hb]; simp

theorem transition_product {R : Type*} [Ring R] [Algebra ℂ R] (S V : R) :
    transition (S * V) =
      transition S + transition V + Complex.I • (transition S * transition V) := by
  simp only [transition, displacement_product, smul_add,
    smul_mul_assoc, mul_smul_comm, smul_smul]
  norm_num

/-- The forward matrix element equals total transition probability in that channel. -/
theorem matrix_optical_channel {n : Type*} [Fintype n] [DecidableEq n]
    (S : Matrix n n ℂ) (hS : S ∈ unitary (Matrix n n ℂ)) (j : n) :
    2 * (transition S j j).im = ∑ k, Complex.normSq (transition S k j) := by
  have hh := congrArg (fun M : Matrix n n ℂ => (M j j).re) (exact_optical_identity S hS)
  simp only [Matrix.smul_apply, smul_eq_mul, Matrix.sub_apply, Matrix.star_eq_conjTranspose,
    Matrix.conjTranspose_apply, Matrix.mul_apply] at hh
  simpa [Complex.mul_re, Complex.normSq_apply, pow_two, two_mul] using hh

/-- Direct instance on the canonical boundary S matrix. -/
theorem boundary_exact_optical (theta : ℝ) :
    (-Complex.I) • (transition (Smat theta) - star (transition (Smat theta))) =
      star (transition (Smat theta)) * transition (Smat theta) :=
  exact_optical_identity (Smat theta) (Smat_mem_unitary theta)

/-- The existing tower orbit may have noncommuting self-adjoint generators. -/
theorem tower_orbit_exact_optical (P : SiteProfile)
    (A C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : IsSelfAdjoint A) (hC : IsSelfAdjoint C) (s t : ℝ) :
    (-Complex.I) •
      (transition (operatorOrbit P A C s t) - star (transition (operatorOrbit P A C s t))) =
      star (transition (operatorOrbit P A C s t)) * transition (operatorOrbit P A C s t) :=
  exact_optical_identity _ (orbit_unitary P A C hA hC s t)

/-- A concrete instance within the existing tower, using its Pauli observables. -/
theorem pauli_orbit_exact_optical (P : SiteProfile) (n : ℕ) (s t : ℝ) :
    let S := operatorOrbit P (sitePauliX P n) (sitePauliY P n) s t
    (-Complex.I) • (transition S - star (transition S)) =
      star (transition S) * transition S :=
  tower_orbit_exact_optical P _ _ (site_pauli_x_selfadjoint P n)
    (site_pauli_y_selfadjoint P n) s t

/-- Direct nonlinear composition law on the existing noncommuting orbit. -/
theorem tower_orbit_transition_product (P : SiteProfile)
    (A C : TowerHilbert P →L[ℂ] TowerHilbert P) (s t : ℝ) :
    transition (operatorOrbit P A C s t) =
      transition (ChatgptAudit.Angular034.boundedPhase P A s) +
      transition (ChatgptAudit.Angular034.boundedPhase P C t) +
      Complex.I • (transition (ChatgptAudit.Angular034.boundedPhase P A s) *
        transition (ChatgptAudit.Angular034.boundedPhase P C t)) :=
  transition_product _ _

/-- The canonical first Taylor polynomial, used as a negative control. -/
def linearBoundary (theta : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  1 + (theta : ℂ) • Grot

theorem linear_boundary_defect (theta : ℝ) :
    (linearBoundary theta)ᴴ * linearBoundary theta =
      (1 + (theta : ℂ)^2) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [linearBoundary, Grot, Matrix.mul_apply, Fin.sum_univ_two,
      Matrix.conjTranspose_apply] <;> ring

theorem nonzero_linear_boundary_not_unitary (theta : ℝ) (ht : theta ≠ 0) :
    linearBoundary theta ∉ unitary (Matrix (Fin 2) (Fin 2) ℂ) := by
  intro h
  have he := (Unitary.mem_iff.mp h).1
  change (linearBoundary theta)ᴴ * linearBoundary theta = 1 at he
  rw [linear_boundary_defect] at he
  have hz := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℂ => M 0 0) he
  simp only [Matrix.smul_apply, Matrix.one_apply_eq, smul_eq_mul, mul_one] at hz
  have hs : (theta : ℂ)^2 = 0 := by linear_combination hz
  have hr : theta^2 = 0 := by exact_mod_cast hs
  apply ht
  nlinarith

end

#print axioms displacement
#print axioms opticalBalance
#print axioms optical_balance_eq
#print axioms optical_balance_zero_iff
#print axioms unitary_optical_balance
#print axioms displacement_product
#print axioms displacement_order_difference
#print axioms transition
#print axioms transition_reconstructs
#print axioms transition_star
#print axioms transition_positive_product
#print axioms exact_optical_identity
#print axioms transition_product
#print axioms matrix_optical_channel
#print axioms boundary_exact_optical
#print axioms tower_orbit_exact_optical
#print axioms pauli_orbit_exact_optical
#print axioms tower_orbit_transition_product
#print axioms linearBoundary
#print axioms linear_boundary_defect
#print axioms nonzero_linear_boundary_not_unitary
end ChatgptAudit.OpticalS
