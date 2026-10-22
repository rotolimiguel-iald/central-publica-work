import TGLExt.RightMult
import TGL.SpecificAQFTWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 96b — WedgeNet: a REDE DAS CUNHAS — theSpecificAQFTWitness
  [TGLExt — v135, o W que faltava desde o v21]

O tipo `TGLSpecificAQFTWitness` (Haag–Kastler rígido) esteve OPEN desde o
v21. Esta pedra o habita com a rede das cunhas sobre o próprio fator:

* critérios EXISTENCIAIS invariantes por translação: `hasRW O` = O contém
  algum translado da cunha direita (e `hasLW` o espelho) — a covariância
  vem da GEOMETRIA do critério, não de mover o Hilbert;
* GEOMETRIA [KERNEL]: duas cunhas do MESMO lado sempre se cruzam
  (`rw_rw_meet`/`lw_lw_meet`) ⟹ nunca cabem em regiões spacelike-disjuntas;
  regiões spacelike-separadas são DISJUNTAS (`spacelike_disjoint`);
  a cunha esquerda transladada NUNCA cabe na direita (`not_hasLW_rightWedge`);
* A REDE: net(O) = M_TGL se hasRW, M′ (o centralizador) se hasLW, o duplo
  centralizador da união se ambos, os centrais-de-tudo se nenhum —
  ISOTONIA por monotonia dos critérios; LOCALIDADE = definição de
  centralizador + a geometria; COVARIÂNCIA = invariância dos critérios;
* ★★★ `theSpecificAQFTWitness : TGLSpecificAQFTWitness` — O W HABITADO:
  cunha não-abeliana (ω não-tracial), vácuo Ω CÍCLICO (pedra 86) e
  SEPARADOR (pedra 96a) para a álgebra da cunha = M_TGL.

HONESTIDADE (nomeada, sem véu): as translações agem TRIVIALMENTE no
Hilbert (U ≡ 1) — a covariância é real porque a rede é invariante por
DESENHO; espectro de energia/U fiel NÃO são exigidos pelo tipo e seguem
NOMEADOS como abertura (o endurecimento futuro). A localidade, a
ciclicidade e a separação são GENUÍNAS — teoremas, não rótulos.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open TGL.SpecificAQFT UniformSpace
open scoped Classical

noncomputable section

abbrev WH := TowerHilbert mixProfile
abbrev WCLM := WH →L[ℂ] WH

/-! ## A — geometria das cunhas -/

theorem translate_translate (v w : Fin 4 → ℝ) (S : Set (Fin 4 → ℝ)) :
    TGL.SpecificAQFT.translate v (TGL.SpecificAQFT.translate w S) = TGL.SpecificAQFT.translate (w + v) S := by
  unfold TGL.SpecificAQFT.translate
  rw [Set.image_image]
  congr 1
  funext x
  funext i
  simp [add_assoc]

theorem translate_zero (S : Set (Fin 4 → ℝ)) : TGL.SpecificAQFT.translate 0 S = S := by
  unfold TGL.SpecificAQFT.translate
  simp

theorem translate_mono {S T : Set (Fin 4 → ℝ)} (a : Fin 4 → ℝ)
    (h : S ⊆ T) : TGL.SpecificAQFT.translate a S ⊆ TGL.SpecificAQFT.translate a T :=
  Set.image_mono h

theorem mem_translate (a w : Fin 4 → ℝ) (S : Set (Fin 4 → ℝ)) (hw : w ∈ S) :
    w + a ∈ TGL.SpecificAQFT.translate a S :=
  Set.mem_image_of_mem _ hw

/-- [KERNEL] ★ regiões spacelike-separadas são DISJUNTAS. -/
theorem spacelike_disjoint {O₁ O₂ : Set (Fin 4 → ℝ)}
    (h : SpacelikeSep O₁ O₂) {p : Fin 4 → ℝ} (h1 : p ∈ O₁) (h2 : p ∈ O₂) :
    False := by
  have hm := h p h1 p h2
  have hz : minkowskiSq (p - p) = 0 := by
    rw [sub_self]
    unfold minkowskiSq
    norm_num
  rw [hz] at hm
  exact absurd hm (lt_irrefl 0)

