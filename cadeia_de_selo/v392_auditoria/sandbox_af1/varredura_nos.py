# Auditor c1: roda a varredura RECURSIVA do candidato v392 sobre o tgl_kernel REAL do Nos (so leitura) e sobre o conjunto embutido,
# para ver se arquivos soltos no Nos (nao embutidos) mudariam o resultado no rito.
import ast, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
CAND = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v392/um_v392_candidato.py"
NOSK = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel"
src = open(CAND, encoding="utf-8").read()
tree = ast.parse(src)
want = {"_lean_strip_comments_and_strings", "_lean_source_forbidden_tokens", "_LEAN_FORBIDDEN_TOKENS"}
ns = {"os": os, "re": __import__("re"), "FORMAL_DIR": NOSK}
emb_names = set()
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in want:
        exec(compile(ast.Module([node], []), "cand", "exec"), ns)
    elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in want for t in node.targets):
        exec(compile(ast.Module([node], []), "cand", "exec"), ns)
    elif isinstance(node, (ast.Assign, ast.AnnAssign)) and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in getattr(node, "targets", [getattr(node, "target", None)])):
        d = ast.literal_eval(node.value)
        emb_names = set(d.keys())
hits = ns["_lean_source_forbidden_tokens"]()
# arquivos .lean no Nos (TGL, TGLExt recursivo) que NAO estao no conjunto embutido do candidato
extra = []
for lab in ("TGL", "TGLExt"):
    base = os.path.join(NOSK, lab)
    for r, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith(".lean") and not f.startswith("Probe"):
                rel = lab + "/" + os.path.relpath(os.path.join(r, f), base).replace(os.sep, "/")
                if rel not in emb_names:
                    extra.append(rel)
print(json.dumps({"tokens": ns["_LEAN_FORBIDDEN_TOKENS"], "hits_no_Nos": hits, "n_embutidos": len(emb_names),
                  "lean_no_Nos_fora_do_embutido": sorted(extra)}, ensure_ascii=False, indent=1)[:4000])
