# -*- coding: utf-8 -*-
# Auditor REPRO, item (3b): comparar, numero a numero, o RESULTADO_OPTICO.json do construtor com o da copia rodada
# na pasta do auditor. Campos volateis (horas, caminhos, tentativas, comparacao com tentativa anterior) sao listados a parte.
import os, sys, json, math

W = "C:\\IALD\\Central de Patentes\\work\\frequencia_defasa_12out\\"
AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(W + "2_OPTICO\\RESULTADO_OPTICO.json", encoding="utf-8"))
B = json.load(open(os.path.join(AUD, "repro_otico", "2_OPTICO", "RESULTADO_OPTICO.json"), encoding="utf-8"))
VOLATEIS = {"inicio_utc", "fim_utc", "tentativas_preservadas", "comparacao_com_tentativa_anterior", "caminho"}
dif, vol, n_folhas, n_num = [], [], [0], [0]


def walk(a, b, path):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            p = path + "/" + str(k)
            if k in VOLATEIS:
                if a.get(k) != b.get(k):
                    vol.append(p)
                continue
            if k not in a or k not in b:
                dif.append([p, "chave ausente em " + ("construtor" if k not in a else "auditor")])
                continue
            walk(a[k], b[k], p)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            dif.append([path, "listas de tamanhos diferentes %d vs %d" % (len(a), len(b))])
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, path + "[%d]" % i)
    else:
        n_folhas[0] += 1
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
            n_num[0] += 1
        if a != b:
            if isinstance(a, float) and isinstance(b, float) and (math.isnan(a) and math.isnan(b)):
                return
            dif.append([path, repr(a)[:200], repr(b)[:200]])


walk(A, B, "")
out = {"construtor_sha256": __import__("hashlib").sha256(open(W + "2_OPTICO\\RESULTADO_OPTICO.json", "rb").read()).hexdigest(),
       "auditor_sha256": __import__("hashlib").sha256(open(os.path.join(AUD, "repro_otico", "2_OPTICO", "RESULTADO_OPTICO.json"), "rb").read()).hexdigest(),
       "folhas_comparadas": n_folhas[0], "folhas_numericas": n_num[0], "diferencas": dif, "volateis_diferentes": vol}
# vereditos por parte lado a lado
va = {x["id"]: (x["veredito_O"], x["veredito_parte"]) for x in A["partes"]}
vb = {x["id"]: (x["veredito_O"], x["veredito_parte"]) for x in B["partes"]}
out["vereditos_por_parte_iguais"] = va == vb
out["vereditos"] = {k: [va[k], vb.get(k)] for k in va}
ca = {x["id"]: x["resultado"] for x in A["controles"]}
cb = {x["id"]: x["resultado"] for x in B["controles"]}
out["controles_iguais"] = ca == cb
out["controles"] = {k: [ca[k], cb.get(k)] for k in ca}
out["controles_ok"] = [A["controles_ok"], B["controles_ok"]]
out["beta_runtime"] = [A["beta_runtime"], B["beta_runtime"]]
SAIDA = os.path.join(AUD, "saidas", "A3b_COMPARACAO_OTICO.json")
open(SAIDA, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps({k: v for k, v in out.items() if k not in ("vereditos", "controles")}, ensure_ascii=False, indent=1)[:6000])