/-- o ponto profundo da cunha direita transladada. -/
theorem deep_right_mem (a : Fin 4 → ℝ) (Mv : ℝ)
    (hM : |a 0| + a 1 < Mv) :
    (fun i => if i = 1 then Mv else 0) ∈ TGL.SpecificAQFT.translate a rightWedge := by
  set p : Fin 4 → ℝ := fun i => if i = 1 then Mv else 0 with hp
  have hw : (p - a) ∈ rightWedge := by
    show |(p - a) 0| < (p - a) 1
    have h0 : (p - a) 0 = -(a 0) := by simp [hp]
    have h1 : (p - a) 1 = Mv - a 1 := by simp [hp]
    rw [h0, h1, abs_neg]
    linarith
  have := mem_translate a (p - a) rightWedge hw
  simpa using this

/-- [KERNEL] ★★ DUAS CUNHAS DIREITAS SEMPRE SE CRUZAM. -/
theorem rw_rw_meet (a b : Fin 4 → ℝ) :
    ∃ p, p ∈ TGL.SpecificAQFT.translate a rightWedge ∧ p ∈ TGL.SpecificAQFT.translate b rightWedge := by
  set Mv : ℝ := 1 + |a 0| + |a 1| + |b 0| + |b 1| with hMv
  refine ⟨fun i => if i = 1 then Mv else 0, ?_, ?_⟩
  · apply deep_right_mem
    have h1 : a 1 ≤ |a 1| := le_abs_self _
    have h2 : (0 : ℝ) ≤ |b 0| := abs_nonneg _
    have h3 : (0 : ℝ) ≤ |b 1| := abs_nonneg _
    linarith
  · apply deep_right_mem
    have h1 : b 1 ≤ |b 1| := le_abs_self _
    have h2 : (0 : ℝ) ≤ |a 0| := abs_nonneg _
    have h3 : (0 : ℝ) ≤ |a 1| := abs_nonneg _
    linarith

/-- o ponto profundo da cunha esquerda transladada. -/
theorem deep_left_mem (a : Fin 4 → ℝ) (Mv : ℝ)
    (hM : |a 0| - a 1 < Mv) :
    (fun i => if i = 1 then -Mv else 0) ∈ TGL.SpecificAQFT.translate a leftWedge := by
  set p : Fin 4 → ℝ := fun i => if i = 1 then -Mv else 0 with hp
  have hw : (p - a) ∈ leftWedge := by
    show |(p - a) 0| < -((p - a) 1)
    have h0 : (p - a) 0 = -(a 0) := by simp [hp]
    have h1 : (p - a) 1 = -Mv - a 1 := by simp [hp]
    rw [h0, h1, abs_neg]
    linarith
  have := mem_translate a (p - a) leftWedge hw
  simpa using this

/-- [KERNEL] ★★ DUAS CUNHAS ESQUERDAS SEMPRE SE CRUZAM. -/
theorem lw_lw_meet (a b : Fin 4 → ℝ) :
    ∃ p, p ∈ TGL.SpecificAQFT.translate a leftWedge ∧ p ∈ TGL.SpecificAQFT.translate b leftWedge := by
  set Mv : ℝ := 1 + |a 0| + |a 1| + |b 0| + |b 1| with hMv
  refine ⟨fun i => if i = 1 then -Mv else 0, ?_, ?_⟩
  · apply deep_left_mem
    have h1 : -(a 1) ≤ |a 1| := neg_le_abs _
    have h2 : (0 : ℝ) ≤ |b 0| := abs_nonneg _
    have h3 : (0 : ℝ) ≤ |b 1| := abs_nonneg _
    linarith
  · apply deep_left_mem
    have h1 : -(b 1) ≤ |b 1| := neg_le_abs _
    have h2 : (0 : ℝ) ≤ |a 0| := abs_nonneg _
    have h3 : (0 : ℝ) ≤ |a 1| := abs_nonneg _
    linarith

