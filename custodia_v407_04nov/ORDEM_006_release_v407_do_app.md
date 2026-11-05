# ORDEM 006 — A release v407 do app, o contrato JEV v407 e a memória científica da fila (F0.3)

04/11/2026. De: o orquestrador da cadeia de selo da gerência c1 (`pos_treino_v407.py`, passo S10, automático). Para: `claude-app-orquestrador` (o app Claude em modo work). Ordem do operador (verbatim em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt`, sha16 `b89e4c909f37e163`): «o app e o contrato do JEV precisam ser sempre atualizados para a forma canônica mais madura, podia ser até automático isso, e o orquestrador pode executar o que vc mandar». A `ORDEM_001` continua valendo inteira (quem você é, o Escritório fora, o que nunca faz sem o operador).

Estado lido do selo e do git pela cadeia agora, não digitado: versão **v407**, `um.py` pino **833121339e649f71** (sha256 inteiro `833121339e649f7171e2eccca1a19b3a1564aa306a787ed8cea76ded0fdf3475`), a versão anterior **v406**; o espelho público `the_boundary` no commit **bf901715** e a Central no commit **cc10b8f4** (HEAD local no momento da ordem; se a custódia ainda não os publicou, o commit vigente é o que o `git` local disser e você o declara). O app instalado deve estar na release **v407** quando você terminar; a cadeia só fecha o C21 da custódia (G1) com o seu recibo conferido na fonte.

## 1. A release v407 do app e o contrato JEV v407 (fase A/B; construtor ≠ revisor)

Ponto de partida obrigatório: a pasta da release anterior (`C:\IALD\Central de Patentes\work\iald_v406_20261103`): copie-a para `C:\IALD\Central de Patentes\work\iald_v407_<data>\` e leia primeiro o `LICOES_*.md` inteiro dela (o que ela manda para a próxima release, e que você aplica antes de construir: flags de retenção, `max_chars` do `reading`, a janela P2 — deslize pelos sufixos mais antigos primeiro até o pacote `shared` caber, e **mantenha os literais `limites`/`diz`/`nao_diz` na cápsula compacta**; não compacte `the_iald_index`).
- A ordem na missão: `deploy → submit → accept → claim verify → verify_installed`.
- Fontes da ciência: o selo, o core e o manifesto do kernel do Nós (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\`: `um_absoluto_selo.json`, `um_absoluto.json`, `tgl_kernel_proof_manifest.json`) e o espelho público (o `prepare.py` lê o git local do `the_boundary`). Só leitura no Nós e no espelho.
- `app/prepare.py` gera `jev_control_v407.json` (valida, canoniza, grava em `canonical_releases\v407_<hash>\`), com `cfg.release = v407`; siga o `install_plan.json` e os `*_stdout.txt` da release anterior como roteiro.
- **Construtor ≠ revisor:** rode um revisor independente (outro agente/sessão do app, estreito, com a lista da release anterior: `REVISAO_*` e `INSTALLED_VERIFICATION.json`); no máximo duas rodadas; ressalvas BAIXAS vão escritas.
- **Reinício do serviço web:** se a instalação exigir reiniciar o serviço (porta 8082, supervisor), pare: é do operador (`INSTALLED_RESTART_REQUIRED`). Diga-lhe em uma linha.
- Nada toca `um.py`, selo, kernel, gate, cofre, nem `C:\IALD\Central de Patentes\Chatgpt\` (só leitura). Nenhuma chamada paga de geração para validar.

Entrega: `RELEASE.json`, `deployment.json`, `INSTALLED_VERIFICATION.json` (status `PASS`, `identity.release = v407`), `LICOES_v407.md`, o contrato `jev_control_v407.json` pinado, e `TORRE_IALD\torre.py gerar` rodado depois.

## 2. A memória científica da fila sincronizada à v407 (F0.3)

Texto da unidade: o `DESPACHO_CODEX_F03_*` mais recente em `C:\IALD\Central de Patentes\work\custodia_*`. Onde diz «coordenadora» ou «Codex», leia-se você. Reaproveite `work\scientific_memory_sync_20261013` (snapshot imutável, hashes e trechos, revisão independente real, ativação **pela API com proteção de concorrência**, conferência da geração recebida em processo novo, recibo em `work\scientific_memory_sync_<data>_v407\`). **Gate:** se algum passo exigir escrever dentro de `C:\IALD\Central de Patentes\Chatgpt\`, PARE e relate; a pasta é do ChatGPT e segue só leitura. Relatório de até 15 linhas.

## 3. As duas tarefas agendadas (se ainda não existem)

`IALD X diario` (18:00) e `IALD ronda da fila` (08:30). Se a criação for negada, diga em uma linha e não contorne.

## 4. O recibo que a cadeia espera (e o prazo)

A cadeia (`pos_treino_v407.py`, passo S10) espera, por até 24 h, ao mesmo tempo: (a) `RELATORIO_<data>.md` nesta pasta, escrito depois desta ordem e citando `ORDEM_006`, ou `RESULTADOS\006_RESULTADO.json` com `estado: cumprida` (a forma durável do `CANAL_DESASSISTIDO.md`); (b) `INSTALLED_VERIFICATION.json` em `work\iald_v407_*\`, `status PASS`, release v407; (c) `jev_control_v407.json` pinado em `canonical_releases\v407_<hash>\`; e então **confere na fonte** `C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json`: `operational_core.current_release = v407`, `release_source_sha256` = o pino acima, `jev_control.release = v407` e o sha256 do arquivo do contrato. Sem recibo em 24 h a cadeia PARA, visível, e a gerência decide; nunca marca «ok» sem a conferência. Depósito em `memory\fila\depositos\claude-app\`, `transition` na sua referência ACOM e registro no Mapa de Rotas (rota `app.release.v407`, nova). Recusa e parada são resultado; o que você traz é [DECLARADO] até a gerência conferir na fonte.

— O orquestrador da cadeia de selo (v407), em nome da gerência c1, 04/11/2026.

---

## Ao lado (04/11/2026): o que mudou desde o molde. Escrito pela sessão de custódia, `claude-site-custodia`, por encargo da gerência c1.

O S10 da cadeia não rodou, porque a cadeia parou em S7 e a gerência mandou não relançá-la. Por isso esta ordem foi escrita pela custódia, com a função `renderizar_ordem` do próprio `pos_treino_v407.py`. Versão, pino e commits acima foram lidos do selo e do git. A custódia da v407 está **PUBLICADA**: espelho, site, Central, Central pública, conferência final, ACOM t2 e rota `custodia.v407`. A medida final do organismo (C19) espera só esta release e os dois recibos abaixo.

**1. A F0.3 da v407 já foi feita por você. Não refaça a seção 2 do molde.**
O recibo é `C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407\DELIVERY_v407.json` (sha16 `753016234e685585`), estado `ATIVADA_PELA_API_COM_CAS__CURRENT_EM_PROCESSO_NOVO`. Ele também está no seu `RELATORIO_20261103_AO_LADO.md`, §6.
Falta só um recibo no esquema que o quadro do organismo lê: o C19 procura `DELIVERY_*R1.json` com `release` e `status` começando por `ACTIVATED_VERIFIED`. O seu recibo usa `versao` e `estado`, por isso o quadro marca «nenhuma».
Escreva, na mesma pasta, `DELIVERY_TECHNICAL_R1.json` no esquema da fila. O molde é `work\scientific_memory_sync_20261028_v404_R2\DELIVERY_TECHNICAL_R1.json`:
- `release`, `epoch` e `generation` lidos do seu `CHECK_DEPOIS_v407.json` e do `selo_lido_no_nos`;
- `status` = `ACTIVATED_VERIFIED_` mais o que valer;
- `independent_review` apontando para o parecer;
- `provider_calls` = 0;
- `receipts` com o caminho e o sha256 do `DELIVERY_v407.json`.
Nada novo é afirmado: é o mesmo fato no esquema do leitor. Isso não escreve em `Chatgpt\`.

**2. As lições da v406 que entram antes de construir.** Elas estão em `C:\IALD\Central de Patentes\work\iald_v406_20261103\LICOES_v406.md` (sha16 `fce97e4b238562b8`), na seção «para a próxima», e em `C:\IALD\Central de Patentes\work\iald_v406_20261103\LICOES_v406_AO_LADO.md` (sha16 `4eec434847e35159`), lições 3, 5 e 6.
- Na v406, a folga mínima declarada da janela P2 foi **41.975 B** (DeepSeek; Kimi 45.364; MiMo 41.992). Uma release de cerca de 30 KB no `shared` consome três quartos disso. Por isso sai `_v402`: entra em `P2_RETIRED_LITERAL_SUFFIXES` e deixa `SHARED_P2_SUFFIXES`, com os literais `limites`/`diz`/`nao_diz` mantidos. Se a v407 for do porte da v405, sai também `_v403`.
- O F1 do parecer (`protected_fields` e o `name_status`) entra antes de construir.
- Na revisão da instalação:
  - reescreva o D4: o manifesto ativo sai do «baseline intacto» e os logs do supervisor entram na varredura;
  - **meça** `accounts_modified`, `bench_restarted` e `client_files_changed`, em vez de lê-los de constante.
- Confira `quiet()` antes de pedir o reinício.

**3. O reinício do filho web (porta 8082).** Se a instalação exigir reinício, ele continua sendo do operador, como diz o molde. Peça em uma linha só, com `quiet()` conferido e a janela medida da v406, 87 s. Ele autorizou o reinício da v406 no chat em 03/11. A autorização não se estende à v407.

**4. As tarefas agendadas.** A seção 3 do molde **não se repete por esta ordem.** A criação foi negada três vezes pelo classificador (`RESULTADOS\004_RESULTADO.json`). Não contorne.

**5. Depois de você.** A custódia roda de novo `custodiar.py executar --versao v407 --publicar`. Esse passo fecha C21, C19, C20 e C17C, conferindo na fonte os quatro elos da seção 4 do molde e o `DELIVERY_TECHNICAL_R1.json` do item 1. Entregue como manda a `ORDEM_001`, seção 6.

## Quadro de vigência deste túnel (regra do operador de 04/11/2026: o que foi cumprido ou superado não fica parecendo pendente)

Verbatim da regra: `C:\IALD\Central de Patentes\work\abrogacao_04nov\OPERADOR_04nov_abrogacao_verbatim.txt`, sha256 `e469431de0ce1126e94be18e8b49ecfc538da58242a73c26a7ad13daaaf959fd`.

| Ordem | Estado | Por quê |
|---|---|---|
| `ORDEM_001`, `CANAL_DESASSISTIDO.md` | **VIGENTES** | quem você é e como entrega |
| ORDEM 006 (esta) | **VIGENTE** | a release v407 do app e o recibo da F0.3 no esquema da fila |
| ORDEM 004, §1 | cumprida | a v406 foi instalada em 03/11, de 20:18 a 20:20 (`RELATORIO_20261103_AO_LADO.md`, §3) |
| ORDEM 004, §2 | superada | a F0.3 foi feita direto para a v407 em 04/11 (§6 do mesmo relatório) |
| ORDEM 004, §3 | sem nova tentativa | negada três vezes; esta ordem não a repete |
| ORDEM 004, §§4 e 5 | superadas por esta ordem | o C21 da v406 deixa de ser alvo; o automático do S10 não rodou na v407 |
| ORDEM 005 | cumprida | `RESULTADOS\005_RESULTADO.json` |
| ORDENS 002 e 003 | esta ordem não as muda | o filme da v406 aguarda o operador escutar e decidir a voz |

— `claude-site-custodia`, em nome próprio, por encargo da gerência c1, 04/11/2026.
