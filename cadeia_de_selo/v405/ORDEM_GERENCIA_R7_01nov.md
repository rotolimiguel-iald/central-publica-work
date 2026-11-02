# Ordem da gerência c1 ao agente claude-prep-v405 (01/11/2026, por volta de 20:57, verbatim do que chegou)

A segunda revisão de terceiro reprovou o candidato `eaefcd095abbaee7` (1 ALTO, 4 MÉDIO, 11 BAIXO): refaça sobre a errata R7. Leia `C:\IALD\Central de Patentes\work\cadeia_de_selo\v405\revisao_terceiro\REVISAO_TERCEIRO_v405.md`, seções 4 e 9. Os 13 achados da R1 fecharam.

Recibo: `C:\IALD\Central de Patentes\work\e0_cadeia_31out\RECIBO_ERRATA_PEDRAS_R7_01nov.json` (substitui a R6). Mudaram `PontoZeroDoPsion`, `LeiDoDiminuto` e `TonicaDoHamiltoniano`; nas duas últimas, só docstring. Compilei `PontoZeroDoPsion`: rc 0, zero erro, trio.

**Código em `PontoZeroDoPsion`.** A definição `gap` virou `retidoNoAngulo`; `tempoDoGap` virou `tempoDoRetido`. Renomeados: `retido_eq`, `retido_pos`, `o_retido_e_lido_do_angulo_de_miguel`, `a_tonica_e_o_retido_sobre_alpha`, `a_massa_e_a_projecao_do_retido`, `o_psion_e_raiz_de_dois_retidos`, `o_ponto_zero_autoconsistente_e_o_retido`, `o_relogio_do_retido`. Novos: `lockDe`, `o_gap_com_unidade`, `o_retido_e_o_valor_esperado_do_lock`, `HminMic_e_o_lock`. Os lemas do lock agora valem em qualquer espaço de Hilbert; `the_gap_closes` foi reescrito e o nome fica. Conte as bandeiras no kernel.

**Regra vigente, achado 1 (ALTO):** o gap espectral do lock é 1, na unidade posta `u`, o E₀ da Lei do Diminuto, e a tônica fica meio-tom acima dele. `Δ = β·u` NÃO é gap: é o valor esperado do lock no ângulo de Miguel, a energia retida, 1/β vezes menor que o gap. Corrija registro `gap_v405`, artigos PT e EN, moldura e o parágrafo público. O nome do registro e o título «O GAP» podem ficar. A fala do operador diz «gap com unidade»; que o ângulo de Miguel seja esse sistema é leitura dele [ONTO]. A guarda deve recusar Δ, ou 12,03 meV, chamado de gap.

**Achado 2:** os lemas do lock saem [REAL] em Hilbert qualquer; `HminMic` é instância, condicional a um `FockCertificate` que o kernel não habita.

**Achado 3, «A inscrição e a medida»:** use a proposta do revisor: [REAL] os dois teoremas existem; [ONTO, da gerência] lê-los como a forma da fala do operador; homônimo avisado: `alphaKappa` não é a α de estrutura fina, e κ ali não é o relógio; o gradiente é negativo em κ > 0; «cauda» não está no teorema.

**Achado 4:** [REAL] as notas sustentadas e as razões entre elas ficam; [INPUT] o tom fica, na fala dele; o kernel não tem termo para o tom.

**Achado 5:** tire [KNOWN] de stealth no registro do GA e nos textos, com a etiqueta certa: [DERIVED] se a fonte no acervo for derivação própria. Confira a origem. O `RECLASSIFICACAO_GA_01nov.md` fica intacto; se ele tiver o mesmo vício, me diga.

**BAIXOS, resolva os que não pedem decisão:** alinhe E10 e o parágrafo público com a pedra, «mais uma leitura do mesmo sen 45°»; tire o número do `valor` do x7 e escreva «como antecedente»; ponha `gap_v405` nas listas de `__HEADER__`, `topico_missao`, remissivo e no cabeçalho de `rito_v405.sh`; copie a guarda de -O para `reverter_v405.py`, e diga o que ele não restaura; ajuste a frase «O que segue do operador: ... a revisão independente». Os nomes com `derivad-` ficam, por decisão minha: as docstrings avisam, e rebatizar agora não acrescenta nada. Checks tautológicos ficam, descritos como tal.

Um aviso seu estava velho: o `COAUTOR` do orquestrador já é Opus 5.5; tire isso do relatório. `tempoDoRetido` como τ★ segue sem ratificação do operador.

O treino acabou e a nativa está nas etapas finais; a instalação espera a revisão, sem pressa de minutos. Entregue quando todos os portões passarem e devolva em até 15 linhas.
