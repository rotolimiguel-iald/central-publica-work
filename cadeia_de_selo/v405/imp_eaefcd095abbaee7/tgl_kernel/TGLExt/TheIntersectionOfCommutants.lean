import TGLExt.Commutant
import TGLExt.TheConjugationOfOperators

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A INTERSEÇÃO DOS COMUTANTES: onde exatamente mora a cláusula que falta
  [TGLExt — a pedra da REDUÇÃO DO ÚLTIMO ENUNCIADO]

A v251 montou o certificado com SETE das oito cláusulas provadas e a oitava
posta como hipótese nomeada. Esta pedra faz três coisas com essa oitava, e
nenhuma delas a descarrega:

* ★★ `commutant_iUnion` — o comutante de uma UNIÃO é a INTERSEÇÃO dos
  comutantes. Elementar, verdadeiro em qualquer anel;
* ★★★ `commutant_towerImage_eq_iInter` — e a imagem da torre É uma união
  sobre os andares (é assim que `towerImage` está definido), logo
  **M′ = ⋂_N (M_N)′**: comutar com a torre é comutar com CADA andar;
* ★★★★ `the_missing_clause_is_a_distributivity` — pela redução, a hipótese
  do certificado condicional é EXATAMENTE a distributividade da conjugação
  sobre essa interseção.

E a honestidade, no mesmo kernel: `image_does_not_commute_with_intersection`
— imagem NÃO distribui sobre interseção em geral. Existe função e existem
dois conjuntos cuja imagem da interseção é vazia enquanto a interseção das
imagens não é. **É exatamente essa a forma do obstáculo.**

O QUE ISTO ACRESCENTA: o último enunciado deixa de ser "prove Tomita" e
passa a ser um alvo com forma reconhecível — uma distributividade que, no
caso geral, é FALSA, e que portanto só pode valer pela estrutura específica
da torre (a v250 provou que em CADA andar o comutante é a multiplicação à
direita; o que falta é o passo do limite, e agora sabe-se por quê).

O QUE ISTO NÃO FAZ: não prova a cláusula, não acende bandeira, não move o
gate. Nomear a forma do obstáculo não o remove — a v252 já disse isso.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — a redução: comutar com a união é comutar com cada peça -/

/-- [KERNEL] ★★ O COMUTANTE DE UMA UNIÃO É A INTERSEÇÃO DOS COMUTANTES. -/
theorem commutant_iUnion {A : Type} [Ring A] {ι : Type} (S : ι → Set A) :
    commutantSet (⋃ i, S i) = ⋂ i, commutantSet (S i) := by
  ext x
  constructor
  · intro hx
    refine Set.mem_iInter.mpr ?_
    intro i s hs
    exact hx s (Set.mem_iUnion.mpr ⟨i, hs⟩)
  · intro hx s hs
    obtain ⟨i, hi⟩ := Set.mem_iUnion.mp hs
    exact (Set.mem_iInter.mp hx i) s hi

/-! ## B — a imagem do andar, e a torre como união dos andares -/

/-- a imagem do ANDAR N: os operadores que a torre põe no nível N. -/
def towerImageAt (P : SiteProfile) (N : ℕ) :
    Set (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  {T | ∃ x : Matrix (chainIdx N) (chainIdx N) ℂ, T = towerPi P x}

/-- [KERNEL] a imagem da torre É a união das imagens dos andares — não é
    uma escolha de leitura, é a própria definição de `towerImage`. -/
theorem towerImage_eq_iUnion (P : SiteProfile) :
    towerImage P = ⋃ N, towerImageAt P N := by
  ext T
  constructor
  · rintro ⟨N, x, rfl⟩
    exact Set.mem_iUnion.mpr ⟨N, x, rfl⟩
  · intro h
    obtain ⟨N, hN⟩ := Set.mem_iUnion.mp h
    obtain ⟨x, rfl⟩ := hN
    exact ⟨N, x, rfl⟩

/-- [KERNEL] ★★★ **M′ = ⋂_N (M_N)′**: comutar com a torre é comutar com
    CADA andar. A v250 já disse o que é o comutante de um andar; esta
    igualdade diz que o objeto inteiro é a interseção desses. -/
theorem commutant_towerImage_eq_iInter (P : SiteProfile) :
    commutantSet (towerImage P) = ⋂ N, commutantSet (towerImageAt P N) := by
  rw [towerImage_eq_iUnion, commutant_iUnion]

/-! ## C — a cláusula que falta, reescrita -/

/-- [KERNEL] ★★★★ A CLÁUSULA QUE FALTA É UMA DISTRIBUTIVIDADE: a hipótese
    do certificado condicional (v251) equivale, palavra por palavra, a
    dizer que a imagem por conjugação cobre a INTERSEÇÃO dos comutantes
    dos andares. -/
theorem the_missing_clause_is_a_distributivity (P : SiteProfile) :
    (commutantSet (towerImage P)
        ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P))))
      ↔ ((⋂ N, commutantSet (towerImageAt P N))
        ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P)))) := by
  rw [commutant_towerImage_eq_iInter]

/-! ## D — a honestidade: por que o passo do limite é duro -/

/-- [KERNEL] [HONESTIDADE] ★★★ IMAGEM NÃO DISTRIBUI SOBRE INTERSEÇÃO: há
    função e há dois conjuntos cuja imagem da interseção é VAZIA enquanto a
    interseção das imagens NÃO é. Esta é exatamente a forma do obstáculo do
    passo do limite — a distributividade que falta é, no caso geral, FALSA,
    e só pode valer pela estrutura específica da torre. -/
theorem image_does_not_commute_with_intersection :
    ∃ (α β : Type) (f : α → β) (S T : Set α),
      f '' (S ∩ T) ≠ (f '' S) ∩ (f '' T) := by
  refine ⟨Bool, Unit, fun _ => (), {true}, {false}, ?_⟩
  intro hEq
  have hmem : (() : Unit)
      ∈ ((fun _ : Bool => (() : Unit)) '' ({true} : Set Bool))
        ∩ ((fun _ : Bool => (() : Unit)) '' ({false} : Set Bool)) :=
    ⟨⟨true, rfl, rfl⟩, ⟨false, rfl, rfl⟩⟩
  rw [← hEq] at hmem
  obtain ⟨b, hb, _⟩ := hmem
  have h1 : b = true := hb.1
  have h2 : b = false := hb.2
  rw [h1] at h2
  exact Bool.noConfusion h2

end

end TGLExt
