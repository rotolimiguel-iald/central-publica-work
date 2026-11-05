# ORDEM 007 — A release v408 do app, o contrato JEV v408 e a memória científica da fila (F0.3)

05/11/2026. De: o orquestrador da cadeia de selo da gerência c1 (`pos_treino_v408.py`, passo S10, automático). Para: `claude-app-orquestrador` (o app Claude em modo work). Ordem do operador (verbatim em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt`, sha16 `685b8d8bcf0ddbbd`): «liste as pedras que eu preciso nominar e em seguida produza a v408, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo (site, repositório, e todos os links), todos os dispositovos e a central de patentes e em seguida publicar, push e commit de tudo»; herdada e vigente para o app: a ordem de 03/11/2026 («o app e o contrato do JEV precisam ser sempre atualizados para a forma canônica mais madura, podia ser até automático isso, e o orquestrador pode executar o que vc mandar»). A `ORDEM_001` continua valendo inteira (quem você é, o Escritório fora, o que nunca faz sem o operador).

Estado lido do selo e do git pela cadeia agora, não digitado: versão **v408**, `um.py` pino **e7bc6b10e8ff76be** (sha256 inteiro `e7bc6b10e8ff76beb40e05e45fb47adf9bcc2f9222440552af017deb4435e365`), a versão anterior **v407**; o espelho público `the_boundary` no commit **f9139b6f** e a Central no commit **cc10b8f4** (HEAD local no momento da ordem; se a custódia ainda não os publicou, o commit vigente é o que o `git` local disser e você o declara). O app instalado deve estar na release **v408** quando você terminar; a cadeia só fecha o C21 da custódia (G1) com o seu recibo conferido na fonte.

## 1. A release v408 do app e o contrato JEV v408 (fase A/B; construtor ≠ revisor)

Ponto de partida obrigatório: a pasta da release anterior (`C:\IALD\Central de Patentes\work\iald_v407_20261104`): copie-a para `C:\IALD\Central de Patentes\work\iald_v408_<data>\` e leia primeiro o `LICOES_*.md` inteiro dela (o que ela manda para a próxima release, e que você aplica antes de construir: flags de retenção, `max_chars` do `reading`, a janela P2).
- **A janela P2 do `shared` (decisão de projeto D53 da gerência c1, 04/11/2026):** no `shared` ficam em literal completo só a versão corrente (v408) e a anterior (v407); as anteriores (as mais velhas que v407) passam a tópicos regenerados, **sem compactar `the_iald_index` nem os literais `limites`/`diz`/`nao_diz` da versão corrente**. Se ainda assim não couber, você MEDE e propõe o teto novo com os números (bytes por versão, folga), antes do `finalize`; não desliza por adivinhação.
- A ordem na missão: `deploy → submit → accept → claim verify → verify_installed`.
- Fontes da ciência: o selo, o core e o manifesto do kernel do Nós (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\`: `um_absoluto_selo.json`, `um_absoluto.json`, `tgl_kernel_proof_manifest.json`) e o espelho público (o `prepare.py` lê o git local do `the_boundary`). Só leitura no Nós e no espelho.
- `app/prepare.py` gera `jev_control_v408.json` (valida, canoniza, grava em `canonical_releases\v408_<hash>\`), com `cfg.release = v408`; siga o `install_plan.json` e os `*_stdout.txt` da release anterior como roteiro.
- **Construtor ≠ revisor:** rode um revisor independente (outro agente/sessão do app, estreito, com a lista da release anterior: `REVISAO_*` e `INSTALLED_VERIFICATION.json`); no máximo duas rodadas; ressalvas BAIXAS vão escritas.
- **Reinício do filho web:** se a instalação exigir reiniciar o serviço (porta 8082, supervisor), pare: é do operador (`INSTALLED_RESTART_REQUIRED`). Peça-lhe em uma linha, por versão.
- Nada toca `um.py`, selo, kernel, gate, cofre, nem `C:\IALD\Central de Patentes\Chatgpt\` (só leitura). Nenhuma chamada paga de geração para validar.

Entrega: `RELEASE.json`, `deployment.json`, `INSTALLED_VERIFICATION.json` (status `PASS`, `identity.release = v408`), `LICOES_v408.md`, o contrato `jev_control_v408.json` pinado, e `TORRE_IALD\torre.py gerar` rodado depois.

## 2. A memória científica da fila sincronizada à v408 (F0.3)

Texto da unidade: o `DESPACHO_CODEX_F03_*` mais recente em `C:\IALD\Central de Patentes\work\custodia_*`. Onde diz «coordenadora» ou «Codex», leia-se você. Reaproveite `work\scientific_memory_sync_20261013` (snapshot imutável, hashes e trechos, revisão independente real, ativação **pela API com proteção de concorrência**, conferência da geração recebida em processo novo, recibo em `work\scientific_memory_sync_<data>_v408\`). **Gate:** se algum passo exigir escrever dentro de `C:\IALD\Central de Patentes\Chatgpt\`, PARE e relate; a pasta é do ChatGPT e segue só leitura. Relatório de até 15 linhas.

## 3. As duas tarefas agendadas (se ainda não existem)

`IALD X diario` (18:00) e `IALD ronda da fila` (08:30). Se a criação for negada, diga em uma linha e não contorne.

## 4. O recibo que a cadeia espera (e o prazo)

A cadeia (`pos_treino_v408.py`, passo S10) espera, por até 24 h, ao mesmo tempo: (a) `RELATORIO_<data>.md` nesta pasta, escrito depois desta ordem e citando `ORDEM_007`, ou `RESULTADOS\007_RESULTADO.json` com `estado: cumprida` (a forma durável do `CANAL_DESASSISTIDO.md`); (b) `INSTALLED_VERIFICATION.json` em `work\iald_v408_*\`, `status PASS`, release v408; (c) `jev_control_v408.json` pinado em `canonical_releases\v408_<hash>\`; e então **confere na fonte** `C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json`: `operational_core.current_release = v408`, `release_source_sha256` = o pino acima, `jev_control.release = v408` e o sha256 do arquivo do contrato. Sem recibo em 24 h a cadeia PARA, visível, e a gerência decide; nunca marca «ok» sem a conferência. Depósito em `memory\fila\depositos\claude-app\`, `transition` na sua referência ACOM e registro no Mapa de Rotas (rota `app.release.v408`, nova). Recusa e parada são resultado; o que você traz é [DECLARADO] até a gerência conferir na fonte.

— O orquestrador da cadeia de selo (v408), em nome da gerência c1, 05/11/2026.

---

## Ao lado (05/11/2026): o que mudou desde o molde. Escrito pela sessão de custódia, `claude-site-custodia`, pela ordem de handoff da gerência c1.

O orquestrador da c1 foi parado antes do S7 e do S10, porque os dois são da custódia (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v408\ORDEM_HANDOFF_CUSTODIA_v408.md`, sha16 `7dcf96f399fab917`, item 2). Por isso esta ordem foi escrita pela custódia, com a função `renderizar_ordem` do próprio `pos_treino_v408.py`. Versão, pino e commits acima foram lidos do selo e do git. O espelho já está em v408; a Central pública (C18) e a medida final do organismo (C19) seguem com a custódia e não precisam esperar você.

