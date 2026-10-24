# ESPEC G1 — perna 1 da custódia: espelho `the_boundary` + site da TGL

> Especificação escrita por leitura (nenhum script da esteira foi executado). Alvo: quem for construir `tools\custodia_g1\` e `tools\custodiar.py` (perna 1). Língua: português; identificadores como estão no código.
> Leitura de 24/10/2026, das 09:00 às 09:30 (hora local). Autoria: subagente de leitura do fluxo G1 (modelo Sonnet 5.5), a pedido do orquestrador. Estatutos usados abaixo: **[LIDO]** visto no código ou no arquivo; **[MEDIDO]** medido por script de leitura nesta sessão; **[DECLARADO]** afirmado na origem (memória, rota, handoff), não verificado aqui; **[PROPOSTA]** sugestão desta especificação.

## 0. Escopo, estado do mundo na leitura e o que NÃO foi feito

**Escopo.** Só a perna (1): espelho `C:\IALD\Artigo\the_boundary` e site `C:\IALD\Site\tgl\v3.0` (fonte) / `v3.0_bancada` (ferramentas). Fora: cofre/runner/16 dispositivos/FINAL/ledger/snapshot (perna 2), Central pública (perna 3), quadro/ACOM/rotas (perna 4). Onde as pernas se tocam, está dito (§5 e lacunas L10/L11).

**Estado do mundo [MEDIDO] — duas fotografias, porque a custódia v398 andou enquanto eu lia:**
- Selo do Nós: v398, pino `c632fa261ce3f538`, selado `2026-10-24 00:26:08`; diário com o bloco `v398 SELADA (COMPLETA)`; `HANDOFF_v398_CUSTODIA.md` e `rodada_v398_stdout.txt` presentes.
- **Fotografia das 09:01.** Espelho em `bb2c392a` (custódia v397), árvore limpa. O passo zero da v398 já tinha rodado (08:47:27; `the_boundary_BACKUPS\um_v397_388cc3742323421c`, manifesto `conferido_contra_origem: true`, 2.059 arquivos). `custodia_v398_espelho.py` e `custodia_v398_geradores.py` ainda não existiam. As medidas sobre o código dos scripts v395–v397 e dos geradores fixos (§2 a §4) são desta fotografia.
- **Fotografia das 09:25.** A outra sessão terminou o espelho da v398 pelo método antigo: `custodia_v398_espelho.py` (gravado 09:04, 40.354 B) e `custodia_v398_geradores.py` (09:09, 24.352 B), escritos à mão; commit `35e8cdf6` (09:11:44); manifesto do site 09:15, ensaio de subida 09:15:53, subida em curso (`subidas\20261024_092423`). Li os dois scripts v398 (diff contra os v397; §2 e §3) e re-medi o espelho e o site (§8). Dos 58 arquivos da §7 só `gerar_estado_atual.py` mudou desde a minha leitura (remendado pelos geradores v398 às 09:09); os demais geradores fixos seguem idênticos.
- Esta especificação não toca nada disso. A v398, já resolvida à mão, vira o **teste de aceitação** de G1 (§6); o primeiro uso real fica para a v399.
- Não inscrevi esta tarefa na memória ACOM: o `init` escreveria no banco comum, fora do que o enunciado permite (só arquivos novos nas três pastas indicadas).

**Notação.** `N` = versão a custodiar (hoje v398); `P` = versão que está no espelho antes da custódia (hoje v397); `PIN16` = 16 primeiros hex do `sha256` de `um.py`. Atenção: `P` nem sempre é `N-1` (custódia conjunta v393+v394: o espelho passou de v392 a v394); `P` deve ser lido de `Um (absoluto) — Grande Atrator\um_absoluto_selo.json` do espelho (`um_version`) e conferido contra o diário (§E01).

**Variáveis usadas nos comandos** (os comandos são os das custódias v395–v397, extraídos do transcrito em `work\custodia_v396_22out\cadeia_v395_comandos.txt` e conferidos com a ordem dada para a v397):

```
PY="C:/Python314/python.exe -X utf8"
BANC="C:/IALD/Site/tgl/v3.0_bancada"          # ferramentas do site (tools\), revisoes\, subidas\, fragmentos\
SITE="C:/IALD/Site/tgl/v3.0"                  # fonte do site que sobe ao ar
TB="C:/IALD/Artigo/the_boundary"              # espelho (repositório git, branch main)
ESP="$TB/Um (absoluto) — Grande Atrator"      # pasta do artigo C dentro do espelho
NOS="C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
CEN="C:/IALD/Central de Patentes"
BK="C:/IALD/Artigo/the_boundary_BACKUPS"      # fora do repositório
```

## 1. Mapa dos passos (uma página)

Tempo [MEDIDO nos carimbos de início de cada chamada do transcrito da v395, 21/10 — logo, limites superiores]: do passo zero (20:59:41) ao leitor de IA (21:12:46), ~13 min de máquina; E02+E03 ≤ 6 min (21:00:09 -> 21:06:35, com a leitura da saída); E04 ≤ 9 s (21:06:35 -> 21:06:44); E05–E07 ≤ 13 s (21:06:44 -> 21:06:57); E08+E09 ≤ 61 s; E10–E12 ≤ 36 s; E13–E17 ≤ 130 s; E18 ≤ 122 s; E19 ≈ 4 s. [MEDIDO por data de modificação na v398, 24/10] passo zero 08:47:27; `custodia_v398_espelho.py` gravado 09:04 e `custodia_v398_geradores.py` 09:09 (cerca de 17 e 22 min depois do passo zero, escritos à mão); commit 09:11:44; manifesto do site 09:15; ensaio de subida 09:15:53; subida iniciada às 09:24.

| id | passo | script (cwd) | escreve em |
|---|---|---|---|
| E00 | gatilho e pré-condições | `tools\estado_do_organismo.py --sem-rede` (CEN) + checagens novas | `CEN\organismo\ESTADO_DO_ORGANISMO.{md,json}` |
| E01 | passo zero: backup de bytes de P, fora do repo | `tools/custodia_vN_passo0_backup.py` (BANC) | `BK\um_vP_<pinP>\` |
| E02 | espelho, modo conferir | `tools/custodia_vN_espelho.py --conferir` (BANC) | `BANC\revisoes\custodia_vN_espelho.json` (`modo:"conferir"`) |
| E03 | espelho, cópia | `tools/custodia_vN_espelho.py` (BANC) | `ESP\**`, `TB\cache\**`, `TB\fontes_pinadas` (via ESP), mesmo relatório (`modo:"copiar"`) |
| E04 | geradores: prosa da versão no espelho e no site | `tools/custodia_vN_geradores.py` (BANC) | `TB\tools\gerar_estado_atual.py`, `TB\LEDGER.md`, `TB\CITATION.cff`, `BANC\revisoes\arco_vN_texto.json`, `SITE\index.html`, `SITE\i18n.js` |
| E05 | ESTADO_ATUAL.md | `tools/gerar_estado_atual.py` (TB) | `TB\ESTADO_ATUAL.md` |
| E06 | varredura de arquivos sensíveis, `git add -A`, portas nº 1 | `tools/gerar_portas.py` (TB) | `PORTA.{md,json}` de toda pasta, `llms.txt`, `TUNEL.{json,md}`, bloco AS PORTAS do `README.md`, `tools\relatorio_portas.json` (ignorado) |
| E07 | geradores do site (bancada) | `gerar_read_brief`, `gerar_llms_site`, `gerar_head_camada_texto`, `gerar_secoes` (BANC) | `SITE\read-brief.md` + `TB\read-brief.md`, `SITE\llms.txt`, `BANC\fragmentos\*`, `SITE\secoes\*` + `TB\secoes\*` |
| E08 | laço portas <-> README | `gerar_portas.py` + `gerar_readme_frente.py` (TB), 2 voltas na v395 e na v397 | `TB\README.md`, `PORTA.*`, `TUNEL.*` |
| E09 | verificações do espelho | `verificar_portas.py`, `guarda_do_selo.py` (TB) | só stdout |
| E10 | commit do espelho | `git commit -q -F <mensagem>` (TB) | `.git` |
| E11 | push | `git push origin main` (TB) | GitHub |
| E12 | pós-push | `tools/pos_push.py` (TB) | só stdout (rede) |
| E13 | dados literais do selo no site | `tools/atualizar_dados_selo_site.py [--conferir]` (BANC) | `SITE\index.html`, `SITE\i18n.js` |
| E14 | aplicar o selo ao index | `tools/aplicar_selo.py [--conferir]` (BANC) | `SITE\index.html` |
| E15 | corpo inteiro e gêmeo Markdown | `gerar_llms_full.py`, `gerar_index_md.py` (BANC) | `SITE\llms-full.txt`, `SITE\index.md` |
| E16 | sitemap e manifesto de subida | `gerar_sitemap.py`, `gerar_manifesto.py` (BANC) | `SITE\sitemap.xml`, `BANC\revisoes\manifesto_vN.json` |
| E17 | subida em ensaio | `subir_site.py --manifesto ... --dry-run` (BANC) | `BANC\subidas\<stamp>_dryrun\RELATORIO.md` |
| E18 | subida | `subir_site.py --manifesto ...` (BANC) | ar (SFTP) + `BANC\subidas\<stamp>\{MANIFESTO_SUBIDA.json,estado_antes.json,antes\,RELATORIO.md}` |
| E19 | leitor de IA (R1) | `leitor_ia.py --relatorio ...` (BANC) | `BANC\revisoes\leitor_ia_<data>_vN.md` |
| E20 | medição final do organismo | `estado_do_organismo.py` (CEN) | `CEN\organismo\*` |

**Dependências duras** [LIDO]: E04 precisa do relatório `modo:"copiar"` de E03; E05 lê a `gerar_estado_atual.py` já remendada em E04; E06 só enxerga com `git ls-files` o que já foi `git add`; E07 lê `PORTA.json`/`TUNEL.json` de E06; `gerar_readme_frente` lê `PORTA.json`/`TUNEL.json`/`LEDGER.md`/core; E13 precisa de `BK\um_<versão do "Current seal" do index>_<pin>\` e de `revisoes\arco_vN_texto.json` (E04); E15–E16 leem o espelho já empurrado.

## 2. Passo a passo

Em cada passo: **Comando** (o de hoje, copiável) · **Muda por versão** (e de onde sai) · **Saídas** · **Idempotência** (como saber que já foi aplicado) · **Gates** · **Prosa à mão** (remete ao catálogo da §3).

### E00 — gatilho e pré-condições

**Comando (leitura):** `cd "$CEN" && $PY tools/estado_do_organismo.py --sem-rede` — rc 0 tudo OK, 1 defasagem, 2 falha de leitura [LIDO]; só grava o próprio quadro (`CEN\organismo\ESTADO_DO_ORGANISMO.{md,json}`).

**As três marcas** (ordem do operador de 23/10: «pode custodiar sempre que o handoff aparecer, como regra»; teste em `estado_do_organismo.py` l.96–112 [LIDO]):
1. `NOS\um_absoluto_selo.json`: `um_version` = N **e** `sha256["um.py"][:16]` = `sha256(NOS\um.py)[:16]`; se o `um.py` do Nós difere do pino, o medidor diz `EM_OBRA` e a custódia **espera**.
2. `NOS\MEMORIA_DA_LINHAGEM.md`: a última linha `^## [^\n]*\*\*(vNNN) SELADA` é N (o regex de hoje fixa `v3\d\d`: lacuna L15).
3. `NOS\HANDOFF_vN_CUSTODIA.md` + `NOS\rodada_vN_stdout.txt` + pasta `CEN\work\cadeia_de_selo\vN`.

**Pré-condições que a esteira de hoje NÃO testa** [PROPOSTA — cada uma falha com a lista do que falta, nunca em silêncio]:
- `git -C "$TB" fetch` ; `git -C "$TB" status --porcelain` vazio ; `HEAD` = `origin/main`. (O `git add -A` de E06/E08 varre tudo: meio-trabalho alheio entraria no commit.)
- Trava exclusiva: arquivo `BK\.custodia_lock.json` {pid, N, hora}; recusar se existir e for recente. Concorrência é real: durante esta leitura outra sessão custodiou a v398 nesta árvore (L13).
- `ESP\um_absoluto_selo.json` → `um_version` = P, P < N, e `PIN[P]` do diário = `sha256(ESP\um.py)[:16]`.
- Insumos que E03 exigirá: `CEN\work\cadeia_de_selo\vN_kernel\`, `DIFF_v{N-1}_vN.diff`, `DIFF_KERNEL_vN.txt` (em `cadeia_de_selo\vN` e, se houver, em `vN_kernel`), os 3 recibos B(n) (E03, bloco abaixo), e no `um.py` os dicionários `_VK_FONTES`/`_VK_VERBATINS2` de K = 392..N.
- Existência (sem ler o conteúdo) dos arquivos privados que E03 e E08 exigem e do `.env` de credenciais do site (E18); todos ficam fora de qualquer repositório.
- Python 3.14, `git`, rede (E12, E17–E19); `gh` é opcional (L12).
- Se o Nós já tiver selo N+1 > N (custódia atrasada): o alvo passa a ser a versão mais nova, em custódia conjunta (precedente v393+v394); sem isso `gerar_read_brief.py` para com «espelho != canônico» (a menos de `--espelho-atras-do-canonico`, E07).

**Saída:** `START`, `WAIT` (EM_OBRA) ou `STOP` + lista. **Idempotência:** `ESP\um_absoluto_selo.json.um_version` >= N e E20 sem `DEFASADO` nas superfícies «Espelho», «Espelho (GitHub raw)», «Site (fonte)», «Site (ar)» ⇒ nada a fazer.

---

### E01 — passo zero: backup de bytes de P, fora do repositório

**Comando:** `cd "$BANC" && $PY tools/custodia_vN_passo0_backup.py` (`tail -6` no transcrito).

**Muda por versão** [diff v395→v396→v397 e v397→v398; 8 trechos, todos mecânicos]:

| onde | v396 | v397 | v398 (outra sessão, hoje) | fonte para G1 |
|---|---|---|---|---|
| docstring l.2 | «CUSTÓDIA v396 (22/10, handoff v396; molde v395…)» | «v397 (23/10 … regra do operador de 23/10…)» | «v398 (24/10 …)», **com erro de cópia no elo v396** («21/10 … molde v394»; o certo é 22/10, molde v395) — L19 | f-string (PRO-01) |
| l.70 `SEMENTES + ("vP",)` | `"v395"` | `"v396"` | `"v397"` | P |
| l.77 `assert pin_esp == PIN["vP"]` e a mensagem | v395 | v396 | v397 | P; `PIN[P]` ← diário |
| l.78 `dest = BK / ("um_vP_" + pin_esp)` | `um_v395_` | `um_v396_` | `um_v397_` | P, `pin_esp` |
| l.79 `man["versao"]` | v395 | v396 | v397 | P |
| l.80 `man["regra"]` «(custódia vN; molde da custódia vP)» | v396 / v395 | v397 / v396 | v398 / v397 | N, P (PRO-02) |
| l.81 `man["gerador"]` `…/custodia_vN_passo0_backup.py` | v396 | v397 | v398 | N (PRO-03) |
| l.133 comentário final | `# v395: nenhuma semente` | `# v396: …` | `# v397: …` | P |

Lido do disco, não digitado [LIDO]: `PIN` ← `NOS\MEMORIA_DA_LINHAGEM.md` (regex `^## [^\n]*\*\*(v3\d\d) SELADA[^*\n]*\*\*[^\n]*\n`; o sha16 sai do cabeçalho entre crases desde a v387); `pin_esp` ← `sha256(ESP\um.py)`; selo do espelho.

