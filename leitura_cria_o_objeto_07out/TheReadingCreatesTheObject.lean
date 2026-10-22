import TGLExt.O16.PeriodHeatCalibration_v3
import TGLExt.O16.RotationGeneratorBridges
import TGLExt.TheObserverReadsTheAngle

set_option autoImplicit false

/-!
# A LEITURA CRIA O OBJETO   [CANDIDATA — 07/10/2026; o nome definitivo é do operador]

## A cunhagem do operador (verbatim por sha256 `f2a4b509946edc05…`, 07/10/2026)

> «vc disse que a leitura não acrescenta o objeto, e vc tem razão, porque a LEITURA CRIA o objeto,
> antes da leitura o objeto é Nome (posto relativo), após a leitura o objeto é identidade,
> relação de contorno»

## O que esta pedra compõe (nada novo além de um lema de uma linha; o resto já está no kernel)

* **ANTES da leitura — a face não fecha.** `the_face_does_not_close`: o boost real `B(s)` só é a
  identidade em `s = 0`. A rapidez corre pela reta inteira sem voltar: a posição é RELATIVA
  (ao zero escolhido), não há contorno. [lema novo, uma linha: `sinh s = 0 ⟹ s = 0`]
* **A leitura — a face lida no ângulo.** `Circle.exp (κ·t)` (`ChatgptAudit.PolarPeriod016`):
  ler o parâmetro do boost como ângulo.
* **APÓS a leitura — a relação de contorno.** `the_reading_creates_the_contour`: a leitura
  identifica `t` com `u` exatamente módulo `P·ℤ` (o quociente angular é FIEL) se e só se
  `κ·P = ±2π` — uma volta inteira, nem mais nem menos. É a identificação que fecha o contorno.
  [`faithful_period_iff`, já no kernel]
* **A identidade criada.** `the_read_face_closes`: o boost continuado à rapidez `2π·i` é a
  identidade (`wick_boost_two_pi`, já no kernel). E o contorno fiel dá a temperatura,
  `1/P = κ/2π` (`reciprocal_temperature`, já no kernel), que entra no balanço de Clausius do
  segmento de boost (`boost_defect_with_derived_period`, já no kernel).
* **A primeira leitura identifica; reler não acrescenta.** `the_first_reading_identifies`
  (`the_observer_reads_the_angle`: `P₊·𝒪_θ = e^{iθ}·P₊`) e `rereading_adds_nothing`
  (`observing_adds_nothing`: `P₊·(P₊·𝒪_θ) = P₊·𝒪_θ`), já no kernel. A docstring do kernel já
  dizia: «A primeira leitura identifica; a segunda confirma que a operação não altera.»

## O que esta pedra NÃO afirma

* Não afirma estado KMS: a continuação de Wick aqui é identidade de matrizes (a pedra de origem
  diz o mesmo). O KMS da luz na cunha entra por citação (Bisognano–Wichmann 1975) [KNOWN].
* Não cria as rotações que mudam a direção da luz: cada leitura cria o objeto do SEU plano. Esta
  lê o plano do boost (t–x). A tela transversal (a helicidade) tem a sua leitura (D1′). Os planos
  que giram uma direção nula noutra não têm leitura tipada no kernel.
* A leitura ontológica «Nome (posto relativo) → identidade (relação de contorno)» é do operador
  [ONTO]; os teoremas abaixo são a forma matemática que ela encontra no kernel [REAL].
-/

namespace TGLExt.TheReadingCreatesTheObject

open ChatgptAudit.PolarPeriod016 ChatgptAudit.Wick016

/-- ★ **ANTES DA LEITURA, A FACE NÃO FECHA.** O boost real só é a identidade em `s = 0`:
    a rapidez não volta; a posição é relativa. -/
theorem the_face_does_not_close (s : ℝ) (h : TGLExt.boost s = 1) : s = 0 := by
  have h01 := congrFun (congrFun h 0) 1
  simp [TGLExt.boost] at h01
  exact h01

