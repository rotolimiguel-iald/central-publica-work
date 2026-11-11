AEscala R5 — a cláusula do Tetelestai: o reconhecimento em 1 − β (D100), com a ratificação D101 nas docstrings (10/11/2026; autor claude-autor-aescala)

Por ordem da gerência c1 (D100 e D101), construí a R5 da pedra `TGLExt.AEscala` a partir da R4 (sha256 cd45cf1528269760d9b70d860c11185ef3f825817d1e90d92895955759d3d194, conferido no arquivo). Só acréscimo: os 62 nomes da R4 ficam com nome e enunciado (mudou só a docstring da `os_passos_sao_o_ciclo_ate_o_tetelestai` e o cabeçalho); `a_escala` e `existe_o_algoritmo_e_e_a_iald` não ganharam item.

Arquivos em `C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R5_tetelestai_um_menos_beta\`: `AEscala.lean` (114 793 B, sha256 e4570f85566074fc9ad2b80bffcddc24da2333a7b0d890654aa72df864b32d67); `RECIBO_AESCALA_R5_10nov.json` (sha256 a2df3099c4843b56df146e889d60652ef83059a31a5fcf3055444a8d0512f84a); `compile_log.txt`.

Compilação [REAL]: `lake env lean` só no arquivo externo, sandbox k410c; rc 0 na primeira rodada; 0 erros, 0 avisos, 0 sorry, 0 axiom; 68 declarações (59 teoremas, 1 structure, 8 defs); 62 auditadas por `#print axioms`, todas no trio.

Teoremas novos (para n bits, todo custo c):
- `o_tetelestai_e_um_menos_beta` (T6): havendo solução, 0 < b < 1, 0 ≤ s e n·ln 2 + ln((1 − b)/b) ≤ s: (i) (1 − b)·Z(s) ≤ nº de soluções; (ii) Z(s) − nº de soluções ≤ b·Z(s); (iii) (1 − b)·Re (leitura c s) ≤ nº de soluções/|X|, para todo leitor do fundo.
- `o_sistema_reconhece_a_singularidade_do_sinal` (T7): com UMA solução, (1 − b)·Z(s) ≤ 1, 1 ≤ Z(s) e Z(s) − 1 ≤ b·Z(s).
- `beta_e_o_operador_modular_do_tetelestai` (T8): com o acoplamento do kernel (`TGLCoupling`, β só por nome): 0 < β < 1; T6 e T7 com b = β; |R|² = β e |T|² = 1 − β; |T|²·Z ≤ nº de soluções e Z − nº de soluções ≤ |R|²·Z; e a identidade aritmética de que o excesso sobre as oitavas é a mesma constante ln((1 − β)/β).
- `a_informacao_completa_se_reconstroi` (a opcional, fechou): ‖trava c t uniforme − P_Nome uniforme‖ ≤ √(b/(1 − b))·‖P_Nome uniforme‖ para t ≥ n·ln 2/2 e t ≥ n·ln 2/2 + ln((1 − b)/b)/2 (de `a_trava_em_tempo_linear`, v409).
- auxiliares da autoria: `a_flutuacao_do_fundo_e_cotada` (Z(s) ≤ nº de soluções + |X|·e^(−s), s ≥ 0, todo X) e `ate_meio_o_tempo_do_tetelestai_nao_e_negativo` (b ≤ ½ ⟹ o limiar é ≥ 0).

ACHADO (o número corrigiu a frase): a T6 como pedida, sem a hipótese 0 ≤ s, é falsa para b > ½ (o limiar pode ser negativo e, com s < 0, os pixels sem solução crescem). Contraexemplo numérico calculado por script, no recibo (b genérico, não é β): n = 1, custos (0, 2), b = 0,9, s no limiar ≈ −1,504: (1 − b)·Z = 2,125 > 1. Acrescentei `0 ≤ s` a T6, T7 e T8; é automática quando b ≤ ½ (lema). O kernel dá 0 < β < 1 (os dois campos de `TGLCoupling`) e não dá β ≤ ½, porque β nunca é literal.

Lemas de β do kernel usados: `TGLCoupling.beta_pos`, `TGLCoupling.beta_lt_one` (campos), `TGLCoupling.reflection_weight` (|R|² = β) e `normSq_reflection_add_transmission` (|R|² + |T|² = 1; daí |T|² = 1 − β).

Docstrings: na T3, a decisão exata (Z ≥ 1 ⟺ solução) é formalização da gerência e a cláusula do Tetelestai do operador é a T6; nas novas, [TEOREMA] as desigualdades e [dicionário; leitura do operador, fala 11] que o limiar é o Tetelestai e que β é o seu operador modular; a citação do dispositivo (runner da patente ACOM Mirror, âncoras T12 a T15, [PILOTO][SIM], nada ali valida física, α² nominal fora da transformada), conferida no runner só em leitura e sem número de desempenho; e o limite repetido: é o tempo de UMA leitura de Z, lida de uma vez pelo psíon; o termo que liga esse tempo à formalização do Mathlib não está no kernel; a creditação é do Clay.

D101 (só docstring): os nomes novos da R3 (com os três campos), da R4 e os quatro da R5 dados pela gerência passam a RATIFICADOS pelo operador em 10/11/2026 (fala 12, sha256 b7907df0843d9ff5b71d81cb8f7569c0dd8bee532a2fb4bd2e431b6ee31e04eb); os seis de enunciado mudado, “ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo”; a D87 fica. RESSALVA da autoria: os dois nomes auxiliares da R5 foram cunhados depois dessa fala; a pedra os marca [DECLARADO pela autoria] e não diz que o operador os ratificou.

Cabeçalho com as 12 falas por sha256 lido do arquivo. Aspas: script da gerência com trocas 0 (102 angulares, todas verbatim). Frase canônica D84 (3) e forma do tempo D94 (6) intactas; nenhuma frase vedada; β nunca literal. Nada ficou sem fechar; nada instalado; nada escrito no sandbox, no Nós, na pasta v410 nem na pasta das patentes.
