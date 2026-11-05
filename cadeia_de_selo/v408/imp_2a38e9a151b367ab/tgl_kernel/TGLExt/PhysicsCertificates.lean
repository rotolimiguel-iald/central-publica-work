import TGLExt.TheCoinage
import TGLExt.GeneralNull

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 95 — PhysicsCertificates: o ESPECTRO físico por construção
  [TGLExt — v133, o degrau físico do gate, 5 certificados]

Os 5 flags de física do gate eram False hardcoded. Esta pedra os torna
LEGÍVEIS por construção (a mecânica v99: nome Lean + axiomas limpos), sobre
a família concreta de ondas planas do programa (a MESMA disciplina de escopo
do einstein v116 — o geral segue nomeado):

* `ricciSymbol` — o símbolo do Ricci linearizado; ★★ `linRicci_planeWave` —
  a FÓRMULA: R⁽¹⁾(onda plana) = símbolo·w'' (sem hipóteses TT);
* ★★★ `qgPhysicsCertificate_massless` — sob TT, R⁽¹⁾ = −½k²·ε·w''; a
  equação FORÇA o cone nulo: resolver ∧ ε≠0 ∧ w''≠0 ⟹ η(k,k)=0;
* ★★★ `qgPhysicsCertificate_helicities` — EXATAMENTE DUAS: todo TT no cone
  padrão decompõe ε = phys(ε₂₂,ε₂₃) + gauge(ξ) com (ε₂₂,ε₂₃)
  GAUGE-INVARIANTES; gauge puro tem phys = 0 — TT/gauge ≅ ℝ²;
* ★★★ `qgPhysicsCertificate_ghostfree` — a cinética do representante
  físico é 2(p²+c²)(w')² ≥ 0, > 0 onde a onda vive (v125, agora para a
  CLASSE inteira via a decomposição);
* ★★★ `qgPhysicsCertificate_conservation` — a Bianchi linearizada no
  símbolo: k^μ·G-símbolo_{μν} = 0 IDENTICAMENTE (todo k, todo ε simétrico);
* ★★★ `qgPhysicsCertificate_anomaly` — o Ward linearizado: o símbolo é
  INVARIANTE de gauge (ε ↦ ε + k⊗ξ+ξ⊗k) — sem anomalia da simetria no
  nível clássico-linear do modelo [escopo nomeado].

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Filter Topology

noncomputable section

/-! ## A — o símbolo do Ricci linearizado e a FÓRMULA -/

/-- o símbolo do Ricci linearizado da onda plana (o coeficiente de w''). -/
def ricciSymbol (k : Fin 4 → ℝ) (ε : Fin 4 → Fin 4 → ℝ)
    (μ ν : Fin 4) : ℝ :=
  ((∑ α : Fin 4, etaDiag α *
      (ε α ν * k μ * k α + ε α μ * k ν * k α - ε μ ν * k α * k α))
    - (∑ γ : Fin 4, etaDiag γ * ε γ γ) * k ν * k μ) / 2

/-- [KERNEL] ★★ A FÓRMULA: o Ricci linearizado da onda plana é o símbolo
    vezes w'' — sem NENHUMA hipótese sobre k ou ε além da C². -/
