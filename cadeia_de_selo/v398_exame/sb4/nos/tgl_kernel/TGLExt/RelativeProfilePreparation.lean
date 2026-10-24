-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_026 (06/09/2026), transposta em 06/09/2026
-- Lote 024..026: a perturbacao de GIBBS realizada no mesmo Hilbert da torre (estado fiel,
--   normalizado, distinto da orbita modular; resposta quadratica; calor/fonte por normalizacao);
--   o LIMITE TERMICO: para perfil constante nao tracial a preparacao NAO tem limite em norma
--   (nao-Cauchy) e o acoplamento da torre e ilimitado; corte com escala escolhida; AFINIDADE:
--   criterio exato (Cauchy <=> afinidade-limite > 0), estado global no Hilbert original, fiel e
--   ciclico; perfil gradual (muda em infinitos sitios, ainda fiel). Estatuto [REAL / INPUT / OPEN]:
--   selecao fisica, area, H3 dinamico, dimensao/assinatura, globalizacao e a classificacao geral
--   dos estados normais (disjuncao) seguem INPUT/OPEN — a bancada NAO promoveu nao-Cauchy a teorema
--   geral de disjuncao nem importou Kakutani.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100%; manifestos 202/206/220;
--   3/3 auditores da bancada exit 0; recompilacao INDEPENDENTE 22/22, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ThermalLimitControls
import TGLExt.SignatureInTheLimit

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Profile026
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024 ChatgptAudit.Thermal025
open scoped ComplexOrder Kronecker
noncomputable section

def relativeFilter {ι : Type} [DecidableEq ι] (p q : ι → ℝ) : Matrix ι ι ℂ :=
  Matrix.diagonal (fun i => (Real.sqrt (q i/p i) : ℂ))

def profileVector (P Q : SiteProfile) (N : ℕ) : TowerHilbert P :=
  towerPi P (relativeFilter (towerW P N) (towerW Q N)) (hOmega P)

def profileState (P Q : SiteProfile) (N : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) : ℂ :=
  inner ℂ (profileVector P Q N) (A (profileVector P Q N))

theorem relative_filter_self_adjoint {ι : Type} [DecidableEq ι] (p q : ι → ℝ) :
    (relativeFilter p q)ᴴ=relativeFilter p q := by
  ext i j
  by_cases hij : i=j
  · subst j; simp [relativeFilter]
  · simp [relativeFilter,Matrix.conjTranspose_apply,Matrix.diagonal_apply_ne _ hij,
      Matrix.diagonal_apply_ne _ (Ne.symm hij)]

theorem relative_weighted_square (p q : ℝ) (hp : 0<p) (hq : 0≤q) :
    p*(Real.sqrt (q/p))^2=q := by
  rw [Real.sq_sqrt (div_nonneg hq hp.le)]
  field_simp [ne_of_gt hp]

theorem relative_amplitude_product (p q r z : ℝ) (hp : 0<p) (hq : 0≤q) :
    Real.sqrt ((q*z)/(p*r))=Real.sqrt (q/p)*Real.sqrt (z/r) := by
  rw [show (q*z)/(p*r)=(q/p)*(z/r) from (div_mul_div_comm q p z r).symm]
  exact Real.sqrt_mul (div_nonneg hq hp.le) _

theorem relative_filter_product {ι κ : Type} [DecidableEq ι] [DecidableEq κ]
    (p q : ι → ℝ) (r z : κ → ℝ) (hp : ∀ i, 0<p i) (hq : ∀ i, 0≤q i) :
    relativeFilter (productWeights p r) (productWeights q z)=
      (relativeFilter p q) ⊗ₖ (relativeFilter r z) := by
  rw [relativeFilter,relativeFilter,relativeFilter,Matrix.diagonal_kronecker_diagonal]
  congr 1
  funext x
  simp only [productWeights,relative_amplitude_product _ _ _ _ (hp _) (hq _),Complex.ofReal_mul]

theorem relative_filter_local_state {ι : Type} [Fintype ι] [DecidableEq ι]
    (p q : ι → ℝ) (hp : ∀ i, 0<p i) (hq : ∀ i, 0≤q i) (a : Matrix ι ι ℂ) :
    (∑ i, (p i:ℂ)*((relativeFilter p q)ᴴ*a*relativeFilter p q) i i)=
      ∑ i, (q i:ℂ)*a i i := by
  rw [relative_filter_self_adjoint]
  apply Finset.sum_congr rfl
  intro i _
  have hc : (p i:ℂ)*(Real.sqrt (q i/p i):ℂ)^2=(q i:ℂ) := by
    exact_mod_cast relative_weighted_square (p i) (q i) (hp i) (hq i)
  simp only [relativeFilter,Matrix.diagonal_mul,Matrix.mul_diagonal]
  calc
    (p i:ℂ)*((Real.sqrt (q i/p i):ℂ)*a i i*(Real.sqrt (q i/p i):ℂ))=
      ((p i:ℂ)*(Real.sqrt (q i/p i):ℂ)^2)*a i i := by ring
    _=_ := by rw [hc]

