# -*- coding: utf-8 -*-
"""conferir_citacoes_v395.py -- confere, por script, toda fala do operador que a v395 EMBUTE (regua nº 1: nunca fabricar citacao): (a) cada texto embutido em _V395_VERBATINS2 e' IGUAL, byte a byte, ao arquivo duravel da cadeia
(insumos\\cunhagens) e o sha256 bate; (b) a fonte original (work\\cunhagens_13out) existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` do registro cunhagens_v395 esta VERBATIM num dos textos embutidos;
(d) o contrato do psibit_v395 lista exatamente as falas embutidas; (e) os .pysnip da v395 nao trazem citacao entre `` '' alem das do registro («Eu prefiro que seja psibit» no EN/PT e' a fala; conferida contra o texto). Sai 0 se tudo bate."""
import ast, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
pins = open(os.path.join(HERE, "v395_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)
ns = {}
alvo = {"_V395_VERBATINS2", "_V395_SPECS", "_V395_PSIBIT_CONTRACT"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
V = ns["_V395_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True
todos = ""
for k, v in V.items():
    b = open(v["arquivo"], "rb").read()
    igual = hashlib.sha256(b).hexdigest() == v["sha256"] and b.decode("utf-8") == v["text"]
    orig = v.get("fonte_original", ""); orig_ok = None
    if orig and os.path.exists(orig):
        orig_ok = hashlib.sha256(open(orig, "rb").read()).hexdigest() == v["sha256"]
    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok}
    ok = ok and igual and (orig_ok is True)
    todos += " " + re.sub(r"\s+", " ", v["text"])
cg = [s for s in ns["_V395_SPECS"] if s["nome"] == "cunhagens_v395"][0]
for it in cg["leituras_do_operador"]:
    achou = re.sub(r"\s+", " ", it["trecho"]) in todos
    R["leituras"][it["trecho"][:70]] = "VERBATIM" if achou else "NAO ACHADA"; ok = ok and achou
R["contrato_lista_as_falas_embutidas"] = sorted(ns["_V395_PSIBIT_CONTRACT"]["verbatins"]) == sorted(V) and sorted(cg["verbatins"]) == sorted(V); ok = ok and R["contrato_lista_as_falas_embutidas"]
for lang, quote in (("pt", "«Eu prefiro que seja psibit»"), ("en", "``I prefer it to be psibit''")):
    sn = open(os.path.join(HERE, "artigo_%s_v395.pysnip" % lang), encoding="utf-8").read()
    achou = quote in sn and "Eu prefiro que seja psibit" in todos
    R["snippets"][lang] = {"citacao": quote, "presente_no_snippet": quote in sn, "fala_embutida_tem_o_trecho": "Eu prefiro que seja psibit" in todos}; ok = ok and achou
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v395.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
