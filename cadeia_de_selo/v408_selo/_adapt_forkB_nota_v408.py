# -*- coding: utf-8 -*-
"""_adapt_forkB_nota_v408.py -- (claude-construtor-v408, fork B, 04/11/2026) corrige, por troca de CONTAGEM EXATA, a data DUPLICADA que _adapt_forkB_pequenos_v408.py deixou na nota de cabecalho de cinco arquivos
(«# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B), 04/11/2026]» -> «# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B)]»). Backup de bytes, temporario -> conferir -> substituir, ast.parse / sh -n, fim de linha preservado. Escrito pelo Write."""
import ast, hashlib, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
A = "# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B), 04/11/2026]"; B = "# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B)]"
for nome in ("fila_memoria_v408.py", "b3_recibo_v408.py", "superficies_v408.py", "gerar_derivacao_pos_rito_v408.py", "chain_pos_rito_v408.sh"):
    p = os.path.join(HERE, nome); raw = open(p, "rb").read(); t = raw.decode("utf-8")
    assert t.count(A) == 1, (nome, t.count(A))
    t = t.replace(A, B); novo = t.encode("utf-8")
    if nome.endswith(".py"):
        ast.parse(t)
    bak = p + ".bak_" + TS + "_adapt"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    tmp = p + ".tmp_adapt"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, p); assert open(p, "rb").read() == novo
    if nome.endswith(".sh"):
        r = subprocess.run(["sh", "-n", p], capture_output=True, text=True); assert r.returncode == 0, r.stderr
    print("%-36s %d -> %d B sha16 %s (backup %s)" % (nome, len(raw), len(novo), hashlib.sha256(novo).hexdigest()[:16], os.path.basename(bak)))
