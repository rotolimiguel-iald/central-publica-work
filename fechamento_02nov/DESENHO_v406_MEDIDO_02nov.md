# DESENHO v406 — o que foi MEDIDO depois do desenho (ao lado, 02/11/2026, gerência c1)

> O `DESENHO_v406.md` ficou com os bytes que a cadeia pinou (`insumos\DESENHO_v406.md`); as medidas vão aqui, ao lado.

- **MEDIDO (02/11/2026, 19:56–20:30, tarefa `IALD_build_k406c`, `v406\kernel\construir_marcas.txt`):** `lake build` incremental com os 301 a frio = **1736 s** (< 2400: nenhum patch de timeout; margem 2,1× sob os 3600 s do um.py); Audit = **280 s** (< 1200); rc 0/0; `Build completed successfully (10291 jobs)`; soma dos tempos dos 301 módulos 15 986 s (máximo 166 s). Pós-build verde (`POS_BUILD_v406.json`, 40 sinais, 0 falhas): 1794 bandeiras `ext_fch406_*`, escada 10066 → 11860, TOTAL 33732/26911/0, as 8 âncoras no trio. Candidato gerado: `um_v406_candidato.py` sha16 `7938fd4e97dc32f1` (42 726 415 B, 32 patches).