**Saídas:** `BK\um_vP_<pinP>\` = cópia byte a byte de `ESP\**` exceto `PORTA.md`, `PORTA.json`, `bancada\`, `cache\`; mais `BACKUP_MANIFEST.json` {`versao`, `um_py_sha16`, `origem`, `data_backup`, `regra`, `gerador`, `excluidos`, `arquivos{rel:{bytes,sha256}}`, `n_arquivos`, `conferido_contra_origem`}. Escreve só em `BK`.

**Idempotência.** `copia_bytes` pula arquivo igual por tamanho e sha; o manifesto é regravado (muda `data_backup`). Marca [PROPOSTA]: existe `BK\um_vP_*` com manifesto `conferido_contra_origem == true`, `versao == "vP"` e `sha256(<backup>\um.py)[:16] == PIN[P]` ⇒ pular. **Não rodar depois de E03:** o assert `pin_esp == PIN["vP"]` falha (o espelho já está em N) — L14.

**Gates (assert; saem com traceback):** `PIN[P]` existe no diário · `pin_esp == selo_esp.sha256["um.py"][:16] == PIN[P]` · backup relido == origem (`div == []`) · não existem `um_v360_*` nem `um_v382_*` (`PULADAS`) · `SEMENTES = ()`.

**Prosa à mão:** PRO-01, PRO-02, PRO-03 (todas viram f-string; a «cadeia de moldes» da docstring é só história e pode sair: o mapa de rotas e `work\custodia_v*` já a guardam).

---

### E02 — espelho em modo conferir (usado antes da cópia)

**Comando:** `cd "$BANC" && $PY tools/custodia_vN_espelho.py --conferir 2>&1 | tail -12`.

**O que faz:** roda os itens 1–3 de E03 (passo zero, selo/rodada/gate/kernel, varredura de material privado) e grava `revisoes\custodia_vN_espelho.json` com `modo:"conferir"` e `copiados:null`. Não copia nada.

**Idempotência:** sempre seguro, **mas sobrescreve o relatório de E03**: se rodar depois da cópia, o assert `REL["modo"] == "copiar"` de E04 falha. Ordem fixa: E02 antes de E03.

**Gates:** os mesmos de E03 até a varredura (G-esp-1 a G-esp-10 e G-esp-14).

---

### E03 — espelho: cópia

**Comando:** `cd "$BANC" && $PY tools/custodia_vN_espelho.py 2>&1 | tail -6` (sem flag). Última linha: `4) espelho: {tipo: n} | kernel: k copiados, o órfãos removidos | um.py do espelho = <pin> | relatório …`.

**Muda por versão** [diff v396→v397; 9 pontos]:

| onde (v397) | v396 | v397 | fonte para G1 |
|---|---|---|---|
| l.2 docstring | … | … | PRO-04 (texto livre; a lista entre parênteses sai de `_VN_FONTES`) |
| l.49 `REL` | `custodia_v396_espelho.json` | `custodia_v397_espelho.json` | N |
| l.51 `VERSAO` | `"v396"` | `"v397"` | `selo["um_version"]` |
| l.52 `STDOUTS` | `…"v396")` | `…"v396", "v397")` | v383..N menos `PULADAS` |
| l.108 e l.111 backup | `um_v395_*` e `"v395"` | `um_v396_*` e `"v396"` | P |
| l.294–300 bloco DIFF | `DIFF_v395_v396.diff`, `DIFF_KERNEL_v396.txt` → `diferencas_v396\` | `DIFF_v396_v397.diff`, `DIFF_KERNEL_v397.txt` → `diferencas_v397\` | N e N-1; em `CEN\work\cadeia_de_selo\vN` e `vN_kernel` |
| l.310 e l.312 `_dic` (duas listas de nomes) | até `_V396_FONTES` e `_V396_VERBATINS2` | até `_V397_*` | regex sobre o `um.py` (abaixo) |
| l.382–392 bloco `_H` | `_H396` = `49e723b412fcdb11`, `7a9cacaddc7744f1`, `0a594bac20bf5874` | `_H397` = `776ce2ae5959867e`, `fa1fc15fcd598591`, `40ba026b5735558a` → `recibos_bancada_v397\` | handoff §«O elo B(n)» e sha16 dos 3 arquivos (abaixo) |

Dicionários do `um.py` [MEDIDO, 0,2 s, regex sem `ast.parse`]: `^(_V\d{3}_(?:FONTES|VERBATINS2))\s*=` acha o par completo para K = 392..398; G1 deve exigir o par para todo K de 392 a N e montar `_dic` e o `set` do assert a partir disso.

**Os 3 recibos B(n)** [MEDIDO]: o sha16 digitado em `_H397` (copiado do handoff) é exatamente o `sha256[:16]` de `CEN\work\cadeia_de_selo\v397\bancada_B3\RECIBO_SINCRONIZACAO_v397_20261023_171531.json`, de `…\bancada_B3_servico\RECIBO_PARADA_v397.json` e de `…\RECIBO_RELIGAMENTO_v397.json`. O mesmo vale para a v398 (`0f306c551a2ccbee`, `a3339191387ad9df`, `12354ad5c5ac52f2`). Logo o hash não precisa ser digitado: calcular dos 3 arquivos (pasta `vN`, nomes por padrão, caminhos com `ensaio` excluídos) e conferir contra o parágrafo do handoff «O elo B(n) da Bancada Um» (recibo da aplicação com o nome do arquivo e `sha256`, depois parada e religamento).

**Confirmação na v398** [MEDIDO, diff v397→v398 do espelho]: os 9 pontos da tabela mudaram exatamente assim (`REL`, `VERSAO`, `STDOUTS`, backup, bloco DIFF, `_dic` duas vezes, bloco `_H398`, docstring). O único acréscimo novo foi excluir também `bateria_pre_selo` do filtro dos recibos (existe `cadeia_de_selo\v398\bateria_pre_selo\ensaio_1\RECIBO_SINCRONIZACAO_v397_*.json`, que não é recibo da versão); `_H398` foi digitado do handoff. Logo o filtro por nome de pasta é frágil: o critério certo é o nome do arquivo (`RECIBO_SINCRONIZACAO_vN_*`, `RECIBO_PARADA_vN`, `RECIBO_RELIGAMENTO_vN`) dentro de `bancada_B3\` e `bancada_B3_servico\`.

**Já dinâmico (não muda o código)** [LIDO]:
- selo e core do Nós: o mapa `sha256` do selo dá a lista de artefatos selados e o destino por pasta; também `rite_checkpoints` e `qg_closure_verdict`;
- `tgl_kernel_proof_manifest.json` e `NOS\tgl_kernel\`; `rodada_v*_stdout*.txt` (sem `tentativa`); `tgl_kernel_*capture*.txt`;
- `CEN\Chatgpt\TUNEL` (arquivos de 1º nível e `.md` de 2º nível; muda todo dia);
- `cache\` (`d1_camb\v3`, `diamante_rede`, `auditoria`, `bancada_30set`, `bancada_01out` e 4 arquivos soltos);
- `quantum_pillar\` (worker, spec e 2 rodadas fixas) e `Bancada_Um\investigacao\preregistro_*` (3 + 3 pastas);
- ORD, P391 e C13 (v390 a v392): **congelados**, com sha16 digitados e conferidos por assert;
- `fontes_pinadas\`: todo caminho absoluto dos dicionários `_VK_FONTES` e `_VK_VERBATINS2`; só entra se o `sha256` bate com o pino do `um.py`; fonte idêntica a algo já no git não duplica, o mapa aponta a cópia.

**Saídas:**
- Em `ESP\`: `um.py`; selados; DECLARADOS (`um_absoluto_selo.json`, `um_absoluto_pt.txt`, `um_absoluto_en.txt`, `A_PROVA_DA_QG_TGL_arvore.md`, `DESENHO_DO_FECHAMENTO_QG.md`, `MEMORIA_DA_LINHAGEM.md`, `O_FECHAMENTO_ESTRUTURA.md`, `NOTA_DE_CUSTODIA.md`); `rodadas\`; `Lean\tgl_kernel\` (cópia por hash do manifesto, `.lean` órfão removido); `diferencas_vN\`; `recibos_bancada_vN\`; `fontes_pinadas\` com `MAPA_FONTES_PINADAS.json`; `quantum_pillar\`; `preregistro_*`; `superposicao_passagem_v390\`; `estatuto_da_prova_v391\`; `cunhagens_13out_v392\`; `bancada\TUNEL\`.
- Em `TB\cache\`.
- `BANC\revisoes\custodia_vN_espelho.json` com `modo:"copiar"`; chaves: `selo` (pin16, pin, bytes_um_py, timestamp, result_hash, gate, gate_identico_ao_espelho, rodada, teoremas_limpos, campos_com_CONFIRMED_a_ler, bandeiras, kernel, selo_esp_campos_novos), `passo_zero`, `varredura_privada`, `fontes_pinadas`, `copiados`, `kernel_copiados`, `kernel_orfaos_removidos`, `nao_levados`.
- **Não toca** em `README.md`, `ESTADO_ATUAL.md`, `LEDGER.md`, `CITATION.cff`, `PORTA.*`, `llms.txt`, `TUNEL.*`, `read-brief.md`, `secoes\`.

**Idempotência.** `copia_bytes` (temporário `*.tmp_custodia`, depois `replace`) pula arquivo igual; o script aceita rerodar com o espelho já em N (imprime «RERODADA: já na nova»). Marca [PROPOSTA]: relatório com `modo=="copiar"`, `selo.pin16 == PIN16` e `sha256(ESP\um.py)[:16] == PIN16`.

**Gates (todos `assert` ⇒ rc 1) [LIDO]:**
- G-esp-1: `pin_esp in (selo_esp.um.py[:16], pin)`.
- G-esp-2: existe **um** `BK\um_vP_*` com `conferido_contra_origem` e `versao == "vP"`.
- G-esp-3: não há pastas de semente `um_v360_*` nem `um_v382_*`.
- G-esp-4: o arquivo privado de marcadores existe (`assert PRIV`); a guarda de 7 termos sozinha é tida como fraca.
- G-esp-5: `fail_closed_selftest == FAIL_CLOSED_SELFTEST_PASSED`.
- G-esp-6: todo artefato do mapa `sha256` do selo existe no Nós com o hash do selo.
- G-esp-7: rodada completa (`rite_checkpoints.switch_on is False` e `reused == 0`).
- G-esp-8: `qg_closure_verdict` do Nós == o do selo do espelho; se mudou, PARAR E AVISAR (decisão do operador).
- G-esp-9: kernel sem arquivo ausente ou divergente do manifesto e com 0 declarações fora do trio.
- G-esp-10: `teoremas limpos: a/b` do stdout com `a == b`.
- G-esp-11: hashes congelados de ORD, P391 e C13.
- G-esp-12: `set(_dic) == {…}`.
- G-esp-13: os 3 recibos achados por sha16.
- G-esp-14: varredura de material privado: nenhum termo-guarda a mais que no espelho em artefato do programa (em `TUNEL` e `FONTE_TUNEL` o arquivo é só pulado e dito).
- Só imprime, não bloqueia: campos do selo com a palavra CONFIRMED (`campos_com_CONFIRMED_a_ler`) — L09.

**Prosa à mão:** PRO-04, PRO-05 (comentários `# vN:`), PRO-06 (mensagens de assert), PRO-18 (`nao_levados`, estático).

---

### E04 — geradores: a prosa da versão (espelho e fonte local do site)

**Comando:** `cd "$BANC" && $PY tools/custodia_vN_geradores.py 2>&1 | tail -10`. Última linha: `OK: geradores, LEDGER, CITATION (selo corrente), site (arco vN) | (sha16, 'a/b') | bandeiras novas: k | …`.

**O que faz** — seis escritas, cada uma por `patch(p, pares, rot, marca, exige_crescer=True)` [LIDO]: lê os bytes; se a `marca` já está no texto, imprime «já aplicado» e sai; senão grava `<arquivo>.bak_<TS>` ao lado, detecta CRLF e converte `\n` em `\r\n` nas trocas, exige `s.count(old) == 1` em cada troca, grava `*.tmp` e substitui; exige que o arquivo tenha crescido (exceto o CITATION).

