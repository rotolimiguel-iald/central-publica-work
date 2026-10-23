# -*- coding: utf-8 -*-
"""renderizar_textos_sb2.py -- exame final v397 (c1, 23/10/2026): renderiza TODAS as funcoes publicas de texto de textos_v397.py (as que a cadeia grava no Nos, na memoria,
no Atlas, no CORE, no Haja_Luz, nos topicos, no aviso e no handoff) contra o NOS DO SANDBOX sb2 (montado pelo harness do fechar sobre a MINHA copia do pacote 388cc374),
importando as copias do sandbox de leitura_v397/textos_v397 (as que o fechar do sandbox usa). Grava cada texto em final\\textos_renderizados_<suf>\\<nome>.txt, para a
varredura de citacao por bytes. Nada fora de v397_exame e' escrito; nada e' gravado em superficie alguma."""
import inspect, json, os, sys, hashlib
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
SB, SUF = sys.argv[1], sys.argv[2]
PK = os.path.join(SB, "work", "cadeia_de_selo", "v397"); POS = os.path.join(PK, "pos_rito")
sys.path.insert(0, POS); sys.path.insert(0, PK)
import leitura_v397 as L  # noqa: E402
import textos_v397 as T  # noqa: E402
assert os.path.normcase(os.path.abspath(L.NOS)).startswith(os.path.normcase(os.path.abspath(SB))), "a leitura nao aponta para o Nos do sandbox: %s" % L.NOS
assert os.path.normcase(os.path.abspath(T.NOS)).startswith(os.path.normcase(os.path.abspath(SB))), "os textos nao apontam para o Nos do sandbox: %s" % T.NOS
V, PROB = L.ler()
OUT = os.path.join(H, "textos_renderizados_%s" % SUF); os.makedirs(OUT, exist_ok=True)
R = {"sandbox": SB, "nos_leitura": L.NOS, "nos_textos": T.NOS, "problemas_da_leitura": PROB, "textos": {}}
K = {"readme_paragrafo": "(paragrafo)", "ap_nome": "?", "ap_sha": "?", "ap_ver": "?", "ap_evento": "?", "ap_bat": "?", "par_sha": "?", "rel_sha": "?", "rel_man": "?"}
for nome, f in sorted(vars(T).items()):
    if nome.startswith("_") or not inspect.isfunction(f) or f.__module__ != T.__name__:
        continue
    ps = list(inspect.signature(f).parameters)
    try:
        if nome == "verificar_paragrafo_readme":
            continue
        if nome == "paragrafo_readme":
            r = f(); r = r[0] if isinstance(r, tuple) else r
        elif nome == "handoff":
            par, _ = T.paragrafo_readme(); K["readme_paragrafo"] = par; r = f(V, K)
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
json.dump(R, open(os.path.join(H, "RENDER_TEXTOS_%s.json" % SUF), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:5000])
