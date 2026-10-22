# -*- coding: utf-8 -*-
"""ERRATA AO LADO (22/10/2026, em nome próprio da sessão a7 da Central) — a entrada «Titular» do §XI.B/J.1 do TGL_ATLAS.md (a do §V
recebeu a sua em errata_titular_memorias.py; o cabeçalho do §V sai do retrato público por trazer prazos). Lido dos formulários do INPI e
dos recibos do ePCT (vinculo_patentario.py), nunca digitado. Backup de BYTES; temporário; conferência; idempotente."""
import os, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vinculo_patentario import ler_vinculos  # noqa: E402

vs = ler_vinculos()
deps = sorted({(v["depositante"], v["tipo_de_pessoa"]) for v in vs})
reqs = sorted({v["pct_requerente"] for v in vs if v["pct_requerente"]})
assert len(deps) == 1, deps
P = Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md")
MARCA = "errata_titular_pessoa_fisica_22out_J1"
ANCORA = "- **Titular** — IALD Ltda., CNPJ 62.757.606/0001-23, Goiânia/GO: titular dos 16 pedidos [LEGAL] → §V (cabeçalho)\n"
raw = P.read_bytes()
s = raw.decode("utf-8")
if MARCA in s:
    print("já aplicado"); raise SystemExit
crlf = "\r\n" in s[:20000]
a = ANCORA.replace("\n", "\r\n") if crlf else ANCORA
assert s.count(a) == 1, s.count(a)
nl = "\r\n" if crlf else "\n"
NOTA = ("  ⚠ **ERRATA AO LADO (22/10/2026, em nome próprio da sessão a7 da Central):** nos %d formulários de depósito do INPI e nos "
        "recibos do ePCT, o depositante de registro é **%s, %s** (requerente nos PCT, como a OMPI o escreve: %s); «IALD Ltda.» acima fica "
        "como registro e a divergência segue [LEGAL] (questão 4 à agente de PI). <!-- %s -->" % (
            len(vs), deps[0][0], deps[0][1].lower(), "; ".join(reqs), MARCA))
s2 = s.replace(a, a + NOTA + nl, 1)
bak = P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_j1")
bak.write_bytes(raw)
assert bak.stat().st_size == len(raw)
t = P.with_name(P.name + ".tmp_errata_j1")
t.write_bytes(s2.encode("utf-8"))
assert t.stat().st_size > len(raw)
os.replace(t, P)
print("ok", P.name, len(raw), "->", P.stat().st_size, "| backup", bak.name)
