import TGLExt.QuedaSemGeometria
import TGLExt.F1Fecho394.PhysicalFockNetRealizationR2

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

/-!
# (CANDIDATA, 11/11/2026) As cunhas de referencial são covariantes — fiação, não matemática nova
  [sandbox `k410c`; fora do kernel canônico; nomes PROVISÓRIOS da gerência — o nome é do operador]

O kernel v410 já tem o grupo de Lorentz gerado agindo sobre a rede da luz
(`TGLExt/F1Fecho394/`: `generatedLorentz`, `helicityUnitary`, `compactLocalized`,
`compactLocalized_lorentz_iff`, `compactLocalized_translate_iff`, `physicalFrameRegion`,
`helicityPoincareH1`, `PhysicalFockNetRealizationR2`). O que faltava era a fiação com o
`IsotropicPost` de `QuedaSemGeometria`, cujo único habitante era o modelo de brinquedo `Rapidity`.
Este arquivo faz três coisas, e só elas.

* **A. A covariância das cunhas.** Para o elemento de Poincaré `g = (M, b)`
  (`M : generatedLorentz`, `b : Spacetime`), a região da cunha transformada é `g.region O` e o
  subespaço localizado dela é a IMAGEM, pelo unitário `g.unitary`, do subespaço da cunha padrão
  (`cunha_covariante`, `submodulo_da_cunha_e_a_imagem`). Especializações: à cunha direita, às cunhas
  `lorentzRegion L W` e às cunhas de referencial `physicalFrameRegion L a W` do kernel.
* **B. `IsotropicPost` habitado por um predicado FÍSICO da rede.** `Frame` é o tipo dos
  referenciais (um referencial `(N, c)` é a cunha direita vista da imagem de Poincaré `(N, c)`),
  `PoincareEl` os elementos que transformam (só `SMul` compatível com as regiões; sem instância de
  grupo), e o predicado `PRede` diz: o subespaço localizado da cunha é não nulo e simpleticamente
  ortogonal ao da cunha oposta. É covariante por teorema (A) e vale na cunha padrão
  por teoremas do kernel (`physical_canonical_net_nonzero`, `physical_frame_opposite_symplectic`).
  Por `clausius_everywhere_from_one_wedge_by_covariance` vale em TODO referencial.
* **C. KMS da cunha transformada.** Se o vácuo é KMS (β = 1) para o fluxo `Γ(B0(2πt))` na álgebra da
  cunha direita (`vacuum_bw_kms`, do kernel) e `Γ(U)` fixa o vácuo, então é KMS para o fluxo
  conjugado na álgebra da cunha `g.region` (`kms_da_cunha_transformada`).

HONESTIDADE (a régua). `PRede` NÃO é a lei de Clausius nem a H3: é a não-trivialidade e a localidade
simplética do subespaço da cunha, e a pedra só mostra que ela se transporta por covariância. A
H3 é a forma de ÁREA (erro microscópico de área sobre `t²` em toda tela e direção nula) e NÃO está
aqui. O KMS da parte C é a perna algébrica de Bisognano–Wichmann (vácuo KMS para o fluxo da cunha);
não é a identificação do fluxo com o grupo modular da cunha transformada (isso exigiria o vácuo
cíclico e separante para a álgebra transformada, que decorre por conjugação mas não é enunciado
aqui), nem Clausius, nem uma lei no espaço-tempo curvo. A família de Lorentz de cunhas é a do grupo
GERADO `generatedLorentz` (que, pelo kernel, contém todo Lorentz ortócrono: `LorentzFutureGenerationR6`),
sem as cunhas das direções nulas de um átlas curvo.

RESSALVAS DA REVISÃO DE TERCEIRO (R2, 11/11/2026): a transitividade do `IsotropicPost` é trivial
por construção (`Frame` é o próprio conjunto de elementos de Poincaré; “todo referencial” quer
dizer toda imagem de Poincaré da cunha padrão); `PRede` não exige que o subespaço da cunha oposta
seja não nulo, e a cláusula simplética já era teorema do kernel para todo `(L, a)`: a habitação é
real, mas formal e fraca; `fluxoDaCunha g` é “da cunha” por definição (conjugação): não se prova
aqui que seja o fluxo geométrico da região, e ele depende de `g`, não só da região; `gamma_symm'`
repete um lema do kernel (`F1Rede.BosonicFockGroupActions.gamma_symm`). O `β` do KMS é o parâmetro
de temperatura inversa; `β_TGL` não aparece. O gate não se move; sem sorry, sem axiom.
-/

