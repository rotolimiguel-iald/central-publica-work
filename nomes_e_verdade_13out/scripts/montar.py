# -*- coding: utf-8 -*-
"""Nomes e Verdade (13/10): monta o sandbox curto C:/t/nm1.
  toolchain/   copia do toolchain elan leanprover--lean4---v4.31.0 (conferida por agregado de sha256)
  src_base/    Palavra e ADENDO1 (dependencias de IALD, sem mudanca), pinadas por sha
  src_old/     as quatro fontes ORIGINAIS pinadas (rank, tempo, IALD r3, identidade r2) = a linha de base
  src_new/     (preenchido depois) Posto, Santo, IALD, Verdade
  out_base/ out_old/ out_new/ meta/   saidas (-o) e leituras de kernel, todas DENTRO do sandbox
LEAN_PATH usa o .lake do Nos SO PARA LEITURA (nada e escrito la). Grava medidas/SANDBOX_MONTAGEM.json."""
import os, sys, shutil, hashlib, json, time, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = "C:/t/nm1"
TC = os.path.expanduser("~/.elan/toolchains/leanprover--lean4---v4.31.0").replace("\\", "/")
W = "C:/IALD/Central de Patentes/work"
BASE = {
    "Palavra.lean": (W + "/organismo_iald_12out/2_CONSTRUCAO/sandbox/TGLExt/Palavra.lean", "33184b49a8bba7e7"),
    "TheSingularityReadsTheAttractorAdendo1.lean": (
        W + "/organismo_iald_12out/2_CONSTRUCAO/sandbox/TGLExt/TheSingularityReadsTheAttractorAdendo1.lean", "433d13c223b03971"),
}
OLD = {
    "TheUnitIsTheRank.lean": (W + "/frequencia_defasa_12out/5_R3/sandbox/TGLExt/TheUnitIsTheRank.lean", "e95775d61db38633"),
    "TheTimeIsNotAPost.lean": (W + "/tempo_santo_12out/5_R2/1_PEDRA/sandbox/TheTimeIsNotAPost.lean", "4d8a82591badd010"),
    "IALD.lean": (W + "/organismo_iald_12out/7_R3_DOCSTRINGS/fonte/TGLExt/IALD.lean", "d7c1f1d3b03e6095"),
    "TheIdentityHasAName.lean": (W + "/identidade_cordeiro_13out/5_R2/pedra/TheIdentityHasAName.lean", "ecae0725b21a98e6"),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def arvore(raiz):
    agg = hashlib.sha256()
    n = 0
    tot = 0
    mapa = {}
    for r, ds, fs in os.walk(raiz):
        ds.sort()
        for f in sorted(fs):
            p = os.path.join(r, f)
            rel = os.path.relpath(p, raiz).replace("\\", "/")
            hs = sha(p)
            mapa[rel] = hs
            n += 1
            tot += os.path.getsize(p)
            agg.update((rel + "|" + hs + "\n").encode())
    return n, tot, agg.hexdigest(), mapa


t0 = time.time()
for sub in ("toolchain", "src_base", "src_old", "src_new", "out_base", "out_old", "out_new", "meta"):
    if os.path.exists(os.path.join(SB, sub)):
        print("FALHA VISIVEL: ja existe " + sub)
        sys.exit(2)
fontes = {}
for grupo, tab in (("base", BASE), ("old", OLD)):
    for nome, (orig, pref) in tab.items():
        h = sha(orig)
        if not h.startswith(pref):
            print("FALHA VISIVEL: sha divergente", nome, h)
            sys.exit(2)
        fontes[grupo + ":" + nome] = {"origem": orig, "sha256": h, "bytes": os.path.getsize(orig), "prefixo_esperado": pref}
shutil.copytree(TC, os.path.join(SB, "toolchain"))
for sub in ("out_base", "out_old", "out_new", "meta", "src_new"):
    os.makedirs(os.path.join(SB, sub))
for grupo, tab in (("base", BASE), ("old", OLD)):
    d0 = os.path.join(SB, "src_" + grupo, "TGLExt")
    os.makedirs(d0)
    for nome, (orig, pref) in tab.items():
        d = os.path.join(d0, nome)
        shutil.copyfile(orig, d)
        if sha(d) != fontes[grupo + ":" + nome]["sha256"]:
            print("FALHA VISIVEL: copia divergente", nome)
            sys.exit(2)
n1, b1, a1, m1 = arvore(TC)
n2, b2, a2, m2 = arvore(os.path.join(SB, "toolchain"))
res = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "sandbox": SB,
       "toolchain": {"origem": TC, "arquivos": n1, "bytes": b1, "agregado_origem": a1, "agregado_copia": a2, "igual": m1 == m2},
       "fontes": fontes, "segundos": round(time.time() - t0, 1),
       "receita_agregado": "sha256 da concatenacao ordenada de 'caminho_relativo|sha256\\n'"}
os.makedirs(os.path.join(AQUI, "medidas"), exist_ok=True)
json.dump(res, open(os.path.join(AQUI, "medidas", "SANDBOX_MONTAGEM.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k != "fontes" else {n: c["sha256"][:16] for n, c in v.items()}) for k, v in res.items()}, ensure_ascii=False, indent=1))
if not res["toolchain"]["igual"]:
    print("FALHA VISIVEL: copia do toolchain nao bate")
    sys.exit(2)