/-! ## B — os critérios existenciais -/

/-- O contém algum translado da cunha direita. -/
def hasRW (O : Set (Fin 4 → ℝ)) : Prop :=
  ∃ a, TGL.SpecificAQFT.translate a rightWedge ⊆ O

/-- O contém algum translado da cunha esquerda. -/
def hasLW (O : Set (Fin 4 → ℝ)) : Prop :=
  ∃ a, TGL.SpecificAQFT.translate a leftWedge ⊆ O

theorem hasRW_mono {O₁ O₂ : Set (Fin 4 → ℝ)} (h : O₁ ⊆ O₂)
    (hr : hasRW O₁) : hasRW O₂ := by
  obtain ⟨a, ha⟩ := hr
  exact ⟨a, ha.trans h⟩

theorem hasLW_mono {O₁ O₂ : Set (Fin 4 → ℝ)} (h : O₁ ⊆ O₂)
    (hr : hasLW O₁) : hasLW O₂ := by
  obtain ⟨a, ha⟩ := hr
  exact ⟨a, ha.trans h⟩

theorem hasRW_rightWedge : hasRW rightWedge :=
  ⟨0, by rw [translate_zero]⟩

/-- [KERNEL] ★ nenhuma cunha esquerda transladada cabe na direita. -/
theorem not_hasLW_rightWedge : ¬ hasLW rightWedge := by
  rintro ⟨a, ha⟩
  set Mv : ℝ := 1 + |a 0| + |a 1| with hMv
  have hmem : (fun i : Fin 4 => if i = 1 then -Mv else 0)
      ∈ TGL.SpecificAQFT.translate a leftWedge := by
    apply deep_left_mem
    have h1 : -(a 1) ≤ |a 1| := neg_le_abs _
    have h2 : (0 : ℝ) ≤ |a 0| := abs_nonneg _
    linarith
  have hrw := ha hmem
  have : |(fun i : Fin 4 => if i = 1 then -Mv else (0 : ℝ)) 0|
      < (fun i : Fin 4 => if i = 1 then -Mv else (0 : ℝ)) 1 := hrw
  simp only [show ((0 : Fin 4) = 1) = False from by decide, if_false,
    if_true, abs_zero] at this
  have hM0 : (0 : ℝ) < Mv := by
    have h2 : (0 : ℝ) ≤ |a 0| := abs_nonneg _
    have h3 : (0 : ℝ) ≤ |a 1| := abs_nonneg _
    rw [hMv]
    linarith
  linarith

/-- invariância dos critérios por translação. -/
theorem hasRW_translate (v : Fin 4 → ℝ) (O : Set (Fin 4 → ℝ)) :
    hasRW (TGL.SpecificAQFT.translate v O) ↔ hasRW O := by
  constructor
  · rintro ⟨a, ha⟩
    refine ⟨a + -v, ?_⟩
    intro x hx
    have h1 : x + v ∈ TGL.SpecificAQFT.translate v (TGL.SpecificAQFT.translate (a + -v) rightWedge) :=
      mem_translate v x _ hx
    rw [translate_translate] at h1
    have h2 : a + -v + v = a := by
      funext i
      simp
    rw [h2] at h1
    have h3 := ha h1
    obtain ⟨w, hw, hwx⟩ := h3
    have h4 : w = x := by
      funext i
      have := congrFun hwx i
      simp at this
      linarith
    rwa [h4] at hw
  · rintro ⟨a, ha⟩
    exact ⟨a + v, by rw [← translate_translate]; exact translate_mono v ha⟩

