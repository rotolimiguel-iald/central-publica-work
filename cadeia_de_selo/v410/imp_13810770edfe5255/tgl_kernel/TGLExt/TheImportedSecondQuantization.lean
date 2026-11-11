import TGLExt.ContratoQG_v32
import TGLExt.O16.OrbitalBoostUnitary_v2
import TGLExt.O16.OrbitalPositiveEnergyContract
import TGLExt.O16.WedgeDraggedFrame_v6
import TGLExt.O16.ConstructedImportH3_v2
import TGLExt.Solder4D

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# A SEGUNDA QUANTIZAÇÃO IMPORTADA: o contrato v3.2 da TGL HABITADO SOB HIPÓTESES NOMEADAS (a QG por citação)
  [TGLExt — v372, pedra da gerência (26/09/2026)]

Ordem do operador (26/09/2026, verbatim): «concordo com tudo, mas quero que vc execute tudo, não quero ordem 17,
execute o que falta e rode a próxima versão antes do ringdown» · «ou seja, a próxima versão é a versão com a
solução da gravidade quantica toda formalizada». Regra de quitação do operador (27/08/2026, verbatim em
`TheImportedEquilibrium`): «levar a H3 como KNOWN não é falta de prova, é justamente usar prova pré-concebida, ou
prova emprestada, eu não preciso pagar o preço de nada que já foi pago antes de mim.»

## O que esta pedra PROVA (sem sorry, sem axiom)

`qg_formalized_by_citation`: dados (i) a camada de UMA partícula da luz, (ii) o funtor de segunda quantização,
(iii) o tensor de Maxwell e (iv) G, existem habitantes de `ContratoH2v32`, `ContratoH3v32` e
`ContratoImportH3v32` — o contrato v3.2 inteiro — sobre o par construído, para TODO relógio N.

## O que é CITADO (hipóteses NOMEADAS, cada campo com a fonte; nunca `axiom`)

* `LightOneParticle` — a representação de Wigner da luz (m = 0, helicidade ±1) [Wigner 1939] e a rede de
  subespaços reais padrão da localização modular [Brunetti–Guido–Longo, Rev. Math. Phys. 14 (2002) 759].
  O espaço e as TRANSLAÇÕES são os OBJETOS PAGOS da bancada (`orbitalTranslation 0`, ORDEM 016 A-3), não citados.
* `FockCertificate` — a segunda quantização bosônica funtorial [Araki 1963; Leyland–Roberts–Testard 1978],
  Reeh–Schlieder e Bisognano–Wichmann para a cunha [Bisognano–Wichmann 1975/76; BGL 2002], Tomita–Takesaki,
  o núcleo de Takesaki [Takesaki 1973] e a semifinitude do núcleo de um fator III₁ [Connes 1973; Takesaki 1973].
* `MaxwellCertificate` — o tensor de Maxwell ordenado por Wick como forma no Fock [Wightman; campos livres], o
  elo da carga modular no plano nulo [Casini–Teste–Torroba 2017; Wall 2011] e um estado coerente regular de
  energia modular não nula [Longo, Lett. Math. Phys. 109 (2019) 2587].
* G > 0 [INPUT na rota de Jacobson, PRL 75 (1995) 1260 — o contrato já prova `G_not_predicted`].

## O que é COMPOSTO aqui, e o que NÃO é (cético da gerência, 26/09 — medido)

COMPOSTO de verdade: translações fiéis ⟸ `Γ_one_particle` + ι injetivo + `orbitalTranslation_faithful` [PAGO];
covariância dos boosts (`V_translations`, `V_net`) ⟸ funtorialidade + `B0_conj` [PAGO] + `R_cov` + `K_boost`; o frame ⟸
`wedgeFrame` [PAGO]; a tela plana ⟸ conta aqui; κ = 1/ρ(N) ⟸ `ContratoH2.observer_unit_of_index`; H3 ⟸ `H3_of_null_solution` +
`construct_null_solution` [PAGO]; a classe admissível (vácuo e translação provados).
CITAÇÃO, não composição: energia positiva (o conteúdo no Fock é `Γ_positive`; o PAGO só descarrega a premissa);
ergodicidade nula (`Γ_no_fixed` + `null_no_eigen`, ambos citados); KMS (reenuncia `bw_kms`).
IDENTIDADES POR CONSTRUÇÃO (não contam): `bw` (Δ^{it} := V(−2πt)); `flow_implemented` (o fluxo é dado como Ad Γ(B));
os locks (H3Lt := 1 − P_F: `PF_locks`/`PF_maximal` são álgebra — é a FORMA do lock mínimo do kernel, V354RegularSusy);
`raychaudhuri_einstein` (a resposta é construída como a solução nula); `pair_realization` = `source_realization` =
`tomita` (o mesmo campo); `same_horizon` (autorreconhecimento, U = 1); `photon_mass`.

## Limitações ditas (não disfarçadas)

* HELICIDADE: no grupo que o contrato enxerga (translações + boosts de UMA cunha) a helicidade NÃO é observável — a fase de
  Wigner de um subgrupo a um parâmetro é removível por calibre. `helicity` é o RÓTULO da representação citada [Wigner
  1939]; o escalar sem massa DUPLICADO também satisfaz as hipóteses. A distinção fóton/escalar vive nas rotações e no PCT,
  FORA do tipo (W não tem rotações). `massless_scalar_refused` recusa o RÓTULO 0, não o conteúdo escalar.
* TRAÇO: o tipo canônico `ContinuousCoreData` exige um traço TOTAL, tracial em todo par; o traço de Takesaki vive no cone
  positivo. A extensão total é NÃO-PADRÃO (satisfazível: o cético exibiu uma, por idempotentes de Riesz).
* MAXWELL/CTT: `charge_link` só vale no domínio NOMEADO `Dom` (invariante, com o vácuo) e com integrabilidade conjunta no
  plano nulo; Casini–Teste–Torroba/Wall são derivações de FÍSICA [KNOWN-física]; o rigoroso publicado é para o escalar
  livre (Morinelli–Tanimoto–Wegener 2022, a conferir).
