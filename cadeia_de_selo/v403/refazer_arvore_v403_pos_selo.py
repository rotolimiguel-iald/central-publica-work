# -*- coding: utf-8 -*-
"""refaz C:/t/k403c/arvore (so-fontes) a partir do kernel v403 que o Nos tem (LEITURA do Nos), como pos_build_kernel_v403.py a fez; confere os sha contra kernel/KERNEL_RECIBO_v403.json. Nao muda o recibo.
Escrito em 24/10/2026 (NAO executado na preparacao). Molde: refazer_arvore_v402_pos_selo.py."""
import hashlib, json, os, shutil, sys
H = os.path.dirname(os.path.abspath(__file__))
NK = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"; ARV = r"C:\t\k403c\arvore"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
R = json.load(open(os.path.join(H, "kernel", "KERNEL_RECIBO_v403.json"), encoding="utf-8"))
assert os.path.normpath(R["arvore"]) == os.path.normpath(ARV)
if os.path.isdir(ARV): shutil.rmtree(ARV)
os.makedirs(ARV)
for rel in ("TGL", "TGLExt"): shutil.copytree(os.path.join(NK, rel), os.path.join(ARV, rel), copy_function=shutil.copy2)
for f in os.listdir(NK):
    p = os.path.join(NK, f)
    if os.path.isfile(p) and not f.startswith("TGLExt.lean.bak"): shutil.copy2(p, os.path.join(ARV, f))
bad = []
def chk(n, a, b):
    if a != b: bad.append((n, a, b))
chk("raiz", sha(os.path.join(ARV, "TGLExt.lean")), R["raiz"]["sha256_depois"]); chk("raiz==Nos", sha(os.path.join(NK, "TGLExt.lean")), R["raiz"]["sha256_depois"])
chk("audit", sha(os.path.join(ARV, "TGL", "Audit.lean")), R["audit"]["sha256_depois"]); chk("audit==Nos", sha(os.path.join(NK, "TGL", "Audit.lean")), R["audit"]["sha256_depois"])
for p in R["pedras"]:
    chk(p["path"], sha(os.path.join(ARV, *p["path"].split("/"))), p["sha256"]); chk(p["path"] + " Nos", sha(os.path.join(NK, *p["path"].split("/"))), p["sha256"])
n = no = 0; links = []
for d, ds, fs in os.walk(ARV):
    for x in ds + fs:
        if os.path.islink(os.path.join(d, x)): links.append(x)
    for f in fs:
        if f.lower().endswith(".lean"):
            n += 1; no += os.path.relpath(os.path.join(d, f), ARV).replace("\\", "/").startswith("TGLExt/O16/")
chk("n_lean", n, R["varredura_tokens"]["arquivos_lean"]); chk("n_o16", no, R["varredura_tokens"]["arquivos_lean_em_TGLExt_O16"]); chk("links", links, [])
print(json.dumps({"ok": not bad, "pedras": len(R["pedras"]), "n_lean": n, "n_o16": no, "divergencias": bad}, ensure_ascii=False)); sys.exit(1 if bad else 0)
