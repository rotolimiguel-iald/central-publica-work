# -*- coding: utf-8 -*-
"""montar_registros_v392.py -- junta os specs dos registros v392 (V\\registros\\grupo_*.py, escritos por grupo) e GERA, por script, o codigo de pinos/dados que entra no um.py candidato:
  _V392_FONTES    : {chave: {arquivo, papel, sha256, bytes}}  -- sha256 e bytes LIDOS DO DISCO na geracao (nunca digitados); os registros os relem a cada rito (fail-closed);
  _V392_VERBATINS2: {chave: {arquivo, text (EMBUTIDO), sha256, bytes, trechos, quando}}  -- a fala do operador EMBUTIDA; cada trecho citado TEM de estar nos bytes do arquivo-fonte (assert);
  _V392_SPECS     : a lista dos specs (dados) interpretada pelo motor (registros_motor_v392.py);
  _V392_NOMES_REGISTROS.
Um grupo_*.py define: FONTES = [{"chave","arquivo","papel"}], VERBATINS = [{"chave","arquivo","trechos":[...],"quando"}], SPECS = [{...}] (ver registros\\SCHEMA.md).
Valida: nomes unicos; chaves referenciadas existem; arquivos existem e estao em pasta duravel (nada de scratchpad/AppData/Temp); todo texto novo passa a guarda P18; verbatim byte a byte.
Uso (import): from montar_registros_v392 import montar; codigo, info = montar()  |  CLI: python -I -B -X utf8 montar_registros_v392.py  -> grava registros_pins_v392.py e registros_info_v392.json"""
import glob, hashlib, importlib.util, json, os, pprint, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v392 as G  # noqa: E402
sha256 = lambda b: hashlib.sha256(b).hexdigest()
PROIBIDOS_CAMINHO = re.compile(r"scratchpad|AppData|[\\/]Temp[\\/]|[\\/]tmp[\\/]|C:[\\/]t[\\/]", re.I)
REQ = ("nome", "veredito_prefixo", "veredito_sufixo")


def carregar_grupos(filtro=None):
    grupos = []
    for p in sorted(glob.glob(os.path.join(HERE, "registros", "grupo_*.py"))):
        if filtro and filtro not in os.path.basename(p):
            continue
        spec = importlib.util.spec_from_file_location("v392_" + os.path.basename(p)[:-3], p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        grupos.append((os.path.basename(p), m))
    return grupos


def montar(filtro=None):
    fontes, verb, specs, origem = {}, {}, [], {}
    for nome_g, m in carregar_grupos(filtro):
        for f in getattr(m, "FONTES", []):
            assert set(f) >= {"chave", "arquivo", "papel"}, (nome_g, f)
            assert not PROIBIDOS_CAMINHO.search(f["arquivo"]), ("fonte em pasta nao duravel", f["arquivo"])
            b = open(f["arquivo"], "rb").read()
            novo = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
            assert fontes.get(f["chave"], novo) == novo, ("chave de fonte repetida com conteudo diferente", f["chave"])
            fontes[f["chave"]] = novo
        for v in getattr(m, "VERBATINS", []):
            assert set(v) >= {"chave", "arquivo", "trechos"}, (nome_g, v)
            b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
            for tr in v["trechos"]:
                assert tr in t, ("trecho NAO verbatim nos bytes do arquivo", v["chave"], tr)
            novo = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", "")}
            assert verb.get(v["chave"], novo) == novo, ("chave de verbatim repetida com conteudo diferente", v["chave"])
            verb[v["chave"]] = novo
        for s in getattr(m, "SPECS", []):
            assert all(k in s for k in REQ), (nome_g, s.get("nome"), "faltam campos obrigatorios", REQ)
            assert s["nome"] not in origem, ("registro repetido", s["nome"], origem.get(s["nome"]))
            assert s["nome"].endswith("_v392") or s["nome"] == "final_step_name_adopted_v392", s["nome"]
            origem[s["nome"]] = nome_g; specs.append(s)
    for s in specs:
        for ch in s.get("fontes", []):
            assert ch in fontes, (s["nome"], "fonte nao declarada", ch)
        for ch in s.get("verbatins", []):
            assert ch in verb, (s["nome"], "verbatim nao declarado", ch)
        for ck in s.get("checks", []):
            assert set(ck) >= {"id", "descricao", "onde", "caminho", "op"}, (s["nome"], ck)
            if ck["onde"].startswith("fonte:"):
                assert ck["onde"].split(":", 1)[1] in fontes, (s["nome"], "fonte do check nao declarada", ck["onde"])
        corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
        v = G.violacoes(corpo)
        assert not v, (s["nome"], "texto novo fere a guarda P18", v[:3])
    nomes = [s["nome"] for s in specs]
    codigo = ("# ====================== v392 (13/10/2026) -- OS REGISTROS POR SPEC: fontes pinadas por sha256 (lidas do disco por montar_registros_v392.py), verbatins EMBUTIDOS, specs ======================\n"
              "_V392_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n"
              "_V392_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n"
              "_V392_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
              "_V392_NOMES_REGISTROS = " + repr(nomes) + "\n")
    ns = {}; exec(compile(codigo, "<registros_pins>", "exec"), ns)
    assert ns["_V392_FONTES"] == fontes and ns["_V392_VERBATINS2"] == verb and ns["_V392_SPECS"] == specs
    info = {"n_registros": len(specs), "nomes": nomes, "origem": origem, "n_fontes": len(fontes), "n_verbatins": len(verb),
            "fontes": {k: {x: v[x] for x in ("arquivo", "sha256", "bytes", "papel")} for k, v in fontes.items()},
            "verbatins": {k: {x: v[x] for x in ("arquivo", "sha256", "bytes")} for k, v in verb.items()}}
    return codigo, info


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    codigo, info = montar()
    open(os.path.join(HERE, "registros_pins_v392.py"), "w", encoding="utf-8", newline="\n").write(codigo)
    json.dump(info, open(os.path.join(HERE, "registros_info_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("registros:", info["n_registros"], "fontes:", info["n_fontes"], "verbatins:", info["n_verbatins"]); print(info["nomes"])
