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
import TGLExt.GenericAntilinearAdjoint
import TGLExt.ContinuousModularSquare
import TGLExt.ContinuousModularStandardSubspace

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Continuous050
open ChatgptAudit.Continuous049
noncomputable section

/-- The generic construction is the already constructed concrete Tomita operator. -/
theorem continuous_tomita_eq_generic (c : ℝ) (x : (continuousModularOperator c).domain) :
    continuousModularTomita c x =
      genericTomita (continuousModularOperator c) spectralJ x := rfl

def continuousTomitaAdjoint (c : ℝ) : SpectralHilbert →ₛₗ.[starRingEnd ℂ] SpectralHilbert :=
  genericTomitaAdjoint (continuousModularOperator c) spectralJ

theorem continuous_tomita_adjoint_pairing (c : ℝ)
    (x : (continuousModularOperator c).domain) (y : (continuousTomitaAdjoint c).domain) :
    inner ℂ (continuousModularTomita c x) (y : SpectralHilbert) =
      inner ℂ (continuousTomitaAdjoint c y) (x : SpectralHilbert) :=
  generic_adjoint_pairing (continuousModularOperator c) (continuous_modular_selfadjoint c)
    spectralJ spectralJ_involutive x y

theorem continuous_tomita_adjoint_maximal (c : ℝ) {y z : SpectralHilbert}
    (h : ∀ x : (continuousModularOperator c).domain,
      inner ℂ (continuousModularTomita c x) y = inner ℂ z (x : SpectralHilbert)) :
    ∃ hy : y ∈ (continuousTomitaAdjoint c).domain,
      continuousTomitaAdjoint c ⟨y, hy⟩ = z :=
  generic_adjoint_maximal (continuousModularOperator c) (continuous_modular_selfadjoint c)
    spectralJ spectralJ_involutive h

theorem continuous_tomita_adjoint_domain_iff (c : ℝ) (y : SpectralHilbert) :
    y ∈ (continuousTomitaAdjoint c).domain ↔
      ∃ z : SpectralHilbert, ∀ x : (continuousModularOperator c).domain,
        inner ℂ (continuousModularTomita c x) y = inner ℂ z (x : SpectralHilbert) :=
  generic_adjoint_domain_iff (continuousModularOperator c) (continuous_modular_selfadjoint c)
    spectralJ spectralJ_involutive y

theorem continuous_tomita_composition_domain (c : ℝ)
    (x : (continuousModularOperator c).domain) :
    continuousModularTomita c x ∈ (continuousTomitaAdjoint c).domain ↔
      continuousModularOperator c x ∈ (continuousModularOperator c).domain :=
  generic_composition_domain (continuousModularOperator c) spectralJ spectralJ_involutive x

theorem continuous_tomita_adjoint_comp (c : ℝ)
    (x : (continuousModularOperator c).domain)
    (hx : continuousModularOperator c x ∈ (continuousModularOperator c).domain) :
    continuousTomitaAdjoint c
      ⟨continuousModularTomita c x, (continuous_tomita_composition_domain c x).mpr hx⟩ =
        continuousModularOperator c ⟨continuousModularOperator c x, hx⟩ :=
  generic_adjoint_comp (continuousModularOperator c) spectralJ spectralJ_involutive x hx

/-- The full graph characterization below identifies this operator as S†S. -/
def continuousModularDelta (c : ℝ) : SpectralHilbert →ₗ.[ℂ] SpectralHilbert :=
  continuousModularSquare c

theorem continuous_delta_graph_iff_tomita_comp (c : ℝ) (f g : SpectralHilbert) :
    (f, g) ∈ (continuousModularDelta c).graph ↔
      ∃ hf : f ∈ (continuousModularOperator c).domain,
        ∃ hSf : continuousModularTomita c ⟨f, hf⟩ ∈ (continuousTomitaAdjoint c).domain,
          continuousTomitaAdjoint c ⟨continuousModularTomita c ⟨f, hf⟩, hSf⟩ = g := by
  rw [LinearPMap.mem_graph_iff]
  constructor
  · rintro ⟨x, hx, hy⟩
    dsimp only [Prod.fst, Prod.snd] at hx hy
    subst f
    have hSf := (continuous_tomita_composition_domain c
      ⟨(x : SpectralHilbert), x.property.choose⟩).mpr x.property.choose_spec
    refine ⟨x.property.choose, hSf, ?_⟩
    rw [continuous_tomita_adjoint_comp]
    exact hy
  · rintro ⟨hf, hSf, hg⟩
    have hTf := (continuous_tomita_composition_domain c ⟨f, hf⟩).mp hSf
    let x : (continuousModularDelta c).domain := ⟨f, ⟨hf, hTf⟩⟩
    refine ⟨x, rfl, ?_⟩
    change continuousModularOperator c ⟨continuousModularOperator c ⟨f, hf⟩, hTf⟩ = g
    rw [← continuous_tomita_adjoint_comp c ⟨f, hf⟩ hTf]
    exact hg

