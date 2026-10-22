# -*- coding: utf-8 -*-
"""conferir_citacoes_v390.py -- confere, por script, que toda citacao do operador na v390 (os trechos entre `` e '' dos .pysnip PT e EN) esta VERBATIM num dos dois
textos do operador da ordem v390, lidos por sha256 (a regua nº 1: nunca fabricar citacao); o EN cita as MESMAS do PT; e os trechos pinados no gerador sao os mesmos.
Sem normalizacao alem de espacos. Sai 0 se tudo bate."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OD = os.path.join(os.path.dirname(HERE), "superposicao_passagem_07out")
TX = {}
for fn, pin in (("CUNHAGEM_OPERADOR_07out_verbatim.txt", "e2a915e23692f85cbd8815d14a80a40d10bef4e71396f33138dcb986064ca3a7"),
                ("CUNHAGEM_OPERADOR_07out_nomes_verbatim.txt", "0a9a5a98b3a3bd99242fb937ed234850ac0fa4c3c8904ac5144f34e99493a343"),
                ("CUNHAGEM_OPERADOR_07out_concordo_verbatim.txt", "d16bc8a7dc54962e102ed58b4c536411927e48d8ed574adb372febb94c3fdda7")):   # ADENDO 001
    b = open(os.path.join(OD, fn), "rb").read(); assert hashlib.sha256(b).hexdigest() == pin, fn
    TX[fn] = re.sub(r"\s+", " ", b.decode("utf-8"))
R = {"estrito": {}}; ok = True; por = {}
for lg in ("pt", "en"):
    src = open(os.path.join(HERE, "artigo_%s_v390.pysnip" % lg), encoding="utf-8").read()
    cits = [re.sub(r"\s+", " ", c) for c in re.findall(r"``(.*?)''", src, flags=re.S)]
    por[lg] = cits
    for c in cits:
        onde = [fn for fn, t in TX.items() if c in t]
        R["estrito"]["%s: %s" % (lg, c[:90])] = onde or "NAO ACHADA"; ok = ok and bool(onde)
R["n"] = {k: len(v) for k, v in por.items()}
R["en_cita_as_mesmas_do_pt"] = sorted(por["en"]) == sorted(por["pt"]); ok = ok and R["en_cita_as_mesmas_do_pt"] and R["n"]["pt"] > 0
pins = open(os.path.join(HERE, "v390_pins.py"), encoding="utf-8").read()
R["trechos_pinados_todos_citados"] = all(c in pins for c in por["pt"]); ok = ok and R["trechos_pinados_todos_citados"]
R["ok"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v390.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
print("CITACOES (estrito, contra os textos por sha256):", "TODAS VERBATIM" if ok else "FALHOU")
sys.exit(0 if ok else 1)
