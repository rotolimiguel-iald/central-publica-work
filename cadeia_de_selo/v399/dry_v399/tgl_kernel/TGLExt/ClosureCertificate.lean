import TGLExt.TheMasterFires

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O CERTIFICADO DE FECHAMENTO: as flags deixam de ser declaração
  [TGLExt — v99, o incremento 16 do programa SemifiniteAnalysis]

A correção de engenharia (leitura externa absorvida, 17/07/2026): as seis
flags do gate estavam escritas como `False` no runtime — fail-closed por
DECLARAÇÃO. Esta pedra as torna fail-closed por CONSTRUÇÃO: define o TIPO
`QGClosureCertificate` cujos campos FORÇAM o conteúdo que falta, no máximo
que a mathlib de hoje permite tipar:

* `PhysicalNetData` — a rede exigida: HilbertHomeData + isotonia GENUÍNA
  (alguma inclusão não-sobrejetiva: mata a rede constante) + ação externa
  NÃO-TRIVIAL (mata o grupo PUnit);
* `UnboundedDiracData` — o Dirac modular ILIMITADO: LinearPMap com
  star(D) = D (o adjunto ilimitado da mathlib — que já força domínio
  denso), kernel não-trivial, e GAP QUADRÁTICO em torno do kernel (sem
  teorema espectral: a forma);
* `SmoothFrameData` — o four-frame como CAMPO: E : ℝ⁴ → M₄(ℝ) suave
  (C^∞) com det invertível em TODA PARTE — mata o frame pontual;
* o certificado compõe: rede física + Dirac + canto de Breuer no kernel
  do Dirac (0 < τ < ∞ em morada ∞-dim) + campo suave + coframe paralelo
  (a face plana; curvatura e covariância = v2).

O TERMO `qgClosureCertificate` NÃO É CONSTRUÍDO — e não pode ser, hoje:
provamos em kernel os PROBES NEGATIVOS que mostram por quê (o grupo dos
habitantes atuais é PUnit: `constant_net_group_trivial`; inclusões-
identidade não testemunham isotonia genuína). O runtime passa a ler as
flags POR NOME DE TERMO LEAN: ausência do termo ⟹ False, mecânico.

O QUE AINDA NÃO É TIPÁVEL (nomeado, sem véu): fator III₁/classificação
de tipos, afiliação a álgebra de von Neumann semifinita, H3 DERIVADO da
dinâmica do estado, spin-2 contínuo = a segunda metade do certificado
(v2) — pendem de camadas que a mathlib não tem; construí-las é o
programa.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/-! ## A rede física exigida (mata a rede constante) -/

/-- [DATA — o alvo, não o habitante] a rede FÍSICA exigida pelo gate:
    o pacote do v56 MAIS isotonia genuína (alguma inclusão que não é
    sobrejetiva — fibras crescem de verdade) MAIS grupo externo
    não-trivial. Os habitantes atuais (v96) NÃO satisfazem os dois
    últimos campos — e é exatamente isso que o certificado força. -/
structure PhysicalNetData (Region : Type) (leR : Region → Region → Prop)
    (H : Region → Type) (W : Region → Type)
    [∀ O, NormedAddCommGroup (H O)] [∀ O, InnerProductSpace ℂ (H O)]
    [∀ O, CompleteSpace (H O)]
    [∀ O, NormedAddCommGroup (W O)] [∀ O, NormedSpace ℂ (W O)] where
  net : HilbertHomeData Region leR H W
  genuinely_isotone : ∃ (O₁ O₂ : Region) (hle : leR O₁ O₂),
    ¬ Function.Surjective (net.incl hle)
  external_nontrivial : Nontrivial net.G

/-! ## O Dirac ilimitado exigido (mata o operador limitado de bancada) -/

/-- [DATA — o alvo] o Dirac modular ILIMITADO: parcialmente definido,
    com star(D) = D no sentido do adjunto ilimitado da mathlib (que já
    força domínio denso), kernel não-trivial, e o GAP como desigualdade
    quadrática (sem teorema espectral: a forma força a separação do
    zero). -/
