# Plano da Fase B — app/JEV v398 (NÃO executar sem ordem da gerência)

Estatutos: [REAL] medido/lido aqui, [DECLARADO] afirmado numa fonte e não verificado aqui, [OPEN] pendente. Nada neste plano foi executado: a Fase A só preparou arquivos em `iald_v398_20261024\` (nenhum serviço tocado, nenhuma geração paga). Consulta ao Mapa de Rotas antes de preparar: `rotas.py consultar "app v395"` → 0 rotas, 1379 registros, cabeça `743781e933da392d` [REAL].

```powershell
$PY = 'C:\Python314\python.exe'            # sempre sem -I (psutil/anthropic/dotenv/tiktoken estão no site do usuário)
$W  = 'C:\IALD\Central de Patentes\work\iald_v398_20261024'
```

## 0. O que a Fase A deixou pronto [REAL]

| Arquivo | Origem | Observação |
|---|---|---|
| `app\RELEASE.json` | novo | `release=v398`, `espelho_commit=null`, `um_py_sha256` lido do selo (Nós = cofre = hash dos bytes do `um.py`) |
| `release_cfg.py` | novo | lê `RELEASE.json`, deriva cofre/unidade/datas/sufixos; `load(require_commit=True)` **para** com mensagem clara se o commit for `null` |
| `app\prepare.py`, `finalize.py`, `count_final_public.py`, `validate_plan.py` | v395 + substituições asseguradas | zero literal de versão; `prepare` usa o commit FIXADO (não o HEAD) |
| `task.py`, `verify_sources.py`, `verify_installed.py`, `review\review_app.py` | v395 (verify_installed = variante R2 corrigida) | `task.init` exige `ORDEM_DO_OPERADOR.txt` verbatim; `review_app.py <id>` exige revisor ≠ dono/construtor |
| `transaction.py`, `maintenance.py`, `deploy_controlled.py`, `app\build\*.py` | cópia **byte a byte** da v395 | os 3 primeiros têm o mesmo sha256 que o `review_final.json` da v395 fixou |
| `mission_step.py`, `app\preflight_offline.py` | novos | claim/submit/accept com ator explícito (não testado: não há missão); preflight somente leitura |
| `app\AUDITORIA_PARAMETRIZACAO.txt` | gerado | diff v395→v398 de cada arquivo + hashes lidos dos arquivos |

Não copiados de propósito: `install_plan.json` (é saída de `validate_plan.py`, com os hashes/caminhos da v395; a v398 gera o seu), `DATA_PLAN`, `PREPARED_BINDING`, `packages\`, `science\`, recibos e a missão ACOM da v395. Os originais da v395 não foram alterados.

## 1. Entradas que só a gerência fornece (B0)

1. **`espelho_commit`** em `app\RELEASE.json` (hash de 40 hex do commit da v398 já publicado). [REAL] Em 24/10 ~09:30 o HEAD local do espelho era `35e8cdf6ba461034f3b20fff118248c20ae922ec` ("custodia(v398)…", 09:11:44), com selo `v398`/pino igual; o `git ls-remote` mostrou o mesmo hash em `main` (chamada de rede inadvertida da Fase A). Com esse hash injetado **só em memória**, o preflight passou 100% (10 caminhos rastreados e iguais ao cofre, 5 fontes de hipótese únicas). O valor **não** foi gravado: a gerência decide. Gravar com backup de bytes (`RELEASE.json.bak_<stamp>`), temporário→conferir→substituir.
2. **`ORDEM_DO_OPERADOR.txt`** em `$W` com a ordem verbatim do operador para esta release (a da v395 foi «Atualize tudo com a versão nova do um.py.» [DECLARADO: reaproveitar exige confirmação]). O script não a inventa.
3. **Atores** em `release_cfg.py` (`OWNER=claude-gerencia-a7`, `BUILDER=sonnet-app-v398-construtor`; rótulos locais, não autenticação). O **revisor é outro id**, passado na hora.
4. **Corte do haiku55** (seção 3). Padrão automático = `('_v395','_v396','_v397','_v398')`. Para cortar: `EXPAND_OVERRIDE` em `release_cfg.py` **antes** do `finalize` (depois os arquivos são imutáveis).
5. **Janela de manutenção**: o filho web fica fora do ar por segundos (até 90 s para o `/login` 200). Avisar o operador; nenhuma tarefa/reserva ativa.

## 2. Passos

| # | Comando | Grava | Conferir / gate |
|---|---|---|---|
| B0a | `& $PY -B -X utf8 "$W\app\preflight_offline.py"` | nada | `ok:true`, exit 0 (hoje: 16/17 — falta só o commit) |
| B0b | `& $PY -B -X utf8 "$W\task.py"` | `ORIGINAL.txt`, `init_receipt.json`, `mission_configured.json`, `unit.json`, `SESSION_REFERENCE.json`; missão ACOM; unidade `F9.APP_V398_20261024` no quadro | `REGISTERED`. **Cria missão e unidade (efeito no ACOM/quadro)** |
| B0c | `& $PY -B -X utf8 "$W\mission_step.py" claim sources --actor claude-gerencia-a7` e `… claim app --actor sonnet-app-v398-construtor --lease-seconds 14400` | `receipts\*.json` | status `working`; o lease do `app` cobre B2–B6 |
| B1 | `& $PY -B -X utf8 "$W\verify_sources.py"` (parte 1 usou `--offline`: sem `git ls-remote`, `remote_main`/`release_ready` = null) | `sources_verified.json` | `release_ready:true`. **Rede: `git ls-remote origin`** (leitura, gratuita). Depois `mission_step.py submit sources --actor claude-gerencia-a7 --evidence "$W\sources_verified.json"` |
| B2 | `& $PY -B -X utf8 "$W\app\prepare.py"` | `app\RUNTIME_BASELINE.json`, `PUBLIC_GIT_BINDING.json`, `BUILT.json`, `science\memory_stage\**` (fontes do commit, kernel ~1428 `.lean`, cluster full/prompt, core, JEV, core_packet, manifests), `packages\haiku55\` e `packages\shared\` | sem rede; só AST do `um.py`; ~80 MB em disco (ensaio em sandbox: 32,5 s, OK); falha se `espelho_commit` for `null`, se o selo/pino divergir ou se o código de runtime mudar durante o build |
| B3 | `& $PY -B -X utf8 "$W\app\finalize.py"` | `packages\haiku_expanded\`, `packages\sonnet_public\prefix.md`, `native_prefix.md`, `science\memory_stage\manifest_install.json`, `DATA_PLAN.json`, `PREPARED_BINDING.json` | gancho de auditoria proíbe rede/`.env`/subprocesso (ensaio em sandbox: 10,7 s, OK). Imprime `estimated_remaining_tokens`; **aborta sem gravar** se < 15 000 |
| B4 | `& $PY -B -X utf8 "$W\app\count_final_public.py"` | por pacote: `*_count_intent.json`, `*_count_result.json`, `native_count.json`, `manifest.json`; `NATIVE_COUNTS_COMPLETE.json` | **único passo que chama a API Anthropic: 6 × `count_tokens`** (gratuitas [DECLARADO]), `max_retries=0`, zero geração, lê `IALD_CLAUDE_API_KEY` do `.env` sem imprimi-la. Barra se `remaining < 10 000`. Falha no meio **não se repete**: o script recusa; refazer a partir do B3 em pasta nova |
| B5 | `& $PY -B -X utf8 "$W\app\validate_plan.py"` | `packages\*\manifest_install.json`, `$W\install_plan.json`, `$W\validation\final_checks.json`, `app\DELIVERY_PREPARED.json` | carrega os pacotes com os loaders atuais; checa `.py` de runtime intactos e nenhum destino `.py` na raiz |
| B6 | revisor independente: `& $PY -B -X utf8 "$W\review\review_app.py" <id-do-revisor>`; depois `mission_step.py submit app --actor sonnet-app-v398-construtor --evidence <DELIVERY_PREPARED, install_plan, final_checks, NATIVE_COUNTS_COMPLETE>` e `mission_step.py accept app --actor <id-do-revisor> --evidence "$W\validation\review_final.json"` (idem `accept sources` com artefato **próprio** do revisor) | `validation\review_final.json` | `PASS`; o servidor recusa aceite pelo próprio autor. O revisor **não confia neste plano nem nos números do relatório da Fase A**: relê o `install_plan.json`, recomputa hashes e compara com o cofre |
| B7 | `mission_step.py claim deploy --actor claude-gerencia-a7 --lease-seconds 7200`; sonda ociosa: `& $PY -B -X utf8 -c "import sys;sys.path.insert(0,r'$W');import transaction;print(transaction.quiet())"` | `receipts\*.json` | `{'active_jobs':0,'reserved_calls':0}`. Exatamente 1 processo `iald_web_server.py`, dono da porta 8082, pai = `start_iald_web.ps1` sem `-NoSupervise`. `Get-FileHash iald_web_server.py` ainda `ef771e621eae5768…` (senão reavaliar o item 6.1) |
| B8 | `& $PY -B -X utf8 "$W\deploy_controlled.py"` | `maintenance.json`, `deployment.json` (backups `.bak_<stamp>` ao lado de cada arquivo trocado), `restart.json`; produção: `canonical_releases\v398_<commit12>\`, `.iald_runtime\haiku55\` e `\haiku\` (prefix/manifest/native_count), `core_packet_v398_bound.txt`, `iald_nucleo_fixo.json` **por último** | suspende supervisor+filho, termina **só o PID do filho**, aplica o plano com CAS e reversão automática em falha, retoma o supervisor; espera `/login`=200 e novo PID (até 90 s). Roda **uma vez** (recusa se houver `deployment.json`) |
| B9 | `& $PY -B -X utf8 "$W\verify_installed.py"` | `INSTALLED_VERIFICATION.json` | processo novo; releia hashes de todos os arquivos do plano, loaders, pacotes, JEV; zero chamada de provedor |
| B10 | verificação pós-instalação (seção 5), `submit`/`accept` de `deploy` e `verify` por revisor ≠ autor, memórias da casa (moldes: `assemble_delivery.py`, `memory_update.py` da v395, a parametrizar) | recibos | gate da régua: NOT_FALSIFIED nunca é CONFIRMED; o gate/`um.py`/kernel não se movem |

## 3. Estimativa do pacote haiku55 [REAL = medido; resto = estimativa]

Âncora medida (instalada, v395): prefixo 1 670 168 B → 896 672 tokens nativos; pedido com ferramentas +1 547; janela 1 000 000; saída reservada 16 384; margem 1 024; **sobra hoje 84 373**. Piso de runtime (`load_package` e `count`): **sobra ≥ 10 000**.

**Pelo tamanho dos insumos (v395→v398, cofre):** `.txt` do artigo 930 398→951 675 (+2,29 %); forma canônica 245 408→255 369 (+4,06 %); resultado 12 741 855→12 895 671 (+1,21 %); manifesto de prova 3 789 360→3 806 398 (+0,45 %); `um_absoluto_manifest.md` 3 699 682→3 720 030 (+0,55 %). Só por razão de tamanho, o haiku55 cresce +7 KB a +68 KB → sobra 46 500 a 80 000 tokens.

**Pelo codec (mecanístico, antes do ensaio):** o `core` passa de 425 para **435 tópicos** (+10 novos, +89 264 B: `testemunha_estatica_v396`, `cunhagens_v396`, `kh_n1_cobertura_v396`, `teste_de_veracidade_fase9_v397`, `cunhagens_v397`, `kh_n1_cobertura_v397`, `afinacao_das_cordas_v398`, `sonico_v398`, `cunhagens_v398`, `kh_n1_cobertura_v398`) e 51 mudam (+29 315 B, quase tudo `kernel_formalization`). Reproduzindo a v395 com o mesmo codec, a expansão (100 758 B em 26 tópicos) + o trecho do bootstrap (7 337 B) fecham os 108 095 B medidos entre base e expandido.

**Ensaio offline medido (sandbox no scratchpad: rede bloqueada por gancho de auditoria, portão da missão simulado, commit hipotético `35e8cdf6…`; nada gravado em `iald_v398_20261024\` nem na produção):** `prepare.py` v398 concluiu em 32,5 s (435 tópicos, 1 428 fontes formais) e `finalize.py` em 10,7 s. Base haiku 1 614 847 B (previsto 1 615 069); **haiku_expanded 1 719 266 B** com 30 tópicos expandidos (previsto 1 719 488; +49 098 B = +2,9 % sobre o instalado); sobra estimada pelo próprio guarda 54 915 tokens (cálculo conservador a 0,60 tok/B); `shared` 834 497 B (v395: 785 304); prompt do cluster 759 026 B (709 590); prompt público (Sonnet) 910 627 B (860 813); `native_prefix` 51 274 B; `jev_control_v398.json` 6 147 B (teto 10 000); 1 446 arquivos de dados → plano de 1 454. Tokens **nativos** só saem do B4; pelas densidades medidas da v395: haiku55 ≈ 923–926 mil, `shared` ≈ 428–432 mil, Sonnet público ≈ 462–467 mil.

| Opção de expansão (previsão do codec) | Prefixo (B) | vs instalado | Sobra (tokens) a 0,537 / 0,558 / 0,600 tok/B |
|---|---|---|---|
| sem expansão (base) | 1 615 069 | −55 099 | 113 956 / 115 119 / 117 433 |
| P2: `_v397,_v398` | 1 686 866 | +16 698 | 75 408 / 75 056 / 74 355 |
| **P4 (padrão): `_v395…_v398`** | **1 719 488** (medido 1 719 266) | **+49 320** | **57 894 / 56 853 / 54 781** |
| P1: regra literal da v395 (`_v394,_v395`) | 1 724 571 | +54 403 | 55 165 / 54 017 / 51 732 |
| P3: `_v394…_v398` | 1 775 079 | +104 911 | 28 047 / 25 833 / 21 427 |

**Risco de passar de 1 000 000 tokens: nenhum nas cinco opções.** O limite real é o piso de 10 000: só seria atingido com prefixo ≥ 1,794–1,809 MB (+124 a +139 KB sobre o instalado). Recomendo **P4** (equivale à regra da v395 «release instalada até a corrente»); P3 deixaria só ~21–28 mil tokens de conversa, por isso **não**. Se o `finalize` real estimar < 40 000 de sobra, cortar para P2 (`EXPAND_OVERRIDE=('_v397','_v398')` em `release_cfg.py`, antes do `finalize`) ou, no limite, instalar `packages\haiku55\prefix.md` (sem expansão; exige contagem própria); o guarda aborta sem gravar se < 15 000. Os pacotes `haiku` (compacto, hoje 402 716 tok) e Sonnet público (436 948 tok) têm >530 mil de sobra. Histórico do haiku55 (prefixos instalados): 1 049 607 → 1 190 187 → 1 637 152/175 (v394) → 1 670 168 B (v395): +33 KB na última troca.

## 4. Custo esperado

- **Contagens (B4):** 6 chamadas `count_tokens` (2 por pacote), sem geração: **gratuitas** [DECLARADO — o próprio código as marca como gratuitas «[KNOWN, não verificado]»; sujeitas a limite de taxa].
- **Reaquecimento do cache na 1ª chamada Claude de cada pacote** (prefixo novo = cache frio; TTL `5m` por padrão no código): tarifas do app `HAIKU_PRICES_5M=(0,50; 0,05; 2,50; 0,625)` US$/M (entrada, leitura de cache, saída, escrita 5 min — `claude_route_bridge.py:14`) [REAL como código; DECLARADO como preço do provedor]. haiku55 ≈ 0,925 M tokens → **≈ US$ 0,58 na escrita fria** e ≈ US$ 0,046 por releitura dentro do TTL; haiku compacto ≈ 0,43 M → ≈ US$ 0,27 / 0,022; Sonnet público ≈ 0,465 M × US$ 2,50/M (escrita = 1,25 × US$ 2,00 [DECLARADO]) ≈ US$ 1,16 / 0,09. Pior caso (os três a frio uma vez) ≈ US$ 2,0, mais saída e raciocínio da resposta. Com TTL `1h` a escrita dobra [DECLARADO]. Se o teste vivo cair no MiMo (modo automático, como na v395), o aquecimento Claude só ocorre quando uma rota Claude for usada.
- Nenhuma geração paga nos passos B0–B3, B5–B9.

## 5. O que conferir depois (B10)

> [nota operacional do operador — omitida no retrato público]

## 6. Riscos e pendências

1. **Reinício do filho web carrega código «novo»?** [REAL] O processo 10916 (iniciado 23/10 13:56:09) roda o `iald_web_server.py` de sha256 `3d4e693b8f1ff551…`, o mesmo que o plano `chat_release\INSTALL_PLAN_R2.json` (sha256 `5af41c6bd9a4c052…`) fixou, `chat_release\DEPLOYMENT.json` instalou em 22/10 11:05:23 (backup `iald_web_server.py.bak_20261022_110523_326776` = baseline `e5f7aafb…`) e `chat_release\DEPLOY_REVIEW_R2.json` aprovou (PASS, revisor `codex-independent-security-reviewer-dalton`); `CURRENT_INSTALLED_VERIFICATION_R3.json` (22/10 17:18) e `APK40_REVIEW.json` (23/10 14:03:42, após o início do processo) ainda fixavam esse hash. O arquivo em disco (mtime 23/10 15:25:45, sha256 `ef771e621eae5768…`) difere **só na linha 129** (`GOOGLE_API_KEY = _segredo("GOOGLE_API_KEY", "<legado>")` → `""`): reconstruído o hash antigo trocando só essa linha, ele bate com o revisado. Coincide (inferência) com a limpeza de segredo registrada em `MEMORY_2.md` («a chave do Google saiu dos 8 arquivos .py … nenhum processo reiniciado; ROTAÇÃO = operador»): `.env`, `iald_mcp_server.py` e 6 cópias antigas em `Atualização Web_server\` foram gravados no mesmo segundo. **Não houve revisão independente dessa gravação** (nenhum recibo achado). Efeito do reinício: a chave passa a vir só do ambiente/`.env`; se não estiver lá, `GOOGLE_SEARCH_AVAILABLE` fica falso e a busca cai para o ddgs [`.env` é vedado: não verificado].
2. **Corrida do runtime**: `RUNTIME_BASELINE` fixa o hash de todo `*.py` do app em B2 e o reafere em B2/B3/B5; qualquer edição concorrente de código do app nessa janela derruba o build (o servidor tem 9 backups de edição entre 17 e 22/10, mais a gravação sem backup de 23/10). Fazer B2–B5 de uma vez e repetir em pasta nova se falhar.
3. A missão ACOM e a unidade do quadro são criadas por `task.py` (B0b) — escolha da gerência. **Ensaiados offline em sandbox (portão da missão simulado):** `prepare.py`, `finalize.py`, `verify_sources.py`. **Só sintaxe, não exercitados:** `task.init`, `mission_step.py`, `count_final_public.py`, `validate_plan.py`, `review_app.py`, `verify_installed.py` (dependem de missão, contagens ou produção). `transaction.py`/`maintenance.py`/`deploy_controlled.py` são os da v395, byte a byte.
4. `verify_sources.py` usa rede (`git ls-remote`); `count_final_public.py` lê o `.env` (chave nunca impressa).
5. Reversão: não há script de desinstalação. `apply_plan` reverte sozinho se falhar **durante** a instalação; depois de concluída, reverter = nova janela de manutenção restaurando os `.bak_<stamp>` listados em `deployment.json` (primeiro `iald_nucleo_fixo.json` e os pacotes `.iald_runtime`) — a escrever se necessário.
6. Fora do escopo: fila científica, builds iOS/Android/lojas, memórias pós-implantação (moldes da v395 em `iald_v395_20261022\`).

## 7. Parte 1 da Fase B executada (24/10, 09:55–10:02, por `sonnet-app-v398-construtor`) [REAL]

- **B0:** `espelho_commit` gravado em `app\RELEASE.json` (HEAD local = `origin/main` local = ordem da gerência; backup `RELEASE.json.bak_20261024_095530`). Atores em `release_cfg.py`: `OWNER=claude-gerencia-a7`, `BUILDER=sonnet-app-v398-construtor` (rótulos locais). `verify_sources.py` ganhou `--offline` (parte 1 não permitia `git ls-remote`) e passou a usar o construtor como ator. Ordem do operador = `ORDEM_DO_OPERADOR.txt`, sha256 lido por script = `objective_sha256` da missão.
- **Missão ACOM** criada por `task.py` (`SESSION_REFERENCE.json`); unidade `F9.APP_V398_20261024` no quadro; `app` e `sources` reivindicadas pelo construtor (lease de 12 h, ainda `working`, **sem submit**).
- **Executados:** `verify_sources --offline` (36 artefatos, `CUSTODY_AND_SEAL_VERIFIED`), `prepare` (33 s), `finalize` (padrão P4, 30 tópicos expandidos), `count_final_public` (6 × `count_tokens`, 0 geração), `validate_plan` (`PASS_PREPARED`, 11 testes, 1 454 arquivos: 1 447 novos + 7 sobrescritos = prefix/manifest/native_count de `haiku55` e `haiku` + `iald_nucleo_fixo.json`).
- **Defeito achado e corrigido:** `count_final_public.py` e `validate_plan.py` reusam o nome `cfg` (config da requisição Claude) dentro do laço e sombreavam o `cfg` de release → `AttributeError` **antes de qualquer chamada de rede** (nenhum recibo de contagem existia). O objeto de release passou a `relcfg` (backups `.bak_20261024_100019` e `_100036_step2`); `count`, `validate_plan` e `review_app` foram reensaiados em sandbox com contagens falsas antes da contagem real.
- **Tokens nativos medidos (permanente / pedido / sobra, com 16 384 de saída e 1 024 de margem já descontados):** haiku55 919 987 / 921 534 / 61 058; haiku 426 157 / 427 704 / 554 888; Sonnet público 460 624 / 462 171 / 520 421. A sobra do haiku55 era 84 373 na v395.
- **Não feitos (ordem da gerência):** revisão independente, `submit`/`accept`, claim de `deploy`, `deploy_controlled`, `verify_installed`, qualquer escrita em `C:\IALD\projetos_pyhton\IALD`.

Próximo (revisor ≠ `claude-gerencia-a7` e ≠ `sonnet-app-v398-construtor`):

```powershell
& $PY -B -X utf8 "$W\review\review_app.py" <id-do-revisor>
# depois, o construtor entrega e o revisor aceita (o servidor recusa aceite pelo próprio autor):
& $PY -B -X utf8 "$W\mission_step.py" submit sources --actor sonnet-app-v398-construtor --evidence "$W\sources_verified.json"
& $PY -B -X utf8 "$W\mission_step.py" submit app --actor sonnet-app-v398-construtor --evidence "$W\app\DELIVERY_PREPARED.json" "$W\install_plan.json" "$W\validation\final_checks.json" "$W\app\NATIVE_COUNTS_COMPLETE.json"
& $PY -B -X utf8 "$W\mission_step.py" accept app --actor <id-do-revisor> --evidence "$W\validation\review_final.json"
```

### 7.1 Submit executado (24/10, após a autorização da gerência) [REAL]

`sources` (revisão 4) e `app` (revisão 5) estão `review_pending`, com as leases liberadas; `deploy` e `verify` seguem `open`. Recibos (um evento cada, idempotente): `receipts\v398-sources-submit.json` (sha256 505b1640a45d0e68f331dcd879e6789dce3009e470c409acba5af38fea1d7875) e `receipts\v398-app-submit.json` (sha256 81c6c39b2fc3902cd5cb9dcaa8e0aed638d3e37bf47968a08017949cdee5d159). Evidência pinada em `sources`: `sources_verified.json` e `app\PUBLIC_GIT_BINDING.json`; em `app`: `DELIVERY_PREPARED.json`, `install_plan.json`, `validation\final_checks.json`, `NATIVE_COUNTS_COMPLETE.json`, os três `prefix.md` (haiku55, haiku, Sonnet público) e `manifest_install.json` (candidato do `iald_nucleo_fixo.json`). Sem accept, sem claim de `deploy`, sem rede.

Revisor `sonnet-app-v398-revisor` (o servidor recusa aceite pelo autor; o accept de `sources` exige artefato PRÓPRIO do revisor, pois `review_app.py` não cobre o cofre/commit por inteiro):

```powershell
$PY = 'C:\Python314\python.exe'; $W = 'C:\IALD\Central de Patentes\work\iald_v398_20261024'
& $PY -B -X utf8 "$W\review\review_app.py" sonnet-app-v398-revisor
& $PY -B -X utf8 "$W\mission_step.py" accept app --actor sonnet-app-v398-revisor --evidence "$W\validation\review_final.json"
& $PY -B -X utf8 "$W\mission_step.py" accept sources --actor sonnet-app-v398-revisor --evidence "<arquivo do revisor, ex. $W\validation\review_sources.json>"
```
Com `app` e `sources` aceitos, `deploy` fica reivindicável por `claude-gerencia-a7` (o ator de `deploy_controlled.py`).
