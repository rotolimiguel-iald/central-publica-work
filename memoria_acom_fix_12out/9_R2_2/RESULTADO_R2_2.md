ACOM R2.2 — 13/10

# Conserto ACOM 12/10, R2.2: os achados da revisão independente da R2.1 (K4c, K4b, K3r, P8b, N1, N3 pela via do app e o manifesto)

Construtor: subagente da gerência c1, 13/10/2026. Antes de tocar em qualquer coisa, conferi a base por script
(`runs\s0_preparar.json`). Todos os hashes bateram:

- `RESULTADO_R2_1.md` `f0f4637f39e131c8`
- `CANDIDATO_MANIFESTO_R2_1.json` `f7ccb802d2388ac3`
- `implantar.py` `b913952cb2592b84`
- `reverter.py` `b6e3906baa88a7e5`
- `implantacao_lib.py` `c72ddd0a5686a4e0`
- `implantar_config_producao_r2_1.json` `66f8caea867e91e1`
- `REVISAO_R2_1.md` `8d113857fd263bb0`
- o candidato R2.1 em disco, 15/15 contra o seu manifesto

Escrevi só em `9_R2_2\`. Estatutos: [REAL] medido aqui · [DERIVED] deduzido do código ou de medida · [DECLARADO]
afirmado na origem e não refeito aqui · [OPEN] · [INPUT] decisão do operador ou da gerência.

## Veredito em uma linha

**R2.2 PRONTA PARA A DECISÃO DO OPERADOR** [REAL nas cópias].

- **Consertos.** Os 7 consertos pedidos estão no código. Cada um tem teste que reproduz o cenário do revisor: **15 dos
  19 testes novos FALHAM na R2.1**, e os 4 que passam lá são controles. Na R2.2 passam os 19.
- **Suíte inteira.** Dá **278 de 278 PASSA**: as 259 da R2.1 mais 19 novos.
- **Ensaio.** O ensaio de implantação e reversão, com processos simulados, roda os **21 cenários** pedidos. A
  promessa da R2.2 vale em cada um deles.
- **Runbook.** O roteiro do operador está em `RUNBOOK_OPERADOR.md`.
- **Produção.** Nada foi rodado em produção.

## 1. O que mudou

| arquivo | sha16 R2.1 → R2.2 | conserto |
|---|---|---|
| `MEMORIA_IALD\lib\iald_memory\guard.py` | `0a49de819f89b4d5` → `0d1d34015e9b0f6a` | N1 por componentes |
| `MEMORIA_IALD\session_memory.py` | `ca5409aa8359cf08` → `7e62693b8064d646` | só o comentário do `_guarded_read` (documental, revisão §1) |
| `projetos_pyhton\IALD\iald_web_server.py` | `68698c9583efac1c` → `ae5750e8af309fde` | N1 e N3 pela via do app |
| `implantar.py` | `b913952cb2592b84` → `11104b0e2dd8f80d` | P8b |
| `reverter.py` | `b6e3906baa88a7e5` → `62f212555a845e1a` | K4c, K4b, K3r |
| `implantacao_lib.py` | `c72ddd0a5686a4e0` → `3f42bf41edf2c6d0` | `reversao_limpa` (K4c), diagnóstico do reinício (P8b), `descrever_estado` |

- Os outros 12 arquivos do candidato são byte a byte os da R2.1.
- Manifesto: `CANDIDATO_MANIFESTO_R2_2.json` `58184a0173281540`. Ele traz o campo `r2_2_mudancas` e o campo novo
  `ferramentas_implantacao`, com o sha das três ferramentas R2.2.
- Config: `implantar_config_producao_r2_2.json` `14422d91e08182ae`. É a da R2.1 com quatro trocas:
  - candidato `9_R2_2\candidato_r2_2\C`;
  - manifesto R2.2;
  - recibos em `9_R2_2\recibos_producao_r2_2`;
  - `recibos_dirs_anteriores` com as pastas da R2.1 e do R2.

  O script `scripts\s2_config_producao.py` confere que o resto é igual.

## 2. Os consertos [REAL nas cópias]

1. **K4c.** No reverter, um alvo fora do original na conferência logo antes de religar agora entra em `falhas`
   (status `FALHOU_EM_reiniciar_app`).
   - Antes, ele virava `NAO_EXECUTADO`, sem falha, e o status saía `REVERTIDA`.
   - Há também uma **conferência final** dos 15 alvos depois de religar (`conferencia_final`). Uma divergência ali
     também é falha, e a ação manda parar o app.
   - `REVERTIDA` agora exige o app religado (há uma guarda defensiva para isso).
   - `ok` na saída só é true com o app religado ou com a ação manual registrada.
   - A trava do implantar (`recibos_pendentes`) só aceita uma **reversão limpa** (`reversao_limpa`): real, sem falhas,
     e em `REVERTIDA` com `app_religado` diferente de false. Um recibo `REVERTIDA` com `app_religado: false`, que é o
     que a R2.1 gravava no K4c, **não libera a trava**.
2. **K4b.** Sempre que o reverter não religa, `acao_requerida` é preenchida com o **estado LIDO** (tarefa, supervisores,
   filhos web, porta) e com o comando para rodar de novo. Isso vale também quando a conferência levanta exceção (alvo
   travado em modo exclusivo).
   - `--sem-reiniciar` passa a dar `REVERTIDA_SEM_RELIGAR`, com a ação manual (Enable e Start da tarefa).
3. **K3r.** O `parar_app` do reverter recebeu o conserto K3. Se não conseguir parar o app:
   - nada é restaurado (como na R2.1);
   - a tarefa é reabilitada **se e só se esta execução a desabilitou**;
   - o recibo diz o estado LIDO. Exemplo: «0 supervisor(es), 1 filho(s) web… o app está VIVO SEM SUPERVISOR», com a
     ação de manter (rodar `stop_iald_web.ps1` e depois `Start-ScheduledTask`) ou de reverter;
   - o passo de religar não sobrescreve mais essa ação com «Ele fica parado».
4. **P8b.** A saída 3 continua **por desenho**.
   - Durante a espera, `iniciar_app_gerido` amostra os pids do filho web e do supervisor e devolve
     `diagnostico_reinicio`:
     - `LENTO_PROVAVEL`: um só pid, estável;
     - `LACO_DE_QUEDA_PROVAVEL`: o pid trocou, o filho sumiu e voltou, ou nunca ficou de pé com o supervisor vivo;
     - `INDETERMINADO`: amostras insuficientes.
   - O diagnóstico vai ao recibo e **à própria saída** do implantar.
   - `acao_requerida` explica como distinguir: duas leituras de `ProcessId`/`CreationDate` com 1 minuto entre elas,
     mais `/login`. Ela também diz o que fazer em cada caso.
   - O caso lento não traz o comando de reversão; esse é o invariante do passo 8 desde a R2.1.
   - O texto nunca transforma uma implantação verificada em falha (há uma proteção).
5. **N1.** `guard.path_shape_reason` recusa a forma do caminho **antes** do `os.path.realpath`, com recusa visível:
   - mais de 32.767 caracteres dá `path_too_long`;
   - mais de 256 componentes, contados em tempo linear, dá `path_too_many_components`.

   A checagem está em `path_reason` (e portanto em `is_confidential_path`), em `read_checked` (e portanto no
   `session_memory`) e no `agi_validate_path` do app. Este último chama `realpath` antes do guard.
   - Medido: 16.000 componentes passaram de 2,8–3,7 s (R2.1) para menos de 50 ms.
   - Na R2.1, um caminho de 40.000 caracteres levantava `ValueError` do `stat` (exceção, não recusa).
6. **N3 pela via do app.** O `agi_validate_path` agora confere o arquivo existente **pelo handle** do guard
   (`read_checked`). O handle é de leitura, sem `FILE_SHARE_DELETE`, com contagem de links, identidade e caminho
   final, e esse caminho final também precisa estar dentro da whitelist. Os dois pontos que leem bytes passaram a usar
   os bytes do mesmo handle, nunca um segundo `open` por nome:
   - `/admin/api/agi/files/read`;
   - a ação `read` do `agi_execute`.

   A decodificação ficou igual à do `open(..., 'r')`: utf-8, com latin-1 de reserva, e CRLF vira LF. A comparação com
   a whitelist ignora o prefixo estendido `\\?\`, porque o caminho final do handle não o traz e uma raiz pode trazê-lo.
   - A edição foi feita por script, com âncora exata e CRLF preservado (`scripts\s1_editar_web_server.py` e
     `s1b_…`). A chave nunca foi impressa e continua idêntica.
   - Cópias redigidas: `runs\iald_web_server_r2_2_redigido.py`.
7. **Documental.** O campo `ferramentas` do manifesto agora cita o sha real do `aplicar_blocos.py`
   (`9c86bcc996922653`). O valor antigo (`df08a17e7cc71f40`, do R1) fica ao lado, em `sha256_citado_ate_r2_1`.

## 3. Medidas [REAL] (detalhe em `TESTES_R2_2.md` `0524b04e89eb55e1`)

- **Suíte inteira R2.2:** **278/278 PASSA**. Foi rodada na cópia `copia\`, sob a guarda da auditoria, com Python
  3.14.3, sem rede e sem provedor. Resultado em `copia\testes_r2\RESULTADOS_TESTES.json` `6767685fd0dc6bdd`; saída em
  `runs\suite_completa_r2_2_final_stdout.txt`.
  - Bloqueios da guarda: 3 por rodada, todos `BLOCK_NETWORK ('::1', 0)` (a sonda IPv6, como nas revisões).
  - Leituras fora da pasta: o perfil do Python em AppData, o índice do orquestrador em `mode=ro` e o `__pycache__` do
    app. Nenhuma leitura do banco ACOM de produção (`runs\s6_guarda_resumo.json`).
  - A 1ª rodada (`runs\suite_completa_r2_2_rodada1_stdout.txt`) deu 276/277. A falha era o teste R2.1 do P8, que
    proíbe o comando de reversão no caso lento, e o texto P8b o citava. Corrigido no texto; o teste não foi mexido.
- **Testes novos na cópia da R2.1** (`copia_r2_1`: candidato R2.1 e ferramentas R2.1 byte a byte em `ref_r2_1\`):
  **15 FALHAM, 4 passam** (os controles). Na R2.2 passam os 19.
- **N3 via app**, pelo handler real, com troca ativa por hardlink durante 12 s:
  - R2.1: **294** leituras do canário;
  - R2.2: **0** leituras do canário e 2.059 recusas.
- **Ensaio** (`runs\s5_ensaio_r2_2.json` `1bd579acfebccdc2`, 2ª rodada completa), com os 21 cenários: K1a, K1b2, K1c,
  K1d, K2, K3, K4, K5, K6, P8, K2b, K2c, K2d, K3b, K3r, K4b, K4c, K6b, K6c, P8b e CFG.
  - **K4c:** a 1ª reversão dá `FALHOU_EM_reiniciar_app`, com rc 1, sem religar, ação preenchida e a trava vendo a
    implantação pendente. A 2ª dá `REVERTIDA`.
  - **K4b:** `FALHOU_EM_reiniciar_app` com a ação preenchida («Estado LIDO… o app está PARADO»). A 2ª dá `REVERTIDA`.
  - **K3r:** `FALHOU_EM_parar_app`, nada restaurado, tarefa reabilitada, recibo com o estado lido e sem «fica
    parado». Depois, a reversão normal dá `REVERTIDA`.
  - **P8:** rc 3, leitura LENTO, sem mandar reverter.
  - **P8b:** rc 3, leitura LAÇO DE QUEDA, com o «como distinguir».
  - **CFG:** os comandos do runbook na forma positiva funcionam.
  - Em todos, menos K2b/K2c/K2d, os originais terminam idênticos, o banco igual ao original e a lib v1 lendo o banco.
    K2b/K2c/K2d são o operador renomeando, apagando ou truncando o recibo; terminam como na R2.1 (TESTES §3).
  - A **1ª rodada** do ensaio (`runs\s5_ensaio_r2_2_rodada1_bug_P8b.json`) achou um defeito meu. No P8b, com o filho
    web que nunca fica de pé, o texto levantava `UnboundLocalError` e a implantação verificada saía rc 1. Corrigi, pus
    o teste `test_T_P8b_child_never_up_is_crash_loop` e refiz o ensaio inteiro.
  - Numa rodada parcial anterior, o implantar do cenário K3r falhou uma vez no `parar_app` do simulador. Não se
    repetiu em 3 rodadas seguintes [REAL; leio como instabilidade do simulador, causa não isolada, OPEN].
- **Patch:** `DIFF_R2_1_R2_2.patch` `991fe46e8dffe6bd`, com 56.807 B, os 3 arquivos do candidato e as 3 ferramentas.
  - `git -c core.autocrlf=false apply` sobre a cópia do candidato R2.1 e das ferramentas R2.1 reproduz os 18
    arquivos byte a byte (`DIFF_R2_1_R2_2_APPLY_CHECK.json` `e40ad7b0c8ce39d7`).
  - O web server entrou redigido dos dois lados. A chave está fora de todo trecho do patch e é a mesma nos dois
    candidatos.

## 4. Para o operador

Leia `RUNBOOK_OPERADOR.md` (`8b412619a5e91563`). Ele cobre, com os comandos exatos e os caminhos da R2.2:

- a janela quieta (fechar as sessões Claude e Codex, inclusive a da gerência);
- o dry-run exigindo `DRY_RUN_OK`;
- a implantação com `--pular-mover-backups` exigindo `CONCLUIDA`, ou como ler a saída 3;
- as conferências: `/login` 200, `Get-ScheduledTask` habilitada, 1 filho web, e a 7_VERIFICACAO com janela de mais
  de 30 min e o llama online;
- mover os backups (dry-run antes);
- reverter, exigindo `REVERTIDA`, `app_religado: true` e `acao_requerida: null`;
- as regras dos recibos;
- o contexto `1bcf55a4` que ficará recusado, o psion não restaurado e a política de instantâneos (≈ 8,6 GB/dia,
  decisão D1-B pendente).

## 5. O que NÃO fiz, e o que resta

- **Nada em produção.** Não toquei `C:\IALD\MEMORIA_IALD`, `C:\IALD\projetos_pyhton\IALD`, a tarefa agendada,
  processos reais nem `D:\IALD_ARQUIVO`. Não rodei `implantar.py`/`reverter.py` contra a config de produção, nem em
  dry-run. Sem rede, sem provedor. Confidenciais nunca abertos: tudo foi sintético, inclusive o psion e os hardlinks.
  Não segui junções.
- **Desvio deliberado:** não executei o `init`/`transition` da memória ACOM do CLAUDE.md global. Eles escreveriam no
  banco de produção, contra a regra desta tarefa.
- **Mapa de rotas:** consultei antes; a rota `programa.memoria_acom.conserto_delta_12out` existe. O registro sai em
  `registro_mapa_F9.MEMORIA_ACOM_R2_2.json` para a gerência registrar. Eu não registrei.
- **Chave:** o `iald_web_server.py` de `candidato_r2_2` carrega a chave de produção, porque é o que se instala.
  Conferi por script: nenhum outro arquivo de `9_R2_2` a contém. Não publicar `work\memoria_acom_fix_12out`.
- **Não refiz:**
  - a repetição do heartbeat com varredor (o código do heartbeat não mudou na R2.2);
  - os ataques N2 (a classe «conteúdo», `*.env.txt` e ADS, segue aberta na decisão D4 [INPUT]);
  - o N3 por renomeio (equivale a cópia, gravidade baixa; segue como na R2.1 [DERIVED]).
- **Cmdlets reais do Agendador:** seguem nunca exercitados [OPEN]. Tudo passou pelo backend simulado.
- **P8b em produção:** a amostragem depende de cada `listar()` do PowerShell, cerca de 1–2 s por amostra [DERIVED, não
  medido]. Com `esperar_inicio_s` de 180 s há dezenas de amostras. Um filho que morre e renasce entre duas amostras com
  o mesmo pid não é distinguível, mas o Windows raramente reutiliza um pid tão cedo [DERIVED]. Por isso o runbook manda
  também a leitura manual de `ProcessId`/`CreationDate`.
- **K2b/K2c/K2d:** a recuperação automática depois de renomear ou apagar um recibo continua perdida. A regra do runbook
  (§6) é a defesa.
- **Escala da v2:** os instantâneos do banco inteiro (D1-B) e a retenção em D: são decisão pendente [INPUT].
- **Revisão:** a R2.2 não foi revista por terceiro.

## 6. Artefatos (sha256 por script em `MANIFESTO_R2_2.json`)

**Entrega:**

- `candidato_r2_2\C` (15) · `CANDIDATO_MANIFESTO_R2_2.json`
- `implantar.py` · `reverter.py` · `implantacao_lib.py` · `implantar_config_producao_r2_2.json` (recibos irão para
  `recibos_producao_r2_2\`, que ainda não existe)
- `DIFF_R2_1_R2_2.patch` + `DIFF_R2_1_R2_2_APPLY_CHECK.json`
- `TESTES_R2_2.md` · `RUNBOOK_OPERADOR.md` · `registro_mapa_F9.MEMORIA_ACOM_R2_2.json`
- `src_r2_2\` (testes novos) · `scripts\` · `runs\`

**Cópias regeráveis:** `copia\` (R2.2) · `copia_r2_1\` (R2.1) · `ref_r2_1\` (as 3 ferramentas R2.1, byte a byte) ·
`ensaio\`.
