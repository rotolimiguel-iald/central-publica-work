# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] pos-selo: refaz C:/t/k411c/arvore a partir do Nos v411 e confere contra KERNEL_RECIBO_v411.json; a v411 NAO tem modulo novo (R['pedras'] e' VAZIA: so' a raiz, o Audit e as contagens sao conferidos); NAO executado na preparacao
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] pos-selo: refaz C:/t/k410c/arvore a partir do Nos v410 e confere contra KERNEL_RECIBO_v410.json (o corpo le tudo do recibo; NAO executado na preparacao); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
"""refaz C:/t/k411c/arvore (so-fontes) a partir do kernel v411 que o Nos tem (LEITURA do Nos), como pos_build_kernel_v411.py a fez; confere os sha contra kernel/KERNEL_RECIBO_v411.json: a raiz TGLExt.lean, o TGL/Audit.lean, os modulos novos em TGLExt/ (R["pedras"]: path e sha256, um por um, na arvore refeita E no Nos; na v411 a lista e' VAZIA: nenhum modulo novo) e as contagens de arquivos .lean (R["varredura_tokens"]). Nao muda o recibo.
POS-SELO: so' roda DEPOIS de a v411 estar no Nos (o instalador copia o candidato e o rito materializa os modulos); ANTES disso o Nos ainda e' a v410 e a conferencia reprova (e e' o que tem de acontecer: fail-closed). ATENCAO: apaga e refaz C:/t/k411c/arvore (shutil.rmtree); por isso NAO foi executado na preparacao -- a conferencia equivalente (as mesmas contagens e os mesmos sha contra a arvore ja' existente) foi feita so' por leitura em 06/11/2026 (pos_build_kernel_v411.py e p00).
Molde escrito em 24/10/2026 (refazer_arvore_v39x_pos_selo.py), adaptado a v411 em 06/11/2026 (claude-construtor-v411, fork B). Molde direto: refazer_arvore_v410_pos_selo.py."""
import hashlib, json, os, shutil, sys
H = os.path.dirname(os.path.abspath(__file__))
NK = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"; ARV = r"C:\t\k411c\arvore"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
R = json.load(open(os.path.join(H, "kernel", "KERNEL_RECIBO_v411.json"), encoding="utf-8"))
SANDBOX = r"C:\t\k411c\final"   # (v411) o recibo do kernel da v411 aponta a arvore para o SANDBOX (o pos_build_kernel_v411.py nao refaz a copia so-fontes): ela e' so' conferida, NUNCA apagada
_n_ = lambda p_: os.path.normcase(os.path.normpath(p_))
assert _n_(R["arvore"]) in (_n_(ARV), _n_(SANDBOX)) and _n_(ARV) != _n_(SANDBOX) and R["pedras"] == [], ("o recibo da v411 (nenhum modulo novo) nao aponta a arvore esperada", R["arvore"])
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
_vt = R.get("varredura_tokens")
if _vt:
    chk("n_lean", n, _vt["arquivos_lean"]); chk("n_o16", no, _vt["arquivos_lean_em_TGLExt_O16"])
else:   # (v411) o recibo da v411 nao traz varredura_tokens: as contagens sao conferidas contra as FONTES do sandbox medido (sem .lake), so' lidas
    nsb = nosb = 0
    for d, ds, fs in os.walk(SANDBOX):
        ds[:] = [x for x in ds if x != ".lake"]
        for f in fs:
            if f.lower().endswith(".lean") and os.path.relpath(os.path.join(d, f), SANDBOX).replace("\\", "/").split("/")[0] in ("TGL", "TGLExt", "TGLExt.lean", "TGL.lean"):
                nsb += 1; nosb += os.path.relpath(os.path.join(d, f), SANDBOX).replace("\\", "/").startswith("TGLExt/O16/")
    chk("n_lean==sandbox", n - sum(1 for f in os.listdir(ARV) if f.lower().endswith(".lean") and f not in ("TGLExt.lean", "TGL.lean")), nsb); chk("n_o16==sandbox", no, nosb)
chk("links", links, [])
print(json.dumps({"ok": not bad, "pedras": len(R["pedras"]), "n_lean": n, "n_o16": no, "divergencias": bad}, ensure_ascii=False)); sys.exit(1 if bad else 0)
