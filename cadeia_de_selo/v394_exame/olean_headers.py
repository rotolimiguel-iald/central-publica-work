# -*- coding: utf-8 -*-
# Exame final v394: le o cabecalho de .olean (so' leitura; nenhum lake roda). Todos os 191 novos (189 + raiz + Audit) do sandbox,
# uma amostra dos antigos do sandbox e uma amostra do Nos; mais os lean-toolchain. Escreve so' em v394_exame.
import os, json, random, re, sys
H = os.path.dirname(os.path.abspath(__file__))
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v394"
SB = r"C:\t\k394\final"; NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
GH_431 = "68218e876d2a38b1985b8590fff244a83c321783"
def hdr(p):
    b = open(p, "rb").read(96)
    if b[:5] != b"olean":
        return {"magic": False}
    ver = b[7:7 + 33].split(b"\0")[0].decode("ascii", "replace")
    m = re.search(rb"[0-9a-f]{40}", b)
    return {"magic": True, "fmt": list(b[5:7]), "versao": ver, "githash": m.group(0).decode() if m else None}
novos = json.load(open(os.path.join(V, "kernel_modulos_novos_v394.lista.json"), encoding="utf-8"))["novos"]
alvos = [r[:-5] + ".olean" for r in novos] + ["TGLExt.olean", "TGL/Audit.olean"]
lib = lambda root: os.path.join(root, ".lake", "build", "lib", "lean")
res = {"novos_sandbox": {}, "amostra_antigos_sandbox": {}, "amostra_nos": {}}
for rel in alvos:
    p = os.path.join(lib(SB), *rel.split("/"))
    res["novos_sandbox"][rel] = hdr(p) if os.path.exists(p) else {"ausente": True}
todos = []
for dp, dn, fn in os.walk(lib(SB)):
    for f in fn:
        if f.endswith(".olean"):
            todos.append(os.path.relpath(os.path.join(dp, f), lib(SB)).replace(os.sep, "/"))
random.seed(394)
antigos = [x for x in todos if x not in set(alvos)]
for rel in random.sample(antigos, min(300, len(antigos))):
    res["amostra_antigos_sandbox"][rel] = hdr(os.path.join(lib(SB), *rel.split("/")))
nos_todos = []
for dp, dn, fn in os.walk(lib(NOS)):
    for f in fn:
        if f.endswith(".olean"):
            nos_todos.append(os.path.relpath(os.path.join(dp, f), lib(NOS)).replace(os.sep, "/"))
for rel in random.sample(nos_todos, min(300, len(nos_todos))):
    res["amostra_nos"][rel] = hdr(os.path.join(lib(NOS), *rel.split("/")))
def resumo(d):
    vs = {}
    for v in d.values():
        k = "%s|%s" % (v.get("versao"), v.get("githash"))
        vs[k] = vs.get(k, 0) + 1
    return vs
pk = os.path.join(SB, ".lake", "packages")
mathlib_oleans = []
for dp, dn, fn in os.walk(pk):
    for f in fn:
        if f.endswith(".olean"):
            mathlib_oleans.append(os.path.join(dp, f))
    if len(mathlib_oleans) > 4000:
        break
random.shuffle(mathlib_oleans)
res["amostra_packages_sandbox"] = {os.path.relpath(p, pk): hdr(p) for p in mathlib_oleans[:100]}
R = {"n_novos": len(alvos), "novos": resumo(res["novos_sandbox"]), "n_olean_sandbox": len(todos), "antigos_amostra_300": resumo(res["amostra_antigos_sandbox"]),
     "n_olean_nos": len(nos_todos), "nos_amostra_300": resumo(res["amostra_nos"]), "packages_amostra_100": resumo(res["amostra_packages_sandbox"]),
     "githash_4_31_0_esperado": GH_431,
     "lean_toolchain": {"sandbox": open(os.path.join(SB, "lean-toolchain")).read().strip(), "nos": open(os.path.join(NOS, "lean-toolchain")).read().strip()},
     "ausentes_novos": [k for k, v in res["novos_sandbox"].items() if v.get("ausente")]}
json.dump(dict(R, detalhe=res), open(os.path.join(H, "OLEAN_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
