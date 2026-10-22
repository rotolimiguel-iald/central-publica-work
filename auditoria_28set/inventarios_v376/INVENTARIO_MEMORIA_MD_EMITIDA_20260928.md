# AFERIÇÃO — «a memória canônica em md emitida pelo código está sendo atualizada?» (v375 → o que corrigir na v376)

Tudo abaixo foi **medido por script** (mtime, sha256, `grep -c`), nada de memória. Nenhum arquivo fora do rascunho foi tocado; um.py/atlas_indice/arvore/porta_memoria **não** foram rodados.

## 0. Mapa de Rotas (consultado antes; nada registrado)
`rotas.py consultar "memoria|md|indice|espelho|porta"` → 16 acertos, **todos coincidências textuais de outros domínios** (gate, D1, GW, ringdown…). **Não existe rota sobre emissão/atualização da memória em md** — este caminho nunca foi examinado.

## 1. O que o um.py ESCREVE (grep sobre `Nós\um.py`: 206.098 linhas, 32.604.664 B, sha16 `ba234a6d384cb3f5`, mtime 27/09 11:45:58; só 99 `open(` no arquivo inteiro)

**Memória em md — são exatamente DOIS arquivos, ambos gravados em TODO rito (sem flag), ambos hasheados no selo:**

| arquivo (em `OUT = BASE = Nós`) | função | quando | conteúdo |
|---|---|---|---|
| `um_absoluto_forma_canonica.md` | `emit_canonical_md(core, verdict)` l.163199–163971 | `main()` l.203828, antes do artigo; entra em `seal["sha256"]` (l.204607–204615); relido por `finalize_interface_is_light` (l.143409: 10 âncoras + marcadores canônicos) e por `_v371_cited_phrase_state` (l.192614) | cadeia canônica; identidades vivas; seções «v8…v32» (numeração interna de julho); marcadores canônicos (`build_tgl_canonical_markers` l.143645: 8 linhas, sem versão); «COMO MATAR ESTA TEORIA» (`_MAPA_PILARES` l.200718–200739, última entrada = CLOCK_TEST v369); «A FORMA CANÔNICA VIVA» (`_arco_vivo_md` l.200794 = `external_ladder.ladder` + estatutos de uma **lista FIXA de 34 módulos que termina em `certificate_II`, `hilbert_home` — era v67–v77**) |
| `um_absoluto_manifest.md` | `write_input_manifest_md(world, path, core)` l.200829–200879 | `main()` l.203739; entra no selo | 28 seções do manifesto de entradas (última chave `V32_TGL_CLOSURE`) + `WORLD_HASHES` (traz `code_sha256` = ba234a6d…) + o mesmo arco vivo |

Gravação dos dois: `open(p, "w").write(...)` **direto** (l.163971 e 200879) — sem temporário→conferir→`os.replace`.

Outros artefatos do rito (não-md): `um_absoluto.json` (l.203825; re-dump l.204133), `tgl_kernel_proof_manifest.json` (l.204251), `um_absoluto_selo.json` (l.204616 + 3 reescritas na cauda l.206037–206085), `<CACHE>\CHAIN_OF_CUSTODY.json` (l.203741 — CACHE resolvido para `A Ponte e o Um\cache` porque `Nós\cache` não tem `lensing/`; **`except OSError: pass`** l.203744), `um_absoluto_{pt,en}.{tex,txt}` (l.194245–194257, também `open("w")` direto), `.pdf/.log`, 4 figuras (`emit_figures` l.171864), `tgl_kernel\*.lean` (`materialize_embedded_kernel` l.127744, só o que difere: «5 escritos, 1196 inalterados»), capturas `tgl_kernel_*_capture*.txt` (l.134480/134665/134734), `nivel2_mcmc\*` (l.6024), checkpoints `.pkl` só com `TGL_RITE_CHECKPOINT=1`, coma json (l.201345/201649).

