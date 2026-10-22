# -*- coding: utf-8 -*-
"""A3b -- compara FOLHA A FOLHA o RESULTADO_OPTICO.json do construtor (2_OPTICO) com o da copia do auditor.
Diferencas so podem estar em carimbos de tempo, duracao e caminhos (a copia vive noutra pasta)."""
import hashlib, json, os, re

U = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out\2_OPTICO\RESULTADO_OPTICO.json"
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(R2, "otico", "2_OPTICO", "RESULTADO_OPTICO.json")
OUT = os.path.join(R2, "saidas", "A3b_COMPARACAO_OTICO.json")


def folhas(x, pre=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from folhas(v, pre + "/" + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from folhas(v, pre + "[%d]" % i)
    else:
        yield pre, x


a = json.load(open(U, encoding="utf-8"))
b = json.load(open(M, encoding="utf-8"))
fa, fb = dict(folhas(a)), dict(folhas(b))
so_a = sorted(set(fa) - set(fb))
so_b = sorted(set(fb) - set(fa))
dif = [(k, fa[k], fb[k]) for k in sorted(set(fa) & set(fb)) if fa[k] != fb[k]]
ESPERADO = re.compile(r"(quando_local|quando_utc|duracao_s|caminho|/arquivo$|/arquivos/|/destino|/script$|/log$|"
                      r"conferencia_freeze|preservacao_rodada1|/fonte/|FREEZE_json/caminho|/sha256$|/bytes$)")
esperadas = [d for d in dif if ESPERADO.search(d[0])]
inesperadas = [d for d in dif if not ESPERADO.search(d[0])]
num_a = sum(1 for v in fa.values() if isinstance(v, (int, float)) and not isinstance(v, bool))
iguais_num = sum(1 for k, v in fa.items() if isinstance(v, (int, float)) and not isinstance(v, bool) and k in fb and fb[k] == v)
out = dict(construtor=dict(caminho=U, sha256=hashlib.sha256(open(U, "rb").read()).hexdigest()),
           auditor=dict(caminho=M, sha256=hashlib.sha256(open(M, "rb").read()).hexdigest()),
           n_folhas_construtor=len(fa), n_folhas_auditor=len(fb), so_no_construtor=so_a, so_no_auditor=so_b,
           n_diferencas=len(dif), n_esperadas=len(esperadas), inesperadas=[list(map(str, d)) for d in inesperadas],
           esperadas=[[d[0], str(d[1])[:120], str(d[2])[:120]] for d in esperadas],
           folhas_numericas_construtor=num_a, folhas_numericas_identicas=iguais_num,
           vereditos=dict(construtor={x["id"]: (x["face_O"], x["conforme_ao_esperado"]) for x in a["por_parte"]},
                          auditor={x["id"]: (x["face_O"], x["conforme_ao_esperado"]) for x in b["por_parte"]}),
           controles=dict(construtor={x["id"]: x["comportou_como_esperado"] for x in a["controles"]},
                          auditor={x["id"]: x["comportou_como_esperado"] for x in b["controles"]}))
out["vereditos_identicos"] = out["vereditos"]["construtor"] == out["vereditos"]["auditor"]
out["controles_identicos"] = out["controles"]["construtor"] == out["controles"]["auditor"]
with open(OUT, "x", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("esperadas", "vereditos", "controles")}, ensure_ascii=False, indent=1)[:6000])
print("esperadas (amostra):")
for d in out["esperadas"][:40]:
    print("  ", d[0][:110])
