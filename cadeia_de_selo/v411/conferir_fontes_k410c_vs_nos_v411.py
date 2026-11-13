# -*- coding: utf-8 -*-
"""conferir_fontes_k410c_vs_nos_v411.py -- (claude-construtor-v411, 12/11/2026) ANTES de copiar o sandbox: confere por sha256 que as FONTES do sandbox de origem C:\\t\\k410c\\final
(todo .lean fora de .lake, a raiz TGLExt.lean, lakefile.toml, lean-toolchain, lake-manifest.json) sao as do kernel do Nos v410 SELADO (so' leitura nos dois). Arquivo que so' existe num
dos dois lados e' listado (nao e' erro por si). Grava CONFERENCIA_FONTES_K410C_v411.json. Nada e' escrito fora desta pasta. Molde: conferir_fontes_k409c_vs_nos_v410.py (so' os rotulos sobem).
A v411 NAO tem modulo novo: o sandbox k411c tem de ser o kernel da v410 byte a byte (DESENHO_v411 secao 1)."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS_K = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
SB = sys.argv[1] if len(sys.argv) > 1 else os.path.join("C:" + os.sep, "t", "k410c", "final")
SAIDA = sys.argv[2] if len(sys.argv) > 2 else "CONFERENCIA_FONTES_K410C_v411.json"
EXTRA = ["TGLExt.lean", "TGL.lean", "lakefile.toml", "lean-toolchain", "lake-manifest.json"]


def fontes(raiz):
    out = {}
    for dp, dn, fn in os.walk(raiz):
        dn[:] = [d for d in dn if d not in (".lake", ".git", "probe")]
        for f in fn:
            if f.endswith(".lean") and ".bak_" not in f:
                p = os.path.join(dp, f)
                out[os.path.relpath(p, raiz).replace(os.sep, "/")] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    for f in EXTRA:
        p = os.path.join(raiz, f)
        if os.path.exists(p):
            out[f] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


a, b = fontes(NOS_K), fontes(SB)
comuns = sorted(set(a) & set(b))
dif = [r for r in comuns if a[r] != b[r]]
so_nos = sorted(set(a) - set(b))
so_sb = sorted(set(b) - set(a))
selo = json.load(open(os.path.join(os.path.dirname(NOS_K), "um_absoluto_selo.json"), encoding="utf-8"))
rep = {"nos_kernel": NOS_K, "sandbox": SB, "selo_um_version": selo.get("um_version"), "n_nos": len(a), "n_sandbox": len(b), "n_comuns": len(comuns), "n_diferentes": len(dif),
       "diferentes": dif[:50], "so_no_nos": so_nos[:50], "so_no_sandbox": so_sb[:50], "todas_as_comuns_iguais": not dif, "todas_as_do_nos_no_sandbox": not so_nos,
       "identico": (not dif and not so_nos and not so_sb)}
p = os.path.join(HERE, SAIDA)
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
print(json.dumps({k: v for k, v in rep.items() if k not in ("diferentes",)}, ensure_ascii=False, indent=1)[:3000])
sys.exit(0 if rep["selo_um_version"] == "v410" and rep["todas_as_comuns_iguais"] and rep["todas_as_do_nos_no_sandbox"] else 1)