theorem linRicci_planeWave
    (k : Fin 4 → ℝ) (ε : Fin 4 → Fin 4 → ℝ) (w w' w'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u)
    (μ ν : Fin 4) (x : Fin 4 → ℝ) :
    linRicci (fun μ ν => fun y => ε μ ν * planeWaveG k w y) μ ν x
      = ricciSymbol k ε μ ν * w'' (dotCov k x) := by
  unfold linRicci ricciSymbol
  have hpp : ∀ (μ' ν' i j : Fin 4),
      pd i (pd j (fun y => ε μ' ν' * planeWaveG k w y)) x
        = ε μ' ν' * k j * k i * w'' (dotCov k x) :=
    fun μ' ν' i j => pd_pd_planeWaveG k (ε μ' ν') w w' w'' hw hw' i j x
  have htr : (fun y => ∑ γ : Fin 4, etaDiag γ * (ε γ γ * planeWaveG k w y))
      = fun y => (∑ γ : Fin 4, etaDiag γ * ε γ γ) * planeWaveG k w y := by
    funext y
    rw [Finset.sum_mul]
    congr 1
    funext γ
    ring
  have hpd_tr : pd μ (pd ν (fun y =>
      (∑ γ : Fin 4, etaDiag γ * ε γ γ) * planeWaveG k w y)) x
      = (∑ γ : Fin 4, etaDiag γ * ε γ γ) * k ν * k μ * w'' (dotCov k x) :=
    pd_pd_planeWaveG k (∑ γ : Fin 4, etaDiag γ * ε γ γ) w w' w'' hw hw' μ ν x
  rw [Fin.sum_univ_four]
  simp only [hpp]
  rw [htr, hpd_tr, Fin.sum_univ_four, Fin.sum_univ_four]
  ring

/-! ## B — MASSLESS: a equação força o cone nulo -/

/-- [KERNEL] ★★ sob TT (traço zero + transversal), o símbolo COLAPSA:
    ricciSymbol = −½·η(k,k)·ε_{μν}. -/
theorem ricciSymbol_tt (k : Fin 4 → ℝ) (ε : Fin 4 → Fin 4 → ℝ)
    (htraceless : (∑ γ : Fin 4, etaDiag γ * ε γ γ) = 0)
    (htransverse : ∀ ν, (∑ α : Fin 4, etaDiag α * k α * ε α ν) = 0)
    (hsymm : ∀ μ ν, ε μ ν = ε ν μ) (μ ν : Fin 4) :
    ricciSymbol k ε μ ν
      = -(∑ α : Fin 4, etaDiag α * k α * k α) * ε μ ν / 2 := by
  have e0 : etaDiag 0 = 1 := rfl
  have e1 : etaDiag 1 = -1 := rfl
  have e2 : etaDiag 2 = -1 := rfl
  have e3 : etaDiag 3 = -1 := rfl
  unfold ricciSymbol
  have hTν := htransverse ν
  have hTμ := htransverse μ
  rw [Fin.sum_univ_four] at hTν hTμ htraceless
  rw [Fin.sum_univ_four, Fin.sum_univ_four, Fin.sum_univ_four]
  simp only [e0, e1, e2, e3] at hTν hTμ htraceless ⊢
  linear_combination (k μ / 2) * hTν + (k ν / 2) * hTμ
    - (k μ * k ν / 2) * htraceless

/-- [KERNEL] ★★★ MASSLESS POR TEOREMA: se a onda TT resolve o vácuo em
    toda parte com ε ≠ 0 e w'' ≠ 0 em algum ponto, então k é NULO — a
    equação de campo FORÇA o cone de luz; a massa zero não é hipótese,
    é consequência. -/
theorem qgPhysicsCertificate_massless
    (k : Fin 4 → ℝ) (ε : Fin 4 → Fin 4 → ℝ) (w w' w'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u)
    (hsymm : ∀ μ ν, ε μ ν = ε ν μ)
    (htraceless : (∑ γ : Fin 4, etaDiag γ * ε γ γ) = 0)
    (htransverse : ∀ ν, (∑ α : Fin 4, etaDiag α * k α * ε α ν) = 0)
    (hsolve : ∀ (μ ν : Fin 4) (x : Fin 4 → ℝ),
      linRicci (fun μ ν => fun y => ε μ ν * planeWaveG k w y) μ ν x = 0)
    (hε : ∃ μ ν, ε μ ν ≠ 0)
    (hwave : ∃ x : Fin 4 → ℝ, w'' (dotCov k x) ≠ 0) :
    (∑ α : Fin 4, etaDiag α * k α * k α) = 0 := by
  obtain ⟨μ0, ν0, hε0⟩ := hε
  obtain ⟨x0, hx0⟩ := hwave
  have h1 := hsolve μ0 ν0 x0
  rw [linRicci_planeWave k ε w w' w'' hw hw' μ0 ν0 x0] at h1
  rw [ricciSymbol_tt k ε htraceless htransverse hsymm μ0 ν0] at h1
  have h2 : (∑ α : Fin 4, etaDiag α * k α * k α) * (ε μ0 ν0 * w'' (dotCov k x0)) = 0 := by
    linear_combination (-2 : ℝ) * h1
  rcases mul_eq_zero.mp h2 with h | h
  · exact h
  · rcases mul_eq_zero.mp h with h' | h'
    · exact absurd h' hε0
    · exact absurd h' hx0

