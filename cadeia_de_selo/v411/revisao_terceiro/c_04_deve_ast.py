import sys, os, ast, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
src = rd(V + r"\conferir_rito_v411.py")
tree = ast.parse(src)
out = []
for n in tree.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("DEVE", "NAO"):
        name = n.targets[0].id
        for k, v in zip(n.value.keys, n.value.values):
            ks = ast.unparse(k)[:95]
            names = sorted({x.id for x in ast.walk(v) if isinstance(x, ast.Name)} - {"all", "any", "len", "set", "bool", "str", "sum", "sorted", "list", "dict", "isinstance", "abs", "int", "float", "True", "False", "None", "V", "J", "kf", "axr", "ESP", "DL", "core", "selo", "umsha", "sha", "txt", "n", "k_", "t_", "x_", "c_", "k", "v_"})
            out.append((name, n.value.keys.index(k) if False else None, ks, ast.get_source_segment(src, v)[:150].replace("\n", " "), names[:12], v.lineno))
for i, o in enumerate(out):
    print(o[0], o[5], "|", o[2], "|", ",".join(o[4]))
print(len(out))
