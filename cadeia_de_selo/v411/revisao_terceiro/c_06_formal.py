import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
root = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
files = {}
for dp, ds, names in os.walk(root):
    if ".lake" in dp.replace("\\", "/").split("/"): continue
    for nm in sorted(names):
        if nm == "ExtrairDeps.lean": continue
        if nm.endswith(".lean") or nm in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            p = os.path.join(dp, nm); rel = os.path.relpath(p, root).replace("\\", "/")
            files[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()
E = json.load(open(V + r"\ESPERADOS_v411.json", encoding="utf-8"))
print("entradas no Nos real agora:", len(files), "esperado", E["h8_entradas"], "residuais", E["h8_residuais_do_nos"], [r in files for r in E["h8_residuais_do_nos"]])
core = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
ff = core["kernel_formalization"]["formal_files_sha256"]
print("falso nos:", len(ff), "iguais ao Nos real:", sum(1 for k in ff if files.get(k) == ff[k]), "so no real:", [k for k in files if k not in ff][:5], "so no falso:", [k for k in ff if k not in files][:5])
# marcadores do kernel no Nos: a cadeia usa construir_marcas.txt (so' leitura de tempo)
