# RUNBOOK DO OPERADOR — implantação e reversão do conserto ACOM (R2.2, 13/10/2026)

Este roteiro é para o operador (Luiz) executar à mão, no PowerShell, na máquina de produção. Tudo aqui é **ato do
operador**. A gerência e os agentes não rodaram nada disto em produção, nem em dry-run. Estatutos: [REAL] medido ·
[DERIVED] deduzido · [DECLARADO] afirmado e não refeito aqui · [OPEN] · [INPUT] decisão do operador.

Pasta da R2.2: `C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2`

- Ferramentas: `implantar.py`, `reverter.py`, `implantacao_lib.py`.
- Configuração: `implantar_config_producao_r2_2.json`.
- Candidato: `candidato_r2_2\C`, com 15 arquivos e o manifesto `CANDIDATO_MANIFESTO_R2_2.json`.
- Recibos: `recibos_producao_r2_2\`. A pasta nasce no primeiro dry-run.

**Use só os comandos deste roteiro.** Os comandos do `RESULTADO_R2_1.md` (§4) e do `REVISAO_R2.md` (§5) estão
superados. A trava da R2.2 também lê os recibos da R2.1 e do R2.

---

## 0. Antes de começar: a janela quieta

1. **Feche todas as sessões do Claude Code e do Codex**, inclusive a da gerência (c1). É ela que hospeda os MCPs
   `iald-orchestrator` e `bancada-um`.
   - Motivo: quem já carregou a biblioteca de memória v1 passa a falhar fechado até reiniciar.
   - Pior: uma sessão que grave pela v1 entre o backup (passo 2) e a migração (passo 3) entra na migração, mas **se
     perde numa reversão**.
2. Não rode `session_memory.py` durante a janela.
3. O llama pode ficar como está.
4. Abra um PowerShell novo. Confira o Python:

   ```powershell
   python --version
   ```

   Deve dar 3.12 ou mais. O revisor mediu `C:\Python314\python.exe`, versão 3.14.3 [REAL, revisão R2.1 §5b].
5. Duração esperada com `--pular-mover-backups`: de 1 a 4 minutos de app parado [DERIVED, revisão R2 §4]. Inclui
   o silêncio de 10 s, duas cópias do banco de 357 MB, a migração, a troca de 15 arquivos, os blocos, o verify deep e
   até 180 s de espera pelo reinício.

---

## 1. Dry-run, imediatamente antes de implantar (só lê)

O dry-run lê e não muda nada. Ele confere:

- a trava de recibos anteriores;
- o CAS dos 15 alvos contra a produção;
- o banco: sem `-journal`, ninguém segurando escrita, `journal_mode` delete;
- o espaço em D:;
- o limite do `MEMORY.md` (até 200 linhas e 24.000 B);
- a tarefa agendada e os processos.

Ele grava só um recibo `RECIBO_IMPLANTACAO_dry_run_<carimbo>.json`.

```powershell
python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\implantar.py" --config "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\implantar_config_producao_r2_2.json" --dry-run
$LASTEXITCODE
```

**Exija `"status": "DRY_RUN_OK"` e saída 0.** Qualquer outra coisa = **pare**. Não implante. Leve a linha impressa à
gerência. Os casos mais prováveis:

| o que aparece | significado | o que fazer |
|---|---|---|
| `RECUSADA_RECIBO_ANTERIOR_NAO_REVERTIDO` | existe uma implantação real anterior (R2, R2.1 ou R2.2) sem reversão limpa | não implantar; rodar a reversão que `acao_requerida` indica (seção 5) |
| `FALHOU_EM_pre_conferencias` com «CAS» | um alvo de produção mudou desde o candidato | parar; a gerência refaz o candidato |
| `FALHOU_EM_aplicar_blocos` | por exemplo, o `MEMORY.md` passaria de 200 linhas ou 24.000 B | parar; enxugar o `MEMORY.md` pela regra dos dois arquivos e repetir o dry-run |

Folga do `MEMORY.md` às 08:57: 188 linhas e 18.928 B. São 12 linhas de folga [REAL, revisão R2.1 §5b].

---

## 2. Implantar (sem mover os backups legados agora)

Rode logo depois do dry-run, ainda na janela quieta. **Não abra o recibo enquanto roda.** Desde a R2.1 um leitor de
até 30 s é tolerado, mas não há motivo para testar isso.

```powershell
python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\implantar.py" --config "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\implantar_config_producao_r2_2.json" --pular-mover-backups
$LASTEXITCODE
```

A saída é uma linha JSON. Ela traz `status`, o caminho do `recibo` e `acao_requerida`.

| saída | `status` | o que fazer |
|---|---|---|
| **0** | `CONCLUIDA` | **o esperado.** Siga para a seção 3 |
| **3** | `CONCLUIDA_AGUARDANDO_REINICIO` | a implantação foi verificada (passos 0–7), mas o app não respondeu `/login` no prazo. **NÃO reverta de imediato**: leia a seção 2.1 |
| **1** | `FALHOU_EM_<passo>` ou `RECUSADA_…` | leia `acao_requerida`. Se houve mudança (passos 3–7), o app fica parado e a tarefa desabilitada **por desenho**: rode a reversão (seção 5). Se a falha veio antes de qualquer mudança (passos 0–2), o app voltou ao estado de antes. Confira a seção 3 itens 1–3 |

### 2.1 Saída 3: app saudável atrasado ou app v2 em laço de queda?

A saída 3 cobre **dois casos** (por desenho; P8/P8b da revisão R2.1):

- o app v2 sobe, mas demora (saudável atrasado);
- o app v2 morre ao nascer e o supervisor o relança sem parar (laço de queda).

A R2.2 observou os pids do app durante a espera. Ela escreve a leitura no campo `diagnostico_reinicio` (na saída e no
recibo) e explica, em `acao_requerida`, como distinguir os dois casos e o que fazer.

- `diagnostico_reinicio.leitura = "LENTO_PROVAVEL"`: um só filho web, sempre o mesmo pid. **Não reverta.** Confira em
  alguns minutos, como abaixo.
- `diagnostico_reinicio.leitura = "LACO_DE_QUEDA_PROVAVEL"`: o pid do filho web mudou, ou o filho sumiu e voltou, ou
  nunca ficou de pé com o supervisor vivo. Confirme como abaixo. **Confirmado o laço, não espere: reverta (seção 5)**
  e leve o log do app à gerência.

**Como distinguir.** Rode duas vezes, com 1 minuto entre elas:

```powershell
Get-CimInstance Win32_Process -Filter "name='python.exe'" | Where-Object { $_.CommandLine -match 'iald_web_server\.py' } | Select-Object ProcessId,CreationDate
(Invoke-WebRequest -UseBasicParsing -Uri http://127.0.0.1:8082/login).StatusCode
```

- **App lento (saudável atrasado):** o MESMO `ProcessId` nas duas leituras, a `CreationDate` antiga, e `/login`
  passando a dar 200. Espere e confira de novo. Se em 10 minutos `/login` ainda não der 200 **e** o `ProcessId`
  estiver mudando, trate como laço de queda.
- **Laço de queda:** o `ProcessId` muda entre as leituras, ou some e volta. A `CreationDate` é sempre recente e
  `/login` nunca dá 200. O código novo não sobe: **reverta** (seção 5).

---

## 3. Conferências depois de implantar (com `CONCLUIDA`, ou com a saída 3 já resolvida)

1. **O app responde.** Deve dar `200`:

   ```powershell
   (Invoke-WebRequest -UseBasicParsing -Uri http://127.0.0.1:8082/login).StatusCode
   ```

2. **A tarefa agendada está HABILITADA.** `State` deve ser `Running` ou `Ready`, **nunca** `Disabled`:

   ```powershell
   Get-ScheduledTask -TaskName 'IALD Web Server' | Select-Object TaskName,State
   ```

   Se der `Disabled` com o app no ar: `Enable-ScheduledTask -TaskName 'IALD Web Server'`, e avise a gerência.
3. **Um supervisor e um filho web.** Deve listar exatamente 1 processo:

   ```powershell
   Get-CimInstance Win32_Process -Filter "name='python.exe'" | Where-Object { $_.CommandLine -match 'iald_web_server\.py' } | Select-Object ProcessId,CreationDate
   ```

4. **Reabra as sessões** (Claude Code e Codex). A janela quieta termina aqui.
5. **Repetir a `7_VERIFICACAO`** (ato da gerência, por um verificador independente). Base:
   `memoria_acom_fix_12out\7_VERIFICACAO\VERIFICACAO_FINAL.md`, os itens 1 a 10, agora contra o
   `RECIBO_IMPLANTACAO_<carimbo>.json` **real** que o passo 2 imprimiu.
   - A observação precisa ter **janela de mais de 30 minutos**, que contenha ao menos uma batida do heartbeat (o
     intervalo é de 1.800 s).
   - O **llama precisa estar online** (o servidor do modelo em :8081 [DECLARADO, CLAUDE.md]).
   - Sem isso, o item 7b («nenhum evento a mais») não discrimina.
   - Depois do reinício, a primeira batida grava **1 evento**, de classe estabelecida, cerca de 90 s após o start
     [DERIVED, revisão R2 §4.6].
   - Exija CONFERE nos itens 1 a 10.

---

## 4. Mover os backups legados para D: (depois, com o app v2 no ar)

O arquivador **instalado** só toca `memory.sqlite3.bak_*`, e a v2 não cria esse tipo de arquivo. Por isso ele roda
com o app no ar. Medida da revisão R2.1, às 08:57: 785 backups legados, com 99,8 GB [REAL]. São de 10 a 25 minutos
de E/S [DERIVED, revisão R2 §4.1].

**Primeiro o dry-run.** Ele lê e mostra o plano: `found`, `to_move` e o `plan` com os bytes.

```powershell
python -X utf8 C:\IALD\MEMORIA_IALD\mover_backups_antigos.py --state C:\IALD\MEMORIA_IALD\state --dest D:\IALD_ARQUIVO\MEMORIA_IALD\backups_ate_20261012 --keep 3 --dry-run
```

Confira se `to_move` é o número de backups menos 3. Depois, o mesmo comando **sem** `--dry-run`:

```powershell
python -X utf8 C:\IALD\MEMORIA_IALD\mover_backups_antigos.py --state C:\IALD\MEMORIA_IALD\state --dest D:\IALD_ARQUIVO\MEMORIA_IALD\backups_ate_20261012 --keep 3
```

- **Exija** `"ok": true` e `"failed": null`. Guarde o `manifest_jsonl` e o seu sha256: eles ficam em
  `D:\IALD_ARQUIVO\MEMORIA_IALD\backups_ate_20261012\`.
- O arquivador copia, confere o sha256 e só então remove a origem. Uma falha preserva a origem.

---

## 5. Reverter (só se algo falhou, ou por decisão de desfazer)

O reverter acha sozinho a **única** implantação pendente de reversão:

```powershell
python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\reverter.py" --config "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\implantar_config_producao_r2_2.json"
$LASTEXITCODE
```

Se ele recusar porque há 0 ou mais de 1 pendente, use o recibo que o implantar imprimiu:

```powershell
python -X utf8 "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\reverter.py" --recibo "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\recibos_producao_r2_2\RECIBO_IMPLANTACAO_<carimbo>.json"
```

Para ver o plano sem mudar nada, acrescente `--dry-run` a qualquer dos dois.

**Exija, todos juntos:** `"status": "REVERTIDA"`, `"app_religado": true`, `"acao_requerida": null`, `"ok": true` e
saída 0. Depois refaça a seção 3, itens 1 a 3: `/login` 200, tarefa não `Disabled`, 1 filho web.

| o que aparece | significado | o que fazer |
|---|---|---|
| `FALHOU_EM_<passo>` (saída 1) | a reversão não fechou; o app **não** foi religado sobre estado misto | leia `acao_requerida`: ela traz o **estado LIDO** (tarefa, supervisores, filhos web) e o comando. Remova a causa (ex.: um arquivo preso por outro processo) e rode **o mesmo comando** de novo. O 2º reverter fecha (K4, K4b, K4c, K5 no ensaio) |
| `FALHOU_EM_parar_app` | o reverter **não conseguiu parar o app**: nada foi restaurado e a implantação continua no lugar | a tarefa foi reabilitada se foi ele que a desabilitou. Se `acao_requerida` diz «VIVO SEM SUPERVISOR», há duas saídas: manter a v2 (rodar `stop_iald_web.ps1` na pasta do app e depois `Start-ScheduledTask -TaskName 'IALD Web Server'`) ou reverter (remover a causa e rodar o reverter de novo). Confira `Get-ScheduledTask` e os processos |
| `REVERTIDA_AGUARDANDO_REINICIO` | arquivos e banco voltaram, mas o app ORIGINAL não respondeu `/login` no prazo | faça o «como distinguir» da seção 2.1. Um laço de queda aqui é do app original: **não rode o implantar**, chame a gerência |
| `REVERTIDA_SEM_RELIGAR` | só com `--sem-reiniciar`, por escolha: tudo voltou, o app não foi religado | `acao_requerida` diz como subir: `Enable-ScheduledTask` e `Start-ScheduledTask` |

- `--forcar-reinicio` religa sobre estado misto. **Só por decisão explícita** do operador, depois de falar com a
  gerência.
- Os backups legados movidos para D: ficam lá, salvo `--mover-backups-de-volta`.
- O banco v1 restaurado não recebe os eventos v2 posteriores à migração. Eles ficam como evidência em `journal\` e
  `snapshots\`.

---

## 6. Regras dos recibos (valem sempre)

- **Nunca renomeie, apague nem edite um recibo** (`RECIBO_IMPLANTACAO_*`, `RECIBO_REVERSAO_*`, `BLOCOS_RECIBO_*`,
  `MIGRACAO_RECIBO_*`). A trava e a reversão dependem deles.
  - Com o recibo renomeado ou apagado, a recuperação automática se perde (K2b, K2c).
  - Com o recibo truncado, tudo recusa (K2d).
- Para guardar uma cópia, **copie para FORA** de `recibos_producao_r2_2`. Por exemplo:

  ```powershell
  New-Item -ItemType Directory -Force "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\copias_de_recibos" | Out-Null
  Copy-Item "<caminho do recibo>" "C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\copias_de_recibos\"
  ```

  Uma cópia **dentro** da pasta de recibos, com o prefixo `RECIBO_IMPLANTACAO`, conta como segunda implantação
  pendente.
- **Nunca rode o implantar de novo antes de reverter** uma implantação real que falhou ou concluiu. A própria trava
  recusa.
- A pasta `9_R2_2` contém o `iald_web_server.py` do candidato **com a chave de API de produção**. Não publique nem
  copie `work\memoria_acom_fix_12out` para fora. O git da Central já ignora `**/iald_web_server*`.

---

## 7. O que muda depois da implantação (saiba antes)

1. **Contexto `1bcf55a4-06fe-5e57-a2ad-640f2de13b53`** (casa IALD, operator, revisão 3) **ficará recusado**. Depois
   da implantação, `get` e `project` desse contexto são recusados pelo filtro D4 (`escritorio_path`); `verify` e
   `transition` seguem. A recusa é visível, sem redação silenciosa.
   - Uma sessão que use esse contexto verá a recusa.
   - O destino do contexto é decisão do operador [INPUT].
   - Fontes: REVISAO_R2 §4.4 e RESULTADO_INTEGRACAO_R2 §6.4 [REAL lá].
2. **O psion não é restaurado.** Nem a implantação nem a reversão restauram o `iald_psion_state_32B.json`.
   - As ferramentas nunca abrem esse arquivo.
   - O heartbeat v2 continua a atualizá-lo, agora com troca atômica e uma cópia diária de bytes
     `iald_psion_state_32B.json.bak_<AAAAMMDD>` ao lado (D3c; `HEARTBEAT_PSION_DAILY_BAK = True` no candidato [REAL]).
   - Restaurar os bytes de 27/09, ou manter os atuais e deixar a média móvel recuperar, é decisão do operador [INPUT].
     As opções estão em `0_DIAGNOSTICO\ESPECIFICACAO.md`, §D3(c): «Restauração: NÃO executar agora».
3. **Política de instantâneos: decisão pendente** [INPUT, D1-B].
   - Na v2, o instantâneo é o **banco inteiro** (357 MB) e sai a cada 50 mutações ou depois de 60 minutos.
   - Ficam 3 no C:, cerca de 1,1 GB fixos. Os outros vão para `D:\IALD_ARQUIVO\MEMORIA_IALD\snapshots`.
   - Com cerca de 24 instantâneos por dia, são **≈ 8,6 GB/dia para D:, sem poda** [DERIVED, revisão R2 §4.5;
     especificação §3.2]. Isso dá cerca de 7 meses de D:, que tinha 2,10 TB livres às 08:57 [REAL, revisão R2.1 §5b].
   - Cada instantâneo custa de 0,8 a 2,3 s dentro da trava de escrita.
   - A saída é a opção D1-B (compactar o banco vivo para cerca de 3 MB) ou uma retenção em D:. Até lá, acompanhe o
     espaço livre de D: semanalmente:

     ```powershell
     Get-PSDrive D
     ```

4. **MCPs e sessões que já tinham a v1 carregada** falham fechado (`Unsupported or missing memory schema`) até
   reiniciar. Basta reabrir.
5. **Os cmdlets reais do Agendador** (`Disable`, `Stop`, `Enable` e `Start-ScheduledTask`) **nunca rodaram de verdade**
   [OPEN]. Todos os ensaios usaram o backend simulado. Daí a conferência da tarefa na seção 3, item 2.

---

## 8. Resumo em uma tela

| # | comando ou ato | exigir |
|---|---|---|
| 0 | fechar as sessões Claude e Codex (inclusive a da gerência) | janela quieta |
| 1 | `implantar.py --config …r2_2.json --dry-run` | `DRY_RUN_OK`, saída 0 |
| 2 | `implantar.py --config …r2_2.json --pular-mover-backups` | `CONCLUIDA`, saída 0 (saída 3: seção 2.1) |
| 3 | `/login`, `Get-ScheduledTask`, processos; reabrir as sessões; 7_VERIFICACAO com janela > 30 min e llama online | 200; não `Disabled`; 1 filho web; CONFERE |
| 4 | `mover_backups_antigos.py … --dry-run`, depois sem `--dry-run` | plano coerente; `ok: true`, `failed: null` |
| 5 | (se preciso) `reverter.py --config …r2_2.json` | `REVERTIDA`, `app_religado: true`, `acao_requerida: null`, `ok: true` |
| — | recibos | nunca renomear, apagar nem editar; copiar só para fora |


---

> **AO LADO (13/10/2026, gerência c1; revisão independente da R2.2, `11_REVISAO_R2_2\REVISAO_R2_2.md`, veredito PODE_IMPLANTAR_COM_RESSALVAS; nenhum comando quebrado):**
> 1. **§3 item 3:** confira também o supervisor, não só o filho web. Em PowerShell: `Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" | Where-Object { $_.CommandLine -like '*start_iald_web.ps1*' } | Select-Object ProcessId,CreationDate`. Deve haver um supervisor e um filho web.
> 2. **Folga do MEMORY.md:** às 10:37 eram 191 linhas (folga de 9 até 200), não 12. O dry-run decide; se recusar por limite, a gerência move linhas para o MEMORY_2.md antes.
> 3. **Banco ocupado:** se o dry-run demorar, é a sonda `BEGIN IMMEDIATE`, que espera até 30 s por um escritor. Feche as sessões e repita; não force.