* NÃO-VACUIDADE: nenhum habitante de `FockCertificate` ou `MaxwellCertificate` é exibido; a não-vacuidade é ARGUMENTADA
  (o campo livre da literatura), não provada — como o «VACUIDADE, dita» do contrato v3.1.

## Estatuto, sem enfeite

**PROVADA POR CITAÇÃO** — implicação fechada a partir de hipóteses NOMEADAS (§0.1(c) da ORDEM 016). O axioma ω(I) = 1 e
β NÃO entram nesta implicação; o conteúdo TGL vem dos TIPOS (o contrato, os Three Locks, κ por N).
NÃO é «PROVADA por termo»: nenhum habitante é exibido sem as hipóteses, e os três nomes reservados do gate NÃO
são cunhados aqui (o leitor A-8 por tipo exato ACEITA o alvo por citação e RECUSA o habitante fechado: `QGReaderUVLock`).
H_min: H3Lt := 1 − P_F é a FORMA do lock mínimo do kernel (V354RegularSusy); a identificação MICROSCÓPICA no Fock da luz
(o zero de H_min = o núcleo do Hamiltoniano oculto K = −log Δ = a reta do vácuo) está em `QGReaderUVLock` §4. UV: DISSOLVIDA PELA TIPAGEM (`QGReaderUVLock.uv_dissolved_by_typing`: a métrica não é quantizada). NOT_FALSIFIED ≠
CONFIRMED; PROVADA ≠ CONFIRMADA.
-/

noncomputable section
namespace TGLExt.ImportedSQ
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerGeometry016
open TGLExt.ContratoQGv31.ProbeResidual ChatgptAudit.TeleologicalConstruct016
open MeasureTheory Matrix Complex Set
open scoped InnerProductSpace

/-- a fibra de helicidade (duas componentes complexas). -/
abbrev Fib := EuclideanSpace ℂ (Fin 2)

/-- o espaço de UMA partícula da luz: L² da órbita sem massa [PAGO — ORDEM 016 A-3]. -/
abbrev H1 := Lp Fib 2 (orbitalMeasure 0)

/-- as translações de uma partícula [PAGO]. -/
abbrev U1 (a : Fin 4 → ℝ) : H1 ≃ₗᵢ[ℂ] H1 := orbitalTranslationEquiv 0 a

/-- estados de vetor de uma partícula com energia positiva, na forma analítica do contrato. -/
def OneParticlePositiveEnergy : Prop :=
  ∀ a ∈ forwardCone, ∀ f : H1, ∃ F : ℂ → ℂ, DiffContOnCl ℂ F upperHalf ∧
    (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖F z‖ ≤ M) ∧ (∀ t : ℝ, F t = ⟪f, U1 (t • a) f⟫_ℂ)

/-- [PAGO] a energia positiva de uma partícula (A-3.2 da bancada). -/
theorem oneParticle_positive_energy : OneParticlePositiveEnergy := by
  intro a ha f
  obtain ⟨F, h1, h2, h3⟩ := orbital_positive_energy_v31_shape (E := Fib) 0 a ha f
  exact ⟨F, h1, h2, fun t => by rw [h3 t]; rfl⟩

/-! ## 1. A camada de uma partícula da luz -/

/-- o boost da cunha: o boost orbital PAGO da bancada (ORDEM 016 A-3.3), agindo nas duas componentes de helicidade.
    Por que ele representa a LUZ neste grupo: ao longo de UM subgrupo a um parâmetro de boosts, a fase de Wigner da
    helicidade é um COBORDO (ação livre e própria de ℝ na órbita sem massa, com transversal boreliana), logo removível por
    um multiplicador que comuta com as translações [KNOWN — trivialidade de cociclos para ações livres próprias; a conferir].
    A helicidade só se vê nas rotações e no PCT, fora do tipo do contrato (ver «Limitações»). -/
def B0 (s : ℝ) : H1 ≃ₗᵢ[ℂ] H1 := orbitalBoostUnitary (E := Fib) 0 s

/-- [PAGO] -/
theorem B0_zero : B0 0 = LinearIsometryEquiv.refl ℂ H1 := orbitalBoostUnitary_zero (E := Fib) 0

/-- [PAGO] -/
theorem B0_add (s t : ℝ) : B0 (s + t) = (B0 t).trans (B0 s) := orbitalBoostUnitary_add (E := Fib) 0 s t

/-- [PAGO] -/
theorem B0_continuous (f : H1) : Continuous (fun s => B0 s f) :=
  orbitalBoostUnitary_strongly_continuous (E := Fib) 0 f

/-- [PAGO] o boost conjuga as translações pela ação geométrica (A-3.3). -/
theorem B0_conj (s : ℝ) (a : Fin 4 → ℝ) :
    (B0 s).conjStarAlgEquiv (orbitalTranslation (E := Fib) 0 a) = orbitalTranslation (E := Fib) 0 (wedgeBoostMap s a) :=
  orbitalBoostUnitary_conj_translations (E := Fib) 0 s a

/-- [PAGO] o boost de uma partícula não tem autovetor (ProductOrbitalSpectrum_v3). -/
theorem B0_no_eigen (f : H1) (h : ∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ B0 s f = c • f) : f = 0 :=
  orbitalScalarBoost_no_eigen (E := Fib) 0 f h

/-- **LightOneParticle** — o rótulo de helicidade e a rede de subespaços reais [CITADO: Wigner 1939; BGL 2002].
    As TRANSLAÇÕES (`U1`) e o BOOST (`B0`) são os PAGOS pela bancada. -/