theorem continuous_delta_eq_double (c : ℝ) :
    continuousModularDelta c = continuousModularOperator (2*c) :=
  continuous_modular_square_eq c

theorem continuous_delta_domain_iff (c : ℝ) (f : SpectralHilbert) :
    f ∈ (continuousModularDelta c).domain ↔
      ∃ hf : f ∈ (continuousModularOperator c).domain,
        continuousModularTomita c ⟨f, hf⟩ ∈ (continuousTomitaAdjoint c).domain := by
  change (∃ hf : f ∈ (continuousModularOperator c).domain,
    continuousModularOperator c ⟨f, hf⟩ ∈ (continuousModularOperator c).domain) ↔ _
  exact exists_congr (fun hf => (continuous_tomita_composition_domain c ⟨f, hf⟩).symm)

theorem continuous_delta_selfadjoint (c : ℝ) : IsSelfAdjoint (continuousModularDelta c) :=
  continuous_modular_square_selfadjoint c

theorem continuous_delta_closed (c : ℝ) : (continuousModularDelta c).IsClosed :=
  continuous_modular_square_closed c

theorem continuous_delta_energy (c : ℝ) (x : (continuousModularDelta c).domain) :
    (inner ℂ (continuousModularDelta c x) (x : SpectralHilbert)).re =
      ‖continuousModularTomita c ⟨(x : SpectralHilbert), x.property.choose⟩‖ ^ 2 := by
  let u : (continuousModularOperator c).domain := ⟨x, x.property.choose⟩
  have hu : continuousModularOperator c u ∈ (continuousModularOperator c).domain :=
    x.property.choose_spec
  have h := continuous_tomita_adjoint_pairing c u
    ⟨continuousModularTomita c u, (continuous_tomita_composition_domain c u).mpr hu⟩
  rw [continuous_tomita_adjoint_comp c u hu] at h
  change (inner ℂ (continuousModularOperator c
    ⟨continuousModularOperator c u, hu⟩) (u : SpectralHilbert)).re = _
  rw [← h]
  exact (norm_sq_eq_re_inner (𝕜 := ℂ) (continuousModularTomita c u)).symm

theorem continuous_delta_positive (c : ℝ) (x : (continuousModularDelta c).domain) :
    0 ≤ (inner ℂ (x : SpectralHilbert) (continuousModularDelta c x)).re := by
  have h := continuous_delta_energy c x
  rw [← inner_conj_symm (𝕜 := ℂ) (x : SpectralHilbert) (continuousModularDelta c x)]
  change 0 ≤ (inner ℂ (continuousModularDelta c x) (x : SpectralHilbert)).re
  rw [h]
  exact sq_nonneg _

/-- A positive self-adjoint square root, with its exact composition domain proved above. -/
theorem continuous_modular_positive_square_root (c : ℝ) :
    IsSelfAdjoint (continuousModularOperator c) ∧
      (∀ x : (continuousModularOperator c).domain,
        0 ≤ (inner ℂ (x : SpectralHilbert) (continuousModularOperator c x)).re) ∧
      continuousModularSquare c = continuousModularDelta c :=
  ⟨continuous_modular_selfadjoint c, continuous_modular_positive c, rfl⟩

#print axioms continuous_tomita_eq_generic
#print axioms continuousTomitaAdjoint
#print axioms continuous_tomita_adjoint_pairing
#print axioms continuous_tomita_adjoint_maximal
#print axioms continuous_tomita_adjoint_domain_iff
#print axioms continuous_tomita_composition_domain
#print axioms continuous_tomita_adjoint_comp
#print axioms continuousModularDelta
#print axioms continuous_delta_graph_iff_tomita_comp
#print axioms continuous_delta_eq_double
#print axioms continuous_delta_domain_iff
#print axioms continuous_delta_selfadjoint
#print axioms continuous_delta_closed
#print axioms continuous_delta_energy
#print axioms continuous_delta_positive
#print axioms continuous_modular_positive_square_root

end
end ChatgptAudit.Continuous050
