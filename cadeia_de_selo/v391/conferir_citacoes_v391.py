# -*- coding: utf-8 -*-
"""conferir_citacoes_v391.py -- confere, por script, toda citacao entre `` e '' dos .pysnip PT e EN da v391 (a regua nº 1: nunca fabricar citacao):
 (a) as do OPERADOR estao VERBATIM no texto dele lido por sha256 (sem normalizacao alem de espacos); o EN cita as MESMAS do PT; os trechos pinados sao os citados;
 (b) as frases de EPOCA citadas na errata ao lado estao no proprio artigo v390 selado (o .txt emitido), comparadas sem as aspas internas;
 (c) no EN, as aspas dentro de «the management's translation: …» sao traducao DITA, contadas (tantas quantas as do operador) e nao conferidas como verbatim.
Sai 0 se tudo bate."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
PIN = "5dffde4644139da50bf82757f070e84c870833af4728b2194ed4ad8d3aa826bb"
b = open(os.path.join(HERE, "OPERADOR_07out_estatuto_verbatim.txt"), "rb").read(); assert hashlib.sha256(b).hexdigest() == PIN
OP = re.sub(r"\s+", " ", b.decode("utf-8"))
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[`']", "", s.replace("---", "—"))).strip()
TXT = {lg: norm(open(os.path.join(NOS, "um_absoluto_%s.txt" % lg), encoding="utf-8").read().replace("—", "---").replace("---", "—")) for lg in ("pt", "en")}
R = {"operador": {}, "epoca": {}, "traducao_en": []}; ok = True; por = {}
for lg in ("pt", "en"):
    src = open(os.path.join(HERE, "artigo_%s_v391.pysnip" % lg), encoding="utf-8").read()
    src = re.sub(r'"\s*\n\s*r"', "", src)   # junta os r"..." r"..." de uma mesma frase
    tr_a = src.find("the management's translation:") if lg == "en" else -1
    tr_b = src.find("'')", tr_a) + 3 if tr_a >= 0 else -1
    cits = [(m_.start(), re.sub(r"\s+", " ", m_.group(1))) for m_ in re.finditer(r"``(.*?)''", src, flags=re.S)]
    por[lg] = []
    for pos, c in cits:
        if lg == "en" and tr_a <= pos < tr_b:
            R["traducao_en"].append(c[:90]); continue
        if c in OP:
            por[lg].append(c); R["operador"]["%s: %s" % (lg, c[:90])] = "VERBATIM"
        else:
            achou = norm(c) in TXT[lg]
            R["epoca"]["%s: %s" % (lg, c[:90])] = "NO ARTIGO v390" if achou else "NAO ACHADA"
            ok = ok and achou
R["n_operador"] = {k: len(v) for k, v in por.items()}
R["en_cita_as_mesmas_do_pt"] = sorted(por["en"]) == sorted(por["pt"]); ok = ok and R["en_cita_as_mesmas_do_pt"] and len(por["pt"]) == 2
R["traducao_conta"] = len(R["traducao_en"]) == len(por["pt"]); ok = ok and R["traducao_conta"]
pins = open(os.path.join(HERE, "v391_pins.py"), encoding="utf-8").read()
R["trechos_pinados_todos_citados"] = all(c in re.sub(r"'\s*\n\s*'", "", pins).replace("\\'", "'") for c in por["pt"]); ok = ok and R["trechos_pinados_todos_citados"]
R["n_epoca"] = len(R["epoca"]); ok = ok and R["n_epoca"] == 16
R["ok"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v391.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
print("CITACOES (estrito):", "TODAS CONFEREM" if ok else "FALHOU")
sys.exit(0 if ok else 1)