structure LightOneParticle where
  /-- a helicidade da representação: ±1 (a luz). -/
  helicity : ℤ
  helicity_light : helicity = 1 ∨ helicity = -1
  /-- a rede de subespaços reais padrão (localização modular) [BGL 2002]. -/
  K : Set (Fin 4 → ℝ) → Submodule ℝ H1
  K_mono : ∀ O₁ O₂ : Set (Fin 4 → ℝ), O₁ ⊆ O₂ → K O₁ ≤ K O₂
  /-- localidade de uma partícula: regiões tipo-espaço dão subespaços simpleticamente ortogonais. -/
  K_local : ∀ O₁ O₂ : Set (Fin 4 → ℝ), SpacelikeSep O₁ O₂ →
    ∀ f ∈ K O₁, ∀ g ∈ K O₂, (⟪f, g⟫_ℂ).im = 0
  K_translate : ∀ (a : Fin 4 → ℝ) (O : Set (Fin 4 → ℝ)) (f : H1), f ∈ K O ↔ U1 a f ∈ K (TGL.SpecificAQFT.translate a O)
  K_boost : ∀ (s : ℝ) (O : Set (Fin 4 → ℝ)) (f : H1), f ∈ K O ↔ B0 s f ∈ K (wedgeBoostMap s '' O)
  /-- continuidade forte das translações de uma partícula [KNOWN — convergência dominada; não formalizado]. -/
  U1_continuous : ∀ f : H1, Continuous (fun a : Fin 4 → ℝ => U1 a f)
  /-- as translações nulas não têm autovetor [KNOWN — p·n tem distribuição absolutamente contínua na órbita
      sem massa (a superfície p·n = c tem medida nula); não formalizado]. -/
  null_no_eigen : ∀ f : H1, (∀ l : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ U1 (l • nullDir) f = c • f) → f = 0

/-! ## 2. O certificado de Fock -/

/-- o corpo da condição KMS a β para (M, Ω, α) — a MESMA forma de `KMSAt`, sem o W. -/
def KMSBody {F : Type} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]
    (M : VonNeumannAlgebra F) (Ω : F) (α : ℝ → (F ≃ₗᵢ[ℂ] F)) (β : ℝ) : Prop :=
  ∀ A : F →L[ℂ] F, A ∈ M → ∀ B : F →L[ℂ] F, B ∈ M → ∃ G : ℂ → ℂ,
    DiffContOnCl ℂ G (kmsStrip β) ∧
    (∃ C : ℝ, ∀ z : ℂ, 0 ≤ z.im → z.im ≤ β → ‖G z‖ ≤ C) ∧
    (∀ t : ℝ, G t = ⟪(star A) Ω, α t (B Ω)⟫_ℂ) ∧
    (∀ t : ℝ, G (t + β * I) = ⟪(star B) Ω, α (-t) (A Ω)⟫_ℂ)

