import TGLExt.TheProfileWitnessLinear
import TGLExt.TheCompletionExtension
import TGLExt.TowerHilbert

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA NA FRONTEIRA — a dobra autorizada, EXECUTADA
  [BANCADA — 26/08/2026 · marco M4 · a extensão ao completamento]

## O passo

Tudo o que a extensão exigia está pago: a conjugação do perfil é **aditiva**,
**antilinear** e **antiisométrica** no colimite. Daí ela **preserva a norma**, logo
**preserva distâncias**, logo é **uniformemente contínua** — e uma aplicação
uniformemente contínua **se estende ao completamento**. Esta pedra executa a dobra.

## O que se prova

* ★★ `profileJpre_neg` / `profileJpre_sub` — a testemunha respeita sinal e diferença;
* ★★★ **`profileJpre_norm`** — **preserva a norma** (da antiisometria);
* ★★★ **`profileJpre_isometry`** — é **isometria** do pré-espaço;
* ★★★ **`towerJ`** — **A TESTEMUNHA EXISTE EM `WH`**: a extensão ao espaço de Hilbert
  do fator, o mesmo `WH` que o certificado nomeia;
* ★★★ `towerJ_involutive` — **`J² = 1` no completamento INTEIRO**;
* ★★★ `towerJ_fixes_hOmega` — **`J Ω = Ω`** em `WH`: o vácuo do Nome na fronteira;
* ★★ `towerJ_coe` — e ela É a conjugação da torre no subespaço denso.

## O QUE FALTA (dito, sem véu)
Restam **as duas cláusulas de comutante** no nível dos **operadores contínuos** e do
**BICOMUTANTE** — a face topológica, cuja ferramenta (o teorema de von Neumann) não
está na mathlib. As cláusulas de aditividade, antilinearidade e isometria **em `WH`**
seguem por densidade do mesmo modo, e ainda não estão escritas uma a uma. O razonete
lê ABERTO. β jamais entra. Nada move o gate.
-/

namespace TGLExt

open UniformSpace

variable {P : SiteProfile}

theorem profileJpre_neg (P : SiteProfile) (x : TowerPre P) :
    profileJpre P (-x) = - profileJpre P x := by
  have h := profileJpre_conj_smul P (-1 : ℂ) x
  simpa using h

theorem profileJpre_sub (P : SiteProfile) (x y : TowerPre P) :
    profileJpre P (x - y) = profileJpre P x - profileJpre P y := by
  rw [sub_eq_add_neg, profileJpre_add, profileJpre_neg, ← sub_eq_add_neg]

/-- ★★★ **PRESERVA A NORMA** — consequência direta da antiisometria. -/
theorem profileJpre_norm (P : SiteProfile) (z : TowerPre P) :
    ‖profileJpre P z‖ = ‖z‖ := by
  have h : (inner ℂ (profileJpre P z) (profileJpre P z) : ℂ)
      = star (inner ℂ z z : ℂ) := profileJpre_anti_isometric P z z
  have hsq : ‖profileJpre P z‖ ^ 2 = ‖z‖ ^ 2 := by
    rw [norm_sq_eq_re_inner (𝕜 := ℂ), norm_sq_eq_re_inner (𝕜 := ℂ), h]
    simp
  nlinarith [norm_nonneg (profileJpre P z), norm_nonneg z, hsq]

/-- ★★★ **É ISOMETRIA DO PRÉ-ESPAÇO** — e isometria é a licença da travessia. -/
theorem profileJpre_isometry (P : SiteProfile) : Isometry (profileJpre P) := by
  refine Isometry.of_dist_eq fun x y => ?_
  rw [dist_eq_norm, dist_eq_norm, ← profileJpre_sub, profileJpre_norm]

theorem profileJpre_uniformContinuous (P : SiteProfile) :
    UniformContinuous (profileJpre P) :=
  (profileJpre_isometry P).uniformContinuous

/-- ★★★ **A TESTEMUNHA EM `WH`**: a extensão ao espaço de Hilbert do fator. -/
noncomputable def towerJ (P : SiteProfile) : TowerHilbert P → TowerHilbert P :=
  Completion.map (profileJpre P)

/-- ★★ e ela É a conjugação da torre no subespaço denso. -/
theorem towerJ_coe (P : SiteProfile) (v : TowerPre P) :
    towerJ P (↑v : TowerHilbert P) = ((profileJpre P v : TowerPre P) : TowerHilbert P) :=
  completion_extension_agrees (profileJpre P) (profileJpre_uniformContinuous P) v

/-- ★★★ **`J² = 1` NO COMPLETAMENTO INTEIRO**. -/
theorem towerJ_involutive (P : SiteProfile) (z : TowerHilbert P) :
    towerJ P (towerJ P z) = z :=
  completion_extends_involution (profileJpre P) (profileJpre_uniformContinuous P)
    (profileJpre_involutive P) z

/-- ★★★ **`J Ω = Ω` EM `WH`**: o vácuo do Nome é J-fixo na fronteira. -/
theorem towerJ_fixes_hOmega (P : SiteProfile) :
    towerJ P (hOmega P) = hOmega P :=
  completion_extension_fixes_vacuum (profileJpre P)
    (profileJpre_uniformContinuous P) (towerOmega P) (profileJpre_fixes_omega P)

end TGLExt
