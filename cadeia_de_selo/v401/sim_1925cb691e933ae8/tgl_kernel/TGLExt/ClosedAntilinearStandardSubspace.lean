-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_049 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import Mathlib.Analysis.InnerProductSpace.StandardSubspace
import Mathlib.LinearAlgebra.LinearPMap
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 800000

open Complex ClosedSubmodule
open scoped ComplexInnerProductSpace

namespace ChatgptAudit.Continuous049
noncomputable section
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
variable (D : Submodule ℂ H) (S : D →ₛₗ[starRingEnd ℂ] H)

/-- Fixed vectors of a partially defined antilinear map, as a real submodule. -/
def fixedRealSubmodule : Submodule ℝ H where
  carrier := {x | ∃ hx : x ∈ D, S ⟨x, hx⟩ = x}
  zero_mem' := ⟨D.zero_mem, map_zero S⟩
  add_mem' := by
    rintro x y ⟨hx, hSx⟩ ⟨hy, hSy⟩
    refine ⟨D.add_mem hx hy, ?_⟩
    change S (⟨x, hx⟩ + ⟨y, hy⟩) = x + y
    rw [map_add, hSx, hSy]
  smul_mem' := by
    rintro c x ⟨hx, hSx⟩
    refine ⟨D.smul_mem (c : ℂ) hx, ?_⟩
    change S ((c : ℂ) • (⟨x, hx⟩ : D)) = c • x
    rw [map_smulₛₗ, hSx]
    simp

theorem mem_fixedRealSubmodule_iff (x : H) :
    x ∈ fixedRealSubmodule D S ↔ ∃ hx : x ∈ D, S ⟨x, hx⟩ = x := Iff.rfl

theorem fixedRealSubmodule_closed
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H), S x)))) :
    IsClosed (fixedRealSubmodule D S : Set H) := by
  have heq : (fixedRealSubmodule D S : Set H) =
      (fun x : H => (x, x)) ⁻¹' Set.range (fun x : D => ((x : H), S x)) := by
    ext x
    constructor
    · rintro ⟨hx, hSx⟩
      exact ⟨⟨x, hx⟩, Prod.ext rfl hSx⟩
    · rintro ⟨y, hy⟩
      have hxy : (y : H) = x := congrArg Prod.fst hy
      subst x
      exact ⟨y.property, congrArg Prod.snd hy⟩
  rw [heq]
  exact hclosed.preimage (continuous_id.prodMk continuous_id)

/-- Closed real fixed space; only closedness of the partial graph is used here. -/
def fixedClosedSubmodule
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H), S x)))) :
    ClosedSubmodule ℝ H :=
  ⟨fixedRealSubmodule D S, fixedRealSubmodule_closed D S hclosed⟩

/-- Regard S as a semilinear endomorphism of its invariant domain. -/
def domainConjugation (hmaps : ∀ x : D, S x ∈ D) : D →ₛₗ[starRingEnd ℂ] D where
  toFun x := ⟨S x, hmaps x⟩
  map_add' x y := Subtype.ext (map_add S x y)
  map_smul' c x := Subtype.ext (map_smulₛₗ S c x)

theorem domainConjugation_involutive
    (hmaps : ∀ x : D, S x ∈ D)
    (hinv : ∀ x : D, S ⟨S x, hmaps x⟩ = (x : H)) :
    Function.Involutive (domainConjugation D S hmaps) := by
  intro x
  exact Subtype.ext (hinv x)

theorem domain_fixed_decomposition
    (hmaps : ∀ x : D, S x ∈ D)
    (hinv : ∀ x : D, S ⟨S x, hmaps x⟩ = (x : H)) (x : D) :
    ∃ h k : H, h ∈ fixedRealSubmodule D S ∧ k ∈ fixedRealSubmodule D S ∧
      (x : H) = h + I • k ∧ S x = h - I • k := by
  let R := domainConjugation D S hmaps
  have hRR : R (R x) = x := domainConjugation_involutive D S hmaps hinv x
  let h : D := (1 / 2 : ℂ) • (x + R x)
  let k : D := (-I / 2 : ℂ) • (x - R x)
  have hRh : R h = h := by
    dsimp [h]
    rw [map_smulₛₗ, map_add, hRR]
    simp only [map_div₀, map_one, map_ofNat]
    module
  have hRk : R k = k := by
    dsimp [k]
    rw [map_smulₛₗ, map_sub, hRR]
    have hc : (starRingEnd ℂ) (-I / 2) = I / 2 := by
      simp only [map_div₀, map_neg, map_ofNat, Complex.conj_I, neg_neg]
    rw [hc]
    module
  refine ⟨h, k, ⟨h.property, congrArg Subtype.val hRh⟩,
    ⟨k.property, congrArg Subtype.val hRk⟩, ?_, ?_⟩
  · change (x : H) = (1 / 2 : ℂ) • ((x : H) + S x) +
      I • ((-I / 2 : ℂ) • ((x : H) - S x))
    rw [smul_smul]
    have hc : (I : ℂ) * (-I / 2) = 1 / 2 := by
      ring_nf
      norm_num
    rw [hc]
    module
  · change S x = (1 / 2 : ℂ) • ((x : H) + S x) -
      I • ((-I / 2 : ℂ) • ((x : H) - S x))
    rw [smul_smul]
    have hc : (I : ℂ) * (-I / 2) = 1 / 2 := by
      ring_nf
      norm_num
    rw [hc]
    module