theorem profile_state_local (P Q : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileState P Q N (towerPi P a)=tState Q N a := by
  change inner ℂ (towerPi P _ (hOmega P)) (towerPi P a (towerPi P _ (hOmega P)))=_
  rw [←mul_apply_eq_comp,←towerPi_mul,tower_local_vectors_inner P (le_refl N),
    tPush_self,tInner]
  simpa only [tState,mul_assoc] using
    relative_filter_local_state (towerW P N) (towerW Q N) (towerW_pos P N)
      (fun i => (towerW_pos Q N i).le) a

theorem profile_state_one (P Q : SiteProfile) (N : ℕ) : profileState P Q N 1=1 := by
  rw [←towerPi_one (P := P) N,profile_state_local,tState_one]

theorem profile_vector_norm (P Q : SiteProfile) (N : ℕ) : ‖profileVector P Q N‖=1 := by
  have hh := profile_state_one P Q N
  change inner ℂ (profileVector P Q N) (profileVector P Q N)=1 at hh
  have hn : ‖profileVector P Q N‖^2=1 := by
    rw [norm_sq_eq_re_inner (𝕜 := ℂ),hh]; rfl
  nlinarith [norm_nonneg (profileVector P Q N)]

theorem profile_state_marginal (P Q : SiteProfile) {L N : ℕ} (hLN : L≤N)
    (a : Matrix (chainIdx L) (chainIdx L) ℂ) :
    profileState P Q N (towerPi P a)=tState Q L a := by
  rw [←towerPi_compat hLN a,profile_state_local,tState_tPush]

theorem profile_omega_overlap (P Q : SiteProfile) (N : ℕ) :
    inner ℂ (hOmega P) (profileVector P Q N)=
      (diagonalAffinity (towerW P N) (towerW Q N):ℂ) := by
  change omegaState P (towerPi P (relativeFilter _ _))=_
  rw [omegaState_pi]
  simp only [tState,relativeFilter,Matrix.diagonal_apply_eq,←Complex.ofReal_mul,
    weighted_sqrt_ratio _ _ (towerW_pos P N _) (towerW_pos Q N _).le,
    ←Complex.ofReal_sum,diagonalAffinity]

theorem relative_filter_reverse {ι : Type} [Fintype ι] [DecidableEq ι]
    (p q : ι → ℝ) (hp : ∀ i, 0<p i) (hq : ∀ i, 0<q i) :
    relativeFilter p q*relativeFilter q p=1 := by
  rw [relativeFilter,relativeFilter,Matrix.diagonal_mul_diagonal,←Matrix.diagonal_one]
  congr 1
  funext i
  have he : Real.sqrt (q i/p i)*Real.sqrt (p i/q i)=1 := by
    rw [←Real.sqrt_mul (div_pos (hq i) (hp i)).le]
    have hr : q i/p i*(p i/q i)=1 := by field_simp [ne_of_gt (hp i),ne_of_gt (hq i)]
    rw [hr,Real.sqrt_one]
  exact_mod_cast he

theorem relative_filter_positive {ι : Type} [Fintype ι] [DecidableEq ι]
    (p q : ι → ℝ) (hp : ∀ i, 0<p i) (hq : ∀ i, 0<q i) :
    (relativeFilter p q).PosDef := by
  rw [relativeFilter,Matrix.posDef_diagonal_iff]
  intro i
  exact Complex.zero_lt_real.mpr (Real.sqrt_pos.mpr (div_pos (hq i) (hp i)))

#print axioms relative_filter_self_adjoint
#print axioms relative_weighted_square
#print axioms relative_amplitude_product
#print axioms relative_filter_product
#print axioms relative_filter_local_state
#print axioms profile_state_local
#print axioms profile_state_one
#print axioms profile_vector_norm
#print axioms profile_state_marginal
#print axioms profile_omega_overlap
#print axioms relative_filter_reverse
#print axioms relative_filter_positive
end
end ChatgptAudit.Profile026
