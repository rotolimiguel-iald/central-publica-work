# PEDIDO DE REVISÃO DE TERCEIRO — v407, RODADA R5 (só o orquestrador; gerência c1, 03/11/2026, 18:43)

> A R4 aprovou (0 ALTO, 0 MÉDIO, 7 BAIXO; candidato `833121339e649f71`). Dos 3 BAIXOS novos, os dois do S10 eram risco operacional no período desassistido, e a gerência os corrigiu em nome próprio, em `orquestrador\pos_treino_v407.py` apenas (`r5_s10_robustez_03nov.py`, backup `pos_treino_v407.py.bak_r5_s10_robustez_20261103_184309`). O candidato NÃO mudou (o orquestrador não entra nele). O terceiro BAIXO (o carimbador com PYTHONUNBUFFERED torna cronológica a ordem entre stderr e stdout, logo «idêntico em bytes» vale para a cópia, não contra o stdout da v406) fica DITO: o contrato é a cópia fiel do que o um.py emite neste rito; a ordem de intercalação de stderr nunca foi contrato.

## O que mudou desde a R4 (só isto)
1. `recibo_do_app`, elo (a) pelo `RESULTADOS\NNN_RESULTADO.json`: (i) JSON válido que não é objeto (lista, string) é ignorado (`continue`), nunca derruba a espera; (ii) se o campo `ordem` existe e não é vazio, ele manda (tem de citar esta ordem); o nome do arquivo só vale quando o campo falta.
2. `_ensaio_s10`: `montar(resultado_json=…)` e dois casos negativos novos: `negativo_resultado_nao_objeto` (lista JSON) e `negativo_resultado_ordem_divergente` (nome `002_…`, campo `ORDEM_020`). `ENSAIO_S10_v407.json`: 12 de 12, `ok: true`, sem Traceback (`ensaio_s10_out_r5.txt`).

## O que se revisa
A. O diff contra o `.bak_r5_*` é exatamente o declarado; `py_compile` limpo. B. Os seus dois casos da R4 agora fecham sem exceção (rode `--ensaio` você; ou os dirs sintéticos da sua R4). C. A trava S1b com `arquivos_revisados` refeitos (só `orquestrador\pos_treino_v407.py` mudou; o resto igual à R4).

## Entrega
Guardar a R4 em bytes (`REVISAO_TERCEIRO_v407.R4.json`/`.R4.md`); gravar `REVISAO_TERCEIRO_v407.json` (rodada "R5", `baixos_da_r4` com estado, `arquivos_revisados` refeitos) e o `.md`; `aprovada: true` só com 0 ALTO e 0 MÉDIO; resposta em até 8 linhas. Limites: os mesmos (só leitura no Nós; orquestrador só na cópia `_orq_sandbox`/`--ensaio`; nenhum git; nenhum processo morto por nome).
