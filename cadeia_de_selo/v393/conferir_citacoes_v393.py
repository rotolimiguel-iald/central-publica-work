# -*- coding: utf-8 -*-
"""conferir_citacoes_v393.py -- confere, por script, toda citacao entre `` e '' dos .pysnip PT e EN da v393 (regua nº 1: nunca fabricar citacao): cada uma esta VERBATIM num dos 4 arquivos do
operador de 14/10 (lidos por sha256 contra os pinos embutidos). As quatro cunhagens entram nos .pysnip por _V393_CUNHAGENS (texto embutido), nao digitadas. Sai 0 se tudo bate."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
pins = open(os.path.join(HERE, "v393_pins.py"), encoding="utf-8").read(); ns = {}; exec(compile(pins, "<pins>", "exec"), ns)
OP = ""; R = {"operador": {}, "cunhagens": {}}; ok = True
for k, v in ns["_V393_CUNHAGENS"].items():
    b = open(v["arquivo_informativo"], "rb").read()
    igual = hashlib.sha256(b).hexdigest() == v["sha256"] and b.decode("utf-8") == v["text"]
    R["cunhagens"][k] = "EMBUTIDA_IGUAL_AO_ARQUIVO" if igual else "DIFERE"; ok = ok and igual
    OP += " " + re.sub(r"\s+", " ", b.decode("utf-8"))
for arq in ("artigo_pt_v393.pysnip", "artigo_en_v393.pysnip", "quadro_pt_v393.pysnip", "quadro_en_v393.pysnip"):
    src = open(os.path.join(HERE, arq), encoding="utf-8").read()
    src = re.sub(r'"\s*\n\s*r"', "", src)
    for m_ in re.finditer(r"``(.*?)''", src, flags=re.S):
        c = re.sub(r"\s+", " ", m_.group(1))
        if "_v393_tex" in c or "\" +" in c or "+ \"" in c:   # citacao montada em runtime a partir de _V393_CUNHAGENS (texto embutido)
            R["operador"]["%s: %s" % (arq, "(montada de _V393_CUNHAGENS)")] = "EMBUTIDA"; continue
        achou = c in OP
        R["operador"]["%s: %s" % (arq, c[:90])] = "VERBATIM" if achou else "NAO ACHADA"; ok = ok and achou
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v393.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