structure UnboundedDiracData (ℍ : Type) [NormedAddCommGroup ℍ]
    [InnerProductSpace ℂ ℍ] [CompleteSpace ℍ] where
  D : ℍ →ₗ.[ℂ] ℍ
  selfadjoint : IsSelfAdjoint D
  gap : ℝ
  gap_pos : 0 < gap
  ker_witness : ∃ x : D.domain, (x : ℍ) ≠ 0 ∧ D x = 0
  quad_gap : ∀ x : D.domain,
    (∀ y : D.domain, D y = 0 → inner ℂ (y : ℍ) (x : ℍ) = 0) →
    gap * ‖(x : ℍ)‖ ≤ ‖D x‖

/-- o kernel do Dirac como submódulo da morada (a imagem do ker do
    toFun sob a inclusão do domínio). -/
def UnboundedDiracData.kerSub {ℍ : Type} [NormedAddCommGroup ℍ]
    [InnerProductSpace ℂ ℍ] [CompleteSpace ℍ]
    (dd : UnboundedDiracData ℍ) : Submodule ℂ ℍ :=
  (LinearMap.ker dd.D.toFun).map dd.D.domain.subtype

/-! ## O four-frame como CAMPO suave (mata o frame pontual) -/

/-- [DATA — o alvo] o frame como CAMPO sobre ℝ⁴: suave (C^∞) e com
    determinante invertível em TODA PARTE. A covariância sob o grupo da
    rede é o campo seguinte (v2 — pede a ação geométrica). -/
structure SmoothFrameData where
  E : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  smooth : ∀ i j : Fin 4, ContDiff ℝ (⊤ : ℕ∞) (fun x => E x i j)
  det_unit : ∀ x, IsUnit (E x).det

/-! ## O certificado (v1 — a metade tipável hoje) -/

/-- [DATA — O CERTIFICADO] o termo cuja EXISTÊNCIA (com axiomas limpos)
    é o que o gate passa a ler. NÃO construído — não pode ser, hoje: os
    campos forçam rede não-constante com grupo não-trivial, Dirac
    ilimitado auto-adjunto com gap, canto de Breuer no seu kernel em
    morada ∞-dim, e frame-campo suave com coframe paralelo. A metade
    ainda não-tipável (III₁, afiliação semifinita, H3 derivado, spin-2
    contínuo) está nomeada no cabeçalho e pertence ao v2. -/
structure QGClosureCertificate where
  Region : Type
  leR : Region → Region → Prop
  H : Region → Type
  W : Region → Type
  [instH₁ : ∀ O, NormedAddCommGroup (H O)]
  [instH₂ : ∀ O, InnerProductSpace ℂ (H O)]
  [instH₃ : ∀ O, CompleteSpace (H O)]
  [instW₁ : ∀ O, NormedAddCommGroup (W O)]
  [instW₂ : ∀ O, NormedSpace ℂ (W O)]
  core : PhysicalNetData Region leR H W
  ℍ : Type
  [instD₁ : NormedAddCommGroup ℍ]
  [instD₂ : InnerProductSpace ℂ ℍ]
  [instD₃ : CompleteSpace ℍ]
  dirac : UnboundedDiracData ℍ
  home_infinite : ¬ FiniteDimensional ℂ ℍ
  corner_pos : 0 < dimOrTop ℂ dirac.kerSub
  corner_finite : dimOrTop ℂ dirac.kerSub < ⊤
  frame : SmoothFrameData
  coframe_parallel : ∀ (x : Fin 4 → ℝ) (i j : Fin 4),
    fderiv ℝ (fun y => (frame.E y)⁻¹ i j) x = 0

/-! ## Os probes negativos EM KERNEL: por que o certificado não fecha hoje -/

/-- [KERNEL] ★ o grupo dos habitantes atuais é TRIVIAL: PUnit não é
    Nontrivial — a rede constante do v96 NÃO alimenta o certificado
    (o probe que mostra que o tipo morde). -/
theorem constant_net_group_trivial : ¬ Nontrivial PUnit := by
  intro h
  obtain ⟨a, b, hab⟩ := h.exists_pair_ne
  exact hab (Subsingleton.elim a b)

/-- [KERNEL] ★ a exigência de isotonia genuína MORDE: a identidade é
    sobrejetiva — inclusões-identidade (a rede constante) não podem
    testemunhar `genuinely_isotone`. -/
theorem identity_inclusion_cannot_witness {α : Type} :
    Function.Surjective (fun x : α => x) := fun y => ⟨y, rfl⟩

end

end TGLExt
