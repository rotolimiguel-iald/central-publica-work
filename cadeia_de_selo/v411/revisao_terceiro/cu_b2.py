"""CU-B2: controles do PROPRIO scan da D181 (positivos plantados) + contagens cruas da fala curta (17 chars) no candidato e na base."""
import re, sys, json, os, hashlib
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cu_b1.py"), encoding="utf-8").read()
cut = src.index("alvos = {}")
g = {"__name__": "cu_b1_defs"}
sys.stdout = open(os.devnull, "w")
exec(compile(src[:cut], "cu_b1_defs", "exec"), g)
sys.stdout = sys.__stdout__
varrer, falas, NEEDLES, toks, V, NOS, TOPO_WIN = g["varrer"], g["falas"], g["NEEDLES"], g["toks"], g["V"], g["NOS"], g["TOPO_WIN"]


def rd(p):
    return open(p, "rb").read().decode("utf-8", errors="replace")

R = {}


def resumo(r):
    return {"ocorrencias": len(r["ocorrencias"]), "nomes": len(r["nomes"]), "excedentes": r["n_janelas_excedentes"], "tipos": sorted({(o["tipo"], o["forma"]) for o in r["ocorrencias"]})[:6]}


# controle 1: o candidato ANTIGO (falas embutidas) tem de ser achado
old = rd(os.path.join(V, "um_v411_candidato.py.bak_20261112_195053"))
bsrc = rd(os.path.join(NOS, "um.py"))
r = varrer("candidato antigo (R1)", old, bsrc, None, TOPO_WIN)
R["C1_candidato_antigo_deve_ser_recusado"] = resumo(r)
r["janelas_excedentes"] = r["janelas_excedentes"][:3]
print("C1 candidato antigo:", R["C1_candidato_antigo_deve_ser_recusado"], "| falas distintas achadas (inteiro):", sorted({o["fala"] for o in r["ocorrencias"] if o["tipo"] == "inteiro"}))
sys.stdout.flush()
# controle 2: texto limpo + uma linha de fala plantada em cada forma
art = rd(r"C:\t\k411c\dry_v411\dry_v411_pt.txt")
base_art = rd(os.path.join(NOS, "um_absoluto_pt.txt"))
fala3 = [f for f in falas if f[0] == 3][0][3].strip()
lin = [l for l in re.split(r"(?<=[.!?])\s+", fala3) if len(l) >= 24][0]
for nome, txt in (("linha_crua", art + "\n" + lin + "\n"), ("linha_json_ascii", art + "\n" + json.dumps(lin, ensure_ascii=True)[1:-1]), ("linha_unicode_escape", art + "\n" + lin.encode("unicode_escape").decode("ascii")),
                  ("seis_palavras", art + "\n" + " ".join(lin.split()[:7]) + "\n"), ("nome_arquivo", art + "\n" + os.path.basename(falas[3][2]))):
    rr = varrer(nome, txt, base_art, None, TOPO_WIN)
    R["C2_" + nome] = resumo(rr)
    print("C2", nome, R["C2_" + nome])
rr = varrer("limpo", art, base_art, None, TOPO_WIN)
R["C3_limpo"] = resumo(rr)
print("C3 limpo:", R["C3_limpo"])
# contagem crua da fala curta (indice 10): raw e AST, candidato x base
f10 = [f for f in falas if f[0] == 10][0][3].strip()
import ast


def ast_strs(s):
    out = []
    for n in ast.walk(ast.parse(s)):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            out.append(n.value)
    return "\n".join(out)


csrc = rd(os.path.join(V, "um_v411_candidato.py"))
print("fala10 (len %d, sha16 %s) contagem crua: candidato raw %d | base raw %d | candidato AST %d | base AST %d" % (len(f10), hashlib.sha256(f10.encode()).hexdigest()[:16], csrc.count(f10), bsrc.count(f10), ast_strs(csrc).count(f10), ast_strs(bsrc).count(f10)))
# variantes de caixa/pontuacao da fala10
low = re.sub(r"\s+", " ", f10.lower())
print("fala10 em minusculas: candidato AST", ast_strs(csrc).lower().count(low), "| base AST", ast_strs(bsrc).lower().count(low))
json.dump(R, open(r"C:\t\k411c\revisao_CU\b2_controles.json", "w"), indent=1)
