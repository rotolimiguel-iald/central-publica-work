PLANO v406 — corrente (selo do Nós); espelho igual
  E00   ok   gatilho: as três marcas do Nós                                 as três marcas de v406: PRONTA; em obra no Nós: v407
  E01   ok   passo zero: backup de bytes de P                               um_v405_0030242565cc13f6 (2257 arquivos; lista e tamanhos conferem (2257 arquivos); sha256 de uma amostra de 4
  E03   ok   espelho: conferir e copiar                                     1105 pares presentes no espelho (selados e kernel conferidos por sha256; 3 barrados pela guarda, ditos no rela
  E04   ok   geradores: ESTADO, LEDGER, CITATION, arco do site              as 6 marcas presentes (CITATION, LEDGER, arco_json, gerar_estado_atual, i18n.js, index.html)
  E05   ok   ESTADO_ATUAL.md                                                ESTADO_ATUAL.md traz ddcb91930982d614 e o bloco da custódia (202122 bytes)
  E06   ok   varredura de sensíveis, git add -A, portas nº 1                PORTA.json/TUNEL.json/README com ddcb91930982d614
  E08   ok   laço portas ⇄ README ⇄ geradores do site (ponto fixo)          portas/README/geradores no ponto fixo; 0 números citados defasados
  E08B  ok   parágrafos prontos do handoff no README (teto de 40 KB)        o README traz os parágrafos prontos desta versão
  E09   ok   verificações: portas e guarda do selo                          recibo de E09 (2026-11-03T02:24:44): verificar_portas ERROS 0 e guarda_do_selo ok; commit a381c4d1
  C1    ok   sondagem -> fatos_vNNN.json                                    FATOS_CUSTODIA.json já está no cofre
  C5    ok   snapshot incremental do Chatgpt\ (segundo plano)               Chatgpt_20261103_022447_delta_de_20261102_005712 (9 copiados, 477552 idênticos à base)
  C3    ok   cofre um_unificado + tgl_kernel                                re-hash: 36/36 artefatos e 1747/1747 arquivos formais do kernel conferem por sha256 (manifesto declara 0 diver
  C4    ok   medição cofre × cofre (pré-voo da pedra)                       medição gravada
  C6    ok   runner da Fronteira: repin + stub da pedra genérica            o runner tem _medir_v406_custodia
  C7    ok   runner: duas execuções                                         3 execuções com FRONTEIRA_SINCRONIZADA_V406 e custodia_v406.pass
  C8    ok   módulo dos 16 dispositivos: camada genérica                    o módulo tem a camada v406
  C9    ok   os 16 dispositivos                                             16/16 com a camada v406 no resultado mais recente
  C10   ok   os 16 *_FINAL.py (build)                                       16/16 FINAL: o sha256 de cada um é o do manifesto e todos embutem o módulo comum de hoje (com a camada v406)
  C11   ok   os 16 *_FINAL.py (rodar)                                       rc 0 em 16/16 (recibo durável de 2026-11-03T02:46:45; os 16 FINAL de hoje têm os sha256 do recibo)
  C12   ok   ledger de pinos                                                ledger no kernel v406, 0 erros, 0 avisos
  E10   ok   commit do espelho                                              commit a381c4d1
  E11   ok   push do espelho                                                commit a381c4d1 contido em origin/main (ref local)
  E12   ok   pós-push: o raw serve o que o selo descreve                    quadro de 2026-11-03 06:11:04: sim
  E13   ok   site: dados literais do selo                                   nota «Current seal» = v406 ddcb91930982d614
  E14   ok   site: aplicar o selo ao index                                  index.html diz «v406 · ddcb91930982d614»
  E15   FALT site: corpo inteiro e gêmeo Markdown                           4 números citados defasados: SITE:llms-full.txt cita secoes/07-o-programa-um-py.md=11736, real 11628; SITE:llm
  E16   ok   site: sitemap e manifesto de subida                            manifesto confere com o disco inteiro: 1579 arquivos, 0 mudados, 0 novos, 0 sumidos
  E17   ok   site: subida em ensaio (conjunto esperado)                     ensaio 20261103_083951_dryrun cobre o alvo (disco de v3.0): 1579 arquivos, sha16 de cada um igual; 8 diferença
  E18   FALT site: subida                                                   o ar (pelo registro das subidas verificadas) difere do alvo (disco de v3.0): 7 diferem (ex.: llms.txt, read-br [para fora]
  E19   FALT site: leitor de IA (R1)                                        depende de E18 (o ar (pelo registro das subidas verificadas) difere do alvo (disco de v3.0): 7 diferem (ex.: l
  C2    ok   ACOM: inscrição (init) da custódia                             referência custodia_v406_ddcb9193.json
  C13   ok   registro: diário do site, Atlas; memórias e linha do MEMORY.md Atlas, as 6 memórias/diários (DIARIO_DO_SITE.md, site-sessao-estado.md, tgl-fronteira-teorica.md, central-de-p
  C17A  ok   ACOM: transição t1 (espelho, site, Central local)              revisão ACOM 2 (≥ 1); último evento dor-v406-custodia-v406-03nov-t2-custodia-publicada
  C14   ok   commit e push da Central (lista de permissão)                  commit 42f3b0c9 em origin/main (ref local)
  C15   ok   conferência final independente                                 CONFERENCIA_FINAL_v406.json: 13/13
  C16   ok   registro «PUBLICADA» (pós-push) e a rota custodia.vN           MEMORY.md e handoff-v406-custodia.md dizem PUBLICADA (ou a fila da memória o tem para a gerência); rota custod
  C17B  ok   ACOM: transição t2 (custódia publicada)                        revisão ACOM 2 (≥ 2); último evento dor-v406-custodia-v406-03nov-t2-custodia-publicada
  C18   INDE Central pública: 3 repositórios, /central/, um.acom            o quadro (medido em 03/11 06:11:04) é anterior a à última modificação de llms/sitemap do site (03/11 08:39:49) [para fora]
  C19   FALT Nós vivo e quadro do organismo (a medida final)                quadro de 2026-11-03 06:11:04: 7 DEFASADO e 0 FALHA de G1 (ex.: App (fila científica) / memória científica da 
  C20   FALT pernas que o selo já puxa: Bancada Um, ACTIVE.json, memória ci DEFASADO no organismo: memória canônica da fila/app (ACTIVE.json) (release v404 (!= v406)); memória científica
  C21   oper app: a release instalada contra a versão (só conferir; constru DEFASADO: o app instalado está na release v405; a versão é v406. Decisão do OPERADOR: pipeline work\iald_v406_
  C17C  FALT ACOM: transição t3 (organismo medido)                          revisão ACOM 2 < 3 [para fora]
  contagem: APLICADO 34, FALTA 6, INDETERMINADO 1, OPERADOR 1
FALTAM 7 passo(s): E15, E18, E19, C18, C19, C20, C17C
TEXTOS (só o que os passos pendentes consomem): nenhum passo pendente precisa de prosa nova
  parágrafos prontos no handoff: PARAGRAFO_README_v397, PARAGRAFO_O_FECHAMENTO_v406 | marcadores opcionais presentes: TITULO_EN_v406, ENTROU_EN_v406, KERNEL_LEITURA_EN_v406, ABERTOS_EN_v406, ARCO_EN_v406, ARCO_PT_v406, COMMIT_v406
DECISÕES DO OPERADOR ABERTAS (7) — G1 não as toma:
   - [C21] DEFASADO: o app instalado está na release v405; a versão é v406. Decisão do OPERADOR: pipeline work\iald_v406_<data>\app (fase A/B; construtor ≠ revisor; troca do serviço pelo operador). G1 só CONFERE: não constrói, não instala, não reinicia o serviço
   - [handoff (verbatim)] o nome da candidata e das pedras candidatas do dia; a decisão [LEGAL] D2; o README pinado (D39); a ratificação das decisões D34 a D40 da gerência que ele ainda não leu. [OPEN]: a discriminação a 5σ (β_TGL na natureza), K(O) ≠ ⊥ para O compacto, o lema que liga o psíon ao canto, o magnetismo na cadeia da tensão, qual é o disco, quais são as cinco notas, `H_BW
       (o que o handoff lista como ato de custódia (a custódia, subir o site, commit/push) está nos passos de G1; G1 não sabe se as decisões já foram tomadas)
   - [quadro de 2026-11-03 06:11:04] iald.ia.br / llms.txt no ar (Kimi, 23/10): esperado 200, achado 404 (PENDENTE_OPERADOR)
   - [quadro de 2026-11-03 06:11:04] iald.ia.br / sitemap.xml no ar (Kimi, 23/10): esperado 200, achado 404 (PENDENTE_OPERADOR)
   - [quadro de 2026-11-03 06:11:04] iald.ia.br / robots.txt no ar (ORDEM 020 C: upload pelo painel da hospedagem): esperado 200, achado 404 (PENDENTE_OPERADOR)
   - [quadro de 2026-11-03 06:11:04] App IALD (ciência própria) / release instalada no app = selo corrente (release do app: pipeline work/iald_vNNN_*/app): esperado v406, achado v405 (DEFASADO)
   - [quadro de 2026-11-03 06:11:04] Zenodo / versão depositada = selo corrente (depósito é ato do operador): esperado v406, achado v401 (PENDENTE_OPERADOR)
