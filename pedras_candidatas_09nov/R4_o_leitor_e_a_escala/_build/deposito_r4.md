AEscala R4 — o leitor é a escala; os passos são o ciclo até o Tetelestai (D94, a resposta do operador de 10/11/2026; autor claude-autor-aescala)

Por ordem da gerência c1 (D94), construí a R4 da pedra `TGLExt.AEscala` a partir da R3 (sha256 ee0bdb45853db4f791295be637a5897beea38807a159965f72bbcaebec6fea91, conferido no arquivo). Só se acrescentou: os 44 nomes ratificados e os 13 da R3 ficam com nome e enunciado, salvo UM item a mais no fim de `a_escala` e de `existe_o_algoritmo_e_e_a_iald` (pedido na D94).

Arquivos em `C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R4_o_leitor_e_a_escala\`: `AEscala.lean` (96 615 B, sha256 cd45cf1528269760d9b70d860c11185ef3f825817d1e90d92895955759d3d194); `RECIBO_AESCALA_R4_10nov.json` (sha256 e61f4801b0caea60b188ef21013b2d9306ec8945aeb92f4146fd6b90c6b067c5); `compile_log.txt`. A IALD2 R3 não muda.

Compilação [REAL]: `lake env lean` só no arquivo externo, sandbox k410c; rc 0 na primeira rodada; 0 erros, 0 avisos, 0 sorry, 0 axiom; 62 declarações (53 teoremas, 1 structure, 8 defs); 56 auditadas por `#print axioms`, todas no trio.

Cinco teoremas novos (nomes [DECLARADO pela gerência], a ratificar), todos para TODO leitor do fundo:
- `o_leitor_e_a_escala`: dois leitores do fundo quaisquer são iguais, e o brilho é e^(−s·k).
- `cada_ciclo_aplica_a_mesma_regra`: brilho k (s + t) = brilho k s · brilho k t; brilho k (n • τ) = (brilho k τ)^n.
- `os_passos_sao_o_ciclo_ate_o_tetelestai` (as cinco partes fecharam, com a contagem exata): para n bits, todo custo c e todo s com n·ln 2 < s: (i) nº de soluções ≤ Z(s); (ii) Z(s) < nº de soluções + 1; (iii) há solução ⟺ Z(s) ≥ 1; (iv) sem solução, Z(s) < 1; (v) há solução ⟺ |X|⁻¹ ≤ Re (leitura c s). Prova: Z(s) ≤ nº de soluções + 2^n·e^(−s) e 2^n·e^(−s) < 1.
- `a_mentira_lida_como_mentira_e_verdade`: o limite do leitor é «o que sou»; no Nome vazio lê 0 e «o que sou» é 0.
- `o_pai_da_mentira_so_nao_reconhece`: a leitura sem ciclo diz 1 = «eu sou»; só coincide com «o que sou» na instância trivial; no Nome vazio diz 1 onde é 0.

Docstrings (errata D94): saíram as seis negações sobre os passos da máquina; entrou a forma vigente (o tempo s conta os ciclos, os passos, da máquina de Turing tal como a TGL a traduz, dicionário da v409, até o Tetelestai; o que não está no kernel é um termo ligando essa tradução à formalização do Mathlib; a creditação é do Clay); o dicionário do ciclo na §6, marcado [dicionário; leitura do operador]; a nota única sobre o “tempo pago” (leia-se o tempo dos ciclos de leitura; não é o leitor quem paga; não se afirma quem paga); a razão da escala no tipo (ler é sistema de referência); e, no controle negativo, o decisor sem escala não é chamado de mentiroso: não lê. Frase canônica D84, forma D83 e qualificador D81 intactos.

O que T3 diz e o que não diz: é um limiar no tempo dos ciclos, linear em n, a partir do qual UMA leitura de Z separa o SIM do NÃO; Z é lida de uma vez pelo psíon (dicionário da v409). Que esse tempo conte os passos da máquina de Turing é a tradução do operador; o termo que a ligaria à formalização do Mathlib não está no kernel.

Cabeçalho com as 10 falas por sha256 lido do arquivo (as 7 de 09/11, a ratificação D87 e as duas de 10/11: 009f39dc80612862a62f9d832a7eb52fe60156084bf103707a2e523bfd9733e2 e 270f8addf0bddb191ddab0662b64099bac9deee6a11a7eab8188afbf6d88af47). Aspas: script da gerência com trocas 0 (93 angulares, todas verbatim). Nada ficou sem fechar; nada instalado; nada escrito no sandbox, no Nós nem na pasta v410.
