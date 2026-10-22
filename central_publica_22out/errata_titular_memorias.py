# -*- coding: utf-8 -*-
"""ERRATA AO LADO (22/10/2026, em nome próprio da sessão a7 da Central): o depositante dos 16 pedidos, LIDO dos formulários de depósito
do INPI (vault/normalized_docs) e dos recibos do ePCT, é a pessoa física do operador — não a IALD Ltda. A nota entra logo depois das duas
frases «Titular: IALD Ltda.» (TGL_CORE_MEMORY.md e §V do TGL_ATLAS.md); o texto antigo fica como registro; a divergência já anotada no
Atlas (§XI.B/J.6, questão 4 à agente de PI) segue [LEGAL]. Backup de BYTES; temporário; conferência de tamanho; respeita CRLF/LF."""
import os, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vinculo_patentario import ler_vinculos  # noqa: E402

vs = ler_vinculos()
deps = sorted({(v["depositante"], v["tipo_de_pessoa"]) for v in vs})
reqs = sorted({v["pct_requerente"] for v in vs if v["pct_requerente"]})
assert len(deps) == 1, deps
NOTA = ("> ⚠ **ERRATA AO LADO (22/10/2026, em nome próprio da sessão a7 da Central; o texto acima fica como registro):** lido dos %d "
        "formulários de depósito do INPI (texto extraído no cofre) e dos recibos do ePCT, o **depositante de registro é %s, %s** (o inventor, "
        "o mesmo); o requerente nos PCT, como a OMPI o escreve: %s. A palavra do operador no mesmo dia: «patente é minha, Luiz Antonio "
        "Rotoli Miguel». A divergência com «titular IALD Ltda.» já anotada no §XI.B/J.6 (questão 4 à agente de PI) segue [LEGAL]. "
        "<!-- errata_titular_pessoa_fisica_22out -->" % (len(vs), deps[0][0], deps[0][1].lower(), "; ".join(reqs)))
ALVOS = [(Path(r"C:\IALD\Central de Patentes\memory\TGL_CORE_MEMORY.md"),
          "**Titular:** IALD Ltda. (CNPJ 62.757.606/0001-23, Goiânia/GO) — Luiz Antonio Rotoli Miguel\n(ORCID 0009-0005-1114-6106). PT-BR na interação e documentação; inglês no código.\n"),
         (Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md"),
          "> **Titular:** IALD Ltda. (CNPJ 62.757.606/0001-23) · **Inventor:** Luiz Antonio Rotoli Miguel.\n")]
TS = time.strftime("%Y%m%d_%H%M%S")
for p, ancora in ALVOS:
    raw = p.read_bytes()
    s = raw.decode("utf-8")
    if "errata_titular_pessoa_fisica_22out" in s:
        print("já aplicado:", p.name); continue
    crlf = "\r\n" in s[:20000]
    a = ancora.replace("\n", "\r\n") if crlf else ancora
    assert s.count(a) == 1, (p.name, s.count(a))
    nl = "\r\n" if crlf else "\n"
    if p.name == "TGL_ATLAS.md":
        novo = a + "> " + nl + NOTA + nl          # dentro do bloco de citação do cabeçalho do §V
    else:
        novo = a + nl + NOTA + nl
    s2 = s.replace(a, novo, 1)
    bak = p.with_name(p.name + ".bak_" + TS)
    bak.write_bytes(raw)
    assert bak.stat().st_size == len(raw)
    t = p.with_name(p.name + ".tmp_errata")
    t.write_bytes(s2.encode("utf-8"))
    assert t.stat().st_size > len(raw)
    os.replace(t, p)
    print("ok", p.name, len(raw), "->", p.stat().st_size, "| backup", bak.name)
