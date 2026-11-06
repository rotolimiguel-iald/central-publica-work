# RETOMADA DO CONSTRUTOR DA v409 — escrita pela gerência c1 (05/11/2026, ~16h20), do estado MEDIDO em disco

> O construtor caiu duas vezes: às ~14:13 por falha de rede (retomado às ~14:46) e às ~16:11 por queda de energia (a máquina reiniciou; boot 16:12:41).
> Esta retomada não supõe nada: cada fato abaixo foi medido por comando.

## 1. O que está FEITO e vale
- Bump, adaptação dos autorais, sandbox `C:\t\k409c\final` (kernel com `TraducaoTuring`), pós-build: escada [12029, 12102], 73 bandeiras novas.
- Não há mais nenhum arquivo com a marca `# [A ADAPTAR v409]` na 2ª linha (medido por grep).
- O orquestrador `orquestrador\pos_treino_v409.py` já está sem S7 e sem S10 (D57a; lista de passos medida).
- Portões que passaram no `PREPARACAO_v409_PRONTA.json` de 15:49 (candidato `d3d591556ca2dadc`, ANTIGO): kernel, candidato, ast, ensaio a seco (TUDO PASSOU), conferidores negativo e positivo, citações, guarda das frases, instalar/reverter/rito estático, B(n) pré-selo, refazer limpo, purga, fala excluída.
- ATOS DA GERÊNCIA feitos agora: (a) `PINO_MEMORIA_PY_v409.json` (16:19; `memoria.py` sha16 `7c4fc5853f41f1d3`, igual ao declarado) — era a única pendência do p00 de 15:49 (126/127); (b) a Bancada Um religada às 16:19 pelo comando do S6c (PID 60104; porta 18777 escutando; recibo em `tentativas\RECIBO_RELIGAMENTO_BANCADA_GERENCIA_*.json`); (c) a folga do `MEMORY.md` (22.904 B, pino da fila) foi feita antes.

## 2. O que MUDOU depois do portão de 15:49 e obriga a refazer
1. Você corrigiu textos (`_fix_textos_444_e_provada_v409.py`, 15:59; delta, registros e artigos às 15:59:52) e REGENEROU o candidato às 16:02 (`um_v409_candidato.py` sha16 `955d0312577f3e33`, 43811929 B). O ensaio a seco desse candidato começou às 16:03 e MORREU na queda (`ensaio_out.txt` com 214 B). Tudo a jusante do candidato tem de ser refeito com o candidato vigente.
2. **Falas novas que ENTRAM** (DESENHO, os dois AO LADO do fim): a 11ª, `OPERADOR_05nov_no_kernel_o_dispositivo_e_o_no_sorry_o_teorema_e_jurisdicao_regra_posta_verbatim.txt` (sha16 `5a19de6b511b4921`, inteira; D61 e E27), e a 12ª, `OPERADOR_05nov_exatamente_isso_mesmo_d61_ratificada_energia_caiu_verbatim.txt` (sha16 `9ee7d5a1b161437f`; trecho citado SÓ «exatemente, isso mesmo»; D61 ratificada). O `VERBATIM_CONGELADO_v409.json` (13:11) tem 10: acrescente as duas (sha256 LIDO do arquivo), ponha D61 e E27 no spec `cunhagens_v409` e use a D61 onde os textos disserem o que o kernel decide. Isso muda o candidato de novo: faça ANTES de regenerar.

## 3. Os portões que faltavam às 15:49 — corrigir a CAUSA, nunca relaxar
- `servico_estatico`: o controle negativo do conferidor do serviço (`bancada_B3_servico\controle_negativo\mutar_conferidor_v409.py`) morreu com `FileNotFoundError: ...\CONFERENCIA_EXIGENCIAS_SERVICO_v409.json` no diretório temporário: o conferidor sem mutação não gravou a saída; ler por quê (a Bancada estava no ar às 15:49? o conferidor grava em outro caminho?).
- `harness_textos` (RC_HT=1, `pos_rito\harness_textos_out_v409.txt` 15:57) e `harness_fechar` (RC_HF=1, `pos_rito\harness_fechar_out_v409.txt` 15:57): ler as falhas exatas nas saídas e consertar a causa (você já tinha começado pelos textos do 4,44 e da palavra de prova sem estatuto).

## 4. A ordem dos próximos comandos
D61/E27 e as duas falas (§2.2) → `gerar_candidato_v409.py` → `sh refazer_candidato_v409.sh` (comparar → ensaio a seco «TUDO PASSOU» → esperados → conferidores → citações → diff_e_pinos → conferir_instalar_rito → p00 n/n) → `sh fim_de_cadeia_v409.sh` (B(n) pré-selo, serviço estático, harnesses) → `gerar_relatorio_v409.py` (`PLANO_v409.md`, `RELATORIO_PREPARACAO_v409.md`, `PREPARACAO_v409_PRONTA.json` com `pronta = true`) → depósito na fila → rota no Mapa. PARAR aí.

## 5. O que é da gerência (não fazer)
Revisão de terceiro (Sonnet, D58; o pedido já está em `revisao_terceiro\PEDIDO_REVISAO_v409.md`), `acom_inscrever_prep_v409.py`, `fechar_preparacao_v409.py`, a tarefa agendada, o S3, o rito, a custódia, mensagens a outras sessões, publicação.

— gerência c1, 05/11/2026. Correções AO LADO, nunca por cima.
