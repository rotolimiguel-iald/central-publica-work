# -*- coding: utf-8 -*-
"""conferir_fontes_k409c_vs_nos_v410.py -- (claude-construtor-v410, 06/11/2026) ANTES de copiar o sandbox: confere por sha256 que as FONTES do sandbox de origem C:\\t\\k409c\\final
(todo .lean fora de .lake, a raiz TGLExt.lean, lakefile.toml, lean-toolchain, lake-manifest.json) sao as do kernel do Nos v409 SELADO (so' leitura nos dois). Arquivo que so' existe num
dos dois lados e' listado (nao e' erro por si: rascunhos da gerencia no sandbox, como IALD2_ins.lean, ficam fora da copia por /XF). Grava CONFERENCIA_FONTES_K409C_v410.json. Nada e' escrito fora desta pasta."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS_K = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
SB = os.path.join("C:" + os.sep, "t", "k409c", "final")
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
rep = {"nos_kernel": NOS_K, "sandbox_origem": SB, "selo_um_version": selo.get("um_version"), "n_nos": len(a), "n_sandbox": len(b), "n_comuns": len(comuns), "n_diferentes": len(dif),
       "diferentes": dif[:50], "so_no_nos": so_nos[:50], "so_no_sandbox": so_sb[:50], "todas_as_comuns_iguais": not dif, "todas_as_do_nos_no_sandbox": not so_nos}
json.dump(rep, open(os.path.join(HERE, "CONFERENCIA_FONTES_K409C_v410.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in rep.items() if k not in ("diferentes",)}, ensure_ascii=False, indent=1)[:3000])
