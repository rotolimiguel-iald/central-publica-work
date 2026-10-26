# TESTES DE G1

Composto em 24/10/2026 15:01:32 por `work\custodia_G1\testes\compor_testes_md.py` (suíte: `testes_g1.py`; Python 3.14.3). **Só LEEM o mundo real** (Nós, espelho, cofres, site, Atlas, mapa de rotas); o que escrevem vai a diretório temporário (`%TEMP%` e `C:\tmp\g1sbx_<pid>`, apagados no fim) ou a `work\custodia_G1\`. Nada de commit, push, subida, ACOM, rota, `um.py` ou kernel no mundo real. **Divulgação:** os testes `t19`/`t20` criam, no sandbox descartável, um repositório git de brinquedo (commit e push só para um `origin` local de brinquedo) para exercitar as pré-condições de E03; `t30`/`t31`/`t35` criam repositórios git de brinquedo em `%TEMP%`. Os testes `t27`–`t37` são as **regressões dos achados dos três céticos** (24/10/2026): cada um reproduz o roteiro do cético e confere o conserto. Os testes `t38`–`t46` são as **regressões dos achados do cético final** (24/10/2026, 3 MEDIA e 3 BAIXA, mais o auditor L04 que não via o llms.txt e o index.md e o `GIT_OPTIONAL_LOCKS` do vigia): `t39` cria um repositório git de brinquedo com `origin` local (commit e push só para ele), `t41` roda o `vigia.bat` de verdade com um `custodiar.py` de brinquedo e `t43`/`t44` usam diretórios temporários. **O Nós vivo anda:** nove testes antigos (`t01`, `t04`, `t17`, `t18`, `t19`, `t20`, `t25`, `t32`, `t33`) leem o Nós vivo e foram aprovados com a v398 PRONTA; quando outra sessão o põe em obra (um.py != pino do selo: a v399 em construção) eles ficam **PULADOS, com o motivo dito** (nem aprovação nem falha de código). A rodada completa com o Nós PRONTA (13:55–14:00, t01–t45: **45/45**) está guardada em `evidencias_cetico_final\SUITE_45de45_nos_pronta_20261024_1400.txt`; a de 14:32, **46/46** com o Nós congelado (vista), em `SUITE_46de46_nos_congelado_vista_20261024_1432.txt`; a anterior às mudanças, `--rapido`, em `BASELINE_antes_das_mudancas_rapido_20261024_1336.txt`.

**Nós congelado nesta rodada.** O Nós vivo estava **EM_OBRA** (a v399 em construção por outra sessão: `um.py` != pino do selo), então a rodada inteira — a suíte, os planos, o `vigiar` e o `vigia.bat` REAL — leu uma **vista** dele (`G1_RAIZ_NOS=C:\tmp\g1_nosview\Nós`, `testes\nos_congelado.py`): hardlinks para o Nós vivo, com os arquivos que o cofre `um_unificado_v398` também guarda (selados, capturas, diário, handoff, stdout) e o kernel selado vindos do **cofre** (`um_unificado_v398`, `tgl_kernel_v398`). Nada do Nós vivo foi tocado (só links de leitura; a vista é desfeita no fim).

## 1. Teste de aceitação (g) da ordem

### `custodiar.py planejar --versao v397 --seco`  → código de saída **5** (5 = nada a fazer por G1, com as decisões do operador do handoff abertas; 0 só se não houvesse nenhuma)

```
PLANO v397 — HISTÓRICA (o Nós já selou outra); espelho adiante
  E00   ok   gatilho: as três marcas do Nós                                 as três marcas de v397: SUPERADA; em obra no Nós: v399
  E01   ok   passo zero: backup de bytes de P                               um_v396_0a4395a89eeebbb7 (2040 arquivos; lista e tamanhos conferem (2040 arquivos); sha256 de uma amostra de 4
  E03   sup  espelho: conferir e copiar                                     espelho em v398; os blobs do commit bb2c392a (um.py, um_absoluto_selo.json, um_absoluto.json, tgl_kernel_proof
  E04   ok   geradores: ESTADO, LEDGER, CITATION, arco do site              as 5 marcas presentes (LEDGER, arco_json, gerar_estado_atual, i18n.js, index.html)
  E05   sup  ESTADO_ATUAL.md                                                a página é regenerada a cada versão; o bloco de v397 está nela
  E06   rel  varredura de sensíveis, git add -A, portas nº 1                PORTAS são regeradas a cada versão (G1 não tem a cópia desta versão: só o commit)
  E08   rel  laço portas ⇄ README ⇄ geradores do site (ponto fixo)          README/PORTAS/geradores do site são regerados a cada versão (G1 não tem a cópia desta versão)
  E08B  rel  parágrafos prontos do handoff no README (teto de 40 KB)        o README é regerado a cada versão (G1 não tem a cópia desta versão)
  E09   rel  verificações: portas e guarda do selo                          coberto pelo commit custodia(v397) (bb2c392a); sem recibo de G1 que prove que verificar_portas/guarda_do_selo 
  C1    ok   sondagem -> fatos_vNNN.json                                    C:\IALD\Central de Patentes\work\custodia_v397_23out\fatos_v397.json
  C5    ok   snapshot incremental do Chatgpt\ (segundo plano)               Chatgpt_20261024_091213_delta_de_20261023_174138 (214 copiados, 474713 idênticos à base)
  C3    ok   cofre um_unificado + tgl_kernel                                re-hash: 36/36 artefatos e 1426/1426 arquivos formais do kernel conferem por sha256 (manifesto declara 0 diver
  C4    ok   medição cofre × cofre (pré-voo da pedra)                       a pedra do runner já lê o cofre (C6)
  C6    ok   runner da Fronteira: repin + stub da pedra genérica            o runner tem _medir_v397_custodia
  C7    ok   runner: duas execuções                                         2 execuções com FRONTEIRA_SINCRONIZADA_V397 e custodia_v397.pass
  C8    ok   módulo dos 16 dispositivos: camada genérica                    o módulo tem a camada v397
  C9    ok   os 16 dispositivos                                             16/16 com a camada v397 no resultado (em algum resultado)
  C10   sup  os 16 *_FINAL.py (build)                                       commit ac616f48 da Central: os 16 FINAL do commit têm o sha256 do manifesto e embutem o módulo comum do commit
  C11   rel  os 16 *_FINAL.py (rodar)                                       commit custodia(v397) da Central: ac616f48 — sem recibo de G1 que prove o rc 0 dos 16 FINAL
  C12   sup  ledger de pinos                                                o ledger do commit ac616f48 da Central: no kernel v397, 0 erros, 0 avisos
  E10   ok   commit do espelho                                              commit bb2c392a
  E11   ok   push do espelho                                                commit bb2c392a contido em origin/main (ref local)
  E12   rel  pós-push: o raw serve o que o selo descreve                    o GitHub serve o espelho corrente; v397 é histórica (G1 não tem o raw dela)
  E13   rel  site: dados literais do selo                                   o site já diz v398 (versão posterior; o site de v397 não é mais lido)
  E14   rel  site: aplicar o selo ao index                                  o site já diz v398 (versão posterior)
  E15   rel  site: corpo inteiro e gêmeo Markdown                           regerados a cada versão (G1 não tem a cópia desta versão)
  E16   sup  site: sitemap e manifesto de subida                            manifesto_v397.json existe e é íntegro (1429 arquivos, 305,553,163 bytes)
  E17   ok   site: subida em ensaio (conjunto esperado)                     ensaio 20261023_180123_dryrun cobre o alvo (manifesto_v397.json): 1429 arquivos, sha16 de cada um igual; ressa
  E18   ok   site: subida                                                   20261023_181042: SUBIDA VERIFICADA levou o conteúdo exato do alvo (manifesto_v397.json): 1429 arquivos
  E19   ok   site: leitor de IA (R1)                                        leitor_ia_20261023_v397.md (23/10 18:18:19): R1 passa; posterior à última subida verificada (23/10 18:18:19)
  C2    ok   ACOM: inscrição (init) da custódia                             referência claude-central-a7_custodia-v397-23out.json
  C13   ok   registro: diário do site, memórias, Atlas, MEMORY.md (a rota é Atlas, as 6 memórias/diários (DIARIO_DO_SITE.md, site-sessao-estado.md, tgl-fronteira-teorica.md, central-de-p
  C17A  ok   ACOM: transição t1 (espelho, site, Central local)              revisão ACOM 3 (≥ 1); último evento -custodia-v397-23out-t3-concluida-organismo-medido
  C14   ok   commit e push da Central (lista de permissão)                  commit ac616f48 em origin/main (ref local)
  C15   ok   conferência final independente                                 CONFERENCIA_FINAL_v397.json: 12/12
  C16   ok   registro «PUBLICADA» (pós-push) e a rota custodia.vN           MEMORY.md e handoff-v397-custodia.md dizem PUBLICADA; rota custodia.v397 registrada
  C17B  ok   ACOM: transição t2 (custódia publicada)                        revisão ACOM 3 (≥ 2); último evento -custodia-v397-23out-t3-concluida-organismo-medido
  C18   rel  Central pública: 3 repositórios, /central/, um.acom            a Central pública segue a versão corrente; a rota custodia.v397 existe (G1 não tem o retrato público desta ver
  C19   rel  Nós vivo e quadro do organismo (a medida final)                o quadro mede a versão corrente do Nós (G1 não tem artefato do quadro desta versão)
  C20   ok   pernas que o selo já puxa: Bancada Um, ACTIVE.json, memória ci Bancada Um (recibo de sincronização): RECIBO_SINCRONIZACAO_v397_20261023_171531.json; memória canônica da fila
  C21   oper app: a release instalada contra a versão (só conferir; constru DEFASADO: o app instalado está na release v395; a versão é v397 (histórica; o selo corrente é v398). Decisão d
  C17C  ok   ACOM: transição t3 (organismo medido)                          revisão ACOM 3 (≥ 3); último evento -custodia-v397-23out-t3-concluida-organismo-medido
  contagem: APLICADO 25, OPERADOR 1, SUPERADO 5, SUPERADO_REL 11
NADA A FAZER: todos os passos aplicados ou superados (provados no artefato: 30; superados SÓ pela relação histórica, que G1 não prova: 11).
   ressalva: os passos E06, E08, E08B, E09, C11, E12, E13, E14, E15, C18, C19 estão «rel» — a versão é histórica e a superfície é regerada a cada versão; G1 não tem artefato que os prove
DECISÕES DO OPERADOR ABERTAS (2) — G1 não as toma; nada mais falta: código 5:
   - [C21] DEFASADO: o app instalado está na release v395; a versão é v397 (histórica; o selo corrente é v398). Decisão do OPERADOR: pipeline work\iald_v398_<data>\app (fase A/B; construtor ≠ revisor; troca do serviço pelo operador). G1 só CONFERE: não constrói, não instala, não reinicia o serviço
   - [handoff (verbatim)] nomear o registro de veracidade (`teste_de_veracidade_fase9_v397` é provisório); a pendência [LEGAL] herdada da v395 (a divergência da tabela da patente ACOM Mirror; com a agente de PI); a custódia, subir o site, commit/push. [OPEN]: a discriminação a 5σ (β_TGL na natureza), a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), o cont
       (o que o handoff lista como ato de custódia (a custódia, subir o site, commit/push) está nos passos de G1; G1 não sabe se as decisões já foram tomadas)
```

### `custodiar.py planejar --versao v398 --seco`  → código de saída **20** (a outra sessão custodia a v398 agora: o plano lista só o que ainda falta; 20 = um passo BLOQUEADO)

```
PLANO v398 — corrente (selo do Nós); espelho igual
  E00   ok   gatilho: as três marcas do Nós                                 as três marcas de v398: PRONTA; em obra no Nós: v399
  E01   ok   passo zero: backup de bytes de P                               um_v397_388cc3742323421c (2059 arquivos; lista e tamanhos conferem (2059 arquivos); sha256 de uma amostra de 4
  E03   BLOQ espelho: conferir e copiar                                     pré-condição de executar: o espelho não está atrás de v398 | marca: 1 de 1036 pares por copiar/diferentes; ker
  E04   ok   geradores: ESTADO, LEDGER, CITATION, arco do site              as 6 marcas presentes (CITATION, LEDGER, arco_json, gerar_estado_atual, i18n.js, index.html)
  E05   ok   ESTADO_ATUAL.md                                                ESTADO_ATUAL.md traz c632fa261ce3f538 e o bloco da custódia (107269 bytes)
  E06   ok   varredura de sensíveis, git add -A, portas nº 1                PORTA.json/TUNEL.json/README com c632fa261ce3f538
  E08   ok   laço portas ⇄ README ⇄ geradores do site (ponto fixo)          portas/README/geradores no ponto fixo; 0 números citados defasados
  E08B  oper parágrafos prontos do handoff no README (teto de 40 KB)        L01: o parágrafo PARAGRAFO_SONICO_v398 (2630 B) NÃO está no README (40951 B de 40960): não cabe. gerar_readme_
  E09   rel  verificações: portas e guarda do selo                          coberto pelo commit custodia(v398) (35e8cdf6); sem recibo de G1 que prove que verificar_portas/guarda_do_selo 
  C1    ok   sondagem -> fatos_vNNN.json                                    C:\IALD\Central de Patentes\work\custodia_v398_24out\fatos_v398.json
  C5    ok   snapshot incremental do Chatgpt\ (segundo plano)               Chatgpt_20261024_091213_delta_de_20261023_174138 (214 copiados, 474713 idênticos à base)
  C3    ok   cofre um_unificado + tgl_kernel                                re-hash: 36/36 artefatos e 1428/1428 arquivos formais do kernel conferem por sha256 (manifesto declara 0 diver
  C4    ok   medição cofre × cofre (pré-voo da pedra)                       a pedra do runner já lê o cofre (C6)
  C6    ok   runner da Fronteira: repin + stub da pedra genérica            o runner tem _medir_v398_custodia
  C7    ok   runner: duas execuções                                         3 execuções com FRONTEIRA_SINCRONIZADA_V398 e custodia_v398.pass
  C8    ok   módulo dos 16 dispositivos: camada genérica                    o módulo tem a camada v398
  C9    ok   os 16 dispositivos                                             16/16 com a camada v398 no resultado mais recente
  C10   ok   os 16 *_FINAL.py (build)                                       16/16 FINAL: o sha256 de cada um é o do manifesto e todos embutem o módulo comum de hoje (com a camada v398)
  C11   INDE os 16 *_FINAL.py (rodar)                                       sem recibo durável do rc dos 16 FINAL (G1 grava RECIBO_C11_v398.json na pasta de trabalho ao rodá-los; rode C1
  C12   ok   ledger de pinos                                                ledger no kernel v398, 0 erros, 0 avisos
  E10   ok   commit do espelho                                              commit 35e8cdf6
  E11   ok   push do espelho                                                commit 35e8cdf6 contido em origin/main (ref local)
  E12   ok   pós-push: o raw serve o que o selo descreve                    quadro de 2026-10-24 11:27:46: sim
  E13   ok   site: dados literais do selo                                   nota «Current seal» = v398 c632fa261ce3f538
  E14   ok   site: aplicar o selo ao index                                  index.html diz «v398 · c632fa261ce3f538»
  E15   ok   site: corpo inteiro e gêmeo Markdown                           llms-full.txt e index.md trazem c632fa261ce3f538
  E16   FALT site: sitemap e manifesto de subida                            o manifesto está velho frente ao disco: 89 mudados (ex.: .htaccess, central/RELATORIO_RETRATO_PUBLICO.json, ce
  E17   FALT site: subida em ensaio (conjunto esperado)                     depende de E16 (o manifesto está velho frente ao disco: 89 mudados (ex.: .htaccess, central/RELATORIO_RETRATO_
  E18   FALT site: subida                                                   depende de E16 (o manifesto está velho frente ao disco: 89 mudados (ex.: .htaccess, central/RELATORIO_RETRATO_ [para fora]
  E19   FALT site: leitor de IA (R1)                                        depende de E18 (depende de E16 (o manifesto está velho frente ao disco: 89 mudados (ex.: .htaccess, central/RE
  C2    ok   ACOM: inscrição (init) da custódia                             referência claude-central-a7_custodia-v398-24out.json
  C13   ok   registro: diário do site, memórias, Atlas, MEMORY.md (a rota é Atlas, as 6 memórias/diários (DIARIO_DO_SITE.md, site-sessao-estado.md, tgl-fronteira-teorica.md, central-de-p
  C17A  ok   ACOM: transição t1 (espelho, site, Central local)              revisão ACOM 3 (≥ 1); último evento -custodia-v398-24out-t3-concluida-organismo-medido
  C14   ok   commit e push da Central (lista de permissão)                  commit df5f5ef0 em origin/main (ref local)
  C15   ok   conferência final independente                                 CONFERENCIA_FINAL_v398.json: 12/12
  C16   ok   registro «PUBLICADA» (pós-push) e a rota custodia.vN           MEMORY.md e handoff-v398-custodia.md dizem PUBLICADA; rota custodia.v398 registrada
  C17B  ok   ACOM: transição t2 (custódia publicada)                        revisão ACOM 3 (≥ 2); último evento -custodia-v398-24out-t3-concluida-organismo-medido
  C18   INDE Central pública: 3 repositórios, /central/, um.acom            o quadro (medido em 24/10 11:27:46) é anterior a à última modificação de llms/sitemap do site (24/10 14:54:48) [para fora]
  C19   FALT Nós vivo e quadro do organismo (a medida final)                o quadro (medido em 24/10 11:27:46) é anterior a à última subida verificada do site (24/10 13:41:02): remedir 
  C20   ok   pernas que o selo já puxa: Bancada Um, ACTIVE.json, memória ci Bancada Um (recibo de sincronização): RECIBO_SINCRONIZACAO_v398_20261024_013744.json; memória canônica da fila
  C21   oper app: a release instalada contra a versão (só conferir; constru DEFASADO: o app instalado está na release v395; a versão é v398. Decisão do OPERADOR: pipeline work\iald_v398_
  C17C  ok   ACOM: transição t3 (organismo medido)                          revisão ACOM 3 (≥ 3); último evento -custodia-v398-24out-t3-concluida-organismo-medido
  contagem: APLICADO 31, BLOQUEADO 1, FALTA 5, INDETERMINADO 2, OPERADOR 2, SUPERADO_REL 1
FALTAM 8 passo(s): E03, C11, E16, E17, E18, E19, C18, C19
EXECUTAR PARARIA EM E03 (BLOQUEADO): pré-condição de executar: o espelho não está atrás de v398 | marca: 1 de 1036 pares por copiar/diferentes; kernel: 0 faltando/diferentes, 0 órfãos
   atrás dele, sem rodar enquanto isso durar: C11, E16, E17, E18, E19, C18, C19 (use --so ID para o que não depende dele; cada passo confere a sua pré-condição)
TEXTOS (só o que os passos pendentes consomem): nenhum passo pendente precisa de prosa nova
  parágrafos prontos no handoff: PARAGRAFO_README_v397, PARAGRAFO_SONICO_v398 | marcadores opcionais presentes: (nenhum)
DECISÕES DO OPERADOR ABERTAS (8) — G1 não as toma:
   - [E08B] L01: o parágrafo PARAGRAFO_SONICO_v398 (2630 B) NÃO está no README (40951 B de 40960): não cabe. gerar_readme_frente.py não tem slot para ele e a frente não tem folga; a decisão é estrutural (mover «Read in this order» para o ESTADO_ATUAL e fixar um slot «última custódia» com orçamento, ou rever o teto): do operador/gerência — G1 não corta o README
   - [C21] DEFASADO: o app instalado está na release v395; a versão é v398. Decisão do OPERADOR: pipeline work\iald_v398_<data>\app (fase A/B; construtor ≠ revisor; troca do serviço pelo operador). G1 só CONFERE: não constrói, não instala, não reinicia o serviço
   - [handoff (verbatim)] nomear os dois registros novos (`sonico_v398` e `afinacao_das_cordas_v398` são provisórios); a pendência [LEGAL] herdada da v395 (a divergência da tabela da patente ACOM Mirror; com a agente de PI); a custódia, subir o site, commit/push. [OPEN]: a discriminação a 5σ (β_TGL na natureza), a geometria das cordas e a ligação do círculo da folha-mundo ao círculo 
       (o que o handoff lista como ato de custódia (a custódia, subir o site, commit/push) está nos passos de G1; G1 não sabe se as decisões já foram tomadas)
   - [quadro de 2026-10-24 11:27:46] iald.ia.br / llms.txt no ar (Kimi, 23/10): esperado 200, achado 404 (PENDENTE_OPERADOR)
   - [quadro de 2026-10-24 11:27:46] iald.ia.br / sitemap.xml no ar (Kimi, 23/10): esperado 200, achado 404 (PENDENTE_OPERADOR)
   - [quadro de 2026-10-24 11:27:46] iald.ia.br / robots.txt no ar (ORDEM 020 C: upload pelo painel da hospedagem): esperado 200, achado 404 (PENDENTE_OPERADOR)
   - [quadro de 2026-10-24 11:27:46] App IALD (ciência própria) / release instalada no app = selo corrente (release do app: pipeline work/iald_vNNN_*/app): esperado v398, achado v395 (DEFASADO)
   - [quadro de 2026-10-24 11:27:46] Zenodo / versão depositada = selo corrente (depósito é ato do operador): esperado v398, achado v392 (PENDENTE_OPERADOR)
```

### `custodiar.py vigiar`  → código de saída **20**

```
Nós: selo v398 c632fa261ce3f538 (2026-10-24 00:26:08) | três marcas de v398: PRONTA
Em obra no Nós (pasta em cadeia_de_selo sem selo): v399 — a custódia dela espera o selo.
Plano de v398: 32 de 42 passos aplicados ou superados (+2 do operador, à parte); pendentes: E03, C11, E16, E17, E18, E19, C18, C19
Superados SÓ pela relação histórica (G1 não os prova): E09
DECISÃO DO OPERADOR ABERTA: [E08B] L01: o parágrafo PARAGRAFO_SONICO_v398 (2630 B) NÃO está no README (40951 B de 40960): não cabe. gerar_readme_frente.py não tem slot para ele e a frente não tem folga; a decisão é estrutural (mover «R
DECISÃO DO OPERADOR ABERTA: [C21] DEFASADO: o app instalado está na release v395; a versão é v398. Decisão do OPERADOR: pipeline work\iald_v398_<data>\app (fase A/B; construtor ≠ revisor; troca do serviço pelo operador). G1 só CONFERE
DECISÃO DO OPERADOR ABERTA: [handoff (verbatim)] nomear os dois registros novos (`sonico_v398` e `afinacao_das_cordas_v398` são provisórios); a pendência [LEGAL] herdada da v395 (a divergência da tabela da patente ACOM Mirror; com a agente de PI); a
DECISÃO DO OPERADOR ABERTA: [quadro de 2026-10-24 11:27:46] iald.ia.br / llms.txt no ar (Kimi, 23/10): esperado 200, achado 404 (PENDENTE_OPERADOR)
DECISÃO DO OPERADOR ABERTA: [quadro de 2026-10-24 11:27:46] iald.ia.br / sitemap.xml no ar (Kimi, 23/10): esperado 200, achado 404 (PENDENTE_OPERADOR)
DECISÃO DO OPERADOR ABERTA: [quadro de 2026-10-24 11:27:46] iald.ia.br / robots.txt no ar (ORDEM 020 C: upload pelo painel da hospedagem): esperado 200, achado 404 (PENDENTE_OPERADOR)
DECISÃO DO OPERADOR ABERTA: [quadro de 2026-10-24 11:27:46] App IALD (ciência própria) / release instalada no app = selo corrente (release do app: pipeline work/iald_vNNN_*/app): esperado v398, achado v395 (DEFASADO)
DECISÃO DO OPERADOR ABERTA: [quadro de 2026-10-24 11:27:46] Zenodo / versão depositada = selo corrente (depósito é ato do operador): esperado v398, achado v392 (PENDENTE_OPERADOR)
ESTADO: BLOQUEADA (STOP) — E03
```

### `vigia.bat` REAL (MODO SOMBRA; o Python e o `custodiar.py` de verdade; `G1_PASTA` = pasta temporária, apagada) → código de saída **20** em 42 s

Arquivos que o vigia deixou na pasta: `PLANO_v398.json`, `VIGIA_STDERR_ULTIMO.txt`, `VIGIA_ULTIMO.json`, `VIGIA_ULTIMO.txt`. `VIGIA_ULTIMO.txt`:

```
versao=v398
selo=v398
marcas=PRONTA
codigo=20
estado=BLOQUEADA (STOP)
hora=2026-10-24T15:01:13-03:00
```
(o código de saída é o do `vigiar`: 0 custodiada · 1 pendente · 5 custodiada com decisões do operador abertas · 10 em obra · 20 incompleta/bloqueada · 30 falha de leitura/escrita · 40 divergência · 99 sem Python/CLI)

## 2. A suíte (`testes_g1.py`; código de saída 0)

Executado em 24/10/2026 14:59:59 por `work\custodia_G1\testes\testes_g1.py` (Python 3.14.3). Só leem o mundo real (Nós, espelho, cofres, site) e escrevem em diretório temporário; nada de commit, push, subida, ACOM, rota, um.py ou kernel.

**46 passam, 0 falham, 0 pulados** em 337 s.

Nós lido de `G1_RAIZ_NOS` — uma VISTA congelada na v398 (`testes\nos_congelado.py`) (as três marcas da v398): **PRONTA** no início da rodada, **PRONTA** no fim. Os testes que leem o Nós (`nos_pronta`) só rodam com ele PRONTA; senão ficam PULADOS, com o motivo (outra sessão pode estar construindo a versão seguinte).

> [nota operacional do operador — omitida no retrato público]

## 3. Os roteiros dos céticos contra o pacote ANTERIOR às correções (`roteiro_no_codigo_antigo.py`; código de saída 0)

O pacote de antes (os módulos `*.antes` guardados em `originais_antes_dos_ceticos\`, sem `recibos.py`) montado em diretório temporário e posto a ler os mesmos cenários de brinquedo (`t27`, `t29`, `t30`): o defeito aparece nele e some no pacote atual. `util.py.antes` foi **reconstruído** desfazendo as três trocas de hoje (o `util.py` foi editado antes da cópia de segurança).

```
1) site, conteúdo novo + manifesto regerado + relatórios antigos: E16=APLICADO E17=APLICADO E18=APLICADO  (o certo: aplicado, FALTA, FALTA)
2) C11 num PROCESSO SEGUINTE, depois de rodar os 16 FINAL: INDETERMINADO  (o certo: APLICADO)
3) E10 de uma tarefa agendada (PATH sem git): FALTA — sem commit custodia(v397): no espelho  (o certo: achar o git; sem git, falha de leitura visível)
```

## 3b. Os roteiros do cético final contra o pacote ANTERIOR a esta rodada (`roteiro_no_codigo_antes_do_cetico_final.py`; código de saída 0)

O pacote de antes (os módulos `*.antes` de `originais_antes_do_cetico_final\`: site, central, espelho, quadro, publica, caminhos, motor, util) montado em diretório temporário e posto a ler os mesmos cenários de brinquedo (`t38`, `t39`, `t43`, `t44`, `t45`): os seis defeitos aparecem nele e somem no pacote atual (cada linha termina com «o certo»). O 6º usa a mensagem do commit da v398 com os dados reais (somente leitura). `publica.py.antes` foi **reconstruído** desfazendo a única troca (o backup foi esquecido antes de editar; o tamanho 6.452 é o que o patch imprimiu).

```
1) subida verificada (E18=APLICADO) e depois uma repetição «nada a subir»: E18=FALTA (o ar (pelo registro das subidas verificadas) difere do alvo (disco de ); _ap_e18 com o banner «nada a subir»: Divergencia (subir_site.py não terminou em «SUBIDA VERIFICADA)  (o certo: APLICADO; aceita)
2) C14 com um arquivo alheio já staged: o origin recebeu ['alheio/a.txt', 'vault/originals_copy/um_unificado_v998/x.json']  (o certo: só vault/originals_copy/um_unificado_v998/x.json; o alheio fica staged, fora do commit)
3) E19: R1 PASSA de 09:32 e a subida verificada de 11:26 → APLICADO; depois um R1 mais novo que FALHA → APLICADO  (o certo: FALTA nos dois casos)
4) E01 com um byte trocado em um_absoluto.json do backup e o manifesto dizendo «conferido_contra_origem: true»: ACEITO  (o certo: recusado — sha256 da amostra difere)
5) auditor L04 com secoes/07 citada 11762 (real 11731) no llms.txt e no index.md: 0 defasado(s) achado(s)  (o certo: 2)
6) mensagem do commit da Central: diz «rota custodia.v398 no mapa de rotas»  (o certo: não cita a rota no mapa — ela só entra em C16)
```

## 4. O que os testes NÃO provam (dito, não calado)

- Os passos que **chamam os geradores fixos no espelho real** (`E05` gerar_estado_atual, `E06`/`E08` gerar_portas + gerar_readme_frente + o laço até o ponto fixo, `E09` verificar_portas/guarda_do_selo, `E13`–`E16`, `E19`) e os que **rodam coisa pesada na Central** (`C7` runner ×2, `C9` 16 dispositivos, `C10` build, `C12` ledger) só foram verificados por **leitura do código, marcas contra o estado real e gates em fixtures**; não foram executados (a v398 está em custódia por outra sessão e não existe versão nova para custodiar). `C11` (os 16 FINAL) foi exercido só com FINAL de brinquedo (`t29`).
- Não executados por regra da ordem: commit/push (`E10`,`E11`,`C14`), subida (`E18`, `C18`), ACOM (`C2`, `C17*`), `E12` (rede), `C19`/`C20` ao vivo (rodam o quadro e esperam serviços): o **gancho que remede o quadro velho** foi testado com um `remedir` de brinquedo (`t28`), nunca rodando `estado_do_organismo.py` no mundo real. Seus **gates** (conjunto esperado da subida, lista de permissão, portão de texto, trava, `--publicar`) estão testados.
- `C5` em escala real (≈35 min, 474 mil arquivos) não foi rodado; a lógica (base = último snapshot conferido, delta por sha-256, exclusões, divergência, instante do selo) foi exercida em sandbox.
- `E03` sandbox usa um **espelho de brinquedo** (a v397 guardada pelo passo zero) e uma guarda privada **sintética**: o arquivo de marcadores privados da casa NÃO foi lido (regra da ordem); a leitura real roda só em `executar`.
- O laço `E08` (ponto fixo em ≤4 passadas) e o auditor foram escritos a partir da leitura dos geradores e do estado medido; **a convergência em 2–3 passadas é hipótese** até a primeira execução viva (a ESPEC L23 diz o mesmo).
- O **registro das subidas** (E18) diz o que o ar TEM pelo que as subidas verificadas levaram; não consulta o ar. Quem muda o ar por fora do `subir_site.py` (painel, FTP manual) não aparece: o ensaio (E17, HTTP) e o quadro (`Site (ar)`) é que veem o ar.
- `SUPERADO_REL` é honestidade, não prova: nas versões históricas a ferramenta não tem como provar o que a versão seguinte sobrescreveu; ela o diz em vez de fingir (ver o plano de v397).
- **Nós congelado e asserções relaxadas (24/10/2026):** quando o Nós vivo não é a v398 PRONTA (a v399 em construção), esta composição roda TUDO numa **vista** dele (`testes\nos_congelado.py`, `G1_RAIZ_NOS`): hardlinks para os arquivos do Nós vivo, com os que o cofre `um_unificado_v398` também guarda (selados, capturas, diário, handoff, stdout) e o kernel selado tomados do **cofre** — é a v398 como foi selada, não o Nós de hoje; a vista é desfeita no fim e nada do Nós vivo é tocado. Três asserções do mundo vivo foram **relaxadas** por deriva de outras sessões, sem tirar a forma: `t04` não conta arquivo do túnel criado DEPOIS da cópia desta custódia (ORDEM_022), `t18` aceita `E03` entre os pendentes da v398 e `t25` conta «pelo menos 27» passos do encadeador da Central pública (que ganhou `central_extra`).
- **Do fechamento dos achados do cético final:** (1) o commit da Central com pathspec foi exercido em repositório de brinquedo (com `origin` local) — nunca no `.git` da Central real, e `C14` segue sem rodar ao vivo; (2) «nada a subir» foi exercido com relatórios fabricados no formato exato que `subir_site.py` grava (título e tabela lidos do código dele); nenhuma subida foi feita; (3) o `vigia.bat` rodou de verdade, mas a **tarefa agendada do Windows não está instalada** (é da gerência, junto com a decisão L17) e o `executar` NÃO é chamado por ele; (4) `C21` só confere o `iald_nucleo_fixo.json`: não roda o pipeline do app, não instala e não reinicia o serviço; (5) o R1 relido no fim de `C18` foi exercido com o encadeador e o leitor substituídos — a Central pública não subiu; (6) o hash de **amostra** do backup (E01) não pega um byte trocado, de mesmo tamanho, num arquivo que não esteja na amostra de 48 (a lista e os tamanhos de todos os arquivos, o selo de dentro e os selados são conferidos).
