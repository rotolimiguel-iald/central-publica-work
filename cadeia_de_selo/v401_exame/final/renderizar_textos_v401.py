# -*- coding: utf-8 -*-
"""renderizar_textos_v401.py -- exame final v401 (c1, 24/10/2026; molde: renderizar_textos_v399.py): renderiza TODAS as funcoes publicas de texto de textos_v401.py contra o NOS DO
SANDBOX sb7 (montado pelo harness do fechar sobre a MINHA copia do pacote, com --manter), importando as copias do sandbox de leitura_v401/textos_v401. Grava cada texto em
final\\textos_renderizados_v401\\<nome>.txt, para a varredura de citacao por bytes. Nada fora de v400_exame\\final e' escrito. uso: python -B -X utf8 renderizar_textos_v401.py <SB>"""
import inspect, json, os, sys, hashlib
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
SB = sys.argv[1]
PK = os.path.join(SB, "work", "cadeia_de_selo", "v401"); POS = os.path.join(PK, "pos_rito")
sys.path.insert(0, POS); sys.path.insert(0, PK)
import leitura_v401 as L  # noqa: E402
import textos_v401 as T  # noqa: E402
assert os.path.normcase(os.path.abspath(L.NOS)).startswith(os.path.normcase(os.path.abspath(SB))), "a leitura nao aponta para o Nos do sandbox: %s" % L.NOS
assert os.path.normcase(os.path.abspath(T.NOS)).startswith(os.path.normcase(os.path.abspath(SB))), "os textos nao apontam para o Nos do sandbox: %s" % T.NOS
V, PROB = L.ler()
OUT = os.path.join(H, "textos_renderizados_v401"); os.makedirs(OUT, exist_ok=True)
R = {"sandbox": SB, "nos_leitura": L.NOS, "nos_textos": T.NOS, "problemas_da_leitura": PROB, "textos": {}}
K = {"ap_nome": "?", "ap_sha": "?", "ap_ver": "?", "ap_evento": "?", "ap_bat": "?", "par_sha": "?", "rel_sha": "?", "rel_man": "?"}
K["readme_paragrafo"] = T.paragrafo_readme()[0]; K["readme_paragrafo_falsidade"] = T.paragrafo_falsidade()[0]
for nome, f in sorted(vars(T).items()):
    if nome.startswith("_") or not inspect.isfunction(f) or f.__module__ != T.__name__:
        continue
    ps = list(inspect.signature(f).parameters)
    try:
        if nome.startswith("verificar"):
            continue
        if nome.startswith("paragrafo"):
            r = f(); r = r[0] if isinstance(r, tuple) else r
        elif nome == "handoff":
            r = f(V, K)
        elif nome == "aviso":
            r = f(V, "REIVINDICACAO_DO_EXAME")
        elif ps == ["V"]:
            r = f(V)
        elif not ps:
            r = f()
        else:
            R["textos"][nome] = {"pulada": "assinatura %s" % ps}; continue
        if not isinstance(r, str):
            R["textos"][nome] = {"nao_texto": type(r).__name__}; continue
        open(os.path.join(OUT, nome + ".txt"), "w", encoding="utf-8", newline="\n").write(r)
        R["textos"][nome] = {"bytes": len(r.encode("utf-8")), "sha16": hashlib.sha256(r.encode("utf-8")).hexdigest()[:16]}
    except Exception as e:   # noqa: BLE001
        R["textos"][nome] = {"erro": repr(e)[:300]}
json.dump(R, open(os.path.join(H, "RENDER_TEXTOS_v401.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"problemas": PROB, "n_render": sum(1 for v in R["textos"].values() if "bytes" in v), "nao_renderizados": {k: v for k, v in R["textos"].items() if "bytes" not in v}}, ensure_ascii=False, indent=1))
