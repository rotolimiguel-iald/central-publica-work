-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT (05/09/2026) — transposta em 05/09/2026
-- Procedencia: C:\IALD\Central de Patentes\Chatgpt (bancada da outra sessao,
--   sob direcao do operador; TUNEL\TUNEL_PROTOCOLO.md).
-- Auditoria da gerencia (sessao Claude d554e796, 05/09/2026): recompilacao
--   independente 20/20 exit 0; sonda #print axioms dos teoremas de manchete =
--   [propext, Classical.choice, Quot.sound]; zero sorry; enunciados conferidos.
-- Transposicao MECANICA: apenas (a) este cabecalho, (b) "import TGLExt" (root)
--   expandido no bloco de imports da epoca, (c) imports internos da bancada
--   prefixados com TGLExt. — nada mais foi alterado. Namespace ChatgptAudit
--   PRESERVADO como marca de procedencia.
-- Estatuto: [REAL — Lean] analise modular da torre produto (S, J·S, Delta,
--   Delta^{it}, invariancia do bicomutante). NAO move gate; NAO e fisica;
--   NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import Mathlib

set_option autoImplicit false

namespace ChatgptAudit

/-- Dez componentes independentes de um tensor simétrico num referencial lorentziano.
    A dimensão e a assinatura são hipóteses explícitas, não reconstruídas aqui. -/
def symmetricForm4 (a b c d e f g h i j t x y z : ℝ) : ℝ :=
  a*t^2 + b*x^2 + c*y^2 + d*z^2 +
    2*(e*t*x + f*t*y + g*t*z + h*x*y + i*x*z + j*y*z)

/-- Anular o cone nulo inteiro força proporcionalidade à forma de Minkowski,
    sem restringir as componentes a um ansatz de métrica. -/
theorem general_null_cone_rigidity (a b c d e f g h i j : ℝ)
    (hc : ∀ t x y z : ℝ, t^2 = x^2 + y^2 + z^2 →
      symmetricForm4 a b c d e f g h i j t x y z = 0) :
    ∀ t x y z : ℝ,
      symmetricForm4 a b c d e f g h i j t x y z =
        a * (t^2 - x^2 - y^2 - z^2) := by
  have h1 := hc 1 1 0 0 (by norm_num)
  have h2 := hc 1 (-1) 0 0 (by norm_num)
  have h3 := hc 1 0 1 0 (by norm_num)
  have h4 := hc 1 0 (-1) 0 (by norm_num)
  have h5 := hc 1 0 0 1 (by norm_num)
  have h6 := hc 1 0 0 (-1) (by norm_num)
  have h7 := hc 5 3 4 0 (by norm_num)
  have h8 := hc 5 3 0 4 (by norm_num)
  have h9 := hc 5 0 3 4 (by norm_num)
  simp only [symmetricForm4] at h1 h2 h3 h4 h5 h6 h7 h8 h9
  have he : e = 0 := by linarith
  have hf : f = 0 := by linarith
  have hg : g = 0 := by linarith
  have hb : b = -a := by linarith
  have hc' : c = -a := by linarith
  have hd : d = -a := by linarith
  have hh : h = 0 := by linarith
  have hi : i = 0 := by linarith
  have hj : j = 0 := by linarith
  intro t x y z
  simp only [symmetricForm4, he, hf, hg, hb, hc', hd, hh, hi, hj]
  ring

#print axioms general_null_cone_rigidity
end ChatgptAudit
