"""Auditor de reproducao F1.TEMPO, rodada 2 -- item (3a): compara, folha a folha, o RESULTADO_OPTICO.json da copia do auditor com o
do construtor (rodada 2) e, por subitem, com o da rodada 1. Somente leitura na casa. Saida JSON em argv[1].
"""
import hashlib, json, os, sys

AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEU = os.path.join(AUD, "otico", "tentativas", "tentativa_001_ensaio", "RESULTADO_OPTICO.json")
MEU_AN = os.path.join(AUD, "otico", "tentativas", "tentativa_001_ensaio", "ACHADOS_FORA_DO_PREREGISTRO.json")
BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\2_OPTICO"
R2 = os.path.join(BASE, "rodada_2", "RESULTADO_OPTICO.json")
R2_AN = os.path.join(BASE, "rodada_2", "ACHADOS_FORA_DO_PREREGISTRO.json")
R1 = os.path.join(BASE, "RESULTADO_OPTICO.json")
ESPERADO_R2 = "bcc6177e0a46ca47357371f0e89258a2ae60dfb3708449f5a32e11364ba67c4b"
ESPERADO_R1_16 = "2c67b7ea6f118630"

IGNORAR = ("inicio_utc", "fim_utc", "segundos", "pasta_da_tentativa", "runner", "ambiente", "script_impressao_digital",
           "anexo_achados_fora_do_preregistro", "seconds", "taken_at")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def folhas(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from folhas(v, path + "/" + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from folhas(v, path + "[%d]" % i)
    else:
        yield path, x


def ignorado(p):
    return any(("/" + k) in p and (p.split("/" + k)[1] == "" or p.split("/" + k)[1][0] in "/[") for k in IGNORAR)


out = {"meu": {"arquivo": MEU, "sha256": sha(MEU)}, "construtor_r2": {"arquivo": R2, "sha256": sha(R2), "sha_confere_com_o_relatado": sha(R2) == ESPERADO_R2},
       "construtor_r1": {"arquivo": R1, "sha16": sha(R1)[:16], "confere": sha(R1)[:16] == ESPERADO_R1_16},
       "anexo": {"meu": sha(MEU_AN), "construtor_r2": sha(R2_AN), "identicos_bit_a_bit": sha(MEU_AN) == sha(R2_AN)}}
a = json.load(open(MEU, encoding="utf-8"))
b = json.load(open(R2, encoding="utf-8"))
fa = dict(folhas(a))
fb = dict(folhas(b))
so_a = sorted(set(fa) - set(fb))
so_b = sorted(set(fb) - set(fa))
dif, n_num, n_num_ig, n_outros, n_outros_ig = [], 0, 0, 0, 0
for p in sorted(set(fa) & set(fb)):
    if ignorado(p):
        continue
    va, vb = fa[p], fb[p]
    if isinstance(va, (int, float)) and not isinstance(va, bool):
        n_num += 1
        if va == vb and type(va) == type(vb):
            n_num_ig += 1
        else:
            dif.append((p, va, vb))
    else:
        n_outros += 1
        if va == vb:
            n_outros_ig += 1
        else:
            dif.append((p, str(va)[:200], str(vb)[:200]))
out["comparacao_folha_a_folha"] = {"folhas_numericas_comparadas": n_num, "numericas_identicas_bit_a_bit": n_num_ig,
                                   "outras_folhas_comparadas": n_outros, "outras_identicas": n_outros_ig,
                                   "diferencas": dif[:200], "n_diferencas": len(dif),
                                   "so_no_meu": so_a[:50], "so_no_construtor": so_b[:50]}
# por subitem e por afirmacao
sa, sb = a.get("subitens_oticos", {}), b.get("subitens_oticos", {})
out["subitens"] = {k: {"meu": sa[k]["resultado"], "construtor_r2": sb.get(k, {}).get("resultado"),
                       "fora_da_tolerancia_meu": sa[k]["criterios_fora_da_tolerancia"]} for k in sa}
out["controles"] = {k: {"meu": v["comportou_se_como_registrado"], "construtor_r2": b["controles_oticos"].get(k, {}).get("comportou_se_como_registrado")}
                    for k, v in a.get("controles_oticos", {}).items()}
out["por_afirmacao"] = {k: {"meu": v["resultado_da_face_otica"], "construtor_r2": b["por_afirmacao_face_otica"][k]["resultado_da_face_otica"],
                            "veredito_meu": v["veredito_da_afirmacao"]} for k, v in a["por_afirmacao_face_otica"].items()}
# rodada 1: so os resultados por subitem e o maximo do T9.o(c)
r1 = json.load(open(R1, encoding="utf-8"))


def achar_t9c(res):
    for c in res["subitens_oticos"]["T9.o"]["criterios"]:
        if c["nome"].startswith("(c) max_{1<=k<=10^4}"):
            return c
    return None


def achar_t9c_r1(res):
    s = res.get("subitens_oticos") or res.get("subitens") or {}
    t9 = s.get("T9.o") if isinstance(s, dict) else None
    return t9


out["T9o_c"] = {"meu": achar_t9c(a), "construtor_r2": achar_t9c(b)}
t9r1 = achar_t9c_r1(r1)
out["T9o_r1_resumo"] = (json.dumps(t9r1, ensure_ascii=False)[:1500] if t9r1 else "estrutura diferente na rodada 1: chaves %s" % list(r1.keys())[:40])
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
c = out["comparacao_folha_a_folha"]
print("R2 sha confere:", out["construtor_r2"]["sha_confere_com_o_relatado"], "| R1 confere:", out["construtor_r1"]["confere"], "| anexo identico:", out["anexo"]["identicos_bit_a_bit"])
print("numericas:", c["folhas_numericas_comparadas"], "identicas:", c["numericas_identicas_bit_a_bit"], "| outras:", c["outras_folhas_comparadas"], "identicas:", c["outras_identicas"], "| diferencas:", c["n_diferencas"])
for d in c["diferencas"][:40]:
    print("  DIF", d)
print("so no meu:", c["so_no_meu"][:10], "| so no construtor:", c["so_no_construtor"][:10])
print("subitens:", {k: (v["meu"], v["construtor_r2"]) for k, v in out["subitens"].items()})
print("controles:", {k: (v["meu"], v["construtor_r2"]) for k, v in out["controles"].items()})
print("T9.o(c) meu:", out["T9o_c"]["meu"]["medida"], out["T9o_c"]["meu"].get("k_do_max"), out["T9o_c"]["meu"].get("primeiro_k_acima_de_1e_13"))
print("T9.o(c) r2 :", out["T9o_c"]["construtor_r2"]["medida"], out["T9o_c"]["construtor_r2"].get("k_do_max"), out["T9o_c"]["construtor_r2"].get("primeiro_k_acima_de_1e_13"))
