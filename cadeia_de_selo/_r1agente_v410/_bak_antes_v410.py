# -*- coding: utf-8 -*-
"""_bak_antes_v410.py -- (claude-construtor-v410, 06/11/2026) backup de BYTES <arquivo>.bak_<ts> na mesma pasta ANTES de reescrever cada arquivo dado (regra do backup imediato). Uso: python _bak_antes_v410.py arq1 arq2 ..."""
import datetime, os, sys
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
for p in sys.argv[1:]:
    b = open(p, "rb").read(); bk = p + ".bak_" + ts
    open(bk, "wb").write(b); assert open(bk, "rb").read() == b
    print(p, "->", os.path.basename(bk), len(b))
