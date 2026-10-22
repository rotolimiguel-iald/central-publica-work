# -*- coding: utf-8 -*-
"""Prepara o sandbox C:/t/id2 para a AUDITORIA da r2 (nao para compilar a pedra, que compila sem sobreposicao):
(1) copia r1 para src/IdR1/TheIdentityHasAName_r1.lean trocando SO o namespace (TGLExt.TheIdentityHasAName ->
    TGLExt.TheIdentityHasAName_r1), para que r1 e r2 convivam num ambiente e a tabela r1->r2 compare os tipos compilados;
(2) monta a sobreposicao C:/t/id2/ov: COPIA (bytes) de cada .olean do TGLExt do Nos + o TGLExt.olean raiz, conferida
    por sha256 origem = destino (o Lean resolve o pacote TGLExt pela primeira entrada do LEAN_PATH que tem a pasta).
Grava logs/PREPARO_SANDBOX.json. Uso: preparar_sandbox_r2.py"""
import os, json, hashlib, shutil
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.dirname(R2)
LOGS = os.path.join(R2, "logs")
KB = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel/.lake/build/lib/lean"
OV = "C:/t/id2/ov"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


r1 = os.path.join(W, "3_PEDRA", "pedra", "TheIdentityHasAName.lean")
b = open(r1, "rb").read()
assert hashlib.sha256(b).hexdigest() == "1b68316aecf6cdc62a1c7eba0927a4976d6ddae9d840fd87c7880a4c36890262"
t = b.decode("utf-8")
n_ocorr = t.count("TGLExt.TheIdentityHasAName")
t2 = t.replace("TGLExt.TheIdentityHasAName", "TGLExt.TheIdentityHasAName_r1")
dst = "C:/t/id2/src/IdR1/TheIdentityHasAName_r1.lean"
os.makedirs(os.path.dirname(dst), exist_ok=True)
open(dst, "wb").write(t2.encode("utf-8"))
# conferencia: desfazer a troca devolve os bytes da r1
assert t2.replace("TGLExt.TheIdentityHasAName_r1", "TGLExt.TheIdentityHasAName").encode("utf-8") == b

man = {}
agg = hashlib.sha256()
src_dir = KB + "/TGLExt"
for raiz, dirs, files in os.walk(src_dir, followlinks=False):
    dirs.sort()
    for f in sorted(files):
        if not f.endswith(".olean"):
            continue
        s = os.path.join(raiz, f)
        rel = "TGLExt/" + os.path.relpath(s, src_dir).replace(os.sep, "/")
        d = os.path.join(OV, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copyfile(s, d)
        a, c = sha(s), sha(d)
        assert a == c, rel
        man[rel] = a
        agg.update((rel + "|" + a + "\n").encode())
s = KB + "/TGLExt.olean"
shutil.copyfile(s, OV + "/TGLExt.olean")
a, c = sha(s), sha(OV + "/TGLExt.olean")
assert a == c
man["TGLExt.olean"] = a
agg.update(("TGLExt.olean|" + a + "\n").encode())
out = {"r1_origem": r1, "r1_copia": dst, "r1_copia_sha256": hashlib.sha256(t2.encode("utf-8")).hexdigest(),
       "troca": "TGLExt.TheIdentityHasAName -> TGLExt.TheIdentityHasAName_r1", "ocorrencias_trocadas": n_ocorr,
       "desfazer_a_troca_devolve_r1": True,
       "ov": OV, "ov_n_olean_copiados": len(man), "ov_agregado_sha256": agg.hexdigest(), "ov_arquivos": man}
json.dump(out, open(os.path.join(LOGS, "PREPARO_SANDBOX.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "ov_arquivos"}, ensure_ascii=False))
