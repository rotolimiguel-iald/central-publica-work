# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R2): B. pedra\<Nome>.lean (R2) contra pedra\antes_de_20261103_144624_r2\<Nome>.lean (R1).
Fora de comentarios/docstrings o texto tem de ser identico nas 5 alteradas; as 4 nao alteradas, bytes identicos.
Tambem: 9 embutidos no candidato == sandbox == pedra == BUNDLE (sha256). So le."""
import ast, difflib, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
SB = "C:/t/k407c/final/"
sha = lambda b: hashlib.sha256(b).hexdigest()

def strip_lean(s):
    """remove comentarios de linha (--), de bloco aninhado (/- -/, inclusive /-- e /-!) respeitando literais de string."""
    out = []; i = 0; n = len(s); depth = 0
    while i < n:
        c = s[i]
        if depth > 0:
            if s.startswith("/-", i): depth += 1; i += 2; continue
            if s.startswith("-/", i): depth -= 1; i += 2; continue
            i += 1; continue
        if s.startswith("/-", i): depth = 1; i += 2; continue
        if s.startswith("--", i):
            while i < n and s[i] != "\n": i += 1
            continue
        if c == '"':
            j = i + 1
            while j < n and s[j] != '"':
                j += 2 if s[j] == "\\" else 1
            out.append(s[i:j+1]); i = j + 1; continue
        out.append(c); i += 1
    return "".join(out)

def norm(s):
    t = strip_lean(s)
    return [ln.rstrip() for ln in t.replace("\r\n", "\n").split("\n") if ln.strip()]

BJ = json.load(open(R + "BUNDLE_v407.json", encoding="utf-8"))
def embutidos(p):
    s = open(p, "rb").read().decode("utf-8"); tr = ast.parse(s)
    for nd in tr.body:
        if isinstance(nd, ast.Assign) and isinstance(nd.targets[0], ast.Name) and nd.targets[0].id == "_EMBEDDED_KERNEL_FILES":
            return ast.literal_eval(nd.value)
E7 = embutidos(R + "um_v407_candidato.py")
mods = {b["rel"]: b for b in BJ["modulos"]}
res = {}
for rel, b in mods.items():
    nome = os.path.basename(rel)
    p2 = R + "pedra/" + nome; p1 = R + "pedra/antes_de_20261103_144624_r2/" + nome
    b2 = open(p2, "rb").read()
    emb = E7[rel].encode("utf-8"); sb = open(SB + rel, "rb").read()
    cad = (sha(emb) == sha(sb) == sha(b2) == b["sha256"]) and len(emb) == b["bytes"]
    if os.path.exists(p1):
        b1 = open(p1, "rb").read()
        n1, n2 = norm(b1.decode("utf-8")), norm(b2.decode("utf-8"))
        d = [l for l in difflib.unified_diff(n1, n2, "R1", "R2", lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
        raw = list(difflib.unified_diff(b1.decode("utf-8").split("\n"), b2.decode("utf-8").split("\n"), "R1", "R2", lineterm="", n=0))
        nraw = len([l for l in raw if l[:1] in "+-" and not l.startswith(("---", "+++"))])
        print(f"{nome:24s} ALTERADA   bytes R1 {len(b1)} R2 {len(b2)} | linhas brutas dif {nraw} | dif fora de comentarios: {len(d)} | embutido==sandbox==pedra==BUNDLE: {cad}")
        for l in d[:20]: print("      !!", l[:200])
        res[nome] = {"alterada": True, "dif_codigo": len(d), "cadeia_ok": cad, "sha16": sha(b2)[:16]}
    else:
        # nao alterada: comparar com origem normalizada? aqui: com a R1 do sandbox/pedra antiga se existir; senao com 'antes_de_20261103_144624_r2/sandbox'
        alt = R + "pedra/antes_de_20261103_144624_r2/sandbox/" + nome
        alt_ok = None
        if os.path.exists(alt): alt_ok = open(alt, "rb").read() == b2
        print(f"{nome:24s} NAO ALTERADA bytes {len(b2)} | identica a copia R1 em antes_*/sandbox: {alt_ok} | embutido==sandbox==pedra==BUNDLE: {cad}")
        res[nome] = {"alterada": False, "cadeia_ok": cad, "sha16": sha(b2)[:16], "igual_r1_sandbox": alt_ok}
json.dump(res, open(R + "revisao_terceiro/b2_pedra_r2_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
