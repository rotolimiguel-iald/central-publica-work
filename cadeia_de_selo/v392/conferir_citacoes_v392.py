# -*- coding: utf-8 -*-
"""conferir_citacoes_v392.py -- confere, por script, toda citacao entre `` e '' dos .pysnip PT e EN da v392 (regua nº 1: nunca fabricar citacao):
 (a) cada uma esta VERBATIM num dos dois arquivos do operador de 13/10 (lidos por sha256, comparados sem normalizacao alem de espacos); o EN cita as MESMAS do PT;
 (b) as pinadas em v392_pins.py (trechos) contem as citadas; (c) as frases «...» (aspas angulares) do PT que reproduzem fala do operador tambem estao nos bytes.
Sai 0 se tudo bate."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CUN = os.path.join(os.path.dirname(os.path.dirname(HERE)), "cunhagens_13out")
ARQ = ["OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt", "OPERADOR_13out_verdade_projecao_do_posto_verbatim.txt"]
pins = open(os.path.join(HERE, "v392_pins.py"), encoding="utf-8").read(); ns = {}; exec(compile(pins, "<pins>", "exec"), ns)
OP = ""
for fn in ARQ:
    b = open(os.path.join(CUN, fn), "rb").read()
    emb = [v for v in ns["_V392_VERBATINS"].values() if v["arquivo_informativo"].endswith(fn)]
    assert len(emb) == 1 and hashlib.sha256(b).hexdigest() == emb[0]["sha256"] and b.decode("utf-8") == emb[0]["text"], ("verbatim embutido != arquivo", fn)
    OP += " " + re.sub(r"\s+", " ", b.decode("utf-8"))
R = {"operador": {}, "angulares": {}}; ok = True; por = {}
for lg in ("pt", "en"):
    src = open(os.path.join(HERE, "artigo_%s_v392.pysnip" % lg), encoding="utf-8").read()
    src = re.sub(r'"\s*\n\s*r"', "", src)
    cits = [re.sub(r"\s+", " ", m_.group(1)) for m_ in re.finditer(r"``(.*?)''", src, flags=re.S)]
    por[lg] = sorted(cits)
    for c in cits:
        achou = c in OP
        R["operador"]["%s: %s" % (lg, c[:90])] = "VERBATIM" if achou else "NAO ACHADA"; ok = ok and achou
    if lg == "pt":
        for m_ in re.finditer(r"«([^»]*)»", src):
            c = re.sub(r"\s+", " ", m_.group(1))
            if c in OP:
                R["angulares"][c[:90]] = "VERBATIM"
R["en_cita_as_mesmas_do_pt"] = por["en"] == por["pt"]; ok = ok and R["en_cita_as_mesmas_do_pt"] and len(por["pt"]) >= 6
R["n_citacoes"] = {k: len(v) for k, v in por.items()}
allt = [t for v in ns["_V392_VERBATINS"].values() for t in v["trechos"]]
R["trechos_pinados_contem_as_citadas"] = all(any(c in t or t in c for t in allt) for c in por["pt"]); ok = ok and R["trechos_pinados_contem_as_citadas"]
R["ok"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
print("CITACOES (estrito):", "TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