| # | alvo | operação | âncora | marca de idempotência |
|---|---|---|---|---|
| a | `TB\tools\gerar_estado_atual.py` | insere, junto à âncora (DEPOIS dela até a v397; ANTES dela na v398), o bloco de código `# custódia vN (dd/mm/2026, sessão a7 da Central)`: título `### vN · the custody`, linha da tabela (sha16 e rito lidos do diário na hora de gerar), `TXT`, `NOTA`, `ERR` e, quando existe, o parágrafo pronto do handoff | v396 e v397: a única linha com «Errata beside (dd/mm/2026, the custody of vP» (assert `len == 1`). **v398: o par de linhas `L.append("")` e `L.append("## What is PROVED …")`** (âncora trocada à mão para o parágrafo da v397 não ficar sob o bloco da v398; assert `count == 1`) | `"custódia vN (dd/mm/2026"` presente no arquivo |
| b | `TB\LEDGER.md` | insere o bloco `### The custody — vN (COMPLETE round)` antes de `\n## What is closed / What remains open` | essa linha de título | `"### The custody — vN (COMPLETE round)"` |
| c | `TB\CITATION.cff` | troca por regex as duas descrições do selo corrente: `(vP on <data>; the Zenodo deposit holds v392)` e `the pin of um.py at vP … (<bytes> bytes; sealed <ts>)` | regexes com `vP` | `"(vN on"` |
| d | `BANC\revisoes\arco_vN_texto.json` | grava {gerador, pin16, en, pt} | – | arquivo existe |
| e | `SITE\index.html` | insere `<div><span data-i18n="art.c.cl.arcN">EN</span></div>` depois do div do arco anterior | o texto EN exato de `arco_vP_texto.json` | `data-i18n="art.c.cl.arcN"` |
| f | `SITE\i18n.js` | insere `'art.c.cl.arcN': '…'` (en e pt: 2 ocorrências) depois do arco anterior | `'art.c.cl.arcP': '<texto exato>'` | `'art.c.cl.arcN'` |

**Efeito colateral a notar:** (e) e (f) alteram a **fonte local do site antes de qualquer subida**; se a esteira parar depois de E04, o medidor passa a acusar «fonte mais nova que a última subida» (comportamento correto, mas é estado intermediário visível).

**Muda por versão** — o script inteiro é reescrito à mão a cada custódia. [MEDIDO] Não existe `derivar_geradores_*.py` nas pastas `work\custodia_v39*` (só `derivar_passo0`, `derivar_espelho`, `derivar_central`); passo zero e espelho são derivados por trocas contadas, os geradores não. Itens que variam (diff v395→v396→v397):
1. Docstring: sessão, data, a ordem do operador citada verbatim, nome do handoff (PRO-07).
2. `BK<P>` com o PIN16 de P digitado no caminho (`…\um_v396_0a4395a89eeebbb7`).
3. `REL` e `REL["versao"] == "vN"`; `selo.get("um_version") == "vN"`.
4. `assert SEL["kernel"]["novos"] == [...]`: lista digitada dos módulos (v396 `TGLExt/TestemunhaEstatica.lean`; v397 `TGLExt/Token.lean`; a v398 tem 2 módulos).
5. Nomes dos registros: `core["<nome>_vN"]` mudam de versão a versão (`psibit_v395`, `testemunha_estatica_v396`, `teste_de_veracidade_fase9_v397`); `cunhagens_vN` e `kh_n1_cobertura_vN` são fixos. `novos == [...]` digitado (v397: 3 registros; v398: 4, `afinacao_das_cordas_v398`, `cunhagens_v398`, `kh_n1_cobertura_v398`, `sonico_v398`).
6. Bandeiras novas digitadas (`NBAND == 1 and … == ["ext_tok397_0001"]`; a v398 tem 40).
7. Asserts de forma específicos de cada registro (`unconditional`, `fock_face`, `conditional_psion_face`, `mechanics`, `lido`, `checks`…): os registros novos não compartilham o mesmo desenho.
8. Contagens digitadas: `NCUN == 3/4/6`, `NCHK == 35`, `NTERM == 19`, `NSUP == 8`, `NMEC == 14`, `len(CONTRATOS) == 5` (v398: 7 contratos com `expected_ladder`).
9. Escada digitada na v395/v396 (`TEOR == "9451/9451"`, `"9498/9498"`, `KERNEL_9451_OF_9451_FLAGS`); a v397 já lê.
10. `FRASE` verbatim digitada (v397) em vez de lida do core.
11. Os textos `TXT`, `ERR`, `NOTA`, `BLOCO`, `EN`, `PT` (PRO-08 a PRO-14) e o texto de ligação do commit.
12. Âncora `Errata beside (dd/mm/2026, the custody of vP`; regex do CITATION com `vP`; chaves `art.c.cl.arcP` e `arcN`; `arco_vP_texto.json`.
13. Constantes digitadas do depósito Zenodo: o DOI `10.5281/zenodo.23366324` (5 linhas do script), o pino `b590c0aa80055e2a…` (2 linhas) e «holds v392» (6 linhas) (L16).
14. «sessão a7 da Central» e a data, digitadas em comentários e no `BLOCO` (PRO-11, PRO-15).
15. [MEDIDO na v398] a forma dos registros também muda: a cobertura do kernel passou a ser lida de `kh_n1_cobertura_v398["lido"]["constantes_cobertas"]` e `["teoremas_cobertos"]` (na v397 saía por regex do `verdict`); G1 deve aceitar as duas formas ou ler da fonte primária (manifesto do kernel).
16. [MEDIDO na v398] a errata dos contratos lista os 7 contratos com `expected_ladder` (`len(CONTRATOS) == 7`, inclusive os dois que nascem na v398), enquanto o handoff diz «cinco contratos»: a contagem do handoff e a do `um.py` divergem; o invariante útil é «todo contrato tem `expected_ladder == ESC` depois da troca».

**Entradas lidas (de onde saem):** relatório de E03; selo do Nós (`um_version`, pino, `timestamp`, `bytes_um_py`); core do Nós; core de P lido de `BK\um_vP_<pinP>\um_absoluto.json` (backup de E01 — dependência E01→E04); diário (bloco `vN SELADA`: sha16 do cabeçalho e `**a/b**` da escada); `HANDOFF_vN_CUSTODIA.md` (parágrafo entre marcadores); `CEN\work\custodia_vN_*\fatos_vN.json` (`contratos_expected_ladder`; **dependência cruzada com a perna 2**); `NOS\tgl_kernel\TGL\GravitonShadow.lean` (só v396).

**Gates (assert):**
- `REL.modo == "copiar"`, `copiados` não nulo, `versao == "vN"`; `selo.sha256["um.py"] == PIN` e `um_version == "vN"`.
- `_ok(registro)` para cada registro novo: `all_verified is True`, `does_not_gate_core is True`, veredito com `GATE_UNMOVED` ou `GATE_UNTOUCHED`, sem CONFIRMED (salvo `NOT_CONFIRMED` e `NOT_A_CONFIRMATION`).
- Registros novos e bandeiras novas == listas esperadas; contagens (item 8).
- Escada: `P1.n_theorems_clean/n_theorems_expected == TEOR`, `P1.declaracoes_auditadas == TERMOS`, `KERNEL_%d_OF_%d_FLAGS` no veredito do estatuto.
- `kh_n1`: veredito casa `CLOSURE_(\d+)_CONSTANTS_(\d+)_THEOREMS_NONE_OUTSIDE_THE_TRIO` com constantes == TERMOS; as erratas citam «piso» e «h8».
- Todo contrato tem `expected_ladder == ESC`.
- Parágrafo pronto: cada número do registro (`%.2f` etc.) aparece no texto, a frase verbatim e o sha16 `9b182958a5a7a1bc` estão no parágrafo, sem CONFIRMED.
- Diário: sha16 e escada == PIN16 e TEOR.
- Textos do arco: sem `'`, `<`, `\` nem quebra de linha; EN sem CONFIRMED; PT sem CONFIRMADA fora de «PROVADA ≠ CONFIRMADA».
- `patch()`: `count == 1` em cada troca e crescimento do arquivo.

**Prosa à mão:** PRO-07 a PRO-15. **Ordem:** E04 antes de E05 e de E13.

---

### E05 — ESTADO_ATUAL.md

**Comando:** `cd "$TB" && $PY tools/gerar_estado_atual.py 2>&1 | tail -1`. Saída: `ESTADO_ATUAL.md: vN pin <16> | kernel f/t | rito a/b | n linhas`.

**Muda por versão:** nada no código (a não ser o bloco `custódia vN` que E04 acabou de inserir). Lê do **espelho** (não do Nós): selo, `um_absoluto.json`, `Lean\tgl_kernel_proof_manifest.json`, `um.py`, `rodadas\rodada_v*_stdout.txt` (a mais nova define a versão; o rito sai de `(\d+)/(\d+) teoremas`), `MEMORIA_DA_LINHAGEM.md` do espelho (cópia de E03), `CITATION.cff` (linha «Zenodo deposit of vNNN, deposited AAAA-MM-DD (byte-identical to the seal: um.py sha256 …» e `doi:` — `SystemExit` se faltar), e `tools\estatuto_tres_apoios.py` (que relê core, selo e `um_absoluto_en.txt`).

**Saída:** `TB\ESTADO_ATUAL.md` (escrita por temporário; o tamanho da página, em KB, é medido depois de montada — marcador `__KB_DESTA_PAGINA__`).

**Idempotência:** determinística para o mesmo disco (sem data/hora no corpo). Marca: o arquivo contém `PIN16` e `### vN · the custody`.

**Gates:** `rito != "?"`, `sujos == 0` (axiom_report fora do trio), CITATION com a linha do depósito, o estatuto recusa se um invariante do core não bate.

**Atenção:** este arquivo cresce a cada custódia (L02).

---

### E06 — varredura de arquivos sensíveis, `git add -A`, portas nº 1

**Comando (como está no transcrito):**
```
cd "$TB" && git status --porcelain --untracked-files=all | grep -i -E "\.bak|\.tmp|\.env|auth\.json|\.pem$|\.key$|<nomes dos dois stacks confidenciais da casa>" | head -5 ; git add -A && $PY tools/gerar_portas.py 2>&1 | tail -2
```
A varredura usa `;` e `head -5`: **imprime, não bloqueia** (L09). O `.gitignore` já ignora `*.bak_*`, `cache/*` (com exceções), `tools/relatorio_portas.json`, `__pycache__/`; **não** ignora `*.tmp` nem `*.tmp_custodia` (resíduo de falha de E03 entraria no commit).

**`gerar_portas.py`** [LIDO]: sem argumentos; lê `git ls-files -z` (portanto só enxerga o que foi `git add`ed), `selo`, `Lean\tgl_kernel_proof_manifest.json`, `um.py` (versão da última pedra em `_ESQUELETO_STONES`), `CITATION.cff` (depósito) e o módulo do estatuto (lido ANTES de escrever: se recusar, nada se grava). Escreve `PORTA.md` e `PORTA.json` em **toda** pasta rastreada, `llms.txt`, `TUNEL.json` e `TUNEL.md` na raiz, o bloco entre `<!-- PORTAS:INI -->` e `<!-- PORTAS:FIM -->` do `README.md` (antes do hash, para a porta não mentir sobre o README) e `tools\relatorio_portas.json` (ignorado). Saída final `OK`/`FALHOU` e rc 0/1 conforme URLs que não resolvem.

**Muda por versão:** nada no código; a versão do selo sai de `selo["um_version"]` (campo `versao_do_selo`) e a «confirmada por transcrição» da última `rodadas\rodada_vNNN_*` rastreada (**fail-closed** se não houver nenhuma).

**Idempotência:** NÃO é byte-idempotente: cada `PORTA.json`/`TUNEL.json` grava `gerado_utc` com segundos (l.841, 1006, 1647) e o rodapé dos `PORTA.md` leva a data UTC [MEDIDO: o commit da v397 tocou 433 arquivos, 87.320 inserções]. É idempotente no conteúdo, exceto por esses carimbos — o teste de ponto fixo de E08 precisa normalizá-los.

**Gates:** o selo está no `git ls-files`; existe transcrição de rodada; todas as URLs geradas resolvem em arquivo rastreado (rc 1 se não). **Só imprime:** `[ATENCAO] o sha256 de um.py em disco DIFERE do pin do selo` (`pin_confere_com_disco` falso) — não bloqueia (L09).

---

### E07 — geradores do site (bancada), lendo o espelho já «portado»

**Comando (como no transcrito, cwd BANC):**
```
for f in gerar_read_brief gerar_llms_site gerar_head_camada_texto gerar_secoes; do $PY tools/$f.py 2>&1 | tail -1 | cut -c1-200; done
```
O laço **esconde o rc** de cada script (`tail`): um gerador que falha passa batido se for o do meio (L09).

| script | lê | escreve | opções |
|---|---|---|---|
| `gerar_read_brief.py` | `TB\TUNEL.json`, `PORTA.json`, selo e core do espelho, `ESTADO_ATUAL.md`, `CITATION.cff`, `NOS\um.py` (só para conferir nomes de função) | `SITE\read-brief.md` e `TB\read-brief.md` (mesmos bytes; `.bak_<STAMP>` de cada) | `--conferir` (HEAD em toda URL, rc 1 se falhar), `--espelho-atras-do-canonico` |
| `gerar_llms_site.py` | `TUNEL`, `PORTA`, selo, `SITE\secoes\*`, `BANC\central_publica\acom\um_acom_info.json` (**perna 3**) | `SITE\llms.txt` | `--conferir` |
| `gerar_head_camada_texto.py` | `TUNEL`, `PORTA`, selo, `CITATION.cff` | `BANC\fragmentos\head_camada_texto.html` e `jsonld_camada_texto.json` (não publicados) | – |
| `gerar_secoes.py` | `BANC\tools\secoes_fatias.json` (estático: 8 sínteses EN/PT, a última edição é de 07/10), arquivos do espelho por marcadores literais únicos, `um.py` (tabela `prove_*`) | os mesmos bytes em `TB\secoes\` e `SITE\secoes\`: 8 partes, `selo-cartao.md`, `um-py-funcoes.tsv` | `--conferir` (rc 1 se difere) |

**Muda por versão:** nada no código — tudo sai do selo, de `PORTA.json`/`TUNEL.json`, do estatuto e do `ESTADO_ATUAL.md` (o rito, por regex `\*\*(\d+)/(\d+) clean\*\*`). Nenhuma prosa por versão [MEDIDO: `grep` de `v39x`, `PARAGRAFO`, `teste_de_veracidade` nesses 4 arquivos e nos de E13–E16 não acha nada].

**Gates principais:** pino igual em selo, TUNEL e PORTA; pino do selo do **Nós** == pino do espelho (senão `assert`; com `--espelho-atras-do-canonico` vira aviso); β == α·√e (1e-12); as 8 partes iguais no site e no espelho; `selo-cartao.md` existe; nenhum termo proibido; `CONFIRMED` e `NOT_FALSIFIED` presentes e nenhuma frase «gravidade quântica confirmada»; Read Brief ≤ 30 KB; fatia ≤ 30 KB e trecho ≤ 4000 B; cartão ≤ 12 KB.

**Idempotência:** reescrevem sempre e gravam novo `.bak_<STAMP>` mesmo sem mudança (acumulam backups no site); conteúdo estável para o mesmo disco. Marca: o arquivo contém `PIN16` e, no read-brief, é idêntico nos dois lados.

**Defeito de ordem medido (L04):** `gerar_read_brief.py` e `gerar_llms_site.py` rodam **antes** de `gerar_secoes.py` e antes do ponto fixo do README, mas citam os bytes lidos do `TUNEL.json` de E06.

---

### E08 — laço portas ⇄ README (2 voltas no transcrito da v395 e na ordem dada para a v397)

**Comando (como no transcrito):**
```
cd "$TB" && git add -A && $PY tools/gerar_portas.py 2>&1 | tail -1 && $PY tools/gerar_readme_frente.py 2>&1 | tail -1 | cut -c1-200 \
 && git add -A && $PY tools/gerar_portas.py 2>&1 | tail -1 && $PY tools/gerar_readme_frente.py 2>&1 | tail -1 | cut -c1-120 \
 && git add -A && echo "unstaged: $(git diff --name-only | wc -l) | staged: $(git diff --cached --name-only | wc -l)"
```
**`gerar_readme_frente.py`** [LIDO, 297 linhas]: sem argumentos. Lê `PORTA.json`, `TUNEL.json`, selo, `LEDGER.md` (seções copiadas **verbatim** pelo título: `Abstract`, `✦ The core on one page`, `Citing This Work`, `License`, `Author`), o bloco `PORTAS:INI/FIM` que está no README, `CITATION.cff` (depósito), `estatuto_tres_apoios`, o core selado do espelho (registro `teste_de_veracidade_fase9_v\d+` mais novo) e o git (`git log --diff-filter=A … LEDGER.md`; `git show <commit>:LEDGER.md`). Exige um arquivo privado de termos proibidos (fora do repositório; `SystemExit` se faltar). Grava `README.md.bak_<STAMP>` (ignorado) e `README.md` (LF, por temporário).

**Muda por versão:** no código, nada em si — mas o item do 4,44 (l.255–268) foi **remendado à mão na v397** por três scripts em `work\custodia_v397_23out\` (`patch_readme_v397.py`, `…b.py`, `…c.py`; trocas contadas, backup de bytes, `py_compile`) para a frente caber nos 40 KB; ver L01 e L03.

**Gates (assert/SystemExit):** pin igual em selo, PORTA e TUNEL; estatuto == PORTA/selo (versão, nº de arquivos e de termos, gate); nenhum termo proibido; `PORTAS:INI/FIM` uma vez cada; `CONFIRMED` e `NOT_FALSIFIED` presentes; **tamanho ≤ 40.960 B**; toda URL raw da frente está no TUNEL/PORTA.

**Idempotência:** o README leva a data local (`hoje`) no comentário `FRENTE:GERADA` e no rodapé: idêntico dentro do mesmo dia, diferente no dia seguinte. Marca: README contém `PIN16`.

**O que a ordem de hoje faz e por que 2 voltas** [LIDO/MEDIDO]: `gerar_portas` amarra o bloco AS PORTAS no README antes de hashear; `gerar_readme_frente` regenera a frente a partir de `PORTA/TUNEL` (que levam o tamanho/hash do README da volta anterior) e mantém o bloco; a volta seguinte reconcilia. É uma iteração de ponto fixo disfarçada de «rodar duas vezes».

**Defeitos medidos desta ordem (L04) — o mesmo defeito em duas custódias seguidas:**
1. Estado v397 (`bb2c392a`): `read-brief.md` (site e espelho) e `llms-full.txt` diziam README = **40.942** bytes (TUNEL e disco: **40.941**) e `secoes\04-o-gerador-e-o-piso-do-espectro.md` = **13.427** (TUNEL: **13.429**). `gerar_read_brief.py` (E07) roda depois da 1ª `gerar_portas`, antes das voltas do README e antes de `gerar_secoes`: cita bytes lidos de um TUNEL velho.
2. Estado v398 (`35e8cdf6`, 09:25): o README já confere, mas `secoes\07-o-programa-um-py.md` está citada como **11.762** (TUNEL: **11.731**) e `secoes\08-os-artigos-e-os-instrumentos.md` como **13.472** (TUNEL: **13.411**), em `read-brief.md` (site e espelho), em `llms.txt` do site e em `llms-full.txt`; só o `index.md` confere. São 2 de 10 citações no read-brief, 2 de 8 no `llms.txt` e 2 de 10 no `llms-full.txt` — e esses arquivos estão sendo subidos agora.
3. Medida: regex sobre «arquivo.ext … (N bytes» contra `TUNEL.json`; a lista dos arquivos defasados muda a cada custódia, o defeito é o mesmo.

**Ordem de dependência correta [PROPOSTA]:** `gerar_secoes` → `git add` → `gerar_portas` → `gerar_readme_frente` ⇄ `gerar_portas` até o README parar de mudar → `gerar_read_brief` + `gerar_llms_site` + `gerar_head_camada_texto` → `git add` → `gerar_portas` (hash final do read-brief) → verificações. Teste de ponto fixo: sha256 de {`README.md`, `ESTADO_ATUAL.md`, `read-brief.md`, `llms.txt`, `secoes\*`, `TUNEL.json` e `PORTA.json` **com `gerado_utc` e a data do rodapé normalizados**} igual entre duas passadas completas (teto de 4 passadas; senão STOP com a lista dos arquivos que oscilam). Mais um **auditor de números citados** (o que fiz à mão acima): para cada «arquivo (N bytes)» nas superfícies publicadas, N == `TUNEL.json`; divergência ⇒ falha.

---

### E09 — verificações do espelho

**Comandos:**
```
cd "$TB" && $PY tools/verificar_portas.py 2>&1 | tail -3 && $PY tools/guarda_do_selo.py 2>&1 | tail -4 | cut -c1-220
```
- `verificar_portas.py` (216 linhas, independente do gerador): toda URL raw/tree resolve e está rastreada; toda pasta rastreada tem as duas portas; «porta acima» existe e a cadeia fecha na raiz; toda subpasta é citada pelo pai; todo arquivo rastreado aparece em alguma porta; selo das portas == selo em disco; `sha256[:16]` de cada arquivo listado == disco; blob do git (`git cat-file --batch`) == porta. **Não tem código de saída**: a falha só aparece em `ERROS ... N` e `VEREDITO: FALHOU` (L08). Aprovação = `ERROS ........................ 0` e `VEREDITO: TODAS AS PORTAS RESOLVEM`.
- `guarda_do_selo.py` (148 linhas): para todo `um_absoluto_selo.json` do repositório, cada artefato do mapa `sha256` confere no disco **e** no blob do git (o que o raw serve); cópia de selo em `fontes_pinadas` é conferida pelo mapa. rc 1 em erro. Aprovação = `ERROS ........................ 0` e `VEREDITO: O QUE SE PUBLICA E O QUE O SELO DESCREVE`.

**Muda por versão:** nada. **Idempotência:** só leitura. **Gates:** os dois acima; ambos precisam passar antes de E10. **Prosa:** nenhuma.

---

### E10 — commit do espelho

**Comando:** `cd "$TB" && git commit -q -F "<arquivo da mensagem>" && git log -1 --format="%h %s" | cut -c1-110`. A mensagem é um arquivo escrito à mão a cada custódia (na v395 ficou no scratchpad da sessão: `commit_espelho_v395.txt`; nas outras não conferi onde) [LIDO no transcrito].

**Molde observado nos 3 commits** (`git log`, ASCII sem acentos): assunto `custodia(vN): <título em PT sem acento> - selo, modulo <Nome>, escada <A>/<B>, fontes pinadas da vN, PORTAS, README[ (<nota>)]`; corpo: `um.py vN <PIN16> (rodada COMPLETA, autoteste fail-closed; gate identico ao da vP).` · `Kernel <F> formais / <T> declaracoes auditadas, todas no trio; <K> bandeiras novas …` · `Backup da vP fora do repositorio (um_vP_<pinP>).` · `ESTADO_ATUAL, LEDGER e CITATION (selo corrente) ao lado …` + marcadores `-` com o que entrou · `PROVADA = validade; a creditacao segue recusada; o gate nao se moveu.` · linha `Co-Authored-By: <modelo da sessão>`.

**Muda por versão:** título, nome do módulo, escada, K, a lista de marcadores (PRO-16) e o autor do trailer.

**Idempotência:** `git log -1 --format=%s` começa por `custodia(vN):` e `git status --porcelain` está vazio.

**Gates:** `unstaged: 0` (impresso em E08, não afirmado por assert); PROPOSTA: nenhum arquivo staged casa os padrões sensíveis; a mensagem passa pela mesma varredura de termos proibidos dos geradores; E09 aprovado.

**Autoridade:** a regra de 23/10 manda custodiar sem perguntar; a memória diz que «a subida é da gerência»; os gates reservados ao operador (Zenodo, nome das pedras e dos registros, [LEGAL], reescrever histórico público) ficam de fora (L17).

### E11 — push

**Comando:** `cd "$TB" && git push origin main 2>&1 | tail -2`.

**Muda por versão:** nada. **Idempotência:** `git fetch` e `git rev-parse HEAD` == `git rev-parse origin/main`. **Gates:** rc do `git push`; sem `--force`. Autenticação é a do git da máquina (não lida).

### E12 — pós-push (o raw do GitHub serve o que o selo descreve)

**Comando:** `cd "$TB" && $PY tools/pos_push.py 2>&1 | tail -7 | cut -c1-200`.

**O que confere** [LIDO]: para cada artefato do mapa `sha256` do selo + `tgl_kernel_proof_manifest.json`, `um_absoluto_selo.json`, `README.md`, `llms.txt`, `ESTADO_ATUAL.md`: (1) `git rev-parse HEAD:<caminho>` == `sha` da API `contents` (o commit chegou); (2) `sha256` do raw == selo (ou disco); e o README raw contém `PIN16`. **Códigos:** 0 tudo confere; 1 divergência real; 2 o commit chegou mas o CDN ainda serve bytes velhos (repetir em minutos); 3 INCONCLUSIVO (a API anônima não respondeu e o raw serve o esperado). G1: repetir 2 e 3 com recuo, parar em 1.

**Muda por versão:** nada. **Idempotência:** só leitura pela rede; repetível sem efeito. O workflow `kernel.yml` do GitHub (build do kernel + auditoria dos termos, até 120 min, dispara quando muda `Lean/**`) **não é consultado** (L12).

---

### E13 — dados literais do selo no site (sem trocar de versão de site)

**Comando:** `cd "$BANC" && $PY tools/atualizar_dados_selo_site.py --conferir && $PY tools/atualizar_dados_selo_site.py`.

**Como decide** [LIDO]: os valores NOVOS saem de `TB\PORTA.json` (`versao_confirmada_por_transcricao`), do selo, do manifesto do kernel e da contagem de quebras de linha do `um.py` do espelho. Os valores ANTIGOS saem de `BK\um_<vant>_<pin>\`, onde `vant` e o pin vêm da nota «Current seal» do `SITE\index.html` (a nota que diz `Current seal:`, a versão em negrito e o pin). Troca 19 âncoras exatas (EN e PT, em `index.html` e `i18n.js`, cada uma com a contagem esperada) e insere a linha do arco se faltar (E04 já a inseriu).

**Muda por versão:** nada no código. O que muda são os valores lidos e a existência de `BK\um_<vant>_<pin>\` e de `BANC\revisoes\arco_vN_texto.json`.

**Idempotência:** «o site já está no selo do espelho — nada a fazer» (pin antigo igual ao novo). `--conferir` só mostra o que mudaria.

**Gates:** PORTA igual ao selo do espelho; o backup de `vant` existe; cada âncora aparece exatamente o número esperado de vezes (senão `FAIL-CLOSED: âncoras não conferem — nada gravado`); o texto do arco não tem aspa simples, quebra de linha nem a palavra CONFIRMED fora da régua; o arquivo novo tem pelo menos 98% do antigo.

**Atenção:** o site ficou parado na v392 por duas custódias (v393+v394 e v395) porque este passo não rodava (rota `custodia.v396`); desde a v397 roda depois de E12. As 19 âncoras são frágeis à edição do `index.html` e do `i18n.js` por outra sessão (L20).

### E14 — aplicar o selo ao index

**Comando:** `cd "$BANC" && $PY tools/aplicar_selo.py 2>&1 | tail -1 | cut -c1-200 && $PY tools/aplicar_selo.py --conferir 2>&1 | tail -1`.

**O que faz** [LIDO]: chama `gerar_head_camada_texto.py` por conta própria; regenera as regiões protegidas `head-camada-de-texto`, `porta-texto` e `jsonld-e-scripts` (marcadores `CLAUDE:INICIO` e `CLAUDE:FIM`); re-carimba todo `data-selo="pin"` e `data-selo="version"`; troca, nos links do corpo, os DOIs que o `CITATION.cff` marca como versão anterior do Zenodo pelo DOI corrente; exige o padrão literal `vNNN · <pin16>`, as três regiões uma vez cada e os primeiros 8192 bytes até o link do DOI (regra R13).

**Muda por versão:** nada. **Idempotência:** imprime «index.html já diz o selo vN pin (nada a mudar)» e não regrava. `--conferir`: rc 0 com `VEREDITO: O INDEX DIZ O QUE O SELO DESCREVE`, ou rc 1.

### E15 — corpo inteiro em um arquivo e gêmeo Markdown da home

**Comando:** `cd "$BANC" && $PY tools/gerar_llms_full.py 2>&1 | tail -1 | cut -c1-120 && $PY tools/gerar_index_md.py 2>&1 | tail -1 | cut -c1-160`.

**Lê:** selo, `PORTA`, `TUNEL`, módulo do estatuto, `SITE\read-brief.md`, `SITE\secoes\*` (conferidas contra `TB\secoes\`) e os títulos das 8 partes. **Escreve:** `SITE\llms-full.txt` (cabeçalho, índice de deslocamentos em bytes, estatuto, Read Brief, 8 partes, cartão) e `SITE\index.md` (~10 a 14 KB).

**Gates:** parte que difere entre site e espelho, parte faltando, estatuto diferente do selo, alias ou porta ausente ⇒ `SystemExit`. **Muda por versão:** nada; não há prosa por versão. **Idempotência:** conteúdo estável; grava um `.bak_<STAMP>` novo a cada rodada.

**Dependência de ordem:** o `llms-full.txt` embute o Read Brief; se E07 citou bytes velhos (L04), eles viajam também.

### E16 — sitemap e manifesto de subida

**Comandos:**
```
cd "$BANC" && $PY tools/gerar_sitemap.py --saida "C:/IALD/Site/tgl/v3.0/sitemap.xml" --base "C:/IALD/Site/tgl/v3.0" 2>&1 | grep -c "fora:"
cd "$BANC" && $PY tools/gerar_manifesto.py --base "C:\IALD\Site\tgl\v3.0" --saida "C:/IALD/Site/tgl/v3.0_bancada/revisoes/manifesto_vN.json" 2>&1 | tail -1 | cut -c1-120
```
- `gerar_sitemap.py`: a lista de candidatos está **fixa no código** (home, read-brief, linhas de pesquisa, `central/index.html`, llms, llms-full, index.md, filmes, as 8 partes e 5 páginas antigas); `lastmod` é a data de modificação do arquivo; página com `noindex` e arquivo inexistente saem e são ditos como `fora:`. O `grep -c "fora:"` do transcrito só conta; G1 deve comparar com a lista esperada, que hoje não está escrita em lugar nenhum.
- `gerar_manifesto.py`: `--base` e `--saida` obrigatórios, `--url-base` (padrão: o site), `--so` (lista explícita); lista **todo** o `v3.0` com bytes e sha256 lidos agora, menos `*.bak_*`, `_identidade/`, `Versões Anteriores/`, `Música/`, `v3.0_bancada/`, `.env`, `CLAUDE.md`, `LEIA-ME.md`, `*.tmp` e afins. **O escopo é o site inteiro**, inclusive `central/` (L10).

**Muda por versão:** só o nome do manifesto (`manifesto_vN.json`). **Idempotência:** sobrescreve com `.bak_<STAMP>`; o conteúdo só muda se algum arquivo do site mudou.

### E17 — subida em ensaio (dry-run)

**Comando:** `cd "$BANC" && $PY tools/subir_site.py --manifesto "C:/IALD/Site/tgl/v3.0_bancada/revisoes/manifesto_vN.json" --dry-run 2>&1 | tail -1`. Depois, no transcrito, `grep "DIFERENTE\|AUSENTE" subidas/<stamp>_dryrun/RELATORIO.md` (revisão a olho do que subiria).

**O que faz** [LIDO]: confere que o disco bate com o manifesto (bytes e sha256 relidos agora; recusa caminho proibido); compara cada arquivo com o ar por `HEAD` e `GET` (todo arquivo de até 64 MB é baixado para o hash; arquivos `.ht*` entram sempre); testa a conexão sem enviar; grava `subidas\<stamp>_dryrun\RELATORIO.md`. Nada é enviado.

**Muda por versão:** só o nome do manifesto. **Idempotência:** só leitura do ar; cada rodada grava uma pasta `<stamp>_dryrun` nova.

**Gate [PROPOSTA]:** conjunto esperado do que deve diferir (E04 a E16 conhecem os arquivos que escreveram: `index.html`, `i18n.js`, `read-brief.md`, `llms.txt`, `llms-full.txt`, `index.md`, `sitemap.xml`, `secoes\*`); qualquer `DIFERENTE`, `NOVO` ou `AUSENTE` fora dele (por exemplo em `central\**`) ⇒ STOP com relatório (L10).

### E18 — subida

**Comando:** `cd "$BANC" && $PY tools/subir_site.py --manifesto "…/manifesto_vN.json" 2>&1 | grep -E "VEREDITO|SUBIDA|ERROS" | head -4`.

**O que faz** [LIDO]: credenciais em arquivo fora da bancada (não lidas aqui); transporte SFTP por regra desde 07/10 (`--permitir-ftp-em-claro` só com palavra expressa do operador: **G1 nunca passa**); copia o manifesto; faz **backup do ar** dos arquivos que serão trocados (`subidas\<stamp>\antes\` e `estado_antes.json`); envio atômico (nome temporário e rename); verificação no ar por HTTP 200, bytes, sha256, Range e content-type; roda `C:\IALD\Artigo\the_boundary\tools\guarda_do_site.py` (aprovação: `O SITE DIZ O QUE O SELO DESCREVE`); se a verificação dos arquivos falha, **reverte sozinho**; se só a guarda falha, os arquivos ficam e a decisão (corrigir e resubir, ou `--restaurar <stamp>`) é humana. rc 0 só em `SUBIDA VERIFICADA`.

**Muda por versão:** só o nome do manifesto.

**Idempotência:** «nada a subir: o ar já é igual ao manifesto» (rc 0). **Gates:** manifesto válido; E17 sem surpresa; E09 e E12 verdes; `--sem-guarda` proibido para G1.

### E19 — leitor de IA (R1)

**Comando:** `cd "$BANC" && $PY tools/leitor_ia.py --relatorio revisoes/leitor_ia_<AAAAMMDD>_vN.md 2>&1 | grep -E "R1:|Bytes somados" | cut -c1-160`.

**O que faz:** simula um leitor sem JavaScript que lê só os primeiros 64 KB de cada página, parte da home e segue até 4 páginas de texto do site; passa se achar os quatro alvos (Read Brief, `llms.txt` do site, `um.py` raw, selo raw) em até 2 saltos e até 100 KB somados. rc 0 passa, rc 1 falha. **Muda por versão:** só o nome do relatório. **Idempotência:** gera um relatório novo a cada rodada.

### E20 — medição final

**Comando:** `cd "$CEN" && $PY tools/estado_do_organismo.py` (com rede). **Pós-condições da perna 1** (itens do medidor, l.113–180 [LIDO]):
- Espelho: `um.py` igual ao pino do Nós; `um_version` == N; existe `BK\um_v{N-1}_*` (**o medidor assume P = N-1**, falso em custódia conjunta: L20); `LEDGER.md` contém `### The custody — vN`; `ESTADO_ATUAL.md` e `README.md` contêm `PIN16`; `CITATION.cff` contém o pino inteiro; existem `diferencas_vN\` e `recibos_bancada_vN\`; `HEAD == origin/main` e nada rastreado pendente.
- Espelho (GitHub raw): README raw traz o pino; selo raw tem `um_version == vN`.
- Site (fonte): nota «Current seal» == (vN, PIN16); `data-selo` pin no index; `art.c.cl.arcN` no index e no i18n; `read-brief.md`, `llms.txt`, `llms-full.txt` e `index.md` com o pino; última subida «SUBIDA VERIFICADA»; nenhum arquivo da fonte mais novo que a última subida.
- Site (ar): o index diz «vN · PIN16»; `llms.txt` e `read-brief.md` no ar trazem o pino.

**Muda por versão:** nada (N, PIN16 e P saem do selo). **Idempotência:** só leitura; grava apenas o próprio quadro. **Gates:** rc 0 sem `DEFASADO` nas quatro superfícies acima; rc 1 ou 2 ⇒ a custódia não está completa.

---

## 3. Prosa escrita à mão hoje: catálogo por versão, molde factual e marcador do handoff

### 3.1 Marcadores do handoff: o que existe e o que falta

**Existe** [LIDO nos handoffs v397 e v398]: comentários HTML `<!-- INICIO_PARAGRAFO_<TAG> --> … <!-- FIM_PARAGRAFO_<TAG> -->` com texto em português pronto para README e site. As TAG são irregulares: `README_v397` (handoff v397 e repetido, «o MESMO, intocado», no v398) e `SONICO_v398` (novo no v398). Tamanhos [MEDIDO]: bloco `README_v397` 2.298 B; bloco `SONICO_v398` 2.630 B. O gerador da v397 acha o bloco com a TAG escrita no código (`re.search(r"<!-- INICIO_PARAGRAFO_README_v397 -->\n(.*?)<!-- FIM_PARAGRAFO_README_v397 -->", …, re.S)`).

**Onde o parágrafo da v397 foi parar** [MEDIDO]: `ESTADO_ATUAL.md` (1 vez, verbatim, com marcadores); `LEDGER.md` (1 vez, dentro do bloco da custódia); `README.md` **não** verbatim — uma nota de 453 B lida do registro; site **não** verbatim — só a linha do arco (index.html 1 ocorrência, i18n.js 2) e **zero** ocorrências do 4,44 em `read-brief.md`, `llms.txt`, `llms-full.txt` e `index.md` (L18).

**Regra de leitura para G1 [PROPOSTA]:** `<!-- INICIO_(?P<id>[A-Za-z0-9_]+) -->\n(?P<corpo>.*?)<!-- FIM_(?P=id) -->` com DOTALL (atenção: as TAG têm `v` minúsculo, como `README_v397`; uma classe só com maiúsculas não casa); a identidade do bloco é o `id`. Cada `id` entra **uma vez** em cada alvo (ESTADO, LEDGER): bloco já presente e byte-idêntico ⇒ pular; presente e diferente ⇒ STOP; ausente ⇒ inserir. Hoje isso falha de dois modos (L05): a âncora do `gerar_estado_atual.py` até a v397 punha o bloco novo entre o ERR e o parágrafo do anterior, e o handoff v398 traz o `README_v397` de novo. [MEDIDO na v398] a outra sessão resolveu os dois à mão: trocou a âncora para antes de `## What is PROVED` e conferiu que o bloco `README_v397` do handoff v398 é byte-idêntico ao do handoff v397 (`m7.group(0) == m7o.group(0)`), que é exatamente a checagem proposta aqui.

**Falta** [PROPOSTA — o autor do handoff (a sessão do Nós) já gera os parágrafos pelas mesmas funções que o artigo e os confere contra o core antes de o handoff nascer; os blocos abaixo seguem o mesmo padrão e G1 só os **confere** contra selo, core e arquivos, nunca os toma como fonte]:
- `INICIO_FATOS_CUSTODIA_vN` com JSON: `versao`, `pin16`, `titulo_pt`, `titulo_en`, `modulos_novos[]`, `n_bandeiras_novas`, `escada{de,para}`, `registros_novos[]`, `recibos_bn{aplicacao{arquivo,sha16},parada{sha16},religamento{sha16}}`, `artigos{en_pdf,en_txt,pt_pdf,pt_txt}` (sha16), `inscricoes{n,data}`, `abertos_en[]`, `abertos_pt[]`, `pendencias_operador[]`, `nomes_provisorios[]`.
- `INICIO_ARCO_EN_vN` e `INICIO_ARCO_PT_vN`: o texto da linha do arco do site (até ~1.800 B; sem aspa simples, `<`, barra invertida nem quebra de linha; os números do registro).
- `INICIO_ENTROU_EN_vN`: o parágrafo «what entered» do ESTADO (hoje `TXT`).
- `INICIO_ABERTOS_EN_vN`: o item «what stays open» do ERR.
- `INICIO_COMMIT_vN`: o corpo do commit do espelho (ASCII).
Sem esses blocos: usar o molde factual da §3.3 ou **PARAR com a lista do que falta** (regra do enunciado).

### 3.2 Catálogo (cada string, por versão)

Convenção: «gerad.» = `custodia_vN_geradores.py`; linhas citadas são as do arquivo da v397 (v396 e v395 entre parênteses quando diferem).

**PRO-01 — passo zero, docstring (l.2).** v395: «CUSTÓDIA v395 (21/10, handoff v395; molde v394: backup da v394)» · v396: «… (22/10 … molde v395 …)» · v397: «… (23/10 … molde v396; regra do operador de 23/10: custodiar quando o handoff aparecer)» · v398 (outra sessão): «… (24/10 … regra do operador de 24/10 …)» com erro de cópia no elo v396 (L19). Molde: f-string de uma linha; a cadeia «Do molde: …» sai.

**PRO-02 / PRO-03 — passo zero, `man["regra"]` e `man["gerador"]`.** `"… (custódia vN; molde da custódia vP)"` e `"Site/tgl/v3.0_bancada/tools/custodia_vN_passo0_backup.py"`. Molde: f-string.

**PRO-04 — espelho, docstring (l.2).** A parte que muda é o parêntese «fontes pinadas + as da vN (…)»: v395 «fontes pinadas + as da v395; diffs da v395; recibos do B(n) da v395» · v396 «… (os insumos da pedra TestemunhaEstatica e as 3 cunhagens de 22/10) …» · v397 «… (a pedra Token, o resultado do Teste da Única Palavra e os três recibos da Fase 9, as 6 cunhagens de 23/10) …». Molde: nomes tirados das chaves de `_VN_FONTES` e `len(_VN_VERBATINS2)`; o resto é f-string.

**PRO-05 / PRO-06 — espelho, comentários `# vN:` e mensagens de assert** com a versão (`BACKUP DA vP NÃO CONFERE`, `vN: %s ausente`, `recibos do B(n) da vN não achados por sha256`). Molde: f-string.

**PRO-07 — gerad., docstring (l.2–10): a ordem do operador citada verbatim.** v395 (21/10): «versão nova do um.py avançamos segue O handoff de custódia para a sessão do site está em Nós\HANDOFF_v395_CUSTODIA.md atualize tudo, toda a central, site, repositório e tudo mais e faça commit e push» · v396 (22/10): «Encontre vulnerabilidades em php e as corrija. A licença é como você falou mesmo, tudo certo. Atualize tudo com a nova versão do um.py» · v397 (23/10): «pode custodiar sempre que o handoff aparecer, como regra». Molde: citar **o caminho e o sha16 do arquivo `OPERADOR_<dd>out_*_verbatim.txt`** da pasta de trabalho da sessão (já existe, p.ex. `work\custodia_v396_22out\OPERADOR_22out_custodia_v396_verbatim.txt`) e a regra permanente de 23/10; não colar o texto.

**PRO-08 — gerad. `TXT` (v395 l.83 · v396 l.107 · v397 l.112): o parágrafo «what entered» (EN) da linha da tabela do ESTADO e do LEDGER.**
- v395: «THE PSIONIC MODE IN THE FRACTALIZATION OF THE ONE: 1 new kernel module (Psibit), %d new flags (named declarations; the compiler auxiliaries are covered by KH-N1 without a flag); ladder **9332** -> %s …» (a escada anterior está **digitada** no texto); registro `psibit_v395` (mecânica da órbita do Um pela matriz-S; conjunção incondicional `psibit_is_the_mode_of_the_reader`; face do psion condicional a um certificado de Fock sem habitante); `cunhagens_v395`: 4 falas de 21/10; divergência [LEGAL] do ACOM Mirror.
- v396: «THE STATIC WITNESS: 1 new kernel module (TestemunhaEstatica; the name is provisional, the operator names it) …»; registro `testemunha_estatica_v396` (canto do psion, projetor de Bell 4x4, fluxo diagonal construído; 19 termos da pedra + 8 de apoio + 14 checagens); composição incondicional `the_psion_inhabits_the_static_witness`; face de Fock ainda condicional; `cunhagens_v396`: 3 falas de 22/10.
- v397: «THE UNIQUE WORD TEST: 1 new kernel module (Token; the name is the operator’s, 23/10), 1 new flag (`ext_tok397_0001` …)»; registro `teste_de_veracidade_fase9_v397` (z_disc, p, z_δ, poder, ln B, K; 35 checagens; «NOT blind»); `cunhagens_v397`: 6 falas de 23/10.
- v398 [MEDIDO em `custodia_v398_geradores.py`, escrito à mão em 09:09]: «THE SONIC AND THE TUNING OF THE STRINGS: 2 new kernel modules (`Sonico` — the name is the operator’s, 23/10 — and `AfinacaoDasCordas`, ratified by him), 40 new flags (6 of the sonic, 34 of the tuning; named declarations only), two UNCONDITIONAL compositions in the trio (`sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory`, `ext_son398_0003`; `the_strings_close_the_face_from_outside_the_tgl_closes_the_reading`, `ext_afi398_0027`); ladder 9499/9499 -> 9539/9539 …»; dois registros novos com 8 e 7 checagens, a entropia do colapso em θ_M como único número [DERIVED], a lei de custo [INPUT], `MasslessFirstLevel` [KNOWN], d = 9 [DECLARADO], geometria [OPEN]; `cunhagens_v398`: 6 inscrições de 23/10 (cinco do operador e uma leitura da gerência por ele ratificada, rotulada); kh_n1 29.294/23.284; e o quadro do Teste da Única Palavra (v397) «stays at the top, unchanged». Os números (`values` dos dois registros: ln 2, H₂ em nat e em oitava, ζ, D) saem do core; a frase em inglês é nova.
- Molde factual: esqueleto fixo `<TÍTULO EN em caixa alta>: K new kernel module(s) (<nomes>), <NB> new flag(s) (<nomes ou faixa>); ladder <A> -> <B> (<T> audited declarations, <KT> theorems, none outside the trio); <cláusulas por registro>; <cunhagens>: <N> inscriptions of the operator of <dd/mm> by sha256; certified by the sha256 the program reads of itself (<PIN16>)`. Fatos: K e nomes ← módulos novos (manifesto do espelho × backup de P); NB ← bandeiras do core (N × P); A, B ← `estatuto_da_prova_v391.prova_1_kernel` (P × N); T ← `len(axiom_report)`; KT ← veredito de `kh_n1_cobertura_vN`; N ← `len(cunhagens_vN.verbatim)`; data ← `cunhagens_vN` / handoff. **Cláusulas por registro:** não há fonte automática em inglês hoje (`diz`/`nao_diz`/`limites` do core estão em português ASCII); opções: (1) bloco `ENTROU_EN_vN` do handoff; (2) o parágrafo «What enters.» da seção da versão em `um_absoluto_en.txt` (texto selado pelo próprio programa; ex.: seção «Sonic and the tuning of the strings», linhas 105–119 do artigo da v398); (3) tabela fechada de frases por token de veredito (`THE_CREDITATION_STEP_NOT_REACHED`, `NOT_FALSIFIED_WITH_POWER`, `NO_NEW_SIGMA_COMPUTED`, `NOT_BLIND_TO_DATA_STATED`, `GATE_UNMOVED`…), com token desconhecido ⇒ STOP.

**PRO-09 — gerad. `ERR` (v395 l.93 · v396 l.119 · v397 l.123): a «Errata beside» do ESTADO e do LEDGER (EN, 3 a 4 itens).**
- Item 1 «kh_n1 coverage» (mecânico): `<TERMOS_P> -> <TERMOS> constants, <KT_P> -> <KT> theorems; the formal tree of the Nós <F_P> -> <F> entries`; `kh_n1_cobertura_vP now charges floors at h2, h3 and h6 and a minimum tree size at h8; the exact equalities and the exact tree pin live in kh_n1_cobertura_vN`. Na v395 os números de P estão **digitados** (29026, 23069, 1423); v396 e v397 leem do core de P. Fonte: veredito `CLOSURE_(\d+)_CONSTANTS_(\d+)_THEOREMS_…` dos dois `kh_n1_cobertura`, manifesto do espelho × backup. Condição: o registro de P tem uma errata com «piso» e «h8» (assert).
- Item 2 «The contracts … now read expected_ladder = <ESC>» (mecânico): v395 «three v394 contracts» · v396 «four contracts» · v397 «five contracts». Fonte: `fatos_vN.json` (perna 2) ou varredura de `um.py` por `*_CONTRACT` com `expected_ladder`. Na v398 o handoff diz «cinco contratos» e `fatos_v398.json` lista sete (`_V398_SONICO_CONTRACT` e `_V398_AFINACAO_CONTRACT` nascem com 9539): a lista da errata é a dos contratos de versão **anterior** a N.
- Item 3 (sob medida): v395 «What stays open» (entra como item 3) · v396 docstring de `bell_cci_half` lida do arquivo Lean (`TGL\GravitonShadow.lean`) · v397 a regra do 4,44. Fonte: bloco do handoff (a regra do 4,44 está no parágrafo «A regra do 4,44» do handoff) ou marcador novo.
- Item 4 «What stays open» (v396, v397): discriminação a 5σ, face de Fock do psion, contrato conjunto da rede e H3 em toda direção nula, F8.1, nomes provisórios, [LEGAL] do ACOM Mirror. Fonte: a frase «[OPEN]: …» do parágrafo «Pendências SÓ do operador» do handoff (em português) ⇒ precisa de `ABERTOS_EN_vN`.
- v398 [MEDIDO]: item 1 igual em forma («with the two modules the coverage grows (29229 -> 29294 constants …)»); item 2 «The seven contracts … expected_ladder = 9539»; item 3 novo, «What the kernel proves and what is reading» (as duas composições são termos incondicionais no trio; os registros conferem cálculo e não provam a natureza; a lei de custo é [INPUT]; `MasslessFirstLevel` é nomeada e não provada [KNOWN]; geometria das cordas e ligação dos dois círculos [OPEN]; as leituras do operador são [INPUT/ONTO]; «the rule of 4.44 stays: the panel of v397 is unchanged, with its 5σ line»); item 4 «What stays open» com os nomes provisórios dos dois registros novos.
- Cabeçalho do item: «Errata beside (dd/mm/2026, the custody of vN; read from … none typed)» — a data e a lista de fontes são digitadas.

**PRO-10 — gerad. `NOTA` (v395 l.102 · v396 l.134 · v397 l.137): «Status that goes with vN (not to be cut)».** Esqueleto fixo (PROVED = validade; CONFIRMED = creditação; ressalva de v392; bandeiras por termo que seguem False — `%s` lido do selo; «The vP copy lives outside the repository; the stdout vN is in rodadas/; the diffs of vN are in diferencas_vN/; the pinned sources … in fontes_pinadas/ … (now with the vN sources, …); the B(n) receipts … recibos_bancada_vN/»; depósito Zenodo). Variável: o parêntese das fontes — v395 «among them the patent document of the Psibit stone» · v396 «the TestemunhaEstatica stone, its independent exam, its result and the KH-N1 coverage of v396, plus the three inscriptions of 22/10» · v397 «the Token stone, the result of the Unique Word Test and its three receipts, the KH-N1 coverage of v397, plus the six inscriptions of 23/10» — e, na v397, a oração «(the Unique Word Test reads z_disc = 4.44 …)». Molde: lista tirada das chaves de `_VN_FONTES`/`_VN_VERBATINS2`; a oração do z_disc só se existir registro de veracidade (ver L03). **v398 [MEDIDO]:** o parêntese passou a «(now with the v398 sources: the two stones, the KH-N1 coverage of v398 and the six inscriptions of 23/10)» e a oração do z_disc ganhou a versão certa à mão, «(the Unique Word Test, v397, reads z_disc = …)» — enquanto a nota gerada do README rotula esse teste com a versão do selo corrente (L03).

**PRO-11 — gerad. `BLOCO` (LEDGER; v395 l.155 · v396 l.188 · v397 l.193).** Bloco `### The custody — vN (COMPLETE round)`. Esqueleto fixo com 12 números (PIN16, bytes, escada, timestamp, sha16/rito do diário, `TXT`, veredito do registro, `NOTA`, formais, termos, bandeiras acesas e apagadas, `ERR`). A frase de abertura é a única parte livre: v395 «Prepared by the session a7 of the Central on the operator’s order of 21/10/2026 (handoff v395 of the management c1).» · v396 «… order of 22/10/2026 (handoff v396 …)» · v397 «… under the operator’s standing order of the same day («custodiar sempre que o handoff aparecer»; handoff v397 …)». Molde: `<sessão>` e `<data>` por parâmetro; a ordem do operador por referência ao arquivo verbatim (PRO-07). A v397 acrescentou o parágrafo pronto (`PAR`) como último item do bloco. **v398 [MEDIDO]:** «Prepared by the session a7 of the Central on 24/10/2026 under the operator’s standing order of 23/10 (…; handoff v398 of the management c1)»; o bloco cita dois vereditos de registro («Verdicts read from the sealed core: … and …») e termina com o parágrafo `SONICO_v398`.

**PRO-12 — gerad. CITATION (duas descrições).** `the current seal of the repository, one page, regenerated at every custody (vN on <data>; the Zenodo deposit holds v392)` e `the pin of um.py at vN, the repository head (<bytes> bytes; sealed <ts>); the Zenodo deposit 10.5281/zenodo.23366324 holds v392 (b590c0aa80055e2a…)`. Digitados: o DOI, «v392» e o pino abreviado do depósito (L16). Molde: ler a linha `Zenodo deposit of vK, deposited <data> (byte-identical to the seal: um.py sha256 <16>…` e `doi:` do próprio `CITATION.cff` (os outros geradores já fazem isso).

**PRO-13 / PRO-14 — gerad. `EN` e `PT` do arco (v395 l.182/189 · v396 l.215/224 · v397 l.222/231): a linha `art.c.cl.arcN` do site (index.html e i18n.js).**
- Esqueleto fixo (igual nas três versões): «The custody of vN (complete round): <TÍTULO> — K new kernel module(s) (<nomes>), ladder <A> (named declarations with axioms in the trio; <T> audited declarations, none outside the trio); <CLÁUSULAS>; <N> inscriptions of the operator of <dd/mm> by sha256[; <nota>]. Certified by the sha256 the program reads of itself (<PIN16>). Kernel <F> files / <T> terms. Proved is not a judgement of nature; the gate did not move»; PT análogo, fechando com «PROVADA ≠ CONFIRMADA; o gate não se moveu».
- Cláusulas (sob medida): v395 «a leitura do par (peso, Palavra, Verbo) … é uma bijeção de conjuntos sobre o livro de códigos, com perda zero, e o colapso perde exatamente a paridade, um bit (incondicional, no kernel); a face do psion é condicional a um certificado de Fock sem habitante exibido; psibit = psion = modo do leitor é a leitura do operador; a patente do ACOM Mirror diverge de si mesma …» · v396 «o par do psion, o projetor de Bell, ecoa; a redução dele a um sítio é (1/2) I e não ecoa; … a ponte é construída, não derivada da dinâmica da teoria; … ao lado da docstring de bell_cci_half, o 1/2 é a entropia linear, e a entropia de von Neumann da redução é ln 2 nat» · v397 «o registro de veracidade lê por sha256 o resultado do teste aberto uma vez em 23/10/2026: z_disc = 4,44 (calibrado; p unilateral 4,4e−6), abaixo do degrau de 5σ da creditação, que não foi alcançado (4,44 é menor que 5); … a fala do operador, verbatim: «o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica» — leitura dele, não critério da régua». O texto do arco é gerado **duas vezes** (EN e PT) e cada versão traduz a mão.
- v398 [MEDIDO, EN8/PT8 em `custodia_v398_geradores.py`]: «The custody of v398 (complete round): the sonic and the tuning of the strings — 2 new kernel modules (Sonico, the operator’s name, and AfinacaoDasCordas, ratified by him), 40 new flags, two unconditional compositions in the trio, ladder 9539/9539 (29294 audited declarations, none outside the trio). The registry of the sonic reads the kernel of the rite and checks 8 computations … ln 2 is the fair bit (0.693147) … the collapse entropy at θ_M, 0.065140 nat = 0.093977 octave, not in the kernel; the cost law is an input … The registry of the tuning checks 7 … ζ(−1) = −1/12 and ζ(−1, 1/2) = 1/24 … D = 26 and D = 10, with D = 10 read as d = 9 (the house’s d, declared); the geometry is open … 6 inscriptions of 23/10 by sha256. The panel of the Unique Word Test (v397) stays at the top unchanged: z_disc = 4.44, calibrated, one-sided p 4.4e−6, below the 5σ step of accreditation, which was not reached. …». A regra do 4,44 sobrevive no arco da v398 por essa oração.
- Molde: esqueleto de arquivo-modelo (`moldes\arco_en.txt`, `arco_pt.txt`) com os campos factuais e uma única lacuna `{CLAUSULAS}`; a lacuna vem de `ARCO_EN_vN`/`ARCO_PT_vN` do handoff ou, na falta, do primeiro parágrafo «What enters.»/«O que entra.» da seção da versão no artigo emitido (texto selado), limpo das marcações de LaTeX e das aspas simples.

**PRO-15 — gerad. código inserido em `gerar_estado_atual.py`.** Comentário `# custódia vN (dd/mm/2026, sessão a7 da Central): ao lado; sha16 e rito LIDOS do diário[; o parágrafo pronto do handoff, verbatim]` e o título `### vN · the custody` (as versões anteriores à v390 tinham títulos próprios: «the whole is one», «the dissipation law», …). Digitados: a data e «sessão a7 da Central» (parâmetro de G1). **v398:** a âncora deixou de ser a linha do ERR anterior e passou a ser o par `L.append("")` + `L.append("## What is PROVED …")` (inserção antes dele), com `assert g.count(ANC) == 1` e a conferência de que o bloco da v397 existe uma vez; é a âncora estável que G1 deve adotar. Efeito medido: o parágrafo `README_v397` ficou no caractere 71.730 do ESTADO (texto normalizado para LF), antes do cabeçalho `### v398` (73.920), e o `SONICO_v398` no 79.156. Molde: o bloco passa a ser dado (`custodias.json`: lista de {versão, título, linha, nota, errata, parágrafos}) lido por um laço único em `gerar_estado_atual.py`, em vez de cada versão acrescentar código (L02, L05).

**PRO-16 — mensagem do commit do espelho (E10).** Um arquivo novo por custódia. v395: assunto «custodia(v395): o modo psionico na fractalizacao do Um - selo, modulo Psibit, escada 9451/9451, fontes pinadas da v395, PORTAS, README» e corpo longo com a ordem do operador entre aspas, 6 marcadores e a nota [LEGAL] · v396: assunto «… a testemunha estatica - … modulo TestemunhaEstatica, escada 9498/9498 …» e corpo curto com 3 marcadores de errata · v397: assunto «… o Teste da Unica Palavra - selo, modulo Token, escada 9499/9499, fontes pinadas da v397, PORTAS, README (a regra do 4,44)» e corpo com 3 marcadores. Trailer: v395 e v396 «Claude Opus 5.5», v397 e v398 «Claude Fable 5.1» (modelo da sessão). v398: assunto «custodia(v398): o sonico e a afinacao das cordas - selo, modulos Sonico e AfinacaoDasCordas, escada 9539/9539, fontes pinadas da v398, PORTAS, README» e corpo com 4 linhas factuais (pino, 1428 formais / 29294 declaracoes, 40 bandeiras novas [6 do sonico, 34 da afinacao], backup da v397) e 3 marcadores de errata (kh_n1 29229 -> 29294; «os sete contratos»; a lei de custo é INPUT, `MasslessFirstLevel` hipótese nomeada, geometria OPEN). Molde: assunto e as 4 primeiras linhas do corpo são factuais (título do diário em ASCII, módulo, escada, PIN16, F/T, K, P e o pino de P); os marcadores vêm de `COMMIT_vN` do handoff; o trailer é parâmetro (`--trailer`), G1 não o inventa.

**PRO-17 — nota do Teste da Única Palavra no README (`gerar_readme_frente.py` l.255–268).** Gerada do registro `teste_de_veracidade_fase9_v\d+` mais novo do core do espelho (bom padrão: nenhum número digitado; `assert z_disc_calibrado < 5` e o token `THE_CREDITATION_STEP_NOT_REACHED`). Ressalvas medidas: rotula a nota com `(versao, data)` do SELO CORRENTE, não do registro (L03), e custa 453 B de uma frente que tem 19 B de folga (L01).

**PRO-18 — `nao_levados` (espelho, relatório).** Dicionário de 26 chaves com texto livre; a última entrada é da v394; nenhuma chave cita v395, v396 ou v397 [MEDIDO] (L19). Molde: lista fixa em arquivo de dados + uma entrada gerada por versão («HANDOFF_vN_CUSTODIA.md: documento de trabalho; fica no Nós e no cofre da Central»).

**PRO-19 — apertos editoriais da frente (`patch_readme_v397.py`, `…b.py`, `…c.py`).** Três scripts de trocas contadas em `gerar_readme_frente.py` para o README caber em 40.960 B: 41.542 -> 41.101 -> 40.941 B (9 trocas de prosa no `b`, 2 no `c`). Tudo à mão, sem lugar na esteira. Na v398 não há folga para repetir (L01).

### 3.3 Moldes factuais: cada campo e de onde sai

| campo | fonte (nunca digitado) |
|---|---|
| N, P | `NOS\um_absoluto_selo.json` → `um_version`; `ESP\um_absoluto_selo.json` → `um_version`; conferir P no diário |
| PIN, PIN16, timestamp, bytes de `um.py` | selo do Nós; tamanho de `NOS\um.py` |
| escada de→para | `core.estatuto_da_prova_v391.prova_1_kernel` (`n_theorems_clean`/`n_theorems_expected`) de N e de P (core de P em `BK\um_vP_<pinP>\um_absoluto.json`) |
| termos auditados, formais | `len(axiom_report)`, `len(formal_files_sha256)` do manifesto |
| módulos novos | diferença de `formal_files_sha256` entre N e P (campo `selo.kernel.novos` do relatório de E03) |
| bandeiras novas | chaves de `core.kernel_formalization` em N que não estão em P |
| bandeiras apagadas | `selo.bandeiras.apagadas` do relatório de E03 |
| registros novos | chaves de `core` em N que não estão em P |
| cobertura do kernel | veredito `CLOSURE_(\d+)_CONSTANTS_(\d+)_THEOREMS_…` de `kh_n1_cobertura_vN` e `_vP` |
| contratos com `expected_ladder` | atribuições `_V\d{3}_\w*_CONTRACT` no `um.py` (ou `fatos_vN.json`); os de versão anterior a N entram na errata |
| nº de inscrições, data | `len(cunhagens_vN.verbatim)`; data do handoff |
| recibos B(n) | sha16 dos 3 arquivos de `cadeia_de_selo\vN`, conferidos com o handoff |
| sha16 e rito do diário | bloco `vN SELADA` de `MEMORIA_DA_LINHAGEM.md` |
| título PT | cabeçalho do bloco `vN SELADA` («— <TÍTULO> (vN): K módulos novos, escada A → B») |
| título EN | **sem fonte hoje** (o artigo emitido tem títulos de seção em EN que diferem do título escolhido na custódia) |
| z_disc, p, z_δ, poder, ln B, K | `teste_de_veracidade_fase9_vK.lido` do K mais novo |
| depósito Zenodo | `CITATION.cff` (linha «Zenodo deposit of vK» e `doi:`) |
| sessão, data da custódia, ordem do operador, trailer | parâmetros de G1 (arquivo verbatim da ordem, por caminho e sha16) |

### 3.4 A v398 como caso de teste: o que saiu dos arquivos e o que a outra sessão escreveu à mão

**Saiu dos arquivos, sem digitar** [MEDIDO em `fatos_v398.json`, no handoff e no core]: P = v397, N = v398, PIN16 `c632fa261ce3f538`, escada 9499 -> 9539, 29.294 termos, 1.428 formais, 2 módulos novos (`TGLExt/AfinacaoDasCordas.lean`, `TGLExt/Sonico.lean`), 4 registros novos (`afinacao_das_cordas_v398`, `cunhagens_v398`, `kh_n1_cobertura_v398`, `sonico_v398`), 40 bandeiras novas, 7 contratos com `expected_ladder` (5 de versão anterior e 2 nascidos na v398), os 3 recibos B(n) (`0f306c551a2ccbee`, `a3339191387ad9df`, `12354ad5c5ac52f2`, conferidos com os arquivos), os blocos `README_v397` e `SONICO_v398` por marcador, o título PT do diário.

**Escrito à mão na v398** [MEDIDO nos scripts de 09:04 e 09:09] — é a lista do que G1 teria de receber por marcador ou gerar por molde: o título EN; o `TXT` (EN); os itens 3 e 4 do `ERR` (EN); o parêntese das fontes e a oração do z_disc no `NOTA`; a frase de abertura do `BLOCO`; `EN8` e `PT8` (a linha do arco); o corpo do commit; as listas e contagens dos asserts (2 módulos, 4 registros, 40 bandeiras, 7 contratos, 8 e 7 checagens, 6 inscrições); a âncora do `gerar_estado_atual.py`; a exclusão `bateria_pre_selo`; os 3 sha16 dos recibos; o `PIN16` de P no caminho do backup.

**Não foi feito** [MEDIDO às 09:25]: o parágrafo `SONICO_v398` **não entrou no README** (0 ocorrências de «sônico», «sonic» e «afina»; README = 40.941 B, teto 40.960 B), embora o handoff peça README e site (L01). O quadro do Teste da Única Palavra seguiu no README, com o rótulo errado de versão (L03).

**Falta para G1 (PARAR e listar)** quando os blocos propostos em §3.1 não existirem: título EN; cláusulas EN do `TXT` e do arco (a versão PT existe no bloco `SONICO_v398`, mas o arco é uma síntese de um parágrafo); itens 3 e 4 do `ERR` em inglês; corpo do commit; o arquivo verbatim da ordem do operador que dispara a custódia; o trailer; onde caber o parágrafo novo no README (L01); como rotular o Teste da Única Palavra (L03).

---

## 4. Valores digitados hoje (a régua: hash e pino jamais de memória)

[MEDIDO por regex nos scripts da v397] sha16 digitados: `custodia_v397_passo0_backup.py` 1 (referência de handoff na docstring); `custodia_v397_espelho.py` **22**; `custodia_v397_geradores.py` 3; `gerar_readme_frente.py` 0. Na v398 (scripts de 09:04 e 09:09): passo zero 1, espelho **25** (os 22 mais os 3 recibos novos), geradores 2 (`BK397` e o pino do depósito; o sha16 da frase do 4,44 deixou de ser digitado porque o parágrafo passou a ser comparado por bytes com o do handoff anterior).

| onde | o que está digitado | de onde deveria sair | situação |
|---|---|---|---|
| espelho: blocos `_H394`…`_H397` | 12 sha16 de recibos B(n) (3 por versão, de v394 a v397) | `sha256[:16]` dos arquivos `RECIBO_*` de `cadeia_de_selo\vK` | [MEDIDO] os de v397 e v398 batem com os arquivos e com o handoff; G1 calcula e confere com o handoff e com a cópia já publicada em `recibos_bancada_vK\` |
| espelho: ORD, P391, C13 (v390 a v392) | 8 sha16 (3 verbatins + ordem + pedra; verbatim do estatuto; 2 verbatins de 13/10) | handoffs v390–v392 (afirmações) conferidas contra o conteúdo do arquivo | congelados e históricos: mover para dado (`espelho_fixos.json`), com o mesmo assert |
| espelho: `QP`, runs do pilar | nomes `run_20261004_153246_0063ce8d`, `run_20261005_103708_37e566b6` | idem | congelado, mesmo destino |
| espelho/geradores: docstrings | `1ff1503ec169eb12` (handoff v380), `b590c0aa80055e2a` (pino do depósito v392) | `CITATION.cff` | texto de história; sair da docstring |
| geradores: `BK396` | caminho `…\um_v396_0a4395a89eeebbb7` | `BK.glob("um_vP_*")` único + manifesto (E01) | derivar |
| geradores: `FRASE` e `9b182958a5a7a1bc` | a fala do operador (verbatim) e o sha16 dela | `_V397_FRASE_444` no `um.py` / `cunhagens_v397.verbatim` / arquivo verbatim da fala | ler e conferir o sha16 do arquivo |
| geradores: CITATION | `10.5281/zenodo.23366324` (5 linhas), `b590c0aa80055e2a…` (2) e «holds v392» (6) | linha do depósito e `doi:` do `CITATION.cff` | ler (L16) |
| geradores: contagens | `NCUN` (4, 3, 6), `NCHK == 35`, `NTERM == 19`, `NSUP == 8`, `NMEC == 14`, `len(CONTRATOS) == 5`, `KN.bandeiras == [3, 3]`, `NBAND == 1` | invariantes em vez de igualdades (ex.: todo contrato de versão anterior tem `expected_ladder == ESC`; `NBAND == len(bandeiras novas do core)`; `NCUN == len(verbatim)`) | trocar igualdade por invariante; na v398 elas quebram (7 contratos, 40 bandeiras, 2 módulos, 4 registros) |
| geradores: listas | módulos novos, registros novos, nomes de bandeiras | diferença N × P calculada | calcular e só então conferir com o handoff |
| geradores v395/v396: escada | `"9451/9451"`, `"9498/9498"`, `KERNEL_9451_OF_9451_FLAGS`; `9332` e `29026/23069/1423` nos textos | estatuto do core de N e de P | ler (a v397 já lê) |
| `gerar_estado_atual.py` (cada bloco) | a data e «sessão a7 da Central» | parâmetros | parâmetro |
| mensagem do commit | PIN16, F/T, K, pino de P | selo/core/manifesto | gerar |

**Padrões bons que G1 deve copiar** (já presentes): a escada, o sha16 e o rito do bloco `vN SELADA` lidos do diário e comparados com o selo (`L397 == (PIN16, TEOR)`); `_ok(registro)` com `all_verified`, `does_not_gate_core` e veredito `GATE_UNMOVED/UNTOUCHED` sem CONFIRMED; o README lendo o registro mais novo `teste_de_veracidade_fase9_v\d+` por regex em vez de nome fixo; `atualizar_dados_selo_site.py` calculando as âncoras a partir dos valores de P (backup) e de N (espelho), sem digitar nada; `patch()` com `count == 1`, backup de bytes e CRLF.

---

## 5. Fronteiras com as outras pernas

**Perna 2 (Central privada).** (a) `custodia_vN_geradores.py` lê `CEN\work\custodia_vN_*\fatos_vN.json` (feito por `sondar_vN.py`, que é da perna 2): é uma dependência cruzada hoje invisível. Recomendação: um único `sondar` dentro de `tools\custodia_g1\`, consumido pelas duas pernas. (b) Insumos da perna 1 que a perna 2/Nós produzem: `work\cadeia_de_selo\vN`, `vN_kernel`, `vN_selo` e os 2 diffs; os 3 recibos B(n) são do elo da Bancada Um (feito antes do handoff).

**Perna 3 (Central pública).** `work\central_publica_22out\atualizar_central_publica.py` (uma ordem, `--publicar` para publicar, `--listar` para listar) tem no grupo `site` 12 passos, dos quais **cinco repetem a cauda da perna 1**: `llms_site` (`gerar_llms_site.py`), `sitemap`, `manifesto`, `subir_ensaio` e `subir` (`publica=True`). Consequências [LIDO]:
- `gerar_llms_site.py` depende de `BANC\central_publica\acom\um_acom_info.json`, que é gerado pelo passo `acom` da perna 3 (E07 falha se o arquivo faltar).
- O manifesto de ambas cobre `v3.0` inteiro: quem sobe primeiro publica também o meio-trabalho da outra. Se a perna 3 subir entre E04 e E18, o ar recebe o `index.html` com a linha do arco N mas ainda com o padrão `vP · pinP` do selo (que só E13 e E14 re-carimbam); a guarda de `subir_site` compara esse pino com o selo do espelho, acusa e **não reverte** («ARQUIVOS VERIFICADOS; GUARDA FALHOU — NÃO REVERTIDO»).
- Ordem que G1 deve impor [PROPOSTA]: perna 1 inteira (E00 a E19) e só depois a perna 3 com `--publicar`; ou a perna 3 sem `llms_site`, `sitemap`, `manifesto`, `subir_ensaio`, `subir` quando a perna 1 já os fez (`--so` lista os passos). Uma trava comum (§2, E00) impede as duas ao mesmo tempo.

**Perna 4 (quadro, ACOM, rotas).** `estado_do_organismo.py` é o gatilho (E00) e a pós-condição (E20). Suposições dele que valem para a perna 1: P = N-1 (`BK.glob("um_v%d_*" % (N-1))`) e `v3\d\d` (L15, L20). O registro no mapa de rotas e a transição ACOM são da perna 4 e vêm depois de E20.

**Outras sessões que escrevem nas mesmas superfícies [DECLARADO pelas rotas e memórias]:** c1/Nós (selo, handoff, `cadeia_de_selo`), a7/Central (esta esteira), Kimi (`/central/` e `frontend\`, handoff `HANDOFF_KIMI_PARA_CLAUDE_ETAPA1_CENTRAL_20261023.md`), Codex (ORDEM 020: Cloudflare/WAF; `.htaccess`, que entra no manifesto como «A ENVIAR SEMPRE»). Nenhuma delas é consultada por E00 hoje.

---

## 6. Contrato mínimo sugerido para `tools\custodia_g1\` (perna 1)

[PROPOSTA — o que a especificação acima exige, sem desenho além disso.]
- **Contexto** (imutável, lido uma vez): N, P, PIN16 de N e P, caminhos (`NOS`, `TB`, `ESP`, `SITE`, `BANC`, `BK`, `CEN`), `fatos` (superset do `fatos_vN.json` atual + `P`, `pinP`, `backup_dir`, `recibos_bn`, `dic_names`, `diffs`, `contratos`, `registros_novos`, `modulos_novos`, `bandeiras_novas`, `blocos_do_handoff`), parâmetros (`sessao`, `trailer`, `ordem_do_operador` como caminho+sha16, `data`).
- **Passo** = {`id`, `pre(ctx)` → lista de falhas, `ja_aplicado(ctx)` → bool (a marca de cada passo desta especificação), `executar(ctx)` → resultado, `pos(ctx)` → lista de falhas}. Falha de leitura é falha visível; nada de `tail` escondendo rc.
- **Relatório por passo** em `work\custodia_G1\runs\vN_<stamp>\E##.json`: comando, rc, últimas linhas, duração, e sha256 antes/depois dos arquivos que o passo escreveu.
- **Modos**: `--ate E##`, `--so E##,E##`, `--ensaio` (nada de commit, push, subida; e nada gravado em `v3.0`), `--publicar` (liga E10, E11, E18; sem ele G1 para no commit local). Nunca `--force`, `--sem-guarda` nem `--permitir-ftp-em-claro`.
- **Códigos de saída**: 0 completo; 10 `WAIT` (EM_OBRA); 20 `STOP` com lista do que falta (handoff sem bloco, âncora ausente, gate); 30 falha de leitura; 40 divergência do ar/GitHub (E12/E18).
- **Viabilidade do ensaio em cópia** [MEDIDO]: os geradores do espelho (`gerar_estado_atual`, `gerar_portas`, `gerar_readme_frente`, `verificar_portas`, `guarda_do_selo`, `pos_push`) usam raiz relativa a `__file__` (rodam em um clone); os da bancada (`gerar_read_brief`, `gerar_llms_site`, `gerar_head_camada_texto`, `gerar_secoes`, `aplicar_selo`, `gerar_llms_full`, `gerar_index_md`, `gerar_sitemap`, `leitor_ia`) têm `ESP = r"C:\IALD\Artigo\the_boundary"` fixo, `atualizar_dados_selo_site.py` tem `TB` e `BK` fixos, e `subir_site.py` tem o caminho da guarda fixo. Um ensaio em clone exige parametrizar essas raízes (variável de ambiente ou argumento) por patch contado em arquivo novo, ou aceitar o ensaio só como `--conferir` + comparação de sha256 das saídas.
- **Teste de aceitação com a v398** [PROPOSTA]: a v398 foi feita à mão, está commitada no espelho (`35e8cdf6`) e em subida. Terminada a subida, rodar G1 em ensaio sobre a v398 (fatos da v398, handoff v398, ordem do operador de 23/10) e comparar, byte a byte, com o espelho em `35e8cdf6` e com o site subido, **exceto** os campos de prosa da §3.2 (que G1 recebe por bloco ou molde) e os carimbos de data e hora normalizados (§E08). Todo byte diferente fora disso é defeito de G1 ou lacuna desta especificação. As diferenças de L02, L03 e L04 existem na referência e G1 deve corrigi-las: entram na comparação como «diferença esperada», uma a uma. O espelho de referência é lido por `git worktree` em outro caminho, para não colidir com a custódia seguinte.

---

## 7. Fontes lidas

Tudo lido no disco por script de leitura; hashes e tamanhos abaixo foram calculados agora (não digitados). Se um destes arquivos mudar, a parte correspondente da especificação precisa ser relida (a outra sessão está mexendo na esteira).

**Scripts, handoffs e pastas de trabalho** (a perna 1 inteira, mais as peças das pernas 2, 3 e 4 que a tocam):

| arquivo | bytes | sha16 | modificado |
|---|---:|---|---|
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v395_passo0_backup.py` | 7,006 | `5d701546bf7fad5e` | 2026-10-21 17:59 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v396_passo0_backup.py` | 7,082 | `93e5d1abeb98c792` | 2026-10-22 19:57 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v397_passo0_backup.py` | 7,223 | `429b49cb85c0d9f7` | 2026-10-23 17:21 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v398_passo0_backup.py` | 7,090 | `dc001710c828d63f` | 2026-10-24 08:47 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v395_espelho.py` | 35,544 | `dc0960c8ba086170` | 2026-10-21 17:59 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v396_espelho.py` | 37,104 | `840dde8783d7aa9c` | 2026-10-22 19:57 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v397_espelho.py` | 38,707 | `b93ca1de38298e52` | 2026-10-23 17:25 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v395_geradores.py` | 16,873 | `691b3ccb7a1dce51` | 2026-10-21 18:06 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v396_geradores.py` | 20,480 | `d2a58e22e27bbd79` | 2026-10-22 20:13 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v397_geradores.py` | 21,338 | `efbbcbcb1946b7b6` | 2026-10-23 17:41 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_read_brief.py` | 26,903 | `c1fb48259afa4e2f` | 2026-10-07 21:09 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_llms_site.py` | 14,576 | `4c58cd4fda03664d` | 2026-10-23 08:20 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_head_camada_texto.py` | 9,901 | `ca9a920388a8a409` | 2026-10-07 21:00 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_secoes.py` | 18,079 | `d8a408d26dc00974` | 2026-10-07 19:28 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\atualizar_dados_selo_site.py` | 12,575 | `d3b122b444c7e9c4` | 2026-10-07 18:25 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\aplicar_selo.py` | 8,524 | `66dcf5e2dbd1801b` | 2026-10-14 14:50 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_llms_full.py` | 8,369 | `a51c4beb41e27ffc` | 2026-10-07 21:21 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_index_md.py` | 9,815 | `fcd6f5eed891fa85` | 2026-10-07 21:08 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_sitemap.py` | 4,611 | `50ebb76190b0257d` | 2026-10-22 12:14 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_manifesto.py` | 4,252 | `097b181cf55870bd` | 2026-09-11 09:47 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\subir_site.py` | 29,270 | `804facbdceccc8d4` | 2026-10-07 20:57 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\leitor_ia.py` | 6,578 | `b5ab720a27ffd48b` | 2026-10-07 21:11 |
| `C:\IALD\Artigo\the_boundary\tools\gerar_estado_atual.py` | 110,787 | `187dd5fef736e714` | 2026-10-23 17:47 |
| `C:\IALD\Artigo\the_boundary\tools\gerar_portas.py` | 100,414 | `b51f7e5f57d27caf` | 2026-10-07 20:12 |
| `C:\IALD\Artigo\the_boundary\tools\gerar_readme_frente.py` | 21,101 | `cc3f68acaabb2209` | 2026-10-23 17:59 |
| `C:\IALD\Artigo\the_boundary\tools\verificar_portas.py` | 9,398 | `e792a7752c992c90` | 2026-09-17 08:55 |
| `C:\IALD\Artigo\the_boundary\tools\guarda_do_selo.py` | 6,959 | `adad9c022dde75dd` | 2026-10-19 18:48 |
| `C:\IALD\Artigo\the_boundary\tools\guarda_do_site.py` | 3,845 | `31cc1979effd76cc` | 2026-09-11 16:02 |
| `C:\IALD\Artigo\the_boundary\tools\pos_push.py` | 5,300 | `d82730bf0fa52d29` | 2026-10-07 20:13 |
| `C:\IALD\Artigo\the_boundary\tools\estatuto_tres_apoios.py` | 46,367 | `e5c6a3c5c7b0ef95` | 2026-10-19 18:42 |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\patch_readme_v397.py` | 3,614 | `99f72a9afdabc04f` | 2026-10-23 17:41 |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\patch_readme_v397b.py` | 6,410 | `b55b6c7a6122c17b` | 2026-10-23 17:57 |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\patch_readme_v397c.py` | 2,383 | `617553510289f948` | 2026-10-23 17:58 |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\derivar_espelho_v397.py` | 4,229 | `7048daa1a0bd6e48` | 2026-10-23 17:25 |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\derivar_passo0_v397.py` | 1,815 | `e1b92905097dbb0f` | 2026-10-23 17:20 |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\sondar_v397.py` | 5,982 | `a1f1bd2b39f6d06a` | 2026-10-23 17:18 |
| `C:\IALD\Central de Patentes\work\custodia_v397_23out\fatos_v397.json` | 2,410 | `27e107f4c3d8f0eb` | 2026-10-23 17:19 |
| `C:\IALD\Central de Patentes\work\central_publica_22out\atualizar_central_publica.py` | 6,989 | `968cdc13ee88bc49` | 2026-10-23 15:21 |
| `C:\IALD\Central de Patentes\tools\estado_do_organismo.py` | 30,951 | `14f407f32b3f1f36` | 2026-10-24 08:47 |
| `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v397_CUSTODIA.md` | 13,643 | `5efc1157be1b0eb0` | 2026-10-23 17:17 |
| `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v398_CUSTODIA.md` | 19,061 | `29cc6c45ec520aa7` | 2026-10-24 01:40 |
| `C:\IALD\Site\tgl\v3.0_bancada\HANDOFF_KIMI_PARA_CLAUDE_ETAPA1_CENTRAL_20261023.md` | 3,510 | `dd2a28559f544a90` | 2026-10-23 18:23 |

**Estado do mundo no momento da leitura** (HEAD do espelho: `35e8cdf6 2026-10-24 09:11:44 -0300`):

| arquivo (estado medido no momento da leitura) | bytes | sha16 | modificado |
|---|---:|---|---|
| `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` | 166,716 | `7b46af660e7cb895` | 2026-10-24 01:31 |
| `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json` | 12,895,671 | `d9cc6b16a6784488` | 2026-10-24 01:05 |
| `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\MEMORIA_DA_LINHAGEM.md` | 1,085,526 | `7f02097ffeb27d7a` | 2026-10-24 01:33 |
| `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_en.txt` | 966,920 | `346f8ac1e7f02656` | 2026-10-24 01:05 |
| `C:\IALD\Artigo\the_boundary\README.md` | 40,941 | `ca4c76f7bc53f157` | 2026-10-24 09:09 |
| `C:\IALD\Artigo\the_boundary\ESTADO_ATUAL.md` | 107,269 | `938b3afbc6fd8a96` | 2026-10-24 09:09 |
| `C:\IALD\Artigo\the_boundary\LEDGER.md` | 713,530 | `e409518955960cfc` | 2026-10-24 09:09 |
| `C:\IALD\Artigo\the_boundary\CITATION.cff` | 3,689 | `a52edb4d58e5a224` | 2026-10-24 09:09 |
| `C:\IALD\Artigo\the_boundary\read-brief.md` | 22,188 | `c0143673289afc91` | 2026-10-24 09:09 |
| `C:\IALD\Artigo\the_boundary\TUNEL.json` | 1,245,540 | `d4deb0addb1ae53c` | 2026-10-24 09:09 |
| `C:\IALD\Artigo\the_boundary\PORTA.json` | 110,428 | `e3a9e18971800d54` | 2026-10-24 09:09 |
| `C:\IALD\Site\tgl\v3.0\index.html` | 158,500 | `e229420f68e3e46b` | 2026-10-24 09:15 |
| `C:\IALD\Site\tgl\v3.0\i18n.js` | 155,088 | `c1952a38e1af8579` | 2026-10-24 09:15 |
| `C:\IALD\Site\tgl\v3.0\read-brief.md` | 22,188 | `c0143673289afc91` | 2026-10-24 09:09 |
| `C:\IALD\Site\tgl\v3.0\llms-full.txt` | 154,282 | `57f914701c5d48f7` | 2026-10-24 09:15 |
| `C:\IALD\Central de Patentes\work\custodia_v398_24out\fatos_v398.json` | 3,357 | `da3793d738ddf6d2` | 2026-10-24 08:42 |

**Lidos depois (09:20 a 09:30), quando a outra sessão já tinha escrito a custódia v398** (o `gerar_estado_atual.py` abaixo é o estado após o remendo das 09:09; os demais da tabela anterior não mudaram):

| arquivo | bytes | sha16 | modificado |
|---|---:|---|---|
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v398_espelho.py` | 40,354 | `b13b5006271a4e05` | 2026-10-24 09:04 |
| `C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v398_geradores.py` | 24,352 | `611ebc14dc1589b3` | 2026-10-24 09:09 |
| `C:\IALD\Artigo\the_boundary\tools\gerar_estado_atual.py` | 119,600 | `b0f2e2f8461f8d30` | 2026-10-24 09:09 |

**Lido, não tabelado:** `C:\IALD\Artigo\the_boundary\.gitignore`, `.github\workflows\kernel.yml`, `.gitattributes`; `work\custodia_v396_22out\cadeia_v395_comandos.txt` e `cadeia_central_publica_comandos.txt` (transcrito extraído); `work\custodia_v397_23out\{sondar_v397.py, fatos_v397.json, acom_*.py, registro_*.py}`; `work\custodia_v398_24out\{sondar_v398.py, fatos_v398.json}` e a listagem de `work\cadeia_de_selo\v398`; `C:\IALD\MAPA_DE_ROTAS` (consulta «custodia», rotas `custodia.v393_v394.conjunta`, `custodia.v395`, `custodia.v396`, `custodia.v397`); memória `custodiar-quando-o-handoff-aparecer-23out.md` e `handoff-v397-custodia.md`.

**Não li (de propósito):** `.env` do site e qualquer coisa em `~/.tgl_site`, `~/.iald_privado`, `~/.iald_keys`; o conteúdo dos arquivos privados de marcadores e de termos proibidos (só sei que existem por exigência do código).

**Li só em diagonal:** `gerar_portas.py` (1.669 linhas: li `ler_selo`, `main` e o cabeçalho; não li cada descritor), `estatuto_tres_apoios.py` (532 linhas: cabeçalho e `ler`), `gerar_llms_full.py`, `gerar_index_md.py`, `gerar_secoes.py`, `gerar_llms_site.py` (cabeçalhos, entradas, saídas e asserts), `subir_site.py` (modos e comparação; não li `transporte_sftp.py`).

---

## 8. Lacunas

Ordem: o que o resultado da v398 confirmou e bloqueia o primeiro uso real de G1 (L01 a L07), gates frouxos (L08 a L14), robustez (L15 a L22), limites desta leitura (L23). Quando uma medida é de antes do commit da v398, o texto diz «estado v397». Severidade em maiúsculas; evidência com o estatuto.

### A. Confirmados pelo resultado da v398 e bloqueantes para o primeiro uso real

**L01 — ALTA — o README não tem folga para o parágrafo novo.** [MEDIDO] `README.md` = 40.941 B contra o teto de 40.960 B (folga de 19 B). A nota do 4,44 já custa 453 B; os blocos prontos do handoff v398 pesam 2.298 B (`README_v397`) e 2.630 B (`SONICO_v398`). Seções do README: AS PORTAS 7.640 B, «Proved on three supports» 4.928 B, «The core on one page» 6.589 B (mais 2.730 B em PT), «Citing This Work» 3.296 B, «Read in this order» 829 B. Efeito: `gerar_readme_frente.py` para com «a frente passou de 40 KB» ao incluir o item do sônico; a v397 precisou de 3 scripts de aperto (PRO-19). Ação: decisão estrutural antes da v398 — mover «Read in this order» (829 B) para o ESTADO_ATUAL, que já tem «Reading order»; fixar um slot «última custódia» com orçamento (até 1,2 KB) alimentado pelos registros, como a nota do 4,44, com recusa visível e nunca truncamento. **Resultado na v398** [MEDIDO às 09:25]: o README ficou em 40.941 B e o parágrafo do sônico não entrou (0 ocorrências de «sônico», «sonic» e «afina»), embora o handoff v398 peça README e site.

**L02 — ALTA — o ESTADO_ATUAL.md vai passar de 100.000 caracteres.** [MEDIDO, estado v397] 99.323 B e 97.440 caracteres (normalizado para LF); «## Reading order» começa no caractere 94.608; crescimento por custódia nos commits: +3.687 B (v395), +7.016 B (v396), +6.870 B (v397). O próprio README diz que leitores reais cortam perto de 100.000 caracteres (medida de 19/09). Com +7 KB, a v398 empurra «Reading order» e as instruções de download para depois do corte: a página quebra a regra que ensina. Ação: blocos por versão anterior a N saem do ESTADO (ficam no LEDGER, que já os recebe); o ESTADO guarda o bloco da versão corrente e uma tabela de uma linha por versão (dado, não código; ver PRO-15). **Resultado na v398** [MEDIDO às 09:25]: `ESTADO_ATUAL.md` = 107.269 B brutos (+7.946 B sobre a v397; 461 quebras CRLF, 105.657 caracteres brutos, 105.196 normalizado para LF); «## Reading order» no caractere bruto 102.802 (102.363 normalizado), isto é, **depois** do corte de 100.000; já está no commit `35e8cdf6`.

**L03 — ALTA — rótulo errado do Teste da Única Palavra no README da v398.** [LIDO] `gerar_readme_frente.py` l.263–267 imprime `(versao, data)` do selo corrente ao lado de `_k`, o registro `teste_de_veracidade_fase9_v\d+` de maior chave (v397 enquanto não existir outro). Na v398 sairia «The Unique Word Test (v398, 2026-10-24 00:26:08) … read from registry teste_de_veracidade_fase9_v397». O número corrige a frase, e aqui a frase estaria errada. Ação: versão = sufixo da chave do registro; data = a do bloco do diário daquela versão. **Resultado na v398** [MEDIDO]: o README commitado diz «The Unique Word Test (v398, 2026-10-24 00:26:08) `[REAL: read from registry teste_de_veracidade_fase9_v397]`»; o texto escrito à mão no `NOTA` do ESTADO diz certo («the Unique Word Test, v397, …»).

**L04 — ALTA — a ordem de geração deixa números citados defasados; o ponto fixo hoje não é testável.** [MEDIDO, estado v397] `read-brief.md` (site e espelho) e `llms-full.txt` citam README = 40.942 B (TUNEL e disco: 40.941) e `secoes/04-…` = 13.427 B (TUNEL: 13.429): 2 de 10 citações de tamanho. `gerado_utc` com segundos em todo `PORTA.json` e `TUNEL.json` (`gerar_portas.py` l.841, 1006, 1647) impede comparar bytes entre passadas. Ação: ordem, ponto fixo normalizado e auditor de números citados de E08. **Resultado na v398** [MEDIDO às 09:25]: o defeito voltou com outros arquivos — `secoes\07-…` citada como 11.762 (TUNEL 11.731) e `secoes\08-…` como 13.472 (TUNEL 13.411) em `read-brief.md`, `llms.txt` (site) e `llms-full.txt`, que estão sendo subidos.

**L05 — MÉDIA (resolvida à mão na v398; fixar como regra) — âncora do ESTADO e bloco repetido no handoff.** [LIDO] até a v397 a âncora era «Errata beside (23/10/2026, the custody of v397» (l.508 de `gerar_estado_atual.py`) e o parágrafo da v397 estava na l.510; `patch()` insere logo depois da âncora, de modo que o bloco da v398 teria ficado entre o ERR e o parágrafo da v397. [MEDIDO] o handoff v398 repete o bloco `INICIO_PARAGRAFO_README_v397`. A outra sessão evitou os dois defeitos à mão: trocou a âncora para as linhas `L.append("")` e `L.append("## What is PROVED …")` (insere antes) e comparou por bytes o bloco repetido com o do handoff v397; o parágrafo da v397 ficou no caractere 71.730 e o cabeçalho `### v398` no 73.920. Ação: tornar as duas decisões regra de G1 (§3.1, PRO-15); a âncora «antes de What is PROVED» é estável para todas as versões.

**L06 — ALTA — valores digitados e contagens que quebram na v398.** [MEDIDO] 22 sha16 digitados no espelho v397 e 3 nos geradores (§4). Executar a lógica da v397 sobre os fatos da v398 pararia no primeiro assert: 7 contratos em vez de 5, 2 módulos novos em vez de 1, 40 bandeiras novas em vez de 1, 4 registros novos em vez de 3. Ação: invariantes no lugar de igualdades (§4). **Resultado na v398** [MEDIDO]: `custodia_v398_geradores.py` reescreveu esses asserts à mão (`NBAND == 40`, `len(CONTRATOS) == 7`, `KN.bandeiras == [2, 2]`, `declaracoes_no_trio == [41, 41]`, listas de módulos e de registros; 317 linhas diferentes no diff contra o v397) e `custodia_v398_espelho.py` ganhou `_H398` e a exclusão de `bateria_pre_selo`.

**L07 — ALTA — a prosa da versão não tem fonte automática.** [MEDIDO] §3.4: faltam título EN, cláusulas EN do `TXT` e do arco, itens 3 e 4 do `ERR`, corpo do commit, ordem do operador (arquivo verbatim) e trailer. O handoff v398 não traz os blocos propostos em §3.1. Ação: acrescentar os marcadores ao gerador do handoff (a sessão do Nós) ou aceitar o molde de §3.3 com STOP e lista; a tradução EN/PT não deve ser automática sem fonte selada. **Resultado na v398**: a outra sessão escreveu à mão o `TXT`, o `ERR`, o `NOTA`, o `BLOCO`, o `EN8`/`PT8` e o corpo do commit (§3.4).

### B. Gates frouxos

**L08 — MÉDIA — `verificar_portas.py` não tem código de saída.** [LIDO] 216 linhas, nenhum `sys.exit` nem `SystemExit`; a falha só aparece em `VEREDITO: FALHOU`. Ação: acrescentar `sys.exit(1 if erros else 0)` (patch contado) ou ler `ERROS ... N` e o veredito do stdout.

**L09 — MÉDIA — gates que só imprimem.** [LIDO] (a) a varredura de arquivos sensíveis antes do `git add -A` usa `;` e `head -5`; (b) `campos_com_CONFIRMED_a_ler` do espelho só é impresso; (c) `[ATENCAO] o sha256 de um.py em disco DIFERE do pin do selo`, de `gerar_portas.py`, só imprime; (d) o laço de E07 e as cadeias com `tail -1` escondem o rc; (e) `fontes_pinadas.fora` (1 de 254 na v397, o `KH_N1_v392.json` da casa) só aparece no relatório; (f) em `TUNEL` e `FONTE_TUNEL`, arquivo com termo-guarda é pulado e só dito. Ação: tornar (a) a (e) bloqueantes, com lista permitida explícita.

**L10 — ALTA — escopo da subida.** [LIDO] `gerar_manifesto` lista o `v3.0` inteiro (inclui `central\`) e `subir_site` envia tudo que difere do ar; `.ht*` entra sempre; ensaio e subida baixam o site inteiro (arquivos até 64 MB) duas vezes. Sem conjunto esperado, a perna 1 pode publicar meio-trabalho da perna 3 e das sessões do Kimi e do Codex. Ação: conjunto esperado em E17 e, quando possível, `--so` com a lista dos arquivos escritos nesta custódia.

**L11 — MÉDIA — passos duplicados com a perna 3.** §5: `llms_site`, `sitemap`, `manifesto`, `subir_ensaio` e `subir` existem nas duas; `gerar_llms_site.py` precisa do `um_acom_info.json` da perna 3. Ação: ordem única e trava comum (§5).

**L12 — MÉDIA — o CI do GitHub não é consultado.** [LIDO] `.github\workflows\kernel.yml` (build do kernel e auditoria dos termos, até 120 min, dispara em mudança de `Lean/**`, como os módulos novos da v398); E12 só confere bytes. [MEDIDO] `gh` 2.100.0 está instalado. Ação: registrar no relatório o estado da execução do workflow (consulta assíncrona, que não bloqueia a subida).

**L13 — MÉDIA — sem trava nem exigência de árvore limpa.** [MEDIDO] durante esta leitura outra sessão custodiou a v398 na mesma árvore; `git add -A` varre tudo. Ação: §2, E00.

**L14 — BAIXA — o passo zero só roda uma vez.** [LIDO] depois de E03 o assert `pin_esp == PIN["vP"]` falha; E02 depois de E03 estraga o relatório de que E04 depende. Ação: marcas de idempotência de E01 a E03 (§2).

### C. Robustez

**L15 — MÉDIA (vence na v400) — `v3\d\d` fixo.** [MEDIDO] `custodia_vNNN_passo0_backup.py` l.63 (`(v3\d\d) SELADA`) e `estado_do_organismo.py` l.107. Na v400 o passo zero não acha o pino de P e o medidor nunca vê a v400 selada. Ação: `v\d{3}`.

**L16 — MÉDIA — depósito Zenodo digitado.** [MEDIDO] nos geradores v397 o DOI aparece em 5 linhas (docstring, `NOTA`, `BLOCO`, regex e troca do CITATION), o pino do depósito em 2 e «holds v392» em 6. Quando o operador depositar uma versão nova (ato dele), esses lugares ficam errados. Ação: ler a linha «Zenodo deposit of vK» e o `doi:` do `CITATION.cff`, como os outros geradores já fazem.

**L17 — ALTA — autoridade e portões.** A memória diz que «a subida é da gerência» e que os textos públicos passam por três portões (asserções, gate de pré-push, revisor distinto) [DECLARADO]. [MEDIDO] não há hook de pré-push (`.git\hooks` sem hooks ativos, `core.hooksPath` vazio): o «gate de pré-push» não está codificado. Ação: definir os três portões como passos de G1; `--publicar` explícito para E10, E11 e E18; decisões reservadas ao operador (Zenodo, nomes de pedras e de registros, [LEGAL], reescrita de histórico público) ficam fora e viram `STOP`.

**L18 — MÉDIA (decisão da gerência e do operador) — a regra do 4,44 «em tudo mais» e os dois z_disc.** [MEDIDO] o README mostra duas vezes o z_disc: 4,28 (V1, `hubble_ratio_opening_v388`, no texto do estatuto) e 4,44 (nota do Teste da Única Palavra). `index.md` e `llms-full.txt` do site têm o 4,28 e `read-brief.md` e `llms.txt` não citam z_disc; nenhum dos quatro tem o 4,44, embora a ordem de 23/10 peça o z_disc calibrado no início do artigo, no README «e em tudo mais». O módulo `estatuto_tres_apoios.py` só lê o V1. Ação: decidir qual número o módulo do estatuto reporta e como cita o outro; só então propagar.

**L19 — BAIXA — prosa copiada com erro e documentação incompleta.** [MEDIDO] `custodia_v398_passo0_backup.py` repete na docstring «CUSTÓDIA v396 (21/10, handoff v396; molde v394 …)» (o certo: 22/10, molde v395); o `nao_levados` do espelho tem 26 chaves e nenhuma cita v395, v396 ou v397. Ação: f-strings (PRO-01) e uma entrada gerada por versão (PRO-18).

**L20 — MÉDIA — fragilidades do site e do medidor.** (a) `atualizar_dados_selo_site.py` tem 19 âncoras com contagem exata e E04 exige o arco anterior idêntico ao JSON: edição alheia do `index.html` ou do `i18n.js` derruba a custódia (fail-closed, sem diagnóstico guiado). (b) O medidor assume P = N-1 (`BK.glob("um_v%d_*" % (N-1))`): numa custódia conjunta dá DEFASADO falso; [MEDIDO] não existe `um_v393_*` em `the_boundary_BACKUPS`.

**L21 — BAIXA — custódia conjunta e listas fixas.** `STDOUTS`, o nome `DIFF_v{N-1}_vN.diff` e `bm["versao"]` supõem a sequência; `CANDIDATOS` do sitemap é lista escrita no código (página nova do site não entra sozinha); o `lastmod` do sitemap é a data de modificação do arquivo.

**L22 — BAIXA — fim de linha, backups e idempotência por dia.** [MEDIDO] os `custodia_vN_espelho.py` (v395 a v398) e os `…passo0_backup.py` (v395 a v397), derivados por `write_text` no Windows, estão em CRLF; os `…geradores.py`, escritos à mão, e o `custodia_v398_passo0_backup.py` estão em LF; `Path.write_text` no Windows grava CRLF — [MEDIDO] no espelho só o `ESTADO_ATUAL.md` está em CRLF (461 quebras), enquanto README, LEDGER, CITATION, read-brief, llms.txt, TUNEL e PORTA estão em LF, e no site tudo está em LF (G1 deve abrir com `newline=""` e preservar o fim de linha de cada alvo); os geradores do site gravam `.bak_<STAMP>` a cada rodada, mesmo sem mudança (acumulam em `v3.0`, que o manifesto exclui); README e PORTA levam data, então a mesma custódia rodada em outro dia muda bytes.

### D. Limites desta leitura

**L23 — o que esta especificação NÃO prova.** Nenhum script foi executado: o comportamento em tempo de execução vem da leitura do código e do transcrito da v395 (tempos são limites superiores); «duas voltas bastam» e «o ponto fixo converge em poucas passadas» são hipóteses não testadas; não li `transporte_sftp.py`, nem `gerar_portas.py` inteiro (só `ler_selo`, `main` e o cabeçalho), nem o código interno dos descritores; não fiz nenhuma chamada de rede (nada foi conferido no ar, no GitHub nem no CI); as medidas de tamanho e as citações defasadas são do disco às ~09:00 de 24/10 e a sessão que custodia a v398 pode já tê-las mudado; os arquivos privados e as credenciais não foram lidos; a memória ACOM não foi inscrita (§0).