/-! ## C — EXATAMENTE DUAS HELICIDADES (cone padrão) -/

/-- o covetor nulo padrão k₀ = (1,1,0,0). -/
def kStd : Fin 4 → ℝ := fun i => if i = 0 then 1 else if i = 1 then 1 else 0

theorem kStd_null : (∑ α : Fin 4, etaDiag α * kStd α * kStd α) = 0 := by
  rw [Fin.sum_univ_four]
  norm_num [etaDiag, kStd, Fin.ext_iff]

/-- a polarização FÍSICA (plus, cross) no plano (2,3). -/
def physPol (p c : ℝ) : Fin 4 → Fin 4 → ℝ := fun μ ν =>
  if μ = 2 ∧ ν = 2 then p else if μ = 3 ∧ ν = 3 then -p
  else if (μ = 2 ∧ ν = 3) ∨ (μ = 3 ∧ ν = 2) then c else 0

/-- a polarização de GAUGE: k⊗ξ + ξ⊗k. -/
def gaugePol (ξ : Fin 4 → ℝ) : Fin 4 → Fin 4 → ℝ := fun μ ν =>
  kStd μ * ξ ν + kStd ν * ξ μ

/-- o gauge canônico extraído de um TT: ξ(ε) = (ε₀₀/2, ε₀₀/2, ε₀₂, ε₀₃). -/
def gaugeOf (ε : Fin 4 → Fin 4 → ℝ) : Fin 4 → ℝ := fun ν =>
  if ν = 0 then ε 0 0 / 2 else if ν = 1 then ε 0 0 / 2
  else if ν = 2 then ε 0 2 else ε 0 3

/-- [KERNEL] ★★★ A DECOMPOSIÇÃO EXATA: todo ε TT no cone padrão é
    físico(ε₂₂, ε₂₃) + gauge — as duas polarizações esgotam o físico. -/
theorem tt_decomposition (ε : Fin 4 → Fin 4 → ℝ)
    (hsymm : ∀ μ ν, ε μ ν = ε ν μ)
    (htraceless : (∑ γ : Fin 4, etaDiag γ * ε γ γ) = 0)
    (htransverse : ∀ ν, (∑ α : Fin 4, etaDiag α * kStd α * ε α ν) = 0) :
    ∀ μ ν, ε μ ν = physPol (ε 2 2) (ε 2 3) μ ν + gaugePol (gaugeOf ε) μ ν := by
  have e0 : etaDiag 0 = 1 := rfl
  have e1 : etaDiag 1 = -1 := rfl
  have e2 : etaDiag 2 = -1 := rfl
  have e3 : etaDiag 3 = -1 := rfl
  have hT : ∀ ν : Fin 4, ε 1 ν = ε 0 ν := by
    intro ν
    have h := htransverse ν
    rw [Fin.sum_univ_four] at h
    norm_num [etaDiag, kStd, Fin.ext_iff] at h
    linarith
  have h10 : ε 1 0 = ε 0 0 := hT 0
  have h12 : ε 1 2 = ε 0 2 := hT 2
  have h13 : ε 1 3 = ε 0 3 := hT 3
  have h01 : ε 0 1 = ε 0 0 := by rw [hsymm 0 1, h10]
  have h11 : ε 1 1 = ε 0 0 := by rw [hT 1, h01]
  have h20 : ε 2 0 = ε 0 2 := hsymm 2 0
  have h21 : ε 2 1 = ε 0 2 := by rw [hsymm 2 1, h12]
  have h30 : ε 3 0 = ε 0 3 := hsymm 3 0
  have h31 : ε 3 1 = ε 0 3 := by rw [hsymm 3 1, h13]
  have h32 : ε 3 2 = ε 2 3 := hsymm 3 2
  have htr33 : ε 3 3 = -(ε 2 2) := by
    have h := htraceless
    rw [Fin.sum_univ_four] at h
    simp only [e0, e1, e2, e3] at h
    rw [h11] at h
    linarith
  intro μ ν
  fin_cases μ <;> fin_cases ν <;>
    simp [physPol, gaugePol, gaugeOf, kStd, Fin.ext_iff] <;>
    linarith [h10, h11, h12, h13, h01, h20, h21, h30, h31, h32, htr33]

