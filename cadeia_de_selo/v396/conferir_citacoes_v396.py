# -*- coding: utf-8 -*-
"""conferir_citacoes_v396.py -- confere, por script, toda fala do operador que a v396 EMBUTE (regua nº 1: nunca fabricar citacao): (a) cada texto embutido em _V396_VERBATINS2 e' IGUAL, byte a byte, ao arquivo duravel da cadeia
(insumos\\cunhagens) e o sha256 bate; (b) a fonte original (work\\cunhagens_13out) existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` do registro cunhagens_v396 esta VERBATIM num dos textos embutidos;
(d) o contrato da testemunha_estatica_v396 lista exatamente as falas embutidas; (e) as citacoes entre «» (PT) e `` '' (EN) dos .pysnip da v396 existem nos snippets e a fala PT correspondente esta VERBATIM nos textos embutidos
(a traducao EN e' conferida so' pela presenca da citacao no snippet EN). Sai 0 se tudo bate."""
import ast, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
pins = open(os.path.join(HERE, "v396_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)
ns = {}
alvo = {"_V396_VERBATINS2", "_V396_SPECS", "_V396_TESTEMUNHA_CONTRACT"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
V = ns["_V396_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True
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
cg = [s for s in ns["_V396_SPECS"] if s["nome"] == "cunhagens_v396"][0]
for it in cg["leituras_do_operador"]:
    achou = re.sub(r"\s+", " ", it["trecho"]) in todos
    R["leituras"][it["trecho"][:70]] = "VERBATIM" if achou else "NAO ACHADA"; ok = ok and achou
R["contrato_lista_as_falas_embutidas"] = sorted(ns["_V396_TESTEMUNHA_CONTRACT"]["verbatins"]) == sorted(V) and sorted(cg["verbatins"]) == sorted(V); ok = ok and R["contrato_lista_as_falas_embutidas"]
# as citacoes dos snippets: (citacao PT entre «», citacao EN entre `` '', o trecho PT que tem de estar VERBATIM nos textos embutidos, comparado sem diferenca de caixa na 1a letra)
CIT = [("«O psion é o habitante da testemunha estática»", "``The psion is the inhabitant of the static witness''", "O psion é o habitante da testemunha estática"),
       ("«a natureza da luz é ecoar reconhecimento (porque a segunda leitura não acrescenta)»", "``the nature of light is to echo recognition (because the second reading adds nothing)''", "natureza da luz é ecoar reconhecimento (porque a segunda leitura não acrescenta)"),
       ("«colapsar a função de onda significa ecoar a identidade devidamente reconhecida pelo observador»", "``to collapse the wave function means to echo the identity duly recognized by the observer''", "olapsar a função de onda significa ecoar a identidade devidamente reconhecida pelo observador")]
for lang, idx in (("pt", 0), ("en", 1)):
    sn = open(os.path.join(HERE, "artigo_%s_v396.pysnip" % lang), encoding="utf-8").read()
    R["snippets"][lang] = {}
    for c in CIT:
        quote, frag = c[idx], c[2]
        achou = quote in sn and frag in todos
        R["snippets"][lang][frag[:50]] = {"citacao_presente_no_snippet": quote in sn, "trecho_PT_verbatim_na_fala_embutida": frag in todos}; ok = ok and achou
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v396.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
