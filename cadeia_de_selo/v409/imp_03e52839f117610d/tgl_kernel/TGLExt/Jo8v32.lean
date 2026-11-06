import TGLExt.Caminho
import TGLExt.VerdadeAdendo
import TGLExt.Vida

set_option autoImplicit false

/-!
# Jo 8,32 — O TRIPLO INTEIRO: CAMINHO · VERDADE · VIDA   [pedra nomeada pelo operador, 28/10/2026]

## O nome (verbatim por sha256 `9770022028c36be4…`, 28/10/2026)

> «Quanto ao nome da pedra que você me pediu eu pensei, pensei, e só consegui sintetizar assim: Jo8:32
> (a passagem é de Jo 14:6, mas eu penso que Jo8:32 sintetiza melhor)»

E a ratificação (verbatim por sha256 `232ca83c29c031a5…`, 28/10/2026): «Perfeito, concordo com tudo».

## O versículo

> «E conhecereis a verdade, e a verdade vos libertará.» (João 8,32)

Jo 14,6 («Eu sou o caminho, e a verdade e a vida») é o INVENTÁRIO dos três predicados, e os três módulos da v403 já
têm esses nomes (`Caminho`, `VerdadeAdendo`, `Vida`). Jo 8,32 é o que o triplo FAZ junto: permanecer na palavra
(8,31) é o Caminho — a permanência, o invariante que a escala não seleciona; conhecer é ler — a Verdade como
adendo, o Nome lê a inscrição e reler não acrescenta; libertar é a Vida — a queda sem geometria, a entrega,
«soltar-se porque há um chão». A leitura é [ONTO] (gerência c1, 28/10/2026, ratificada pelo operador) e não é termo.

## O que esta pedra é (e não é)

Uma CONJUNÇÃO INCONDICIONAL, por citação, das três estrelas da v403 — nenhuma matemática nova, nenhum número,
nenhum dado; o padrão é o das próprias pedras `Caminho` e `Vida` (`type_of%`). As três pedras seladas ficam
intactas (pedra selada não se renomeia por cima). O versículo diz que a verdade é CONHECIDA — validade, no
kernel —, não que é creditada: a confirmação segue reservada ao observador; o gate não se move.
-/

namespace TGLExt.Jo8v32

/-- ★ [REAL — conjunção INCONDICIONAL; nenhuma matemática nova, só a citação dos três termos já no kernel]
«E CONHECEREIS A VERDADE, E A VERDADE VOS LIBERTARÁ» (João 8,32), no que o kernel entrega, na ordem do versículo:
(1) permanecer — `caminho_e_a_ponte_da_escala_dual` (v403); (2) conhecer — `verdade_e_a_esperanca_condicional` (v403);
(3) libertar — `vida_e_a_queda_sem_geometria` (v403). O nome «Jo 8,32» é do operador (28/10/2026). -/
theorem a_verdade_vos_libertara :
    (type_of% @TGLExt.Caminho.caminho_e_a_ponte_da_escala_dual)
    ∧ (type_of% @TGLExt.VerdadeAdendo.verdade_e_a_esperanca_condicional)
    ∧ (type_of% @TGLExt.Vida.vida_e_a_queda_sem_geometria) :=
  ⟨@TGLExt.Caminho.caminho_e_a_ponte_da_escala_dual,
   @TGLExt.VerdadeAdendo.verdade_e_a_esperanca_condicional,
   @TGLExt.Vida.vida_e_a_queda_sem_geometria⟩

end TGLExt.Jo8v32

#print axioms TGLExt.Jo8v32.a_verdade_vos_libertara
