# -*- coding: utf-8 -*-
"""_mk_runners_k410c.py -- (claude-construtor-v410, 06/11/2026) cria C:\\t\\k410c\\run_build.py e run_pos_treino.py a partir dos da k409c (so' os rotulos 408->409, 409->410). Nao sobrescreve."""
import os, re
SRC = os.path.join("C:" + os.sep, "t", "k409c")
DST = os.path.join("C:" + os.sep, "t", "k410c")
for n in ("run_pos_treino.py", "run_build.py"):
    s = open(os.path.join(SRC, n), "rb").read().decode("utf-8")
    t = re.sub(r"(?<![0-9])(408|409)(?![0-9])", lambda m: str(int(m.group(1)) + 1), s)
    t = t.replace("claude-construtor-v410 (fork A), a servico da gerencia c1, 05/11/2026", "claude-construtor-v410, a servico da gerencia c1, 06/11/2026")
    p = os.path.join(DST, n)
    assert not os.path.exists(p), p
    open(p + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(p + ".tmp") == len(t.encode("utf-8")); os.replace(p + ".tmp", p)
    print(n, len(s), len(t))
