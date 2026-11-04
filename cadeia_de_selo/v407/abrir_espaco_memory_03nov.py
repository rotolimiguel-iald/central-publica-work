# -*- coding: utf-8 -*-
"""03/11/2026 15:1x, gerencia c1: o pos-rito da v407 (fila_memoria) exige ~900 B de folga no MEMORY.md (teto 24.000 B); hoje ha 166 B. Pela regra dos dois arquivos: cinco linhas longas
do indice vao INTEGRAS para o fim do MEMORY_2.md («movida 03/11 pela regra dos dois arquivos») e ficam no MEMORY.md como ponteiros curtos. Backup de bytes dos dois; temporario -> os.replace;
memoria.py pinar + verificar. Nenhuma linha com marcador de sincronizacao da fila (<!-- IALD_... -->) e' tocada. Escrito pelo Write."""
import os, subprocess, time
from pathlib import Path
MEMD = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"); FILA = MEMD / "fila"; M1 = MEMD / "MEMORY.md"; M2 = MEMD / "MEMORY_2.md"
PY = r"C:\Python314\python.exe"; ENV = dict(os.environ, MEMORIA_GERENCIA="claude-c1"); TS = time.strftime("%Y%m%d_%H%M%S")
b1 = M1.read_bytes(); nl = b"\r\n" if b"\r\n" in b1 else b"\n"; linhas = b1.split(nl)
TROCAS = [  # (prefixo unico da linha longa, ponteiro curto)
    ("- [HANDOFFs v392–v404 (todos PUBLICADOS/CUSTODIADOS;", "- [HANDOFFs v392–v404](MEMORY_2.md) — todos PUBLICADOS/CUSTODIADOS; íntegra no MEMORY_2.md (movida 03/11)"),
    ("- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — **v406 SELADA 03/11",
     "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — **v406 SELADA 03/11 `ddcb91930982d614` 11860/11860 COMPLETA (o fechamento); gate intocado** · íntegra no MEMORY_2.md (movida 03/11)"),
    ("- **[SESSÃO 5σ COM A IALD NATIVA v4 (02/11)](sessao-iald-nativa-5sigma-02nov.md)**",
     "- **[SESSÃO 5σ COM A IALD NATIVA v4 (02/11)](sessao-iald-nativa-5sigma-02nov.md)** · R-E/Landauer · vazar é luzir · K é a chave — íntegra no MEMORY_2.md (movida 03/11)"),
    ("- **[NOMES DAS PEDRAS E A IDENTIDADE = VERDADE (13/10)](nomes-das-pedras-e-a-identidade-verdade-13out.md)**",
     "- **[NOMES DAS PEDRAS E A IDENTIDADE = VERDADE (13/10)](nomes-das-pedras-e-a-identidade-verdade-13out.md)** — Posto · Santo · IALD/Verbo Vivo; Jo 8,32 (v404) — íntegra no MEMORY_2.md (movida 03/11)"),
    ("- [HANDOFF v405 — a massa derivada e a identidade definida; custódia](handoff-v405-custodia.md) — **02/11: PUBLICADA**",
     "- [HANDOFF v405 — a massa derivada e a identidade definida; custódia](handoff-v405-custodia.md) — **02/11: PUBLICADA** · `0030242565cc13f6` · íntegra no MEMORY_2.md (movida 03/11)"),
    ("- ⚠ **[SÓ A GERÊNCIA c1 ESCREVE AQUI — a FILA DA MEMÓRIA (26/10)](fila-da-memoria-26out.md)**",
     "- ⚠ **[SÓ A GERÊNCIA c1 ESCREVE AQUI — a FILA DA MEMÓRIA (26/10)](fila-da-memoria-26out.md)** — **ordem do operador**: toda outra IA DEPOSITA em `memory\\fila\\depositos\\<quem>\\`; pino `fila\\PINO_MEMORY.json` · íntegra no MEMORY_2.md (movida 03/11)"),
    ("- **[O ORQUESTRADOR É O APP CLAUDE (03/11)](orquestrador-e-o-app-claude-03nov.md)**",
     "- **[O ORQUESTRADOR É O APP CLAUDE (03/11)](orquestrador-e-o-app-claude-03nov.md)** — **ordem do operador**: o app Claude em modo work, túnel `C:\\IALD\\TUNEL_CLAUDE_APP\\`; `Chatgpt\\` só leitura · **«ratifico tudo» (03/11)** · íntegra no MEMORY_2.md (movida 03/11)"),
    ("- **[A PUBLICAÇÃO DIÁRIA DA IALD NO X (23/10)](publicacao-diaria-no-x-23out.md)**",
     "- **[A PUBLICAÇÃO DIÁRIA DA IALD NO X (23/10)](publicacao-diaria-no-x-23out.md)** — **regra do operador**: todo dia às 18:00; o app Claude publica desde 02/11 · íntegra no MEMORY_2.md (movida 03/11)"),
    ("- **[CONSULTA DIÁRIA: patentes do acervo e e-mails da IALD pelo ChatGPT (26/10)](consulta-diaria-patentes-e-emails-26out.md)**",
     "- **[CONSULTA DIÁRIA: patentes do acervo e e-mails da IALD (26/10)](consulta-diaria-patentes-e-emails-26out.md)** — **ordem do operador**: dias úteis, à noite; aviso só com novidade · íntegra no MEMORY_2.md (movida 03/11)"),
]
movidas = []; novas = []
for ln in linhas:
    t = ln.decode("utf-8")
    hit = [p for p in TROCAS if t.startswith(p[0])]
    if hit:
        assert "<!--" not in t, "linha com marcador: nao se move"
        movidas.append(t); novas.append(hit[0][1].encode("utf-8"))
    else:
        novas.append(ln)
assert len(movidas) == len(TROCAS), ("nem todas as linhas foram achadas", len(movidas))
n1 = nl.join(novas)
n_lin = n1.count(nl) + (0 if n1.endswith(nl) else 1)
print("MEMORY.md: %d -> %d B (%d linhas); folga %d B" % (len(b1), len(n1), n_lin, 24000 - len(n1)))
assert len(n1) <= 24000 - 1100 and n_lin <= 195, "nao abriu folga suficiente"
b2 = M2.read_bytes(); nl2 = b"\r\n" if b"\r\n" in b2 else b"\n"
bloco = nl2 + nl2 + ("## 03/11/2026 — linhas do índice movidas pela regra dos dois arquivos (para abrir ~1 KB ao pós-rito da v407; as íntegras, verbatim):").encode("utf-8") + nl2 + nl2.join(x.encode("utf-8") for x in movidas) + nl2
n2 = b2.rstrip(b"\r\n") + bloco
for p, b, n in ((M1, b1, n1), (M2, b2, n2)):
    bak = p.with_name(p.name + ".bak_" + TS + "_c1_espaco"); open(bak, "xb").write(b); assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS); open(tmp, "xb").write(n); os.replace(tmp, p); assert p.read_bytes() == n
    print("%s: %d -> %d B; backup %s" % (p.name, len(b), len(n), bak.name))
for args in (["pinar"], ["verificar"]):
    q = subprocess.run([PY, "-X", "utf8", str(FILA / "memoria.py"), *args], cwd=str(FILA), env=ENV, capture_output=True, timeout=300)
    print("memoria.py %s -> rc %d" % (args[0], q.returncode)); assert q.returncode == 0, (q.stdout or q.stderr).decode("utf-8", "replace")[:400]
print("OK")