namespace TGLExt.CunhasCovariantesCandidata

open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.MaxwellLocalization F1Fecho.OrbitalSpatial
open F1Fecho.OrbitalScreen F1Fecho.SpacetimeLorentz

noncomputable section

/-! ## 0. Álgebra da ação do Lorentz sobre os pontos -/

/-- a ação sobre os pontos é multiplicativa: `action (M·N) = action M ∘ action N`. -/
theorem action_mul' (M N : TGLExt.LorentzGrp) (z : Spacetime) :
    action (M * N) z = action M (action N z) := by
  apply PiLp.ext
  intro i
  have h1 : (fun i => action (M * N) z i) = (M * N).val.mulVec (fun i => z i) := action_apply _ _
  have h3 : (fun i => action N z i) = N.val.mulVec (fun i => z i) := action_apply _ _
  have h2 : (fun i => action M (action N z) i) = M.val.mulVec (fun i => action N z i) :=
    action_apply _ _
  rw [h3, Matrix.mulVec_mulVec, ← TGLExt.lorentzGrp_mul_val] at h2
  exact congrFun (h1.trans h2.symm) i

/-- a identidade age como a identidade. -/
theorem action_one' (z : Spacetime) : action (1 : TGLExt.LorentzGrp) z = z := by
  apply PiLp.ext
  intro i
  have h1 : (fun i => action (1 : TGLExt.LorentzGrp) z i) =
      (1 : TGLExt.LorentzGrp).val.mulVec (fun i => z i) := action_apply _ _
  rw [TGLExt.lorentzGrp_one_val, Matrix.one_mulVec] at h1
  exact congrFun h1 i

/-! ## A. A covariância das cunhas -/

/-- Um elemento do grupo de Poincaré da rede: um Lorentz do grupo gerado e uma translação. -/
structure PoincareEl where
  /-- a parte de Lorentz (do subgrupo gerado, que o kernel prova agir sobre a rede) -/
  M : generatedLorentz
  /-- a translação -/
  b : Spacetime

/-- a imagem de uma região por `x ↦ action M x + b` (é `translateRegion b (lorentzRegion M O)`). -/
def PoincareEl.region (g : PoincareEl) (O : Set Spacetime) : Set Spacetime :=
  translateRegion g.b (lorentzRegion g.M O)

/-- o unitário do kernel: `U1 b ∘ helicityUnitary M` (`helicityPoincareH1`). -/
def PoincareEl.unitary (g : PoincareEl) : H1 ≃ₗᵢ[ℂ] H1 :=
  helicityPoincareH1 (fun i => g.b i) g.M

/-- [CANDIDATA, fiação] ★ A COVARIÂNCIA DAS CUNHAS: `v` está localizado em `O` se e só se `U(g) v` está
    localizado em `g.region O` (rede de testes compactos; é `compactLocalized_lorentz_iff` seguido de
    `compactLocalized_translate_iff`). -/
theorem cunha_covariante (g : PoincareEl) (O : Set Spacetime) (v : H1) :
    v ∈ compactLocalized O ↔ g.unitary v ∈ compactLocalized (g.region O) := by
  unfold PoincareEl.unitary PoincareEl.region helicityPoincareH1
  rw [LinearIsometryEquiv.trans_apply]
  rw [compactLocalized_lorentz_iff g.M O v]
  exact compactLocalized_translate_iff g.b (lorentzRegion g.M O) _

