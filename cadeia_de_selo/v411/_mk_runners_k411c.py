# -*- coding: utf-8 -*-
"""_mk_runners_k411c.py -- (claude-construtor-v411, 12/11/2026) cria C:\\t\\k411c\\run_build.py e run_pos_treino.py a partir dos da k410c (so' os rotulos 409->410, 410->411). Nao sobrescreve."""
import os, re
SRC = os.path.join("C:" + os.sep, "t", "k410c")
DST = os.path.join("C:" + os.sep, "t", "k411c")
for n in ("run_pos_treino.py", "run_build.py"):
    s = open(os.path.join(SRC, n), "rb").read().decode("utf-8")
    t = re.sub(r"(?<![0-9])(409|410)(?![0-9])", lambda m: str(int(m.group(1)) + 1), s)
    t = t.replace("claude-construtor-v411, a servico da gerencia c1, 06/11/2026", "claude-construtor-v411, a servico da gerencia c1, 12/11/2026")
    assert "410" not in t.replace("v410)", "").replace("k410c", "") or n == "run_pos_treino.py", (n, [l for l in t.splitlines() if "410" in l])
    p = os.path.join(DST, n)
    assert not os.path.exists(p), p
    open(p + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(p + ".tmp") == len(t.encode("utf-8")); os.replace(p + ".tmp", p)
    print(n, len(s), len(t))
