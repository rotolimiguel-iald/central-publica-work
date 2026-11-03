-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_050 (06-07/09/2026), transposta em 07/09/2026
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
import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Tactic

set_option autoImplicit false

namespace ChatgptAudit.Continuous050
open Complex
noncomputable section

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- The inner product identity follows from semilinearity and the norm, by polarization. -/
theorem antiunitary_inner_conj (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (x y : H) :
    inner ℂ (J x) (J y) = star (inner ℂ x y) := by
  have hp : ‖J x + J y‖ = ‖x + y‖ := by
    rw [← map_add, J.norm_map]
  have hm : ‖J x - J y‖ = ‖x - y‖ := by
    rw [← map_sub, J.norm_map]
  have hip : ‖J x + I • J y‖ = ‖x - I • y‖ := by
    conv_rhs => rw [← J.norm_map (x - I • y)]
    rw [map_sub, map_smulₛₗ]
    simp
  have him : ‖J x - I • J y‖ = ‖x + I • y‖ := by
    conv_rhs => rw [← J.norm_map (x + I • y)]
    rw [map_add, map_smulₛₗ]
    simp [sub_eq_add_neg]
  rw [inner_eq_sum_norm_sq_div_four, inner_eq_sum_norm_sq_div_four]
  simp only [RCLike.I_to_complex, hp, hm, hip, him]
  simp
  ring

theorem antiunitary_pairing_flip (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hJ : Function.Involutive J) (x y : H) :
    inner ℂ (J x) y = inner ℂ (J y) x := by
  have h := antiunitary_inner_conj J x (J y)
  rw [hJ y] at h
  change inner ℂ (J x) y = (starRingEnd ℂ) (inner ℂ x (J y)) at h
  simpa only [inner_conj_symm] using h

/-- The antilinear partial map S=JT has exactly the domain of T. -/
def genericTomita (T : H →ₗ.[ℂ] H) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    H →ₛₗ.[starRingEnd ℂ] H where
  domain := T.domain
  toFun := J.toLinearEquiv.toLinearMap.comp T.toFun

theorem generic_tomita_apply (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (x : T.domain) :
    genericTomita T J x = J (T x) := rfl

/-- The candidate domain is later proved to equal the full adjoint domain. -/
def genericAdjointDomain (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) : Submodule ℂ H :=
  T.domain.comap J.toLinearEquiv.toLinearMap

def genericAdjointInput (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    genericAdjointDomain T J →ₛₗ[starRingEnd ℂ] T.domain :=
  ((J.toLinearEquiv.toLinearMap.domRestrict (genericAdjointDomain T J)).codRestrict
    T.domain (fun y => y.property))

theorem generic_adjoint_input_coe (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (y : genericAdjointDomain T J) :
    (genericAdjointInput T J y : H) = J (y : H) := rfl

/-- This partial map is identified as the maximal antilinear adjoint when T is self-adjoint. -/
def genericTomitaAdjoint (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) : H →ₛₗ.[starRingEnd ℂ] H where
  domain := genericAdjointDomain T J
  toFun := T.toFun.comp (genericAdjointInput T J)

theorem generic_tomita_adjoint_apply (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (y : genericAdjointDomain T J) :
    genericTomitaAdjoint T J y = T (genericAdjointInput T J y) := rfl

theorem generic_pairing_with_J (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (x : T.domain) (y : H) :
    inner ℂ (genericTomita T J x) y = inner ℂ (J y) (T x) :=
  antiunitary_pairing_flip J hJ (T x) y

/-- Adjoint convention: the representative lies in the first inner-product argument. -/
theorem generic_adjoint_pairing [CompleteSpace H] (T : H →ₗ.[ℂ] H)
    (hT : IsSelfAdjoint T) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hJ : Function.Involutive J) (x : T.domain) (y : genericAdjointDomain T J) :
    inner ℂ (genericTomita T J x) (y : H) =
      inner ℂ (genericTomitaAdjoint T J y) (x : H) := by
  have hs : T.IsFormalAdjoint T := by
    have h := LinearPMap.adjoint_isFormalAdjoint (T := T) hT.dense_domain
    simpa only [LinearPMap.isSelfAdjoint_def.mp hT] using h
  rw [generic_pairing_with_J T J hJ]
  exact (hs (genericAdjointInput T J y) x).symm

/-- Maximality uses the actual Mathlib adjoint, not only the formal pairing identity. -/
theorem generic_adjoint_maximal [CompleteSpace H] (T : H →ₗ.[ℂ] H)
    (hT : IsSelfAdjoint T) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hJ : Function.Involutive J) {y z : H}
    (h : ∀ x : T.domain,
      inner ℂ (genericTomita T J x) y = inner ℂ z (x : H)) :
    ∃ hy : y ∈ genericAdjointDomain T J, genericTomitaAdjoint T J ⟨y, hy⟩ = z := by
  have hadj : J y ∈ (LinearPMap.adjoint T).domain := by
    apply LinearPMap.mem_adjoint_domain_of_exists
    refine ⟨z, fun x => ?_⟩
    rw [← h x, generic_pairing_with_J T J hJ]
  have hy : y ∈ genericAdjointDomain T J := by
    change J y ∈ T.domain
    rwa [LinearPMap.isSelfAdjoint_def.mp hT] at hadj
  refine ⟨hy, ?_⟩
  apply hT.dense_domain.eq_of_inner_left ℂ
  intro x hx
  exact (generic_adjoint_pairing T hT J hJ ⟨x, hx⟩ ⟨y, hy⟩).symm.trans (h ⟨x, hx⟩)

theorem generic_adjoint_domain_iff [CompleteSpace H] (T : H →ₗ.[ℂ] H)
    (hT : IsSelfAdjoint T) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hJ : Function.Involutive J) (y : H) :
    y ∈ genericAdjointDomain T J ↔ ∃ z : H, ∀ x : T.domain,
      inner ℂ (genericTomita T J x) y = inner ℂ z (x : H) := by
  constructor
  · intro hy
    exact ⟨genericTomitaAdjoint T J ⟨y, hy⟩,
      fun x => generic_adjoint_pairing T hT J hJ x ⟨y, hy⟩⟩
  · rintro ⟨z, hz⟩
    exact (generic_adjoint_maximal T hT J hJ hz).choose

/-- The composition domain is paid explicitly; no invariance of all of D(T) is assumed. -/
theorem generic_composition_domain (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J) (x : T.domain) :
    genericTomita T J x ∈ genericAdjointDomain T J ↔ T x ∈ T.domain := by
  change J (J (T x)) ∈ T.domain ↔ T x ∈ T.domain
  rw [hJ]

theorem generic_adjoint_comp (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (x : T.domain) (hx : T x ∈ T.domain) :
    genericTomitaAdjoint T J
      ⟨genericTomita T J x, (generic_composition_domain T J hJ x).mpr hx⟩ =
      T ⟨T x, hx⟩ := by
  change T (genericAdjointInput T J
    ⟨genericTomita T J x, (generic_composition_domain T J hJ x).mpr hx⟩) = T ⟨T x, hx⟩
  congr 1
  apply Subtype.ext
  exact hJ (T x)

#print axioms antiunitary_inner_conj
#print axioms antiunitary_pairing_flip
#print axioms genericTomita
#print axioms generic_tomita_apply
#print axioms genericAdjointDomain
#print axioms genericAdjointInput
#print axioms generic_adjoint_input_coe
#print axioms genericTomitaAdjoint
#print axioms generic_tomita_adjoint_apply
#print axioms generic_pairing_with_J
#print axioms generic_adjoint_pairing
#print axioms generic_adjoint_maximal
#print axioms generic_adjoint_domain_iff
#print axioms generic_composition_domain
#print axioms generic_adjoint_comp

end
end ChatgptAudit.Continuous050
