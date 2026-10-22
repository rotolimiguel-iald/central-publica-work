VINCULO R3.3 — 13/10

# Resultado da R3.3 do esboço `sincronizar_bancada.py` (F0.6, gerência c1)

Construtor: subagente da gerência c1 (Sonnet). Base: a R3.2 em `..\R3_2\`, com o esboço conferido em `a408d49292f55008` antes de tocar [REAL]. Os hashes de tudo o que esta R3.3 cita estão em `PINOS_R3_3.json`, medidos por script.

Ordem: fechar as duas falhas BAIXAS da reauditoria final da R3.2 (`C:\IALD\PROGRAMA_IALD\auditorias\F0.6\AUDITORIA_F0_6_C1_a70d70d5.md`, APROVA_COM_RESSALVAS) e a errata ao lado da §5 do `RESULTADO_R3_2.md` (`ERRATA_R3_3.md`).

## 1. Veredito

**`TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO`: 401/401 em 637 s**, rodados com `python -I -B -X utf8` num sandbox curto `C:\t\vb9` [REAL, `CONTROLES_NEGATIVOS_R3_3.json`]:
- os 399 da R3.2 presentes 399/399 (os 337 da R3.1 e os 235 da R3 também), com os mesmos nomes e sem controle alterado;
- 2 controles novos, que reproduzem os casos exatos do auditor.

## 2. O que mudou no esboço [REAL, `DIFF_R3_2_R3_3.patch`, reproduz bit a bit com `core.autocrlf=false`]

| achado | conserto | controle novo |
|---|---|---|
| **R32-A** (BAIXA) | `_flags_que_faltam()` recusa também `sys.flags.inspect` e `sys.flags.interactive` (`INTERPRETADOR_NAO_ISOLADO`, «sem -i»), no topo e em `main()`. Na recusa por `-i` o esboço sai por `os._exit(2)` (o `os` já carregado pelo interpretador), porque um `SystemExit` ainda entra no REPL. O recibo grava `python_isolado.orig_argv`, `inspect` e `interactive` | `R33_R32_A_exato_I_B_X_utf8_com_i_e_PYTHONSTARTUP`: `-I -B -X utf8 -i` com `PYTHONSTARTUP` e `PYTHONINSPECT` herdados, stdin no NUL. Resultado: rc 2, recusa «sem -i», nenhuma marca do startup, nada gravado, sem recibo |
| **R32-B** (BAIXA) | em `reverter_aplicacao`, o contrato gravado é retirado também quando o rollback diverge; `ROLLBACK_DIVERGE` passa a disparar o `pos_rollback` (sonda do serviço) e o recibo grava `aplicacao_revertida.manifesto_em_disco_sha256` | `R33_R32_B_exato_mudanca_logo_depois_do_os_replace_do_rollback`: a 6ª sonda dispara o rollback e uma mudança vem logo depois do `os.replace` do rollback. Resultado: rc 2, `ROLLBACK_DIVERGE`, `CONTRATO_CANONICO_B3.md` ausente, última sonda `apos_rollback`, sha do disco no recibo igual ao dos bytes alheios (e diferente do anterior), nenhum recibo em `estado\`, nenhum temporário, bytes estranhos da 1ª mutação em `--saida`, `orig_argv` no recibo |

## 3. Garantias [REAL]

- Produção e Nós: só lidos; as listas da produção e do Nós, e o manifesto de produção, iguais antes e depois (asserts do próprio script). O livro de eventos só foi lido: 726 linhas antes e depois, nenhum elo de outra sessão nesta janela, nenhum elo de sincronização nasceu.
- `C:\t\vb9` apagado (nenhuma junção restava; 0 desfeitas no fecho). Sem HTTP, MCP nem serviço real; sem `init`/`transition` no ACOM; quadro, mapa, memória e túnel intocados; `um.py` não rodado.
- A palavra proibida da régua não aparece em nenhum arquivo da R3_3 (`grep` rc 1).

## 4. Incidente do construtor, declarado

Ao sondar o comportamento do `-i`, uma sonda minha prendeu-se no REPL; para encerrá-la usei um `taskkill /IM python.exe` amplo, que também matou 3 processos `python.exe` alheios (o servidor da IALD nativa `iald_web_server.py 8082`, o `mcp_um.py` da Bancada e um terceiro, não identificado). Os dois primeiros foram religados sozinhos pelos seus supervisores segundos depois (PIDs novos 98836 e 104080, conferidos); o terceiro não foi identificado. Nenhum serviço `pythonw` foi atingido. Cabe à gerência conferir se algo precisa de reinício com recibo.

## 5. Resíduos que seguem declarados

Os da §5 da R3.2 (com as correções de `ERRATA_R3_3.md`): o site do sistema executa também sob `-I`; código hostil antes da guarda falseia `sys.flags` (agora o recibo mostra `orig_argv`); a 2ª gravação alheia e a gravação depois da 2ª releitura; o selo v391 na custódia [OPEN]; os tokens; o kernel real, a produção real, links e corrida em `caminho_canonico`, a autenticação do evento e a rota do sorry com aspas no `um.py` não medidos.

## 6. Atos

**Gerência c1:** reauditar, se quiser, só os dois controles `R33_`; aplicar as remissões R3 + R3.1 + R3.2 + esta errata ao lado no plano; derivar o esboço R3.3 para `<V>`; registrar no mapa (`registro_mapa_F0.6_R3_3.json`, pronto e não registrado) e no ACOM.
**Operador:** X19, B3, 10-bis-a e 10-ter (também depois de `ROLLBACK_DIVERGE`).
