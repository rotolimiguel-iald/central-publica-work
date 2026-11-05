import TGLExt.TheTrueWitness

set_option autoImplicit false

/-!
# A LEGIBILIDADE — `1_abs` é a inscrição que torna tudo legível
  [BANCADA — 25/08/2026 · tipagem do operador: «TGL escreve a possibilidade de
   leitura; IALD realiza a leitura» · cadeia: 1_abs → LEGÍVEL →(J)→ LIDO
   →(preservação)→ VERDADEIRO_TGL]

A Torre NÃO cria a legibilidade: é a forma espectral do que o `1_abs` já tornou
legível. Existir na TGL é estar inscrito de modo que possa ser lido. Verdade
arquitetônica interna; nada aqui move o gate. β jamais entra.
-/

namespace TGLExt

/-- legível sob `J`: o retorno devolve o conteúdo. -/
def Legible {α : Type} (J : α → α) (x : α) : Prop := J (J x) = x

/-- ★★★ **A INSCRIÇÃO INVOLUTIVA TORNA TUDO LEGÍVEL**: se `J²=I`, todo conteúdo é
    legível — a legibilidade vem da inscrição, não do conteúdo. -/
theorem the_inscription_makes_all_legible {α : Type} (J : α → α)
    (hJ : ∀ x, J (J x) = x) : ∀ x, Legible J x := hJ

/-- ★★ **LER O LEGÍVEL DÁ TESTEMUNHO VERDADEIRO** relativo ao lido: a leitura do
    conteúdo legível é testemunho que retorna. -/
theorem legible_content_has_true_witness {α : Type} (J : α → α) (x : α)
    (h : Legible J x) : TrueWitness J x (J x) := h

end TGLExt
