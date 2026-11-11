# RETOMADA DA v410 — estado MEDIDO na parada (gerência c1, 06/11/2026 08:47)

> Motivo: o operador avisou que os créditos iam acabar («precisamos parar os trabalhos e aguardar a volta dos creditos») e mandou anotar tudo
> para continuar exatamente daqui. O construtor (agente) foi PARADO pela gerência (TaskStop) às ~08:45, no meio do passo «gerador» (reescrita
> do `gerar_candidato_v410.py` a partir do molde). Nada foi instalado no Nós; o um.py vivo é a v409 selada `53284ba461ecd940`.

## 1. O que está FEITO (medido em disco)
- DESENHO `DESENHO_v410.md` sha16 `283efc9c6d750e6d` (com o AO LADO da seção 5: 9 falas, D63–D70, E29, N_CHECKS_FECHO = 15, 19 âncoras).
- Insumo `insumos\IALD2.lean` sha16 `8fb9abacba40fb3c` (19/19 no trio, 0 avisos); recibo `insumos\RECIBO_PEDRAS_v410_NOMES.json`.
- Sandbox `C:\t\k410c\final` copiado do k409c; a pedra no sandbox `TGLExt\IALD2.lean` sha16 `4ad51565a1acdf60` CONTÉM a seção 5; `IALD2.olean` existe.
- Build + Audit do kernel no sandbox TERMINARAM: marcas `kernel\construir_marcas.txt` → rc_audit=0 07:36:05 | epoch_audit_fim=1793961365 | rc=0 | fim 2026-11-06 07:36:05.
- Bump, motor, scripts adaptados (forkA/forkB), registros, artigos PT/EN, guarda de frases (`GUARDA_FRASES_v410.json`), `CANDIDATO_v410.json`, `FORMAL_MAP_v410.json`.
- Candidato `um_v410_candidato.py` sha16 `6972d418b20133e6`; `comparar_v409_v410` ok = True (15 nós novos, 26 mudados, todos explicados; gate não se move).

## 2. O que FALTA (ordem; molde v409, `RETOMADA_CONSTRUTOR_v409.md` §4)
1. Conferir se o candidato acima é o FINAL do gerador (o construtor parou no meio de «Now the generator (full rewrite from the v409 molde)»): rodar de novo `gerar_candidato_v410.py` e `comparar_v409_v410.py`; se o sha16 mudar, vale o novo.
2. `ensaio_a_seco_v410.py` até «TUDO PASSOU» (corrigir a CAUSA, nunca relaxar teste) — inclui as 15 checagens do registro `iald2_v410`.
3. esperados → conferidores (controle negativo e caminho positivo) → citações → diff_e_pinos → conferir_instalar_rito → p00 → fim_de_cadeia (B19 pré-selo) → gerar_relatorio → `PREPARACAO_v410_PRONTA.json` pronta = true → depósito na fila (`claude-construtor-v410`) → rota no Mapa.
4. Gerência: revisor Sonnet (até 3 rodadas, D69) → `fechar_preparacao_v410.py` → `acom_inscrever_prep_v410.py` → pino da memória/folga → tarefa agendada `IALD_pos_treino_v410` (`C:\t\k410c\run_pos_treino.py`) → rito → HANDOFF à custódia (sem S7/S10).

## 3. Como retomar
- A gerência relança um construtor NOVO (o agente parado não se retoma) com o prompt da v410 (mesmas regras; está na conversa da sessão 6da8f00d e é o molde do da v409), dizendo: «leia PRIMEIRO `RETOMADA_CONSTRUTOR_v410.md`; o kernel do k410c está pronto (não refazer); comece pelo item 2.1».
- A Bancada (127.0.0.1:18777): conferir com GET; se cair, o comando do S6c do orquestrador da v409, com recibo em `tentativas\`.

## 4. Pendente do OPERADOR
- Ratificar os nomes das declarações da IALD2 (D63; hoje [DECLARADO]): `o_enunciado`, `o_algoritmo_iald`, `iald_ao_quadrado`, `o_signo_do_nome`, `o_signo_do_par`, `a_iald_e_o_seletor_luminodinamico` e os demais.
- D65: da fala «a solução definitiva de P=np» o um.py cita só «IALD — É O MEU ALGORITMO DE LEITURA DA TGL» (se quiser outro recorte, é decisão dele).

— gerência c1. Correções AO LADO, nunca por cima.