/-- **FockCertificate L** — a segunda quantização da luz, CITADA campo a campo. -/
structure FockCertificate (L : LightOneParticle) where
  F : Type
  [instN : NormedAddCommGroup F]
  [instI : InnerProductSpace ℂ F]
  [instC : CompleteSpace F]
  /-- o vácuo de Fock. -/
  Ω : F
  Ω_norm : ‖Ω‖ = 1
  /-- o Fock é de dimensão infinita [KNOWN]. -/
  F_infinite : ¬ FiniteDimensional ℂ F
  /-- o funtor de segunda quantização nos unitários [Araki 1963; LRT 1978]. -/
  Γ : (H1 ≃ₗᵢ[ℂ] H1) → (F ≃ₗᵢ[ℂ] F)
  Γ_refl : Γ (LinearIsometryEquiv.refl ℂ H1) = LinearIsometryEquiv.refl ℂ F
  Γ_trans : ∀ u v : H1 ≃ₗᵢ[ℂ] H1, Γ (u.trans v) = (Γ u).trans (Γ v)
  Γ_vac : ∀ u : H1 ≃ₗᵢ[ℂ] H1, Γ u Ω = Ω
  /-- o setor de uma partícula e a sua preservação: Γ(u) ∘ ι = ι ∘ u. -/
  ι : H1 →ₗᵢ[ℂ] F
  Γ_one_particle : ∀ (u : H1 ≃ₗᵢ[ℂ] H1) (ξ : H1), Γ u (ι ξ) = ι (u ξ)
  /-- continuidade forte transportada [KNOWN]. -/
  Γ_strong : ∀ u : ℝ → (H1 ≃ₗᵢ[ℂ] H1), (∀ ξ, Continuous (fun s => u s ξ)) →
    ∀ ψ : F, Continuous (fun s => Γ (u s) ψ)
  Γ_strong4 : ∀ u : (Fin 4 → ℝ) → (H1 ≃ₗᵢ[ℂ] H1), (∀ ξ, Continuous (fun a => u a ξ)) →
    ∀ ψ : F, Continuous (fun a => Γ (u a) ψ)
  /-- a condição espectral é preservada pela segunda quantização [KNOWN]. -/
  Γ_positive : OneParticlePositiveEnergy →
    ∀ a ∈ forwardCone, ∀ ψ : F, ∃ G : ℂ → ℂ, DiffContOnCl ℂ G upperHalf ∧
      (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖G z‖ ≤ M) ∧ (∀ t : ℝ, G t = ⟪ψ, Γ (U1 (t • a)) ψ⟫_ℂ)
  /-- sem espectro pontual em uma partícula ⟹ só o vácuo é fixo no Fock [KNOWN; demonstração escrita da
      bancada, DIAMANTE_MODULAR 16/09, por Fubini]. -/
  Γ_no_fixed : ∀ u : ℝ → (H1 ≃ₗᵢ[ℂ] H1),
    u 0 = LinearIsometryEquiv.refl ℂ H1 → (∀ s t, u (s + t) = (u t).trans (u s)) →
    (∀ ξ, Continuous (fun s => u s ξ)) →
    (∀ f : H1, (∀ l : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ u l f = c • f) → f = 0) →
    ∀ ψ : F, (∀ l : ℝ, Γ (u l) ψ = ψ) → ψ ∈ (ℂ ∙ Ω)
  /-- a álgebra de Weyl de um subespaço real [Araki 1963]. -/
  R : Submodule ℝ H1 → VonNeumannAlgebra F
  R_mono : ∀ K K' : Submodule ℝ H1, K ≤ K' → (R K : Set (F →L[ℂ] F)) ⊆ R K'
  R_local : ∀ K K' : Submodule ℝ H1, (∀ f ∈ K, ∀ g ∈ K', (⟪f, g⟫_ℂ).im = 0) →
    ∀ x ∈ R K, ∀ y ∈ R K', Commute x y
  /-- covariância funtorial: se u leva K em K', Ad Γ(u) leva R K em R K'. -/
  R_cov : ∀ (u : H1 ≃ₗᵢ[ℂ] H1) (K K' : Submodule ℝ H1), (∀ f, f ∈ K ↔ u f ∈ K') →
    ∀ x : F →L[ℂ] F, x ∈ R K ↔ (Γ u).conjStarAlgEquiv x ∈ R K'
  /-- Reeh–Schlieder na cunha (K(W) padrão) [Araki 1963; BGL 2002]. -/
  wedge_cyclic : Dense ((Submodule.span ℂ
      ((fun T : F →L[ℂ] F => T Ω) '' (R (L.K rightWedge) : Set (F →L[ℂ] F))) : Submodule ℂ F) : Set F)
  wedge_separating : ∀ a ∈ R (L.K rightWedge), (a : F →L[ℂ] F) Ω = 0 → a = 0
  wedge_nonabelian : ∃ a ∈ R (L.K rightWedge), ∃ b ∈ R (L.K rightWedge), a * b ≠ b * a
  /-- ★ BISOGNANO–WICHMANN da luz: o boost segundo-quantizado em 2πt satisfaz KMS a β = 1 na cunha
      [Bisognano–Wichmann 1975/76; BGL 2002 + Araki 1963]. -/
  bw_kms : KMSBody (R (L.K rightWedge)) Ω (fun t => Γ (B0 (2 * Real.pi * t))) 1
  /-- a conjugação modular [Tomita–Takesaki; BGL 2002 — o PCT]. -/
  J : F ≃ₛₗᵢ[starRingEnd ℂ] F
  J_invol : ∀ ξ : F, J (J ξ) = ξ
  J_vac : J Ω = Ω
  /-- a realização analítica de Tomita do par [Tomita–Takesaki]. -/
  tomita : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
    (R (L.K rightWedge)).toStarSubalgebra Ω J (fun t => Γ (B0 (-(2 * Real.pi * t))))
  /-- o fluxo modular como automorfismo da cunha (Ad Δ^{it} preserva M) [Tomita–Takesaki]. -/
  flow : ℝ → ((R (L.K rightWedge)).toStarSubalgebra ≃⋆ₐ[ℂ] (R (L.K rightWedge)).toStarSubalgebra)
  flow_zero : flow 0 = StarAlgEquiv.refl
  flow_add : ∀ s t : ℝ, flow (s + t) = (flow s).trans (flow t)
  flow_is_Ad : ∀ (t : ℝ) (a : (R (L.K rightWedge)).toStarSubalgebra),
    ((flow t) a).val = (Γ (B0 (-(2 * Real.pi * t)))).conjStarAlgEquiv a.val
  /-- o núcleo de Takesaki [Takesaki 1973]. -/
  Core : Type
  [instCR : Ring Core]
  [instCS : StarRing Core]
  [instCA : Algebra ℂ Core]
  embedding : (R (L.K rightWedge)).toStarSubalgebra →⋆ₐ[ℂ] Core
  embedding_injective : Function.Injective embedding
  dualAction : ℝ → (Core ≃⋆ₐ[ℂ] Core)
  dualAction_zero : dualAction 0 = StarAlgEquiv.refl
  dualAction_add : ∀ s t : ℝ, dualAction (s + t) = (dualAction s).trans (dualAction t)
  trace : Core → ENNReal
  trace_zero : trace 0 = 0
  trace_tracial : ∀ x y : Core, trace (x * y) = trace (y * x)
  trace_star : ∀ x : Core, trace (star x) = trace x
  trace_dual_scaling : ∀ (s : ℝ) (x : Core),
    trace ((dualAction s) x) = ENNReal.ofReal (Real.exp (-s)) * trace x
  /-- uma projeção finita não nula do núcleo II_∞, partida em duas metades de traço igual [Connes 1973]. -/
  PF : Core
  PF_sa : star PF = PF
  PF_idem : PF * PF = PF
  PF_ne : PF ≠ 0
  PF_pos : 0 < trace PF
  PF_fin : trace PF < ⊤
  Pp : Core
  Pm : Core
  Pp_sa : star Pp = Pp
  Pp_idem : Pp * Pp = Pp
  Pm_sa : star Pm = Pm
  Pm_idem : Pm * Pm = Pm
  split : Pp + Pm = PF
  orth : Pp * Pm = 0
  trace_additive : trace PF = trace Pp + trace Pm
  equal_halves : trace Pp = trace Pm

attribute [instance] FockCertificate.instN FockCertificate.instI FockCertificate.instC
attribute [instance] FockCertificate.instCR FockCertificate.instCS FockCertificate.instCA

variable {L : LightOneParticle} (C : FockCertificate L)

theorem Γ_symm (u : H1 ≃ₗᵢ[ℂ] H1) : C.Γ u.symm = (C.Γ u).symm := by
  have h1 : C.Γ (u.trans u.symm) = (C.Γ u).trans (C.Γ u.symm) := C.Γ_trans u u.symm
  rw [LinearIsometryEquiv.self_trans_symm, C.Γ_refl] at h1
  apply LinearIsometryEquiv.ext; intro ψ
  have := congrArg (fun e : C.F ≃ₗᵢ[ℂ] C.F => e ((C.Γ u).symm ψ)) h1
  simp only [LinearIsometryEquiv.coe_trans, Function.comp_apply, LinearIsometryEquiv.apply_symm_apply] at this
  exact this.symm

theorem U1_zero : U1 0 = LinearIsometryEquiv.refl ℂ H1 := by
  apply LinearIsometryEquiv.ext; intro f
  exact orbitalTranslation_zero 0 f

