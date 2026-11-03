# -*- coding: utf-8 -*-
# regras (lote E2_refazer) de derivar_encanamento_v406.py: refazer, regras, regerar e o pino da memoria. ORIGEM v405 FINAL. Mapa: 403 -> 405 (a base selada), 405 -> 406 (esta rodada). Escrito pela ferramenta Write (barras invertidas).
entrada("refazer_candidato_v405.sh", autoral=True, regras=[])
entrada("refazer_sandbox_v405_pos_selo.sh", autoral=True, regras=[])
entrada("refazer_arvore_v405_pos_selo.py", autoral=True, regras=[])
entrada("regras_v405.py", autoral=True, regras=[
    ("ESCRITO em 27/10/2026 pela preparacao", "ESCRITO em 01/11/2026 pela preparacao", 1),
])
entrada("regerar_v405.sh", autoral=True, regras=[
    ("tudo o que depende das TRES PEDRAS (work\\cadeia_de_selo\\v406_kernel\\pedras\\Caminho.lean, Vida.lean e VerdadeAdendo.lean):", "tudo o que depende das OITO PEDRAS (as fontes da ordem da gerencia, conferidas por gerar_pino_das_pedras_v406.py contra os recibos):", 1),
    ("# ANTES: (1) atualizar pedras_sha16_da_ordem.json (o pino de cada pedra, lido do arquivo da pedra)", "# ANTES: (1) regenerar o pino (gerar_pino_das_pedras_v406.py le o arquivo de cada pedra e o recibo vigente; aplicar_errata_pedras_v406.py abre o caminho)", 1),
])
entrada("pino_memoria_py_v405.py", autoral=True, regras=[])
