# -*- coding: utf-8 -*-
"""_desfazer_dicionario_v408.py -- (claude-construtor-v408, 04/11/2026) a MUDANCA DE INSUMO da gerencia (04/11 tarde: o 4o modulo e' PIgualNP, nao Dicionario) chegou DEPOIS de o preparar_bundle_v408 ter gravado o Dicionario no sandbox C:\\t\\k408c\\final
e de o kernel ter sido construido com ele. Este script DESFAZ, com BACKUP DE BYTES de tudo o que toca (nada e' apagado sem copia): (1) TGLExt/Dicionario.lean sai do sandbox (vai para C:\\t\\k408c\\superado_dicionario_<TS>\\), com os artefatos do build dele em .lake/build;
(2) a raiz TGLExt.lean do sandbox volta a ser a do Nos v407 (os bytes do Nos, so' lidos), guardando a raiz com o import do Dicionario em .bak; (3) em v408\\: pedra\\Dicionario.lean e pedra\\origem\\Dicionario.lean vao para pedra\\superado_dicionario_<TS>\\;
kernel_modulos_novos_v408.json e BUNDLE_v408.json ganham .bak_<TS>_dicionario e sao removidos (o preparar_bundle os regrava); kernel\\ (logs e marcas do build com o Dicionario) vai para kernel\\superado_dicionario_<TS>\\. Grava RECIBO_DESFAZER_DICIONARIO_v408.json. Nunca toca o Nos.
Uso: python -I -B -X utf8 _desfazer_dicionario_v408.py"""
import datetime, hashlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
K8 = os.path.join("C:" + os.sep, "t", "k408c", "final")
SUP = os.path.join("C:" + os.sep, "t", "k408c", "superado_dicionario_" + TS)
NOS_RAIZ = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel", "TGLExt.lean")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rec = {"quando": TS, "movidos": [], "backups": [], "raiz": {}}


def mover(src, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(src))
    assert not os.path.exists(dst), dst
    h = sha(src); shutil.copy2(src, dst); assert sha(dst) == h; os.remove(src)
    rec["movidos"].append({"de": src, "para": dst, "sha256": h})


# (1) o modulo e os artefatos do build dele
p = os.path.join(K8, "TGLExt", "Dicionario.lean")
assert os.path.exists(p), "o sandbox nao tem TGLExt/Dicionario.lean: nada a desfazer?"
mover(p, os.path.join(SUP, "TGLExt"))
for sub in (os.path.join(".lake", "build", "lib", "lean", "TGLExt"), os.path.join(".lake", "build", "ir", "TGLExt")):
    d = os.path.join(K8, sub)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.startswith("Dicionario.") or f == "Dicionario":
                q = os.path.join(d, f)
                if os.path.isfile(q):
                    mover(q, os.path.join(SUP, sub))
# (2) a raiz volta a ser a do Nos
raiz_nos = open(NOS_RAIZ, "rb").read()
raiz_k8 = open(os.path.join(K8, "TGLExt.lean"), "rb").read()
assert raiz_k8 != raiz_nos and raiz_k8.startswith(raiz_nos) and b"import TGLExt.Dicionario" in raiz_k8, "a raiz do sandbox nao e' a do Nos + os imports do preparo com o Dicionario"
bak = os.path.join(K8, "TGLExt.lean.bak_%s_com_dicionario" % TS)
open(bak, "wb").write(raiz_k8); assert open(bak, "rb").read() == raiz_k8; rec["backups"].append(bak)
tmp = os.path.join(K8, "TGLExt.lean.tmp"); open(tmp, "wb").write(raiz_nos); assert os.path.getsize(tmp) == len(raiz_nos); os.replace(tmp, os.path.join(K8, "TGLExt.lean"))
assert open(os.path.join(K8, "TGLExt.lean"), "rb").read() == raiz_nos
rec["raiz"] = {"antes_sha256": hashlib.sha256(raiz_k8).hexdigest(), "depois_sha256": hashlib.sha256(raiz_nos).hexdigest(), "igual_ao_nos": True}
# (3) a pasta v408
for rel in (os.path.join("pedra", "Dicionario.lean"), os.path.join("pedra", "origem", "Dicionario.lean")):
    q = os.path.join(HERE, rel)
    if os.path.exists(q):
        mover(q, os.path.join(HERE, "pedra", "superado_dicionario_" + TS, os.path.dirname(rel).replace("pedra", "").strip(os.sep)))
for nome in ("kernel_modulos_novos_v408.json", "BUNDLE_v408.json"):
    q = os.path.join(HERE, nome)
    if os.path.exists(q):
        b = q + ".bak_%s_dicionario" % TS; shutil.copy2(q, b); assert sha(b) == sha(q); rec["backups"].append(b); os.remove(q)
kd = os.path.join(HERE, "kernel")
if os.path.isdir(kd):
    dst = os.path.join(kd, "superado_dicionario_" + TS); os.makedirs(dst)
    for f in sorted(os.listdir(kd)):
        q = os.path.join(kd, f)
        if os.path.isfile(q):
            mover(q, dst)
json.dump(rec, open(os.path.join(HERE, "RECIBO_DESFAZER_DICIONARIO_v408_%s.json" % TS), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("desfeito:", len(rec["movidos"]), "arquivos movidos;", len(rec["backups"]), "backups; raiz do sandbox == Nos:", rec["raiz"]["igual_ao_nos"])