theorem mem_domain_iff_fixed_sum
    (hmaps : ∀ x : D, S x ∈ D)
    (hinv : ∀ x : D, S ⟨S x, hmaps x⟩ = (x : H)) (x : H) :
    x ∈ D ↔ ∃ h k : H, h ∈ fixedRealSubmodule D S ∧
      k ∈ fixedRealSubmodule D S ∧ x = h + I • k := by
  constructor
  · intro hx
    obtain ⟨h, k, hh, hk, hsum, _⟩ := domain_fixed_decomposition D S hmaps hinv ⟨x, hx⟩
    exact ⟨h, k, hh, hk, hsum⟩
  · rintro ⟨h, k, ⟨hh, _⟩, ⟨hk, _⟩, rfl⟩
    exact D.add_mem hh (D.smul_mem I hk)

theorem fixed_sum_tomita (h k : H)
    (hh : h ∈ fixedRealSubmodule D S) (hk : k ∈ fixedRealSubmodule D S) :
    S ⟨h + I • k, D.add_mem hh.choose (D.smul_mem I hk.choose)⟩ = h - I • k := by
  change S ((⟨h, hh.choose⟩ : D) + I • (⟨k, hk.choose⟩ : D)) = h - I • k
  rw [map_add, map_smulₛₗ, hh.choose_spec, hk.choose_spec]
  simp [sub_eq_add_neg]

theorem fixed_subspace_separating
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H), S x)))) :
    fixedClosedSubmodule D S hclosed ⊓ (fixedClosedSubmodule D S hclosed).mulI = ⊥ := by
  apply le_antisymm
  · intro x hx
    obtain ⟨hxK, hxI⟩ := hx
    change ∃ hx : x ∈ D, S ⟨x, hx⟩ = x at hxK
    change x ∈ (fixedClosedSubmodule D S hclosed).mulI at hxI
    rw [ClosedSubmodule.mem_mapEquiv_iff] at hxI
    change ∃ hy : (-I) • x ∈ D, S ⟨(-I) • x, hy⟩ = (-I) • x at hxI
    obtain ⟨hxD, hSx⟩ := hxK
    obtain ⟨hyD, hSy⟩ := hxI
    have he : (I : ℂ) • x = (-I : ℂ) • x := by
      calc
        (I : ℂ) • x = S ((-I : ℂ) • (⟨x, hxD⟩ : D)) := by
          rw [map_smulₛₗ, hSx]
          simp
        _ = (-I : ℂ) • x := hSy
    have hxzero : x = 0 := by
      have hz : (2 * I : ℂ) • x = 0 := by
        rw [mul_smul]
        have he' : I • x = -(I • x) := by simpa only [neg_smul] using he
        simpa only [two_smul] using (eq_neg_iff_add_eq_zero.mp he')
      exact (smul_eq_zero.mp hz).resolve_left (by norm_num)
    simpa only [ClosedSubmodule.mem_bot] using hxzero
  · exact bot_le

theorem fixed_subspace_cyclic
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H), S x))))
    (hmaps : ∀ x : D, S x ∈ D)
    (hinv : ∀ x : D, S ⟨S x, hmaps x⟩ = (x : H))
    (hdense : Dense (D : Set H)) :
    fixedClosedSubmodule D S hclosed ⊔ (fixedClosedSubmodule D S hclosed).mulI = ⊤ := by
  let K := fixedClosedSubmodule D S hclosed
  let L : ClosedSubmodule ℝ H := K ⊔ K.mulI
  have hD : (D : Set H) ⊆ (L : Set H) := by
    intro x hx
    obtain ⟨h, k, hh, hk, rfl⟩ := (mem_domain_iff_fixed_sum D S hmaps hinv x).mp hx
    have hh' : h ∈ K ⊔ K.mulI := (show K ≤ K ⊔ K.mulI from le_sup_left) hh
    change h + I • k ∈ K ⊔ K.mulI
    change k ∈ K at hk
    have hkI : I • k ∈ K.mulI := by
      rw [ClosedSubmodule.mem_mapEquiv_iff]
      simpa [scalarSMulCLE_symm_apply, Units.smul_def, smul_smul] using hk
    exact (K ⊔ K.mulI).toSubmodule.add_mem hh'
      ((show K.mulI ≤ K ⊔ K.mulI from le_sup_right) hkI)
  have htop : (Set.univ : Set H) ⊆ (L : Set H) := by
    rw [← hdense.closure_eq]
    exact closure_minimal hD L.isClosed
  apply top_unique
  intro x _
  exact htop (Set.mem_univ x)

/-- A closed, densely defined antilinear involution determines its real standard subspace. -/
def closedAntilinearStandardSubspace
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H), S x))))
    (hmaps : ∀ x : D, S x ∈ D)
    (hinv : ∀ x : D, S ⟨S x, hmaps x⟩ = (x : H))
    (hdense : Dense (D : Set H)) : StandardSubspace H where
  toClosedSubmodule := fixedClosedSubmodule D S hclosed
  IsSeparating := fixed_subspace_separating D S hclosed
  IsCyclic := fixed_subspace_cyclic D S hclosed hmaps hinv hdense

#print axioms fixedRealSubmodule
#print axioms mem_fixedRealSubmodule_iff
#print axioms fixedRealSubmodule_closed
#print axioms fixedClosedSubmodule
#print axioms domainConjugation
#print axioms domainConjugation_involutive
#print axioms domain_fixed_decomposition
#print axioms mem_domain_iff_fixed_sum
#print axioms fixed_sum_tomita
#print axioms fixed_subspace_separating
#print axioms fixed_subspace_cyclic
#print axioms closedAntilinearStandardSubspace

end
end ChatgptAudit.Continuous049
