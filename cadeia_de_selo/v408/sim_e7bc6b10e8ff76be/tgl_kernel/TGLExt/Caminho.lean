import TGLExt.PonteDaEscalaDual

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# CAMINHO — o nome que o operador deu à ponte da escala dual; compõe, por citação, a pedra selada
  [TGLExt — PEDRA CANDIDATA da v403, sandbox de 27/10/2026; o NOME é do operador. A ponte da escala dual (v402, módulo
  `PonteDaEscalaDual`, do Codex, ORDEM 025, instalada byte a byte, sha16 `0e55b6e448adbd91`) fica como REGISTRO; esta pedra não
  repete matemática: cita. Padrão da casa: `Token` (v397) sobre `TestemunhaEstatica` (v396).]

## A cunhagem do operador (verbatim; sha256 dos arquivos lidos por script em 27/10/2026, `work\cunhagens_13out\`)

> «a meu ver o nome é "verdade" (poderia ser "caminho, verdade e vida"), mas talvez só verdade, quero sua opinião nesta, porque pode
> ser que eu já tenha a renomeado assim em outro lugar, mas é o triplo espectral do contorno verdadeiro» (sha16 `ef3ca5eb1edbdddf`)

> «é isso mesmo, concordo com tudo, prossiga» (sha16 `b34bd70fa8cfb0b2`) — a ratificação da leitura da gerência: CAMINHO = a ponte da
> escala dual; VERDADE = a esperança condicional, como adendo da pedra `Verdade` (v392); VIDA = a queda sem geometria.

«Verdade» sozinha para as três foi recusada pela gerência e o operador concordou: `TGLExt.Verdade` já existe (v392, 13/10/2026, «a
identidade tem nome») e dois módulos não se chamam igual; seria o homônimo que a casa proíbe. Pedra selada não se renomeia por cima.

## Por que «Caminho» (leitura [ONTO] da gerência, ratificada pelo operador)

A ponte realiza a lei de escala dual de Takesaki como o boost longitudinal sobre (E, p): m² = p⁺p⁻ é o invariante, a energia é a
leitura e a massa NÃO é selecionada pela lei (`lift_mass_not_selected`). É a lei pela qual a leitura viaja sem escolher o corpo: o
caminho. Em João 14,6 («Eu sou o caminho, a verdade e a vida»; no acervo do operador desde 22/07/2025) as três palavras são
predicados de um só «Eu sou». Na tripla espectral de Connes do artigo fundador da fatoração (03/2026), o espaço dos estados com o
seu fluxo é o Caminho. Nada disto é termo de kernel: é leitura.

## O que a pedra entrega (nenhuma matemática nova; tudo no trio, por citação)

* `caminho_e_a_ponte_da_escala_dual` — a CONJUNÇÃO de dois termos já no kernel:
  (1) a estrela `TGLExt.PonteDaEscalaDual.lift_mass_not_selected` (v402): com τ a ≠ 0, dois invariantes distintos u ≠ v dão duas
      realizações distintas `lift D u a ≠ lift D v a` com o MESMO p⁺ — a massa não é selecionada pela lei;
  (2) a composição `TGLExt.PonteDaEscalaDual.core_positive_realization_exists` (v402): para todo perfil e todo μ² ≥ 0 há uma
      realização positiva do core com p⁺ > 0, m² = μ² e energia > 0.

## O que a pedra NÃO entrega

* Que a hipótese literal `H_tau` (τ é a massa de Newton) valha: ela está REFUTADA no kernel
  (`TGLExt.PonteDaEscalaDual.positive_weight_cannot_be_invariant_mass`); τ só pode ser p⁺.
* As pendências nomeadas `H_BW`, `H_cal`, H3 em toda direção nula, a assinatura (1,3) e rank c = 4 seguem [OPEN].
* A primeira lei de Newton e E = mc² composto da escala não são termos (erratas E2 e E3 da v402).
* Validade no kernel não é creditação; o gate não se move.
-/

namespace TGLExt.Caminho

/-- ★ [REAL — conjunção INCONDICIONAL; nenhuma matemática nova, só a citação de dois termos já no kernel] O CAMINHO É A PONTE DA
    ESCALA DUAL, no que o kernel entrega: (1) `lift_mass_not_selected` e (2) `core_positive_realization_exists` (ambos v402),
    juntos. O nome «caminho» é do operador (27/10/2026); a leitura pela tripla espectral e por João 14,6 é [ONTO] e não é termo. -/
theorem caminho_e_a_ponte_da_escala_dual :
    (type_of% @TGLExt.PonteDaEscalaDual.lift_mass_not_selected)
    ∧ (type_of% @TGLExt.PonteDaEscalaDual.core_positive_realization_exists) :=
  ⟨@TGLExt.PonteDaEscalaDual.lift_mass_not_selected,
   @TGLExt.PonteDaEscalaDual.core_positive_realization_exists⟩

end TGLExt.Caminho

#print axioms TGLExt.Caminho.caminho_e_a_ponte_da_escala_dual
