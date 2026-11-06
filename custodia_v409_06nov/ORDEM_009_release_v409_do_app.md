# ORDEM 009 — A release v409 do app, o contrato JEV v409 e a memória científica da fila (F0.3)

06/11/2026. De: a sessão de custódia (`claude-site-custodia`), pela ordem de handoff da gerência c1 (pela D57, a cadeia da v409 termina no handoff e não tem S10). Para: `claude-app-orquestrador` (o app Claude em modo work). Ordem do operador (verbatim em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_05nov_energia_caiu_de_novo_continue_ate_v409_publicada_verbatim.txt`, sha16 `209636842f72466d`): «energia caiu de novo, continue até termos a v409 publicada»; e a autorização de publicar dada por ele à custódia em 06/11/2026 («Publicar tudo agora»); herdada e vigente para o app: a ordem de 03/11/2026 («o app e o contrato do JEV precisam ser sempre atualizados para a forma canônica mais madura, podia ser até automático isso, e o orquestrador pode executar o que vc mandar»). A `ORDEM_001` continua valendo inteira (quem você é, o Escritório fora, o que nunca faz sem o operador).

Estado lido do selo e do git pela cadeia agora, não digitado: versão **v409**, `um.py` pino **53284ba461ecd940** (sha256 inteiro `53284ba461ecd94060cc2d12fed992bba70ab857f70198b24e6535b9f24f8da6`), a versão anterior **v408**; o espelho público `the_boundary` no commit **1c76ad4a** e a Central no commit **1aa509c4** (HEAD local no momento da ordem; se a custódia ainda não os publicou, o commit vigente é o que o `git` local disser e você o declara). O app instalado deve estar na release **v409** quando você terminar; a cadeia só fecha o C21 da custódia (G1) com o seu recibo conferido na fonte.

## 1. A release v409 do app e o contrato JEV v409 (fase A/B; construtor ≠ revisor)

Ponto de partida obrigatório: a pasta da release anterior (`C:\IALD\Central de Patentes\work\iald_v408_20261105`): copie-a para `C:\IALD\Central de Patentes\work\iald_v409_<data>\` e leia primeiro o `LICOES_*.md` inteiro dela (o que ela manda para a próxima release, e que você aplica antes de construir: flags de retenção, `max_chars` do `reading`, a janela P2).
- **A janela P2 do `shared` (decisão de projeto D53 da gerência c1, 04/11/2026):** no `shared` ficam em literal completo só a versão corrente (v409) e a anterior (v408); as anteriores (as mais velhas que v408) passam a tópicos regenerados, **sem compactar `the_iald_index` nem os literais `limites`/`diz`/`nao_diz` da versão corrente**. Se ainda assim não couber, você MEDE e propõe o teto novo com os números (bytes por versão, folga), antes do `finalize`; não desliza por adivinhação.
- A ordem na missão: `deploy → submit → accept → claim verify → verify_installed`.
- Fontes da ciência: o selo, o core e o manifesto do kernel do Nós (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\`: `um_absoluto_selo.json`, `um_absoluto.json`, `tgl_kernel_proof_manifest.json`) e o espelho público (o `prepare.py` lê o git local do `the_boundary`). Só leitura no Nós e no espelho.
- `app/prepare.py` gera `jev_control_v409.json` (valida, canoniza, grava em `canonical_releases\v409_<hash>\`), com `cfg.release = v409`; siga o `install_plan.json` e os `*_stdout.txt` da release anterior como roteiro.
- **Construtor ≠ revisor:** rode um revisor independente (outro agente/sessão do app, estreito, com a lista da release anterior: `REVISAO_*` e `INSTALLED_VERIFICATION.json`); no máximo duas rodadas; ressalvas BAIXAS vão escritas.
- **Reinício do filho web:** se a instalação exigir reiniciar o serviço (porta 8082, supervisor), pare: é do operador (`INSTALLED_RESTART_REQUIRED`). Peça-lhe em uma linha, por versão.
- Nada toca `um.py`, selo, kernel, gate, cofre, nem `C:\IALD\Central de Patentes\Chatgpt\` (só leitura). Nenhuma chamada paga de geração para validar.

Entrega: `RELEASE.json`, `deployment.json`, `INSTALLED_VERIFICATION.json` (status `PASS`, `identity.release = v409`), `LICOES_v409.md`, o contrato `jev_control_v409.json` pinado, e `TORRE_IALD\torre.py gerar` rodado depois.

## 2. A memória científica da fila sincronizada à v409 (F0.3)

Texto da unidade: o `DESPACHO_CODEX_F03_*` mais recente em `C:\IALD\Central de Patentes\work\custodia_*`. Onde diz «coordenadora» ou «Codex», leia-se você. Reaproveite `work\scientific_memory_sync_20261013` (snapshot imutável, hashes e trechos, revisão independente real, ativação **pela API com proteção de concorrência**, conferência da geração recebida em processo novo, recibo em `work\scientific_memory_sync_<data>_v409\`). **Gate:** se algum passo exigir escrever dentro de `C:\IALD\Central de Patentes\Chatgpt\`, PARE e relate; a pasta é do ChatGPT e segue só leitura. Relatório de até 15 linhas.

## 3. As tarefas agendadas

Não se repetem por esta ordem: a criação foi negada três vezes (`RESULTADOS\004_RESULTADO.json`) e a ORDEM 006 as tirou de vigência.

## 4. O recibo que a cadeia espera (e o prazo)

A custódia espera, ao mesmo tempo: (a) `RELATORIO_<data>.md` nesta pasta, escrito depois desta ordem e citando `ORDEM_009`, ou `RESULTADOS\009_RESULTADO.json` com `estado: cumprida` (a forma durável do `CANAL_DESASSISTIDO.md`); (b) `INSTALLED_VERIFICATION.json` em `work\iald_v409_*\`, `status PASS`, release v409; (c) `jev_control_v409.json` pinado em `canonical_releases\v409_<hash>\`; e então **confere na fonte** `C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json`: `operational_core.current_release = v409`, `release_source_sha256` = o pino acima, `jev_control.release = v409` e o sha256 do arquivo do contrato. Sem recibo, o C21 da custódia fica aberto, visível; nunca se marca «ok» sem a conferência. Depósito em `memory\fila\depositos\claude-app\`, `transition` na sua referência ACOM e registro no Mapa de Rotas (rota `app.release.v409`, nova). Recusa e parada são resultado; o que você traz é [DECLARADO] até a gerência conferir na fonte.

— `claude-site-custodia`, pela ordem de handoff da gerência c1, 06/11/2026.

---

## Ao lado (06/11/2026): o que mudou desde o molde da v408

**1. As lições da v408** estão em `C:\IALD\Central de Patentes\work\iald_v408_20261105\LICOES_v408.md` (sha16 `cd261e18b215c51e`). Com só v408 e v407 em literal, o pacote do `shared` ficou em 838.165 B, e a folga mínima declarada foi 14.757 B (DeepSeek; Kimi 18.146; MiMo 14.774). Pela D53, agora ficam v409 e v408 em literal, e a v407 vira tópico regenerado. Meça antes do `finalize` e escreva no `LICOES_v409.md` os bytes por versão e a folga. Se não couber, proponha o teto com os números, sem deslizar por adivinhação.
**2. Lição da F0.3 da v408:** antes do CAS, confira as coordenadas de todos os trechos e a igualdade dos hashes nos caminhos definitivos. Entregue o `DELIVERY_TECHNICAL_R1.json` direto no esquema da fila.
**3. O reinício do filho web (porta 8082)** é do operador, por versão, em uma linha, com `quiet()` conferido.
**4. Os instantâneos da ACOM** (lição da v408) já foram reconciliados em 05/11: 3 locais, os mais velhos no arquivo `D:\`, restauração isolada verificada (`work\custodia_v408_05nov\RESTAURACAO_SNAPSHOT_ACOM_v408.json`). Nada a fazer.

## Quadro de vigência deste túnel (regra do operador de 04/11/2026)

Verbatim da regra: `C:\IALD\Central de Patentes\work\abrogacao_04nov\OPERADOR_04nov_abrogacao_verbatim.txt`, sha256 `e469431de0ce1126e94be18e8b49ecfc538da58242a73c26a7ad13daaaf959fd`.

| Ordem | Estado | Por quê |
|---|---|---|
| `ORDEM_001`, `CANAL_DESASSISTIDO.md` | **VIGENTES** | quem você é e como entrega |
| ORDEM 009 (esta) | **VIGENTE** | a release v409 do app, o contrato JEV v409 e a F0.3 da v409 |
| ORDEM 007 | cumprida | a release v408 (`RESULTADOS\007_RESULTADO.json`, estado cumprida) |
| ORDEM 008 | sem objeto | ab-rogava a 007, mas a 007 já tinha sido cumprida quando a 008 foi escrita |
| ORDENS 004, 005 e 006 | cumpridas ou superadas | como dizem os quadros da 006 e da 007 |
| ORDENS 002 e 003 | esta ordem não as muda | o filme da v406 aguarda o operador escutar e decidir a voz |
