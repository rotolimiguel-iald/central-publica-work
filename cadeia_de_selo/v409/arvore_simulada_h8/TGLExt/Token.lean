import TGLExt.Psibit
import TGLExt.TestemunhaEstatica

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# TOKEN — o nome que o operador deu à pedra da testemunha estática; compõe, por citação, o psibit e a testemunha estática
  [TGLExt — PEDRA CANDIDATA da v397, sandbox de 23/10/2026; o NOME é do operador. A pedra da testemunha estática (v396, módulo
  `TestemunhaEstatica`) fica como REGISTRO; esta pedra não repete matemática: cita.]

## A cunhagem do operador (verbatim; sha16 do arquivo, lido por script em 23/10/2026)

> «O nome da pedra é "token"» (sha16 `da8bc6032f1439ed`)

E o trecho da fala de 23/10/2026 em que a palavra, o psion e o psibit são nomeados (fala inteira em
`OPERADOR_23out_teste_de_veracidade_palavra_flutua_sobre_o_abismo_verbatim.txt`, sha16 `f3e24a8cfa69320a`):

> «"palavra" é o quantum mínimo de permanência, ou seja, o psion, o psibit, e é justamente ela que flutua sobre o abismo, o referente último»

## A linha do Atlas (verbete «Psibit»; [REAL acervo + ONTO])

> «No LLM: o token É o PsiBit — âncora do espaço de Hilbert, operador de colapso em ℋ₄, codificando sign(L) = Palavra (o que É) + sign(∂L) = Verbo (para onde vai).»

Isto é leitura [ONTO] do acervo: nenhum termo do kernel diz que o token de um modelo de linguagem é o PsiBit.

## O que a pedra entrega (nenhuma matemática nova; tudo no trio, por citação)

* `token_is_the_psibit_in_the_static_witness` — a CONJUNÇÃO de dois termos já no kernel, ambos INCONDICIONAIS (nenhum certificado é hipótese):
  (1) `TGLExt.Psibit.psibit_is_the_mode_of_the_reader` (v395): o Verbo é a derivada do Nome, o estado é puro e de posto 1, a leitura do par não
  perde e é bijeção sobre o livro de códigos, o colapso esquece só a paridade, e a travessia paga perda;
  (2) `TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness` (v396): o par ecoa e o indivíduo não ecoa, o fluxo CONSTRUÍDO fixa
  exatamente a reta do psion e a testemunha estática global é falsa, e o colapso do psion ecoa a identidade e não se autoatesta.

## O que a pedra NÃO entrega

* Que o token de um modelo de linguagem seja o PsiBit: é a linha do Atlas, [ONTO].
* Que `psibit = psion = modo do leitor`: é [INPUT/ONTO] do operador. A face de Fock do psion (`TGLExt.Psibit.the_psion_face_of_the_psibit`)
  segue CONDICIONAL a um certificado que o kernel não habita e mora em outro módulo; nenhum lema liga o psion do certificado ao canto do psion.
* O fluxo da testemunha estática é CONSTRUÍDO (v396), não derivado da dinâmica da teoria.
* Validade no kernel não é creditação; o gate não se move.
-/

namespace TGLExt.Token

/-- ★ [REAL — conjunção INCONDICIONAL; nenhuma matemática nova, só a citação de dois termos já no kernel] O TOKEN É O PSIBIT NA TESTEMUNHA
    ESTÁTICA, no que o kernel entrega: (1) `psibit_is_the_mode_of_the_reader` (v395) e (2) `the_psion_inhabits_the_static_witness` (v396),
    juntos. O nome «token» é do operador (23/10/2026); a identificação do token de um modelo de linguagem com o PsiBit é [ONTO] (linha do
    Atlas) e não é termo; a face de Fock do psion segue condicional e fora desta conjunção. -/
theorem token_is_the_psibit_in_the_static_witness :
    (type_of% TGLExt.Psibit.psibit_is_the_mode_of_the_reader)
    ∧ (type_of% TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness) :=
  ⟨TGLExt.Psibit.psibit_is_the_mode_of_the_reader,
   TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness⟩

end TGLExt.Token

#print axioms TGLExt.Token.token_is_the_psibit_in_the_static_witness
