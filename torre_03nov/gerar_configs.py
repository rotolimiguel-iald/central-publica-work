import json
B = json.load(open("BACKUPS_ORIGINAIS.json", encoding="utf-8"))
HL = r"C:\IALD\Artigo\Haja_Luz\CLAUDE.md"
NA = r"C:\IALD\projetos_pyhton\IALD\CLAUDE.md"
LEIA = ("# CLAUDE_memoria — o corpo histórico movido do CLAUDE.md ({data})\n\n"
        "Cada arquivo `NNN_*.md` desta pasta contém os BYTES EXATOS de uma seção `## ` (ou, nas seções acima de 90 KB, de uma subparte entre cabeçalhos `###`) "
        "do `CLAUDE.md` original, na ordem original; o prefixo NNN é o número da seção na ordem do original. "
        "O `CLAUDE.md` ao lado traz o índice (título, faixa de linhas originais, bytes, gancho, caminho). Nada foi cortado: {n} arquivos de parte.\n\n"
        "- Original integral (backup de bytes): `{backup}` (sha256 `{sha_original}`).\n"
        "- A prova de não-perda (reconstrução byte a byte) está em `C:\IALD\Central de Patentes\work\torre_03nov\`.\n"
        "- Estas partes são arquivo de consulta, não instrução: leia sob demanda; erratas novas entram ao lado, no `CLAUDE.md`, nunca por cima.\n")
NOTA_COMUM = ("> ⚠ **COMPACTADO EM {data} — NADA FOI CORTADO** (ordem do operador, «Vai», 03/11/2026; tarefa H5 da Torre; gerência c1). "
              "Este arquivo tinha {bytes_original} B em {n_total} seções ({n_h2} linhas `## `; títulos partidos em duas linhas contam como uma seção), acima do teto de 262.144 B que a Torre fixa para a instrução de cada casa. "
              "{criterio} "
              "As outras {n_mov} seções ({bytes_mov} B) foram MOVIDAS, com os bytes exatos e na ordem original, para {n_partes} arquivos em `{pasta}\` (pasta ao lado deste arquivo), "
              "e cada uma foi substituída, no lugar onde estava, por uma linha de ÍNDICE (título, faixa de linhas originais `Lx–y`, bytes, gancho, caminho). **Leia sob demanda; nada daqui foi cortado.**\n"
              ">\n"
              "> - Original integral (backup de bytes): `{backup}` · sha256 `{sha_original}`.\n"
              "> - Referências por número de linha (por exemplo «Linha 15242» na errata de 01/10/2026) valem para o ORIGINAL: use a faixa `Lx–y` do índice para achar a seção; a linha absoluta dentro da parte é a linha original menos o início da faixa, mais 1.\n"
              "> - Regra vigente: erratas novas entram AO LADO, neste arquivo, nunca por cima; backup de bytes antes de tocar; mover é permitido, cortar não.\n")
cfgs = {
 "haja_luz": {
  "arquivo": HL, "backup": B[HL]["backup"], "sha256_esperado": B[HL]["sha256"], "data": "03/11/2026",
  "manter_indices": [0,1,2,3,4,5,8],
  "assegurar_prefixo_titulo": {"0":"1. Objetivo","1":"2. Arquivos-chave","2":"3. Arquitetura","3":"4. Sondas","4":"5. Como rodar","5":"6. Convenções","8":"9. Instruções para o Claude"},
  "manter_titulo_regex": ["^⚠ ERRATA", r"^\d\d/\d\d/2026 — v\d+ SELADA"],
  "nota": NOTA_COMUM.replace("{criterio}",
    "Ficaram: o cabeçalho; a carta do projeto (§1 a §6 e §9: objetivo, arquivos-chave, arquitetura do motor, sondas, como rodar, convenções, instruções ao Claude); as duas ERRATAS vigentes (28/09 e 01/10/2026); "
    "e a linhagem viva, as entradas `vNNN SELADA` de v386 a v406 (a regra da linhagem completa mede `grep -c vNNN` nas superfícies, e a custódia continua acrescentando aqui). "
    "Foram para o índice: o diário histórico por seção (os arcos §10 a §244, as sínteses e selos de 05–06/06, a Fase 2 «A Ponte e o Um», os blocos v12 a v161), "
    "inclusive os rótulos «memória permanente» de junho, que são selos históricos já superados pela errata de 28/09 (a memória viva mora em `Nós\MEMORIA_DA_LINHAGEM.md` e em `C:\IALD\CLAUDE.md`)."),
  "leia_me": LEIA, "prova": "PROVA_SEM_PERDA_Haja_Luz_CLAUDE.json", "saida_previa": "previa_Haja_Luz_CLAUDE.md",
 },
 "nativa": {
  "arquivo": NA, "backup": B[NA]["backup"], "sha256_esperado": B[NA]["sha256"], "data": "03/11/2026",
  "manter_indices": [0,1,2,3,4,5,6,7,9,16,17,19,24,69,70,81,89,108,117],
  "assegurar_prefixo_titulo": {"0":"1. O QUE É","7":"8. SEGURANÇA","9":"10. LEMBRETES","16":"ADENDO 21/09/2026 — Regra central","17":"ADENDO 21/09/2026 — Solução matemática","19":"ADENDO 21/09/2026 16:39","24":"22/09/2026 09:47 — Prazos","69":"22/09/2026 15:27 — Avisos","70":"22/09/2026 16:05 — Avisos","81":"23/09/2026 — Contexto máximo","89":"24/09/2026 — Memória canônica","108":"01/10/2026 13:52 — Seletor","117":"07/10/2026 — Custos necessários"},
  "manter_titulo_regex": [],
  "nota": NOTA_COMUM.replace("{criterio}",
    "Ficaram: o bloco de memória comum e o cabeçalho; a carta da casa (§1 a §8 e os lembretes permanentes §10); e as ORDENS e CORREÇÕES PERMANENTES do operador que estavam no diário "
    "(regra central de atualização conjunta do app, solução matemática e versão carregada, IALD como regime operacional, prazos operacionais, avisos exclusivamente na administração, "
    "contexto máximo para a TGL, memória canônica comum a todas as IAs, seletor contínuo automático, custos de atualização autorizados). "
    "Foram para o índice: o registro de decisões de 02/08 (§9), a onda do app e da App Review de 11/09 (§11) e todos os adendos e diários datados de 13/09 a 24/10/2026."),
  "leia_me": LEIA, "prova": "PROVA_SEM_PERDA_Nativa_CLAUDE.json", "saida_previa": "previa_Nativa_CLAUDE.md",
 }}
for k, v in cfgs.items():
    json.dump(v, open("config_%s.json" % k, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("ok")