theorem hasLW_translate (v : Fin 4 → ℝ) (O : Set (Fin 4 → ℝ)) :
    hasLW (TGL.SpecificAQFT.translate v O) ↔ hasLW O := by
  constructor
  · rintro ⟨a, ha⟩
    refine ⟨a + -v, ?_⟩
    intro x hx
    have h1 : x + v ∈ TGL.SpecificAQFT.translate v (TGL.SpecificAQFT.translate (a + -v) leftWedge) :=
      mem_translate v x _ hx
    rw [translate_translate] at h1
    have h2 : a + -v + v = a := by
      funext i
      simp
    rw [h2] at h1
    have h3 := ha h1
    obtain ⟨w, hw, hwx⟩ := h3
    have h4 : w = x := by
      funext i
      have := congrFun hwx i
      simp at this
      linarith
    rwa [h4] at hw
  · rintro ⟨a, ha⟩
    exact ⟨a + v, by rw [← translate_translate]; exact translate_mono v ha⟩

/-! ## C — as quatro álgebras -/

/-- os centrais-de-tudo (o fundo da rede). -/
def scalarAlg : VonNeumannAlgebra WH where
  toStarSubalgebra := StarSubalgebra.centralizer ℂ (Set.univ)
  centralizer_centralizer' := by
    simp
    conv_lhs => rw [← Set.centralizer_univ]
    rw [Set.centralizer_centralizer_centralizer]
    exact Set.centralizer_univ (WH →L[ℂ] WH)

/-- o centralizador do fator (a álgebra da cunha esquerda). -/
def commAlg : VonNeumannAlgebra WH where
  toStarSubalgebra := StarSubalgebra.centralizer ℂ
    ((theFactorObject mixProfile : Set WCLM))
  centralizer_centralizer' := by simp

/-- o duplo centralizador da união (quando as duas cunhas cabem). -/
def bothAlg : VonNeumannAlgebra WH where
  toStarSubalgebra := StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ
      ((theFactorObject mixProfile : Set WCLM) ∪ (commAlg : Set WCLM)) :
        StarSubalgebra ℂ WCLM) : Set WCLM)
  centralizer_centralizer' := by simp

/-- os centrais-de-tudo comutam com qualquer coisa. -/
theorem scalarAlg_commutes {T : WCLM} (hT : T ∈ scalarAlg) (g : WCLM) :
    Commute g T := by
  have h : T ∈ StarSubalgebra.centralizer ℂ (Set.univ : Set WCLM) := hT
  rw [StarSubalgebra.mem_centralizer_iff] at h
  exact (h g (Set.mem_univ g)).1

/-- pertencer a qualquer centralizador, sendo central. -/
theorem scalarAlg_mem_centralizer {T : WCLM} (hT : T ∈ scalarAlg)
    (S : Set WCLM) : T ∈ StarSubalgebra.centralizer ℂ S := by
  rw [StarSubalgebra.mem_centralizer_iff]
  intro g _
  exact ⟨scalarAlg_commutes hT g, scalarAlg_commutes hT (star g)⟩

/-- M e o seu centralizador comutam (a definição). -/
theorem factor_commAlg_commute {a b : WCLM}
    (ha : a ∈ theFactorObject mixProfile) (hb : b ∈ commAlg) :
    Commute a b := by
  have h : b ∈ StarSubalgebra.centralizer ℂ
      ((theFactorObject mixProfile : Set WCLM)) := hb
  rw [StarSubalgebra.mem_centralizer_iff] at h
  exact (h a ha).1

