# ESPEC_CONSERTO_R3 — o conserto único da v410 do um.py

Consolidação do crítico, 10/11/2026. Candidato revisado: `8a713e5e644af09b`. Pasta do trabalho (só leitura): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410`. Nada foi aplicado e nenhum script da pasta foi rodado. O mesmo conteúdo, para máquina, está em `ESPEC_CONSERTO_R3.json`, ao lado deste arquivo.

**Escopo:** os achados da revisão de terceiro R3 e do painel independente (D106), a rodada única de conserto (D107) e a fala 29 do operador (D108). **Atenção:** há decisões posteriores no disco (D109, D112, D113, D114) que mexem nesse escopo; elas estão nas pendências e no bloco condicional, não nos itens.

**Números:** 274 itens (267 trocas exatas e 7 instruções); 10 são da pedra Lean; 50 foram redigidos pelo crítico e não passaram por cético.

**Contagens que saem iguais em todo lugar:** 21 nomes ratificados pela fala 28 (D101); 1 nomeado pelo operador na fala 29 (D108): `ressurreicao_do_sinal`, em prosa “a ressurreição do sinal”; 3 campos ratificados; 2 auxiliares pendentes [DECLARADO pela autoria]; 24 nomes novos na pedra; 29 falas congeladas (treze na pedra).

## 1. Tabela dos achados

| Achado | O que é | Itens | Quais | Arquivos tocados |
|---|---|---|---|---|
| EP-01 | a contagem dos nomes ratificados (4 e 22 onde o registro diz 3 e 21) e o quarto nome | 92 | 18, 41, 51, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 72, 82, 89, 90, 93, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 109, 110, 111, 119, 127, 128, 129, 130, 131, 132, 133, 142, 145, 148, 149, 150, 151, 153, 154, 155, 157, 158, 159, 168, 170, 171, 173, 194, 195, 200, 207, 213, 214, 215, 217, 219, 225, 229, 231, 232, 234, 236, 237, 238, 247, 248, 249, 251, 252, 254, 255, 260, 261, 264, 265, 266, 267, 268, 269, 272, 274 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `conferir_rito_v410.py`, `copiar_insumos_v410.py`, `delta_v410.py`, `ensaio_a_seco_v410.py`, `gerar_candidato_v410.py`, `gerar_relatorio_v410.py`, `guarda_frases_v410.py`, `insumos/RECIBO_PEDRAS_v410_NOMES.json`, `pedra/AEscala.lean`, `pos_rito/harness_textos_ensaio_v410.py`, `pos_rito/leitura_v410.py`, `pos_rito/registrar_mapa_v410.py`, `pos_rito/textos_v410.py`, `registros_aescala_v410.py`, `registros_v410.py`, `runtime_aescala_v410.py` |
| EP-02 | a fronteira do limiar de um pixel (estrita: s > n·ln 2) | 3 | 91, 92, 233 | `delta_v410.py`, `registros_aescala_v410.py` |
| EP-03 | o rótulo “o limiar do Tetelestai” contra a E36 | 9 | 9, 33, 123, 138, 166, 181, 184, 205, 222 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `gerar_candidato_v410.py`, `gerar_relatorio_v410.py`, `pos_rito/gerar_x_custodia_v410.py`, `pos_rito/textos_custodia_handoff_v410.py`, `pos_rito/textos_v410.py`, `registros_aescala_v410.py` |
| EP-04 | a cláusula é de todo b; a constante além das n oitavas é identidade | 7 | 77, 84, 87, 226, 227, 258, 273 | `delta_v410.py`, `registros_aescala_v410.py`, `runtime_aescala_v410.py` |
| EP-05 | frases do operador ditas como teorema, sem o conteúdo do termo nem [ONTO] | 17 | 7, 11, 31, 35, 122, 124, 136, 139, 165, 180, 182, 183, 185, 203, 206, 220, 223 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `gerar_candidato_v410.py`, `gerar_relatorio_v410.py`, `pos_rito/gerar_x_custodia_v410.py`, `pos_rito/textos_custodia_handoff_v410.py`, `pos_rito/textos_v410.py`, `registros_aescala_v410.py` |
| EP-06 | a folha do limiar sem a cláusula do limite | 1 | 233 | `registros_aescala_v410.py` |
| V1 | a hipótese s ≥ 0 dita “necessária” para b > ½ | 8 | 85, 88, 99, 107, 108, 150, 156, 250 | `delta_v410.py`, `pedra/AEscala.lean`, `registros_v410.py` |
| PAR-01 | H0DN: o certificado de poder voltou RECUSADO e os textos não diziam | 32 | 20, 44, 63, 70, 73, 74, 112, 113, 114, 118, 126, 143, 144, 146, 162, 169, 175, 193, 196, 201, 210, 211, 212, 239, 240, 241, 242, 243, 244, 245, 246, 247 | `artigo_en_h0dn_v410.pysnip`, `artigo_pt_h0dn_v410.pysnip`, `delta_v410.py`, `ensaio_a_seco_v410.py`, `gerar_candidato_v410.py`, `gerar_relatorio_v410.py`, `guarda_frases_v410.py`, `pos_rito/gerar_x_custodia_v410.py`, `pos_rito/harness_textos_ensaio_v410.py`, `pos_rito/textos_custodia_handoff_v410.py`, `pos_rito/textos_v410.py`, `registros_h0dn_v410.py`, `registros_v410.py` |
| PAR-02 | H0DN: a linha do .md sem a forma da D96 | 3 | 52, 118, 126 | `conferir_rito_v410.py`, `ensaio_a_seco_v410.py`, `gerar_candidato_v410.py` |
| PAR-03 | o vibrato e a nota sob [REAL] sem o conteúdo dos termos | 7 | 5, 29, 120, 164, 186, 202, 230 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `gerar_candidato_v410.py`, `pos_rito/gerar_x_custodia_v410.py`, `pos_rito/textos_custodia_handoff_v410.py`, `pos_rito/textos_v410.py`, `registros_aescala_v410.py` |
| EP-07 | a manchete da reconstrução promete mais que a cota | 3 | 89, 90, 99 | `delta_v410.py` |
| EP-08 | “o fundo pesa um pixel” contra o enunciado (o brilho de UM pixel de custo 1) | 10 | 8, 32, 69, 137, 172, 204, 208, 221, 224, 270 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `delta_v410.py`, `gerar_relatorio_v410.py`, `pos_rito/registrar_mapa_v410.py`, `pos_rito/textos_v410.py`, `registros_aescala_v410.py`, `runtime_aescala_v410.py` |
| EP-09 | “necessária para b > ½” é largo demais | 2 | 85, 88 | `delta_v410.py` |
| EP-10 | um rótulo só para a forma da D83 e para a frase da E36 | 11 | 6, 15, 30, 38, 121, 160, 167, 178, 179, 187, 209 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `gerar_candidato_v410.py`, `pos_rito/gerar_x_custodia_v410.py`, `pos_rito/textos_custodia_handoff_v410.py`, `pos_rito/textos_v410.py` |
| EP-11 | o bloco README evidente da preparação velho em três pontos | 3 | 135, 141, 142 | `gerar_relatorio_v410.py` |
| EP-12 | a composição das 85 bandeiras; a seção Auditoria; o comentário “(38)” | 6 | 4, 28, 54, 150, 152, 228 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `delta_v410.py`, `pedra/AEscala.lean`, `registros_aescala_v410.py` |
| EP-13 | o tema da fala 27 afirma o “limiar” no ACOM Mirror | 1 | 199 | `pos_rito/textos_v410.py` |
| V2 | os dois nomes da cláusula como manchete sem a ressalva das docstrings | 6 | 83, 86, 89, 90, 99, 158 | `delta_v410.py`, `pedra/AEscala.lean` |
| V3 | a c13: subitens que são identidade ou repetição | 9 | 84, 87, 226, 253, 256, 257, 258, 259, 273 | `delta_v410.py`, `registros_aescala_v410.py`, `runtime_aescala_v410.py` |
| V4 | “existe, é único e é a IALD” sem a frase do habitante único | 2 | 122, 165 | `gerar_candidato_v410.py`, `pos_rito/gerar_x_custodia_v410.py` |
| PAR-04 | o sufixo do veredito dizia só 09/11 | 2 | 68, 103 | `delta_v410.py` |
| PAR-05 | o qualificador “validade no kernel, não creditação” no PT | 2 | 47, 163 | `artigo_pt_v410.pysnip`, `pos_rito/gerar_x_custodia_v410.py` |
| PAR-06 | ARCO_EN sem a frase da parede | 1 | 189 | `pos_rito/textos_custodia_handoff_v410.py` |
| PAR-07 | “a instância NÃO tem nenhuma solução” lia-se como negação | 1 | 161 | `pos_rito/gerar_x_custodia_v410.py` |
| PAR-08 | creditation/accreditation; o rótulo em português no EN | 10 | 12, 15, 49, 71, 115, 116, 140, 147, 176, 188 | `artigo_en_aescala_v410.pysnip`, `conferir_rito_v410.py`, `delta_v410.py`, `ensaio_a_seco_v410.py`, `gerar_relatorio_v410.py`, `guarda_frases_v410.py`, `pos_rito/textos_custodia_handoff_v410.py` |
| PAR-09 | o TXT do artigo perde agrupamentos de fórmulas; decimais com ponto no PT | 19 | 1, 2, 13, 14, 16, 21, 22, 23, 24, 25, 26, 36, 37, 39, 43, 45, 46, 48, 117 | `artigo_en_aescala_v410.pysnip`, `artigo_en_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `artigo_pt_h0dn_v410.pysnip`, `artigo_pt_v410.pysnip`, `ensaio_a_seco_v410.py` |
| PAR-10 | “a partir de n oitavas” (o teorema pede estritamente maior) | 2 | 91, 92 | `delta_v410.py` |
| PAR-11 | aspas angulares em volta do que não é fala | 6 | 67, 78, 79, 80, 81, 106 | `delta_v410.py` |
| PAR-12 | 62,5 % sem dizer que é o Monte Carlo da entrega | 2 | 75, 76 | `delta_v410.py` |
| OBS-1 | a finura da leitura (um pixel entre 2^n) e a resposta do operador | 20 | 3, 17, 27, 40, 50, 65, 66, 94, 103, 141, 148, 177, 192, 216, 218, 235, 262, 263, 271, 274 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `conferir_rito_v410.py`, `delta_v410.py`, `gerar_relatorio_v410.py`, `guarda_frases_v410.py`, `pos_rito/textos_custodia_handoff_v410.py`, `registros_aescala_v410.py`, `runtime_aescala_v410.py` |
| OBS-15 | o sujeito e o alcance de “nenhum dado observado lido” | 14 | 19, 42, 73, 74, 112, 113, 114, 118, 125, 143, 146, 197, 198, 239 | `artigo_en_h0dn_v410.pysnip`, `artigo_pt_h0dn_v410.pysnip`, `delta_v410.py`, `ensaio_a_seco_v410.py`, `gerar_candidato_v410.py`, `gerar_relatorio_v410.py`, `guarda_frases_v410.py`, `pos_rito/textos_v410.py`, `registros_h0dn_v410.py` |
| OBS-16 | a forma canônica do Clay citada sozinha | 4 | 134, 174, 190, 191 | `gerar_relatorio_v410.py`, `pos_rito/textos_custodia_handoff_v410.py` |
| OBS-17 | o README leva o Clay em PT e EN e a D81 só em PT | 4 | 134, 174, 190, 191 | `gerar_relatorio_v410.py`, `pos_rito/textos_custodia_handoff_v410.py` |
| R3-MEDIO | a R3: a ratificação do quarto nome sem apoio no ADENDO 6 | 38 | 56, 58, 59, 82, 95, 96, 98, 100, 101, 102, 103, 109, 110, 119, 129, 130, 132, 151, 171, 173, 195, 207, 215, 219, 231, 232, 234, 236, 237, 248, 251, 260, 265, 266, 267, 268, 269, 272 | `delta_v410.py`, `gerar_candidato_v410.py`, `gerar_relatorio_v410.py`, `pedra/AEscala.lean`, `pos_rito/registrar_mapa_v410.py`, `pos_rito/textos_v410.py`, `registros_aescala_v410.py`, `registros_v410.py`, `runtime_aescala_v410.py` |
| R3-BAIXO-1 | a R3: rotular a identidade aritmética; a cláusula vale para todo b | 2 | 84, 87 | `delta_v410.py` |
| R3-BAIXO-2 | a R3: “no kernel.);” no artigo | 2 | 10, 34 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip` |
| D108 | a decisão do operador de 10/11, 15:54: o quarto nome e “o observador é a escala” | 28 | 3, 17, 27, 40, 50, 61, 63, 64, 65, 66, 82, 89, 90, 94, 103, 148, 177, 192, 200, 214, 216, 217, 218, 229, 235, 262, 263, 271 | `artigo_en_aescala_v410.pysnip`, `artigo_pt_aescala_v410.pysnip`, `conferir_rito_v410.py`, `delta_v410.py`, `guarda_frases_v410.py`, `pos_rito/textos_custodia_handoff_v410.py`, `pos_rito/textos_v410.py`, `registros_aescala_v410.py`, `runtime_aescala_v410.py` |

Todo achado da lista da ordem tem item. O que ficou só em parte, ou de fora, está na seção 9, com o motivo.

## 2. Como aplicar

- Cada item do tipo TROCA_EXATA troca trecho_atual por trecho_novo no arquivo indicado, o número de vezes do campo ocorrencias (1, salvo quando dito; onde é mais de 1, trocam-se TODAS). O trecho atual foi conferido contra o arquivo de hoje (o candidato revisado é 8a713e5e644af09b): existe exatamente esse número de vezes.
- Os itens de um mesmo arquivo não se sobrepõem e podem ser aplicados em qualquer ordem; a ordem da lista é a do arquivo (de cima para baixo). Aplicados todos em memória, os arquivos .py e .pysnip resultantes passam em ast.parse.
- As quebras de linha dos trechos estão em LF; ao aplicar, usar o fim de linha do arquivo (campo fim_de_linha, medido: delta_v410.py, ensaio_a_seco_v410.py e pos_rito/textos_v410.py são LF; pos_rito/textos_custodia_handoff_v410.py, copiar_insumos_v410.py e pos_rito/registrar_mapa_v410.py são CRLF; gerar_relatorio_v410.py é misto: manter o da linha tocada).
- Os itens do tipo INSTRUCAO não são troca exata: dependem de insumo que ainda não existe (o recibo da R6, o recibo dos nomes) ou de escolha do construtor; o critério está no próprio item.
- As formas ratificadas não mudam uma letra: a forma (a) do P = nP de Turing (FRASE_D81), a forma canônica do Clay (D84), a frase do tempo (D94), a cláusula do limite (D99) e a cláusula do Tetelestai e de 1 − β (D100) entram só por constante do delta, nunca digitadas; as frases novas vão AO LADO.
- Aspas angulares só em fala congelada: todos os trechos novos entre « » foram conferidos por script contra os arquivos OPERADOR_*.txt; a fala 29 foi copiada do arquivo, não digitada.
- Depois de aplicar: pedra R6 (autor), kernel refeito, ADENDO 7 e recibos; regenerar as saídas (lista na seção própria); rodar as guardas e os testes sem candidato do pós-rito ANTES do rito.

## 3. Pendências para a gerência

1. ESCOPO (o mais importante): esta ESPEC foi fechada no escopo da ordem do crítico (D106 a D108; fala 29; 29 falas congeladas, treze na pedra). No disco há decisões posteriores da própria gerência que mexem nesse escopo: D109 (16:04; a fala 30 ratifica a leitura da D108; “30 falas, quatorze na pedra”; emenda a D107), D112 e D113 (16:25 e 16:30; a constante da luz ENTRA na v410 como seção 7 nova da pedra R6, com teoremas novos e nomes a ratificar), D114 (16:33; ORDEM KIMI H0DN-03B conferida) e a fala das 16:44 (OPERADOR_10nov_tudo_depende_da_escala…, sha256 d7004a035f0586f7…), sem decisão registrada que eu tenha achado. Decidir, antes da ordem ao construtor, quais falas entram congeladas; o bloco condicional traz as variantes dos lugares digitados (itens 53, 62, 64, 128, 131, 153, 200, 229 e 103, 104, 105, 111, 145) e a lista do que falta redigir.
2. D113 contra frases desta ESPEC: se a seção 7 (a constante da escala) entrar na pedra R6, deixam de ser verdade (a) “nenhum teorema novo entra na v410 por esta fala, e a formalização própria fica [OPEN]” (FRASE_FINURA_ESPELHOS_PT/EN e _D108_PARTE_2, item 94; repetida na D108, item 103); (b) “muda SÓ o identificador … nenhum enunciado e nenhuma prova mudam” (cabeçalho da pedra, item 152; a D107, que diz que a R6 “so' muda comentarios e … o identificador”); (c) o assert de 2 pendentes e o token TWO_AUXILIARY_NAMES (itens 68 e 59), se os nomes da seção 7 ficarem [DECLARADO]; (d) “para a estrutura LeitorDoFundo” na frase das bandeiras (itens 28, 4 e 228), se a seção trouxer outra estrutura. A frase de limite da finura fecha sem a constante da luz, e o operador disse depois que é ela que falta: pela regra do posto, ler a ele o destino da frase antes de selar.
3. ADENDO 7 (não existe em disco; sem ele o delta consertado não carrega): tem de trazer (a) a fala 29 no formato do ADENDO 6: “verbatim sha256 `77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4`; arquivo `work\cunhagens_13out\OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt`” e a frase “a 29ª congelada”; (b) “`revisao_terceiro\REVISAO_TERCEIRO_v410.json` sha16 `8184102c73a34fe6`; pedido de correção sha16 `7e262affa4010036`; candidato revisado `8a713e5e644af09b`” (o formato do ADENDO 4; a conferência do conserto vai regravar esse JSON: o sha16 fica no adendo); (c) o sha16 do resultado do painel entre crases (`1ccebc2577babd64`, de PAINEL_R3_v410_RESULTADO.json); (d) “`work\h0dn_bg1_v410_09nov\ORDEM_KIMI_H0DN_03_10nov.md`, sha256 `17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f`” (o formato do ADENDO 3). Os hashes acima foram lidos por script pelos redatores e céticos e, o da revisão e o do pedido, de novo nesta consolidação; a gerência os confere ao escrever. O nome do arquivo do adendo (DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md) é suposição dos redatores.
4. Os recibos da R6: o delta consertado lê do recibo dos nomes a chave nova nomeados_pelo_operador_D108 e ratificados_D101 com 21 nomes, e precisa de um recibo do autor da R6 (as listas dos teoremas com o identificador novo, o quarto na última posição, e o sha256 da pedra instalada). Os nomes das chaves são do autor e do instalador (as duas instruções: itens 149 e 57).
5. [ONTO] e a regra de 04/11 (provar ou podar): a letra da D106 (“é leitura do operador [ONTO]”) reprova na regra F29 da guarda; os itens do g3 escrevem “é do operador [ONTO]”, que passa por redação (itens 120, 124, 29, 35, 223 e pares). Cabe à gerência dizer se marcar essas identificações como [ONTO] contraria a regra que a F29 guarda; precedente de uso: as docstrings da pedra (l.243, 256, 870, 977, 992) e o artigo (l.48).
6. «o que sou» (PAR-11): o item do g5:22 NÃO foi levado. O trecho é fala congelada letra por letra e a decisão do delta (linha 888, h) o guarda entre aspas angulares; são 13 ocorrências (a linha do .md; delta 184, 522, 540, 805, 853, 888; registros_v410.py 183, 197; runtime_v410.py 149, 150, 252, 253). Escolher: (A) ficam as 13; (B) trocam-se as 13 por aspas tipográficas e escreve-se ao lado da 888(h) que a decisão mudou.
7. A extensão do PAR-09 (itens 1, 13, 14, 22, 25, 36, 37, 46, 117): o expoente de e e o “n ln 2” não estão entre as três fórmulas que o painel citou; entraram porque uma delas é a fórmula da cláusula do limite (D99), que o TXT rendia “e^-s· c(x)” (a constante não muda; só o LaTeX). Se a gerência vetar, saem esses itens juntos; as fórmulas novas do g3 nos artigos já vão com o expoente entre parênteses e podem ficar.
8. H0DN, a ordem vigente: a frase do retorno (itens 73 e 74) nomeia a ORDEM KIMI H0DN-03 (06:26), que fica pinada por sha256. Depois dela a gerência conferiu a ORDEM 03B (D114, 16:33; sha256 c2b45aa48711f97ed336f74acd7cbd7ef5ec17062d3d22f74895f5c6a68fb7c5; não executada). A frase continua verdadeira; decidir se ela cita a 03B (e se a 03B vira pino no lugar da 03 ou ao lado).
9. A errata dos demais consertos: a E38 só cobre a contagem dos nomes e o quarto nome. A E36 muda de redação antes do selo (itens 107 e 108), os textos do H0DN ganham o retorno e o alcance, e as leituras ganham [ONTO]: ninguém redigiu o “dizia / lê-se” disso. Decidir se a E38 ganha um parágrafo ou se nasce outra errata (e, no H0DN, se há decisão nova: mudariam decisoes e erratas do contrato do H0DN e o controle da última decisão).
10. A pedra R6 é do autor: além dos itens da seção da pedra, há frases do mesmo tipo fora deles, que a R6 pode acompanhar ou não: l.1030 (“A hipótese s ≥ 0 é necessária”, em a_flutuacao_do_fundo_e_cotada, sem teorema de necessidade), l.1047-1048 e l.1130-1131; l.856-858 (o título “EM n OITAVAS O FUNDO PESA UM PIXEL” e “é a escala em que … separa o Nome do fundo”, que o enunciado não entrega) e l.899-900 (“a partir do qual UMA leitura de Z separa”, a fronteira frouxa); l.14 (a lista das decisões da abertura não ganha D106 a D108); l.15 («A Escala» entre aspas angulares como palavras do operador: o mesmo achado do PAR-11); l.602 (a forma da D83 sem o rótulo novo).
11. O rótulo curto “o teorema do Tetelestai” para os_passos_sao_o_ciclo_ate_o_tetelestai segue em runtime_aescala_v410.py:210 (descrição da c8), registros_v410.py:281 (E35, “dizia”), gerar_relatorio_v410.py:149 e :165 e em comentários e mensagens (delta 938, 942; registros_aescala 11; conferir_rito 434, 531; ensaio 2873; pos_rito/textos_v410.py 1346; textos_custodia_handoff 124, 212, 213; leitura_v410 790, 808). Pela E36 a cláusula do Tetelestai é a de 1 − β: decidir se o rótulo curto fica.
12. Duas ressalvas matemáticas que a D106 não pediu e que ficaram de fora dos textos: (EP-07, V2) para b ≥ ½ o fator √(b/(1 − b)) é ≥ 1 e a cota da reconstrução não informa (“fica perto do Nome” entra sem essa ressalva, itens 89 e 90); (EP-04) o limiar n·ln 2 + ln((1 − β)/β) é só SUFICIENTE (o kernel não diz que o reconhecimento ocorre nesse tempo nem que não ocorre antes).
13. PAR-08 fora da v410: os textos novos ficam com “creditation” (item 188), mas o README pinado e o portão do G1 (tools\custodia_g1\textos.py:22, :239, :303; readme_pinado.py:127-174) e seções seladas do artigo EN usam “accreditation”: o handoff EN sai com as duas palavras. E as etiquetas “[DECLARADO by the authorship …]” e “[PILOTO][SIM]” seguem em português no EN (são etiquetas da régua).
14. Observações 16 e 17 fora do README: a forma canônica do Clay segue sem a frase do habitante único no post (pos_rito/gerar_x_custodia_v410.py:78), nos ARCO PT e EN (textos_custodia_handoff_v410.py:180 e :185) e em pos_rito/textos_v410.py:912 e :1388 (nestes dois o Clay vai em PT e EN e a D81 só em PT). Se a regra for ao ARCO_EN, a frase EN do habitante único tem apóstrofo e a guarda do ARCO recusa aspa simples. E o handoff (ESCALA_TIPO_PT/EN) segue dizendo “existe, é único e é a IALD” sem a frase (V4): a D106 só a mandou à linha do .md e ao post.
15. H0DN, textos que seguem sem o retorno ou sem a forma da D96: o parágrafo curto do README e do site (pos_rito/textos_v410.py:915: ganhou só o alcance); :527, :657 e :1469; gerar_relatorio_v410.py:307 e :309; as chaves poder_certificado_pt/en do README evidente; o COMMIT (textos_custodia_handoff_v410.py:191); e conferir_rito_v410.py:452 e :533 não exigem o retorno nem o alcance na seção do artigo.
16. A fala 29: a leitura dita de volta ao operador (e ratificada por ele na fala 30) citava a segunda linha só até “frequencia.”; a ESPEC cita a linha inteira, com a frase sobre Einstein, que não foi lida de volta a ele. A tradução da fala para o EN (“our translation”) e “the resurrection of the signal” são da casa.
17. O que ninguém rodou: a guarda das frases, a P18 e o portão do G1 de verdade, os testes sem candidato do pós-rito, o LaTeX dos artigos e o ensaio. Nesta consolidação os 267 itens exatos foram aplicados EM MEMÓRIA (cada trecho atual existe o número certo de vezes, sem sobreposição; os arquivos .py e .pysnip resultantes passam em ast.parse) e os textos principais, rendidos com valores de ensaio, passaram numa cópia de leitura da guarda (as funções puras extraídas pelos redatores). Os 50 itens redigidos pelo crítico (os que juntam grupos ou tornam exato o que estava em prosa; entre eles o código da c5, da c8 e da c11) não passaram por cético: itens 12, 14, 37, 56, 57, 58, 59, 61, 63, 64, 65, 66, 82, 94, 99, 103, 105, 111, 117, 130, 131, 133, 140, 141, 145, 148, 150, 168, 171, 173, 194, 200, 214, 215, 217, 225, 229, 236, 238, 247, 261, 262, 263, 264, 266, 267, 268, 269, 271, 274.
18. Menores: (a) o sufixo do veredito do registro (item 68) é longo; há forma mais curta nos efeitos do item; (b) ASSINA (delta l.1071) diz “06 e 09/11/2026” e as erratas E33 a E38 são de 10/11; (c) FRASE_D64_PT segue sem “(validade no kernel, não creditação)”, que a EN tem (PAR-05: a D106 só pediu o artigo e o post); (d) a política do FLAGS (“so' declaracao NOMEADA tem bandeira”), por_origem “aescala_nomeada: 85” e a lista de 17 constantes (gerar_candidato_v410.py:550) contam outra história que a frase nova das bandeiras; (e) D102 a D105 foram postas fora do um.py por leitura dos pedidos ACOM; (f) a D107 entra no rótulo da linha da Escala e nas decisões do registro, embora seja de processo.
19. Mapa de Rotas e memória ACOM: este crítico consultou o estado em disco e não registrou nada (a escrita foi limitada à pasta do conserto; sem referência própria na memória ACOM). O registro da rota fica com a gerência.

## 4. O RENOMEAR: `a_informacao_completa_se_reconstroi` passa a `ressurreicao_do_sinal`

Decisão do operador de última hora (D108, fala 29 de 10/11, 15:54): «o quarto nome=ressureiçãodosinal». O identificador segue a ortografia do dicionário; a grafia dele fica no verbatim. Em prosa: “a ressurreição do sinal”. Enunciado e prova não mudam.

**Regra:** nenhum trecho novo traz o identificador velho, salvo frase de registro que o diga nome de trabalho da gerência (D106, D108, E38, a entrada da E38 no registro das cunhagens, o cabeçalho e a docstring da pedra, a constante NOME_DE_TRABALHO_DO_QUARTO_AESCALA e a chave nome_de_trabalho_do_quarto do contrato, que a c11 usa como controle negativo); enunciado e prova do teorema não mudam.

**Fontes que trazem o identificador velho hoje** (conferido por busca; o resto lê do delta):

| Arquivo | Linhas | Ocorrências |
|---|---|---|
| `delta_v410.py` | 1013, 1015, 1026 | 4 |
| `runtime_aescala_v410.py` | 28 | 1 |
| `pedra/AEscala.lean` | 38, 132, 1169 | 3 |
| `insumos/AEscala.lean` | 38, 132, 1169, 1412 | 4 |
| `pedra/origem/AEscala.lean` | 38, 132, 1169, 1412 | 4 |
| `insumos/AEscala_embutida.lean` | 38, 132, 1169 | 3 |

- `pedra/AEscala.lean` (a instalada) e `insumos/AEscala.lean` (a fonte do autor): a fonte tem uma ocorrência a mais, na seção Auditoria (`#print axioms`), que a instalada não traz. `pedra/origem/AEscala.lean` e `insumos/AEscala_embutida.lean` são registro de origem e saída regerada.
- **Itens que tiram o identificador velho:** 89, 90, 93, 151, 155, 159, 255.
- **Itens de registro que o citam como nome de trabalho (permitido):** 55, 103, 110, 149, 150, 151, 157, 219.
- **O título velho usado como nome** (“a informação completa se reconstrói”): `delta_v410.py` l.1013; `pedra/AEscala.lean` l.1163. As demais ocorrências de “reconstrução” são a conta da c13 e a prova de reconstrução do selo ACOM: não são o nome e ficam.
- **Quem lê do delta:** registros_aescala_v410.py, registros_v410.py, os .pysnip dos artigos, gerar_candidato_v410.py, gerar_relatorio_v410.py, gerar_esperados_v410.py, runtime_v410.py, ensaio_a_seco_v410.py, conferir_rito_v410.py e pos_rito/*.py não digitam o identificador (conferido por busca nesta consolidação: só as fontes listadas acima o trazem).
- **Saídas que regeram sozinhas (não editar):** um_v410_candidato.py; v410_pins.py; DIFF_v409_v410.diff; CANDIDATO_v410.json; ESPERADOS_v410.json; GUARDA_FRASES_v410.json; PREPARACAO_v410_PRONTA.json; BUNDLE_v410.json (raiz e insumos); insumos/AEscala_embutida.lean; insumos/RECIBO_PEDRAS_v410_NOMES.json (pelo instalador da R6); kernel/FLAGS_v410.json, KERNEL_RECIBO, POS_BUILD e os logs; ensaio_a_seco_v410.json; EXAME_PONTOS_*.json; dry_v410/, dry_pre410/, falso_nos/, imp_*/, sim_*/, conferidor_import_*/, arvore_simulada_h8/; pos_rito/CUSTODIA_v410_RASCUNHO.txt.
- **Registros de época, que ficam:** insumos/RECIBO_AESCALA_R5_10nov.json e compile_log_AEscala_R5.txt; insumos/AEscala.lean e pedra/origem/AEscala.lean enquanto fonte da R5 (a R6 entra ao lado); _r2_gerar_instalador_r5_v410.py, _r2_instalar_pedra_r5_v410.py, _r5ag_02_delta_v410.py, _r5ag_05_runtime_aescala_v410.py (scripts de adaptação já aplicados); acom_c1_20261110_d102 e d108; PAINEL_R3_v410_RESULTADO.json; revisao_terceiro/* (a R3, o pedido, as sondas Lean); um_v410_candidato.trabalho_r5ag_*.py; os ADENDOS 1 a 6 (não trazem o identificador).

## 5. A pedra Lean (comentários e um identificador; exige recompilar o kernel)

Itens 150, 151, 152, 153, 154, 155, 156, 157, 158, 159. Mudam o cabeçalho (a ratificação; a seção Auditoria; a linha da R6), a lista das falas (a fala 13 da pedra), a tabela, duas docstrings (a do quarto teorema e a frase da necessidade em `o_tetelestai_e_um_menos_beta`) e UM identificador. Nenhum enunciado e nenhuma prova mudam por estes itens. A pedra muda de sha256: a R6 é do autor; o kernel é refeito; recibo do autor, recibo dos nomes, BUNDLE, FLAGS, KERNEL_RECIBO, POS_BUILD, pinos e ESPERADOS são regerados. A seção 7 da D113 (a constante da escala) NÃO está nesta ESPEC.

| Item | Linha | O quê | Achados |
|---|---|---|---|
| 150 | 1 | as cópias da pedra e a fonte do autor (a R6 é do autor; o construtor instala) | EP-01, EP-12, V1 |
| 151 | 37 | cabecalho, linhas 37-39 (a frase da ratificacao da R5) | EP-01, R3-MEDIO |
| 152 | 42 | cabecalho, linhas 42-43 (a compilacao e a frase da secao Auditoria) + a linha nova da R6 | EP-12 |
| 153 | 45 | linha 45 (titulo da lista das falas) | EP-01 |
| 154 | 109 | depois da linha 110 (fim da fala 12): a fala 13, no formato das vizinhas | EP-01 |
| 155 | 132 | linha 132 (tabela fala -> termos) | EP-01 |
| 156 | 1062 | docstring de o_tetelestai_e_um_menos_beta, l.1062-1063 (só a frase da necessidade) | V1 |
| 157 | 1163 | linha 1163 (abertura da docstring do teorema renomeado) | EP-01 |
| 158 | 1168 | linha 1168 (fim da docstring do teorema renomeado) | EP-01, V2 |
| 159 | 1169 | linha 1169 (o identificador do teorema) | EP-01 |

## 6. Conflitos resolvidos

- A fala 29 no delta (linhas 485 e 497): g1:13 e g6:1/g6:2 usavam as mesmas âncoras e criavam duas constantes quase homônimas para a segunda linha da fala. Fica UMA (FRASE_OBSERVADOR_E_A_ESCALA, a linha inteira) mais FRASE_O_QUARTO_NOME; a constante curta do g1 saiu. Itens 65, 66.
- DECISOES[“D108”]: o g1 (item 24) e o g6 (item 6) redigiam a mesma entrada na mesma âncora. Vira UM item (103): (1) o quarto nome; (2) a finura da leitura, pela constante _D108_PARTE_2, definida no bloco da finura ANTES do DECISOES.update (item 94). A D108 não concatena mais FRASE_RECONSTROI_PT sozinha (quebrava a c8).
- FRASE_RECONSTROI_PT/EN (delta, linhas 1013-1016): g1:14/15 mudavam a abertura e g2:32/33 a constante inteira. Fica a constante do g2 com “o nome é do operador, D108” (itens 89 e 90); o assert da linha 1026 é o do g1:16 (item 93).
- O rótulo da frase da E36 no artigo EN (linha 43): g3:16 escrevia “INPUT/dicionário” e g5:12 trocava por “INPUT/dictionary”. Fica o texto do g3 com a palavra do g5 (item 15); a linha 37 tem item próprio com contexto (12, 15).
- O ADENDO 7 no delta: g1 (item 12, em prosa) e g4 (item 3) definiam ADENDO7_ARQ e _ADENDO7_TXT cada um. Ficam definidos UMA vez (item 63) e usados pelo bloco da fala 29 e pelo pino da ORDEM KIMI H0DN-03.
- As fórmulas novas do g3 nos artigos (e^(−t·c(x)), e^(−s·c(x)), e^(−s·k)) colidiam com a regra da extensão do PAR-09 (g5:7): vão já com o expoente entre parênteses, para o TXT não render “e^-t· c(x)”.
- g6:3, g6:4 e g6:5 se ancoravam um no texto do outro (os dois últimos não existiam no arquivo): viram um bloco só, com âncora no arquivo de hoje (item 94).
- As contagens saem iguais em todo lugar: 21 ratificados pela fala 28 (D101), 1 nomeado pelo operador na fala 29 (D108), 3 campos, 2 auxiliares pendentes [DECLARADO pela autoria], 24 nomes novos, 29 falas congeladas (treze na pedra). Os números de nomes vêm de len(); os digitados (“tres”, “ONE”, “TWO”) ficam amarrados pelo assert do item 59.
- O rótulo “o limiar de um pixel, a decisão exata” sai com as mesmas palavras nos nove lugares (itens do g2:10 a g2:18); a frase da hipótese s ≥ 0 muda numa constante só (FRASE_TETELESTAI_PT/EN) e as cópias à mão (a E36 no delta e em registros_v410.py, a docstring da pedra) dizem o mesmo; o retorno do H0DN é uma constante (FRASE_H0DN_RETORNO_PT/EN) usada em todo lugar.
- Discordâncias com os céticos: nenhuma de conteúdo. Onde o cético deu a correção, ela entrou (g1:2, 24, 35; g2:19, 20, 23 a 26, 29, 30, 31; g3: os catorze trechos; g4:1, 2, 5, 6, 20, 29, 30; g5:25, 28; g6:3 a 6). No g1:2 tirei o marcador “[o autor escreve aqui o fato medido]” do texto; no g1:27 mantive o sufixo do redator (o cético deu ok e ofereceu um mais curto: está nos efeitos do item); os condicionais da D109 (g1:3, 12, 25, 59, 60) ficaram no escopo da ordem, com a variante no bloco condicional.

## 7. Bloco condicional: se a fala 30 (D109) for congelada na v410

A ordem deste crítico fixa 29 falas congeladas (treze na pedra) e as decisões D106 a D108. No disco, a gerência registrou depois a D109 (10/11, 16:04): a fala 30 do operador (16:02:58; «é isso mesmo, perfeito. ratificado. …»; sha256 7857d4ddf9d3cfc0b290836b3c0e1bcadf3a61031ee03ebb4688b824269cfdfd, 126 bytes) ratifica a leitura da D108, e o registro diz “falas congeladas: 30 (quatorze na pedra)”. Se a gerência congelar a fala 30 na v410, os lugares DIGITADOS abaixo mudam; o resto acompanha por len().

- Itens com a contagem de falas digitada: 53, 62, 64, 128, 131, 153, 200, 229.
- Itens com a lista de decisões digitada: 103, 104, 105, 111, 145.

**Item 153, variante:**

~~~~text
## As QUATORZE falas do operador (09 e 10/11/2026)
~~~~

**Item 61, 62, 63, 64, 82, 200, variante:**

~~~~text
N_MENTIRA_LIDA, N_TESTE_SEM_PODER, N_CLAUSULA_TETELESTAI, N_CONFIRMO_TUDO, N_QUARTO_NOME, N_RATIFICADO_SEM_LOOP)   # as falas desta versao: as de 06 a 09/11 e as SETE de 10/11 (D94, D96, D100, D101, D108 e D109), todas inteiras;   [N_RATIFICADO_SEM_LOOP é nome sugerido]
~~~~

**Item 104, 105, 111, 145, 247, variante:**

~~~~text
"D99", "D100", "D101", "D106", "D107", "D108", "D109")
DECISOES_FORA_DO_UMPY = ("D97", "D98", "D102", "D103", "D104", "D105")   [rótulo “D63 a D96, D99 a D101 e D106 a D109”; token “D63_TO_D96_D99_TO_D101_AND_D106_TO_D109”; o controle do ensaio passa a == "D109"; MD_ROTULO_ESCALA e o adendo no relatório passam a “D106 a D109”]
~~~~

**Item 128, variante:**

~~~~text
e as sete de 10/11, D94, D96, D100, D101, D108 e D109: os passos sao o ciclo ate' o Tetelestai com o leitor que e' a escala, a mentira lida como mentira, o teste sem poder preditivo, a clausula do Tetelestai, a ratificacao dos nomes, o quarto nome com o observador que e' a escala e a ratificacao dessa leitura;
~~~~

**Item 53, variante:**

~~~~text
as sete de 10/11 dos ADENDOS 2, 3, 5, 6 e 7, D94, D96, D100, D101, D108 e D109);
~~~~

**O que falta redigir e conferir se a fala 30 entrar:**

- o texto de DECISOES["D109"] (ninguém o redigiu nem conferiu)
- a constante N_ do arquivo da fala 30, a data, os trechos citados em FRASES_V410, o par em pos_rito/textos_v410.py (par_), N_FALA e _P_30, e a fala no ADENDO 7 (“a 30ª congelada”)
- a entrada 14 na lista das falas da pedra (formato das vizinhas) e a fala em NOMES_FALAS do registro a_escala_v410
- a enumeração das falas no estatuto do registro (item 53 e vizinhos) e as falas_novas do relatório
- a D107 e a D108 já citam a D109 (emenda e ratificação): se a D109 entrar no um.py, a tupla DECISOES_FORA_DO_UMPY volta a não tê-la

## 8. Os itens, por arquivo e por posição

### Arquivo `artigo_en_aescala_v410.pysnip`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\artigo_en_aescala_v410.pysnip`. Fim de linha: LF. Itens: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18.

#### Item 1 — linha 12 — PAR-09 — EXTENSÃO

- **Local:** EXTENSAO, a gerencia decide: linha 12 dos snippets da Escala (a tabela _zx410, que rende a CLAUSULA do limite, forma ratificada D99) e linha 28 dos snippets da IALD2 (Z(s) na primeira ocorrencia); rende nas linhas 115, 139 e 141 do TXT
- **Origem:** g5:7 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
e^{-s\cdot c(x)}
~~~~

Trecho novo:

~~~~text
e^{(-s\cdot c(x))}
~~~~

- **Justificativa:** Mesma classe das tres citadas e pega a forma ratificada: a clausula diz “Z(s) = Σ_x e^(−s·c(x))” e o TXT a rende “Z(s)=Σ_x e^-s· c(x)”, que lido ao pe' da letra e' e^(−s) vezes c(x). A constante da clausula NAO muda; muda so' a escrita LaTeX dela no snippet, e o TXT passa a render “e^(-s· c(x))”.
- **Apoio:** delta_v410.py:943-945 (CLAUSULA_Z_PT/EN, lidas do ADENDO 4; _FORMULA_Z = “Z(s) = Σ_x e^(−s·c(x))”); saida conferida na copia do conversor (testa_txt.py)
- **Decisão do crítico:** EXTENSÃO do PAR-09 (o painel citou três fórmulas; esta é da mesma classe): entra, porque a fórmula é a da cláusula do limite, forma ratificada (D99), que o TXT rendia “e^-s· c(x)”; a constante da cláusula NÃO muda, só a escrita LaTeX dela; a gerência pode vetar a extensão sem afetar os outros itens (pendências)
- **Efeitos colaterais:**
  - ensaio_a_seco_v410.py:3202 tem o literal r"\sum_x e^{-s\cdot c(x)}" num tex.replace (o controle negativo que tira a formula): TEM de acompanhar, virando r"\sum_x e^{(-s\cdot c(x))}"; senao o negativo deixa de tirar a formula e a checagem reprova
  - ensaio_a_seco_v410.py:3162 e conferir_rito_v410.py:438 comparam por DL.comparavel, que tira parenteses e chaves: passam sem mudanca
  - o grupo leituras_do_operador (itens 5, 7, 11 e 13) acrescenta formulas da mesma familia nos snippets da Escala: “$e^{-t\cdot c(x)}$”, “$e^{-s\cdot c(x)}$” e “$e^{-s\cdot k}$”. Renderiam “e^-t· c(x)” no TXT. Se esta extensao for aceita, a mesma escrita vale para elas: “e^{(-t\cdot c(x))}”, “e^{(-s\cdot c(x))}”, “e^{(-s\cdot k)}”; e a contagem deste item sobe nos dois snippets da Escala
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 2 — linha 16 — PAR-09

- **Local:** linha 16 dos dois snippets (a tabela de _mz410 que leva a frase Unicode do contrato a LaTeX); rende na linha 141 do TXT
- **Origem:** g5:2 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
r"$\sqrt{b/(1-b)}$"
~~~~

Trecho novo:

~~~~text
r"$\sqrt{(b/(1-b))}$"
~~~~

- **Justificativa:** A fonte (FRASE_RECONSTROI, Unicode) ja' traz os parenteses; quem os perde e' esta tabela: o conversor troca \sqrt por √ e depois tira as chaves, e o TXT sai “√b/(1-b)”. Com os parenteses dentro do radical o TXT rende “√(b/(1-b))”; no PDF o radical cobre a fracao entre parenteses.
- **Apoio:** pedra\AEscala.lean:1173 (Real.sqrt (b / (1 - b))); delta_v410.py:1013 e :1015 (FRASE_RECONSTROI_PT/EN: “√(b/(1 − b))”); um_v410_candidato.py:189684 (sqrt -> √) e :189766 (tira as chaves)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - DL.comparavel (delta_v410.py:763-770) tira parenteses e chaves dos dois lados: os controles que procuram a frase da reconstrucao na secao seguem passando sem mudanca
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 3 — linha 19 — D108, OBS-1

- **Local:** auxiliar novo _fn410, logo depois de _pm410 [o trecho atual comeca na linha 19 do arquivo, contada por script]
- **Origem:** g6:12 (g6_a_finura_e_o_observador). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
    _pm410 = lambda m_: _fl410(1.0 - m_) if isinstance(m_, float) else "n/a"
~~~~

Trecho novo:

~~~~text
    _pm410 = lambda m_: _fl410(1.0 - m_) if isinstance(m_, float) else "n/a"
    _fn410 = lambda t_: "".join((_zx410[p_] if p_ in _zx410 else _mz410(p_)) for p_ in re.split("(" + "|".join(re.escape(k_) for k_ in _zx410) + ")", t_)).replace("$$", "")   # (D108: a frase da finura em LaTeX: 2^n e n·ln 2 em modo matematico pelo _zx410, o resto pelo _mz410; o par de cifroes que sobrar na costura e' fundido)
~~~~

- **Justificativa:** A frase nova traz 2^n (que so' o _zl410 converte) e ≤, ≥, −, ·, ½, <, > e nomes entre crases (que so' o _mz410 converte): o auxiliar novo junta os dois, sem mudar os existentes.
- **Apoio:** artigo_en_aescala_v410.pysnip:12-18 (_zx410, _zl410 e _mz410). Simulado com copia dos auxiliares em _latex_sim.py: cifroes balanceados, nenhum ^ fora de modo matematico, nenhum caractere fora dos que o artigo ja' usa.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - A simulacao NAO e' o pdflatex: o ensaio a seco do artigo (PDF e TXT) e' quem confirma a renderizacao; o achado PAR-09 do painel mostra que o TXT perde agrupamentos em formulas com fracao, e por isso a frase nao usa \frac nem expoente composto.
  - O snippet ja' usa o modulo re (linhas 13 e 15): nada a importar.

#### Item 4 — linha 25 — EP-12

- **Local:** linha 25 (o par EN do item anterior)
- **Origem:** g5:24 (g5_forma_e_render). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
r" flags \texttt{ext\_aescala\_410\_*}; the stone by sha256 "
~~~~

Trecho novo:

~~~~text
r" flags \texttt{ext\_aescala\_410\_*} (composition: " + str(_ca410["n_nomes"] + _ca410["n_nomes_novos"]) + r" from declarations named in the stone, " + str(len(_ca410["campos_novos_da_estrutura"])) + r" from the fields of the structure \texttt{LeitorDoFundo} and " + str(_ca410["n_flags"] - _ca410["n_nomes"] - _ca410["n_nomes_novos"] - len(_ca410["campos_novos_da_estrutura"])) + r" from constants the compiler generates for the structure; all count in the ladder); the stone by sha256 "
~~~~

- **Justificativa:** O mesmo conteudo do PT, com as mesmas contas.
- **Apoio:** kernel\FLAGS_v410.json, contado por conta_bandeiras.py (nesta pasta): 85 bandeiras ext_aescala_410_* = 68 declaracoes nomeadas na pedra (59 theorem, 8 def, 1 structure) + 3 campos da estrutura (brilho, sem_escala_nao_ha_medida, a_lei_da_dissipacao) + 14 constantes geradas para a estrutura (mk, rec, recOn, casesOn, ctorIdx, noConfusion, noConfusionType, mk.inj, mk.injEq, mk.noConfusion, mk.sizeOf_spec, mk._flat_ctor, _sizeOf_1, _sizeOf_inst); insumos\RECIBO_PEDRAS_v410_NOMES.json: 44 nomes + 24 nomes novos = 68, 3 campos; registros_aescala_v410.py:46 (a escada esperada soma TODAS as bandeiras)
- **Decisão do crítico:** aceita a observação do cético: três das 14 constantes têm nome interno do Lean (_sizeOf_1, _sizeOf_inst, mk._flat_ctor); a decisão da gerência dizia só “constantes que o compilador gera para a estrutura”: sai o adjetivo, e a frase fica igual à do registro (item do g5:25) (par EN)
- **Efeitos colaterais:**
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 5 — linha 28 — PAR-03

- **Local:** l.28, paragraph “The insignia, the vibrato, finite time and the two Names.”
- **Origem:** g3:11 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
dissipation sustains the note, and the note is the modular conjugation;
~~~~

Trecho novo:

~~~~text
given a zero-cost pixel, the decay generated by the cost, $e^{(-t\cdot c(x))}$, does not touch what has zero cost and does not bring the uniform state to zero, and the performed reading (the average, over the pixels, of the weights $e^{(-s\cdot c(x))}$) never falls below the fraction of zero-cost pixels, does not increase with time and tends to it (\texttt{o\_vibrato\_sustenta\_a\_nota}); on the paired space of the kernel, $J^2=1$ and $JKJ=-K$ (\texttt{a\_nota\_e\_a\_conjugacao\_modular}); the identification of that decay with the vibrato and of the note with $J$ is the operator's \textsf{[ONTO]};
~~~~

- **Justificativa:** Par do item PT: as mesmas hipóteses, os mesmos dois termos e a mesma marca [ONTO].
- **Apoio:** pedra/AEscala.lean:244-250 (o_vibrato_sustenta_a_nota, hipotese h: existe x com c x = 0: (1) a trava nao toca o custo zero; (2) trava c t (uniforme X) != 0; (3) card{c = 0}/|X| <= leituraPerformada c s; (4) Antitone; (5) Tendsto para card{c = 0}/|X|); leituraPerformada = particao/|X|: TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):920; trava = e^(-t c(x)) por pixel: TraducaoTuring.lean:472-477 (mesma copia); docstring l.242-243 ([ONTO]) | pedra/AEscala.lean:257-258 (a_nota_e_a_conjugacao_modular: conjJ (conjJ p) = p e conjJ (pairK d (conjJ p)) = -pairK d p, isto e', J^2 = 1 e JKJ = -K); docstring l.256 (a identificacao nota = J e' do operador, ONTO)
- **Decisão do crítico:** fico com a correção do cético: “disso” vinha logo depois de J² = 1 e JKJ = −K e a leitura mais próxima atribuía o vibrato às identidades de J; a docstring (AEscala.lean:242-243) liga o vibrato ao decaimento: “desse decaimento” (par EN); (crítico) as fórmulas novas com expoente vão na escrita da extensão do PAR-09 (o expoente entre parênteses), para o TXT do artigo não render “e^-t· c(x)”
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)
  - ensaio_a_seco_v410.py:3153-3163 e conferir_rito_v410.py:435-438 (r2: clausula ao lado do teorema, Z(s) definida na primeira ocorrencia, unicode cru) e :442-449 (r5): conferidos por leitura; os titulos em negrito da lista DA410/DA410E (ensaio l.3122-3123) nao mudam
  - dry_v410/dry_v410_pt.txt e dry_v410_en.txt, o candidato e os ESPERADOS sao regenerados pelo construtor

#### Item 6 — linha 30 — EP-10

- **Local:** l.30, paragraph “The Clay question in the TGL dictionary.”
- **Origem:** g3:12 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
\textsf{[REAL]} The mandatory form: 
~~~~

Trecho novo:

~~~~text
\textsf{[REAL the validity in the kernel; INPUT the operator's reading]} The mandatory form: 
~~~~

- **Justificativa:** Par do item PT: o mesmo rótulo da forma da D83, com as palavras que a própria forma EN usa (“validity in the kernel”).
- **Apoio:** pedra/AEscala.lean:598-604 (a forma da D83 e' a leitura do operador, fala 6; validade no kernel; a creditacao e' do Clay) e :778-779 (a_pergunta_do_clay_tem_resposta: a validade)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)

#### Item 7 — linha 34 — EP-05

- **Local:** l.34, list “The THEOREMS of the kernel, in the trio”
- **Origem:** g3:13 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
the reader is the scale, any two background readers are the same (\texttt{o\_leitor\_e\_a\_escala});
~~~~

Trecho novo:

~~~~text
any two background readers are the same and, in every background reader, the pixel of cost $k$ has brightness $e^{(-s\cdot k)}$ at time $s$ (\texttt{o\_leitor\_e\_a\_escala});
~~~~

- **Justificativa:** Par do item PT: a frase fica só como nome; vai o conteúdo do enunciado.
- **Apoio:** pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** o conteúdo fica como o redator propôs (ok do cético); (crítico) as fórmulas novas com expoente vão na escrita da extensão do PAR-09 (o expoente entre parênteses), para o TXT do artigo não render “e^-t· c(x)”
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)

#### Item 8 — linha 35 — EP-08

- **Local:** parágrafo “The scale in the type…”, l.35
- **Origem:** g2:37 (g2_tetelestai_e_limiar). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
half per octave and, in $n$ octaves, the background weighs one pixel; each cycle
~~~~

Trecho novo:

~~~~text
half per octave and, in $n$ octaves, the brightness of a pixel of cost 1 is $1/2^n$, the weight of one pixel in the reading (\texttt{em\_n\_oitavas\_o\_fundo\_pesa\_um\_pixel}; that the whole background weighs less than one pixel of the Name, past that time, comes from the threshold theorem, next); each cycle
~~~~

- **Justificativa:** Par EN do item 36; “brightness” é a palavra do próprio artigo EN (l.40).
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - os mesmos do item 36

#### Item 9 — linha 35 — EP-03

- **Local:** parágrafo “The scale in the type…”, l.35
- **Origem:** g2:12 (g2_tetelestai_e_limiar). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
the threshold of the Tetelestai (\texttt{os\_passos\_sao\_o\_ciclo\_ate\_o\_tetelestai}): "
~~~~

Trecho novo:

~~~~text
the one-pixel threshold, the exact decision (\texttt{os\_passos\_sao\_o\_ciclo\_ate\_o\_tetelestai}): "
~~~~

- **Justificativa:** Par EN do item 11; “the one-pixel threshold … the exact decision” é o vocabulário da FRASE_E36_EN.
- **Apoio:** pedra\AEscala.lean:897-898 (docstring: “o limiar de um pixel … é a DECISÃO exata, formalização da gerência; a CLÁUSULA DO TETELESTAI … é a `o_tetelestai_e_um_menos_beta`”); delta_v410.py:1092-1093 (E36); pedra\AEscala.lean:903-909 (o enunciado só traz desigualdades sobre Z(s))
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - os mesmos do item 11

#### Item 10 — linha 36 — R3-BAIXO-2

- **Local:** l.36 (the limit clause inside parentheses)
- **Origem:** g3:14 (g3_leituras_onto). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
linear in the bits (" + _zl410(_ca410["clausula_z_en"]) + r"); that the steps are
~~~~

Trecho novo:

~~~~text
linear in the bits. " + _zl410(_ca410["clausula_z_en"]) + r" That the steps are
~~~~

- **Justificativa:** A R3 aponta o PT; o EN renderiza o mesmo “in the kernel.);” (dry_v410_en.txt l.139). Mesmo conserto, pela regra do par PT/EN: a cláusula EN (D99) fica como frase própria, byte a byte.
- **Apoio:** delta_v410.py:943 (CLAUSULA_Z_EN; nao muda); artigo_en_aescala_v410.pysnip:42 (o mesmo molde)
- **Decisão do crítico:** entra, embora a letra da D106 (item 6) diga só o artigo PT: o EN rende o mesmo “in the kernel.);” e a régua manda redigir o par com a mesma forma (o cético deu ok ao trecho)
- **Efeitos colaterais:**
  - ensaio_a_seco_v410.py:3160-3161 e conferir_rito_v410.py:436-437: “linear in the bits” seguido da clausula EXATA em ate' 1400 caracteres; segue passando
  - dry_v410/dry_v410_pt.txt e dry_v410_en.txt, o candidato e os ESPERADOS sao regenerados pelo construtor

#### Item 11 — linha 36 — EP-05

- **Local:** l.36, end of the list of theorems
- **Origem:** g3:15 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
\textsf{[INPUT]}; a lie read as a lie is truth (\texttt{a\_mentira\_lida\_como\_mentira\_e\_verdade}); the Father of Lies only does not recognize (\texttt{o\_pai\_da\_mentira\_so\_nao\_reconhece}). "
~~~~

Trecho novo:

~~~~text
\textsf{[INPUT]}. \textsf{[REAL]} For every background reader, the limit of the reading in time is the number of solutions divided by the number of pixels and is 0 when there is no solution (\texttt{a\_mentira\_lida\_como\_mentira\_e\_verdade}); at $s=0$ the reading is 1 on every instance and coincides with that quotient only on the instance in which every pixel is a solution (\texttt{o\_pai\_da\_mentira\_so\_nao\_reconhece}); the reading that these two names and \texttt{o\_leitor\_e\_a\_escala} carry (that there is no reader that is not the observer of the light; that nothing escapes the Name; the theological reading of the Father of Lies) is the operator's \textsf{[ONTO]}. "
~~~~

- **Justificativa:** Par do item PT: o conteúdo dos dois termos, as frases só como nomes, a marca [ONTO] nos três nomes.
- **Apoio:** pedra/AEscala.lean:978-980 (a_mentira_lida_como_mentira_e_verdade: L.limite c = oQueSou (nomeDasSolucoes c) e, sem solucao, L.limite c = 0 e oQueSou = 0); o que sou do Nome das solucoes = numero de solucoes / numero de pixels (|X|): TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):805-807 (o_que_sou_das_solucoes, v409); docstring l.976-977 ([ONTO]) | pedra/AEscala.lean:993-998 (o_pai_da_mentira_so_nao_reconhece: L.leitura c 0 = 1; = euSou X; coincide com oQueSou (nomeDasSolucoes c) se e so' se para todo x, c x = 0; sem solucao le 1 onde o que sou e' 0); docstring l.992 ([ONTO])
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)

#### Item 12 — linha 37 — PAR-08 — redigido pelo crítico

- **Local:** linha 37 (o rótulo do tempo no artigo EN)
- **Origem:** g5:12, critico (g5_forma_e_render). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
\textbf{Time.} \textsf{[INPUT/dicionário]} 
~~~~

Trecho novo:

~~~~text
\textbf{Time.} \textsf{[INPUT/dictionary]} 
~~~~

- **Justificativa:** O artigo EN levava o rótulo em português na costura do tempo; fica o mesmo rótulo do handoff EN. O trecho leva o contexto (“Time.”) para ser único no arquivo em qualquer ordem de aplicação.
- **Apoio:** g5 item 12; pos_rito\textos_custodia_handoff_v410.py:128
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - depende dos itens do g5:13, 14 e 15 (senão o ensaio e o conferidor reprovam a seção EN)

#### Item 13 — linha 38 — PAR-09 — EXTENSÃO

- **Local:** EXTENSAO, a gerencia decide: linhas 38 e 44 dos dois snippets da Escala; rende nas linhas 139 e 141 do TXT como “nln 2”
- **Origem:** g5:8 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 2

Trecho atual:

~~~~text
n\ln 2+
~~~~

Trecho novo:

~~~~text
n\,\ln 2+
~~~~

- **Justificativa:** O conversor escreve “ln” colado no n: “s^*=nln 2+”. Com o espaco fino o TXT rende “n ln 2” e o PDF nao muda de sentido.
- **Apoio:** um_v410_candidato.py:189668 (o espaco fino vira U+2009 no TXT) e :189744-189746 (\ln -> ln); saida conferida em testa_txt.py
- **Decisão do crítico:** EXTENSÃO do PAR-09 (mesma classe: “nln 2” no TXT); entra com o item da linha 40, que o redator deixou nos efeitos colaterais
- **Efeitos colaterais:**
  - na linha 40 dos mesmos snippets ha' “$n\ln2$” (sem espaco): passa a “$n\,\ln 2$” (1 ocorrencia em cada arquivo)
  - nenhum controle procura “n\ln” (Grep: 0)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 14 — linha 40 — PAR-09 — EXTENSÃO; redigido pelo crítico

- **Local:** linha 40 (a mesma fórmula, sem espaço)
- **Origem:** g5:8, critico (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
$n\ln2$
~~~~

Trecho novo:

~~~~text
$n\,\ln 2$
~~~~

- **Justificativa:** A mesma escrita do item do g5:8 na linha 40.
- **Apoio:** g5 item 8 (efeito) e a conferência do g5, item 8
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 15 — linha 43 — EP-10, PAR-08

- **Local:** l.43, paragraph “The clause of the Tetelestai (R5, D100).”
- **Origem:** g3:16, g5:12 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
r"\textsf{[INPUT/dicionário]} " + _mz410(_ca410["frase_e36_en"])
~~~~

Trecho novo:

~~~~text
r"\textsf{[REAL the one-pixel threshold; INPUT/dictionary the operator's reading]} " + _mz410(_ca410["frase_e36_en"])
~~~~

- **Justificativa:** Par do item PT. O artigo EN escreve o rótulo do dicionário como o PT (“INPUT/dicionário”, a constante ROTULO_TEMPO, l.37 do mesmo snippet); o trecho novo conserva essa grafia.
- **Apoio:** registros_aescala_v410.py:115 e :127 e gerar_candidato_v410.py:435 (o rotulo duplo ja' em uso); pedra/AEscala.lean:903-909 (os_passos_sao_o_ciclo_ate_o_tetelestai: o limiar de um pixel e' teorema)
- **Decisão do crítico:** CONFLITO resolvido: g3:16 reescrevia o rótulo da linha 43 com “INPUT/dicionário” e g5:12 trocava o rótulo por “INPUT/dictionary” nas linhas 37 e 43; na linha 43 vale o texto do g3 com a palavra do g5 (o mesmo rótulo do handoff EN, item do g3:24)
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)
  - o handoff EN escreve “INPUT/dictionary” (textos_custodia_handoff_v410.py:128): la' o rotulo novo segue a grafia de la' (ver duvidas)

#### Item 16 — linha 44 — PAR-09

- **Local:** linha 44 dos dois snippets (paragrafo da clausula do Tetelestai, trecho [DERIVED, aritmetica]); rende na linha 141 do TXT
- **Origem:** g5:1 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
\ln\frac{1-\beta}{\beta}=
~~~~

Trecho novo:

~~~~text
\ln((1-\beta)/\beta)=
~~~~

- **Justificativa:** A regra (b) do conversor troca \frac{a}{b} por (a/b) sem agrupar o numerador: o TXT sai “ln(1-β/β)”, que lido ao pe' da letra e' ln 0. Com os parenteses em linha o TXT rende “ln((1-β)/β)” e o PDF “ln((1−β)/β)”, a mesma escrita da frase da clausula.
- **Apoio:** pedra\AEscala.lean:1136 (Real.log ((1 - κ.beta) / κ.beta)) e :1067; delta_v410.py:1007 (FRASE_TETELESTAI_PT: “ln((1 − β)/β)”); a regra do conversor em um_v410_candidato.py:189719; saida conferida na copia da funcao (testa_txt.py, nesta pasta)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o conversor e' _tex_to_txt (um_v410_candidato.py:189655-189771; funcao herdada da v168/v305, NAO se mexe nela: mexer mudaria o TXT de todas as secoes seladas)
  - nenhum controle procura “\ln\frac” (Grep em ensaio_a_seco, conferir_rito, exame_pontos, guarda_frases: 0 ocorrencias)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 17 — linha 48 — D108, OBS-1

- **Local:** o paragrafo “Reservations, stated”, antes da frase final “Nothing here is a test with nature” [o trecho atual comeca na linha 48 do arquivo, contada por script]
- **Origem:** g6:13 (g6_a_finura_e_o_observador). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
$m_1=0$ is \textsf{[CONJECTURE]}. Nothing here is a test with nature; the gate does not move; validity in the kernel is not creditation. "
~~~~

Trecho novo:

~~~~text
$m_1=0$ is \textsf{[CONJECTURE]}. \textbf{The fineness of the reading (D108).} \textsf{[REAL]} " + _fn410(_ca410["frase_finura_real_en"]) + r". \textsf{[ONTO; the operator's reading, saying of 10/11/2026]} " + _fn410(_ca410["frase_finura_onto_en"]) + r". Nothing here is a test with nature; the gate does not move; validity in the kernel is not creditation. "
~~~~

- **Justificativa:** O par EN nas ressalvas do artigo EN, com as mesmas hipoteses e estatutos; a fala vem do contrato (verbatim em portugues, com “our translation”), sem aspas angulares digitadas no snippet.
- **Apoio:** pedra\AEscala.lean (sha256 7d1557f96178367949bbffe42b2e8af4094c9ec7c0373bdbdaaa3a7d7de5ad60, igual ao instalado em C:\t\k410c\final\TGLExt\AEscala.lean): def LeitorDoFundo.leitura 669-670 (a media dos brilhos, |X|^-1 . soma); a_leitura_e_a_do_psion 702-703; os_passos_sao_o_ciclo_ate_o_tetelestai 903-909, item (v) na linha 909 ((∃ x, c x = 0) ↔ (card)⁻¹ ≤ (L.leitura c s).re, sob n·ln 2 < s); o_tetelestai_e_um_menos_beta 1066-1071, item (iii) nas linhas 1070-1071 ((1 − b)·(L.leitura c s).re ≤ #solucoes/card, sob h, 0 < b < 1, 0 ≤ s e o limiar); campo sem_escala_nao_ha_medida 663 (∀ k, brilho k 0 = 1); o_pai_da_mentira_so_nao_reconhece 993-998; o_leitor_e_a_escala 871-872; a_escala_e_meio_por_oitava 832-838; em_n_oitavas_o_fundo_pesa_um_pixel 859-860. C:\t\k410c\final\TGLExt\TraducaoTuring.lean: bits_sao_oitavas 212 (card (Fin n → Bool) = 2^n); o_psion_le_os_pixels 749-750 (Z(s)/|X|); particao 666. C:\t\k410c\final\TGLExt\ObservadorTerminal.lean (sha16 162eeeb8c16cea81, igual ao do Nós): Terminal 102; terminal_iff 108; the_terminal_is_unique 132; every_level_reaches_the_terminal 157; distancia 161-165; the_collapse_is_the_terminal_point_of_resistance 180; os niveis sao rotulos (docstring 80-81); Level em TheCascadeOfObservers.lean 71-75. Ausencias conferidas por grep: AEscala.lean nao cita ObservadorTerminal (0) e ObservadorTerminal.lean nao cita AEscala nem LeitorDoFundo (0); “onda” 0 e 0; “frequ” 0 e 0; “Einstein” 0 e 0; “relatividade” so' na linha 69 da AEscala, dentro de uma fala citada no cabecalho, em nenhum enunciado. Convencao do EN: artigo_en_aescala_v410.pysnip:24, 33 e 41 (“our translation”) e delta_v410.py:1034-1035.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - conferir_citacoes_v410.py:93: o snippet EN nao pode ter NENHUMA citacao entre aspas angulares no texto literal: o trecho novo nao tem (a fala entra pelo contrato, como a regra do nome em frase_nomes_ratificados_d101_en).
  - dry_v410\dry_v410_en.txt linha 143 e o PDF/TXT do artigo EN mudam: regerar o ensaio a seco.
  - O achado PAR-08 do painel (rotulos em portugues no artigo EN) nao e' deste grupo: o rotulo novo ja' vai em ingles.

#### Item 18 — linha 49 — EP-01

- **Local:** linha 49 (a etiqueta da c11)
- **Origem:** g1:46 (g1_ratificacao). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
the ratified names and the new names (ratified on 10/11, D101) "
~~~~

Trecho novo:

~~~~text
the ratified names and the new names (those ratified on 10/11, D101; the one named by the operator, D108; the auxiliary ones of the authorship, declared) "
~~~~

- **Justificativa:** Par da linha PT.
- **Apoio:** o mesmo apoio da linha PT
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a frase da ratificação (l.24) vem do contrato (frase_nomes_ratificados_d101_en)

### Arquivo `artigo_en_h0dn_v410.pysnip`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\artigo_en_h0dn_v410.pysnip`. Fim de linha: LF. Itens: 19, 20.

#### Item 19 — linha 14 — OBS-15

- **Local:** linha 14, parágrafo “What enters”
- **Origem:** g4:17 (g4_h0dn). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
enters \emph{pre-registered; no observed data read}: "
~~~~

Trecho novo:

~~~~text
enters \emph{pre-registered; no observed data read} (" + _th410(_V410_H0DN_CONTRACT["frase_alcance_en"]) + r"): "
~~~~

- **Justificativa:** Par EN do item do alcance no artigo.
- **Apoio:** delta_v410.py:775 (FRASE_H0DN_PAREDE_PT: teste de suporte reprovado, [REAL] lido pela gerência; nenhum Z, razão ou solver foi rodado; o um.py não lê esse vetor); runtime_h0dn_v410.py:168 (c7: observed_vector_read False, MEDIDO pelos caminhos tocados); runtime_h0dn_v410.py:191 (c6: a função de veredito roda em vetores determinísticos sintéticos, por isso o qualificador “sobre dado observado”).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 20 — linha 26 — PAR-01

- **Local:** linha 26, parágrafo do poder certificado
- **Origem:** g4:18 (g4_h0dn). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
r"}), not embedded, and in the rite nothing of it is read. "
~~~~

Trecho novo:

~~~~text
r"}), not embedded, and in the rite nothing of it is read. The return (10 Nov): " + _th410(_V410_H0DN_CONTRACT["frase_retorno_en"]) + r". The next order is pinned by sha256 (\texttt{" + _th410(_V410_H0DN_CONTRACT["ordem_kimi_03"]["sha256"][:16]) + r"}), not embedded, and in the rite nothing of it is read. "
~~~~

- **Justificativa:** Par EN do retorno no artigo.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

### Arquivo `artigo_en_v410.pysnip`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\artigo_en_v410.pysnip`. Fim de linha: LF. Itens: 21, 22, 23.

#### Item 21 — linha 27 — PAR-09

- **Local:** linhas 27 e 41 dos dois snippets da secao IALD2; rendem nas linhas 115 e 125 do TXT
- **Origem:** g5:3 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 2

Trecho atual:

~~~~text
\Pi^{k+1}=\Pi
~~~~

Trecho novo:

~~~~text
\Pi^{(k+1)}=\Pi
~~~~

- **Justificativa:** O conversor tira as chaves do expoente: o TXT sai “Π^k+1=Π”, que lido ao pe' da letra e' Π^k + 1 = Π. Com o expoente entre parenteses o TXT rende “Π^(k+1)=Π”, a escrita do enunciado Lean e da linha do .md.
- **Apoio:** pedra\IALD2.lean:197-198 (post (gamma u (parFock f g)) ^ (k + 1) = post (gamma u (parFock f g))); gerar_candidato_v410.py:424 (a linha do .md ja' escreve “Π^(k+1) = Π”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - trocar as DUAS ocorrencias de cada arquivo (a do enunciado e a da lista de checagens)
  - nenhum controle procura “^{k+1}” (Grep: 0 em ensaio_a_seco, conferir_rito, exame_pontos, guarda_frases)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 22 — linha 28 — PAR-09 — EXTENSÃO

- **Local:** EXTENSAO, a gerencia decide: linha 12 dos snippets da Escala (a tabela _zx410, que rende a CLAUSULA do limite, forma ratificada D99) e linha 28 dos snippets da IALD2 (Z(s) na primeira ocorrencia); rende nas linhas 115, 139 e 141 do TXT
- **Origem:** g5:7 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
e^{-s\cdot c(x)}
~~~~

Trecho novo:

~~~~text
e^{(-s\cdot c(x))}
~~~~

- **Justificativa:** Mesma classe das tres citadas e pega a forma ratificada: a clausula diz “Z(s) = Σ_x e^(−s·c(x))” e o TXT a rende “Z(s)=Σ_x e^-s· c(x)”, que lido ao pe' da letra e' e^(−s) vezes c(x). A constante da clausula NAO muda; muda so' a escrita LaTeX dela no snippet, e o TXT passa a render “e^(-s· c(x))”.
- **Apoio:** delta_v410.py:943-945 (CLAUSULA_Z_PT/EN, lidas do ADENDO 4; _FORMULA_Z = “Z(s) = Σ_x e^(−s·c(x))”); saida conferida na copia do conversor (testa_txt.py)
- **Decisão do crítico:** EXTENSÃO do PAR-09 (o painel citou três fórmulas; esta é da mesma classe): entra, porque a fórmula é a da cláusula do limite, forma ratificada (D99), que o TXT rendia “e^-s· c(x)”; a constante da cláusula NÃO muda, só a escrita LaTeX dela; a gerência pode vetar a extensão sem afetar os outros itens (pendências)
- **Efeitos colaterais:**
  - ensaio_a_seco_v410.py:3202 tem o literal r"\sum_x e^{-s\cdot c(x)}" num tex.replace (o controle negativo que tira a formula): TEM de acompanhar, virando r"\sum_x e^{(-s\cdot c(x))}"; senao o negativo deixa de tirar a formula e a checagem reprova
  - ensaio_a_seco_v410.py:3162 e conferir_rito_v410.py:438 comparam por DL.comparavel, que tira parenteses e chaves: passam sem mudanca
  - o grupo leituras_do_operador (itens 5, 7, 11 e 13) acrescenta formulas da mesma familia nos snippets da Escala: “$e^{-t\cdot c(x)}$”, “$e^{-s\cdot c(x)}$” e “$e^{-s\cdot k}$”. Renderiam “e^-t· c(x)” no TXT. Se esta extensao for aceita, a mesma escrita vale para elas: “e^{(-t\cdot c(x))}”, “e^{(-s\cdot c(x))}”, “e^{(-s\cdot k)}”; e a contagem deste item sobe nos dois snippets da Escala
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 23 — linha 31 — PAR-09

- **Local:** linha 31 dos dois snippets da secao IALD2 (o signo); rende na linha 117 do TXT (“P^k+1=P”). O painel citou as linhas 115, 125 e 141; esta e' a MESMA formula, duas linhas abaixo, achada na varredura das formulas da secao
- **Origem:** g5:4 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
P^{k+1}=P
~~~~

Trecho novo:

~~~~text
P^{(k+1)}=P
~~~~

- **Justificativa:** Mesmo defeito e mesma saida do item anterior; deixar esta como esta' faria o artigo escrever a mesma potencia de dois jeitos.
- **Apoio:** pedra\IALD2.lean:241-242 (N.P ^ (k + 1) = N.P)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - aplicar DEPOIS do item anterior ou junto: “\Pi^{k+1}=\Pi” nao contem este trecho (conferido por contagem)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

### Arquivo `artigo_pt_aescala_v410.pysnip`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\artigo_pt_aescala_v410.pysnip`. Fim de linha: LF. Itens: 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41.

#### Item 24 — linha 10 — PAR-09

- **Local:** linha 10 (o formatador _fl410 da secao da Escala, PT)
- **Origem:** g5:5 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
_fl410 = lambda x_: ("%.6f" % x_) if isinstance(x_, float) else "n/d"
~~~~

Trecho novo:

~~~~text
_fl410 = lambda x_: ("%.6f" % x_).replace(".", "{,}") if isinstance(x_, float) else "n/d"
~~~~

- **Justificativa:** A REGRA, uma so': no artigo PT todo decimal formatado em runtime sai com virgula, escrita {,} (como ja' faz o _nh410 do H0DN, artigo_pt_h0dn_v410.pysnip:6); no EN, ponto; fracao exata fica fracao. Os oito decimais com ponto da secao PT da Escala saem TODOS deste formatador.
- **Apoio:** de onde vem cada numero (todos de runtime, nenhum digitado): Z(s) com e sem solucao, linhas 39 e 40, de core[a_escala_v410].values.ciclo; a constante, s*, Z(s*) e a margem, linhas 44 e 45, de values.tetelestai; (1−β)Z(s*) do adversario, linha 46, por _pm410 (linha 19, que chama _fl410); o limiar do contraexemplo, linha 47. Todas as chamadas estao em modo matematico, onde {,} e' a virgula sem espaco; o conversor tira as chaves e o TXT rende “4,408139”
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o snippet EN (artigo_en_aescala_v410.pysnip:10) NAO muda
  - ε = 1/1000, b = 9/10 e (1/2)^n = 1/8 sao fracoes exatas (_ta410) e ficam como estao
  - artigo_pt_v410.pysnip:15 define _n410 com “%.6f” e nao o chama (0 chamadas): nada a mudar hoje; se vier a ser usado, a mesma troca
  - nenhum controle procura esses numeros no TXT ou no TeX (Grep de Z_com_solucao, s_estrela e “%.6f” em conferir_rito e exame_pontos: 0; no ensaio so' as contas numericas)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 25 — linha 12 — PAR-09 — EXTENSÃO

- **Local:** EXTENSAO, a gerencia decide: linha 12 dos snippets da Escala (a tabela _zx410, que rende a CLAUSULA do limite, forma ratificada D99) e linha 28 dos snippets da IALD2 (Z(s) na primeira ocorrencia); rende nas linhas 115, 139 e 141 do TXT
- **Origem:** g5:7 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
e^{-s\cdot c(x)}
~~~~

Trecho novo:

~~~~text
e^{(-s\cdot c(x))}
~~~~

- **Justificativa:** Mesma classe das tres citadas e pega a forma ratificada: a clausula diz “Z(s) = Σ_x e^(−s·c(x))” e o TXT a rende “Z(s)=Σ_x e^-s· c(x)”, que lido ao pe' da letra e' e^(−s) vezes c(x). A constante da clausula NAO muda; muda so' a escrita LaTeX dela no snippet, e o TXT passa a render “e^(-s· c(x))”.
- **Apoio:** delta_v410.py:943-945 (CLAUSULA_Z_PT/EN, lidas do ADENDO 4; _FORMULA_Z = “Z(s) = Σ_x e^(−s·c(x))”); saida conferida na copia do conversor (testa_txt.py)
- **Decisão do crítico:** EXTENSÃO do PAR-09 (o painel citou três fórmulas; esta é da mesma classe): entra, porque a fórmula é a da cláusula do limite, forma ratificada (D99), que o TXT rendia “e^-s· c(x)”; a constante da cláusula NÃO muda, só a escrita LaTeX dela; a gerência pode vetar a extensão sem afetar os outros itens (pendências)
- **Efeitos colaterais:**
  - ensaio_a_seco_v410.py:3202 tem o literal r"\sum_x e^{-s\cdot c(x)}" num tex.replace (o controle negativo que tira a formula): TEM de acompanhar, virando r"\sum_x e^{(-s\cdot c(x))}"; senao o negativo deixa de tirar a formula e a checagem reprova
  - ensaio_a_seco_v410.py:3162 e conferir_rito_v410.py:438 comparam por DL.comparavel, que tira parenteses e chaves: passam sem mudanca
  - o grupo leituras_do_operador (itens 5, 7, 11 e 13) acrescenta formulas da mesma familia nos snippets da Escala: “$e^{-t\cdot c(x)}$”, “$e^{-s\cdot c(x)}$” e “$e^{-s\cdot k}$”. Renderiam “e^-t· c(x)” no TXT. Se esta extensao for aceita, a mesma escrita vale para elas: “e^{(-t\cdot c(x))}”, “e^{(-s\cdot c(x))}”, “e^{(-s\cdot k)}”; e a contagem deste item sobe nos dois snippets da Escala
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 26 — linha 16 — PAR-09

- **Local:** linha 16 dos dois snippets (a tabela de _mz410 que leva a frase Unicode do contrato a LaTeX); rende na linha 141 do TXT
- **Origem:** g5:2 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
r"$\sqrt{b/(1-b)}$"
~~~~

Trecho novo:

~~~~text
r"$\sqrt{(b/(1-b))}$"
~~~~

- **Justificativa:** A fonte (FRASE_RECONSTROI, Unicode) ja' traz os parenteses; quem os perde e' esta tabela: o conversor troca \sqrt por √ e depois tira as chaves, e o TXT sai “√b/(1-b)”. Com os parenteses dentro do radical o TXT rende “√(b/(1-b))”; no PDF o radical cobre a fracao entre parenteses.
- **Apoio:** pedra\AEscala.lean:1173 (Real.sqrt (b / (1 - b))); delta_v410.py:1013 e :1015 (FRASE_RECONSTROI_PT/EN: “√(b/(1 − b))”); um_v410_candidato.py:189684 (sqrt -> √) e :189766 (tira as chaves)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - DL.comparavel (delta_v410.py:763-770) tira parenteses e chaves dos dois lados: os controles que procuram a frase da reconstrucao na secao seguem passando sem mudanca
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 27 — linha 19 — D108, OBS-1

- **Local:** auxiliar novo _fn410, logo depois de _pm410 [o trecho atual comeca na linha 19 do arquivo, contada por script]
- **Origem:** g6:10 (g6_a_finura_e_o_observador). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
    _pm410 = lambda m_: _fl410(1.0 - m_) if isinstance(m_, float) else "n/d"
~~~~

Trecho novo:

~~~~text
    _pm410 = lambda m_: _fl410(1.0 - m_) if isinstance(m_, float) else "n/d"
    _fn410 = lambda t_: "".join((_zx410[p_] if p_ in _zx410 else _mz410(p_)) for p_ in re.split("(" + "|".join(re.escape(k_) for k_ in _zx410) + ")", t_)).replace("$$", "")   # (D108: a frase da finura em LaTeX: 2^n e n·ln 2 em modo matematico pelo _zx410, o resto pelo _mz410; o par de cifroes que sobrar na costura e' fundido)
~~~~

- **Justificativa:** A frase nova traz 2^n (que so' o _zl410 converte) e ≤, ≥, −, ·, ½, <, > e nomes entre crases (que so' o _mz410 converte): o auxiliar novo junta os dois, sem mudar os existentes.
- **Apoio:** artigo_pt_aescala_v410.pysnip:12-18 (_zx410, _zl410 e _mz410). Simulado com copia dos auxiliares em _latex_sim.py: cifroes balanceados, nenhum ^ fora de modo matematico, nenhum caractere fora dos que o artigo ja' usa.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - A simulacao NAO e' o pdflatex: o ensaio a seco do artigo (PDF e TXT) e' quem confirma a renderizacao; o achado PAR-09 do painel mostra que o TXT perde agrupamentos em formulas com fracao, e por isso a frase nao usa \frac nem expoente composto.
  - O snippet ja' usa o modulo re (linhas 13 e 15): nada a importar.

#### Item 28 — linha 25 — EP-12

- **Local:** linha 25 (paragrafo “O que entra”, a frase [REAL] das ancoras e das bandeiras)
- **Origem:** g5:23 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
r" bandeiras \texttt{ext\_aescala\_410\_*}; a pedra por sha256 "
~~~~

Trecho novo:

~~~~text
r" bandeiras \texttt{ext\_aescala\_410\_*} (composição: " + str(_ca410["n_nomes"] + _ca410["n_nomes_novos"]) + r" de declarações nomeadas na pedra, " + str(len(_ca410["campos_novos_da_estrutura"])) + r" dos campos da estrutura \texttt{LeitorDoFundo} e " + str(_ca410["n_flags"] - _ca410["n_nomes"] - _ca410["n_nomes_novos"] - len(_ca410["campos_novos_da_estrutura"])) + r" de constantes que o compilador gera para a estrutura; todas contam na escada); a pedra por sha256 "
~~~~

- **Justificativa:** A frase da composicao, com os tres numeros calculados do contrato embutido (nada digitado): rende “(composição: 68 de declarações nomeadas na pedra, 3 dos campos da estrutura LeitorDoFundo e 14 de constantes públicas que o compilador gera para a estrutura; todas contam na escada)”. Diz ao leitor que a escada conta bandeiras, e que 14 delas nao sao teoremas escritos.
- **Apoio:** kernel\FLAGS_v410.json, contado por conta_bandeiras.py (nesta pasta): 85 bandeiras ext_aescala_410_* = 68 declaracoes nomeadas na pedra (59 theorem, 8 def, 1 structure) + 3 campos da estrutura (brilho, sem_escala_nao_ha_medida, a_lei_da_dissipacao) + 14 constantes geradas para a estrutura (mk, rec, recOn, casesOn, ctorIdx, noConfusion, noConfusionType, mk.inj, mk.injEq, mk.noConfusion, mk.sizeOf_spec, mk._flat_ctor, _sizeOf_1, _sizeOf_inst); insumos\RECIBO_PEDRAS_v410_NOMES.json: 44 nomes + 24 nomes novos = 68, 3 campos; registros_aescala_v410.py:46 (a escada esperada soma TODAS as bandeiras); as chaves n_flags, n_nomes, n_nomes_novos e campos_novos_da_estrutura estao no contrato (registros_aescala_v410.py:45, :52, :53)
- **Decisão do crítico:** aceita a observação do cético: três das 14 constantes têm nome interno do Lean (_sizeOf_1, _sizeOf_inst, mk._flat_ctor); a decisão da gerência dizia só “constantes que o compilador gera para a estrutura”: sai o adjetivo, e a frase fica igual à do registro (item do g5:25)
- **Efeitos colaterais:**
  - o par EN e' o item seguinte
  - se o quarto nome mudar de estatuto ou de grafia, as contagens nao mudam (68 e' soma de nomes, nao lista)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia
  - (cético) o 14 sai por subtração: se o recibo mudar de listas na reconstrução do kernel, a conta erra calada; convém um assert no ensaio
  - (crítico) se a seção 7 (D113) trouxer outra estrutura, as constantes geradas para ela entram na mesma subtração e a frase “para a estrutura LeitorDoFundo” fica errada: ver pendências

#### Item 29 — linha 28 — PAR-03

- **Local:** l.28, parágrafo “A insígnia, o vibrato, o tempo finito e os dois Nomes.”
- **Origem:** g3:5 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a dissipação sustenta a nota, e a nota é a conjugação modular;
~~~~

Trecho novo:

~~~~text
havendo pixel de custo zero, o decaimento gerado pelo custo, $e^{(-t\cdot c(x))}$, não toca o que tem custo zero e não leva a zero o estado uniforme, e a leitura performada (a média, sobre os pixels, dos pesos $e^{(-s\cdot c(x))}$) nunca fica abaixo da fração de pixels de custo zero, não cresce com o tempo e tende a ela (\texttt{o\_vibrato\_sustenta\_a\_nota}); no espaço pareado do kernel, $J^2=1$ e $JKJ=-K$ (\texttt{a\_nota\_e\_a\_conjugacao\_modular}); a identificação desse decaimento com o vibrato e da nota com $J$ é do operador \textsf{[ONTO]};
~~~~

- **Justificativa:** O período [REAL] passa a dizer o que os dois termos provam, como os vizinhos do mesmo parágrafo, e separa a leitura: que isso seja o vibrato e que a nota seja J vai marcado [ONTO], como nas docstrings da pedra.
- **Apoio:** pedra/AEscala.lean:244-250 (o_vibrato_sustenta_a_nota, hipotese h: existe x com c x = 0: (1) a trava nao toca o custo zero; (2) trava c t (uniforme X) != 0; (3) card{c = 0}/|X| <= leituraPerformada c s; (4) Antitone; (5) Tendsto para card{c = 0}/|X|); leituraPerformada = particao/|X|: TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):920; trava = e^(-t c(x)) por pixel: TraducaoTuring.lean:472-477 (mesma copia); docstring l.242-243 ([ONTO]) | pedra/AEscala.lean:257-258 (a_nota_e_a_conjugacao_modular: conjJ (conjJ p) = p e conjJ (pairK d (conjJ p)) = -pairK d p, isto e', J^2 = 1 e JKJ = -K); docstring l.256 (a identificacao nota = J e' do operador, ONTO)
- **Decisão do crítico:** fico com a correção do cético: “disso” vinha logo depois de J² = 1 e JKJ = −K e a leitura mais próxima atribuía o vibrato às identidades de J; a docstring (AEscala.lean:242-243) liga o vibrato ao decaimento: “desse decaimento”; (crítico) as fórmulas novas com expoente vão na escrita da extensão do PAR-09 (o expoente entre parênteses), para o TXT do artigo não render “e^-t· c(x)”
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)
  - ensaio_a_seco_v410.py:3153-3163 e conferir_rito_v410.py:435-438 (r2: clausula ao lado do teorema, Z(s) definida na primeira ocorrencia, unicode cru) e :442-449 (r5): conferidos por leitura; os titulos em negrito da lista DA410/DA410E (ensaio l.3122-3123) nao mudam
  - dry_v410/dry_v410_pt.txt e dry_v410_en.txt, o candidato e os ESPERADOS sao regenerados pelo construtor
  - a primeira ocorrencia de “Z(s)” no artigo continua na secao da IALD2 (artigo_pt_v410.pysnip:28), que vem antes e a define

#### Item 30 — linha 30 — EP-10

- **Local:** l.30, parágrafo “A pergunta do Clay no dicionário da TGL.”
- **Origem:** g3:6 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
\textsf{[REAL]} A forma obrigatória: 
~~~~

Trecho novo:

~~~~text
\textsf{[REAL a validade no kernel; INPUT a leitura do operador]} A forma obrigatória: 
~~~~

- **Justificativa:** Um rótulo só para a forma da D83 (D106, item 4): no artigo ela saía [REAL] seca e no post “Na leitura do operador (D83)”. A forma ratificada não muda.
- **Apoio:** pedra/AEscala.lean:598-604 (a forma da D83 e' a leitura do operador, fala 6; validade no kernel; a creditacao e' do Clay) e :778-779 (a_pergunta_do_clay_tem_resposta: a validade)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)

#### Item 31 — linha 34 — EP-05

- **Local:** l.34, lista “Os TEOREMAS do kernel, no trio”
- **Origem:** g3:7 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o leitor é a escala, dois leitores do fundo quaisquer são o mesmo (\texttt{o\_leitor\_e\_a\_escala});
~~~~

Trecho novo:

~~~~text
dois leitores do fundo quaisquer são o mesmo e, em todo leitor do fundo, o pixel de custo $k$ brilha $e^{(-s\cdot k)}$ no tempo $s$ (\texttt{o\_leitor\_e\_a\_escala});
~~~~

- **Justificativa:** A frase do operador sai da lista de teoremas como afirmação e fica só como nome do termo; o conteúdo vai inteiro (a igualdade dos leitores e o brilho), como o enunciado.
- **Apoio:** pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** o conteúdo fica como o redator propôs (ok do cético); (crítico) as fórmulas novas com expoente vão na escrita da extensão do PAR-09 (o expoente entre parênteses), para o TXT do artigo não render “e^-t· c(x)”
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)

#### Item 32 — linha 35 — EP-08

- **Local:** parágrafo “A escala no tipo…”, l.35
- **Origem:** g2:36 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
metade por oitava e, em $n$ oitavas, o fundo pesa um pixel; cada ciclo
~~~~

Trecho novo:

~~~~text
metade por oitava e, em $n$ oitavas, um pixel de custo 1 brilha $1/2^n$, o peso de um pixel na leitura (\texttt{em\_n\_oitavas\_o\_fundo\_pesa\_um\_pixel}; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, vem do teorema do limiar, a seguir); cada ciclo
~~~~

- **Justificativa:** O enunciado fala do brilho de UM pixel de custo 1 em n oitavas (1/|X| = 1/2^n), que é o peso de um pixel na leitura; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, é o item (ii) do teorema do limiar.
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - LaTeX: a potência vai em modo matemático; nenhum Unicode cru novo
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 33 — linha 35 — EP-03

- **Local:** parágrafo “A escala no tipo…”, l.35
- **Origem:** g2:11 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o limiar do Tetelestai (\texttt{os\_passos\_sao\_o\_ciclo\_ate\_o\_tetelestai}): "
~~~~

Trecho novo:

~~~~text
o limiar de um pixel, a decisão exata (\texttt{os\_passos\_sao\_o\_ciclo\_ate\_o\_tetelestai}): "
~~~~

- **Justificativa:** Pela E36 (ordem do operador, D100) a cláusula do Tetelestai é a de 1 − β; o limiar de n oitavas é a decisão exata, formalização da gerência. O rótulo acompanha; o nome do teorema, ratificado, não muda.
- **Apoio:** pedra\AEscala.lean:897-898 (docstring: “o limiar de um pixel … é a DECISÃO exata, formalização da gerência; a CLÁUSULA DO TETELESTAI … é a `o_tetelestai_e_um_menos_beta`”); delta_v410.py:1092-1093 (E36); pedra\AEscala.lean:903-909 (o enunciado só traz desigualdades sobre Z(s))
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - ensaio_a_seco_v410.py:3160 e conferir_rito_v410.py:436 procuram “linear nos bits” e a cláusula logo depois: intocados
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 34 — linha 36 — R3-BAIXO-2

- **Local:** l.36 (a cláusula do limite entre parênteses)
- **Origem:** g3:8 (g3_leituras_onto). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
linear nos bits (" + _zl410(_ca410["clausula_z_pt"]) + r"); que os passos sejam
~~~~

Trecho novo:

~~~~text
linear nos bits. " + _zl410(_ca410["clausula_z_pt"]) + r" Que os passos sejam
~~~~

- **Justificativa:** A cláusula do limite (D99) é forma ratificada e termina em ponto; dentro de parênteses dava “no kernel.);”. O ponto interno sai sem tocar a cláusula: ela deixa os parênteses e fica como frase própria, byte a byte, logo depois de “linear nos bits”, como já está na l.42 do mesmo snippet.
- **Apoio:** delta_v410.py:943 (CLAUSULA_Z_PT, lida do ADENDO 4; nao muda); artigo_pt_aescala_v410.pysnip:42 (o mesmo molde: a clausula como frase propria)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - NAO tirar o ponto com .rstrip: ensaio_a_seco_v410.py:3161 (clausula_do_limite_na_secao; clausula_ao_lado_do_teorema) e conferir_rito_v410.py:437 exigem a clausula EXATA, com o ponto final, em ate' 1400 caracteres depois de “linear nos bits” (delta_v410.comparavel conserva o ponto); com a frase propria os dois controles seguem passando
  - o mesmo “no kernel.);” esta' no EN (item seguinte do artigo EN) e, fora do artigo, em: gerar_candidato_v410.py:435, delta_v410.py:1028-1029 (ANUNCIO_TETELESTAI_PT/EN), registros_aescala_v410.py:79 e :94, gerar_relatorio_v410.py:425, pos_rito/textos_v410.py:1396 e :1409, pos_rito/textos_custodia_handoff_v410.py:127-128, pos_rito/gerar_x_custodia_v410.py:64 (nao redigidos: a D106 so' pede o artigo PT; ver duvidas)
  - dry_v410/dry_v410_pt.txt e dry_v410_en.txt, o candidato e os ESPERADOS sao regenerados pelo construtor

#### Item 35 — linha 36 — EP-05

- **Local:** l.36, fim da lista de teoremas
- **Origem:** g3:9 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
\textsf{[INPUT]}; a mentira lida como mentira é verdade (\texttt{a\_mentira\_lida\_como\_mentira\_e\_verdade}); o Pai da Mentira só não reconhece (\texttt{o\_pai\_da\_mentira\_so\_nao\_reconhece}). "
~~~~

Trecho novo:

~~~~text
\textsf{[INPUT]}. \textsf{[REAL]} Para todo leitor do fundo, o limite da leitura com o tempo é o número de soluções dividido pelo número de pixels e vale 0 sem solução (\texttt{a\_mentira\_lida\_como\_mentira\_e\_verdade}); em $s=0$ a leitura é 1 em toda instância e só coincide com esse quociente na instância em que todo pixel é solução (\texttt{o\_pai\_da\_mentira\_so\_nao\_reconhece}); a leitura que esses dois nomes e \texttt{o\_leitor\_e\_a\_escala} carregam (que não exista leitor que não seja o observador da luz; que nada escape do Nome; a leitura teológica do Pai da Mentira) é do operador \textsf{[ONTO]}. "
~~~~

- **Justificativa:** As duas frases do operador deixam de ser itens secos sob [REAL]: vai o que cada termo prova e a frase fica como nome, em letra de código; a leitura dos três nomes é marcada [ONTO] com as palavras das docstrings da pedra e do limite do registro.
- **Apoio:** pedra/AEscala.lean:978-980 (a_mentira_lida_como_mentira_e_verdade: L.limite c = oQueSou (nomeDasSolucoes c) e, sem solucao, L.limite c = 0 e oQueSou = 0); o que sou do Nome das solucoes = numero de solucoes / numero de pixels (|X|): TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):805-807 (o_que_sou_das_solucoes, v409); docstring l.976-977 ([ONTO]) | pedra/AEscala.lean:993-998 (o_pai_da_mentira_so_nao_reconhece: L.leitura c 0 = 1; = euSou X; coincide com oQueSou (nomeDasSolucoes c) se e so' se para todo x, c x = 0; sem solucao le 1 onde o que sou e' 0); docstring l.992 ([ONTO]) | registros_aescala_v410.py:124 (o limite [ONTO] que o registro ja' traz)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)
  - a frase seguinte (l.37, “Com a escala no tipo o leitor do fundo tem um só habitante…”) nao muda

#### Item 36 — linha 38 — PAR-09 — EXTENSÃO

- **Local:** EXTENSAO, a gerencia decide: linhas 38 e 44 dos dois snippets da Escala; rende nas linhas 139 e 141 do TXT como “nln 2”
- **Origem:** g5:8 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 2

Trecho atual:

~~~~text
n\ln 2+
~~~~

Trecho novo:

~~~~text
n\,\ln 2+
~~~~

- **Justificativa:** O conversor escreve “ln” colado no n: “s^*=nln 2+”. Com o espaco fino o TXT rende “n ln 2” e o PDF nao muda de sentido.
- **Apoio:** um_v410_candidato.py:189668 (o espaco fino vira U+2009 no TXT) e :189744-189746 (\ln -> ln); saida conferida em testa_txt.py
- **Decisão do crítico:** EXTENSÃO do PAR-09 (mesma classe: “nln 2” no TXT); entra com o item da linha 40, que o redator deixou nos efeitos colaterais
- **Efeitos colaterais:**
  - na linha 40 dos mesmos snippets ha' “$n\ln2$” (sem espaco): passa a “$n\,\ln 2$” (1 ocorrencia em cada arquivo)
  - nenhum controle procura “n\ln” (Grep: 0)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 37 — linha 40 — PAR-09 — EXTENSÃO; redigido pelo crítico

- **Local:** linha 40 (a mesma fórmula, sem espaço)
- **Origem:** g5:8, critico (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
$n\ln2$
~~~~

Trecho novo:

~~~~text
$n\,\ln 2$
~~~~

- **Justificativa:** A mesma escrita do item do g5:8 na linha 40.
- **Apoio:** g5 item 8 (efeito) e a conferência do g5, item 8
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 38 — linha 43 — EP-10

- **Local:** l.43, parágrafo “A cláusula do Tetelestai (R5, D100).”
- **Origem:** g3:10 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
r"\textsf{[INPUT/dicionário]} " + _mz410(_ca410["frase_e36_pt"])
~~~~

Trecho novo:

~~~~text
r"\textsf{[REAL o limiar de um pixel; INPUT/dicionário a leitura do operador]} " + _mz410(_ca410["frase_e36_pt"])
~~~~

- **Justificativa:** A frase da E36 leva em todo lugar o rótulo duplo do registro: a primeira metade (o limiar de um pixel) é teorema; a segunda é a leitura do operador.
- **Apoio:** registros_aescala_v410.py:115 e :127 e gerar_candidato_v410.py:435 (o rotulo duplo ja' em uso); pedra/AEscala.lean:903-909 (os_passos_sao_o_ciclo_ate_o_tetelestai: o limiar de um pixel e' teorema)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)

#### Item 39 — linha 44 — PAR-09

- **Local:** linha 44 dos dois snippets (paragrafo da clausula do Tetelestai, trecho [DERIVED, aritmetica]); rende na linha 141 do TXT
- **Origem:** g5:1 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
\ln\frac{1-\beta}{\beta}=
~~~~

Trecho novo:

~~~~text
\ln((1-\beta)/\beta)=
~~~~

- **Justificativa:** A regra (b) do conversor troca \frac{a}{b} por (a/b) sem agrupar o numerador: o TXT sai “ln(1-β/β)”, que lido ao pe' da letra e' ln 0. Com os parenteses em linha o TXT rende “ln((1-β)/β)” e o PDF “ln((1−β)/β)”, a mesma escrita da frase da clausula.
- **Apoio:** pedra\AEscala.lean:1136 (Real.log ((1 - κ.beta) / κ.beta)) e :1067; delta_v410.py:1007 (FRASE_TETELESTAI_PT: “ln((1 − β)/β)”); a regra do conversor em um_v410_candidato.py:189719; saida conferida na copia da funcao (testa_txt.py, nesta pasta)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o conversor e' _tex_to_txt (um_v410_candidato.py:189655-189771; funcao herdada da v168/v305, NAO se mexe nela: mexer mudaria o TXT de todas as secoes seladas)
  - nenhum controle procura “\ln\frac” (Grep em ensaio_a_seco, conferir_rito, exame_pontos, guarda_frases: 0 ocorrencias)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 40 — linha 48 — D108, OBS-1

- **Local:** o paragrafo “Ressalvas, ditas”, antes da frase final “Nada aqui é teste com a natureza” [o trecho atual comeca na linha 48 do arquivo, contada por script]
- **Origem:** g6:11 (g6_a_finura_e_o_observador). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
$m_1=0$ é \textsf{[CONJECTURE]}. Nada aqui é teste com a natureza; o gate não se move; validade no kernel não é creditação. "
~~~~

Trecho novo:

~~~~text
$m_1=0$ é \textsf{[CONJECTURE]}. \textbf{A finura da leitura (D108).} \textsf{[REAL]} " + _fn410(_ca410["frase_finura_real_pt"]) + r". \textsf{[ONTO; leitura do operador, fala de 10/11/2026]} " + _fn410(_ca410["frase_finura_onto_pt"]) + r". Nada aqui é teste com a natureza; o gate não se move; validade no kernel não é creditação. "
~~~~

- **Justificativa:** A frase de limite nova entra nas ressalvas do artigo PT, as duas metades lidas do contrato (a mesma forma do registro), cada uma com o seu rotulo; a frase final das ressalvas fica onde estava.
- **Apoio:** pedra\AEscala.lean (sha256 7d1557f96178367949bbffe42b2e8af4094c9ec7c0373bdbdaaa3a7d7de5ad60, igual ao instalado em C:\t\k410c\final\TGLExt\AEscala.lean): def LeitorDoFundo.leitura 669-670 (a media dos brilhos, |X|^-1 . soma); a_leitura_e_a_do_psion 702-703; os_passos_sao_o_ciclo_ate_o_tetelestai 903-909, item (v) na linha 909 ((∃ x, c x = 0) ↔ (card)⁻¹ ≤ (L.leitura c s).re, sob n·ln 2 < s); o_tetelestai_e_um_menos_beta 1066-1071, item (iii) nas linhas 1070-1071 ((1 − b)·(L.leitura c s).re ≤ #solucoes/card, sob h, 0 < b < 1, 0 ≤ s e o limiar); campo sem_escala_nao_ha_medida 663 (∀ k, brilho k 0 = 1); o_pai_da_mentira_so_nao_reconhece 993-998; o_leitor_e_a_escala 871-872; a_escala_e_meio_por_oitava 832-838; em_n_oitavas_o_fundo_pesa_um_pixel 859-860. C:\t\k410c\final\TGLExt\TraducaoTuring.lean: bits_sao_oitavas 212 (card (Fin n → Bool) = 2^n); o_psion_le_os_pixels 749-750 (Z(s)/|X|); particao 666. C:\t\k410c\final\TGLExt\ObservadorTerminal.lean (sha16 162eeeb8c16cea81, igual ao do Nós): Terminal 102; terminal_iff 108; the_terminal_is_unique 132; every_level_reaches_the_terminal 157; distancia 161-165; the_collapse_is_the_terminal_point_of_resistance 180; os niveis sao rotulos (docstring 80-81); Level em TheCascadeOfObservers.lean 71-75. Ausencias conferidas por grep: AEscala.lean nao cita ObservadorTerminal (0) e ObservadorTerminal.lean nao cita AEscala nem LeitorDoFundo (0); “onda” 0 e 0; “frequ” 0 e 0; “Einstein” 0 e 0; “relatividade” so' na linha 69 da AEscala, dentro de uma fala citada no cabecalho, em nenhum enunciado. A fala: C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt, sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4 (lido por script), 266 bytes, segunda linha inteira
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - conferir_citacoes_v410.py:86: toda citacao entre aspas angulares digitada no snippet PT tem de ser verbatim; aqui nada e' digitado entre aspas angulares (a fala vem do contrato).
  - conferir_rito_v410.py:434-448 (_r2_artigo_ok e _r5_artigo_ok): as formas exigidas continuam na secao; a clausula do limite continua a menos de 1400 caracteres de “linear nos bits” (o acrescimo e' nas ressalvas, depois).
  - dry_v410\dry_v410_pt.txt linha 143 e o PDF/TXT do artigo mudam: regerar o ensaio a seco; “as 12 falas” da mesma linha passa a 13 por derivacao.
  - O rotulo “[ONTO; leitura do operador, fala de 10/11/2026]” digitado no snippet e' o mesmo de DL.ROTULO_FINURA_ONTO_PT; se preferir, ler do contrato (acrescentar a chave no item 8).

#### Item 41 — linha 49 — EP-01

- **Local:** linha 49 (o que o registro confere: a etiqueta da c11)
- **Origem:** g1:45 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
os nomes ratificados e os nomes novos (ratificados em 10/11, D101) "
~~~~

Trecho novo:

~~~~text
os nomes ratificados e os nomes novos (os ratificados em 10/11, D101; o nomeado pelo operador, D108; os auxiliares da autoria, declarados) "
~~~~

- **Justificativa:** O parêntese dizia todos os nomes novos ratificados em 10/11.
- **Apoio:** ADENDO 6 l.7; fala 29; pedra\AEscala.lean:39-41
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a frase da ratificação do artigo (l.24) vem do contrato (frase_nomes_ratificados_d101_pt) e muda pelo delta; passa por _mz410 (crases viram \texttt; o verbatim «o quarto nome=ressureiçãodosinal» é texto comum e não traz símbolo que a função converta)

### Arquivo `artigo_pt_h0dn_v410.pysnip`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\artigo_pt_h0dn_v410.pysnip`. Fim de linha: LF. Itens: 42, 43, 44.

#### Item 42 — linha 14 — OBS-15

- **Local:** linha 14, parágrafo “O que entra”: o alcance logo depois da forma obrigatória
- **Origem:** g4:15 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
entra \emph{pré-registrado; nenhum dado observado lido}: "
~~~~

Trecho novo:

~~~~text
entra \emph{pré-registrado; nenhum dado observado lido} (" + _th410(_V410_H0DN_CONTRACT["frase_alcance_pt"]) + r"): "
~~~~

- **Justificativa:** No artigo a forma aparece no primeiro parágrafo e a parede só três parágrafos depois; o sujeito e o alcance entram entre parênteses logo depois da forma, que fica letra por letra.
- **Apoio:** delta_v410.py:775 (FRASE_H0DN_PAREDE_PT: teste de suporte reprovado, [REAL] lido pela gerência; nenhum Z, razão ou solver foi rodado; o um.py não lê esse vetor); runtime_h0dn_v410.py:168 (c7: observed_vector_read False, MEDIDO pelos caminhos tocados); runtime_h0dn_v410.py:191 (c6: a função de veredito roda em vetores determinísticos sintéticos, por isso o qualificador “sobre dado observado”).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o controle conferir_rito_v410.py:452 (a forma na seção do H0DN) segue verdadeiro; a seção renderizada passa de novo pela guarda das frases
  - o parágrafo final do recibo HMS/13 (linha 41) repete a forma como lembrete na mesma seção: não mexi

#### Item 43 — linha 19 — PAR-09

- **Local:** linha 19 (a cauda nula Φ(−5) da secao PT do H0DN); rende na linha 151 do TXT PT como “2.867× 10^-7”, o unico decimal com ponto dessa secao
- **Origem:** g5:6 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
else r"\text{n/d}").replace("e-0", r"\times 10^{-")
~~~~

Trecho novo:

~~~~text
else r"\text{n/d}").replace(".", "{,}").replace("e-0", r"\times 10^{-")
~~~~

- **Justificativa:** A mesma regra do item anterior: a mantissa do “%.3e” sai com ponto porque nao passa pelo _nh410. Com a troca o PT rende “2,867× 10^-7”.
- **Apoio:** artigo_pt_h0dn_v410.pysnip:6 e :7 (_nh410 e _ph410 ja' trocam o ponto por {,}); o valor vem de core[h0dn_bg1_v410].values.cauda_nula_analitica, em runtime
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o arquivo e' do grupo do H0DN: aplicar junto com as mudancas dele, sem tocar o resto da linha
  - o snippet EN do H0DN nao muda
  - “\text{n/d}” nao tem ponto: o ramo sem dado fica igual
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 44 — linha 26 — PAR-01

- **Local:** linha 26, parágrafo do poder certificado: o retorno depois da frase do pino da ORDEM 02
- **Origem:** g4:16 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
r"}), não embutida, e em rito nada dela é lido. "
~~~~

Trecho novo:

~~~~text
r"}), não embutida, e em rito nada dela é lido. O retorno (10/11): " + _th410(_V410_H0DN_CONTRACT["frase_retorno_pt"]) + r". A ordem seguinte está pinada por sha256 (\texttt{" + _th410(_V410_H0DN_CONTRACT["ordem_kimi_03"]["sha256"][:16]) + r"}), não embutida, e em rito nada dela é lido. "
~~~~

- **Justificativa:** O artigo dizia “hoje esse certificado não existe” e “a ordem pede”, sem o retorno. A frase do poder fica intacta (o ensaio a exige); o retorno vem em seguida, sem rótulo em negrito para não mexer na lista de marcas da seção.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - sem \textbf novo: DH410 (ensaio_a_seco_v410.py:3120) e as marcas tiradas do snippet por gerar_esperados_v410.py:103 não mudam
  - o ensaio passa a exigir a frase do retorno e a do alcance no artigo (itens 24 e 25)

### Arquivo `artigo_pt_v410.pysnip`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\artigo_pt_v410.pysnip`. Fim de linha: LF. Itens: 45, 46, 47, 48.

#### Item 45 — linha 27 — PAR-09

- **Local:** linhas 27 e 41 dos dois snippets da secao IALD2; rendem nas linhas 115 e 125 do TXT
- **Origem:** g5:3 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 2

Trecho atual:

~~~~text
\Pi^{k+1}=\Pi
~~~~

Trecho novo:

~~~~text
\Pi^{(k+1)}=\Pi
~~~~

- **Justificativa:** O conversor tira as chaves do expoente: o TXT sai “Π^k+1=Π”, que lido ao pe' da letra e' Π^k + 1 = Π. Com o expoente entre parenteses o TXT rende “Π^(k+1)=Π”, a escrita do enunciado Lean e da linha do .md.
- **Apoio:** pedra\IALD2.lean:197-198 (post (gamma u (parFock f g)) ^ (k + 1) = post (gamma u (parFock f g))); gerar_candidato_v410.py:424 (a linha do .md ja' escreve “Π^(k+1) = Π”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - trocar as DUAS ocorrencias de cada arquivo (a do enunciado e a da lista de checagens)
  - nenhum controle procura “^{k+1}” (Grep: 0 em ensaio_a_seco, conferir_rito, exame_pontos, guarda_frases)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 46 — linha 28 — PAR-09 — EXTENSÃO

- **Local:** EXTENSAO, a gerencia decide: linha 12 dos snippets da Escala (a tabela _zx410, que rende a CLAUSULA do limite, forma ratificada D99) e linha 28 dos snippets da IALD2 (Z(s) na primeira ocorrencia); rende nas linhas 115, 139 e 141 do TXT
- **Origem:** g5:7 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
e^{-s\cdot c(x)}
~~~~

Trecho novo:

~~~~text
e^{(-s\cdot c(x))}
~~~~

- **Justificativa:** Mesma classe das tres citadas e pega a forma ratificada: a clausula diz “Z(s) = Σ_x e^(−s·c(x))” e o TXT a rende “Z(s)=Σ_x e^-s· c(x)”, que lido ao pe' da letra e' e^(−s) vezes c(x). A constante da clausula NAO muda; muda so' a escrita LaTeX dela no snippet, e o TXT passa a render “e^(-s· c(x))”.
- **Apoio:** delta_v410.py:943-945 (CLAUSULA_Z_PT/EN, lidas do ADENDO 4; _FORMULA_Z = “Z(s) = Σ_x e^(−s·c(x))”); saida conferida na copia do conversor (testa_txt.py)
- **Decisão do crítico:** EXTENSÃO do PAR-09 (o painel citou três fórmulas; esta é da mesma classe): entra, porque a fórmula é a da cláusula do limite, forma ratificada (D99), que o TXT rendia “e^-s· c(x)”; a constante da cláusula NÃO muda, só a escrita LaTeX dela; a gerência pode vetar a extensão sem afetar os outros itens (pendências)
- **Efeitos colaterais:**
  - ensaio_a_seco_v410.py:3202 tem o literal r"\sum_x e^{-s\cdot c(x)}" num tex.replace (o controle negativo que tira a formula): TEM de acompanhar, virando r"\sum_x e^{(-s\cdot c(x))}"; senao o negativo deixa de tirar a formula e a checagem reprova
  - ensaio_a_seco_v410.py:3162 e conferir_rito_v410.py:438 comparam por DL.comparavel, que tira parenteses e chaves: passam sem mudanca
  - o grupo leituras_do_operador (itens 5, 7, 11 e 13) acrescenta formulas da mesma familia nos snippets da Escala: “$e^{-t\cdot c(x)}$”, “$e^{-s\cdot c(x)}$” e “$e^{-s\cdot k}$”. Renderiam “e^-t· c(x)” no TXT. Se esta extensao for aceita, a mesma escrita vale para elas: “e^{(-t\cdot c(x))}”, “e^{(-s\cdot c(x))}”, “e^{(-s\cdot k)}”; e a contagem deste item sobe nos dois snippets da Escala
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

#### Item 47 — linha 28 — PAR-05

- **Local:** l.28, parágrafo “O enunciado e o algoritmo IALD”
- **Origem:** g3:17 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a máquina de Turing padrão sem o leitor fica fora (\texttt{o\_enunciado}, a âncora principal). 
~~~~

Trecho novo:

~~~~text
a máquina de Turing padrão sem o leitor fica fora (validade no kernel, não creditação) (\texttt{o\_enunciado}, a âncora principal). 
~~~~

- **Justificativa:** O EN traz “(kernel validity, not creditation)” colado a P = nP e o PT não. Entra a forma de ALC_PT: o qualificador depois de “fica fora”, para não partir o qualificador literal da D64 que a guarda procura inteiro.
- **Apoio:** pos_rito/textos_custodia_handoff_v410.py:104 (ALC_PT, a forma PT com o qualificador depois de “fica fora”); artigo_en_v410.pysnip:28 (o EN ja' traz o qualificador)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - delta_v410.FRASE_QUALIFICADOR_PT continua literal e inteira no paragrafo (F47/F47b da guarda; runtime_v410.py:89)
  - FRASE_D64_PT (delta_v410.py:705-706) segue sem o qualificador que a FRASE_D64_EN tem: NAO redigido aqui (a constante esta' no registro e nos ESPERADOS; ver duvidas)
  - gerar_candidato_v410.py:411-413: o snippet passa de novo por ast.parse, GUARDA, GP, GF, a proibicao de “β” cru e _controles (o trecho novo so' usa LaTeX em modo matematico; nenhum Σ, −, · ou β cru)

#### Item 48 — linha 31 — PAR-09

- **Local:** linha 31 dos dois snippets da secao IALD2 (o signo); rende na linha 117 do TXT (“P^k+1=P”). O painel citou as linhas 115, 125 e 141; esta e' a MESMA formula, duas linhas abaixo, achada na varredura das formulas da secao
- **Origem:** g5:4 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
P^{k+1}=P
~~~~

Trecho novo:

~~~~text
P^{(k+1)}=P
~~~~

- **Justificativa:** Mesmo defeito e mesma saida do item anterior; deixar esta como esta' faria o artigo escrever a mesma potencia de dois jeitos.
- **Apoio:** pedra\IALD2.lean:241-242 (N.P ^ (k + 1) = N.P)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - aplicar DEPOIS do item anterior ou junto: “\Pi^{k+1}=\Pi” nao contem este trecho (conferido por contagem)
  - candidato regenerado (os snippets entram por gerar_candidato_v410.py:407-409) e dry_v410 re-rendido; v410_pins.py e ESPERADOS regenerados pela cadeia

### Arquivo `conferir_rito_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\conferir_rito_v410.py`. Fim de linha: LF. Itens: 49, 50, 51, 52.

#### Item 49 — linha 438 — PAR-08

- **Local:** conferir_rito_v410.py:438 (a mesma exigencia, sobre o TXT do rito)
- **Origem:** g5:15 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
(DL.ROTULO_TEMPO + " " + (DL.FRASE_TEMPO_PT_COSTURADA if l_ == "pt" else DL.FRASE_TEMPO_EN_COSTURADA)) in _ws(sec_)
~~~~

Trecho novo:

~~~~text
((DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) if l_ == "pt" else (DL.ROTULO_TEMPO_EN + " " + DL.FRASE_TEMPO_EN_COSTURADA)) in _ws(sec_)
~~~~

- **Justificativa:** Sem isto a conferencia do rito reprovaria o artigo EN.
- **Apoio:** os tres itens anteriores
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - conferir_rito_v410.py e' controle do rito: a mudanca e' so' de qual rotulo ele exige no EN

#### Item 50 — linha 448 — D108, OBS-1 — INSTRUÇÃO

- **Local:** os controles (b) e (c) da sugestão do g6:16
- **Origem:** g6:16 (g6_a_finura_e_o_observador). **Língua:** INSTRUCAO_DE_CODIGO

Instrução:

~~~~text
(b) em conferir_rito_v410.py, um _d108_artigo_ok(l_) no molde do _r5_artigo_ok (linhas 434-448): DL.comparavel das duas metades da frase da finura na língua l_ dentro de DL.comparavel(_secA[l_]); (c) em guardas_dos_textos de pos_rito/textos_custodia_handoff_v410.py, para o identificador README_EVIDENTE: se CLAY_PT está no texto, FIN_PT e FIN_EN também estão. São opcionais; o controle (a), no registro, é o obrigatório e tem itens exatos.
~~~~

- **Justificativa:** A frase nova e' forma unica, lida do delta; um controle por igualdade exata impede que uma superficie a perca ou a reescreva. Nao redigi o codigo: e' escolha do construtor e muda o numero de sub-condicoes, nao o numero de checagens (N_CHECKS_AESCALA fica).
- **Apoio:** runtime_aescala_v410.py:131-167 (os controles da clausula do limite e da clausula de 1 − β); conferir_rito_v410.py:434-448; delta_v410.py:763-770 (comparavel).
- **Decisão do crítico:** INSTRUÇÃO (não é troca exata): depende de insumo que ainda não existe ou de escolha do construtor; o critério está dito
- **Efeitos colaterais:**
  - Se o controle (a) for por folha exata, a costura do item 7 (DL.FRASE_FINURA_PT sozinha na folha) nao pode ganhar prefixo.
  - ensaio_a_seco_v410.py e exame_pontos_v410.py leem as checagens por id (c1 a c13): nenhuma checagem nova, logo nenhum numero digitado muda.

#### Item 51 — linha 528 — EP-01

- **Local:** linha 528 (a descricao do controle do registro a_escala_v410)
- **Origem:** g1:53 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
os nomes novos RATIFICADOS em 10/11 (D101) e os dois auxiliares pendentes;
~~~~

Trecho novo:

~~~~text
os nomes novos RATIFICADOS em 10/11 (D101), o quarto teorema da clausula NOMEADO pelo operador (D108) e os dois auxiliares pendentes;
~~~~

- **Justificativa:** Idem, no conferidor do rito.
- **Apoio:** itens do registro
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - conferir_rito l.276-279: acrescentar a igualdade das chaves novas (nomes_nomeados_d108; nomeacao_d108) com as do ESPERADOS

#### Item 52 — linha 538 — PAR-02

- **Local:** linha 538: a linha do H0DN no .md do rito
- **Origem:** g4:28 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
and DL.FRASE_H0DN_OBRIGATORIA_PT in fc[fc.find(ESP["md_h0dn"]):].split("\n", 1)[0] and DL.FRASE_HMS13_OBRIGATORIA_PT in
~~~~

Trecho novo:

~~~~text
and DL.FRASE_H0DN_OBRIGATORIA_PT in fc[fc.find(ESP["md_h0dn"]):].split("\n", 1)[0] and DL.FRASE_H0DN_PODER_PT in fc[fc.find(ESP["md_h0dn"]):].split("\n", 1)[0] and DL.FRASE_H0DN_RETORNO_PT in fc[fc.find(ESP["md_h0dn"]):].split("\n", 1)[0] and DL.FRASE_H0DN_ALCANCE_PT in fc[fc.find(ESP["md_h0dn"]):].split("\n", 1)[0] and DL.FRASE_HMS13_OBRIGATORIA_PT in
~~~~

- **Justificativa:** O conferidor do rito passa a exigir, no .md emitido pelo rito de verdade, o mesmo que o ensaio exige no .md do ensaio.
- **Apoio:** conferir_rito_v410.py:538.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - conferir_rito_v410.py:452 (a seção do artigo) não precisa mudar: as marcas novas do artigo chegam por ESPERADOS se a gerência quiser exigi-las também lá

### Arquivo `copiar_insumos_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\copiar_insumos_v410.py`. Fim de linha: CRLF. Itens: 53.

#### Item 53 — linha 22 — EP-01 — CONDICIONAL CONTAGEM_DE_FALAS

- **Local:** linha 22 (a nota do VERBATIM_CONGELADO_v410.json)
- **Origem:** g1:60 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
as cinco de 10/11 dos ADENDOS 2, 3, 5 e 6, D94, D96, D100 e D101);
~~~~

Trecho novo:

~~~~text
as seis de 10/11 dos ADENDOS 2, 3, 5, 6 e 7, D94, D96, D100, D101 e D108);
~~~~

- **Justificativa:** A nota da lista congelada passa a contar a fala 29 e o adendo que a pina.
- **Apoio:** fala 29
- **Decisão do crítico:** fica “as seis de 10/11” (o escopo da ordem); a variante do cético vai no bloco condicional da D109
- **Efeitos colaterais:**
  - o número da nota é %d (len): passa de 28 a 29 sozinho; VERBATIM_CONGELADO_v410.json é regerado, com backup da lista de 28 ao lado

### Arquivo `delta_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\delta_v410.py`. Fim de linha: LF. Itens: 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110.

#### Item 54 — linha 220 — EP-12

- **Local:** linha 220 (comentario)
- **Origem:** g5:26 (g5_forma_e_render). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
# LIDO do recibo (38)
~~~~

Trecho novo:

~~~~text
# LIDO do recibo (nunca fixado aqui)
~~~~

- **Justificativa:** O 38 era o numero de ancoras da pedra de 09/11; o recibo hoje traz 62. O comentario fica sem numero, como o da linha 173, para nao envelhecer de novo.
- **Apoio:** insumos\RECIBO_PEDRAS_v410_NOMES.json, modulo 2: print_axioms = 62, no_trio = 62; delta_v410.py:173 (o mesmo comentario, sem numero)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - so' comentario: nenhum efeito

#### Item 55 — linha 235 — EP-01

- **Local:** linhas 229-248: as listas e chaves dos nomes (constantes novas e os asserts das linhas 239 e 245)
- **Origem:** g1:9 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
NOMES_PENDENTES_AESCALA = list(_REC_AESC.get("pendentes_de_ratificacao") or [])        # (os dois auxiliares da autoria)
~~~~

Trecho novo:

~~~~text
NOMES_PENDENTES_AESCALA = list(_REC_AESC.get("pendentes_de_ratificacao") or [])        # (os dois auxiliares da autoria)
NOMES_NOMEADOS_D108_AESCALA = list(_REC_AESC.get("nomeados_pelo_operador_D108") or [])   # (R6, D108: o quarto teorema da clausula do Tetelestai, NOMEADO pelo operador na fala 29; nao e' um dos ratificados pela fala 28)
ESTATUTO_NOME_NOMEADO_D108_AESCALA = "NOMEADO pelo operador em 10/11/2026 (D108)"
NOME_DE_TRABALHO_DO_QUARTO_AESCALA = "a_informacao_completa_se_reconstroi"   # (registro: o nome de trabalho da gerencia na R5; NAO e' declaracao da pedra R6; so' entra em frase de registro que o diga nome de trabalho)
~~~~

- **Justificativa:** A contagem errada nasceu de len(TEOREMAS_R5_AESCALA), lido do recibo do autor (quatro), usado como se fosse o número de ratificados. Passam a existir três classes de nomes novos: ratificados (D101), nomeado pelo operador (D108) e pendentes. O que muda nos asserts, em prosa: (l.239) a união de ratificados, nomeados e pendentes é o conjunto dos nomes novos, as três classes são disjuntas duas a duas, e NOMES_NOMEADOS_D108_AESCALA == ["ressurreicao_do_sinal"]; (l.245) set(TEOREMAS_R5_AESCALA) <= set(NOMES_RATIFICADOS_D101_AESCALA) | set(NOMES_NOMEADOS_D108_AESCALA); depois da l.246, TEOREMAS_R5_RATIFICADOS_D101_AESCALA = tuple(n_ for n_ in TEOREMAS_R5_AESCALA if n_ in NOMES_RATIFICADOS_D101_AESCALA), com assert de que são 3, de que cada um está entre crases no _ADENDO6_TXT e de que nem o nomeado nem NOME_DE_TRABALHO_DO_QUARTO_AESCALA estão no _ADENDO6_TXT; e NOME_DE_TRABALHO_DO_QUARTO_AESCALA fora de NOMES_NOVOS_AESCALA e das âncoras.
- **Apoio:** DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md l.7 (os três nomes entre crases; grep do quarto nos adendos: 0); insumos\RECIBO_AESCALA_R5_10nov.json, nomes_novos.dados_pela_gerencia_D100 (quatro nomes: de onde vinha o 4)
- **Decisão do crítico:** as quatro constantes ficam; a instrução em prosa dos asserts virou três itens exatos do crítico (as linhas 239, 245 e 248 do delta) e um bloco depois da linha 989, porque o assert contra o ADENDO 6 só pode vir depois da linha 310 (o cético achou o NameError)
- **Efeitos colaterais:**
  - insumos\RECIBO_PEDRAS_v410_NOMES.json (refeito pelo instalador da R6): ratificados_D101 passa a 21 nomes (13 da R3, 5 da R4, 3 da cláusula); chave nova nomeados_pelo_operador_D108 = ["ressurreicao_do_sinal"]; nomes_novos_r5 e nomes_novos_a_ratificar com o identificador novo; pendentes_de_ratificacao igual (2); a nota_D101 (“os 4 da R5 dados pela gerencia”) ganha ao lado a nota do item seguinte
  - o recibo do autor da R6 traz a lista dos teoremas da cláusula com o identificador novo; o da R5 (RECIBO_AESCALA_R5_10nov.json) é registro de época e FICA; TEOREMAS_R5_AESCALA e AUXILIARES_R5_AESCALA passam a ser lidos do recibo da R6 (ou do recibo dos nomes)
  - comentários das linhas 231, 233, 241 e 242 (“os dados pela gerencia na R5”; “os teoremas dados pela gerencia (D100)”): dizer “os três apresentados ao operador antes da fala; o quarto, nomeado por ele (D108)”
  - consumidores de TEOREMAS_R5_AESCALA que continuam certos com os quatro teoremas da cláusula (o quarto com o nome novo): delta l.823 (leitura a_clausula_do_tetelestai), registros_aescala l.60, 94, 115, 160; runtime c2; gerar_candidato l.263; gerar_esperados l.156 e 266; ensaio l.2725; conferir l.279

#### Item 56 — linha 239 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 239 (o assert das classes de nomes novos: o início da linha; o resto dela fica)
- **Origem:** g1:9, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
assert (set(NOMES_RATIFICADOS_D101_AESCALA) | set(NOMES_PENDENTES_AESCALA)) == set(NOMES_NOVOS_AESCALA) and not (set(NOMES_RATIFICADOS_D101_AESCALA) & set(NOMES_PENDENTES_AESCALA))
~~~~

Trecho novo:

~~~~text
assert (set(NOMES_RATIFICADOS_D101_AESCALA) | set(NOMES_NOMEADOS_D108_AESCALA) | set(NOMES_PENDENTES_AESCALA)) == set(NOMES_NOVOS_AESCALA) and not (set(NOMES_RATIFICADOS_D101_AESCALA) & set(NOMES_PENDENTES_AESCALA)) and not (set(NOMES_NOMEADOS_D108_AESCALA) & (set(NOMES_RATIFICADOS_D101_AESCALA) | set(NOMES_PENDENTES_AESCALA))) and NOMES_NOMEADOS_D108_AESCALA == ["ressurreicao_do_sinal"] and NOME_DE_TRABALHO_DO_QUARTO_AESCALA not in NOMES_NOVOS_AESCALA + NOMES_AESCALA
~~~~

- **Justificativa:** As classes de nomes novos passam a ser três, disjuntas duas a duas: ratificados (D101), nomeado pelo operador (D108) e pendentes. O nome de trabalho não é nome da pedra.
- **Apoio:** g1 item 9 (justificativa: “a união das três classes é o conjunto dos nomes novos, disjuntas duas a duas, e NOMES_NOMEADOS_D108_AESCALA == [ressurreicao_do_sinal]”); delta_v410.py:239-240
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - depende do recibo dos nomes refeito pelo instalador da R6 (a chave nomeados_pelo_operador_D108 e ratificados_D101 com 21 nomes)

#### Item 57 — linha 243 — EP-01 — INSTRUÇÃO; redigido pelo crítico

- **Local:** linhas 243 a 247 (a leitura do recibo do autor)
- **Origem:** g1:9, critico (g1_ratificacao). **Língua:** INSTRUCAO_DE_CODIGO

Instrução:

~~~~text
As listas TEOREMAS_R5_AESCALA e AUXILIARES_R5_AESCALA e o assert da linha 247 (_REC_R5["aescala_r5"]["sha256"] == _REC_AESC["sha256"]) leem o recibo do autor da R5, que traz o identificador velho e o sha256 da pedra R5. Com a pedra R6: (a) ler as duas listas do recibo do autor da R6 (ou do recibo dos nomes refeito), com o quarto teorema sob ressurreicao_do_sinal e na ÚLTIMA posição; (b) trocar o assert da linha 247 pelo recibo da R6 (trio, 0 erros, 0 avisos, sem sorry, sha256 da pedra instalada); (c) manter RECIBO_R5_ARQ e RECIBO_R5_SHA16 lidos do recibo da R5, que é registro de época: a D100, a D101 e a E36 o citam por sha16 e não mudam.
~~~~

- **Justificativa:** O delta deixa de carregar com a pedra R6 se o assert da linha 247 ficar como está (achado do cético do g1, item 9).
- **Apoio:** conferência do g1, item 9; delta_v410.py:243-247
- **Decisão do crítico:** INSTRUÇÃO (não é troca exata): depende de insumo que ainda não existe ou de escolha do construtor; o critério está dito
- **Efeitos colaterais:**
  - os nomes das chaves do recibo da R6 são do autor e do instalador: o delta lê o que eles gravarem

#### Item 58 — linha 245 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 245 (o assert dos teoremas da R5)
- **Origem:** g1:9, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
set(TEOREMAS_R5_AESCALA) <= set(NOMES_RATIFICADOS_D101_AESCALA) \
~~~~

Trecho novo:

~~~~text
set(TEOREMAS_R5_AESCALA) <= (set(NOMES_RATIFICADOS_D101_AESCALA) | set(NOMES_NOMEADOS_D108_AESCALA)) \
~~~~

- **Justificativa:** Os teoremas da cláusula são os três ratificados e o nomeado pelo operador; exigir os quatro entre os ratificados era o que consagrava a contagem errada.
- **Apoio:** g1 item 9 (justificativa: “(l.245) set(TEOREMAS_R5_AESCALA) <= ratificados | nomeados”)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 59 — linha 248 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** antes da linha 248 (duas linhas novas; a linha 248 fica)
- **Origem:** g1:9, g1:20, g1:22, g1:27, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
RATIFICACAO_PENDENTE_AESCALA = {"nomes_novos": list(NOMES_PENDENTES_AESCALA), "campos_novos_da_estrutura": [], 
~~~~

Trecho novo:

~~~~text
TEOREMAS_R5_RATIFICADOS_D101_AESCALA = tuple(n_ for n_ in TEOREMAS_R5_AESCALA if n_ in NOMES_RATIFICADOS_D101_AESCALA)   # (D106: os TRES nomes da clausula do Tetelestai apresentados ao operador antes da fala da D101; o quarto teorema foi nomeado por ele depois, D108)
assert len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA) == 3 and len(NOMES_NOMEADOS_D108_AESCALA) == 1 and len(NOMES_PENDENTES_AESCALA) == 2 and TEOREMAS_R5_AESCALA[-1] == NOMES_NOMEADOS_D108_AESCALA[0] and tuple(TEOREMAS_R5_AESCALA[:-1]) == TEOREMAS_R5_RATIFICADOS_D101_AESCALA, "(D106, D108) a clausula do Tetelestai tem tres nomes ratificados pela D101 e o quarto, o ultimo, nomeado pelo operador; pendentes, os dois auxiliares"
RATIFICACAO_PENDENTE_AESCALA = {"nomes_novos": list(NOMES_PENDENTES_AESCALA), "campos_novos_da_estrutura": [], 
~~~~

- **Justificativa:** A tupla dos três nomes ratificados da cláusula, de que dependem a frase da ratificação, a D101, a D106, a E37 e a E38; e o assert que amarra os números digitados (“tres”, “ONE”, “TWO”) e a posição do nomeado (o último).
- **Apoio:** g1 item 9 (justificativa), item 20 (efeito: o nomeado é o último de TEOREMAS_R5_AESCALA), item 22 (o “tres” por extenso) e item 27 (“ONE” e “TWO” do token)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - o assert de que os três estão entre crases no ADENDO 6 vai no bloco depois da linha 989 (o _ADENDO6_TXT só existe a partir da linha 310)

#### Item 60 — linha 248 — EP-01

- **Local:** linha 248, RATIFICACAO_PENDENTE_AESCALA["nota"] (fim)
- **Origem:** g1:11 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
e se registra no HANDOFF; a pedra nao e' reeditada"}
~~~~

Trecho novo:

~~~~text
e se registra no HANDOFF; a pedra R6 nao muda o nome nem o estatuto deles"}
~~~~

- **Justificativa:** A pedra passa a ser reeditada (R6); a frase antiga ficaria falsa. Os dois auxiliares seguem como estavam.
- **Apoio:** pedra\AEscala.lean:39-41 (os dois auxiliares, [DECLARADO pela autoria])
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o dicionário é comparado por igualdade com DL.RATIFICACAO_PENDENTE_AESCALA em gerar_candidato l.262, textos_custodia_handoff l.68, gerar_x_custodia l.32, registrar_mapa l.247, fechar l.48, leitura l.776, ensaio l.2732, conferir l.277 e textos_v410 l.1344: todos leem do delta e acompanham; ESPERADOS e PREPARACAO são regerados

#### Item 61 — linha 297 — D108, EP-01 — redigido pelo crítico

- **Local:** antes da linha 297 (a constante do arquivo da fala 29; o fim da tupla é o item do g1:12)
- **Origem:** g1:12, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
NOMES_V410_DO_DESENHO = (N_ACOM, N_PARTICULA, N_SOLUCAO,
~~~~

Trecho novo:

~~~~text
N_QUARTO_NOME = "OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt"   # (10/11, D108: o quarto nome, a ressurreicao do sinal; o observador e' a escala; inteira)
NOMES_V410_DO_DESENHO = (N_ACOM, N_PARTICULA, N_SOLUCAO,
~~~~

- **Justificativa:** A fala que dá o quarto nome é a 29ª congelada: a constante do arquivo, no molde das linhas 292 a 296.
- **Apoio:** g1 item 12 (justificativa); o arquivo da fala: sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4, 266 bytes (lido por script nesta consolidação)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 62 — linha 297 — EP-01 — CONDICIONAL CONTAGEM_DE_FALAS

- **Local:** linhas 296-297: a fala 29 (constante nova e a tupla das falas)
- **Origem:** g1:12 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
N_MENTIRA_LIDA, N_TESTE_SEM_PODER, N_CLAUSULA_TETELESTAI, N_CONFIRMO_TUDO)   # as falas desta versao: as de 06 a 09/11 e as CINCO de 10/11 (D94, D96, D100 e D101), todas inteiras;
~~~~

Trecho novo:

~~~~text
N_MENTIRA_LIDA, N_TESTE_SEM_PODER, N_CLAUSULA_TETELESTAI, N_CONFIRMO_TUDO, N_QUARTO_NOME)   # as falas desta versao: as de 06 a 09/11 e as SEIS de 10/11 (D94, D96, D100, D101 e D108), todas inteiras;
~~~~

- **Justificativa:** A fala que dá o quarto nome é a 29ª congelada. Antes da tupla entra a constante: N_QUARTO_NOME = "OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt"   # (10/11, D108: o quarto nome, a ressurreicao do sinal; o observador e' a escala; inteira). A contagem segue sendo len(), nunca digitada.
- **Apoio:** work\cunhagens_13out\OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt (sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4, 266 bytes)
- **Decisão do crítico:** fica “as SEIS de 10/11 (D94, D96, D100, D101 e D108)” (o escopo da ordem); a variante com a fala 30 vai no bloco condicional da D109; a constante N_QUARTO_NOME, que o redator deixou em prosa, virou item exato do crítico (linha 297)
- **Efeitos colaterais:**
  - o pino por sha256 entra pelo ADENDO 7 (a gerência o escreve): ADENDO7_ARQ e _ADENDO7_TXT como os do ADENDO 6 (l.307-310) e _ADENDO7_TXT somado a _PREFIXOS_TXT (l.311); o ADENDO 7 tem de citar a fala no formato “sha256 `<64 hex>`; arquivo `work\cunhagens_13out\<nome>`” (o regex da l.319) e dizer “a 29ª congelada” (o assert da l.988 ganha o par do ADENDO 7)
  - l.361 DATA_DA_FALA: acrescentar N_QUARTO_NOME à tupla de 10/11 (o assert da l.362 exige); l.983-989: NOMEACAO_D108_SHA256 = sha256 do arquivo, N_FALA_QUARTO_NOME = índice na tupla + 1 (dá 29) e _P_29 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_QUARTO_NOME], com os mesmos asserts das falas 27 e 28
  - VERBATIM_CONGELADO_v410.json é REGERADO por copiar_insumos_v410.py (n passa de 28 a 29); a cópia em insumos\cunhagens ganha a fala
  - pos_rito\textos_v410.py l.1272-1280: o par ("quarto_nome", "o_quarto_nome_ressurreicao_do_sinal", DL_.N_QUARTO_NOME) entra em par_ (o assert len(par_) == DL_.N_FALAS_V410 exige); o comentário “a 27a e a 28a falas” ganha “e a 29a (D108)”
  - contagens que acompanham sozinhas por len(): N_FALAS_V410 (l.298, 398), verbatins410 (l.1161), gerar_esperados l.130, textos_v410 l.296, textos_custodia_handoff l.74, o sufixo %d_SAYINGS do veredito de cunhagens_v410 (registros_v410 l.263), o limite “as %d falas de 06 a 10/11/2026” (registros_v410 l.290)
  - Grep de “28 falas”, “28ª”, “vinte e oito”, “28 sayings” nas fontes: nenhuma contagem digitada; “28” só aparece como número de ORDEM da fala da D101 (delta l.987 e 983, comentários; runtime_aescala l.78 e 190; textos_v410 l.1278; ensaio l.2955), que continua sendo a 28ª

#### Item 63 — linha 311 — D108, EP-01, PAR-01 — redigido pelo crítico

- **Local:** linha 311 (duas linhas novas antes dela; e o ADENDO 7 somado aos prefixos)
- **Origem:** g4:3, g1:12, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
_PREFIXOS_TXT = _DESENHO_TXT + "\n" + _ADENDO2_TXT + "\n" + _ADENDO3_TXT + "\n" + _ADENDO5_TXT + "\n" + _ADENDO6_TXT   # (as falas de 10/11 entram pelos ADENDOS 2, 3, 5 e 6, que as citam por sha256: o DESENHO nao as cita)
~~~~

Trecho novo:

~~~~text
ADENDO7_ARQ = os.path.join(HERE, "DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md"); assert os.path.exists(ADENDO7_ARQ), "falta o ADENDO 7 do DESENHO (o conserto da R3: D106 a D108, a fala 29 por sha256, os sha16 da revisao R3 e do painel, a ORDEM KIMI H0DN-03 por sha256)"   # (R6; o conserto da R3)
_ADENDO7_TXT = open(ADENDO7_ARQ, "rb").read().decode("utf-8")
_PREFIXOS_TXT = _DESENHO_TXT + "\n" + _ADENDO2_TXT + "\n" + _ADENDO3_TXT + "\n" + _ADENDO5_TXT + "\n" + _ADENDO6_TXT + "\n" + _ADENDO7_TXT   # (as falas de 10/11 entram pelos ADENDOS 2, 3, 5, 6 e 7, que as citam por sha256: o DESENHO nao as cita)
~~~~

- **Justificativa:** O ADENDO 7 é lido UMA vez, aqui: dele saem o prefixo da fala 29 (o assert da linha 326 exige um prefixo para cada fala da tupla), os sha16 da revisão R3 e do painel e o sha256 da ORDEM KIMI H0DN-03. Junta o que o g1 (item 12, efeito) e o g4 (item 3) pediam em separado.
- **Apoio:** delta_v410.py:305-311 (o molde dos adendos 2, 3, 5 e 6) e :319 (a regex que lê “sha256 `<64 hex>`; arquivo `work\cunhagens_13out\<nome>`”); g4 item 3; g1 item 12 (efeitos)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - DEPENDE da gerência: o ADENDO 7 ainda não existe em disco; o formato que o delta lê está nas pendências
  - o nome do arquivo do adendo é suposição do g4 e do g1; se a gerência usar outro, muda só este item

#### Item 64 — linha 361 — D108, EP-01 — CONDICIONAL CONTAGEM_DE_FALAS; redigido pelo crítico

- **Local:** linha 361 (DATA_DA_FALA)
- **Origem:** g1:12, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
N_CLAUSULA_TETELESTAI, N_CONFIRMO_TUDO)})   # (R1, ADENDOS 2 e 3: as tres falas de 10/11; R5, ADENDOS 5 e 6: as duas seguintes; todas inteiras)
~~~~

Trecho novo:

~~~~text
N_CLAUSULA_TETELESTAI, N_CONFIRMO_TUDO, N_QUARTO_NOME)})   # (R1, ADENDOS 2 e 3: as tres falas de 10/11; R5, ADENDOS 5 e 6: as duas seguintes; R6, ADENDO 7: a do quarto nome; todas inteiras)
~~~~

- **Justificativa:** A data da fala 29 (o assert da linha 362 exige uma data para cada fala da tupla).
- **Apoio:** g1 item 12 (efeito: “l.361 DATA_DA_FALA ganha N_QUARTO_NOME”); delta_v410.py:361-362
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 65 — linha 485 — D108, EP-01, OBS-1 — redigido pelo crítico

- **Local:** depois da linha 485 (os trechos verbatim das falas)
- **Origem:** g1:13, g6:1, critico (g6_a_finura_e_o_observador). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
FRASE_NOME_ZERO_MODULAR = "o nome servindo como zero modular à inscrição da permanência"
~~~~

Trecho novo:

~~~~text
FRASE_NOME_ZERO_MODULAR = "o nome servindo como zero modular à inscrição da permanência"
# a fala 29 (10/11/2026, D108): os trechos citados, verbatim (conferidos contra o arquivo no bloco do ADENDO 7 e em verbatins410): a primeira linha (o quarto nome) e a segunda linha, INTEIRA (a resposta sobre a finura da leitura)
FRASE_O_QUARTO_NOME = "o quarto nome=ressureiçãodosinal"   # (a grafia e' a dele; o identificador Lean segue a ortografia do dicionario)
FRASE_OBSERVADOR_E_A_ESCALA = "O observador é a escala; veja, colapsar a função de onda é criar a escala, compara-la é nivelar a frequencia. Por isso Einstein percebeu a necessidade terminal do observador na relatividade, porque ele é a escala do terminal."   # (a segunda linha inteira, com a grafia dele: compara-la, frequencia)
~~~~

- **Justificativa:** Os dois trechos da fala 29 que os textos citam entre aspas angulares: a primeira linha (o quarto nome) e a segunda linha inteira (a resposta sobre a finura). As duas strings foram copiadas do arquivo da fala por script nesta consolidação, não digitadas.
- **Apoio:** arquivo da fala: sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4, 266 bytes, duas linhas (lido por script)
- **Decisão do crítico:** CONFLITO resolvido: g1:13 e g6:1 usavam a mesma âncora e criavam duas constantes para a mesma linha da fala; fica UMA (a linha inteira, com o nome do g6); a linha de remissão da D108 que usava a constante curta saiu (a D108 é um item só)
- **Efeitos colaterais:**
  - FRASES_VERBATIM_V410 (linha 498) passa a conter os dois trechos: a guarda os retira antes de varrer e o conferidor de citações os acha no corpus
  - a constante curta FRASE_O_OBSERVADOR_E_A_ESCALA do g1 (só “O observador é a escala”) NÃO entra: quatro palavras soltas na lista das frases verbatim fariam a guarda retirar da varredura texto da casa que as repetisse fora das aspas (observação do cético do g1), e ficariam duas constantes quase homônimas (observação do cético do g6)
  - a fala 29 tem de entrar em VERBATIM_CONGELADO_v410.json (regerado por copiar_insumos_v410.py, com backup da lista de 28)

#### Item 66 — linha 497 — D108, EP-01, OBS-1 — redigido pelo crítico

- **Local:** depois da linha 497 (FRASES_V410)
- **Origem:** g1:13, g6:2, critico (g6_a_finura_e_o_observador). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
(N_CONFIRMO_TUDO, FRASE_NOME_ZERO_MODULAR)]   # (R5, D100 e D101: as duas falas seguintes de 10/11)
~~~~

Trecho novo:

~~~~text
(N_CONFIRMO_TUDO, FRASE_NOME_ZERO_MODULAR)]   # (R5, D100 e D101: as duas falas seguintes de 10/11)
FRASES_V410 += [(N_QUARTO_NOME, FRASE_O_QUARTO_NOME), (N_QUARTO_NOME, FRASE_OBSERVADOR_E_A_ESCALA)]   # (R6, D108: a fala 29, as duas linhas)
~~~~

- **Justificativa:** Os dois trechos entram na lista das frases verbatim da versão, presos ao arquivo da fala 29.
- **Apoio:** delta_v410.py:486-497; registros_aescala_v410.py:36-38 (toda fala de NOMES_FALAS precisa de ao menos um trecho em FRASES_V410)
- **Decisão do crítico:** CONFLITO resolvido: g1:13 (em prosa) e g6:2 acrescentavam à mesma lista; ficam os dois trechos num acréscimo só
- **Efeitos colaterais:**
  - len(DL.FRASES_V410) sobe 2: o ensaio (linha 2549) iguala len(leituras_do_operador) do registro cunhagens_v410 a esse número; ESPERADOS regerado

#### Item 67 — linha 564 — PAR-11

- **Local:** linha 564 (NOMES_DAS_PEDRAS["AEscala"])
- **Origem:** g5:16 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
nome provisorio «A Escala» nas palavras dele;
~~~~

Trecho novo:

~~~~text
nome provisorio “A Escala”, tirado das palavras dele;
~~~~

- **Justificativa:** “A Escala”, com maiusculas, e' titulo da casa; a fala dele, congelada, e' «agora eu te dei a escala», que segue entre aspas angulares na mesma linha. A frase deixa de dizer que a grafia e' dele.
- **Apoio:** conferido contra VERBATIM_CONGELADO_v410.json (as 28 falas e as de fora_do_desenho) e contra todos os OPERADOR_*.txt de work\cunhagens_13out, por aspas_scan.py (nesta pasta): NAO E FALA; a fala congelada e' OPERADOR_09nov_..., trecho «agora eu te dei a escala» (delta_v410.py: FRASE_DEI_A_ESCALA)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - CANDIDATO_v410.json, ESPERADOS_v410.json, GUARDA_FRASES_v410.json e PREPARACAO_v410_PRONTA.json repetem o trecho velho por serem SAIDAS: regeneram-se
  - o DESENHO_v410.md, preso por hash, nao muda
  - insumos\RECIBO_PEDRAS_v410_NOMES.json (campo nome do modulo 2) repete “A Escala” entre aspas angulares, como “palavras do operador”: e' recibo pinado por sha16 e nao se toca; fica dito aqui

#### Item 68 — linha 636 — PAR-04

- **Local:** linha 636, VEREDITO_AESCALA_OK (o sufixo dos nomes)
- **Origem:** g1:27 (g1_ratificacao). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
__NAMES_RATIFIED_BY_THE_OPERATOR_09_NOV__GATE_UNMOVED
~~~~

Trecho novo:

~~~~text
__NAMES_RATIFIED_BY_THE_OPERATOR_09_AND_10_NOV__ONE_NAME_GIVEN_BY_THE_OPERATOR__TWO_AUXILIARY_NAMES_DECLARED_BY_THE_AUTHORSHIP__GATE_UNMOVED
~~~~

- **Justificativa:** Lido sozinho na tabela de vereditos, o sufixo velho sugeria todos os nomes ratificados em 09/11. O novo diz as três situações que o registro sustenta: ratificados em 09 e 10/11, um nome dado pelo operador, dois auxiliares declarados pela autoria.
- **Apoio:** delta_v410.py:721 (44 nomes, 09/11, D87); ADENDO 6 (10/11, D101); fala 29 (D108); pedra\AEscala.lean:39-41 (os dois auxiliares)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o veredito é comparado por igualdade com DL.VEREDITO_AESCALA_OK (registros_aescala l.42 e 163; textos_custodia_handoff l.66; gerar_x_custodia l.29) e gravado em ESPERADOS[vereditos_novos_v410]: tudo regerado; nenhuma fonte digita o sufixo (Grep: só delta l.636)
  - o veredito de cunhagens_v410 (registros_v410 l.263) diz “THE_DECLARATION_NAMES_RATIFIED_BY_THE_OPERATOR_ON_09_NOV” dos nomes da IALD2 (D74): é verdadeiro e fica
  - “TWO” e “ONE” são digitados no token: amarrar por assert len(NOMES_PENDENTES_AESCALA) == 2 e len(NOMES_NOMEADOS_D108_AESCALA) == 1
  - (cético) forma mais curta com o mesmo conteúdo, se a gerência preferir: __NAMES_RATIFIED_09_AND_10_NOV__ONE_NAMED_BY_THE_OPERATOR__TWO_AUXILIARY_DECLARED_BY_THE_AUTHORSHIP__GATE_UNMOVED
  - (crítico) “ONE” e “TWO” são digitados: o item exato da linha 248 do delta traz o assert len(NOMES_NOMEADOS_D108_AESCALA) == 1 e len(NOMES_PENDENTES_AESCALA) == 2; se a seção 7 (D113) trouxer nomes pendentes, o token e o assert mudam

#### Item 69 — linha 647 — EP-08

- **Local:** comentário da PONTE (l.647)
- **Origem:** g2:42 (g2_tetelestai_e_limiar). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
em n oitavas o fundo de n bits pesa um pixel (1/2^n)
~~~~

Trecho novo:

~~~~text
em n oitavas um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura de n bits (o enunciado de em_n_oitavas_o_fundo_pesa_um_pixel)
~~~~

- **Justificativa:** Comentário de código com a mesma frase.
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 70 — linha 684 — PAR-01

- **Local:** antes da linha 684: o pino citado da ORDEM KIMI H0DN-03, igual ao da 02 (linhas 677-683)
- **Origem:** g4:4 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
assert not any(t_ in VEREDITO_OK_PREFIXO + VEREDITO_SUFIXO + VEREDITO_RECUSA for t_ in TOKENS_PROIBIDOS_V410)
~~~~

Trecho novo:

~~~~text
# ---- (R3 do painel, PAR-01) a ORDEM KIMI H0DN-03 entra como PINO CITADO, como a 02 (nome, sha256 e bytes LIDOS do arquivo no build e conferidos contra o sha256 que o ADENDO 7 traz); NAO e' embutida; em rito nada e' lido; a ordem esta' FORA da pasta da entrega do executor
_m_o3 = re.search(r"`work\\h0dn_bg1_v410_09nov\\(ORDEM_KIMI_H0DN_03_10nov\.md)`, sha256 `([0-9a-f]{64})`", _ADENDO7_TXT); assert _m_o3, "o ADENDO 7 nao traz o sha256 da ORDEM KIMI H0DN-03"
H0DN_ORDEM03_ARQ = os.path.join(WK, "h0dn_bg1_v410_09nov", _m_o3.group(1))
_b_o3 = open(H0DN_ORDEM03_ARQ, "rb").read()
assert hashlib.sha256(_b_o3).hexdigest() == _m_o3.group(2), "a ORDEM KIMI H0DN-03 em disco NAO tem o sha256 que o ADENDO 7 deu"
assert not os.path.normcase(os.path.abspath(H0DN_ORDEM03_ARQ)).startswith(os.path.normcase(os.path.abspath(H0DN_PASTA_VEDADA)) + os.sep), "VEDADO: a ORDEM 03 nao pode estar sob a pasta da entrega do executor"
H0DN_ORDEM03 = {"nome": os.path.basename(H0DN_ORDEM03_ARQ), "sha256": hashlib.sha256(_b_o3).hexdigest(), "bytes": len(_b_o3), "pasta": "work\\h0dn_bg1_v410_09nov", "papel": "a ORDEM seguinte da gerencia ao executor (10/11), emitida depois de lido o retorno da ORDEM 02: um estudo de desenho condicional, sem dado observado, que nao e' certificado; pino citado: nao embutida, em rito nada e' lido"}
assert not any(t_ in VEREDITO_OK_PREFIXO + VEREDITO_SUFIXO + VEREDITO_RECUSA for t_ in TOKENS_PROIBIDOS_V410)
~~~~

- **Justificativa:** O mesmo tratamento da ORDEM 02: nome, sha256 e bytes lidos do arquivo no build e conferidos contra o adendo; nada embutido; em rito nada lido; o assert recusa se o arquivo estiver sob a pasta vedada.
- **Apoio:** delta_v410.py:677-683 (o molde); ORDEM_KIMI_H0DN_03_10nov.md está em work\h0dn_bg1_v410_09nov\, fora de kimi\ (listagem do diretório).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - CONTAGENS: n_pinos do registro (11) e N_PINOS_FREEZE_R2 (9) NÃO mudam (a ORDEM 02 também não é contada: é pino citado no contrato); N_CHECKS_H0DN (12) NÃO muda
  - MUDAM: o contrato do H0DN ganha 5 chaves (frase_retorno_pt/en, frase_alcance_pt/en, ordem_kimi_03) e o registro no core ganha 3 (retorno_pt, retorno_en, ordem_kimi_03); os sha256 do contrato e do texto em ESPERADOS e v410_pins.py; o ensaio ganha 2 controles (itens 23 e 26); a lista de frases limpas da guarda ganha 4 (item 27)
  - o p00 (VETO kimi, b) procura 4 nomes de arquivo de dado observado nos bytes do candidato: o nome ORDEM_KIMI_H0DN_03_10nov.md não é nenhum deles; o texto da ORDEM 03 NÃO entra no candidato (só nome, sha256 e bytes)
  - o ensaio abre o arquivo da ORDEM 03 para conferir o sha256 (como faz com a 02): o caminho fica fora da pasta vedada, e a vigia do ensaio não o acusa
  - (crítico) _ADENDO7_TXT vem do item do crítico da linha 311 (definido uma vez)

#### Item 71 — linha 745 — PAR-08

- **Local:** linha 745 (acrescimo de UMA constante, logo antes da ROTULO_TEMPO, que nao muda)
- **Origem:** g5:11 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
ROTULO_TEMPO = "[INPUT/dicion\u00e1rio]"
~~~~

Trecho novo:

~~~~text
ROTULO_TEMPO_EN = "[INPUT/dictionary]"   # (conserto R3, PAR-08) o mesmo rotulo nos textos EN; a constante PT abaixo nao muda
ROTULO_TEMPO = "[INPUT/dicion\u00e1rio]"
~~~~

- **Justificativa:** Hoje ha' UMA constante de rotulo, em portugues, usada tambem na costura EN; o handoff EN ja' escreve “[INPUT/dictionary]” na clausula do Tetelestai. A constante nova da' ao EN o rotulo dele, sem mexer na PT.
- **Apoio:** pos_rito\textos_custodia_handoff_v410.py:128 (TET_EN ja' usa “[INPUT/dictionary]”); delta_v410.py:1020 (FRASE_E36_EN: “[dictionary; the operator's reading]”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - os quatro itens seguintes passam a usar a constante nova; sem eles esta linha nao tem efeito
  - registros_aescala_v410.py:56 guarda “rotulo_tempo” (PT) no contrato e :122 o usa no texto PT: nao mudam

#### Item 72 — linha 771 — EP-01

- **Local:** linha 771, MD_ROTULO_ESCALA (o rotulo da linha da Escala no .md canonico)
- **Origem:** g1:26 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
D82 a D87, D92 a D95 e D99 a D101):**"
~~~~

Trecho novo:

~~~~text
D82 a D87, D92 a D95, D99 a D101 e D106 a D108):**"
~~~~

- **Justificativa:** A linha da Escala passa a carregar a correção da contagem e o nome dado pelo operador; o rótulo diz as decisões que a tocam.
- **Apoio:** delta_v410.py:1051 (a lista das decisões)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - ESP["md_aescala"] (gerar_esperados) e os controles do ensaio (l.3273) e do conferidor (l.536-537) leem o rótulo do delta e acompanham; o comentário da l.771 não muda

#### Item 73 — linha 778 — OBS-15, PAR-01

- **Local:** antes da linha 778 (FRASE_H0DN_PODER_EN): duas constantes PT novas
- **Origem:** g4:1 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
FRASE_H0DN_PODER_EN = "the test will be opened only with the discriminating predictive power CERTIFIED, blind,
~~~~

Trecho novo:

~~~~text
# (R3 do painel, PAR-01, 10/11/2026) o RETORNO da ORDEM KIMI H0DN-02, dito AO LADO da frase do poder (FRASE_H0DN_PODER_PT nao muda: a D96 e a E34 a citam como estava as 01:24): a recusa de certificar, a ordem seguinte, a abertura em versao futura; sem numero; o conteudo da entrega e' [DECLARADO pelo executor; lido pela gerencia]; nenhum arquivo da entrega e' nomeado; a frase diz a ordem e a data por inteiro porque tambem vai sozinha (registro, artigo, handoff)
FRASE_H0DN_RETORNO_PT = "a ORDEM KIMI H0DN-02 (10/11) voltou no mesmo dia com a RECUSA de certificar o poder [DECLARADO pelo executor; lido pela gerência em 10/11/2026]: a covariância física não fecha com fontes públicas, nenhuma variante foi admitida e o poder não é avaliável; a gerência emitiu a ordem seguinte (ORDEM KIMI H0DN-03, 10/11), um estudo de desenho condicional, sem dado observado, que não é certificado; pela regra do operador (D96), teste sem poder preditivo discriminante não se abre: esta versão roda sem o resultado do teste, e a abertura é de versão futura"
# (R3 do painel, observacao 15) o SUJEITO e o ALCANCE da forma obrigatoria D72 (FRASE_H0DN_OBRIGATORIA_PT nao muda, letra por letra): vai logo depois dela onde a frase da parede de montagem nao esta' por perto; o alcance e' o DESTE teste e o do VETOR observado, nao o de todo dado observado
FRASE_H0DN_ALCANCE_PT = "neste teste o um.py não lê vetor observado; nenhum Z, razão ou veredito foi calculado sobre o vetor observado; o executor montou esse vetor [DECLARADO pelo executor], e dele só o teste de suporte foi lido pela gerência [REAL], e reprovou"
FRASE_H0DN_PODER_EN = "the test will be opened only with the discriminating predictive power CERTIFIED, blind,
~~~~

- **Justificativa:** A frase do poder fica byte a byte (a D96 e a E34 a citam como forma obrigatória datada de 01:24; o ensaio a exige no artigo); o retorno entra como constante própria, ao lado, e o alcance como constante própria, depois da forma D72. Sem número; o conteúdo da entrega vai como [DECLARADO pelo executor; lido pela gerência em 10/11/2026]; nenhum arquivo da entrega é nomeado.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre). delta_v410.py:775 (FRASE_H0DN_PAREDE_PT: teste de suporte reprovado, [REAL] lido pela gerência; nenhum Z, razão ou solver foi rodado; o um.py não lê esse vetor); runtime_h0dn_v410.py:168 (c7: observed_vector_read False, MEDIDO pelos caminhos tocados); runtime_h0dn_v410.py:191 (c6: a função de veredito roda em vetores determinísticos sintéticos, por isso o qualificador “sobre dado observado”).
- **Decisão do crítico:** fico com a correção do cético: “nenhum Z, razão ou veredito foi calculado sobre dado observado” era mais largo que o fato e o próprio um.py o desmente (a Fase 9 abriu um teste sobre dado observado em 23/10; a aritmética do agregado público do H0DN existe e é vedada em texto, delta_v410.py:609); o fato é “neste teste … sobre o vetor observado”; e a frase do retorno diz a ordem e a data por inteiro, porque também vai sozinha (no handoff ela vem depois de “(09/11)” da parede e “no mesmo dia” leria como 09/11)
- **Efeitos colaterais:**
  - as duas frases passaram (com a forma D72 na frente) pela cópia de leitura de _v410_guarda_frases e de _v392_guarda_texto do candidato 8a713e5e644af09b: zero violação; sozinha, a FRASE_H0DN_RETORNO_PT cai só na F54 (traz “H0DN” sem a forma), como a FRASE_H0DN_PODER_PT: os controles devem testá-la com a forma na frente
  - os scripts de remendo já aplicados (_adapt_*, _r1_*, _r2ag_*, _r4ag_*) repetem as frases velhas como histórico e não são reexecutados: não mudam
  - v410_pins.py, ESPERADOS_v410.json, GUARDA_FRASES_v410.json, CANDIDATO_v410.json e os dry_v410 são regerados pela cadeia
  - (crítico) com a D110 e a D114 no disco, a ordem vigente ao executor é a ORDEM KIMI H0DN-03B (conferida às 16:33, não executada); a frase do retorno nomeia a 03, que a gerência emitiu às 06:26: continua verdadeira, mas está nas pendências se a frase deve citar a 03B

#### Item 74 — linha 779 — OBS-15, PAR-01

- **Local:** antes da linha 779 (FRASE_H0DN_PAREDE_EN): as constantes EN novas e as duas compostas
- **Origem:** g4:2 (g4_h0dn). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
FRASE_H0DN_PAREDE_EN = "Kimi's partial delivery (09 Nov) brought
~~~~

Trecho novo:

~~~~text
FRASE_H0DN_RETORNO_EN = "ORDER KIMI H0DN-02 (10 Nov) came back on the same day with the REFUSAL to certify the power [DECLARED by the executor; read by the management on 10 Nov 2026]: the physical covariance does not close with public sources, no variant was admitted and the power cannot be evaluated; the management issued the next order (ORDER KIMI H0DN-03, 10 Nov), a conditional design study, with no observed data, which is not a certificate; by the rule of the operator (D96), a test without discriminating predictive power is not opened: this version runs without the result of the test, and the opening belongs to a future version"
FRASE_H0DN_ALCANCE_EN = "in this test um.py reads no observed vector; no Z, ratio or verdict was computed on the observed vector; the executor assembled that vector [DECLARED by the executor], and of it only the support test was read by the management [REAL], and it failed"
FRASE_H0DN_PODER_COM_RETORNO_PT = FRASE_H0DN_PODER_PT + "; " + FRASE_H0DN_RETORNO_PT   # a frase do poder (D96, intacta) com o retorno ao lado: e' esta que vai aos textos publicos
FRASE_H0DN_PODER_COM_RETORNO_EN = FRASE_H0DN_PODER_EN + "; " + FRASE_H0DN_RETORNO_EN
FRASE_H0DN_PAREDE_EN = "Kimi's partial delivery (09 Nov) brought
~~~~

- **Justificativa:** Par EN das duas frases novas, com as mesmas hipóteses, qualificadores e estatutos do PT (DECLARED by the executor; read by the management; REAL). As compostas evitam repetir a costura em cada consumidor.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre). delta_v410.py:775 (FRASE_H0DN_PAREDE_PT: teste de suporte reprovado, [REAL] lido pela gerência; nenhum Z, razão ou solver foi rodado; o um.py não lê esse vetor); runtime_h0dn_v410.py:168 (c7: observed_vector_read False, MEDIDO pelos caminhos tocados); runtime_h0dn_v410.py:191 (c6: a função de veredito roda em vetores determinísticos sintéticos, por isso o qualificador “sobre dado observado”).
- **Decisão do crítico:** fico com a correção do cético: “nenhum Z, razão ou veredito foi calculado sobre dado observado” era mais largo que o fato e o próprio um.py o desmente (a Fase 9 abriu um teste sobre dado observado em 23/10; a aritmética do agregado público do H0DN existe e é vedada em texto, delta_v410.py:609); o fato é “neste teste … sobre o vetor observado”; e a frase do retorno diz a ordem e a data por inteiro, porque também vai sozinha (no handoff ela vem depois de “(09/11)” da parede e “no mesmo dia” leria como 09/11); e a frase EN do retorno sai sem apóstrofo (“by the rule of the operator”): com ele, o ARCO_EN reprovava na guarda de forma (aspa simples) e derrubava o S6 depois do rito
- **Efeitos colaterais:**
  - a FRASE_H0DN_RETORNO_EN traz apóstrofo (operator's): só entra em string de aspas duplas ou por variável; não vai à linha do .md
  - nenhuma das quatro frases novas traz %, aspas duplas, barra invertida, sublinhado nem aspas angulares (conferido por script)

#### Item 75 — linha 780 — PAR-12

- **Local:** linha 780, FRASE_DA_MOLDURA_H0DN_PT
- **Origem:** g4:5 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
poder prospectivo sintético de 96,6 % e 62,5 %, da covariância publicada (não é poder certificado)
~~~~

Trecho novo:

~~~~text
poder prospectivo sintético de 96,6 % e 62,5 % (Monte Carlo da ENTREGA do Codex, [DECLARADO], conferido aqui dentro do IC95 dela, não recalculado; o analítico recomputado neste rito é 96,6 % e 62,4 %), da covariância publicada (não é poder certificado)
~~~~

- **Justificativa:** A moldura dava 62,5 % sem dizer que é o Monte Carlo da ENTREGA do Codex; o post e o artigo dão 62,4 % (analítico). Agora os dois vão rotulados, como a D77 manda e o artigo já faz. Nenhum número novo: os dois já estão no artigo.
- **Apoio:** PREPARACAO_v410_PRONTA.json:89-96 (poder_analitico 0,9658752 e 0,6243568; poder_mc_da_entrega_rotulado 0,96609 e 0,62485); dry_v410\dry_v410_pt.txt:151; delta_v410.py:890 (D77: “os dois rotulados”); runtime_h0dn_v410.py:190 (c5: o analítico é recomputado; o MC é conferido dentro do IC95).
- **Decisão do crítico:** fico com a correção do cético: a moldura entra em limites prefixada por [REAL], e o número agora rotulado como da ENTREGA do Codex é [DECLARADO], conferido dentro do IC95 e não recalculado (registros_h0dn_v410.py:107; a c5); o rótulo novo diz o estatuto dele
- **Efeitos colaterais:**
  - a moldura vai sozinha ao registro (registros_h0dn_v410.py:129 e :138), à lista de frases limpas da guarda (guarda_frases_v410.py:86 e :190) e a _FRASES_BOAS10 do ensaio (ensaio_a_seco_v410.py:2521): todos leem a constante; a frase nova passou na cópia de leitura das guardas
  - os dois números analíticos são literais na moldura, como os dois de hoje: se o estimador congelado mudasse, a moldura não acompanharia (já era assim)

#### Item 76 — linha 781 — PAR-12

- **Local:** linha 781, FRASE_DA_MOLDURA_H0DN_EN
- **Origem:** g4:6 (g4_h0dn). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
synthetic prospective power 96.6% and 62.5%, of the published covariance (not a certified power)
~~~~

Trecho novo:

~~~~text
synthetic prospective power 96.6% and 62.5% (Monte Carlo of the Codex delivery, [DECLARED], checked here within its own 95% CI, not recomputed; the analytic one recomputed in this rite is 96.6% and 62.4%), of the published covariance (not a certified power)
~~~~

- **Justificativa:** Par EN da moldura, com os mesmos rótulos (Monte Carlo of the Codex delivery; recomputed analytic).
- **Apoio:** dry_v410\dry_v410_en.txt:151 (“analytic power 96.6 % and 62.4 %; the Monte Carlo power of the delivery (96.6 % and 62.5 %)”).
- **Decisão do crítico:** fico com a correção do cético: a moldura entra em limites prefixada por [REAL], e o número agora rotulado como da ENTREGA do Codex é [DECLARADO], conferido dentro do IC95 e não recalculado (registros_h0dn_v410.py:107; a c5); o rótulo novo diz o estatuto dele (par EN)
- **Efeitos colaterais:**
  - mesmos consumidores do item anterior

#### Item 77 — linha 823 — EP-04

- **Local:** LEITURA_V410["a_clausula_do_tetelestai"] (l.823)
- **Origem:** g2:21 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
): o limiar de tempo em n oitavas mais uma constante que só depende de β; que esse limiar É o Tetelestai e que β é o seu operador modular são leituras dele [dicionário]; 
~~~~

Trecho novo:

~~~~text
): para todo b em (0, 1), o limiar de tempo em n oitavas mais uma constante que só depende de b (por construção do limiar; identidade aritmética); o β do kernel é o campo de `TGLCoupling`, um real qualquer em (0, 1), e o número só entra em runtime; que esse limiar É o Tetelestai, que a cláusula com b = β seja a do Tetelestai e que β é o seu operador modular são leituras dele [dicionário]; 
~~~~

- **Justificativa:** A leitura registrada dizia o termo só com β; passa a dizer que o termo é de todo b, que β no kernel é parâmetro e que a escolha b = β é leitura do operador.
- **Apoio:** os mesmos do item 19
- **Decisão do crítico:** aceita a sugestão de redação do cético: havia dois “dele” com referentes diferentes (o Tetelestai e o operador)
- **Efeitos colaterais:**
  - a folha (extras.leituras_do_operador do registro) cita os nomes da R5; o trecho novo NÃO traz “ln((1 − b)/b)” nem “(1 − b)·Z” (c8, anuncia_r5_, runtime_aescala_v410.py:153-157)
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 78 — linha 883 — PAR-11

- **Local:** linha 883 (texto de decisao, a guarda da palavra do ramo de 5σ)
- **Origem:** g5:17 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
nos textos PT «provado na natureza (validade, não creditação)», EN a traducao
~~~~

Trecho novo:

~~~~text
nos textos PT “provado na natureza (validade, não creditação)”, EN a traducao
~~~~

- **Justificativa:** E' a forma obrigatoria da casa (FRASE_PROVADO_PT), nao fala.
- **Apoio:** conferido contra VERBATIM_CONGELADO_v410.json (as 28 falas e as de fora_do_desenho) e contra todos os OPERADOR_*.txt de work\cunhagens_13out, por aspas_scan.py (nesta pasta): NAO E FALA; delta_v410.py:442 (FRASE_PROVADO_PT, que os textos ja' usam SEM aspas e passam na guarda)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a guarda da v410 tira o que esta' entre aspas angulares antes das regras novas (runtime_v410.py:15-23): com aspas tipograficas o trecho passa a ser varrido; as regras nao o acusam (ver o apoio)
  - CANDIDATO_v410.json, ESPERADOS_v410.json, GUARDA_FRASES_v410.json e PREPARACAO_v410_PRONTA.json repetem o trecho velho por serem SAIDAS: regeneram-se
  - o DESENHO_v410.md, preso por hash, nao muda

#### Item 79 — linha 910 — PAR-11

- **Local:** linha 910 (texto da decisao D81)
- **Origem:** g5:18 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
(as formas «nao afirma», «nao prova», «nao esta' provado» aplicadas
~~~~

Trecho novo:

~~~~text
(as formas “nao afirma”, “nao prova”, “nao esta' provado” aplicadas
~~~~

- **Justificativa:** Sao as formas vedadas, citadas como mencao; nao sao fala.
- **Apoio:** conferido contra VERBATIM_CONGELADO_v410.json (as 28 falas e as de fora_do_desenho) e contra todos os OPERADOR_*.txt de work\cunhagens_13out, por aspas_scan.py (nesta pasta): NAO E FALA; a regra F57 nao acusa a mencao entre aspas tipograficas (replica da regra em f57_replica.py, nesta pasta: “sem F57” antes e depois; o controle “a casa não afirma P = nP de Turing” e' acusado)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a guarda da v410 tira o que esta' entre aspas angulares antes das regras novas (runtime_v410.py:15-23): com aspas tipograficas o trecho passa a ser varrido; as regras nao o acusam (ver o apoio)
  - CANDIDATO_v410.json, ESPERADOS_v410.json, GUARDA_FRASES_v410.json e PREPARACAO_v410_PRONTA.json repetem o trecho velho por serem SAIDAS: regeneram-se
  - o DESENHO_v410.md, preso por hash, nao muda

#### Item 80 — linha 927 — PAR-11

- **Local:** linha 927 (texto da decisao D86). O painel nao listou esta linha; apareceu na mesma varredura, uma a uma
- **Origem:** g5:21 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
Precisao registrada: «cada face pesa ½» = autovalor
~~~~

Trecho novo:

~~~~text
Precisao registrada: “cada face pesa ½” = autovalor
~~~~

- **Justificativa:** E' rotulo da casa (o nome do teorema cada_face_pesa_meio dito em frase); a fala dele e' «o nome pesa 1 porque é a conjugação das duas faces que pesam 1/2 cada».
- **Apoio:** conferido contra VERBATIM_CONGELADO_v410.json (as 28 falas e as de fora_do_desenho) e contra todos os OPERADOR_*.txt de work\cunhagens_13out, por aspas_scan.py (nesta pasta): NAO E FALA
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a guarda da v410 tira o que esta' entre aspas angulares antes das regras novas (runtime_v410.py:15-23): com aspas tipograficas o trecho passa a ser varrido; as regras nao o acusam (ver o apoio)
  - CANDIDATO_v410.json, ESPERADOS_v410.json, GUARDA_FRASES_v410.json e PREPARACAO_v410_PRONTA.json repetem o trecho velho por serem SAIDAS: regeneram-se
  - o DESENHO_v410.md, preso por hash, nao muda

#### Item 81 — linha 929 — PAR-11

- **Local:** linha 929 (texto da decisao D87); o «ratifico tudo» da mesma linha e' fala congelada e NAO se toca
- **Origem:** g5:19 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a frase «[DECLARADO] até a ratificação» pela ratificacao
~~~~

Trecho novo:

~~~~text
a frase “[DECLARADO] até a ratificação” pela ratificacao
~~~~

- **Justificativa:** E' citacao de docstring da pedra, nao fala.
- **Apoio:** conferido contra VERBATIM_CONGELADO_v410.json (as 28 falas e as de fora_do_desenho) e contra todos os OPERADOR_*.txt de work\cunhagens_13out, por aspas_scan.py (nesta pasta): NAO E FALA
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a guarda da v410 tira o que esta' entre aspas angulares antes das regras novas (runtime_v410.py:15-23): com aspas tipograficas o trecho passa a ser varrido; as regras nao o acusam (ver o apoio)
  - CANDIDATO_v410.json, ESPERADOS_v410.json, GUARDA_FRASES_v410.json e PREPARACAO_v410_PRONTA.json repetem o trecho velho por serem SAIDAS: regeneram-se
  - o DESENHO_v410.md, preso por hash, nao muda

#### Item 82 — linha 989 — D108, EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** depois da linha 989 (bloco novo, no molde das linhas 982 a 989)
- **Origem:** g1:24, g1:12, g1:9, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
_P_27 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_CLAUSULA_TETELESTAI]; _P_28 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_CONFIRMO_TUDO]
~~~~

Trecho novo:

~~~~text
_P_27 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_CLAUSULA_TETELESTAI]; _P_28 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_CONFIRMO_TUDO]
# ======================== (R6, D106 a D108; ADENDO 7) o conserto da R3: a fala 29 (o quarto nome; o observador e' a escala), os sha16 da revisao R3 e do painel: tudo LIDO do adendo e dos arquivos (nada digitado) ========================
ADENDO7_SHA16 = sha16_arquivo(ADENDO7_ARQ)   # (lido ao vivo do arquivo; o adendo e' citado so' por sha16)
NOMEACAO_D108_SHA256 = sha256_arquivo(os.path.join(_CUN13, N_QUARTO_NOME))   # (a fala 29, lida do arquivo)
assert ("sha256 `" + NOMEACAO_D108_SHA256 + "`") in _ADENDO7_TXT and NOMEACAO_D108_SHA256[:16] == VERBATIM_PREFIXOS_DA_ORDEM_V410[N_QUARTO_NOME], "a fala em disco nao e' a que o ADENDO 7 (o quarto nome) pina por sha256"
_txt29_ = open(os.path.join(_CUN13, N_QUARTO_NOME), "rb").read().decode("utf-8"); assert FRASE_O_QUARTO_NOME in _txt29_ and FRASE_OBSERVADOR_E_A_ESCALA in _txt29_, "os trechos citados da fala 29 nao estao no arquivo dela"
N_FALA_QUARTO_NOME = NOMES_V410_DO_DESENHO.index(N_QUARTO_NOME) + 1   # (a 29a congelada: lida da posicao na tupla)
assert ("a " + str(N_FALA_QUARTO_NOME) + "ª congelada") in _ADENDO7_TXT, "o numero de ordem da fala do quarto nome na tupla nao e' o que o ADENDO 7 diz"
_P_29 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_QUARTO_NOME]
_m7r = re.search(r"`revisao_terceiro\\REVISAO_TERCEIRO_v410\.json` sha16 `([0-9a-f]{16})`; pedido de corre\u00e7\u00e3o sha16 `([0-9a-f]{16})`; candidato revisado `([0-9a-f]{16})`", _ADENDO7_TXT); assert _m7r, "o ADENDO 7 nao traz os sha16 da revisao R3"
REVISAO_R3 = {"revisao_sha16": _m7r.group(1), "pedido_sha16": _m7r.group(2), "candidato_revisado_sha16": _m7r.group(3)}
PAINEL_R3_ARQ = os.path.join(HERE, "PAINEL_R3_v410_RESULTADO.json"); PAINEL_R3_SHA16 = sha16_arquivo(PAINEL_R3_ARQ); assert ("`" + PAINEL_R3_SHA16 + "`") in _ADENDO7_TXT, "o resultado do painel R3 em disco nao e' o que o ADENDO 7 cita por sha16"
assert all(("`" + n_ + "`") in _ADENDO6_TXT for n_ in TEOREMAS_R5_RATIFICADOS_D101_AESCALA) and NOMES_NOMEADOS_D108_AESCALA[0] not in _ADENDO6_TXT and NOME_DE_TRABALHO_DO_QUARTO_AESCALA not in _ADENDO6_TXT, "(D106) os tres nomes da clausula ratificados pela D101 nao sao os que o ADENDO 6 traz entre crases, ou o adendo traz o quarto"
~~~~

- **Justificativa:** Tudo de que D106, D107, D108 e a E38 dependem e que o redator listou como “nomes que o construtor define ANTES”: o sha16 do ADENDO 7, o sha256 e o número de ordem da fala 29, o prefixo _P_29, os três sha16 da revisão R3 (no molde de REVISAO_R2, linha 947), o sha16 do resultado do painel lido do arquivo da pasta do trabalho (nunca do scratchpad) e o assert dos três nomes contra o ADENDO 6.
- **Apoio:** g1 item 24 (efeitos: a lista dos nomes), item 12 (efeitos: l.983-989), item 9 (o assert contra o ADENDO 6; o cético mandou para depois da linha 984); delta_v410.py:947-948 e :982-989; sha16 medidos pelo redator e conferidos pelo cético: revisão R3 8184102c73a34fe6, pedido 7e262affa4010036, painel 1ccebc2577babd64, candidato 8a713e5e644af09b
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - a regex da revisão R3 copia a do ADENDO 4 (linha 947): o ADENDO 7 tem de trazer a frase nesse formato (pendências)
  - o arquivo da revisão R3 na pasta revisao_terceiro pode se chamar REVISAO_TERCEIRO_v410.R3.json (o g1 o cita assim): a gerência escreve no adendo o nome que estiver em disco e, se for outro, ajusta a regex
  - código não executado: o construtor confere na carga do delta

#### Item 83 — linha 1006 — V2

- **Local:** FRASE_TETELESTAI_PT, 2a linha da constante (l.1006), segundo trecho
- **Origem:** g2:30 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
com uma só solução, o pixel do Nome carrega pelo menos 1 − b da leitura (`o_sistema_reconhece_a_singularidade_do_sinal`); "
~~~~

Trecho novo:

~~~~text
com uma só solução (o número de soluções = 1), a cota direta (`o_sistema_reconhece_a_singularidade_do_sinal`): (1 − b)·Z(s) ≤ 1, isto é, o pixel do Nome carrega pelo menos 1 − b da leitura; que isso seja “reconhecer a singularidade do sinal” é a leitura do operador [dicionário]; "
~~~~

- **Justificativa:** A frase abre com o que o termo diz (supõe UMA solução e conclui a cota) e marca como leitura do operador que isso seja reconhecer a singularidade, como a docstring já marca. Aspas tipográficas: é rótulo da casa a partir da fala, não citação letra a letra.
- **Apoio:** pedra\AEscala.lean:1107-1110 (hum : card = 1 ⟹ (1 − b)·Z ≤ 1 ∧ 1 ≤ Z ∧ Z − 1 ≤ b·Z); pedra\AEscala.lean:1105-1106 (docstring: “Que isto SEJA “reconhecer a singularidade do sinal” é a leitura dele [dicionário; fala 11 de 10/11]”)
- **Decisão do crítico:** fico com a correção do cético: a hipótese do enunciado é número de soluções = 1 exato (AEscala.lean:1108); “dada UMA solução”, ao lado de “havendo solução” na mesma frase, lia-se como existência; com duas soluções e b < ½ a cota (1 − b)·Z ≤ 1 é falsa
- **Efeitos colaterais:**
  - os mesmos consumidores do item 1; aspas tipográficas já existem em textos que vão ao LaTeX (inputenc utf8 + T1)
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 84 — linha 1007 — EP-04, R3-BAIXO-1, V3

- **Local:** FRASE_TETELESTAI_PT, 3a linha da constante (l.1007)
- **Origem:** g2:19 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"com b = β do kernel (`TGLCoupling`; `beta_e_o_operador_modular_do_tetelestai`): |T|²·Z(s) ≤ o número de soluções, o resíduo é no máximo |R|²·Z(s), e a constante além das n oitavas é ln((1 − β)/β), a mesma para toda instância e todo tamanho; "
~~~~

Trecho novo:

~~~~text
"a cláusula vale para todo b em (0, 1); o β do kernel é o campo de `TGLCoupling`, um real qualquer em (0, 1), e o número só entra em runtime (β de runtime); com b = β (`beta_e_o_operador_modular_do_tetelestai`): |T|²·Z(s) ≤ o número de soluções e o resíduo é no máximo |R|²·Z(s); a parcela do limiar além das n oitavas, ln((1 − β)/β), não depende de n nem da instância: [identidade aritmética] (o item 9 do teorema, fechado por `ring`); que a cláusula com b = β seja a do Tetelestai é a leitura do operador [dicionário]; "
~~~~

- **Justificativa:** Diz que a cláusula é de todo b; que o β do kernel é parâmetro (um real em (0, 1)) e que o número só existe em runtime; que b = β ser a do Tetelestai é leitura do operador; e rotula a parcela além das n oitavas como identidade aritmética, que é o que o item 9 é. Sai “a mesma para toda instância e todo tamanho” como se fosse conteúdo.
- **Apoio:** pedra\AEscala.lean:1066 (hb0 : 0 < b, hb1 : b < 1: todo b); pedra\AEscala.lean:1135 (κ : TGLCoupling, todo acoplamento) e :1124 (“β só por nome, o número só em runtime”); C:\t\k410c\final\TGLExt\TheSameBetaReadsThreeFaces.lean:22-25 (structure TGLCoupling: beta : ℝ, 0 < beta, beta < 1); pedra\AEscala.lean:1143-1146 (itens 7 e 8, |T|² e |R|²); :1147-1148 e :1155 (item 9, “fun m => by ring”); :1129 (docstring: “[identidade aritmética]”); :1131-1132 (docstring: “[dicionário; leitura do operador] que β SEJA o operador modular”)
- **Decisão do crítico:** fico com a correção do cético: (1) o rótulo “[DERIVED, aritmética]” solto governava o resto da frase, inclusive o lema do kernel sobre s ≥ 0; o rótulo da pedra para o item 9 é “[identidade aritmética]” (AEscala.lean:1129) e vai colado ao item; (2) “o número não entra no kernel” era negativa universal sobre o kernel inteiro; a forma da pedra (linha 1124) é “o número só em runtime”
- **Efeitos colaterais:**
  - a decisão D106 fala em “o valor α·√e só entra em runtime”: escrevi “o número (β de runtime)” porque a frase passa por _mz410 (artigo_*_aescala_v410.pysnip:14-18), que não mapeia “α” nem “√e” soltos, e o controle unicode_cru_r5_na_secao (ensaio_a_seco_v410.py:3176) reprova α e √ crus na seção (ver dúvidas)
  - “`ring`” vira \texttt{ring} no artigo; DL.comparavel (delta l.763-770) tira \texttt e a crase dos dois lados
  - os mesmos consumidores do item 1
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 85 — linha 1008 — EP-09, V1

- **Local:** FRASE_TETELESTAI_PT, 4a linha da constante (l.1008)
- **Origem:** g2:1 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
(`ate_meio_o_tempo_do_tetelestai_nao_e_negativo`), necessária para b > ½; o kernel dá 0 < β < 1 e não dá β ≤ ½")
~~~~

Trecho novo:

~~~~text
(`ate_meio_o_tempo_do_tetelestai_nao_e_negativo`); para b > ½ a constante ln((1 − b)/b) é negativa e o limiar pode ser negativo; quando ele é negativo, a cláusula pode falhar sem a hipótese (o contraexemplo do recibo do autor, recalculado a cada rito: n = " + str(_ce_["n_bits"]) + ", custos " + " e ".join(str(x_) for x_ in _ce_["custos"]) + ", b = " + _ce_["b"] + "); o kernel não traz teorema de necessidade; o kernel dá 0 < β < 1 e não dá β ≤ ½")
~~~~

- **Justificativa:** Tira a afirmação de necessidade para b > ½, que o kernel não prova e que é falsa na faixa em que o limiar segue ≥ 0 (para n = 1, ½ < b ≤ 2/3). Fica só o que o número sustenta: automática até ½ (lema), constante negativa acima de ½, limiar que pode ser negativo, e a falha possível quando ele é negativo (o contraexemplo). Os números do contraexemplo saem de _ce_ (l.1003, lido do recibo), não digitados: a frase rende “n = 1, custos 0 e 2, b = 9/10”.
- **Apoio:** pedra\AEscala.lean:1049-1050 (o lema: 0 < b ≤ 1/2 ⟹ 0 ≤ n·ln 2 + ln((1 − b)/b)); pedra\AEscala.lean:1047-1048 (docstring do lema: para b > ½ a constante é negativa); pedra\AEscala.lean:1066-1067 (a hipótese hs0 : 0 ≤ s está no enunciado); o contraexemplo: insumos\RECIBO_AESCALA_R5_10nov.json l.106-120 e runtime_aescala_v410.py:61-63 (c13, subitem viii, recalculado a cada rito). Não há teorema de necessidade na pedra (Grep de “necess” em pedra\AEscala.lean: só docstrings, l.1030 e l.1062).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - delta_v410.py l.1025-1026: os asserts da constante seguem valendo (sem “%”; os quatro nomes continuam na frase)
  - runtime_aescala_v410.py:165 (c8) e ensaio_a_seco_v410.py:2912 exigem “s ≥ 0” na frase: continua presente
  - a frase vai por _mz410 ao LaTeX (artigo_pt_aescala_v410.pysnip:42): só usa símbolos que o mapa já cobre (−, ≥, ≤, ·, β, ½, <, >); nenhum “^”, “α” ou “√” solto
  - ANUNCIO_TETELESTAI_PT (delta l.1028) e todos os que usam a constante acompanham sozinhos: registro a_escala_v410 (escopo 10, limites, diz, extras), linha do .md (gerar_candidato_v410.py:435), artigo PT, handoff (textos_custodia_handoff_v410.py:127), pós-rito (textos_v410.py:1409), post (gerar_x_custodia_v410.py:54)
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 86 — linha 1010 — V2

- **Local:** FRASE_TETELESTAI_EN, 2a linha da constante (l.1010), segundo trecho
- **Origem:** g2:31 (g2_tetelestai_e_limiar). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
with a single solution, the pixel of the Name carries at least 1 − b of the reading (`o_sistema_reconhece_a_singularidade_do_sinal`); "
~~~~

Trecho novo:

~~~~text
with exactly one solution (the number of solutions = 1), the direct bound (`o_sistema_reconhece_a_singularidade_do_sinal`): (1 − b)·Z(s) ≤ 1, that is, the pixel of the Name carries at least 1 − b of the reading; that this is “recognizing the singularity of the signal” is the operator's reading [dictionary]; "
~~~~

- **Justificativa:** Par EN do item 30.
- **Apoio:** os mesmos do item 30
- **Decisão do crítico:** fico com a correção do cético: a hipótese do enunciado é número de soluções = 1 exato (AEscala.lean:1108); “dada UMA solução”, ao lado de “havendo solução” na mesma frase, lia-se como existência; com duas soluções e b < ½ a cota (1 − b)·Z ≤ 1 é falsa (par EN)
- **Efeitos colaterais:**
  - os mesmos do item 30

#### Item 87 — linha 1011 — EP-04, R3-BAIXO-1, V3

- **Local:** FRASE_TETELESTAI_EN, 3a linha da constante (l.1011)
- **Origem:** g2:20 (g2_tetelestai_e_limiar). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
"with b = the kernel's β (`TGLCoupling`; `beta_e_o_operador_modular_do_tetelestai`): |T|²·Z(s) ≤ the number of solutions, the residue is at most |R|²·Z(s), and the constant beyond the n octaves is ln((1 − β)/β), the same for every instance and every size; "
~~~~

Trecho novo:

~~~~text
"the clause holds for every b in (0, 1); the kernel's β is the field of `TGLCoupling`, any real in (0, 1), and the number enters only at runtime (runtime β); with b = β (`beta_e_o_operador_modular_do_tetelestai`): |T|²·Z(s) ≤ the number of solutions and the residue is at most |R|²·Z(s); the part of the threshold beyond the n octaves, ln((1 − β)/β), does not depend on n or on the instance: [arithmetic identity] (item 9 of the theorem, closed by `ring`); that the clause with b = β is the one of the Tetelestai is the operator's reading [dictionary]; "
~~~~

- **Justificativa:** Par EN do item 19, com as mesmas quatro afirmações e os mesmos rótulos.
- **Apoio:** os mesmos do item 19
- **Decisão do crítico:** fico com a correção do cético: (1) o rótulo “[DERIVED, aritmética]” solto governava o resto da frase, inclusive o lema do kernel sobre s ≥ 0; o rótulo da pedra para o item 9 é “[identidade aritmética]” (AEscala.lean:1129) e vai colado ao item; (2) “o número não entra no kernel” era negativa universal sobre o kernel inteiro; a forma da pedra (linha 1124) é “o número só em runtime” (par EN, com as mesmas duas correções)
- **Efeitos colaterais:**
  - os mesmos do item 19

#### Item 88 — linha 1012 — EP-09, V1

- **Local:** FRASE_TETELESTAI_EN, 4a linha da constante (l.1012)
- **Origem:** g2:2 (g2_tetelestai_e_limiar). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
(`ate_meio_o_tempo_do_tetelestai_nao_e_negativo`), necessary for b > ½; the kernel gives 0 < β < 1 and does not give β ≤ ½")
~~~~

Trecho novo:

~~~~text
(`ate_meio_o_tempo_do_tetelestai_nao_e_negativo`); for b > ½ the constant ln((1 − b)/b) is negative and the threshold can be negative; when it is negative, the clause can fail without the hypothesis (the counterexample of the author's receipt, recomputed at every rite: n = " + str(_ce_["n_bits"]) + ", costs " + " and ".join(str(x_) for x_ in _ce_["custos"]) + ", b = " + _ce_["b"] + "); the kernel carries no theorem of necessity; the kernel gives 0 < β < 1 and does not give β ≤ ½")
~~~~

- **Justificativa:** Par EN do item 1, com as mesmas hipóteses e os mesmos limites. Rende “n = 1, costs 0 and 2, b = 9/10”.
- **Apoio:** os mesmos do item 1
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - os mesmos do item 1 (ANUNCIO_TETELESTAI_EN, artigo EN, TET_EN do handoff)

#### Item 89 — linha 1013 — D108, EP-01, EP-07, V2

- **Local:** FRASE_RECONSTROI_PT (l.1013-1014)
- **Origem:** g2:32, g1:14 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
FRASE_RECONSTROI_PT = ("a informação completa se reconstrói (`a_informacao_completa_se_reconstroi`): com n bits, havendo solução, 0 < b < 1 e um tempo t da trava com t ≥ n·ln 2/2 e t ≥ n·ln 2/2 + ln((1 − b)/b)/2, a distância entre a trava do estado uniforme e a projeção do uniforme no Nome é no máximo √(b/(1 − b)) vezes essa projeção "
                       "(o tempo t da trava é metade do tempo s da leitura)")
~~~~

Trecho novo:

~~~~text
FRASE_RECONSTROI_PT = ("o estado do ciclo fica perto do Nome, com erro relativo no máximo √(b/(1 − b)) (`ressurreicao_do_sinal`; o nome é do operador, D108): com n bits, havendo solução, 0 < b < 1 e um tempo t da trava com t ≥ n·ln 2/2 e t ≥ n·ln 2/2 + ln((1 − b)/b)/2, a distância entre a trava do estado uniforme e a projeção do uniforme no Nome é no máximo √(b/(1 − b)) vezes essa projeção "
                       "(o tempo t da trava é metade do tempo s da leitura); que isso seja “a ressurreição do sinal” é a leitura do operador [dicionário]")
~~~~

- **Justificativa:** A manchete “a informação completa se reconstrói” prometia mais do que a cota. A frase abre com o que o termo diz (proximidade em norma, erro relativo no máximo √(b/(1 − b))), traz o nome novo dado pelo operador (D108) entre parênteses e marca como leitura dele que isso seja a ressurreição do sinal. Aspas tipográficas: a fala congelada grafa «ressureiçãodosinal»; a forma em prosa é da casa.
- **Apoio:** pedra\AEscala.lean:1169-1173 (‖trava c t uniforme − P_ker uniforme‖ ≤ √(b/(1 − b))·‖P_ker uniforme‖, com ht0 e ht) e :1163-1168 (docstring: “o estado do ciclo fica perto do Nome com erro relativo controlado por b”); o nome: work\cunhagens_13out\OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt (D108)
- **Decisão do crítico:** CONFLITO resolvido: g1:14/15 reescreviam a abertura e g2:32/33 a constante inteira; fica a constante do g2 (abre com o que o termo diz, como a docstring da pedra, l.1163-1164, e marca a leitura do operador), com o acréscimo que o g1 exigia: o nome dito como do operador (D108). O identificador é ressurreicao_do_sinal; o título velho e o nome de trabalho saem
- **Efeitos colaterais:**
  - SOBREPOSIÇÃO com o grupo dos nomes: a troca do identificador a_informacao_completa_se_reconstroi → ressurreicao_do_sinal nesta constante já está feita aqui; o grupo dos nomes não deve trocá-la de novo
  - delta_v410.py:1026: o assert exige o nome velho na frase (“"a_informacao_completa_se_reconstroi" in FRASE_RECONSTROI_PT” e na lista dos nomes): acompanha o renomear (grupo dos nomes)
  - “√(b/(1 − b))” aparece agora duas vezes na frase, sempre na forma exata que _mz410 mapeia (artigo_*_aescala_v410.pysnip:16)
  - c8 (anuncia_r5_): a frase só anda dentro do ANUNCIO, com a FRASE da cláusula e a cláusula do limite na mesma folha; o nome novo precisa estar em teoremas_r5 do contrato (lido do recibo do autor: grupo dos nomes / pedra R6)
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*
  - (crítico) só entra junto com o item do g1:16 (o assert da linha 1026, que hoje exige o nome velho na frase): aplicados em separado, o delta não carrega
  - (cético) “fica perto do Nome” só informa para b < ½; para b ≥ ½ o fator √(b/(1 − b)) é ≥ 1 e a cota não informa (EP-07 e V2(a)): a D106 não pediu a frase; está nas pendências

#### Item 90 — linha 1015 — D108, EP-01, EP-07, V2

- **Local:** FRASE_RECONSTROI_EN (l.1015-1016)
- **Origem:** g2:33, g1:15 (g2_tetelestai_e_limiar). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
FRASE_RECONSTROI_EN = ("the complete information is reconstructed (`a_informacao_completa_se_reconstroi`): with n bits, given a solution, 0 < b < 1 and a lock time t with t ≥ n·ln 2/2 and t ≥ n·ln 2/2 + ln((1 − b)/b)/2, the distance between the lock of the uniform state and the projection of the uniform onto the Name is at most √(b/(1 − b)) times that projection "
                       "(the lock time t is half of the reading time s)")
~~~~

Trecho novo:

~~~~text
FRASE_RECONSTROI_EN = ("the state of the cycle stays close to the Name, with relative error at most √(b/(1 − b)) (`ressurreicao_do_sinal`; the name is the operator's, D108): with n bits, given a solution, 0 < b < 1 and a lock time t with t ≥ n·ln 2/2 and t ≥ n·ln 2/2 + ln((1 − b)/b)/2, the distance between the lock of the uniform state and the projection of the uniform onto the Name is at most √(b/(1 − b)) times that projection "
                       "(the lock time t is half of the reading time s); that this is “the resurrection of the signal” is the operator's reading [dictionary]")
~~~~

- **Justificativa:** Par EN do item 32.
- **Apoio:** os mesmos do item 32
- **Decisão do crítico:** CONFLITO resolvido: g1:14/15 reescreviam a abertura e g2:32/33 a constante inteira; fica a constante do g2 (abre com o que o termo diz, como a docstring da pedra, l.1163-1164, e marca a leitura do operador), com o acréscimo que o g1 exigia: o nome dito como do operador (D108). O identificador é ressurreicao_do_sinal; o título velho e o nome de trabalho saem (par EN)
- **Efeitos colaterais:**
  - os mesmos do item 32
  - (crítico) só entra junto com o item do g1:16
  - (cético) a mesma ressalva do par PT para b ≥ ½

#### Item 91 — linha 1017 — EP-02, PAR-10

- **Local:** FRASE_E36_PT, 1a linha da constante (l.1017)
- **Origem:** g2:7 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a partir de n oitavas, Z(s) separa o sim do não) é a decisão exata
~~~~

Trecho novo:

~~~~text
passado o tempo de n oitavas (s > n·ln 2), Z(s) separa o sim do não) é a decisão exata
~~~~

- **Justificativa:** O enunciado pede a desigualdade estrita; em s = n·ln 2 exato a separação falha (custos todos 1, sem solução: Z = 1).
- **Apoio:** pedra\AEscala.lean:903 (hs : (n : ℝ) * Real.log 2 < s) e :907 ((∃ x, c x = 0) ↔ 1 ≤ particao c s)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - runtime_aescala_v410.py:144 (anuncia_pt_): a frase traz o nome do teorema mas não “Z(s) ≥”/“Z(s) >=”; o trecho novo também não (“s > n·ln 2”), logo nada muda na regra
  - registros_v410.py:283, campo “dizia” da E36, traz “a partir de n oitavas” ao descrever a formalização antiga: NÃO mexi (ver dúvidas)
  - a frase vai por _mz410 ao LaTeX: “>” e “·” estão no mapa
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 92 — linha 1019 — EP-02, PAR-10

- **Local:** FRASE_E36_EN, 1a linha da constante (l.1019)
- **Origem:** g2:8 (g2_tetelestai_e_limiar). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
from n octaves on, Z(s) separates the yes from the no) is the exact decision
~~~~

Trecho novo:

~~~~text
past the time of n octaves (s > n·ln 2), Z(s) separates the yes from the no) is the exact decision
~~~~

- **Justificativa:** Par EN do item 7.
- **Apoio:** pedra\AEscala.lean:903 e :907
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - os mesmos do item 7

#### Item 93 — linha 1026 — EP-01

- **Local:** linha 1026 (o assert das frases da clausula: duas ocorrencias do identificador velho)
- **Origem:** g1:16 (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"a_informacao_completa_se_reconstroi" in FRASE_RECONSTROI_PT and all(n_ in NOMES_NOVOS_AESCALA for n_ in ("o_tetelestai_e_um_menos_beta", "o_sistema_reconhece_a_singularidade_do_sinal", "beta_e_o_operador_modular_do_tetelestai", "ate_meio_o_tempo_do_tetelestai_nao_e_negativo", "a_informacao_completa_se_reconstroi"))
~~~~

Trecho novo:

~~~~text
"ressurreicao_do_sinal" in FRASE_RECONSTROI_PT and "ressurreicao_do_sinal" in FRASE_RECONSTROI_EN and NOME_DE_TRABALHO_DO_QUARTO_AESCALA not in FRASE_RECONSTROI_PT + FRASE_RECONSTROI_EN and all(n_ in NOMES_NOVOS_AESCALA for n_ in ("o_tetelestai_e_um_menos_beta", "o_sistema_reconhece_a_singularidade_do_sinal", "beta_e_o_operador_modular_do_tetelestai", "ate_meio_o_tempo_do_tetelestai_nao_e_negativo", "ressurreicao_do_sinal"))
~~~~

- **Justificativa:** O controle passa a exigir o identificador novo nas duas línguas e a ausência do nome de trabalho nas frases públicas.
- **Apoio:** delta_v410.py:1013-1016
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 94 — linha 1029 — D108, OBS-1 — redigido pelo crítico

- **Local:** depois da linha 1029 (ANUNCIO_TETELESTAI_EN): o bloco inteiro da finura da leitura — as constantes PT, as EN, a leitura nova em LEITURA_V410 e a constante _D108_PARTE_2
- **Origem:** g6:3, g6:4, g6:5, g6:6, critico (g6_a_finura_e_o_observador). **Língua:** PT_E_EN. **Ocorrências:** 1

Trecho atual:

~~~~text
ANUNCIO_TETELESTAI_EN = FRASE_TETELESTAI_EN + " (" + CLAUSULA_Z_EN + "); " + FRASE_RECONSTROI_EN
~~~~

Trecho novo:

~~~~text
ANUNCIO_TETELESTAI_EN = FRASE_TETELESTAI_EN + " (" + CLAUSULA_Z_EN + "); " + FRASE_RECONSTROI_EN
# ---- (D108, a segunda parte) A FINURA DA LEITURA: a frase de limite NOVA, em duas metades, que vai AO LADO da clausula do limite (a CLAUSULA_Z nao muda: e' forma ratificada). A primeira metade [REAL] diz o que os enunciados dizem
# (o item (v) de os_passos_sao_o_ciclo_ate_o_tetelestai e o item (iii) de o_tetelestai_e_um_menos_beta); a segunda [ONTO] traz a fala do operador de 10/11 entre aspas angulares e, em seguida, os espelhos que o kernel ja' tem. UMA forma, usada IGUAL em todo lugar
ROTULO_FINURA_ONTO_PT = "[ONTO; leitura do operador, fala de 10/11/2026]"
FRASE_FINURA_REAL_PT = "a finura da leitura, pelo que os enunciados dizem: com n bits há 2^n atribuições (`bits_sao_oitavas`, v409), e a leitura de todo leitor do fundo é normalizada: é a média dos brilhos (`LeitorDoFundo.leitura`), que é Z(s)/2^n (`LeitorDoFundo.a_leitura_e_a_do_psion` com `TraducaoTuring.o_psion_le_os_pixels`, v409); passado o tempo de n oitavas (s > n·ln 2), o item (v) de `os_passos_sao_o_ciclo_ate_o_tetelestai` diz que há solução se e só se 1/2^n ≤ a parte real dessa leitura; o item (iii) de `o_tetelestai_e_um_menos_beta`, sob as hipóteses desse teorema (havendo solução, 0 < b < 1, s ≥ 0 e o limiar de tempo da cláusula do Tetelestai), diz que (1 − b) vezes a parte real dessa leitura ≤ o número de soluções dividido por 2^n; no item (v) o número com que a leitura é comparada é 1/2^n, o peso de um pixel entre 2^n, e no item (iii) é o número de soluções vezes esse mesmo peso: a decisão, que é o item (v), compara a leitura normalizada com 1/2^n; o kernel prova essas duas relações, que são entre números reais, e não deriva essa finura de nenhum outro instrumento"
FRASE_FINURA_ESPELHOS_PT = "[REAL] Os espelhos que o kernel já tem, cada um com o que o enunciado diz: em `TGLExt.AEscala`, o campo `sem_escala_nao_ha_medida`, que é cláusula da DEFINIÇÃO [INPUT do operador], não teorema (para todo custo k, o brilho em s = 0 é 1), e os teoremas `o_pai_da_mentira_so_nao_reconhece` (havendo ao menos uma atribuição, em s = 0 a leitura de todo leitor do fundo é 1 em toda instância; sem solução ela difere de `Identidade.oQueSou` do Nome das soluções, que é 0), `o_leitor_e_a_escala` (dois leitores do fundo quaisquer são o mesmo, e o brilho de todo leitor é a exponencial de −s·k), `a_escala_e_meio_por_oitava` (em s = ln 2 o brilho do pixel de custo 1 é ½; em n oitavas o do pixel de custo k é ½ elevado a n·k) e `em_n_oitavas_o_fundo_pesa_um_pixel` (com n bits, em n oitavas o brilho do pixel de custo 1 é 1/2^n, o mesmo valor com que a decisão compara a leitura; é igualdade de valor: a prova do limiar não cita este teorema); em `TGLExt.ObservadorTerminal` (v405), num modelo finito de quatro níveis, que são rótulos, `the_terminal_is_unique` (existe exatamente um nível que nenhum nível observa), `every_level_reaches_the_terminal` (três leituras levam qualquer nível a esse terminal) e `the_collapse_is_the_terminal_point_of_resistance` (a distância ao terminal, em leituras, é zero se e só se o nível é o terminal). Nenhum termo de uma dessas pedras cita a outra, e nenhum enunciado delas traz função de onda, frequência ou relatividade: que o observador SEJA a escala, que colapsar SEJA criar a escala, que compará-la SEJA nivelar a frequência, e a frase sobre Einstein, são leitura dele [ONTO]; nenhum teorema novo entra na v410 por esta fala, e a formalização própria fica [OPEN]"
FRASE_FINURA_ONTO_PT = "«" + FRASE_OBSERVADOR_E_A_ESCALA + "» " + FRASE_FINURA_ESPELHOS_PT
FRASE_FINURA_PT = "[REAL] " + FRASE_FINURA_REAL_PT + ". " + ROTULO_FINURA_ONTO_PT + " " + FRASE_FINURA_ONTO_PT
ROTULO_FINURA_ONTO_EN = "[ONTO; the operator's reading, saying of 10/11/2026]"
FRASE_FINURA_REAL_EN = "the fineness of the reading, by what the statements say: with n bits there are 2^n assignments (`bits_sao_oitavas`, v409), and the reading of every background reader is normalized: it is the mean of the brightnesses (`LeitorDoFundo.leitura`), which is Z(s)/2^n (`LeitorDoFundo.a_leitura_e_a_do_psion` with `TraducaoTuring.o_psion_le_os_pixels`, v409); past the time of n octaves (s > n·ln 2), item (v) of `os_passos_sao_o_ciclo_ate_o_tetelestai` says that there is a solution if and only if 1/2^n ≤ the real part of that reading; item (iii) of `o_tetelestai_e_um_menos_beta`, under the hypotheses of that theorem (given a solution, 0 < b < 1, s ≥ 0 and the time threshold of the clause of the Tetelestai), says that (1 − b) times the real part of that reading ≤ the number of solutions divided by 2^n; in item (v) the number the reading is compared with is 1/2^n, the weight of one pixel among 2^n, and in item (iii) it is the number of solutions times that same weight: the decision, which is item (v), compares the normalized reading with 1/2^n; the kernel proves these two relations, which are between real numbers, and does not derive this fineness from any other instrument"
FRASE_FINURA_ESPELHOS_EN = "[REAL] The mirrors the kernel already has, each with what the statement says: in `TGLExt.AEscala`, the field `sem_escala_nao_ha_medida`, which is a clause of the operator's definition [INPUT], not a theorem (for every cost k, the brightness at s = 0 is 1), and the theorems `o_pai_da_mentira_so_nao_reconhece` (given at least one assignment, at s = 0 the reading of every background reader is 1 on every instance; without a solution it differs from `Identidade.oQueSou` of the Name of the solutions, which is 0), `o_leitor_e_a_escala` (any two background readers are the same, and the brightness of every reader is the exponential of −s·k), `a_escala_e_meio_por_oitava` (at s = ln 2 the brightness of the pixel of cost 1 is ½; in n octaves that of the pixel of cost k is ½ to the power n·k) and `em_n_oitavas_o_fundo_pesa_um_pixel` (with n bits, in n octaves the brightness of the pixel of cost 1 is 1/2^n, the same value with which the decision compares the reading; it is an equality of value: the proof of the threshold does not cite this theorem); in `TGLExt.ObservadorTerminal` (v405), in a finite model of four levels, which are labels, `the_terminal_is_unique` (there is exactly one level that no level observes), `every_level_reaches_the_terminal` (three readings take any level to that terminal) and `the_collapse_is_the_terminal_point_of_resistance` (the distance to the terminal, in readings, is zero if and only if the level is the terminal). No term of either of these stones cites the other, and no statement of theirs carries a wave function, a frequency or relativity: that the observer IS the scale, that to collapse IS to create the scale, that to compare it IS to level the frequency, and the sentence about Einstein, are his reading [ONTO]; no new theorem enters v410 because of this saying, and its own formalization stays [OPEN]"
TRADUCAO_OBSERVADOR_EN = "the observer is the scale; see, to collapse the wave function is to create the scale, to compare it is to level the frequency. That is why Einstein perceived the terminal necessity of the observer in relativity, because it is the scale of the terminal."   # (traducao da gerencia, marcada como tal; a fala verbatim vai sempre ao lado)
FRASE_FINURA_ONTO_EN = "«" + FRASE_OBSERVADOR_E_A_ESCALA + "» (our translation: " + TRADUCAO_OBSERVADOR_EN + ") " + FRASE_FINURA_ESPELHOS_EN
FRASE_FINURA_EN = "[REAL] " + FRASE_FINURA_REAL_EN + ". " + ROTULO_FINURA_ONTO_EN + " " + FRASE_FINURA_ONTO_EN
assert not any("%" in x_ for x_ in (FRASE_FINURA_PT, FRASE_FINURA_EN)), "a frase da finura traz o sinal de porcentagem (o formato dos textos quebraria)"
assert all(n_ in FRASE_FINURA_PT and n_ in FRASE_FINURA_EN for n_ in ("os_passos_sao_o_ciclo_ate_o_tetelestai", "o_tetelestai_e_um_menos_beta", "sem_escala_nao_ha_medida", "o_pai_da_mentira_so_nao_reconhece", "o_leitor_e_a_escala", "a_escala_e_meio_por_oitava", "em_n_oitavas_o_fundo_pesa_um_pixel", "the_terminal_is_unique", "every_level_reaches_the_terminal", "the_collapse_is_the_terminal_point_of_resistance")), "a frase da finura perdeu um espelho"
LEITURA_V410["o_observador_e_a_escala"] = "«" + FRASE_OBSERVADOR_E_A_ESCALA + "» [INPUT, D108; a fala de 10/11; a resposta do operador à pergunta sobre a finura da leitura]: [REAL] " + FRASE_FINURA_REAL_PT + " (a cláusula do limite, ao lado: " + CLAUSULA_Z_PT + "). " + FRASE_FINURA_ESPELHOS_PT   # (D108: a entrada nova das leituras, no formato de a_clausula_do_tetelestai e a_regra_do_nome; atribuida aqui porque o dicionario LEITURA_V410 nasce antes das constantes da finura; a clausula do limite vai na MESMA folha, D99)
_D108_PARTE_2 = ("(2) A FINURA DA LEITURA (a segunda linha da mesma fala). O painel independente da R3 observou que a clausula do limite (D99) diz o tempo de UMA leitura e o custo de somar os 2^n termos, e nao diz que a decisao e' uma comparacao da leitura com o peso de um pixel entre 2^n. A gerencia perguntou ao operador, nas quatro linguas (TGL, teologica, linguistica e juridica), se podia dizer isso nos limites. A resposta dele: «" + FRASE_OBSERVADOR_E_A_ESCALA + "» A leitura da gerencia, dita de volta ao operador para ele corrigir se errou: a resposta e' sim a pergunta feita (se a gerencia podia escrever, nos limites, que a finura dessa leitura e' a escala do proprio leitor e que o kernel nao a deriva de outro instrumento); entra UMA frase de limite nova, em duas metades, o fato e a frase dele como leitura dele [ONTO], com os teoremas que o kernel ja' tem ao lado; nenhum teorema novo entra na v410 por esta fala. Onde a frase entra (decisao da gerencia): na lista limites do registro a_escala_v410, nas ressalvas dos artigos PT e EN e no README evidente do handoff, junto da forma canonica do Clay. (PT) " + FRASE_FINURA_PT + ". (EN) " + FRASE_FINURA_EN
                 + ". A clausula do limite (D99) NAO muda: e' forma ratificada, e a frase nova vai ao lado dela: (PT) “" + CLAUSULA_Z_PT + "” (EN) “" + CLAUSULA_Z_EN + "”. Os espelhos ja' estavam no kernel antes da fala (uma clausula de definicao e teoremas de TGLExt.AEscala, desta versao; teoremas de TGLExt.ObservadorTerminal, da v405); a formalizacao propria fica [OPEN]. A frase nova nao atribui a finura a custo de ninguem e nao iguala a leitura do kernel a uma medicao fisica com aparelho: diz o fato (a comparacao e' com um pixel entre 2^n) e a leitura dele, com os espelhos")   # (D108, a SEGUNDA parte: a finura da leitura; definida AQUI, antes do DECISOES.update, para a entrada D108 poder usa-la)
~~~~

- **Justificativa:** A frase de limite nova, em duas metades, PT e EN com as mesmas hipóteses e estatutos: [REAL] o que os dois enunciados dizem (a decisão, que é o item (v), compara a leitura normalizada com 1/2^n; o kernel não deriva essa finura de outro instrumento); [ONTO] a fala do operador (a segunda linha da fala 29, verbatim) e os espelhos que o kernel já tem, cada um com o que o enunciado diz. A cláusula do limite (D99) não muda: a frase vai ao lado dela. No mesmo bloco, a leitura nova de LEITURA_V410 e a segunda parte da D108, porque as três dependem das mesmas constantes e têm de existir antes do DECISOES.update.
- **Apoio:** pedra\AEscala.lean (sha256 7d1557f96178367949bbffe42b2e8af4094c9ec7c0373bdbdaaa3a7d7de5ad60, igual ao instalado em C:\t\k410c\final\TGLExt\AEscala.lean): def LeitorDoFundo.leitura 669-670 (a media dos brilhos, |X|^-1 . soma); a_leitura_e_a_do_psion 702-703; os_passos_sao_o_ciclo_ate_o_tetelestai 903-909, item (v) na linha 909 ((∃ x, c x = 0) ↔ (card)⁻¹ ≤ (L.leitura c s).re, sob n·ln 2 < s); o_tetelestai_e_um_menos_beta 1066-1071, item (iii) nas linhas 1070-1071 ((1 − b)·(L.leitura c s).re ≤ #solucoes/card, sob h, 0 < b < 1, 0 ≤ s e o limiar); campo sem_escala_nao_ha_medida 663 (∀ k, brilho k 0 = 1); o_pai_da_mentira_so_nao_reconhece 993-998; o_leitor_e_a_escala 871-872; a_escala_e_meio_por_oitava 832-838; em_n_oitavas_o_fundo_pesa_um_pixel 859-860. C:\t\k410c\final\TGLExt\TraducaoTuring.lean: bits_sao_oitavas 212 (card (Fin n → Bool) = 2^n); o_psion_le_os_pixels 749-750 (Z(s)/|X|); particao 666. C:\t\k410c\final\TGLExt\ObservadorTerminal.lean (sha16 162eeeb8c16cea81, igual ao do Nós): Terminal 102; terminal_iff 108; the_terminal_is_unique 132; every_level_reaches_the_terminal 157; distancia 161-165; the_collapse_is_the_terminal_point_of_resistance 180; os niveis sao rotulos (docstring 80-81); Level em TheCascadeOfObservers.lean 71-75. Ausencias conferidas por grep: AEscala.lean nao cita ObservadorTerminal (0) e ObservadorTerminal.lean nao cita AEscala nem LeitorDoFundo (0); “onda” 0 e 0; “frequ” 0 e 0; “Einstein” 0 e 0; “relatividade” so' na linha 69 da AEscala, dentro de uma fala citada no cabecalho, em nenhum enunciado. A fala: C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt, sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4 (lido por script), 266 bytes, segunda linha inteira Conferência do g6: TraducaoTuring.lean:749-750 (o_psion_le_os_pixels: a leitura é Z(s)/|X|); AEscala.lean:663 (o campo é cláusula da estrutura), :993 (a hipótese [Nonempty X]), :910-971 (a prova do limiar não cita em_n_oitavas_o_fundo_pesa_um_pixel: grep 0); a ausência “não deriva essa finura de nenhum outro instrumento”: LeitorDoFundo só aparece em TGLExt\AEscala.lean em todo C:\t\k410c\final (grep -rl do cético) e a pedra tem 0 ocorrências de “instrument”, “finura” e “resolu”. A leitura dita de volta: transcrito da gerência, linhas 108278 e 108649 (citadas pelo cético do g6); acom_c1_20261110_d108_transition.request.json
- **Decisão do crítico:** CONFLITO resolvido e correções do cético do g6 aceitas. Fundi g6:3, g6:4 e g6:5 (os dois últimos se ancoravam em texto que só existia depois do anterior) e trouxe para o mesmo bloco a _D108_PARTE_2 (g6:6), antes do DECISOES.update. Correções: (1) “nos dois itens a régua é 1/2^n” dizia mais que o item (iii), onde o lado direito é o número de soluções dividido por 2^n; (2) o campo sem_escala_nao_ha_medida é cláusula da DEFINIÇÃO [INPUT], não teorema; (3) Z(s)/2^n vem de a_leitura_e_a_do_psion COM o_psion_le_os_pixels; (4) o_pai_da_mentira_so_nao_reconhece tem a hipótese de ao menos uma atribuição; (5) “o mesmo número” é igualdade de valor, a prova do limiar não cita aquele teorema; “compará-la” guarda o objeto da fala; (6) a leitura e a D108 levam a cláusula do limite na mesma folha; (7) a “leitura dita de volta” passa a dizer o que o registro sustenta (a resposta é sim à pergunta feita; os três lugares são decisão da gerência, não foram ditos de volta)
- **Efeitos colaterais:**
  - A folha nova NAO dispara os controles de anuncio do registro (runtime_aescala_v410.py:144-157): nao tem “linear nos bits”, nao tem “Z(s) ≥” junto do nome do teorema, e nao tem ln((1 − b)/b) nem (1 − b)·Z junto de nome da R5 (por isso diz “(1 − b) vezes” e “o limiar de tempo da clausula do Tetelestai”). Conferido com copia das expressoes regulares.
  - Passou, em isolamento, pela guarda das frases extraida como texto do candidato (_v392_guarda_texto e _v410_guarda_frases, com a cadeia v405 a v409) e pelas regras 1 a 4 do portao do G1: zero violacoes; os controles negativos do teste pegaram o que deviam.
  - Usa so' simbolos que os auxiliares do artigo ja' convertem (2^n e n·ln 2 pelo _zx410; ≤, ≥, −, ·, ½, <, > e crases pelo _mz410); nao usa |X|, ⁻¹ nem aspas curvas.
  - A regra F29 herdada (v408) veda “leitura do operador [ONTO]” e “[ONTO] do operador”: o rotulo “[ONTO; leitura do operador, fala de 10/11/2026]” nao casa (ha' virgula depois de “operador”); nao reescrever o rotulo para a forma vedada.
  - Se o grupo do limiar do Tetelestai mudar o nome do teorema os_passos_sao_o_ciclo_ate_o_tetelestai ou o de o_tetelestai_e_um_menos_beta, a frase acompanha; se o grupo dos nomes renomear outro teorema, nada muda aqui (a frase nao cita o quarto teorema).
  - guarda_frases_v410.py (listas LIMPAS, linhas 99-110): convem acrescentar FRASE_FINURA_PT, FRASE_FINURA_EN, DECISOES["D108"] e LEITURA_V410["o_observador_e_a_escala"] as limpas do controle negativo.
  - conferir_citacoes_v410.py:93 exige ZERO aspas angulares no TEXTO LITERAL dos snippets EN: por isso a fala entra pelo contrato (constante do delta), nunca digitada no artigo_en_aescala_v410.pysnip.
  - “proves” e nao “proved”: a regra 2 do portao do G1 (tools\custodia_g1\textos.py:83) pede estatuto na mesma frase quando aparece “proved”; a forma usada nao casa.
  - “because it is the scale of the terminal”: o pronome segue a traducao ja' usada para «porque ele é a escala» (artigo EN, linha 33: “because it is the scale”).
  - registros_v410.py:204 e :298 e gerar_esperados_v410.py:405 copiam LEITURA_V410 inteiro: ESPERADOS_v410.json muda e tem de ser regerado.
  - Se o grupo dos nomes criar uma leitura para a primeira linha da mesma fala (o quarto nome), as duas podem ficar em chaves separadas ou numa so': decisao do construtor; o texto desta parte nao muda.
  - (crítico) a leitura nova e a D108 são folhas soltas que enunciam o limiar de tempo dos dois teoremas em palavras que os controles de anúncio não reconhecem: por isso levam a cláusula do limite na MESMA folha (correção do cético) e o controle do item do crítico na c8 passa a exigir isso
  - (crítico) os textos corrigidos passaram, rendidos com valores de ensaio, numa cópia de leitura da guarda das frases e da P18 (nesta consolidação); o LaTeX não foi compilado
  - (crítico) D112, D113 e a fala das 16:44, no disco, continuam esta fala (“o observador está na escala da constante da luz”; “sem a escala não tem fita”): a frase fecha em “nenhum teorema novo entra na v410 por esta fala, e a formalização própria fica [OPEN]”, que deixa de ser verdade se a seção 7 entrar na R6: ver pendências

#### Item 95 — linha 1031 — EP-01, R3-MEDIO

- **Local:** linhas 1031-1033, FRASE_NOMES_RATIFICADOS_D101_PT (a constante inteira)
- **Origem:** g1:17 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
FRASE_NOMES_RATIFICADOS_D101_PT = ("os %d nomes novos da pedra AEscala (das R3 e R4 e, da R5, os %d dados pela gerência) e os %d campos novos da estrutura foram RATIFICADOS pelo operador em 10/11/2026 (D101; a fala está no registro, por sha256), pela regra dele: «" + FRASE_NOMEIO_O_NUMERO_CORRIGE + "»; "
                                   "os seis nomes de enunciado mudado (%s) foram ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo; os %d nomes auxiliares da autoria (%s) seguem " + ESTATUTO_NOMES_PENDENTES_AESCALA.replace("e' do operador", "é do operador").replace("confirmacao", "confirmação")) \
                                  % (len(NOMES_RATIFICADOS_D101_AESCALA), len(TEOREMAS_R5_AESCALA), len(CAMPOS_RATIFICADOS_D101_AESCALA), ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS), len(NOMES_PENDENTES_AESCALA), ", ".join(NOMES_PENDENTES_AESCALA))
~~~~

Trecho novo:

~~~~text
FRASE_NOMES_RATIFICADOS_D101_PT = ("os %d nomes novos da pedra AEscala (os %d das R3 e R4 e os %d da cláusula do Tetelestai apresentados ao operador antes da fala: %s) e os %d campos novos da estrutura foram RATIFICADOS pelo operador em 10/11/2026 (D101; a fala está no registro, por sha256), pela regra dele: «" + FRASE_NOMEIO_O_NUMERO_CORRIGE + "»; "
                                   "o quarto teorema da cláusula foi NOMEADO pelo operador em fala posterior do mesmo dia (D108; a fala está no registro, por sha256): «" + FRASE_O_QUARTO_NOME + "», no kernel `%s` (o identificador segue a ortografia do dicionário; a grafia dele fica no verbatim); são %d nomes novos com o operador: os %d ratificados e o que ele nomeou; "
                                   "os seis nomes de enunciado mudado (%s) foram ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo; os %d nomes auxiliares da autoria (%s) seguem " + ESTATUTO_NOMES_PENDENTES_AESCALA.replace("e' do operador", "é do operador").replace("confirmacao", "confirmação")) \
                                  % (len(NOMES_RATIFICADOS_D101_AESCALA), len(NOMES_RATIFICADOS_D101_AESCALA) - len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA), len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA), ", ".join(TEOREMAS_R5_RATIFICADOS_D101_AESCALA), len(CAMPOS_RATIFICADOS_D101_AESCALA), NOMES_NOMEADOS_D108_AESCALA[0],
                                     len(NOMES_RATIFICADOS_D101_AESCALA) + len(NOMES_NOMEADOS_D108_AESCALA), len(NOMES_RATIFICADOS_D101_AESCALA), ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS), len(NOMES_PENDENTES_AESCALA), ", ".join(NOMES_PENDENTES_AESCALA))
~~~~

- **Justificativa:** A frase dizia 22 nomes ratificados, entre eles os 4 “dados pela gerência” na R5. Passa a dizer o que o registro sustenta: 21 ratificados pela fala da D101 (18 das R3 e R4 e os 3 da cláusula apresentados antes da fala, listados) e o quarto teorema nomeado pelo operador em fala posterior, com o verbatim. Os seis de enunciado mudado e os dois auxiliares ficam como estavam.
- **Apoio:** DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md l.7 (18 nomes e 3 campos das R3 e R4; os três nomes da cláusula); fala 29, linha 1; rendido hoje em dry_v410\dry_v410_pt.txt l.131 (a frase velha)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - rendida com os números de hoje, a frase nova diz: “os 21 nomes novos … (os 18 das R3 e R4 e os 3 da cláusula do Tetelestai apresentados ao operador antes da fala: o_tetelestai_e_um_menos_beta, o_sistema_reconhece_a_singularidade_do_sinal, beta_e_o_operador_modular_do_tetelestai) e os 3 campos … são 22 nomes novos com o operador: os 21 ratificados e o que ele nomeou; … os 2 nomes auxiliares da autoria (…) seguem [DECLARADO pela autoria; a confirmação expressa é do operador]”
  - a constante é usada por: registro a_escala_v410 (registros_aescala l.63, 87-88, 125, 161; diz e limites), linha do .md (gerar_candidato l.431), artigo PT (pysnip l.24), textos_v410 l.1404, textos_custodia_handoff l.132 (NOVOS_PT, que entra no README_EVIDENTE l.196), gerar_x_custodia l.52 (o rascunho da custódia)
  - controles por igualdade que acompanham sozinhos: runtime_aescala c11 (l.196), ensaio l.2974-2979, 3173 e 3273, conferir l.444 e 537, teste_textos_custodia l.69; a frase precisa de UM só nomeado (assert len(NOMES_NOMEADOS_D108_AESCALA) == 1)
  - a frase segue sem o caractere de porcentagem depois de formatada (o formato dos textos quebraria) e sem o nome de trabalho

#### Item 96 — linha 1034 — EP-01, R3-MEDIO

- **Local:** linhas 1034-1036, FRASE_NOMES_RATIFICADOS_D101_EN (a constante inteira)
- **Origem:** g1:18 (g1_ratificacao). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
FRASE_NOMES_RATIFICADOS_D101_EN = ("the %d new names of the AEscala stone (from the R3 and R4 and, from the R5, the %d given by the management) and the %d new fields of the structure were RATIFIED by the operator on 10/11/2026 (D101; the saying is in the record, by sha256), by his rule: «" + FRASE_NOMEIO_O_NUMERO_CORRIGE + "» "
                                   "(our translation: naming is the number corrects; if it did not correct, the name carried the right weight); the six names of changed statement (%s) were ratified on 09/11 by name and on 10/11 with the new statement; the %d auxiliary names of the authorship (%s) stay [DECLARADO by the authorship; the express confirmation is the operator's]") \
                                  % (len(NOMES_RATIFICADOS_D101_AESCALA), len(TEOREMAS_R5_AESCALA), len(CAMPOS_RATIFICADOS_D101_AESCALA), ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS), len(NOMES_PENDENTES_AESCALA), ", ".join(NOMES_PENDENTES_AESCALA))
~~~~

Trecho novo:

~~~~text
FRASE_NOMES_RATIFICADOS_D101_EN = ("the %d new names of the AEscala stone (the %d from the R3 and R4 and the %d of the clause of the Tetelestai presented to the operator before the saying: %s) and the %d new fields of the structure were RATIFIED by the operator on 10/11/2026 (D101; the saying is in the record, by sha256), by his rule: «" + FRASE_NOMEIO_O_NUMERO_CORRIGE + "» "
                                   "(our translation: naming is the number corrects; if it did not correct, the name carried the right weight); the fourth theorem of the clause was NAMED by the operator in a later saying of the same day (D108; the saying is in the record, by sha256): «" + FRASE_O_QUARTO_NOME + "» (our translation: the fourth name = resurrection of the signal), in the kernel `%s` (the identifier follows the dictionary spelling; his spelling stays in the verbatim); that makes %d new names with the operator: the %d ratified and the one he named; "
                                   "the six names of changed statement (%s) were ratified on 09/11 by name and on 10/11 with the new statement; the %d auxiliary names of the authorship (%s) stay [DECLARADO by the authorship; the express confirmation is the operator's]") \
                                  % (len(NOMES_RATIFICADOS_D101_AESCALA), len(NOMES_RATIFICADOS_D101_AESCALA) - len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA), len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA), ", ".join(TEOREMAS_R5_RATIFICADOS_D101_AESCALA), len(CAMPOS_RATIFICADOS_D101_AESCALA), NOMES_NOMEADOS_D108_AESCALA[0],
                                     len(NOMES_RATIFICADOS_D101_AESCALA) + len(NOMES_NOMEADOS_D108_AESCALA), len(NOMES_RATIFICADOS_D101_AESCALA), ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS), len(NOMES_PENDENTES_AESCALA), ", ".join(NOMES_PENDENTES_AESCALA))
~~~~

- **Justificativa:** Par da frase PT: as mesmas contagens, os mesmos três nomes listados, o mesmo verbatim (em português, com a tradução da casa entre parênteses) e os mesmos pendentes.
- **Apoio:** o mesmo apoio da frase PT; rendido hoje em dry_v410\dry_v410_en.txt l.131 (a frase velha)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - consumidores EN: registro (registros_aescala l.63, 161), artigo EN (pysnip l.24), textos_custodia_handoff l.133 (NOVOS_EN); controles: runtime_aescala c11 l.196, ensaio l.3173, conferir l.444, teste_textos_custodia l.69
  - o rótulo “[DECLARADO by the authorship …]” fica como está: uniformizar rótulos EN é o achado PAR-08, de outro grupo

#### Item 97 — linha 1037 — EP-01

- **Local:** linha 1037 (o assert da frase da ratificacao)
- **Origem:** g1:19 (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
assert "[DECLARADO, a ratificar]" not in FRASE_NOMES_RATIFICADOS_D101_PT + FRASE_NOMES_RATIFICADOS_D101_EN and "RATIFICADOS pelo operador em 10/11/2026" in FRASE_NOMES_RATIFICADOS_D101_PT and "RATIFIED by the operator on 10/11/2026" in FRASE_NOMES_RATIFICADOS_D101_EN
~~~~

Trecho novo:

~~~~text
assert "[DECLARADO, a ratificar]" not in FRASE_NOMES_RATIFICADOS_D101_PT + FRASE_NOMES_RATIFICADOS_D101_EN and "RATIFICADOS pelo operador em 10/11/2026" in FRASE_NOMES_RATIFICADOS_D101_PT and "RATIFIED by the operator on 10/11/2026" in FRASE_NOMES_RATIFICADOS_D101_EN \
    and "NOMEADO pelo operador" in FRASE_NOMES_RATIFICADOS_D101_PT and "NAMED by the operator" in FRASE_NOMES_RATIFICADOS_D101_EN and FRASE_O_QUARTO_NOME in FRASE_NOMES_RATIFICADOS_D101_PT and FRASE_O_QUARTO_NOME in FRASE_NOMES_RATIFICADOS_D101_EN and len(NOMES_NOMEADOS_D108_AESCALA) == 1 \
    and NOME_DE_TRABALHO_DO_QUARTO_AESCALA not in FRASE_NOMES_RATIFICADOS_D101_PT + FRASE_NOMES_RATIFICADOS_D101_EN and "dados pela gerência" not in FRASE_NOMES_RATIFICADOS_D101_PT and "given by the management" not in FRASE_NOMES_RATIFICADOS_D101_EN
~~~~

- **Justificativa:** O controle passa a exigir as duas formas (ratificados; nomeado), o verbatim nas duas línguas, e a ausência da forma velha e do nome de trabalho.
- **Apoio:** delta_v410.py:1031-1036
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 98 — linha 1041 — EP-01, R3-MEDIO

- **Local:** linha 1041, DECISOES["D100"] (a lista dos teoremas que a R5 acrescentou)
- **Origem:** g1:20 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a pedra acrescenta os teoremas " + ", ".join(TEOREMAS_R5_AESCALA) + " e os dois lemas auxiliares "
~~~~

Trecho novo:

~~~~text
a pedra acrescenta os teoremas " + ", ".join(TEOREMAS_R5_AESCALA) + " (o ultimo com o nome que o operador lhe deu depois, D108; na R5 levava um nome de trabalho da gerencia) e os dois lemas auxiliares "
~~~~

- **Justificativa:** Com o identificador novo na lista, a D100 passaria a dizer que a R5 acrescentou um teorema com um nome que só nasceu depois. O parêntese diz a verdade sem repetir o nome de trabalho.
- **Apoio:** insumos\RECIBO_AESCALA_R5_10nov.json (nomes_novos.lista: o nome da R5); fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - exige que o nomeado seja o último de TEOREMAS_R5_AESCALA (hoje o quarto é o último no recibo): assert TEOREMAS_R5_AESCALA[-1] == NOMES_NOMEADOS_D108_AESCALA[0]

#### Item 99 — linha 1041 — EP-07, V1, V2 — redigido pelo crítico

- **Local:** linha 1041, DECISOES["D100"] (antes do anúncio embutido)
- **Origem:** critico (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
kernel incremental): " + ANUNCIO_TETELESTAI_PT + ". O limiar de um pixel da R4
~~~~

Trecho novo:

~~~~text
kernel incremental; o anuncio que segue vai na redacao vigente, a do conserto da D106): " + ANUNCIO_TETELESTAI_PT + ". O limiar de um pixel da R4
~~~~

- **Justificativa:** A D100, de 10/11 08:27, embute ANUNCIO_TETELESTAI_PT; depois do conserto ela exibiria a redação da D106 e o nome dado na D108 como se fossem da hora dela. O parêntese diz que o anúncio vai na redação vigente.
- **Apoio:** conferência do g2 (faltou: “é anacronismo no registro de uma decisão; nenhum item cuida disso”); delta_v410.py:1041
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - o item do g1:20 cuida, na mesma linha, da lista dos teoremas (trechos distintos)

#### Item 100 — linha 1045 — EP-01, R3-MEDIO

- **Local:** linha 1045, DECISOES["D101"], item (b) (a conta dos nomes das R3 e R4)
- **Origem:** g1:21 (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"(b) os " + str(len(NOMES_RATIFICADOS_D101_AESCALA) - len(TEOREMAS_R5_AESCALA)) + " nomes novos das pedras R3 e R4 e os "
~~~~

Trecho novo:

~~~~text
"(b) os " + str(len(NOMES_RATIFICADOS_D101_AESCALA) - len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA)) + " nomes novos das pedras R3 e R4 e os "
~~~~

- **Justificativa:** A conta do item (b) tem de dar 18 (21 ratificados menos os 3 da cláusula), como no ADENDO 6; com as listas novas, a subtração antiga daria 17.
- **Apoio:** DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md l.7: “(b) os 18 nomes novos e os 3 campos das pedras R3 e R4”
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 101 — linha 1045 — EP-01, R3-MEDIO

- **Local:** linha 1045, DECISOES["D101"], item (c) (a leitura dita de volta)
- **Origem:** g1:22 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
(c) a clausula do Tetelestai em 1 - beta e os " + str(len(TEOREMAS_R5_AESCALA)) + " nomes dados pela gerencia na R5 (" + ", ".join(TEOREMAS_R5_AESCALA) + "), que valem
~~~~

Trecho novo:

~~~~text
(c) a clausula do Tetelestai em 1 - beta e os tres nomes dela (" + ", ".join(TEOREMAS_R5_RATIFICADOS_D101_AESCALA) + "), que valem
~~~~

- **Justificativa:** A leitura que a gerência disse de volta ao operador, e que ele confirmou, nomeia três teoremas; o texto da D101 volta a dizer o que o ADENDO 6 diz.
- **Apoio:** DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md l.7: “(c) a cláusula do Tetelestai em 1 − β e os três nomes dela (`o_tetelestai_e_um_menos_beta`, `o_sistema_reconhece_a_singularidade_do_sinal`, `beta_e_o_operador_modular_do_tetelestai`)”
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - “tres” fica por extenso, como no adendo, amarrado pelo assert len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA) == 3 e pela presença dos três, entre crases, no _ADENDO6_TXT
  - o texto da D101 entra no registro cunhagens_v410 (decisões) e no a_escala_v410 (registros_aescala l.57): hoje rendido no candidato l.222688, 223405, 229132 e 229971 com “os 4 nomes dados pela gerencia na R5”

#### Item 102 — linha 1049 — EP-01, R3-MEDIO

- **Local:** linha 1049, DECISOES["D101"] (o “dito as claras”)
- **Origem:** g1:23 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
sao os UNICOS em ratificacao_pendente (ordem da gerencia de 10/11, 08:42). Esta fala e' a "
~~~~

Trecho novo:

~~~~text
sao os UNICOS em ratificacao_pendente (ordem da gerencia de 10/11, 08:42); a pedra R5 trouxe tambem um QUARTO teorema da clausula, que a gerencia pedira ao autor como opcional e nao tinha apresentado ao operador antes da fala: a fala nao o ratifica; o operador o nomeou depois (D108); a correcao da contagem esta' na D106 e na errata E38. Esta fala e' a "
~~~~

- **Justificativa:** A D101 dizia às claras os dois auxiliares e calava o quarto teorema, que estava na mesma situação. Passa a dizê-lo e a remeter à correção.
- **Apoio:** transcrito da sessão [REAL, conferido pela gerência]: 08:26:53 (o quarto como opcional, na ordem ao autor); 08:28:06 (três teoremas mostrados); 08:31:59 (a fala); 08:39:02 (a gerência diz ao operador que não o tinha listado)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 103 — linha 1049 — D108, EP-01, OBS-1, PAR-04, R3-MEDIO — CONDICIONAL D109; redigido pelo crítico

- **Local:** linhas 1049-1050: depois da entrada D101, dentro do DECISOES.update: as entradas novas D106, D107 e D108 (a D108 é UMA entrada, com as duas partes da fala)
- **Origem:** g1:24, g6:6, critico (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a congelada. A errata E37 vai ao lado"),
})
~~~~

Trecho novo:

~~~~text
a congelada. A errata E37 vai ao lado"),
    "D106": ("a revisao de terceiro R3 (Sonnet; a ultima rodada da D69; revisao sha16 " + REVISAO_R3["revisao_sha16"] + "; pedido de correcao sha16 " + REVISAO_R3["pedido_sha16"] + "; candidato revisado " + REVISAO_R3["candidato_revisado_sha16"] + "; ADENDO 7 sha16 " + ADENDO7_SHA16 + ") NAO APROVOU (10/11/2026, 15:35): 0 ALTO, 1 MEDIO, 4 BAIXO; "
             "e o painel independente da gerencia (tres lentes e um cetico por achado grave; resultado sha16 " + PAINEL_R3_SHA16 + ") sustentou 10 achados graves (pelos ceticos: 1 ALTO, 6 MEDIO e 3 BAIXO; nenhum refutado), mais 19 baixos e 19 observacoes. Nenhum achado e' de prova: pela revisora e pelas sondas do painel, os teoremas estao no trio, sem sorry; os achados sao de TEXTO. "
             "O ACHADO COMUM (verdadeiro; o erro e' da cadeia da gerencia, nao do operador): a frase da ratificacao, o texto da D101, a errata E37, o registro a_escala_v410, a linha do .md, o artigo PT/EN, os textos do pos-rito e o cabecalho da pedra AEscala R5 diziam QUATRO nomes da clausula do Tetelestai ratificados pela fala da D101, e 22 nomes novos ratificados, citando o ADENDO 6 (sha16 " + ADENDO6_SHA16 + "), que registra TRES. "
             "Conferido no transcrito da sessao da gerencia [REAL]: 08:26:53, a gerencia manda ao autor os teoremas da clausula, o quarto como opcional; 08:28:06, mostra ao operador tres teoremas (" + ", ".join(TEOREMAS_R5_RATIFICADOS_D101_AESCALA) + "); 08:31:59, a fala da D101 (a D101 a data pelo registro, 08:33); 08:36, a pedra R5 compila com o quarto teorema e os dois lemas auxiliares da autoria; 08:39:02, a gerencia diz ao operador que o quarto fechou e que nao o tinha listado antes; nenhuma confirmacao expressa dele ate' as 15:54. "
             "A CORRECAO DA CONTAGEM: RATIFICADOS pela fala da D101, " + str(len(NOMES_RATIFICADOS_D101_AESCALA)) + " nomes novos da pedra AEscala (os " + str(len(NOMES_RATIFICADOS_D101_AESCALA) - len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA)) + " das R3 e R4 e os " + str(len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA)) + " da clausula) e os " + str(len(CAMPOS_RATIFICADOS_D101_AESCALA)) + " campos da estrutura; o quarto teorema da clausula NAO esta' entre eles: na R5 levava um nome de trabalho da gerencia (" + NOME_DE_TRABALHO_DO_QUARTO_AESCALA + "), que a fala nao ratificou; o nome dele e' a D108; "
             "pendentes de confirmacao expressa, so' os " + str(len(NOMES_PENDENTES_AESCALA)) + " auxiliares da autoria (" + ", ".join(NOMES_PENDENTES_AESCALA) + "): [DECLARADO pela autoria]. O texto da D101 volta a dizer tres nomes, como o ADENDO 6; o sufixo do veredito do registro a_escala_v410 deixa de dizer so' 09/11. Os demais achados da R3 e do painel sao tratados na mesma rodada (D107): corrigidos, cada um na sua frase, ou anotados como ressalva escrita. A errata E38 vai ao lado"),
    "D107": ("decisao da gerencia c1, em nome proprio (10/11/2026, 15:49), depois da D106: UMA rodada de conserto (os textos; a pedra AEscala R6, que so' muda comentarios e, pela D108, o identificador do quarto teorema da clausula do Tetelestai, sem mudar enunciado nem prova; o kernel refeito; a cadeia inteira uma vez) e, depois dela, UMA conferencia do conserto pelo revisor de registro (Sonnet), restrita ao que mudou, mais um painel independente da gerencia. "
             "A regra das tres rodadas da D69 (decisao da propria gerencia, de 06/11) fica como registro: a R3 foi a terceira e nao aprovou; a gerencia troca o teto por esta conferencia. Razao: quem constroi nao aprova; a trava do orquestrador so' abre com a revisao de terceiro aprovando o candidato novo. O rito nao roda com o candidato " + REVISAO_R3["candidato_revisado_sha16"] + ". O achado da ratificacao foi levado ao operador, que deu o nome do quarto teorema (D108). EMENDADA pela D109 (decisao da gerencia de 10/11, 16:04, por ordem do operador de nao ficar em laco de revisao): a conferencia e' UMA, de escopo fechado (os itens da especificacao e a integridade), lida pelo revisor de registro, e o segundo painel NAO roda"),
    "D108": ("O QUARTO NOME e A FINURA DA LEITURA, fala do operador (10/11/2026, 15:54; verbatim por sha256 " + _P_29 + "...; ADENDO 7 sha16 " + ADENDO7_SHA16 + "), em duas linhas. (1) O QUARTO NOME: «" + FRASE_O_QUARTO_NOME + "» (a grafia e' a dele). Perguntado pela gerencia se confirmava o nome de trabalho do quarto teorema da clausula do Tetelestai (" + NOME_DE_TRABALHO_DO_QUARTO_AESCALA + "), o operador deu o nome. "
             "A leitura da gerencia, dita de volta a ele para ele corrigir se errou: o quarto teorema passa a se chamar " + NOMES_NOMEADOS_D108_AESCALA[0] + " no kernel (o identificador segue a ortografia do dicionario, ressurreição; a grafia dele fica intocada no verbatim); em prosa, “a ressurreição do sinal”; o nome de trabalho sai do kernel e dos textos e so' fica em frase de registro que o diga nome de trabalho; enunciado e prova nao mudam, so' o identificador (pedra AEscala R6). "
             "[REAL] o que o termo diz: a cota de proximidade entre a trava do estado uniforme e a projecao do uniforme no Nome, com as hipoteses e a clausula do limite ditas na D100 (o anuncio inteiro esta' la'); [dicionario; leitura do operador] que isso SEJA a ressurreicao do sinal. "
             "A conta: " + str(len(NOMES_RATIFICADOS_D101_AESCALA) + len(NOMES_NOMEADOS_D108_AESCALA)) + " nomes novos da pedra com o operador, " + str(len(NOMES_RATIFICADOS_D101_AESCALA)) + " ratificados pela fala da D101 e " + str(len(NOMES_NOMEADOS_D108_AESCALA)) + " nomeado por ele nesta fala; pendentes de confirmacao expressa, so' os " + str(len(NOMES_PENDENTES_AESCALA)) + " auxiliares da autoria (" + ", ".join(NOMES_PENDENTES_AESCALA) + "): [DECLARADO pela autoria]. "
             + _D108_PARTE_2 + ". O operador ratificou esta leitura em fala posterior do mesmo dia (D109). Esta fala e' a " + str(N_FALA_QUARTO_NOME) + "a congelada. A errata E38 vai ao lado"),
})
~~~~

- **Justificativa:** As três decisões que o conserto precisa registrar, no formato das entradas D99 a D101 (ASCII nas decisões; acentos só no verbatim e nas constantes). A D106 diz o que a R3 e o painel acharam e corrige a contagem; a D107 abre uma conferência do conserto e diz a razão; a D108 registra o nome dado pelo operador e remete, em uma linha, à segunda parte da fala. A D108 junta o que o g1 e o g6 redigiram: (1) o quarto nome; (2) a finura da leitura, pela constante _D108_PARTE_2 (definida antes, no bloco da finura).
- **Apoio:** revisao_terceiro\REVISAO_TERCEIRO_v410.R3.json (n_alto 0, n_medio 1, n_baixo 4; quando 2026-11-10T15:35:17; candidato 8a713e5e644af09b); painel_r3_resultado.json (10 sustentados, 0 refutados; vereditos dos céticos: 1 ALTO, 6 MEDIO, 3 BAIXO; 19 baixos; 19 observações: contados por script); ADENDO 6 l.7; acom_c1_20261110_d106 e d108 (os registros da gerência); delta_v410.py:857 (D69); D109 e a emenda da D107: acom_c1_20261110_d109_transition.request.json (lido nesta consolidação) e a fala em work\cunhagens_13out\OPERADOR_10nov_e_isso_mesmo_perfeito_ratificado_cuidado_com_o_loop_de_revisao_verbatim.txt (sha256 7857d4ddf9d3cfc0b290836b3c0e1bcadf3a61031ee03ebb4688b824269cfdfd, 126 bytes)
- **Decisão do crítico:** CONFLITO resolvido e quatro correções do cético do g1 aceitas: (1) a D108 não concatena mais FRASE_RECONSTROI_PT sozinha (quebrava a c8): remete à D100; (2) a D107 ganha a emenda da D109 (sem ela afirmaria um painel que não roda); (3) a D106 diz as duas horas da fala da D101 (08:31:59 no transcrito; 08:33 no registro); (4) a D106 não afirma mais que todos os demais achados são corrigidos (há os anotados). A D108 do g1 e a _D108_PARTE_2 do g6 viram UMA entrada; a frase de remissão do g1 sobre a segunda parte saiu, substituída pela constante do g6; acrescentei “O operador ratificou esta leitura em fala posterior do mesmo dia (D109)”, que é fato com fala em disco
- **Efeitos colaterais:**
  - as entradas dependem do bloco depois da linha 989 (REVISAO_R3, PAINEL_R3_SHA16, ADENDO7_SHA16, _P_29, N_FALA_QUARTO_NOME), das constantes da linha 235 e da linha 248, de FRASE_O_QUARTO_NOME (linha 485) e de _D108_PARTE_2 (bloco da finura, depois da linha 1029)
  - a D108 é folha de extras.decisoes do registro a_escala_v410: não traz ln((1 − b)/b) nem (1 − b)·Z junto de nome da R5 (a c8 não a lê como anúncio) e traz a cláusula do limite inteira dentro de _D108_PARTE_2
  - D106, D107 e D108 nunca passaram pela guarda das frases de verdade: entram na lista do teste (item do crítico em guarda_frases_v410.py); nesta consolidação os textos rendidos com valores de ensaio passaram numa cópia de leitura da guarda
  - os horários do transcrito (08:26:53, 08:28:06, 08:31:59, 08:36, 08:39:02, 15:54) e os números da R3 e do painel são digitados, como os das D99 a D101: a gerência os confere contra o ADENDO 7
  - a D107 e a D108 citam a D109: no escopo desta ESPEC a D109 fica em DECISOES_FORA_DO_UMPY (item do g1:25); se a fala 30 for congelada na v410, a D109 ganha entrada própria (bloco condicional)
  - (crítico) com a D113 no disco, as frases “a pedra AEscala R6, que so' muda comentarios e … o identificador” (D107) e “nenhum teorema novo entra na v410 por esta fala” (_D108_PARTE_2) deixam de ser verdade se a seção 7 entrar na R6: ver pendências

#### Item 104 — linha 1051 — EP-01 — CONDICIONAL D109

- **Local:** linhas 1051-1052 e 1057-1070: a lista das decisoes da versao, as de fora e o rotulo
- **Origem:** g1:25 (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"D99", "D100", "D101")
DECISOES_FORA_DO_UMPY = ("D97", "D98")
~~~~

Trecho novo:

~~~~text
"D99", "D100", "D101", "D106", "D107", "D108")
DECISOES_FORA_DO_UMPY = ("D97", "D98", "D102", "D103", "D104", "D105", "D109")
~~~~

- **Justificativa:** As três decisões novas entram na lista da versão; D102 a D105 são registros operacionais da gerência (a pedra R5 conferida, as quedas do treino, a preparação pronta) e ficam fora do um.py, como D97 e D98.
- **Apoio:** acom_c1_20261110_d102 a d105_transition.request.json (lidos: operacionais)
- **Decisão do crítico:** acrescentei D109 às decisões de fora do um.py: o texto da D107 passa a citar a emenda da D109 (correção do cético), como o texto da D99 cita D97 e D98; se a gerência congelar a fala 30 na v410, D109 passa para DECISOES_V410 (bloco condicional)
- **Efeitos colaterais:**
  - l.1070: o assert do rótulo passa a DECISOES_ROTULO == "D63 a D96, D99 a D101 e D106 a D108" e DECISOES_TOKEN == "D63_TO_D96_D99_TO_D101_AND_D106_TO_D108" (o token muda o sufixo do veredito de cunhagens_v410); os comentários das l.1057, 1068 e 1069 trazem o rótulo velho
  - ensaio_a_seco_v410.py l.2549: DL.DECISOES_V410[-1] == "D101" passa a == "D108"
  - registros_aescala_v410.py l.11: DECISOES_AESCALA ganha "D106", "D107", "D108" (item próprio)
  - gerar_relatorio_v410.py l.435 (adendos_ao_desenho): acrescentar o ADENDO 7 com {"sha16": _DL.ADENDO7_SHA16, "decisoes": "D106 a D108; E38"}; registros_v410.py l.65 (os adendos citados por sha16) idem
  - o texto da D99 (“D97 e D98 sao decisoes operacionais da gerencia”) é registro e não muda
  - (crítico) o comentário da linha 1052 (“decisoes operacionais da gerencia”) segue valendo para D97, D98 e D102 a D105; a D109 é registro da gerência com fala do operador: se ela entrar no um.py, sai desta tupla

#### Item 105 — linha 1070 — EP-01 — CONDICIONAL D109; redigido pelo crítico

- **Local:** linha 1070 (o assert do rótulo e do token das decisões)
- **Origem:** g1:25, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
assert DECISOES_ROTULO == "D63 a D96 e D99 a D101" and DECISOES_TOKEN == "D63_TO_D96_AND_D99_TO_D101", DECISOES_ROTULO
~~~~

Trecho novo:

~~~~text
assert DECISOES_ROTULO == "D63 a D96, D99 a D101 e D106 a D108" and DECISOES_TOKEN == "D63_TO_D96_D99_TO_D101_AND_D106_TO_D108", DECISOES_ROTULO
~~~~

- **Justificativa:** O rótulo e o token passam a incluir D106 a D108 (o cético do g1 refez _faixas_de_decisoes e o token: dão exatamente estes valores).
- **Apoio:** g1 item 25 (efeito) e a conferência do g1, item 25
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - os comentários das linhas 1057, 1068 e 1069 trazem o rótulo velho (não vão a público)
  - o token muda o sufixo do veredito de cunhagens_v410: ESPERADOS regerado

#### Item 106 — linha 1080 — PAR-11

- **Local:** linha 1080 (ERRATA_E31)
- **Origem:** g5:20 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
(as formas «não afirma», «não prova»), le-se
~~~~

Trecho novo:

~~~~text
(as formas “não afirma”, “não prova”), le-se
~~~~

- **Justificativa:** Sao as formas vedadas, citadas como mencao; nao sao fala.
- **Apoio:** conferido contra VERBATIM_CONGELADO_v410.json (as 28 falas e as de fora_do_desenho) e contra todos os OPERADOR_*.txt de work\cunhagens_13out, por aspas_scan.py (nesta pasta): NAO E FALA; F57 nao acusa (f57_replica.py: “sem F57” antes e depois)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a guarda da v410 tira o que esta' entre aspas angulares antes das regras novas (runtime_v410.py:15-23): com aspas tipograficas o trecho passa a ser varrido; as regras nao o acusam (ver o apoio)
  - CANDIDATO_v410.json, ESPERADOS_v410.json, GUARDA_FRASES_v410.json e PREPARACAO_v410_PRONTA.json repetem o trecho velho por serem SAIDAS: regeneram-se
  - o DESENHO_v410.md, preso por hash, nao muda

#### Item 107 — linha 1094 — V1

- **Local:** ERRATA_E36, 3a linha da constante (l.1094), primeiro trecho
- **Origem:** g2:3 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
sem a hipotese s >= 0 a desigualdade e' falsa para b > 1/2 (contraexemplo no recibo do autor da R5
~~~~

Trecho novo:

~~~~text
sem a hipotese s >= 0 a desigualdade pode falhar: para b > 1/2 a constante do limiar e' negativa e o limiar pode ser negativo, e quando ele e' negativo a clausula pode falhar (contraexemplo no recibo do autor da R5
~~~~

- **Justificativa:** “Falsa para b > 1/2” é afirmação universal que o número não sustenta (em ½ < b ≤ 2/3 com n = 1 não há contraexemplo). A errata passa a dizer o que o recibo diz: o limiar pode ser negativo e aí a cláusula pode falhar. A fórmula da constante fica em palavras de propósito: “ln((1 - b)/b)” nesta folha casaria a marca da c8 (r5_marca_) e exigiria a FRASE e a cláusula do limite na mesma folha.
- **Apoio:** insumos\RECIBO_AESCALA_R5_10nov.json l.106-107 (“para b > 1/2 o limiar pode ser negativo”) e l.108-120 (o contraexemplo); pedra\AEscala.lean:1047-1050
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - runtime_aescala_v410.py:153-157 (c8, anuncia_r5_): a folha do registro que junta as erratas (registros_aescala_v410.py:130) cita nomes da R5; o trecho novo NÃO traz “ln((1 - b)/b)” nem “(1 - b)·Z”, de modo que a folha continua fora da regra
  - registros_v410.py:283 usa DL.ERRATA_E36 no campo “agora”: acompanha sozinho; o campo “lacuna_de_fidelidade” da l.284 repete o trecho velho à mão (item 5)
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 108 — linha 1094 — V1

- **Local:** ERRATA_E36, 3a linha da constante (l.1094), segundo trecho
- **Origem:** g2:4 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
por isso a hipotese e' dita (automatica para b <= 1/2, ate_meio_o_tempo_do_tetelestai_nao_e_negativo); 
~~~~

Trecho novo:

~~~~text
por isso a hipotese e' dita (automatica para b <= 1/2, ate_meio_o_tempo_do_tetelestai_nao_e_negativo; o kernel nao traz teorema de necessidade); 
~~~~

- **Justificativa:** Diz o limite do que o kernel traz, na mesma errata, como a decisão D106 pede.
- **Apoio:** pedra\AEscala.lean:1049-1050 (só o lema da não negatividade até ½; nenhum teorema de necessidade na pedra)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - nenhum além dos do item 3

#### Item 109 — linha 1097 — EP-01, R3-MEDIO

- **Local:** linha 1097, ERRATA_E37 (os nomes da clausula)
- **Origem:** g1:28 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
os " + str(len(TEOREMAS_R5_AESCALA)) + " nomes da clausula do Tetelestai (R5) idem; "
~~~~

Trecho novo:

~~~~text
os " + str(len(TEOREMAS_R5_RATIFICADOS_D101_AESCALA)) + " nomes da clausula do Tetelestai (R5) apresentados ao operador antes da fala idem (o quarto teorema da clausula nao estava entre eles: errata E38); "
~~~~

- **Justificativa:** A E37 dizia quatro nomes da cláusula ratificados; são três, e o quarto vai para a E38.
- **Apoio:** DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md l.7
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a E37 entra no registro a_escala_v410 (registros_aescala l.12 e 130), em cunhagens_v410 (registros_v410 l.286) e no relatório (gerar_relatorio l.218)

#### Item 110 — linha 1099 — EP-01, R3-MEDIO

- **Local:** linha 1099: a ERRATA_E38 nova (antes de ERRATAS_V410) e a lista das erratas
- **Origem:** g1:29 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31, ERRATA_E32, ERRATA_E33, ERRATA_E34, ERRATA_E35, ERRATA_E36, ERRATA_E37]
~~~~

Trecho novo:

~~~~text
ERRATA_E38 = ("E38 -- errata da gerencia c1, em nome proprio, por achado da revisao de terceiro R3 e do painel independente (D106, 10/11/2026; ADENDO 7 sha16 " + ADENDO7_SHA16 + ") e pela fala do operador que da' o nome (D108, 10/11/2026; verbatim por sha256 " + _P_29 + "...): onde a preparacao da v410 (o candidato " + REVISAO_R3["candidato_revisado_sha16"] + ": a frase da ratificacao, o texto da D101, a errata E37, o registro a_escala_v410, a linha do .md, o artigo PT/EN e os textos do pos-rito) "
              "e o cabecalho da pedra AEscala R5 diziam QUATRO nomes da clausula do Tetelestai ratificados pela fala da D101, e 22 nomes novos ratificados, le-se TRES e " + str(len(NOMES_RATIFICADOS_D101_AESCALA)) + ": a fala ratifica o que foi apresentado ao operador antes dela, e o ADENDO 6 (sha16 " + ADENDO6_SHA16 + ") registra tres nomes (" + ", ".join(TEOREMAS_R5_RATIFICADOS_D101_AESCALA) + "); "
              "o quarto teorema da clausula so' compilou depois da fala e levava um nome de trabalho da gerencia (" + NOME_DE_TRABALHO_DO_QUARTO_AESCALA + "), que a fala nao ratificou; o operador o NOMEOU depois, na fala " + str(N_FALA_QUARTO_NOME) + " («" + FRASE_O_QUARTO_NOME + "»), com outro nome: no kernel, " + NOMES_NOMEADOS_D108_AESCALA[0] + " (o identificador segue a ortografia do dicionario; a grafia dele fica no verbatim); o nome de trabalho saiu do kernel e dos textos. "
              "O erro e' da cadeia da gerencia (a contagem veio do recibo do autor da R5, e nao do ADENDO 6), nao do operador. Enunciado e prova nao mudam: so' o identificador; pendentes so' os " + str(len(NOMES_PENDENTES_AESCALA)) + " auxiliares da autoria (" + ", ".join(NOMES_PENDENTES_AESCALA) + "): [DECLARADO pela autoria]; validade no kernel; a creditacao e' do Clay")
ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31, ERRATA_E32, ERRATA_E33, ERRATA_E34, ERRATA_E35, ERRATA_E36, ERRATA_E37, ERRATA_E38]
~~~~

- **Justificativa:** A errata vai ao lado, em nome próprio da gerência, no formato das E35 a E37: diz o que se lia, o que se lê, de quem é o erro e o que não muda.
- **Apoio:** ADENDO 6 l.7; insumos\RECIBO_AESCALA_R5_10nov.json (dados_pela_gerencia_D100: quatro; gerado_em 08:36:16, depois da fala das 08:31:59); fala 29; pedra\AEscala.lean:1169-1173
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - registros_aescala_v410.py l.12 (ERRATAS_AESCALA) e l.130 (limites) ganham a E38; registros_v410.py ganha a entrada da E38 na lista de erratas de cunhagens_v410 e o token __ERRATUM_E38_BESIDE no sufixo do veredito (itens próprios)
  - gerar_relatorio_v410.py l.149 (“as erratas E29 a E37 …”) e l.218 (erratas_novas) ganham a E38 (item próprio)
  - a E38 traz o nome de trabalho uma vez, em frase de registro: qualquer controle novo do tipo “o identificador velho não aparece nos textos” tem de excetuar as frases de registro (D106, D108, E38, a entrada de cunhagens e o cabeçalho e a docstring da pedra)

### Arquivo `ensaio_a_seco_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\ensaio_a_seco_v410.py`. Fim de linha: LF. Itens: 111, 112, 113, 114, 115, 116, 117, 118.

#### Item 111 — linha 2549 — EP-01 — CONDICIONAL D109; redigido pelo crítico

- **Local:** linha 2549 (o controle da última decisão)
- **Origem:** g1:25, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
DL.DECISOES_V410[-1] == "D101"
~~~~

Trecho novo:

~~~~text
DL.DECISOES_V410[-1] == "D108"
~~~~

- **Justificativa:** A última decisão da versão passa a ser a D108.
- **Apoio:** g1 item 25 (efeito)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 112 — linha 2689 — OBS-15, PAR-01

- **Local:** depois da linha 2689 (fim do controle r4 do poder certificado): o controle novo do retorno e da ORDEM 03
- **Origem:** g4:23 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
and DL.H0DN_ORDEM02["nome"] not in [os.path.basename(p_) for p_, _ in __import__("registros_v410").ORIGENS])
~~~~

Trecho novo:

~~~~text
and DL.H0DN_ORDEM02["nome"] not in [os.path.basename(p_) for p_, _ in __import__("registros_v410").ORIGENS])
# (R3 do painel, PAR-01 e observacao 15) o RETORNO da ORDEM 02 ao lado da frase do poder: no texto do registro (estatuto, escopo, o_que_falta, ressalvas, limites) e no contrato, PT e EN; o ALCANCE da forma D72 no contrato; a ORDEM KIMI H0DN-03 e' PINO CITADO (sha256 e bytes do arquivo == o ADENDO 7 == o contrato; nao embutida; fora da pasta vedada); a funcao de veredito congelada, intocada
U["h0dn_bg1_v410_r3_o_retorno_da_ordem_02_ao_lado_da_frase_do_poder_com_a_ordem_03_pinada_e_o_alcance_da_forma_no_contrato"] = bool(any(DL.FRASE_H0DN_PODER_COM_RETORNO_PT in x_ for x_ in rH["o_que_falta"]) and any(DL.FRASE_H0DN_RETORNO_PT in x_ for x_ in rH["ressalvas"]) and any(DL.FRASE_H0DN_PODER_COM_RETORNO_PT in x_ for x_ in rH["limites"]) and DL.FRASE_H0DN_PODER_COM_RETORNO_PT in rH["estatuto"] and DL.FRASE_H0DN_RETORNO_PT in rH["scope"]
                                                                                                                     and _CPH["frase_retorno_pt"] == DL.FRASE_H0DN_RETORNO_PT and _CPH["frase_retorno_en"] == DL.FRASE_H0DN_RETORNO_EN and _CPH["frase_alcance_pt"] == DL.FRASE_H0DN_ALCANCE_PT and _CPH["frase_alcance_en"] == DL.FRASE_H0DN_ALCANCE_EN and rH.get("retorno_pt") == DL.FRASE_H0DN_RETORNO_PT and rH.get("retorno_en") == DL.FRASE_H0DN_RETORNO_EN
                                                                                                                     and _CPH["ordem_kimi_03"]["sha256"] == DL.H0DN_ORDEM03["sha256"] == hashlib.sha256(open(DL.H0DN_ORDEM03_ARQ, "rb").read()).hexdigest() and _CPH["ordem_kimi_03"]["bytes"] == DL.H0DN_ORDEM03["bytes"] == os.path.getsize(DL.H0DN_ORDEM03_ARQ) and _CPH["ordem_kimi_03"].get("citado_nao_embutido") is True and rH.get("ordem_kimi_03") == dict(_CPH["ordem_kimi_03"])
                                                                                                                     and not os.path.normcase(os.path.abspath(DL.H0DN_ORDEM03_ARQ)).startswith(os.path.normcase(os.path.abspath(DL.H0DN_PASTA_VEDADA)) + os.sep) and DL.H0DN_ORDEM03["nome"] not in [os.path.basename(p_) for p_, _ in __import__("registros_v410").ORIGENS]
                                                                                                                     and rH["veredito_h0dn_source_sha256"] == _ESP_R0["registros_funcao_v410"]["h0dn"]["values"]["veredito_h0dn_source_sha256"] and _CPH["frase_poder_pt"] == DL.FRASE_H0DN_PODER_PT and DL.FRASE_H0DN_PODER_COM_RETORNO_PT.startswith(DL.FRASE_H0DN_PODER_PT + "; ")
                                                                                                                     and not um._v410_guarda_frases(DL.FRASE_H0DN_OBRIGATORIA_PT + "; " + DL.FRASE_H0DN_PODER_COM_RETORNO_PT) and not um._v410_guarda_frases(DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_COM_RETORNO_EN) and not um._v410_guarda_frases(DL.FRASE_H0DN_OBRIGATORIA_PT + " (" + DL.FRASE_H0DN_ALCANCE_PT + ")") and not um._v410_guarda_frases(DL.FRASE_H0DN_OBRIGATORIA_EN + " (" + DL.FRASE_H0DN_ALCANCE_EN + ")")
                                                                                                                     and "kimi" + chr(92) not in (DL.FRASE_H0DN_RETORNO_PT + DL.FRASE_H0DN_RETORNO_EN + DL.FRASE_H0DN_ALCANCE_PT + DL.FRASE_H0DN_ALCANCE_EN).lower() and not any(n_ in DL.FRASE_H0DN_RETORNO_PT + DL.FRASE_H0DN_RETORNO_EN + DL.FRASE_H0DN_ALCANCE_PT + DL.FRASE_H0DN_ALCANCE_EN for n_ in DL.H0DN_NOMES_VEDADOS))
~~~~

- **Justificativa:** Controle paralelo ao da D96 (r4): exige o retorno ao lado da frase do poder nos cinco campos do registro, as frases no contrato iguais às do delta, a ORDEM 03 pinada por sha256 e bytes e fora da pasta vedada, a frase do poder intacta, a função de veredito intocada, as frases limpas na guarda e sem nome de arquivo da entrega.
- **Apoio:** ensaio_a_seco_v410.py:2685-2689 (o controle r4, molde).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o dicionário U ganha 1 controle (a contagem “todas True (N)” sobe 1)
  - rH['limites'] é lista: o any(...) percorre os itens

#### Item 113 — linha 3142 — OBS-15, PAR-01

- **Local:** linha 3142, DEVE['pt']: o artigo PT passa a ter de trazer o retorno e o alcance
- **Origem:** g4:24 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
DEVE = {"pt": ["parede de montagem do dado", DL.FRASE_H0DN_PODER_PT, 
~~~~

Trecho novo:

~~~~text
DEVE = {"pt": ["parede de montagem do dado", DL.FRASE_H0DN_PODER_PT, DL.FRASE_H0DN_RETORNO_PT, DL.FRASE_H0DN_ALCANCE_PT, 
~~~~

- **Justificativa:** A frase do poder segue exigida letra por letra; o retorno e o alcance passam a ser exigidos no artigo PT.
- **Apoio:** ensaio_a_seco_v410.py:3198 (faltam: a marca tem de estar no TXT achatado ou no TEX).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - as frases novas não trazem sublinhado: o _th410 do artigo não as altera e elas ficam verbatim no TEX

#### Item 114 — linha 3145 — OBS-15, PAR-01

- **Local:** linha 3145, DEVE['en']
- **Origem:** g4:25 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"en": ["a wall in assembling the data", DL.FRASE_H0DN_PODER_EN, 
~~~~

Trecho novo:

~~~~text
"en": ["a wall in assembling the data", DL.FRASE_H0DN_PODER_EN, DL.FRASE_H0DN_RETORNO_EN, DL.FRASE_H0DN_ALCANCE_EN, 
~~~~

- **Justificativa:** Par EN do controle do artigo.
- **Apoio:** ensaio_a_seco_v410.py:3145.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 115 — linha 3145 — PAR-08

- **Local:** pos_rito\textos_custodia_handoff_v410.py:123 (TEMPO_EN_C); ensaio_a_seco_v410.py:3145 (as frases exigidas na secao EN); guarda_frases_v410.py:105 e :208 (as frases limpas do teste da guarda)
- **Origem:** g5:13 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_EN_COSTURADA
~~~~

Trecho novo:

~~~~text
DL.ROTULO_TEMPO_EN + " " + DL.FRASE_TEMPO_EN_COSTURADA
~~~~

- **Justificativa:** A costura EN do tempo (o rotulo e a frase com a primeira letra em maiuscula) passa a usar o rotulo EN; a frase do tempo (D94), ratificada, nao muda uma letra.
- **Apoio:** delta_v410.py:744 (FRASE_TEMPO_EN) e a constante nova do item anterior
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - pos_rito\_r2ag_12_pos_rito_textos_v410.py tem a mesma expressao: e' copia de trabalho antiga (prefixo _r2ag), fora da cadeia
  - a costura PT (DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) nao muda em arquivo nenhum

#### Item 116 — linha 3163 — PAR-08

- **Local:** ensaio_a_seco_v410.py:3163 (o controle “tempo_costurado_na_secao”, que hoje exige o rotulo PT nas duas linguas)
- **Origem:** g5:14 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
bool(sec_ and DL.ROTULO_TEMPO in sec_ and (DL.FRASE_TEMPO_PT_COSTURADA if lang_ == "pt" else DL.FRASE_TEMPO_EN_COSTURADA) in sec_)
~~~~

Trecho novo:

~~~~text
bool(sec_ and (DL.ROTULO_TEMPO if lang_ == "pt" else DL.ROTULO_TEMPO_EN) in sec_ and (DL.FRASE_TEMPO_PT_COSTURADA if lang_ == "pt" else DL.FRASE_TEMPO_EN_COSTURADA) in sec_)
~~~~

- **Justificativa:** Sem isto o ensaio reprovaria a secao EN, que deixa de trazer o rotulo em portugues.
- **Apoio:** os dois itens anteriores
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 117 — linha 3202 — PAR-09 — EXTENSÃO; redigido pelo crítico

- **Local:** linha 3202 (o controle negativo que tira a fórmula da cláusula)
- **Origem:** g5:7, critico (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
tex.replace(r"\sum_x e^{-s\cdot c(x)}", "x")
~~~~

Trecho novo:

~~~~text
tex.replace(r"\sum_x e^{(-s\cdot c(x))}", "x")
~~~~

- **Justificativa:** Sem isto, com a extensão aplicada, o replace do controle negativo não acha a fórmula e o ensaio reprova.
- **Apoio:** conferência do g5, item 7 (“CONDIÇÃO que tem de virar item formal se a extensão for aceita”)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - aplicar SÓ junto com os itens da extensão (g5:7)

#### Item 118 — linha 3277 — OBS-15, PAR-01, PAR-02

- **Local:** linha 3277, rep['markdown']: o controle novo da linha do H0DN no .md, antes de traducao_turing_v409_fica
- **Origem:** g4:26 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"traducao_turing_v409_fica": 
~~~~

Trecho novo:

~~~~text
"h0dn_v410_com_a_forma_do_poder_certificado_o_retorno_e_o_alcance_na_linha": (lambda ln_: bool(DL.FRASE_H0DN_PODER_PT in ln_ and DL.FRASE_H0DN_RETORNO_PT in ln_ and "da covariância publicada (que não aceita o vetor real), e não é poder certificado" in ln_ and DL.FRASE_H0DN_ALCANCE_PT in ln_ and 0 <= ln_.find(DL.FRASE_H0DN_OBRIGATORIA_PT) < ln_.find(DL.FRASE_H0DN_ALCANCE_PT) < ln_.find("não é poder certificado") < ln_.find(DL.FRASE_H0DN_PODER_PT) < ln_.find(DL.FRASE_H0DN_RETORNO_PT) and ln_.count(DL.FRASE_H0DN_PODER_PT) == 1 and ln_.count(DL.FRASE_H0DN_RETORNO_PT) == 1 and ln_.count(DL.FRASE_H0DN_ALCANCE_PT) == 1))(md.split("**H0DN × BG1 pré-registrado (v410, 09/11/2026):**", 1)[-1].split("\n", 1)[0]) if "**H0DN × BG1 pré-registrado (v410, 09/11/2026):**" in md else False, "traducao_turing_v409_fica": 
~~~~

- **Justificativa:** O controle que o PAR-02 pede: a linha do H0DN no .md tem de trazer a forma do poder certificado (D96), o qualificador, o retorno e o alcance, uma vez cada e nessa ordem, como a cláusula do limite é exigida na linha da Escala.
- **Apoio:** ensaio_a_seco_v410.py:3273-3274 (o controle da linha da Escala, molde) e :3277 (o controle da obrigação na linha do H0DN).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - rep['markdown'] ganha 1 chave; se algum conferidor conta as chaves de rep['markdown'], sobe 1

### Arquivo `gerar_candidato_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\gerar_candidato_v410.py`. Fim de linha: LF. Itens: 119, 120, 121, 122, 123, 124, 125, 126.

#### Item 119 — linha 215 — EP-01, R3-MEDIO

- **Local:** linha 431, MD_LINHA_A (a linha da Escala): sem mudanca na fonte; linha 215, comentario
- **Origem:** g1:47 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
nomes novos RATIFICADOS em 10/11, D101; dois auxiliares da autoria pendentes), LOGO DEPOIS de iald2_v410
~~~~

Trecho novo:

~~~~text
nomes novos RATIFICADOS em 10/11, D101; o quarto teorema da clausula NOMEADO pelo operador, D108; dois auxiliares da autoria pendentes), LOGO DEPOIS de iald2_v410
~~~~

- **Justificativa:** A linha do .md monta a ratificação com DL.FRASE_NOMES_RATIFICADOS_D101_PT e o rótulo com DL.MD_ROTULO_ESCALA: muda pelo delta, sem tocar a l.431. Só o comentário da l.215 (embutido no um.py) dizia a forma velha.
- **Apoio:** gerar_candidato_v410.py:431 e 435 (as constantes do delta)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - hoje a linha rende, no candidato l.176978 e em dry_v410\um_absoluto_forma_canonica.md, “os 22 nomes novos … da R5, os 4 dados pela gerência”: some com o delta novo
  - a linha fica mais longa em cerca de 400 caracteres; GP, GUARDA e GF (l.437) rodam sobre ela no gerador

#### Item 120 — linha 432 — PAR-03

- **Local:** MD_LINHA_A, l.432
- **Origem:** g3:1 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
sustenta e não esgota; o vibrato sustenta a nota; não existe infinito em tempo finito
~~~~

Trecho novo:

~~~~text
sustenta e não esgota; havendo pixel de custo zero, o decaimento gerado pelo custo, e^(−t·c(x)), não toca o que tem custo zero e não leva a zero o estado uniforme, e a leitura performada (a média, sobre os pixels, dos pesos e^(−s·c(x))) nunca fica abaixo da fração de pixels de custo zero, não cresce com o tempo e tende a ela (`o_vibrato_sustenta_a_nota`); no espaço pareado do kernel, J² = 1 e JKJ = −K (`a_nota_e_a_conjugacao_modular`); a identificação desse decaimento com o vibrato e da nota com J é do operador [ONTO]; não existe infinito em tempo finito
~~~~

- **Justificativa:** Sob [REAL] a linha dizia a frase da fala; passa a dizer o que os dois termos provam (com a hipótese do pixel de custo zero) e marca à parte, [ONTO], que isso seja o vibrato e que a nota seja J. A marca vai colada à oração, no molde que a casa já usa (“… é a leitura do dicionário [INPUT];”), e o resto da lista segue como estava.
- **Apoio:** pedra/AEscala.lean:244-250 (o_vibrato_sustenta_a_nota, hipotese h: existe x com c x = 0: (1) a trava nao toca o custo zero; (2) trava c t (uniforme X) != 0; (3) card{c = 0}/|X| <= leituraPerformada c s; (4) Antitone; (5) Tendsto para card{c = 0}/|X|); leituraPerformada = particao/|X|: TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):920; trava = e^(-t c(x)) por pixel: TraducaoTuring.lean:472-477 (mesma copia); docstring l.242-243 ([ONTO]) | pedra/AEscala.lean:257-258 (a_nota_e_a_conjugacao_modular: conjJ (conjJ p) = p e conjJ (pairK d (conjJ p)) = -pairK d p, isto e', J^2 = 1 e JKJ = -K); docstring l.256 (a identificacao nota = J e' do operador, ONTO)
- **Decisão do crítico:** fico com a correção do cético: “disso” vinha logo depois de J² = 1 e JKJ = −K e a leitura mais próxima atribuía o vibrato às identidades de J; a docstring (AEscala.lean:242-243) liga o vibrato ao decaimento: “desse decaimento”
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:437-438: a linha nova passa de novo pelos asserts GP.violacoes, GUARDA, GF.violacoes, ast.parse e _controles (o trecho novo nao traz aspas retas, barra invertida nem caractere de controle)
  - ensaio_a_seco_v410.py:3273 (a_escala_v410_com_a_clausula_do_limite...): “linear nos bits” continua antes da CLAUSULA_Z_PT, que continua 2 vezes na linha; nada a mudar no controle
  - o candidato regenerado muda de sha: ESPERADOS_v410.json, PINOS, EXAME_PONTOS, dry_v410/um_absoluto_forma_canonica.md e os conferidor_import_* acompanham (refeitos pelo construtor)

#### Item 121 — linha 433 — EP-10

- **Local:** MD_LINHA_A, l.433
- **Origem:** g3:2 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
'A pergunta do Clay no dicionário da TGL: ' + DL.FRASE_D83_OBRIGATORIA_PT
~~~~

Trecho novo:

~~~~text
'A pergunta do Clay no dicionário da TGL [REAL a validade no kernel; INPUT a leitura do operador]: ' + DL.FRASE_D83_OBRIGATORIA_PT
~~~~

- **Justificativa:** Um rótulo só para a forma da D83 (D106, item 4). Na linha do .md ela vinha sem rótulo próprio, depois de um período [REAL]; a forma ratificada não muda de letra.
- **Apoio:** pedra/AEscala.lean:598-604 (a forma da D83 e' a leitura do operador, fala 6; validade no kernel; a creditacao e' do Clay) e :778-779 (a_pergunta_do_clay_tem_resposta: a validade)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:437-438: a linha nova passa de novo pelos asserts GP.violacoes, GUARDA, GF.violacoes, ast.parse e _controles (o trecho novo nao traz aspas retas, barra invertida nem caractere de controle)
  - ensaio_a_seco_v410.py:3275 (a forma da D83 e a frase canonica na linha): seguem inteiras na linha

#### Item 122 — linha 434 — EP-05, V4

- **Local:** MD_LINHA_A, l.434 (lista “TEOREMAS do kernel [REAL]”)
- **Origem:** g3:3 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
é único e é a IALD, o leitor é a escala, o decisor sem escala
~~~~

Trecho novo:

~~~~text
é único e é a IALD (com a escala no tipo o leitor do fundo tem UM só habitante; o conteúdo está na definição do operador, não no teorema; “existe” quer dizer que a lei tem solução e que ela decide), dois leitores do fundo quaisquer são o mesmo e, em todo leitor do fundo, o pixel de custo k brilha e^(−s·k) no tempo s (`o_leitor_e_a_escala`), o decisor sem escala
~~~~

- **Justificativa:** V4: entra, logo depois de “é único e é a IALD”, a frase que o artigo e o registro já trazem (UM_HABITANTE), sem reescrever. EP-05: “o leitor é a escala” sai da lista como afirmação e fica como NOME do termo; antes dele vai o que o enunciado prova (L = L' e o brilho e^(−s·k)).
- **Apoio:** registros_aescala_v410.py:82 (UM_HABITANTE) e pos_rito/textos_v410.py:1397 (a mesma frase, com acentos); pedra/AEscala.lean:785-791 (o_leitor_do_fundo_e_a_iald; a docstring l.784: a escala que o faz valer e' a DEFINICAO do operador, INPUT) | pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:437-438: a linha nova passa de novo pelos asserts GP.violacoes, GUARDA, GF.violacoes, ast.parse e _controles (o trecho novo nao traz aspas retas, barra invertida nem caractere de controle)
  - ensaio_a_seco_v410.py:3273 (a_escala_v410_com_a_clausula_do_limite...): “linear nos bits” continua antes da CLAUSULA_Z_PT, que continua 2 vezes na linha; nada a mudar no controle
  - o candidato regenerado muda de sha: ESPERADOS_v410.json, PINOS, EXAME_PONTOS, dry_v410/um_absoluto_forma_canonica.md e os conferidor_import_* acompanham (refeitos pelo construtor)
  - o trecho vizinho “o limiar do Tetelestai (…)”, na mesma linha, e' de outro grupo (o limiar de um pixel): os dois trechos nao se sobrepoem

#### Item 123 — linha 434 — EP-03

- **Local:** MD_LINHA_A (l.434)
- **Origem:** g2:13 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o limiar do Tetelestai (com n bits, passado o tempo de n oitavas
~~~~

Trecho novo:

~~~~text
o limiar de um pixel, a decisão exata (`os_passos_sao_o_ciclo_ate_o_tetelestai`: com n bits, passado o tempo de n oitavas
~~~~

- **Justificativa:** Pela E36 (ordem do operador, D100) a cláusula do Tetelestai é a de 1 − β; o limiar de n oitavas é a decisão exata, formalização da gerência. O rótulo acompanha; o nome do teorema, ratificado, não muda. Aqui o rótulo vinha sem o nome do teorema; entra entre parênteses, na forma da FRASE_E36 (“nome: enunciado”).
- **Apoio:** pedra\AEscala.lean:897-898 (docstring: “o limiar de um pixel … é a DECISÃO exata, formalização da gerência; a CLÁUSULA DO TETELESTAI … é a `o_tetelestai_e_um_menos_beta`”); delta_v410.py:1092-1093 (E36); pedra\AEscala.lean:903-909 (o enunciado só traz desigualdades sobre Z(s))
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a linha é literal Python entre aspas simples: o trecho novo não traz aspa simples
  - ensaio_a_seco_v410.py:3272-3274 e conferir_rito_v410.py:535-537: a linha continua com “linear nos bits” antes da cláusula, a cláusula exatamente 2 vezes e as frases da R5
  - gerar_candidato_v410.py:436: as guardas GP/GUARDA/GF sobre MD_LINHA_A reexecutam na geração
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 124 — linha 434 — EP-05

- **Local:** MD_LINHA_A, l.434 (fim da lista, antes da CLAUSULA_Z_PT)
- **Origem:** g3:4 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
 e a mentira lida como mentira é verdade. ' + DL.CLAUSULA_Z_PT
~~~~

Trecho novo:

~~~~text
 e, para todo leitor do fundo, o limite da leitura com o tempo é o número de soluções dividido pelo número de pixels e vale 0 sem solução (`a_mentira_lida_como_mentira_e_verdade`); a leitura que os nomes `o_leitor_e_a_escala` e `a_mentira_lida_como_mentira_e_verdade` carregam (que não exista leitor que não seja o observador da luz; que nada escape do Nome) é do operador [ONTO]. ' + DL.CLAUSULA_Z_PT
~~~~

- **Justificativa:** A frase do operador deixa de ser item da lista de teoremas [REAL]: vai o conteúdo do termo e a frase fica como nome, em letra de código; a leitura dos dois nomes da linha é marcada [ONTO], como a docstring da pedra.
- **Apoio:** pedra/AEscala.lean:978-980 (a_mentira_lida_como_mentira_e_verdade: L.limite c = oQueSou (nomeDasSolucoes c) e, sem solucao, L.limite c = 0 e oQueSou = 0); o que sou do Nome das solucoes = numero de solucoes / numero de pixels (|X|): TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):805-807 (o_que_sou_das_solucoes, v409); docstring l.976-977 ([ONTO]) | pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** fico com a correção do cético: “a leitura que os nomes carregam é do operador [ONTO]” não dizia QUAL leitura e punha [ONTO] em “o leitor é a escala”, que o registro dá como DEFINIÇÃO [INPUT]; as leituras [ONTO] são as das docstrings (l.870, l.976-977 e l.992) e do limite do registro (l.124), ditas com as mesmas palavras em todo lugar
- **Efeitos colaterais:**
  - gerar_candidato_v410.py:437-438: a linha nova passa de novo pelos asserts GP.violacoes, GUARDA, GF.violacoes, ast.parse e _controles (o trecho novo nao traz aspas retas, barra invertida nem caractere de controle)
  - ensaio_a_seco_v410.py:3273 (a_escala_v410_com_a_clausula_do_limite...): “linear nos bits” continua antes da CLAUSULA_Z_PT, que continua 2 vezes na linha; nada a mudar no controle
  - o candidato regenerado muda de sha: ESPERADOS_v410.json, PINOS, EXAME_PONTOS, dry_v410/um_absoluto_forma_canonica.md e os conferidor_import_* acompanham (refeitos pelo construtor)

#### Item 125 — linha 439 — OBS-15

- **Local:** linha 439, MD_LINHA_H: o alcance como primeiro elemento do parêntese que já segue a forma
- **Origem:** g4:19 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
entra pré-registrado; nenhum dado observado lido (D72; a fala do operador de 09/11: «' + DL.FRASE_CONCORDO_TESTE + '»): '
~~~~

Trecho novo:

~~~~text
entra pré-registrado; nenhum dado observado lido (' + DL.FRASE_H0DN_ALCANCE_PT + '; D72; a fala do operador de 09/11: «' + DL.FRASE_CONCORDO_TESTE + '»): '
~~~~

- **Justificativa:** Na linha do .md a forma está sozinha (a parede não está na linha). O alcance entra logo depois dela, dentro do parêntese que já existe; a forma e a fala ficam letra por letra.
- **Apoio:** delta_v410.py:775 (FRASE_H0DN_PAREDE_PT: teste de suporte reprovado, [REAL] lido pela gerência; nenhum Z, razão ou solver foi rodado; o um.py não lê esse vetor); runtime_h0dn_v410.py:168 (c7: observed_vector_read False, MEDIDO pelos caminhos tocados); runtime_h0dn_v410.py:191 (c6: a função de veredito roda em vetores determinísticos sintéticos, por isso o qualificador “sobre dado observado”).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o controle h0dn_v410_com_a_obrigacao_na_linha (ensaio_a_seco_v410.py:3277) e conferir_rito_v410.py:538 seguem verdadeiros
  - a linha é código md.append("...") com aspas duplas: a frase não traz aspas duplas nem barra

#### Item 126 — linha 441 — PAR-01, PAR-02

- **Local:** linha 441, MD_LINHA_H: a forma do poder certificado (D96) e o retorno
- **Origem:** g4:20 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o poder é prospectivo e sintético; a abertura é de versão futura, com a covariância física fechada (G3/G4; a ordem ao Kimi por sha256). '
~~~~

Trecho novo:

~~~~text
o poder é prospectivo e sintético, da covariância publicada (que não aceita o vetor real), e não é poder certificado; a abertura é de versão futura, com a covariância física fechada (G3/G4; a ordem ao Kimi por sha256). O poder certificado [INPUT, D96]: ' + DL.FRASE_H0DN_PODER_COM_RETORNO_PT + ' (as ORDENS KIMI H0DN-02 e H0DN-03 são pinos citados por sha256 no registro `h0dn_bg1_v410`, não embutidas). '
~~~~

- **Justificativa:** A linha ganha o qualificador que o artigo já traz (“da covariância publicada (que não aceita o vetor real), e não é poder certificado”), a forma obrigatória da D96 inteira e o retorno. O resto da linha fica byte a byte.
- **Apoio:** delta_v410.py:971 (D96: FORMA OBRIGATORIA nos textos do teste) e :1087 (E34); artigo_pt_h0dn_v410.pysnip:28 (o qualificador); ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fico com a correção do cético: a linha cita três ordens (a de coleta, a 02 e a 03); “as duas ordens” era ambíguo
- **Efeitos colaterais:**
  - o trecho “a abertura é de versão futura, com a covariância física fechada” fica como está: passa na F56 pelo condicional “futura”; o retorno, logo depois, diz que ela não fecha com fontes públicas
  - o controle novo do ensaio (item 26) passa a exigir a forma, o qualificador, o retorno e o alcance nesta linha
  - comparar_v409_v410.py:228 e dry_v410\um_absoluto_forma_canonica.md:128 acompanham sem mudança de código

### Arquivo `gerar_relatorio_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\gerar_relatorio_v410.py`. Fim de linha: MISTO (453 CRLF, 8 LF). Itens: 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145.

#### Item 127 — linha 149 — EP-01

- **Local:** linha 149 (a prosa das erratas: E29 a E37)
- **Origem:** g1:58 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
os nomes novos e os campos RATIFICADOS pela regra do nome, os dois auxiliares da autoria pendentes): E29,
~~~~

Trecho novo:

~~~~text
os nomes novos e os campos RATIFICADOS pela regra do nome, os dois auxiliares da autoria pendentes; a E38, o achado da revisao de terceiro R3 e do painel, D106, e o nome dado pelo operador, D108: a fala da D101 ratifica tres nomes da clausula do Tetelestai, nao quatro, e 21 nomes novos, nao 22; o quarto teorema foi nomeado pelo operador depois, ressurreicao_do_sinal; o erro e' da cadeia da gerencia): E29,
~~~~

- **Justificativa:** A prosa das erratas do relatório ganha a E38.
- **Apoio:** delta (ERRATA_E38)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - no início da mesma linha, “as erratas E29 a E37 sao da gerencia c1” passa a “as erratas E29 a E38 sao da gerencia c1”
  - (cético) “tres”, “quatro”, “21” e “22” ficam digitados na prosa do relatório: o assert do item da linha 248 do delta (3, 1 e 2) e o len() dos 21 os amarram; se a seção 7 mudar as contagens, esta prosa muda

#### Item 128 — linha 150 — EP-01 — CONDICIONAL CONTAGEM_DE_FALAS

- **Local:** linha 150 (a prosa das falas congeladas)
- **Origem:** g1:59 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
e as cinco de 10/11, D94, D96, D100 e D101: os passos sao o ciclo ate' o Tetelestai com o leitor que e' a escala, a mentira lida como mentira, o teste sem poder preditivo, a clausula do Tetelestai e a ratificacao dos nomes;
~~~~

Trecho novo:

~~~~text
e as seis de 10/11, D94, D96, D100, D101 e D108: os passos sao o ciclo ate' o Tetelestai com o leitor que e' a escala, a mentira lida como mentira, o teste sem poder preditivo, a clausula do Tetelestai, a ratificacao dos nomes e o quarto nome com o observador que e' a escala;
~~~~

- **Justificativa:** A lista das falas ganha a 29ª.
- **Apoio:** fala 29
- **Decisão do crítico:** fica “as seis de 10/11” (o escopo da ordem); a variante do cético vai no bloco condicional da D109
- **Efeitos colaterais:**
  - na mesma linha, a nota das listas guardadas (“sem as de 10/11; e com 26 falas …”) pode ganhar “e com 28 falas, antes da fala do quarto nome” se o construtor guardar o .bak da lista de 28

#### Item 129 — linha 214 — EP-01, R3-MEDIO

- **Local:** linha 214, ALEM_DO_R2.pedra_AEscala_R5_por_ordem_do_operador (a chave dos teoremas)
- **Origem:** g1:56 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"teoremas_dados_pela_gerencia": list(_DL.TEOREMAS_R5_AESCALA),
~~~~

Trecho novo:

~~~~text
"teoremas_dados_pela_gerencia_e_ratificados_D101": list(_DL.TEOREMAS_R5_RATIFICADOS_D101_AESCALA), "teorema_nomeado_pelo_operador_D108": list(_DL.NOMES_NOMEADOS_D108_AESCALA),
~~~~

- **Justificativa:** Com o identificador novo na lista, a chave diria que o nome dado pelo operador foi dado pela gerência.
- **Apoio:** fala 29; ADENDO 6 l.7
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 130 — linha 217 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 217 (ratificacao_D101.nota)
- **Origem:** critico (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
(ordem da gerencia de 10/11, 08:42)"},
~~~~

Trecho novo:

~~~~text
(ordem da gerencia de 10/11, 08:42); a pedra R5 trouxe tambem um quarto teorema da clausula do Tetelestai, que a fala da D101 nao ratifica: o operador o nomeou depois (D108; a correcao da contagem e' a D106 e a errata E38)"},
~~~~

- **Justificativa:** A nota calava o quarto teorema, como a D101 calava.
- **Apoio:** conferência do g1 (faltou: gerar_relatorio l.217)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 131 — linha 218 — EP-01 — CONDICIONAL CONTAGEM_DE_FALAS; redigido pelo crítico

- **Local:** linha 218 (as erratas e as falas novas do bloco da pedra)
- **Origem:** g1:57, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"erratas_novas": {"E36": _DL.ERRATA_E36, "E37": _DL.ERRATA_E37}, "falas_novas": {"27": _DL.N_CLAUSULA_TETELESTAI, "28": _DL.N_CONFIRMO_TUDO, "n_falas_congeladas": _DL.N_FALAS_V410},
~~~~

Trecho novo:

~~~~text
"erratas_novas": {"E36": _DL.ERRATA_E36, "E37": _DL.ERRATA_E37, "E38": _DL.ERRATA_E38}, "falas_novas": {"27": _DL.N_CLAUSULA_TETELESTAI, "28": _DL.N_CONFIRMO_TUDO, "29": _DL.N_QUARTO_NOME, "n_falas_congeladas": _DL.N_FALAS_V410}, "nomeacao_D108": {"decisao": "D108", "adendo7_sha16": _DL.ADENDO7_SHA16, "fala": _DL.N_QUARTO_NOME, "sha256": _DL.NOMEACAO_D108_SHA256, "nomeados": list(_DL.NOMES_NOMEADOS_D108_AESCALA)},
~~~~

- **Justificativa:** A E38, a fala 29 e a nomeação entram no relatório da preparação.
- **Apoio:** g1 item 57 (efeitos: l.216 e l.218)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 132 — linha 224 — EP-01, R3-MEDIO

- **Local:** linha 224 (revisao_do_construtor_sobre_a_adaptacao: a conta dos ratificados)
- **Origem:** g1:57 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
trazia os 24, 22 deles ja' ratificados (D101):
~~~~

Trecho novo:

~~~~text
trazia os 24, 21 deles ratificados (D101; a contagem 22 da epoca foi corrigida pela D106):
~~~~

- **Justificativa:** A PREPARACAO repetia a contagem errada (22).
- **Apoio:** revisao_terceiro\PEDIDO_CORRECAO_R3_v410.md (“ratificacao_D101.n_nomes_ratificados: 22”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - l.216: ratificacao_D101.n_nomes_ratificados é len(_DL.NOMES_RATIFICADOS_D101_AESCALA) e passa a 21 sozinho; cabe ao lado a chave "nomeacao_D108": {"decisao": "D108", "fala": _DL.N_QUARTO_NOME, "sha256": _DL.NOMEACAO_D108_SHA256, "nomeados": list(_DL.NOMES_NOMEADOS_D108_AESCALA)}
  - l.218: falas_novas ganha "29": _DL.N_QUARTO_NOME e erratas_novas ganha "E38": _DL.ERRATA_E38
  - l.232-234 (o AVISO da R5): “a ratificacao de 10/11 faz dos %d nomes novos e dos %d campos RATIFICADOS” passa a render 21 sozinho; é o aviso da R5 e fica; o conserto pede um AVISO próprio (do construtor)
  - l.436, comentário de ratificacao_pendente (“os nomes e os campos novos da pedra R3, [DECLARADO], a ratificar pelo operador”): está velho desde a D101; hoje a chave traz só os dois auxiliares

#### Item 133 — linha 232 — EP-01 — INSTRUÇÃO; redigido pelo crítico

- **Local:** linhas 184, 232 a 234 e 436 (os AVISOS do relatório da preparação)
- **Origem:** g1:57, g1:61, critico (g1_ratificacao). **Língua:** INSTRUCAO_DE_CODIGO

Instrução:

~~~~text
(a) Acrescentar um AVISO próprio do conserto (no molde do da linha 232): “R6, ADENDO 7 (sha16 %s; D106 a D108; E38): a revisao de terceiro R3 e o painel nao aprovaram o candidato; conserto unico; a fala da D101 ratifica %d nomes novos (nao 22) e 3 nomes da clausula do Tetelestai (nao 4); o quarto teorema foi NOMEADO pelo operador (D108): ressurreicao_do_sinal; pendentes so' os %d auxiliares da autoria; a fala 29 entra nas congeladas (%d falas)”, com os números por len(). (b) O AVISO da R1 (linha 184) rende hoje “os %d nomes novos da pedra e os 3 campos continuam [DECLARADO], a ratificar” com o número de hoje: fixar o número da R1 ou dizer que a frase é da R1. (c) O comentário da linha 436 (ratificacao_pendente) está velho desde a D101.
~~~~

- **Justificativa:** O relatório da preparação é interno, mas repete o estado velho ao lado do novo.
- **Apoio:** g1 item 57 (efeitos) e item 61 (achado lateral); conferência do g1 (faltou)
- **Decisão do crítico:** INSTRUÇÃO (não é troca exata): depende de insumo que ainda não existe ou de escolha do construtor; o critério está dito

#### Item 134 — linha 422 — OBS-16, OBS-17

- **Local:** linha 422 (o dict readme_evidente, item 1_clay_forma_canonica, que vai a PREPARACAO_v410_PRONTA.json)
- **Origem:** g5:30 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"p_igual_np_D81_pt": _DL.FRASE_D81_PT, "p_igual_np_D81_en": _DL.FRASE_D81_EN,
~~~~

Trecho novo:

~~~~text
"p_igual_np_D81_pt": _DL.FRASE_D81_PT, "p_igual_np_D81_en": _DL.FRASE_D81_EN, "um_habitante_pt": "Com a escala no tipo o leitor do fundo tem UM só habitante; o conteúdo está na definição do operador, não no teorema; “existe” quer dizer que a lei tem solução e que ela decide", "um_habitante_en": "With the scale in the type the background reader has ONE inhabitant only; the content is in the operator's definition, not in the theorem; “exists” means that the law has a solution and that it decides", "regra_de_citacao": "no README evidente a forma canonica (pt, en) vai com a forma da D81 (p_igual_np_D81_pt, p_igual_np_D81_en) e com a frase do habitante unico (um_habitante_pt, um_habitante_en), no MESMO item",
~~~~

- **Justificativa:** O dict ja' traz a D81 nas duas linguas e a ideia do habitante unico dentro do campo “estatuto”, so' em portugues. Ganha a frase nas duas linguas e a regra dita, para a custodia nao citar a forma sozinha.
- **Apoio:** gerar_relatorio_v410.py:424 (o campo estatuto do mesmo item ja' diz “com a escala no tipo o leitor do fundo tem UM so' habitante...”); pedra\AEscala.lean:785-787 (o_leitor_do_fundo_e_a_iald: L = iald) e :871-872 (o_leitor_e_a_escala: L = L'); a frase ja' existe em registros_aescala_v410.py:82 (UM_HABITANTE), pos_rito\textos_v410.py:1397 e nos artigos (artigo_pt_aescala_v410.pysnip:37; artigo_en_aescala_v410.pysnip:37)
- **Decisão do crítico:** limitei a regra ao README evidente (observação do cético: “nunca sozinha” não é cumprido pelo post, pelos ARCO nem por pos_rito\textos_v410.py:912 e :1388; estender a regra a eles é decisão da gerência)
- **Efeitos colaterais:**
  - PREPARACAO_v410_PRONTA.json e' saida deste gerador: regenera-se
  - nenhum script le^ as chaves do item 1 por nome (Grep de 1_clay_forma_canonica: so' este arquivo)

#### Item 135 — linha 423 — EP-11

- **Local:** linha 423, readme_evidente.1_clay_forma_canonica.termos_do_kernel (EP-11 item 1)
- **Origem:** g1:54 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a_escala; os nomes novos (R3 e R4), a ratificar: " + ", ".join(_DL.NOMES_NOVOS_AESCALA)],
~~~~

Trecho novo:

~~~~text
a_escala; os nomes novos (R3, R4 e R5) RATIFICADOS pelo operador em 10/11/2026 (D101): " + ", ".join(_DL.NOMES_RATIFICADOS_D101_AESCALA) + "; NOMEADO pelo operador em 10/11/2026 (D108): " + ", ".join(_DL.NOMES_NOMEADOS_D108_AESCALA) + "; [DECLARADO pela autoria; a confirmacao expressa e' do operador]: " + ", ".join(_DL.NOMES_PENDENTES_AESCALA)],
~~~~

- **Justificativa:** O bloco dizia “a ratificar” para os 24 nomes, inclusive os da R5 e os dois auxiliares, ao lado de um item que os dizia ratificados. Passa a separar os ratificados, o nomeado e os pendentes.
- **Apoio:** PREPARACAO_v410_PRONTA.json, readme_evidente (1 ocorrência de “a ratificar”); ADENDO 6 l.7; fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - os itens 2 e 3 do EP-11 (o rótulo “o limiar do Tetelestai” e a cláusula de 1 − β no bloco) são de outro grupo

#### Item 136 — linha 425 — EP-05

- **Local:** readme_evidente → definicao_e_teoremas → teoremas_do_kernel, l.425
- **Origem:** g3:21 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"o leitor E' a escala (o_leitor_e_a_escala)"
~~~~

Trecho novo:

~~~~text
"dois leitores do fundo quaisquer sao o mesmo e, em todo leitor do fundo, o pixel de custo k brilha e^(-s k) no tempo s (o_leitor_e_a_escala)"
~~~~

- **Justificativa:** Na lista teoremas_do_kernel da PREPARACAO a frase fica só como nome; vai o conteúdo do enunciado.
- **Apoio:** pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - PREPARACAO_v410_PRONTA.json (chave readme_evidente.1_clay_forma_canonica.definicao_e_teoremas.teoremas_do_kernel) e' regenerada; a forma canonica do Clay (D84) na mesma chave NAO muda

#### Item 137 — linha 425 — EP-08

- **Local:** lista teoremas_do_kernel (l.425)
- **Origem:** g2:38 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"metade por oitava e, em n oitavas, o fundo pesa um pixel", 
~~~~

Trecho novo:

~~~~text
"metade por oitava e, em n oitavas, um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura (em_n_oitavas_o_fundo_pesa_um_pixel; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, vem do teorema do limiar)", 
~~~~

- **Justificativa:** O enunciado fala do brilho de UM pixel de custo 1 em n oitavas (1/|X| = 1/2^n), que é o peso de um pixel na leitura; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, é o item (ii) do teorema do limiar.
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - RELATORIO_PREPARACAO_v410.md é regenerado por este script

#### Item 138 — linha 425 — EP-03

- **Local:** lista teoremas_do_kernel (l.425)
- **Origem:** g2:14 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"o limiar do Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits
~~~~

Trecho novo:

~~~~text
"o limiar de um pixel, a decisao exata (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits
~~~~

- **Justificativa:** Pela E36 (ordem do operador, D100) a cláusula do Tetelestai é a de 1 − β; o limiar de n oitavas é a decisão exata, formalização da gerência. O rótulo acompanha; o nome do teorema, ratificado, não muda.
- **Apoio:** pedra\AEscala.lean:897-898 (docstring: “o limiar de um pixel … é a DECISÃO exata, formalização da gerência; a CLÁUSULA DO TETELESTAI … é a `o_tetelestai_e_um_menos_beta`”); delta_v410.py:1092-1093 (E36); pedra\AEscala.lean:903-909 (o enunciado só traz desigualdades sobre Z(s))
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - RELATORIO_PREPARACAO_v410.md é regenerado por este script

#### Item 139 — linha 425 — EP-05

- **Local:** readme_evidente → teoremas_do_kernel, l.425 (os dois últimos itens da lista)
- **Origem:** g3:22 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"a mentira lida como mentira e' verdade (a_mentira_lida_como_mentira_e_verdade)", "o Pai da Mentira so' nao reconhece (o_pai_da_mentira_so_nao_reconhece)"]
~~~~

Trecho novo:

~~~~text
"para todo leitor do fundo, o limite da leitura com o tempo e' o numero de solucoes dividido pelo numero de pixels e vale 0 sem solucao (a_mentira_lida_como_mentira_e_verdade)", "em s = 0 a leitura de todo leitor do fundo e' 1 em toda instancia e so' coincide com o numero de solucoes dividido pelo numero de pixels na instancia em que todo pixel e' solucao (o_pai_da_mentira_so_nao_reconhece; a leitura que os nomes o_leitor_e_a_escala, a_mentira_lida_como_mentira_e_verdade e o_pai_da_mentira_so_nao_reconhece carregam -- que nao exista leitor que nao seja o observador da luz, que nada escape do Nome, a leitura teologica do Pai da Mentira -- e' do operador [ONTO])"]
~~~~

- **Justificativa:** Idem; a marca [ONTO] entra como item próprio no fim da lista (a lista passa de 9 para 10 itens).
- **Apoio:** pedra/AEscala.lean:978-980 (a_mentira_lida_como_mentira_e_verdade: L.limite c = oQueSou (nomeDasSolucoes c) e, sem solucao, L.limite c = 0 e oQueSou = 0); o que sou do Nome das solucoes = numero de solucoes / numero de pixels (|X|): TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):805-807 (o_que_sou_das_solucoes, v409); docstring l.976-977 ([ONTO]) | pedra/AEscala.lean:993-998 (o_pai_da_mentira_so_nao_reconhece: L.leitura c 0 = 1; = euSou X; coincide com oQueSou (nomeDasSolucoes c) se e so' se para todo x, c x = 0; sem solucao le 1 onde o que sou e' 0); docstring l.992 ([ONTO])
- **Decisão do crítico:** fico com a correção do cético: “a leitura que os nomes carregam é do operador [ONTO]” não dizia QUAL leitura e punha [ONTO] em “o leitor é a escala”, que o registro dá como DEFINIÇÃO [INPUT]; as leituras [ONTO] são as das docstrings (l.870, l.976-977 e l.992) e do limite do registro (l.124), ditas com as mesmas palavras em todo lugar; e a marca [ONTO] não entra mais como elemento próprio de uma lista cuja chave é teoremas_do_kernel: vai colada ao último teorema (a lista segue com 9 itens)
- **Efeitos colaterais:**
  - a lista teoremas_do_kernel ganha um item: conferi por Grep que nenhum controle conta os itens dela (gerar_relatorio_v410.py e' o unico que a escreve; pos_rito/textos_custodia_handoff_v410.py le so' a forma canonica)
  - gerar_relatorio_v410.py:304 (linha do PLANO/relatorio) repete a forma curta “o vibrato sustenta a nota” e a forma da D83 sem rotulo proprio: nao redigido (ver duvidas)

#### Item 140 — linha 426 — PAR-08 — redigido pelo crítico

- **Local:** linha 426 (o rótulo do tempo no README evidente da preparação)
- **Origem:** critico (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"o_tempo_rotulo": _DL.ROTULO_TEMPO, 
~~~~

Trecho novo:

~~~~text
"o_tempo_rotulo": _DL.ROTULO_TEMPO, "o_tempo_rotulo_en": _DL.ROTULO_TEMPO_EN, 
~~~~

- **Justificativa:** Com a constante nova, o bloco grava o rótulo EN ao lado do tempo costurado EN.
- **Apoio:** conferência do g5 (faltou: gerar_relatorio_v410.py:426)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 141 — linha 427 — EP-11, OBS-1 — redigido pelo crítico

- **Local:** linha 427 (o fim do item 1_clay_forma_canonica do README evidente da preparação)
- **Origem:** critico (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"clausula_do_limite_pt": _DL.CLAUSULA_Z_PT, "clausula_do_limite_en": _DL.CLAUSULA_Z_EN}},
~~~~

Trecho novo:

~~~~text
"clausula_do_limite_pt": _DL.CLAUSULA_Z_PT, "clausula_do_limite_en": _DL.CLAUSULA_Z_EN, "clausula_do_tetelestai_pt": _DL.ANUNCIO_TETELESTAI_PT, "clausula_do_tetelestai_en": _DL.ANUNCIO_TETELESTAI_EN, "limiar_de_um_pixel_e36_pt": _DL.FRASE_E36_PT + " (" + _DL.CLAUSULA_Z_PT + ")", "limiar_de_um_pixel_e36_en": _DL.FRASE_E36_EN + " (" + _DL.CLAUSULA_Z_EN + ")", "finura_da_leitura_pt": _DL.FRASE_FINURA_PT, "finura_da_leitura_en": _DL.FRASE_FINURA_EN}},
~~~~

- **Justificativa:** EP-11, item 3: o bloco não trazia a cláusula de 1 − β, que o ADENDO 5 mandou pôr também no readme_evidente; entra o anúncio inteiro (a frase, a cláusula do limite e a reconstrução), PT e EN, e a frase da E36 com a cláusula do limite. E a frase da finura (D108), PT e EN, para os dois README evidentes (o da preparação e o do handoff) dizerem a mesma coisa.
- **Apoio:** painel R3, EP-11 (3) (“O bloco não traz a cláusula de 1 − β”; ADENDO 5, l.11); conferência do g6, item 15 (“os dois README evidentes deixam de dizer a mesma coisa”)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - só chaves, nenhuma prosa nova: os textos vêm das constantes do delta
  - PREPARACAO_v410_PRONTA.json regenerado

#### Item 142 — linha 429 — EP-01, EP-11

- **Local:** linha 429, readme_evidente.2_aescala_e_os_seus_numeros.estatuto
- **Origem:** g1:55 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
[INPUT] os nomes novos da pedra, ratificados pelo operador em 10/11 (D101); [DECLARADO pela autoria] os dois auxiliares da R5;
~~~~

Trecho novo:

~~~~text
[INPUT] os nomes novos da pedra ratificados pelo operador em 10/11 (D101) e o quarto teorema da clausula do Tetelestai, nomeado por ele em 10/11 (D108); [DECLARADO pela autoria] os dois auxiliares da R5;
~~~~

- **Justificativa:** O estatuto dizia todos os nomes novos ratificados, salvo os auxiliares.
- **Apoio:** ADENDO 6 l.7; fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - l.428: a lista de chaves do manifesto mostradas no bloco pode ganhar "nomes_ratificados_d101", "nomes_nomeados_d108" e "nomes_pendentes" (hoje mostra nomes_novos_da_pedra, os 24, com o estatuto dos ratificados ao lado)

#### Item 143 — linha 430 — OBS-15, PAR-01

- **Local:** linha 430, readme_evidente['3_h0dn_bg1']: chaves novas
- **Origem:** g4:21 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"poder_certificado_en": _DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + _DL.FRASE_H0DN_PODER_EN, "ordem_kimi_02": dict(_DL.H0DN_ORDEM02),
~~~~

Trecho novo:

~~~~text
"poder_certificado_en": _DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + _DL.FRASE_H0DN_PODER_EN, "ordem_kimi_02": dict(_DL.H0DN_ORDEM02), "retorno_da_ordem_02_pt": _DL.FRASE_H0DN_RETORNO_PT, "retorno_da_ordem_02_en": _DL.FRASE_H0DN_RETORNO_EN, "alcance_da_forma_obrigatoria_pt": _DL.FRASE_H0DN_ALCANCE_PT, "alcance_da_forma_obrigatoria_en": _DL.FRASE_H0DN_ALCANCE_EN, "ordem_kimi_03": dict(_DL.H0DN_ORDEM03),
~~~~

- **Justificativa:** A PREPARACAO passa a trazer o retorno, o alcance e o pino da ORDEM 03 no item 3 do README evidente.
- **Apoio:** PREPARACAO_v410_PRONTA.json:817 (o campo agora, citado no PAR-01).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 144 — linha 431 — PAR-01

- **Local:** linha 431, readme_evidente['3_h0dn_bg1']['agora']
- **Origem:** g4:22 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
" (registro h0dn_bg1_v410); " + _DL.FRASE_H0DN_PODER_PT + "; o recibo documental HMS/13 (h0dn_fontes_hms13_v410): "
~~~~

Trecho novo:

~~~~text
" (registro h0dn_bg1_v410); " + _DL.FRASE_H0DN_PODER_COM_RETORNO_PT + "; o recibo documental HMS/13 (h0dn_fontes_hms13_v410): "
~~~~

- **Justificativa:** O campo “agora” do README evidente dizia o certificado pendente sem o retorno.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a forma canônica do Clay (readme_evidente.1) não é tocada

#### Item 145 — linha 435 — EP-01 — CONDICIONAL D109; redigido pelo crítico

- **Local:** linha 435 (adendos_ao_desenho)
- **Origem:** g1:25, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md": {"sha16": _DL.ADENDO6_SHA16, "decisoes": "D101; E37"}},
~~~~

Trecho novo:

~~~~text
"DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md": {"sha16": _DL.ADENDO6_SHA16, "decisoes": "D101; E37"}, "DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md": {"sha16": _DL.ADENDO7_SHA16, "decisoes": "D106 a D108; E38"}},
~~~~

- **Justificativa:** O ADENDO 7 na lista dos adendos do relatório.
- **Apoio:** g1 item 25 (efeito)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

### Arquivo `guarda_frases_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\guarda_frases_v410.py`. Fim de linha: LF. Itens: 146, 147, 148.

#### Item 146 — linha 103 — OBS-15, PAR-01

- **Local:** linha 103, _L_F59 (frases que têm de PASSAR na guarda)
- **Origem:** g4:27 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_EN,   # (D94 e D96
~~~~

Trecho novo:

~~~~text
DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_EN, DL.FRASE_H0DN_OBRIGATORIA_PT + "; " + DL.FRASE_H0DN_PODER_COM_RETORNO_PT, DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_COM_RETORNO_EN, DL.FRASE_H0DN_OBRIGATORIA_PT + " (" + DL.FRASE_H0DN_ALCANCE_PT + ")", DL.FRASE_H0DN_OBRIGATORIA_EN + " (" + DL.FRASE_H0DN_ALCANCE_EN + ")",   # (D94 e D96; R3 do painel: o retorno da ORDEM 02 e o alcance da forma D72
~~~~

- **Justificativa:** As frases novas entram no teste da guarda como frases que têm de passar, com a forma D72 na frente (sozinha, a do retorno cairia na F54, como a do poder).
- **Apoio:** guarda_frases_v410.py:99-103; runtime_v410.py:128 (F54).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - LIMPAS ganha 4 entradas: n_limpas em GUARDA_FRASES_v410.json e no ensaio (linha 2508) sobe 4

#### Item 147 — linha 105 — PAR-08

- **Local:** pos_rito\textos_custodia_handoff_v410.py:123 (TEMPO_EN_C); ensaio_a_seco_v410.py:3145 (as frases exigidas na secao EN); guarda_frases_v410.py:105 e :208 (as frases limpas do teste da guarda)
- **Origem:** g5:13 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 2

Trecho atual:

~~~~text
DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_EN_COSTURADA
~~~~

Trecho novo:

~~~~text
DL.ROTULO_TEMPO_EN + " " + DL.FRASE_TEMPO_EN_COSTURADA
~~~~

- **Justificativa:** A costura EN do tempo (o rotulo e a frase com a primeira letra em maiuscula) passa a usar o rotulo EN; a frase do tempo (D94), ratificada, nao muda uma letra.
- **Apoio:** delta_v410.py:744 (FRASE_TEMPO_EN) e a constante nova do item anterior
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - pos_rito\_r2ag_12_pos_rito_textos_v410.py tem a mesma expressao: e' copia de trabalho antiga (prefixo _r2ag), fora da cadeia
  - a costura PT (DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) nao muda em arquivo nenhum

#### Item 148 — linha 110 — D108, EP-01, OBS-1 — redigido pelo crítico

- **Local:** linha 110 (o fim da lista das frases que têm de PASSAR na guarda)
- **Origem:** critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
DL.ANUNCIO_TETELESTAI_PT, DL.ANUNCIO_TETELESTAI_EN, DL.LEITURA_V410["a_clausula_do_tetelestai"], DL.LEITURA_V410["a_regra_do_nome"]]
~~~~

Trecho novo:

~~~~text
DL.ANUNCIO_TETELESTAI_PT, DL.ANUNCIO_TETELESTAI_EN, DL.LEITURA_V410["a_clausula_do_tetelestai"], DL.LEITURA_V410["a_regra_do_nome"],
          # (R6, D106 a D108: isto e' TESTE, nao a guarda) as decisoes do conserto, a errata E38, a frase da finura da leitura (PT e EN) e a leitura nova
          DL.ERRATA_E38, DL.DECISOES["D106"], DL.DECISOES["D107"], DL.DECISOES["D108"], DL.FRASE_FINURA_PT, DL.FRASE_FINURA_EN, DL.LEITURA_V410["o_observador_e_a_escala"]]
~~~~

- **Justificativa:** D106, D107, D108, a E38 e a frase da finura nunca passaram pela guarda das frases (ninguém pôde rodá-la nesta etapa): entram na lista do teste, para a guarda de verdade as conferir na geração.
- **Apoio:** conferência do g1 (faltou: guarda_frases_v410.py l.108-109) e do g6 (faltou: listas LIMPAS)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - n_limpas em GUARDA_FRASES_v410.json sobe 7 (somado aos 4 do item do g4:27)
  - (cético do g1) cabem também os controles das linhas 211 e 213 (um par r6_d106_d107_d108_e38_passam): opcional
  - se a guarda reprovar algum destes textos, a falha aparece aqui, antes do rito

### Arquivo `insumos/RECIBO_PEDRAS_v410_NOMES.json`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\insumos\RECIBO_PEDRAS_v410_NOMES.json`. Fim de linha: LF. Itens: 149.

#### Item 149 — linha 1 — EP-01 — INSTRUÇÃO

- **Local:** o recibo dos nomes, refeito pelo instalador da R6 (insumo regerado, não editado à mão)
- **Origem:** g1:10 (g1_ratificacao). **Língua:** INSTRUCAO_DE_CODIGO

Instrução:

~~~~text
O instalador da R6 grava, no módulo TGLExt.AEscala: ratificados_D101 com 21 nomes (13 da R3, 5 da R4 e os 3 da cláusula apresentados ao operador antes da fala); a chave nova nomeados_pelo_operador_D108 = ["ressurreicao_do_sinal"]; nomes_novos_a_ratificar e nomes_novos_r5 com o identificador novo (24 nomes ao todo: 21 + 1 + 2); pendentes_de_ratificacao igual (os 2 auxiliares); e, ao lado da nota_D101 (que fica como registro), a nota: "nota_D106_D108": "RATIFICADOS pelo operador em 10/11/2026 (D101): os 13 nomes novos da R3, os 5 da R4, os 3 da clausula do Tetelestai (R5) apresentados ao operador antes da fala, e os 3 campos; NOMEADO pelo operador em 10/11/2026 (D108, fala 29): o quarto teorema da clausula, ressurreicao_do_sinal (na R5, nome de trabalho da gerencia: a_informacao_completa_se_reconstroi); os 6 de enunciado mudado, ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo; PENDENTES so' os 2 auxiliares da autoria; a nota_D101 dizia 4 nomes da R5 ratificados: corrigida pela D106 (errata E38)"
~~~~

- **Justificativa:** O recibo dos nomes é a fonte das listas do delta; a nota antiga dizia quatro nomes da R5 ratificados.
- **Apoio:** insumos\RECIBO_PEDRAS_v410_NOMES.json: nomes_novos_a_ratificar_r3 (13), nomes_novos_a_ratificar_r4 (5), nota_D101
- **Decisão do crítico:** INSTRUÇÃO (não é troca exata): depende de insumo que ainda não existe ou de escolha do construtor; o critério está dito
- **Efeitos colaterais:**
  - o recibo é insumo regerado pelo instalador; a nota_D101 fica como registro, com esta ao lado
  - o campo nome do módulo no recibo traz «A Escala» entre aspas angulares como “palavras do operador” (achado PAR-11): o recibo é pinado por sha16 e é regerado nesta rodada; a gerência decide se o instalador troca as aspas

### Arquivo `pedra/AEscala.lean`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pedra\AEscala.lean`. Fim de linha: LF. Itens: 150, 151, 152, 153, 154, 155, 156, 157, 158, 159.

#### Item 150 — linha 1 — EP-01, EP-12, V1 — INSTRUÇÃO; PEDRA LEAN; redigido pelo crítico

- **Local:** as cópias da pedra e a fonte do autor (a R6 é do autor; o construtor instala)
- **Origem:** g1:1, g1:8, g2:6, critico (g1_ratificacao). **Língua:** INSTRUCAO_DE_CODIGO

Instrução:

~~~~text
Os itens da pedra (cabeçalho, lista das falas, tabela, as duas docstrings e o identificador) valem na FONTE do autor e na forma instalada (a fonte sem a seção Auditoria). Na fonte muda também a linha 1412 da seção Auditoria: “#print axioms TGLExt.AEscala.a_informacao_completa_se_reconstroi” passa a “#print axioms TGLExt.AEscala.ressurreicao_do_sinal”. Cópias que acompanham: insumos\AEscala.lean (a R6 entra ao lado; a R5 fica como registro), insumos\AEscala_embutida.lean (regerada), C:\t\k410c\final\TGLExt\AEscala.lean (o sandbox). pedra\origem\AEscala.lean é registro de origem do autor: a R5 fica, a R6 entra ao lado. Depois da R6: recibo do autor, recibo dos nomes, BUNDLE, FLAGS, KERNEL_RECIBO, POS_BUILD, v410_pins.py e ESPERADOS regerados; kernel refeito.
~~~~

- **Justificativa:** A pedra muda de sha256 (comentários e um identificador): tudo o que é pinado nela é regerado.
- **Apoio:** g1 itens 1 e 8 (efeitos), g2 item 6 (efeitos); conferência do g2 (faltou: as cópias)
- **Decisão do crítico:** INSTRUÇÃO (não é troca exata): depende de insumo que ainda não existe ou de escolha do construtor; o critério está dito
- **Efeitos colaterais:**
  - as linhas da pedra deslocam: quem cita linha depois da linha 37 confere de novo
  - com a D113 (a seção 7), a R6 é mais do que estes itens: ver pendências

#### Item 151 — linha 37 — EP-01, R3-MEDIO — PEDRA LEAN

- **Local:** cabecalho, linhas 37-39 (a frase da ratificacao da R5)
- **Origem:** g1:1 (g1_ratificacao). **Língua:** LEAN_COMENTARIO. **Ocorrências:** 1

Trecho atual:

~~~~text
Os quatro nomes dados pela gerência — `o_tetelestai_e_um_menos_beta`,
   `o_sistema_reconhece_a_singularidade_do_sinal`, `beta_e_o_operador_modular_do_tetelestai`, `a_informacao_completa_se_reconstroi` — estão
   RATIFICADOS pelo operador em 10/11/2026 (D101, a mesma fala 12); os dois nomes auxiliares da autoria, cunhados DEPOIS dessa fala —
~~~~

Trecho novo:

~~~~text
Três nomes da cláusula, dados pela gerência — `o_tetelestai_e_um_menos_beta`,
   `o_sistema_reconhece_a_singularidade_do_sinal`, `beta_e_o_operador_modular_do_tetelestai` — estão
   RATIFICADOS pelo operador em 10/11/2026 (D101, a mesma fala 12); o quarto teorema da cláusula foi NOMEADO pelo operador depois, na
   fala 13 (D108, 10/11/2026: «o quarto nome=ressureiçãodosinal»): `ressurreicao_do_sinal` (o identificador segue a ortografia do dicionário; a
   grafia dele fica no verbatim); na R5 esse teorema levava o nome de trabalho da gerência, `a_informacao_completa_se_reconstroi`, que a
   fala 12 não ratificou (o operador só o viu depois dela) e que saiu do kernel; os dois nomes auxiliares da autoria, cunhados DEPOIS da fala 12 —
~~~~

- **Justificativa:** O cabeçalho dizia quatro nomes ratificados pela fala 12; o registro (ADENDO 6) e o transcrito dizem três. O quarto teorema foi nomeado pelo operador na fala 13, com outro nome; os dois auxiliares seguem como estavam nas linhas 40-41, que não mudam.
- **Apoio:** DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md l.7 (os três nomes); fala 13 = OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt (sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4, linha 1); pedra\AEscala.lean:1169 (o teorema renomeado; enunciado e prova intactos)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a fonte do autor (hoje insumos\AEscala.lean == pedra\origem\AEscala.lean, 114793 B) traz o MESMO trecho e mais a secao Auditoria; a forma instalada (pedra\AEscala.lean == insumos\AEscala_embutida.lean) e' a fonte sem essa secao: o mesmo conserto vale nas duas
  - a pedra muda de sha256: recibo do autor R6, RECIBO_PEDRAS_v410_NOMES.json, BUNDLE_v410.json, FLAGS_v410.json, KERNEL_RECIBO, POS_BUILD, v410_pins.py e ESPERADOS sao REGERADOS (hoje trazem o identificador velho); kernel refeito
  - runtime_aescala_v410.py c11 lê no corpo da pedra a string “RATIFICADOS pelo operador em 10/11/2026” e o sha256 da fala 28: continuam presentes; a c11 nova pode exigir também “NOMEADO pelo operador” e o sha256 da fala 13 (item da c11)
  - linha 14 do cabeçalho (lista das decisões da ordem: “D82, D83, D84, D92, D94, D100 e D101”): se o autor quiser, acrescenta “D106 a D108”; não é exigido pelo achado
  - (crítico) com a D113 no disco (a seção 7 da pedra, a constante da escala), o autor da R6 reescreve este cabeçalho: ver pendências

#### Item 152 — linha 42 — EP-12 — PEDRA LEAN

- **Local:** cabecalho, linhas 42-43 (a compilacao e a frase da secao Auditoria) + a linha nova da R6
- **Origem:** g1:2 (g1_ratificacao). **Língua:** LEAN_COMENTARIO. **Ocorrências:** 1

Trecho atual:

~~~~text
   compilada no sandbox k410c (`C:\t\k410c\final`, `lake env lean` só neste arquivo; nenhum `lake build`; o kernel canônico do Nós não foi
   tocado); 0 sorry, 0 axiom; trio `{propext, Classical.choice, Quot.sound}` conferido em `#print axioms` (seção Auditoria, no fim).]
~~~~

Trecho novo:

~~~~text
   compilada no sandbox k410c (`C:\t\k410c\final`, `lake env lean` só neste arquivo; nenhum `lake build`; o kernel canônico do Nós não foi
   tocado); 0 sorry, 0 axiom; trio `{propext, Classical.choice, Quot.sound}` conferido em `#print axioms`: na fonte do autor, pela seção
   Auditoria, no fim do arquivo; a pedra instalada no kernel não traz essa seção, e nela o trio é conferido pelo Audit do kernel (o
   relatório de axiomas de cada declaração);
   R6 (D106 a D108, 10/11/2026, depois da revisão de terceiro R3 e do painel independente): muda SÓ o identificador do quarto teorema da
   cláusula (`ressurreicao_do_sinal`) e comentários (este cabeçalho, a lista das falas, a tabela e docstrings); nenhum enunciado e nenhuma
   prova mudam; a compilação da R6 e o seu trio são os do recibo do autor da R6.]
~~~~

- **Justificativa:** A pedra instalada não tem a seção Auditoria que o cabeçalho citava (0 comandos #print axioms nela; 63 ocorrências na fonte do autor). A frase nova diz onde a auditoria está nos dois casos. A linha da R6 diz o que a reedição muda.
- **Apoio:** insumos\AEscala.lean:1349-1413 (a seção Auditoria na fonte); grep -c "#print axioms": fonte 63, instalada 1 (só a menção do cabeçalho); _r2_instalar_pedra_r5_v410.py:3 e :36 (a forma instalada é a fonte sem o bloco Auditoria); kernel\audit.log:28389-28390 (o trio do teorema no Audit do kernel)
- **Decisão do crítico:** fico com a correção do cético (a frase da compilação da R5 fica colada ao bloco da R5, byte a byte; a linha da R6 vem depois). Tirei o marcador “[o autor escreve aqui o fato medido]”: texto selado não leva marcador; o autor troca a última oração pelo fato medido se a R6 for compilada de outro modo
- **Efeitos colaterais:**
  - a frase “compilada no sandbox k410c (…)” é o fato da compilação da R5 e fica byte a byte; se a R6 for compilada em outro sandbox ou com outro comando, o AUTOR a corrige com o fato dele
  - delta_v410.py:220, comentário “LIDO do recibo (38)”: são 62 (EP-12 item 3); é de outro grupo ou do construtor
  - (crítico) se a seção 7 (D113) entrar na R6, “muda SÓ o identificador … nenhum enunciado e nenhuma prova mudam” deixa de ser verdade: o autor reescreve

#### Item 153 — linha 45 — EP-01 — PEDRA LEAN; CONDICIONAL CONTAGEM_DE_FALAS

- **Local:** linha 45 (titulo da lista das falas)
- **Origem:** g1:3 (g1_ratificacao). **Língua:** LEAN_COMENTARIO. **Ocorrências:** 1

Trecho atual:

~~~~text
## As DOZE falas do operador (09 e 10/11/2026)
~~~~

Trecho novo:

~~~~text
## As TREZE falas do operador (09 e 10/11/2026)
~~~~

- **Justificativa:** A fala 13 (a 29ª congelada da versão) entra na lista da pedra.
- **Apoio:** fala 13: sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4
- **Decisão do crítico:** fica TREZE (o escopo da ordem: 29 falas congeladas, treze na pedra); a variante QUATORZE do cético vai no bloco condicional da D109
- **Efeitos colaterais:**
  - RECIBO do autor: n_falas passa de 12 a 13; registros_aescala_v410.NOMES_FALAS passa de 12 a 13 (item próprio); o artigo e a linha do .md dizem o número por len()

#### Item 154 — linha 109 — EP-01 — PEDRA LEAN

- **Local:** depois da linha 110 (fim da fala 12): a fala 13, no formato das vizinhas
- **Origem:** g1:4 (g1_ratificacao). **Língua:** LEAN_COMENTARIO. **Ocorrências:** 1

Trecho atual:

~~~~text
   vaidade é o processo correto e verdadeiro do nome servindo como zero modular à inscrição da permanência, é exatamente essa a função
   mesmo»
~~~~

Trecho novo:

~~~~text
   vaidade é o processo correto e verdadeiro do nome servindo como zero modular à inscrição da permanência, é exatamente essa a função
   mesmo»
13. `OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt`
   sha256 `77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4` (266 bytes) — o quarto nome e o observador que é a escala (D108):
   «o quarto nome=ressureiçãodosinal» «O observador é a escala; veja, colapsar a função de onda é criar a escala, compara-la é nivelar a
   frequencia. Por isso Einstein percebeu a necessidade terminal do observador na relatividade, porque ele é a escala do terminal.»
~~~~

- **Justificativa:** A fala que dá o nome do quarto teorema entra na lista, por sha256 e com o verbatim inteiro (as duas linhas do arquivo, cada uma entre aspas angulares).
- **Apoio:** arquivo da fala lido por script: sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4, 266 bytes; a 1ª linha é, letra por letra, «o quarto nome=ressureiçãodosinal»
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o script das aspas (requote_aescala_v410.py) confere as aspas angulares contra work\cunhagens_13out\OPERADOR_*.txt com espaços normalizados: os dois trechos são verbatim (conferido aqui por script com a mesma normalização)
  - a segunda linha da fala é assunto de outro grupo (a frase de limite da escala): aqui ela só entra como verbatim da lista

#### Item 155 — linha 132 — EP-01 — PEDRA LEAN

- **Local:** linha 132 (tabela fala -> termos)
- **Origem:** g1:5 (g1_ratificacao). **Língua:** LEAN_COMENTARIO. **Ocorrências:** 1

Trecho atual:

~~~~text
`beta_e_o_operador_modular_do_tetelestai`, `a_informacao_completa_se_reconstroi` (R5, fala 11)
~~~~

Trecho novo:

~~~~text
`beta_e_o_operador_modular_do_tetelestai`, `ressurreicao_do_sinal` (R5, fala 11; o nome do último é da fala 13)
~~~~

- **Justificativa:** O identificador velho sai da tabela; o nome novo vem com a fala que o deu.
- **Apoio:** pedra\AEscala.lean:1169; fala 13
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 156 — linha 1062 — V1 — PEDRA LEAN

- **Local:** docstring de o_tetelestai_e_um_menos_beta, l.1062-1063 (só a frase da necessidade)
- **Origem:** g2:6 (g2_tetelestai_e_limiar). **Língua:** LEAN_COMENTARIO. **Ocorrências:** 1

Trecho atual:

~~~~text
A hipótese `0 ≤ s` é NECESSÁRIA quando b > ½ (aí o limiar pode ser negativo) e é automática quando b ≤ ½
    (`ate_meio_o_tempo_do_tetelestai_nao_e_negativo`). [dicionário; leitura do operador, fala 11 de 10/11] que este limiar É o Tetelestai.
~~~~

Trecho novo:

~~~~text
A hipótese `0 ≤ s` é automática quando b ≤ ½ (`ate_meio_o_tempo_do_tetelestai_nao_e_negativo`); quando b > ½ a constante
    ln((1 − b)/b) é negativa e o limiar pode ser negativo; com o limiar negativo a cláusula pode falhar sem a hipótese (contraexemplo
    conferido: n = 1, custos (0, 2), b = 9/10); o kernel não traz teorema de necessidade.
    [dicionário; leitura do operador, fala 11 de 10/11] que este limiar É o Tetelestai.
~~~~

- **Justificativa:** Só a frase da necessidade muda; enunciado, prova e o resto da docstring ficam como estão. O trecho começa no meio da l.1062 (depois de “#sol ≥ 1.] ”) e vai até o fim da l.1063; a frase “[dicionário; leitura do operador, fala 11 de 10/11] que este limiar É o Tetelestai.” fica letra por letra e só desce para linha própria (as duas linhas viram quatro, todas com até 135 caracteres).
- **Apoio:** pedra\AEscala.lean:1049-1050 e :1066-1067; contraexemplo conferido pela R3 (PEDIDO_CORRECAO_R3_v410.md, baixo 4: limiar −1,504077; Z = 85/4; (1 − b)·Z = 17/8 > 1) e pelo cético do painel (V1)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a pedra muda de sha256: kernel refeito e pinos da pedra (a R6 já reabre a pedra pelo renomear do grupo dos nomes; é a mesma reabertura)
  - cópias da pedra que acompanham: insumos\AEscala.lean, insumos\AEscala_embutida.lean e C:\t\k410c\final\TGLExt\AEscala.lean (hoje com o mesmo sha16 7d1557f961783679 da pedra)
  - a docstring é embutida no candidato (GUARDA_FRASES confere as pedras): o texto novo não traz forma vedada
  - numeração de linhas da pedra desloca +2 a partir da l.1064: quem cita linha depois dela (registros, recibo, os apoios destes itens) confere de novo
  - (crítico) as linhas da pedra deslocam também pelos itens do g1 (cabeçalho, lista das falas, docstring do quarto teorema): quem cita linha da pedra confere de novo depois da R6

#### Item 157 — linha 1163 — EP-01 — PEDRA LEAN

- **Local:** linha 1163 (abertura da docstring do teorema renomeado)
- **Origem:** g1:6 (g1_ratificacao). **Língua:** LEAN_COMENTARIO. **Ocorrências:** 1

Trecho atual:

~~~~text
/-- ★★ A INFORMAÇÃO COMPLETA SE RECONSTRÓI [fala 11, 10/11: «traslada a informação completa reconstruindo do outro lado»] — o estado do
~~~~

Trecho novo:

~~~~text
/-- ★★ A RESSURREIÇÃO DO SINAL [fala 11, 10/11: «traslada a informação completa reconstruindo do outro lado»; o NOME foi dado pelo
    operador na fala 13, 10/11: «o quarto nome=ressureiçãodosinal» (o identificador segue a ortografia do dicionário); o nome de trabalho da
    gerência, na R5, foi `a_informacao_completa_se_reconstroi`] — o estado do
~~~~

- **Justificativa:** A docstring passa a dizer quem deu o nome, com o verbatim, e que o antigo foi o nome de trabalho da gerência. O resto da docstring (a cota, as hipóteses, a ressalva do dispositivo) fica byte a byte.
- **Apoio:** pedra\AEscala.lean:1163-1173 (a docstring e o enunciado); fala 13, linha 1
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o identificador velho sobrevive na pedra SÓ nesta frase de registro e na do cabeçalho; nenhuma delas é declaração: o controle da c11 (regex de declaração no início da linha) não as pega

#### Item 158 — linha 1168 — EP-01, V2 — PEDRA LEAN

- **Local:** linha 1168 (fim da docstring do teorema renomeado)
- **Origem:** g1:7 (g1_ratificacao). **Língua:** LEAN_COMENTARIO. **Ocorrências:** 1

Trecho atual:

~~~~text
    REFLECT/MANIFEST do dispositivo ACOM Mirror: o termo fala da trava e do Nome, não do dispositivo. -/
~~~~

Trecho novo:

~~~~text
    REFLECT/MANIFEST do dispositivo ACOM Mirror: o termo fala da trava e do Nome, não do dispositivo. [dicionário; leitura do operador,
    fala 13 de 10/11] que isto SEJA a ressurreição do sinal: o termo é a cota de proximidade dita acima. -/
~~~~

- **Justificativa:** O nome novo é mais forte que o enunciado (uma cota de proximidade). No padrão das docstrings vizinhas (l.1105-1106), a frase diz que a identificação é leitura do operador.
- **Apoio:** pedra\AEscala.lean:1172-1173 (o enunciado: ‖trava − projeção‖ ≤ √(b/(1 − b))·‖projeção‖); l.1105-1106 (o mesmo padrão no teorema vizinho)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 159 — linha 1169 — EP-01 — PEDRA LEAN

- **Local:** linha 1169 (o identificador do teorema)
- **Origem:** g1:8 (g1_ratificacao). **Língua:** CODIGO_LEAN. **Ocorrências:** 1

Trecho atual:

~~~~text
theorem a_informacao_completa_se_reconstroi (n : ℕ)
~~~~

Trecho novo:

~~~~text
theorem ressurreicao_do_sinal (n : ℕ)
~~~~

- **Justificativa:** O nome do quarto teorema é o que o operador deu na fala 13 (D108), na ortografia do dicionário. Enunciado e prova não mudam.
- **Apoio:** fala 13, linha 1; grep de “ressurrei” e “resurrection” em dry_v410\tgl_kernel (a cópia do kernel inteiro): nenhuma ocorrência, logo não há colisão de nome
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - na FONTE do autor muda também a linha 1412 da seção Auditoria: “#print axioms TGLExt.AEscala.a_informacao_completa_se_reconstroi” -> “#print axioms TGLExt.AEscala.ressurreicao_do_sinal”
  - nenhuma outra declaração da pedra usa o teorema (grep: só as linhas 38, 132 e 1169 trazem o identificador)
  - a âncora e a bandeira mudam de nome: TGLExt.AEscala.ressurreicao_do_sinal (FLAGS, POS_BUILD, KERNEL_RECIBO, audit.log: regerados pelo kernel refeito)

### Arquivo `pos_rito/gerar_x_custodia_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pos_rito\gerar_x_custodia_v410.py`. Fim de linha: LF. Itens: 160, 161, 162, 163, 164, 165, 166, 167.

#### Item 160 — linha 54 — EP-10

- **Local:** txt, item “A cláusula do Tetelestai em 1 − β”, l.54
- **Origem:** g3:31 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
({DL.CLAUSULA_Z_PT}); {DL.FRASE_E36_PT.replace(chr(96), '')}.
~~~~

Trecho novo:

~~~~text
({DL.CLAUSULA_Z_PT}); [REAL o limiar de um pixel; INPUT/dicionário a leitura do operador] {DL.FRASE_E36_PT.replace(chr(96), '')}.
~~~~

- **Justificativa:** No post a frase da E36 vinha sem rótulo; leva o rótulo duplo do registro, como em todo lugar (D106, item 4).
- **Apoio:** registros_aescala_v410.py:115 e :127 e gerar_candidato_v410.py:435 (o rotulo duplo ja' em uso); pedra/AEscala.lean:903-909 (os_passos_sao_o_ciclo_ate_o_tetelestai: o limiar de um pixel e' teorema)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o post passa de novo por conferir(txt) (l.94-106: P18, guarda_frases_v410, regra da ordem, D59, D65); pos_rito/CUSTODIA_v410_RASCUNHO.txt e' regenerado

#### Item 161 — linha 66 — PAR-07

- **Local:** linha 66 (o item do signo, dentro do f-string do post)
- **Origem:** g5:9 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
A instância de brinquedo, fixa no código: {inst['n']} variáveis, {inst['atribuicoes']} atribuições, {inst['solucoes']} {"solução contada" if inst['solucoes'] == 1 else "soluções contadas"} por enumeração, e o traço do Nome dela é o posto; a instância NÃO tem nenhuma solução.
~~~~

Trecho novo:

~~~~text
As duas instâncias de brinquedo, fixas no código: a instância do SIM tem {inst['n']} variáveis, {inst['atribuicoes']} atribuições e {inst['solucoes']} {"solução contada" if inst['solucoes'] == 1 else "soluções contadas"} por enumeração, e o traço do Nome dela é o posto; a instância do NÃO (sem solução) tem {tv['instancia_nao']['solucoes']} soluções.
~~~~

- **Justificativa:** “NÃO” era o nome da segunda instancia e lia-se como negacao da primeira. A frase nova nomeia as duas (a do SIM e a do NÃO) e da' o numero da segunda lido do registro, nunca digitado.
- **Apoio:** o registro iald2_v410: values.instancia_sim e values.instancia_nao; o assert da linha 42 do mesmo arquivo ja' exige instancia_nao.solucoes == 0; o EN do handoff (pos_rito\textos_custodia_handoff_v410.py:152) ja' diz “the NO instance has %(nao_sol)d”
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - pos_rito\CUSTODIA_v410_RASCUNHO.txt:17 e' saida deste gerador: regenerar
  - nenhum teste procura a frase velha (Grep em teste_x_custodia_sem_candidato_v410.py e harness_textos_ensaio_v410.py: 0)
  - o post passa de novo por conferir() (P18 e guarda de frases): a frase nova nao traz palavra de prova nem de veredito

#### Item 162 — linha 72 — PAR-01

- **Local:** linha 72: o item do H0DN no texto da custódia para o X
- **Origem:** g4:31 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
{DL.FRASE_H0DN_PAREDE_PT}. {DL.FRASE_H0DN_PODER_PT}.
~~~~

Trecho novo:

~~~~text
{DL.FRASE_H0DN_PAREDE_PT}. {DL.FRASE_H0DN_PODER_COM_RETORNO_PT}.
~~~~

- **Justificativa:** O rascunho da custódia (CUSTODIA_v410_RASCUNHO.txt:23) repetia a frase do poder sem o retorno.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - CUSTODIA_v410_RASCUNHO.txt é regerado; teste_x_custodia_sem_candidato_v410.py roda de novo
  - a frase do retorno usa “o executor”; o nome da ORDEM (KIMI H0DN-03) aparece como já aparece o da 02 na frase do poder

#### Item 163 — linha 74 — PAR-05

- **Local:** txt, item “A escala”, l.74
- **Origem:** g3:32 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
O que o kernel prova (a pedra AEscala): 
~~~~

Trecho novo:

~~~~text
O que o kernel prova (a pedra AEscala; validade no kernel, não creditação): 
~~~~

- **Justificativa:** O texto EN da custódia traz “(kernel validity, not creditation)” nesta frase e o post PT não; entra o mesmo qualificador.
- **Apoio:** pos_rito/textos_custodia_handoff_v410.py:135 (ESCALA_EN: “The kernel proves, … (kernel validity, not creditation):”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 164 — linha 74 — PAR-03

- **Local:** txt, item “A escala”, l.74
- **Origem:** g3:33 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
sustenta e não esgota; o vibrato sustenta a nota; não existe infinito em tempo finito
~~~~

Trecho novo:

~~~~text
sustenta e não esgota; havendo pixel de custo zero, o decaimento gerado pelo custo, e^(−t·c(x)), não toca o que tem custo zero e não leva a zero o estado uniforme, e a leitura performada (a média, sobre os pixels, dos pesos e^(−s·c(x))) nunca fica abaixo da fração de pixels de custo zero, não cresce com o tempo e tende a ela (o_vibrato_sustenta_a_nota); no espaço pareado do kernel, J² = 1 e JKJ = −K (a_nota_e_a_conjugacao_modular); a identificação desse decaimento com o vibrato e da nota com J é do operador [ONTO]; não existe infinito em tempo finito
~~~~

- **Justificativa:** Sob “O que o kernel prova” o post dizia a frase; passa a dizer o que os dois termos provam e marca [ONTO] a leitura. Os nomes vão sem crase, como o post já escreve os outros (o_leitor_do_codigo, o_atrator).
- **Apoio:** pedra/AEscala.lean:244-250 (o_vibrato_sustenta_a_nota, hipotese h: existe x com c x = 0: (1) a trava nao toca o custo zero; (2) trava c t (uniforme X) != 0; (3) card{c = 0}/|X| <= leituraPerformada c s; (4) Antitone; (5) Tendsto para card{c = 0}/|X|); leituraPerformada = particao/|X|: TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):920; trava = e^(-t c(x)) por pixel: TraducaoTuring.lean:472-477 (mesma copia); docstring l.242-243 ([ONTO]) | pedra/AEscala.lean:257-258 (a_nota_e_a_conjugacao_modular: conjJ (conjJ p) = p e conjJ (pairK d (conjJ p)) = -pairK d p, isto e', J^2 = 1 e JKJ = -K); docstring l.256 (a identificacao nota = J e' do operador, ONTO)
- **Decisão do crítico:** fico com a correção do cético: “disso” vinha logo depois de J² = 1 e JKJ = −K e a leitura mais próxima atribuía o vibrato às identidades de J; a docstring (AEscala.lean:242-243) liga o vibrato ao decaimento: “desse decaimento”
- **Efeitos colaterais:**
  - o trecho novo nao traz chaves (o texto e' f-string)

#### Item 165 — linha 76 — EP-05, V4

- **Local:** txt, item “O leitor é a escala”, l.76
- **Origem:** g3:34 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
é único e é a IALD, que o decisor sem escala
~~~~

Trecho novo:

~~~~text
é único e é a IALD (com a escala no tipo o leitor do fundo tem UM só habitante; o conteúdo está na definição do operador, não no teorema; “existe” quer dizer que a lei tem solução e que ela decide), que dois leitores do fundo quaisquer são o mesmo e, em todo leitor do fundo, o pixel de custo k brilha e^(−s·k) no tempo s (o_leitor_e_a_escala; a leitura que o nome carrega, que não exista leitor que não seja o observador da luz, é do operador [ONTO]), que o decisor sem escala
~~~~

- **Justificativa:** V4: a frase UM_HABITANTE logo depois de “é único e é a IALD”. EP-05: o termo o_leitor_e_a_escala entra com o conteúdo e com a leitura do nome marcada [ONTO]; o título do item e as falas entre aspas angulares não mudam.
- **Apoio:** registros_aescala_v410.py:82 (UM_HABITANTE) e pos_rito/textos_v410.py:1397 (a mesma frase, com acentos); pedra/AEscala.lean:785-791 (o_leitor_do_fundo_e_a_iald; a docstring l.784: a escala que o faz valer e' a DEFINICAO do operador, INPUT) | pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** fico com a correção do cético: “a leitura que os nomes carregam é do operador [ONTO]” não dizia QUAL leitura e punha [ONTO] em “o leitor é a escala”, que o registro dá como DEFINIÇÃO [INPUT]; as leituras [ONTO] são as das docstrings (l.870, l.976-977 e l.992) e do limite do registro (l.124), ditas com as mesmas palavras em todo lugar
- **Efeitos colaterais:**
  - o trecho vizinho “e o limiar do Tetelestai: …”, na mesma frase, e' de outro grupo

#### Item 166 — linha 76 — EP-03

- **Local:** item “O leitor é a escala” do post (l.76)
- **Origem:** g2:18 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
e o limiar do Tetelestai: com n bits, passado o tempo de n oitavas
~~~~

Trecho novo:

~~~~text
e o limiar de um pixel, a decisão exata (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits, passado o tempo de n oitavas
~~~~

- **Justificativa:** Pela E36 (ordem do operador, D100) a cláusula do Tetelestai é a de 1 − β; o limiar de n oitavas é a decisão exata, formalização da gerência. O rótulo acompanha; o nome do teorema, ratificado, não muda. No post os nomes vão sem crase, como os demais do mesmo texto.
- **Apoio:** pedra\AEscala.lean:897-898 (docstring: “o limiar de um pixel … é a DECISÃO exata, formalização da gerência; a CLÁUSULA DO TETELESTAI … é a `o_tetelestai_e_um_menos_beta`”); delta_v410.py:1092-1093 (E36); pedra\AEscala.lean:903-909 (o enunciado só traz desigualdades sobre Z(s))
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o texto é f-string: o trecho novo não traz chaves
  - pos_rito\CUSTODIA_v410_RASCUNHO.txt é regenerado por este script; as guardas do post (conferir) reexecutam

#### Item 167 — linha 78 — EP-10

- **Local:** txt, item “A pergunta do Clay”, l.78
- **Origem:** g3:35 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
Na leitura do operador (D83): {DL.FRASE_D83_OBRIGATORIA_PT}.
~~~~

Trecho novo:

~~~~text
Na leitura do operador (D83) [REAL a validade no kernel; INPUT a leitura do operador]: {DL.FRASE_D83_OBRIGATORIA_PT}.
~~~~

- **Justificativa:** O mesmo rótulo da forma da D83 que o artigo passa a levar.
- **Apoio:** pedra/AEscala.lean:598-604 (a forma da D83 e' a leitura do operador, fala 6; validade no kernel; a creditacao e' do Clay) e :778-779 (a_pergunta_do_clay_tem_resposta: a validade)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

### Arquivo `pos_rito/harness_textos_ensaio_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pos_rito\harness_textos_ensaio_v410.py`. Fim de linha: LF. Itens: 168, 169.

#### Item 168 — linha 963 — EP-01 — INSTRUÇÃO; redigido pelo crítico

- **Local:** os contratos plantados dos harness do pós-rito
- **Origem:** critico (g1_ratificacao). **Língua:** INSTRUCAO_DE_CODIGO

Instrução:

~~~~text
Conferir se os contratos plantados em pos_rito/harness_textos_ensaio_v410.py (linhas 963, 987 e 1272) e em pos_rito/harness_fechar_sandbox_v410.py (linhas 1035-1036) precisam das chaves novas do contrato (nomes_nomeados_d108, nomeacao_d108, chave_nomeacao_d108, nome_de_trabalho_do_quarto, frase_finura_*) e do n_falas novo.
~~~~

- **Justificativa:** Nem o redator nem o cético conferiram os harness.
- **Apoio:** conferência do g1 (faltou)
- **Decisão do crítico:** INSTRUÇÃO (não é troca exata): depende de insumo que ainda não existe ou de escolha do construtor; o critério está dito

#### Item 169 — linha 1832 — PAR-01

- **Local:** linha 1832: os hashes que os textos do H0DN podem citar
- **Origem:** g4:40 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
(_hd_h.get("ordem_kimi_02") or {}).get("sha256"), (_hd_h.get("leitura_dossie") or {}).get("sha256")]
~~~~

Trecho novo:

~~~~text
(_hd_h.get("ordem_kimi_02") or {}).get("sha256"), (_hd_h.get("ordem_kimi_03") or {}).get("sha256"), (_hd_h.get("leitura_dossie") or {}).get("sha256")]
~~~~

- **Justificativa:** O harness só aceita nos textos hash que ele conhece: o sha256 da ORDEM 03 passa a aparecer (o que falta do registro; o parágrafo do retorno).
- **Apoio:** pos_rito\harness_textos_ensaio_v410.py:1831-1834.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

### Arquivo `pos_rito/leitura_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pos_rito\leitura_v410.py`. Fim de linha: LF. Itens: 170.

#### Item 170 — linha 814 — EP-01

- **Local:** linha 814 (a descricao do elo do registro a_escala_v410)
- **Origem:** g1:52 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
os nomes novos e os campos novos da pedra ditos RATIFICADOS em 10/11 (D101) e os dois auxiliares da autoria ditos [DECLARADO pela autoria],
~~~~

Trecho novo:

~~~~text
os nomes novos ratificados e os campos novos da pedra ditos RATIFICADOS em 10/11 (D101), o quarto teorema da clausula dito NOMEADO pelo operador (D108) e os dois auxiliares da autoria ditos [DECLARADO pela autoria],
~~~~

- **Justificativa:** A descrição do elo dizia todos os nomes novos ditos ratificados.
- **Apoio:** itens do registro
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

### Arquivo `pos_rito/registrar_mapa_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pos_rito\registrar_mapa_v410.py`. Fim de linha: CRLF. Itens: 171, 172, 173.

#### Item 171 — linha 259 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 259 (o texto que vai ao Mapa de Rotas)
- **Origem:** critico (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
(so' os %d auxiliares da autoria seguem [DECLARADO pela autoria]; os %d anteriores foram ratificados na D87)
~~~~

Trecho novo:

~~~~text
(o quarto teorema da clausula do Tetelestai foi NOMEADO pelo operador, D108: %s; so' os %d auxiliares da autoria seguem [DECLARADO pela autoria]; os %d anteriores foram ratificados na D87)
~~~~

- **Justificativa:** Com o delta novo a frase renderia 21 ratificados e 2 pendentes e calaria o quarto teorema (21 + 2 não fecha 24).
- **Apoio:** conferência do g1 (faltou: registrar_mapa_v410.py l.259)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - aplicar junto com o item seguinte (o argumento do formato)

#### Item 172 — linha 259 — EP-08

- **Local:** texto do registro no Mapa de Rotas (l.259)
- **Origem:** g2:43 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o fundo de n bits pesa 1/2^n em n oitavas)
~~~~

Trecho novo:

~~~~text
em n oitavas um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura de n bits)
~~~~

- **Justificativa:** O arquivo não estava na lista de fontes; repete a frase velha no texto que irá ao Mapa de Rotas depois do rito.
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - achado por Grep (“fundo de n bits”) fora da lista de fontes da ordem

#### Item 173 — linha 262 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 262 (o argumento novo do formato)
- **Origem:** critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
FA["estatuto_novos"], len(DL_.NOMES_PENDENTES_AESCALA), 
~~~~

Trecho novo:

~~~~text
FA["estatuto_novos"], ", ".join(DL_.NOMES_NOMEADOS_D108_AESCALA), len(DL_.NOMES_PENDENTES_AESCALA), 
~~~~

- **Justificativa:** O %s novo do item anterior.
- **Apoio:** conferência do g1 (faltou)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

### Arquivo `pos_rito/textos_custodia_handoff_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pos_rito\textos_custodia_handoff_v410.py`. Fim de linha: CRLF. Itens: 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192.

#### Item 174 — linha 116 — OBS-16, OBS-17

- **Local:** linha 116 (a constante D81_PT e o comentario do portao)
- **Origem:** g5:27 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
D81_PT = DL.FRASE_D81_PT   # D81: P = nP de Turing (a maquina com o leitor), na forma obrigatoria; a forma EN (DL.FRASE_D81_EN) reprova no portao do G1 (a frase e' partida em «;» e o fragmento com PROVED fica sem o estatuto): so' a PT entra nestes textos
~~~~

Trecho novo:

~~~~text
D81_PT, D81_EN = DL.FRASE_D81_PT, DL.FRASE_D81_EN   # D81: P = nP de Turing (a maquina com o leitor), na forma obrigatoria, PT e EN. A forma EN antiga punha o estatuto DEPOIS dos dois-pontos e reprovava no portao do G1 (o portao parte a frase ali, e o pedaco com a palavra da prova ficava sem o estatuto). A forma EN vigente do delta traz o estatuto colado a palavra da prova, no mesmo pedaco; quem decide e' o portao, mais abaixo (o README passa por guardas_dos_textos)
UMH_PT = "Com a escala no tipo o leitor do fundo tem UM só habitante; o conteúdo está na definição do operador, não no teorema; “existe” quer dizer que a lei tem solução e que ela decide"   # a frase do habitante unico (a do registro a_escala_v410 e do artigo PT), para ir ao lado da forma canonica do Clay
UMH_EN = "With the scale in the type the background reader has ONE inhabitant only; the content is in the operator's definition, not in the theorem; “exists” means that the law has a solution and that it decides"   # (a do artigo EN)
~~~~

- **Justificativa:** O que acontece com a forma EN no portao: o comentario descreve a forma EN ANTIGA. A FRASE_D81_EN de hoje foi reescrita e, numa replica das regras 1 a 3 do portao, PASSA; a antiga reprova na mesma replica. A saida que nao fere o portao e' usar a constante vigente do delta, sem mudar uma letra dela, e deixar o proprio portao decidir na execucao. As duas constantes novas trazem a frase do habitante unico, que ja' existe.
- **Apoio:** replica do portao (portao_replica.py, nesta pasta, copiada de tools\custodia_g1\textos.py:73-87): FRASE_D81_EN vigente PASSA; a forma antiga (delta_v410.py.bak_20261109_164644_antes_textos_d80_d82) reprova com “proved sem estatuto na mesma frase”; delta_v410.py:712 (a forma vigente); pedra\AEscala.lean:785-787 (o_leitor_do_fundo_e_a_iald: L = iald) e :871-872 (o_leitor_e_a_escala: L = L'); a frase ja' existe em registros_aescala_v410.py:82 (UM_HABITANTE), pos_rito\textos_v410.py:1397 e nos artigos (artigo_pt_aescala_v410.pysnip:37; artigo_en_aescala_v410.pysnip:37)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - as tres linhas ficam DENTRO do trecho que pos_rito\teste_textos_custodia_sem_candidato_v410.py:15 executa (de “REV_EN = ” ate' “3. as guardas”): o teste as enxerga
  - a replica cobre so' as regras 1 a 3 do portao; o portao de verdade e a guarda de frases rodam em guardas_dos_textos (linha 237) e no teste sem candidato: o construtor confere la'
  - se o portao de verdade recusar a forma EN: a saida de reserva e' por ALC_EN (linhas 102-103 do mesmo arquivo, que ja' passa no ENTROU_EN) no lugar de D81_EN no item seguinte, sem tocar a FRASE_D81_EN

#### Item 175 — linha 121 — PAR-01

- **Local:** linha 121: PODER_PT e PODER_EN passam a ser a frase do poder COM o retorno (alcança H0DN_EN :142, ABERTOS_EN :175, ARCO_EN :181, ARCO_PT :186 e README_EVIDENTE :197)
- **Origem:** g4:29 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
PODER_PT, PODER_EN = DL.FRASE_H0DN_PODER_PT, DL.FRASE_H0DN_PODER_EN
~~~~

Trecho novo:

~~~~text
PODER_PT, PODER_EN = DL.FRASE_H0DN_PODER_COM_RETORNO_PT, DL.FRASE_H0DN_PODER_COM_RETORNO_EN
~~~~

- **Justificativa:** Uma troca só leva o retorno aos cinco textos da custódia e do handoff que repetem a frase do poder, PT e EN, com o mesmo texto do artigo.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o COMMIT (linha 191) não usa PODER_PT: traz só “so sera aberto com o poder ... certificado (D96)”, que segue verdadeiro; não mexi
  - H0DN_EN (linha 142) e o post seguem dizendo “com a covariância física fechada” no condicional; o retorno vem logo depois
  - os textos EN passam pelo portão do G1 e pelos testes teste_textos_custodia_sem_candidato_v410.py: rodar de novo (não rodei nada da pasta)

#### Item 176 — linha 123 — PAR-08

- **Local:** pos_rito\textos_custodia_handoff_v410.py:123 (TEMPO_EN_C); ensaio_a_seco_v410.py:3145 (as frases exigidas na secao EN); guarda_frases_v410.py:105 e :208 (as frases limpas do teste da guarda)
- **Origem:** g5:13 (g5_forma_e_render). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_EN_COSTURADA
~~~~

Trecho novo:

~~~~text
DL.ROTULO_TEMPO_EN + " " + DL.FRASE_TEMPO_EN_COSTURADA
~~~~

- **Justificativa:** A costura EN do tempo (o rotulo e a frase com a primeira letra em maiuscula) passa a usar o rotulo EN; a frase do tempo (D94), ratificada, nao muda uma letra.
- **Apoio:** delta_v410.py:744 (FRASE_TEMPO_EN) e a constante nova do item anterior
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - pos_rito\_r2ag_12_pos_rito_textos_v410.py tem a mesma expressao: e' copia de trabalho antiga (prefixo _r2ag), fora da cadeia
  - a costura PT (DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) nao muda em arquivo nenhum

#### Item 177 — linha 124 — D108, OBS-1

- **Local:** constantes FIN_PT e FIN_EN, logo depois de CLZ_PT, CLZ_EN [o trecho atual comeca na linha 124 do arquivo, contada por script]
- **Origem:** g6:14 (g6_a_finura_e_o_observador). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
CLZ_PT, CLZ_EN = DL.CLAUSULA_Z_PT, DL.CLAUSULA_Z_EN   # (R2, D99; ADENDO 4) a clausula do limite do teorema do Tetelestai, lida do delta (que a le do ADENDO 4)
~~~~

Trecho novo:

~~~~text
CLZ_PT, CLZ_EN = DL.CLAUSULA_Z_PT, DL.CLAUSULA_Z_EN   # (R2, D99; ADENDO 4) a clausula do limite do teorema do Tetelestai, lida do delta (que a le do ADENDO 4)
FIN_PT, FIN_EN = DL.FRASE_FINURA_PT, DL.FRASE_FINURA_EN   # (D108) a finura da leitura: a frase de limite nova, as duas metades ([REAL] o que os enunciados dizem; [ONTO] a fala do operador de 10/11 e os espelhos), lida do delta
assert "%" not in FIN_PT + FIN_EN, "a frase da finura traz o sinal de porcentagem (o formato dos textos quebraria)"
~~~~

- **Justificativa:** O handoff le a frase do delta, como le a clausula do limite; nada e' digitado.
- **Apoio:** pos_rito\textos_custodia_handoff_v410.py:124-126 (o padrao das frases lidas do delta e do assert do “%”).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 178 — linha 127 — EP-10

- **Local:** TET_PT, l.127
- **Origem:** g3:23 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
". [INPUT/dicionário] " + DL.FRASE_E36_PT
~~~~

Trecho novo:

~~~~text
". [REAL o limiar de um pixel; INPUT/dicionário a leitura do operador] " + DL.FRASE_E36_PT
~~~~

- **Justificativa:** O rótulo duplo do registro na frase da E36.
- **Apoio:** registros_aescala_v410.py:115 e :127 e gerar_candidato_v410.py:435 (o rotulo duplo ja' em uso); pedra/AEscala.lean:903-909 (os_passos_sao_o_ciclo_ate_o_tetelestai: o limiar de um pixel e' teorema)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - l.129: o assert de “%” em TET_PT/TET_EN segue valendo (o rotulo novo nao traz “%”)

#### Item 179 — linha 128 — EP-10

- **Local:** TET_EN, l.128
- **Origem:** g3:24 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
". [INPUT/dictionary] " + DL.FRASE_E36_EN
~~~~

Trecho novo:

~~~~text
". [REAL the one-pixel threshold; INPUT/dictionary the operator's reading] " + DL.FRASE_E36_EN
~~~~

- **Justificativa:** Par do item PT, na grafia que o handoff EN já usa (“INPUT/dictionary”).
- **Apoio:** registros_aescala_v410.py:115 e :127 e gerar_candidato_v410.py:435 (o rotulo duplo ja' em uso); pedra/AEscala.lean:903-909 (os_passos_sao_o_ciclo_ate_o_tetelestai: o limiar de um pixel e' teorema)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 180 — linha 130 — EP-05

- **Local:** ESCALA_TIPO_PT, l.130
- **Origem:** g3:25 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
é único e é a IALD, o leitor é a escala, o decisor sem escala não é leitor do fundo (ele não mente: não lê)
~~~~

Trecho novo:

~~~~text
é único e é a IALD, dois leitores do fundo quaisquer são o mesmo e, em todo leitor do fundo, o pixel de custo k brilha e^(−s·k) no tempo s (`o_leitor_e_a_escala`), o decisor sem escala não é leitor do fundo (ele não mente: não lê)
~~~~

- **Justificativa:** A frase do operador fica só como nome; vai o conteúdo do enunciado. (A frase UM_HABITANTE não entra aqui: a D106, item 3, a manda para a linha do .md e para o post; ver dúvidas.)
- **Apoio:** pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - ESCALA_TIPO_PT entra no README_EVIDENTE (l.196) e ESCALA_TIPO_EN em ESCALA_EN (l.136): acompanham sozinhos; os textos do handoff passam de novo pela guarda de frases e pelo portao do G1 no pos-rito
  - o trecho vizinho “o limiar do Tetelestai (…)” e' de outro grupo

#### Item 181 — linha 130 — EP-03

- **Local:** ESCALA_TIPO_PT (l.130)
- **Origem:** g2:16 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o limiar do Tetelestai (com n bits, passado o tempo de n oitavas
~~~~

Trecho novo:

~~~~text
o limiar de um pixel, a decisão exata (`os_passos_sao_o_ciclo_ate_o_tetelestai`: com n bits, passado o tempo de n oitavas
~~~~

- **Justificativa:** Pela E36 (ordem do operador, D100) a cláusula do Tetelestai é a de 1 − β; o limiar de n oitavas é a decisão exata, formalização da gerência. O rótulo acompanha; o nome do teorema, ratificado, não muda. Entra o nome do teorema, que aqui faltava.
- **Apoio:** pedra\AEscala.lean:897-898 (docstring: “o limiar de um pixel … é a DECISÃO exata, formalização da gerência; a CLÁUSULA DO TETELESTAI … é a `o_tetelestai_e_um_menos_beta`”); delta_v410.py:1092-1093 (E36); pedra\AEscala.lean:903-909 (o enunciado só traz desigualdades sobre Z(s))
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - textos_custodia_handoff_v410.py:201-222 (guardas_dos_textos): o trecho novo não traz aspa simples, “<”, barra invertida nem quebra de linha (regra do ARCO); “linear nos bits” continua com a cláusula ao lado
  - PREPARACAO_v410_PRONTA.json (readme_evidente) é regenerado

#### Item 182 — linha 130 — EP-05

- **Local:** ESCALA_TIPO_PT, l.130 (fim da lista)
- **Origem:** g3:26 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
 e a mentira lida como mentira é verdade. " + CLZ_PT
~~~~

Trecho novo:

~~~~text
 e, para todo leitor do fundo, o limite da leitura com o tempo é o número de soluções dividido pelo número de pixels e vale 0 sem solução (`a_mentira_lida_como_mentira_e_verdade`); a leitura que os nomes `o_leitor_e_a_escala` e `a_mentira_lida_como_mentira_e_verdade` carregam (que não exista leitor que não seja o observador da luz; que nada escape do Nome) é do operador [ONTO]. " + CLZ_PT
~~~~

- **Justificativa:** O mesmo texto da linha do .md: conteúdo do termo, frase como nome, leitura marcada [ONTO].
- **Apoio:** pedra/AEscala.lean:978-980 (a_mentira_lida_como_mentira_e_verdade: L.limite c = oQueSou (nomeDasSolucoes c) e, sem solucao, L.limite c = 0 e oQueSou = 0); o que sou do Nome das solucoes = numero de solucoes / numero de pixels (|X|): TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):805-807 (o_que_sou_das_solucoes, v409); docstring l.976-977 ([ONTO])
- **Decisão do crítico:** fico com a correção do cético: “a leitura que os nomes carregam é do operador [ONTO]” não dizia QUAL leitura e punha [ONTO] em “o leitor é a escala”, que o registro dá como DEFINIÇÃO [INPUT]; as leituras [ONTO] são as das docstrings (l.870, l.976-977 e l.992) e do limite do registro (l.124), ditas com as mesmas palavras em todo lugar

#### Item 183 — linha 131 — EP-05

- **Local:** ESCALA_TIPO_EN, l.131
- **Origem:** g3:27 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
is unique and is the IALD, the reader is the scale, the decider without a scale is not a background reader (it does not lie: it does not read)
~~~~

Trecho novo:

~~~~text
is unique and is the IALD, any two background readers are the same and, in every background reader, the pixel of cost k has brightness e^(−s·k) at time s (`o_leitor_e_a_escala`), the decider without a scale is not a background reader (it does not lie: it does not read)
~~~~

- **Justificativa:** Par do item PT.
- **Apoio:** pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 184 — linha 131 — EP-03

- **Local:** ESCALA_TIPO_EN (l.131)
- **Origem:** g2:17 (g2_tetelestai_e_limiar). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
the threshold of the Tetelestai (with n bits, past the time of n octaves
~~~~

Trecho novo:

~~~~text
the one-pixel threshold, the exact decision (`os_passos_sao_o_ciclo_ate_o_tetelestai`: with n bits, past the time of n octaves
~~~~

- **Justificativa:** Par EN do item 16.
- **Apoio:** pedra\AEscala.lean:897-898 (docstring: “o limiar de um pixel … é a DECISÃO exata, formalização da gerência; a CLÁUSULA DO TETELESTAI … é a `o_tetelestai_e_um_menos_beta`”); delta_v410.py:1092-1093 (E36); pedra\AEscala.lean:903-909 (o enunciado só traz desigualdades sobre Z(s))
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - os mesmos do item 16

#### Item 185 — linha 131 — EP-05

- **Local:** ESCALA_TIPO_EN, l.131 (end of the list)
- **Origem:** g3:28 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
 and a lie read as a lie is truth. " + CLZ_EN
~~~~

Trecho novo:

~~~~text
 and, for every background reader, the limit of the reading in time is the number of solutions divided by the number of pixels and is 0 when there is no solution (`a_mentira_lida_como_mentira_e_verdade`); the reading that the names `o_leitor_e_a_escala` and `a_mentira_lida_como_mentira_e_verdade` carry (that there is no reader that is not the observer of the light; that nothing escapes the Name) is the operator's [ONTO]. " + CLZ_EN
~~~~

- **Justificativa:** Par do item PT.
- **Apoio:** pedra/AEscala.lean:978-980 (a_mentira_lida_como_mentira_e_verdade: L.limite c = oQueSou (nomeDasSolucoes c) e, sem solucao, L.limite c = 0 e oQueSou = 0); o que sou do Nome das solucoes = numero de solucoes / numero de pixels (|X|): TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):805-807 (o_que_sou_das_solucoes, v409); docstring l.976-977 ([ONTO])
- **Decisão do crítico:** fico com a correção do cético: “a leitura que os nomes carregam é do operador [ONTO]” não dizia QUAL leitura e punha [ONTO] em “o leitor é a escala”, que o registro dá como DEFINIÇÃO [INPUT]; as leituras [ONTO] são as das docstrings (l.870, l.976-977 e l.992) e do limite do registro (l.124), ditas com as mesmas palavras em todo lugar (par EN)

#### Item 186 — linha 136 — PAR-03

- **Local:** ESCALA_EN, l.136
- **Origem:** g3:29 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
sustains and does not exhaust; the vibrato sustains the note; there is no infinity in finite time
~~~~

Trecho novo:

~~~~text
sustains and does not exhaust; given a zero-cost pixel, the decay generated by the cost, e^(−t·c(x)), does not touch what has zero cost and does not bring the uniform state to zero, and the performed reading (the average, over the pixels, of the weights e^(−s·c(x))) never falls below the fraction of zero-cost pixels, does not increase with time and tends to it (`o_vibrato_sustenta_a_nota`); on the paired space of the kernel, J² = 1 and JKJ = −K (`a_nota_e_a_conjugacao_modular`); the identification of that decay with the vibrato and of the note with J is the operator's [ONTO]; there is no infinity in finite time
~~~~

- **Justificativa:** Sob “The kernel proves” o handoff dizia a frase; passa a dizer o que os dois termos provam e marca [ONTO] a leitura. É o par EN do texto da linha do .md e do post.
- **Apoio:** pedra/AEscala.lean:244-250 (o_vibrato_sustenta_a_nota, hipotese h: existe x com c x = 0: (1) a trava nao toca o custo zero; (2) trava c t (uniforme X) != 0; (3) card{c = 0}/|X| <= leituraPerformada c s; (4) Antitone; (5) Tendsto para card{c = 0}/|X|); leituraPerformada = particao/|X|: TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):920; trava = e^(-t c(x)) por pixel: TraducaoTuring.lean:472-477 (mesma copia); docstring l.242-243 ([ONTO]) | pedra/AEscala.lean:257-258 (a_nota_e_a_conjugacao_modular: conjJ (conjJ p) = p e conjJ (pairK d (conjJ p)) = -pairK d p, isto e', J^2 = 1 e JKJ = -K); docstring l.256 (a identificacao nota = J e' do operador, ONTO)
- **Decisão do crítico:** fico com a correção do cético: “disso” vinha logo depois de J² = 1 e JKJ = −K e a leitura mais próxima atribuía o vibrato às identidades de J; a docstring (AEscala.lean:242-243) liga o vibrato ao decaimento: “desse decaimento” (par EN)
- **Efeitos colaterais:**
  - o handoff nao tem texto PT com o vibrato (Grep: “vibrato” so' na l.136)

#### Item 187 — linha 137 — EP-10

- **Local:** CLAY_TXT_EN, l.137
- **Origem:** g3:30 (g3_leituras_onto). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
" In the reading of the operator (D83): " + D83_EN
~~~~

Trecho novo:

~~~~text
" In the reading of the operator (D83) [REAL the validity in the kernel; INPUT the operator's reading]: " + D83_EN
~~~~

- **Justificativa:** O mesmo rótulo da forma da D83 que o artigo EN passa a levar.
- **Apoio:** pedra/AEscala.lean:598-604 (a forma da D83 e' a leitura do operador, fala 6; validade no kernel; a creditacao e' do Clay) e :778-779 (a_pergunta_do_clay_tem_resposta: a validade)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - l.193 (README_EVIDENTE, “A forma da D83: ”) ja' vem sob “[REAL] a validade no kernel; [INPUT] a definição da pergunta no dicionário, que é do operador”: sem mudanca

#### Item 188 — linha 155 — PAR-08

- **Local:** linhas 155 (ENTROU_EN), 164 (KERNEL_LEITURA_EN) e 182 (ARCO_EN, duas vezes): as QUATRO ocorrencias da palavra no arquivo
- **Origem:** g5:10 (g5_forma_e_render). **Língua:** EN. **Ocorrências:** 4

Trecho atual:

~~~~text
accreditation
~~~~

Trecho novo:

~~~~text
creditation
~~~~

- **Justificativa:** As formas ratificadas e o artigo EN escrevem “creditation” (kernel validity, not creditation; the creditation is Clay's); a custodia EN escrevia “accreditation” nas frases de fecho. Uma palavra so'.
- **Apoio:** delta_v410.py:443 (FRASE_PROVADO_EN), :704-707 (o qualificador e a D64 EN), :712 (FRASE_D81_EN), :744 (FRASE_TEMPO_EN); artigo_en_aescala_v410.pysnip:48
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o portao do G1 aceita as duas palavras (tools\custodia_g1\textos.py:83) e nenhuma das quatro frases tem a palavra da prova: nao muda o resultado do portao
  - nenhum teste procura “accreditation” (Grep em pos_rito\teste_textos_custodia_sem_candidato_v410.py e harness_textos_ensaio_v410.py: 0)
  - FORA da pasta do trabalho e fora deste conserto: o README pinado e o portao do G1 usam “accreditation” na formula “CONFIRMED is accreditation, the one refused word” (tools\custodia_g1\readme_pinado.py:127-174; textos.py:22). Ver duvidas

#### Item 189 — linha 181 — PAR-06

- **Local:** linha 181, ARCO_EN: a frase da parede na mesma posição do ARCO_PT (linha 186)
- **Origem:** g4:30 (g4_h0dn). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
"The H0DN × BG1 test of the Hubble ratio enters the registry h0dn_bg1_v410: " + OBR_EN + ". " + PODER_EN + ". The documentary receipt HMS/13: "
~~~~

Trecho novo:

~~~~text
"The H0DN × BG1 test of the Hubble ratio enters the registry h0dn_bg1_v410: " + OBR_EN + ". " + PAREDE_EN.replace("'", "’") + ". " + PODER_EN + ". The documentary receipt HMS/13: "
~~~~

- **Justificativa:** O ARCO_PT traz a forma, a parede e o poder; o ARCO_EN pulava a parede. Com ela, a forma deixa de estar sozinha no ARCO_EN (observação 15).
- **Apoio:** pos_rito\textos_custodia_handoff_v410.py:186 (ARCO_PT) e :120 (PAREDE_EN = DL.FRASE_H0DN_PAREDE_EN).
- **Decisão do crítico:** fico com a correção do cético: PAREDE_EN começa por “Kimi's partial delivery” (apóstrofo ASCII) e a guarda de forma do ARCO reprova aspa simples (o ARCO vai em HTML e em JS); a constante não muda: o apóstrofo tipográfico entra só nesta posição
- **Efeitos colaterais:**
  - o ARCO_EN cresce (a parede EN tem 449 caracteres e o retorno 590): se o ARCO tiver teto de tamanho em algum destino, conferir

#### Item 190 — linha 193 — OBS-16, OBS-17

- **Local:** linha 193 (README_EVIDENTE, item (1))
- **Origem:** g5:28 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a creditação é do Clay. PT: " + CLAY_PT + " EN: " + CLAY_EN + " A forma da D83: " + D83_PT
~~~~

Trecho novo:

~~~~text
a creditação é do Clay. PT: " + CLAY_PT + " P = nP de Turing, na forma da D81: " + D81_PT + ". " + UMH_PT + ". EN: " + CLAY_EN + " P = nP of Turing, in the form of D81: " + D81_EN + ". " + UMH_EN + ". A forma da D83: " + D83_PT
~~~~

- **Justificativa:** A forma canonica do Clay (D84) NAO muda. Passa a vir, em cada lingua, seguida das duas frases que ja' existem: a do alcance (a maquina de Turing padrao sem o leitor fica fora por estatuto) e a do habitante unico (o conteudo esta' na definicao do operador, nao no teorema). O leitor de lingua inglesa deixa de receber a forma sem a D81.
- **Apoio:** PREPARACAO_v410_PRONTA.json, chave readme_evidente (a forma canonica PT e EN, iguais as de DL.FRASE_CLAY_CANONICA_*); delta_v410.py:711-712 (D81 PT e EN); pedra\AEscala.lean:785-787 (o_leitor_do_fundo_e_a_iald: L = iald) e :871-872 (o_leitor_e_a_escala: L = L'); a frase ja' existe em registros_aescala_v410.py:82 (UM_HABITANTE), pos_rito\textos_v410.py:1397 e nos artigos (artigo_pt_aescala_v410.pysnip:37; artigo_en_aescala_v410.pysnip:37); o item (1) novo inteiro passa na replica do portao (casos_readme.json, nesta pasta)
- **Decisão do crítico:** fico com a correção do cético: (1) “a forma canônica vem sempre com …” era desmentido no mesmo handoff (ARCO, post); (2) o rótulo “O alcance (D81)” colidia com o vocabulário da casa (o alcance é a D64): fica o rótulo que a linha 194 já usava. A forma canônica do Clay (D84) e a forma da D81 não mudam uma letra
- **Efeitos colaterais:**
  - o item seguinte tira a D81 PT do lugar antigo (senao ela apareceria duas vezes)
  - pos_rito\teste_textos_custodia_sem_candidato_v410.py:61 exige DL.FRASE_D81_PT no README: segue verdadeiro; convem acrescentar ali “and DL.FRASE_D81_EN in R and G["UMH_PT"] in R and G["UMH_EN"] in R” para a regra ficar guardada
  - o handoff cresce: o assert de crescimento (linha 250) so' pede mais de 3000 bytes

#### Item 191 — linha 194 — OBS-16, OBS-17

- **Local:** linha 194 (README_EVIDENTE, a frase da D81 no lugar antigo)
- **Origem:** g5:29 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"P = nP de Turing, na forma da D81: " + D81_PT + ". Os termos do kernel: de 
~~~~

Trecho novo:

~~~~text
"Os termos do kernel: de 
~~~~

- **Justificativa:** A D81 PT foi para junto da forma canonica (item anterior); aqui ela sairia repetida.
- **Apoio:** o item anterior
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - aplicar SO' junto com o item anterior

#### Item 192 — linha 194 — D108, OBS-1

- **Local:** README_EVIDENTE, item (1) (a pergunta do Clay, na forma canonica), no fim, depois da lista dos termos do kernel [o trecho atual comeca na linha 194 do arquivo, contada por script]
- **Origem:** g6:15 (g6_a_finura_e_o_observador). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
`existe_o_algoritmo_e_e_a_iald` e `a_escala`. "
~~~~

Trecho novo:

~~~~text
`existe_o_algoritmo_e_e_a_iald` e `a_escala`. O limite do que a decisão compara (D108). PT: " + FIN_PT + ". EN: " + FIN_EN + ". "
~~~~

- **Justificativa:** A frase de limite nova vai no item do README que traz a forma canonica do Clay, em PT e EN como a propria forma canonica; a forma canonica e a forma da D81 nao mudam.
- **Apoio:** pedra\AEscala.lean (sha256 7d1557f96178367949bbffe42b2e8af4094c9ec7c0373bdbdaaa3a7d7de5ad60, igual ao instalado em C:\t\k410c\final\TGLExt\AEscala.lean): def LeitorDoFundo.leitura 669-670 (a media dos brilhos, |X|^-1 . soma); a_leitura_e_a_do_psion 702-703; os_passos_sao_o_ciclo_ate_o_tetelestai 903-909, item (v) na linha 909 ((∃ x, c x = 0) ↔ (card)⁻¹ ≤ (L.leitura c s).re, sob n·ln 2 < s); o_tetelestai_e_um_menos_beta 1066-1071, item (iii) nas linhas 1070-1071 ((1 − b)·(L.leitura c s).re ≤ #solucoes/card, sob h, 0 < b < 1, 0 ≤ s e o limiar); campo sem_escala_nao_ha_medida 663 (∀ k, brilho k 0 = 1); o_pai_da_mentira_so_nao_reconhece 993-998; o_leitor_e_a_escala 871-872; a_escala_e_meio_por_oitava 832-838; em_n_oitavas_o_fundo_pesa_um_pixel 859-860. C:\t\k410c\final\TGLExt\TraducaoTuring.lean: bits_sao_oitavas 212 (card (Fin n → Bool) = 2^n); o_psion_le_os_pixels 749-750 (Z(s)/|X|); particao 666. C:\t\k410c\final\TGLExt\ObservadorTerminal.lean (sha16 162eeeb8c16cea81, igual ao do Nós): Terminal 102; terminal_iff 108; the_terminal_is_unique 132; every_level_reaches_the_terminal 157; distancia 161-165; the_collapse_is_the_terminal_point_of_resistance 180; os niveis sao rotulos (docstring 80-81); Level em TheCascadeOfObservers.lean 71-75. Ausencias conferidas por grep: AEscala.lean nao cita ObservadorTerminal (0) e ObservadorTerminal.lean nao cita AEscala nem LeitorDoFundo (0); “onda” 0 e 0; “frequ” 0 e 0; “Einstein” 0 e 0; “relatividade” so' na linha 69 da AEscala, dentro de uma fala citada no cabecalho, em nenhum enunciado. A fala: C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt, sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4 (lido por script), 266 bytes, segunda linha inteira
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - guardas_dos_textos (linhas 201-227): o README passa pela guarda de frases e pelo portao do G1; a frase nao tem hash, nao tem “proved/provada”, nao cita o ACOM Mirror, nao tem 4,44 nem os nomes da D59; conferido em isolamento com copia das regras.
  - O README ja' traz ESCALA_TIPO_PT no item (2), com a CLAUSULA_Z e a clausula do Tetelestai: o controle da linha 212-215 continua satisfeito.
  - pos_rito\CUSTODIA_v410_RASCUNHO.txt, HARNESS_TEXTOS_ENSAIO_v410.json e os testes sem candidato (teste_textos_custodia_sem_candidato_v410.py) guardam o README antigo: regerar.
  - gerar_relatorio_v410.py:422-427 (o readme_evidente da PREPARACAO, chave 1_clay_forma_canonica) leva clausula_do_limite_pt e clausula_do_limite_en e NAO leva a frase nova: a ordem nao o listou; se a gerencia quiser paridade, acrescentar ali "finura_da_leitura_pt": _DL.FRASE_FINURA_PT e "finura_da_leitura_en": _DL.FRASE_FINURA_EN.
  - Os sete textos do handoff (ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO, COMMIT) e a linha do .md canonico (gerar_candidato_v410.py:434-435) tambem trazem a clausula do limite e NAO recebem a frase nova: a ordem limitou o lugar a tres superficies.
  - (crítico) o README evidente da preparação (gerar_relatorio_v410.py) ganha as chaves finura_da_leitura_pt/en no item do crítico da linha 427: os dois README evidentes dizem a mesma coisa

### Arquivo `pos_rito/textos_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pos_rito\textos_v410.py`. Fim de linha: LF. Itens: 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212.

#### Item 193 — linha 765 — PAR-01

- **Local:** linha 765, handoff: a frase do retorno no dicionário do handoff
- **Origem:** g4:36 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"parede_h0dn": DL_.FRASE_H0DN_PAREDE_PT, 
~~~~

Trecho novo:

~~~~text
"parede_h0dn": DL_.FRASE_H0DN_PAREDE_PT, "retorno_h0dn": DL_.FRASE_H0DN_RETORNO_PT, 
~~~~

- **Justificativa:** Aplicar junto com o item seguinte.
- **Apoio:** pos_rito\textos_v410.py:765.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 194 — linha 765 — EP-01 — redigido pelo crítico

- **Local:** linha 765 (o dicionário do handoff)
- **Origem:** g1:48, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"n_pend": len(DL_.NOMES_PENDENTES_AESCALA), 
~~~~

Trecho novo:

~~~~text
"nomeado_lista": ", ".join(DL_.NOMES_NOMEADOS_D108_AESCALA), "n_pend": len(DL_.NOMES_PENDENTES_AESCALA), 
~~~~

- **Justificativa:** A chave que o item do g1:48 usa no formato.
- **Apoio:** g1 item 48 (efeito)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 195 — linha 790 — EP-01, R3-MEDIO

- **Local:** linha 790 (Pendencias SO do operador) e a chave nova na linha 765
- **Origem:** g1:48 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
%(nomes_novos_lista)s; só a confirmação expressa dos %(n_pend)d nomes auxiliares da autoria
~~~~

Trecho novo:

~~~~text
%(nomes_novos_lista)s; o quarto teorema da cláusula do Tetelestai ele nomeou em 10/11 (D108): `%(nomeado_lista)s`; só a confirmação expressa dos %(n_pend)d nomes auxiliares da autoria
~~~~

- **Justificativa:** O parágrafo lista o que o operador já ratificou e o que ainda é dele; com a lista de 21, o quarto teorema ficaria sem dono. Ele o nomeou: não é pendência.
- **Apoio:** fala 29; delta (NOMES_NOMEADOS_D108_AESCALA)
- **Decisão do crítico:** o trecho fica; a chave nomeado_lista (linha 765), que o redator deixou em prosa, virou item exato do crítico
- **Efeitos colaterais:**
  - l.765: acrescentar ao dicionário "nomeado_lista": ", ".join(DL_.NOMES_NOMEADOS_D108_AESCALA); n_nomes_novos já é len(DL_.NOMES_RATIFICADOS_D101_AESCALA) e passa de 22 a 21 sozinho
  - o trecho “os %(n_nomes_novos)d nomes novos da `AEscala` (R3, R4 e R5) … ele ratificou em 10/11” fica verdadeiro com 21

#### Item 196 — linha 790 — PAR-01

- **Local:** linha 790, handoff, a lista [OPEN]: o estado do teste em 10/11
- **Origem:** g4:37 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a covariância física, o vetor observado e os IDs; %(parede_h0dn)s), a máquina de Turing padrão sem o leitor
~~~~

Trecho novo:

~~~~text
a covariância física, o vetor observado e os IDs; %(parede_h0dn)s; %(retorno_h0dn)s), a máquina de Turing padrão sem o leitor
~~~~

- **Justificativa:** O handoff é a memória que a próxima sessão lê: a lista do que está aberto passa a dizer que a ordem voltou com a recusa e qual é a ordem seguinte.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o registro ACOM da D98 previa “HANDOFF (README: estado do teste em 10/11)” (citado pelo cético do PAR-01): é este trecho

#### Item 197 — linha 915 — OBS-15

- **Local:** linha 915, _paragrafo_v410_de (o parágrafo curto do README/site): o alcance depois da forma
- **Origem:** g4:38 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
[REAL · DERIVED · DECLARADO · INPUT · OPEN]: %s. O teste da razão de Hubble local/fundo (nulo
~~~~

Trecho novo:

~~~~text
[REAL · DERIVED · DECLARADO · INPUT · OPEN]: %s (%s). O teste da razão de Hubble local/fundo (nulo
~~~~

- **Justificativa:** Neste item do parágrafo público a forma está sozinha: a parede não está nele. Aplicar junto com o item seguinte.
- **Apoio:** delta_v410.py:775 (FRASE_H0DN_PAREDE_PT: teste de suporte reprovado, [REAL] lido pela gerência; nenhum Z, razão ou solver foi rodado; o um.py não lê esse vetor); runtime_h0dn_v410.py:168 (c7: observed_vector_read False, MEDIDO pelos caminhos tocados); runtime_h0dn_v410.py:191 (c6: a função de veredito roda em vetores determinísticos sintéticos, por isso o qualificador “sobre dado observado”).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - verificar_paragrafo_v410 (linhas 927-970) roda de novo sobre o parágrafo; a frase do alcance não traz aspas angulares nem número do quadro

#### Item 198 — linha 915 — OBS-15

- **Local:** linha 915, _paragrafo_v410_de: o argumento novo do formato
- **Origem:** g4:39 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
% (DL_.FRASE_H0DN_OBRIGATORIA_PT, hv["n_pinos"], hd["mechanics"]["n_checks"], p1, p2, Ls, DL_.FRASE_PROVADO_PT, q_x),
~~~~

Trecho novo:

~~~~text
% (DL_.FRASE_H0DN_OBRIGATORIA_PT, DL_.FRASE_H0DN_ALCANCE_PT, hv["n_pinos"], hd["mechanics"]["n_checks"], p1, p2, Ls, DL_.FRASE_PROVADO_PT, q_x),
~~~~

- **Justificativa:** O %s novo do item anterior.
- **Apoio:** pos_rito\textos_v410.py:915.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 199 — linha 1030 — EP-13

- **Local:** _TEMA_ESPECIAL, 1a entrada (l.1030)
- **Origem:** g2:44 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"a cláusula do Tetelestai está no ACOM Mirror: o limiar de 1 − β, em que β é o operador modular do Tetelestai (D100)"
~~~~

Trecho novo:

~~~~text
"a fala do operador sobre a cláusula do Tetelestai no ACOM Mirror: 1 − β, com β como o operador modular do Tetelestai (leitura dele [dicionário]; D100)"
~~~~

- **Justificativa:** O tema afirmava, como fato da casa, que a cláusula está no ACOM Mirror como “o limiar de 1 − β”. Pela aferição da gerência (ADENDO 5) o runner traz o par (β, 1 − β), não um limiar de parada com esse nome; “limiar” é a formalização da gerência. O tema passa a dizer que é a fala e a leitura do operador.
- **Apoio:** DESENHO_v410_ADENDO_5_POS_CANDIDATO_10nov.md l.7 (“a cláusula está como o par (β, 1 − β), não como um limiar de parada com esse nome”; “Que esse par SEJA a cláusula do Tetelestai em computação é a leitura do operador [dicionário]”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o tema continua citando “ACOM Mirror”: os textos que listam as falas seguem sob a mesma regra de hoje ([PILOTO][SIM] e “nada ali valida física” no mesmo texto, textos_custodia_handoff_v410.py:216)
  - pos_rito\_r5ag_22_pos_rito_falas_v410.py guarda a redação velha como registro de época: não se toca

#### Item 200 — linha 1278 — D108, EP-01 — CONDICIONAL CONTAGEM_DE_FALAS; redigido pelo crítico

- **Local:** linha 1278 (par_: os sha16 das falas achados pelo nome)
- **Origem:** g1:12, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
("confirmo", "confirmo_tudo_nomeio_e_o_numero_corrige", DL_.N_CONFIRMO_TUDO))   # (R5, D100 e D101: a 27a e a 28a falas)
~~~~

Trecho novo:

~~~~text
("confirmo", "confirmo_tudo_nomeio_e_o_numero_corrige", DL_.N_CONFIRMO_TUDO), ("quarto_nome", "o_quarto_nome_ressurreicao_do_sinal", DL_.N_QUARTO_NOME))   # (R5, D100 e D101: a 27a e a 28a falas; R6, D108: a 29a)
~~~~

- **Justificativa:** O assert da linha 1280 exige um par para cada fala congelada.
- **Apoio:** g1 item 12 (efeito: o par da fala 29)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 201 — linha 1325 — PAR-01

- **Local:** linha 1325, _hd: o assert do registro lido pelo pós-rito
- **Origem:** g4:32 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
and (hd.get("ordem_kimi_02") or {}).get("sha256") == DL_.H0DN_ORDEM02["sha256"] and hd.get("ressalvas"), "o registro h0dn_bg1_v410 nao traz a ordem, o dossie, o que falta (com a frase do poder certificado), as ressalvas e a ORDEM 02 pinada"
~~~~

Trecho novo:

~~~~text
and (hd.get("ordem_kimi_02") or {}).get("sha256") == DL_.H0DN_ORDEM02["sha256"] and any(DL_.FRASE_H0DN_RETORNO_PT in x_ for x_ in (hd.get("o_que_falta") or [])) and any(DL_.FRASE_H0DN_RETORNO_PT in x_ for x_ in (hd.get("ressalvas") or [])) and (hd.get("ordem_kimi_03") or {}).get("sha256") == DL_.H0DN_ORDEM03["sha256"] and hd.get("ressalvas"), "o registro h0dn_bg1_v410 nao traz a ordem, o dossie, o que falta (com a frase do poder certificado e o retorno da ORDEM 02), as ressalvas e as ORDENS 02 e 03 pinadas"
~~~~

- **Justificativa:** O pós-rito recusa um core cujo registro não traga o retorno e o pino da ORDEM 03.
- **Apoio:** pos_rito\textos_v410.py:1325.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 202 — linha 1383 — PAR-03

- **Local:** insig, l.1383 (repetição; fora da lista da D106, item 2)
- **Origem:** g3:36 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o vibrato sustenta a nota, e a nota é a conjugação modular (`o_vibrato_sustenta_a_nota`, `a_nota_e_a_conjugacao_modular`); 
~~~~

Trecho novo:

~~~~text
havendo pixel de custo zero, o decaimento gerado pelo custo, e^(−t·c(x)), não toca o que tem custo zero e não leva a zero o estado uniforme, e a leitura performada (a média, sobre os pixels, dos pesos e^(−s·c(x))) nunca fica abaixo da fração de pixels de custo zero, não cresce com o tempo e tende a ela (`o_vibrato_sustenta_a_nota`); no espaço pareado do kernel, J² = 1 e JKJ = −K (`a_nota_e_a_conjugacao_modular`); a identificação desse decaimento com o vibrato e da nota com J é do operador [ONTO]; 
~~~~

- **Justificativa:** A seção pública “A Escala” do README repete a frase do achado sob “[REAL os termos · INPUT as falas]”. Mesmo texto da linha do .md. A D106 não lista este arquivo: a gerência decide se entra.
- **Apoio:** pedra/AEscala.lean:244-250 (o_vibrato_sustenta_a_nota, hipotese h: existe x com c x = 0: (1) a trava nao toca o custo zero; (2) trava c t (uniforme X) != 0; (3) card{c = 0}/|X| <= leituraPerformada c s; (4) Antitone; (5) Tendsto para card{c = 0}/|X|); leituraPerformada = particao/|X|: TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):920; trava = e^(-t c(x)) por pixel: TraducaoTuring.lean:472-477 (mesma copia); docstring l.242-243 ([ONTO]) | pedra/AEscala.lean:257-258 (a_nota_e_a_conjugacao_modular: conjJ (conjJ p) = p e conjJ (pairK d (conjJ p)) = -pairK d p, isto e', J^2 = 1 e JKJ = -K); docstring l.256 (a identificacao nota = J e' do operador, ONTO)
- **Decisão do crítico:** fico com a correção do cético: “disso” vinha logo depois de J² = 1 e JKJ = −K e a leitura mais próxima atribuía o vibrato às identidades de J; a docstring (AEscala.lean:242-243) liga o vibrato ao decaimento: “desse decaimento”; entra, embora fora da lista da D106: é a seção pública do README e repete a frase do achado
- **Efeitos colaterais:**
  - a string e' formatada com “%”: o trecho novo nao traz “%”; a secao passa por _sem_chaves (o trecho novo nao traz chaves)
  - l.448 e a moldura (ea[moldura_pt]) repetem a forma curta “o vibrato sustenta a nota”: nao redigidas (ver duvidas)

#### Item 203 — linha 1395 — EP-05

- **Local:** tipo, l.1395 (repetição; a D106, item 1, não lista este arquivo)
- **Origem:** g3:37 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o leitor é a escala, dois leitores do fundo quaisquer são o mesmo (`o_leitor_e_a_escala`);
~~~~

Trecho novo:

~~~~text
dois leitores do fundo quaisquer são o mesmo e, em todo leitor do fundo, o pixel de custo k brilha e^(−s·k) no tempo s (`o_leitor_e_a_escala`);
~~~~

- **Justificativa:** O mesmo conserto do artigo PT, na seção pública do README.
- **Apoio:** pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** entra, embora fora da lista da D106 (a seção pública do README repete a frase; o cético deu ok)

#### Item 204 — linha 1395 — EP-08

- **Local:** bloco da escala no tipo (l.1395)
- **Origem:** g2:39 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
metade por oitava e, em n oitavas, o fundo pesa um pixel; "
~~~~

Trecho novo:

~~~~text
metade por oitava e, em n oitavas, um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura (`em_n_oitavas_o_fundo_pesa_um_pixel`; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, vem do teorema do limiar, a seguir); "
~~~~

- **Justificativa:** O enunciado fala do brilho de UM pixel de custo 1 em n oitavas (1/|X| = 1/2^n), que é o peso de um pixel na leitura; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, é o item (ii) do teorema do limiar.
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - string de formato com %s: o trecho novo não traz “%”

#### Item 205 — linha 1396 — EP-03

- **Local:** bloco da escala no tipo (l.1396)
- **Origem:** g2:15 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o limiar do Tetelestai (`os_passos_sao_o_ciclo_ate_o_tetelestai`): com n bits
~~~~

Trecho novo:

~~~~text
o limiar de um pixel, a decisão exata (`os_passos_sao_o_ciclo_ate_o_tetelestai`): com n bits
~~~~

- **Justificativa:** Pela E36 (ordem do operador, D100) a cláusula do Tetelestai é a de 1 − β; o limiar de n oitavas é a decisão exata, formalização da gerência. O rótulo acompanha; o nome do teorema, ratificado, não muda.
- **Apoio:** pedra\AEscala.lean:897-898 (docstring: “o limiar de um pixel … é a DECISÃO exata, formalização da gerência; a CLÁUSULA DO TETELESTAI … é a `o_tetelestai_e_um_menos_beta`”); delta_v410.py:1092-1093 (E36); pedra\AEscala.lean:903-909 (o enunciado só traz desigualdades sobre Z(s))
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a linha é string de formato com %s: o trecho novo não traz “%”

#### Item 206 — linha 1396 — EP-05

- **Local:** tipo, l.1396 (repetição; a D106, item 1, não lista este arquivo)
- **Origem:** g3:38 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a mentira lida como mentira é verdade (`a_mentira_lida_como_mentira_e_verdade`); o Pai da Mentira só não reconhece (`o_pai_da_mentira_so_nao_reconhece`). "
~~~~

Trecho novo:

~~~~text
para todo leitor do fundo, o limite da leitura com o tempo é o número de soluções dividido pelo número de pixels e vale 0 sem solução (`a_mentira_lida_como_mentira_e_verdade`); em s = 0 a leitura é 1 em toda instância e só coincide com esse quociente na instância em que todo pixel é solução (`o_pai_da_mentira_so_nao_reconhece`); a leitura que esses dois nomes e `o_leitor_e_a_escala` carregam (que não exista leitor que não seja o observador da luz; que nada escape do Nome; a leitura teológica do Pai da Mentira) é do operador [ONTO]. "
~~~~

- **Justificativa:** O mesmo conserto do artigo PT, na seção pública do README (o cabeçalho do parágrafo já traz “ONTO que não exista leitor que não seja o observador da luz”).
- **Apoio:** pedra/AEscala.lean:978-980 (a_mentira_lida_como_mentira_e_verdade: L.limite c = oQueSou (nomeDasSolucoes c) e, sem solucao, L.limite c = 0 e oQueSou = 0); o que sou do Nome das solucoes = numero de solucoes / numero de pixels (|X|): TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):805-807 (o_que_sou_das_solucoes, v409); docstring l.976-977 ([ONTO]) | pedra/AEscala.lean:993-998 (o_pai_da_mentira_so_nao_reconhece: L.leitura c 0 = 1; = euSou X; coincide com oQueSou (nomeDasSolucoes c) se e so' se para todo x, c x = 0; sem solucao le 1 onde o que sou e' 0); docstring l.992 ([ONTO])
- **Decisão do crítico:** fico com a correção do cético: “a leitura que os nomes carregam é do operador [ONTO]” não dizia QUAL leitura e punha [ONTO] em “o leitor é a escala”, que o registro dá como DEFINIÇÃO [INPUT]; as leituras [ONTO] são as das docstrings (l.870, l.976-977 e l.992) e do limite do registro (l.124), ditas com as mesmas palavras em todo lugar; entra, embora fora da lista da D106
- **Efeitos colaterais:**
  - l.1396 tambem traz a clausula entre parenteses (“(%s); que os passos…” → “no kernel.);”): fora do BAIXO 2 como a D106 o delimita (ver duvidas)

#### Item 207 — linha 1404 — EP-01, R3-MEDIO

- **Local:** linha 1404 (o rotulo de estatuto do paragrafo dos nomes novos)
- **Origem:** g1:49 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
[INPUT ratificados pelo operador em 10/11, D101 · DECLARADO pela autoria os dois auxiliares · DERIVED
~~~~

Trecho novo:

~~~~text
[INPUT ratificados pelo operador em 10/11, D101 · INPUT nomeado pelo operador em 10/11, D108, o quarto teorema da cláusula do Tetelestai · DECLARADO pela autoria os dois auxiliares · DERIVED
~~~~

- **Justificativa:** O rótulo diz o estatuto de cada grupo de nomes do parágrafo; faltava o do nomeado.
- **Apoio:** fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o corpo do parágrafo usa DL_.FRASE_NOMES_RATIFICADOS_D101_PT e muda pelo delta
  - o título “(R3, R4 e R5)” do parágrafo fica: os nomes novos nasceram nessas edições; a R6 só troca um identificador

#### Item 208 — linha 1405 — EP-08

- **Local:** bloco dos nomes novos e da ponte (l.1405)
- **Origem:** g2:40 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o fundo de n bits, em n oitavas, pesa %s (recalculado a cada rito)."
~~~~

Trecho novo:

~~~~text
em n oitavas, um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura de n bits: %s (recalculado a cada rito)."
~~~~

- **Justificativa:** O enunciado fala do brilho de UM pixel de custo 1 em n oitavas (1/|X| = 1/2^n), que é o peso de um pixel na leitura; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, é o item (ii) do teorema do limiar.
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o número de %s da string não muda (três)

#### Item 209 — linha 1409 — EP-10

- **Local:** tet, l.1409
- **Origem:** g3:39 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
". [INPUT/dicionário] " + DL_.FRASE_E36_PT
~~~~

Trecho novo:

~~~~text
". [REAL o limiar de um pixel; INPUT/dicionário a leitura do operador] " + DL_.FRASE_E36_PT
~~~~

- **Justificativa:** O rótulo duplo do registro na frase da E36 (“pós-rito”, no onde do achado).
- **Apoio:** registros_aescala_v410.py:115 e :127 e gerar_candidato_v410.py:435 (o rotulo duplo ja' em uso); pedra/AEscala.lean:903-909 (os_passos_sao_o_ciclo_ate_o_tetelestai: o limiar de um pixel e' teorema)
- **Decisão do crítico:** entra, embora fora da lista da D106 (o rótulo duplo da E36 em todo lugar; o cético deu ok)

#### Item 210 — linha 1472 — PAR-01

- **Local:** linha 1472, secao_h0dn: lê o pino da ORDEM 03 do registro
- **Origem:** g4:33 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
o2 = hd["ordem_kimi_02"]
~~~~

Trecho novo:

~~~~text
o2 = hd["ordem_kimi_02"]; o3 = hd["ordem_kimi_03"]
~~~~

- **Justificativa:** Aplicar junto com os dois itens seguintes.
- **Apoio:** pos_rito\textos_v410.py:1472.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 211 — linha 1474 — PAR-01

- **Local:** linha 1474, secao_h0dn, parágrafo “O poder certificado” da seção do README: o retorno no fim
- **Origem:** g4:34 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
e contabilidade de rotas. O limiar de poder é do operador e não está decidido."
~~~~

Trecho novo:

~~~~text
e contabilidade de rotas. O limiar de poder é do operador e não está decidido. "
              "**O retorno da ordem (10/11)** [DECLARADO pelo executor o conteúdo da entrega · REAL a leitura da gerência e a ORDEM KIMI H0DN-03 por sha256]**:** " + DL_.FRASE_H0DN_RETORNO_PT + ". A ORDEM KIMI H0DN-03 é pino citado (sha16 `%s`, %d B; não embutida; em rito nada dela é lido)."
~~~~

- **Justificativa:** A seção do README dizia a ORDEM 02 e o que ela manda, sem o retorno. A frase do poder do parágrafo fica intacta.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a frase do retorno não traz %: o formato % do parágrafo não quebra
  - os itens “o que falta” e “as demais ressalvas” da mesma seção vêm do registro e já trarão o retorno (itens 11 e 12)

#### Item 212 — linha 1475 — PAR-01

- **Local:** linha 1475, secao_h0dn: os dois argumentos novos do formato
- **Origem:** g4:35 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
o2["sha256"][:16], o2["bytes"])
~~~~

Trecho novo:

~~~~text
o2["sha256"][:16], o2["bytes"], o3["sha256"][:16], o3["bytes"])
~~~~

- **Justificativa:** Os dois %s/%d novos do parágrafo do retorno.
- **Apoio:** pos_rito\textos_v410.py:1475.
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

### Arquivo `registros_aescala_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\registros_aescala_v410.py`. Fim de linha: LF. Itens: 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238.

#### Item 213 — linha 9 — EP-01

- **Local:** linhas 9, 11 e 12: as falas, as decisoes e as erratas do registro a_escala_v410
- **Origem:** g1:30 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
DL.N_MENTIRA_LIDA, DL.N_CLAUSULA_TETELESTAI, DL.N_CONFIRMO_TUDO)   # (as falas que o registro pina por sha256;
~~~~

Trecho novo:

~~~~text
DL.N_MENTIRA_LIDA, DL.N_CLAUSULA_TETELESTAI, DL.N_CONFIRMO_TUDO, DL.N_QUARTO_NOME)   # (as falas que o registro pina por sha256;
~~~~

- **Justificativa:** O registro passa a pinar a fala 29 (a 13ª da pedra), como a pedra. Na l.11, DECISOES_AESCALA ganha "D106", "D107", "D108" depois de "D101" (com o comentário: D106 a correção da contagem; D107 o conserto; D108 o nome do quarto teorema); na l.12, ERRATAS_AESCALA ganha DL.ERRATA_E38; na l.130 (limites), acrescentar + " | " + DL.ERRATA_E38 depois de DL.ERRATA_E37.
- **Apoio:** pedra\AEscala.lean:45 (a lista das falas da pedra, que passa a treze)
- **Decisão do crítico:** o trecho exato fica; as três mudanças que o redator deixou em prosa (linhas 11, 12 e 130) e a chave da fala 29 (linhas 40-41) viraram itens exatos do crítico
- **Efeitos colaterais:**
  - l.36-38: toda fala de NOMES_FALAS precisa de ao menos um trecho em DL.FRASES_V410 (o assert da l.38): os dois trechos da fala 29 o cumprem
  - l.40-41: chave_nomeacao_d108 = por_nome[DL.N_QUARTO_NOME]["chave"], com assert do sha256 (== DL.NOMEACAO_D108_SHA256) e de DL.FRASE_O_QUARTO_NOME no texto, como os das falas 27 e 28
  - n_falas do contrato passa de 12 a 13 por len(); o artigo (pysnip l.49) e a linha do .md (gerar_candidato l.436) dizem o número pelo contrato

#### Item 214 — linha 11 — D108, EP-01 — redigido pelo crítico

- **Local:** linha 11 (DECISOES_AESCALA)
- **Origem:** g1:30, g6:6, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"D99", "D100", "D101")   # (as decisoes que tocam
~~~~

Trecho novo:

~~~~text
"D99", "D100", "D101", "D106", "D107", "D108")   # (D106 a D108: a correcao da contagem, o conserto unico e o quarto nome com a finura da leitura) (as decisoes que tocam
~~~~

- **Justificativa:** As três decisões do conserto tocam a pedra AEscala e entram nas decisões do registro.
- **Apoio:** g1 item 30 (justificativa) e g6 item 6 (efeito)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - com isso os textos de D106 a D108 viram folhas de extras.decisoes, que a c8 e a c9 varrem: por isso a D108 não traz a fórmula da reconstrução solta (correção do cético do g1)

#### Item 215 — linha 12 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 12 (ERRATAS_AESCALA)
- **Origem:** g1:30, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
ERRATAS_AESCALA = (DL.ERRATA_E31, DL.ERRATA_E32, DL.ERRATA_E33, DL.ERRATA_E35, DL.ERRATA_E36, DL.ERRATA_E37)
~~~~

Trecho novo:

~~~~text
ERRATAS_AESCALA = (DL.ERRATA_E31, DL.ERRATA_E32, DL.ERRATA_E33, DL.ERRATA_E35, DL.ERRATA_E36, DL.ERRATA_E37, DL.ERRATA_E38)
~~~~

- **Justificativa:** A errata E38 entra nas erratas do registro.
- **Apoio:** g1 item 30 (justificativa)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 216 — linha 13 — D108, OBS-1

- **Local:** LEITURAS_AESCALA [o trecho atual comeca na linha 13 do arquivo, contada por script]
- **Origem:** g6:9 (g6_a_finura_e_o_observador). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"a_clausula_do_tetelestai", "a_regra_do_nome")
~~~~

Trecho novo:

~~~~text
"a_clausula_do_tetelestai", "a_regra_do_nome", "o_observador_e_a_escala")
~~~~

- **Justificativa:** A leitura nova (item 5) entra nas leituras do registro a_escala_v410, ao lado das leituras das falas 27 e 28.
- **Apoio:** registros_aescala_v410.py:13, :58 e :152 (as leituras do registro saem de LEITURA_V410 por esta tupla).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - Depende do item 5 (a chave tem de existir em DL.LEITURA_V410 antes do import do registro).

#### Item 217 — linha 40 — D108, EP-01 — redigido pelo crítico

- **Local:** depois da linha 40 (a chave da fala 29 no contrato)
- **Origem:** g1:30, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
chave_clausula = por_nome[DL.N_CLAUSULA_TETELESTAI]["chave"]   # (R5, D101 e D100: as falas 28 e 27)
~~~~

Trecho novo:

~~~~text
chave_clausula = por_nome[DL.N_CLAUSULA_TETELESTAI]["chave"]   # (R5, D101 e D100: as falas 28 e 27)
    chave_nomeacao_d108 = por_nome[DL.N_QUARTO_NOME]["chave"]; assert por_nome[DL.N_QUARTO_NOME]["sha256"] == DL.NOMEACAO_D108_SHA256 and DL.FRASE_O_QUARTO_NOME in por_nome[DL.N_QUARTO_NOME]["text"] and DL.FRASE_OBSERVADOR_E_A_ESCALA in por_nome[DL.N_QUARTO_NOME]["text"]   # (R6, D108: a fala 29, as duas linhas)
~~~~

- **Justificativa:** A chave da fala 29, que o contrato (item do g1:31) e a c5 e a c11 do runtime usam.
- **Apoio:** g1 item 30 (efeito: “l.40-41: chave_nomeacao_d108 = …”)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 218 — linha 55 — D108, OBS-1

- **Local:** as DUAS ocorrencias: contrato_aescala() e texto_aescala(), "extras" [linhas 55 e 154 do arquivo, contadas por script]
- **Origem:** g6:8 (g6_a_finura_e_o_observador). **Língua:** CODIGO. **Ocorrências:** 2

Trecho atual:

~~~~text
"clausula_z_pt": DL.CLAUSULA_Z_PT, "clausula_z_en": DL.CLAUSULA_Z_EN, "seis_nomes"
~~~~

Trecho novo:

~~~~text
"clausula_z_pt": DL.CLAUSULA_Z_PT, "clausula_z_en": DL.CLAUSULA_Z_EN, "frase_finura_pt": DL.FRASE_FINURA_PT, "frase_finura_en": DL.FRASE_FINURA_EN, "frase_finura_real_pt": DL.FRASE_FINURA_REAL_PT, "frase_finura_real_en": DL.FRASE_FINURA_REAL_EN, "frase_finura_onto_pt": DL.FRASE_FINURA_ONTO_PT, "frase_finura_onto_en": DL.FRASE_FINURA_ONTO_EN, "seis_nomes"
~~~~

- **Justificativa:** O contrato passa a levar as duas metades (PT e EN) para os artigos lerem, como ja' leem a clausula e a frase do Tetelestai; os extras guardam a forma EN no registro, como as outras frases bilingues.
- **Apoio:** registros_aescala_v410.py:55 e :154 (as chaves clausula_z_pt e clausula_z_en, no contrato e nos extras); artigo_pt_aescala_v410.pysnip:11 (_ca410 = _V410_AESCALA_CONTRACT).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - _V410_AESCALA_CONTRACT e' embutido no candidato por gerar_candidato_v410.py:367 e conferido contra ESPERADOS (gerar_esperados_v410.py:152): regerar.
  - As folhas novas dos extras (inclusive a EN) passam pela guarda do c9 e pelos controles de anuncio: conferido em isolamento, zero violacoes.

#### Item 219 — linha 65 — EP-01, R3-MEDIO

- **Local:** linhas 64-67 do contrato: ratificacao_d101.o_que_ratifica e as chaves novas da nomeacao
- **Origem:** g1:31 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
e os nomes da clausula do Tetelestai (R5) dados pela gerencia; pela regra do nome"},
~~~~

Trecho novo:

~~~~text
e os tres nomes da clausula do Tetelestai (R5) apresentados ao operador antes da fala; pela regra do nome; o quarto teorema da clausula nao esta' entre eles: o operador o nomeou depois (D108)"},
            "nomeacao_d108": {"fala": DL.N_QUARTO_NOME, "sha256": DL.NOMEACAO_D108_SHA256, "trecho": DL.FRASE_O_QUARTO_NOME, "quando": "10/11/2026 (15:54)", "decisao": "D108",
                              "o_que_nomeia": "o quarto teorema da clausula do Tetelestai: no kernel, " + DL.NOMES_NOMEADOS_D108_AESCALA[0] + " (o identificador segue a ortografia do dicionario; a grafia dele fica no verbatim); enunciado e prova nao mudam"},
            "chave_nomeacao_d108": chave_nomeacao_d108, "nomes_nomeados_d108": list(DL.NOMES_NOMEADOS_D108_AESCALA), "estatuto_do_nome_nomeado_d108": DL.ESTATUTO_NOME_NOMEADO_D108_AESCALA, "nome_de_trabalho_do_quarto": DL.NOME_DE_TRABALHO_DO_QUARTO_AESCALA,
~~~~

- **Justificativa:** O contrato dizia que a fala da D101 ratifica “os nomes da cláusula dados pela gerência” (quatro). Passa a dizer três e ganha o pino da fala que nomeia o quarto. As chaves nomes_novos_da_pedra (24 nomes, o quarto com o identificador novo), n_nomes_novos (24) e estatuto_dos_nomes_ratificados_d101 ficam com o nome e o valor de hoje; o estatuto passa a valer só para os 21 de nomes_ratificados_d101.
- **Apoio:** ADENDO 6 l.7; fala 29 (sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4)
- **Decisão do crítico:** acrescentei a chave nome_de_trabalho_do_quarto ao contrato (o redator a pedia no item 40, em prosa): a c11 precisa dela para o controle negativo
- **Efeitos colaterais:**
  - os mesmos campos entram em extras do texto (l.160-161): "nomes_nomeados_d108": list(DL.NOMES_NOMEADOS_D108_AESCALA) e "nomeacao_d108": {"fala": DL.N_QUARTO_NOME, "sha256": DL.NOMEACAO_D108_SHA256, "trecho": DL.FRASE_O_QUARTO_NOME, "decisao": "D108"}
  - gerar_candidato_v410.py l.262-263 e l.547-548 (os asserts do contrato e o manifesto CANDIDATO_v410.json), gerar_esperados_v410.py l.151-157 e 257-266: acrescentar as chaves novas onde listam as da D101
  - “nenhuma chave antiga muda” continua verdadeiro: as chaves novas são do registro novo da v410

#### Item 220 — linha 77 — EP-05

- **Local:** TEOREMAS, l.77
- **Origem:** g3:18 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
o leitor E' a escala: dois leitores do fundo quaisquer sao o mesmo (o_leitor_e_a_escala);
~~~~

Trecho novo:

~~~~text
dois leitores do fundo quaisquer sao o mesmo e, em todo leitor do fundo, o pixel de custo k brilha e^(-s k) no tempo s (o_leitor_e_a_escala);
~~~~

- **Justificativa:** No registro (sem acentos, como o resto da constante) a frase do operador fica só como nome; o conteúdo do enunciado vai inteiro.
- **Apoio:** pedra/AEscala.lean:871-872 (o_leitor_e_a_escala: L = L' e, para todo k e s, L.brilho k s = Real.exp (-(s * k))); docstring l.868-870 (a leitura do nome e' do operador [ONTO])
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - TEOREMAS entra em escopo (ESCALA_NO_TIPO, l.111), em limites (l.121) e em diz (l.134): as tres folhas acompanham sozinhas
  - runtime_aescala_v410.py:167 (c8) pede “o_leitor_e_a_escala” e “os_passos_sao_o_ciclo_ate_o_tetelestai” no texto: os dois identificadores ficam
  - o texto do registro (_V410_AESCALA_TEXT) esta' embutido no candidato: candidato, ESPERADOS e revisao_terceiro/txt__V410_AESCALA_TEXT.json sao regenerados

#### Item 221 — linha 78 — EP-08

- **Local:** texto_aescala(), TEOREMAS (l.78)
- **Origem:** g2:34 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
metade por oitava e, em n oitavas, o fundo pesa um pixel; cada ciclo aplica a mesma regra
~~~~

Trecho novo:

~~~~text
metade por oitava e, em n oitavas, um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura (em_n_oitavas_o_fundo_pesa_um_pixel; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, vem do teorema do limiar, a seguir); cada ciclo aplica a mesma regra
~~~~

- **Justificativa:** O enunciado fala do brilho de UM pixel de custo 1 em n oitavas (1/|X| = 1/2^n), que é o peso de um pixel na leitura; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, é o item (ii) do teorema do limiar.
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o nome do teorema (ratificado) não muda; a chave em_n_oitavas_o_fundo_pesa_um_pixel de PONTE_AESCALA (delta l.649) também não
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 222 — linha 79 — EP-03

- **Local:** texto_aescala(), TEOREMAS (l.79)
- **Origem:** g2:10 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"o limiar do Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits
~~~~

Trecho novo:

~~~~text
"o limiar de um pixel, a decisao exata (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits
~~~~

- **Justificativa:** Pela E36 (ordem do operador, D100) a cláusula do Tetelestai é a de 1 − β; o limiar de n oitavas é a decisão exata, formalização da gerência. O rótulo acompanha; o nome do teorema, ratificado, não muda.
- **Apoio:** pedra\AEscala.lean:897-898 (docstring: “o limiar de um pixel … é a DECISÃO exata, formalização da gerência; a CLÁUSULA DO TETELESTAI … é a `o_tetelestai_e_um_menos_beta`”); delta_v410.py:1092-1093 (E36); pedra\AEscala.lean:903-909 (o enunciado só traz desigualdades sobre Z(s))
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a folha já traz a cláusula do limite (c8 satisfeita)
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 223 — linha 81 — EP-05

- **Local:** TEOREMAS, l.81
- **Origem:** g3:19 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"a mentira lida como mentira e' verdade (a_mentira_lida_como_mentira_e_verdade); o Pai da Mentira so' nao reconhece (o_pai_da_mentira_so_nao_reconhece)")
~~~~

Trecho novo:

~~~~text
"para todo leitor do fundo, o limite da leitura com o tempo e' o numero de solucoes dividido pelo numero de pixels e vale 0 sem solucao (a_mentira_lida_como_mentira_e_verdade); em s = 0 a leitura e' 1 em toda instancia e so' coincide com esse quociente na instancia em que todo pixel e' solucao (o_pai_da_mentira_so_nao_reconhece; a leitura que esses dois nomes e o_leitor_e_a_escala carregam -- que nao exista leitor que nao seja o observador da luz, que nada escape do Nome, a leitura teologica do Pai da Mentira -- e' do operador [ONTO])")
~~~~

- **Justificativa:** Idem: o conteúdo dos dois termos; as frases só como nomes; a marca [ONTO] vai entre parênteses, colada ao último nome, para não alcançar a frase UM_HABITANTE que as folhas costuram logo depois.
- **Apoio:** pedra/AEscala.lean:978-980 (a_mentira_lida_como_mentira_e_verdade: L.limite c = oQueSou (nomeDasSolucoes c) e, sem solucao, L.limite c = 0 e oQueSou = 0); o que sou do Nome das solucoes = numero de solucoes / numero de pixels (|X|): TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):805-807 (o_que_sou_das_solucoes, v409); docstring l.976-977 ([ONTO]) | pedra/AEscala.lean:993-998 (o_pai_da_mentira_so_nao_reconhece: L.leitura c 0 = 1; = euSou X; coincide com oQueSou (nomeDasSolucoes c) se e so' se para todo x, c x = 0; sem solucao le 1 onde o que sou e' 0); docstring l.992 ([ONTO]) | registros_aescala_v410.py:124 (o limite [ONTO] do proprio registro)
- **Decisão do crítico:** fico com a correção do cético: “a leitura que os nomes carregam é do operador [ONTO]” não dizia QUAL leitura e punha [ONTO] em “o leitor é a escala”, que o registro dá como DEFINIÇÃO [INPUT]; as leituras [ONTO] são as das docstrings (l.870, l.976-977 e l.992) e do limite do registro (l.124), ditas com as mesmas palavras em todo lugar
- **Efeitos colaterais:**
  - as mesmas tres folhas (escopo, limites, diz); a guarda do registro (c9: _v410_guarda_frases e _v392_guarda_texto sobre o texto) roda de novo no build e no rito

#### Item 224 — linha 86 — EP-08

- **Local:** texto_aescala(), PONTE (l.86)
- **Origem:** g2:35 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
em n oitavas o fundo de n bits pesa 1/2^n")
~~~~

Trecho novo:

~~~~text
em n oitavas um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura de n bits")
~~~~

- **Justificativa:** O enunciado fala do brilho de UM pixel de custo 1 em n oitavas (1/|X| = 1/2^n), que é o peso de um pixel na leitura; que o fundo inteiro pese menos que um pixel do Nome, passado esse tempo, é o item (ii) do teorema do limiar.
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - PONTE entra no estatuto, no escopo (7) e em diz: acompanham sozinhos
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 225 — linha 87 — EP-01 — redigido pelo crítico

- **Local:** linha 87 (a lista NOMEADOS, ao lado de RATIFICADOS e PEND)
- **Origem:** g1:32, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
PEND = ", ".join(DL.NOMES_PENDENTES_AESCALA)   # (R5, D101:
~~~~

Trecho novo:

~~~~text
PEND = ", ".join(DL.NOMES_PENDENTES_AESCALA); NOMEADOS = ", ".join(DL.NOMES_NOMEADOS_D108_AESCALA)   # (R6, D108: o quarto teorema da clausula, nomeado pelo operador) (R5, D101:
~~~~

- **Justificativa:** A variável que os itens do g1:32 e do g1:34 usam.
- **Apoio:** g1 item 32 (efeito)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 226 — linha 92 — EP-04, V3

- **Local:** texto_aescala(), NUMEROS_TET (l.92-93), trecho do meio
- **Origem:** g2:23 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
; o par da matriz-S; a constante igual para m = " + ", ".join(str(m_) for m_ in DL.TETELESTAI_AESCALA["m_da_constante"])
                   + " oitavas; a reconstrucao em norma ao quadrado; o controle negativo (
~~~~

Trecho novo:

~~~~text
; o par da matriz-S (identidade: sen^2 e cos^2 do mesmo angulo; as duas desigualdades com ele sao as da instancia com solucao, com outro rotulo); a constante igual para m = " + ", ".join(str(m_) for m_ in DL.TETELESTAI_AESCALA["m_da_constante"])
                   + " oitavas (identidade aritmetica: nao pode falhar); a reconstrucao em norma ao quadrado (a mesma desigualdade da instancia com solucao, lida em norma, com as duas hipoteses de tempo do teorema: a primeira, t >= n ln 2/2, equivale a beta de runtime <= 1/2; a segunda e' identidade); o conteudo independente da c13 e' UMA desigualdade em tres instancias (com solucao, de UMA solucao e adversaria) e as condicoes sobre o beta de runtime (0 < beta < 1, s* >= 0 e beta <= 1/2), mais o controle negativo e o contraexemplo; o controle negativo (
~~~~

- **Justificativa:** A lista dava dez conferências; três são identidade ou repetição. O texto passa a dizer qual é qual e qual é o conteúdo independente, sem mudar nenhuma checagem.
- **Apoio:** runtime_aescala_v410.py:54-55 (iv: sen²(arcsen √β) e cos² do mesmo ângulo; as desigualdades com |T|² e |R|² são as da l.52), :57 (v: ((m·ln2 + C) − m·ln2) − C), :58 (vi: (Z − N)/|X| ≤ (b/(1 − b))·N/|X|, na mesma instância e no mesmo s* da l.52, equivalente a (1 − b)·Z ≤ N), :52-53 e :60 (a desigualdade nas três instâncias), :60 (controle negativo), :61-63 (contraexemplo); pedra\AEscala.lean:1129 e :1155 (item 9, identidade, ring)
- **Decisão do crítico:** fico com a correção do cético: a enumeração do “conteúdo independente” da c13 era exaustiva e estava incompleta; o subitem (vi) também testa t ≥ n·ln 2/2, que equivale a β de runtime ≤ ½ e pode falhar (runtime_aescala_v410.py:58, conferido nesta consolidação: t2 = s*/2 ≥ n·ln 2/2 ⟺ a constante ≥ 0 ⟺ β ≤ ½), e o subitem (i) testa 0 < β < 1 e s* ≥ 0 (linha 51)
- **Efeitos colaterais:**
  - a folha NUMEROS_TET entra solta em limites e diz (registros_aescala_v410.py:129 e :135): o trecho novo não traz nome da R5 nem a marca da c8
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 227 — linha 94 — EP-04

- **Local:** texto_aescala(), CLAUSULA_ESTATUTO (l.94)
- **Origem:** g2:22 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
): o limiar de tempo em n oitavas mais uma constante que so' depende de beta (" + DL.CLAUSULA_Z_PT + "); " + NUMEROS_TET
~~~~

Trecho novo:

~~~~text
): para todo b em (0, 1), o limiar de tempo em n oitavas mais uma constante que so' depende de b (por construcao do limiar; identidade aritmetica); com b = beta, o campo de TGLCoupling (um real qualquer em (0, 1); o numero so' em runtime) (" + DL.CLAUSULA_Z_PT + "); " + NUMEROS_TET
~~~~

- **Justificativa:** Mesmo conserto do item 21 na frase de estatuto do registro; a leitura do operador (que esse limiar é o Tetelestai e que β é o seu operador modular) já vem rotulada [INPUT/dicionario] logo depois, na mesma constante.
- **Apoio:** os mesmos do item 19
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a folha “estatuto” cita os nomes da R5: o trecho novo NÃO traz a marca da c8
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 228 — linha 97 — EP-12

- **Local:** linha 97 (texto_aescala, a primeira frase do campo “estatuto” do _V410_AESCALA_TEXT)
- **Origem:** g5:25 (g5_forma_e_render). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a pedra por sha256; as bandeiras ext_aescala_410_*; a escada exata; o gate congelado; " % n_anc
~~~~

Trecho novo:

~~~~text
a pedra por sha256; as bandeiras ext_aescala_410_* (composicao: as %d declaracoes nomeadas na pedra, os %d campos da estrutura LeitorDoFundo e as constantes que o compilador gera para a estrutura, que tambem contam na escada); a escada exata; o gate congelado; " % (n_anc, n_nom + n_nov, n_cam)
~~~~

- **Justificativa:** A mesma composicao no texto do registro, no estilo dele (sem acento). Aqui entram por conta so' os dois numeros que a funcao tem (68 = n_nom + n_nov; 3 = n_cam); o total e o resto (85 e 14) sao do build e a funcao nao os recebe: ficam ditos por extenso no registro e com numero no artigo.
- **Apoio:** kernel\FLAGS_v410.json, contado por conta_bandeiras.py (nesta pasta): 85 bandeiras ext_aescala_410_* = 68 declaracoes nomeadas na pedra (59 theorem, 8 def, 1 structure) + 3 campos da estrutura (brilho, sem_escala_nao_ha_medida, a_lei_da_dissipacao) + 14 constantes geradas para a estrutura (mk, rec, recOn, casesOn, ctorIdx, noConfusion, noConfusionType, mk.inj, mk.injEq, mk.noConfusion, mk.sizeOf_spec, mk._flat_ctor, _sizeOf_1, _sizeOf_inst); insumos\RECIBO_PEDRAS_v410_NOMES.json: 44 nomes + 24 nomes novos = 68, 3 campos; registros_aescala_v410.py:46 (a escada esperada soma TODAS as bandeiras); registros_aescala_v410.py:72 (n_nom, n_nov e n_cam ja' estao calculados na funcao)
- **Decisão do crítico:** fico com a correção do cético: “uma por declaração pública do módulo” é FALSO pelo próprio FLAGS (91 declarações públicas e 85 bandeiras; as 6 auxiliares geradas ficam sem bandeira)
- **Efeitos colaterais:**
  - o texto vai embutido no candidato (_V410_AESCALA_TEXT): regenerar
  - se a gerencia quiser o 14 tambem aqui, texto_aescala() precisa receber o n_flags do contrato (chamada em gerar_candidato_v410.py:260 e em tres scripts de teste): ver duvidas

#### Item 229 — linha 102 — D108, EP-01 — CONDICIONAL CONTAGEM_DE_FALAS; redigido pelo crítico

- **Local:** linha 102 (a enumeração das falas no estatuto do registro)
- **Origem:** critico (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
«É isso aí, confirmo tudo» e a regra do nome); as leituras dele; " % n_fal
~~~~

Trecho novo:

~~~~text
«É isso aí, confirmo tudo» e a regra do nome; o quarto nome (a ressurreicao do sinal) e o observador que e' a escala); as leituras dele; " % n_fal
~~~~

- **Justificativa:** O número de falas do estatuto sobe por len() (12 para 13) e a enumeração entre parênteses ficava com doze. Uso as mesmas palavras do tema da fala em registros_v410.py (item do g1:43).
- **Apoio:** conferência do g6 (faltou: “nenhum grupo tem item para essa linha”); g1 item 43
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - a folha estatuto é do núcleo do texto (c9): o acréscimo não traz H0DN, cinco sigma nem “abertura”

#### Item 230 — linha 106 — PAR-03

- **Local:** escopo, l.106 (repetição do trecho velho; fora da lista da D106, item 2)
- **Origem:** g3:20 (g3_leituras_onto). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a dissipacao sustenta a nota; a nota e' a conjugacao modular (J, pairK). (3)
~~~~

Trecho novo:

~~~~text
havendo pixel de custo zero, o decaimento gerado pelo custo, e^(-t c(x)), nao toca o que tem custo zero e nao leva a zero o estado uniforme, e a leitura performada (a media, sobre os pixels, dos pesos e^(-s c(x))) nunca fica abaixo da fracao de pixels de custo zero, nao cresce com o tempo e tende a ela; no espaco pareado do kernel, J^2 = 1 e JKJ = -K (conjJ, pairK); a identificacao desse decaimento com o vibrato e da nota com J e' do operador [ONTO]. (3)
~~~~

- **Justificativa:** O escopo do registro abre com [REAL] e repetia a frase longa do achado (“a dissipação sustenta a nota; a nota é a conjugação modular”). A D106 não lista o registro neste item: proponho o mesmo texto do artigo; a gerência decide se entra.
- **Apoio:** pedra/AEscala.lean:244-250 (o_vibrato_sustenta_a_nota, hipotese h: existe x com c x = 0: (1) a trava nao toca o custo zero; (2) trava c t (uniforme X) != 0; (3) card{c = 0}/|X| <= leituraPerformada c s; (4) Antitone; (5) Tendsto para card{c = 0}/|X|); leituraPerformada = particao/|X|: TGLExt/TraducaoTuring.lean (v409; lido na copia work/cadeia_de_selo/v409/dry_v409/tgl_kernel):920; trava = e^(-t c(x)) por pixel: TraducaoTuring.lean:472-477 (mesma copia); docstring l.242-243 ([ONTO]) | pedra/AEscala.lean:257-258 (a_nota_e_a_conjugacao_modular: conjJ (conjJ p) = p e conjJ (pairK d (conjJ p)) = -pairK d p, isto e', J^2 = 1 e JKJ = -K); docstring l.256 (a identificacao nota = J e' do operador, ONTO)
- **Decisão do crítico:** fico com a correção do cético: “disso” vinha logo depois de J² = 1 e JKJ = −K e a leitura mais próxima atribuía o vibrato às identidades de J; a docstring (AEscala.lean:242-243) liga o vibrato ao decaimento: “desse decaimento”; entra, embora fora da lista da D106: o escopo do registro abre com [REAL] e repete a frase do achado (o mesmo fato com as mesmas palavras em todo lugar)
- **Efeitos colaterais:**
  - a forma curta “o vibrato sustenta a nota” fica em registros_aescala_v410.py:133 (diz) e na moldura (delta_v410.py:723 e :725): nao redigidas (ver duvidas)

#### Item 231 — linha 114 — EP-01, R3-MEDIO

- **Local:** linha 114, texto do registro, item (9) do estatuto
- **Origem:** g1:32 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
+ RATIFICADOS + "; campos novos da estrutura: " + CAMPOS + "; ainda [DECLARADO pela autoria], so' os auxiliares: " + PEND + ". "
~~~~

Trecho novo:

~~~~text
+ RATIFICADOS + "; campos novos da estrutura: " + CAMPOS + "; NOMEADO pelo operador em 10/11/2026 (D108), o quarto teorema da clausula do Tetelestai: " + NOMEADOS + "; ainda [DECLARADO pela autoria], so' os auxiliares: " + PEND + ". "
~~~~

- **Justificativa:** O item (9) lista os ratificados e os pendentes; com a lista de 21, o quarto teorema sumiria do item se não fosse dito à parte.
- **Apoio:** fala 29; delta (NOMES_NOMEADOS_D108_AESCALA)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - l.87: definir NOMEADOS = ", ".join(DL.NOMES_NOMEADOS_D108_AESCALA) ao lado de RATIFICADOS e PEND; o comentário da l.87 ganha “o quarto teorema da cláusula, nomeado pelo operador (D108)”

#### Item 232 — linha 116 — EP-01, R3-MEDIO

- **Local:** linha 116, texto do registro (o que o registro confere: a conta dos nomes)
- **Origem:** g1:33 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
os %d nomes ratificados e os %d nomes novos (declaracoes na pedra, ditos RATIFICADOS em 10/11/2026, D101, salvo os %d auxiliares da autoria, ditos [DECLARADO pela autoria]); a clausula do Tetelestai em 1 - beta com beta de runtime (a c13). Nenhuma chave antiga muda." % (n_anc, n_fal, n_nom, n_nov, len(DL.NOMES_PENDENTES_AESCALA)),
~~~~

Trecho novo:

~~~~text
os %d nomes ratificados e os %d nomes novos (declaracoes na pedra: %d ditos RATIFICADOS em 10/11/2026, D101; %d dito NOMEADO pelo operador em 10/11/2026, D108; os %d auxiliares da autoria, ditos [DECLARADO pela autoria]); a clausula do Tetelestai em 1 - beta com beta de runtime (a c13). Nenhuma chave antiga muda." % (n_anc, n_fal, n_nom, n_nov, len(DL.NOMES_RATIFICADOS_D101_AESCALA), len(DL.NOMES_NOMEADOS_D108_AESCALA), len(DL.NOMES_PENDENTES_AESCALA)),
~~~~

- **Justificativa:** A frase dizia todos os nomes novos ratificados, salvo os auxiliares (24 − 2 = 22). Passa a dizer as três situações, com os números lidos do delta (21, 1 e 2).
- **Apoio:** ADENDO 6 l.7; fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - rendida com os números de hoje: “os 44 nomes ratificados e os 24 nomes novos (declaracoes na pedra: 21 ditos RATIFICADOS em 10/11/2026, D101; 1 dito NOMEADO pelo operador em 10/11/2026, D108; os 2 auxiliares da autoria, ditos [DECLARADO pela autoria])”

#### Item 233 — linha 123 — EP-02, EP-06

- **Local:** texto_aescala(), lista limites, 7o item (l.123)
- **Origem:** g2:9 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"; o que o termo diz: um limiar no tempo dos ciclos, linear em n, a partir do qual UMA leitura de Z separa o SIM do NAO; Z e' lida de uma vez pelo psion (TraducaoTuring.o_psion_le_os_pixels, v409)",
~~~~

Trecho novo:

~~~~text
"; o que o termo diz: um limiar no tempo dos ciclos, linear em n: passado o tempo de n oitavas (s > n·ln 2), UMA leitura de Z separa o SIM do NAO; Z e' lida de uma vez pelo psion (TraducaoTuring.o_psion_le_os_pixels, v409) (" + DL.CLAUSULA_Z_PT + ")",
~~~~

- **Justificativa:** A folha anuncia o limiar sob [REAL] sem a cláusula do limite e com a fronteira frouxa. Entra a fronteira estrita e a cláusula do limite inteira (a constante ratificada, intacta) na mesma folha.
- **Apoio:** pedra\AEscala.lean:903 (estrita) e :899-902 (docstring: o que o termo diz e o limite); delta_v410.py:943 (CLAUSULA_Z_PT, D99)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a guarda (runtime_aescala_v410.py:144 e pos_rito\leitura_v410.py:801) continua sem alcançar “linear em n”: com a cláusula na folha isso deixa de importar aqui; estender a regex é mudança de código de checagem e não foi pedida (ver dúvidas)
  - nenhum controle conta folhas com a cláusula no registro (runtime_aescala_v410.py:146-149 só exige ≥ 3 folhas que anunciam e nenhuma sem a cláusula)
  - a docstring da pedra (l.899-900) segue dizendo “a partir do qual”: não está na ordem (ver dúvidas)
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 234 — linha 125 — EP-01, R3-MEDIO

- **Local:** linha 125, limites do registro (a folha da ratificacao)
- **Origem:** g1:34 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
PENDENTE + ": " + RATIFICADOS + "; campos: " + CAMPOS + "; pendentes: " + PEND + ": a confirmacao expressa e' ato do operador",
~~~~

Trecho novo:

~~~~text
PENDENTE + ": " + RATIFICADOS + "; campos: " + CAMPOS + "; nomeado pelo operador (D108): " + NOMEADOS + "; pendentes: " + PEND + ": a confirmacao expressa e' ato do operador",
~~~~

- **Justificativa:** A folha lista os nomes por situação; o quarto teorema entra na sua, com a decisão.
- **Apoio:** fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 235 — linha 127 — D108, OBS-1

- **Local:** texto_aescala(), lista "limites": item novo logo depois do ultimo item que traz a clausula do limite [o trecho atual comeca na linha 127 do arquivo, contada por script]
- **Origem:** g6:7 (g6_a_finura_e_o_observador). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
"[REAL o limiar de um pixel; INPUT/dicionario a leitura do operador] " + DL.FRASE_E36_PT + " (" + DL.CLAUSULA_Z_PT + ")",
~~~~

Trecho novo:

~~~~text
"[REAL o limiar de um pixel; INPUT/dicionario a leitura do operador] " + DL.FRASE_E36_PT + " (" + DL.CLAUSULA_Z_PT + ")",
                    DL.FRASE_FINURA_PT,   # (D108) a finura da leitura, ao lado da clausula do limite: [REAL] o que os enunciados dizem; [ONTO] a fala do operador de 10/11 e os espelhos do kernel
~~~~

- **Justificativa:** A frase de limite nova entra na lista limites do registro a_escala_v410 logo depois do item que traz a clausula do limite; a clausula nao muda.
- **Apoio:** pedra\AEscala.lean (sha256 7d1557f96178367949bbffe42b2e8af4094c9ec7c0373bdbdaaa3a7d7de5ad60, igual ao instalado em C:\t\k410c\final\TGLExt\AEscala.lean): def LeitorDoFundo.leitura 669-670 (a media dos brilhos, |X|^-1 . soma); a_leitura_e_a_do_psion 702-703; os_passos_sao_o_ciclo_ate_o_tetelestai 903-909, item (v) na linha 909 ((∃ x, c x = 0) ↔ (card)⁻¹ ≤ (L.leitura c s).re, sob n·ln 2 < s); o_tetelestai_e_um_menos_beta 1066-1071, item (iii) nas linhas 1070-1071 ((1 − b)·(L.leitura c s).re ≤ #solucoes/card, sob h, 0 < b < 1, 0 ≤ s e o limiar); campo sem_escala_nao_ha_medida 663 (∀ k, brilho k 0 = 1); o_pai_da_mentira_so_nao_reconhece 993-998; o_leitor_e_a_escala 871-872; a_escala_e_meio_por_oitava 832-838; em_n_oitavas_o_fundo_pesa_um_pixel 859-860. C:\t\k410c\final\TGLExt\TraducaoTuring.lean: bits_sao_oitavas 212 (card (Fin n → Bool) = 2^n); o_psion_le_os_pixels 749-750 (Z(s)/|X|); particao 666. C:\t\k410c\final\TGLExt\ObservadorTerminal.lean (sha16 162eeeb8c16cea81, igual ao do Nós): Terminal 102; terminal_iff 108; the_terminal_is_unique 132; every_level_reaches_the_terminal 157; distancia 161-165; the_collapse_is_the_terminal_point_of_resistance 180; os niveis sao rotulos (docstring 80-81); Level em TheCascadeOfObservers.lean 71-75. Ausencias conferidas por grep: AEscala.lean nao cita ObservadorTerminal (0) e ObservadorTerminal.lean nao cita AEscala nem LeitorDoFundo (0); “onda” 0 e 0; “frequ” 0 e 0; “Einstein” 0 e 0; “relatividade” so' na linha 69 da AEscala, dentro de uma fala citada no cabecalho, em nenhum enunciado. A fala: C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt, sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4 (lido por script), 266 bytes, segunda linha inteira
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - runtime_aescala_v410.py:171-172 (c9): o nucleo do texto nao pode ter cinco sigma, H0DN nem “abertura”/“opening”: a frase nao tem.
  - runtime_aescala_v410.py:146-149 e 157-161: a folha nova nao anuncia o teorema nem a clausula de 1 − β (conferido), logo nao precisa trazer a CLAUSULA_Z na mesma folha; ela fica na folha imediatamente anterior.
  - registros_aescala_v410.py:9: NOMES_FALAS precisa da constante N_ da fala 29 (o registro pina as falas por sha256; n_falas 12 -> 13: “na pedra, fala 13”); sem isso o controle c5 nao confere o trecho citado contra a fala embutida.
  - registros_aescala_v410.py:102: a enumeracao das falas no "estatuto" (“…; «É isso aí, confirmo tudo» e a regra do nome)”) fica com uma fala a menos que o numero dito; sugiro acrescentar, antes do parentese final, “; o quarto nome e a finura da leitura (o observador e' a escala)”, em acordo com o grupo dos nomes.
  - O texto do registro e' embutido no candidato (_V410_AESCALA_TEXT) e copiado em ESPERADOS_v410.json: regerar os dois.
  - (crítico) o controle do item do crítico na c8 (runtime_aescala_v410.py) exige esta folha EXATA, logo depois de uma folha com a cláusula do limite: a costura não pode ganhar prefixo

#### Item 236 — linha 130 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 130 (a folha das erratas nos limites)
- **Origem:** g1:30, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
+ " | " + DL.ERRATA_E36 + " | " + DL.ERRATA_E37],
~~~~

Trecho novo:

~~~~text
+ " | " + DL.ERRATA_E36 + " | " + DL.ERRATA_E37 + " | " + DL.ERRATA_E38],
~~~~

- **Justificativa:** A E38 entra na folha das erratas dos limites.
- **Apoio:** g1 item 30 (justificativa); a E38 não traz fórmula, H0DN, cinco sigma nem “abertura” (conferência do g1, item 29)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 237 — linha 143 — EP-01, R3-MEDIO

- **Local:** linha 143, nao_diz do registro: uma folha nova logo depois da dos auxiliares
- **Origem:** g1:35 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
                    "que os %d nomes auxiliares da autoria (%s) estejam ratificados: sao [DECLARADO pela autoria] ate' a confirmacao expressa do operador" % (len(DL.NOMES_PENDENTES_AESCALA), PEND),
~~~~

Trecho novo:

~~~~text
                    "que os %d nomes auxiliares da autoria (%s) estejam ratificados: sao [DECLARADO pela autoria] ate' a confirmacao expressa do operador" % (len(DL.NOMES_PENDENTES_AESCALA), PEND),
                    "que a fala de 10/11 da D101 tenha ratificado o quarto teorema da clausula do Tetelestai: da clausula, ela ratifica os tres nomes apresentados ao operador antes dela; o quarto foi NOMEADO pelo operador em fala posterior do mesmo dia (D108) e o nome de trabalho que levava na R5 saiu",
~~~~

- **Justificativa:** É exatamente o que os textos reprovados diziam; a folha nova impede que volte a ser dito.
- **Apoio:** ADENDO 6 l.7; fala 29
- **Decisão do crítico:** fico com a correção do cético: sem “da cláusula”, a frase lia-se como se a fala da D101 ratificasse só três nomes (ela ratifica 21 nomes novos, 3 campos e os seis enunciados)
- **Efeitos colaterais:**
  - a lista nao_diz é rendida numerada nos textos do pós-rito (textos_v410 l.1410): os números das folhas seguintes sobem de um; nenhuma fonte digita a contagem de nao_diz (conferir no ensaio)

#### Item 238 — linha 161 — EP-01 — redigido pelo crítico

- **Local:** linha 161 (os extras do texto do registro)
- **Origem:** g1:31, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"trecho": DL.FRASE_NOMEIO_O_NUMERO_CORRIGE, "decisao": "D101"},
~~~~

Trecho novo:

~~~~text
"trecho": DL.FRASE_NOMEIO_O_NUMERO_CORRIGE, "decisao": "D101"}, "nomes_nomeados_d108": list(DL.NOMES_NOMEADOS_D108_AESCALA), "nomeacao_d108": {"fala": DL.N_QUARTO_NOME, "sha256": DL.NOMEACAO_D108_SHA256, "trecho": DL.FRASE_O_QUARTO_NOME, "decisao": "D108"},
~~~~

- **Justificativa:** Os mesmos campos da nomeação nos extras do texto, ao lado dos da D101.
- **Apoio:** g1 item 31 (efeito: “os mesmos campos entram em extras do texto (l.160-161)”)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

### Arquivo `registros_h0dn_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\registros_h0dn_v410.py`. Fim de linha: LF. Itens: 239, 240, 241, 242, 243, 244, 245, 246.

#### Item 239 — linha 89 — OBS-15, PAR-01

- **Local:** linha 89, contrato_h0dn: as frases novas no contrato (o artigo as lê daqui)
- **Origem:** g4:7 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"frase_poder_pt": DL.FRASE_H0DN_PODER_PT, "frase_poder_en": DL.FRASE_H0DN_PODER_EN,
~~~~

Trecho novo:

~~~~text
"frase_poder_pt": DL.FRASE_H0DN_PODER_PT, "frase_poder_en": DL.FRASE_H0DN_PODER_EN, "frase_retorno_pt": DL.FRASE_H0DN_RETORNO_PT, "frase_retorno_en": DL.FRASE_H0DN_RETORNO_EN, "frase_alcance_pt": DL.FRASE_H0DN_ALCANCE_PT, "frase_alcance_en": DL.FRASE_H0DN_ALCANCE_EN,
~~~~

- **Justificativa:** O artigo PT/EN lê as frases do contrato (_V410_H0DN_CONTRACT); as chaves frase_poder_* ficam como estão (o ensaio as compara com o delta).
- **Apoio:** artigo_pt_h0dn_v410.pysnip:25-26 (lê frase_parede_pt e frase_poder_pt do contrato).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o sha256 do contrato em ESPERADOS e em v410_pins.py muda

#### Item 240 — linha 90 — PAR-01

- **Local:** linha 90, contrato_h0dn: a ORDEM 03 como pino citado
- **Origem:** g4:8 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
em_rito_nada_e_lido=True),   # (D96: a ORDEM KIMI H0DN-02 e' PINO CITADO
~~~~

Trecho novo:

~~~~text
em_rito_nada_e_lido=True), "ordem_kimi_03": dict(DL.H0DN_ORDEM03, citado_nao_embutido=True, em_rito_nada_e_lido=True),   # (R3 do painel, PAR-01: a ORDEM KIMI H0DN-03 e' PINO CITADO como a 02, conferida contra o ADENDO 7) (D96: a ORDEM KIMI H0DN-02 e' PINO CITADO
~~~~

- **Justificativa:** A ORDEM 03 entra no contrato com a mesma forma da 02.
- **Apoio:** registros_h0dn_v410.py:90 (o molde).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 241 — linha 109 — PAR-01

- **Local:** linha 109, texto_h0dn['estatuto']
- **Origem:** g4:9 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
[OPEN] o certificado de poder: " + DL.FRASE_H0DN_PODER_PT + ". H0DN x BG1: "
~~~~

Trecho novo:

~~~~text
[OPEN] o certificado de poder: " + DL.FRASE_H0DN_PODER_COM_RETORNO_PT + ". H0DN x BG1: "
~~~~

- **Justificativa:** O estatuto do registro dizia o certificado pendente sem dizer que a ordem voltou com a recusa.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 242 — linha 115 — PAR-01

- **Local:** linha 115, texto_h0dn['escopo']: o retorno DEPOIS da frase que diz o que a ORDEM 02 manda
- **Origem:** g4:10 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a ORDEM KIMI H0DN-02 (pino citado por sha256, nao embutida) manda fechar a covariancia fisica e entregar o certificado de poder as cegas, sem o vetor observado; a funcao de veredito congelada nao muda. "
~~~~

Trecho novo:

~~~~text
a ORDEM KIMI H0DN-02 (pino citado por sha256, nao embutida) manda fechar a covariancia fisica e entregar o certificado de poder as cegas, sem o vetor observado; " + DL.FRASE_H0DN_RETORNO_PT + " (a ORDEM KIMI H0DN-03 tambem e' pino citado por sha256, nao embutida); a funcao de veredito congelada nao muda. "
~~~~

- **Justificativa:** No escopo a ordem do tempo é: a regra, o que a ORDEM 02 manda, o retorno. O retorno vai depois do “manda”, para não ler como se a ordem ainda estivesse a caminho.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 243 — linha 121 — PAR-01

- **Local:** linha 121, texto_h0dn['o_que_falta'][3]
- **Origem:** g4:11 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
" + DL.FRASE_H0DN_PODER_PT + " [OPEN; ORDEM KIMI H0DN-02, pino citado: sha256 " + DL.H0DN_ORDEM02["sha256"] + ", " + str(DL.H0DN_ORDEM02["bytes"]) + " bytes; o teste segue " + Q + "]"]
~~~~

Trecho novo:

~~~~text
" + DL.FRASE_H0DN_PODER_COM_RETORNO_PT + " [OPEN; ORDEM KIMI H0DN-02, pino citado: sha256 " + DL.H0DN_ORDEM02["sha256"] + ", " + str(DL.H0DN_ORDEM02["bytes"]) + " bytes; ORDEM KIMI H0DN-03, pino citado: sha256 " + DL.H0DN_ORDEM03["sha256"] + ", " + str(DL.H0DN_ORDEM03["bytes"]) + " bytes; o teste segue " + Q + "]"]
~~~~

- **Justificativa:** O item do que falta diz o retorno e pina a ordem seguinte ao lado da 02.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o sha256 inteiro da ORDEM 03 passa a aparecer no texto do registro e, por ele, na seção do README (pos_rito\textos_v410.py, falta): o harness precisa conhecê-lo (item 40)

#### Item 244 — linha 122 — PAR-01

- **Local:** linha 122, texto_h0dn['ressalvas'][1]
- **Origem:** g4:12 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
Q + ": " + DL.FRASE_H0DN_PODER_PT + " ([INPUT, D96], ordem do operador de 10/11; E34)"
~~~~

Trecho novo:

~~~~text
Q + ": " + DL.FRASE_H0DN_PODER_PT + " ([INPUT, D96], ordem do operador de 10/11; E34); " + DL.FRASE_H0DN_RETORNO_PT
~~~~

- **Justificativa:** A etiqueta ([INPUT, D96]; E34) é só da frase do poder; o retorno vem depois dela, com o estatuto próprio que a frase já traz.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 245 — linha 128 — PAR-01

- **Local:** linha 128, texto_h0dn['limites'][1]
- **Origem:** g4:13 (g4_h0dn). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
): " + DL.FRASE_H0DN_PODER_PT + "; o limiar de poder e' do operador e nao esta' decidido"
~~~~

Trecho novo:

~~~~text
): " + DL.FRASE_H0DN_PODER_COM_RETORNO_PT + "; o limiar de poder e' do operador e nao esta' decidido"
~~~~

- **Justificativa:** Mesmo acréscimo no limite que repete a frase do poder.
- **Apoio:** ORDEM_KIMI_H0DN_03_10nov.md (fora da pasta kimi; sha256 17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f, 5221 bytes, lidos agora por script): l.4 “Tipo: ESTUDO DE DESENHO, não certificado. Sem dado observado”; l.9 (§0) nenhuma variante admitida, poder não avaliável, “A recusa de certificar está certa e fica”; l.23 “O certificado continua recusado até haver variante admitida”. D96: delta_v410.py:967-971 e DESENHO_v410_ADENDO_3 (teste sem poder preditivo discriminante não se abre).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 246 — linha 138 — PAR-01

- **Local:** linha 138, texto_h0dn['extras']: as frases e o pino no registro do core
- **Origem:** g4:14 (g4_h0dn). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"poder_pt": DL.FRASE_H0DN_PODER_PT, "poder_en": DL.FRASE_H0DN_PODER_EN, "ordem_kimi_02": dict(DL.H0DN_ORDEM02, citado_nao_embutido=True, em_rito_nada_e_lido=True),
~~~~

Trecho novo:

~~~~text
"poder_pt": DL.FRASE_H0DN_PODER_PT, "poder_en": DL.FRASE_H0DN_PODER_EN, "ordem_kimi_02": dict(DL.H0DN_ORDEM02, citado_nao_embutido=True, em_rito_nada_e_lido=True), "retorno_pt": DL.FRASE_H0DN_RETORNO_PT, "retorno_en": DL.FRASE_H0DN_RETORNO_EN, "ordem_kimi_03": dict(DL.H0DN_ORDEM03, citado_nao_embutido=True, em_rito_nada_e_lido=True),
~~~~

- **Justificativa:** O registro do core passa a trazer o retorno e o pino da ORDEM 03 (o pós-rito os lê de lá).
- **Apoio:** runtime_h0dn_v410.py:220 (out_.update(t_['extras'])).
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - o registro h0dn_bg1_v410 ganha 3 chaves no core: ESPERADOS (chaves e hashes do registro) muda; nenhuma chave antiga muda

### Arquivo `registros_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\registros_v410.py`. Fim de linha: LF. Itens: 247, 248, 249, 250, 251.

#### Item 247 — linha 65 — EP-01, PAR-01 — redigido pelo crítico

- **Local:** linha 65 (NAO_PINADOS: os adendos citados só por sha16)
- **Origem:** g1:25, g4:3, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md": DL.ADENDO6_SHA16}
~~~~

Trecho novo:

~~~~text
"DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md": DL.ADENDO6_SHA16, "DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md": DL.ADENDO7_SHA16}
~~~~

- **Justificativa:** O ADENDO 7 passa a ser citado por sha16 (D106, D108, E38): entra na lista, como os adendos 2 a 6.
- **Apoio:** g1 item 25 (efeito); conferência do g4 (faltou)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético

#### Item 248 — linha 263 — EP-01, R3-MEDIO

- **Local:** linha 263, o sufixo do veredito de cunhagens_v410 (a errata nova)
- **Origem:** g1:42 (g1_ratificacao). **Língua:** EN. **Ocorrências:** 1

Trecho atual:

~~~~text
__DECISIONS_%s__ERRATUM_E37_BESIDE__
~~~~

Trecho novo:

~~~~text
__DECISIONS_%s__ERRATUM_E38_BESIDE__ERRATUM_E37_BESIDE__
~~~~

- **Justificativa:** O veredito lista as erratas ao lado; a E38 entra à frente, no padrão.
- **Apoio:** delta (ERRATA_E38)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - ESPERADOS e os controles comparam o veredito por igualdade com o que o registro monta: regerados

#### Item 249 — linha 264 — EP-01

- **Local:** linha 264, estatuto de cunhagens_v410 (a lista dos temas das falas)
- **Origem:** g1:43 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
a ratificacao dos nomes novos e a regra do nome, 10/11, D101; os nomes das declaracoes RATIFICADOS em 09/11, D74;
~~~~

Trecho novo:

~~~~text
a ratificacao dos nomes novos e a regra do nome, 10/11, D101; o quarto nome (a ressurreicao do sinal) e o observador que e' a escala, 10/11, D108; os nomes das declaracoes RATIFICADOS em 09/11, D74;
~~~~

- **Justificativa:** A lista dos temas ganha a fala 29.
- **Apoio:** fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 250 — linha 284 — V1

- **Local:** spec das erratas, entrada da E36, campo lacuna_de_fidelidade (l.284)
- **Origem:** g2:5 (g2_tetelestai_e_limiar). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
sem a hipotese s >= 0 a desigualdade e' falsa para b > 1/2 (contraexemplo no recibo do autor da R5)"
~~~~

Trecho novo:

~~~~text
sem a hipotese s >= 0 a desigualdade pode falhar: para b > 1/2 a constante do limiar e' negativa e o limiar pode ser negativo, e quando ele e' negativo a clausula pode falhar (contraexemplo no recibo do autor da R5); o kernel nao traz teorema de necessidade"
~~~~

- **Justificativa:** O arquivo não estava na lista de fontes, mas repete à mão o trecho velho da E36; sem acompanhar, a frase reprovada volta ao candidato pelo spec das erratas.
- **Apoio:** os mesmos do item 3
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - achado por Grep (“falsa para b”) fora da lista de fontes da ordem
  - regenerar pelo construtor (nao editar a mao): um_v410_candidato.py, CANDIDATO_v410.json, ESPERADOS_v410.json, v410_pins.py, GUARDA_FRASES_v410.json, PREPARACAO_v410_PRONTA.json (readme_evidente), pos_rito\CUSTODIA_v410_RASCUNHO.txt, dry_v410\*

#### Item 251 — linha 288 — EP-01, R3-MEDIO

- **Local:** linhas 286-288: a entrada da E38 na lista de erratas de cunhagens_v410, depois da entrada da E37
- **Origem:** g1:44 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
             "estatuto": "[INPUT: a fala do operador de 10/11 (D101); REAL: os termos no kernel e o recibo do autor da R5 (compilacao no trio, sem sorry); DECLARADO: os dois auxiliares da autoria; ONTO: que o ato de nomear seja o zero modular da inscricao da permanencia]", "assinatura": ASSINA},
~~~~

Trecho novo:

~~~~text
             "estatuto": "[INPUT: a fala do operador de 10/11 (D101); REAL: os termos no kernel e o recibo do autor da R5 (compilacao no trio, sem sorry); DECLARADO: os dois auxiliares da autoria; ONTO: que o ato de nomear seja o zero modular da inscricao da permanencia]", "assinatura": ASSINA},
            {"ao_lado_de": "a preparacao da v410 (a frase da ratificacao dos nomes novos, o texto da D101, a errata E37, o registro a_escala_v410, a linha do .md, o artigo PT/EN e os textos do pos-rito) e o cabecalho da pedra AEscala R5", "dizia": "que a fala de 10/11 da D101 ratificara quatro nomes da clausula do Tetelestai, e 22 nomes novos ao todo.", "agora": DL.ERRATA_E38,
             "lacuna_de_fidelidade": "a gerencia contou pelo recibo do autor da R5 (quatro teoremas) e nao pelo ADENDO 6 (tres nomes, os apresentados ao operador antes da fala); o quarto teorema so' foi dito a ele depois da fala; a revisao de terceiro R3 e o painel independente o acharam (D106); o operador deu o nome do teorema em 10/11 (D108)",
             "estatuto": "[REAL: o ADENDO 6, o transcrito da sessao da gerencia e a pedra AEscala R6 no kernel deste rito (so' o identificador muda; enunciado e prova nao); INPUT: a fala do operador de 10/11 que da' o nome (D108); DECLARADO: os dois auxiliares da autoria; dicionario: que o termo seja a ressurreicao do sinal e' leitura do operador]", "assinatura": ASSINA},
~~~~

- **Justificativa:** A lista de erratas do registro das cunhagens ganha a E38, no formato das vizinhas (ao lado de; dizia; agora; lacuna de fidelidade; estatuto; assinatura).
- **Apoio:** ADENDO 6 l.7; insumos\RECIBO_AESCALA_R5_10nov.json; fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a contagem de erratas do registro sobe de um (conferir no ensaio e em gerar_esperados se algum controle a digita)
  - ASSINA (delta l.1071) diz “06 e 09/11/2026”; as erratas E33 a E38 são de 10/11: é de outro grupo ou do construtor

### Arquivo `runtime_aescala_v410.py`

Caminho: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\runtime_aescala_v410.py`. Fim de linha: LF. Itens: 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274.

#### Item 252 — linha 5 — EP-01

- **Local:** linha 5 (comentario do cabecalho)
- **Origem:** g1:36 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
foram RATIFICADOS pelo operador em 10/11/2026 (D101), salvo os dois lemas auxiliares da autoria, que ficam [DECLARADO pela autoria].
~~~~

Trecho novo:

~~~~text
foram RATIFICADOS pelo operador em 10/11/2026 (D101), salvo o quarto teorema da clausula do Tetelestai, NOMEADO por ele em fala posterior do mesmo dia (D108: ressurreicao_do_sinal), e os dois lemas auxiliares da autoria, que ficam [DECLARADO pela autoria].
~~~~

- **Justificativa:** O comentário vai embutido no um.py e dizia todos os nomes novos ratificados, salvo os dois auxiliares.
- **Apoio:** ADENDO 6 l.7; fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 253 — linha 7 — V3

- **Local:** comentário do cabeçalho (l.7)
- **Origem:** g2:25 (g2_tetelestai_e_limiar). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
o par da matriz-S, a constante independente do tamanho, a reconstrucao, o controle negativo e o contraexemplo da hipotese s >= 0); c8 tambem confere,
~~~~

Trecho novo:

~~~~text
o par da matriz-S (identidade), a constante independente do tamanho (identidade aritmetica), a reconstrucao (a mesma desigualdade, lida em norma, com as hipoteses de tempo), o controle negativo e o contraexemplo da hipotese s >= 0; o conteudo independente e' UMA desigualdade em tres instancias, as condicoes sobre o beta de runtime (0 < beta < 1, s* >= 0 e beta <= 1/2), o controle negativo e o contraexemplo); c8 tambem confere,
~~~~

- **Justificativa:** Comentário que descreve a c13; acompanha o item 24.
- **Apoio:** os mesmos do item 23
- **Decisão do crítico:** fico com a correção do cético: a enumeração do “conteúdo independente” da c13 era exaustiva e estava incompleta; o subitem (vi) também testa t ≥ n·ln 2/2, que equivale a β de runtime ≤ ½ e pode falhar (runtime_aescala_v410.py:58, conferido nesta consolidação: t2 = s*/2 ≥ n·ln 2/2 ⟺ a constante ≥ 0 ⟺ β ≤ ½), e o subitem (i) testa 0 < β < 1 e s* ≥ 0 (linha 51)
- **Efeitos colaterais:**
  - o arquivo é embutido no candidato: regenerar

#### Item 254 — linha 8 — EP-01

- **Local:** linha 8 (comentario: o que a c5 e a c11 conferem)
- **Origem:** g1:37 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
c5 as falas 27 e 28; c11 a ratificacao D101 (a fala por sha256 == o pino == o cabecalho da pedra) e os dois auxiliares pendentes
~~~~

Trecho novo:

~~~~text
c5 as falas 27, 28 e 29; c11 a ratificacao D101 e a nomeacao D108 (cada fala por sha256 == o pino == o cabecalho da pedra) e os dois auxiliares pendentes
~~~~

- **Justificativa:** Acompanha a c5 e a c11 novas.
- **Apoio:** itens da c5 e da c11
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - l.107: c5_ok_ exige também c_["chave_nomeacao_d108"] in ver_; o comentário “(R5: as falas 27 e 28 entre as do registro)” ganha a 29

#### Item 255 — linha 28 — EP-01

- **Local:** linha 28 (docstring: a lista dos teoremas da clausula)
- **Origem:** g1:38 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
beta_e_o_operador_modular_do_tetelestai; a_informacao_completa_se_reconstroi;
~~~~

Trecho novo:

~~~~text
beta_e_o_operador_modular_do_tetelestai; ressurreicao_do_sinal;
~~~~

- **Justificativa:** A única ocorrência do identificador velho no runtime embutido.
- **Apoio:** pedra\AEscala.lean:1169
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - Grep: é a única ocorrência em runtime_aescala_v410.py; registros, .pysnip, gerar_candidato, gerar_relatorio e pos_rito não digitam o identificador (leem do delta)

#### Item 256 — linha 29 — V3

- **Local:** docstring da função que calcula a cláusula (l.29-30)
- **Origem:** g2:26 (g2_tetelestai_e_limiar). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
o par da matriz-S (sen^2 = beta, cos^2 = 1 - beta); a constante nao depende do tamanho; a reconstrucao em
    norma ao quadrado; o controle negativo (uma oitava a menos viola a desigualdade no adversario); o contraexemplo de s < 0.
~~~~

Trecho novo:

~~~~text
o par da matriz-S (sen^2 = beta, cos^2 = 1 - beta: identidade); a constante nao depende do tamanho (identidade aritmetica); a reconstrucao em
    norma ao quadrado (a mesma desigualdade, lida em norma, com as duas hipoteses de tempo do teorema); o controle negativo (uma oitava a menos viola a desigualdade no adversario); o contraexemplo de s < 0.
    O conteudo independente e' UMA desigualdade em tres instancias, as condicoes sobre o beta de runtime (0 < beta < 1, s* >= 0 e, pela primeira hipotese de tempo da reconstrucao, beta <= 1/2), o controle negativo e o contraexemplo.
~~~~

- **Justificativa:** Docstring que descreve a c13; acompanha o item 24. Acrescenta uma linha à docstring.
- **Apoio:** os mesmos do item 23
- **Decisão do crítico:** fico com a correção do cético: a enumeração do “conteúdo independente” da c13 era exaustiva e estava incompleta; o subitem (vi) também testa t ≥ n·ln 2/2, que equivale a β de runtime ≤ ½ e pode falhar (runtime_aescala_v410.py:58, conferido nesta consolidação: t2 = s*/2 ≥ n·ln 2/2 ⟺ a constante ≥ 0 ⟺ β ≤ ½), e o subitem (i) testa 0 < β < 1 e s* ≥ 0 (linha 51)
- **Efeitos colaterais:**
  - a l.28 da mesma docstring cita a_informacao_completa_se_reconstroi: a troca do identificador é do grupo dos nomes
  - o arquivo é embutido no candidato: regenerar

#### Item 257 — linha 55 — V3

- **Local:** comentário do subitem (iv) (l.55)
- **Origem:** g2:27 (g2_tetelestai_e_limiar). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
# (iv) o par da matriz-S: |R|^2 = beta, |T|^2 = 1 - beta; |T|^2 Z <= numero de solucoes; o residuo <= |R|^2 Z
~~~~

Trecho novo:

~~~~text
# (iv) [identidade: sen^2 e cos^2 de arcsen(raiz de beta); as duas desigualdades sao as de (ii) com outro rotulo] o par da matriz-S: |R|^2 = beta, |T|^2 = 1 - beta; |T|^2 Z <= numero de solucoes; o residuo <= |R|^2 Z
~~~~

- **Justificativa:** Comentário do subitem; o código da linha não muda.
- **Apoio:** runtime_aescala_v410.py:52 e :54-55
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 258 — linha 57 — EP-04, V3

- **Local:** comentário do subitem (v) (l.57)
- **Origem:** g2:28 (g2_tetelestai_e_limiar). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
# (v) a constante alem das m oitavas e' a mesma para todo m
~~~~

Trecho novo:

~~~~text
# (v) [identidade aritmetica: nao pode falhar; na pedra, o item 9 e' fechado por ring] a constante alem das m oitavas e' a mesma para todo m
~~~~

- **Justificativa:** Comentário do subitem; o código da linha não muda.
- **Apoio:** runtime_aescala_v410.py:57; pedra\AEscala.lean:1147-1148 e :1155
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 259 — linha 58 — V3

- **Local:** comentário do subitem (vi) (l.58)
- **Origem:** g2:29 (g2_tetelestai_e_limiar). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
# (vi) a reconstrucao: em norma ao quadrado, (Z(2t) - n_sol)/|X| <= (beta/(1 - beta)) n_sol/|X| (o quadrado da cota)
~~~~

Trecho novo:

~~~~text
# (vi) [a mesma desigualdade de (ii), lida em norma: (Z - N) <= (beta/(1 - beta)) N equivale a (1 - beta) Z <= N; as duas condicoes de tempo sao as hipoteses do teorema: a primeira equivale a beta de runtime <= 1/2, a segunda e' identidade] a reconstrucao: em norma ao quadrado, (Z(2t) - n_sol)/|X| <= (beta/(1 - beta)) n_sol/|X| (o quadrado da cota)
~~~~

- **Justificativa:** Comentário do subitem; o código da linha não muda.
- **Apoio:** runtime_aescala_v410.py:52 e :58 (mesma instância com2_, mesmo tempo 2·t2_ = s*)
- **Decisão do crítico:** fico com a correção do cético: a enumeração do “conteúdo independente” da c13 era exaustiva e estava incompleta; o subitem (vi) também testa t ≥ n·ln 2/2, que equivale a β de runtime ≤ ½ e pode falhar (runtime_aescala_v410.py:58, conferido nesta consolidação: t2 = s*/2 ≥ n·ln 2/2 ⟺ a constante ≥ 0 ⟺ β ≤ ½), e o subitem (i) testa 0 < β < 1 e s* ≥ 0 (linha 51)

#### Item 260 — linha 78 — EP-01, R3-MEDIO

- **Local:** linha 78 (docstring da funcao: a descricao da c11)
- **Origem:** g1:39 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
ditos RATIFICADOS em 10/11/2026 (D101: a fala 28 por sha256 == o pino == o cabecalho da pedra; a regra do nome), os dois auxiliares da autoria ditos [DECLARADO pela autoria] e unicos pendentes;
~~~~

Trecho novo:

~~~~text
os ratificados ditos RATIFICADOS em 10/11/2026 (D101: a fala 28 por sha256 == o pino == o cabecalho da pedra; a regra do nome), o quarto teorema da clausula do Tetelestai dito NOMEADO pelo operador (D108: a fala 29 por sha256 == o pino == o cabecalho da pedra; o nome de trabalho da R5 nao e' declaracao na pedra), os dois auxiliares da autoria ditos [DECLARADO pela autoria] e unicos pendentes;
~~~~

- **Justificativa:** A docstring dizia todos os nomes novos ditos ratificados.
- **Apoio:** itens da c11
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok

#### Item 261 — linha 107 — EP-01 — redigido pelo crítico

- **Local:** linha 107 (c5)
- **Origem:** g1:37, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
and c_["chave_clausula_tetelestai"] in ver_   # (R5: as falas 27 e 28 entre as do registro)
~~~~

Trecho novo:

~~~~text
and c_["chave_clausula_tetelestai"] in ver_ and c_["chave_nomeacao_d108"] in ver_   # (R5: as falas 27 e 28 entre as do registro; R6, D108: a fala 29)
~~~~

- **Justificativa:** A c5 passa a exigir a fala 29 entre as do registro.
- **Apoio:** g1 item 37 (efeito)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - código não executado

#### Item 262 — linha 167 — D108, OBS-1 — redigido pelo crítico

- **Local:** antes da linha 167 (c8: o controle novo da finura)
- **Origem:** g6:16, critico (g6_a_finura_e_o_observador). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_ and "validade no kernel" in txt_ws_
~~~~

Trecho novo:

~~~~text
    # (R6, D108) a FINURA DA LEITURA: a frase de limite nova e' uma folha EXATA da lista limites, logo depois de uma folha que traz a clausula do limite; a forma EN esta' no texto; e toda folha do registro que traz a metade [REAL] da frase traz a clausula do limite na MESMA folha (as excecoes: a propria folha dos limites e as frases soltas dos extras)
    fin_pt_ = ws_(c_["frase_finura_pt"]); fin_en_ = ws_(c_["frase_finura_en"]); fin_real_pt_ = ws_(c_["frase_finura_real_pt"]); lim_ws_ = [ws_(x_) for x_ in t_["limites"]]
    sem_fin_ = sorted(cam_ for cam_, x_ in folhas_ if fin_real_pt_ in x_ and clz_pt_ not in x_ and x_ != fin_pt_ and not cam_.startswith(".extras.frase_finura"))
    finura_ok_ = bool(fin_pt_ in lim_ws_ and lim_ws_.index(fin_pt_) > 0 and clz_pt_ in lim_ws_[lim_ws_.index(fin_pt_) - 1] and fin_en_ in txt_ws_ and not sem_fin_)
    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_ and "validade no kernel" in txt_ws_
~~~~

- **Justificativa:** O controle (a) do g6:16, tornado obrigatório pelo cético: a frase nova enuncia o limiar de tempo dos dois teoremas em palavras que os controles de anúncio não reconhecem; sem ele, nada impede que uma superfície do registro leve a frase sem a cláusula do limite ao lado.
- **Apoio:** g6 item 16 (a) e a conferência do g6, item 16; runtime_aescala_v410.py:133-149 (folhas_, ws_, clz_pt_)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - depende das chaves frase_finura_pt, frase_finura_en e frase_finura_real_pt do contrato (item do g6:8) e da folha do item do g6:7
  - código não executado: o construtor confere no ensaio

#### Item 263 — linha 167 — D108, OBS-1 — redigido pelo crítico

- **Local:** linha 167 (c8: o fecho)
- **Origem:** g6:16, critico (g6_a_finura_e_o_observador). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
and clausula_ok_ and clausula_r5_ok_
~~~~

Trecho novo:

~~~~text
and clausula_ok_ and clausula_r5_ok_ and finura_ok_
~~~~

- **Justificativa:** O controle da finura entra no resultado da c8.
- **Apoio:** g6 item 16 (a)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - código não executado

#### Item 264 — linha 178 — EP-01 — INSTRUÇÃO; redigido pelo crítico

- **Local:** comentários e docstrings que repetem a forma velha (não vão ao texto público, mas vão embutidos no um.py)
- **Origem:** g1:9, g1:40, g5:26, critico (g1_ratificacao). **Língua:** INSTRUCAO_DE_CODIGO

Instrução:

~~~~text
Trocar, nos comentários das linhas 178 e 230 de runtime_aescala_v410.py, “RATIFICADOS em 10/11 (D101), salvo os dois auxiliares da autoria, pendentes” por “RATIFICADOS em 10/11 (D101), salvo o quarto teorema da clausula, NOMEADO pelo operador (D108), e os dois auxiliares da autoria, pendentes”; no delta, os comentários das linhas 231, 233, 241 e 242 (“os dados pela gerencia na R5”) por “os tres apresentados ao operador antes da fala; o quarto, nomeado por ele (D108)”; a linha 476 (“as falas 27 e 28”) e a 361 já têm item; os comentários “38 ancoras” das linhas 167 e 632 do delta ficam sem número, como o da linha 220 (item do g5:26).
~~~~

- **Justificativa:** São comentários; não mudam texto público nem controle. Ficam listados para o construtor não deixar a forma velha no código embutido.
- **Apoio:** g1 item 9 (efeitos), item 40 (justificativa); conferências do g1 e do g5 (faltou)
- **Decisão do crítico:** INSTRUÇÃO (não é troca exata): depende de insumo que ainda não existe ou de escolha do construtor; o critério está dito

#### Item 265 — linha 190 — EP-01, R3-MEDIO

- **Local:** linhas 178-197: a checagem c11 (a logica, em prosa) e o comentario da linha 190
- **Origem:** g1:40 (g1_ratificacao). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
# (R5, D101) a ratificacao de 10/11: os 22 nomes e os 3 campos RATIFICADOS (declaracoes na pedra), os 2 auxiliares pendentes (declaracoes na pedra, [DECLARADO pela autoria], nunca ratificados), a fala 28 embutida por sha256 == o pino == o cabecalho da pedra, a regra do nome no texto, e NUNCA o estatuto antigo
~~~~

Trecho novo:

~~~~text
# (R5, D101; R6, D108) a ratificacao de 10/11: os nomes ratificados e os campos RATIFICADOS (declaracoes na pedra; o numero e' o do contrato, nunca digitado), o quarto teorema da clausula NOMEADO pelo operador (declaracao na pedra com o nome dele; a fala 29 embutida por sha256 == o pino == o cabecalho da pedra; o nome de trabalho da R5 NAO e' declaracao na pedra), os auxiliares pendentes (declaracoes na pedra, [DECLARADO pela autoria], nunca ratificados), a fala 28 embutida por sha256 == o pino == o cabecalho da pedra, a regra do nome no texto, e NUNCA o estatuto antigo
~~~~

- **Justificativa:** A c11 conferia que ratificados ∪ pendentes = nomes novos e que os teoremas da R5 estavam todos entre os ratificados (o que consagrava os quatro). O que muda, em prosa: (1) nomes_ratificados_d101 ∪ nomes_nomeados_d108 ∪ nomes_pendentes == nomes_novos_da_pedra, as três classes disjuntas; (2) set(teoremas_r5) <= ratificados ∪ nomeados (l.195); (3) cada nomeado é declaração na pedra (rx_decl_) e o nome de trabalho NÃO é (rx_decl_ falso para ele): o controle negativo; (4) a fala 29: o texto embutido tem o sha256 do contrato (nomeacao_d108), traz o trecho «o quarto nome=ressureiçãodosinal», o sha256 está no corpo da pedra e o corpo traz “NOMEADO pelo operador”; (5) o texto do registro traz a frase PT e a EN (já exigido) e “NOMEADO pelo operador em 10/11/2026”; (6) nenhum nomeado e nenhum pendente em nomes_ratificados_d101. A l.178 (“---- c11 os nomes RATIFICADOS (D87) e os nomes NOVOS da pedra (R3, R4 e R5): RATIFICADOS em 10/11 (D101), salvo os dois auxiliares da autoria, pendentes”) e a l.230 (o mesmo texto na docstring) passam a dizer “… RATIFICADOS em 10/11 (D101), salvo o quarto teorema da clausula, NOMEADO pelo operador (D108), e os dois auxiliares da autoria, pendentes”.
- **Apoio:** pedra\AEscala.lean:37-41 (o cabeçalho novo traz “NOMEADO pelo operador” e a lista das falas traz o sha256 da fala 13) e :1169 (a declaração com o nome novo)
- **Decisão do crítico:** o comentário fica; a lógica da c11 que o redator descreveu em prosa (seis pontos) virou cinco itens exatos do crítico em runtime_aescala_v410.py (não executados)
- **Efeitos colaterais:**
  - values_ (l.217): ratificacao_d101 ganha ao lado "nomeacao_d108": {"ok", "fala_sha256", "nomeados", "n_nomeados_declarados", "nome_de_trabalho_declarado": False}; gerar_esperados l.265, ensaio l.2721 e conferir l.278 leem ratificacao_d101 e ganham o par
  - ensaio_a_seco_v410.py l.2955-2979: os controles negativos da c11 (o sha256 da fala 28 trocado; o estatuto antigo plantado; a frase da D101 retirada) seguem valendo; cabem dois novos: o sha256 da fala 29 trocado no pino e o nome de trabalho posto em nomes_nomeados_d108, ambos com recusa na c11
  - o contrato do runtime precisa do nome de trabalho para o controle negativo: chave "nome_de_trabalho_do_quarto": DL.NOME_DE_TRABALHO_DO_QUARTO_AESCALA (registro; não entra em texto público)

#### Item 266 — linha 194 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 194 (c11: as classes de nomes novos)
- **Origem:** g1:40, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
set(c_["nomes_ratificados_d101"]) | set(c_["nomes_pendentes"]) == set(c_["nomes_novos_da_pedra"]) and not (set(c_["nomes_ratificados_d101"]) & set(c_["nomes_pendentes"]))
~~~~

Trecho novo:

~~~~text
set(c_["nomes_ratificados_d101"]) | set(c_["nomes_nomeados_d108"]) | set(c_["nomes_pendentes"]) == set(c_["nomes_novos_da_pedra"]) and not (set(c_["nomes_ratificados_d101"]) & set(c_["nomes_pendentes"])) and not (set(c_["nomes_nomeados_d108"]) & (set(c_["nomes_ratificados_d101"]) | set(c_["nomes_pendentes"])))
~~~~

- **Justificativa:** Ponto (1) da descrição do g1:40: três classes, disjuntas, que cobrem os nomes novos da pedra.
- **Apoio:** g1 item 40 (justificativa, ponto 1)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - código não executado

#### Item 267 — linha 195 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 195 (c11: os teoremas da R5)
- **Origem:** g1:40, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
set(c_["teoremas_r5"]) <= set(c_["nomes_ratificados_d101"]) and set(c_["auxiliares_r5"])
~~~~

Trecho novo:

~~~~text
set(c_["teoremas_r5"]) <= (set(c_["nomes_ratificados_d101"]) | set(c_["nomes_nomeados_d108"])) and set(c_["auxiliares_r5"])
~~~~

- **Justificativa:** Ponto (2) da descrição do g1:40.
- **Apoio:** g1 item 40 (justificativa, ponto 2)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - código não executado

#### Item 268 — linha 198 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** antes da linha 198 (c11: o bloco novo da nomeação)
- **Origem:** g1:40, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
    c11_ok_ = (len(decl_) == c_["n_nomes"] == len(c_["nomes"])
~~~~

Trecho novo:

~~~~text
    # (R6, D108) a NOMEACAO do quarto teorema: o nomeado e' declaracao na pedra e o nome de trabalho da R5 NAO e' (o controle negativo); a fala 29 embutida por sha256 == o pino == o cabecalho da pedra, com o trecho citado; a pedra e o registro o dizem NOMEADO pelo operador; nenhum nomeado entre os ratificados nem entre os pendentes
    nd_ = c_["nomeacao_d108"]; rv3_ = _V410_VERBATINS2.get(c_["chave_nomeacao_d108"]) or {}; txt3_ = str(rv3_.get("text", ""))
    nom_decl_ = {n_: rx_decl_(n_) for n_ in c_["nomes_nomeados_d108"]}
    nom_d108_ok_ = bool(rv3_.get("sha256") == nd_["sha256"] and _h410.sha256(txt3_.encode("utf-8")).hexdigest() == nd_["sha256"] and nd_["trecho"] in txt3_ and nd_["sha256"] in body_ws_ and "NOMEADO pelo operador" in body_ws_ and nd_["decisao"] == "D108"
                        and len(nom_decl_) == 1 and all(nom_decl_.values()) and not rx_decl_(c_["nome_de_trabalho_do_quarto"]) and c_["nome_de_trabalho_do_quarto"] not in c_["nomes_novos_da_pedra"]
                        and not (set(c_["nomes_nomeados_d108"]) & set(c_["nomes_ratificados_d101"])) and not (set(c_["nomes_nomeados_d108"]) & set(c_["nomes_pendentes"]))
                        and ws_(c_["estatuto_do_nome_nomeado_d108"]) in txt_ws_ and ws_(nd_["trecho"]) in txt_ws_)
    c11_ok_ = (len(decl_) == c_["n_nomes"] == len(c_["nomes"])
~~~~

- **Justificativa:** Pontos (3) a (6) da descrição do g1:40: o nomeado é declaração e o nome de trabalho não é; a fala 29 por sha256 no contrato, no texto embutido e no corpo da pedra; “NOMEADO pelo operador” na pedra e no registro.
- **Apoio:** g1 item 40 (justificativa, pontos 3 a 6); runtime_aescala_v410.py:179 (rx_decl_ só casa em início de linha), :191-193 (o molde da fala 28)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - depende do item do g1:1 (o cabeçalho da pedra traz “NOMEADO pelo operador”), do g1:4 (o sha256 da fala 29 na lista das falas da pedra), do g1:31 (as chaves do contrato) e do g1:32 (o estatuto no texto)
  - código não executado: o construtor confere no ensaio; cabem dois controles negativos novos (o sha256 da fala 29 trocado no pino; o nome de trabalho posto em nomes_nomeados_d108)

#### Item 269 — linha 199 — EP-01, R3-MEDIO — redigido pelo crítico

- **Local:** linha 199 (c11: o fecho)
- **Origem:** g1:40, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
and novos_ok_ and seis_ok_ and rat_d101_ok_)
~~~~

Trecho novo:

~~~~text
and novos_ok_ and seis_ok_ and rat_d101_ok_ and nom_d108_ok_)
~~~~

- **Justificativa:** A nomeação entra no resultado da c11 (a descrição pública do item do g1:41 só é verdadeira com isto).
- **Apoio:** g1 item 40 e a conferência do g1, item 40 (dependência do item 41)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - código não executado

#### Item 270 — linha 208 — EP-08

- **Local:** descricao da checagem c6 (l.208)
- **Origem:** g2:41 (g2_tetelestai_e_limiar). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
em n oitavas o fundo de n bits pesa 1/2^n", "ok": bool(c6_ok_)}
~~~~

Trecho novo:

~~~~text
em n oitavas um pixel de custo 1 brilha 1/2^n, o peso de um pixel na leitura de n bits", "ok": bool(c6_ok_)}
~~~~

- **Justificativa:** Mesma frase na descrição da c6; o código da checagem não muda.
- **Apoio:** pedra\AEscala.lean:859-860 (L.brilho 1 (n·ln 2) = 1 / |Fin n → Bool|) e :861-863 (|X| = 2^n); :968-969 (a leitura é Z/|X|); pedra\AEscala.lean:903 e :906 (item ii: Z(s) < número de soluções + 1 para s > n·ln 2; docstring l.894: “a flutuação do fundo já pesa menos que UM pixel de Nome”)
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a descrição vai ao core e aos ESPERADOS: regenerar

#### Item 271 — linha 210 — D108, OBS-1 — redigido pelo crítico

- **Local:** linha 210 (a descrição pública da c8)
- **Origem:** g6:16, critico (g6_a_finura_e_o_observador). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
nenhum numero de desempenho)", "ok": bool(c8_ok_)},
~~~~

Trecho novo:

~~~~text
nenhum numero de desempenho); a frase de limite da finura da leitura (D108) como folha da lista limites, logo depois de uma folha com a clausula do limite, e em EN no texto", "ok": bool(c8_ok_)},
~~~~

- **Justificativa:** A descrição da checagem passa a dizer o que ela confere a mais.
- **Apoio:** g6 item 16 (a)
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - a descrição vai ao core e aos ESPERADOS: regerar

#### Item 272 — linha 213 — EP-01, R3-MEDIO

- **Local:** linha 213, a descricao da c11 (vai ao core e ao artigo)
- **Origem:** g1:41 (g1_ratificacao). **Língua:** PT. **Ocorrências:** 1

Trecho atual:

~~~~text
e o registro os diz RATIFICADOS pelo operador em 10/11/2026 (D101: a fala por sha256 == o pino == o cabecalho da pedra; a regra do nome), nunca com o estatuto antigo; os %d auxiliares da autoria ditos [DECLARADO pela autoria], os unicos pendentes; os seis nomes de enunciado mudado ditos com a forma vigente (R2, B3; D101)" % (c_["n_nomes"], c_["n_nomes_novos"], len(c_["campos_novos_da_estrutura"]), len(c_["nomes_pendentes"])), "ok": bool(c11_ok_)},
~~~~

Trecho novo:

~~~~text
e o registro diz %d deles RATIFICADOS pelo operador em 10/11/2026 (D101: a fala por sha256 == o pino == o cabecalho da pedra; a regra do nome), nunca com o estatuto antigo; %d dito NOMEADO pelo operador em 10/11/2026 (D108: a fala por sha256 == o pino == o cabecalho da pedra; o nome de trabalho nao e' declaracao na pedra); os %d auxiliares da autoria ditos [DECLARADO pela autoria], os unicos pendentes; os seis nomes de enunciado mudado ditos com a forma vigente (R2, B3; D101)" % (c_["n_nomes"], c_["n_nomes_novos"], len(c_["campos_novos_da_estrutura"]), len(c_["nomes_ratificados_d101"]), len(c_["nomes_nomeados_d108"]), len(c_["nomes_pendentes"])), "ok": bool(c11_ok_)},
~~~~

- **Justificativa:** A descrição pública da checagem dizia os 24 nomes novos ditos ratificados. Passa a dizer quantos são ratificados, o nomeado e os pendentes, com os números do contrato.
- **Apoio:** ADENDO 6 l.7; fala 29
- **Decisão do crítico:** fica como o redator propôs; o cético deu ok
- **Efeitos colaterais:**
  - a descrição das checagens é gravada em ESPERADOS e no core; o artigo a cita pela etiqueta c11 (pysnip l.49)
  - rendida com os números de hoje: “… os 24 nomes NOVOS da pedra (e os 3 campos novos da estrutura): cada um e' declaracao na pedra embutida e o registro diz 21 deles RATIFICADOS … 1 dito NOMEADO pelo operador … os 2 auxiliares da autoria …”

#### Item 273 — linha 215 — EP-04, V3

- **Local:** descricao da checagem c13 (l.215)
- **Origem:** g2:24 (g2_tetelestai_e_limiar). **Língua:** DESCRICAO_DE_CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
o par da matriz-S (sen^2 = beta, cos^2 = 1 - beta; |T|^2 Z <= o numero de solucoes; o residuo <= |R|^2 Z); a constante e' a mesma para m = 1, 3, 8 oitavas; a reconstrucao em norma ao quadrado; o CONTROLE NEGATIVO (
~~~~

Trecho novo:

~~~~text
o par da matriz-S (sen^2 = beta, cos^2 = 1 - beta: identidade; |T|^2 Z <= o numero de solucoes e o residuo <= |R|^2 Z sao as mesmas desigualdades, com outro rotulo); a constante e' a mesma para m = 1, 3, 8 oitavas (identidade aritmetica: nao pode falhar); a reconstrucao em norma ao quadrado (a mesma desigualdade, lida em norma, com as duas hipoteses de tempo do teorema: a primeira equivale a beta de runtime <= 1/2; a segunda e' identidade); o conteudo independente e' UMA desigualdade em tres instancias (com solucao, de UMA solucao e adversaria) e as condicoes sobre o beta de runtime (0 < beta < 1, s* >= 0 e beta <= 1/2), mais os dois que seguem; o CONTROLE NEGATIVO (
~~~~

- **Justificativa:** Só a descrição da c13 (a string do campo descricao); o código da checagem não muda.
- **Apoio:** os mesmos do item 23
- **Decisão do crítico:** fico com a correção do cético: a enumeração do “conteúdo independente” da c13 era exaustiva e estava incompleta; o subitem (vi) também testa t ≥ n·ln 2/2, que equivale a β de runtime ≤ ½ e pode falhar (runtime_aescala_v410.py:58, conferido nesta consolidação: t2 = s*/2 ≥ n·ln 2/2 ⟺ a constante ≥ 0 ⟺ β ≤ ½), e o subitem (i) testa 0 < β < 1 e s* ≥ 0 (linha 51)
- **Efeitos colaterais:**
  - a descrição vai ao core (mechanics.checks) e aos ESPERADOS: regenerar; a guarda das frases passa também nas descrições (ensaio_a_seco_v410.py:2591 mostra o padrão para o H0DN)

#### Item 274 — linha 217 — EP-01, OBS-1 — redigido pelo crítico

- **Local:** linha 217 (values_: os dois blocos novos, antes de ratificacao_d101)
- **Origem:** g1:40, g6:16, critico (g1_ratificacao). **Língua:** CODIGO. **Ocorrências:** 1

Trecho atual:

~~~~text
"ratificacao_d101": {"ok": bool(rat_d101_ok_), 
~~~~

Trecho novo:

~~~~text
"nomeacao_d108": {"ok": bool(nom_d108_ok_), "fala_sha256": nd_["sha256"], "nomeados": list(c_["nomes_nomeados_d108"]), "n_nomeados_declarados": sum(1 for v_ in nom_decl_.values() if v_), "nome_de_trabalho_declarado": bool(rx_decl_(c_["nome_de_trabalho_do_quarto"]))}, "finura_d108": {"ok": bool(finura_ok_), "folhas_com_a_metade_real_sem_a_clausula_do_limite": sem_fin_}, "ratificacao_d101": {"ok": bool(rat_d101_ok_), 
~~~~

- **Justificativa:** Os valores medidos da nomeação (g1:40, efeito) e do controle da finura (g6:16).
- **Apoio:** g1 item 40 (efeito: values_) e g6 item 16
- **Decisão do crítico:** item redigido pelo crítico (junta itens de grupos ou torna exato um efeito colateral que o redator deixou em prosa); não passou por cético
- **Efeitos colaterais:**
  - gerar_esperados_v410.py l.265, ensaio_a_seco_v410.py l.2721 e conferir_rito_v410.py l.278 comparam os valores com ESPERADOS: regerar; se listarem as chaves à mão, ganham as duas
  - código não executado

## 9. Achados sem item, ou só em parte, com o motivo

- EP-04 (parte): nenhum texto diz que o limiar n·ln 2 + ln((1 − β)/β) é só suficiente; a D106 não pediu.
- EP-07 e V2(a) (parte): a ressalva de que para b ≥ ½ o fator √(b/(1 − b)) é ≥ 1 não entrou; a D106 não pediu.
- EP-06 (parte): a regex da guarda do anúncio (runtime_aescala_v410.py:144; pos_rito/leitura_v410.py:801) segue sem pegar “linear em n”; a folha foi consertada, a lacuna de cobertura fica (é código de checagem).
- V1, EP-02 e EP-08 nas docstrings da pedra fora da linha 1062 (l.1030, 1047-1048, 1130-1131, 856-858, 899-900): são do autor da R6; estão nas pendências.
- EP-03 (família vizinha): o rótulo curto “o teorema do Tetelestai” em descrições, comentários e mensagens (lista nas pendências).
- V3: o parágrafo do artigo que relata a c13 (artigo_pt_aescala_v410.pysnip:44-47 e o par EN) não ganhou a nota de que parte dos subitens é identidade; a decisão só pediu as descrições. E o subitem (v) da c13 segue sem poder falhar (só rotulado).
- PAR-03 (forma curta): “o vibrato sustenta a nota” segue como afirmação na moldura (delta_v410.py:723 e :725, frase obrigatória da c9), em registros_aescala_v410.py:133, gerar_relatorio_v410.py:304 e pos_rito/textos_v410.py:448.
- EP-05 (restos): pos_rito/registrar_mapa_v410.py:260 (“o leitor E' a escala … e a mentira lida como mentira e' verdade”, vai ao Mapa de Rotas), a moldura (delta 723, 725) e registros_aescala_v410.py:117 (dito como definição do dicionário).
- EP-10 (restos): a forma da D83 sem o rótulo novo em pos_rito/textos_v410.py:912, :1252, :1388; pos_rito/registrar_mapa_v410.py:260; gerar_relatorio_v410.py:304; textos_custodia_handoff_v410.py:193; registros_aescala_v410.py:111, :118, :136; e na docstring da pedra, l.602.
- R3-BAIXO-2 (restos): “no kernel.);” segue em gerar_candidato_v410.py:435, delta_v410.py:1028-1029 (ANUNCIO_TETELESTAI), registros_aescala_v410.py:79 e :94, gerar_relatorio_v410.py:425, pos_rito/textos_v410.py:1396 e :1409, textos_custodia_handoff_v410.py:127-128 e gerar_x_custodia_v410.py:54; a D106 só pediu o artigo (PT; o EN entrou pela regra do par).
- PAR-05 (resto): FRASE_D64_PT (delta_v410.py:705-706) sem o qualificador que a FRASE_D64_EN tem.
- PAR-11 (restos): «o que sou» (13 ocorrências; decisão A ou B da gerência); comentários de código e mensagens de assert com aspas angulares (delta 9, 364, 703, 772, 1025; runtime_v410.py; pos_rito), que não vão a público; o cabeçalho da pedra (l.15) e o recibo dos nomes, que trazem «A Escala» como palavras do operador.
- PAR-08 (restos): “accreditation” no G1 (fora da pasta do trabalho) e nas seções seladas do artigo EN; etiquetas da régua em português nos textos EN.
- PAR-09 (restos): na seção do H0DN, “K=E(z_ )^2β/3” e “Z=( h-log_10H_ bg)/σ_ nulo” no TXT (artigo_pt_h0dn_v410.pysnip:16 e o par EN; a escrita $K=E(z_{*})^{(2\beta/3)}$ rende certo, conferida pelo cético numa cópia do conversor); e o resto do artigo PT selado mistura ponto e vírgula nos decimais (não se toca). O conversor _tex_to_txt não muda.
- EP-12, item 1 (restos): a política do FLAGS, por_origem “aescala_nomeada: 85” e a lista bandeiras_de_constantes_geradas_pela_structure (17 nomes); “85 bandeiras” sem a composição no README item (2) e em pos_rito/textos_v410.py:911.
- OBS-16 e OBS-17 fora do README evidente (post, ARCO PT/EN, pos_rito/textos_v410.py:912 e :1388) e V4 no handoff (ESCALA_TIPO_PT/EN): decisão da gerência.
- OBS-15, PAR-01 e PAR-02 (restos): os textos do H0DN listados nas pendências (pos_rito/textos_v410.py:915, :527, :657, :1469; gerar_relatorio_v410.py:307, :309; o COMMIT; o conferidor do rito).
- OBS-1 (restos): a frase da finura fica fora da linha do .md canônico (gerar_candidato_v410.py:434-435), dos outros textos do handoff (ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO, COMMIT), de pos_rito/textos_v410.py e do rascunho da custódia: a ordem listou três superfícies (o README evidente da preparação ganhou as chaves).
- A errata dos consertos de texto que não são a contagem dos nomes (a E36 que muda de redação; o H0DN; as leituras): sem item em nenhum grupo; pendência.
- Os BAIXOS 3 e 4 da R3 (as três variantes da F59 e as sondas do Clay; a observação sobre (i) e (ii) do teorema): a própria revisora os deu como anotação, sem mudança (versão seguinte / nenhuma correção).
- Os 19 baixos e as 19 observações do painel que não estão na lista da ordem deste crítico (por exemplo as observações 2 a 14, 18 e 19): não vieram no material; ficam como ressalva escrita, pela D107 emendada.
- D109, D112, D113, D114 e as falas do operador posteriores às 15:54 (fala 30; “o observador está na escala da constante da luz”; “sem a escala não tem fita”; “tudo depende da escala”): fora do escopo da ordem; só o bloco condicional da D109 e as pendências as tratam. A seção 7 da pedra (D113) não tem nenhum item.
- Dois itens dos grupos não são itens de texto e saíram da lista: g1:50 e g1:51 (o redator só registrou que o arquivo muda pelo delta) e g1:61 (o inventário, que virou a seção O RENOMEAR).

## 10. Itens dos grupos que não foram levados como estavam

- **g1:10** — NAO LEVADO: virou instrução (insumo regerado pelo instalador da R6): ver o item de instrução do recibo dos nomes
- **g1:13** — NAO LEVADO: fundido com g6:1 e g6:2 num item só do crítico (a mesma âncora, linha 485): fica UMA constante para a segunda linha da fala (a linha inteira), sem a constante curta quase homônima
- **g1:14** — fundido em g2:32
- **g1:15** — fundido em g2:33
- **g1:24** — NAO LEVADO: reescrito pelo crítico: D106 e D107 com as correções do cético; a D108 vira UM item só, com a segunda parte do g6
- **g1:50** — NAO LEVADO: não é item: o redator conferiu que o arquivo não digita a contagem (muda pelo delta)
- **g1:51** — NAO LEVADO: não é item: idem (muda pelo delta)
- **g1:61** — NAO LEVADO: é inventário, não item: virou a seção O RENOMEAR do .md e a chave renomear do .json
- **g4:3** — NAO LEVADO: fundido no item do crítico da linha 311 do delta (ADENDO7_ARQ e _ADENDO7_TXT definidos UMA vez, para o g1 e para o g4)
- **g5:12** — NAO LEVADO: fundido: na linha 43 vale o item do g3:16 com a palavra “dictionary”; na linha 37 o item do crítico (trecho único, com o contexto do rótulo do tempo)
- **g5:22** — NAO LEVADO: NÃO APLICAR (decisão do cético, que mantenho): «o que sou» é fala congelada letra por letra (quatro arquivos de work\cunhagens_13out) e a decisão registrada em delta_v410.py:888 (h) a guarda entre aspas angulares; o item trocava 1 de 13 ocorrências; a escolha (A: ficam as 13; B: trocam-se as 13 e escreve-se ao lado da 888(h)) é da gerência
- **g6:1** — NAO LEVADO: fundido com g1:13 (item do crítico, linha 485 do delta)
- **g6:2** — NAO LEVADO: fundido com g1:13 (item do crítico, linha 497 do delta)
- **g6:3** — NAO LEVADO: fundido no bloco único da finura (item do crítico, linha 1029 do delta)
- **g6:4** — NAO LEVADO: fundido no bloco único da finura (a âncora só existia depois do item 3)
- **g6:5** — NAO LEVADO: fundido no bloco único da finura (a âncora só existia depois do item 4)
- **g6:6** — NAO LEVADO: fundido na D108 única (item do crítico): a constante _D108_PARTE_2 é definida no bloco da finura, antes do DECISOES.update (o cético achou o NameError e a colisão de âncora)
- **g6:16** — NAO LEVADO: era sugestão de controle em prosa: o controle (a), que o cético mandou tornar OBRIGATÓRIO, virou três itens exatos do crítico na c8; os controles (b) e (c) viraram instrução

## 11. O que regenerar depois de aplicar

- um_v410_candidato.py
- v410_pins.py
- DIFF_v409_v410.diff
- CANDIDATO_v410.json
- ESPERADOS_v410.json
- GUARDA_FRASES_v410.json
- PREPARACAO_v410_PRONTA.json
- BUNDLE_v410.json (raiz e insumos)
- insumos/AEscala_embutida.lean
- insumos/RECIBO_PEDRAS_v410_NOMES.json (pelo instalador da R6)
- kernel/FLAGS_v410.json, KERNEL_RECIBO, POS_BUILD e os logs
- ensaio_a_seco_v410.json
- EXAME_PONTOS_*.json
- dry_v410/, dry_pre410/, falso_nos/, imp_*/, sim_*/, conferidor_import_*/, arvore_simulada_h8/
- pos_rito/CUSTODIA_v410_RASCUNHO.txt
- VERBATIM_CONGELADO_v410.json (por copiar_insumos_v410.py, com backup da lista de 28 ao lado)
- revisao_terceiro/txt__V410_AESCALA_TEXT.json
- dry_v410/*.txt, .tex e .pdf (o ensaio a seco do artigo)
- RELATORIO_PREPARACAO_v410.md

## 12. O que esta consolidação conferiu e o que não conferiu

- **itens exatos conferidos contra os arquivos:** 267
- **sobreposicoes:** 0
- **sintaxe dos arquivos com tudo aplicado em memoria:** ast.parse sem erro em todos os .py e .pysnip tocados
- **aspas angulares novas fora do corpus das falas:** 0
- **identificador velho fora de frase de registro:** 0
- **guarda copia de leitura:** os textos rendidos com valores de ensaio (FRASE_TETELESTAI, FRASE_RECONSTROI, FRASE_E36, o anuncio, FRASE_NOMES_RATIFICADOS, FRASE_FINURA, D100, D101, D106, D107, D108, E36 a E38, as leituras, as frases do H0DN, as molduras, o veredito) passaram sem violacao na copia das funcoes puras da guarda (P18 e a guarda das frases v405 a v410) extraida pelos redatores; seis controles negativos reprovaram como deviam
- **o que nao foi feito:** nao rodei o delta, o um.py, o ensaio, a cadeia, o lake nem script da pasta; nao compilei LaTeX; nao li a pasta da entrega do executor; os itens redigidos pelo critico nao passaram por cetico

