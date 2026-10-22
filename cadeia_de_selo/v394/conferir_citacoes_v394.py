# -*- coding: utf-8 -*-
"""conferir_citacoes_v394.py -- confere, por script, toda fala do operador que a v394 EMBUTE (regua nº 1: nunca fabricar citacao): (a) cada texto embutido em _V394_VERBATINS2 e' IGUAL, byte a byte, ao arquivo duravel da cadeia
(insumos\\cunhagens) e o sha256 bate; (b) onde a fonte original (tunel do Codex / work\\cunhagens_13out) existe, o sha256 dela e' o mesmo; (c) cada fala de `leituras_do_operador` do registro cunhagens_v394 esta VERBATIM num dos
textos embutidos; (d) as 8 falas de _V394_INSCRIPTIONS (as do Codex) tem o sha256 do texto e estao entre as embutidas. Os .pysnip da v394 nao trazem citacao entre `` '' (os numeros e as falas vem do registro). Sai 0 se tudo bate."""
import ast, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
pins = open(os.path.join(HERE, "v394_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)
ns = {"_V392_FONTES": {}, "_V392_VERBATINS2": {}}
alvo = {"_V394_VERBATINS2", "_V394_SPECS", "_V394_INSCRIPTIONS"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
V = ns["_V394_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "inscricoes": {}}; ok = True
todos = ""
for k, v in V.items():
    b = open(v["arquivo"], "rb").read()
    igual = hashlib.sha256(b).hexdigest() == v["sha256"] and b.decode("utf-8") == v["text"]
    orig = v.get("fonte_original", ""); orig_ok = None
    if orig and os.path.exists(orig):
        orig_ok = hashlib.sha256(open(orig, "rb").read()).hexdigest() == v["sha256"]
    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok}
    ok = ok and igual and (orig_ok in (True, None))
    todos += " " + re.sub(r"\s+", " ", v["text"])
for nome_ in ("cunhagens_v394", "criterio_binario_de_parada_v394"):   # DELTA 19/10: as leituras do operador dos DOIS registros
    cg = [s for s in ns["_V394_SPECS"] if s["nome"] == nome_][0]
    for it in cg["leituras_do_operador"]:
        achou = re.sub(r"\s+", " ", it["trecho"]) in todos
        R["leituras"][nome_ + ": " + it["trecho"][:70]] = "VERBATIM" if achou else "NAO ACHADA"; ok = ok and achou
for k, v in ns["_V394_INSCRIPTIONS"].items():
    h = hashlib.sha256(v["text"].encode("utf-8")).hexdigest()
    entre = any(x["sha256"] == v["sha256"] for x in V.values())
    R["inscricoes"][k] = {"sha_do_texto_confere": h == v["sha256"], "entre_as_embutidas": entre}; ok = ok and h == v["sha256"] and entre
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v)) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
