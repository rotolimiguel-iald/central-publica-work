import ast, glob, os
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
rd = lambda p: open(p, "rb").read().decode("utf-8")
o = rd(glob.glob(os.path.join(V, "conferir_rito_v411.py.bak_*_r1fix"))[0])
n = rd(os.path.join(V, "conferir_rito_v411.py"))
for tag, s in (("antes", o), ("hoje", n)):
    t = ast.parse(s)
    achado = []
    for x in ast.walk(t):
        if isinstance(x, ast.Dict) and len(x.keys) > 60:
            ks = [k.value for k in x.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            achado.append((len(x.keys), sum(1 for k in ks if "registros por spec v411" in k), sum(1 for k in ks if "(C-02)" in k)))
    print(tag, "dicts grandes (n chaves, tem spec411, tem C-02):", achado)
