# EMENDA ao recibo_parada_v404.py (gerência c1, 28/10/2026 22:00, antes do uso no 10-bis-a)

**O que estava:** o script registrava em `pid` o PID do recibo de religamento da v403 (43840), com a frase «último PID conhecido do serviço».
**O número corrige a frase:** o processo vivo na porta 18777 antes da parada era o PID 61408, criado em 28/10/2026 13:48:15
(linha de comando conferida por `Win32_Process`): o serviço foi religado de novo depois do recibo da v403. O molde da v403 tinha
o mesmo defeito (o `pid` 892 do recibo de parada da v403 era o do religamento da v402; o PID parado de fato, 47248, só aparecia
no texto da autorização).

**A emenda:** `pid` passa a ser o PID lido da porta antes da parada, dado por `V404_PID_PARADO` (e a data de criação por
`V404_PID_PARADO_CRIADO`), com a conferência de que esse PID já não existe; o PID do recibo da v403 fica dito em `pid_estado`,
com a razão da diferença. A lista de chaves do recibo é a MESMA do molde (o conferidor estático exige a igualdade).

| arquivo | sha16 |
|---|---|
| `recibo_parada_v404.py` (emendado) | `06a96f0e8ad165ba` |
| `recibo_parada_v404.py.bak_20261028_220026` (bytes antes da emenda) | `acb92c77d3325246` |

**Conferência estática** (`conferir_exigencias_servico_v404.py`, rodada numa CÓPIA no scratchpad porque o recibo real da conferência
não se sobrescreve): 26/27; a única condição reprovada é «o um.py do Nós AINDA NÃO é o candidato», que era do estado pré-instalação
e hoje reprova porque o Nós JÁ é o candidato (`3820476c83267f61`), como deve ser depois do rito. Cópia: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\conf_servico_20261028_220056\v404\bancada_B3_servico\CONFERENCIA_EXIGENCIAS_SERVICO_v404.json`.

Lição para o molde da v405: o recibo de parada lê o PID da porta no momento, nunca do recibo anterior.
