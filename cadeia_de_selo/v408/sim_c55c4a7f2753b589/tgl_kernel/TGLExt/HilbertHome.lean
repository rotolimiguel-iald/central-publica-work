import TGLExt.CovariantCorner

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A morada é o pacote de Hilbert: as quatro propriedades DERIVADAS
  [TGLExt — v56, a Resposta 6 do especialista auditada e kernelizada]

A Resposta 6 (`RESPOSTA_Q6_MORADA_PACOTE_HILBERT.md`) reorganiza o
levantamento: a MORADA é o pacote de fibras de Hilbert L²(C_𝒪, τ_𝒪); o NOME
é a seção Ω; o VERBO é o transporte da conexão; o HABITANTE é o subpacote
ker 𝒟 (não um ponto espectral); o CANTO é a projeção ortogonal derivada
P_F(𝒪) = proj_{ker 𝒟_𝒪}; e as quatro condições do teorema do canto SEGUEM
dos entrelaçamentos de 𝒟. A interface-alvo que o especialista enviou
(`HilbertHomeGlobalLift.lean`, NÃO selada por ele) postulava as quatro
propriedades como CAMPOS — trivialmente habitável (lição v22/v23) e com a
isotonia = `True` placeholder. Esta pedra INVERTE o desenho: só os
ENTRELAÇAMENTOS são hipóteses; as propriedades são TEOREMAS — e valem em
dimensão INFINITA (a primeira pedra do programa fora da sombra finita):

* ★ `ker_map_of_intertwine` — o entrelaçamento `D₂∘U = V∘D₁` (U equivalência
  isométrica, V isometria) transporta o NÚCLEO: `U(ker D₁) = ker D₂`;
* ★ `starProjection_ker_covariant` — COVARIÂNCIA EXTERNA derivada:
  `P_{ker D₂} = U ∘ P_{ker D₁} ∘ U⁻¹` (pointwise; via
  `Submodule.starProjection_map_apply` da mathlib);
* ★ `starProjection_ker_internal_fix` — INVARIÂNCIA INTERNA derivada:
  `D∘U = V∘D ⟹ P∘U = U∘P` (o transporte interno fixa o canto);
* ★ `starProjection_ker_isotone` — ISOTONIA derivada: a inclusão isométrica
  entrelaçada leva núcleo em núcleo e o canto maior FIXA a imagem do menor
  (`P₂(ιx) = ιx` — a forma pontual de `ι P₁ ι* ⪯ P₂`);
* `lagrangian_zero_iff_mem_ker` — a PALAVRA no pacote: `‖Dx‖ = 0 ⟺ x ∈ ker D`
  (EL seleciona o subpacote, agora em Hilbert genérico);
* `HilbertHomeData` — a morada TIPADA: fibras + locks + transportes com
  entrelaçamentos como únicos campos-lei; `PF` é DEF (derivada), com os
  três teoremas `PF_*` como leitura; `BreuerTraceData` — a camada analítica
  0 < τ(P_F) < ∞ como DADOS declarados [KNOWN-EXTERNO: Breuer 1968/69,
  fora da mathlib — jamais fingida como prova];
* ★ `solder_recovers_curvature` — a SOLDA: ρ* injetiva ⟹ F determina R
  único (a recuperação `R = ρ*⁻¹(F_∇)` é bem-posta).