**1. A janela P2 (D53) e os números da v407.** Em `C:\IALD\Central de Patentes\work\iald_v407_20261104\LICOES_v407.md` (sha16 `c106992fe804c5ad`), item 1 e «para a próxima» item 1: o `shared` cresceu +29.323 B na v407, a folga ficou em 11.856 B, e o maior bloco é `_v405` (106.216 B). A D53 acima é a resposta da gerência: só v408 e v407 em literal completo; `_v403` a `_v406` viram tópicos regenerados. Meça antes do `finalize` e escreva no `LICOES_v408.md` os bytes por versão e a folga que sobrou.

**2. A F0.3 da v408 precisa de autorização nova do operador.** O recibo da v407 (`C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407\DELIVERY_TECHNICAL_R1.json`, sha16 `c4bfe19833189c44`) diz: «uma escrita única autorizada pelo operador … esgotada com a ativação; a v408 pede outra». Peça-lhe em uma linha, junto com o pedido de reinício, se houver. Sem a autorização, pare a seção 2 e diga isso no resultado. Ao entregar, escreva direto o `DELIVERY_TECHNICAL_R1.json` no esquema da fila (`release`, `status ACTIVATED_VERIFIED_…`, `epoch`, `generation`, `receipts` com sha256): é o que o quadro do organismo (C19/C20) lê.

**3. O reinício do filho web (porta 8082)** continua sendo do operador, por versão, em uma linha, com `quiet()` conferido e a janela medida da v407 (34,26 s; v406: 87 s). A autorização da v407 não vale para a v408.

**4. A seção 3 do molde (tarefas agendadas) não se repete.** Foi negada três vezes (`RESULTADOS\004_RESULTADO.json`) e a ORDEM 006 já a tirou de vigência. Não contorne.

**5. Depois de você.** A custódia confere na fonte os quatro elos da seção 4 e roda de novo `custodiar.py executar --versao v408 --publicar` para fechar C21, C19, C20 e C17C. Entregue como manda a `ORDEM_001`, seção 6: `RESULTADOS\007_RESULTADO.json` com `estado: cumprida` e aviso de até 15 linhas.

## Quadro de vigência deste túnel (regra do operador de 04/11/2026: o que foi cumprido ou superado não fica parecendo pendente)

Verbatim da regra: `C:\IALD\Central de Patentes\work\abrogacao_04nov\OPERADOR_04nov_abrogacao_verbatim.txt`, sha256 `e469431de0ce1126e94be18e8b49ecfc538da58242a73c26a7ad13daaaf959fd`.

| Ordem | Estado | Por quê |
|---|---|---|
| `ORDEM_001`, `CANAL_DESASSISTIDO.md` | **VIGENTES** | quem você é e como entrega |
| ORDEM 007 (esta) | **VIGENTE** | a release v408 do app, o contrato JEV v408 e a F0.3 da v408 |
| ORDEM 006 | cumprida | a release v407 foi instalada em 04/11, de 14:51 a 14:52 (`RESULTADOS\006_RESULTADO.json`) |
| ORDEM 005 | cumprida | `RESULTADOS\005_RESULTADO.json` |
| ORDEM 004 | cumprida ou superada | como diz o quadro da ORDEM 006; a §3 não se repete |
| ORDENS 002 e 003 | esta ordem não as muda | o filme da v406 aguarda o operador escutar e decidir a voz |

— `claude-site-custodia`, em nome próprio, pela ordem de handoff da gerência c1, 05/11/2026.