theorem U1_add (v w : Fin 4 → ℝ) : U1 (v + w) = (U1 w).trans (U1 v) := by
  apply LinearIsometryEquiv.ext; intro f
  show orbitalTranslation 0 (v + w) f = orbitalTranslation 0 v (orbitalTranslation 0 w f)
  rw [orbitalTranslation_add]

theorem U1_neg (v : Fin 4 → ℝ) : U1 (-v) = (U1 v).symm := by
  apply LinearIsometryEquiv.ext; intro f
  apply (U1 v).injective
  rw [LinearIsometryEquiv.apply_symm_apply]
  show orbitalTranslation 0 v (orbitalTranslation 0 (-v) f) = f
  simpa only [neg_neg] using orbitalTranslation_inverse (E := Fib) 0 (-v) f

/-! ## 3. O par: a rede da luz -/

/-- as translações no Fock como operadores. -/
def UF (a : Fin 4 → ℝ) : C.F →L[ℂ] C.F := (C.Γ (U1 a)).toContinuousLinearEquiv.toContinuousLinearMap

theorem UF_apply (a : Fin 4 → ℝ) (ψ : C.F) : UF C a ψ = C.Γ (U1 a) ψ := rfl

theorem UF_conj (a : Fin 4 → ℝ) (x : C.F →L[ℂ] C.F) :
    UF C a * x * UF C (-a) = (C.Γ (U1 a)).conjStarAlgEquiv x := by
  apply ContinuousLinearMap.ext; intro ψ
  rw [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply]
  simp only [ContinuousLinearMap.mul_apply, UF_apply, U1_neg, Γ_symm]

/-- **lightNet L C** — o W da luz: Fock, rede de Weyl dos subespaços K(O), vácuo, translações. -/
def lightNet : TGLSpecificAQFTWitness where
  m := 0
  H := C.F
  net := fun O => C.R (L.K O)
  vac := C.Ω
  U := UF C
  helicity := L.helicity
  peso_do_nome := Or.inr (by rcases L.helicity_light with h | h <;> rw [h] <;> decide)
  vac_norm := C.Ω_norm
  isotony := fun O₁ O₂ h => C.R_mono _ _ (L.K_mono O₁ O₂ h)
  locality := fun O₁ O₂ h => C.R_local _ _ (L.K_local O₁ O₂ h)
  U_zero := by
    apply ContinuousLinearMap.ext; intro ψ
    rw [UF_apply, U1_zero, C.Γ_refl]; rfl
  U_add := fun v w => by
    apply ContinuousLinearMap.ext; intro ψ
    rw [ContinuousLinearMap.mul_apply, UF_apply, UF_apply, UF_apply, U1_add, C.Γ_trans]; rfl
  U_star := fun v => by
    rw [show UF C (-v) = (C.Γ (U1 v)).symm.toContinuousLinearEquiv.toContinuousLinearMap by
      rw [UF, U1_neg, Γ_symm]]
    exact LinearIsometryEquiv.star_eq_symm _
  covariance := fun a O x => by
    rw [UF_conj]
    exact C.R_cov (U1 a) (L.K O) (L.K (TGL.SpecificAQFT.translate a O)) (L.K_translate a O) x
  vac_invariant := fun a => C.Γ_vac (U1 a)
  wedge_nonabelian := C.wedge_nonabelian
  vac_cyclic_wedge := C.wedge_cyclic
  vac_separating_wedge := C.wedge_separating

/-- **lightBoost** — o grupo de boosts da cunha no Fock: V(s) = Γ(B(s)). -/
def lightBoost : WedgeBoostRep (lightNet C) where
  V := fun s => C.Γ (B0 s)
  V_zero := by rw [B0_zero, C.Γ_refl]; rfl
  V_add := fun a b => by rw [B0_add, C.Γ_trans]; rfl
  V_continuous := C.Γ_strong B0 B0_continuous
  V_vac := fun s => C.Γ_vac (B0 s)
  V_translations := fun s a => by
    apply ContinuousLinearMap.ext; intro ψ
    rw [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply]
    show C.Γ (B0 s) (C.Γ (U1 a) ((C.Γ (B0 s)).symm ψ)) = C.Γ (U1 (wedgeBoostMap s a)) ψ
    have hB : U1 (wedgeBoostMap s a) = (((B0 s).symm).trans (U1 a)).trans (B0 s) := by
      apply LinearIsometryEquiv.ext; intro f
      have h := congrArg (fun T : H1 →L[ℂ] H1 => T f) (B0_conj s a)
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply] at h
      exact h.symm
    rw [hB, C.Γ_trans, C.Γ_trans, Γ_symm]; rfl
  V_net := fun s O T hT => by
    have h := (C.R_cov (B0 s) (L.K O) (L.K (wedgeBoostMap s '' O)) (L.K_boost s O) T).mp hT
    exact h

/-- **lightRealization** — a realização modular do par; os três locks no núcleo com H3Lt := 1 − P_F
    (o transformado limitado PADRÃO: a origem microscópica de H_min segue [OPEN]). -/
def lightRealization : TGLModularRealization (lightNet C) where
  infiniteHilbert := C.F_infinite
  modular :=
    { wedgeAlgebra := C.R (L.K rightWedge)
      wedgeAlgebra_eq := rfl
      modularFlow := C.flow
      modularFlow_zero := C.flow_zero
      modularFlow_add := C.flow_add
      modularConjugation := C.J
      modularConjugation_involutive := C.J_invol
      modularConjugation_vac := C.J_vac }
  core :=
    { Core := C.Core
      embedding := C.embedding
      embedding_injective := C.embedding_injective
      dualAction := C.dualAction
      dualAction_zero := C.dualAction_zero
      dualAction_add := C.dualAction_add
      canonicalTrace := C.trace
      trace_zero := C.trace_zero
      trace_tracial := C.trace_tracial
      trace_star := C.trace_star
      trace_dual_scaling := C.trace_dual_scaling }
  threeLocks :=
    { H3Lt := 1 - C.PF
      H3Lt_selfAdjoint := by rw [star_sub, star_one, C.PF_sa]
      PF := C.PF
      PF_selfAdjoint := C.PF_sa
      PF_idempotent := C.PF_idem
      PF_locks := by rw [mul_sub, mul_one, C.PF_idem, sub_self]
      PF_maximal := fun q _ _ hq => by
        rw [mul_sub, mul_one, sub_eq_zero] at hq
        exact hq.symm
      PF_nonzero := C.PF_ne
      PF_trace_pos := C.PF_pos
      PF_trace_finite := C.PF_fin
      Pplus := C.Pp
      Pminus := C.Pm
      Pplus_selfAdjoint := C.Pp_sa
      Pplus_idempotent := C.Pp_idem
      Pminus_selfAdjoint := C.Pm_sa
      Pminus_idempotent := C.Pm_idem
      split := C.split
      orthogonal := C.orth
      trace_split_additive := C.trace_additive
      equal_face_trace := C.equal_halves }