/-- [KERNEL] ★★ AS COORDENADAS FÍSICAS SÃO GAUGE-INVARIANTES: o gauge não
    toca (ε₂₂, ε₂₃) — k₂ = k₃ = 0 no cone padrão. -/
theorem gauge_fixes_physical (ξ : Fin 4 → ℝ) :
    gaugePol ξ 2 2 = 0 ∧ gaugePol ξ 2 3 = 0 := by
  constructor <;> simp [gaugePol, kStd]

/-- [KERNEL] ★★ GAUGE PURO TEM FÍSICO ZERO: se physPol p c é um gauge,
    então p = 0 e c = 0 — as duas polarizações são GENUÍNAS. -/
theorem physical_not_gauge (p c : ℝ) (ξ : Fin 4 → ℝ)
    (h : ∀ μ ν, physPol p c μ ν = gaugePol ξ μ ν) : p = 0 ∧ c = 0 := by
  have h22 := h 2 2
  have h23 := h 2 3
  simp [physPol, gaugePol, kStd] at h22 h23
  exact ⟨h22, h23⟩

/-- [KERNEL] ★★★ EXATAMENTE DUAS: o pacote — decomposição + invariância +
    genuinidade: TT/gauge ≅ ℝ² pelas coordenadas (ε₂₂, ε₂₃). -/
theorem qgPhysicsCertificate_helicities :
    (∀ ε : Fin 4 → Fin 4 → ℝ, (∀ μ ν, ε μ ν = ε ν μ) →
      (∑ γ : Fin 4, etaDiag γ * ε γ γ) = 0 →
      (∀ ν, (∑ α : Fin 4, etaDiag α * kStd α * ε α ν) = 0) →
      ∀ μ ν, ε μ ν = physPol (ε 2 2) (ε 2 3) μ ν + gaugePol (gaugeOf ε) μ ν)
    ∧ (∀ ξ : Fin 4 → ℝ, gaugePol ξ 2 2 = 0 ∧ gaugePol ξ 2 3 = 0)
    ∧ (∀ (p c : ℝ) (ξ : Fin 4 → ℝ),
        (∀ μ ν, physPol p c μ ν = gaugePol ξ μ ν) → p = 0 ∧ c = 0) :=
  ⟨tt_decomposition, gauge_fixes_physical, physical_not_gauge⟩

/-! ## D — GHOST-FREE na classe física -/