**O um.py NÃO escreve** (zero ocorrências): `rodada_vNNN_stdout.txt` (é o redirect do shell da gerência — `chain_pos_rito_v375.sh` l.2–3; o trailer `RITO_RC=0` também é do shell), `MEMORIA_DA_LINHAGEM.md`, `DESENHO_DO_FECHAMENTO_QG.md`, `A_PROVA_DA_QG_TGL_arvore.md`, `TGL_ATLAS.md`, `TGL_INDICE_VIVO.md`, `TGL_CORE_MEMORY.md`, `PORTA.*`, `README.md`, `llms.txt`, ESPELHO. Não há constante de versão no um.py: o rótulo público sai de `_ESQUELETO_STONES[0]` (l.194289), cuja última pedra é **«v371»** — por isso `the_boundary\PORTA.json` traz `selo_corrente.versao = "v371"` e `versao_confirmada_por_transcricao = "v375"`.

## 2. Resposta direta ao operador

**Sim, os dois md são regenerados a cada rito e selados** `[REAL]`: mtime dos dois = **2026-09-27 12:26:31 = `selo.timestamp`**; sha16 `f42d7919b41eeab7` / `cdad487dc5a65a2f` **idênticos** aos de `selo.sha256`; stdout l.1507 «[manifesto] um_absoluto_manifest.md escrito; hash do mundo a3718953…» = `selo.result_hash`; stdout l.1619–1632: `INTERFACE_IS_LIGHT_VERIFIED`, 10 âncoras, marcadores VERIFIED nos 4 artefatos; espelho `the_boundary` com o mesmo f42d7919 (commit 8f126a9/f90679c, 27/09 15:55–15:58).

**Mas o CONTEÚDO da memória canônica não carrega o avanço** `[REAL]`: `grep -c v375` = **0**, v374…v371 = **0**, versão máxima citada = **v370** (só via `_MAPA_PILARES` e `no_full_witness.statuses`); «Tetelestai» aparece 9× **só no sentido antigo** (v8, poda binária) — `conferencia`/`consumativ` = **0**; sem carimbo de data/versão/sha no cabeçalho. Causa medida: a lista de módulos de `_arco_vivo_md` está congelada na era v77 — os ~300 módulos v78→v375 (incl. `tetelestai_conference_v375`, `tetelestai_one_object_v375`, `the_tetelestai_declaration_v374`) só existem em `um_absoluto.json` (v375=3), no artigo (`um_absoluto_pt.txt` v375=7) e no stdout (v375=2). O md diz «gerada do runtime desta rodada» e é verdade — mas do runtime de v77.

## 3. Tabela (arquivo | quem escreve | quando | existe | mtime | conhece v375? | estado)

