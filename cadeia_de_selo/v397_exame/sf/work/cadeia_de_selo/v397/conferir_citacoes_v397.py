# -*- coding: utf-8 -*-
"""conferir_citacoes_v397.py -- confere, por script, toda fala do operador que a v397 EMBUTE ou CITA (regua nº 1: nunca fabricar citacao): (a) cada texto embutido em _V397_VERBATINS2 e' IGUAL, byte a byte, ao arquivo duravel da
cadeia (insumos\\cunhagens) e o sha256 bate; (b) a fonte original (work\\cunhagens_13out) existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` dos registros cunhagens_v397 e teste_de_veracidade_fase9_v397 esta VERBATIM
num dos textos embutidos; (d) o registro de veracidade e as cunhagens listam exatamente as falas que usam; (e) as citacoes entre «» (PT) e `` '' (EN) dos .pysnip e do runtime do quadro existem nos snippets e a fala PT correspondente esta
VERBATIM nos textos embutidos; (f) a frase do operador do QUADRO (4,44) e' VERBATIM e a PARAFRASE da gerencia («o 5σ é o cala a boca; 4,44 é ...») NAO aparece em nenhum artefato (ela nao e' citacao); (g) as citacoes da pedra Token (as falas e a
linha do Atlas) existem verbatim nas falas embutidas / no Atlas. Sai 0 se tudo bate."""
import ast, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v397 as DL  # noqa: E402
pins = open(os.path.join(HERE, "v397_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)
ns = {}
alvo = {"_V397_VERBATINS2", "_V397_SPECS", "_V397_VERACIDADE_SPEC"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
V = ns["_V397_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}, "pedra": {}}; ok = True
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
R["n_falas_embutidas"] = len(V); ok = ok and len(V) == 4
cg = [s for s in ns["_V397_SPECS"] if s["nome"] == "cunhagens_v397"][0]; vr = ns["_V397_VERACIDADE_SPEC"]
for nome, spec in (("cunhagens_v397", cg), ("teste_de_veracidade_fase9_v397", vr)):
    for it in spec["leituras_do_operador"]:
        achou = re.sub(r"\s+", " ", it["trecho"]) in todos
        R["leituras"][nome + ": " + it["trecho"][:60]] = "VERBATIM" if achou else "NAO ACHADA"; ok = ok and achou
R["cunhagens_listam_as_quatro_falas"] = sorted(cg["verbatins"]) == sorted(V); ok = ok and R["cunhagens_listam_as_quatro_falas"]
R["veracidade_lista_as_tres_falas_que_usa"] = set(vr["verbatins"]) <= set(V) and len(vr["verbatins"]) == 3; ok = ok and R["veracidade_lista_as_tres_falas_que_usa"]
# as citacoes dos snippets: (citacao PT entre «», citacao EN entre `` '', o trecho PT que tem de estar VERBATIM nos textos embutidos)
CIT = [("«merece ser lido sobre uma face e relido sobre a outra»", "``merece ser lido sobre uma face e relido sobre a outra''", "merece ser lido sobre uma face e relido sobre a outra"),
       ("«o psion, o psibit, e é justamente ela que flutua sobre o abismo, o referente último»", "``o psion, o psibit, e é justamente ela que flutua sobre o abismo, o referente último''", "o psion, o psibit, e é justamente ela que flutua sobre o abismo, o referente último")]
for lang, idx in (("pt", 0), ("en", 1)):
    sn = open(os.path.join(HERE, "artigo_%s_v397.pysnip" % lang), encoding="utf-8").read()
    R["snippets"][lang] = {}
    for c in CIT:
        quote, frag = c[idx], c[2]
        achou = quote in sn and frag in todos
        R["snippets"][lang][frag[:50]] = {"citacao_presente_no_snippet": quote in sn, "trecho_PT_verbatim_na_fala_embutida": frag in todos}; ok = ok and achou
# (f) a frase do quadro e' VERBATIM e a parafrase da gerencia nao aparece
rq = open(os.path.join(HERE, "runtime_quadro_v397.py"), encoding="utf-8").read()
nsq = {}; exec(compile(rq, "<runtime_quadro_v397>", "exec"), nsq)
R["frase_do_quadro_verbatim_nas_falas"] = nsq["_V397_FRASE_444"] in todos and nsq["_V397_FRASE_444"] == DL.FRASE_DO_OPERADOR_4_44; ok = ok and R["frase_do_quadro_verbatim_nas_falas"]
PARAFRASE = "5σ é o cala a boca"   # «o 5σ é o cala a boca; 4,44 é um silêncio...» (parafrase da gerencia, NAO verbatim)
arts = ["runtime_quadro_v397.py", "artigo_pt_v397.pysnip", "artigo_en_v397.pysnip", "registros_v397.py", "gerar_candidato_v397.py", "pedra/Token.lean", "v397_pins.py"]
R["parafrase_da_gerencia_ausente"] = {a: (PARAFRASE not in open(os.path.join(HERE, *a.split("/")), encoding="utf-8").read()) for a in arts}; ok = ok and all(R["parafrase_da_gerencia_ausente"].values())
# (g) a pedra Token: as falas e a linha do Atlas
tok = open(DL.STONE_SRC, encoding="utf-8").read()
for q in ('O nome da pedra é "token"', DL.FRASE_DO_OPERADOR_PALAVRA):
    R["pedra"]["fala: " + q[:50]] = bool(("«" + q + "»") in tok and re.sub(r"\s+", " ", q) in todos); ok = ok and R["pedra"]["fala: " + q[:50]]
ATLAS = os.path.join(DL.WK, "..", "memory", "TGL_ATLAS.md")
atl = re.sub(r"\s+", " ", open(ATLAS, encoding="utf-8").read().replace("**", "")) if os.path.exists(ATLAS) else ""
linha_atlas = "No LLM: o token É o PsiBit — âncora do espaço de Hilbert"
R["pedra"]["linha_do_atlas_no_Atlas"] = linha_atlas in atl; R["pedra"]["linha_do_atlas_na_pedra"] = linha_atlas in tok.replace("«", "").replace("»", "")
ok = ok and R["pedra"]["linha_do_atlas_no_Atlas"] and R["pedra"]["linha_do_atlas_na_pedra"]
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