/-! ## 4. H2 da luz, por composição -/

/-- o implementador modular: Δ^{it} = V(−2πt). -/
def lightDelta (t : ℝ) : C.F ≃ₗᵢ[ℂ] C.F := (lightBoost C).V (-(2 * Real.pi * t))

/-- [COMPOSTO] ★ translações fiéis: Γ injetivo no setor de uma partícula + a fidelidade orbital PAGA. -/
theorem light_translations_faithful (a : Fin 4 → ℝ) (h : (lightNet C).U a = 1) : a = 0 := by
  apply orbitalTranslation_faithful (E := Fib) 0 le_rfl a
  intro f
  have h1 : C.Γ (U1 a) (C.ι f) = C.ι f := by
    have := congrArg (fun T : C.F →L[ℂ] C.F => T (C.ι f)) h
    exact this
  rw [C.Γ_one_particle] at h1
  exact C.ι.injective h1

/-- [COMPOSTO] ★ energia positiva: `Γ_positive` + a energia positiva de uma partícula PAGA. -/
theorem light_positive_energy : PositiveEnergy (lightNet C) := by
  intro a ha ψ
  obtain ⟨G, h1, h2, h3⟩ := C.Γ_positive oneParticle_positive_energy a ha ψ
  exact ⟨G, h1, h2, fun t => by rw [h3 t]; rfl⟩

/-- [COMPOSTO] ★ ergodicidade nula: `Γ_no_fixed` + a ausência de autovalor nulo de uma partícula. -/
theorem light_null_ergodic (ψ : C.F) (h : ∀ l : ℝ, (lightNet C).U (l • nullDir) ψ = ψ) :
    ψ ∈ (ℂ ∙ C.Ω) := by
  apply C.Γ_no_fixed (fun l => U1 (l • nullDir))
  · simp only [zero_smul]; exact U1_zero
  · intro s t; rw [add_smul]; exact U1_add _ _
  · intro ξ
    exact (L.U1_continuous ξ).comp (continuous_id.smul continuous_const)
  · exact L.null_no_eigen
  · intro l; exact h l

/-- [COMPOSTO] a KMS da cunha para t ↦ Δit(−t) = V(2πt), lida de `bw_kms`. -/
theorem light_kms : KMSAt (lightNet C) (fun t => lightDelta C (-t)) 1 := by
  intro A hA B hB
  obtain ⟨G, h1, h2, h3, h4⟩ := C.bw_kms A hA B hB
  refine ⟨G, h1, h2, fun t => ?_, fun t => ?_⟩
  · rw [h3 t]; simp only [lightDelta, lightBoost, lightNet]; congr 3; ring
  · rw [h4 t]; simp only [lightDelta, lightBoost, lightNet]; congr 3; ring

/-- a tela da métrica soldada do frame da cunha é plana (−1₂) — conta. -/
theorem wedgeFrame_screen_flat (x : Fin 4 → ℝ) (hx : x ∈ rightWedge) :
    screenBlockV31 (TGLExt.solderMetric4 (wedgeFrame x)⁻¹) = -1 := by
  have hd : (wedgeFrame x).det ≠ 0 := (wedgeFrame_det_pos x hx).ne'
  set d := x 1 ^ 2 - x 0 ^ 2 with hdd
  have hd' : d ≠ 0 := by rw [hdd, ← wedgeFrame_det]; exact hd
  set M : Matrix (Fin 4) (Fin 4) ℝ :=
    !![x 1 / d, -(x 0) / d, 0, 0; -(x 0) / d, x 1 / d, 0, 0; 0, 0, 1, 0; 0, 0, 0, 1] with hM
  have hinv : (wedgeFrame x)⁻¹ = M := by
    apply Matrix.inv_eq_right_inv
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [wedgeFrame, M, Matrix.mul_apply, Fin.sum_univ_four] <;> field_simp <;> ring
  rw [hinv]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [screenBlockV31, TGLExt.solderMetric4, TGLExt.eta4, M, Matrix.mul_apply, Fin.sum_univ_four,
      Matrix.diagonal_apply]

/-- **lightH2** — o H2 v3.1 da luz, sobre o par (lightNet, lightRealization) e o relógio N. -/
def lightH2 (N : KillingNormalization) :
    TGLExt.ContratoQGv31.ContratoH2 (lightNet C) (lightRealization C) N where
  kappa := 1 / ContratoH2.refRadius N
  kappa_pos := one_div_pos.mpr (ContratoH2.refRadius_pos N)
  Δit := lightDelta C
  flow_implemented := fun t a => C.flow_is_Ad t a
  kms := light_kms C
  boost := lightBoost C
  bw := fun t => rfl
  translations_continuous := fun ψ => C.Γ_strong4 U1 L.U1_continuous ψ
  translations_faithful := light_translations_faithful C
  positive_energy := light_positive_energy C
  null_ergodic := light_null_ergodic C
  observer_unit := ContratoH2.observer_unit_of_index N
  E := wedgeFrame
  smooth_on := fun i j => (wedgeFrame_smooth i j).contDiffOn
  det_unit_on := wedgeFrame_det_unit
  dragged := fun s x _ => wedgeFrame_dragged s x
  fiducial_is_modular := fun x _ => wedgeFrame_fiducial _ (one_div_pos.mpr (ContratoH2.refRadius_pos N)) x