HONESTIDADE. O que esta pedra NÃO faz: construir o pacote a partir da rede
III₁ — o próprio especialista o declara ("o conteúdo não trivial é construir
o pacote"). O teorema aberto é agora ÚNICO e nomeado:
`TGL_SOLDERED_BREUER_HILBERT_PACKAGE` — a existência canônica de
(𝒟_𝒪, transportes, τ, solda) derivada de ω(I)=1. Gravidade quântica
comprovada incondicionalmente: AINDA NÃO. β JAMAIS entra. Sem sorry, sem
axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Submodule
open scoped ENNReal

noncomputable section

variable {H₁ H₂ W₁ W₂ : Type}
  [NormedAddCommGroup H₁] [InnerProductSpace ℂ H₁] [CompleteSpace H₁]
  [NormedAddCommGroup H₂] [InnerProductSpace ℂ H₂] [CompleteSpace H₂]
  [NormedAddCommGroup W₁] [NormedSpace ℂ W₁]
  [NormedAddCommGroup W₂] [NormedSpace ℂ W₂]

/-! ## A — o núcleo transportado e as projeções derivadas (dimensão infinita OK) -/

/-- [KERNEL] ★ O ENTRELAÇAMENTO TRANSPORTA O NÚCLEO: se `D₂∘U = V∘D₁` com
    `U` equivalência isométrica e `V` isometria (injetiva), então
    `U(ker D₁) = ker D₂` — o subpacote físico é levado exatamente no
    subpacote físico. -/
theorem ker_map_of_intertwine (U : H₁ ≃ₗᵢ[ℂ] H₂) (D₁ : H₁ →L[ℂ] W₁)
    (D₂ : H₂ →L[ℂ] W₂) (V : W₁ →ₗᵢ[ℂ] W₂)
    (h : ∀ x, D₂ (U x) = V (D₁ x)) :
    D₁.ker.map (U.toLinearEquiv : H₁ →ₗ[ℂ] H₂) = D₂.ker := by
  ext y
  simp only [Submodule.mem_map, LinearMap.mem_ker, ContinuousLinearMap.coe_coe]
  constructor
  · rintro ⟨x, hx0, rfl⟩
    show D₂ (U x) = 0
    rw [h x, hx0, map_zero]
  · intro hy
    refine ⟨U.symm y, ?_, ?_⟩
    · have hUy := h (U.symm y)
      rw [U.apply_symm_apply] at hUy
      have h0 : V (D₁ (U.symm y)) = 0 := by
        rw [← hUy]
        exact hy
      exact V.injective (by simpa using h0)
    · show U (U.symm y) = y
      exact U.apply_symm_apply y

/-- [KERNEL] ★ COVARIÂNCIA EXTERNA DERIVADA: o canto do pacote é
    `P_{ker D₂} = U ∘ P_{ker D₁} ∘ U⁻¹` — a condição (3) do teorema do canto
    deixa de ser hipótese: SEGUE do entrelaçamento. -/
theorem starProjection_ker_covariant (U : H₁ ≃ₗᵢ[ℂ] H₂) (D₁ : H₁ →L[ℂ] W₁)
    (D₂ : H₂ →L[ℂ] W₂) (V : W₁ →ₗᵢ[ℂ] W₂)
    (h : ∀ x, D₂ (U x) = V (D₁ x)) (y : H₂) :
    D₂.ker.starProjection y
      = U (D₁.ker.starProjection (U.symm y)) := by
  have hmap := starProjection_map_apply U D₁.ker y
  simp only [ker_map_of_intertwine U D₁ D₂ V h] at hmap
  exact hmap

/-- [KERNEL] ★ INVARIÂNCIA INTERNA DERIVADA: `D∘U = V∘D ⟹ P∘U = U∘P` — o
    transporte interno fixa o canto do pacote (condição (2), agora teorema). -/
theorem starProjection_ker_internal_fix (U : H₁ ≃ₗᵢ[ℂ] H₁)
    (D : H₁ →L[ℂ] W₁) (V : W₁ →ₗᵢ[ℂ] W₁)
    (h : ∀ x, D (U x) = V (D x)) (x : H₁) :
    D.ker.starProjection (U x) = U (D.ker.starProjection x) := by
  have hcov := starProjection_ker_covariant U D D V h (U x)
  rw [U.symm_apply_apply] at hcov
  exact hcov

/-- [KERNEL] ★ ISOTONIA DERIVADA: a inclusão isométrica entrelaçada leva
    núcleo em núcleo, e o canto da região maior FIXA a imagem do menor —
    `P₂(ι x) = ι x` para `x ∈ ker D₁` (a forma pontual de `ι P₁ ι* ⪯ P₂`;
    condição (4), agora teorema — o `True` placeholder da interface do
    especialista substituído pelo enunciado genuíno). -/
theorem starProjection_ker_isotone (ι : H₁ →ₗᵢ[ℂ] H₂) (D₁ : H₁ →L[ℂ] W₁)
    (D₂ : H₂ →L[ℂ] W₂) (V : W₁ →ₗᵢ[ℂ] W₂)
    (h : ∀ x, D₂ (ι x) = V (D₁ x)) {x : H₁} (hx : x ∈ D₁.ker) :
    D₂.ker.starProjection (ι x) = ι x := by
  rw [starProjection_eq_self_iff]
  show D₂ (ι x) = 0
  have hx0 : D₁ x = 0 := hx
  rw [h x, hx0, map_zero]

/-- [KERNEL] A PALAVRA NO PACOTE: a ação de um lock anula sse o vetor está
    no subpacote físico — Euler–Lagrange seleciona `ker D` em Hilbert
    genérico (a versão de pacote do `action_locks_zero_iff` do v54). -/
theorem lagrangian_zero_iff_mem_ker (D : H₁ →L[ℂ] W₁) (x : H₁) :
    ‖D x‖ = 0 ↔ x ∈ D.ker := by
  rw [norm_eq_zero]
  exact Iff.rfl

end

/-! ## B — a morada tipada: entrelaçamentos como únicas leis; P_F DERIVADA -/

section HomeStructure

variable (Region : Type) (leR : Region → Region → Prop)
  (H : Region → Type) (W : Region → Type)
  [∀ O, NormedAddCommGroup (H O)] [∀ O, InnerProductSpace ℂ (H O)]
  [∀ O, CompleteSpace (H O)]
  [∀ O, NormedAddCommGroup (W O)] [∀ O, NormedSpace ℂ (W O)]

/-- A MORADA (dados): fibras de Hilbert + locks 𝒟_𝒪 + transportes interno/
    externo/inclusão, com os ENTRELAÇAMENTOS como únicas leis. O canto NÃO é
    campo: é derivado (`HilbertHomeData.PF`). Rigidez: não há propriedade do
    canto a postular — quem habita este tipo só fornece dados e
    entrelaçamentos; as quatro condições saem por teorema. -/
structure HilbertHomeData where
  /-- o operador dos Three Locks de cada região (𝒟_𝒪). -/
  locks : ∀ O, H O →L[ℂ] W O
  /-- o transporte modular interno (λ_𝒪(s)) e sua face no alvo. -/
  internal : ∀ O, ℝ → (H O ≃ₗᵢ[ℂ] H O)
  internalW : ∀ O, ℝ → (W O →ₗᵢ[ℂ] W O)
  /-- entrelaçamento interno: `𝒟 λ(s) = λ(s) 𝒟`. -/
  internal_intertwines : ∀ O s x,
    locks O ((internal O s) x) = internalW O s (locks O x)
  /-- o grupo externo e sua ação nas regiões. -/
  G : Type
  act : G → Region → Region
  external : ∀ g O, H O ≃ₗᵢ[ℂ] H (act g O)
  externalW : ∀ g O, W O →ₗᵢ[ℂ] W (act g O)
  /-- entrelaçamento externo: `𝒟_{g𝒪} U_g = U_g 𝒟_𝒪`. -/
  external_intertwines : ∀ g O x,
    locks (act g O) ((external g O) x) = externalW g O (locks O x)
  /-- inclusões isométricas das fibras (isotonia da rede). -/
  incl : ∀ {O₁ O₂}, leR O₁ O₂ → (H O₁ →ₗᵢ[ℂ] H O₂)
  inclW : ∀ {O₁ O₂}, leR O₁ O₂ → (W O₁ →ₗᵢ[ℂ] W O₂)
  /-- entrelaçamento da inclusão: `𝒟_{𝒪₂} ι = ι 𝒟_{𝒪₁}`. -/
  incl_intertwines : ∀ {O₁ O₂} (hle : leR O₁ O₂) (x : H O₁),
    locks O₂ ((incl hle) x) = inclW hle (locks O₁ x)

end HomeStructure

noncomputable section

variable {Region : Type} {leR : Region → Region → Prop}
  {H W : Region → Type}
  [∀ O, NormedAddCommGroup (H O)] [∀ O, InnerProductSpace ℂ (H O)]
  [∀ O, CompleteSpace (H O)]
  [∀ O, NormedAddCommGroup (W O)] [∀ O, NormedSpace ℂ (W O)]

/-- ★ O CANTO DERIVADO: `P_F(𝒪) = proj_{ker 𝒟_𝒪}` — definição, não campo. -/
def HilbertHomeData.PF (P : HilbertHomeData Region leR H W) (O : Region) :
    H O →L[ℂ] H O :=
  (P.locks O).ker.starProjection

/-- [KERNEL] ★ (2) do teorema do canto, DERIVADA no pacote. -/
theorem HilbertHomeData.PF_internal_fix (P : HilbertHomeData Region leR H W)
    (O : Region) (s : ℝ) (x : H O) :
    P.PF O ((P.internal O s) x) = (P.internal O s) (P.PF O x) :=
  starProjection_ker_internal_fix (P.internal O s) (P.locks O)
    (P.internalW O s) (P.internal_intertwines O s) x

/-- [KERNEL] ★ (3) do teorema do canto, DERIVADA no pacote. -/
theorem HilbertHomeData.PF_external_covariant
    (P : HilbertHomeData Region leR H W) (g : P.G) (O : Region)
    (y : H (P.act g O)) :
    P.PF (P.act g O) y
      = (P.external g O) (P.PF O ((P.external g O).symm y)) :=
  starProjection_ker_covariant (P.external g O) (P.locks O)
    (P.locks (P.act g O)) (P.externalW g O)
    (P.external_intertwines g O) y

/-- [KERNEL] ★ (4) do teorema do canto, DERIVADA no pacote. -/
theorem HilbertHomeData.PF_isotone (P : HilbertHomeData Region leR H W)
    {O₁ O₂ : Region} (hle : leR O₁ O₂) {x : H O₁}
    (hx : x ∈ (P.locks O₁).ker) :
    P.PF O₂ ((P.incl hle) x) = (P.incl hle) x :=
  starProjection_ker_isotone (P.incl hle) (P.locks O₁) (P.locks O₂)
    (P.inclW hle) (P.incl_intertwines hle) hx

/-- A CAMADA DE BREUER [KNOWN-EXTERNO, declarada como DADOS — jamais fingida
    como prova]: o traço semifinito do core com `0 < τ(P_F) < ∞`, garantido
    pela teoria de Breuer–Fredholm (Breuer 1968/69) quando cada lock é
    Breuer–Fredholm com núcleo não-nulo — a condição (1). A construção
    canônica desta camada a partir da rede III₁ é O teorema aberto
    (`TGL_SOLDERED_BREUER_HILBERT_PACKAGE`). -/
structure BreuerTraceData (P : HilbertHomeData Region leR H W) where
  tau : ∀ O, (H O →L[ℂ] H O) → ℝ≥0∞
  tau_PF_pos : ∀ O, 0 < tau O (P.PF O)
  tau_PF_finite : ∀ O, tau O (P.PF O) < ⊤

/-! ## C — a solda: a recuperação da curvatura é bem-posta -/

/-- [KERNEL] ★ A SOLDA RECUPERA A CURVATURA: se a representação `ρ*` é
    INJETIVA (fidelidade), então cada curvatura de gauge `F` na imagem
    determina UM ÚNICO tensor `R` com `ρ*(R) = F` — a passagem
    `R_{μνρσ} = ρ*⁻¹(F_∇)` é bem-posta. Sem a fidelidade, os negativos
    corretos são `holonomy_not_geometric` / `modular_metric_not_unique`. -/
theorem solder_recovers_curvature {A B : Type} [AddCommGroup A]
    [AddCommGroup B] [Module ℂ A] [Module ℂ B] (ρ : A →ₗ[ℂ] B)
    (hρ : Function.Injective ρ) {F : B} (hF : F ∈ LinearMap.range ρ) :
    ∃! R : A, ρ R = F := by
  obtain ⟨R, hR⟩ := hF
  exact ⟨R, hR, fun R' hR' => hρ (by rw [hR', hR])⟩

end

end TGLExt
