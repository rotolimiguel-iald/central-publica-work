# Helper F0.3 v409 — somente preparação para revisão

O helper `promote_v409.py` deriva de `scientific_memory_sync_20261105_v408/promote_v408.py`; diferenças em `PROMOTION_HELPER.patch`. Não foi importado nem executado. Análise sintática por AST apenas; nenhuma alegação de teste funcional. A autorização humana permanece pendente e o quadro permanece AGUARDA_OPERADOR.

`promotion/PLAN.json` é o plano executável candidato, preparado diretamente dos recibos, sem chamar o helper. `PROMOTION_PLAN.json` continua sendo o plano original aceito; ambos têm pinos próprios. O manifesto final é byte a byte o `MANIFEST_FINAL_CANDIDATE.json` revisado. O backup histórico do manifesto do staging fica preservado em work e não é um dos 16 arquivos publicados.

## Contrato de aprovação conjunta

O parent guardará a aprovação humana real em `C:\IALD\Central de Patentes\work\iald_v409_20261106\APROVACAO_V409.json`. O helper lê `operator_order:{path,sha256}` no topo e os campos vinculantes da fila no objeto `f03`, especificados em `promotion/APPROVAL_REQUIREMENTS.json`. Outros campos da aprovação conjunta podem tratar do app/restart; este helper não os executa. O original humano deve ser TXT não vazio na raiz da missão parent. O parent verifica autoridade e sentido; um arquivo preenchido por modelo não concede autorização.

Todas as etapas após `plan` exigem `--approval-sha256` com o hash lido do arquivo de aprovação efetivamente conferido. O contrato vincula geração, baseline, plano executável, script, plano revisado e referência parent. Divergência recusa; não atualizar baseline para vencer conflito.

## Execução futura, somente depois do gate

Cada etapa em processo separado, conferindo código zero; nenhuma destas linhas foi executada nesta preparação:

```powershell
$Q = 'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261106_v409'
$Wapp = 'C:\IALD\Central de Patentes\work\iald_v409_20261106'
$approvalPin = (Get-FileHash "$Wapp\APROVACAO_V409.json" -Algorithm SHA256).Hash.ToLower()
# $member deve ser o titular real da reivindicação vigente, após liberação humana normal do quadro.
& C:\Python314\python.exe -B -X utf8 "$Q\promote_v409.py" materialize --member $member --approval-sha256 $approvalPin
& C:\Python314\python.exe -B -X utf8 "$Q\promote_v409.py" verify-final --approval-sha256 $approvalPin
# PARAR para revisão real distinta dos caminhos finais e recibo QUEUE_FINAL_PATHS.json.
& C:\Python314\python.exe -B -X utf8 "$Q\promote_v409.py" activate --member $member --approval-sha256 $approvalPin
& C:\Python314\python.exe -B -X utf8 "$Q\promote_v409.py" receipt --approval-sha256 $approvalPin
```

Antes de cada mutação, o parent reivindica o requisito correspondente em sua missão, sincroniza e faz preflight com referência/revisão/lease atuais. A CLI preserva `require_claim` do quadro; não substitui o protocolo de missão do parent.

Materialização publica somente o diretório inativo, por rename sem sobrescrita no Windows; ACTIVE deve continuar com o baseline. `verify-final` verifica todas as 13 fontes/33036 coordenadas e os três modos nos caminhos definitivos. O parent grava `Wapp/review/QUEUE_FINAL_PATHS.json` com `status=PASS`, reviewer distinto do builder, generation, manifest_sha256, verification_sha256 e expected_active_sha256. Esses campos estão listados em APPROVAL_REQUIREMENTS.json.

Ativação passa por `ScientificMemorySync.activate` e API real `activate_release`, com lock de processo e expected_active_sha256; alvo exatamente já ativo é reconhecimento idempotente. Após interrupção, conferir ponteiro e recibos antes de qualquer ação; não repetir envio nem forçar baseline. Recepção em processo novo e preservação produzem `DELIVERY_TECHNICAL_R1.json` somente após sucesso. Nenhum restart, app, rede, geração de IA, um.py ou Lean pertence ao helper.