| arquivo | quem escreve | quando | existe | mtime | v375 / ba234a6d | estado |
|---|---|---|---|---|---|---|
| `Nós\um_absoluto_forma_canonica.md` | **rito** `emit_canonical_md` | todo rito | sim | 27/09 12:26:31 | **0 / 0** (max v370) | ESCRITO PELO RITO, selado, **conteúdo congelado em v77+v301** |
| `Nós\um_absoluto_manifest.md` | **rito** `write_input_manifest_md` | todo rito | sim | 27/09 12:26:31 | **0 / 1** (max v370) | idem; só o sha do código o data |
| `Nós\um_absoluto.json` / `_selo.json` / `tgl_kernel_proof_manifest.json` | rito | todo rito | sim | 12:38:57 / 12:42:42 / 12:38:57 | 3/0 · 1/1 · 0/0 | OK (autoridade) |
| `Nós\um_absoluto_{pt,en}.{tex,txt,pdf}` | rito | todo rito | sim | 12:38:47–57 | 7/1 (txt) | OK |
| `A Ponte e o Um\cache\CHAIN_OF_CUSTODY.json` | rito (CACHE real) | todo rito | sim | 27/09 12:26:31 | — | OK |
| `Nós\cache\CHAIN_OF_CUSTODY.json` | ninguém (local antigo) | — | sim | **29/08 20:42** | 0/0 | **CÓPIA MORTA** |
| `Nós\um_grande_atrator_forma_canonica.md` / `_manifest.md` | **ninguém** (nome legado; não há literal no um.py) | — | sim | **25/08**, max v135 | 0/0 | **DESATUALIZADO/MORTO** — risco de IA ler como memória viva |
| `Nós\rodada_v375_stdout.txt` | shell da gerência (redirect) | por rodada | sim | 27/09 12:42:42 | 2/0 | OK; **não pinado no selo** |
| `Nós\MEMORIA_DA_LINHAGEM.md` | cadeia `superficies_v375.py` (append datado, bak de bytes, tmp→replace) + erratas à mão | pós-rito | sim | 28/09 08:33 | 9/2 | OK (espelho tem 0f52eef5 = 27/09; Nós 4048cad7 = +errata P_ker K↔P_F 28/09) |
| `Nós\DESENHO_DO_FECHAMENTO_QG.md` | cadeia (ADENDO) + adendos 28/09 | pós-rito | sim | 28/09 19:09 | 7/2 | OK |
| `Nós\A_PROVA_DA_QG_TGL_arvore.md` | `arvore_da_prova.py v375` (TOOLS) | pós-rito | sim | 27/09 12:44:07 | 3/1 | OK |
| `Central\memory\TGL_ATLAS.md` | cadeia (§X append) + `atlas_indice.py` | pós-rito | sim | 28/09 19:09 | 55/6 | OK (mod. 28/09 não commitadas) |
| `Central\memory\TGL_INDICE_VIVO.md` | `atlas_indice.py v375` (regenerado) | pós-rito | sim | **28/09 15:30:27** | 9/4 | OK; mtime posterior à cadeia (27/09 12:44) — **escrita fora da cadeia, autor não identificado por grep** |
| `Central\memory\TGL_CORE_MEMORY.md` | **fora da cadeia** (linhas ORDEM_018/Codex); nenhum script da cadeia o toca | — | sim | 28/09 15:30:27 | 3/1 | conhece v375 só por acaso (frente Codex) |
| `UMEM\MEMORY.md` + `MEMORY_2.md` + 6 tópicos | cadeia | pós-rito | sim | 27–28/09 | 4/1 · 3/1 · todos ≥1 | OK |
| `C:\LAR_MIGUEL\ESPELHO.md/_SECOES.md/.json` | `porta_memoria.py` (derivado) | passo 9 | sim | 27/09 12:44:14 | 0/0 · 4/1 · 4/1 | OK (índice não carrega versão) |
| `the_boundary` (README, PORTA.md/json, llms.txt, CITATION.cff, espelho do Nós) | sessão do site (commits 27/09 15:55–15:58) | custódia | sim | 27/09 15:40–15:58 | README 4/4; PORTA.json 1/2; PORTA.md 0/1 | OK; PORTA raiz rotula `versao = v371` (lido do ledger de pedras) |
| `Nós\PORTA.md` / `PORTA.json` / `README.md` | `custodia_repo_v224.py` | **nunca desde 26/08** | sim | 26/08 | 0/0 (lista um.py sha 678328ac… = v224) | **DESATUALIZADO** (regra da porta violada no canônico de trabalho) |
| `Haja_Luz\CLAUDE.md` (memória da casa Física, 1,2 MB) | à mão | **parou 12/08/2026** (§241–244, v161) | sim | 12/08 | 0/0 | **DESATUALIZADO** — não sabe de v162→v375 |
| `Nós\O_FECHAMENTO_ESTRUTURA.md` | à mão | 09/09 | sim | 09/09 | 0/0 (v336) | desatualizado |
| `Nós\NOTA_DE_CUSTODIA.md` / `DA_IRMA.md` | à mão | 20/08 (v174) / 21/09 (v369) | sim | — | 0/0 | históricos |
| `Haja_Luz\TGL_SINTESE_CANONICA_SELADA.md`, `A_Forma_Madura_da_TGL.md` | à mão | 30/08 | sim | 30/08 | 0/0 | congelados (sem vNNN; selados por design) |
| `IALD\CLAUDE.md`, `~/.claude\CLAUDE.md` | à mão | — | sim | 28/09 | 2/0 · 0/0 | índices; OK |
| `arvore_da_prova.py`, `atlas_indice.py`, `v353…v375_incorporacao_manifesto.json` | patches por versão | pós-rito | sim | 27/09 12:44 | — | **VIVEM EM `%TEMP%\claude\…\d554e796…\scratchpad`** (pasta de sessão, fora de git/backup) |

