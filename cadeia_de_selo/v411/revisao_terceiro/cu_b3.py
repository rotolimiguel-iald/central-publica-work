"""CU-B3: itens estruturais da D181: quadro do topo sem o item da fala do autor; linha da v411 no stdout; docstring; core cunhagens_v411; veredito; decisoes e erratas. Nao imprime texto de fala."""
import ast, hashlib, json, os, re, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sha256 = lambda b: hashlib.sha256(b).hexdigest()
OLD = os.path.join(V, "um_v411_candidato.py.bak_20261112_195053")
NEW = os.path.join(V, "um_v411_candidato.py")
rd = lambda p: open(p, "rb").read().decode("utf-8", errors="replace")
R = {}
# (a) o item antigo: pegar as funcoes do candidato antigo (so' codigo), ver o rotulo do item
so = rd(OLD)
t = ast.parse(so)
for n in t.body:
    if isinstance(n, ast.FunctionDef) and n.name in ("_v411_fala_do_autor_tex", "_v411_fala_do_autor_md"):
        seg = ast.get_source_segment(so, n)
        print("--- antigo", n.name, len(seg), "chars; linhas:", seg.count("\n") + 1)
        print(seg[:900])
topo = json.load(open(os.path.join(V, "TOPO_RATIFICADO_v411.json"), encoding="utf-8"))
print("TOPO keys:", list(topo.keys()))
print("TOPO tem fala_do_autor_para_o_quadro:", "fala_do_autor_para_o_quadro" in topo, "| ao_lado_d181_12nov:", [k for k in topo if "d181" in k])
bak = os.path.join(V, "TOPO_RATIFICADO_v411.json.bak_20261112_191215_d181")
tb = json.load(open(bak, encoding="utf-8"))
print("TOPO antigo keys que sumiram:", [k for k in tb if k not in topo], "| chaves novas:", [k for k in topo if k not in tb])
print("textos ratificados iguais (todas as outras chaves):", all(json.dumps(tb[k], sort_keys=True) == json.dumps(topo[k], sort_keys=True) for k in tb if k in topo and k != "ao_lado_d181_12nov"), [k for k in tb if k in topo and json.dumps(tb[k], sort_keys=True) != json.dumps(topo[k], sort_keys=True)])
