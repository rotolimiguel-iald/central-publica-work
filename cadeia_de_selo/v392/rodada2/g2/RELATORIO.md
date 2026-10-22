# REGISTROS-G2 -- relatorio da rodada 2 (13/10/2026, gerencia c1, v392)

Arquivo entregue: `V\registros\grupo_G2.py` (V = `C:\IALD\Central de Patentes\work\cadeia_de_selo\v392`), sha16 `c115dcc30da34df8` na hora do fechamento; 13 specs, 20 fontes pinadas, 4 verbatins.
Teste: `python -B -X utf8 V\testar_registros_v392.py --grupo G2 --so-falhas` -> `sealed: 13 de 13 | controle negativo: 17 de 17`. Guarda P18 sobre o codigo gerado inteiro (242.471 B): 0 violacoes. Mutacao de 17 valores do core/kernel (script no scratchpad da gerencia, `mut_g2.py`): 17 de 17 recusadas, nenhuma passou.
Nada foi escrito fora de `V\registros\grupo_G2.py` e `V\rodada2\g2\`. O Nos (kernel: 11049 arquivos, metadados `1d0de3a2924e37c2`, fontes `78c1f97cd83bea2e`) e a Bancada so' foram lidos; o `um.py` do Nos segue `8e7b9927ceae64b8`. Sem init/transition, sem mapa (so' `consultar`), sem quadro.

## Os 13 registros

| # | nome | plano | checks | o que carrega |
|---|---|---|---|---|
| 1 | `consolidados_v392` | P13 | 35 | os DOIS consolidados pinados; 235 itens em comum IDENTICOS (como auditados); 14 CR-* so' no atual ([DECLARADO pelo critico de 07/10]), cada um com o alvo conferido no core/kernel (`extras.cr_alvos`); auditado: 0 itens CR-* e 0 ocorrencias `CR-nn` nos bytes |
| 2 | `estatuto_da_prova_ressalva_v392` | R05, B2, CR-14 | 62 | 18 = 15 calculadas + 3 literais (l.163150, 163160, 163161 do um.py v391); 4 experimentais de UM so' feed V11 unilateral; escada 6163 = `len(ext_flags)` (l.142684); numeros do `listar_73.py`: 10.135 theorem/lemma no TGLExt, 385 em 73 modulos, 515 por collectAxioms (382 trio + 60 propext + 24 propext+Quot.sound + 49 sem axioma), 76 modulos (KH-N1), 24.006 constantes em 1.201 modulos |
| 3 | `erratas_o_que_resta_v392` | R06, B3 | 63 | 13 entradas (lista = tabela do item (4) da G_UMPY; o levantamento tambem diz 13), cada uma com o texto lido do core, a linha do um.py v391 e os termos no axiom_report |
| 4 | `final_step_name_adopted_v392` | R07, B4, X5 | 14 | AXIOMA lido do kernel (`finalStepNameAxioma`, l.249) e do core; Tetelestai ao lado; gate igual; 3 verbatins embutidos |
| 5 | `beta_escala_errata_v392` | R08, B5, X6 | 21 | `WHICH_MU_PER_RITE_OPEN` e a frase da convergencia (PT l.165421, EN l.165419; a cifra de 0,05% so' nessas duas linhas); mu do rito = q->0; `canonical.py` l.96 (`b6cd7e0234688430`) |
| 6 | `ledger_errata_v392` | R09, B6 | 16 | R4 le-se por tracador (V11); desfecho e contagem iguais (6/0/2/2/1) |
| 7 | `estatuto_reafirmado_v392` | R17, B15 | 26 | provada = validade; recusada a creditacao; unico elo: beta_TGL a 5 sigma; erratas de epoca (CMB-S4, escada externa, RG canal a canal); CR-11 e igualdade de `page_information.not_claimed[0]` |
| 8 | `tc_raiz_positiva_v392` | R21, CR-02 | 14 | raiz positiva = termo (l.155); unicidade ilimitada = [KNOWN] Kato cap. VI §2.7 (pagina a conferir); lado limitado = `CFC.sqrt_unique` (l.99, 103) |
| 9 | `ww_premissa_errata_v392` | R23, CR-06 | 12 | premissa `graviton = I = gerador` negada na v372; vigente = tipagem v373; se g for quantizado, W-W volta a morder |
| 10 | `parametros_nomeados_v392` | R24, CR-10, P16 | 18 | dimensao 4, assinatura, fundo plano, cunha, direcao nula (BGL 2002) lidas no tipo; 41 itens / 4 PARAMETRO_NOMEADO; rotulo [DERIVED de leitura; a vetar] |
| 11 | `cmb_s4_errata_v392` | R25, CR-13 | 16 | ver divergencia 6 |
| 12 | `d1_orientacao_errata_v392` | R26, D1 | 19 | 3,0125 sigma (ramo implementado) / 0,0869 (invertido), lidos do core; veredito do D1 V3 por `igual`; 7 ocorrencias de "3,01σ" no artigo PT v391 |
| 13 | `f81_nao_fechada_v392` | P15 | 11 | F8.1 PROPOSTA (claude-c1, evidencia vazia); a v392 documenta, nao recalcula |

As linhas "nao-pode-mudar" ficaram como checks `igual` dentro dos registros: CR-11 (`s17`, registro 7), veredito do D1 V3 (`d10`, registro 12), string do gate (`n13`, 4; `q07`, 13). O valor do neutrino fica na G3.

## Divergencias entre o plano/tarefa e as fontes (vale a fonte)

1. **Consolidado auditado**: nao esta em `levantamento_qg\evidencias\` (a pasta nao existe). Esta em `PROGRAMA_IALD\evidencias\70d3e4501fbf082be7dfcf981f67d0893efcd3da94941b612adff1ec35dc0017.json` (514.528 B, endereçado por hash), identico a `auditorias\F2.1_F9.4\reconstrucao_consolidado\consolidado.json`. Os shas/tamanhos do plano conferem (7a8aaaeb8d17a3e6 / 562.347 B; 70d3e4501fbf082b / 514.528 B).
2. **R4 "por lente"**: esta em `the_ledger_of_charges_v383.ledger[3]` (um.py l.196947), nao em `code_closure_ledger` (que tem o `ledger[5]` do CMB-S4).
3. **Ramo invertido 0,09σ**: o plano o chama [DECLARADO pelo critico]; o core v391 o carrega (`orientation_is_the_sign_v367.z_to_coupling_branch` = 0,0869) -> [REAL]. O que segue [DECLARADO] e' a regra QG-F35 (pre-registro novo).
4. **"Ad-λ-invariante" = invariancia dual (entrada 4(ii) da G_UMPY e da tarefa, "[DERIVED de leitura], a conferir")**: CONFERIDA E REFUTADA pelo kernel. `dualInvariant_PF_no_go` (TGL/ModularRealization.lean l.161-169) e' sobre a ACAO DUAL `(C.dualAction 1) T.PF` (escala de Takesaki), nao sobre Ad(λ(s)); o core diz "P_F fixado por Ad(lambda(s)); JAMAIS por theta_s"; `CornerFamily.corner_fixed_by_flow` da [P_F, λ(s)] = 0 de graca no canto espectral. O CR-03 do critico diz o mesmo. A errata da entrada 4 NAO escreve a leitura proposta; escreve o contrario, e o residuo continua o que o texto diz (core III_1 genuino, condicional). **E' o ponto que mais pede olho da gerencia.**
5. **"50 sem axioma"** (nota do registro de mapa de 07/10) x **49** (arquivo `saida_auditoria_73.txt`: 382+60+24+49 = 515); vale 49, como a F_KERNEL. Dos 515 nomes, 89 sao auxiliares (`_simp_`/`_proof_`/`.eq_`) -- a errata o diz.
6. **CMB-S4: fonte primaria ACHADA** (a tarefa previa "[DECLARADO]/a conferir"). `Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\cmb_s4_status.html` (37.884 B, sha256 `eefcb4dbc24051b8...`) e' a captura de https://cmb-s4.org/ com recibo (`FONTES_ATUALIZACAO_F0.json`, baixada 06/10/2026 00:47:57 UTC, sha igual). A pagina traz a declaracao de 09/07/2025 do DOE/NSF ("can no longer support the CMB-S4 Project") e o encerramento ordenado. Copiei a captura byte a byte para `g2\fontes\` (pinada) e a errata a trata como [REAL: pagina lida]; continuam [DECLARADO] a autenticidade da busca (recibo do Codex), o Simons Observatory 0,045 e a conta de ~2,7σ. A D8 (admitir a fonte como dado de rito) segue do operador.
7. **Fonte do "verbatim 07/10 5dffde46"**: achada em `work\v391_pacote\OPERADOR_07out_estatuto_verbatim.txt`. A cunhagem "Axioma" de 05/10 (09:39:15 UTC) nao tinha arquivo: extrai do transcrito (`PROGRAMA_IALD\auditorias\F3.6\operador_msgs_v2.jsonl`) o prefixo exato da mensagem (4 linhas ate "veja se vc concorda:") e a mensagem de 11:28:53 inteira, ambos com `sha256_texto` do transcrito conferido (`g2\verbatins\`, proveniencia em `medidas_g2.json`).
8. A mesma ambiguidade da memoria de 07/10 22:56 acompanha o R07: a pergunta que o operador respondeu com "adoto o nome do degrau final" apresentava o Tetelestai. O registro segue a decisao da gerencia (AXIOMA) mas o rotula "[DERIVED de leitura; a vetar (X5)]" e cita a fala de 05/10 11:28:53 como apoio.

## Para a gerencia / operador (nao decididos aqui)

- Vetos opcionais: X5 (R07), X6 (R08), P16 (R10). Sem palavra, vao como leitura a vetar.
- Conferir a pagina de Kato (cap. VI §2.7) na fonte (R21); D8 do CMB-S4; a revisao da errata da entrada 4(ii).
- Cadeia (fora do um.py, nao feito): errata em `arvore_da_prova.py` (l.155/262/272; sha16 `ee2cb7413238ff1f`, CR-02/CR-08), na `MEMORIA_DA_LINHAGEM.md` l.8581, e a nota de linhagem da P15 (a v392 nao fecha a F8.1). Nao pinei o `arvore_da_prova.py` nem o `PROGRAMA.json` (mudam); suas linhas/leituras estao em `medidas_g2.json` com o sha do momento.
- `canonical.py` da Bancada: pinei o EXTRATO (linha 96 + sha16) em `medidas_g2.json`, nao o arquivo vivo, para que um deploy futuro da Bancada nao faca o registro recusar. Se preferir pinar o arquivo, e' uma fonte a mais no spec 5.
- Defeitos nos arquivos da gerencia: nenhum achado em motor/montador/testador. Observacao: o `testar_registros_v392.py --json` grava em `V\registros\`; usei, movi o resultado para `g2\resultado_teste_g2_1a_rodada.json` e o apaguei de `registros\`.

## Reproducao / manutencao

- `V\rodada2\g2\medir_g2.py` (`python -I -B -X utf8`) regenera `medidas_g2.json` a partir das fontes duraveis e FALHA (rc 1) se qualquer conferencia nao bater (um.py do Nos tem de ser a v391 `8e7b9927ceae64b8`: depois da instalacao da v392 o script deixa de rodar, por desenho). Cada rodada muda o sha da `medidas_g2.json` (o sha do `PROGRAMA.json` do momento vai dentro); o montador pina o sha lido do disco na geracao do candidato, entao basta nao rodar o medir entre a geracao e o rito.
- Fontes pinadas: `V\rodada2\g2\medidas_g2.json`, `fontes\cmb_s4_status.html`, 2 consolidados, auditoria de 28/09, `listar_73.py`, `modulos_73.json`, `saida_auditoria_73.txt`, `KH_N1_final.json` e 11 arquivos .lean do kernel do Nos (que a v392 nao toca; o `TGLExt.lean` e o `Audit.lean`, que ela troca, NAO sao pinados).