/-- Genérico: se `u` leva `K` em `K'` (por iff), então `K'` é a imagem de `K` por `u`. -/
theorem imagem_de_iff {u : H1 ≃ₗᵢ[ℂ] H1} {K K' : Submodule ℝ H1}
    (h : ∀ f, f ∈ K ↔ u f ∈ K') : (K' : Set H1) = u '' (K : Set H1) := by
  ext w
  constructor
  · intro hw
    refine ⟨u.symm w, ?_, u.apply_symm_apply w⟩
    exact (h (u.symm w)).mpr (by rwa [u.apply_symm_apply])
  · rintro ⟨v, hv, rfl⟩
    exact (h v).mp hv

/-- [CANDIDATA, fiação] ★ O SUBESPAÇO DA CUNHA TRANSFORMADA É A IMAGEM DO DA CUNHA PADRÃO pelo unitário. -/
theorem submodulo_da_cunha_e_a_imagem (g : PoincareEl) (O : Set Spacetime) :
    (compactLocalized (g.region O) : Set H1) = g.unitary '' (compactLocalized O : Set H1) :=
  imagem_de_iff (cunha_covariante g O)

/-- A cunha direita transformada: o subespaço localizado é a imagem do da cunha direita padrão. -/
theorem cunha_direita_transformada (g : PoincareEl) :
    (compactLocalized (g.region physicalRightWedge) : Set H1) =
      g.unitary '' (compactLocalized physicalRightWedge : Set H1) :=
  submodulo_da_cunha_e_a_imagem g physicalRightWedge

/-- Só Lorentz (`L•W`, a cunha com o mesmo vértice): o subespaço de `lorentzRegion L W` é a imagem,
    por `helicityUnitary L`, do de `W`. -/
theorem cunha_lorentz_transformada (L : generatedLorentz) (W : Set Spacetime) :
    (compactLocalized (lorentzRegion L W) : Set H1) =
      helicityUnitary L '' (compactLocalized W : Set H1) :=
  imagem_de_iff (compactLocalized_lorentz_iff L W)

/-- a ponte com a região de referencial do kernel: `physicalFrameRegion L a W` é a região de
    `(L⁻¹, a)`. -/
theorem frame_region_eq (L : generatedLorentz) (a : Spacetime) (W : Set Spacetime) :
    physicalFrameRegion L a W = (PoincareEl.mk L⁻¹ a).region W := by
  ext x
  change action L.val (x - a) ∈ W ↔ ∃ y, y ∈ W ∧ action L⁻¹.val y = x - a
  constructor
  · intro h
    refine ⟨action L.val (x - a), h, ?_⟩
    exact (action L.val).symm_apply_apply (x - a)
  · rintro ⟨y, hy, hxy⟩
    have : action L.val (x - a) = y := by
      rw [← hxy]
      exact (action L.val).apply_symm_apply y
    rwa [this]

/-- ★ AS CUNHAS DE REFERENCIAL DO KERNEL: o subespaço da cunha direita vista do referencial `(L, a)` é
    a imagem do da cunha padrão por `U1 a ∘ helicityUnitary L⁻¹`. -/
theorem cunha_de_referencial (L : generatedLorentz) (a : Spacetime) :
    (compactLocalized (physicalFrameRegion L a physicalRightWedge) : Set H1) =
      (helicityPoincareH1 (fun i => a i) L⁻¹) '' (compactLocalized physicalRightWedge : Set H1) := by
  rw [frame_region_eq]
  exact cunha_direita_transformada ⟨L⁻¹, a⟩

/-! ## B. `IsotropicPost` habitado por um predicado da rede -/

/-- Um REFERENCIAL: a cunha direita padrão vista da imagem de Poincaré `(N, c)`. -/
structure Frame where
  /-- a parte de Lorentz -/
  N : generatedLorentz
  /-- a translação (o vértice) -/
  c : Spacetime

/-- o referencial como elemento de Poincaré. -/
def Frame.toEl (w : Frame) : PoincareEl := ⟨w.N, w.c⟩

/-- A AÇÃO: `(M, b) • (N, c) = (M·N, b + M c)` — a mesma lei de grupo de `helicityPoincareH1_mul`. -/
instance : SMul PoincareEl Frame where
  smul g w := ⟨g.M * w.N, g.b + action g.M.val w.c⟩

theorem Frame.smul_def (g : PoincareEl) (w : Frame) :
    g • w = ⟨g.M * w.N, g.b + action g.M.val w.c⟩ := rfl

/-- a cunha direita do referencial. -/
def Frame.wedge (w : Frame) : Set Spacetime := w.toEl.region physicalRightWedge

/-- a cunha oposta (esquerda) do referencial. -/
def Frame.opposite (w : Frame) : Set Spacetime := w.toEl.region physicalLeftWedge

/-- o referencial padrão: a identidade na origem. -/
def Frame.padrao : Frame := ⟨1, 0⟩

/-- a região da imagem composta é a composta das imagens (a lei de ação, em regiões). -/
theorem region_smul (g : PoincareEl) (w : Frame) (O : Set Spacetime) :
    (g • w).toEl.region O = g.region (w.toEl.region O) := by
  ext y
  change (∃ o, o ∈ O ∧ action (g.M * w.N).val o = y - (g.b + action g.M.val w.c)) ↔
    ∃ x, (∃ o, o ∈ O ∧ action w.N.val o = x - w.c) ∧ action g.M.val x = y - g.b
  constructor
  · rintro ⟨o, ho, h⟩
    refine ⟨action w.N.val o + w.c, ⟨o, ho, by simp⟩, ?_⟩
    have h' : action g.M.val (action w.N.val o) = y - (g.b + action g.M.val w.c) := by
      rw [← action_mul']
      exact h
    rw [map_add, h']
    abel
  · rintro ⟨x, ⟨o, ho, hx⟩, hy⟩
    refine ⟨o, ho, ?_⟩
    change action (g.M.val * w.N.val) o = _
    rw [action_mul', hx, map_sub, hy]
    abel

theorem wedge_smul (g : PoincareEl) (w : Frame) :
    (g • w).wedge = g.region w.wedge := region_smul g w physicalRightWedge

theorem opposite_smul (g : PoincareEl) (w : Frame) :
    (g • w).opposite = g.region w.opposite := region_smul g w physicalLeftWedge

/-- o subespaço localizado da cunha do referencial é não nulo. -/
def LocalizadaNaoNula (w : Frame) : Prop :=
  ∃ v : H1, v ≠ 0 ∧ v ∈ compactLocalized w.wedge

/-- o subespaço da cunha é simpleticamente ortogonal ao da cunha oposta (parte imaginária do produto
    interno nula). -/
def OpostaSimpletica (w : Frame) : Prop :=
  ∀ f ∈ compactLocalized w.wedge, ∀ h ∈ compactLocalized w.opposite, (inner ℂ f h).im = 0

/-- ★ O PREDICADO DA REDE (`P`): a cunha do referencial é não trivial E simpleticamente ortogonal à
    oposta. NÃO é a lei de Clausius nem a H3: é a localidade e a não-trivialidade do subespaço da
    cunha, propriedades da REDE da luz (livre de Maxwell) que o kernel transporta por covariância. -/
def PRede (w : Frame) : Prop := LocalizadaNaoNula w ∧ OpostaSimpletica w

/-- ★ `PRede` é covariante sob o grupo de Poincaré, por teorema do kernel (A). -/
theorem prede_covariante (g : PoincareEl) (w : Frame) (h : PRede w) : PRede (g • w) := by
  obtain ⟨⟨v, hv0, hv⟩, hloc⟩ := h
  refine ⟨⟨g.unitary v, ?_, ?_⟩, ?_⟩
  · intro hz
    exact hv0 (by simpa using hz)
  · rw [wedge_smul]
    exact (cunha_covariante g w.wedge v).mp hv
  · intro f hf k hk
    rw [wedge_smul] at hf
    rw [opposite_smul] at hk
    have hf' : f ∈ g.unitary '' (compactLocalized w.wedge : Set H1) := by
      rw [← submodulo_da_cunha_e_a_imagem g]
      exact hf
    have hk' : k ∈ g.unitary '' (compactLocalized w.opposite : Set H1) := by
      rw [← submodulo_da_cunha_e_a_imagem g]
      exact hk
    obtain ⟨f0, hf0, rfl⟩ := hf'
    obtain ⟨k0, hk0, rfl⟩ := hk'
    rw [LinearIsometryEquiv.inner_map_map]
    exact hloc f0 hf0 k0 hk0

/-- `physicalFrameRegion 1 0 W = W` (o referencial padrão do kernel é a cunha padrão). -/
theorem frame_region_padrao (W : Set Spacetime) :
    physicalFrameRegion (1 : generatedLorentz) 0 W = W := by
  ext x
  change action (1 : TGLExt.LorentzGrp) (x - 0) ∈ W ↔ x ∈ W
  rw [sub_zero, action_one']

/-- a região do referencial padrão é a própria região (a imagem pela identidade). -/
theorem padrao_region (O : Set Spacetime) : Frame.padrao.toEl.region O = O := by
  ext x
  change (∃ y, y ∈ O ∧ action (1 : TGLExt.LorentzGrp) y = x - 0) ↔ x ∈ O
  constructor
  · rintro ⟨y, hy, h⟩
    rw [action_one', sub_zero] at h
    rwa [← h]
  · intro hx
    exact ⟨x, hx, by rw [action_one', sub_zero]⟩

/-- ★ A BASE: `PRede` vale no referencial padrão — por `physical_canonical_net_nonzero` e
    `physical_frame_opposite_symplectic` (kernel). -/
theorem prede_padrao : PRede Frame.padrao := by
  refine ⟨?_, ?_⟩
  · obtain ⟨v, hv, hne⟩ := physical_canonical_net_nonzero
    refine ⟨v, hne, ?_⟩
    change v ∈ compactLocalized (Frame.padrao.toEl.region physicalRightWedge)
    rw [padrao_region]
    exact hv
  · intro f hf h hh
    change f ∈ compactLocalized (Frame.padrao.toEl.region physicalRightWedge) at hf
    change h ∈ compactLocalized (Frame.padrao.toEl.region physicalLeftWedge) at hh
    rw [padrao_region] at hf hh
    apply physical_frame_opposite_symplectic 1 0 f h
    · rw [frame_region_padrao]
      exact compactLocalized_le_localized _ hf
    · rw [frame_region_padrao]
      exact compactLocalized_le_localized _ hh

/-- ★★ `IsotropicPost` HABITADO por um predicado da rede da luz. (R2, revisão de terceiro, achados
    1, 3 e 8.) A TRANSITIVIDADE É TRIVIAL POR CONSTRUÇÃO: `Frame` é `PoincareEl` com outro nome, o
    `SMul` é a multiplicação à esquerda e `padrao` é a identidade (`w = w.toEl • padrao`). Quem
    prova algo é só a covariância (A). `PoincareEl` é uma estrutura local, restrita a
    `generatedLorentz`; aqui só há `SMul` compatível com as regiões (`region_smul`), sem instância
    de grupo nem de ação. A habitação é real (não é o brinquedo `Rapidity`), mas formal e fraca.
    NÃO habita o `IsotropicPost` do índice de telas e direções nulas do kernel e NÃO prova a H3. -/
theorem isotropic_post_da_rede :
    TGLExt.QuedaSemGeometria.IsotropicPost PoincareEl Frame PRede Frame.padrao := by
  refine ⟨?_, prede_covariante⟩
  intro w
  refine ⟨w.toEl, ?_⟩
  cases w with
  | mk N c =>
    change (⟨N, c⟩ : Frame) = ⟨N * 1, c + action N.val 0⟩
    rw [mul_one, map_zero, add_zero]

/-- ★★ O PREDICADO `PRede` VALE EM TODO REFERENCIAL, isto é, em toda imagem de Poincaré (Lorentz
    gerado e translação) da cunha padrão, pelo lema de transporte do kernel. `PRede` não é lei: é
    não-trivialidade e localidade simplética (R2, achado 2). -/
theorem prede_em_todo_referencial : ∀ w : Frame, PRede w :=
  TGLExt.QuedaSemGeometria.clausius_everywhere_from_one_wedge_by_covariance
    isotropic_post_da_rede prede_padrao

/-- Em termos das regiões de referencial do kernel: para todo `(L, a)`, o subespaço localizado de
    `physicalFrameRegion L a physicalRightWedge` é não nulo. -/
theorem cunha_de_referencial_nao_nula (L : generatedLorentz) (a : Spacetime) :
    ∃ v : H1, v ≠ 0 ∧ v ∈ compactLocalized (physicalFrameRegion L a physicalRightWedge) := by
  obtain ⟨⟨v, hv0, hv⟩, _⟩ := prede_em_todo_referencial ⟨L⁻¹, a⟩
  refine ⟨v, hv0, ?_⟩
  rw [frame_region_eq]
  exact hv

/-! ## C. KMS da cunha transformada, por conjugação -/

section KMSConjugado

variable {F : Type} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-- aplicada ao vácuo fixo por `Γ`, a conjugação por `Γ⁻¹` é `Γ⁻¹` do operador aplicado ao vácuo. -/
theorem conj_symm_apply_vac (Γ : F ≃ₗᵢ[ℂ] F) (Ω : F) (hΩ : Γ Ω = Ω) (X : F →L[ℂ] F) :
    Γ.symm.conjStarAlgEquiv X Ω = Γ.symm (X Ω) := by
  rw [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply, LinearIsometryEquiv.symm_symm, hΩ]

/-- o produto interno do corpo KMS não muda sob a conjugação por `Γ` (que fixa o vácuo). -/
theorem inner_conjugado (Γ : F ≃ₗᵢ[ℂ] F) (Ω : F) (hΩ : Γ Ω = Ω) (A B : F →L[ℂ] F)
    (a : F ≃ₗᵢ[ℂ] F) :
    inner ℂ ((star (Γ.symm.conjStarAlgEquiv A)) Ω) (a ((Γ.symm.conjStarAlgEquiv B) Ω)) =
      inner ℂ ((star A) Ω) ((Γ.symm.trans (a.trans Γ)) (B Ω)) := by
  rw [← map_star, conj_symm_apply_vac Γ Ω hΩ, conj_symm_apply_vac Γ Ω hΩ]
  rw [LinearIsometryEquiv.trans_apply, LinearIsometryEquiv.trans_apply]
  rw [← LinearIsometryEquiv.inner_map_map Γ.symm ((star A) Ω) (Γ (a (Γ.symm (B Ω))))]
  rw [LinearIsometryEquiv.symm_apply_apply]

/-- [CANDIDATA, fiação] ★ A CONDIÇÃO KMS SE TRANSPORTA POR CONJUGAÇÃO UNITÁRIA. Se `Ω` é KMS a `β` para o
    fluxo `α` na álgebra `M`, `Γ` fixa `Ω` e leva `M` em `M'` (`x ∈ M ↔ Γ x Γ⁻¹ ∈ M'`), então `Ω` é KMS a
    `β` para o fluxo conjugado `Γ α Γ⁻¹` na álgebra `M'`. A mesma função holomorfa `G` serve. -/
theorem kms_por_conjugacao {M M' : VonNeumannAlgebra F} (Ω : F) (Γ : F ≃ₗᵢ[ℂ] F) (hΩ : Γ Ω = Ω)
    (hM : ∀ x : F →L[ℂ] F, x ∈ M ↔ Γ.conjStarAlgEquiv x ∈ M')
    (α : ℝ → (F ≃ₗᵢ[ℂ] F)) (β : ℝ) (hK : KMSBody M Ω α β) :
    KMSBody M' Ω (fun t => Γ.symm.trans ((α t).trans Γ)) β := by
  have hdesc : ∀ X : F →L[ℂ] F, X ∈ M' → Γ.symm.conjStarAlgEquiv X ∈ M := by
    intro X hX
    rw [hM]
    have h : Γ.conjStarAlgEquiv (Γ.symm.conjStarAlgEquiv X) = X := by
      ext y
      simp
    rwa [h]
  intro A hA B hB
  obtain ⟨G, h1, h2, h3, h4⟩ := hK _ (hdesc A hA) _ (hdesc B hB)
  refine ⟨G, h1, h2, ?_, ?_⟩
  · intro t
    rw [h3 t]
    exact inner_conjugado Γ Ω hΩ A B (α t)
  · intro t
    rw [h4 t]
    exact inner_conjugado Γ Ω hΩ B A (α (-t))

end KMSConjugado

/-- a segunda quantização respeita o inverso. -/
theorem gamma_symm' (u : H1 ≃ₗᵢ[ℂ] H1) : F1Rede.BosonicFock.gamma u.symm =
    (F1Rede.BosonicFock.gamma u).symm := by
  apply LinearIsometryEquiv.ext
  intro x
  apply (F1Rede.BosonicFock.gamma u).injective
  rw [LinearIsometryEquiv.apply_symm_apply]
  have h := congrArg (fun e => e x)
    (F1Rede.BosonicFock.gamma_trans u.symm u)
  simp only [LinearIsometryEquiv.symm_trans_self, F1Rede.BosonicFock.gamma_refl,
    LinearIsometryEquiv.trans_apply, LinearIsometryEquiv.coe_refl, id_eq] at h
  exact h.symm

/-- o boost da cunha transformada: `U B0(s) U⁻¹`. -/
def PoincareEl.boost (g : PoincareEl) (s : ℝ) : H1 ≃ₗᵢ[ℂ] H1 :=
  g.unitary.symm.trans ((B0 s).trans g.unitary)

/-- o fluxo da cunha transformada, no Fock: `Γ(U) Γ(B0(2πt)) Γ(U)⁻¹`. -/
def fluxoDaCunha (g : PoincareEl) (t : ℝ) :
    F1Rede.BosonicFock.F ≃ₗᵢ[ℂ] F1Rede.BosonicFock.F :=
  (F1Rede.BosonicFock.gamma g.unitary).symm.trans
    ((F1Rede.BosonicFock.gamma (B0 (2 * Real.pi * t))).trans
      (F1Rede.BosonicFock.gamma g.unitary))

/-- o fluxo conjugado é a segunda quantização do boost da cunha transformada. -/
theorem fluxoDaCunha_eq (g : PoincareEl) (t : ℝ) :
    fluxoDaCunha g t = F1Rede.BosonicFock.gamma (g.boost (2 * Real.pi * t)) := by
  unfold fluxoDaCunha PoincareEl.boost
  rw [F1Rede.BosonicFock.gamma_trans, F1Rede.BosonicFock.gamma_trans, gamma_symm']

/-- ★★ KMS DA CUNHA TRANSFORMADA: o vácuo de Fock é KMS (β = 1) para o fluxo `fluxoDaCunha g` na álgebra de
    Weyl da cunha direita transformada `g.region physicalRightWedge`. Vem de `vacuum_bw_kms` (kernel, cunha
    padrão), de `net`-covariância (`R_covariance`, via `cunha_covariante`) e de `Γ(U) Ω = Ω`. -/
theorem kms_da_cunha_transformada (g : PoincareEl) :
    KMSBody (F1Fecho.FieldWeyl.R (compactLocalized (g.region physicalRightWedge)))
      F1Rede.BosonicFock.vacuum (fluxoDaCunha g) 1 :=
  kms_por_conjugacao (M := F1Fecho.FieldWeyl.R (compactLocalized physicalRightWedge))
    F1Rede.BosonicFock.vacuum (F1Rede.BosonicFock.gamma g.unitary)
    (F1Rede.BosonicFock.gamma_vacuum g.unitary)
    (fun x => F1Fecho.FieldWeyl.R_covariance g.unitary _ _
      (cunha_covariante g physicalRightWedge) x)
    _ 1 F1Fecho.PhysicalFockNet.vacuum_bw_kms

end

end TGLExt.CunhasCovariantesCandidata

#print axioms TGLExt.CunhasCovariantesCandidata.cunha_covariante
#print axioms TGLExt.CunhasCovariantesCandidata.submodulo_da_cunha_e_a_imagem
#print axioms TGLExt.CunhasCovariantesCandidata.cunha_direita_transformada
#print axioms TGLExt.CunhasCovariantesCandidata.cunha_lorentz_transformada
#print axioms TGLExt.CunhasCovariantesCandidata.cunha_de_referencial
#print axioms TGLExt.CunhasCovariantesCandidata.prede_covariante
#print axioms TGLExt.CunhasCovariantesCandidata.prede_padrao
#print axioms TGLExt.CunhasCovariantesCandidata.isotropic_post_da_rede
#print axioms TGLExt.CunhasCovariantesCandidata.prede_em_todo_referencial
#print axioms TGLExt.CunhasCovariantesCandidata.cunha_de_referencial_nao_nula
#print axioms TGLExt.CunhasCovariantesCandidata.kms_por_conjugacao
#print axioms TGLExt.CunhasCovariantesCandidata.fluxoDaCunha_eq
#print axioms TGLExt.CunhasCovariantesCandidata.kms_da_cunha_transformada