/-- **lightH2v32** — o H2 v3.2: a LUZ (m = 0, helicidade ±1) com a realização de Tomita. -/
def lightH2v32 (N : KillingNormalization) : ContratoH2v32 (lightNet C) (lightRealization C) N :=
  { lightH2 C N with
    photon_mass := rfl
    photon_helicity := L.helicity_light
    pair_realization := C.tomita }

/-! ## 5. O tensor de Maxwell e H3 no MESMO horizonte -/

/-- estados REGULARES para um campo de tensão: unitários, T_nn contínua e com cauda e primeiro momento
    integráveis ao longo de todo gerador nulo. -/
def Regular {W : TGLSpecificAQFTWitness} (D : Set W.H) (T : StressTensorData W) (ψ : W.H) : Prop :=
  ψ ∈ D ∧ (∀ x, MeasureTheory.Integrable (fun p : ℝ × (Fin 2 → ℝ) =>
      p.1 * nullEnergy T ψ (x + (p.1 • nullDir + screenEmbed p.2)))) ∧ ‖ψ‖ = 1 ∧ (∀ x, Continuous (fun u : ℝ => nullEnergy T ψ (x + u • nullDir))) ∧
    (∀ x l, IntegrableOn (fun u : ℝ => nullEnergy T ψ (x + u • nullDir)) (Ioi l)) ∧
    (∀ x l, IntegrableOn (fun u : ℝ => u * nullEnergy T ψ (x + u • nullDir)) (Ioi l))

/-- **MaxwellCertificate** — o tensor de Maxwell da luz e os dois fatos de estado [CITADOS]. -/
structure MaxwellCertificate where
  /-- o domínio NOMEADO dos estados suaves (finitas partículas/coerentes suaves), invariante e com o vácuo [Wightman]. -/
  Dom : Set C.F
  Dom_vac : C.Ω ∈ Dom
  Dom_translate : ∀ (b : Fin 4 → ℝ) (ψ : C.F), ψ ∈ Dom → C.Γ (U1 b) ψ ∈ Dom
  /-- ⟨ψ, :T_ab(x): ψ⟩ do campo de Maxwell livre, simétrico, conservado, covariante [campos livres de Wightman]. -/
  T : StressTensorDataLocalV32 (lightNet C) (lightBoost C)
  /-- ★ o elo da carga modular no plano nulo [Casini–Teste–Torroba 2017; Wall 2011 — KNOWN-física], no domínio nomeado. -/
  charge_link : ∀ ψ, Regular Dom T.toStressTensorData ψ → ∀ k : ℝ,
    HasModularEnergy (lightDelta C) ψ k → k = 2 * Real.pi * nullPlaneCharge T.toStressTensorData ψ
  /-- um estado coerente regular de energia modular não nula [Longo 2019]. -/
  nontrivial : ∃ ψ, Regular Dom T.toStressTensorData ψ ∧ ∃ k : ℝ, HasModularEnergy (lightDelta C) ψ k ∧ k ≠ 0

variable {C}

theorem regular_vac (M : MaxwellCertificate C) : Regular M.Dom M.T.toStressTensorData (lightNet C).vac := by
  have h0 : ∀ y, nullEnergy M.T.toStressTensorData (lightNet C).vac y = 0 := by
    intro y; simp [nullEnergy, pairing, M.T.T_vac y]
  refine ⟨M.Dom_vac, fun x => ?_, C.Ω_norm, fun x => ?_, fun x l => ?_, fun x l => ?_⟩
  · simp only [h0, mul_zero]; exact MeasureTheory.integrable_zero _ _ _
  · simp only [h0]; exact continuous_const
  · simp only [h0]; exact integrableOn_zero
  · simp only [h0, mul_zero]; exact integrableOn_zero

theorem regular_translate (M : MaxwellCertificate C) (b : Fin 4 → ℝ) (ψ : C.F)
    (h : Regular M.Dom M.T.toStressTensorData ψ) :
    Regular M.Dom M.T.toStressTensorData ((lightNet C).U b ψ) := by
  have hs : ∀ x y, nullEnergy M.T.toStressTensorData ((lightNet C).U b ψ) (x + y) =
      nullEnergy M.T.toStressTensorData ψ ((x - b) + y) := by
    intro x y
    simp only [nullEnergy, M.T.T_covariant]
    congr 2; abel
  obtain ⟨hd, hj, hn, hc, hi, hm⟩ := h
  refine ⟨M.Dom_translate b ψ hd, fun x => ?_, ?_, fun x => ?_, fun x l => ?_, fun x l => ?_⟩
  · simp only [hs]; exact hj (x - b)
  · show ‖C.Γ (U1 b) ψ‖ = 1; rw [LinearIsometryEquiv.norm_map]; exact hn
  · simp only [hs]; exact hc (x - b)
  · simp only [hs]; exact hi (x - b) l
  · simp only [hs]; exact hm (x - b) l

/-- **lightH3** — o H3 v3.1 sobre o MESMO H2 da luz, pelo construtor PAGO da bancada; a classe admissível = os estados
    REGULARES do domínio nomeado. -/
def lightH3 (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ) (hG : 0 < G) :
    TGLExt.ContratoQGv31.ContratoH3 (lightNet C) (lightRealization C) N M.T.toStressTensorData :=
  H3_of_null_solution (lightH2 C N) M.T.toStressTensorData G hG {ψ | Regular (W := lightNet C) M.Dom M.T.toStressTensorData ψ}
    (fun ψ h => h.2.2.1) (regular_vac M) (fun b ψ h => regular_translate M b ψ h)
    (fun ψ h k hk => M.charge_link ψ h k hk)
    (by obtain ⟨ψ, hψ, k, hk, hk0⟩ := M.nontrivial; exact ⟨ψ, hψ, k, hk, hk0⟩)
    (fun ψ h => h.2.2.2.1) (fun x hx => wedgeFrame_screen_flat x hx)
    (construct_null_solution M.T.toStressTensorData G {ψ | Regular (W := lightNet C) M.Dom M.T.toStressTensorData ψ}
      (fun ψ h => h.2.2.2.1) (fun ψ h => h.2.2.2.2.1) (fun ψ h => h.2.2.2.2.2))