/-- ★ **A LEITURA CRIA O CONTORNO.** A identificação angular é fiel exatamente com uma volta. -/
theorem the_reading_creates_the_contour {kappa period : ℝ} (hk : kappa ≠ 0) :
    AngularQuotientFaithful kappa period ↔
      kappa*period = 2*Real.pi ∨ kappa*period = -(2*Real.pi) :=
  faithful_period_iff hk

/-- ★ **A FACE LIDA FECHA.** O boost continuado à rapidez `2π·i` é a identidade. -/
theorem the_read_face_closes :
    wickW⁻¹ * complexBoost (Complex.I*((2*Real.pi : ℝ) : ℂ)) * wickW = 1 :=
  wick_boost_two_pi

/-- ★ **O CONTORNO FIEL DÁ A TEMPERATURA.** `1/P = κ/2π`. -/
theorem the_contour_gives_the_temperature {kappa period : ℝ} (hk : 0 < kappa) (hp : 0 < period)
    (h : AngularQuotientFaithful kappa period) : 1/period = kappa/(2*Real.pi) :=
  reciprocal_temperature hk hp h

/-- ★ **A PRIMEIRA LEITURA IDENTIFICA.** Da forma de duas faces, a face com a sua fase. -/
theorem the_first_reading_identifies (θ : ℝ) :
    TGLExt.projPlus * TGLExt.angFamily θ = Complex.exp ((θ : ℂ) * Complex.I) • TGLExt.projPlus :=
  TGLExt.the_observer_reads_the_angle θ

/-- ★ **RELER NÃO ACRESCENTA.** -/
theorem rereading_adds_nothing (θ : ℝ) :
    TGLExt.projPlus * (TGLExt.projPlus * TGLExt.angFamily θ) = TGLExt.projPlus * TGLExt.angFamily θ :=
  TGLExt.observing_adds_nothing θ

/-- ★★★ **A LEITURA CRIA O OBJETO** (a cláusula composta): antes, a face não fecha; a leitura
    fecha o contorno com uma volta e dá a temperatura; a face lida fecha em `2π`; a primeira
    leitura identifica e reler não acrescenta. -/
theorem the_reading_creates_the_object :
    (∀ s : ℝ, TGLExt.boost s = 1 → s = 0) ∧
    (wickW⁻¹ * complexBoost (Complex.I*((2*Real.pi : ℝ) : ℂ)) * wickW = 1) ∧
    (∀ kappa period : ℝ, kappa ≠ 0 →
      (AngularQuotientFaithful kappa period ↔
        kappa*period = 2*Real.pi ∨ kappa*period = -(2*Real.pi))) ∧
    (∀ kappa period : ℝ, 0 < kappa → 0 < period →
      AngularQuotientFaithful kappa period → 1/period = kappa/(2*Real.pi)) ∧
    (∀ θ : ℝ, TGLExt.projPlus * (TGLExt.projPlus * TGLExt.angFamily θ) =
      TGLExt.projPlus * TGLExt.angFamily θ) :=
  ⟨the_face_does_not_close, the_read_face_closes,
   fun _ _ hk => the_reading_creates_the_contour hk,
   fun _ _ hk hp h => the_contour_gives_the_temperature hk hp h,
   rereading_adds_nothing⟩

end TGLExt.TheReadingCreatesTheObject

#print axioms TGLExt.TheReadingCreatesTheObject.the_face_does_not_close
#print axioms TGLExt.TheReadingCreatesTheObject.the_reading_creates_the_contour
#print axioms TGLExt.TheReadingCreatesTheObject.the_read_face_closes
#print axioms TGLExt.TheReadingCreatesTheObject.the_contour_gives_the_temperature
#print axioms TGLExt.TheReadingCreatesTheObject.the_first_reading_identifies
#print axioms TGLExt.TheReadingCreatesTheObject.rereading_adds_nothing
#print axioms TGLExt.TheReadingCreatesTheObject.the_reading_creates_the_object
