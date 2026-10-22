# -*- coding: utf-8 -*-
"""Monta o sandbox curto C:/t/mo2 da rodada 2 (pedra TGLExt.IALD r2):
  toolchain/  = copia do toolchain elan leanprover--lean4---v4.31.0 (byte a byte)
  ov/         = copia verificada de tgl_kernel/.lake/build/lib/lean do Nos (SO LEITURA na origem)
  src/TGLExt/ = fontes das candidatas (Palavra, ADENDO1, TheUnitIsTheRank r3, TheTimeIsNotAPost) conferidas por sha256
Motivo da sobreposicao (medido na F_KERNEL de 12/10 e repetido na construcao): o lean resolve a raiz TGLExt na
PRIMEIRA pasta do LEAN_PATH que a contem; as candidatas nao instaladas tem de morar na mesma raiz que o kernel.
Nada e escrito na origem. Grava medidas/SANDBOX_MONTAGEM.json.
Uso: montar_sandbox.py"""
import os, sys, shutil, hashlib, json, time, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = "C:/t/mo2"
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel"
SRC_OV = NOS + "/.lake/build/lib/lean"
TC = os.path.expanduser("~/.elan/toolchains/leanprover--lean4---v4.31.0").replace("\\", "/")
W = "C:/IALD/Central de Patentes/work"
CAND = {
    "Palavra.lean": (W + "/organismo_iald_12out/2_CONSTRUCAO/sandbox/TGLExt/Palavra.lean", "33184b49a8bba7e7"),
    "TheSingularityReadsTheAttractorAdendo1.lean": (
        W + "/organismo_iald_12out/2_CONSTRUCAO/sandbox/TGLExt/TheSingularityReadsTheAttractorAdendo1.lean",
        "433d13c223b03971"),
    "TheUnitIsTheRank.lean": (W + "/frequencia_defasa_12out/5_R3/sandbox/TGLExt/TheUnitIsTheRank.lean", "e95775d61db38633"),
    "TheTimeIsNotAPost.lean": (W + "/tempo_santo_12out/5_R2/1_PEDRA/sandbox/TheTimeIsNotAPost.lean", "4d8a82591badd010"),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def arvore(raiz):
    agg = hashlib.sha256(); n = 0; tot = 0; mapa = {}
    for r, ds, fs in os.walk(raiz):
        ds.sort()
        for f in sorted(fs):
            p = os.path.join(r, f); rel = os.path.relpath(p, raiz).replace("\\", "/")
            hs = sha(p); mapa[rel] = hs; n += 1; tot += os.path.getsize(p)
            agg.update((rel + "|" + hs + "\n").encode())
    return n, tot, agg.hexdigest(), mapa


t0 = time.time()
for sub in ("toolchain", "ov", "src"):
    if os.path.exists(os.path.join(SB, sub)):
        print("FALHA VISIVEL: ja existe " + sub); sys.exit(2)
# 1. candidatas: conferir sha ANTES de copiar
cand = {}
for nome, (orig, pref) in CAND.items():
    h = sha(orig)
    if not h.startswith(pref):
        print("FALHA VISIVEL: sha divergente", nome, h); sys.exit(2)
    cand[nome] = {"origem": orig, "sha256": h, "bytes": os.path.getsize(orig), "prefixo_esperado": pref}
# 2. copias
shutil.copytree(TC, os.path.join(SB, "toolchain"))
shutil.copytree(SRC_OV, os.path.join(SB, "ov"))
os.makedirs(os.path.join(SB, "src", "TGLExt"))
for nome, (orig, pref) in CAND.items():
    d = os.path.join(SB, "src", "TGLExt", nome)
    shutil.copyfile(orig, d)
    if sha(d) != cand[nome]["sha256"]:
        print("FALHA VISIVEL: copia divergente", nome); sys.exit(2)
# 3. verificacao byte a byte das duas arvores
n1, b1, a1, m1 = arvore(TC); n2, b2, a2, m2 = arvore(os.path.join(SB, "toolchain"))
o1, ob1, oa1, om1 = arvore(SRC_OV); o2, ob2, oa2, om2 = arvore(os.path.join(SB, "ov"))
res = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "sandbox": SB,
       "toolchain": {"origem": TC, "arquivos": n1, "bytes": b1, "agregado_origem": a1, "agregado_copia": a2,
                     "igual": m1 == m2},
       "ov": {"origem": SRC_OV, "arquivos": o1, "bytes": ob1, "agregado_origem": oa1, "agregado_copia": oa2,
              "igual": om1 == om2},
       "candidatas": cand, "segundos": round(time.time() - t0, 1),
       "receita_agregado": "sha256 da concatenacao ordenada de 'caminho_relativo|sha256\\n'"}
os.makedirs(os.path.join(AQUI, "medidas"), exist_ok=True)
json.dump(res, open(os.path.join(AQUI, "medidas", "SANDBOX_MONTAGEM.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k != "candidatas" else {n: c["sha256"][:16] for n, c in v.items()}) for k, v in res.items()},
                 ensure_ascii=False, indent=1))
if not (res["toolchain"]["igual"] and res["ov"]["igual"]):
    print("FALHA VISIVEL: copia nao bate"); sys.exit(2)