/-- **lightH3v32** — o H3 v3.2: o MESMO horizonte da luz e o MESMO boost do tensor. -/
def lightH3v32 (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ) (hG : 0 < G) :
    ContratoH3v32 (lightNet C) (lightRealization C) N (lightBoost C) M.T :=
  { lightH3 M N G hG with
    light_horizon := lightH2v32 C N
    same_stress_boost := rfl
    same_local_horizon := rfl }

/-- o reconhecimento do par por si mesmo (U = identidade): o caso em que a forma nominada NÃO difere. -/
def selfRecognition : ORDEM016.D6.ReconhecimentoPeloConteudo
    ((lightNet C).net rightWedge).toStarSubalgebra ((lightNet C).net rightWedge).toStarSubalgebra
    (lightNet C).vac (lightNet C).vac where
  U := LinearIsometryEquiv.refl ℂ _
  reference := rfl
  algebra := fun A => by
    have : (LinearIsometryEquiv.refl ℂ (lightNet C).H).conjStarAlgEquiv A = A := by
      apply ContinuousLinearMap.ext; intro ψ; rfl
    rw [this]

/-- **lightImport** — o import v3.2: produce = H3 da luz, same_horizon por conteúdo, a fonte É h2. -/
def lightImport (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ) (hG : 0 < G) :
    ContratoImportH3v32 (lightNet C) (lightRealization C) N (lightBoost C) M.T (lightH2v32 C N) where
  produce := lightH3v32 M N G hG
  same_horizon := selfRecognition
  source_realization := C.tomita
  source_is_the_light := rfl

/-! ## 6. O TEOREMA -/

/-- ★★★ **O CONTRATO v3.2 DA TGL HABITADO SOB HIPÓTESES NOMEADAS** (PROVADA POR CITAÇÃO): da luz de uma partícula
    (translações PAGAS), da segunda quantização, do tensor de Maxwell e de G > 0, o contrato v3.2 INTEIRO
    — H2 da luz, H3 no MESMO horizonte, o import — é habitado, para TODO relógio N. -/
theorem qg_formalized_by_citation (L : LightOneParticle) (C : FockCertificate L)
    (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ) (hG : 0 < G) :
    ∃ h2 : ContratoH2v32 (lightNet C) (lightRealization C) N,
      Nonempty (ContratoImportH3v32 (lightNet C) (lightRealization C) N (lightBoost C) M.T h2) :=
  ⟨lightH2v32 C N, ⟨lightImport M N G hG⟩⟩

/-- [COMPOSTO] o κ do H2 da luz é 1/ρ(N) (a temperatura κ/2π é o `unruh_is_kms` do contrato, não reprovado aqui). -/
theorem light_kappa (N : KillingNormalization) : (lightH2 C N).kappa = 1 / ContratoH2.refRadius N := rfl

/-! ## 7. CONTROLES NEGATIVOS (a citação não é vazia de conteúdo) -/

/-- ✗ o funtor TRIVIAL (Γ u = 1 para todo u) NÃO satisfaz a citação: pelo setor de uma partícula ele forçaria
    toda translação orbital a ser a identidade, contra a fidelidade PAGA. -/
theorem trivial_functor_refused (C' : FockCertificate L)
    (htriv : ∀ u : H1 ≃ₗᵢ[ℂ] H1, C'.Γ u = LinearIsometryEquiv.refl ℂ C'.F) : False := by
  have hne : (nullDir : Fin 4 → ℝ) ≠ 0 := by
    intro h; have := congrFun h 0; simp [nullDir] at this
  apply hne
  apply orbitalTranslation_faithful (E := Fib) 0 le_rfl nullDir
  intro f
  have h := C'.Γ_one_particle (U1 nullDir) f
  rw [htriv] at h
  exact (C'.ι.injective h).symm

/-- ✗ o RÓTULO do escalar sem massa (helicidade 0) é recusado pelo tipo: m = 0 exige helicidade ≠ 0. Recusa o RÓTULO,
    não o conteúdo escalar (no grupo do contrato a helicidade não é observável — ver «Limitações»). -/
theorem massless_scalar_refused (W : TGLSpecificAQFTWitness) (hm : W.m = 0) (hh : W.helicity = 0) : False := by
  rcases W.peso_do_nome with h | h
  · rw [hm] at h; exact lt_irrefl 0 h
  · exact h hh

end TGLExt.ImportedSQ

#print axioms TGLExt.ImportedSQ.oneParticle_positive_energy
#print axioms TGLExt.ImportedSQ.Γ_symm
#print axioms TGLExt.ImportedSQ.lightNet
#print axioms TGLExt.ImportedSQ.lightBoost
#print axioms TGLExt.ImportedSQ.lightRealization
#print axioms TGLExt.ImportedSQ.light_translations_faithful
#print axioms TGLExt.ImportedSQ.light_positive_energy
#print axioms TGLExt.ImportedSQ.light_null_ergodic
#print axioms TGLExt.ImportedSQ.light_kms
#print axioms TGLExt.ImportedSQ.wedgeFrame_screen_flat
#print axioms TGLExt.ImportedSQ.lightH2
#print axioms TGLExt.ImportedSQ.lightH2v32
#print axioms TGLExt.ImportedSQ.regular_vac
#print axioms TGLExt.ImportedSQ.regular_translate
#print axioms TGLExt.ImportedSQ.lightH3
#print axioms TGLExt.ImportedSQ.lightH3v32
#print axioms TGLExt.ImportedSQ.lightImport
#print axioms TGLExt.ImportedSQ.qg_formalized_by_citation
#print axioms TGLExt.ImportedSQ.trivial_functor_refused
#print axioms TGLExt.ImportedSQ.massless_scalar_refused
