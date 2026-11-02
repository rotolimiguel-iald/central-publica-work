# -*- coding: utf-8 -*-
import ast, re, sys, glob, os
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v405/"
src = open(R + "runtime_v405.py", encoding="utf-8").read()
t = ast.parse(src)
fn = [n for n in t.body if isinstance(n, ast.FunctionDef) and n.name == "_v405_guarda_frases"][0]
ns = {}
exec(compile(ast.Module([fn], []), "g", "exec"), ns)
g = ns["_v405_guarda_frases"]
pos = ["o gap é Δ", "o gap é `Δ`", "o gap é a energia retida", "Na unidade posta, o gap = β·u", "Δ é o gap", "`Δ` é gap", "energia retida é o gap", "o gap lido do ângulo de Miguel", "the gap is the retained energy", "Delta is the gap", "gap de 12,03 meV", "a escala e o tom ficam", "the scale and the key stay", "mantendo a escala e o tom"]
neg = ["`Δ` não é gap", "Δ não é gap: é 1/β vezes menor", "o gap é 83,1 vezes `Δ`", "the gap is 83.1 times Delta", "Delta is not a gap", "o gap espectral é u", "na unidade posta o gap vale u", "o gap com unidade", "gap_v405", "o valor esperado é Δ", "o lock tem gap espectral 1", "a escala fica"]
print("POS (tem de reprovar):")
for p in pos: print(" ", bool(g(p)), repr(p), [x[0] for x in g(p)][:2])
print("NEG (tem de passar):")
for p in neg: print(" ", not g(p), repr(p), [x[0] for x in g(p)][:2])
print("arquivos:")
for p in sorted(glob.glob(R + "pedra/*.lean")) + [R + x for x in ("artigo_pt_v405.pysnip", "artigo_en_v405.pysnip", "pos_rito/textos_v405_novo.pysnip", "A_IDENTIDADE_traducao_en_da_gerencia.txt")]:
    v = g(open(p, encoding="utf-8").read())
    print(os.path.basename(p), len(v), [(a, b[:70]) for a, b in v[:4]])
