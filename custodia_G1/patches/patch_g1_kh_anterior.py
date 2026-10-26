# -*- coding: utf-8 -*-
"""G1 (25/10/2026, gerência a7, custódia v401): a cobertura do kernel da ANTERIOR. A v400 não trouxe registro `kh_n1_cobertura_v400` (o kernel
não mudou: o registro vigente era o da v399). O patch da custódia conjunta só tratava a versão corrente; na v401, `kh_de(coreB, "v400")` voltou
None e o C4 (a pedra genérica) quebrou ao comparar 29318 >= None. Agora, sem registro próprio da anterior, vale o registro MAIS NOVO até ela
no core da anterior (aqui, `kh_n1_cobertura_v399`), e os fatos dizem qual (`kh_registro_anterior`). Trocas contadas; backup de bytes;
py_compile. Rodar só com o G1 parado."""
import os, py_compile, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\fatos.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
CR, LF = chr(13), chr(10)
NL = CR + LF if (CR + LF) in s else LF
if "kh_reg_ant" in s:
    raise SystemExit("já aplicado")
pares = [
    ('''    khcB, khtB = kh_de(coreB, ant)
''', '''    khcB, khtB = kh_de(coreB, ant)
    kh_reg_ant = "kh_n1_cobertura_" + ant
    if khcB is None:                      # 25/10/2026: a anterior não trouxe kh próprio (a v400): o registro mais novo até ela, no core dela
        kk = _mais_novo_entre(coreB, "kh_n1_cobertura_", "v0", ant)
        if kk:
            khcB, khtB = kh_de(coreB, kk[len("kh_n1_cobertura_"):])
            kh_reg_ant = kk
'''),
    ('''        "kh_registro": kh_reg,
''', '''        "kh_registro": kh_reg,
        "kh_registro_anterior": kh_reg_ant,
'''),
]
for a, b in pares:
    a, b = a.replace(LF, NL), b.replace(LF, NL)
    n = s.count(a)
    assert n == 1, (a[:70], n)
    s = s.replace(a, b)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("fatos.py: kh da anterior pelo registro mais novo até ela | %d -> %d" % (len(raw), P.stat().st_size))