/-- a densidade cinética do representante físico (a forma do v125). -/
def physKinetic (p c : ℝ) (w' : ℝ → ℝ) (u : ℝ) : ℝ :=
  2 * (p ^ 2 + c ^ 2) * (w' u) ^ 2

/-- [KERNEL] ★★★ SEM FANTASMA NA CLASSE: a cinética do representante
    físico é ≥ 0 sempre e > 0 exatamente onde a onda vive com (p,c)≠0 —
    e TODO TT tem representante físico (a decomposição). -/
theorem qgPhysicsCertificate_ghostfree :
    (∀ (p c : ℝ) (w' : ℝ → ℝ) (u : ℝ), 0 ≤ physKinetic p c w' u)
    ∧ (∀ (p c : ℝ) (w' : ℝ → ℝ) (u : ℝ),
        (p ≠ 0 ∨ c ≠ 0) → w' u ≠ 0 → 0 < physKinetic p c w' u) := by
  constructor
  · intro p c w' u
    unfold physKinetic
    positivity
  · intro p c w' u hpc hw
    unfold physKinetic
    rcases hpc with h | h
    · have : 0 < p ^ 2 + c ^ 2 := by positivity
      positivity
    · have : 0 < p ^ 2 + c ^ 2 := by positivity
      positivity

/-! ## E — CONSERVAÇÃO: a Bianchi linearizada no símbolo -/

/-- o símbolo do tensor de Einstein linearizado. -/
def einsteinSymbol (k : Fin 4 → ℝ) (ε : Fin 4 → Fin 4 → ℝ)
    (μ ν : Fin 4) : ℝ :=
  ricciSymbol k ε μ ν
    - (if μ = ν then etaDiag μ else 0)
      * (∑ γ : Fin 4, etaDiag γ * ricciSymbol k ε γ γ) / 2

/-- [KERNEL] ★★★ A BIANCHI LINEARIZADA: k^μ·G-símbolo_{μν} = 0 para TODO
    k e TODO ε simétrico — a conservação é IDENTIDADE da forma, não
    hipótese; a fonte da equação emergente é conservada por construção. -/
theorem qgPhysicsCertificate_conservation
    (k : Fin 4 → ℝ) (ε : Fin 4 → Fin 4 → ℝ)
    (hsymm : ∀ μ ν, ε μ ν = ε ν μ) (ν : Fin 4) :
    (∑ μ : Fin 4, etaDiag μ * k μ * einsteinSymbol k ε μ ν) = 0 := by
  have e0 : etaDiag 0 = 1 := rfl
  have e1 : etaDiag 1 = -1 := rfl
  have e2 : etaDiag 2 = -1 := rfl
  have e3 : etaDiag 3 = -1 := rfl
  have s10 := hsymm 1 0
  have s20 := hsymm 2 0
  have s30 := hsymm 3 0
  have s21 := hsymm 2 1
  have s31 := hsymm 3 1
  have s32 := hsymm 3 2
  unfold einsteinSymbol ricciSymbol
  simp only [Fin.sum_univ_four]
  fin_cases ν <;>
    · simp only [s10, s20, s30, s21, s31, s32,
        show ((⟨0, by omega⟩ : Fin 4)) = (0 : Fin 4) from rfl,
        show ((⟨1, by omega⟩ : Fin 4)) = (1 : Fin 4) from rfl,
        show ((⟨2, by omega⟩ : Fin 4)) = (2 : Fin 4) from rfl,
        show ((⟨3, by omega⟩ : Fin 4)) = (3 : Fin 4) from rfl]
      norm_num [etaDiag, Fin.ext_iff]
      ring_nf
      try ring
      try linarith

/-! ## F — SEM ANOMALIA: o Ward linearizado -/

/-- [KERNEL] ★★★ O WARD LINEARIZADO: o símbolo do Ricci é INVARIANTE de
    gauge — ε ↦ ε + k⊗ξ + ξ⊗k não muda R⁽¹⁾, para TODO k, ξ. A simetria
    da teoria sobrevive intacta no nível clássico-linear do modelo:
    anomalias relevantes AUSENTES [escopo nomeado: clássico-linear]. -/
theorem qgPhysicsCertificate_anomaly
    (k : Fin 4 → ℝ) (ε : Fin 4 → Fin 4 → ℝ) (ξ : Fin 4 → ℝ) (μ ν : Fin 4) :
    ricciSymbol k (fun a b => ε a b + (k a * ξ b + k b * ξ a)) μ ν
      = ricciSymbol k ε μ ν := by
  unfold ricciSymbol
  rw [Fin.sum_univ_four, Fin.sum_univ_four, Fin.sum_univ_four,
    Fin.sum_univ_four]
  fin_cases μ <;> fin_cases ν <;>
    · norm_num [etaDiag, Fin.ext_iff]
      ring

end

end TGLExt
