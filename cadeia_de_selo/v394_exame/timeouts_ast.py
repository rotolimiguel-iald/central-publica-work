# -*- coding: utf-8 -*-
# Exame final v394: varre por AST o candidato e o um.py v393 (copia de bytes em v394\base_v393) atras de
# todo tempo-limite (timeout=..., run_process_checked(..., N), .wait(N), communicate(timeout=), join(N)).
# Compara v393 x v394. So' LE; escreve so' em v394_exame.
import ast, json, os, sys, hashlib
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v394"
H = os.path.dirname(os.path.abspath(__file__))
ALVOS = {"v394": os.path.join(V, "um_v394_candidato.py"), "v393": os.path.join(V, "base_v393", "um.py")}
def fname(f):
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return fname(f.value) + "." + f.attr
    return type(f).__name__
def src(node, text_lines):
    try:
        return ast.unparse(node)[:220]
    except Exception:
        return "?"
out = {}
for tag, p in ALVOS.items():
    b = open(p, "rb").read()
    tree = ast.parse(b.decode("utf-8"), filename=p)
    # mapa linha -> funcao
    funcs = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append((n.lineno, getattr(n, "end_lineno", n.lineno), n.name))
    def owner(ln):
        best = None
        for a, z, nm in funcs:
            if a <= ln <= z and (best is None or a > best[0]):
                best = (a, nm)
        return best[1] if best else "<modulo>"
    hits = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            fn = fname(n.func)
            kws = {k.arg: k.value for k in n.keywords if k.arg}
            hit = None
            if "timeout" in kws or "timeout_seconds" in kws:
                hit = src(kws.get("timeout", kws.get("timeout_seconds")), None)
            elif fn.endswith("run_process_checked") and len(n.args) >= 3:
                hit = src(n.args[2], None)
            elif fn.split(".")[-1] in ("wait", "join", "communicate") and n.args:
                hit = src(n.args[0], None)
            if hit is not None:
                hits.append({"linha": n.lineno, "funcao": owner(n.lineno), "chamada": fn, "limite": hit,
                             "cmd": src(n.args[0], None) if n.args else ""})
    out[tag] = {"sha16": hashlib.sha256(b).hexdigest()[:16], "n": len(hits), "hits": hits}
    del tree
# comparacao por (funcao, chamada, limite, cmd)
def chave(h):
    return (h["funcao"], h["chamada"], h["limite"], h["cmd"])
a = collections = None
s393 = {}
for h in out["v393"]["hits"]:
    s393.setdefault(chave(h), 0); s393[chave(h)] += 1
s394 = {}
for h in out["v394"]["hits"]:
    s394.setdefault(chave(h), 0); s394[chave(h)] += 1
so_394 = [list(k) + [v] for k, v in s394.items() if s393.get(k, 0) != v]
so_393 = [list(k) + [v] for k, v in s393.items() if s394.get(k, 0) != v]
R = {"v393_sha16": out["v393"]["sha16"], "v394_sha16": out["v394"]["sha16"], "n_v393": out["v393"]["n"], "n_v394": out["v394"]["n"],
     "diferentes_no_v394": so_394, "diferentes_no_v393": so_393, "v394_hits": out["v394"]["hits"]}
json.dump(R, open(os.path.join(H, "TIMEOUTS_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("v393", R["v393_sha16"], R["n_v393"], "| v394", R["v394_sha16"], R["n_v394"])
print("DIFERENTES v394:", json.dumps(so_394, ensure_ascii=False, indent=0)[:3000])
print("DIFERENTES v393:", json.dumps(so_393, ensure_ascii=False, indent=0)[:3000])
for h in out["v394"]["hits"]:
    print(h["linha"], h["funcao"], h["chamada"], "LIMITE=", h["limite"], "|", h["cmd"][:120])
