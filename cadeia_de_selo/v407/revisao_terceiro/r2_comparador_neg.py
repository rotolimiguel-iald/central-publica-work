# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R2): o refinamento r_linked de comparar_v406_v407.py (C19+C19b), extraido por AST e executado sobre (a) base x candidato real; (b) base x candidato com o `reading` ao estilo R1 (so' o prefixo,
sem a linha inteira / sem ramificar); (c) reading adulterado (frase antiga trocada; ramificacao por True; prefixo sem a condicao). Espera: (a) tudo True; (b)/(c) algum False."""
import ast, copy, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
src = open(R + "comparar_v406_v407.py", encoding="utf-8").read(); tr = ast.parse(src)
want = {"dump_eq", "mascara", "pares", "r_linked"}
import copy, hashlib, json, os
ns = {"ast": ast, "copy": copy, "hashlib": hashlib, "json": json, "os": os}
for n in tr.body:
    if isinstance(n, ast.FunctionDef) and n.name in want:
        exec(compile(ast.Module([n], []), "cmp", "exec"), ns)
print("funcoes extraidas:", sorted(k for k in ns if k in want))
A = ast.parse(open(R + "base_v406/um.py", "rb").read().decode("utf-8")); B = ast.parse(open(R + "um_v407_candidato.py", "rb").read().decode("utf-8"))
fn = lambda T, nome: [n for n in T.body if isinstance(n, ast.FunctionDef) and n.name == nome][0]
ns["da"] = {"testemunha_estatica_v396": fn(A, "testemunha_estatica_v396")}
def rodar(rotulo, bfun):
    ns["db"] = {"testemunha_estatica_v396": bfun}
    try:
        r = ns["r_linked"]()
    except Exception as e:  # noqa: BLE001
        print("%-70s EXCECAO %r" % (rotulo, e)); return
    falsos = [k for k, v in r.items() if v is not True]
    print("%-70s -> %s" % (rotulo, "tudo True" if not falsos else "REPROVA em " + str(falsos)))
b0 = fn(B, "testemunha_estatica_v396")
rodar("(a) candidato real", b0)
def acha_reading(f):
    for nd in ast.walk(f):
        if isinstance(nd, ast.Dict):
            for i, k in enumerate(nd.keys):
                if isinstance(k, ast.Constant) and k.value == "reading": return nd, i
d0, i0 = acha_reading(b0)
def var(mut):
    f = copy.deepcopy(b0); d, i = acha_reading(f); mut(d, i); return f
# (b) R1: reading = so' o IfExp antigo (sem BinOp)
rodar("(b) reading igual ao da base (C19b ausente)", var(lambda d, i: d.values.__setitem__(i, copy.deepcopy(acha_reading(fn(A, "testemunha_estatica_v396"))[0].values[acha_reading(fn(A, "testemunha_estatica_v396"))[1]]))))
rodar("(c1) frase antiga adulterada no operando direito", var(lambda d, i: setattr(d.values[i].right.body, "value", "everything is proved") if isinstance(d.values[i].right.body, ast.Constant) else setattr(d.values[i].right.orelse, "value", "everything is proved")))
def troca_test(d, i): d.values[i].left.test = ast.Constant(True)
rodar("(c2) ramificacao do prefixo trocada por True", var(troca_test))
def troca_orelse(d, i): d.values[i].left.orelse = ast.Constant("PROVED")
rodar("(c3) ramo else do prefixo = 'PROVED' em vez de ''", var(troca_orelse))
def troca_op(d, i): d.values[i].op = ast.Sub() if False else ast.Mult()
rodar("(c4) operador trocado (+ -> *)", var(troca_op))
def prefixo_texto(d, i): d.values[i].left.body = ast.Constant("the Fock pair is proved")
rodar("(c5) texto do prefixo trocado (o comparador nao confere o texto; o ensaio confere)", var(prefixo_texto))
def chave_extra(d, i): d.keys.append(ast.Constant("extra")); d.values.append(ast.Constant(1))
rodar("(c6) chave nova extra no dict", var(chave_extra))