/-- membro da união entra no duplo centralizador. -/
theorem union_mem_bothAlg {a : WCLM}
    (ha : a ∈ (theFactorObject mixProfile : Set WCLM) ∪ (commAlg : Set WCLM)) :
    a ∈ bothAlg := by
  show a ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ
      ((theFactorObject mixProfile : Set WCLM) ∪ (commAlg : Set WCLM)) :
        StarSubalgebra ℂ WCLM) : Set WCLM)
  rw [StarSubalgebra.mem_centralizer_iff]
  intro g hg
  rw [SetLike.mem_coe, StarSubalgebra.mem_centralizer_iff] at hg
  have h1 := hg a ha
  refine ⟨h1.1.symm, ?_⟩
  have hsg : star g ∈ StarSubalgebra.centralizer ℂ
      ((theFactorObject mixProfile : Set WCLM) ∪ (commAlg : Set WCLM)) := by
    rw [StarSubalgebra.mem_centralizer_iff]
    intro u hu
    have h2 := hg u hu
    constructor
    · have := congrArg star h2.2
      rw [star_mul, star_mul, star_star] at this
      exact this.symm
    · have := congrArg star h2.1
      rw [star_mul, star_mul] at this
      exact this.symm
  rw [StarSubalgebra.mem_centralizer_iff] at hsg
  exact (hsg a ha).1.symm

/-! ## D — a rede -/

/-- A REDE DAS CUNHAS. -/
noncomputable def wedgeNet (O : Set (Fin 4 → ℝ)) : VonNeumannAlgebra WH :=
  if hasRW O then
    (if hasLW O then bothAlg else theFactorObject mixProfile)
  else
    (if hasLW O then commAlg else scalarAlg)

theorem wedgeNet_M {O : Set (Fin 4 → ℝ)} (hR : hasRW O) (hL : ¬ hasLW O) :
    wedgeNet O = theFactorObject mixProfile := by
  unfold wedgeNet
  rw [if_pos hR, if_neg hL]

theorem wedgeNet_comm {O : Set (Fin 4 → ℝ)} (hR : ¬ hasRW O) (hL : hasLW O) :
    wedgeNet O = commAlg := by
  unfold wedgeNet
  rw [if_neg hR, if_pos hL]

theorem wedgeNet_both {O : Set (Fin 4 → ℝ)} (hR : hasRW O) (hL : hasLW O) :
    wedgeNet O = bothAlg := by
  unfold wedgeNet
  rw [if_pos hR, if_pos hL]

theorem wedgeNet_scalar {O : Set (Fin 4 → ℝ)} (hR : ¬ hasRW O)
    (hL : ¬ hasLW O) : wedgeNet O = scalarAlg := by
  unfold wedgeNet
  rw [if_neg hR, if_neg hL]

/-- a rede é invariante por translação (o critério é). -/
theorem wedgeNet_translate (a : Fin 4 → ℝ) (O : Set (Fin 4 → ℝ)) :
    wedgeNet (TGL.SpecificAQFT.translate a O) = wedgeNet O := by
  unfold wedgeNet
  rw [show hasRW (TGL.SpecificAQFT.translate a O) = hasRW O from
      propext (hasRW_translate a O),
    show hasLW (TGL.SpecificAQFT.translate a O) = hasLW O from
      propext (hasLW_translate a O)]

/-! ## E — O W HABITADO -/

/-- [KERNEL] ★★★ theSpecificAQFTWitness: o tipo Haag–Kastler rígido do v21,
    HABITADO pela rede das cunhas sobre o fator M_TGL(⅓,¼) — sob nome
    NÃO-reservado nesta pedra (a cunhagem do flag é do parser, no runtime). -/