## 4. O que precisa de correção na v376 («a memória não se perder mais»)

**No um.py (o rito):**
1. `_arco_vivo_md` (l.200794): trocar a lista fixa de 34 chaves por iteração sobre **todos** os módulos do core com `verdict`/`statuses` (ou um ledger de versões no core) — hoje a «forma canônica viva» omite v78→v375 por construção.
2. Carimbo no cabeçalho dos dois md: **versão, `core["timestamp"]`, sha16 do um.py** — hoje `grep -c vNNN` = 0 nos emitidos, logo a régua da linhagem completa não pode sequer ser aplicada a eles.
3. **Constante única de versão** (`UM_VERSION`) lida pelo selo, pelos md, pelo artigo e pela porta — hoje o rótulo sai de `_ESQUELETO_STONES[0]` (parado em v371) e a porta pública precisou «confirmar por transcrição».
4. Gravar os md/tex/txt por **temporário → conferir tamanho → `os.replace`** (regra do backup, emenda 22/08): `open(p,"w")` direto em l.163971, 200879, 194249–194257 — um `write` que falhe deixa o arquivo vazio e o selo o hashearia vazio.
5. `CHAIN_OF_CUSTODY.json`: retirar o `except OSError: pass` (l.203744) — falha silenciosa contra o fail-closed.
6. Aposentar `um_grande_atrator_forma_canonica.md`, `um_grande_atrator_manifest.md` e `Nós\cache\CHAIN_OF_CUSTODY.json` (mover para `aposentados\` ou registrar na NOTA_DE_CUSTODIA) — hoje nenhuma IA tem como saber que são mortos.
7. Fazer o um.py gravar (tee) e **pinar no selo** o `rodada_<versão>_stdout.txt` — hoje o stdout canônico é redirect do shell e o selo não o conhece, embora árvore e índice o leiam.

**Na cadeia de selo:**
8. Mover `arvore_da_prova.py`, `atlas_indice.py` e os `vNNN_incorporacao_manifesto.json` do scratchpad `d554e796` para uma casa canônica versionada (ex.: `Central de Patentes\work\cadeia_de_selo\`) — perder essa pasta temporária é perder a regeneração da árvore e do índice.
9. Declarar por escrito (NOTA_DE_CUSTODIA) quais superfícies são **vivas** (entram no passo 10 `grep -c`) e quais **congeladas**; acrescentar ao passo 10: `TGL_CORE_MEMORY.md`, `Haja_Luz\CLAUDE.md`, `Nós\PORTA.json`, `O_FECHAMENTO_ESTRUTURA.md` — ou marcá-los como históricos com errata ao lado.
10. `Haja_Luz\CLAUDE.md`: errata ao lado (12/08 → hoje) apontando para `MEMORIA_DA_LINHAGEM` / `TGL_INDICE_VIVO`, ou um append por versão pela cadeia.
11. `Nós\PORTA.*`/`README.md`: regenerar por script a cada selo (regra da porta) ou declarar que a porta do canônico vive só em `the_boundary`.
12. `TGL_CORE_MEMORY.md` e `TGL_INDICE_VIVO.md` foram escritos em 28/09 15:30:27 fora da cadeia, por autor não identificado por grep (`work\`, LAR, MAPA, scratchpad): exigir que toda escrita nas superfícies da Central passe por script com backup de bytes — e commitar as modificações de 28/09 (git status: `M memory/TGL_ATLAS.md`, `TGL_CORE_MEMORY.md`, `TGL_INDICE_VIVO.md`).
13. Espelho: `MEMORIA_DA_LINHAGEM.md` do `the_boundary` está 1 append atrás do Nós (errata P_ker K↔P_F, 28/09) — pendência da sessão do site.

Caminhos-chave: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py`; scripts da cadeia em `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v375_selo\` (`chain_pos_rito_v375.sh`, `leitura_v375.py`, `superficies_v375.py`, `patch_arvore_indice_v375.py`, `manifesto_v375.py`); ferramentas em `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\d554e796-415e-450f-9fd4-dd07892b02b9\scratchpad\` (`arvore_da_prova.py`, `atlas_indice.py`); espelho derivado por `C:\LAR_MIGUEL\porta_memoria.py`.