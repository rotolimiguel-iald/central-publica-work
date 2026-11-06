# RETOMADA 2 DO CONSTRUTOR DA v409 — gerência c1 (05/11/2026, ~17h18), do estado MEDIDO em disco

> A energia caiu de novo às ~17:10 (boot 17:12:33). Nada se perde em disco; morrem os processos.

## 1. Medido
- `preparar_bundle` dos DOIS módulos feito (16:57): `pedra\TraducaoTuring.lean` e `pedra\ParNaFaceDeFock.lean`, `BUNDLE_v409.json` 16:57; raiz `C:\t\k409c\final\TGLExt.lean` 16:57:37 (backup ao lado).
- Build do kernel no sandbox CONCLUÍDO: `kernel\construir_marcas.txt` rc_build=0 às 17:05:33; `kernel\lake_build.log` «Build completed successfully (10306 jobs)»; oleans de `TraducaoTuring` e `ParNaFaceDeFock` em `C:\t\k409c\final\.lake\build\lib\lean\TGLExt\` (16:58).
- O AUDIT NÃO TERMINOU: `kernel\audit.log` parou às 17:06:12 com a última linha CORTADA no meio (a queda pegou o Audit ou o buffer). Refazer o Audit (só a etapa do Audit do `construir_kernel_v409.sh`, no sandbox; não precisa recompilar o kernel) e só então o `pos_build_kernel_v409.py` (o `POS_BUILD_v409.json` em disco é o VELHO, 13:06).
- Adaptações feitas até 17:08:32: runtime, registros, delta (D60/E28), guarda das frases, artigos, gerador do candidato e pós-build para dois módulos (os `_dois_modulos_*`, `_d60_e28_marcas_v409.py`, `_f43_numa_leitura_v409.py`). Conferir por `ast.parse` antes de seguir.
- A Bancada foi religada pela gerência às 17:17 (PID 45344; porta 18777; recibo em `tentativas\`).

## 2. A ordem
Audit (sandbox) → `pos_build_kernel_v409.py` (bandeiras e escada MEDIDAS) → `copiar_insumos_v409.py` → o que faltar das adaptações ao AO LADO mais novo do DESENHO → `gerar_candidato_v409.py` → `refazer_candidato_v409.sh` (comparar → ensaio «TUDO PASSOU» → esperados → conferidores → citações → diff_e_pinos → conferir_instalar_rito → p00 n/n) → `fim_de_cadeia_v409.sh` → `gerar_relatorio_v409.py` → depósito na fila → rota no Mapa. PARAR aí.

— gerência c1, 05/11/2026.
