# ORDEM 002 — A release v407 do app, o contrato JEV v407 e a memória científica da fila (F0.3)

03/11/2026. De: o orquestrador da cadeia de selo da gerência c1 (`pos_treino_v407.py`, passo S10, automático). Para: `claude-app-orquestrador` (o app Claude em modo work). Ordem do operador (verbatim em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt`, sha16 `b89e4c909f37e163`): «o app e o contrato do JEV precisam ser sempre atualizados para a forma canônica mais madura, podia ser até automático isso, e o orquestrador pode executar o que vc mandar». A `ORDEM_001` continua valendo inteira (quem você é, o Escritório fora, o que nunca faz sem o operador).

Estado lido do selo e do git pela cadeia agora, não digitado: versão **v407**, `um.py` pino **833121339e649f71** (sha256 inteiro `833121339e649f7171e2eccca1a19b3a1564aa306a787ed8cea76ded0fdf3475`), a versão anterior **v406**; o espelho público `the_boundary` no commit **ESPELHO00** e a Central no commit **CENTRAL00** (HEAD local no momento da ordem; se a custódia ainda não os publicou, o commit vigente é o que o `git` local disser e você o declara). O app instalado deve estar na release **v407** quando você terminar; a cadeia só fecha o C21 da custódia (G1) com o seu recibo conferido na fonte.

## 1. A release v407 do app e o contrato JEV v407 (fase A/B; construtor ≠ revisor)

Ponto de partida obrigatório: a pasta da release anterior ((nenhuma pasta iald_v4xx encontrada; peça à gerência)): copie-a para `C:\IALD\Central de Patentes\work\iald_v407_<data>\` e leia primeiro o `LICOES_*.md` inteiro dela (o que ela manda para a próxima release, e que você aplica antes de construir: flags de retenção, `max_chars` do `reading`, a janela P2 — deslize pelos sufixos mais antigos primeiro até o pacote `shared` caber, e **mantenha os literais `limites`/`diz`/`nao_diz` na cápsula compacta**; não compacte `the_iald_index`).
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

A cadeia (`pos_treino_v407.py`, passo S10) espera, por até 24 h, ao mesmo tempo: (a) `RELATORIO_<data>.md` nesta pasta, escrito depois desta ordem e citando `ORDEM_002`, ou `RESULTADOS\002_RESULTADO.json` com `estado: cumprida` (a forma durável do `CANAL_DESASSISTIDO.md`); (b) `INSTALLED_VERIFICATION.json` em `work\iald_v407_*\`, `status PASS`, release v407; (c) `jev_control_v407.json` pinado em `canonical_releases\v407_<hash>\`; e então **confere na fonte** `C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json`: `operational_core.current_release = v407`, `release_source_sha256` = o pino acima, `jev_control.release = v407` e o sha256 do arquivo do contrato. Sem recibo em 24 h a cadeia PARA, visível, e a gerência decide; nunca marca «ok» sem a conferência. Depósito em `memory\fila\depositos\claude-app\`, `transition` na sua referência ACOM e registro no Mapa de Rotas (rota `app.release.v407`, nova). Recusa e parada são resultado; o que você traz é [DECLARADO] até a gerência conferir na fonte.

— O orquestrador da cadeia de selo (v407), em nome da gerência c1, 03/11/2026.