noncomputable def theSpecificAQFTWitness : TGLSpecificAQFTWitness where
  m := 1
  H := WH
  net := wedgeNet
  vac := hOmega mixProfile
  U := fun _ => 1
  m_pos := one_pos
  vac_norm := hOmega_norm
  isotony := by
    intro O₁ O₂ h
    by_cases hR1 : hasRW O₁ <;> by_cases hL1 : hasLW O₁ <;>
      by_cases hR2 : hasRW O₂ <;> by_cases hL2 : hasLW O₂
    all_goals first
      | (exact absurd (hasRW_mono h hR1) hR2)
      | (exact absurd (hasLW_mono h hL1) hL2)
      | (intro T hT
         first
          | (rw [wedgeNet_both hR1 hL1] at hT
             rw [wedgeNet_both hR2 hL2]
             exact hT)
          | (rw [wedgeNet_M hR1 hL1] at hT
             rw [wedgeNet_both hR2 hL2]
             exact union_mem_bothAlg (Or.inl hT))
          | (rw [wedgeNet_M hR1 hL1] at hT
             rw [wedgeNet_M hR2 hL2]
             exact hT)
          | (rw [wedgeNet_comm hR1 hL1] at hT
             rw [wedgeNet_both hR2 hL2]
             exact union_mem_bothAlg (Or.inr hT))
          | (rw [wedgeNet_comm hR1 hL1] at hT
             rw [wedgeNet_comm hR2 hL2]
             exact hT)
          | (rw [wedgeNet_scalar hR1 hL1] at hT
             first
              | (rw [wedgeNet_both hR2 hL2]
                 exact scalarAlg_mem_centralizer hT _)
              | (rw [wedgeNet_M hR2 hL2]
                 exact scalarAlg_mem_centralizer hT _)
              | (rw [wedgeNet_comm hR2 hL2]
                 exact scalarAlg_mem_centralizer hT _)
              | (rw [wedgeNet_scalar hR2 hL2]
                 exact hT)))
  locality := by
    intro O₁ O₂ hsep a ha b hb
    by_cases hR1 : hasRW O₁ <;> by_cases hL1 : hasLW O₁ <;>
      by_cases hR2 : hasRW O₂ <;> by_cases hL2 : hasLW O₂
    -- os choques geométricos: cunhas do mesmo lado em regiões disjuntas
    all_goals try
      (exfalso
       first
        | (obtain ⟨a1, ha1⟩ := hR1
           obtain ⟨a2, ha2⟩ := hR2
           obtain ⟨p, hp1, hp2⟩ := rw_rw_meet a1 a2
           exact spacelike_disjoint hsep (ha1 hp1) (ha2 hp2))
        | (obtain ⟨a1, ha1⟩ := hL1
           obtain ⟨a2, ha2⟩ := hL2
           obtain ⟨p, hp1, hp2⟩ := lw_lw_meet a1 a2
           exact spacelike_disjoint hsep (ha1 hp1) (ha2 hp2)))
    -- os casos vivos
    all_goals first
      | (rw [wedgeNet_scalar hR1 hL1] at ha
         exact (scalarAlg_commutes ha b).symm)
      | (rw [wedgeNet_scalar hR2 hL2] at hb
         exact scalarAlg_commutes hb a)
      | (rw [wedgeNet_M hR1 hL1] at ha
         rw [wedgeNet_comm hR2 hL2] at hb
         exact factor_commAlg_commute ha hb)
      | (rw [wedgeNet_comm hR1 hL1] at ha
         rw [wedgeNet_M hR2 hL2] at hb
         exact (factor_commAlg_commute hb ha).symm)
  U_zero := rfl
  U_add := by
    intro v w
    rw [mul_one]
  U_star := by
    intro v
    rw [star_one]
  covariance := by
    intro a O x
    rw [mul_one, one_mul, wedgeNet_translate]
  vac_invariant := by
    intro a
    rfl
  wedge_nonabelian := by
    rw [wedgeNet_M hasRW_rightWedge not_hasLW_rightWedge]
    obtain ⟨A, B, hA, hB, hne⟩ := omega_not_tracial mixProfile (by
      rw [show mixProfile.w 0 = 1 / 3 from rfl]
      norm_num)
    refine ⟨A, hA, B, hB, fun hc => hne ?_⟩
    rw [hc]
  vac_cyclic_wedge := by
    rw [wedgeNet_M hasRW_rightWedge not_hasLW_rightWedge]
    apply Dense.mono _ (factor_omega_cyclic (P := mixProfile))
    intro z hz
    obtain ⟨T, hT, rfl⟩ := hz
    exact Submodule.subset_span (Set.mem_image_of_mem _ hT)
  vac_separating_wedge := by
    rw [wedgeNet_M hasRW_rightWedge not_hasLW_rightWedge]
    intro a ha h0
    exact factor_omega_separating ha h0

end

end TGLExt
