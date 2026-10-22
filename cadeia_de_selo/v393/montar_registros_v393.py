# -*- coding: utf-8 -*-
"""montar_registros_v393.py -- le registros_v393.py (FONTES, VERBATINS, SPECS) e GERA, por script, o codigo de pinos/dados que entra no um.py candidato (sha256/bytes LIDOS DO DISCO, nunca digitados;
trechos dos verbatins conferidos NOS BYTES; texto novo passa pela guarda P18). Molde: montar_registros_v392.py (simplificado: um so' arquivo de dados)."""
import hashlib, json, os, pprint, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v393 as G  # noqa: E402
import registros_v393 as R  # noqa: E402
sha256 = lambda b: hashlib.sha256(b).hexdigest()
PROIBIDOS_CAMINHO = re.compile(r"scratchpad|AppData|[\\/]Temp[\\/]|[\\/]tmp[\\/]|C:[\\/]t[\\/]", re.I)
REQ = ("nome", "veredito_prefixo", "veredito_sufixo")


def montar():
    fontes, verb, specs = {}, {}, []
    for f in R.FONTES:
        assert set(f) >= {"chave", "arquivo", "papel"}, f
        assert not PROIBIDOS_CAMINHO.search(f["arquivo"]), ("fonte em pasta nao duravel", f["arquivo"])
        b = open(f["arquivo"], "rb").read()
        fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
    for v in R.VERBATINS:
        b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
        for tr in v["trechos"]:
            assert tr in t, ("trecho NAO verbatim nos bytes do arquivo", v["chave"], tr)
        verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", "")}
    for s in R.SPECS:
        assert all(k in s for k in REQ) and s["nome"].endswith("_v393"), s.get("nome")
        specs.append(s)
        for ch in s.get("fontes", []):
            assert ch in fontes, (s["nome"], ch)
        for ch in s.get("verbatins", []):
            assert ch in verb, (s["nome"], ch)
        corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
        v = G.violacoes(corpo)
        assert not v, (s["nome"], "texto novo fere a guarda P18", v[:3])
    nomes = [s["nome"] for s in specs]
    codigo = ("_V393_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n"
              "_V393_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n"
              "_V393_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
              "_V393_NOMES_REGISTROS = " + repr(nomes) + "\n"
              "_V392_FONTES.update(_V393_FONTES)   # v393: o motor de registros (v392) le as fontes e os verbatins das duas versoes\n"
              "_V392_VERBATINS2.update(_V393_VERBATINS2)\n")
    return codigo, {"n_registros": len(specs), "nomes": nomes, "n_fontes": len(fontes), "n_verbatins": len(verb),
                    "fontes": {k: {x: v[x] for x in ("arquivo", "sha256", "bytes", "papel")} for k, v in fontes.items()},
                    "verbatins": {k: {x: v[x] for x in ("arquivo", "sha256", "bytes")} for k, v in verb.items()}}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    c, info = montar()
    ns = {"_V392_FONTES": {}, "_V392_VERBATINS2": {}}; exec(compile(c, "<regs>", "exec"), ns)
    print(json.dumps({k: info[k] for k in ("n_registros", "nomes", "n_fontes", "n_verbatins")}, ensure_ascii=False))
